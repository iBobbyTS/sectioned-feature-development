"""Offline contract wiring and real temporary-install regressions, not model evals."""
from pathlib import Path
import hashlib
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'skill/code-review'
SFD = ROOT / 'skill/sectioned-feature-development'

class ReviewCompatibilityTests(unittest.TestCase):
    def test_active_companion_not_historical_only(self):
        self.assertTrue((REVIEW/'SKILL.md').is_file())
        self.assertTrue((REVIEW/'agents/openai.yaml').is_file())
        text = (REVIEW/'SKILL.md').read_text()
        self.assertIn('## Select execution context first', text)
        self.assertIn('`DELEGATED_PASS`', text)
        self.assertIn('`STANDALONE`', text)

    def test_parent_and_companion_protocol_agree(self):
        paths = [REVIEW/'references/delegated-pass.md', SFD/'SKILL.md',
                 SFD/'references/bounded-review.md', SFD/'assets/REVIEW-PACKET.template.md',
                 ROOT/'agents/code_reviewer.toml']
        for path in paths:
            with self.subTest(path=path):
                text = path.read_text()
                self.assertIn('sfd-delegated-review/4.0', text)
                self.assertIn('sfd-delegated-review/4.2', text)
                self.assertIn('DELEGATED_PASS', text)
        for path in [REVIEW/'references/delegated-pass.md', SFD/'references/bounded-review.md', SFD/'assets/REVIEW-PACKET.template.md']:
            for signal in ['CLEAN', 'MATERIAL_CANDIDATES', 'INSUFFICIENT_EVIDENCE']:
                self.assertIn(signal, path.read_text())

    def test_standalone_lifecycle_is_not_delegated_authority(self):
        for name in ['standalone-workflow.md','section-review-protocol.md',
                     'review-loop-protocol.md','ledger-templates.md']:
            with self.subTest(name=name):
                text = (REVIEW/'references'/name).read_text()
                self.assertIn('STANDALONE', text[:700])
                self.assertIn('delegated-pass.md', text[:700])
        original = (REVIEW/'references/standalone-workflow.md').read_text()
        self.assertIn('## Repair-Enabled Mode', original)
        self.assertIn('## Convergence and Stop Conditions', original)

    def test_required_assurance_and_continuity_are_not_weakened(self):
        text = (REVIEW/'references/delegated-pass.md').read_text()
        self.assertIn('**and requires one fresh final full pass**', text)
        self.assertIn('**plus a fresh independent final full pass**', text)
        self.assertIn('TERMINAL_CONTINUATION_UNSUPPORTED', text)
        self.assertIn('CONTINUITY_BLOCKED', text)
        self.assertIn('same_session=false', text)
        self.assertIn('not a new counted full pass', text)
        self.assertIn('Independent sibling writers in isolated worktrees are not a violation', text)

    def test_same_candidate_is_required_for_clean(self):
        text = (REVIEW/'references/delegated-pass.md').read_text()
        self.assertIn('If the frozen candidate changes during review, stop', text)
        self.assertIn('Missing stable reviewer identity or exact candidate evidence', text)
        self.assertIn('A successful external task or hash-valid artifact is not automatically a clean review', text)

    def command(self, home, *args):
        return subprocess.run([sys.executable, str(ROOT/'scripts/install.py'),
                               '--codex-home', str(home), *args],
                              capture_output=True, text=True, check=False)

    def test_companion_only_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)/'home'
            result = self.command(home, '--only','code-review')
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            self.assertIn('skill/code-review ->', result.stdout)
            self.assertNotIn('skill/sectioned-feature-development ->', result.stdout)
            self.assertNotIn('agents/advisor.toml ->', result.stdout)
            self.assertFalse(home.exists())

    def test_companion_only_replace_backs_up_and_preserves_others(self):
        with tempfile.TemporaryDirectory() as temp:
            home = Path(temp)/'home'
            old = home/'skills/code-review'; old.mkdir(parents=True)
            (old/'SKILL.md').write_text('old locally customized review')
            (old/'custom.txt').write_text('preserve in backup')
            core = home/'skills/sectioned-feature-development'; core.mkdir()
            (core/'SKILL.md').write_text('existing 4.0')
            (home/'agents').mkdir(); (home/'agents/advisor.toml').write_text('keep agent')
            (home/'AGENTS.md').write_text('keep policy')
            (home/'config.toml').write_text('keep global config')
            denied = self.command(home, '--only','code-review','--apply')
            self.assertNotEqual(denied.returncode, 0)
            self.assertEqual((old/'SKILL.md').read_text(), 'old locally customized review')
            result = self.command(home, '--only','code-review','--apply','--replace')
            self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
            self.assertEqual((old/'SKILL.md').read_bytes(), (REVIEW/'SKILL.md').read_bytes())
            backups = list((home/'sfd-backups').glob('*/skills/code-review'))
            self.assertEqual(len(backups), 1)
            self.assertEqual((backups[0]/'SKILL.md').read_text(), 'old locally customized review')
            self.assertEqual((backups[0]/'custom.txt').read_text(), 'preserve in backup')
            self.assertEqual((core/'SKILL.md').read_text(), 'existing 4.0')
            self.assertEqual((home/'agents/advisor.toml').read_text(), 'keep agent')
            self.assertEqual((home/'AGENTS.md').read_text(), 'keep policy')
            self.assertEqual((home/'config.toml').read_text(), 'keep global config')

    def test_symlink_companion_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            top=Path(temp);home=top/'home';(home/'skills').mkdir(parents=True)
            real=top/'real';real.mkdir();(real/'SKILL.md').write_text('user data')
            (home/'skills/code-review').symlink_to(real, target_is_directory=True)
            result=self.command(home,'--only','code-review','--apply','--replace')
            self.assertNotEqual(result.returncode,0)
            self.assertEqual((real/'SKILL.md').read_text(),'user data')
            self.assertTrue((home/'skills/code-review').is_symlink())

if __name__ == '__main__':
    unittest.main()
