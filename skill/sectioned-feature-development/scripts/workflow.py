#!/usr/bin/env python3
"""SFD v4 plan/DAG checks and narrow local state helpers. No Git mutations or agent calls."""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import tempfile

PROFILES = {'luna_xhigh', 'terra_high', 'sol_medium', 'astra_medium'}
SHA = re.compile(r'^(?:[a-f0-9]{40}|[a-f0-9]{64})$')
ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,95}$')
BEGIN, END = '<!-- SFD_PLAN_V4 -->', '<!-- /SFD_PLAN_V4 -->'

class Invalid(ValueError):
    pass

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load_plan(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise Invalid('exactly one marked PLAN v4 schedule is required')
    block = text.split(BEGIN, 1)[1].split(END, 1)[0].strip()
    match = re.fullmatch(r'```json\s*\n(.*?)\n```', block, re.S)
    if not match:
        raise Invalid('marked schedule must be one fenced JSON object')
    plan = json.loads(match.group(1))
    validate(plan)
    return plan

def path_prefix(value: str) -> str:
    if not isinstance(value, str) or not value or '\\' in value or any(c in value for c in '*?[]'):
        raise Invalid('path must be a literal relative file/directory prefix')
    p = PurePosixPath(value)
    if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] in {'.git', '.agent-work', 'git-worktree'}:
        raise Invalid(f'unsafe product path: {value}')
    return str(p).rstrip('/')

def overlap(a: str, b: str) -> bool:
    a, b = path_prefix(a), path_prefix(b)
    return a == b or a.startswith(b + '/') or b.startswith(a + '/')

def conflicts(a: dict, b: dict) -> list[str]:
    reasons = []
    for x in a['write_paths']:
        for y in b['write_paths'] + b['read_paths']:
            if overlap(x, y): reasons.append(f'path:{x}<->{y}')
    for x in b['write_paths']:
        for y in a['read_paths']:
            if overlap(x, y): reasons.append(f'path:{x}<->{y}')
    for name in set(a['exclusive_resources']) & set(b['exclusive_resources']):
        reasons.append('resource:' + name)
    for name in ((set(a['mutates_contracts']) & set(b['mutates_contracts'] + b['consumes_contracts'])) |
                 (set(b['mutates_contracts']) & set(a['consumes_contracts']))):
        reasons.append('contract:' + name)
    return sorted(set(reasons))

def validate(p: dict) -> None:
    if not isinstance(p, dict) or p.get('schema_version') != 4:
        raise Invalid('unsupported plan schema')
    for key in ('feature_id', 'run_id'):
        if not isinstance(p.get(key), str) or not ID.fullmatch(p[key]): raise Invalid(f'invalid {key}')
    if p.get('invocation_source') not in {'USER_EXPLICIT','CUSTOM_INSTRUCTIONS_AUTO','AGENT_DISCRETION'}:
        raise Invalid('invalid invocation_source')
    if p.get('execution_mode') not in {'PLAN_ONLY', 'EXECUTE_NO_COMMIT', 'EXECUTE_WITH_COMMITS'}:
        raise Invalid('invalid execution_mode')
    if not SHA.fullmatch(str(p.get('base_ref', ''))): raise Invalid('exact base_ref required')
    if not isinstance(p.get('feature_branch'), str) or not isinstance(p.get('main_branch'), str):
        raise Invalid('branch names required')
    if p.get('status') not in {'DRAFT','APPROVED','COMPLETED'}: raise Invalid('invalid plan status')
    if not re.fullmatch(r'[a-f0-9]{64}', str(p.get('requirements_sha256', ''))):
        raise Invalid('requirements SHA-256 required')
    n = p.get('max_parallel_writers')
    if type(n) is not int or n < 1 or n > 16: raise Invalid('invalid max_parallel_writers')
    if n > 2 and not p.get('parallel_capacity_authority'):
        raise Invalid('more than two writers requires recorded capacity authority')
    sections = p.get('sections')
    if not isinstance(sections, list) or not sections: raise Invalid('sections required')
    if len(sections) > 1 and p['execution_mode'] != 'EXECUTE_WITH_COMMITS':
        raise Invalid('MULTI_SECTION_REQUIRES_COMMITS')
    if p['execution_mode'] == 'EXECUTE_WITH_COMMITS':
        if not p['feature_branch'] or p['feature_branch'] == p['main_branch']:
            raise Invalid('DEDICATED_FEATURE_BRANCH_REQUIRED')
        if not p.get('branch_authority'): raise Invalid('branch base authority required')
    if n > 1 and not p.get('worktree_parent') == 'git-worktree':
        raise Invalid('parallel worktrees must live in ./git-worktree')
    if n > 1 and p['execution_mode'] != 'EXECUTE_WITH_COMMITS':
        raise Invalid('parallel writers require commit mode')
    if not isinstance(p.get('stages'), list) or not p['stages']:
        raise Invalid('stage concurrency policy is required')
    completed_stages = set()
    for stage in p['stages']:
        if not isinstance(stage,dict) or not ID.fullmatch(str(stage.get('id',''))): raise Invalid('invalid stage')
        if stage['id'] in completed_stages or not isinstance(stage.get('depends_on'),list): raise Invalid('duplicate stage or missing prerequisites')
        if not set(stage['depends_on']).issubset(completed_stages): raise Invalid('stages must be acyclic and in execution order')
        if stage.get('parallelism') not in {'serial','bounded-independent-queries','section-dag','candidate-independent'}: raise Invalid('explicit stage parallelism required')
        completed_stages.add(stage['id'])
    if not isinstance(p.get('checks'),dict):raise Invalid('existing check command registry required')
    ids = [s.get('id') for s in sections if isinstance(s, dict)]
    if len(ids) != len(sections) or len(set(ids)) != len(ids) or any(not isinstance(i,str) or not ID.fullmatch(i) for i in ids):
        raise Invalid('unique section IDs required')
    for s in sections:
        for key in ('depends_on','write_paths','read_paths','exclusive_resources','mutates_contracts',
                    'consumes_contracts','requirement_ids','check_ids'):
            if not isinstance(s.get(key), list) or any(not isinstance(v,str) for v in s[key]):
                raise Invalid(f'{s["id"]}: {key} must be a list of strings')
        if any(cid not in p['checks'] for cid in s['check_ids']):raise Invalid('unknown check ID')
        if not s['write_paths'] or not s['requirement_ids'] or not s['check_ids']:
            raise Invalid(f'{s["id"]}: scope, requirements and checks required')
        for path in s['write_paths'] + s['read_paths']: path_prefix(path)
        if any(x not in ids or x == s['id'] for x in s['depends_on']): raise Invalid('invalid dependency')
        if len(set(s['depends_on'])) != len(s['depends_on']): raise Invalid('duplicate dependency')
        if s.get('profile') not in PROFILES: raise Invalid('unknown implementation profile')
        if s.get('assurance') not in {'ONE','TWO'}: raise Invalid('resolved assurance required')
        if type(s.get('parallel_eligible')) is not bool: raise Invalid('parallel_eligible must be boolean')
        for key in ('owner','parallel_reason','acceptance','model_reason','oracle'):
            if not isinstance(s.get(key), str) or not s[key].strip(): raise Invalid(f'{s["id"]}: missing {key}')
        features = s.get('task_features', {})
        for key in ('analogue','ambiguity','semantic_hops','state_coupling','oracle_strength','novel_reasoning'):
            if key not in features: raise Invalid(f'{s["id"]}: missing task feature {key}')
    nodes = {s['id']:s for s in sections}
    visited, visiting = set(), set()
    def visit(sid):
        if sid in visiting: raise Invalid('dependency cycle')
        if sid in visited: return
        visiting.add(sid)
        for dep in nodes[sid]['depends_on']: visit(dep)
        visiting.remove(sid);visited.add(sid)
    for sid in ids: visit(sid)
    order = p.get('integration_order')
    if not isinstance(order,list) or set(order) != set(ids) or len(order) != len(ids):
        raise Invalid('integration_order must contain every section once')
    for s in sections:
        if any(order.index(d) >= order.index(s['id']) for d in s['depends_on']):
            raise Invalid('integration order violates dependencies')

def ready(p: dict, state: dict, plan_hash: str) -> dict:
    validate(p)
    if state.get('feature_id') != p['feature_id'] or state.get('run_id') != p['run_id']:
        raise Invalid('state/plan identity mismatch')
    if p['status'] != 'APPROVED' or state.get('status') != 'ACTIVE':
        return {'ready': [], 'reason': 'FEATURE_NOT_ACTIVE_AND_APPROVED'}
    if state.get('plan_sha256') != plan_hash or state.get('plan_review_status') != 'APPROVED':
        raise Invalid('approved review must cover this exact plan')
    if p['invocation_source'] != 'USER_EXPLICIT' and state.get('user_plan_approval') != 'APPROVED':
        raise Invalid('automatic activation needs user PLAN approval')
    if state.get('advisor_state') in {'REQUIRED','RUNNING','CONTEXT_BLOCKED'}:
        return {'ready': [], 'reason': 'ADVISOR_BARRIER'}
    ss = state.get('sections', {})
    nodes = {s['id']:s for s in p['sections']}
    active = state.get('active', [])
    seen_ws = set()
    for a in active:
        if a.get('section_id') not in nodes: raise Invalid('unknown active section')
        if not a.get('workspace'): raise Invalid('active canonical workspace required')
        ws = str(Path(a['workspace']).resolve())
        if ws in seen_ws: raise Invalid('shared active workspace')
        seen_ws.add(ws)
    count = sum(a.get('stage') in {'IMPLEMENT','REPAIR'} for a in active)
    slots = max(0, p['max_parallel_writers'] - count)
    result, blocked = [], {}
    for sid in p['integration_order']:
        s = nodes[sid]
        if ss.get(sid, {}).get('status', 'PENDING') != 'PENDING': continue
        if any(a['section_id'] == sid for a in active): continue
        if any(ss.get(d, {}).get('status') != 'ACCEPTED' or not ss.get(d, {}).get('integrated') for d in s['depends_on']):
            blocked[sid] = ['prerequisite not accepted+integrated'];continue
        peers = [nodes[a['section_id']] for a in active] + [nodes[k] for k in result]
        reasons = []
        for peer in peers:
            if not s['parallel_eligible'] or not peer['parallel_eligible']:
                reasons.append('serial-only section')
            reasons.extend(conflicts(s,peer))
        if reasons: blocked[sid] = sorted(set(reasons));continue
        if len(result) < slots: result.append(sid)
    return {'ready': result, 'blocked': blocked, 'slots': slots,
            'note': 'candidate set only; orchestrator reserves state before actual dispatch'}

def git_check(repo: Path, p: dict) -> None:
    r = subprocess.run(['git','-C',str(repo),'branch','--show-current'],capture_output=True,text=True,check=True)
    if p['execution_mode'] == 'EXECUTE_WITH_COMMITS' and r.stdout.strip() != p['feature_branch']:
        raise Invalid('scheduler must run on the authorized integration feature branch')
    for section in p['sections']:
        for rel in section['write_paths'] + section['read_paths']:
            q = repo / path_prefix(rel)
            if q.resolve() != q.absolute():raise Invalid('canonical scope paths required; symlink aliases cannot establish isolation')
    if p['max_parallel_writers'] > 1:
        ignore = repo/'.gitignore'
        if not ignore.exists() or '/git-worktree/' not in ignore.read_text().splitlines():
            raise Invalid('add /git-worktree/ to .gitignore before parallel dispatch')

@contextlib.contextmanager
def lock(path: Path):
    try: import fcntl
    except ImportError: raise Invalid('state writes require POSIX locking; validation remains portable')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(f,fcntl.LOCK_UN)

def atomic_json(path: Path, value: dict):
    fd, tmp = tempfile.mkstemp(prefix=path.name+'.',dir=path.parent)
    try:
        with os.fdopen(fd,'w') as f: json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):os.unlink(tmp)

def reserve_review(path: Path, pass_id: str, head: str) -> dict:
    if not ID.fullmatch(pass_id) or not SHA.fullmatch(head): raise Invalid('pass ID and exact head required')
    with lock(path.with_suffix('.lock')):
        state = json.loads(path.read_text())
        if state.get('status') != 'ACTIVE' or state.get('advisor_state') in {'REQUIRED','RUNNING','CONTEXT_BLOCKED'}: raise Invalid('closed/blocked feature cannot reserve a review')
        ledger = state.setdefault('full_reviews', {})
        if pass_id in ledger:
            if ledger[pass_id]['head'] != head: raise Invalid('pass ID reused for different candidate')
            return ledger[pass_id]
        index = int(state.get('full_review_cursor',0)) + 1
        record = {'index':index,'provider':'astra_high' if index%2 else 'glm-5.3','head':head}
        ledger[pass_id]=record;state['full_review_cursor']=index;atomic_json(path,state)
        return record

def follow_up(status: str, explicit_reopen: bool) -> str:
    if status == 'COMPLETED':
        return 'NEW_REVISION_PRESERVE_CLOSED_PLAN' if explicit_reopen else 'NEW_REQUEST_REASSESS_LOCAL_OR_NEW_FEATURE'
    return 'ASSESS_ACTIVE_REQUIREMENT_DELTA'

def main():
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest='cmd',required=True)
    for name in ('validate','ready'):
        q=sub.add_parser(name);q.add_argument('plan',type=Path)
        if name=='ready':q.add_argument('state',type=Path);q.add_argument('--repo',type=Path,required=True)
    q=sub.add_parser('reserve-review');q.add_argument('state',type=Path);q.add_argument('--pass-id',required=True);q.add_argument('--head',required=True)
    q=sub.add_parser('follow-up');q.add_argument('--status',required=True);q.add_argument('--explicit-reopen',action='store_true')
    a=ap.parse_args()
    try:
        if a.cmd in {'validate','ready'}:
            p=load_plan(a.plan)
            if a.cmd=='validate': result={'valid':True,'sections':len(p['sections']),'plan_sha256':digest(a.plan)}
            else:
                if a.repo:git_check(a.repo,p)
                result=ready(p,json.loads(a.state.read_text()),digest(a.plan))
        elif a.cmd=='reserve-review':result=reserve_review(a.state,a.pass_id,a.head)
        else:result={'disposition':follow_up(a.status,a.explicit_reopen)}
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (Invalid,OSError,ValueError,KeyError,TypeError,subprocess.CalledProcessError) as e:
        print(json.dumps({'valid':False,'error':str(e)},ensure_ascii=False));return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
