"""Offline instruction/configuration and preservation checks; not model-behavior evals."""
from pathlib import Path
import hashlib
import json
import tomllib
import unittest

R = Path(__file__).resolve().parents[1]
S = R / 'skill/sectioned-feature-development'
C = R / 'skill/code-review'
V = R / 'docs/version-history/v4.5/appendix'
BASE = json.loads((V/'PRESERVATION.json').read_text())

def text(path):
    return path.read_text()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

class V441HandoffContractTests(unittest.TestCase):
    def test_runtime_helpers_and_installer_are_unchanged(self):
        scripts = {p.relative_to(R).as_posix() for p in (S/'scripts').glob('*.py')}
        self.assertEqual(scripts, set(BASE['runtime_scripts']))
        for name, value in BASE['runtime_scripts'].items():
            self.assertEqual(digest(R/name), value, name)
        self.assertEqual(digest(R/'scripts/install.py'), BASE['installer_sha256'])

    def test_history_and_unrelated_policies_unchanged(self):
        for name, value in {**BASE['unchanged_history'], **BASE['unchanged_policy_files']}.items():
            self.assertEqual(digest(R/name), value, name)

    def test_seven_roles_bindings_stay_the_same(self):
        current = {p.name:tomllib.loads(text(p)) for p in (R/'agents').glob('*.toml')}
        self.assertEqual(set(current), set(BASE['agents']))
        for name, old in BASE['agents'].items():
            for key in ['name','model','model_reasoning_effort','sandbox_mode']:
                self.assertEqual(current[name][key], old[key], (name,key))
            self.assertLessEqual(set(k for k in current[name] if current[name][k] != old.get(k)),
                                 {'description','developer_instructions'})
        self.assertEqual(current['code_explorer.toml'], BASE['agents']['code_explorer.toml'])

    def test_plan_barrier_precedes_dispatch_and_includes_parallel_roots(self):
        root=text(S/'SKILL.md')
        self.assertLess(root.index('## Stop before dispatch'),root.index('## How much to read'))
        for snippet in ['Global PLAN barrier','before spawning any product/test implementer',
                        'selected GLM challenge','early candidate','Do not pre-spawn']:
            self.assertIn(snippet, root)
        parallel=text(S/'references/parallel-execution.md')
        self.assertIn('before **any** product/test implementer',parallel)
        self.assertNotIn('before any dependent product implementation',parallel)

    def test_serial_acceptance_not_process_completion(self):
        root=text(S/'SKILL.md')
        for snippet in ['initial review CLEAN is not S01 accepted',
                        'BLOCKED, ABANDONED or cancelled review does not satisfy a dependency',
                        'A bounded repair of the current unit is allowed']:
            self.assertIn(snippet,root)
        self.assertNotIn('accepted, blocked, or abandoned',text(S/'references/bounded-review.md'))

    def test_subsection_waits_for_live_review_and_closure(self):
        source=text(S/'references/subsections.md')
        self.assertIn('No next same-parent child',source)
        self.assertIn('checkpoint reviewer/delta is live',source)
        self.assertIn('Stop/cancel is not CHECKPOINT_VERIFIED',source)
        self.assertIn('No fresh independent final per child',source)

    def test_parallel_is_explicit_without_new_schema(self):
        source=text(S/'references/parallel-execution.md')
        self.assertIn('both are explicitly named',source)
        self.assertIn('no new schema',source)
        self.assertIn('Default is serial',source)
        self.assertIn('S02 may overlap only if',source)
        self.assertIn('Existing explicit parallel plans need no format migration',source)

    def test_native_discovery_cannot_alias_zas(self):
        role=tomllib.loads(text(R/'agents/code_reviewer.toml'))
        self.assertIn('Native Codex/Astra code reviewer only',role['description'])
        self.assertIn('never ZCode or a ZAS MCP alias',role['description'])
        self.assertIn('Do not call zcode_subagent_spawn',role['developer_instructions'])
        plan=tomllib.loads(text(R/'agents/plan_reviewer.toml'))
        self.assertIn('Native Codex PLAN reviewer',plan['description'])
        self.assertIn('only main can admit findings and release S01',plan['developer_instructions'])

    def test_all_impls_have_early_dispatch_stop_without_receipts(self):
        for p in (R/'agents').glob('impl_*.toml'):
            d=tomllib.loads(text(p))
            self.assertIn('WAITING_FOR_REVIEW',d['developer_instructions'])
            self.assertIn('without product/test edits',d['developer_instructions'])
            self.assertIn('Do not demand machine receipts',d['developer_instructions'])

    def test_provider_schedule_and_id_namespaces_preserved(self):
        source=text(S/'references/external-reviewer-orchestration.md')
        for snippet in ['Astra → ZCode → Astra', 'feature-local',
                        'actual API calls use the original raw ID',
                        'not a native-plus-external stack',
                        'same logical slot', 'REVIEW_ROUTE_MISMATCH']:
            self.assertIn(snippet,source)
        self.assertIn('TERMINAL_CONTINUATION_UNSUPPORTED',source)

    def test_companion_does_not_own_release_or_transport(self):
        root=text(C/'SKILL.md');delegated=text(C/'references/delegated-pass.md')
        self.assertIn('`$code-review` is this review method',root)
        self.assertIn('specifically the native Codex/Astra role',root)
        self.assertIn('never launch or authorize the next implementation',root)
        self.assertIn('sfd-delegated-review/4.2',delegated)
        self.assertIn('No machine receipt',text(S/'assets/REVIEW-PACKET.template.md'))

    def test_prose_handoff_reuses_existing_records(self):
        state=text(S/'assets/FEATURE-STATE.template.md')
        task=text(S/'assets/TASK-PACKET.template.md')
        self.assertIn('native-or-ZAS route + raw returned ID',state)
        self.assertIn('do not rewrite state on every poll',state)
        self.assertIn('Parent dispatch handoff',task)
        self.assertIn('No fake receipt JSON',text(S/'references/artifact-lifecycle.md'))

    def test_ordinary_plan_correction_still_does_not_demand_fresh_approval(self):
        source=text(S/'references/artifact-lifecycle.md')
        self.assertIn('Ordinary corrections need no latest-hash APPROVED',source)
        self.assertIn('Main can proceed when all admitted material issues are resolved',source)

    def test_audit_only_observes_real_mismatches_and_calls(self):
        source=text(S/'references/audit-mode.md')
        self.assertIn('SEQUENCE_GATE_VIOLATION',source)
        self.assertIn('REVIEW_ROUTE_MISMATCH',source)
        self.assertIn('Only an actual ZAS attempt belongs',source)
        self.assertIn('never add review, validation or dispatch gates',source)

    def test_version_and_frontmatter(self):
        import re
        self.assertEqual(text(R/'VERSION').strip(),'4.5.1')
        self.assertEqual(text(S/'VERSION').strip(),'4.5.1')
        for skill in [S,C]:
            source=text(skill/'SKILL.md')
            match=re.match(r'^---\n(.*?)\n---\n',source,re.S)
            self.assertIsNotNone(match)
            raw=dict(line.split(':',1) for line in match.group(1).splitlines() if line.strip())
            meta={'name':raw['name'].strip(),'description':json.loads(raw['description'].strip())}
            self.assertEqual(set(raw),{'name','description'})
            self.assertEqual(set(meta),{'name','description'})
            self.assertEqual(meta['name'],skill.name)
            self.assertLessEqual(len(meta['description']),1024)
            self.assertLess(len(source.splitlines()),500)

if __name__=='__main__':
    unittest.main()
