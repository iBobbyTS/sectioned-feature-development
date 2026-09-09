#!/usr/bin/env python3
"""Local external-advisor export: worktree + Git, no model, upload, reset or checkout.

Restores 3.9 operation while supporting the linked worktrees retained in 4.x.
Secret detection is best-effort; compressed Git history still needs human review.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import tempfile
import time
import zipfile
from pathlib import Path

SECRET_NAMES={'.env','.env.local','.env.production','id_rsa','id_ed25519','credentials.json','secrets.json'}
SECRET_PATTERNS=[re.compile(rb'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'),re.compile(rb'(?i)(?:api[_-]?key|token|secret|password)\s*[:=]\s*["\']?[A-Za-z0-9_\-]{20,}'),re.compile(rb'https?://[^\s/@:]+:[^\s/@]+@')]
EXCLUDE_PARTS={'.venv','venv','node_modules','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','target','dist','build','.next','.svelte-kit'}
ID=re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$')

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def git(repo,*args,check=True):
 return subprocess.run(['git','-C',str(repo),*args],check=check,capture_output=True).stdout

def collect(root,arc,tracked=(),exclusions=None,metadata=False):
 exclusions=exclusions if exclusions is not None else []
 result=[]
 for base,dirs,names in os.walk(root,followlinks=False):
  b=Path(base)
  for n in list(dirs):
   p=b/n;rel=p.relative_to(root).as_posix()
   if p.is_symlink():result.append((p,str(Path(arc)/rel)));dirs.remove(n);continue
   in_git=metadata or rel=='.git' or rel.startswith('.git/')
   if not in_git and n in EXCLUDE_PARTS and not any(t==rel or t.startswith(rel+'/') for t in tracked):
    exclusions.append(str(Path(arc)/rel));dirs.remove(n)
  for n in names:
   p=b/n;rel=p.relative_to(root).as_posix()
   if p.is_symlink() or p.is_file():result.append((p,str(Path(arc)/rel)))
   else:exclusions.append(str(Path(arc)/rel)+' (non-regular)')
 return result

def build(repo,feature,trigger,request,output_dir):
 repo=repo.resolve();outdir=output_dir.expanduser().resolve()
 if not all(ID.fullmatch(x) for x in (repo.name,feature,trigger,request)):raise ValueError('invalid export identity')
 if not (repo/'.git').exists():raise ValueError('repository .git directory or linked-worktree file required')
 if outdir.is_relative_to(repo):raise ValueError('advisor output directory must be outside repository')
 req=repo/'.agent-work/advisor'/request/'ADVISOR-REQUEST.md'
 if not req.is_file():raise ValueError('missing '+str(req))
 head=git(repo,'rev-parse','HEAD').decode().strip()
 status=git(repo,'status','--porcelain=v1','-z','--untracked-files=all')
 gd=Path(git(repo,'rev-parse','--absolute-git-dir').decode().strip()).resolve()
 common=Path(git(repo,'rev-parse','--path-format=absolute','--git-common-dir').decode().strip()).resolve()
 tracked=[x for x in git(repo,'ls-files','-z').decode().split('\0') if x]
 exclusions=[];files=collect(repo,repo.name,tracked,exclusions)
 linked=(repo/'.git').is_file()
 if linked:
  files+=collect(common,'GIT-METADATA/common',metadata=True)
  if gd!=common:files+=collect(gd,'GIT-METADATA/worktree',metadata=True)
 risky=[]
 for p,arc in files:
  if p.is_symlink():continue  # never follow or read external targets
  if p.name in SECRET_NAMES or p.suffix.lower() in {'.pem','.p12','.pfx','.key'}:risky.append(arc);continue
  if p.stat().st_size<=2_000_000 and any(rx.search(p.read_bytes()) for rx in SECRET_PATTERNS):risky.append(arc)
 if risky:
  block=req.parent/'PACKAGE-BLOCKED.json';block.write_text(json.dumps({'status':'BLOCKED_SECRET_REVIEW','paths':sorted(set(risky))},indent=2))
  raise ValueError('secret-like files require human review: '+', '.join(risky[:20]))
 outdir.mkdir(parents=True,exist_ok=True);target=outdir/f'{repo.name}-{feature}-{trigger}.zip'
 if target.is_symlink():raise ValueError('canonical output is a symlink')
 manifest=[]
 with tempfile.TemporaryDirectory(prefix='.advisor-',dir=outdir) as temp:
  temp=Path(temp);bundle=temp/'repository.bundle';archive=temp/'output.zip'
  git(repo,'bundle','create',str(bundle),'--all','HEAD')
  git(repo,'bundle','verify',str(bundle))
  files.append((bundle,'GIT-METADATA/repository.bundle'))
  with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,allowZip64=True) as z:
   for p,arc in files:
    st=p.lstat()
    if stat.S_ISLNK(st.st_mode):
     data=os.readlink(p).encode();info=zipfile.ZipInfo(arc);info.create_system=3;info.external_attr=(stat.S_IFLNK|0o777)<<16
     z.writestr(info,data);manifest.append({'path':arc,'kind':'symlink','size':len(data),'sha256':hashlib.sha256(data).hexdigest()});continue
    h=hashlib.sha256();size=0;info=zipfile.ZipInfo.from_file(p,arc);info.compress_type=zipfile.ZIP_DEFLATED
    with p.open('rb') as source,z.open(info,'w',force_zip64=True) as dest:
     for data in iter(lambda:source.read(1024*1024),b''):dest.write(data);h.update(data);size+=len(data)
    if p.stat().st_mtime_ns!=st.st_mtime_ns or size!=st.st_size:raise ValueError('source changed during freeze: '+arc)
    manifest.append({'path':arc,'kind':'file','size':size,'sha256':h.hexdigest()})
   for name,args in [('STATUS.txt',('status','--short')),('DIFF.patch',('diff','--binary','HEAD')),('INDEX.patch',('diff','--binary','--cached')),('REFS.txt',('show-ref',)),('SUBMODULES.txt',('submodule','status','--recursive'))]:
    data=git(repo,*args,check=False);arc='GIT-EVIDENCE/'+name;z.writestr(arc,data);manifest.append({'path':arc,'size':len(data),'sha256':hashlib.sha256(data).hexdigest(),'kind':'file'})
   restore='Read-only archive. For portable reconstruction: git clone GIT-METADATA/repository.bundle restored; checkout the frozen HEAD; overlay the archived worktree excluding its .git pointer/directory. Original Git metadata is separately preserved for inspection; absolute linked-worktree pointers are not portable. No submodule/LFS download was performed. Check metadata and missing external objects before claiming full restoration.\n'
   z.writestr('RESTORE.md',restore);manifest.append({'path':'RESTORE.md','kind':'file','size':len(restore.encode()),'sha256':hashlib.sha256(restore.encode()).hexdigest()})
   meta={'schema':'advisor-pack-v1','repo':repo.name,'feature':feature,'trigger':trigger,'request':request,'head':head,'linked_worktree':linked,
    'created_at':time.time(),'files':manifest,'exclusions':sorted(exclusions),'git_bundle_verified':True,'history_secret_scan':'NOT_CERTIFIED_MANUAL_SHARING_REVIEW_REQUIRED','automatic_upload':False}
   z.writestr(repo.name+'/ADVISOR-PACK-MANIFEST.json',json.dumps(meta,indent=2))
  if git(repo,'rev-parse','HEAD').decode().strip()!=head or git(repo,'status','--porcelain=v1','-z','--untracked-files=all')!=status:raise ValueError('Git changed during packaging; keep feature paused')
  with zipfile.ZipFile(archive) as z:
   bad=z.testzip()
   if bad:raise ValueError('zip crc failure: '+bad)
  os.replace(archive,target)
 digest=sha(target)
 receipt={'path':str(target),'sha256':digest,'file_count':len(manifest),'head':head,'git_bundle_verified':True,'request_id':request,'share_status':'HUMAN_REVIEW_REQUIRED'}
 (req.parent/'PACKAGE-RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
 return receipt

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',default='.');ap.add_argument('--feature',required=True);ap.add_argument('--trigger',required=True);ap.add_argument('--request',required=True);ap.add_argument('--output-dir',default='~/Desktop/advisor-pack');a=ap.parse_args()
 try:print(json.dumps(build(Path(a.repo),a.feature,a.trigger,a.request,Path(a.output_dir))));return 0
 except (OSError,ValueError,subprocess.CalledProcessError) as exc:print(str(exc),file=__import__('sys').stderr);return 2
if __name__=='__main__':raise SystemExit(main())
