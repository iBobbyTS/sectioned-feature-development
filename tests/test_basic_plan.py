from pathlib import Path
import subprocess,sys,tempfile,unittest
R=Path(__file__).resolve().parents[1];S=R/'skill/sectioned-feature-development'
sys.path.insert(0,str(S/'scripts'));import section_plan as p

BASE='''# PLAN-FULL
Confirmed requirements; no metadata gate.
## S01 — Producer
- Implementer: [@impl_std](subagent://impl_std)
- Depends on: none
Real behavior, tests and independent review are described in prose.
## S02 — Consumer
- Implementer: [@impl_large](subagent://impl_large)
- Depends on: S01
Parent invariant and required joint oracle.
### S02.A — Store
- Implementer: [@impl_large](subagent://impl_large)
- Depends on: none
Store work and oracle.
### S02.B — Projection
- Implementer: [@impl_std](subagent://impl_std)
- Depends on: S02.A
Projection work.
## Final integration
Real final validation, not a section.
'''
class BasicPlanTests(unittest.TestCase):
 def test_plain_no_json_no_state_or_receipts(self):
  r=p.parse(BASE);self.assertFalse(r.errors);self.assertEqual(len(r.units),4)
 def test_missing_model_collected(self):
  self.assertTrue(p.parse(BASE.replace('- Implementer: [@impl_std](subagent://impl_std)\n','')).errors)
 def test_child_no_profile_inheritance(self):
  t=BASE.replace('### S02.B — Projection\n- Implementer: [@impl_std](subagent://impl_std)','### S02.B — Projection')
  self.assertIn('S02.B: missing Implementer',p.parse(t).errors)
 def test_auto_rejected(self):
  self.assertTrue(p.parse(BASE.replace('[@impl_large](subagent://impl_large)','AUTO')).errors)
 def test_label_target_mismatch(self):
  self.assertTrue(p.parse(BASE.replace('subagent://impl_large','subagent://impl_std')).errors)
 def test_duplicate_id(self):self.assertTrue(p.parse(BASE.replace('## S02 —','## S01 —')).errors)
 def test_unknown_dep(self):self.assertTrue(p.parse(BASE.replace('Depends on: S01','Depends on: S99')).errors)
 def test_parent_cycle(self):
  t=BASE.replace('Depends on: none','Depends on: S02',1)
  self.assertTrue(any('cycle' in e for e in p.parse(t).errors))
 def test_child_cycle(self):
  t=BASE.replace('### S02.A — Store\n- Implementer: [@impl_large](subagent://impl_large)\n- Depends on: none','### S02.A — Store\n- Implementer: [@impl_large](subagent://impl_large)\n- Depends on: S02.B')
  self.assertTrue(any('cycle' in e for e in p.parse(t).errors))
 def test_child_not_external_unlock(self):
  t=BASE+'\n## S03 — Bad consumer\n- Implementer: [@impl_std](subagent://impl_std)\n- Depends on: S02.A\n'
  self.assertTrue(any('not child' in e for e in p.parse(t).errors))
 def test_wrong_parent_nesting(self):self.assertTrue(p.parse(BASE.replace('### S02.B','### S03.B')).errors)
 def test_heading_inside_code_not_unit(self):
  r=p.parse(BASE+'\n```markdown\n## S99 — Example only\n```\n');self.assertEqual(len(r.units),4);self.assertFalse(r.errors)
 def test_all_errors_in_one_response(self):
  t=BASE.replace('Depends on: S01','Depends on: S99').replace('[@impl_std](subagent://impl_std)','TBD');self.assertGreaterEqual(len(p.parse(t).errors),3)
 def test_extract_parent_contains_children_not_unrelated(self):
  x=p.extract(p.parse(BASE),'S02');self.assertIn('### S02.A',x);self.assertIn('### S02.B',x);self.assertNotIn('## S01',x);self.assertNotIn('## Final integration',x)
 def test_extract_child_contains_parent_contract(self):
  x=p.extract(p.parse(BASE),'S02.B');self.assertIn('Parent invariant',x);self.assertIn('### S02.B',x);self.assertNotIn('### S02.A',x)
 def test_validate_never_writes_state(self):
  with tempfile.TemporaryDirectory() as t:
   d=Path(t);file=d/'PLAN-FULL.md';file.write_text(BASE)
   out=subprocess.run([sys.executable,str(S/'scripts/section_plan.py'),'validate',str(file)],capture_output=True,text=True)
   self.assertEqual(out.returncode,0,out.stdout);self.assertEqual(list(d.iterdir()),[file]);self.assertEqual(file.read_text(),BASE)
 def test_extract_cannot_replace_plan(self):
  with tempfile.TemporaryDirectory() as t:
   file=Path(t)/'PLAN.md';file.write_text(BASE)
   out=subprocess.run([sys.executable,str(S/'scripts/section_plan.py'),'extract',str(file),'S01','--output',str(file)],capture_output=True)
   self.assertNotEqual(out.returncode,0);self.assertEqual(file.read_text(),BASE)
 def test_installed_template(self):self.assertFalse(p.parse((S/'assets/PLAN-FULL.template.md').read_text()).errors)
 def test_no_plan_passes_no_sections(self):self.assertTrue(p.parse('# empty').errors)
 def test_legacy_schedule_is_warning_not_gate(self):
  r=p.parse(BASE+'\n<!-- SFD_PLAN_V4 -->\n```json\n{"unusable":true}\n```\n<!-- /SFD_PLAN_V4 -->\n')
  self.assertFalse(r.errors);self.assertTrue(r.warnings)
