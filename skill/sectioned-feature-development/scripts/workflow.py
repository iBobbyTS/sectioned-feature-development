#!/usr/bin/env python3
"""SFD v4/4.1 plan/DAG/checkpoint checks and narrow local state helpers. No Git mutations or agent calls."""
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
    validate_subsections(p)

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

# 4.1 additive plan/state helpers; schema-4 atomic plans remain valid.
def inside(path, envelopes):
    path = path_prefix(path)
    return any(path == path_prefix(root) or path.startswith(path_prefix(root) + '/') for root in envelopes)


def validate_subsections(p):
    parents = {s['id'] for s in p['sections']}
    all_ids = set(parents)
    for s in p['sections']:
        children = s.get('subsections', [])
        mode = s.get('delivery_mode', 'ATOMIC')
        if mode not in {'ATOMIC', 'SUBSECTIONS'}:
            raise Invalid('invalid delivery_mode')
        if mode == 'ATOMIC':
            if children: raise Invalid('atomic section cannot contain subsections')
            continue
        if p.get('workflow_revision') != '4.1': raise Invalid('subsections require workflow_revision=4.1')
        if not isinstance(children, list) or len(children) < 2: raise Invalid('use work steps for fewer than two real increments')
        if p['execution_mode'] != 'EXECUTE_WITH_COMMITS' or p['feature_branch'] == p['main_branch']:
            raise Invalid('MULTI_UNIT_REQUIRES_COMMITS_AND_FEATURE_BRANCH')
        if not isinstance(s.get('lineage_id'), str) or not ID.fullmatch(s['lineage_id']):
            raise Invalid('explicit original lineage_id required')
        invariants = s.get('shared_invariants')
        if not isinstance(invariants, list) or not invariants or any(not isinstance(x,str) or not ID.fullmatch(x) for x in invariants) or len(invariants) != len(set(invariants)):
            raise Invalid('unique parent invariant IDs required')
        oracles = s.get('joint_oracles')
        if not isinstance(oracles, list) or not oracles: raise Invalid('parent joint_oracles required')
        covered = set(); oracle_ids = set()
        for o in oracles:
            if not isinstance(o,dict) or not ID.fullmatch(str(o.get('id',''))) or o['id'] in oracle_ids:
                raise Invalid('unique joint oracle IDs required')
            oracle_ids.add(o['id'])
            ci, ii = o.get('check_ids'), o.get('invariants')
            if not isinstance(ci,list) or not ci or any(x not in s['check_ids'] for x in ci):raise Invalid('joint oracle checks must be in parent checks')
            if not isinstance(ii,list) or not ii or any(x not in invariants for x in ii):raise Invalid('joint oracle invariant mismatch')
            if not o.get('procedure') or not o.get('expected'):raise Invalid('joint oracle needs concrete procedure and outcome')
            covered.update(ii)
        if covered != set(invariants):raise Invalid('uncovered parent invariant')
        seen = set()
        for c in children:
            if not isinstance(c,dict) or c.get('unit_kind') != 'SUBSECTION':raise Invalid('explicit SUBSECTION type required')
            cid=c.get('id')
            if not isinstance(cid,str) or not ID.fullmatch(cid) or cid in all_ids:raise Invalid('unique child identity required')
            all_ids.add(cid)
            if c.get('parent_section_id') != s['id']:raise Invalid('child parent mismatch')
            if any(k in c for k in ('subsections','assurance','repair_limit','repair_budget','lineage_id','branch','final_review','max_loc','loc_hard_cap','line_budget')):
                raise Invalid('child cannot add nesting, independent budget/assurance/branch or LOC cap')
            deps=c.get('depends_on')
            if not isinstance(deps,list) or len(set(deps))!=len(deps) or any(x not in seen for x in deps):raise Invalid('child dependencies must be earlier same-parent children')
            if c.get('profile') not in PROFILES:raise Invalid('unknown child implementation profile')
            for key in ('write_paths','read_paths','check_ids','requirement_ids'):
                if not isinstance(c.get(key),list) or any(not isinstance(x,str) for x in c[key]):raise Invalid('invalid child '+key)
            if not c['write_paths'] or any(not inside(x,s['write_paths']) for x in c['write_paths']):raise Invalid('child writes outside parent scope')
            if any(not inside(x,s['write_paths']+s['read_paths']) for x in c['read_paths']):raise Invalid('child reads outside frozen parent context')
            if not c['check_ids'] or any(x not in s['check_ids'] for x in c['check_ids']):raise Invalid('child check IDs must be declared by parent')
            if not c['requirement_ids'] or any(x not in s['requirement_ids'] for x in c['requirement_ids']):raise Invalid('child requirements cannot add authority')
            for key in ('title','outcome','consumer','safe_intermediate_state','oracle','model_reason'):
                if not isinstance(c.get(key),str) or not c[key].strip():raise Invalid('child missing '+key)
            seen.add(cid)


def get_section(p, sid):
    for s in p['sections']:
        if s['id'] == sid:return s
    raise Invalid('unknown parent section')


def artifact_metadata(a):
    return isinstance(a,dict) and isinstance(a.get('path'),str) and bool(a['path']) and bool(re.fullmatch('[a-f0-9]{64}',str(a.get('sha256',''))))


def checkpoint_errors(c, rec, primary_id):
    errors=[]
    if rec.get('status')!='CHECKPOINT_VERIFIED':errors.append('not checkpoint verified')
    if rec.get('invalidated',False):errors.append('checkpoint invalidated')
    for key in ('base','head'):
        if not SHA.fullmatch(str(rec.get(key,''))):errors.append('exact checkpoint '+key+' missing')
    checks=rec.get('checks',{})
    for cid in c['check_ids']:
        e=checks.get(cid,{})
        if e.get('result')!='PASS' or e.get('head')!=rec.get('head') or not artifact_metadata(e.get('artifact')):
            errors.append('missing exact-head check '+cid)
    r=rec.get('review',{})
    if not primary_id or r.get('parent_review_id')!=primary_id:errors.append('parent primary review identity mismatch')
    if r.get('result')!='CLEAN' or r.get('head')!=rec.get('head') or r.get('base')!=rec.get('base') or not r.get('actor_id') or not artifact_metadata(r.get('artifact')):
        errors.append('checkpoint review evidence incomplete')
    if rec.get('open_findings'):errors.append('open checkpoint findings')
    return errors


def next_unit(p, state, sid, plan_hash):
    # Reuse the original plan approval, invocation and resource gates.
    r=ready(p,state,plan_hash)
    if r.get('reason'):return {'next':None,'reason':r['reason']}
    s=get_section(p,sid);ss=state.get('sections',{}).get(sid,{})
    if ss.get('status') in {'ACCEPTED','ABANDONED','COMPLETED','BLOCKED'}:
        return {'next':None,'reason':'PARENT_NOT_DISPATCHABLE'}
    if ss.get('open_findings'):return {'next':None,'reason':'PARENT_FINDING_BARRIER'}
    if any(a['section_id']==sid for a in state.get('active',[])):
        return {'next':None,'reason':'PARENT_ACTOR_BARRIER'}
    if any(state.get('sections',{}).get(d,{}).get('status')!='ACCEPTED' or not state['sections'][d].get('integrated') for d in s['depends_on']):
        return {'next':None,'reason':'PARENT_DEPENDENCY_BARRIER'}
    active=state.get('active',[])
    if sum(a.get('stage') in {'IMPLEMENT','REPAIR'} for a in active)>=p['max_parallel_writers']:
        return {'next':None,'reason':'WRITER_CAPACITY'}
    for a in active:
        other=get_section(p,a['section_id'])
        if not s['parallel_eligible'] or not other['parallel_eligible'] or conflicts(s,other):
            return {'next':None,'reason':'PARENT_RESOURCE_CONFLICT'}
    if s.get('delivery_mode','ATOMIC')=='ATOMIC':
        return {'next':sid,'unit_kind':'SECTION','profile':s['profile']}
    ledger=ss.get('subsections',{})
    for c in s['subsections']:
        rec=ledger.get(c['id'],{})
        if rec.get('status','PENDING')=='PENDING':
            return {'next':c['id'],'parent_section_id':sid,'unit_kind':'SUBSECTION','profile':c['profile'],'lineage_id':s['lineage_id']}
        errors=checkpoint_errors(c,rec,ss.get('primary_review_id'))
        if errors:return {'next':None,'reason':'CHECKPOINT_BARRIER','subsection_id':c['id'],'errors':errors}
    return {'next':None,'reason':'PARENT_RECONCILIATION_REQUIRED'}


def used_repairs(ss, lineage):
    # Imported local counts may be smaller than the documented original lineage count.
    values=[ss.get('repair_waves',0),ss.get('original_lineage_waves',0),
            ss.get('repair_lineage',{}).get('waves_used',0),lineage.get('waves_used',0)]
    if any(type(v) is not int or v<0 for v in values):raise Invalid('repair counts must be known non-negative integers before mutation')
    return max(values)


def acceptance_check(p, state, sid, head, plan_hash):
    errors=[]
    gate=ready(p,state,plan_hash)
    if gate.get('reason'):errors.append(gate['reason'])
    s=get_section(p,sid);ss=state.get('sections',{}).get(sid,{})
    if s.get('delivery_mode')!='SUBSECTIONS':raise Invalid('atomic acceptance remains the existing parent workflow')
    if not SHA.fullmatch(head):raise Invalid('exact final candidate required')
    if ss.get('candidate_head')!=head:errors.append('candidate/state head mismatch')
    if any(x['section_id']==sid for x in state.get('active',[])):errors.append('parent actor still active')
    if ss.get('open_findings'):errors.append('parent has open findings')
    expected={c['id'] for c in s['subsections']};primary_actors=set();writers=set(ss.get('writer_actor_ids',[]));artifacts=[];ancestry=[]
    previous_head=ss.get('section_base')
    if not SHA.fullmatch(str(previous_head or '')):errors.append('missing original parent section_base')
    for c in s['subsections']:
        rec=ss.get('subsections',{}).get(c['id'],{})
        if rec.get('base')!=previous_head:errors.append('checkpoint coverage gap before '+c['id'])
        previous_head=rec.get('head')
        errors.extend(c['id']+': '+e for e in checkpoint_errors(c,rec,ss.get('primary_review_id')))
        r=rec.get('review',{});primary_actors.add(r.get('actor_id'))
        for key in ('base','head'):
            if rec.get(key):ancestry.append(rec[key])
        if r.get('artifact'):artifacts.append(r['artifact'])
        artifacts.extend(e.get('artifact') for e in rec.get('checks',{}).values() if e.get('artifact'))
        writers.update(rec.get('writer_actor_ids',[]))
    primary=ss.get('primary_review',{})
    if primary.get('base')!=ss.get('section_base'):errors.append('primary must reconcile original parent base to final candidate')
    if primary.get('id')!=ss.get('primary_review_id') or primary.get('result')!='CLEAN' or primary.get('head')!=head or not primary.get('actor_id') or not artifact_metadata(primary.get('artifact')):
        errors.append('whole-parent primary reconciliation missing')
    primary_actors.add(primary.get('actor_id'))
    if set(primary.get('covered_subsections',[]))!=expected or primary.get('open_invalidations')!=[]:
        errors.append('cumulative coverage or invalidation reconciliation incomplete')
    if primary.get('artifact'):artifacts.append(primary['artifact'])
    for j in s['joint_oracles']:
        e=ss.get('joint_evidence',{}).get(j['id'],{})
        if e.get('result')!='PASS' or e.get('head')!=head or not artifact_metadata(e.get('artifact')):
            errors.append('missing joint oracle at parent candidate: '+j['id'])
        if e.get('artifact'):artifacts.append(e['artifact'])
    for cid in s['check_ids']:
        e=ss.get('final_checks',{}).get(cid,{})
        if e.get('result')!='PASS' or e.get('head')!=head or not artifact_metadata(e.get('artifact')):
            errors.append('missing parent required check: '+cid)
        if e.get('artifact'):artifacts.append(e['artifact'])
    if not writers or None in primary_actors:errors.append('missing actual writer/reviewer identities')
    if writers & primary_actors:errors.append('writer cannot supply independent primary review')
    budget=state.get('repair_lineages',{}).get(s['lineage_id'],{})
    used=used_repairs(ss,budget)
    needs_final=s['assurance']=='TWO' or used>0 or bool(ss.get('had_material_findings'))
    if needs_final:
        f=ss.get('final_review',{})
        if f.get('result')!='CLEAN' or f.get('head')!=head or not f.get('actor_id') or f['actor_id'] in primary_actors|writers or not artifact_metadata(f.get('artifact')):
            errors.append('fresh independent parent final evidence missing')
        if f.get('artifact'):artifacts.append(f['artifact'])
    return {'eligible_by_metadata':not errors,'errors':errors,'parent_section_id':sid,'candidate_head':head,'needs_final':needs_final,
            'repair_waves':used,'evidence_artifacts':artifacts,'checkpoint_ancestry':sorted(set(ancestry)),
            'warning':'No state mutation. Actual Git/artifact checks and semantic sufficiency remain required.'}


def verify_acceptance_files(repo, result):
    repo=repo.resolve();head=result['candidate_head']
    subprocess.run(['git','-C',str(repo),'cat-file','-e',head+'^{commit}'],check=True,capture_output=True)
    for old in result['checkpoint_ancestry']:
        subprocess.run(['git','-C',str(repo),'merge-base','--is-ancestor',old,head],check=True,capture_output=True)
    for a in result['evidence_artifacts']:
        path=repo/a['path']
        if not path.resolve().is_relative_to(repo) or not path.is_file() or digest(path)!=a['sha256']:
            raise Invalid('missing/hash-mismatched evidence: '+str(a.get('path')))
    result['git_ancestry_and_artifact_hashes_verified']=True
    return result


def reserve_repair(p, path, sid, child_id, attempt_id, findings, plan_hash):
    if not ID.fullmatch(attempt_id) or not findings:raise Invalid('repair attempt ID and finding IDs required')
    with lock(path.with_suffix('.lock')):
        state=json.loads(path.read_text());gate=ready(p,state,plan_hash)
        if gate.get('reason'):raise Invalid('repair barrier: '+gate['reason'])
        s=get_section(p,sid);ss=state.get('sections',{}).get(sid,{})
        if ss.get('status') in {'ACCEPTED','COMPLETED','ABANDONED'}:raise Invalid('closed parent is not a repair budget reset point')
        if child_id and child_id not in {c['id'] for c in s.get('subsections',[])}:raise Invalid('unknown child for repair')
        lineage=s.get('lineage_id',sid)
        b=state.setdefault('repair_lineages',{}).setdefault(lineage,{'waves_used':used_repairs(ss,{}),'attempts':{},'recovery_used':bool(ss.get('recovery_used',False))})
        attempts=b.setdefault('attempts',{})
        payload={'section_id':sid,'subsection_id':child_id,'finding_ids':sorted(set(findings))}
        if attempt_id in attempts:
            prev=attempts[attempt_id]
            if any(prev.get(k)!=v for k,v in payload.items()):raise Invalid('repair attempt ID semantic conflict')
            return prev
        if any(x['section_id']==sid for x in state.get('active',[])):raise Invalid('finish/reap current parent actor before repair reservation')
        used=used_repairs(ss,b)
        approval=b.get('extra_attempt_authority',{}).get(attempt_id,{})
        if used>=5 and (not approval.get('request_id') or not re.fullmatch('[a-f0-9]{64}',str(approval.get('decision_sha256','')))):
            raise Invalid('PARENT_REPAIR_LIMIT: no new child/model/run budget')
        payload.update(wave=used+1,lineage_id=lineage,authority=approval or None)
        attempts[attempt_id]=payload;b['waves_used']=used+1
        ss['repair_waves']=used+1;ss['had_material_findings']=True
        state.setdefault('sections',{})[sid]=ss
        atomic_json(path,state);return payload


def main():
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest='cmd',required=True)
    for name in ('validate','ready'):
        q=sub.add_parser(name);q.add_argument('plan',type=Path)
        if name=='ready':q.add_argument('state',type=Path);q.add_argument('--repo',type=Path,required=True)
    for name in ('next-unit','acceptance-check','reserve-repair'):
        q=sub.add_parser(name);q.add_argument('plan',type=Path);q.add_argument('state',type=Path);q.add_argument('--section',required=True)
        if name!='reserve-repair':q.add_argument('--repo',type=Path,required=True)
        if name=='acceptance-check':q.add_argument('--head',required=True)
        if name=='reserve-repair':
            q.add_argument('--subsection');q.add_argument('--attempt-id',required=True);q.add_argument('--finding',action='append',required=True)
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
        elif a.cmd in {'next-unit','acceptance-check','reserve-repair'}:
            p=load_plan(a.plan);state=json.loads(a.state.read_text());h=digest(a.plan)
            if a.cmd=='next-unit':
                git_check(a.repo,p);result=next_unit(p,state,a.section,h)
            elif a.cmd=='acceptance-check':
                result=acceptance_check(p,state,a.section,a.head,h)
                if result['eligible_by_metadata']:result=verify_acceptance_files(a.repo,result)
                else:
                    print(json.dumps(result,ensure_ascii=False,indent=2));return 2
            else:result=reserve_repair(p,a.state,a.section,a.subsection,a.attempt_id,a.finding,h)
        elif a.cmd=='reserve-review':result=reserve_review(a.state,a.pass_id,a.head)
        else:result={'disposition':follow_up(a.status,a.explicit_reopen)}
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (Invalid,OSError,ValueError,KeyError,TypeError,subprocess.CalledProcessError) as e:
        print(json.dumps({'valid':False,'error':str(e)},ensure_ascii=False));return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
