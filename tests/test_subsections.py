"""4.1 workflow regressions; evidence here is synthetic metadata, not model validation."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'skill/sectioned-feature-development/scripts'))
import workflow as w


def artifact():return {'path':'.agent-work/evidence.txt','sha256':'a'*64}

def check(head):return {'result':'PASS','head':head,'artifact':artifact()}

class SubsectionTests(unittest.TestCase):
 def setUp(self):
  self.p=w.load_plan(R/'tests/fixtures/v41-plan.md');self.p['status']='APPROVED'
  self.s=self.p['sections'][-1];self.sid=self.s['id'];self.units=self.s['subsections']
  self.heads=['0'*39+str(i) for i in range(1,4)]
  self.state={'feature_id':self.p['feature_id'],'run_id':self.p['run_id'],'status':'ACTIVE','plan_sha256':'digest','plan_review_status':'APPROVED','active':[],
   'sections':{s['id']:{'status':'ACCEPTED','integrated':True} for s in self.p['sections'][:-1]}}
  self.ss={'status':'IMPLEMENTING','integrated':False,'primary_review_id':'parent-primary','subsections':{},'writer_actor_ids':['writer'],'repair_waves':0}
  self.state['sections'][self.sid]=self.ss
 def reviewed(self,n):
  c=self.units[n];head=self.heads[n+1];base=self.heads[n]
  self.ss['subsections'][c['id']]={'status':'CHECKPOINT_VERIFIED','base':base,'head':head,'invalidated':False,'open_findings':[],
   'checks':{cid:check(head) for cid in c['check_ids']},'writer_actor_ids':['writer'],
   'review':{'parent_review_id':'parent-primary','base':base,'head':head,'actor_id':'primary-actor','result':'CLEAN','artifact':artifact()}}
 def complete(self):
  for i in range(len(self.units)):self.reviewed(i)
  h=self.heads[-1];self.ss.update(section_base=self.heads[0],candidate_head=h,open_findings=[],primary_review={'id':'parent-primary','base':self.heads[0],'result':'CLEAN','head':h,'actor_id':'primary-actor','artifact':artifact(),'covered_subsections':[c['id'] for c in self.units],'open_invalidations':[]},joint_evidence={j['id']:check(h) for j in self.s['joint_oracles']},final_checks={cid:check(h) for cid in self.s['check_ids']},final_review={'result':'CLEAN','head':h,'actor_id':'fresh-final','artifact':artifact()})
 def test_new_template_valid(self):w.validate(self.p)
 def test_atomic_v4_and_dotted_history_compatible(self):
  self.p.pop('workflow_revision')
  for s in self.p['sections']:
   for k in ('delivery_mode','lineage_id','shared_invariants','joint_oracles','subsections'):s.pop(k,None)
  self.p['sections'][-1]['id']='S04.1.2';self.p['integration_order'][-1]='S04.1.2';w.validate(self.p)
 def test_no_recursive_nesting(self):
  self.units[0]['subsections']=[]
  with self.assertRaises(w.Invalid):w.validate(self.p)
 def test_no_independent_assurance_budget_or_branch(self):
  for key in ['repair_budget','assurance','lineage_id','branch','loc_hard_cap']:
   p=copy.deepcopy(self.p);p['sections'][-1]['subsections'][0][key]='new'
   with self.subTest(key=key),self.assertRaises(w.Invalid):w.validate(p)
 def test_single_parent_multiple_children_requires_commit(self):
  self.p['sections']=[self.s];self.p['integration_order']=[self.sid];self.s['depends_on']=[];self.p['execution_mode']='EXECUTE_NO_COMMIT';self.p['max_parallel_writers']=1
  with self.assertRaises(w.Invalid):w.validate(self.p)
 def test_child_scope_escape_rejected(self):
  self.units[0]['write_paths']=['src/shared.py']
  with self.assertRaises(w.Invalid):w.validate(self.p)
 def test_external_dependency_on_child_rejected(self):
  self.p['sections'][0]['depends_on']=[self.units[0]['id']]
  with self.assertRaises(w.Invalid):w.validate(self.p)
 def test_wrong_parent_and_forward_dependency_rejected(self):
  for k,v in [('parent_section_id','S01'),('depends_on',[self.units[1]['id']])]:
   p=copy.deepcopy(self.p);p['sections'][-1]['subsections'][0][k]=v
   with self.subTest(k=k),self.assertRaises(w.Invalid):w.validate(p)
 def test_joint_oracle_must_cover_invariants(self):
  self.s['joint_oracles'][0]['invariants']=self.s['shared_invariants'][:1]
  with self.assertRaises(w.Invalid):w.validate(self.p)
 def test_next_child_serial(self):
  self.assertEqual(w.next_unit(self.p,self.state,self.sid,'digest')['next'],self.units[0]['id'])
  self.reviewed(0);self.assertEqual(w.next_unit(self.p,self.state,self.sid,'digest')['next'],self.units[1]['id'])
 def test_next_child_requires_review_and_checks(self):
  self.reviewed(0);self.ss['subsections'][self.units[0]['id']]['review']['result']='MATERIAL_CANDIDATES'
  self.assertEqual(w.next_unit(self.p,self.state,self.sid,'digest')['reason'],'CHECKPOINT_BARRIER')
 def test_invalidated_checkpoint_blocks(self):
  self.reviewed(0);self.ss['subsections'][self.units[0]['id']]['invalidated']=True
  self.assertEqual(w.next_unit(self.p,self.state,self.sid,'digest')['reason'],'CHECKPOINT_BARRIER')
 def test_parent_review_workspace_barrier(self):
  self.state['active']=[{'section_id':self.sid,'workspace':'/tmp/subsection-review','stage':'REVIEW'}]
  self.assertEqual(w.next_unit(self.p,self.state,self.sid,'digest')['reason'],'PARENT_ACTOR_BARRIER')
 def test_child_done_is_not_parent_acceptance(self):
  self.complete();r=w.next_unit(self.p,self.state,self.sid,'digest');self.assertEqual(r['reason'],'PARENT_RECONCILIATION_REQUIRED')
  self.assertFalse(self.ss['integrated']);self.assertEqual(self.ss['status'],'IMPLEMENTING')
 def test_checkpoints_do_not_advance_global_counter(self):
  self.state['full_review_cursor']=9;before=copy.deepcopy(self.state)
  w.next_unit(self.p,self.state,self.sid,'digest');self.assertEqual(self.state,before)
 def test_joint_test_missing_not_accepted(self):
  self.complete();self.ss['joint_evidence']={}
  self.assertFalse(w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')['eligible_by_metadata'])
 def test_green_checkpoints_without_parent_reconciliation_not_accepted(self):
  self.complete();self.ss['primary_review']={}
  self.assertFalse(w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')['eligible_by_metadata'])
 def test_missing_or_stale_coverage_not_accepted(self):
  self.complete();self.ss['primary_review']['covered_subsections']=[]
  self.assertFalse(w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')['eligible_by_metadata'])
 def test_stale_final_and_reused_writer_rejected(self):
  self.complete();self.ss['final_review']['head']=self.heads[0]
  self.assertFalse(w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')['eligible_by_metadata'])
  self.ss['final_review']['head']=self.heads[-1];self.ss['final_review']['actor_id']='writer'
  self.assertFalse(w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')['eligible_by_metadata'])
 def test_checkpoint_chain_cannot_skip_unreviewed_range(self):
  self.complete();self.ss['subsections'][self.units[1]['id']]['base']=self.heads[0]
  self.ss['subsections'][self.units[1]['id']]['review']['base']=self.heads[0]
  self.assertFalse(w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')['eligible_by_metadata'])
 def test_complete_parent_gate(self):
  self.complete();self.assertTrue(w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')['eligible_by_metadata'])
 def test_one_clean_vs_repaired_assurance(self):
  self.complete();self.s['assurance']='ONE';self.ss['final_review']={}
  self.assertTrue(w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')['eligible_by_metadata'])
  self.ss['repair_waves']=1
  self.assertFalse(w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')['eligible_by_metadata'])
 def test_child_budget_is_shared_and_attempts_count(self):
  with tempfile.TemporaryDirectory() as t:
   path=Path(t)/'STATE.json';self.ss['repair_waves']=4;path.write_text(json.dumps(self.state))
   a=w.reserve_repair(self.p,path,self.sid,self.units[0]['id'],'repair-5',['F1'],'digest');self.assertEqual(a['wave'],5)
   a2=w.reserve_repair(self.p,path,self.sid,self.units[0]['id'],'repair-5',['F1'],'digest');self.assertEqual(a,a2)
   with self.assertRaises(w.Invalid):w.reserve_repair(self.p,path,self.sid,self.units[1]['id'],'repair-6',['F2'],'digest')
   s=json.loads(path.read_text());self.assertEqual(s['repair_lineages'][self.sid]['waves_used'],5)
   s['repair_lineages'][self.sid]['extra_attempt_authority']={'repair-6':{'request_id':'ADV-01','decision_sha256':'d'*64}};path.write_text(json.dumps(s))
   self.assertEqual(w.reserve_repair(self.p,path,self.sid,self.units[1]['id'],'repair-6',['F2'],'digest')['wave'],6)
   with self.assertRaises(w.Invalid):w.reserve_repair(self.p,path,self.sid,None,'repair-7',['F3'],'digest')
 def test_open_parent_finding_blocks_next_child(self):
  self.reviewed(0);self.ss['open_findings']=['parent-cross-case']
  self.assertEqual(w.next_unit(self.p,self.state,self.sid,'digest')['reason'],'PARENT_FINDING_BARRIER')
 def test_imported_original_lineage_budget_cannot_reset(self):
  with tempfile.TemporaryDirectory() as t:
   path=Path(t)/'STATE.json';self.ss.update(repair_waves=2,original_lineage_waves=6);path.write_text(json.dumps(self.state))
   with self.assertRaises(w.Invalid):w.reserve_repair(self.p,path,self.sid,self.units[0]['id'],'fresh-child-attempt',['F-new'],'digest')
   self.assertEqual(json.loads(path.read_text())['sections'][self.sid]['original_lineage_waves'],6)
 def test_actual_git_ancestry_and_artifact_hash(self):
  with tempfile.TemporaryDirectory() as t:
   repo=Path(t)
   def git(*args):return subprocess.run(['git','-C',str(repo),*args],check=True,capture_output=True,text=True).stdout.strip()
   git('init','-b','main');git('config','user.name','Test');git('config','user.email','test@example.invalid')
   for i in range(3):
    (repo/'source.txt').write_text(str(i));git('add','source.txt');git('commit','-m',f'checkpoint-{i}');self.heads[i]=git('rev-parse','HEAD')
   self.complete();e=repo/'.agent-work/evidence.txt';e.parent.mkdir();e.write_text('retained actual log fixture')
   result=w.acceptance_check(self.p,self.state,self.sid,self.heads[-1],'digest')
   for a in result['evidence_artifacts']:a['sha256']=w.digest(e)
   self.assertTrue(w.verify_acceptance_files(repo,result)['git_ancestry_and_artifact_hashes_verified'])
   e.write_text('changed')
   with self.assertRaises(w.Invalid):w.verify_acceptance_files(repo,result)

if __name__=='__main__':unittest.main()
