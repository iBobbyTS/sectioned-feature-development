import copy,sys,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'skill/sectioned-feature-development/scripts'))
import zas_evidence as z

def page():
 return {'schema':z.PROTOCOL,'agent_id':'A','stream_id':'epoch1','first_available_seq':1,'next_seq':2,'has_more':False,'gap':{'present':False,'reason':None},'loss':{'dropped_events':0,'redacted_fields':0,'truncated_events':0},'events':[{'source':'runtime.session_event','seq':1,'kind':'tool_started','visibility':'metadata','summary':{'tool_name':'read','path':'x','start_line':1,'line_count':20}},{'source':'runtime.session_event','seq':2,'kind':'tool_completed','visibility':'metadata','summary':{'status':'ok'}}]}
class ZasEvidenceTests(unittest.TestCase):
 def test_baseline_not_fake_enhanced(self):
  r=z.capabilities({'capabilities':{}},{'tools':list(z.BASE_TOOLS)})
  self.assertFalse(r['observation_usable']);self.assertEqual(r['mode'],'BETA_BASELINE_LIMITED')
 def test_advertisement_without_tool_not_enhanced(self):
  r=z.capabilities({'capabilities':{'observation':{'protocol':z.PROTOCOL}}},{'tools':list(z.BASE_TOOLS)})
  self.assertFalse(r['observation_usable'])
 def test_both_capabilities_required(self):
  r=z.capabilities({'capabilities':{'observation':{'protocol':z.PROTOCOL}}},{'tools':list(z.BASE_TOOLS)+['zcode_subagent_observe']})
  self.assertTrue(r['observation_usable'])
 def test_tool_absence_is_not_legacy_retry(self):
  with self.assertRaises(z.Invalid):z.capabilities({}, {'tools':['zcode_subagent_agent_poll']})
 def test_valid_window_does_not_classify_loop(self):
  r=z.check_window(page(),'A');self.assertEqual(r['semantic_progress'],'NOT_INFERRED');self.assertIsNone(r['automatic_action'])
 def test_empty_window_not_no_progress(self):
  p=page();p['events']=[];self.assertEqual(z.check_window(p,'A')['semantic_progress'],'NOT_INFERRED')
 def test_public_content_requires_collection_authorization(self):
  p=page();p['events'][0].update(visibility='runtime_public',content='Public progress summary')
  with self.assertRaises(z.Invalid):z.check_window(p,'A')
  self.assertEqual(z.check_window(p,'A',public_content_authorized=True)['event_count'],2)
 def test_private_never_accepted(self):
  p=page();p['events'][0].update(visibility='private',content='opaque')
  with self.assertRaises(z.Invalid):z.check_window(p,'A',public_content_authorized=True)
 def test_stream_reset_requires_explicit_gap(self):
  with self.assertRaises(z.Invalid):z.check_window(page(),'A',stream_id='previous')
  p=page();p['gap']={'present':True,'reason':'stream_reset'};self.assertEqual(z.check_window(p,'A',9,'previous')['coverage'],'GAPPED')
 def test_unbounded_window_is_not_sent_to_semantic_reviewer(self):
  p=page();p['events']*=60
  with self.assertRaises(z.Invalid):z.check_window(p,'A')
 def test_cross_agent_rejected(self):
  with self.assertRaises(z.Invalid):z.check_window(page(),'B')
 def test_repeated_actions_preserved_not_deduped_by_content(self):
  p=page();p['events'][1]=copy.deepcopy(p['events'][0]);p['events'][1]['seq']=2
  self.assertEqual(z.check_window(p,'A')['event_count'],2)
 def test_retention_gap_is_not_inactivity(self):
  p=page();p['first_available_seq']=10;p['next_seq']=10;p['events']=[]
  with self.assertRaises(z.Invalid):z.check_window(p,'A')
  p['gap']={'present':True,'reason':'retention'};self.assertEqual(z.check_window(p,'A')['coverage'],'GAPPED')
if __name__=='__main__':unittest.main()
