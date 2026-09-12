"""Offline documentation/preservation regressions; not model-behavior evaluations.

No runtime Audit scheduling/enforcement code is added by these tests.
"""
import hashlib
import json
from pathlib import Path
import unittest

R = Path(__file__).resolve().parents[1]
S = R / 'skill/sectioned-feature-development'
H = R / 'docs/version-history/v4.5.2'
BASE = json.loads((H/'appendix/INPUT-HASHES.json').read_text())
AUDIT_FILES = {
    'SKILL.md', 'references/artifact-lifecycle.md',
    'assets/FEATURE-STATE.template.md', 'references/audit-mode.md',
}


def text(rel):
    return (S/rel).read_text()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AuditHandoff452Tests(unittest.TestCase):
    def test_audit_is_an_entry_and_final_step_in_the_root(self):
        root = text('SKILL.md')
        self.assertIn('before planning or resumed dispatch', root)
        self.assertLess(root.index('## Audit handoff'), root.index('## Stop before dispatch'))
        self.assertIn('only then send the final feature-delivery response', root)
        self.assertIn('Audit remains LIVE by default', root)

    def test_opt_out_is_explicit_not_a_task_size_or_session_inference(self):
        root = text('SKILL.md')
        self.assertIn('only an explicit user `audit off` disables it', root)
        for term in ['one section', 'no-commit mode', '`continue`', 'new session']:
            self.assertIn(term, root)
        self.assertIn('never silently opts out', root)

    def test_reference_is_read_once_not_at_every_dispatch(self):
        root = text('SKILL.md')
        self.assertIn('read once per fresh context before planning/resumed dispatch', root)
        self.assertIn('Do not reread the full reference at every dispatch', root)
        self.assertIn('[audit-mode.md](audit-mode.md)', text('references/artifact-lifecycle.md'))

    def test_state_keeps_pending_independent_of_product_status(self):
        state = text('assets/FEATURE-STATE.template.md')
        for term in ['Audit mode:', 'Audit scope:', 'Audit delivery:', 'Audit next:',
                     'Main ZIP:', 'ZAS companion:']:
            self.assertIn(term, state)
        self.assertIn('Product COMPLETED does not erase Audit PENDING', state)
        self.assertIn('do not rewrite state on every poll', state)

    def test_takeover_inherits_existing_feature_and_does_not_invent_history(self):
        lifecycle = text('references/artifact-lifecycle.md')
        for term in ['After compaction or takeover', 'same feature', 'source-session pointers',
                     'not implicit OFF', 'permission to manufacture past events',
                     'absence before packaging is not a dispatch gate']:
            self.assertIn(term, lifecycle)

    def test_close_product_but_do_not_erase_pending_delivery(self):
        lifecycle = text('references/artifact-lifecycle.md')
        self.assertIn('mark the business PLAN closed', lifecycle)
        self.assertIn('Product completion is not Audit delivery', lifecycle)
        self.assertIn('Do not set `Next: none` while this obligation remains', lifecycle)

    def test_final_outcomes_require_real_evidence_including_unavailable_tools(self):
        audit = text('references/audit-mode.md')
        for term in ['**COMPLETE:**', '**OFF:**', '**AUDIT_PACK_INCOMPLETE:**',
                     'COMPLETE_WITH_GAPS', 'at most one bounded artifact-only correction',
                     'If invocation was impossible', 'instead of inventing a validator failure']:
            self.assertIn(term, audit)

    def test_zas_pair_is_required_only_when_used_and_no_sidecar(self):
        root = text('SKILL.md')
        self.assertIn('No actual ZAS means NOT_USED', root)
        self.assertIn('No `.sha256` sidecars', root)
        self.assertIn('missing/stale required companion is incomplete', root)
        self.assertIn('xxx-zas.zip', root)

    def test_not_every_pause_or_status_reply_creates_a_zip(self):
        audit = text('references/audit-mode.md')
        self.assertIn('Ordinary status replies, owner pauses and interruptions preserve PENDING', audit)
        self.assertIn('no ZIP is required per turn', audit)
        self.assertIn('not required on every development status reply', audit)

    def test_capture_is_real_once_and_not_a_second_worker_project(self):
        audit = text('references/audit-mode.md')
        self.assertIn('workers return their actual work/check results and do not build separate audit packs', audit)
        self.assertIn('or append through `scripts/audit_trace.py` when convenient', audit)
        self.assertIn('not prose placeholders', audit)
        self.assertIn('Do not trace every file read', audit)
        self.assertIn('written by the finalizer, not a startup prerequisite', audit)

    def test_new_requests_do_not_absorb_pending_old_audit_or_old_clean(self):
        root = text('SKILL.md')
        self.assertIn('neither erases the original pending audit nor inherits its earlier CLEAN', root)
        lifecycle = text('references/artifact-lifecycle.md')
        self.assertIn('not the later worktree disguised as the earlier candidate', lifecycle)
        self.assertIn('No automatic re-audit of already delivered historical tasks', lifecycle)

    def test_no_extra_product_work_for_audit(self):
        root = text('SKILL.md')
        self.assertIn('Audit gaps never require another reviewer, test, repair, Advisor or ZAS call', root)
        self.assertIn('Do not restore JSON state, actor receipts, approval hashes or ready/register/approve gates', root)
        for name in ['workflow.py','execution_artifacts.py','advisor_flow.py','audit_gate.py']:
            self.assertFalse((S/'scripts'/name).exists())

    def test_runtime_helpers_installer_agents_companion_and_knowledge_unchanged(self):
        prefixes = ('skill/sectioned-feature-development/scripts/', 'scripts/', 'agents/',
                    'skill/code-review/', 'skill/sectioned-feature-development/references/planning/')
        for rel, expected in BASE.items():
            if rel.startswith(prefixes):
                self.assertEqual(digest(R/rel), expected, rel)
        expected_scripts = {rel for rel in BASE if rel.startswith('skill/sectioned-feature-development/scripts/')}
        actual_scripts = {p.relative_to(R).as_posix() for p in (S/'scripts').rglob('*')
                          if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
        self.assertEqual(expected_scripts, actual_scripts)

    def test_old_history_local_csv_and_other_skill_files_preserved(self):
        for rel, expected in BASE.items():
            if rel.startswith('docs/version-history/'):
                self.assertEqual(digest(R/rel), expected, rel)
            if rel.startswith('skill/sectioned-feature-development/'):
                short=rel.removeprefix('skill/sectioned-feature-development/')
                if short not in AUDIT_FILES | {'VERSION'}:
                    self.assertEqual(digest(R/rel), expected, rel)

    def test_release_version_primary_only(self):
        self.assertEqual((R/'VERSION').read_text().strip(), '4.5.2')
        self.assertEqual((S/'VERSION').read_text().strip(), '4.5.2')
        self.assertIn('sfd-delegated-review/4.2', (R/'skill/code-review/references/delegated-pass.md').read_text())


if __name__ == '__main__':
    unittest.main()
