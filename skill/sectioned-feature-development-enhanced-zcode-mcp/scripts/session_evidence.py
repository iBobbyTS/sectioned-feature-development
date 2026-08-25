#!/usr/bin/env python3
"""Extract redacted, feature-relevant evidence from local Codex session JSONL files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

DEFAULT_ROOTS = [Path("~/.codex/sessions"), Path("~/.codex-multi-2/sessions")]
SECRET_PATTERNS = [
    (re.compile(r"(?i)(authorization\s*:\s*bearer\s+)[^\s\"']+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)\b(sk-[A-Za-z0-9_-]{12,})\b"), "[REDACTED_API_KEY]"),
    (re.compile(r"(?i)(api[_-]?key\s*[=:]\s*)[^\s,;\"']+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(refresh[_-]?token\s*[=:]\s*)[^\s,;\"']+"), r"\1[REDACTED]"),
    (re.compile(r"(?i)(password\s*[=:]\s*)[^\s,;\"']+"), r"\1[REDACTED]"),
]


class EvidenceError(RuntimeError):
    pass


def redact(text: str) -> str:
    result = text
    for pattern, replacement in SECRET_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def object_timestamp(obj: dict[str, Any]) -> str | None:
    for key in ("timestamp", "timestamp_utc", "created_at", "time"):
        value = obj.get(key)
        if isinstance(value, str):
            return value
    payload = obj.get("payload")
    if isinstance(payload, dict):
        for key in ("timestamp", "timestamp_utc", "created_at", "time"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
    return None


def recursive_values(obj: Any, key: str) -> Iterable[Any]:
    if isinstance(obj, dict):
        for current_key, value in obj.items():
            if current_key == key:
                yield value
            yield from recursive_values(value, key)
    elif isinstance(obj, list):
        for item in obj:
            yield from recursive_values(item, key)


def extract_cwd(obj: dict[str, Any]) -> str | None:
    for value in recursive_values(obj, "cwd"):
        if isinstance(value, str) and value:
            return value
    return None


def content_to_text(content: Any) -> str | None:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                for key in ("input_text", "text", "content"):
                    value = item.get(key)
                    if isinstance(value, str):
                        parts.append(value)
                        break
        return "\n".join(part for part in parts if part) or None
    if isinstance(content, dict):
        for key in ("input_text", "text", "content"):
            value = content.get(key)
            if isinstance(value, str):
                return value
    return None


def extract_role_messages(obj: Any, role: str) -> list[str]:
    messages: list[str] = []
    if isinstance(obj, dict):
        if obj.get("role") == role:
            text = content_to_text(obj.get("content"))
            if text:
                messages.append(text)
        for value in obj.values():
            messages.extend(extract_role_messages(value, role))
    elif isinstance(obj, list):
        for item in obj:
            messages.extend(extract_role_messages(item, role))
    return messages


def event_label(obj: dict[str, Any]) -> str:
    for key in ("type", "event", "kind"):
        value = obj.get(key)
        if isinstance(value, str) and value:
            return value
    payload = obj.get("payload")
    if isinstance(payload, dict):
        for key in ("type", "event", "kind"):
            value = payload.get(key)
            if isinstance(value, str) and value:
                return value
    return "record"


def file_in_window(path: Path, start: datetime | None, end: datetime | None) -> bool:
    modified = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    if start and modified < start:
        return False
    if end and modified > end:
        return False
    return True


def scan_session(path: Path, repo: Path, start: datetime | None, end: datetime | None, keywords: list[str]) -> dict[str, Any] | None:
    records: list[dict[str, Any]] = []
    cwd_values: set[str] = set()
    user_messages: list[tuple[str | None, str]] = []
    timeline: list[tuple[str | None, str, str]] = []
    parse_errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return {"path": str(path), "parse_errors": [str(exc)], "selected": False}

    for lineno, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            parse_errors.append(f"line {lineno}: {exc}")
            continue
        if not isinstance(obj, dict):
            continue
        records.append(obj)
        cwd = extract_cwd(obj)
        if cwd:
            cwd_values.add(cwd)
        timestamp = object_timestamp(obj)
        parsed_timestamp = parse_time(timestamp)
        if start and parsed_timestamp and parsed_timestamp < start:
            continue
        if end and parsed_timestamp and parsed_timestamp > end:
            continue
        for message in extract_role_messages(obj, "user"):
            user_messages.append((timestamp, redact(message)))
        label = event_label(obj)
        if label in {"event_msg", "agent_message", "response_item", "context_compacted", "task_started", "task_complete", "turn_aborted"}:
            summary = ""
            for key in ("message", "summary", "text"):
                candidates = list(recursive_values(obj, key))
                value = next((item for item in candidates if isinstance(item, str) and item), None)
                if value:
                    summary = redact(value)[:1000]
                    break
            timeline.append((timestamp, label, summary))

    repo_text = str(repo.resolve())
    cwd_match = any(Path(cwd).expanduser().resolve() == repo.resolve() or repo_text.startswith(str(Path(cwd).expanduser().resolve()) + "/") or str(Path(cwd).expanduser().resolve()).startswith(repo_text + "/") for cwd in cwd_values if cwd)
    searchable = "\n".join(message for _, message in user_messages).lower()
    keyword_match = not keywords or any(keyword.lower() in searchable for keyword in keywords)
    selected = cwd_match and keyword_match
    return {
        "path": str(path),
        "selected": selected,
        "cwd_values": sorted(cwd_values),
        "user_messages": user_messages,
        "timeline": timeline,
        "parse_errors": parse_errors,
        "record_count": len(records),
    }


def quote_block(text: str) -> str:
    return "\n".join("> " + line for line in text.splitlines())


def command_extract(args: argparse.Namespace) -> int:
    repo = Path(args.repo).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    roots = [Path(item).expanduser() for item in (args.session_root or [str(root) for root in DEFAULT_ROOTS])]
    start = parse_time(args.start)
    end = parse_time(args.end)
    candidates: list[Path] = []
    missing_roots: list[str] = []
    for root in roots:
        if not root.exists():
            missing_roots.append(str(root))
            continue
        candidates.extend(path for path in root.rglob("*.jsonl") if path.is_file() and file_in_window(path, start, end))

    results: list[dict[str, Any]] = []
    for path in sorted(set(candidates)):
        result = scan_session(path, repo, start, end, args.keyword)
        if result and result.get("selected"):
            results.append(result)

    output.mkdir(parents=True, exist_ok=True)
    requirements_lines = [
        "# Recovered Human Messages",
        "",
        "> Derived from authorized local Codex session files. Secrets are redacted. This is fallback evidence; the live `REQUIREMENTS.md` remains authoritative.",
        "",
    ]
    seen_messages: set[tuple[str | None, str]] = set()
    for result in results:
        requirements_lines.append(f"## Session `{result['path']}`")
        requirements_lines.append("")
        for timestamp, message in result["user_messages"]:
            key = (timestamp, message)
            if key in seen_messages:
                continue
            seen_messages.add(key)
            requirements_lines.append(f"### {timestamp or 'timestamp unknown'}")
            requirements_lines.append("")
            requirements_lines.append(quote_block(message))
            requirements_lines.append("")
    if not seen_messages:
        requirements_lines.extend(["`UNKNOWN`: no matching user messages were recovered.", ""])
    (output / "HUMAN-MESSAGES.md").write_text("\n".join(requirements_lines), encoding="utf-8")

    timeline_lines = ["# Session Timeline", ""]
    for result in results:
        timeline_lines.append(f"## Session `{result['path']}`")
        timeline_lines.append("")
        for timestamp, label, summary in result["timeline"]:
            line = f"- `{timestamp or 'unknown'}` **{label}**"
            if summary:
                line += f": {summary.replace(chr(10), ' ')}"
            timeline_lines.append(line)
        if result["parse_errors"]:
            timeline_lines.append(f"- Parser gaps: {len(result['parse_errors'])}")
        timeline_lines.append("")
    if not results:
        timeline_lines.extend(["No matching session was recovered.", ""])
    (output / "SESSION-TIMELINE.md").write_text("\n".join(timeline_lines), encoding="utf-8")

    sources = {
        "repository": str(repo),
        "session_roots": [str(root) for root in roots],
        "missing_roots": missing_roots,
        "start": args.start,
        "end": args.end,
        "keywords": args.keyword,
        "selected_sessions": [
            {
                "path": result["path"],
                "cwd_values": result["cwd_values"],
                "record_count": result["record_count"],
                "parse_errors": result["parse_errors"],
            }
            for result in results
        ],
    }
    (output / "SESSION-SOURCES.json").write_text(json.dumps(sources, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"selected_sessions": len(results), "output": str(output), "missing_roots": missing_roots}, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    extract = sub.add_parser("extract", help="extract relevant redacted human messages and timeline")
    extract.add_argument("--repo", required=True)
    extract.add_argument("--output", required=True)
    extract.add_argument("--session-root", action="append")
    extract.add_argument("--start")
    extract.add_argument("--end")
    extract.add_argument("--keyword", action="append", default=[])
    extract.set_defaults(func=command_extract)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return int(args.func(args))
    except EvidenceError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
