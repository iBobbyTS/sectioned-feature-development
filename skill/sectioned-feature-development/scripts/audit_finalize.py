#!/usr/bin/env python3
"""Validate and atomically publish one canonical sectioned-development audit pack."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import uuid
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

REQUIRED_FILES = {
    "00-README.md",
    "AUDIT-VERDICT.md",
    "HUMAN-REQUIREMENTS.md",
    "INVOCATION-AUDIT.md",
    "COUNTERFACTUAL-MINIMUM.md",
    "PLAN-AUDIT.md",
    "SCOPE-AUDIT.md",
    "REVIEW-AUDIT.md",
    "VALIDATION-AUDIT.md",
    "COST-METRICS.md",
    "SKILL-COMPLIANCE.md",
    "RECOMMENDATIONS.md",
    "requirements/REQUIREMENTS.md",
    "PROCESS-IDENTITY.json",
    "MODEL-TASK-AUDIT.md",
    "PARALLEL-AUDIT.md",
    "SUBSECTION-AUDIT.md",
    "ADVISOR-AUDIT.md",
}
PROCESS_KIND = "sectioned-development-process-audit"
EXCLUDED_GENERATED = {"PACK-METADATA.json", "PACK-MANIFEST.sha256"}
UNSAFE_PARTS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "dist", "build", "DerivedData", ".next",
}
UNSAFE_NAMES = {
    ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519",
    "cookies.json", "auth.json", "credentials.json",
}
PRIVATE_KEY_MARKERS = (
    b"-----BEGIN PRIVATE KEY-----",
    b"-----BEGIN RSA PRIVATE KEY-----",
    b"-----BEGIN OPENSSH PRIVATE KEY-----",
)
STATUS_PACK = {"COMPLETE", "COMPLETE_WITH_GAPS", "INCOMPLETE", "FAILED"}
STATUS_TELEMETRY = {"VALID", "DEGRADED", "INVALID"}
STATUS_EVIDENCE = {"CONSISTENT", "RESOLVABLE_DRIFT", "CONFLICTED"}


class PackError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sanitize_component(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    value = value.strip("-.")
    return value or "unknown"


def run_git(repo: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise PackError(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


@contextmanager
def exclusive_lock(path: Path) -> Iterator[None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def iter_pack_files(pack_dir: Path, *, include_generated: bool = False) -> list[Path]:
    files: list[Path] = []
    for path in sorted(pack_dir.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(pack_dir).as_posix()
        if not include_generated and rel in EXCLUDED_GENERATED:
            continue
        files.append(path)
    return files


def validate_pack_files(pack_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not pack_dir.is_dir():
        return [f"pack directory does not exist: {pack_dir}"], []
    present = {p.relative_to(pack_dir).as_posix() for p in iter_pack_files(pack_dir, include_generated=True)}
    for required in sorted(REQUIRED_FILES - present):
        errors.append(f"missing required file: {required}")
    if not any(p.startswith("git/") for p in present):
        errors.append("missing git evidence directory/files")
    if not any(p.startswith("sources/head/") for p in present):
        warnings.append("sources/head is empty or absent")
    if not any(p.startswith("planning/") for p in present):
        warnings.append("planning evidence is empty or absent")

    identity_path = pack_dir / "PROCESS-IDENTITY.json"
    if identity_path.exists():
        try:
            ident = json.loads(identity_path.read_text())
            if ident.get("kind") != PROCESS_KIND or ident.get("producer") != "sectioned-feature-development" or not ident.get("run_id"):
                errors.append("NOT_SFD_PROCESS_AUDIT")
        except (OSError, ValueError, AttributeError):
            errors.append("INVALID_PROCESS_IDENTITY")
    for path in iter_pack_files(pack_dir, include_generated=True):
        rel = path.relative_to(pack_dir)
        if path.is_symlink() or any(a.is_symlink() for a in path.parents if a != pack_dir.parent):
            errors.append(f"symlink evidence: {rel}")
        if path.suffix.lower()==".zip":errors.append(f"foreign nested audit/archive forbidden: {rel}")
        if any(part in UNSAFE_PARTS for part in rel.parts):
            errors.append(f"unsafe generated/build/cache path: {rel.as_posix()}")
        if path.name in UNSAFE_NAMES or path.name.startswith(".env."):
            errors.append(f"unsafe secret-like filename: {rel.as_posix()}")
        if path.suffix.lower() in {".p12", ".pfx", ".key", ".mobileprovision"}:
            errors.append(f"unsafe credential/key artifact: {rel.as_posix()}")
        if rel.parts and rel.parts[0] == "session" and path.suffix == ".jsonl":
            errors.append(f"raw session JSONL must be replaced by redacted derived evidence: {rel.as_posix()}")
        try:
            if path.stat().st_size <= 8 * 1024 * 1024:
                data = path.read_bytes()
                if any(marker in data for marker in PRIVATE_KEY_MARKERS):
                    errors.append(f"private-key marker found: {rel.as_posix()}")
        except OSError as exc:
            errors.append(f"cannot read {rel.as_posix()}: {exc}")
    return errors, warnings


def file_entries(pack_dir: Path, *, include_generated: bool = False) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for path in iter_pack_files(pack_dir, include_generated=include_generated):
        rel = path.relative_to(pack_dir).as_posix()
        entries.append({
            "path": rel,
            "sha256": sha256_file(path),
            "size": path.stat().st_size,
            "mode": stat.S_IMODE(path.stat().st_mode),
        })
    return entries


def fingerprint_entries(entries: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for entry in entries:
        digest.update(entry["path"].encode("utf-8"))
        digest.update(b"\0")
        digest.update(entry["sha256"].encode("ascii"))
        digest.update(b"\0")
        digest.update(str(entry["mode"]).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def load_trace_status(trace: Path | None) -> tuple[str, list[str]]:
    if trace is None or not trace.exists():
        return "DEGRADED", ["trace unavailable"]
    script = Path(__file__).with_name("audit_trace.py")
    proc = subprocess.run(
        [sys.executable, str(script), "validate", str(trace), "--json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if proc.returncode not in {0, 1}:
        return "INVALID", [proc.stderr.strip() or "trace validator failed"]
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return "INVALID", ["trace validator returned invalid JSON"]
    return str(payload.get("telemetry_status", "INVALID")), list(payload.get("warnings", [])) + list(payload.get("errors", []))


def canonical_paths(repo: Path, feature_id: str, product_head: str, desktop_root: Path) -> tuple[Path, Path]:
    del product_head  # identity is recorded in metadata; the path stays stable across bounded corrections
    repo_name = sanitize_component(repo.name)
    feature = sanitize_component(feature_id)
    desktop_root.mkdir(parents=True, exist_ok=True)
    zip_path = desktop_root / f"{repo_name}-{feature}-sectioned-audit.zip"
    return zip_path, zip_path.with_suffix(zip_path.suffix + ".sha256")


def write_metadata_and_manifest(
    pack_dir: Path,
    *,
    repo: Path,
    feature_id: str,
    feature_base: str,
    product_head: str,
    current_head: str,
    source_fingerprint: str,
    pack_status: str,
    telemetry_status: str,
    evidence_consistency: str,
) -> None:
    metadata = {
        "schema_version": 1,
        "kind": PROCESS_KIND,
        "producer": "sectioned-feature-development",
        "run_id": json.loads((pack_dir / "PROCESS-IDENTITY.json").read_text())["run_id"],
        "generated_at_utc": utc_now(),
        "repository": str(repo),
        "feature_id": feature_id,
        "feature_base": feature_base,
        "product_head": product_head,
        "current_head": current_head,
        "source_fingerprint": source_fingerprint,
        "pack_status": pack_status,
        "telemetry_status": telemetry_status,
        "evidence_consistency": evidence_consistency,
    }
    (pack_dir / "PACK-METADATA.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    entries = file_entries(pack_dir, include_generated=True)
    entries = [entry for entry in entries if entry["path"] != "PACK-MANIFEST.sha256"]
    lines = [f"{entry['sha256']}  {entry['path']}" for entry in entries]
    (pack_dir / "PACK-MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def deterministic_zip(pack_dir: Path, destination: Path) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in iter_pack_files(pack_dir, include_generated=True):
            rel = path.relative_to(pack_dir).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IMODE(path.stat().st_mode) & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes())


def verify_zip(zip_path: Path) -> list[str]:
    errors: list[str] = []
    if not zip_path.is_file():
        return [f"ZIP does not exist: {zip_path}"]
    with zipfile.ZipFile(zip_path, "r") as archive:
        names = set(archive.namelist())
        if "PACK-MANIFEST.sha256" not in names:
            return ["ZIP missing PACK-MANIFEST.sha256"]
        manifest = archive.read("PACK-MANIFEST.sha256").decode("utf-8")
        for line in manifest.splitlines():
            if not line.strip():
                continue
            expected, rel = line.split("  ", 1)
            if rel not in names:
                errors.append(f"manifest member missing from ZIP: {rel}")
                continue
            actual = hashlib.sha256(archive.read(rel)).hexdigest()
            if actual != expected:
                errors.append(f"manifest mismatch: {rel}")
        bad = archive.testzip()
        if bad:
            errors.append(f"ZIP CRC failure: {bad}")
    return errors


def write_state(
    state_path: Path,
    *,
    status: str,
    zip_path: Path | None,
    zip_sha256: str | None,
    source_fingerprint: str | None,
    errors: list[str],
    warnings: list[str],
) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "updated_at_utc": utc_now(),
        "status": status,
        "canonical_zip": str(zip_path) if zip_path else None,
        "zip_sha256": zip_sha256,
        "source_fingerprint": source_fingerprint,
        "errors": errors,
        "warnings": warnings,
    }
    temp = state_path.with_name(state_path.name + f".tmp-{uuid.uuid4().hex}")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temp, state_path)


def shared_preflight(args: argparse.Namespace) -> dict[str, Any]:
    repo = Path(args.repo).expanduser().resolve()
    pack_dir = Path(args.pack_dir).expanduser().resolve()
    trace = Path(args.trace).expanduser().resolve() if args.trace else None
    product_head = run_git(repo, "rev-parse", args.product_head)
    current_head = run_git(repo, "rev-parse", "HEAD")
    feature_base = run_git(repo, "rev-parse", args.feature_base) if args.feature_base else "UNKNOWN"
    errors, warnings = validate_pack_files(pack_dir)
    ident_path = pack_dir / "PROCESS-IDENTITY.json"
    if ident_path.exists():
        try:
            ident = json.loads(ident_path.read_text())
            if ident.get("feature_id") != args.feature_id or ident.get("source_head") != product_head or ident.get("feature_base") != feature_base:
                errors.append("PROCESS_IDENTITY_GIT_MISMATCH")
        except (OSError, ValueError, AttributeError):errors.append("INVALID_PROCESS_IDENTITY")
    telemetry_status, trace_messages = load_trace_status(trace)
    if telemetry_status == "INVALID":
        warnings.append("trace telemetry is INVALID; product evidence may still be independently consistent")
    warnings.extend(trace_messages)
    entries = file_entries(pack_dir, include_generated=False) if pack_dir.is_dir() else []
    evidence_fingerprint = fingerprint_entries(entries)
    identity = f"{feature_base}\0{product_head}\0{current_head}\0{evidence_fingerprint}".encode("utf-8")
    source_fingerprint = hashlib.sha256(identity).hexdigest()
    return {
        "repo": repo,
        "pack_dir": pack_dir,
        "trace": trace,
        "product_head": product_head,
        "current_head": current_head,
        "feature_base": feature_base,
        "errors": errors,
        "warnings": warnings,
        "telemetry_status": telemetry_status,
        "source_fingerprint": source_fingerprint,
    }


def command_check(args: argparse.Namespace) -> int:
    result = shared_preflight(args)
    payload = {
        "ok": not result["errors"],
        "pack_dir": str(result["pack_dir"]),
        "product_head": result["product_head"],
        "current_head": result["current_head"],
        "telemetry_status": result["telemetry_status"],
        "source_fingerprint": result["source_fingerprint"],
        "errors": result["errors"],
        "warnings": result["warnings"],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 1 if result["errors"] else 0


def command_finalize(args: argparse.Namespace) -> int:
    if args.pack_status not in STATUS_PACK:
        raise PackError(f"invalid pack status: {args.pack_status}")
    if args.evidence_consistency not in STATUS_EVIDENCE:
        raise PackError(f"invalid evidence consistency: {args.evidence_consistency}")
    result = shared_preflight(args)
    state_path = Path(args.state).expanduser() if args.state else Path(args.repo).expanduser() / ".agent-work" / "audit" / args.feature_id / "PACK-STATE.json"
    if result["errors"]:
        write_state(state_path, status="FAILED", zip_path=None, zip_sha256=None,
                    source_fingerprint=result["source_fingerprint"], errors=result["errors"], warnings=result["warnings"])
        raise PackError("preflight failed: " + "; ".join(result["errors"]))

    desktop_root = Path(args.desktop_root).expanduser().resolve()
    zip_path, sha_path = canonical_paths(result["repo"], args.feature_id, result["product_head"], desktop_root)
    lock_path = state_path.with_name("FINALIZE.lock")
    with exclusive_lock(lock_path):
        if state_path.exists() and zip_path.exists():
            try:
                existing = json.loads(state_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                existing = {}
            if (
                existing.get("status") == "COMPLETE"
                and existing.get("source_fingerprint") == result["source_fingerprint"]
                and existing.get("canonical_zip") == str(zip_path)
                and not verify_zip(zip_path)
            ):
                print(json.dumps({
                    "status": "COMPLETE",
                    "idempotent": True,
                    "canonical_zip": str(zip_path),
                    "sha256": sha256_file(zip_path),
                    "source_fingerprint": result["source_fingerprint"],
                }, indent=2, sort_keys=True))
                return 0

        telemetry = args.telemetry_status or result["telemetry_status"]
        if telemetry not in STATUS_TELEMETRY:
            raise PackError(f"invalid telemetry status: {telemetry}")
        write_metadata_and_manifest(
            result["pack_dir"],
            repo=result["repo"],
            feature_id=args.feature_id,
            feature_base=result["feature_base"],
            product_head=result["product_head"],
            current_head=result["current_head"],
            source_fingerprint=result["source_fingerprint"],
            pack_status=args.pack_status,
            telemetry_status=telemetry,
            evidence_consistency=args.evidence_consistency,
        )
        temp = desktop_root / f".{zip_path.name}.tmp-{uuid.uuid4().hex}"
        deterministic_zip(result["pack_dir"], temp)
        verify_errors = verify_zip(temp)
        if verify_errors:
            temp.unlink(missing_ok=True)
            write_state(state_path, status="FAILED", zip_path=None, zip_sha256=None,
                        source_fingerprint=result["source_fingerprint"], errors=verify_errors, warnings=result["warnings"])
            raise PackError("ZIP verification failed: " + "; ".join(verify_errors))
        os.replace(temp, zip_path)
        zip_sha = sha256_file(zip_path)
        sha_temp = sha_path.with_name(sha_path.name + f".tmp-{uuid.uuid4().hex}")
        sha_temp.write_text(f"{zip_sha}  {zip_path.name}\n", encoding="utf-8")
        os.replace(sha_temp, sha_path)
        write_state(state_path, status="COMPLETE", zip_path=zip_path, zip_sha256=zip_sha,
                    source_fingerprint=result["source_fingerprint"], errors=[], warnings=result["warnings"])

    print(json.dumps({
        "status": "COMPLETE",
        "idempotent": False,
        "canonical_zip": str(zip_path),
        "sha256": zip_sha,
        "source_fingerprint": result["source_fingerprint"],
        "warnings": result["warnings"],
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def command_verify(args: argparse.Namespace) -> int:
    errors = verify_zip(Path(args.zip).expanduser())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"valid: {Path(args.zip).expanduser()}")
    return 0


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", default=".")
    parser.add_argument("--feature-id", required=True)
    parser.add_argument("--pack-dir", required=True)
    parser.add_argument("--trace")
    parser.add_argument("--feature-base")
    parser.add_argument("--product-head", required=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="validate working pack without publishing")
    add_common(check)
    check.set_defaults(func=command_check)

    finalize = sub.add_parser("finalize", help="atomically publish the canonical ZIP")
    add_common(finalize)
    finalize.add_argument("--desktop-root", default="~/Desktop/audit-pack")
    finalize.add_argument("--state")
    finalize.add_argument("--pack-status", choices=sorted(STATUS_PACK), default="COMPLETE")
    finalize.add_argument("--telemetry-status", choices=sorted(STATUS_TELEMETRY))
    finalize.add_argument("--evidence-consistency", choices=sorted(STATUS_EVIDENCE), default="CONSISTENT")
    finalize.set_defaults(func=command_finalize)

    verify = sub.add_parser("verify", help="verify an already-published ZIP")
    verify.add_argument("--zip", required=True)
    verify.set_defaults(func=command_verify)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except PackError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
