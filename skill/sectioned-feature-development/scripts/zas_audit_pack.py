#!/usr/bin/env python3
"""Publish one feature-associated ZAS companion ZIP; hashes live in JSON, not sidecar files."""
from __future__ import annotations
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile
import zipfile

KIND = 'sectioned-development-zas-audit'
PRODUCER = 'sectioned-feature-development'
PROCESS_KIND = 'sectioned-development-process-audit'
REQUIRED = {'ZAS-IDENTITY.json','ZAS-AUDIT.md','ZAS-RUNS.jsonl'}
GENERATED = {'PACK-MANIFEST.json','.FINALIZE.lock','PACK-STATE.json'}
class Invalid(ValueError): pass

def sha(data): return hashlib.sha256(data).hexdigest()

def companion_path(parent: Path) -> Path:
    if parent.suffix!='.zip' or parent.name.endswith('-zas.zip'): raise Invalid('PRIMARY_PROCESS_ZIP_REQUIRED')
    return parent.with_name(parent.stem+'-zas.zip')

def parent_identity(parent: Path) -> dict:
    if parent.is_symlink() or not parent.is_file(): raise Invalid('PARENT_ARCHIVE_MISSING_OR_SYMLINK')
    with zipfile.ZipFile(parent) as z:
        if 'PROCESS-IDENTITY.json' in z.namelist():
            import audit_finalize
            errors=audit_finalize.verify_zip(parent)
            if errors: raise Invalid('PARENT_MANIFEST_INVALID: '+'; '.join(errors))
            ident=json.loads(z.read('PROCESS-IDENTITY.json'))
            if ident.get('kind')!=PROCESS_KIND or ident.get('producer')!=PRODUCER: raise Invalid('NOT_SFD_PARENT')
            head=ident.get('source_head')
        elif 'metadata.json' in z.namelist():
            import process_audit
            process_audit.verify(parent)
            ident=json.loads(z.read('metadata.json'))
            if ident.get('artifact_type')!=PROCESS_KIND or ident.get('producer',{}).get('name')!=PRODUCER: raise Invalid('NOT_SFD_PARENT')
            head=ident.get('source_head')
        else: raise Invalid('NOT_SFD_PARENT')
        if not ident.get('feature_id') or not ident.get('run_id'): raise Invalid('PARENT_IDENTITY_INCOMPLETE')
        link=json.loads(z.read('ZAS-LINK.json')) if 'ZAS-LINK.json' in z.namelist() else None
    return {'feature_id':ident['feature_id'],'run_id':ident['run_id'],'source_head':head,'filename':parent.name,'sha256':sha(parent.read_bytes()),'link':link}

def validate_link(info, parent):
    link=info['link']
    if not isinstance(link,dict) or link.get('status') not in {'USED','NOT_USED'}: raise Invalid('PARENT_ZAS_LINK_REQUIRED')
    if (link.get('feature_id'),link.get('run_id'))!=(info['feature_id'],info['run_id']): raise Invalid('PARENT_LINK_IDENTITY_MISMATCH')
    expected=companion_path(parent).name if link['status']=='USED' else None
    if link.get('companion_filename')!=expected: raise Invalid('COMPANION_NAME_MISMATCH')
    return link['status']

def validate_payload(files, info):
    import process_audit
    from zas_evidence import no_encrypted_content, check_snapshot
    if not REQUIRED.issubset(files): raise Invalid('ZAS_REQUIRED_EVIDENCE_MISSING')
    ident=json.loads(files['ZAS-IDENTITY.json'])
    if (ident.get('kind'),ident.get('producer'))!=(KIND,PRODUCER): raise Invalid('NOT_ZAS_COMPANION')
    if (ident.get('feature_id'),ident.get('run_id'))!=(info['feature_id'],info['run_id']): raise Invalid('ZAS_IDENTITY_MISMATCH')
    seen=set()
    for line in files['ZAS-RUNS.jsonl'].decode().splitlines():
        if not line.strip(): continue
        row=json.loads(line);pid=row.get('physical_attempt_id')
        if (row.get('feature_id'),row.get('run_id'))!=(info['feature_id'],info['run_id']): raise Invalid('CROSS_FEATURE_ATTEMPT')
        if not isinstance(pid,str) or not pid or pid in seen: raise Invalid('ATTEMPT_ID_REQUIRED_UNIQUE')
        seen.add(pid)
    if not seen: raise Invalid('USED_REQUIRES_ATTEMPT_RECORD')
    for name,data in files.items():
        process_audit.safe_path(name)
        if process_audit.SECRET.search(data): raise Invalid('SECRET_IN_ZAS_EVIDENCE: '+name)
        if name.endswith('.json'):
            obj=json.loads(data);no_encrypted_content(obj)
            if name.startswith('observations/'):
                check_snapshot(obj,obj.get('agent_id'))
        elif name.endswith('.jsonl'):
            for line in data.decode().splitlines():
                if line.strip(): no_encrypted_content(json.loads(line))
    return ident

def staging_files(stage: Path):
    import process_audit
    if stage.is_symlink() or not stage.is_dir(): raise Invalid('ZAS_STAGE_REQUIRED')
    files={}
    for p in sorted(stage.rglob('*')):
        if p.is_symlink(): raise Invalid('SYMLINK_ZAS_EVIDENCE')
        if not p.is_file(): continue
        rel=p.relative_to(stage).as_posix()
        if rel in GENERATED: continue
        if p.suffix=='.sha256': raise Invalid('NO_SHA256_FILES')
        files[rel]=process_audit.safe_file(stage,rel).read_bytes()
    return files

def verify(archive: Path, parent: Path) -> dict:
    if archive.is_symlink() or archive.resolve()!=companion_path(parent).resolve(): raise Invalid('COMPANION_PATH_MISMATCH')
    info=parent_identity(parent)
    if validate_link(info,parent)!='USED': raise Invalid('PARENT_DID_NOT_USE_ZAS')
    with zipfile.ZipFile(archive) as z:
        import process_audit, stat
        names=z.namelist()
        if len(set(names))!=len(names) or z.testzip(): raise Invalid('COMPANION_ZIP_INVALID')
        for entry in z.infolist():
            process_audit.safe_path(entry.filename)
            if entry.is_dir() or stat.S_ISLNK(entry.external_attr>>16) or entry.file_size>32*1024*1024: raise Invalid('INVALID_COMPANION_MEMBER')
        manifest=json.loads(z.read('PACK-MANIFEST.json'));rows=manifest.get('files',[])
        if len({r['path'] for r in rows})!=len(rows) or set(names)!={r['path'] for r in rows}|{'PACK-MANIFEST.json'}: raise Invalid('COMPANION_MANIFEST_CONTENT_MISMATCH')
        files={r['path']:z.read(r['path']) for r in rows}
        if any(sha(files[r['path']])!=r['sha256'] for r in rows): raise Invalid('COMPANION_MANIFEST_HASH_MISMATCH')
    ident=validate_payload(files,info)
    parent_ref={k:info[k] for k in ('feature_id','run_id','source_head','filename','sha256')}
    if ident.get('parent')!=parent_ref: raise Invalid('STALE_OR_WRONG_PARENT')
    return {'valid':True,'kind':KIND,'feature_id':info['feature_id'],'run_id':info['run_id'],
            'path':str(archive.resolve()),'sha256':sha(archive.read_bytes()),'parent_sha256':info['sha256'],'count_as_feature':False}

def publish(stage: Path, parent: Path) -> dict:
    parent=parent.expanduser().resolve();stage=stage.expanduser()
    info=parent_identity(parent)
    if validate_link(info,parent)!='USED': raise Invalid('PARENT_DID_NOT_USE_ZAS')
    if not stage.is_dir() or stage.is_symlink(): raise Invalid('ZAS_STAGE_REQUIRED')
    dest=companion_path(parent)
    if dest.is_symlink(): raise Invalid('COMPANION_OUTPUT_SYMLINK')
    with (stage/'.FINALIZE.lock').open('a+') as lock:
        fcntl.flock(lock.fileno(),fcntl.LOCK_EX)
        files=staging_files(stage);ident=validate_payload(files,info)
        ident['parent']={k:info[k] for k in ('feature_id','run_id','source_head','filename','sha256')}
        files['ZAS-IDENTITY.json']=(json.dumps(ident,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()
        rows=[{'path':name,'sha256':sha(data),'size':len(data)} for name,data in sorted(files.items())]
        files['PACK-MANIFEST.json']=(json.dumps({'schema':1,'files':rows},indent=2)+'\n').encode()
        reused=False
        if dest.exists():
            try:
                with zipfile.ZipFile(dest) as z:
                    reused=len(z.namelist())==len(files) and set(z.namelist())==set(files) and all(z.read(k)==v for k,v in files.items()) and z.testzip() is None
            except (OSError,zipfile.BadZipFile): pass
        if not reused:
            fd,tmp=tempfile.mkstemp(prefix='.'+dest.stem+'-',suffix='.zip',dir=dest.parent);os.close(fd)
            try:
                with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED) as z:
                    for name,data in sorted(files.items()):
                        entry=zipfile.ZipInfo(name,date_time=(2026,1,1,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o100600<<16;z.writestr(entry,data)
                with zipfile.ZipFile(tmp) as z:
                    if z.testzip(): raise Invalid('ZIP_CRC_FAILURE')
                if sha(parent.read_bytes())!=info['sha256']: raise Invalid('PARENT_CHANGED_DURING_FINALIZE')
                os.replace(tmp,dest)
            finally:
                if os.path.exists(tmp): os.unlink(tmp)
        result={**verify(dest,parent),'reused':reused}
        tmp_state=stage/'PACK-STATE.json.tmp';tmp_state.write_text(json.dumps(result,indent=2)+'\n');os.replace(tmp_state,stage/'PACK-STATE.json')
        return result

def complete_optional_pair(parent: Path, stage: Path|None):
    info=parent_identity(parent)
    if info['link'] is None:
        if stage: raise Invalid('PARENT_ZAS_LINK_REQUIRED')
        return {'status':'NOT_USED','companion':None}
    status=validate_link(info,parent)
    if status=='NOT_USED':
        if stage: raise Invalid('NOT_USED_HAS_ZAS_STAGE')
        return {'status':'NOT_USED','companion':None}
    if stage is None: raise Invalid('ZAS_COMPANION_STAGE_REQUIRED')
    return {'status':'COMPLETE','companion':publish(stage,parent)}

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    c=sub.add_parser('finalize');c.add_argument('--parent-zip',type=Path,required=True);c.add_argument('--pack-dir',type=Path,required=True)
    c=sub.add_parser('verify');c.add_argument('--parent-zip',type=Path,required=True);c.add_argument('--zip',type=Path,required=True)
    a=p.parse_args()
    try:
        result=publish(a.pack_dir,a.parent_zip) if a.command=='finalize' else verify(a.zip,a.parent_zip)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile) as exc:
        print(json.dumps({'status':'INCOMPLETE','error':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
