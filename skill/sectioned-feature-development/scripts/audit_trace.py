#!/usr/bin/env python3
"""Append-only, secret-averse trace helper for optional sectioned-development audits."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INVOCATION_SOURCES = {
    "USER_EXPLICIT",
    "CUSTOM_INSTRUCTIONS_AUTO",
    "AGENT_DISCRETION",
}
INVOCATION_TIMINGS = {"FEATURE_START", "MID_FEATURE"}
EVENTS = {
    "audit_init",
    "user_requirement",
    "user_correction",
    "plan_frozen",
    "plan_review_dispatched",
    "plan_review_completed",
    "section_started",
    "implementation_completed",
    "review_dispatched",
    "review_completed",
    "review_cancelled",
    "finding_admitted",
    "finding_rejected",
    "repair_completed",
    "validation_completed",
    "scope_change",
    "owner_decision",
    "hard_cap",
    "recovery_completed",
    "functional_head",
    "feature_completed",
    "audit_note",
    "audit_pack_generated",
}


class TraceError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_git(repo: Path, *args: str, allow_failure: bool = False) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0 and not allow_failure:
        raise TraceError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.decode(errors='replace').strip()}"
        )
    return proc.stdout if proc.returncode == 0 else b""


def git_snapshot(repo_arg: str | None) -> dict[str, Any]:
    if not repo_arg:
        return {
            "repo_root": None,
            "git_branch": None,
            "git_head": None,
            "tracked_diff_sha256": None,
            "status_sha256": None,
        }

    repo = Path(repo_arg).expanduser().resolve()
    root_raw = run_git(repo, "rev-parse", "--show-toplevel")
    root = Path(root_raw.decode().strip()).resolve()
    head = run_git(root, "rev-parse", "HEAD").decode().strip()
    branch = run_git(root, "branch", "--show-current", allow_failure=True).decode().strip() or None
    diff = run_git(root, "diff", "--binary", "HEAD", "--")
    status = run_git(root, "status", "--porcelain=v1", "-z")
    return {
        "repo_root": str(root),
        "git_branch": branch,
        "git_head": head,
        "tracked_diff_sha256": sha256_bytes(diff),
        "status_sha256": sha256_bytes(status),
    }


def parse_fields(items: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise TraceError(f"--field must use key=value: {item!r}")
        key, value = item.split("=", 1)
        key = key.strip()
        if not key:
            raise TraceError("--field key cannot be empty")
        if key in result:
            raise TraceError(f"duplicate --field key: {key}")
        result[key] = value
    return result


def read_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise TraceError(f"trace does not exist: {path}")
    records: list[dict[str, Any]] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise TraceError(f"invalid JSON at line {lineno}: {exc}") from exc
        if not isinstance(obj, dict):
            raise TraceError(f"line {lineno} is not a JSON object")
        records.append(obj)
    return records


def validate_records(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    if not records:
        return ["trace is empty"]
    if records[0].get("event") != "audit_init":
        errors.append("first event must be audit_init")

    feature_id = records[0].get("feature_id")
    for index, record in enumerate(records, start=1):
        if record.get("sequence") != index:
            errors.append(
                f"sequence mismatch at record {index}: got {record.get('sequence')!r}"
            )
        event = record.get("event")
        if event not in EVENTS:
            errors.append(f"record {index} has unknown event: {event!r}")
        for required in ("timestamp_utc", "phase", "summary"):
            if not record.get(required):
                errors.append(f"record {index} missing {required}")
        if record.get("feature_id") != feature_id:
            errors.append(f"record {index} feature_id differs from audit_init")

    init = records[0]
    if init.get("invocation_source") not in INVOCATION_SOURCES:
        errors.append("audit_init has invalid invocation_source")
    if init.get("invocation_timing") not in INVOCATION_TIMINGS:
        errors.append("audit_init has invalid invocation_timing")
    if not init.get("trigger_evidence"):
        errors.append("audit_init missing trigger_evidence")
    if not init.get("audit_enabled_by"):
        errors.append("audit_init missing audit_enabled_by")
    return errors


def write_record(path: Path, record: dict[str, Any], *, create: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "x" if create else "a"
    with path.open(mode, encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def command_init(args: argparse.Namespace) -> int:
    path = Path(args.path)
    if path.exists() and not args.force:
        raise TraceError(f"trace already exists: {path}; use --force to replace")
    if path.exists() and args.force:
        path.unlink()
    if args.invocation_source not in INVOCATION_SOURCES:
        raise TraceError(f"invalid invocation source: {args.invocation_source}")
    if args.invocation_timing not in INVOCATION_TIMINGS:
        raise TraceError(f"invalid invocation timing: {args.invocation_timing}")

    record: dict[str, Any] = {
        "schema_version": 1,
        "sequence": 1,
        "timestamp_utc": utc_now(),
        "event": "audit_init",
        "phase": "preflight",
        "summary": "Optional live process audit enabled by explicit user request.",
        "feature_id": args.feature_id,
        "skill_version": args.skill_version,
        "invocation_source": args.invocation_source,
        "invocation_timing": args.invocation_timing,
        "trigger_evidence": args.trigger_evidence,
        "audit_enabled_by": args.audit_enabled_by,
        "feature_base": args.feature_base,
        "capture_mode": "LIVE",
        "fields": parse_fields(args.field),
        **git_snapshot(args.repo),
    }
    write_record(path, record, create=True)
    print(path)
    return 0


def command_append(args: argparse.Namespace) -> int:
    path = Path(args.path)
    records = read_records(path)
    errors = validate_records(records)
    if errors:
        raise TraceError("existing trace is invalid: " + "; ".join(errors))
    if args.event not in EVENTS - {"audit_init"}:
        raise TraceError(f"invalid append event: {args.event}")

    init = records[0]
    record: dict[str, Any] = {
        "schema_version": 1,
        "sequence": len(records) + 1,
        "timestamp_utc": utc_now(),
        "event": args.event,
        "phase": args.phase,
        "summary": args.summary,
        "feature_id": init["feature_id"],
        "actor": args.actor,
        "profile": args.profile,
        "result": args.result,
        "duration_ms": args.duration_ms,
        "capture_mode": args.capture_mode,
        "fields": parse_fields(args.field),
        **git_snapshot(args.repo),
    }
    write_record(path, record)
    print(record["sequence"])
    return 0


def command_validate(args: argparse.Namespace) -> int:
    records = read_records(Path(args.path))
    errors = validate_records(records)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"valid: {len(records)} records")
    return 0


def command_summary(args: argparse.Namespace) -> int:
    records = read_records(Path(args.path))
    errors = validate_records(records)
    if errors:
        raise TraceError("trace is invalid: " + "; ".join(errors))

    events = Counter(record["event"] for record in records)
    phases = Counter(record["phase"] for record in records)
    results = Counter(record.get("result") for record in records if record.get("result"))
    validations: dict[tuple[str, str], int] = defaultdict(int)
    for record in records:
        if record["event"] != "validation_completed":
            continue
        fields = record.get("fields") or {}
        family = str(fields.get("command_family", "UNKNOWN"))
        fingerprint = str(record.get("tracked_diff_sha256") or "UNKNOWN")
        if record.get("result") in {"PASS", "CLEAN", "SUCCESS"}:
            validations[(family, fingerprint)] += 1

    duplicate_validation_groups = [
        {"command_family": family, "tracked_diff_sha256": fp, "count": count}
        for (family, fp), count in sorted(validations.items())
        if count > 1
    ]
    init = records[0]
    summary = {
        "schema_version": 1,
        "feature_id": init["feature_id"],
        "skill_version": init.get("skill_version"),
        "invocation_source": init.get("invocation_source"),
        "invocation_timing": init.get("invocation_timing"),
        "record_count": len(records),
        "events": dict(sorted(events.items())),
        "phases": dict(sorted(phases.items())),
        "results": dict(sorted(results.items())),
        "duplicate_successful_validation_groups": duplicate_validation_groups,
        "first_timestamp_utc": records[0]["timestamp_utc"],
        "last_timestamp_utc": records[-1]["timestamp_utc"],
        "last_git_head": records[-1].get("git_head"),
        "last_tracked_diff_sha256": records[-1].get("tracked_diff_sha256"),
    }
    text = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(out)
    else:
        print(text, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create a new live audit trace")
    init.add_argument("path")
    init.add_argument("--feature-id", required=True)
    init.add_argument("--skill-version", required=True)
    init.add_argument("--invocation-source", required=True)
    init.add_argument("--invocation-timing", required=True)
    init.add_argument("--trigger-evidence", required=True)
    init.add_argument("--audit-enabled-by", required=True)
    init.add_argument("--feature-base", required=True)
    init.add_argument("--repo", default=".")
    init.add_argument("--field", action="append", default=[])
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=command_init)

    append = sub.add_parser("append", help="append one major audit event")
    append.add_argument("path")
    append.add_argument("--event", required=True)
    append.add_argument("--phase", required=True)
    append.add_argument("--summary", required=True)
    append.add_argument("--repo", default=".")
    append.add_argument("--actor", default="main")
    append.add_argument("--profile", default=None)
    append.add_argument("--result", default=None)
    append.add_argument("--duration-ms", type=int, default=None)
    append.add_argument("--capture-mode", choices=["LIVE", "RECONSTRUCTED"], default="LIVE")
    append.add_argument("--field", action="append", default=[])
    append.set_defaults(func=command_append)

    validate = sub.add_parser("validate", help="validate trace structure")
    validate.add_argument("path")
    validate.set_defaults(func=command_validate)

    summary = sub.add_parser("summary", help="summarize event and duplicate-validation counts")
    summary.add_argument("path")
    summary.add_argument("--output")
    summary.set_defaults(func=command_summary)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except TraceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
