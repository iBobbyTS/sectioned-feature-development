#!/usr/bin/env python3
"""Validate review-admission records and compute section review convergence.

The format is intentionally Markdown-first: humans and agents can inspect it, while
this script enforces the fields that keep review candidates from silently becoming
requirements.
"""

from __future__ import annotations

import argparse
import glob
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

CLASSES = {
    "IN_SCOPE_REPAIR",
    "IN_SCOPE_REPLAN",
    "OWNER_DECISION",
    "EVIDENCE_FAILURE",
    "DEFERRED_OWNER",
    "SCOPE_PROPOSAL",
    "UNSUPPORTED_HYPOTHESIS",
    "NIT_DEBT",
}
MATERIAL = {"IN_SCOPE_REPAIR", "IN_SCOPE_REPLAN", "OWNER_DECISION"}
NON_BLOCKING = {
    "DEFERRED_OWNER",
    "SCOPE_PROPOSAL",
    "UNSUPPORTED_HYPOTHESIS",
    "NIT_DEBT",
}
RESULTS = {"CLEAN", "MATERIAL_FINDINGS", "OWNER_DECISION", "EVIDENCE_FAILURE"}
BOUNDARIES = {
    "inside-section",
    "cross-section",
    "owner-decision",
    "evidence-only",
    "deferred",
    "new-scope",
    "none",
}
FINDING_RE = re.compile(
    r"<!--\s*FINDING:([A-Za-z0-9_.-]+):START\s*-->(.*?)"
    r"<!--\s*FINDING:\1:END\s*-->",
    re.DOTALL | re.IGNORECASE,
)
FIELD_RE = re.compile(r"(?mi)^-\s*([^:\n]+):\s*(.*?)\s*$")


@dataclass(frozen=True)
class Finding:
    finding_id: str
    fields: dict[str, str]


@dataclass(frozen=True)
class Admission:
    path: Path
    mode: str
    section: str
    counting_round: int | None
    attempt: int
    valid: bool
    result: str
    clean: bool
    streak: int
    findings: tuple[Finding, ...]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"admission file not found: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"admission file is not UTF-8: {path}") from exc


def _clean(value: str) -> str:
    value = value.strip().strip("`").strip()
    return value


def _top_fields(text: str) -> dict[str, str]:
    prefix = text.split("## Candidate Decisions", 1)[0]
    return {k.strip(): _clean(v) for k, v in FIELD_RE.findall(prefix)}


def _finding_fields(body: str) -> dict[str, str]:
    return {k.strip(): _clean(v) for k, v in FIELD_RE.findall(body)}


def _required(fields: dict[str, str], name: str, errors: list[str], where: str) -> str:
    value = fields.get(name, "")
    if not value:
        errors.append(f"{where}: missing field '{name}'")
    return value


def _is_none(value: str) -> bool:
    return value.lower() in {"", "none", "n/a", "—", "-"}


def parse_admission(path: Path) -> Admission:
    text = _read(path)
    errors: list[str] = []
    top = _top_fields(text)

    mode = _required(top, "Mode", errors, str(path)).upper()
    section = _required(top, "Section", errors, str(path))
    round_raw = _required(top, "Counting round", errors, str(path))
    attempt_raw = _required(top, "Review attempt", errors, str(path))
    valid_raw = _required(top, "Evidence-valid conclusion", errors, str(path)).lower()
    result = _required(top, "Result", errors, str(path)).upper()
    clean_raw = _required(top, "Clean admission", errors, str(path)).lower()
    streak_raw = _required(top, "Clean streak after", errors, str(path))

    if mode not in {"SECTION", "INTEGRATION"}:
        errors.append(f"{path}: Mode must be SECTION or INTEGRATION")

    counting_round: int | None
    if round_raw.upper() == "N/A":
        counting_round = None
    else:
        try:
            counting_round = int(round_raw)
            if not 1 <= counting_round <= 5:
                errors.append(f"{path}: Counting round must be 1..5 or N/A")
        except ValueError:
            counting_round = None
            errors.append(f"{path}: invalid Counting round: {round_raw!r}")

    try:
        attempt = int(attempt_raw)
        if attempt < 1:
            raise ValueError
    except ValueError:
        attempt = 0
        errors.append(f"{path}: Review attempt must be a positive integer")

    if valid_raw not in {"yes", "no"}:
        errors.append(f"{path}: Evidence-valid conclusion must be yes or no")
    valid = valid_raw == "yes"

    if result not in RESULTS:
        errors.append(f"{path}: invalid Result {result!r}")

    if clean_raw not in {"yes", "no"}:
        errors.append(f"{path}: Clean admission must be yes or no")
    clean = clean_raw == "yes"

    try:
        streak = int(streak_raw)
        if not 0 <= streak <= 2:
            raise ValueError
    except ValueError:
        streak = -1
        errors.append(f"{path}: Clean streak after must be 0..2")

    findings: list[Finding] = []
    seen: set[str] = set()
    for match in FINDING_RE.finditer(text):
        finding_id = match.group(1).upper()
        fields = _finding_fields(match.group(2))
        where = f"{path}:{finding_id}"
        if finding_id in seen:
            errors.append(f"{path}: duplicate finding ID {finding_id}")
        seen.add(finding_id)

        cls = _required(fields, "Admission class", errors, where).upper()
        domain = _required(fields, "Domain", errors, where).lower()
        boundary = _required(fields, "Boundary effect", errors, where).lower()
        if cls not in CLASSES:
            errors.append(f"{where}: invalid Admission class {cls!r}")
        if boundary not in BOUNDARIES:
            errors.append(f"{where}: invalid Boundary effect {boundary!r}")

        if cls in MATERIAL | {"EVIDENCE_FAILURE"}:
            for field in (
                "Contract/repository anchor",
                "Reachable supported trigger",
                "Material consequence",
                "Evidence / falsifiable path",
                "Smallest correct remedy",
                "Decision rationale",
            ):
                value = _required(fields, field, errors, where)
                if _is_none(value):
                    errors.append(f"{where}: '{field}' cannot be none for {cls}")

        expected_boundary = {
            "IN_SCOPE_REPAIR": "inside-section",
            "IN_SCOPE_REPLAN": "cross-section",
            "OWNER_DECISION": "owner-decision",
            "EVIDENCE_FAILURE": "evidence-only",
            "DEFERRED_OWNER": "deferred",
            "SCOPE_PROPOSAL": "new-scope",
            "UNSUPPORTED_HYPOTHESIS": "none",
            "NIT_DEBT": "none",
        }.get(cls)
        if expected_boundary and boundary != expected_boundary:
            errors.append(
                f"{where}: {cls} requires Boundary effect {expected_boundary!r}"
            )

        if cls == "DEFERRED_OWNER":
            owner = _required(fields, "Named deferred owner", errors, where)
            if _is_none(owner):
                errors.append(f"{where}: DEFERRED_OWNER needs a named section")

        if domain == "security" and cls not in {"NIT_DEBT"}:
            for field in (
                "Security asset",
                "Security actor and capability",
                "Security entry point / data flow",
                "Security trust boundary and preconditions",
                "Supported deployment context",
            ):
                value = _required(fields, field, errors, where)
                if cls in MATERIAL | {"OWNER_DECISION"} and _is_none(value):
                    errors.append(f"{where}: security field '{field}' cannot be N/A")

        scope_record = fields.get("Scope-change record", "")
        if cls == "SCOPE_PROPOSAL" and not _is_none(scope_record):
            # A proposal may name a record, but that record must not be described as
            # approved here; approval is a separate owner action.
            if "approved" in scope_record.lower():
                errors.append(
                    f"{where}: admission cannot self-approve a scope-change record"
                )

        findings.append(Finding(finding_id=finding_id, fields=fields))

    classes = {f.fields.get("Admission class", "").upper() for f in findings}
    material_ids = [f.finding_id for f in findings if f.fields.get("Admission class", "").upper() in MATERIAL]
    evidence_ids = [f.finding_id for f in findings if f.fields.get("Admission class", "").upper() == "EVIDENCE_FAILURE"]

    if result == "CLEAN":
        if material_ids or evidence_ids:
            errors.append(f"{path}: CLEAN cannot contain material/evidence-failure findings")
        if not valid or not clean:
            errors.append(f"{path}: CLEAN requires Evidence-valid conclusion=yes and Clean admission=yes")
    elif result == "MATERIAL_FINDINGS":
        if not material_ids:
            errors.append(f"{path}: MATERIAL_FINDINGS needs an admitted material finding")
        if clean:
            errors.append(f"{path}: MATERIAL_FINDINGS cannot be clean")
    elif result == "OWNER_DECISION":
        if "OWNER_DECISION" not in classes:
            errors.append(f"{path}: OWNER_DECISION result needs that admission class")
        if clean:
            errors.append(f"{path}: OWNER_DECISION cannot be clean")
    elif result == "EVIDENCE_FAILURE":
        if "EVIDENCE_FAILURE" not in classes:
            errors.append(f"{path}: EVIDENCE_FAILURE result needs that admission class")
        if valid or clean:
            errors.append(f"{path}: EVIDENCE_FAILURE must be invalid and non-clean")

    if mode == "SECTION" and counting_round is None:
        errors.append(f"{path}: completed SECTION review needs Counting round 1..5")
    if mode == "INTEGRATION" and counting_round is not None:
        errors.append(f"{path}: INTEGRATION Counting round should be N/A")
    if not valid and result != "EVIDENCE_FAILURE":
        errors.append(f"{path}: evidence-invalid full review must use Result EVIDENCE_FAILURE")

    if errors:
        raise ValueError("\n".join(f"- {e}" for e in errors))

    return Admission(
        path=path,
        mode=mode,
        section=section,
        counting_round=counting_round,
        attempt=attempt,
        valid=valid,
        result=result,
        clean=clean,
        streak=streak,
        findings=tuple(findings),
    )


def _expand_paths(values: Iterable[str]) -> list[Path]:
    paths: list[Path] = []
    for value in values:
        matches = [Path(p) for p in glob.glob(value)]
        paths.extend(matches or [Path(value)])
    # Preserve deterministic order while deduplicating.
    return sorted(dict.fromkeys(paths), key=lambda p: str(p))


def command_validate(args: argparse.Namespace) -> int:
    admission = parse_admission(Path(args.file))
    print(
        f"valid: {admission.path} mode={admission.mode} result={admission.result} "
        f"evidence_valid={str(admission.valid).lower()} clean={str(admission.clean).lower()} "
        f"findings={len(admission.findings)}"
    )
    return 0


def command_history(args: argparse.Namespace) -> int:
    paths = _expand_paths(args.files)
    if not paths:
        raise ValueError("no admission files matched")
    records = [parse_admission(path) for path in paths]
    sections = {r.section for r in records if r.mode == "SECTION"}
    if len(sections) != 1:
        raise ValueError(f"history must contain one SECTION, found: {sorted(sections)}")
    records = [r for r in records if r.mode == "SECTION"]
    records.sort(key=lambda r: (r.counting_round or 99, r.attempt, str(r.path)))

    rounds = [r.counting_round for r in records]
    if len(rounds) != len(set(rounds)):
        raise ValueError("history contains duplicate Counting round values")
    if rounds and rounds != list(range(1, max(rounds) + 1)):
        raise ValueError(f"Counting rounds must be contiguous from 1, got {rounds}")
    if len(records) > 5:
        raise ValueError("history contains more than five completed full reviews")

    streak = 0
    accepted = False
    for record in records:
        if record.valid and record.clean:
            streak += 1
        else:
            streak = 0
        expected = min(streak, 2)
        if record.streak != expected:
            raise ValueError(
                f"{record.path}: Clean streak after={record.streak}, expected {expected}"
            )
        if streak >= 2:
            accepted = True

    status = "SECTION_ACCEPTED" if accepted else (
        "HARD_CAP_RECOVERY" if len(records) == 5 else "CONTINUE"
    )
    print(f"section={next(iter(sections))}")
    print(f"completed_rounds={len(records)}")
    print(f"clean_streak={min(streak, 2)}")
    print(f"status={status}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate review admission records and convergence history."
    )
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate", help="validate one admission Markdown file")
    validate.add_argument("file")
    validate.set_defaults(func=command_validate)
    history = sub.add_parser("history", help="validate one section's admission history")
    history.add_argument("files", nargs="+")
    history.set_defaults(func=command_history)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(f"error:\n{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
