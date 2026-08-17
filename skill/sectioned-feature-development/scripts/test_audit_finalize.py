#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("audit_finalize.py")
TRACE_SCRIPT = Path(__file__).with_name("audit_trace.py")
REQUIRED = [
    "00-README.md", "AUDIT-VERDICT.md", "HUMAN-REQUIREMENTS.md", "INVOCATION-AUDIT.md",
    "COUNTERFACTUAL-MINIMUM.md", "PLAN-AUDIT.md", "SCOPE-AUDIT.md", "REVIEW-AUDIT.md",
    "VALIDATION-AUDIT.md", "COST-METRICS.md", "SKILL-COMPLIANCE.md", "RECOMMENDATIONS.md",
    "requirements/REQUIREMENTS.md",
]


class AuditFinalizeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "demo-repo"
        self.root.mkdir()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Test"], check=True)
        (self.root / "file.txt").write_text("base\n")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "base"], check=True)
        self.head = subprocess.check_output(["git", "-C", str(self.root), "rev-parse", "HEAD"], text=True).strip()
        self.pack = self.root / ".agent-work/audit-packs/demo/current"
        for rel in REQUIRED:
            path = self.pack / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {rel}\n")
        for rel in ("git/HEAD.txt", "sources/head/file.txt", "planning/PLAN-FULL.md"):
            path = self.pack / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(self.head + "\n")
        self.trace = self.root / ".agent-work/audit/demo/TRACE.jsonl"
        subprocess.run([
            "python", str(TRACE_SCRIPT), "init", str(self.trace), "--feature-id", "demo",
            "--skill-version", "V3.7", "--invocation-source", "USER_EXPLICIT",
            "--invocation-timing", "FEATURE_START", "--trigger-evidence", "user requested skill",
            "--feature-base", self.head, "--repo", str(self.root),
        ], check=True)
        self.desktop = Path(self.tmp.name) / "Desktop/audit-pack"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_cli(self, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(["python", str(SCRIPT), *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        self.assertEqual(proc.returncode, expect, msg=proc.stderr + proc.stdout)
        return proc

    def common(self) -> list[str]:
        return [
            "--repo", str(self.root), "--feature-id", "demo", "--pack-dir", str(self.pack),
            "--trace", str(self.trace), "--feature-base", self.head, "--product-head", self.head,
        ]

    def test_finalize_is_canonical_atomic_and_idempotent(self) -> None:
        check = json.loads(self.run_cli("check", *self.common()).stdout)
        self.assertTrue(check["ok"])
        first = json.loads(self.run_cli("finalize", *self.common(), "--desktop-root", str(self.desktop)).stdout)
        self.assertFalse(first["idempotent"])
        zip_path = Path(first["canonical_zip"])
        self.assertTrue(zip_path.exists())
        self.run_cli("verify", "--zip", str(zip_path))
        second = json.loads(self.run_cli("finalize", *self.common(), "--desktop-root", str(self.desktop)).stdout)
        self.assertTrue(second["idempotent"])
        self.assertEqual(len(list(self.desktop.glob("*.zip"))), 1)
        state = json.loads((self.root / ".agent-work/audit/demo/PACK-STATE.json").read_text())
        self.assertEqual(state["status"], "COMPLETE")
        self.assertEqual(state["canonical_zip"], str(zip_path))

    def test_raw_session_jsonl_is_rejected(self) -> None:
        raw = self.pack / "session/raw.jsonl"
        raw.parent.mkdir(parents=True, exist_ok=True)
        raw.write_text('{}\n')
        payload = json.loads(self.run_cli("check", *self.common(), expect=1).stdout)
        self.assertTrue(any("raw session" in item for item in payload["errors"]))


if __name__ == "__main__":
    unittest.main()
