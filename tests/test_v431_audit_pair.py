import copy,hashlib,json,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'skill/sectioned-feature-development/scripts';sys.path.insert(0,str(S))
import audit_finalize as main
import zas_audit_pack as zas
import process_audit as intake

class PairTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.repo=self.root/'repo';self.repo.mkdir()
  def git(*args):return subprocess.check_output(['git','-C',str(self.repo),*args],stderr=subprocess.DEVNULL,text=True).strip()
  git('init','-q');git('config','user.name','Fixture');git('config','user.email','f@example.invalid');(self.repo/'a').write_text('a');git('add','a');git('commit','-qm','a');self.head=git('rev-parse','HEAD')
  self.stage=self.root/'main-stage';self.stage.mkdir();self.zstage=self.root/'zas-stage';self.zstage.mkdir();self.out=self.root/'out'
  for name in main.REQUIRED_FILES:
   p=self.stage/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('# fixture\n')
  ident={'kind':main.PROCESS_KIND,'producer':'sectioned-feature-development','feature_id':'f1','run_id':'r1','source_head':self.head,'feature_base':self.head}
  (self.stage/'PROCESS-IDENTITY.json').write_text(json.dumps(ident));(self.stage/'git').mkdir();(self.stage/'git/HEAD.txt').write_text(self.head)
  self.parent=self.out/'repo-f1-sectioned-audit.zip'
  self.link={'schema_version':1,'feature_id':'f1','run_id':'r1','status':'USED','companion_filename':self.parent.stem+'-zas.zip'}
  (self.stage/'ZAS-LINK.json').write_text(json.dumps(self.link))
  (self.zstage/'ZAS-IDENTITY.json').write_text(json.dumps({'schema_version':1,'kind':zas.KIND,'producer':zas.PRODUCER,'feature_id':'f1','run_id':'r1'}))
  (self.zstage/'ZAS-AUDIT.md').write_text('# fixture, no additional model calls\n')
  self.row={'feature_id':'f1','run_id':'r1','physical_attempt_id':'p1','agent_id':'A','caller_assessment':None}
  self.write_row()
 def write_row(self): (self.zstage/'ZAS-RUNS.jsonl').write_text(json.dumps(self.row)+'\n')
 def tearDown(self): self.tmp.cleanup()
 def finalize(self,with_zas=True,ok=True):
  cmd=[sys.executable,str(S/'audit_finalize.py'),'finalize','--repo',str(self.repo),'--feature-id','f1','--pack-dir',str(self.stage),'--feature-base',self.head,'--product-head',self.head,'--desktop-root',str(self.out)]
  if with_zas:cmd+=['--zas-pack-dir',str(self.zstage)]
  r=subprocess.run(cmd,capture_output=True,text=True)
  if ok:self.assertEqual(r.returncode,0,r.stderr+r.stdout);return json.loads(r.stdout)
  self.assertNotEqual(r.returncode,0);return r
 def test_paired_name_and_no_checksum_files(self):
  r=self.finalize();child=zas.companion_path(self.parent)
  self.assertEqual(child.name,'repo-f1-sectioned-audit-zas.zip');self.assertTrue(child.exists())
  self.assertEqual(len(list(self.out.glob('*.zip'))),2)
  self.assertFalse(list(self.root.rglob('*.sha256')))
  with zipfile.ZipFile(self.parent) as z:self.assertNotIn('ZAS-AUDIT.md',z.namelist());self.assertIn('PACK-MANIFEST.json',z.namelist())
  with zipfile.ZipFile(child) as z:self.assertIn('ZAS-AUDIT.md',z.namelist());self.assertFalse(any(n.endswith('.sha256') for n in z.namelist()))
  self.assertTrue(zas.verify(child,self.parent)['valid'])
 def test_idempotent_pair_reuses_both(self):
  a=self.finalize();before=self.parent.read_bytes();b=self.finalize()
  self.assertTrue(b['idempotent']);self.assertTrue(b['zas_companion']['companion']['reused']);self.assertEqual(before,self.parent.read_bytes())
 def test_no_zas_no_companion(self):
  self.link.update(status='NOT_USED',companion_filename=None);(self.stage/'ZAS-LINK.json').write_text(json.dumps(self.link))
  r=self.finalize(with_zas=False);self.assertEqual(r['zas_companion']['status'],'NOT_USED');self.assertEqual(len(list(self.out.glob('*.zip'))),1)
 def test_missing_companion_does_not_report_completion(self):
  self.finalize(with_zas=False,ok=False)
  receipt=json.loads((self.repo/'.agent-work/audit/f1/PACK-STATE.json').read_text());self.assertEqual(receipt['status'],'PAIR_INCOMPLETE')
  parent_before=self.parent.read_bytes();r=self.finalize();self.assertTrue(r['idempotent']);self.assertEqual(parent_before,self.parent.read_bytes())
 def test_wrong_run_rejected_then_only_companion_fixed(self):
  self.row['run_id']='other';self.write_row();self.finalize(ok=False)
  old=self.parent.read_bytes();self.row['run_id']='r1';self.write_row();r=self.finalize();self.assertTrue(r['idempotent']);self.assertEqual(old,self.parent.read_bytes())
 def test_child_is_not_independent_feature(self):
  self.finalize();r=intake.intake(zas.companion_path(self.parent));self.assertEqual(r['class'],'ZAS_COMPANION_CANDIDATE');self.assertFalse(r['count_as_feature'])
 def test_parent_replacement_invalidates_companion(self):
  self.finalize();child=zas.companion_path(self.parent)
  with zipfile.ZipFile(child) as z:old=z.read('ZAS-IDENTITY.json')
  (self.stage/'SUMMARY.md').write_text('corrected')
  r=self.finalize();self.assertFalse(r['idempotent'])
  with zipfile.ZipFile(child) as z:new=z.read('ZAS-IDENTITY.json')
  self.assertNotEqual(json.loads(old)['parent']['sha256'],json.loads(new)['parent']['sha256'])
  self.assertTrue(zas.verify(child,self.parent)['valid'])
 def test_stale_or_forged_companion_hash_blocked(self):
  self.finalize();child=zas.companion_path(self.parent)
  with zipfile.ZipFile(child) as z:items={n:z.read(n) for n in z.namelist()}
  ident=json.loads(items['ZAS-IDENTITY.json']);ident['parent']['sha256']='0'*64;items['ZAS-IDENTITY.json']=json.dumps(ident).encode()
  m=json.loads(items['PACK-MANIFEST.json'])
  for row in m['files']:row['sha256']=zas.sha(items[row['path']])
  items['PACK-MANIFEST.json']=json.dumps(m).encode()
  with zipfile.ZipFile(child,'w') as z:
   for name,data in items.items():z.writestr(name,data)
  with self.assertRaises(zas.Invalid):zas.verify(child,self.parent)
 def test_encrypted_content_cannot_enter_selected_evidence(self):
  (self.zstage/'receipt.json').write_text(json.dumps({'nested':[{'encrypted_content':'NEVER'}]}));self.finalize(ok=False)
 def test_main_cannot_embed_detailed_zas_payload(self):
  (self.stage/'ZAS-AUDIT.md').write_text('wrong archive');self.finalize(ok=False)
 def test_mismatched_companion_name_rejected(self):
  self.link['companion_filename']='somewhere-else.zip';(self.stage/'ZAS-LINK.json').write_text(json.dumps(self.link));self.finalize(ok=False)
 def test_parent_manifest_contains_no_sha_file_and_tamper_rejected(self):
  self.finalize()
  with zipfile.ZipFile(self.parent,'a') as z:z.writestr('UNLISTED.md','injected')
  self.assertTrue(main.verify_zip(self.parent))
if __name__=='__main__':unittest.main()
