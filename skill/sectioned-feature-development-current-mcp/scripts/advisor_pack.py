#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, stat, tempfile, time, zipfile
from pathlib import Path

SECRET_NAMES={'.env','.env.local','.env.production','id_rsa','id_ed25519','credentials.json','secrets.json'}
SECRET_PATTERNS=[re.compile(rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'),re.compile(rb'(?i)(?:api[_-]?key|token|secret|password)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{20,}')]
EXCLUDE_PARTS={'.venv','venv','node_modules','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','target','dist','build','.next','.svelte-kit'}

def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',default='.');ap.add_argument('--feature',required=True);ap.add_argument('--trigger',required=True);ap.add_argument('--request',required=True);ap.add_argument('--output-dir',default='~/Desktop/advisor-pack');a=ap.parse_args()
 repo=Path(a.repo).resolve();outdir=Path(a.output_dir).expanduser();outdir.mkdir(parents=True,exist_ok=True)
 if not (repo/'.git').exists():raise SystemExit('repository .git directory is required')
 risky=[];files=[]
 for p in repo.rglob('*'):
  if p.is_dir():continue
  rel=p.relative_to(repo)
  if any(x in EXCLUDE_PARTS for x in rel.parts):continue
  if p.name in SECRET_NAMES or p.suffix.lower() in {'.pem','.p12','.pfx','.key'}:risky.append(str(rel));continue
  try:
   if p.stat().st_size<=2_000_000:
    data=p.read_bytes()
    if any(rx.search(data) for rx in SECRET_PATTERNS):risky.append(str(rel));continue
  except Exception:pass
  files.append((p,rel))
 if risky:
  block=repo/'.agent-work'/'advisor'/'PACKAGE-BLOCKED.json';block.parent.mkdir(parents=True,exist_ok=True);block.write_text(json.dumps({'status':'BLOCKED_SECRET_REVIEW','paths':risky},indent=2));raise SystemExit('secret-like files require human review: '+', '.join(risky[:20]))
 req=repo/'.agent-work'/'advisor'/a.request/'ADVISOR-REQUEST.md'
 if not req.exists():raise SystemExit(f'missing {req}')
 name=f'{repo.name}-{a.feature}-{a.trigger}.zip';target=outdir/name
 fd,tmp=tempfile.mkstemp(prefix=name+'.',suffix='.tmp',dir=outdir);os.close(fd);tmp=Path(tmp)
 manifest=[]
 try:
  with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED,allowZip64=True) as z:
   for p,rel in files:
    arc=str(Path(repo.name)/rel);z.write(p,arc);manifest.append({'path':arc,'size':p.stat().st_size,'sha256':sha(p)})
   meta={'schema':'advisor-pack-v1','repo':repo.name,'feature':a.feature,'trigger':a.trigger,'request':a.request,'created_at':time.time(),'files':manifest}
   z.writestr(str(Path(repo.name)/'ADVISOR-PACK-MANIFEST.json'),json.dumps(meta,indent=2))
  with zipfile.ZipFile(tmp) as z:
   bad=z.testzip()
   if bad:raise RuntimeError('zip crc failed: '+bad)
  os.replace(tmp,target)
 finally:
  if tmp.exists():tmp.unlink()
 side=target.with_suffix(target.suffix+'.sha256');side.write_text(sha(target)+'  '+target.name+'\n')
 print(json.dumps({'path':str(target),'sha256':sha(target),'file_count':len(manifest)}))
if __name__=='__main__':main()
