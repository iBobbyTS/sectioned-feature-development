"""Maintainer-only contract tests. No Agent/model behavior is evaluated here."""
from pathlib import Path
import hashlib
import json
import re
import tomllib
import unittest

R=Path(__file__).resolve().parents[1]
S=R/'skill/sectioned-feature-development'
K=S/'references/planning'
H=R/'docs/version-history/v4.5.3'
B=json.loads((H/'appendix/INPUT-HASHES.json').read_text())
CASES=json.loads((R/'tests/fixtures/planning-routing-v453.json').read_text())
C={c['id']:c for c in CASES['cases']}
INDEXES=['domains/INDEX.md','languages/INDEX.md','adapters/INDEX.md','concerns/INDEX.md']

def t(p): return p.read_text()
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()

class ExplicitRouting453Tests(unittest.TestCase):
    def test_mode_is_named_at_each_live_entry(self):
        for rel in ['SKILL.md','references/activation-and-orchestration.md',
                    'references/parallel-execution.md','references/artifact-lifecycle.md',
                    'assets/PLAN-FULL.template.md','assets/FEATURE-STATE.template.md']:
            self.assertIn('EXECUTE_WITH_COMMITS',t(S/rel),rel)
            self.assertNotIn('requires the last mode',t(S/rel),rel)
        self.assertIn('before the next product/test edit',t(S/'SKILL.md'))
        self.assertIn('coherent implementation/repair commits',t(S/'references/artifact-lifecycle.md'))

    def test_both_thresholds_and_no_commit_conflict_remain(self):
        for rel in ['SKILL.md','references/activation-and-orchestration.md','references/parallel-execution.md']:
            text=t(S/rel)
            self.assertRegex(text,r'More than one business section.*more than one executable subsection')
            self.assertRegex(text,r'non-main.*feature branch|feature branch.*non-main')
            self.assertIn('no-commit',text)
        self.assertIn('多于一个业务 section 或多于一个可执行 subsection',t(S/'assets/PLAN-FULL.template.md'))

    def test_plan_only_and_commit_granularity_not_redefined(self):
        root=t(S/'SKILL.md')
        self.assertIn('`PLAN_ONLY` permits planning/review only',root)
        self.assertIn('multi-unit plan may be prepared in `PLAN_ONLY`',root)
        self.assertIn('每节恰好一个 commit',t(R/'README.md'))
        self.assertIn('do not commit',t(S/'references/artifact-lifecycle.md'))

    def test_positional_directives_replaced_with_actual_objects(self):
        root=t(S/'SKILL.md')
        self.assertIn('`FINAL_ANSWER` controls',root)
        self.assertNotIn('the latter controls',root)
        self.assertIn('Only a model/semantic error supports changing implementation models',t(S/'references/model-routing.md'))
        self.assertIn('If the feature remains correct without the proposed mechanism',t(S/'references/scope-control.md'))
        for rel in ['SKILL.md','references/scope-control.md','references/model-routing.md','references/section-planning.md']:
            self.assertNotRegex(t(S/rel),r'requires the last mode|If the last answer is yes|Only the first supports|the latter (controls|needs|is not solved)')

    def test_four_catalogs_exist_and_root_links_all(self):
        for index in INDEXES:
            self.assertTrue((K/index).is_file())
            self.assertIn('references/planning/'+index,t(S/'SKILL.md'))
            self.assertIn(index,t(K/'router.md'))
        self.assertIn('all four short catalogs',t(S/'SKILL.md'))

    def test_catalogs_list_existing_guides_and_coverage_is_unchanged(self):
        expected={'domains':14,'languages':20,'adapters':19,'concerns':4}
        for axis,count in expected.items():
            file=K/axis/'INDEX.md'
            links=re.findall(r'\[[^\]]*\]\(([^)]+\.md)\)',t(file))
            guides=[(file.parent/link).resolve() for link in links if not link.startswith('..')]
            self.assertEqual(len(guides),count,axis)
            self.assertEqual(len(set(guides)),count,axis)
            self.assertTrue(all(p.is_file() for p in guides),axis)
        self.assertEqual(len(list((K/'concerns').glob('*.md'))),5)

    def test_router_order_and_no_universal_shortcut(self):
        router=t(K/'router.md')
        self.assertIn('Read all four short indexes first',router)
        self.assertIn('read matching specialized guides next',router)
        self.assertIn('universal only for the uncovered part',router)
        self.assertIn('opening universal without checking the catalogs does not satisfy',router)
        self.assertIn('do not skip an applicable guide because the task seems familiar',router)
        self.assertIn('Use only after',t(K/'universal.md'))
        self.assertNotIn('Use for every activated PLAN',t(K/'universal.md'))

    def test_nonmatch_overlap_and_partial_fallback_are_distinct(self):
        router=t(K/'router.md')
        for term in ['NOT_APPLICABLE','COVERED_BY','UNMATCHED','it does not require universal',
                     'A missing guide for one axis never cancels matches in another axis',
                     'Missing a playbook is not a blocker']:
            self.assertIn(term,router)

    def test_native_plan_reviewer_has_same_policy_and_role(self):
        role=tomllib.loads(t(R/'agents/plan_reviewer.toml'))
        instructions=role['developer_instructions']
        for index in INDEXES:self.assertIn(index,instructions)
        for term in ['Inspect all four short catalogs','only for a specifically named uncovered part',
                     'NATIVE_CODEX only','single pass','Do not use the author']:
            self.assertIn(term,instructions)
        self.assertNotIn('Do not preload indexes',instructions)
        self.assertEqual(role['model'],'gpt-6-astra')
        self.assertEqual(role['model_reasoning_effort'],'xhigh')
        self.assertEqual(role['sandbox_mode'],'read-only')

    def test_plan_author_review_packet_and_external_challenge_connected(self):
        for rel in ['references/artifact-lifecycle.md','references/section-planning.md',
                    'assets/PLAN-REVIEW-REQUEST.template.md','assets/EXTERNAL-REVIEW-PACKET.template.md']:
            text=t(S/rel)
            self.assertRegex(text,r'four.*catalog')
            self.assertRegex(text,r'universal only|universal is only')
        self.assertIn('A code-only DELTA does not reload',t(S/'assets/EXTERNAL-REVIEW-PACKET.template.md'))

    def test_existing_plan_carries_routing_not_new_report(self):
        template=t(S/'assets/PLAN-FULL.template.md')
        for value in ['四维目录已检查','Universal fallback','not needed','NOT_APPLICABLE','COVERED_BY']:
            self.assertIn(value,template)
        router=t(K/'router.md')
        self.assertIn('No JSON, route validator, hash approval or separate report',router)
        self.assertIn('not run a route-completeness gate',router)
        self.assertIn('No requirement to select an entry from every axis',router)

    def test_reuse_and_delta_remain_bounded(self):
        router=t(K/'router.md')
        for term in ['Reuse catalogs/guides already read completely',
                     'do not reread them per section or dispatch',
                     'PLAN_DELTA reloads only changed routes',
                     'No reopening accepted work']:
            self.assertIn(term,router)
        self.assertIn('More routes do not change model tiers',router)

    def test_current_cases_are_manual_not_model_runs(self):
        self.assertFalse(CASES['automatic_model_evaluation_performed'])
        self.assertFalse(CASES['runtime_router_added'])
        self.assertEqual(CASES['inspect_first'],['router.md']+INDEXES)
        self.assertEqual(len(C),8)
        for c in C.values():
            self.assertTrue(c['evidence'])
            self.assertNotIn('universal.md',c['read'])
            self.assertFalse(set(c['read']) & set(c['exclude']))
            for path in c['read']+c['exclude']:self.assertTrue((K/path).is_file(),path)

    def test_complete_match_does_not_default_to_universal(self):
        for id in ['svelte-java','sveltekit-not-java','python-cli','rust-tokio']:
            self.assertFalse(C[id]['universal_for'])
        self.assertIn('languages/java.md',C['svelte-java']['read'])
        self.assertIn('languages/java.md',C['sveltekit-not-java']['exclude'])

    def test_partial_gap_keeps_matched_guides(self):
        c=C['partial-unknown']
        self.assertTrue(c['universal_for'])
        self.assertIn('domains/full-stack.md',c['read'])
        self.assertIn('adapters/frameworks/svelte-sveltekit.md',c['read'])
        self.assertFalse(C['no-specific-match']['read'])
        self.assertTrue(C['no-specific-match']['universal_for'])
        self.assertIn('adapters/platforms/macos.md',C['swift-server']['exclude'])

    def test_runtime_scripts_installer_companion_and_history_preserved(self):
        prefixes=('skill/sectioned-feature-development/scripts/','scripts/','skill/code-review/','docs/version-history/')
        for rel,sha in B.items():
            if rel.startswith(prefixes):self.assertEqual(h(R/rel),sha,rel)
        for name in ['workflow.py','execution_artifacts.py','advisor_flow.py','planning_router.py','routing_gate.py']:
            self.assertFalse((S/'scripts'/name).exists())

    def test_specialized_content_and_six_other_agents_unchanged(self):
        for rel,sha in B.items():
            if (rel.startswith('agents/') and not rel.endswith('plan_reviewer.toml')) or (
                '/references/planning/' in rel and not rel.endswith(('router.md','universal.md','examples.md','INDEX.md'))):
                self.assertEqual(h(R/rel),sha,rel)

    def test_audit_452_core_and_delivery_rules_preserved(self):
        self.assertEqual(h(S/'references/audit-mode.md'),B['skill/sectioned-feature-development/references/audit-mode.md'])
        root=t(S/'SKILL.md')
        for term in ['Audit remains LIVE by default','before planning or resumed dispatch',
                     'only then send the final feature-delivery response',
                     'No actual ZAS means NOT_USED','No `.sha256` sidecars',
                     'Audit gaps never require another reviewer, test, repair, Advisor or ZAS call']:
            self.assertIn(term,root)
        state=t(S/'assets/FEATURE-STATE.template.md')
        self.assertIn('Product COMPLETED does not erase Audit PENDING',state)
        self.assertIn('Next is not none while packaging remains',state)

if __name__=='__main__':unittest.main()
