#!/usr/bin/env python3
"""Append-only, secret-averse trace helper for sectioned-development audits."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import subprocess
import sys
import uuid
from collections import Counter, defaultdict
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

SCHEMA_VERSION = 3
EVENT_FAMILIES = {'audit','invocation','requirements','planning','section','subsection','implementation','review','finding','repair','validation','integration','advisor','model','parallel','recovery','scope','branch','artifact','orchestration','feature'}
INVOCATION_SOURCES = {"USER_EXPLICIT", "CUSTOM_INSTRUCTIONS_AUTO", "AGENT_DISCRETION"}
INVOCATION_TIMINGS = {"FEATURE_START", "MID_FEATURE"}
KNOWN_EVENTS = {
    "audit_init",
    "skill_activation_announced",
    "auto_plan_approval_requested",
    "auto_plan_approved",
    "auto_plan_rejected",
    "late_trigger_detected",
    "branch_transition_selected",
    "agent_role_assigned",
    "orchestration_blocked",
    "sequence_gate_violation",
    "agent_work_tracking_checked",
    "branch_decision",
    "requirements_frozen",
    "user_requirement",
    "user_correction",
    "plan_frozen",
    "plan_review_dispatched",
    "plan_review_completed",
    "section_started",
    "implementation_completed",
    "implementation_amended",
    "review_dispatched",
    "review_completed",
    "review_cancelled",
    "finding_admitted",
    "finding_rejected",
    "finding_reopened",
    "repair_completed",
    "repair_delta_verified",
    "final_review_completed",
    "validation_completed",
    "scope_change",
    "owner_decision",
    "hard_cap",
    "recovery_completed",
    "recovery_delta_verified",
    "functional_head",
    "feature_completed",
    "audit_note",
    "audit_pack_started",
    "audit_pack_failed",
    "audit_pack_generated",
}


class TraceError(RuntimeError):
    pass


@dataclass(frozen=True)
class ValidationReport:
    errors: list[str]
    warnings: list[str]

    @property
    def telemetry_status(self) -> str:
        if self.errors:
            return "INVALID"
        if self.warnings:
            return "DEGRADED"
        return "VALID"


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
    root = Path(run_git(repo, "rev-parse", "--show-toplevel").decode().strip()).resolve()
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


def parse_records_text(text: str) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for lineno, raw in enumerate(text.splitlines(), start=1):
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


def read_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise TraceError(f"trace does not exist: {path}")
    return parse_records_text(path.read_text(encoding="utf-8"))


def validate_records(records: list[dict[str, Any]]) -> ValidationReport:
    errors: list[str] = []
    warnings: list[str] = []
    if not records:
        return ValidationReport(["trace is empty"], [])
    if records[0].get("event") != "audit_init":
        errors.append("first event must be audit_init")

    feature_id = records[0].get("feature_id")
    if not feature_id:
        errors.append("audit_init missing feature_id")
    seen_record_ids: set[str] = set()
    sequences: list[int] = []
    for index, record in enumerate(records, start=1):
        sequence = record.get("sequence")
        if isinstance(sequence, int) and sequence > 0:
            sequences.append(sequence)
        else:
            warnings.append(f"record {index} has invalid/missing sequence: {sequence!r}")
        event = record.get("event")
        if not isinstance(event, str) or not event:
            errors.append(f"record {index} missing event")
        elif event not in KNOWN_EVENTS and record.get('event_family') not in EVENT_FAMILIES:
            warnings.append(f"record {index} has unknown event: {event!r}")
        for required in ("timestamp_utc", "phase", "summary"):
            if not record.get(required):
                errors.append(f"record {index} missing {required}")
        if record.get("feature_id") != feature_id:
            errors.append(f"record {index} feature_id differs from audit_init")
        record_id = record.get("record_id")
        if not record_id:
            warnings.append(f"record {index} missing record_id (legacy trace)")
        elif record_id in seen_record_ids:
            warnings.append(f"duplicate record_id at record {index}: {record_id}")
        else:
            seen_record_ids.add(str(record_id))

    if sequences:
        expected = list(range(min(sequences), min(sequences) + len(sequences)))
        if sequences != expected:
            warnings.append(f"sequence gap/duplication: observed={sequences!r}")
        if sequences[0] != 1:
            warnings.append(f"first sequence is {sequences[0]}, expected 1")

    init = records[0]
    if init.get("invocation_source") not in INVOCATION_SOURCES:
        errors.append("audit_init has invalid invocation_source")
    if init.get("invocation_timing") not in INVOCATION_TIMINGS:
        errors.append("audit_init has invalid invocation_timing")
    if not init.get("trigger_evidence"):
        errors.append("audit_init missing trigger_evidence")
    if not init.get("audit_enabled_by"):
        errors.append("audit_init missing audit_enabled_by")
    return ValidationReport(errors, warnings)


@contextmanager
def trace_lock(path: Path) -> Iterator[None]:
    lock_path = path.with_name(path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def append_record_locked(path: Path, record: dict[str, Any], *, create: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "x" if create else "a"
    with path.open(mode, encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        handle.flush()


def command_init(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser()
    if args.invocation_source not in INVOCATION_SOURCES:
        raise TraceError(f"invalid invocation source: {args.invocation_source}")
    if args.invocation_timing not in INVOCATION_TIMINGS:
        raise TraceError(f"invalid invocation timing: {args.invocation_timing}")

    with trace_lock(path):
        if path.exists() and not args.force:
            raise TraceError(f"trace already exists: {path}; use --force to replace")
        if path.exists():
            path.unlink()
        record: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "record_id": str(uuid.uuid4()),
            "sequence": 1,
            "timestamp_utc": utc_now(),
            "event": "audit_init",
            "phase": "preflight",
            "summary": "Default-on live process audit initialized.",
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
        append_record_locked(path, record, create=True)
    print(path)
    return 0


def command_append(args: argparse.Namespace) -> int:
    path = Path(args.path).expanduser()
    if args.event == "audit_init":
        raise TraceError("audit_init can only be created with init")
    with trace_lock(path):
        records = read_records(path)
        report = validate_records(records)
        if report.errors:
            raise TraceError("existing trace is structurally invalid: " + "; ".join(report.errors))
        init = records[0]
        sequences = [r.get("sequence") for r in records if isinstance(r.get("sequence"), int)]
        next_sequence = (max(sequences) if sequences else 0) + 1
        record: dict[str, Any] = {
            "schema_version": SCHEMA_VERSION,
            "record_id": str(uuid.uuid4()),
            "sequence": next_sequence,
            "timestamp_utc": utc_now(),
            "event": args.event,
            "event_family": getattr(args, "family", None),
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
        append_record_locked(path, record)
    print(record["sequence"])
    return 0


def emit_validation(report: ValidationReport, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps({
            "telemetry_status": report.telemetry_status,
            "errors": report.errors,
            "warnings": report.warnings,
        }, ensure_ascii=False, indent=2, sort_keys=True))
        return
    for error in report.errors:
        print(f"ERROR: {error}", file=sys.stderr)
    for warning in report.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    print(f"telemetry_status: {report.telemetry_status}")


def command_validate(args: argparse.Namespace) -> int:
    report = validate_records(read_records(Path(args.path).expanduser()))
    emit_validation(report, json_output=args.json)
    return 1 if report.errors else 0


def command_summary(args: argparse.Namespace) -> int:
    records = read_records(Path(args.path).expanduser())
    report = validate_records(records)
    if report.errors:
        raise TraceError("trace is structurally invalid: " + "; ".join(report.errors))

    events = Counter(str(record.get("event")) for record in records)
    phases = Counter(str(record.get("phase")) for record in records)
    results = Counter((record["result"] if isinstance(record["result"], str) else str(record["result"].get("status", "STRUCTURED")) if isinstance(record["result"], dict) else "STRUCTURED") for record in records if record.get("result"))
    validations: dict[tuple[str, str], int] = defaultdict(int)
    for record in records:
        if record.get("event") != "validation_completed":
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
        "schema_version": SCHEMA_VERSION,
        "feature_id": init.get("feature_id"),
        "skill_version": init.get("skill_version"),
        "invocation_source": init.get("invocation_source"),
        "invocation_timing": init.get("invocation_timing"),
        "telemetry_status": report.telemetry_status,
        "telemetry_warnings": report.warnings,
        "record_count": len(records),
        "events": dict(sorted(events.items())),
        "phases": dict(sorted(phases.items())),
        "results": dict(sorted(results.items())),
        "duplicate_successful_validation_groups": duplicate_validation_groups,
        "first_timestamp_utc": records[0].get("timestamp_utc"),
        "last_timestamp_utc": records[-1].get("timestamp_utc"),
        "last_git_head": records[-1].get("git_head"),
        "last_tracked_diff_sha256": records[-1].get("tracked_diff_sha256"),
    }
    text = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        out = Path(args.output).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(out)
    else:
        print(text, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="create a new default-on live audit trace")
    init.add_argument("path")
    init.add_argument("--feature-id", required=True)
    init.add_argument("--skill-version", required=True)
    init.add_argument("--invocation-source", required=True)
    init.add_argument("--invocation-timing", required=True)
    init.add_argument("--trigger-evidence", required=True)
    init.add_argument("--audit-enabled-by", default="SKILL_DEFAULT_LIVE")
    init.add_argument("--feature-base", required=True)
    init.add_argument("--repo", default=".")
    init.add_argument("--field", action="append", default=[])
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=command_init)

    append = sub.add_parser("append", help="append one major audit event")
    append.add_argument("path")
    append.add_argument("--event", required=True)
    append.add_argument("--family", choices=sorted(EVENT_FAMILIES))
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

    validate = sub.add_parser("validate", help="validate trace and classify telemetry")
    validate.add_argument("path")
    validate.add_argument("--json", action="store_true")
    validate.set_defaults(func=command_validate)

    summary = sub.add_parser("summary", help="summarize events and duplicate validations")
    summary.add_argument("path")
    summary.add_argument("--output")
    summary.set_defaults(func=command_summary)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except TraceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
