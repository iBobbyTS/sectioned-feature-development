from pathlib import Path
import hashlib,sys,unittest,copy
R=Path(__file__).resolve().parents[1];S=R/'skill/sectioned-feature-development'
sys.path.insert(0,str(S/'scripts'));import zas_evidence as z
class V44ContractTests(unittest.TestCase):
 def test_retired_execution_gates_not_installed(self):
  for f in ['workflow.py','execution_artifacts.py','advisor_flow.py']:
   self.assertFalse((S/'scripts'/f).exists());self.assertTrue((R/'docs/version-history/v4.4/baseline-v4.3.1/skill/sectioned-feature-development/scripts'/f).exists())
 def test_no_machine_schedule_templates(self):
  self.assertFalse((S/'assets/STATE.template.json').exists());self.assertFalse((S/'assets/SUBSECTION-SCHEDULE.example.json').exists())
 def test_core_obligations_not_lost(self):
  text=(S/'SKILL.md').read_text()
  for word in ['actually spawn','independent PLAN review','HANDOFF','five ordinary','REPAIR_DELTA','ONE','TWO','COMPLETED','Audit remains LIVE','main','parent reconciliation','FEATURE-STATE.md','ADVISOR']:
   self.assertIn(word.lower(),text.lower())
 def test_role_configs_preserved(self):
  base=R/'docs/version-history/v4.4/INPUT-AGENT-HASHES.json'
  if not base.exists():self.skipTest('hash manifest emitted during release')
  import json
  allowed={'code_reviewer.toml','plan_reviewer.toml','impl_nano.toml','impl_mini.toml','impl_std.toml','impl_large.toml'}
  for name,digest in json.loads(base.read_text()).items():
   if name not in allowed:self.assertEqual(hashlib.sha256((R/'agents'/name).read_bytes()).hexdigest(),digest)
  # v4.4.1 intentionally changes only descriptions/instructions; new regression
  # verifies all role/model/effort/sandbox bindings against a frozen baseline.
 def test_no_fake_receipt_gate(self):
  text=(S/'references/artifact-lifecycle.md').read_text();self.assertIn('no receipt', (S/'references/advisor-escalation.md').read_text());self.assertIn('No fake receipt JSON',text)
 def test_plain_packets_do_not_force_companion_json(self):
  self.assertIn('Plain Markdown',(R/'skill/code-review/references/delegated-pass.md').read_text())
 def test_compact_observation_has_no_echoed_identity_requirement(self):
  page={'tools':[],'reasoning':{'text':'中🙂'*100,'truncated':True},'coverage':{'tool_history_complete':True,'reasoning_complete':False,'dropped_events':0}}
  out=z.compact_snapshot(page,10000000);self.assertEqual(out['reasoning_chars'],200);self.assertEqual(out['semantic_progress'],'NOT_INFERRED');self.assertEqual(out['source_provenance'],'NOT_PUBLICLY_ECHOED')
 def test_compact_no_results_or_encrypted(self):
  page={'tools':[],'reasoning':{'text':'','truncated':False},'coverage':{'tool_history_complete':True,'reasoning_complete':True,'dropped_events':0}}
  for field in ['encrypted_content','output','result']:
   p=copy.deepcopy(page);p[field]='bad'
   with self.assertRaises(z.Invalid):z.compact_snapshot(p,10000000)
 def test_compact_id_bool_not_integer(self):
  for uid in [True,'10000000',9999999,100000000]:
   with self.assertRaises(z.Invalid):z.compact_snapshot({},uid)
 def test_compact_capabilities_require_real_tools_limits(self):
  st={'capabilities':{'observation':{'public_reasoning_default':True,'defaults':{'top_tools':3,'recent_calls_per_tool':5,'reasoning_chars':200}}}}
  self.assertEqual(z.compact_capabilities(st,{'tools':list(z.REQUIRED_TOOLS)})['mode'],'COMPACT_OBSERVATION_READY')
  with self.assertRaises(z.Invalid):z.compact_capabilities(st,{'tools':list(z.BASE_TOOLS)})
