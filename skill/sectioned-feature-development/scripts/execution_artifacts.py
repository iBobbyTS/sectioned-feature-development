#!/usr/bin/env python3
"""v4.2 artifact lifecycle and local evidence linkage. No model calls or product edits.

Checks link real files/Git objects/recorded tool responses; they do not authenticate
an agent provider or prove the semantic truth of reviewer/test claims.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
import workflow as w
import section_plan
from ensure_agent_work_untracked import ensure_untracked

ASSETS=Path(__file__).resolve().parents[1]/'assets'
WRITERS={'impl_large','impl_std','impl_mini','impl_nano'}
ROLES=WRITERS|{'plan_reviewer','code_reviewer','code_explorer','glm_reviewer'}
REVIEW_STAGES={'PLAN_REVIEW','INITIAL_BOUNDED','SUBSECTION_DELTA','PARENT_RECONCILIATION','REPAIR_DELTA','FINAL_BOUNDED','INTEGRATION'}
WRITE_STAGES={'IMPLEMENT','REPAIR'}

def now():return datetime.now(timezone.utc).isoformat()
def obj(path):
 text=Path(path).read_text()
 try:return json.loads(text)
 except json.JSONDecodeError:
  # One marked machine envelope inside the canonical Markdown ledger; no second admission ledger.
  matches=re.findall(r'<!-- SFD_RECEIPT -->\s*```json\s*(.*?)```',text,re.S)
  if len(matches)!=1:raise w.Invalid('ONE_MARKED_RECEIPT_REQUIRED: '+str(path))
  return json.loads(matches[0])
def proof(path, repo):
 path=Path(path).resolve();repo=Path(repo).resolve()
 if not path.is_relative_to(repo) or not path.is_file() or path.stat().st_size==0:
  raise w.Invalid('ARTIFACT_MISSING_OR_OUTSIDE_REPO: '+str(path))
 return {'path':path.relative_to(repo).as_posix(),'sha256':w.digest(path)}
def verify(a,repo):
 if not w.artifact_metadata(a):raise w.Invalid('ARTIFACT_REFERENCE_REQUIRED')
 p=Path(repo)/a['path']
 if proof(p,repo)!=a:raise w.Invalid('ARTIFACT_HASH_MISMATCH: '+a['path'])
 return p

def git(repo,*args):
 return subprocess.run(['git','-C',str(repo),*args],check=True,capture_output=True,text=True).stdout.strip()
def product_fingerprint(repo):
 h=hashlib.sha256()
 h.update(git(repo,'rev-parse','HEAD').encode())
 h.update(subprocess.check_output(['git','-C',str(repo),'diff','--binary','HEAD','--']))
 raw=subprocess.check_output(['git','-C',str(repo),'ls-files','--others','--exclude-standard','-z'])
 for name in sorted(x for x in raw.decode().split('\0') if x):
  if name.startswith(('.agent-work/','git-worktree/')):continue
  p=Path(repo)/name
  if p.is_file():h.update(name.encode()+b'\0'+p.read_bytes())
 return h.hexdigest()

def render(repo,state):
 """One human projection; no second hand-edited machine state."""
 p=Path(repo)/'.agent-work/FEATURE-STATE.md'
 lines=['# Feature State — '+state['feature_id'],'','<!-- Generated from STATE.json; edit narratives in contracts/ledgers, not counters here. -->',
 '- Run: '+state['run_id'],'- Status: '+state.get('status','DRAFT'),'- PLAN review: '+state.get('plan_review_status','PENDING'),
 '- PLAN SHA: '+str(state.get('plan_sha256')),'- Advisor: '+state.get('advisor_state','NOT_REQUIRED'),
 '- Audit: '+str(state.get('audit_mode','LIVE')),'- Next action: '+state.get('next_action','SAVE_PLAN'),'',
 '## Sections','| ID | Status | Base / candidate | Integrated | Repair waves |','|---|---|---|---|---|']
 for sid,s in state.get('sections',{}).items():
  lines.append(f"| {sid} | {s.get('status','PENDING')} | {s.get('section_base','?')} / {s.get('candidate_head','?')} | {s.get('integrated',False)} | {s.get('repair_waves',0)} |")
 lines+=['','## Artifact references','```json',json.dumps(state,ensure_ascii=False,indent=2),'```','']
 p.write_text('\n'.join(lines))

def save(repo,state):
 w.atomic_json(Path(repo)/'.agent-work/STATE.json',state);render(repo,state)
def load(repo):return obj(Path(repo)/'.agent-work/STATE.json')
def audit_event(repo,state,event,family,fields=None):
 """Best-effort observation; workflow state remains authoritative if telemetry fails."""
 if state.get('audit_mode')=='OFF' or not state.get('audit_trace'):return
 cmd=[sys.executable,str(Path(__file__).with_name('audit_trace.py')),'append',state['audit_trace'],
      '--event',event,'--family',family,'--phase',family,'--summary',event,'--repo',str(repo)]
 for key,value in (fields or {}).items():cmd+=['--field',key+'='+str(value)]
 result=subprocess.run(cmd,capture_output=True,text=True)
 if result.returncode:state.setdefault('audit_gaps',[]).append({'event':event,'error':'TRACE_APPEND_FAILED'})

def init(repo,feature,run,main_actor,audit='LIVE',invocation_source='USER_EXPLICIT',trigger_evidence='explicit user request'):

 repo=repo.resolve();ensure_untracked(repo)
 if not w.ID.fullmatch(feature) or not w.ID.fullmatch(run) or not main_actor:raise w.Invalid('IDENTITY_REQUIRED')
 aw=repo/'.agent-work';state_path=aw/'STATE.json'
 if state_path.exists() or (aw/'PLAN-FULL.md').exists():raise w.Invalid('ACTIVE_ARTIFACTS_EXIST: preserve/archive old feature before initialization')
 for n in ['sections','reviews','replans','audit']: (aw/n).mkdir(parents=True,exist_ok=True)
 for src,dst in [('REQUIREMENTS.template.md','REQUIREMENTS.md'),('PLAN-FULL.template.md','PLAN-FULL.md')]:
  shutil.copy2(ASSETS/src,aw/dst)
 state={'schema_version':4,'workflow_revision':'4.3','feature_id':feature,'run_id':run,'status':'DRAFT',
  'main_actor_id':main_actor,'repo_root':str(repo),'audit_mode':audit,'plan_sha256':None,'plan_review_status':'PENDING',
  'user_plan_approval':'PENDING','advisor_state':'NOT_REQUIRED','actors':{},'active':[],
  'sections':{},'repair_lineages':{},'full_review_cursor':0,'full_reviews':{},'completion':None,'next_action':'REQUIREMENTS_AND_PLAN_AUTHOR'}
 if audit!='OFF':
  trace=aw/'audit'/feature/'TRACE.jsonl';state['audit_trace']=str(trace)
  cmd=[sys.executable,str(Path(__file__).with_name('audit_trace.py')),'init',str(trace),'--feature-id',feature,
       '--skill-version','4.3','--invocation-source',invocation_source,'--invocation-timing','FEATURE_START',
       '--trigger-evidence',trigger_evidence,'--feature-base',git(repo,'rev-parse','HEAD'),'--repo',str(repo),
       '--field','run_id='+run]
  result=subprocess.run(cmd,capture_output=True,text=True)
  if result.returncode:state['audit_gaps']=[{'event':'audit_init','error':'TRACE_INIT_FAILED'}]
 state['invocation_source']=invocation_source;state['trigger_evidence']=trigger_evidence
 save(repo,state);return {'initialized':str(aw),'status':'DRAFT','warning':'templates are NOT approved evidence'}

def verify_actor(state,actor,repo,allowed=None):
 if not actor or actor==state.get('main_actor_id'):raise w.Invalid('REAL_INDEPENDENT_ACTOR_REQUIRED')
 a=state.get('actors',{}).get(actor)
 if not a or (allowed and a.get('role') not in allowed):raise w.Invalid('ACTOR_ROLE_MISMATCH: '+str(actor))
 raw=obj(verify(a.get('launch_receipt'),repo))
 # Store the actual returned tool response, not a role alias. Nested task objects are common in MCP.
 def ids(o):
  if isinstance(o,dict):
   for k,v in o.items():
    if k in {'agent_id','thread_id','session_id'} and isinstance(v,str):yield v
    yield from ids(v)
  elif isinstance(o,list):
   for v in o:yield from ids(v)
 if actor not in set(ids(raw)):raise w.Invalid('ACTOR_NOT_IN_LAUNCH_RECEIPT')
 return a

def register(repo,actor,role,receipt,workspace,requested_model=None,observed_model=None,requested_effort=None,observed_effort=None):
 state=load(repo)
 if role not in ROLES or actor==state.get('main_actor_id'):raise w.Invalid('INVALID_DELEGATED_ROLE')
 if state.get('status')=='COMPLETED':raise w.Invalid('CLOSED_FEATURE')
 old=state.setdefault('actors',{}).get(actor)
 if old and old['role']!=role:raise w.Invalid('ACTOR_ROLE_REUSE')
 expected=w.IMPLEMENTATION_MODELS.get(role)
 if expected:
  if requested_model not in {None,expected[0]} or requested_effort not in {None,expected[1]}:raise w.Invalid('IMPLEMENTER_CONFIG_MISMATCH')
  requested_model,requested_effort=expected
 rec={'role':role,'workspace':str(workspace.resolve()),'launch_receipt':proof(receipt,repo),
      'requested_model':requested_model or 'UNKNOWN','observed_model':observed_model or 'UNKNOWN','requested_effort':requested_effort or 'UNKNOWN','observed_effort':observed_effort or 'UNKNOWN','registered_at':now()}
 if old and old['launch_receipt']!=rec['launch_receipt']:raise w.Invalid('ACTOR_RECEIPT_REPLACEMENT')
 state['actors'][actor]=old or rec;verify_actor(state,actor,repo,{role});audit_event(repo,state,'agent_role_assigned','orchestration',{'actor_id':actor,'profile':role,'workspace':workspace,'requested_model':requested_model,'observed_model':observed_model or 'UNKNOWN','requested_effort':requested_effort or 'UNKNOWN','observed_effort':observed_effort or 'UNKNOWN'});save(repo,state);return state['actors'][actor]

def check_plan(repo,plan_path,allow_draft=False):
 p=w.load_plan(plan_path)
 if p.get('workflow_revision')!='4.3':raise w.Invalid('NEW_EXECUTION_REQUIRES_REVISION_4_3; adopt active legacy work prospectively, do not relabel old evidence')
 legacy=section_plan.parse_plan(plan_path)
 if set(x.section_id for x in legacy.sections)!=set(s['id'] for s in p['sections']):raise w.Invalid('NARRATIVE_SCHEDULE_SECTION_MISMATCH')
 contract=repo/p.get('requirements_path','.agent-work/REQUIREMENTS.md')
 if not contract.is_file() or w.digest(contract)!=p['requirements_sha256']:raise w.Invalid('REQUIREMENTS_FILE_HASH_MISMATCH')
 if not allow_draft and p['status'] not in {'FROZEN','APPROVED'}:raise w.Invalid('PLAN_NOT_APPROVED')
 return p

def plan_evidence(p,state,h,repo):
 if not Path(repo,'.agent-work/PLAN-FULL.md').is_file():raise w.Invalid('PLAN_FILE_MISSING')
 if w.digest(Path(repo)/'.agent-work/PLAN-FULL.md')!=h:raise w.Invalid('PLAN_FILE_HASH_MISMATCH')
 verify(state.get('requirements'),repo)
 if state['requirements']['sha256']!=p['requirements_sha256']:raise w.Invalid('REQUIREMENTS_STATE_MISMATCH')
 author=state.get('plan_author',{});review=state.get('plan_review',{})
 if author.get('actor_id') != state.get('main_actor_id'):raise w.Invalid('PLAN_AUTHOR_MUST_BE_ORCHESTRATOR')
 verify(author.get('artifact'),repo)
 verify_actor(state,review.get('actor_id'),repo,{'plan_reviewer'});rp=verify(review.get('artifact'),repo)
 if author.get('actor_id')==review.get('actor_id'):raise w.Invalid('PLAN_AUTHOR_REVIEWER_COLLISION')
 if review.get('plan_sha256')!=h or review.get('result')!='APPROVED' or not review.get('admission'):
  raise w.Invalid('REAL_PLAN_REVIEW_AND_ADMISSION_REQUIRED')
 if review.get('unresolved_findings'):raise w.Invalid('PLAN_FINDINGS_OPEN')
 for a in state.get('active',[]):
  if a.get('status')=='RESERVED':continue
  verify_actor(state,a.get('actor_id'),repo)
 verify(review['admission'],repo)
 return rp

def record_plan(repo,author,author_output,reviewer,review_output,admission,user_approval):
 state=load(repo);path=repo/'.agent-work/PLAN-FULL.md';p=check_plan(repo,path)
 if state['feature_id']!=p['feature_id'] or state['run_id']!=p['run_id']:raise w.Invalid('FEATURE_ID_MISMATCH')
 if state.get('completion') or (repo/'.agent-work/CLOSURE.json').exists():raise w.Invalid('CLOSED_PLAN_REQUIRES_EXPLICIT_REOPEN')
 state['requirements']=proof(repo/p['requirements_path'],repo)
 state['plan_author']={'actor_id':author,'artifact':proof(author_output,repo)}
 state['plan_review']={'actor_id':reviewer,'artifact':proof(review_output,repo),'admission':proof(admission,repo),
  'result':'APPROVED','plan_sha256':w.digest(path),'unresolved_findings':[]}
 # Main must record actual review result, not turn arbitrary text into approval.
 report=obj(review_output)
 if report.get('result')!='APPROVED' or report.get('plan_sha256')!=w.digest(path) or report.get('actor_id')!=reviewer:
  raise w.Invalid('REVIEW_REPORT_DOES_NOT_APPROVE_THIS_PLAN')
 admission_data=obj(admission)
 if admission_data.get('decision')!='APPROVED' or admission_data.get('unresolved_findings')!=[]:
  raise w.Invalid('MAIN_ADMISSION_REQUIRED')
 state['plan_sha256']=w.digest(path);state['plan_review_status']='APPROVED';state['user_plan_approval']=user_approval
 for s in p['sections']:state['sections'].setdefault(s['id'],{'status':'PENDING','integrated':False,'repair_waves':0})
 state['status']='ACTIVE';state['next_action']='FREEZE_READY_SECTION';plan_evidence(p,state,w.digest(path),repo)
 w.git_check(repo,p);save(repo,state);return {'plan_review':'APPROVED','head':git(repo,'rev-parse','HEAD')}

def atomic_evidence(p,state,sid,head):
 s=w.get_section(p,sid);ss=state.get('sections',{}).get(sid,{})
 errors=[];arts=[];writers=set(ss.get('writer_actor_ids',[]));primary=ss.get('primary_review',{})
 if ss.get('candidate_head')!=head:errors.append('candidate/state head mismatch')
 if not ss.get('section_base') or not writers:errors.append('missing section base or writer identities')
 if ss.get('open_findings'):errors.append('open findings')
 if any(a.get('section_id')==sid for a in state.get('active',[])):errors.append('actor still active')
 for k in ['task_artifact','contract_artifact','handoff_artifact']:
  if not w.artifact_metadata(ss.get(k)):errors.append('missing '+k)
  else:arts.append(ss[k])
 primary_actors={primary.get('actor_id')}
 mechanical=s.get('review_intensity')=='MECHANICAL'
 if not mechanical:
  if primary.get('result')!='CLEAN' or primary.get('head')!=head or not primary.get('actor_id') or primary.get('base')!=ss.get('section_base') or not w.artifact_metadata(primary.get('artifact')):errors.append('primary coverage/closure missing')
  elif primary['actor_id'] in writers:errors.append('writer self-review')
  if primary.get('artifact'):arts.append(primary['artifact'])
 used=w.used_repairs(ss,state.get('repair_lineages',{}).get(s.get('lineage_id',sid),{}))
 needs_final=mechanical or s['assurance']=='TWO' or used>0 or bool(ss.get('had_material_findings'))
 if needs_final:
  f=ss.get('final_review',{})
  if f.get('result')!='CLEAN' or f.get('head')!=head or not f.get('actor_id') or f['actor_id'] in writers|primary_actors or not w.artifact_metadata(f.get('artifact')):errors.append('fresh final missing')
  if f.get('artifact'):arts.append(f['artifact'])
 for cid in s['check_ids']:
  e=ss.get('final_checks',{}).get(cid,{})
  if e.get('result')!='PASS' or e.get('head')!=head or not w.artifact_metadata(e.get('artifact')):errors.append('check missing at candidate: '+cid)
  if e.get('artifact'):arts.append(e['artifact'])
 return {'eligible_by_metadata':not errors,'errors':errors,'parent_section_id':sid,'candidate_head':head,'needs_final':needs_final,
  'repair_waves':used,'evidence_artifacts':arts,'checkpoint_ancestry':[ss.get('section_base')],
  'warning':'File/hash/identity checks are not provider attestation or semantic acceptance.'}

def actor_evidence(p,state,sid,repo):
 ss=state['sections'][sid];writers=set(ss.get('writer_actor_ids',[]));reviews=[]
 for child in ss.get('subsections',{}).values():writers.update(child.get('writer_actor_ids',[]))
 for r in [ss.get('primary_review'),ss.get('final_review'),*(c.get('review') for c in ss.get('subsections',{}).values())]:
  if r:reviews.append(r)
 for aid in writers:verify_actor(state,aid,repo,WRITERS)
 for r in reviews:verify_actor(state,r.get('actor_id'),repo,{'code_reviewer','glm_reviewer'})
 for a in [ss.get('task_artifact'),ss.get('contract_artifact'),ss.get('handoff_artifact')]:verify(a,repo)
 if not ss.get('handoff_head')==ss.get('candidate_head'):raise w.Invalid('HANDOFF_STALE_HEAD')

def ready_files(repo):
 state=load(repo);path=repo/'.agent-work/PLAN-FULL.md';p=check_plan(repo,path);h=w.digest(path)
 plan_evidence(p,state,h,repo);w.git_check(repo,p)
 for sid,s in state.get('sections',{}).items():
  if s.get('status')=='ACCEPTED':
   result=w.acceptance_check(p,state,sid,s['candidate_head'],h)
   if not result['eligible_by_metadata']:raise w.Invalid('ACCEPTED_LABEL_WITHOUT_EVIDENCE: '+sid+': '+str(result['errors']))
   w.verify_acceptance_files(repo,result);actor_evidence(p,state,sid,repo)
   if s.get('integrated'):
    commit=s.get('integration_head')
    if not commit or not s.get('integration_evidence'):raise w.Invalid('INTEGRATED_WITHOUT_RECEIPT')
    verify(s['integration_evidence'],repo)
    git(repo,'merge-base','--is-ancestor',commit,'HEAD')
 return w.ready(p,state,h)

def task(repo,sid):
 state=load(repo);path=repo/'.agent-work/PLAN-FULL.md';p=check_plan(repo,path)
 plan_evidence(p,state,w.digest(path),repo)
 result=w.next_unit(p,state,sid,w.digest(path))
 if not result.get('next'):raise w.Invalid('TASK_NOT_READY: '+str(result))
 s=w.get_section(p,sid);ss=state['sections'][sid]
 if ss.get('status')=='PENDING' and sid not in ready_files(repo)['ready']:raise w.Invalid('PARENT_NOT_READY')
 ss.setdefault('section_base',git(repo,'rev-parse','HEAD'))
 legacy=section_plan.parse_plan(path);body=next(x.body for x in legacy.sections if x.section_id==sid)
 out=repo/'.agent-work/sections'/f'{sid}-PLAN.md'
 out.write_text(legacy.feature_context+'\n'+body+'\n\n## Current executable unit\n```json\n'+json.dumps(next((c for c in s.get('subsections',[]) if c['id']==result['next']),s),indent=2)+'\n```\n')
 contract=repo/'.agent-work/sections'/f'{sid}-CONTRACT.md'
 if not contract.exists():
  contract.write_text(body+'\n\n## Frozen dispatch base\n'+ss['section_base']+'\n')
 ss['task_artifact']=proof(out,repo);ss['contract_artifact']=proof(contract,repo)
 if len(p['sections'])==1:shutil.copy2(out,repo/'.agent-work/PLAN.md')
 ss['task_plan_sha256']=w.digest(path);ss['task_unit_id']=result['next'];ss['task_profile']=result['profile']
 audit_event(repo,state,'implementation_assignment_frozen','planning',{'section_id':sid,'unit_id':result['next'],'profile':result['profile'],'plan_sha256':ss['task_plan_sha256']})
 save(repo,state);return {'task':str(out),'contract':str(contract),'next':result['next'],'profile':result['profile']}

def finish_section(repo,sid,head):
 state=load(repo);p=check_plan(repo,repo/'.agent-work/PLAN-FULL.md')
 plan_evidence(p,state,w.digest(repo/'.agent-work/PLAN-FULL.md'),repo)
 r=w.acceptance_check(p,state,sid,head,w.digest(repo/'.agent-work/PLAN-FULL.md'))
 if not r['eligible_by_metadata']:raise w.Invalid('; '.join(r['errors']))
 w.verify_acceptance_files(repo,r);actor_evidence(p,state,sid,repo)
 if p['execution_mode']=='EXECUTE_NO_COMMIT':
  ss=state['sections'][sid];fingerprint=product_fingerprint(repo)
  refs=[ss.get('handoff_fingerprint'),ss.get('primary_review',{}).get('product_fingerprint')]
  if r.get('needs_final'):refs.append(ss.get('final_review',{}).get('product_fingerprint'))
  refs += [e.get('product_fingerprint') for e in ss.get('final_checks',{}).values()]
  if not refs or any(x!=fingerprint for x in refs):raise w.Invalid('NO_COMMIT_FINGERPRINT_NOT_PROVEN')
 state['sections'][sid]['status']='ACCEPTED';save(repo,state);return r

def close(repo):
 state=load(repo);p=check_plan(repo,repo/'.agent-work/PLAN-FULL.md')
 ready_files(repo)
 if state.get('active') or state.get('advisor_state') in w.ADVISOR_BLOCKING_STATES:raise w.Invalid('ACTIVE_BARRIER')
 if any(s.get('status')!='ACCEPTED' or not s.get('integrated') for s in state['sections'].values()):raise w.Invalid('SECTIONS_NOT_INTEGRATED')
 head=git(repo,'rev-parse','HEAD');final=state.get('final_gate',{})
 if final.get('head')!=head or final.get('readiness') not in {'MERGEABLE','mergeable','MERGEABLE_WITH_DOCUMENTED_GAPS'} or not final.get('artifact'):raise w.Invalid('FINAL_HEAD_EVIDENCE_REQUIRED_OR_NOT_READY')
 verify(final['artifact'],repo)
 c={'feature_id':state['feature_id'],'run_id':state['run_id'],'head':head,'plan_sha256':w.digest(repo/'.agent-work/PLAN-FULL.md'),'closed_at':now()}
 state['completion']=c;state['status']='COMPLETED';state['next_action']='AUDIT_FINALIZE_OR_ARCHIVE'
 w.atomic_json(repo/'.agent-work/CLOSURE.json',c);audit_event(repo,state,'feature_completed','feature',{'head':head,'closure_sha256':w.digest(repo/'.agent-work/CLOSURE.json')});save(repo,state);return c

def stage_start(repo,sid,stage,actor,workspace):
    path=repo/'.agent-work/STATE.json'
    with w.lock(path.with_suffix('.lock')):
        state=load(repo);p=check_plan(repo,repo/'.agent-work/PLAN-FULL.md');h=w.digest(repo/'.agent-work/PLAN-FULL.md')
        plan_evidence(p,state,h,repo);w.git_check(repo,p)
        if state.get('status')!='ACTIVE' or state.get('advisor_state') in w.ADVISOR_BLOCKING_STATES:raise w.Invalid('FEATURE_OR_ADVISOR_BARRIER')
        role_set=WRITERS if stage in WRITE_STAGES else {'code_reviewer','glm_reviewer'}
        verify_actor(state,actor,repo,role_set)
        if stage not in WRITE_STAGES|REVIEW_STAGES:raise w.Invalid('UNKNOWN_STAGE')
        sec=w.get_section(p,sid);ss=state['sections'][sid];ws=workspace.resolve()
        if ss.get('status') in {'ACCEPTED','ABANDONED','COMPLETED'}:raise w.Invalid('CLOSED_PARENT')
        # A parent reservation made immediately before the native spawn is replaced by its actual ID.
        reservations=[a for a in state.get('active',[]) if a.get('section_id')==sid and a.get('status')=='RESERVED']
        for reserve in reservations:
            if Path(reserve.get('workspace','')).resolve()!=ws or reserve.get('actor_id') not in {None,actor}:raise w.Invalid('RESERVATION_IDENTITY_MISMATCH')
            state['active'].remove(reserve)
        if any(a.get('section_id')==sid or Path(a.get('workspace','')).resolve()==ws for a in state.get('active',[])):raise w.Invalid('PARENT_CANDIDATE_BUSY')
        for a in state.get('active',[]):
            other=w.get_section(p,a['section_id'])
            if not sec['parallel_eligible'] or not other['parallel_eligible'] or w.conflicts(sec,other):raise w.Invalid('WORKSPACE_CONTRACT_RESOURCE_CONFLICT')
        if stage in WRITE_STAGES:
            if sum(a.get('stage') in WRITE_STAGES for a in state.get('active',[]))>=p['max_parallel_writers']:raise w.Invalid('WRITER_CAPACITY')
            if p['execution_mode']=='PLAN_ONLY':raise w.Invalid('PLAN_ONLY')
            if p['execution_mode']=='EXECUTE_WITH_COMMITS':
                branch=git(ws,'branch','--show-current')
                expected=ss.get('worker_branch',p['feature_branch'])
                if branch in {'',p['main_branch']} or branch!=expected:raise w.Invalid('WRITER_NOT_ON_AUTHORIZED_BRANCH')
            if stage=='IMPLEMENT':
                next_=w.next_unit(p,state,sid,h)
                if not next_.get('next'):raise w.Invalid('CHECKPOINT_OR_DEPENDENCY_BARRIER: '+str(next_))
            for dep in sec['depends_on']:
                ds=state['sections'][dep]
                if ds.get('status')!='ACCEPTED' or not ds.get('integrated'):raise w.Invalid('DEPENDENCY_NOT_ACCEPTED_INTEGRATED')
                rr=w.acceptance_check(p,state,dep,ds['candidate_head'],h)
                if not rr['eligible_by_metadata']:raise w.Invalid('DEPENDENCY_EVIDENCE_MISSING')
                w.verify_acceptance_files(repo,rr);actor_evidence(p,state,dep,repo)
            ss.setdefault('writer_actor_ids',[])
            if actor not in ss['writer_actor_ids']:ss['writer_actor_ids'].append(actor)
        else:
            if actor in set(ss.get('writer_actor_ids',[])):raise w.Invalid('WRITER_CANNOT_REVIEW')
            if stage=='FINAL_BOUNDED':
                prior={ss.get('primary_review',{}).get('actor_id')}|{c.get('review',{}).get('actor_id') for c in ss.get('subsections',{}).values()}
                if actor in prior:raise w.Invalid('FINAL_REVIEWER_NOT_FRESH')
            verify(ss.get('handoff_artifact'),repo)
        for key in ('task_artifact','contract_artifact'):verify(ss.get(key),repo)
        unit_id=next_['next'] if stage=='IMPLEMENT' else ss.get('active_subsection_id') or sid
        if stage in WRITE_STAGES:
            unit=next((c for c in sec.get('subsections',[]) if c['id']==unit_id),sec)
            planned=unit['profile'];actual=state['actors'][actor]
            if actual['role']!=planned:raise w.Invalid('IMPLEMENTER_DIFFERS_FROM_FROZEN_PLAN: revise and review the plan before dispatch')
            expected=w.IMPLEMENTATION_MODELS[planned]
            for field,value in [('requested_model',expected[0]),('requested_effort',expected[1]),('observed_model',expected[0]),('observed_effort',expected[1])]:
                if actual.get(field) not in {None,'UNKNOWN',value}:raise w.Invalid('IMPLEMENTER_MODEL_OR_EFFORT_MISMATCH: '+field)
            if ss.get('task_plan_sha256')!=h or ss.get('task_unit_id')!=unit_id or ss.get('task_profile')!=planned:
                raise w.Invalid('TASK_ASSIGNMENT_NOT_FROZEN_FOR_THIS_UNIT')
        ss['active_subsection_id']=unit_id if unit_id!=sid else None
        entry={'section_id':sid,'subsection_id':ss['active_subsection_id'],'stage':stage,'actor_id':actor,'workspace':str(ws),'status':'RUNNING',
               'head':git(ws,'rev-parse','HEAD'),'fingerprint':product_fingerprint(ws),'started_at':now()}
        state['active'].append(entry);ss['status']='IMPLEMENTING' if stage in WRITE_STAGES else 'REVIEWING'
        audit_event(repo,state,'stage_started','orchestration',{'actor_id':actor,'section_id':sid,'stage':stage,'subsection_id':ss['active_subsection_id'],'profile':state['actors'][actor]['role'],'planned_profile':unit['profile'] if stage in WRITE_STAGES else None,'plan_sha256':h,'workspace':ws,'head':entry['head'],'repair_waves':ss.get('repair_waves',0)});save(repo,state);return entry

def stage_finish(repo,actor,result):
    path=repo/'.agent-work/STATE.json'
    with w.lock(path.with_suffix('.lock')):
        state=load(repo);matches=[a for a in state.get('active',[]) if a.get('actor_id')==actor]
        if len(matches)!=1:raise w.Invalid('ACTOR_NOT_UNIQUELY_ACTIVE')
        a=matches[0];artifact=proof(result,repo);state['active'].remove(a)
        a['result_artifact']=artifact;a['finished_at']=now();a['final_fingerprint']=product_fingerprint(Path(a['workspace']))
        moved=a['stage'] in REVIEW_STAGES and a['final_fingerprint']!=a['fingerprint']
        a['status']='INVALIDATED_HEAD_MOVED' if moved else 'RESULT_CAPTURED'
        state.setdefault('actor_history',[]).append(a)
        ss=state['sections'][a['section_id']]
        if moved:ss['status']='REVIEW_INVALIDATED';state['next_action']='CLOSE_ONLY_AFFECTED_REVIEW'
        else:ss['status']='AWAITING_ADMISSION'
        audit_event(repo,state,'stage_completed','orchestration',{'actor_id':actor,'section_id':a['section_id'],'stage':a['stage'],'subsection_id':a.get('subsection_id'),'result':a['status'],'artifact_sha256':artifact['sha256']});save(repo,state)
        if moved:raise w.Invalid('REVIEWED_CANDIDATE_CHANGED: observation saved; not clean')
        return a


def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,default=Path.cwd());sub=ap.add_subparsers(dest='cmd',required=True)
 q=sub.add_parser('init');q.add_argument('--feature-id',required=True);q.add_argument('--run-id',required=True);q.add_argument('--main-actor',required=True);q.add_argument('--audit',choices=['LIVE','OFF'],default='LIVE');q.add_argument('--invocation-source',choices=['USER_EXPLICIT','CUSTOM_INSTRUCTIONS_AUTO','AGENT_DISCRETION'],default='USER_EXPLICIT');q.add_argument('--trigger-evidence',default='explicit user request')
 q=sub.add_parser('register');q.add_argument('--actor',required=True);q.add_argument('--role',choices=sorted(ROLES),required=True);q.add_argument('--receipt',type=Path,required=True);q.add_argument('--workspace',type=Path,required=True);q.add_argument('--requested-model');q.add_argument('--observed-model');q.add_argument('--requested-effort');q.add_argument('--observed-effort')
 q=sub.add_parser('approve-plan');q.add_argument('--author',required=True);q.add_argument('--author-output',type=Path,required=True);q.add_argument('--reviewer',required=True);q.add_argument('--review-output',type=Path,required=True);q.add_argument('--admission',type=Path,required=True);q.add_argument('--user-approval',choices=['APPROVED','NOT_APPLICABLE'],required=True)
 sub.add_parser('ready');sub.add_parser('close');sub.add_parser('render-state')
 q=sub.add_parser('task');q.add_argument('--section',required=True)
 q=sub.add_parser('stage-start');q.add_argument('--section',required=True);q.add_argument('--stage',required=True);q.add_argument('--actor',required=True);q.add_argument('--workspace',type=Path,required=True)
 q=sub.add_parser('stage-finish');q.add_argument('--actor',required=True);q.add_argument('--result',type=Path,required=True)
 q=sub.add_parser('accept');q.add_argument('--section',required=True);q.add_argument('--head',required=True)
 a=ap.parse_args();repo=a.repo.resolve()
 try:
  if a.cmd=='init':r=init(repo,a.feature_id,a.run_id,a.main_actor,a.audit,a.invocation_source,a.trigger_evidence)
  elif a.cmd=='register':r=register(repo,a.actor,a.role,a.receipt,a.workspace,a.requested_model,a.observed_model,a.requested_effort,a.observed_effort)
  elif a.cmd=='approve-plan':r=record_plan(repo,a.author,a.author_output,a.reviewer,a.review_output,a.admission,a.user_approval)
  elif a.cmd=='stage-start':r=stage_start(repo,a.section,a.stage,a.actor,a.workspace)
  elif a.cmd=='stage-finish':r=stage_finish(repo,a.actor,a.result)
  elif a.cmd=='ready':r=ready_files(repo)
  elif a.cmd=='task':r=task(repo,a.section)
  elif a.cmd=='accept':r=finish_section(repo,a.section,a.head)
  elif a.cmd=='close':r=close(repo)
  else:render(repo,load(repo));r={'rendered':'FEATURE-STATE.md'}
  print(json.dumps(r,ensure_ascii=False,indent=2));return 0
 except (w.Invalid,OSError,ValueError,KeyError,TypeError,subprocess.CalledProcessError,RuntimeError) as e:
  print(json.dumps({'ok':False,'error':str(e)},ensure_ascii=False));return 2
if __name__=='__main__':raise SystemExit(main())
