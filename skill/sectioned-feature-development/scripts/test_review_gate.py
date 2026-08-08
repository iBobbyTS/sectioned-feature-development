#!/usr/bin/env python3
"""Dependency-free forward tests for review_gate.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).with_name("review_gate.py")


def run(*args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"{args} returned {result.returncode}, expected {expected}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def record(round_no: int, result: str, clean: bool, streak: int, finding: str = "") -> str:
    valid = "no" if result == "EVIDENCE_FAILURE" else "yes"
    return f"""# Review Admission：S01 r{round_no:02d}

- Mode: `SECTION`
- Section: `S01`
- Counting round: `{round_no}`
- Review attempt: `1`
- Raw review: `raw.md`
- Contract revision: `1`
- Plan fingerprint: `abc`
- Assurance envelope revision: `v1`
- Reviewed base: `base`
- Reviewed head: `head{round_no}`
- Evidence-valid conclusion: `{valid}`
- Result: `{result}`
- Clean admission: `{'yes' if clean else 'no'}`
- Clean streak after: `{streak}`

## Candidate Decisions

{finding}

## Round Summary

- Material admitted IDs: `none`
- Non-authoritative scope proposals: `none`
- Unsupported/nit/deferred IDs: `none`
- Evidence invalidated: `none`
- Next action: `fresh review`
"""


def finding(cls: str, boundary: str, domain: str = "correctness") -> str:
    return f"""<!-- FINDING:REV-001:START -->
### REV-001 — Example

- Raw severity: `Must Fix`
- Domain: `{domain}`
- Admission class: `{cls}`
- Contract/repository anchor: `S01-AC-01`
- Reachable supported trigger: `call supported API with x`
- Material consequence: `wrong result`
- Evidence / falsifiable path: `test_case`
- Smallest correct remedy: `repair implementation`
- Boundary effect: `{boundary}`
- Named deferred owner: `none`
- Security asset: `N/A`
- Security actor and capability: `N/A`
- Security entry point / data flow: `N/A`
- Security trust boundary and preconditions: `N/A`
- Supported deployment context: `N/A`
- Decision rationale: `violates frozen criterion`
- Scope-change record: `none`
<!-- FINDING:REV-001:END -->"""


def main() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        r1 = root / "r1.md"
        r2 = root / "r2.md"
        r1.write_text(record(1, "CLEAN", True, 1), encoding="utf-8")
        r2.write_text(record(2, "CLEAN", True, 2), encoding="utf-8")
        run("validate", str(r1))
        hist = run("history", str(r1), str(r2)).stdout
        assert "status=SECTION_ACCEPTED" in hist

        bad_scope = root / "bad-scope.md"
        bad_scope.write_text(
            record(
                1,
                "MATERIAL_FINDINGS",
                False,
                0,
                finding("SCOPE_PROPOSAL", "inside-section"),
            ),
            encoding="utf-8",
        )
        result = run("validate", str(bad_scope), expected=2)
        assert "requires Boundary effect 'new-scope'" in result.stderr

        replan = root / "replan.md"
        replan.write_text(
            record(
                1,
                "MATERIAL_FINDINGS",
                False,
                0,
                finding("IN_SCOPE_REPLAN", "cross-section"),
            ),
            encoding="utf-8",
        )
        run("validate", str(replan))

        five: list[str] = []
        for i in range(1, 6):
            path = root / f"f{i}.md"
            path.write_text(
                record(
                    i,
                    "MATERIAL_FINDINGS",
                    False,
                    0,
                    finding("IN_SCOPE_REPAIR", "inside-section"),
                ),
                encoding="utf-8",
            )
            five.append(str(path))
        hard = run("history", *five).stdout
        assert "status=HARD_CAP_RECOVERY" in hard

        invalid_evidence = root / "evidence.md"
        invalid_evidence.write_text(
            record(
                1,
                "EVIDENCE_FAILURE",
                False,
                0,
                finding("EVIDENCE_FAILURE", "evidence-only"),
            ),
            encoding="utf-8",
        )
        run("validate", str(invalid_evidence))
        evidence_hist = run("history", str(invalid_evidence)).stdout
        assert "completed_rounds=1" in evidence_hist
        assert "clean_streak=0" in evidence_hist

        # A completed evidence-failure review consumes r1; two later clean reviews
        # can accept only at r3, never by silently retrying r1.
        e2 = root / "e2.md"
        e3 = root / "e3.md"
        e2.write_text(record(2, "CLEAN", True, 1), encoding="utf-8")
        e3.write_text(record(3, "CLEAN", True, 2), encoding="utf-8")
        recovered = run(
            "history", str(invalid_evidence), str(e2), str(e3)
        ).stdout
        assert "completed_rounds=3" in recovered
        assert "status=SECTION_ACCEPTED" in recovered

        # No completed review artifact may claim a sixth counting round.
        r6 = root / "r6.md"
        r6.write_text(record(6, "CLEAN", True, 1), encoding="utf-8")
        sixth = run("validate", str(r6), expected=2)
        assert "Counting round must be 1..5" in sixth.stderr

    print("review_gate.py tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
