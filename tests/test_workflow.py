import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[1]
LIB=ROOT/'skill/sectioned-feature-development/scripts'
sys.path.insert(0,str(LIB))
import workflow as w

class WorkflowTests(unittest.TestCase):
 def setUp(self):
  self.plan=w.load_plan(ROOT/'skill/sectioned-feature-development/assets/PLAN-FULL.template.md')
  self.plan['status']='APPROVED'
  self.state={'feature_id':self.plan['feature_id'],'run_id':self.plan['run_id'],'status':'ACTIVE',
   'plan_sha256':'digest','plan_review_status':'APPROVED','advisor_state':'NOT_REQUIRED','sections':{},'active':[]}
 def test_template_and_dag(self):w.validate(self.plan)
 def test_multisection_no_commit_blocked(self):
  self.plan['execution_mode']='EXECUTE_NO_COMMIT'
  with self.assertRaisesRegex(w.Invalid,'MULTI_SECTION'):w.validate(self.plan)
 def test_multisection_main_blocked(self):
  self.plan['feature_branch']='main'
  with self.assertRaisesRegex(w.Invalid,'DEDICATED'):w.validate(self.plan)
 def test_single_no_commit_allowed(self):
  self.plan['sections']=self.plan['sections'][:1];self.plan['integration_order']=['S01']
  self.plan['execution_mode']='EXECUTE_NO_COMMIT';self.plan['feature_branch']='main';self.plan['max_parallel_writers']=1
  w.validate(self.plan)
 def test_cycle_and_stage_cycle_blocked(self):
  self.plan['sections'][0]['depends_on']=['S03']
  with self.assertRaises(w.Invalid):w.validate(self.plan)
 def test_unknown_check_blocked(self):
  self.plan['sections'][0]['check_ids']=['made-up']
  with self.assertRaisesRegex(w.Invalid,'unknown check'):w.validate(self.plan)
 def test_path_escape_and_glob_blocked(self):
  for bad in ['../x','/tmp/x','src/**','.git/config','.agent-work/state.json','git-worktree/a']:
   with self.subTest(bad=bad),self.assertRaises(w.Invalid):w.path_prefix(bad)
 def test_only_root_ready(self):self.assertEqual(w.ready(self.plan,self.state,'digest')['ready'],['S01'])
 def test_unintegrated_dependency_blocks(self):
  self.state['sections']['S01']={'status':'ACCEPTED','integrated':False}
  self.assertEqual(w.ready(self.plan,self.state,'digest')['ready'],[])
 def test_independent_consumers_ready(self):
  self.state['sections']['S01']={'status':'ACCEPTED','integrated':True}
  self.assertEqual(w.ready(self.plan,self.state,'digest')['ready'],['S02','S03'])
 def test_independent_work_can_run_during_review(self):
  self.state['sections']['S01']={'status':'ACCEPTED','integrated':True}
  self.state['active']=[{'section_id':'S02','stage':'REVIEW','workspace':'/tmp/isolated-S02'}]
  self.assertEqual(w.ready(self.plan,self.state,'digest')['ready'],['S03'])
 def test_pending_parent_review_blocks_consumer(self):
  self.state['active']=[{'section_id':'S01','stage':'REVIEW','workspace':'/tmp/isolated-S01'}]
  self.assertEqual(w.ready(self.plan,self.state,'digest')['ready'],[])
 def test_write_read_contract_resource_collisions(self):
  self.state['sections']['S01']={'status':'ACCEPTED','integrated':True}
  for key,value in [('read_paths',['src/ui']),('exclusive_resources',['db-shared']),('consumes_contracts',['new-ui-contract'])]:
   p=copy.deepcopy(self.plan);p['sections'][2][key]=(p['sections'][2][key]+value if key=='read_paths' else value)
   if key=='exclusive_resources':p['sections'][1][key]=value
   if key=='consumes_contracts':p['sections'][1]['mutates_contracts']=value
   with self.subTest(key=key):self.assertEqual(w.ready(p,self.state,'digest')['ready'],['S02'])
 def test_stale_plan_and_auto_approval_blocked(self):
  with self.assertRaises(w.Invalid):w.ready(self.plan,self.state,'changed')
  self.plan['invocation_source']='CUSTOM_INSTRUCTIONS_AUTO'
  with self.assertRaises(w.Invalid):w.ready(self.plan,self.state,'digest')
 def test_completed_plan_cannot_execute(self):
  self.state['status']='COMPLETED';self.assertEqual(w.ready(self.plan,self.state,'digest')['ready'],[])
  self.assertEqual(w.follow_up('COMPLETED',False),'NEW_REQUEST_REASSESS_LOCAL_OR_NEW_FEATURE')
  self.assertEqual(w.follow_up('COMPLETED',True),'NEW_REVISION_PRESERVE_CLOSED_PLAN')
 def test_advisor_barrier(self):
  self.state['advisor_state']='RUNNING';self.assertEqual(w.ready(self.plan,self.state,'digest')['ready'],[])
 def test_review_reservation_concurrent_idempotent(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'state.json';p.write_text(json.dumps(self.state))
   with ThreadPoolExecutor(max_workers=4) as e:r=list(e.map(lambda i:w.reserve_review(p,'pass-'+str(i),'a'*40),range(4)))
   self.assertEqual(sorted(x['index'] for x in r),[1,2,3,4])
   old=w.reserve_review(p,'pass-1','a'*40);self.assertIn(old['index'],range(1,5))
   with self.assertRaises(w.Invalid):w.reserve_review(p,'pass-1','b'*40)
   self.assertEqual([x['provider'] for x in sorted(r,key=lambda x:x['index'])],['astra_high','glm-5.3','astra_high','glm-5.3'])
 def test_real_git_branch_worktree_and_ignore(self):
  with tempfile.TemporaryDirectory() as t:
   repo=Path(t)/'repo';repo.mkdir()
   def g(*a):return subprocess.run(['git','-C',str(repo),*a],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
   g('init','-b','main');g('config','user.email','test@example.invalid');g('config','user.name','Test')
   (repo/'x').write_text('x');g('add','x');g('commit','-m','base')
   with self.assertRaises(w.Invalid):w.git_check(repo,self.plan)
   g('switch','-c',self.plan['feature_branch'])
   with self.assertRaisesRegex(w.Invalid,'gitignore'):w.git_check(repo,self.plan)
   (repo/'.gitignore').write_text('/git-worktree/\n');(repo/'git-worktree').mkdir()
   w.git_check(repo,self.plan)
   g('add','.gitignore');g('commit','-m','worktree setup')
   g('worktree','add','-b','s02','git-worktree/S02','HEAD')
   g('worktree','add','-b','s03','git-worktree/S03','HEAD')
   (repo/'git-worktree/S02/x').write_text('one')
   self.assertEqual((repo/'git-worktree/S03/x').read_text(),'x')
   self.assertEqual((repo/'x').read_text(),'x')

if __name__=='__main__':unittest.main()
