#!/usr/bin/env python3
"""Install SFD, companion code-review, and named Codex agents. Dry-run by default; never rewrites AGENTS.md."""
from __future__ import annotations
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import tempfile
import time
import tomllib

ROOT=Path(__file__).resolve().parents[1]

def file_hash(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def agent_files():
 files=sorted((ROOT/'agents').glob('*.toml'))
 for p in files:
  d=tomllib.loads(p.read_text())
  if d.get('name')!=p.stem or not all(d.get(k) for k in ('description','model','model_reasoning_effort','developer_instructions','sandbox_mode')):
   raise ValueError(f'invalid agent configuration {p.name}')
 return files

def targets(home, only='all'):
 names=['code-review'] if only=='code-review' else ['sectioned-feature-development','code-review']
 for name in names:
  if not (ROOT/'skill'/name/'SKILL.md').is_file():
   raise ValueError(f'missing bundled skill: {name}')
 items=[(ROOT/'skill'/name,home/'skills'/name) for name in names]
 if only=='all':items += [(p,home/'agents'/p.name) for p in agent_files()]
 return items

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--codex-home',type=Path,default=Path(os.environ.get('CODEX_HOME','~/.codex')).expanduser())
 p.add_argument('--apply',action='store_true');p.add_argument('--replace',action='store_true')
 p.add_argument('--only',choices=['all','code-review'],default='all',help='all installs both skills and agents; code-review updates only the companion')
 a=p.parse_args();home=a.codex_home.expanduser().resolve()
 try:
  items=targets(home,a.only)
  for src,dst in items:
   if dst.is_symlink():raise ValueError(f'refusing symlink target: {dst}')
   print(f'{src.relative_to(ROOT)} -> {dst}'+(' [exists]' if dst.exists() else ''))
  if not a.apply:
   print('DRY_RUN: no files changed. --apply installs; --replace backs up existing targets first.');return 0
  occupied=[dst for _,dst in items if dst.exists()]
  if occupied and not a.replace:raise ValueError('targets exist; review dry-run, then use --replace to back them up')
  home.mkdir(parents=True,exist_ok=True)
  backup=None
  if occupied:
   parent=home/'sfd-backups';parent.mkdir(exist_ok=True)
   backup=Path(tempfile.mkdtemp(prefix=time.strftime('%Y%m%d-%H%M%S-'),dir=parent))
   for dst in occupied:
    out=backup/dst.relative_to(home);out.parent.mkdir(parents=True,exist_ok=True)
    if dst.is_dir():shutil.copytree(dst,out)
    else:shutil.copy2(dst,out)
  # Prepare all replacements before modifying existing destinations.
  with tempfile.TemporaryDirectory(prefix='.sfd-install-',dir=home) as temp:
   staged=[]
   for index,(src,dst) in enumerate(items):
    candidate=Path(temp)/str(index)
    if src.is_dir():shutil.copytree(src,candidate,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.DS_Store'))
    else:shutil.copy2(src,candidate)
    staged.append((candidate,dst))
   for candidate,dst in staged:
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.is_dir():shutil.rmtree(dst)  # exact named target already backed up; no unrelated paths
    elif dst.exists():dst.unlink()
    shutil.move(str(candidate),str(dst))
  print(f'INSTALLED. Backup: {backup or "none"}. AGENTS.md, other agents, global config and old differently named skills unchanged.')
  print('Verify exact model/effort availability and fresh-context launch in your actual Codex installation before use.')
  return 0
 except (ValueError,OSError) as e:print('ERROR:',e);return 2
if __name__=='__main__':raise SystemExit(main())
