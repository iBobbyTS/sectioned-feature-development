#!/usr/bin/env python3
"""Validate caller-side ZAS observation identity/cursors; never decides semantic progress or cancels an agent."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

PROTOCOL='zas-observation/1'
BASE_TOOLS={'zcode_subagent_'+n for n in ('status','spawn','poll','list','send','respond','cancel','result','close')}

class Invalid(ValueError):pass

def capabilities(status: dict, catalog: dict) -> dict:
    tools={t.get('name') if isinstance(t,dict) else t for t in catalog.get('tools',[])}
    if not BASE_TOOLS.issubset(tools):raise Invalid('CURRENT_LIFECYCLE_TOOL_MISSING')
    obs=status.get('capabilities',{}).get('observation',{})
    enhanced=(obs.get('protocol')==PROTOCOL and 'zcode_subagent_observe' in tools)
    return {'mode':'ENHANCED_OBSERVATION' if enhanced else 'BETA_BASELINE_LIMITED',
            'observation_usable':enhanced,'service_generation':status.get('service_generation','UNKNOWN'),
            'public_content_supported':enhanced and obs.get('public_content') is True,
            'maturity':'CONTROLLED_BETA','semantic_progress':'NOT_INFERRED'}

def check_window(page: dict, agent_id: str, after_seq: int=0, stream_id: str|None=None, public_content_authorized: bool=False) -> dict:
    if page.get('schema')!=PROTOCOL or page.get('agent_id')!=agent_id:raise Invalid('OBSERVATION_IDENTITY_MISMATCH')
    epoch=page.get('stream_id');gap=page.get('gap')
    if not isinstance(epoch,str) or not epoch or not isinstance(gap,dict) or type(gap.get('present')) is not bool:raise Invalid('OBSERVATION_STREAM_OR_GAP_MISSING')
    if stream_id and stream_id!=epoch and not gap['present']:raise Invalid('STREAM_CHANGED_WITHOUT_GAP')
    first=page.get('first_available_seq');nxt=page.get('next_seq')
    if any(type(x) is not int or x<0 for x in (after_seq,first,nxt)):raise Invalid('INVALID_SEQUENCE')
    if stream_id in {None,epoch} and nxt<after_seq:raise Invalid('CURSOR_REGRESSED')
    if first>after_seq+1 and stream_id in {None,epoch} and not gap['present']:raise Invalid('RETENTION_GAP_UNDECLARED')
    events=page.get('events')
    if not isinstance(events,list) or len(events)>100 or len(json.dumps(page,ensure_ascii=False).encode('utf-8'))>65536:raise Invalid('OBSERVATION_WINDOW_OUT_OF_BOUND')
    if type(page.get('has_more')) is not bool:raise Invalid('PAGINATION_STATE_MISSING')
    last=-1;count=0
    for event in events:
        seq=event.get('seq')
        if type(seq) is not int or seq<first or seq<=last or seq>nxt:raise Invalid('EVENT_SEQUENCE_INVALID')
        if stream_id in {None,epoch} and seq<=after_seq:raise Invalid('EVENT_CURSOR_REPLAY')
        if event.get('agent_id',agent_id)!=agent_id:raise Invalid('CROSS_AGENT_EVENT')
        if event.get('visibility') not in {'metadata','runtime_public'}:raise Invalid('UNSUPPORTED_PRIVATE_VISIBILITY')
        if event.get('content') is not None:
            if not public_content_authorized or event.get('visibility')!='runtime_public':raise Invalid('PUBLIC_CONTENT_NOT_AUTHORIZED')
        last=seq;count+=1
    loss=page.get('loss')
    if not isinstance(loss,dict) or any(type(loss.get(k)) is not int or loss[k]<0 for k in ('dropped_events','redacted_fields','truncated_events')):raise Invalid('LOSS_ACCOUNTING_REQUIRED')
    # Gaps/empty event lists never imply no-progress; the orchestrator must reason with the task.
    return {'agent_id':agent_id,'stream_id':epoch,'next_seq':nxt,'event_count':count,
            'coverage':'GAPPED' if gap['present'] or loss['dropped_events'] else 'BOUNDED_WINDOW',
            'semantic_progress':'NOT_INFERRED','automatic_action':None}

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    c=sub.add_parser('capabilities');c.add_argument('--status',type=Path,required=True);c.add_argument('--catalog',type=Path,required=True)
    c=sub.add_parser('window');c.add_argument('--page',type=Path,required=True);c.add_argument('--agent-id',required=True);c.add_argument('--after-seq',type=int,default=0);c.add_argument('--stream-id');c.add_argument('--public-content-authorized',action='store_true')
    a=p.parse_args()
    try:
        if a.command=='capabilities':result=capabilities(json.loads(a.status.read_text()),json.loads(a.catalog.read_text()))
        else:result=check_window(json.loads(a.page.read_text()),a.agent_id,a.after_seq,a.stream_id,a.public_content_authorized)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (Invalid,ValueError,TypeError,OSError,AttributeError) as exc:print(json.dumps({'valid':False,'error':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
