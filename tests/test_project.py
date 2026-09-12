from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest

R=Path(__file__).resolve().parents[1]
class ProjectTests(unittest.TestCase):
 def test_agents_exact_six_combinations(self):
  ps=[tomllib.loads(p.read_text()) for p in (R/'agents').glob('*.toml')]
  self.assertEqual(len(ps),7);self.assertEqual(len({(x['model'],x['model_reasoning_effort']) for x in ps}),6)
  for x in ps:
   for k in ['name','description','developer_instructions','sandbox_mode']:self.assertTrue(x[k])
   self.assertNotIn('fork_context',x)
  self.assertEqual({x['name'] for x in ps},{'impl_nano','impl_mini','impl_std','impl_large','plan_reviewer','code_reviewer','code_explorer'})
  self.assertFalse((R/'agents/advisor.toml').exists())
 def test_exact_advisor_contract_hash(self):
  import hashlib,json
  spec=json.loads((R/'docs/version-history/v4.1/ADVISOR_CONTRACT_PRESERVATION.json').read_text())
  p=R/'skill/sectioned-feature-development/assets/ADVISOR-REQUEST.template.md'
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),spec['input_sha256'])
 def test_current_tool_family_only_in_adapter(self):
  t=(R/'skill/sectioned-feature-development/references/zcode-mcp-adapter.md').read_text()
  import json
  actual=json.loads((R/'docs/version-history/v4.3/SOURCE-zcode-subagent-public-api.json').read_text())
  # Input commit 753c9ff already renamed the adapter's public wait tool.
  names={'zcode_subagent_'+n for n in ['status','spawn','wait','list','send','respond','cancel','result','close']}
  self.assertTrue(all(n in t for n in names))
  self.assertIn('zas-observation/1.1',t)
  self.assertNotIn('BETA_BASELINE_LIMITED',t)
  self.assertIn('zcode_subagent_observe',t)
  self.assertNotIn('`zcode_review_continue`',t)
 def test_active_doc_links(self):
  paths=[R/'README.md',R/'docs/AGENTS.example.md',*(R/'skill').rglob('*.md'),*(R/'docs/version-history/4.1').glob('*.md')]
  for p in paths:
   for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
    if link.startswith(('http','/','~','#','subagent://')) or '<' in link or '{' in link:continue
    target=link.split('#',1)[0]
    if target:self.assertTrue((p.parent/target).exists(),f'{p}: {target}')
 def test_install_dry_run_and_apply(self):
  with tempfile.TemporaryDirectory() as t:
   home=Path(t)/'codex';cmd=[sys.executable,str(R/'scripts/install.py'),'--codex-home',str(home)]
   subprocess.run(cmd,check=True,capture_output=True);self.assertFalse(home.exists())
   subprocess.run(cmd+['--apply'],check=True,capture_output=True)
   self.assertFalse((home/'agents/advisor.toml').exists());self.assertTrue((home/'agents/impl_std.toml').exists());self.assertTrue((home/'skills/sectioned-feature-development/SKILL.md').exists());self.assertTrue((home/'skills/code-review/SKILL.md').exists())
   (home/'AGENTS.md').write_text('preserve policy');(home/'agents/unrelated.toml').write_text('preserve')
   fail=subprocess.run(cmd+['--apply'],capture_output=True);self.assertNotEqual(fail.returncode,0)
   subprocess.run(cmd+['--apply','--replace'],check=True,capture_output=True)
   self.assertEqual((home/'AGENTS.md').read_text(),'preserve policy');self.assertEqual((home/'agents/unrelated.toml').read_text(),'preserve')
   self.assertTrue(list((home/'sfd-backups').glob('*')))
 def test_explicit_legacy_retirement_backs_up_exact_names(self):
  with tempfile.TemporaryDirectory() as t:
   home=Path(t)/'codex';(home/'agents').mkdir(parents=True)
   for name in ['implementer_1','implementer_2','implementer_3','implementer_4','advisor','unrelated']:(home/'agents'/f'{name}.toml').write_text('original '+name)
   cmd=[sys.executable,str(R/'scripts/install.py'),'--codex-home',str(home),'--apply','--replace','--retire-legacy-agents']
   subprocess.run(cmd,check=True,capture_output=True)
   self.assertFalse((home/'agents/implementer_1.toml').exists());self.assertFalse((home/'agents/advisor.toml').exists())
   self.assertEqual((home/'agents/unrelated.toml').read_text(),'original unrelated')
   self.assertEqual(next((home/'sfd-backups').glob('*/agents/advisor.toml')).read_text(),'original advisor')
if __name__=='__main__':unittest.main()
