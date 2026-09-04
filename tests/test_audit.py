import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'skill/sectioned-feature-development/scripts'))
import audit as a

class AuditTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'stage';self.root.mkdir();self.out=Path(self.tmp.name)/'output'
  self.m=json.loads((ROOT/'skill/sectioned-feature-development/assets/AUDIT-METADATA.template.json').read_text())
  self.m['secret_review']='PASSED'
  for name in a.REQUIRED:
   (self.root/name).write_text('# evidence gap stated\n')
  (self.root/'events.jsonl').write_text('')
  self.update()
 def tearDown(self):self.tmp.cleanup()
 def update(self):
  (self.root/'metadata.json').write_text(json.dumps(self.m))
  manifest=a.manifest(self.root,list(a.REQUIRED))
  (self.root/'EVIDENCE-MANIFEST.json').write_text(json.dumps(manifest))
 def test_publish_verify_idempotent(self):
  r=a.publish(self.root,self.out);self.assertTrue(a.verify(Path(r['path']))['valid'])
  r2=a.publish(self.root,self.out);self.assertTrue(r2['reused']);self.assertEqual(r['sha256'],r2['sha256'])
  self.assertEqual(len(list(self.out.glob('*.zip'))),1)
 def test_changed_requires_explicit_replace(self):
  r=a.publish(self.root,self.out);(self.root/'SUMMARY.md').write_text('corrected');self.update()
  with self.assertRaises(a.Invalid):a.publish(self.root,self.out)
  new=a.publish(self.root,self.out,replace=True);self.assertEqual(new['path'],r['path']);self.assertNotEqual(new['sha256'],r['sha256'])
 def test_foreign_metadata_blocked(self):
  self.m['artifact_type']='runtime-conformance'
  with self.assertRaises(a.Invalid):a.metadata(self.m)
 def test_event_identity_and_duplicates_blocked(self):
  event={'feature_id':'wrong','run_id':self.m['run_id'],'event_id':'e','capture':'LIVE','family':'review'}
  (self.root/'events.jsonl').write_text(json.dumps(event)+'\n');self.update()
  with self.assertRaises(a.Invalid):a.inputs(self.root)
  event['feature_id']=self.m['feature_id'];(self.root/'events.jsonl').write_text((json.dumps(event)+'\n')*2);self.update()
  with self.assertRaises(a.Invalid):a.inputs(self.root)
 def test_secret_and_nested_archive_paths_blocked(self):
  for name in ['.env','runtime.zip','.git/config','target/x']:
   with self.subTest(name=name),self.assertRaises(a.Invalid):a.safe_file(self.root,name)
  (self.root/'SUMMARY.md').write_text('-----BEGIN PRIVATE KEY-----');self.update()
  with self.assertRaises(a.Invalid):a.publish(self.root,self.out)
 def test_symlink_and_path_escape_blocked(self):
  (self.root/'outside').symlink_to(Path(self.tmp.name)/'outside')
  for rel in ['../outside','outside','/etc/passwd']:
   with self.subTest(rel=rel),self.assertRaises(a.Invalid):a.safe_file(self.root,rel)
 def test_hash_tamper_blocked(self):
  (self.root/'SUMMARY.md').write_text('changed after freeze')
  with self.assertRaises(a.Invalid):a.publish(self.root,self.out)
 def test_complete_requires_identity_sources(self):
  self.m['coverage']='COMPLETE';self.update()
  with self.assertRaises(a.Invalid):a.inputs(self.root)
 def rewrite_zip(self,path,changes):
  with zipfile.ZipFile(path) as z:items={n:z.read(n) for n in z.namelist()}
  items.update(changes)
  manifest=json.loads(items['EVIDENCE-MANIFEST.json'])
  for row in manifest['files']:row['sha256']=a.sha(items[row['path']])
  items['EVIDENCE-MANIFEST.json']=json.dumps(manifest).encode()
  with zipfile.ZipFile(path,'w') as z:
   for name,data in items.items():z.writestr(name,data)
 def test_verify_rejects_hash_consistent_wrong_event_identity(self):
  p=Path(a.publish(self.root,self.out)['path'])
  e={'feature_id':'foreign','run_id':self.m['run_id'],'event_id':'e','capture':'LIVE','family':'review'}
  self.rewrite_zip(p,{'events.jsonl':json.dumps(e).encode()})
  with self.assertRaises(a.Invalid):a.verify(p)
 def test_verify_rejects_hash_consistent_wrong_source_identity(self):
  p=Path(a.publish(self.root,self.out)['path'])
  self.m['identity']['requirements_path']='REQUIREMENTS.md'
  self.m['identity']['requirements_sha256']='f'*64
  self.rewrite_zip(p,{'metadata.json':json.dumps(self.m).encode()})
  with self.assertRaises(a.Invalid):a.verify(p)
 def test_auxiliary_filter(self):
  z=Path(self.tmp.name)/'case-3.zip'
  with zipfile.ZipFile(z,'w') as f:f.writestr('SUMMARY.md','runtime stdout')
  self.assertEqual(a.intake(z)['class'],'EXCLUDED_AUXILIARY')
 def test_legacy_filter_not_current(self):
  z=Path(self.tmp.name)/'legacy.zip'
  with zipfile.ZipFile(z,'w') as f:
   for n in ['AUDIT-VERDICT.md','PLAN-AUDIT.md','REVIEW-AUDIT.md','INVOCATION-AUDIT.md']:f.writestr(n,'legacy')
  self.assertEqual(a.intake(z)['class'],'LEGACY_PROCESS')
if __name__=='__main__':unittest.main()
