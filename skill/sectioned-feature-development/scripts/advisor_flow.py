#!/usr/bin/env python3
"""External human-advisor pause/intake. Does not invoke a model or approve product scope."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
import execution_artifacts as e
import workflow as w

TRIGGERS={'ADV-01','ADV-02','ADV-03','ADV-04','ADV-05','ADV-06'}

def request(repo: Path, request_id: str, trigger: str, request_path: Path):
    state=e.load(repo)
    if trigger not in TRIGGERS or not w.ID.fullmatch(request_id):raise w.Invalid('INVALID_ADVISOR_REQUEST_ID')
    if state.get('status')=='COMPLETED' or state.get('completion'):raise w.Invalid('CLOSED_FEATURE')
    if state.get('advisor_state') in w.ADVISOR_BLOCKING_STATES:raise w.Invalid('ADVISOR_ALREADY_PENDING')
    if trigger not in request_path.read_text():raise w.Invalid('REQUEST_TRIGGER_MISMATCH')
    proof=e.proof(request_path,repo)
    target=repo/'.agent-work/advisor'/request_id
    target.mkdir(parents=True,exist_ok=True)
    dest=target/'ADVISOR-REQUEST.md'
    if dest.exists() and dest.resolve()!=request_path.resolve():raise w.Invalid('ADVISOR_REQUEST_EXISTS')
    if dest.resolve()!=request_path.resolve():shutil.copy2(request_path,dest)
    state['advisor']={'request_id':request_id,'trigger':trigger,'request':e.proof(dest,repo),
        'head':e.git(repo,'rev-parse','HEAD'),'requested_at':e.now(),'prior_next_action':state.get('next_action')}
    state['advisor_state']='REQUIRED';state['next_action']='STOP_ACTORS_THEN_PACKAGE_FOR_HUMAN'
    e.audit_event(repo,state,'advisor_required','advisor',{'request_id':request_id,'trigger_id':trigger,'head':state['advisor']['head'],'request_sha256':proof['sha256']})
    e.save(repo,state);return {'state':'REQUIRED','active_actors_to_stop':[a.get('actor_id') for a in state.get('active',[])]}

def package(repo: Path, output: Path):
    state=e.load(repo);a=state.get('advisor',{})
    if state.get('advisor_state') not in {'REQUIRED','PACKAGE_BLOCKED'}:raise w.Invalid('NO_ADVISOR_PACKAGE_PENDING')
    if state.get('active'):raise w.Invalid('STOP_AND_RECORD_ALL_ACTORS_FIRST')
    e.verify(a['request'],repo)
    # Freeze once all actors have stopped; the actual request must name this HEAD.
    head=e.git(repo,'rev-parse','HEAD')
    if head!=a['head']:raise w.Invalid('FROZEN_ADVISOR_HEAD_CHANGED: update the request explicitly')
    cmd=[sys.executable,str(Path(__file__).with_name('advisor_pack.py')),'--repo',str(repo),'--feature',state['feature_id'],
         '--trigger',a['trigger'],'--request',a['request_id'],'--output-dir',str(output)]
    proc=subprocess.run(cmd,text=True,capture_output=True)
    if proc.returncode:
        state['advisor_state']='PACKAGE_BLOCKED';state['next_action']='HUMAN_PACKAGE_BLOCKER'
        e.audit_event(repo,state,'advisor_package_blocked','advisor',{'request_id':a['request_id'],'error':'PACKAGE_FAILED'})
        e.save(repo,state);raise w.Invalid('ADVISOR_PACKAGE_BLOCKED: '+(proc.stderr or proc.stdout).strip()[:1000])
    result=json.loads(proc.stdout)
    a['package']=result;state['advisor_state']='WAITING_EXTERNAL';state['next_action']='WAIT_FOR_HUMAN_ADVISOR_RESULT'
    e.audit_event(repo,state,'advisor_package_ready','advisor',{'request_id':a['request_id'],'package_sha256':result['sha256']})
    e.save(repo,state);return result

def receive(repo: Path, result: Path):
    state=e.load(repo);a=state.get('advisor',{})
    if state.get('advisor_state')!='WAITING_EXTERNAL':raise w.Invalid('NOT_WAITING_EXTERNAL')
    if not result.is_file() or not result.read_text().strip():raise w.Invalid('ADVISOR_RESULT_MISSING')
    dest=repo/'.agent-work/advisor'/a['request_id']/'ADVISOR-RESULT.md'
    if dest.exists():
        # Preserve every verbatim decision round; clarification never overwrites prior evidence.
        index=len(a.get('result_history',[]))+1
        previous=dest.with_name(f'ADVISOR-RESULT.r{index}.md')
        if previous.exists():raise w.Invalid('ADVISOR_RESULT_ARCHIVE_EXISTS')
        shutil.copy2(dest,previous)
        a.setdefault('result_history',[]).append(e.proof(previous,repo))
    if dest.resolve()!=result.resolve():shutil.copy2(result,dest)
    a['result']=e.proof(dest,repo);a['received_at']=e.now()
    state['advisor_state']='WAITING_HUMAN_DECISION';state['next_action']='ASK_HUMAN_ADOPTION'
    e.audit_event(repo,state,'advisor_result_received','advisor',{'request_id':a['request_id'],'result_sha256':a['result']['sha256']})
    e.save(repo,state);return {'state':state['advisor_state'],'result':a['result']}

def adopt(repo: Path, decision: str, human_record: Path, resume_phase: str):
    state=e.load(repo);a=state.get('advisor',{})
    if state.get('advisor_state')!='WAITING_HUMAN_DECISION':raise w.Invalid('HUMAN_ADOPTION_NOT_PENDING')
    if decision not in {'accept','reject','request-clarification'}:raise w.Invalid('INVALID_ADOPTION')
    e.verify(a['result'],repo)
    if e.git(repo,'rev-parse','HEAD')!=a['head']:raise w.Invalid('ADVISOR_FROZEN_HEAD_CHANGED')
    record=e.obj(human_record)
    if record.get('request_id')!=a['request_id'] or record.get('decision')!=decision or not record.get('user_message_id') or not record.get('verbatim_user_message'):
        raise w.Invalid('ACTUAL_HUMAN_ADOPTION_RECEIPT_REQUIRED')
    if decision!='request-clarification' and not resume_phase:raise w.Invalid('EXPLICIT_RESUME_PHASE_REQUIRED')
    if state.get('active'):raise w.Invalid('ACTIVE_ACTOR_BARRIER')
    if a.get('adoption'):a.setdefault('adoption_history',[]).append(a['adoption'])
    a['adoption']=e.proof(human_record,repo);a['decision']=decision;a['resume_phase']=resume_phase
    state['advisor_state']='WAITING_EXTERNAL' if decision=='request-clarification' else ('DECISION_APPLIED' if decision=='accept' else 'HUMAN_REJECTED')
    state['next_action']='WAIT_FOR_ADVISOR_CLARIFICATION' if decision=='request-clarification' else resume_phase
    # No mutation to plan/review/repair/accepted-section state, no implicit merge or reset.
    e.audit_event(repo,state,'advisor_decision_adopted','advisor',{'request_id':a['request_id'],'decision':decision,'resume_phase':resume_phase,'adoption_sha256':a['adoption']['sha256']})
    e.save(repo,state);return {'state':state['advisor_state'],'next_action':state['next_action']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,default=Path.cwd());sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('request');q.add_argument('--request-id',required=True);q.add_argument('--trigger',choices=sorted(TRIGGERS),required=True);q.add_argument('--request-file',type=Path,required=True)
    q=sub.add_parser('package');q.add_argument('--output-dir',type=Path,default=Path('~/Desktop/advisor-pack'))
    q=sub.add_parser('receive');q.add_argument('--result',type=Path,required=True)
    q=sub.add_parser('adopt');q.add_argument('--decision',choices=['accept','reject','request-clarification'],required=True);q.add_argument('--human-record',type=Path,required=True);q.add_argument('--resume-phase',default='')
    a=p.parse_args();repo=a.repo.resolve()
    try:
        if a.command=='request':r=request(repo,a.request_id,a.trigger,a.request_file)
        elif a.command=='package':r=package(repo,a.output_dir.expanduser())
        elif a.command=='receive':r=receive(repo,a.result)
        else:r=adopt(repo,a.decision,a.human_record,a.resume_phase)
        print(json.dumps(r,ensure_ascii=False,indent=2));return 0
    except (w.Invalid,ValueError,KeyError,OSError,subprocess.CalledProcessError) as exc:
        print(json.dumps({'ok':False,'error':str(exc)},ensure_ascii=False));return 2
if __name__=='__main__':raise SystemExit(main())
