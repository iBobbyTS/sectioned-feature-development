"""Offline regressions. All reviewer receipts are synthetic, not real model results."""
import copy, json, unittest
import test_restored_artifacts as fixtures
jwrite, set_schedule, e, w = fixtures.jwrite, fixtures.set_schedule, fixtures.e, fixtures.w

class PlanAdmissionRegression(unittest.TestCase):
 setUp=fixtures.RestoredArtifacts.setUp
 tearDown=fixtures.RestoredArtifacts.tearDown
 git=fixtures.RestoredArtifacts.git
 actor=fixtures.RestoredArtifacts.actor
 approve=fixtures.RestoredArtifacts.approve

 def correction(self,change=True,disposition='CLOSED_PLAN_ONLY'):
  old=self.plan_path.read_text(); snapshot=self.aw/'evidence/reviewed-plan.md';snapshot.write_text(old)
  original=w.digest(snapshot)
  report={'actor_id':self.reviewer,'result':'NEEDS_CORRECTION','plan_sha256':original,
          'candidates':[{'id':'P1','class':'PLAN_NIT','reason':'A local plan wording correction'}]}
  jwrite(self.plan_report,report)
  if change:self.plan_path.write_text(old+'\n<!-- spelling-only clarification; no contract change -->\n')
  self.author_output.write_text(self.plan_path.read_text())
  receipt={'decision':'APPROVED','unresolved_findings':[], 'closure_mode':'PARENT_PLAN_CORRECTION',
           'review_report_sha256':w.digest(self.plan_report),'applied_plan_sha256':w.digest(self.plan_path),
           'candidate_dispositions':[{'id':'P1','disposition':disposition,'reason':'No authority-backed semantic change',
             'evidence':'Original requirement plus original PLAN and the recorded plan diff'}],
           'plan_correction':{'classification':'NO_BOUNDARY_CHANGE','reason':'Same contract and scheduling boundaries',
              'changed_regions':['trailing wording comment'],'reviewed_plan':e.proof(snapshot,self.repo)}}
  jwrite(self.admission,receipt);return receipt,snapshot

 def test_legacy_exact_clean_still_accepted(self):
  self.approve();self.assertEqual(e.ready_files(self.repo)['ready'],['S01'])

 def test_parent_can_reject_unsupported_candidate_without_fake_clean(self):
  self.correction(False,'REJECTED');self.approve();state=e.load(self.repo)
  self.assertEqual(state['plan_review']['review_result'],'NEEDS_CORRECTION')
  self.assertEqual(e.obj(self.plan_report)['result'],'NEEDS_CORRECTION')
  self.assertEqual(e.ready_files(self.repo)['ready'],['S01'])

 def test_local_correction_retains_original_report_and_plan_hash(self):
  _,snapshot=self.correction();before=self.plan_report.read_bytes();self.approve();state=e.load(self.repo)
  self.assertEqual(self.plan_report.read_bytes(),before)
  self.assertEqual(state['plan_review']['reviewed_plan_sha256'],w.digest(snapshot))
  self.assertNotEqual(w.digest(snapshot),w.digest(self.plan_path))
  self.assertEqual(state['plan_sha256'],w.digest(self.plan_path))
  self.assertEqual(e.ready_files(self.repo)['ready'],['S01'])

 def test_unaccounted_candidate_blocks_parent_closure(self):
  receipt,_=self.correction();receipt['candidate_dispositions']=[];jwrite(self.admission,receipt)
  with self.assertRaisesRegex(w.Invalid,'EVERY_PLAN_CANDIDATE'):self.approve()

 def test_bare_approval_of_changed_plan_is_rejected(self):
  self.correction();jwrite(self.admission,{'decision':'APPROVED','unresolved_findings':[]})
  with self.assertRaisesRegex(w.Invalid,'EXPLICIT_PARENT'):self.approve()

 def test_wrong_report_hash_rejected(self):
  receipt,_=self.correction();receipt['review_report_sha256']='0'*64;jwrite(self.admission,receipt)
  with self.assertRaises(w.Invalid):self.approve()

 def test_original_plan_tamper_is_rejected(self):
  _,snapshot=self.correction();snapshot.write_text(snapshot.read_text()+'\nchanged')
  with self.assertRaisesRegex(w.Invalid,'ARTIFACT_HASH'):self.approve()

 def test_changed_model_requires_independent_plan_delta(self):
  receipt,_=self.correction();p=copy.deepcopy(self.plan);p['sections'][0]['profile']='impl_large'
  self.plan_path.write_text(set_schedule(self.plan_path.read_text(),p))
  receipt['applied_plan_sha256']=w.digest(self.plan_path);jwrite(self.admission,receipt)
  with self.assertRaisesRegex(w.Invalid,'PLAN_DELTA_REQUIRED'):self.approve()

 def test_expanded_owner_requires_independent_plan_delta(self):
  receipt,_=self.correction();p=copy.deepcopy(self.plan);p['sections'][0]['write_paths'].append('src/another-owner.py')
  self.plan_path.write_text(set_schedule(self.plan_path.read_text(),p))
  receipt['applied_plan_sha256']=w.digest(self.plan_path);jwrite(self.admission,receipt)
  with self.assertRaisesRegex(w.Invalid,'PLAN_DELTA_REQUIRED'):self.approve()

 def test_user_semantics_cannot_be_auto_closed(self):
  receipt,_=self.correction();report=e.obj(self.plan_report);report['result']='OWNER_DECISION';jwrite(self.plan_report,report)
  receipt['review_report_sha256']=w.digest(self.plan_report);jwrite(self.admission,receipt)
  with self.assertRaisesRegex(w.Invalid,'OWNER_DECISION'):self.approve()

 def test_post_admission_plan_tamper_remains_blocked(self):
  self.correction();self.approve();self.plan_path.write_text(self.plan_path.read_text()+'\nchanged')
  with self.assertRaises(w.Invalid):e.ready_files(self.repo)

 def test_cannot_approve_while_reviewer_still_active(self):
  state=e.load(self.repo);state['active']=[{'actor_id':self.reviewer,'stage':'PLAN_REVIEW'}];e.save(self.repo,state)
  with self.assertRaisesRegex(w.Invalid,'STILL_ACTIVE'):self.approve()

if __name__=='__main__':unittest.main()
