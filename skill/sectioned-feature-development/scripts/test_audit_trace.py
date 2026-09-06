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
        proc = subprocess.run(["python", str(SCRIPT), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        self.assertEqual(proc.returncode, expect, msg=proc.stderr)
        return proc

    def init_trace(self) -> None:
        self.run_cli(
            "init", str(self.trace),
            "--feature-id", "demo",
            "--skill-version", "V3.7",
            "--invocation-source", "CUSTOM_INSTRUCTIONS_AUTO",
            "--invocation-timing", "FEATURE_START",
            "--trigger-evidence", "more than three owners",
            "--feature-base", self.head,
            "--repo", str(self.root),
            "--field", "estimated_owners=4",
        )

    def test_init_append_validate_and_summary(self) -> None:
        self.init_trace()
        self.run_cli("append", str(self.trace), "--event", "requirements_frozen", "--phase", "plan", "--summary", "Requirements captured.", "--repo", str(self.root), "--result", "PASS")
        for message in ("Focused tests passed.", "Focused tests passed again."):
            self.run_cli("append", str(self.trace), "--event", "validation_completed", "--phase", "validation", "--summary", message, "--repo", str(self.root), "--result", "PASS", "--field", "command_family=focused-tests")
        payload = json.loads(self.run_cli("validate", str(self.trace), "--json").stdout)
        self.assertEqual(payload["telemetry_status"], "VALID")
        summary = json.loads(self.run_cli("summary", str(self.trace)).stdout)
        self.assertEqual(summary["record_count"], 4)
        self.assertEqual(summary["duplicate_successful_validation_groups"][0]["count"], 2)

    def test_sequence_gap_and_unknown_event_degrade_but_do_not_invalidate(self) -> None:
        self.init_trace()
        records = [json.loads(line) for line in self.trace.read_text().splitlines()]
        records.append({
            "schema_version": 2,
            "record_id": "manual",
            "sequence": 3,
            "timestamp_utc": "2026-08-17T00:00:00Z",
            "event": "future_event",
            "phase": "audit",
            "summary": "Future vocabulary.",
            "feature_id": "demo",
        })
        self.trace.write_text("\n".join(json.dumps(r) for r in records) + "\n")
        payload = json.loads(self.run_cli("validate", str(self.trace), "--json").stdout)
        self.assertEqual(payload["telemetry_status"], "DEGRADED")
        self.assertTrue(any("unknown event" in item for item in payload["warnings"]))
        self.assertTrue(any("sequence" in item for item in payload["warnings"]))

    def test_concurrent_append_uses_unique_monotonic_sequences(self) -> None:
        self.init_trace()
        processes = []
        for index in range(8):
            processes.append(subprocess.Popen([
                "python", str(SCRIPT), "append", str(self.trace),
                "--event", "audit_note", "--phase", "audit",
                "--summary", f"note {index}", "--repo", str(self.root),
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
        for process in processes:
            stdout, stderr = process.communicate(timeout=20)
            self.assertEqual(process.returncode, 0, msg=stderr + stdout)
        records = [json.loads(line) for line in self.trace.read_text().splitlines()]
        self.assertEqual([record["sequence"] for record in records], list(range(1, 10)))
        self.assertEqual(len({record["record_id"] for record in records}), 9)

    def test_invalid_invocation_source_is_rejected(self) -> None:
        self.run_cli(
            "init", str(self.trace), "--feature-id", "demo", "--skill-version", "V3.7",
            "--invocation-source", "AUTOMATIC", "--invocation-timing", "FEATURE_START",
            "--trigger-evidence", "x", "--feature-base", self.head, "--repo", str(self.root), expect=2,
        )

    def test_current_family_event_is_valid(self):
        self.init_trace()
        self.run_cli('append',str(self.trace),'--event','subsection_checkpoint_recorded','--family','subsection',
                     '--phase','review','--summary','checkpoint saved','--repo',str(self.root))
        data=json.loads(self.run_cli('validate',str(self.trace),'--json').stdout)
        self.assertEqual(data['telemetry_status'],'VALID')

    def test_structured_result_summary_does_not_crash(self):
        self.init_trace()
        self.run_cli('append',str(self.trace),'--event','review_completed','--phase','review','--summary','done','--repo',str(self.root))
        records=[json.loads(x) for x in self.trace.read_text().splitlines()]
        records[-1]['result']={'status':'CLEAN','findings':[]}
        self.trace.write_text('\n'.join(json.dumps(x) for x in records)+'\n')
        result=json.loads(self.run_cli('summary',str(self.trace)).stdout)
        self.assertEqual(result['results']['CLEAN'],1)


if __name__ == "__main__":
    unittest.main()
