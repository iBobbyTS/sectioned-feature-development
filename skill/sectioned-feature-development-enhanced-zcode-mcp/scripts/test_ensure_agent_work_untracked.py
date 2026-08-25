#!/usr/bin/env python3
"""Tests for ensure_agent_work_untracked.py."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from ensure_agent_work_untracked import (
    AlreadyTrackedError,
    ensure_untracked,
)


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout


class EnsureAgentWorkUntrackedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        git(self.repo, "init", "-q")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_adds_local_exclude_and_is_idempotent(self) -> None:
        root, exclude, changed = ensure_untracked(self.repo)
        self.assertEqual(root, self.repo.resolve())
        self.assertTrue(changed)
        self.assertIn(".agent-work/", exclude.read_text(encoding="utf-8"))

        _, same_exclude, second_changed = ensure_untracked(self.repo)
        self.assertEqual(same_exclude, exclude)
        self.assertFalse(second_changed)
        self.assertEqual(
            exclude.read_text(encoding="utf-8").count(".agent-work/"), 1
        )

    def test_accepts_equivalent_existing_pattern(self) -> None:
        exclude = Path(git(self.repo, "rev-parse", "--git-path", "info/exclude").strip())
        if not exclude.is_absolute():
            exclude = self.repo / exclude
        exclude.parent.mkdir(parents=True, exist_ok=True)
        exclude.write_text("/.agent-work/**\n", encoding="utf-8")
        _, _, changed = ensure_untracked(self.repo)
        self.assertFalse(changed)

    def test_refuses_when_agent_work_is_tracked(self) -> None:
        tracked = self.repo / ".agent-work" / "PLAN.md"
        tracked.parent.mkdir(parents=True)
        tracked.write_text("plan\n", encoding="utf-8")
        git(self.repo, "add", ".agent-work/PLAN.md")

        with self.assertRaises(AlreadyTrackedError):
            ensure_untracked(self.repo)

        exclude = Path(git(self.repo, "rev-parse", "--git-path", "info/exclude").strip())
        if not exclude.is_absolute():
            exclude = self.repo / exclude
        content = exclude.read_text(encoding="utf-8") if exclude.exists() else ""
        self.assertNotIn(".agent-work/", content)


if __name__ == "__main__":
    unittest.main()
