#!/usr/bin/env python3
"""Typed process-audit packaging. Explicit evidence only; no session crawling or model calls."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import tempfile
import zipfile

TYPE='sectioned-development-process-audit'
PRODUCER='sectioned-feature-development'
ID=re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$')
REQUIRED={'metadata.json','SUMMARY.md','REQUIREMENTS.md','PLAN-AUDIT.md','REVIEW-AUDIT.md',
 'MODEL-TASK-AUDIT.md','PARALLEL-AUDIT.md','VALIDATION-AUDIT.md','ADVISOR-AUDIT.md','COST-METRICS.md','events.jsonl'}
BLOCKED={'.git','node_modules','__pycache__','.venv','target','build','dist','.cache','raw-sessions'}
SECRET=re.compile(rb'-----BEGIN (?:[A-Z ]+)?PRIVATE KEY-----|\b(?:sk-[A-Za-z0-9_-]{24,}|ghp_[A-Za-z0-9]{30,})\b')

class Invalid(ValueError): pass

def sha(data: bytes) -> str:return hashlib.sha256(data).hexdigest()

def metadata(m: dict):
 if not isinstance(m,dict) or not isinstance(m.get('producer'),dict) or not isinstance(m.get('identity'),dict):
  raise Invalid('invalid metadata envelope')
 if m.get('artifact_type')!=TYPE or m.get('schema_version')!=4 or m.get('producer',{}).get('name')!=PRODUCER:
  raise Invalid('NOT_SFD_PROCESS_AUDIT')
 for k in ('repo','feature_id','run_id'):
  if not isinstance(m.get(k),str) or not ID.fullmatch(m[k]):raise Invalid(f'invalid {k}')
 if not re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})',str(m.get('source_head',''))):raise Invalid('source head required')
 if m.get('coverage') not in {'COMPLETE','COMPLETE_WITH_GAPS','INCOMPLETE'}:raise Invalid('coverage required')
 if m.get('secret_review')!='PASSED':raise Invalid('human/agent secret review is not recorded as PASSED')
 for key in ('requirements_sha256','plan_sha256'):
  if not re.fullmatch('[a-f0-9]{64}',str(m.get('identity',{}).get(key,''))):raise Invalid('identity digest required')

def safe_path(value: str) -> PurePosixPath:
 if not isinstance(value,str):raise Invalid('invalid evidence path type')
 p=PurePosixPath(value)
 if not value or p.is_absolute() or '..' in p.parts or '\\' in value or any(c in value for c in '\n\r'):
  raise Invalid('unsafe evidence path')
 if any(x in BLOCKED for x in p.parts) or any(x.startswith('.env') for x in p.parts) or p.suffix.lower() in {'.zip','.pem','.key','.p12','.pfx'}:
  raise Invalid('foreign archive/cache/secret path forbidden')
 return p

def safe_file(root: Path, value: str) -> Path:
 p=safe_path(value)
 q=root.joinpath(*p.parts)
 for a in [q,*list(q.parents)[:len(p.parts)-1]]:
  if a.is_symlink():raise Invalid('symlink evidence forbidden')
 if not q.is_file() or not q.resolve().is_relative_to(root.resolve()):raise Invalid('evidence outside staging')
 if q.stat().st_size>32*1024*1024:raise Invalid('large evidence requires a separate external artifact reference')
 return q

def validate_payload(m: dict, result: dict[str,bytes]) -> None:
 metadata(m)
 event_ids=set()
 for n,line in enumerate(result['events.jsonl'].decode('utf-8').splitlines(),1):
  if not line.strip():continue
  e=json.loads(line)
  if not isinstance(e,dict) or e.get('feature_id')!=m['feature_id'] or e.get('run_id')!=m['run_id']:
   raise Invalid(f'event identity mismatch line {n}')
  if not isinstance(e.get('family'),str) or not e['family'] or not isinstance(e.get('event_id'),str) or not e['event_id'] or e.get('capture') not in {'LIVE','RECONSTRUCTED'}:
   raise Invalid(f'invalid event envelope line {n}')
  if e.get('family')=='subsection':
   if not isinstance(e.get('parent_section_id'),str) or not isinstance(e.get('subsection_id'),str) or not e.get('lineage_id') or e['parent_section_id']==e['subsection_id']:
    raise Invalid('subsection event requires distinct parent/child and inherited lineage')
   if e.get('section_id') not in {None,e['parent_section_id']}:raise Invalid('subsection event section_id must name parent')
  if e['event_id'] in event_ids:raise Invalid('duplicate event ID')
  event_ids.add(e['event_id'])
 for key,pathkey in [('plan_sha256','plan_path'),('requirements_sha256','requirements_path')]:
  ref=m['identity'].get(pathkey)
  if ref and (not isinstance(ref,str) or ref not in result or sha(result[ref])!=m['identity'][key]):raise Invalid('identity artifact hash mismatch')
  if m['coverage']=='COMPLETE' and not ref:raise Invalid('COMPLETE requires exact identity artifact paths')

def inputs(root: Path) -> tuple[dict,dict[str,bytes]]:
 root=root.resolve()
 if (root/'metadata.json').is_symlink() or (root/'EVIDENCE-MANIFEST.json').is_symlink():raise Invalid('symlink manifest')
 m=json.loads((root/'metadata.json').read_text());metadata(m)
 spec=json.loads((root/'EVIDENCE-MANIFEST.json').read_text())
 if not isinstance(spec,dict) or spec.get('schema_version')!=4 or spec.get('feature_id')!=m['feature_id'] or spec.get('run_id')!=m['run_id']:raise Invalid('manifest identity mismatch')
 rows=spec.get('files',[])
 if not isinstance(rows,list) or any(not isinstance(x,dict) for x in rows):raise Invalid('bad manifest')
 paths=[r.get('path') for r in rows]
 if any(not isinstance(p,str) for p in paths) or len(set(paths))!=len(paths):raise Invalid('duplicate/invalid manifest paths')
 if not REQUIRED.issubset(paths):raise Invalid('required process artifacts missing')
 result={}
 for row in rows:
  data=safe_file(root,row['path']).read_bytes()
  if sha(data)!=row.get('sha256'):raise Invalid('source hash mismatch: '+row['path'])
  if SECRET.search(data):raise Invalid('possible secret; redact locally before publishing: '+row['path'])
  result[row['path']]=data
 validate_payload(m,result)
 result['EVIDENCE-MANIFEST.json']=(root/'EVIDENCE-MANIFEST.json').read_bytes()
 return m,result

def manifest(root: Path, paths: list[str]) -> dict:
 m=json.loads((root/'metadata.json').read_text());metadata(m)
 return {'schema_version':4,'feature_id':m['feature_id'],'run_id':m['run_id'],
  'files':[{'path':p,'sha256':sha(safe_file(root,p).read_bytes())} for p in sorted(set(paths))]}

def verify(path: Path) -> dict:
 with zipfile.ZipFile(path) as z:
  infos=z.infolist();names=[i.filename for i in infos]
  if len(set(names))!=len(names):raise Invalid('duplicate archive paths')
  for info in infos:
   safe_path(info.filename)
   mode=info.external_attr>>16
   if stat.S_ISLNK(mode) or info.is_dir():raise Invalid('only regular evidence files allowed')
   if info.file_size>32*1024*1024:raise Invalid('large evidence requires a separate external artifact reference')
  if z.testzip():raise Invalid('CRC-invalid archive')
  m=json.loads(z.read('metadata.json'));metadata(m)
  spec=json.loads(z.read('EVIDENCE-MANIFEST.json'))
  if not isinstance(spec,dict) or spec.get('schema_version')!=4 or spec.get('feature_id')!=m['feature_id'] or spec.get('run_id')!=m['run_id']:raise Invalid('manifest identity mismatch')
  rows=spec.get('files')
  if not isinstance(rows,list) or any(not isinstance(r,dict) or not isinstance(r.get('path'),str) for r in rows):raise Invalid('invalid manifest rows')
  expected={r['path'] for r in rows}
  if len(expected)!=len(rows) or set(names)!=expected|{'EVIDENCE-MANIFEST.json'} or not REQUIRED.issubset(expected):
   raise Invalid('unexpected/missing archive content')
  payload={}
  for r in rows:
   data=z.read(r['path'])
   if sha(data)!=r.get('sha256'):raise Invalid('manifest hash failure')
   if SECRET.search(data):raise Invalid('possible secret in evidence: '+r['path'])
   payload[r['path']]=data
  validate_payload(m,payload)
 return {'valid':True,'feature_id':m['feature_id'],'run_id':m['run_id'],'sha256':sha(path.read_bytes())}

def publish(root: Path, output: Path, replace: bool=False) -> dict:
 m,files=inputs(root)
 output=output.expanduser();output.mkdir(parents=True,exist_ok=True)
 path=output/f'{m["repo"]}-{m["feature_id"]}-{m["run_id"]}-sfd-audit.zip'
 if path.is_symlink():raise Invalid('canonical output is a symlink')
 if path.exists():
  with zipfile.ZipFile(path) as z:
   if set(z.namelist())==set(files) and all(z.read(k)==v for k,v in files.items()):
    return {**verify(path),'path':str(path.resolve()),'reused':True}
  if not replace:raise Invalid('canonical pack differs; one explicit --replace after correction, no timestamp retry')
 fd,tmp=tempfile.mkstemp(prefix='.sfd-',suffix='.zip',dir=output);os.close(fd)
 try:
  with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED) as z:
   for name,data in sorted(files.items()):
    info=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
    info.external_attr=0o100600<<16;z.writestr(info,data)
  result=verify(Path(tmp));os.replace(tmp,path)
  # Sidecar is part of this protocol, not another audit purpose.
  side=path.with_suffix('.zip.sha256');side.write_text(result['sha256']+'  '+path.name+'\n')
  return {**result,'path':str(path.resolve()),'reused':False}
 finally:
  if os.path.exists(tmp):os.unlink(tmp)

def intake(path: Path) -> dict:
 try:
  with zipfile.ZipFile(path) as z:
   ns=z.namelist();ms=[n for n in ns if n.rsplit('/',1)[-1]=='metadata.json']
   for n in ms:
    m=json.loads(z.read(n))
    if m.get('artifact_type')==TYPE and m.get('schema_version')==4:
     return {'class':'PROCESS_V4_CANDIDATE','needs':'verify identity and manifest before counting'}
   matches=[n for n in ns if n.rsplit('/',1)[-1]=='PROCESS-IDENTITY.json']
   for n in matches:
    m=json.loads(z.read(n))
    if m.get('kind')==TYPE and m.get('producer')==PRODUCER and m.get('run_id'):
     return {'class':'PROCESS_V42_CANDIDATE','needs':'verify manifest and exact Git identity with audit_finalize.py'}
   required={'AUDIT-VERDICT.md','PLAN-AUDIT.md','REVIEW-AUDIT.md','INVOCATION-AUDIT.md','SKILL-COMPLIANCE.md'}
   matched=required & {n.rsplit('/',1)[-1] for n in ns}
   if len(matched)>=4:return {'class':'LEGACY_PROCESS','reason':'multiple process documents; provenance still needs review'}
   return {'class':'EXCLUDED_AUXILIARY','reason':'no typed workflow process provenance'}
 except (OSError,ValueError,zipfile.BadZipFile,KeyError):return {'class':'INVALID_ARCHIVE'}

def main():
 ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='cmd',required=True)
 q=sp.add_parser('manifest');q.add_argument('staging',type=Path);q.add_argument('files',nargs='+')
 q=sp.add_parser('publish');q.add_argument('staging',type=Path);q.add_argument('--output',type=Path,default=Path('~/Desktop/audit-pack'));q.add_argument('--replace',action='store_true')
 for n in ('verify','intake'):
  q=sp.add_parser(n);q.add_argument('archive',type=Path)
 a=ap.parse_args()
 try:
  if a.cmd=='manifest':result=manifest(a.staging,a.files)
  elif a.cmd=='publish':result=publish(a.staging,a.output,a.replace)
  elif a.cmd=='verify':result=verify(a.archive)
  else:result=intake(a.archive)
  print(json.dumps(result,ensure_ascii=False,indent=2));return 0
 except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile) as e:
  print(json.dumps({'valid':False,'error':str(e)},ensure_ascii=False));return 2
if __name__=='__main__':raise SystemExit(main())
