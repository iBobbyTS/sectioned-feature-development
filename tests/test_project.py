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
  self.assertEqual(len(ps),8);self.assertEqual(len({(x['model'],x['model_reasoning_effort']) for x in ps}),6)
  for x in ps:
   for k in ['name','description','developer_instructions','sandbox_mode']:self.assertTrue(x[k])
   self.assertNotIn('fork_context',x)
  advisor=next(x for x in ps if x['name']=='advisor');self.assertEqual(advisor['model'],'gpt-6-astra');self.assertEqual(advisor['sandbox_mode'],'read-only')
 def test_exact_advisor_contract_hash(self):
  import hashlib,json
  spec=json.loads((R/'docs/version-history/4.1/ADVISOR_CONTRACT_PRESERVATION.json').read_text())
  p=R/'skill/sectioned-feature-development/assets/ADVISOR-REQUEST.template.md'
  self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),spec['input_sha256'])
 def test_current_tool_family_only_in_adapter(self):
  t=(R/'skill/sectioned-feature-development/references/zcode.md').read_text()
  used=set(re.findall(r'`(zcode_subagent_[a-z_]+)`',t))
  self.assertEqual(len(used),9)
  self.assertNotIn('`zcode_review_continue`',t)
 def test_active_doc_links(self):
  paths=[R/'README.md',R/'docs/AGENTS.example.md',*(R/'skill').rglob('*.md'),*(R/'docs/version-history/4.1').glob('*.md')]
  for p in paths:
   for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
    if link.startswith(('http','/','~','#')) or '<' in link or '{' in link:continue
    target=link.split('#',1)[0]
    if target:self.assertTrue((p.parent/target).exists(),f'{p}: {target}')
 def test_install_dry_run_and_apply(self):
  with tempfile.TemporaryDirectory() as t:
   home=Path(t)/'codex';cmd=[sys.executable,str(R/'scripts/install.py'),'--codex-home',str(home)]
   subprocess.run(cmd,check=True,capture_output=True);self.assertFalse(home.exists())
   subprocess.run(cmd+['--apply'],check=True,capture_output=True)
   self.assertTrue((home/'agents/advisor.toml').exists());self.assertTrue((home/'skills/sectioned-feature-development/SKILL.md').exists());self.assertTrue((home/'skills/code-review/SKILL.md').exists())
   (home/'AGENTS.md').write_text('preserve policy');(home/'agents/unrelated.toml').write_text('preserve')
   fail=subprocess.run(cmd+['--apply'],capture_output=True);self.assertNotEqual(fail.returncode,0)
   subprocess.run(cmd+['--apply','--replace'],check=True,capture_output=True)
   self.assertEqual((home/'AGENTS.md').read_text(),'preserve policy');self.assertEqual((home/'agents/unrelated.toml').read_text(),'preserve')
   self.assertTrue(list((home/'sfd-backups').glob('*')))
if __name__=='__main__':unittest.main()
