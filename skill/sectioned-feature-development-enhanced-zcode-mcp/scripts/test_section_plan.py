#!/usr/bin/env python3
"""Dependency-free forward tests for section_plan.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("section_plan.py")
TEMPLATE = Path(__file__).parents[1] / "assets" / "PLAN-FULL.template.md"


def run(*args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"command {args} returned {result.returncode}, expected {expected}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def expect_invalid(path: Path, fragment: str) -> None:
    result = run("validate", str(path), expected=2)
    assert fragment in result.stderr, result.stderr


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        plan = root / "PLAN-FULL.md"
        template = TEMPLATE.read_text(encoding="utf-8")
        plan.write_text(template, encoding="utf-8")

        valid = run("validate", str(plan)).stdout
        assert "2 sections" in valid
        listed = run("list", str(plan)).stdout
        assert "S01" in listed and "S02" in listed

        fingerprint = run("fingerprint", str(plan)).stdout.strip()
        assert len(fingerprint) == 64

        current = root / "PLAN.md"
        run("extract", str(plan), "S01", "--output", str(current))
        extracted = current.read_text(encoding="utf-8")
        assert "Source SHA-256" in extracted
        assert "## S01" in extracted
        assert "## S02" not in extracted
        assert "informational" in extracted
        run("extract", str(plan), "S01", "--output", str(current), expected=2)
        run("extract", str(plan), "S99", "--output", str(root / "missing.md"), expected=2)

        hierarchical = root / "HIERARCHICAL.md"
        hierarchical.write_text(template.replace("S02", "S03.1"), encoding="utf-8")
        assert "S03.1" in run("list", str(hierarchical)).stdout

        archive_dir = root / "plans"
        run(
            "archive",
            str(plan),
            "--dest-dir",
            str(archive_dir),
            "--timestamp",
            "20990101-0000",
        )
        assert (archive_dir / "20990101-0000_FULL.md").exists()
        assert plan.exists(), "archive should copy unless --move is explicit"

        missing_required = root / "MISSING.md"
        missing_required.write_text(
            template.replace("### Acceptance criteria", "### Missing", 1),
            encoding="utf-8",
        )
        expect_invalid(missing_required, "missing required heading: Acceptance criteria")

        missing_recommended = root / "WARNING.md"
        missing_recommended.write_text(
            template.replace("### Allowed structural changes", "### Optional Removed", 1),
            encoding="utf-8",
        )
        warning = run("validate", str(missing_recommended)).stderr
        assert "missing recommended heading: Allowed structural changes" in warning

        unknown = root / "UNKNOWN.md"
        unknown.write_text(
            template.replace("- Requires: `S01`", "- Requires: `S99`", 1),
            encoding="utf-8",
        )
        expect_invalid(unknown, "unknown dependency IDs: S99")

        self_dep = root / "SELF.md"
        self_dep.write_text(
            template.replace("- Requires: `none`", "- Requires: `S01`", 1),
            encoding="utf-8",
        )
        expect_invalid(self_dep, "S01 cannot depend on itself")

        cycle = root / "CYCLE.md"
        cycle.write_text(
            template.replace("- Requires: `none`", "- Requires: `S02`", 1),
            encoding="utf-8",
        )
        expect_invalid(cycle, "dependency cycle:")

    print("section_plan.py tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
