#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("audit_trace.py")


class AuditTraceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Test"], check=True)
        (self.root / "file.txt").write_text("base\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "file.txt"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "base"], check=True)
        self.head = subprocess.check_output(["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True).strip()
        self.trace = self.root / ".agent-work" / "audit" / "demo" / "TRACE.jsonl"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_cli(self, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            ["python", str(SCRIPT), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(proc.returncode, expect, msg=proc.stderr)
        return proc

    def init_trace(self) -> None:
        self.run_cli(
            "init",
            str(self.trace),
            "--feature-id", "demo",
            "--skill-version", "V3.5",
            "--invocation-source", "CUSTOM_INSTRUCTIONS_AUTO",
            "--invocation-timing", "FEATURE_START",
            "--trigger-evidence", "more than three owners",
            "--audit-enabled-by", "user requested audit mode",
            "--feature-base", self.head,
            "--repo", str(self.root),
            "--field", "estimated_owners=4",
        )

    def test_init_append_validate_and_summary(self) -> None:
        self.init_trace()
        self.run_cli(
            "append", str(self.trace),
            "--event", "plan_frozen",
            "--phase", "plan",
            "--summary", "Plan validated.",
            "--repo", str(self.root),
            "--result", "PASS",
            "--field", "section_count=1",
        )
        self.run_cli(
            "append", str(self.trace),
            "--event", "validation_completed",
            "--phase", "validation",
            "--summary", "Focused tests passed.",
            "--repo", str(self.root),
            "--result", "PASS",
            "--field", "command_family=focused-tests",
        )
        self.run_cli(
            "append", str(self.trace),
            "--event", "validation_completed",
            "--phase", "validation",
            "--summary", "Focused tests passed again.",
            "--repo", str(self.root),
            "--result", "PASS",
            "--field", "command_family=focused-tests",
        )
        self.run_cli("validate", str(self.trace))
        output = self.run_cli("summary", str(self.trace)).stdout
        summary = json.loads(output)
        self.assertEqual(summary["record_count"], 4)
        self.assertEqual(summary["invocation_source"], "CUSTOM_INSTRUCTIONS_AUTO")
        self.assertEqual(summary["events"]["validation_completed"], 2)
        self.assertEqual(summary["duplicate_successful_validation_groups"][0]["count"], 2)

    def test_invalid_invocation_source_is_rejected(self) -> None:
        self.run_cli(
            "init", str(self.trace),
            "--feature-id", "demo",
            "--skill-version", "V3.5",
            "--invocation-source", "AUTOMATIC",
            "--invocation-timing", "FEATURE_START",
            "--trigger-evidence", "x",
            "--audit-enabled-by", "y",
            "--feature-base", self.head,
            "--repo", str(self.root),
            expect=2,
        )

    def test_corrupt_sequence_fails_validation(self) -> None:
        self.init_trace()
        records = [json.loads(line) for line in self.trace.read_text().splitlines()]
        records[0]["sequence"] = 3
        self.trace.write_text("\n".join(json.dumps(r) for r in records) + "\n")
        self.run_cli("validate", str(self.trace), expect=1)


if __name__ == "__main__":
    unittest.main()
