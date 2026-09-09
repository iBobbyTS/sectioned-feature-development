"""4.2 integration regressions using real temporary Git repos and synthetic model receipts.
These tests do not claim any actual LLM execution.
"""
import copy, hashlib, importlib, json, subprocess, sys, tempfile, unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
S=R/'skill/sectioned-feature-development';sys.path.insert(0,str(S/'scripts'))
import workflow as w
import execution_artifacts as e

def jwrite(path,value):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,indent=2));return path

def set_schedule(text,p):
 return text.split(w.BEGIN)[0]+w.BEGIN+'\n```json\n'+json.dumps(p,indent=2)+'\n```\n'+w.END+'\n'

class RestoredArtifacts(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.repo=Path(self.t.name)/'repo';self.repo.mkdir()
  for args in [('init','-b','main'),('config','user.name','Fixture'),('config','user.email','fixture@example.invalid')]:self.git(*args)
  (self.repo/'src').mkdir();(self.repo/'src/rule.py').write_text('VALUE=1\n');(self.repo/'.gitignore').write_text('/git-worktree/\n')
  self.git('add','src','.gitignore');self.git('commit','-m','base');self.base=self.git('rev-parse','HEAD');self.git('switch','-c','codex/example-feature')
  e.init(self.repo,'example-feature','example-run','parent-real-id','OFF')
  self.aw=self.repo/'.agent-work';(self.aw/'REQUIREMENTS.md').write_text('# Confirmed requirements\nREQ-001: preserve rule output.\n')
  self.plan_path=self.aw/'PLAN-FULL.md';self.plan=w.load_plan(self.plan_path)
  self.plan.update(base_ref=self.base,status='FROZEN',requirements_sha256=w.digest(self.aw/'REQUIREMENTS.md'))
  self.plan_path.write_text(set_schedule(self.plan_path.read_text(),self.plan))
  self.author='parent-real-id';self.reviewer=self.actor('reviewer-actual','plan_reviewer')
  self.author_output=self.aw/'evidence/full-draft.md';self.author_output.write_text(self.plan_path.read_text())
  self.plan_report=jwrite(self.aw/'reviews/plan.json',{'actor_id':self.reviewer,'result':'APPROVED','plan_sha256':w.digest(self.plan_path),'candidates':[]})
  self.admission=jwrite(self.aw/'reviews/admission.json',{'decision':'APPROVED','unresolved_findings':[]})
 def tearDown(self):self.t.cleanup()
 def git(self,*args):return subprocess.run(['git','-C',str(self.repo),*args],check=True,capture_output=True,text=True).stdout.strip()
 def actor(self,aid,role):
  f=jwrite(self.aw/'evidence'/f'{aid}.json',{'agent_id':aid})
  e.register(self.repo,aid,role,f,self.repo,observed_model=None);return aid
 def approve(self):return e.record_plan(self.repo,self.author,self.author_output,self.reviewer,self.plan_report,self.admission,'NOT_APPLICABLE')
 def atomic(self):
  self.approve();e.task(self.repo,'S01');state=e.load(self.repo);ss=state['sections']['S01']
  for aid,role in [('impl','impl_std'),('primary','code_reviewer'),('final','code_reviewer')]:self.actor(aid,role)
  state=e.load(self.repo);ss=state['sections']['S01'];h=self.base
  def a(n):return e.proof(jwrite(self.aw/'evidence'/n,{'fixture':'synthetic recorded result'}),self.repo)
  ss.update(status='AWAITING_ADMISSION',candidate_head=h,writer_actor_ids=['impl'],handoff_artifact=a('handoff.json'),handoff_head=h,open_findings=[],primary_review={'result':'CLEAN','base':h,'head':h,'actor_id':'primary','artifact':a('primary-review.json')},final_review={'result':'CLEAN','head':h,'actor_id':'final','artifact':a('final-review.json')},final_checks={'S01-focused':{'result':'PASS','head':h,'artifact':a('checks.json')}})
  e.save(self.repo,state);return state
 def test_audit_off_keeps_plan_state_and_contract_working_set(self):
  for n in ['PLAN-FULL.md','STATE.json','FEATURE-STATE.md','REQUIREMENTS.md']:self.assertTrue((self.aw/n).exists())
  self.assertEqual(e.load(self.repo)['audit_mode'],'OFF')
 def test_plan_approval_string_alone_does_not_unlock(self):
  state=e.load(self.repo);state.update(status='ACTIVE',plan_sha256=w.digest(self.plan_path),plan_review_status='APPROVED')
  e.save(self.repo,state)
  with self.assertRaises(w.Invalid):e.ready_files(self.repo)
 def test_plan_file_missing_blocks(self):
  self.approve();self.plan_path.unlink()
  with self.assertRaises((OSError,w.Invalid)):e.ready_files(self.repo)
 def test_real_files_roles_and_plan_allow_root_only(self):
  self.approve();self.assertEqual(e.ready_files(self.repo)['ready'],['S01'])
 def test_requirement_digest_must_resolve_actual_file(self):
  self.approve();(self.aw/'REQUIREMENTS.md').write_text('different')
  with self.assertRaises(w.Invalid):e.ready_files(self.repo)
 def test_missing_original_plan_review_report_blocks(self):
  self.approve();self.plan_report.unlink()
  with self.assertRaises(w.Invalid):e.ready_files(self.repo)
 def test_alias_without_actual_launch_id_rejected(self):
  p=jwrite(self.aw/'evidence/alias.json',{'profile':'impl_std'})
  with self.assertRaisesRegex(w.Invalid,'LAUNCH_RECEIPT'):e.register(self.repo,'impl-alias','impl_std',p,self.repo)
 def test_plan_reviewer_cannot_be_implementer(self):
  with self.assertRaisesRegex(w.Invalid,'REUSE'):e.register(self.repo,self.reviewer,'impl_std',self.aw/'evidence/reviewer-actual.json',self.repo)
 def test_main_cannot_register_as_worker(self):
  p=jwrite(self.aw/'evidence/main.json',{'agent_id':'parent-real-id'})
  with self.assertRaises(w.Invalid):e.register(self.repo,'parent-real-id','impl_large',p,self.repo)
 def test_task_materializes_current_parent_contract(self):
  self.approve();r=e.task(self.repo,'S01')
  self.assertTrue(Path(r['task']).is_file());self.assertTrue(Path(r['contract']).is_file())
  self.assertIn('Current executable unit',Path(r['task']).read_text())
 def test_accepted_flag_without_actual_evidence_blocks_consumer(self):
  self.approve();s=e.load(self.repo);s['sections']['S01'].update(status='ACCEPTED',integrated=True,candidate_head=self.base);e.save(self.repo,s)
  with self.assertRaises(w.Invalid):e.ready_files(self.repo)
 def test_atomic_acceptance_needs_handoff_and_fresh_final(self):
  self.atomic();r=e.finish_section(self.repo,'S01',self.base);self.assertTrue(r['eligible_by_metadata'])
 def test_atomic_missing_handoff_rejected(self):
  s=self.atomic();s['sections']['S01'].pop('handoff_artifact');e.save(self.repo,s)
  with self.assertRaises(w.Invalid):e.finish_section(self.repo,'S01',self.base)
 def test_atomic_reviewer_identity_cannot_be_writer(self):
  s=self.atomic();s['sections']['S01']['final_review']['actor_id']='impl';e.save(self.repo,s)
  with self.assertRaises(w.Invalid):e.finish_section(self.repo,'S01',self.base)
 def test_atomic_handoff_contents_tamper_blocks(self):
  s=self.atomic();(self.repo/s['sections']['S01']['handoff_artifact']['path']).write_text('changed')
  with self.assertRaises(w.Invalid):e.finish_section(self.repo,'S01',self.base)
 def test_review_candidate_changed_is_not_clean(self):
  s=self.atomic();e.stage_start(self.repo,'S01','INITIAL_BOUNDED','primary',self.repo)
  (self.repo/'src/rule.py').write_text('VALUE=2\n');p=jwrite(self.aw/'evidence/result.json',{'result':'CLEAN'})
  with self.assertRaisesRegex(w.Invalid,'CANDIDATE_CHANGED'):e.stage_finish(self.repo,'primary',p)
  self.assertEqual(e.load(self.repo)['sections']['S01']['status'],'REVIEW_INVALIDATED')
 def test_no_second_writer_on_same_parent_during_review(self):
  self.atomic();e.stage_start(self.repo,'S01','INITIAL_BOUNDED','primary',self.repo)
  with self.assertRaisesRegex(w.Invalid,'BUSY'):e.stage_start(self.repo,'S01','REPAIR','impl',self.repo)
 def test_multi_parent_no_commit_rejected(self):
  p=copy.deepcopy(self.plan);p['execution_mode']='EXECUTE_NO_COMMIT';p['max_parallel_writers']=1
  with self.assertRaisesRegex(w.Invalid,'MULTI_SECTION'):w.validate(p)
 def test_closed_plan_cannot_be_approved_again(self):
  self.approve();jwrite(self.aw/'CLOSURE.json',{'head':self.base})
  with self.assertRaisesRegex(w.Invalid,'CLOSED_PLAN'):self.approve()
 def test_baseline_subsection_request_unchanged(self):
  base=R/'docs/version-history/v4.3/BASELINE-ADVISOR-REQUEST.md'
  self.assertEqual(base.read_bytes(),(S/'assets/ADVISOR-REQUEST.template.md').read_bytes())

 def subsection_plan(self):
  example=json.loads((S/'assets/SUBSECTION-SCHEDULE.example.json').read_text())
  parent=example['sections'][1]
  parent=json.loads(json.dumps(parent).replace('S02','S01'))
  parent['depends_on']=[]
  self.plan['sections'][0]=parent
  self.plan['checks'].update(example['checks'])
  self.plan['checks'].update({k.replace('S02','S01'):v for k,v in example['checks'].items()})
  self.plan_path.write_text(set_schedule(self.plan_path.read_text(),self.plan))
  self.author_output.write_text(self.plan_path.read_text())
  self.plan_report=jwrite(self.aw/'reviews/plan.json',{'actor_id':self.reviewer,'result':'APPROVED','plan_sha256':w.digest(self.plan_path)})
  return parent
 def test_subsection_model_boundary_required(self):
  p=self.subsection_plan();p['subsections'][0].pop('decomposition_reason')
  with self.assertRaisesRegex(w.Invalid,'decomposition'):w.validate(self.plan)
 def test_multiple_subsections_cannot_bypass_commit_mode(self):
  self.subsection_plan();self.plan['sections']=self.plan['sections'][:1];self.plan['integration_order']=['S01']
  self.plan['execution_mode']='EXECUTE_NO_COMMIT';self.plan['max_parallel_writers']=1
  with self.assertRaises(w.Invalid):w.validate(self.plan)
 def test_subsection_parent_requires_joint_and_real_checkpoint_evidence(self):
  parent=self.subsection_plan();self.approve();e.task(self.repo,'S01')
  for aid,role in [('impl','impl_std'),('primary','code_reviewer'),('final','code_reviewer')]:self.actor(aid,role)
  st=e.load(self.repo);ss=st['sections']['S01'];ss.update(primary_review_id='parent-primary',writer_actor_ids=['impl'],subsections={},open_findings=[])
  def art(name):return e.proof(jwrite(self.aw/'evidence'/name,{'result':'synthetic fixture'}),self.repo)
  old=self.base
  for i,c in enumerate(parent['subsections']):
   (self.repo/'src/rule.py').write_text('VALUE='+str(i+2)+'\n');self.git('add','src/rule.py');self.git('commit','-m','checkpoint '+str(i))
   head=self.git('rev-parse','HEAD')
   ss['subsections'][c['id']]={'status':'CHECKPOINT_VERIFIED','base':old,'head':head,'open_findings':[],
    'writer_actor_ids':['impl'],'checks':{cid:{'result':'PASS','head':head,'artifact':art('check-'+c['id']+'.json')} for cid in c['check_ids']},
    'review':{'parent_review_id':'parent-primary','base':old,'head':head,'actor_id':'primary','result':'CLEAN','artifact':art('review-'+c['id']+'.json')}}
   old=head
  ss.update(candidate_head=head,handoff_head=head,handoff_artifact=art('handoff.json'),status='AWAITING_ADMISSION',
   primary_review={'id':'parent-primary','base':self.base,'head':head,'actor_id':'primary','result':'CLEAN','artifact':art('primary-parent-result.json'),'covered_subsections':[c['id'] for c in parent['subsections']],'open_invalidations':[]},
   final_review={'result':'CLEAN','head':head,'actor_id':'final','artifact':art('final-parent-result.json')},
   final_checks={cid:{'result':'PASS','head':head,'artifact':art('parent-check.json')} for cid in parent['check_ids']},
   joint_evidence={j['id']:{'result':'PASS','head':head,'artifact':art('joint.json')} for j in parent['joint_oracles']})
  e.save(self.repo,st)
  good=w.acceptance_check(self.plan,st,'S01',head,w.digest(self.plan_path));self.assertTrue(good['eligible_by_metadata'],good['errors'])
  nojoint=copy.deepcopy(st);nojoint['sections']['S01']['joint_evidence']={};e.save(self.repo,nojoint)
  with self.assertRaises(w.Invalid):e.finish_section(self.repo,'S01',head)
  e.save(self.repo,st);e.finish_section(self.repo,'S01',head)
  self.assertEqual(e.load(self.repo)['sections']['S01']['status'],'ACCEPTED')
 def test_live_audit_bootstraps_without_changing_execution_contract(self):
  # Initialization is exercised in a second isolated repository to avoid overwriting an active feature.
  other=Path(self.t.name)/'other';other.mkdir()
  subprocess.run(['git','init','-b','main',str(other)],check=True,capture_output=True)
  for k,v in [('user.name','Fixture'),('user.email','fixture@example.invalid')]:subprocess.run(['git','-C',str(other),'config',k,v],check=True)
  (other/'x').write_text('x');subprocess.run(['git','-C',str(other),'add','x'],check=True);subprocess.run(['git','-C',str(other),'commit','-m','base'],check=True,capture_output=True)
  e.init(other,'live-feature','run1','real-main','LIVE')
  state=e.load(other);self.assertTrue(Path(state['audit_trace']).exists());self.assertEqual(state['status'],'DRAFT')
 def test_nonmergeable_final_gate_cannot_mark_completed(self):
  self.atomic();e.finish_section(self.repo,'S01',self.base)
  state=e.load(self.repo);state['sections']['S02']['status']='PENDING';e.save(self.repo,state)
  with self.assertRaises(w.Invalid):e.close(self.repo)

 def test_real_actor_binds_prior_parent_reservation(self):
  self.atomic();st=e.load(self.repo)
  st['active']=[{'section_id':'S01','stage':'INITIAL_BOUNDED','status':'RESERVED','workspace':str(self.repo)}];e.save(self.repo,st)
  e.stage_start(self.repo,'S01','INITIAL_BOUNDED','primary',self.repo)
  self.assertEqual(e.load(self.repo)['active'][0]['actor_id'],'primary')

 def test_plan_admission_can_live_in_original_markdown_ledger(self):
  self.admission=self.aw/'reviews/PLAN-REVIEW.md'
  self.admission.write_text('# PLAN review\nMain admission: approved.\n<!-- SFD_RECEIPT -->\n```json\n{"decision":"APPROVED","unresolved_findings":[]}\n```\n')
  self.approve();self.assertEqual(e.ready_files(self.repo)['ready'],['S01'])

 def test_structural_recovery_preserves_lifetime_counter_and_allows_only_one_window(self):
  self.approve();state=e.load(self.repo)
  artifact=e.proof(jwrite(self.aw/'replans/decision.json',{'classification':'REBOUND_OWNER','boundary_changed':True}),self.repo)
  ledger={'waves_used':5,'recovery_used':True,'structural_recovery':{'original_lineage_id':'S01','replacement_section_id':'S01','generation':1,'boundary_changed':True,'classification':'REBOUND_OWNER','waves_at_boundary_change':5,'decision_artifact':artifact}}
  self.assertEqual(w.repair_limit(self.plan,state,'S01','S01',ledger,7),10)
  ledger['structural_recovery']['generation']=2
  with self.assertRaises(w.Invalid):w.repair_limit(self.plan,state,'S01','S01',ledger,10)
 def test_model_split_is_not_a_recovery_budget(self):
  self.approve();state=e.load(self.repo)
  self.assertEqual(w.repair_limit(self.plan,state,'S01','S01',{'waves_used':5,'model_changed':True},5),5)

if __name__=='__main__':unittest.main()
