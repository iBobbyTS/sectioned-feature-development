"""Offline documentation/fixture tests only. No model routing or application test is claimed."""
import hashlib
import json
from pathlib import Path
import re
import tomllib
import unittest

R=Path(__file__).resolve().parents[1]
S=R/'skill/sectioned-feature-development'
K=S/'references/planning'
H=R/'docs/version-history/v4.5.1'
INVENTORY=json.loads((H/'appendix/KNOWLEDGE_INVENTORY.json').read_text())
BASE=json.loads((H/'appendix/INPUT-HASHES.json').read_text())
CHANGED_453=set(json.loads((R/'docs/version-history/v4.5.3/appendix/AUTHORIZED-CHANGES.json').read_text()))
CASES=json.loads((R/'tests/fixtures/planning-routing-v451.json').read_text())
C={c['id']:c for c in CASES['cases']}

def t(p):return p.read_text()
def all_selected(c):return {p for group in c['selected'].values() for p in group}

class Taxonomy451Tests(unittest.TestCase):
    def test_axes_exact_coverage(self):
        self.assertEqual(len(list((K/'domains').glob('*.md')))-1,14)
        self.assertEqual(len(list((K/'languages').glob('*.md')))-1,20)
        self.assertEqual(len(list((K/'adapters').glob('*/*.md'))),19)
        self.assertEqual(len([p for p in (K/'concerns').glob('*.md') if p.name != 'INDEX.md']),4)
        self.assertEqual(len(INVENTORY),53)

    def test_domains_have_no_language_framework_platform_files(self):
        for name in ['python','rust','swift','swift-macos','svelte','java','react','macos','android']:
            self.assertFalse((K/'domains'/f'{name}.md').exists())
        self.assertIn('engineering domains',t(K/'router.md'))

    def test_language_and_adapter_kinds_are_explicit(self):
        for row in INVENTORY:
            s=t(K/row['path'])
            if row['axis']=='language':self.assertIn('Axis: `language`',s)
            if row['axis'].startswith('adapter/'):
                self.assertIn(f"Axis: `{row['axis']}`",s)
                kind=row['axis'].split('/')[1]
                self.assertIn({'framework':'frameworks','runtime':'runtimes','platform':'platforms'}[kind],row['path'])

    def test_all_guides_have_scope_and_source(self):
        for row in INVENTORY:
            source=t(K/row['path'])
            self.assertIn('## ',source)
            self.assertRegex(source,r'(?i)exclude|exclusion|scope boundary')
            self.assertIn('https://',source)
            self.assertIn('sources.md',source)
            self.assertTrue(row['sources'])

    def test_indexes_are_bounded_catalogs_not_autoload(self):
        s=t(K/'router.md')
        for value in ['Do not preload','No requirement to select an entry from every axis',
                      'Do not compute a Cartesian product','smallest set of guides','relevant selected guides']:
            self.assertIn(value,s)

    def test_existing_shared_core_and_concerns_unchanged(self):
        paths=['references/planning/boundary-handoff.md']  # Universal entry policy is explicitly changed in 4.5.3.
        paths += [p.relative_to(S).as_posix() for p in (K/'concerns').glob('*.md') if p.name != 'INDEX.md']
        for rel in paths:
            key='skill/sectioned-feature-development/'+rel
            self.assertEqual(hashlib.sha256((S/rel).read_bytes()).hexdigest(),BASE[key],key)

    def test_no_runtime_or_companion_install_changes(self):
        prefixes=('skill/sectioned-feature-development/scripts/','skill/code-review/','scripts/')
        for path,h in BASE.items():
            if path.startswith(prefixes):self.assertEqual(hashlib.sha256((R/path).read_bytes()).hexdigest(),h,path)
        for name in ['workflow.py','execution_artifacts.py','planning_router.py','advisor_flow.py']:
            self.assertFalse((S/'scripts'/name).exists())

    def test_history_kept_exactly(self):
        for path,h in BASE.items():
            if path.startswith('docs/version-history/'):
                self.assertEqual(hashlib.sha256((R/path).read_bytes()).hexdigest(),h,path)

    def test_other_agents_unchanged_no_extra_profiles(self):
        names={p.relative_to(R).as_posix() for p in (R/'agents').glob('*.toml')}
        self.assertEqual(names,{p for p in BASE if p.startswith('agents/') and p.endswith('.toml')})
        for p in names:
            if not p.endswith('plan_reviewer.toml'):
                self.assertEqual(hashlib.sha256((R/p).read_bytes()).hexdigest(),BASE[p])
        reviewer=tomllib.loads(t(R/'agents/plan_reviewer.toml'))
        self.assertIn('Select domains and languages independently',reviewer['developer_instructions'])

    def test_manual_scenarios_not_model_success(self):
        self.assertFalse(CASES['automatic_model_evaluation_performed'])
        self.assertFalse(CASES['runtime_router_added'])
        self.assertGreaterEqual(len(C),30)
        for c in C.values():
            self.assertEqual(set(c['selected']),{'domains','languages','adapters','concerns'})
            self.assertTrue(c['evidence'] and c['oracle'])
            self.assertFalse(all_selected(c)&set(c['exclude']))
            for path in all_selected(c)|set(c['exclude']):self.assertTrue((K/path).is_file(),path)

    def test_same_language_different_domains(self):
        for id in ['python-cli','python-service','python-ml','python-data']:
            self.assertIn('languages/python.md',C[id]['selected']['languages'])
        self.assertEqual(len({tuple(C[id]['selected']['domains']) for id in ['python-cli','python-service','python-ml','python-data']}),4)

    def test_same_domain_multiple_languages(self):
        for id in ['java-service','go-service','python-service','kotlin-server']:
            self.assertIn('domains/backend-services.md',C[id]['selected']['domains'])
        self.assertGreater(len({tuple(C[id]['selected']['languages']) for id in ['java-service','go-service','python-service','kotlin-server']}),2)

    def test_no_example_java_or_host_os_inference(self):
        self.assertIn('languages/java.md',C['sveltekit-only']['exclude'])
        self.assertIn('adapters/platforms/macos.md',C['swift-server']['exclude'])
        self.assertIn('adapters/platforms/macos.md',C['host-not-target']['exclude'])
        self.assertIn('adapters/platforms/android.md',C['kotlin-server']['exclude'])
        self.assertIn('adapters/frameworks/aspnet-core.md',C['csharp-desktop']['exclude'])

    def test_no_rust_tokio_or_cli_browser_inference(self):
        self.assertIn('adapters/runtimes/tokio.md',C['rust-sync']['exclude'])
        self.assertIn('adapters/runtimes/tokio.md',C['rust-tokio']['selected']['adapters'])
        self.assertIn('domains/web-frontend.md',C['typescript-cli']['exclude'])
        self.assertIn('domains/games-realtime.md',C['lua-extension']['exclude'])

    def test_partial_unknown_is_supported_without_substitute(self):
        self.assertTrue(C['partial-unknown']['fallback'])
        self.assertTrue(C['partial-unknown']['selected']['adapters'])
        self.assertIn('languages/java.md',C['partial-unknown']['exclude'])
        self.assertFalse(C['unknown-domain']['selected']['languages'])
        self.assertTrue(C['unknown-domain']['selected']['concerns'])
        self.assertIn('Missing a playbook is not a blocker',t(K/'router.md'))

    def test_old_framework_rules_relocated(self):
        self.assertIn('historical',t(K/'adapters/frameworks/django.md'))
        self.assertIn('on_commit',t(K/'adapters/frameworks/django.md'))
        self.assertIn('self-invocation',t(K/'adapters/frameworks/spring.md'))
        self.assertIn('kill_on_drop',t(K/'adapters/runtimes/tokio.md'))
        self.assertIn('Child termination',t(K/'adapters/runtimes/tokio.md'))
        self.assertIn('AppKit are not interchangeable',t(K/'adapters/frameworks/swiftui-appkit.md'))
        self.assertIn('ActionResult',t(K/'adapters/frameworks/svelte-sveltekit.md'))

    def test_no_new_completion_gate_or_language_rank_claim(self):
        source=t(K/'router.md')
        self.assertIn('More routes do not change model tiers',source)
        self.assertIn('not requirement authority',source)
        self.assertIn('not run a route-completeness gate',source)
        self.assertIn('不是精确排名',t(R/'README.md'))

    def test_source_registry_and_guide_sources_match(self):
        data=json.loads(t(H/'appendix/SOURCES.json'))
        for row in INVENTORY:
            for key in row['sources']:self.assertIn(key,data)

if __name__=='__main__':unittest.main()
