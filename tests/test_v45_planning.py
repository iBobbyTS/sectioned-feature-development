"""Maintainer contract tests only; these do not execute/evaluate a model router."""
from pathlib import Path
import hashlib
import json
import re
import tomllib
import unittest

R = Path(__file__).resolve().parents[1]
S = R / 'skill/sectioned-feature-development'
K = S / 'references/planning'
P = json.loads((R/'docs/version-history/v4.5/appendix/PRESERVATION.json').read_text())

def text(path):
    return path.read_text(encoding='utf-8')

class V45PlanningKnowledgeTests(unittest.TestCase):
    def test_complete_library_is_markdown_only(self):
        inventory=json.loads(text(R/'docs/version-history/v4.5.1/appendix/KNOWLEDGE_INVENTORY.json'))
        expected={row['path'] for row in inventory} | {
            'router.md','universal.md','boundary-handoff.md','examples.md','sources.md',
            'domains/INDEX.md','languages/INDEX.md','adapters/INDEX.md',
            'concerns/data-evolution.md','concerns/async-lifecycle.md',
            'concerns/external-integration.md','concerns/performance.md'}
        self.assertEqual({p.relative_to(K).as_posix() for p in K.rglob('*') if p.is_file()}, expected)

    def test_root_and_section_planning_route_to_library(self):
        self.assertIn('references/planning/router.md',text(S/'SKILL.md'))
        source=text(S/'references/section-planning.md')
        self.assertIn('planning/router.md',source)
        self.assertIn('not an extra review, pass, script or user approval',source)

    def test_composition_does_not_imply_java_or_new_gates(self):
        source=text(K/'router.md')
        for snippet in ['all applicable','ONE PLAN','not requirement authority','not evidence that LMDO uses Java',
                        'More routes do not change model tiers','No JSON, route validator, hash approval']:
            self.assertIn(snippet,source)

    def test_unmatched_and_partial_match_fallback(self):
        for filename in ['router.md','universal.md']:
            self.assertIn('unknown',text(K/filename).lower())
        self.assertIn('Missing a playbook is not a blocker',text(K/'router.md'))
        self.assertIn('Svelte + an unknown backend',text(K/'examples.md'))

    def test_only_actual_version_boundary_gets_public_lookup(self):
        source=text(K/'router.md')
        self.assertIn('Use bundled knowledge by default',source)
        self.assertIn('concrete unresolved/version-sensitive seam',source)
        self.assertIn('Installed source/configuration wins',source)
        self.assertIn('Do not upgrade dependencies',source)

    def test_producer_consumer_share_real_contract_without_prerun_claim(self):
        source=text(K/'boundary-handoff.md')
        for snippet in ['OBSERVED', 'SOURCE_INSPECTED', 'PLANNED', 'UNKNOWN',
                        'same contract/fixture', 'real request builder/decoder',
                        'never weaken business requirements to copy a broken current fixture']:
            self.assertIn(snippet,source)
        self.assertIn('One concrete success',source)

    def test_templates_and_lifecycle_carry_contract(self):
        self.assertIn('规划知识路由与边界样例',text(S/'assets/PLAN-FULL.template.md'))
        self.assertIn('Consumer uses that same contract',text(S/'assets/TASK-PACKET.template.md'))
        self.assertIn('actual redacted request/response fixture',text(S/'assets/SECTION-HANDOFF.template.md'))
        lifecycle=text(S/'references/artifact-lifecycle.md')
        self.assertIn("actual producer handoff's wire/serialization/result contract",lifecycle)
        self.assertIn('do not pass the entire library or research conversation',lifecycle)

    def test_plan_reviewer_still_native_independent_and_one_pass(self):
        role=tomllib.loads(text(R/'agents/plan_reviewer.toml'))
        for snippet in ['NATIVE_CODEX only','never author it','references/planning/router.md',
                        'single pass','No extra reviewer, receipt, route script']:
            self.assertIn(snippet,role['developer_instructions'])
        self.assertIn('read-only',role['sandbox_mode'])
        self.assertIn('No clean streak, third full pass',text(S/'references/section-planning.md'))

    def test_external_plan_packet_not_prior_verdict(self):
        source=text(S/'assets/EXTERNAL-REVIEW-PACKET.template.md')
        self.assertIn('For a PLAN challenge only',source)
        self.assertIn("not the native reviewer's verdict",source)
        self.assertIn('A code-only DELTA does not reload',source)

    def test_audit_observes_without_new_report_or_repair(self):
        source=text(S/'references/audit-mode.md').split('## 4.5 planning knowledge observations',1)[1]
        for snippet in ['not a new mandatory report or gate','ROUTE_MISSED','PLAN_OMISSION',
                        'PLAN_ALREADY_REQUIRED_BUT_NOT_IMPLEMENTED','EVIDENCE_GAP',
                        'not new admission classes','Do not request extra agents, rerun checks']:
            self.assertIn(snippet,source)

    def test_companion_is_exactly_unchanged(self):
        files={p.relative_to(R).as_posix() for p in (R/'skill/code-review').rglob('*') if p.is_file()}
        self.assertEqual(files,set(P['unchanged_companion']))
        for path,expected in P['unchanged_companion'].items():
            self.assertEqual(hashlib.sha256((R/path).read_bytes()).hexdigest(),expected,path)

    def test_only_plan_reviewer_text_changed_all_bindings_preserved(self):
        for name,old in P['agents'].items():
            new=tomllib.loads(text(R/'agents'/name))
            if name=='plan_reviewer.toml':
                self.assertEqual(new.keys(),old.keys())
                for k in new:
                    if k!='developer_instructions': self.assertEqual(new[k],old[k],(name,k))
                self.assertTrue(new['developer_instructions'].startswith(old['developer_instructions']))
            else: self.assertEqual(new,old,name)

    def test_manual_routing_cases_are_not_reported_as_agent_runs(self):
        fixture=json.loads(text(R/'tests/fixtures/planning-routing-v45.json'))
        self.assertFalse(fixture['automatic_model_evaluation_performed'])
        self.assertEqual(fixture['common_load'],['router.md','universal.md'])
        self.assertEqual(len(fixture['cases']),12)
        for case in fixture['cases']:
            self.assertTrue(case['evidence'] and case['oracle'])
            self.assertFalse(set(case['load']) & set(case['exclude']))
            for path in case['load']+case['exclude']: self.assertTrue((K/path).is_file(),path)
        cases={c['id']:c for c in fixture['cases']}
        self.assertIn('languages/java.md',cases['svelte-java']['load'])
        self.assertIn('languages/java.md',cases['sveltekit-only']['exclude'])

    def test_no_previous_baseline_copies_or_new_schedule_engine(self):
        historical=R/'docs/version-history'
        self.assertFalse(any(p.is_dir() and p.name.startswith('baseline-v') for p in historical.rglob('*')))
        for name in ['workflow.py','execution_artifacts.py','advisor_flow.py','planning_router.py']:
            self.assertFalse((S/'scripts'/name).exists())

    def test_version_is_primary_only_no_companion_protocol_bump(self):
        self.assertEqual(text(R/'VERSION').strip(),'4.5.1')
        self.assertEqual(text(S/'VERSION').strip(),'4.5.1')
        self.assertIn('sfd-delegated-review/4.2',text(R/'skill/code-review/references/delegated-pass.md'))

    def test_preserves_local_native_final_event_condition(self):
        root=text(S/'SKILL.md')
        for snippet in ['Message Type: FINAL_ANSWER','subAgentActivity.kind=completed',
                        'If an earlier `MESSAGE` conflicts with `FINAL_ANSWER`, the latter controls']:
            self.assertIn(snippet,root)

    def test_sources_are_optional_and_evidence_limit_explicit(self):
        source=text(K/'sources.md')
        self.assertIn('not mandatory context for each worker',source)
        self.assertIn('Rolling docs have no invented publication date',source)
        self.assertIn('no performance improvement is claimed as measured',source)

if __name__=='__main__':
    unittest.main()
