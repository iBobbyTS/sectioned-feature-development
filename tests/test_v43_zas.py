import copy,json,sys,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'skill/sectioned-feature-development/scripts'))
import zas_evidence as z

def page():
 return {'schema':z.PROTOCOL,'agent_id':'A','service_generation':'g1','snapshot_seq':9,'count_scope':'agent_lifetime',
  'tools':[{'tool_name':'read','call_count':2,'recent_calls':[{'seq':8,'tool_call_id':'read-2','arguments':{'path':'x','start_line':1,'line_count':20},'arguments_truncated':False,'redacted_fields':0},{'seq':7,'tool_call_id':'read-1','arguments':{'path':'x','start_line':1,'line_count':20},'arguments_truncated':False,'redacted_fields':0}]}],
  'reasoning':{'text':'公开推理🙂','char_count':5,'truncated':False,'source':{'status':'VERIFIED_RUNTIME_PUBLIC','runtime_version':'TEST-FIXTURE-NOT-LOCAL-PROOF','event_type':'fixture.delta','delta_pointer':'/visible/text'}},
  'coverage':{'tool_history_complete':True,'reasoning_complete':True,'dropped_events':0}}

def status():
 return {'service_generation':'g1','capabilities':{'observation':{'protocol':z.PROTOCOL,'public_reasoning_default':True,'runtime_source_verified':True,'defaults':{'top_tools':3,'recent_calls_per_tool':5,'reasoning_chars':200}}}}

class ZasEvidenceTests(unittest.TestCase):
 def test_upgraded_contract_required_no_baseline(self):
  with self.assertRaises(z.Invalid):z.capabilities({'capabilities':{}},{'tools':list(z.BASE_TOOLS)})
 def test_advertisement_without_tool_is_install_error(self):
  with self.assertRaises(z.Invalid):z.capabilities(status(),{'tools':list(z.BASE_TOOLS)})
 def test_both_capabilities_required(self):
  self.assertEqual(z.capabilities(status(),{'tools':list(z.REQUIRED_TOOLS)})['mode'],'OBSERVATION_READY')
 def test_default_public_reasoning_not_opt_in(self):
  self.assertEqual(z.check_snapshot(page(),'A')['reasoning_chars'],5)
  s=status();s['capabilities']['observation']['public_reasoning_default']=False
  with self.assertRaises(z.Invalid):z.capabilities(s,{'tools':list(z.REQUIRED_TOOLS)})
 def test_tool_absence_not_legacy_retry(self):
  with self.assertRaises(z.Invalid):z.capabilities(status(),{'tools':['zcode_subagent_agent_poll']})
 def test_snapshot_does_not_classify_or_cancel(self):
  r=z.check_snapshot(page(),'A');self.assertEqual(r['semantic_progress'],'NOT_INFERRED');self.assertIsNone(r['automatic_action'])
 def test_empty_snapshot_not_no_progress(self):
  p=page();p['tools']=[];p['reasoning']['text']='';p['reasoning']['char_count']=0
  self.assertEqual(z.check_snapshot(p,'A')['semantic_progress'],'NOT_INFERRED')
 def test_200_unicode_characters_not_bytes(self):
  p=page();p['reasoning'].update(text='中🙂'*100,char_count=200)
  self.assertEqual(z.check_snapshot(p,'A')['reasoning_chars'],200)
  p['reasoning'].update(text='中🙂'*101,char_count=202)
  with self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
 def test_char_count_must_match(self):
  p=page();p['reasoning']['char_count']=4
  with self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
 def test_exact_source_required(self):
  for field,value in [('status','UNVERIFIED'),('delta_pointer','/encrypted_content'),('event_type','')]:
   p=page();p['reasoning']['source'][field]=value
   with self.subTest(field=field),self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
 def test_nested_encrypted_content_rejected(self):
  for value in [{'encrypted_content':'NEVER'}, {'array':[{'nested':{'encrypted_content':'NEVER'}}]}]:
   p=page();p['tools'][0]['recent_calls'][0]['arguments']=value
   with self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
 def test_results_are_not_calls(self):
  for field in ['result','output','stdout','stderr','outcome']:
   p=page();p['tools'][0]['recent_calls'][0][field]='not allowed'
   with self.subTest(field=field),self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
 def test_three_tool_groups_and_five_calls_maximum(self):
  p=page();p['tools']*=4
  with self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
  p=page();p['tools'][0]['call_count']=20;p['tools'][0]['recent_calls']*=3
  with self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
 def test_cross_agent_rejected(self):
  with self.assertRaises(z.Invalid):z.check_snapshot(page(),'B')
 def test_repeated_content_distinct_ids_remains(self):
  self.assertEqual(z.check_snapshot(page(),'A')['tool_calls'],2)
 def test_duplicate_id_rejected(self):
  p=page();p['tools'][0]['recent_calls'][1]['tool_call_id']='read-2'
  with self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
 def test_loss_is_not_inactivity(self):
  p=page();p['coverage']['dropped_events']=1
  self.assertEqual(z.check_snapshot(p,'A')['coverage'],'GAPPED')
 def test_server_cannot_add_progress_verdict(self):
  p=page();p['classification']='NO_PROGRESS_LOOP'
  with self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
 def test_recent_call_order_is_descending(self):
  p=page();p['tools'][0]['recent_calls'].reverse()
  with self.assertRaises(z.Invalid):z.check_snapshot(p,'A')
 def test_mcp_description_only_contains_judgment_vocabulary(self):
  tool=json.loads((R/'docs/contracts/zas-observe-tool.json').read_text())
  self.assertEqual(tool['inputSchema']['required'],['agent_id'])
  self.assertEqual(set(tool['inputSchema']['properties']),{'agent_id'})
  for word in ['PROGRESSING','EXPECTED_WAIT','NEEDS_CLARIFICATION','NO_PROGRESS_LOOP','INSUFFICIENT_OBSERVABILITY']:
   self.assertIn(word,tool['description']);self.assertNotIn(word,json.dumps(tool['outputSchema']))
  self.assertIn('仅在怀疑',tool['description']);self.assertIn('不含结果',tool['description'])
if __name__=='__main__':unittest.main()
