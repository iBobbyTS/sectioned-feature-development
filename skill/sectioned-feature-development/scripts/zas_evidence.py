#!/usr/bin/env python3
"""Validate ZAS compact observation facts. No model, progress classifier, timer, or cancel."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

PROTOCOL = 'zas-observation/1.1'
BASE_TOOLS = {'zcode_subagent_' + n for n in ('status','spawn','poll','list','send','respond','cancel','result','close')}
REQUIRED_TOOLS = BASE_TOOLS | {'zcode_subagent_observe'}
class Invalid(ValueError): pass

def no_encrypted_content(value):
    if isinstance(value, dict):
        if 'encrypted_content' in value: raise Invalid('ENCRYPTED_CONTENT_EXCLUDED')
        for v in value.values(): no_encrypted_content(v)
    elif isinstance(value, list):
        for v in value: no_encrypted_content(v)

def exact(obj, fields, code):
    if not isinstance(obj,dict) or set(obj) != set(fields): raise Invalid(code)

def integer(value, minimum=0):
    return type(value) is int and value >= minimum

def capabilities(status: dict, catalog: dict) -> dict:
    tools={t.get('name') if isinstance(t,dict) else t for t in catalog.get('tools',[])}
    if not REQUIRED_TOOLS.issubset(tools): raise Invalid('ZAS_INSTALLATION_CONTRACT_MISMATCH')
    obs=status.get('capabilities',{}).get('observation',{})
    if (obs.get('protocol') != PROTOCOL or obs.get('public_reasoning_default') is not True
        or obs.get('runtime_source_verified') is not True
        or obs.get('defaults') != {'top_tools':3,'recent_calls_per_tool':5,'reasoning_chars':200}):
        raise Invalid('ZAS_INSTALLATION_CONTRACT_MISMATCH')
    return {'mode':'OBSERVATION_READY','observation_usable':True,
            'service_generation':status.get('service_generation','UNKNOWN'),
            'semantic_progress':'NOT_INFERRED'}

def check_snapshot(page: dict, agent_id: str) -> dict:
    no_encrypted_content(page)
    exact(page, {'schema','agent_id','service_generation','snapshot_seq','count_scope','tools','reasoning','coverage'}, 'OBSERVATION_SHAPE_INVALID')
    if page['schema']!=PROTOCOL or page['agent_id']!=agent_id: raise Invalid('OBSERVATION_IDENTITY_MISMATCH')
    if not isinstance(page['service_generation'],str) or not page['service_generation']: raise Invalid('GENERATION_MISSING')
    if not integer(page['snapshot_seq']) or page['count_scope']!='agent_lifetime': raise Invalid('COUNT_SCOPE_OR_SEQUENCE_INVALID')
    if len(json.dumps(page,ensure_ascii=False).encode('utf-8'))>65536: raise Invalid('OBSERVATION_OUT_OF_BOUND')
    groups=page['tools']
    if not isinstance(groups,list) or len(groups)>3: raise Invalid('TOOL_GROUP_BOUND')
    names=set(); seen=set(); order=[]; total=0
    for group in groups:
        exact(group, {'tool_name','call_count','recent_calls'}, 'TOOL_GROUP_SHAPE_INVALID')
        name=group['tool_name'];count=group['call_count'];calls=group['recent_calls']
        if not isinstance(name,str) or not name or name in names: raise Invalid('TOOL_NAME_INVALID')
        names.add(name)
        if not integer(count,1) or not isinstance(calls,list) or not 1<=len(calls)<=min(5,count): raise Invalid('TOOL_CALL_BOUND')
        seqs=[]
        for call in calls:
            exact(call, {'seq','tool_call_id','arguments','arguments_truncated','redacted_fields'}, 'CALLS_ONLY_NO_RESULTS')
            seq=call['seq'];cid=call['tool_call_id']
            if not integer(seq,1) or seq>page['snapshot_seq'] or not isinstance(cid,str) or not cid or cid in seen: raise Invalid('CALL_IDENTITY_OR_SEQUENCE_INVALID')
            if not isinstance(call['arguments'],dict) or type(call['arguments_truncated']) is not bool or not integer(call['redacted_fields']): raise Invalid('CALL_ARGUMENTS_INVALID')
            seen.add(cid);seqs.append(seq);total+=1
        if seqs!=sorted(set(seqs),reverse=True): raise Invalid('RECENT_CALL_ORDER_INVALID')
        order.append((-count,-seqs[0],name))
    if order!=sorted(order): raise Invalid('TOP_TOOL_ORDER_INVALID')
    r=page['reasoning'];exact(r,{'text','char_count','truncated','source'},'REASONING_SHAPE_INVALID')
    if not isinstance(r['text'],str) or len(r['text'])>200 or type(r['char_count']) is not int or r['char_count']!=len(r['text']) or type(r['truncated']) is not bool: raise Invalid('REASONING_CHARACTER_BOUND')
    src=r['source'];exact(src,{'status','runtime_version','event_type','delta_pointer'},'REASONING_SOURCE_REQUIRED')
    if src['status']!='VERIFIED_RUNTIME_PUBLIC' or any(not isinstance(src[k],str) or not src[k] for k in ('runtime_version','event_type','delta_pointer')) or not src['delta_pointer'].startswith('/') or 'encrypted_content' in src['delta_pointer'].split('/'):
        raise Invalid('REASONING_SOURCE_UNVERIFIED')
    cov=page['coverage'];exact(cov,{'tool_history_complete','reasoning_complete','dropped_events'},'COVERAGE_REQUIRED')
    if any(type(cov[k]) is not bool for k in ('tool_history_complete','reasoning_complete')) or not integer(cov['dropped_events']): raise Invalid('COVERAGE_INVALID')
    return {'agent_id':agent_id,'service_generation':page['service_generation'],'snapshot_seq':page['snapshot_seq'],
            'tool_groups':len(groups),'tool_calls':total,'reasoning_chars':r['char_count'],
            'coverage':'BOUNDED_SNAPSHOT' if all(cov[k] for k in ('tool_history_complete','reasoning_complete')) and not cov['dropped_events'] else 'GAPPED',
            'semantic_progress':'NOT_INFERRED','automatic_action':None}


def compact_capabilities(status: dict, catalog: dict) -> dict:
    """Approved compact contract only; no fabricated source or version proof."""
    tools={t.get('name') if isinstance(t,dict) else t for t in catalog.get('tools',[])}
    obs=status.get('capabilities',{}).get('observation',{})
    if not REQUIRED_TOOLS.issubset(tools) or obs.get('public_reasoning_default') is not True or obs.get('defaults') != {'top_tools':3,'recent_calls_per_tool':5,'reasoning_chars':200}:
        raise Invalid('ZAS_COMPACT_CONTRACT_MISMATCH')
    return {'mode':'COMPACT_OBSERVATION_READY','source_provenance':'NOT_PUBLICLY_ECHOED','semantic_progress':'NOT_INFERRED'}


def compact_snapshot(page: dict, agent_id: int) -> dict:
    """Validate bounded wire content; tool-call correlation, not echoed ID, identifies task."""
    if type(agent_id) is not int or not 10000000<=agent_id<=99999999: raise Invalid('TASK_ID_RANGE')
    no_encrypted_content(page)
    exact(page,{'tools','reasoning','coverage'},'COMPACT_OBSERVATION_SHAPE')
    if len(json.dumps(page,ensure_ascii=False).encode('utf-8'))>65536: raise Invalid('OBSERVATION_OUT_OF_BOUND')
    groups=page['tools']
    if not isinstance(groups,list) or len(groups)>3: raise Invalid('TOOL_GROUP_BOUND')
    names=set();seen=set();order=[];total=0
    for g in groups:
        exact(g,{'tool_name','call_count','recent_calls'},'TOOL_GROUP_SHAPE_INVALID')
        name=g['tool_name'];count=g['call_count'];calls=g['recent_calls']
        if not isinstance(name,str) or not name or name in names:raise Invalid('TOOL_NAME_INVALID')
        names.add(name)
        if not integer(count,1) or not isinstance(calls,list) or not 1<=len(calls)<=min(5,count):raise Invalid('TOOL_CALL_BOUND')
        seqs=[]
        for c in calls:
            exact(c,{'seq','tool_call_id','arguments','arguments_truncated','redacted_fields'},'CALLS_ONLY_NO_RESULTS')
            seq=c['seq'];cid=c['tool_call_id']
            if not integer(seq,1) or not isinstance(cid,str) or not cid or cid in seen:raise Invalid('CALL_IDENTITY_OR_SEQUENCE_INVALID')
            if not isinstance(c['arguments'],dict) or type(c['arguments_truncated']) is not bool or not integer(c['redacted_fields']):raise Invalid('CALL_ARGUMENTS_INVALID')
            seen.add(cid);seqs.append(seq);total+=1
        if seqs!=sorted(set(seqs),reverse=True):raise Invalid('RECENT_CALL_ORDER_INVALID')
        order.append((-count,-seqs[0],name))
    if order!=sorted(order):raise Invalid('TOP_TOOL_ORDER_INVALID')
    r=page['reasoning'];exact(r,{'text','truncated'},'REASONING_SHAPE_INVALID')
    if not isinstance(r['text'],str) or len(r['text'])>200 or type(r['truncated']) is not bool:raise Invalid('REASONING_CHARACTER_BOUND')
    c=page['coverage'];exact(c,{'tool_history_complete','reasoning_complete','dropped_events'},'COVERAGE_REQUIRED')
    if any(type(c[k]) is not bool for k in ('tool_history_complete','reasoning_complete')) or not integer(c['dropped_events']):raise Invalid('COVERAGE_INVALID')
    return {'agent_id_from_call':agent_id,'identity_check':'CALL_CORRELATION_NOT_ATTESTED_BY_PAYLOAD','tool_groups':len(groups),'tool_calls':total,'reasoning_chars':len(r['text']),'source_provenance':'NOT_PUBLICLY_ECHOED','semantic_progress':'NOT_INFERRED','automatic_action':None,'coverage':'GAPPED' if not all(c[k] for k in ('tool_history_complete','reasoning_complete')) or c['dropped_events'] else 'BOUNDED_SNAPSHOT'}

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    c=sub.add_parser('capabilities');c.add_argument('--compact',action='store_true');c.add_argument('--status',type=Path,required=True);c.add_argument('--catalog',type=Path,required=True)
    c=sub.add_parser('snapshot');c.add_argument('--compact',action='store_true');c.add_argument('--page',type=Path,required=True);c.add_argument('--agent-id',required=True)
    a=p.parse_args()
    try:
        if a.command=='capabilities':
            result=(compact_capabilities if a.compact else capabilities)(json.loads(a.status.read_text()),json.loads(a.catalog.read_text()))
        else:
            result=compact_snapshot(json.loads(a.page.read_text()),int(a.agent_id)) if a.compact else check_snapshot(json.loads(a.page.read_text()),a.agent_id)
        print(json.dumps(result,ensure_ascii=False,indent=2));return 0
    except (Invalid,ValueError,TypeError,OSError,AttributeError,KeyError) as exc:
        print(json.dumps({'valid':False,'error':str(exc)}));return 2
if __name__=='__main__':raise SystemExit(main())
