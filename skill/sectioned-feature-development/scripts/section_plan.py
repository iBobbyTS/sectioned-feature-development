#!/usr/bin/env python3
"""Validate, list, extract, fingerprint, and archive sectioned feature plans.

The validator is intentionally strict only about durable markers, minimum
reviewability fields, unique IDs, and dependency integrity. Optional workflow
fields produce warnings rather than retroactively invalidating product work.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

FEATURE_RE = re.compile(
    r"<!--\s*FEATURE-CONTEXT:START\s*-->(.*?)"
    r"<!--\s*FEATURE-CONTEXT:END\s*-->",
    re.DOTALL | re.IGNORECASE,
)
SECTION_ID_PATTERN = r"S\d{2,}(?:\.\d+)*"
SECTION_RE = re.compile(
    rf"<!--\s*SECTION:({SECTION_ID_PATTERN}):START\s*-->(.*?)"
    rf"<!--\s*SECTION:\1:END\s*-->",
    re.DOTALL | re.IGNORECASE,
)
SECTION_MARKER_RE = re.compile(
    rf"<!--\s*SECTION:({SECTION_ID_PATTERN}):(START|END)\s*-->", re.IGNORECASE
)
ID_RE = re.compile(rf"\b{SECTION_ID_PATTERN}\b", re.IGNORECASE)
REQUIRES_LINE_RE = re.compile(
    r"(?mi)^\s*[-*]?\s*(?:Requires|依赖于|前置(?:依赖)?)\s*:\s*(.+?)\s*$"
)

FEATURE_REQUIRED: tuple[tuple[str, ...], ...] = (
    ("Goal", "目标", "一句话目标"),
    ("Observable behavior", "Observable Behavior", "用户/操作者可观察行为"),
    ("Non-goals and unsupported environments", "Non-goals", "非目标"),
    ("Feature acceptance criteria", "Full-feature Acceptance Criteria", "完整功能验收标准"),
)
FEATURE_RECOMMENDED: tuple[tuple[str, ...], ...] = (
    ("Constraints and invariants", "Global Invariants", "全局不变量"),
    ("Ownership and state boundaries", "Ownership / State Boundary"),
    ("Allowed structural changes",),
    ("Validation tiers", "Full-feature Validation Commands", "完整功能验证命令"),
)
SECTION_REQUIRED: tuple[tuple[str, ...], ...] = (
    ("Goal", "目标"),
    ("Dependencies", "依赖"),
    ("Expected scope and direct impact cone", "Expected Scope", "预计范围"),
    ("Non-goals and deferred owner", "Non-goals", "非目标"),
    ("Acceptance criteria", "Acceptance Criteria", "验收标准"),
    ("Validation tiers", "Validation Commands", "验证命令"),
)
SECTION_RECOMMENDED: tuple[tuple[str, ...], ...] = (
    ("Invariants", "Global Invariants", "全局不变量"),
    ("Allowed structural changes",),
    ("Reset triggers",),
    ("Review intensity",),
)


@dataclass(frozen=True)
class Section:
    section_id: str
    title: str
    body: str


@dataclass(frozen=True)
class ParsedPlan:
    path: Path
    text: str
    feature_context: str
    sections: tuple[Section, ...]
    warnings: tuple[str, ...]


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"plan not found: {path}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"plan is not valid UTF-8: {path}") from exc


def _heading_present(body: str, aliases: Iterable[str]) -> bool:
    for alias in aliases:
        if re.search(rf"(?mi)^###\s+{re.escape(alias)}\s*$", body):
            return True
    return False


def _title_for(section_id: str, body: str) -> str:
    match = re.search(
        rf"(?mi)^##\s+{re.escape(section_id)}\s*(?:[—–-]\s*)?(.+?)\s*$", body
    )
    return match.group(1).strip() if match else "<missing title>"


def _marker_errors(text: str) -> list[str]:
    errors: list[str] = []
    stack: list[str] = []
    for marker in SECTION_MARKER_RE.finditer(text):
        section_id = marker.group(1).upper()
        kind = marker.group(2).upper()
        if kind == "START":
            if stack:
                errors.append(
                    f"nested section marker {section_id} inside {stack[-1]} is not allowed"
                )
            stack.append(section_id)
        elif not stack:
            errors.append(f"orphan END marker for {section_id}")
        else:
            started = stack.pop()
            if started != section_id:
                errors.append(f"mismatched marker: started {started}, ended {section_id}")
    errors.extend(f"missing END marker for {section_id}" for section_id in stack)
    return errors


def _find_dependency_cycle(graph: dict[str, set[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def visit(node: str) -> list[str] | None:
        if node in visited:
            return None
        if node in visiting:
            start = stack.index(node)
            return stack[start:] + [node]
        visiting.add(node)
        stack.append(node)
        for dependency in sorted(graph.get(node, set())):
            cycle = visit(dependency)
            if cycle:
                return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for node in sorted(graph):
        cycle = visit(node)
        if cycle:
            return cycle
    return None


def parse_plan(path: Path) -> ParsedPlan:
    text = _read(path)
    errors = _marker_errors(text)
    warnings: list[str] = []

    feature_matches = list(FEATURE_RE.finditer(text))
    if len(feature_matches) != 1:
        errors.append("plan must contain exactly one FEATURE-CONTEXT START/END block")
        feature_context = ""
    else:
        feature_context = feature_matches[0].group(1).strip()
        if not feature_context:
            errors.append("FEATURE-CONTEXT block is empty")

    sections: list[Section] = []
    seen: set[str] = set()
    for match in SECTION_RE.finditer(text):
        section_id = match.group(1).upper()
        body = match.group(2).strip()
        if section_id in seen:
            errors.append(f"duplicate section ID: {section_id}")
        seen.add(section_id)
        if not body:
            errors.append(f"{section_id} block is empty")
        title = _title_for(section_id, body)
        if title == "<missing title>":
            errors.append(f"{section_id} is missing a '## {section_id} — title' heading")
        for aliases in SECTION_REQUIRED:
            if not _heading_present(body, aliases):
                errors.append(f"{section_id} is missing required heading: {aliases[0]}")
        for aliases in SECTION_RECOMMENDED:
            if not _heading_present(body, aliases):
                warnings.append(f"{section_id} is missing recommended heading: {aliases[0]}")
        sections.append(Section(section_id=section_id, title=title, body=body))

    if not sections:
        errors.append("plan contains no complete SECTION blocks")

    if feature_context:
        for aliases in FEATURE_REQUIRED:
            if not _heading_present(feature_context, aliases):
                errors.append(
                    f"FEATURE-CONTEXT is missing required heading: {aliases[0]}"
                )
        for aliases in FEATURE_RECOMMENDED:
            if not _heading_present(feature_context, aliases):
                warnings.append(
                    f"FEATURE-CONTEXT is missing recommended heading: {aliases[0]}"
                )

    known = {section.section_id for section in sections}
    graph: dict[str, set[str]] = {section_id: set() for section_id in known}
    for section in sections:
        dependency_block = re.search(
            r"(?mis)^###\s+(?:Dependencies|依赖)\s*$\s*(.*?)"
            r"(?=^###\s+|\Z)",
            section.body,
        )
        if not dependency_block:
            continue
        block_text = dependency_block.group(1)
        lines = REQUIRES_LINE_RE.findall(block_text)
        refs = {
            item.upper()
            for line in lines
            for item in ID_RE.findall(line)
        } if lines else {item.upper() for item in ID_RE.findall(block_text)}

        if section.section_id in refs:
            errors.append(f"{section.section_id} cannot depend on itself")
            refs.discard(section.section_id)
        unknown = sorted(refs - known)
        if unknown:
            errors.append(
                f"{section.section_id} references unknown dependency IDs: "
                + ", ".join(unknown)
            )
        graph[section.section_id] = refs & known

    cycle = _find_dependency_cycle(graph)
    if cycle:
        errors.append("dependency cycle: " + " -> ".join(cycle))

    raw_starts = len(
        re.findall(rf"<!--\s*SECTION:{SECTION_ID_PATTERN}:START\s*-->", text, re.IGNORECASE)
    )
    raw_ends = len(
        re.findall(rf"<!--\s*SECTION:{SECTION_ID_PATTERN}:END\s*-->", text, re.IGNORECASE)
    )
    if raw_starts != len(sections) or raw_ends != len(sections):
        errors.append(
            "one or more section marker pairs could not be parsed; check IDs and matching END markers"
        )

    if errors:
        raise ValueError("\n".join(f"- {error}" for error in errors))

    return ParsedPlan(
        path=path,
        text=text,
        feature_context=feature_context,
        sections=tuple(sections),
        warnings=tuple(warnings),
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def command_validate(args: argparse.Namespace) -> int:
    plan = parse_plan(Path(args.plan))
    print(
        f"valid: {plan.path} ({len(plan.sections)} sections, "
        f"sha256={sha256_text(plan.text)})"
    )
    for warning in plan.warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return 0


def command_list(args: argparse.Namespace) -> int:
    plan = parse_plan(Path(args.plan))
    for section in plan.sections:
        print(f"{section.section_id}\t{section.title}")
    return 0


def command_extract(args: argparse.Namespace) -> int:
    plan = parse_plan(Path(args.plan))
    requested = args.section.upper()
    selected = next(
        (section for section in plan.sections if section.section_id == requested), None
    )
    if selected is None:
        available = ", ".join(section.section_id for section in plan.sections)
        raise ValueError(f"unknown section {requested}; available: {available}")

    output = Path(args.output)
    if output.exists() and not args.force:
        raise ValueError(f"output exists: {output}; pass --force to replace it")
    output.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    content = (
        "# Current Section Plan\n\n"
        "> Generated from the full plan. The source hash is informational and does not invalidate evidence by itself.\n\n"
        f"- Source plan: `{plan.path}`\n"
        f"- Source SHA-256: `{sha256_text(plan.text)}`\n"
        f"- Section: `{selected.section_id}`\n"
        f"- Extracted at: `{timestamp}`\n\n"
        "## Feature Context\n\n"
        f"{plan.feature_context}\n\n"
        "## Current Section\n\n"
        f"{selected.body}\n"
    )
    output.write_text(content, encoding="utf-8")
    print(f"wrote: {output}")
    return 0


def command_fingerprint(args: argparse.Namespace) -> int:
    plan = parse_plan(Path(args.plan))
    print(sha256_text(plan.text))
    return 0


def command_archive(args: argparse.Namespace) -> int:
    source = Path(args.plan)
    parse_plan(source)
    destination_dir = Path(args.dest_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    timestamp = args.timestamp or datetime.now().astimezone().strftime("%Y%m%d-%H%M")
    destination = destination_dir / f"{timestamp}_FULL.md"
    if destination.exists():
        raise ValueError(f"archive destination exists: {destination}")
    if args.move:
        shutil.move(str(source), str(destination))
    else:
        shutil.copy2(source, destination)
    print(f"archived: {destination}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate plan structure")
    validate.add_argument("plan")
    validate.set_defaults(func=command_validate)

    listing = subparsers.add_parser("list", help="list section IDs and titles")
    listing.add_argument("plan")
    listing.set_defaults(func=command_list)

    extract = subparsers.add_parser("extract", help="extract one section")
    extract.add_argument("plan")
    extract.add_argument("section")
    extract.add_argument("--output", required=True)
    extract.add_argument("--force", action="store_true")
    extract.set_defaults(func=command_extract)

    fingerprint = subparsers.add_parser("fingerprint", help="print informational SHA-256")
    fingerprint.add_argument("plan")
    fingerprint.set_defaults(func=command_fingerprint)

    archive = subparsers.add_parser("archive", help="copy or move full plan to archive")
    archive.add_argument("plan")
    archive.add_argument("--dest-dir", required=True)
    archive.add_argument("--timestamp")
    archive.add_argument("--move", action="store_true")
    archive.set_defaults(func=command_archive)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
