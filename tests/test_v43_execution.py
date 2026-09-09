import copy,json,sys,unittest
from pathlib import Path
import test_restored_artifacts as helpers
from test_restored_artifacts import jwrite,set_schedule,R,S,e,w
import advisor_flow as af
import advisor_pack as ap

class V43ExecutionTests(unittest.TestCase):
 setUp=helpers.RestoredArtifacts.setUp
 tearDown=helpers.RestoredArtifacts.tearDown
 git=helpers.RestoredArtifacts.git
 actor=helpers.RestoredArtifacts.actor
 approve=helpers.RestoredArtifacts.approve
 def test_every_parent_model_fixed_in_plan(self):
  for bad in [None,'AUTO','impl_unknown','implementer_2']:
   p=copy.deepcopy(self.plan);p['sections'][0]['profile']=bad
   with self.subTest(bad=bad),self.assertRaises(w.Invalid):w.validate(p)
 def test_current_revision_restores_all_artifact_checks(self):
  self.assertEqual(self.plan['workflow_revision'],'4.3');self.approve()
  p=copy.deepcopy(self.plan);p.pop('requirements_path')
  with self.assertRaises(w.Invalid):w.validate(p)
 def test_every_child_model_mandatory_not_parent_inherited(self):
  p=json.loads((S/'assets/SUBSECTION-SCHEDULE.example.json').read_text())
  for sec in p['sections']:
   for child in sec.get('subsections',[]):
    q=copy.deepcopy(p)
    for candidate in q['sections']:
     for c in candidate.get('subsections',[]):
      if c['id']==child['id']:c.pop('profile',None)
    with self.assertRaises(w.Invalid):w.validate(q)
 def test_unplanned_tier_dispatch_rejected(self):
  self.approve();e.task(self.repo,'S01');self.actor('cheap','impl_nano')
  with self.assertRaisesRegex(w.Invalid,'IMPLEMENTER_DIFFERS_FROM_FROZEN_PLAN'):e.stage_start(self.repo,'S01','IMPLEMENT','cheap',self.repo)
 def test_correct_tier_dispatch_and_finish(self):
  self.approve();e.task(self.repo,'S01');self.actor('std','impl_std')
  e.stage_start(self.repo,'S01','IMPLEMENT','std',self.repo)
  e.stage_finish(self.repo,'std',jwrite(self.aw/'evidence/result.json',{'result':'DONE'}))
  self.assertFalse(e.load(self.repo)['active'])
 def test_task_from_another_tier_cannot_be_used(self):
  self.approve();e.task(self.repo,'S01');self.actor('std','impl_std')
  state=e.load(self.repo);state['sections']['S01']['task_profile']='impl_large';e.save(self.repo,state)
  with self.assertRaisesRegex(w.Invalid,'TASK_ASSIGNMENT'):e.stage_start(self.repo,'S01','IMPLEMENT','std',self.repo)
 def test_requested_model_contradiction_rejected(self):
  self.approve();r=jwrite(self.aw/'evidence/std.json',{'agent_id':'std'})
  with self.assertRaisesRegex(w.Invalid,'CONFIG_MISMATCH'):e.register(self.repo,'std','impl_std',r,self.repo,requested_model='gpt-6-astra')
 def test_observed_model_contradiction_blocks_writer(self):
  self.approve();e.task(self.repo,'S01');r=jwrite(self.aw/'evidence/std.json',{'agent_id':'std'})
  e.register(self.repo,'std','impl_std',r,self.repo,observed_model='gpt-5.6-luna')
  with self.assertRaises(w.Invalid):e.stage_start(self.repo,'S01','IMPLEMENT','std',self.repo)
 def test_main_plan_author_is_not_an_implementation_fallback(self):
  self.approve();self.assertEqual(e.load(self.repo)['plan_author']['actor_id'],'parent-real-id')
  with self.assertRaises(w.Invalid):self.actor('parent-real-id','impl_large')
 def ask(self):
  self.approve();req=self.aw/'replans/advisor.md';req.parent.mkdir(exist_ok=True);req.write_text('# Decision needed\nADV-02: frozen incompatible conclusions, same bounded probe failed to decide.')
  return af.request(self.repo,'ADV-02-001','ADV-02',req)
 def result(self):
  state=e.load(self.repo);state['advisor_state']='WAITING_EXTERNAL';e.save(self.repo,state)
  p=self.aw/'evidence/advisor-response.md';p.write_text('Preserve accepted work; narrow remaining owner.');return af.receive(self.repo,p)
 def test_advisor_request_blocks_with_audit_off(self):
  self.ask();self.assertEqual(e.load(self.repo)['audit_mode'],'OFF');self.assertEqual(e.ready_files(self.repo)['ready'],[])
  with self.assertRaises(w.Invalid):e.close(self.repo)
 def test_advisor_result_without_human_does_not_resume(self):
  self.ask();self.result();self.assertEqual(e.ready_files(self.repo)['ready'],[])
  with self.assertRaises(w.Invalid):af.adopt(self.repo,'accept',jwrite(self.aw/'evidence/not-human.json',{'decision':'accept'}),'REPAIR')
 def test_human_adoption_preserves_budget(self):
  self.ask();before=copy.deepcopy(e.load(self.repo)['repair_lineages']);self.result()
  receipt=jwrite(self.aw/'evidence/human.json',{'request_id':'ADV-02-001','decision':'accept','user_message_id':'actual-message-fixture','verbatim_user_message':'接受该有界修复，保持原预算。'})
  af.adopt(self.repo,'accept',receipt,'REPAIR')
  self.assertEqual(e.load(self.repo)['repair_lineages'],before);self.assertEqual(e.load(self.repo)['advisor_state'],'DECISION_APPLIED')
 def test_clarification_preserves_original_response(self):
  self.ask();self.result()
  receipt=jwrite(self.aw/'evidence/human.json',{'request_id':'ADV-02-001','decision':'request-clarification','user_message_id':'msg','verbatim_user_message':'请补充边界。'})
  af.adopt(self.repo,'request-clarification',receipt,'')
  response=self.aw/'evidence/clarify.md';response.write_text('Clarified bounded decision.');af.receive(self.repo,response)
  a=e.load(self.repo)['advisor'];self.assertEqual(len(a['result_history']),1);e.verify(a['result_history'][0],self.repo)
 def test_advisor_package_requires_stopped_actors(self):
  self.ask();state=e.load(self.repo);state['active']=[{'actor_id':'not-stopped'}];e.save(self.repo,state)
  with self.assertRaisesRegex(w.Invalid,'STOP_AND_RECORD'):af.package(self.repo,Path(self.t.name)/'export')
 def test_advisor_pack_real_git_and_symlink_no_follow(self):
  self.ask();outside=Path(self.t.name)/'outside';outside.write_text('private external content');(self.repo/'link').symlink_to(outside)
  (self.repo/'build').mkdir();(self.repo/'build/tracked.py').write_text('tracked source')
  self.git('add','build/tracked.py')
  r=af.package(self.repo,Path(self.t.name)/'advisor-pack')
  import zipfile,hashlib
  with zipfile.ZipFile(r['path']) as z:
   names=z.namelist();self.assertIn('repo/.git/HEAD',names);self.assertIn('GIT-METADATA/repository.bundle',names);self.assertIn('repo/build/tracked.py',names)
   self.assertEqual(z.read('repo/link').decode(),str(outside))
   meta=json.loads(z.read('repo/ADVISOR-PACK-MANIFEST.json'))
   for f in meta['files']:self.assertEqual(hashlib.sha256(z.read(f['path'])).hexdigest(),f['sha256'])
  self.assertEqual(e.load(self.repo)['advisor_state'],'WAITING_EXTERNAL')
 def test_git_refs_named_like_cache_directories_are_not_omitted(self):
  self.git('branch','build/source',self.base);self.ask()
  r=af.package(self.repo,Path(self.t.name)/'advisor-pack')
  import zipfile
  with zipfile.ZipFile(r['path']) as z:self.assertIn('repo/.git/refs/heads/build/source',z.namelist())
 def test_advisor_pack_secret_blocks_not_silently_omitted(self):
  self.ask();(self.repo/'.env').write_text('nonsecret fixture still private by filename')
  with self.assertRaises(w.Invalid):af.package(self.repo,Path(self.t.name)/'advisor-pack')
  self.assertEqual(e.load(self.repo)['advisor_state'],'PACKAGE_BLOCKED')
 def test_zas_and_advisor_events_recorded_when_audit_enabled(self):
  import subprocess
  trace=self.aw/'audit/TRACE.jsonl'
  subprocess.run([sys.executable,str(S/'scripts/audit_trace.py'),'init',str(trace),'--feature-id',self.plan['feature_id'],'--skill-version','4.3','--invocation-source','USER_EXPLICIT','--invocation-timing','FEATURE_START','--trigger-evidence','user test','--feature-base',self.base,'--repo',str(self.repo)],check=True,capture_output=True)
  state=e.load(self.repo);state.update(audit_mode='LIVE',audit_trace=str(trace));e.save(self.repo,state)
  e.audit_event(self.repo,state,'zas_observation_decision','zas',{'agent_id':'real-id-fixture','classification':'INSUFFICIENT_OBSERVABILITY'})
  self.ask()
  events=[json.loads(line) for line in trace.read_text().splitlines()]
  self.assertTrue(any(x.get('event_family')=='zas' for x in events))
  self.assertTrue(any(x.get('event')=='advisor_required' for x in events))
  self.assertFalse(e.load(self.repo).get('audit_gaps'))
 def test_advisor_pack_linked_worktree_preserves_actual_git(self):
  wt=Path(self.t.name)/'linked';self.git('worktree','add','-b','other',str(wt),self.base)
  req=wt/'.agent-work/advisor/R1/ADVISOR-REQUEST.md';req.parent.mkdir(parents=True);req.write_text('ADV-02 request')
  r=ap.build(wt,'feature','ADV-02','R1',Path(self.t.name)/'advisor-pack')
  import zipfile
  with zipfile.ZipFile(r['path']) as z:
   self.assertIn('linked/.git',z.namelist());self.assertIn('GIT-METADATA/common/HEAD',z.namelist());self.assertIn('GIT-METADATA/repository.bundle',z.namelist())
  self.assertTrue((wt/'.git').is_file())
if __name__=='__main__':unittest.main()
