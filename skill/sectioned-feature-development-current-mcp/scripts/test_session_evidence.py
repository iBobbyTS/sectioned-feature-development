#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("session_evidence.py")


class SessionEvidenceTest(unittest.TestCase):
    def test_extracts_repo_user_messages_and_redacts_secret(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "repo"
            repo.mkdir()
            sessions = root / "sessions"
            sessions.mkdir()
            session = sessions / "demo.jsonl"
            records = [
                {"timestamp": "2026-08-17T08:00:00Z", "type": "session_meta", "payload": {"cwd": str(repo)}},
                {"timestamp": "2026-08-17T08:01:00Z", "type": "response_item", "payload": {"role": "user", "content": [{"type": "input_text", "text": "实现余额查询 api_key=secret-value"}]}},
                {"timestamp": "2026-08-17T08:02:00Z", "type": "context_compacted", "summary": "compacted"},
            ]
            session.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in records) + "\n")
            output = root / "output"
            proc = subprocess.run([
                "python", str(SCRIPT), "extract", "--repo", str(repo), "--output", str(output),
                "--session-root", str(sessions), "--keyword", "余额查询",
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            human = (output / "HUMAN-MESSAGES.md").read_text()
            self.assertIn("余额查询", human)
            self.assertIn("[REDACTED]", human)
            self.assertNotIn("secret-value", human)
            self.assertTrue((output / "SESSION-TIMELINE.md").exists())
            self.assertTrue((output / "SESSION-SOURCES.json").exists())


if __name__ == "__main__":
    unittest.main()
