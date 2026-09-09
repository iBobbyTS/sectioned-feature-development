# Artifact lifecycle — restored v3.9 operational chain

## Contents
1. [Authority and files](#authority-and-files)
2. [Bootstrap](#bootstrap)
3. [Plan author to saved PLAN](#plan-author-to-saved-plan)
4. [Independent PLAN review to admission](#independent-plan-review-to-admission)
5. [Parent-only local plan correction](#parent-only-local-plan-correction)
6. [One executable task and real delegation](#one-executable-task-and-real-delegation)
7. [Handoff review and acceptance](#handoff-review-and-acceptance)
8. [Continuation completion and follow-up](#continuation-completion-and-follow-up)
9. [Checks and limits](#checks-and-limits)

## Authority and files

This is an execution contract, not Audit. It applies with audit OFF, one section, explicit invocation and no-commit mode. User-explicit invocation removes only the routine human PLAN approval pause. It never waives a persisted PLAN, independent PLAN review, real subagent implementation or bounded review evidence.

Keep the full v3.9 working set: PLAN-FULL.md, PLAN.md, REQUIREMENTS.md, FEATURE-STATE.md, per-parent CONTRACT/HANDOFF, PLAN-REVIEW and parent REVIEW ledgers, and triggered recovery documents. The scripts from v3.9 remain available. STATE.json is the machine scheduling/receipt view introduced for 4.x DAG execution. Render FEATURE-STATE.md from it; don't hand-maintain competing counters or acceptance flags. Contracts and reviewer reports remain the semantic evidence. The generated human state includes references to all such artifacts rather than silently losing fields.

Canonical active root is `.agent-work` on the integration feature checkout. Parallel workers receive absolute paths to its frozen task/contract files; they do not create their own authority or write the parent's STATE. Local worktrees may have scratch, but never a second independently edited PLAN-FULL. Archive the old feature working set before starting a new feature. Archive by copying/moving only identified workflow files; never delete unrelated user work.

## Bootstrap

Resolve initial branch provenance from the root Skill. From main a feature branch is authorized; from non-main ask the three-way base choice. More than one parent OR multiple executable subsections require commit mode and a dedicated feature branch. A planning-only request can draft this execution mode but cannot execute it without user implementation authority.

```bash
python {skill-dir}/scripts/ensure_agent_work_untracked.py --repo .
python {skill-dir}/scripts/execution_artifacts.py --repo . init \
  --feature-id <feature> --run-id <run> --main-actor <actual-parent-session-id>
```

Use `--audit OFF` only on explicit request. `init` creates DRAFT files, not an approved plan. It refuses to overwrite an existing active plan/state. Fill REQUIREMENTS with the complete confirmed contract. Keep exact original/grill/correction provenance in the local audit record when enabled, without passing raw grill history to every worker. A new agent may consume the standalone confirmed contract if outcomes, non-goals, examples, decisions, failure/migration semantics and remaining owner decisions are complete.

## Plan author to saved PLAN

1. Persist REQUIREMENTS before authoring. The main orchestrator authors the complete plan, preserving the uploaded 4.2.1 local policy; do not spawn a nonexistent plan_writer.
2. Save the complete draft at `.agent-work/evidence/plan-draft.md`, then write canonical PLAN-FULL. Record the actual main actor ID as author. Main authorship is not a delegated implementation exception.
3. Do not leave the plan only in chat or accept a short outline. Every section and child has a fixed implementation profile before independent review.
4. Retain the v3.9 FEATURE-CONTEXT/SECTION markers and complete narrative contracts. Add the SFD_PLAN_V4 block for machine scheduling. Parent section IDs/dependencies agree between both views; each child is listed only under its parent. The scheduler block is not another requirement source.
5. Freeze the reviewed proposal with scheduling `status=FROZEN`, `workflow_revision=4.3`, real base/branch, requirements path/hash and check commands. `FROZEN` is not approval. Review/admission update STATE, not the already-reviewed plan bytes.
6. Run both mechanical checks:

```bash
python {skill-dir}/scripts/section_plan.py validate .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/workflow.py validate .agent-work/PLAN-FULL.md
```

7. Auto-triggered work stops here for user approval with an absolute PLAN link; explicit implementation continues. No product code is written during the plan gate.

## Independent PLAN review to admission

Dispatch a different [@plan_reviewer](subagent://plan_reviewer), using PLAN-REVIEW-REQUEST. It must read the saved proposal and actual relevant source. It does not inherit the author's or prior reviewer's reasoning. High-complexity GLM challenge uses the finite existing orchestration policy; it is not a second general planning loop.

Save the complete returned report once. The compact machine envelope contains actual actor_id, `result=APPROVED|NEEDS_CORRECTION|OWNER_DECISION`, exact plan_sha256, candidates, coverage and gaps. The main agent records admission in PLAN-REVIEW.md with one marked JSON envelope (`decision`, `unresolved_findings`) inside that SAME Markdown ledger; arbitrary source text cannot become an approval just by setting a state string. If the plan changes materially, use the existing bounded PLAN delta rule; don't reset accepted code for formatting.

The PLAN-REVIEW ledger may embed the machine envelope below the narrative admission:

````markdown
<!-- SFD_RECEIPT -->
```json
{"decision":"APPROVED","unresolved_findings":[]}
```
````

Do not create a separate RAW/ADMISSION ledger pair. The original reviewer result is an input artifact; this compact envelope is a projection of the main admission already in the same ledger.

Register the real launch receipts and record the plan gate:

```bash
python {skill-dir}/scripts/execution_artifacts.py --repo . register \
  --actor <reviewer-id> --role plan_reviewer --receipt .agent-work/evidence/plan-reviewer-spawn.json --workspace <repo>
# Main plan author uses the main_actor_id established by init; no author launch receipt is fabricated.
python {skill-dir}/scripts/execution_artifacts.py --repo . approve-plan \
  --author <main-actor-id> --author-output .agent-work/evidence/plan-draft.md \
  --reviewer <reviewer-id> --review-output .agent-work/reviews/PLAN-RESULT.json \
  --admission .agent-work/reviews/PLAN-REVIEW.md --user-approval <APPROVED-or-NOT_APPLICABLE>
```

The source response must contain the recorded native/MCP agent/thread/session ID. The helper cannot authenticate a fabricated file or validate a model's reasoning: main still checks the actual tool return and semantic admission. No need to add cryptographic attestation or a proof server.

## Parent-only local plan correction

The independent reviewer supplies candidates; the parent owns admission. Do not force a fresh APPROVED report for every changed PLAN hash. Retain the exact reviewed plan snapshot and unmodified reviewer report before correcting the canonical plan.

The existing `approve-plan` command accepts either (a) the original exact-plan APPROVED path or (b) an explicit `PARENT_PLAN_CORRECTION` admission in the same PLAN-REVIEW ledger. Path (b) requires the raw report hash, the applied plan hash, a disposition/reason/evidence for every original candidate, and, when PLAN bytes changed, the original snapshot plus changed regions and a `NO_BOUNDARY_CHANGE` justification. The helper revalidates the current plan and rejects changed known scheduling/owner/model/requirement boundaries. It cannot certify prose semantics: the parent must check outcome, trust/state/public interfaces and required validation independently. Such a boundary change uses the existing bounded PLAN_DELTA, never this shortcut. A change to check commands/references additionally requires `plan_correction.validation_equivalence` explaining which pre-existing acceptance it expresses; it must not drop a required check or add an unapproved one.

Example admission envelope (replace all placeholders with actual evidence):

```json
{
  "decision": "APPROVED",
  "unresolved_findings": [],
  "closure_mode": "PARENT_PLAN_CORRECTION",
  "review_report_sha256": "<actual original report hash>",
  "applied_plan_sha256": "<actual final PLAN hash>",
  "candidate_dispositions": [
    {"id": "P1", "disposition": "CLOSED_PLAN_ONLY", "reason": "<bounded correction>", "evidence": "<requirement/source/plan delta>"}
  ],
  "plan_correction": {
    "classification": "NO_BOUNDARY_CHANGE",
    "reason": "<why the same approved outcome and boundaries remain>",
    "changed_regions": ["<actual changed plan region>"],
    "reviewed_plan": {"path": ".agent-work/evidence/plan-reviewed.md", "sha256": "<original PLAN hash>"}
  }
}
```

`REJECTED` and `DEFERRED_NIT` dispositions also require a reason and evidence. Do not mark a blocker closed merely by changing its label. Unchanged-plan rejection needs no invented plan delta. The original report can still say NEEDS_CORRECTION; STATE keeps its result/reviewed hash separately from the effective plan and parent approval. Missing original candidates/snapshot, an open owner decision, a changed known boundary, an active reviewer, or edited evidence blocks this path.

Use this existing gate only after real review termination. It does not add a new reviewer, create a second ledger, reset a plan/repair budget, or reopen accepted work. Old exact approved-plan receipts remain valid without migration.

## One executable task and real delegation

```bash
python {skill-dir}/scripts/execution_artifacts.py --repo . ready
python {skill-dir}/scripts/execution_artifacts.py --repo . task --section S01
```

`ready` verifies actual plan/requirement/report references, actors and prerequisites before returning a candidate set. It does not spawn agents. Reserve the parent workspace/resource slot in STATE before actual dispatch; record its tool result immediately after dispatch. One orchestrator serializes reservations and integrations.

`task` uses the v3.9 extractor behavior to write a parent-specific current PLAN, binds the section CONTRACT, and includes the complete selected subsection row when applicable. A serial single-parent workflow also gets `.agent-work/PLAN.md`. Parallel parents use `sections/{ID}-PLAN.md` so their writers never overwrite one global PLAN.

Choose [@impl_large](subagent://impl_large), [@impl_std](subagent://impl_std), [@impl_mini](subagent://impl_mini), or [@impl_nano](subagent://impl_nano) using module/model reasoning evidence. Actually invoke it; main never substitutes its own product/test edits. Persist the returned launch ID, selected profile, requested/observed model and effort, task hash, base, workspace, parent/child and original lineage. Unknown observed telemetry stays UNKNOWN.

Bind each real launch ID to the reserved task with `stage-start` before handing over mutable work. If the host combines creation and dispatch, reserve first and record/bind the returned ID immediately; no second writer is allowed while binding is pending. The helper does not call the host or enforce an OS sandbox.

```bash
python {skill-dir}/scripts/execution_artifacts.py --repo . stage-start \
  --section S01 --stage IMPLEMENT --actor <actual-worker-id> --workspace <absolute-worker-worktree>
# After the actual tool wait/result, save the full return once:
python {skill-dir}/scripts/execution_artifacts.py --repo . stage-finish \
  --actor <actual-worker-id> --result .agent-work/evidence/S01-implementation-result.json
```

Use the same binding for review modes with role-distinct reviewers. `stage-finish` invalidates a review if its candidate fingerprint changed. It does not infer review correctness from a tool-success flag.

The worker returns implementation/check results; the main agent writes the full parent HANDOFF and referenced raw result. Record `section_base`, `candidate_head`, `writer_actor_ids`, handoff head/hash and current TASK/CONTRACT hashes. Commit intended product/test/user docs only. No subagent writes the parent's workflow state or grants acceptance.

## Handoff review and acceptance

Before any reviewer, freeze the candidate HEAD and product fingerprint and save the HANDOFF. Register a distinct review actor; pass the persisted request packet to [@code_reviewer](subagent://code_reviewer) or actual ZCode. Never pass only “review my changes” without range/contract.

Save raw review output once and update the parent REVIEW ledger with candidate IDs, main admission, frozen repair criteria, attempted repair waves and delta closure. Return repairs to a delegated implementer; reuse the original reviewer where technically possible, never falsely claim continuity. Missing/invalid review output retries at most once, then evidence is insufficient.

For atomic parents, primary coverage/closure and any required fresh final must cover the final candidate. For decomposed parents, CHECKPOINT_VERIFIED is local, PARENT_RECONCILIATION establishes cumulative coverage, and the ordinary parent ONE/TWO final requirement remains. All checkpoints/repair attempts count in actual-call audit and the shared parent repair lineage.

```bash
python {skill-dir}/scripts/workflow.py acceptance-check .agent-work/PLAN-FULL.md .agent-work/STATE.json \
  --section S01 --head <candidate> --repo .
python {skill-dir}/scripts/execution_artifacts.py --repo . accept --section S01 --head <candidate>
```

Required final checks must have saved output and exact relevant input/environment identity. Hash verification is not test semantic validation. The main agent reads the actual findings/check results, not only JSON labels. An accepted parent needs a separate recorded feature-branch integration receipt before dependents are unblocked. Native no-commit mode additionally records exact dirty-diff fingerprints; a matching base HEAD alone does not prove uncommitted changes were reviewed.

## Continuation completion and follow-up

After compaction or a new turn, reread PLAN-FULL, FEATURE-STATE/STATE and the current parent task/contract/ledger before a write or dispatch. Don't infer accepted status from chat memory.

After final candidate/integration gates, persist `final_gate` with head, readiness and artifact, then:

```bash
python {skill-dir}/scripts/execution_artifacts.py --repo . close
```

Closure freezes plan digest, final head, feature/run and time. It does not authorize merge to main, push, deletion or cleanup. Audit finalization remains required when enabled, but telemetry can't weaken product gates. Archive the complete current working set locally after delivery. Later user changes are reclassified as local fixes or a new feature; default never appends the old PLAN. Explicit reopening stores the old closed plan/receipt and creates a new revision without clearing lineages.

## Checks and limits

Artifact checks are deliberately local file/Git/identity checks, not a new product proof framework. They address the observed lost PLAN/delegation chain and writer/reviewer snapshot drift. They cannot independently prove that a saved receipt originated from a provider or that a test is a good oracle. Missing old evidence is a legacy gap; do not re-run accepted historical sections merely to satisfy 4.2 fields.

## Retained v3.9 stage sequence (one parent)

Independent parents can overlap only under the 4.x scheduler; this diagram describes one parent. The v3.9 states and recovery dispositions below are retained.

### Parent stage sequence

```text
PREFLIGHT
  -> TRIGGER_DECISION
  -> FEATURE_SCOPE
  -> SECTION_GRAPH
  -> AUTO_PLAN_APPROVAL (automatic invocation only)
  -> PLAN_REVIEW_GATE
       -> approved --------------------------┐
       -> bounded correction -> optional PLAN_DELTA_RECHECK -> approved
       -> owner decision/unresolved blocker -> BLOCK
                                              v
                                     FREEZE_ONE_SECTION
  -> ASSIGN_DISTINCT_IMPLEMENTER
  -> IMPLEMENT_MINIMUM_CHANGE
  -> LOCAL_VALIDATE
  -> REVIEW_INTENSITY + REVIEW_ASSURANCE (`ONE | TWO`)
       -> MECHANICAL -> deterministic checks -> DISTINCT_FINAL_BOUNDED
       -> BOUNDED_OR_HIGH_RISK -> DISTINCT_INITIAL_BOUNDED_REVIEW   # once per stable baseline
            -> clean + ONE ----------------------> SECTION_ACCEPTED
            -> clean + TWO ----------------------> FINAL_BOUNDED_REVIEW
            -> admitted blockers -> REPAIR_DELTA* -> FINAL_BOUNDED_REVIEW
       -> final clean --------------------> SECTION_ACCEPTED -> RELEASE_SECTION_BARRIER
       -> new diff-caused blocker -> REPAIR_DELTA -> FINAL_BOUNDED_REVIEW
       -> owner decision -> BLOCK
       -> more than 5 repair waves -> HARD_CAP_DIAGNOSIS

HARD_CAP_DIAGNOSIS
  -> BACKUP_CURRENT_TIP
  -> fresh recovery planner CLASSIFICATION
       -> CONTINUE_CURRENT
       -> SIMPLIFY_CURRENT
       -> SPLIT_REMAINING
       -> REBOUND_OWNER
       -> REPAIR_EVIDENCE
       -> RESTART_FROM_BASE              # last resort only
  -> MINIMAL_PLAN_UPDATE
  -> RESUME_WITH_PRESERVED_EVIDENCE

ALL_SECTIONS_ACCEPTED
  -> CROSS_SECTION_INTEGRATION_REVIEW
  -> FULL_FEATURE_VALIDATE
  -> MERGE_READINESS
  -> AUDIT_FINALIZE (unless explicitly disabled)
  -> ARCHIVE
```

Advance only when the corresponding code-visible evidence exists. Agent declarations are not gates.


## 4.3 frozen model and external Advisor constraints

Main authors the persisted plan (uploaded 4.2.1 choice); record `--author <main-actor-id>` and its saved plan output, never invent a plan-author subagent launch. Independent PLAN reviewer launch/report/admission remain mandatory. Implementation/repair still require real delegated workers.

Each unit's plan profile must be concrete before review. The task extractor saves `task_plan_sha256`, `task_unit_id`, and `task_profile`; a write-stage launch must match all three and its registered model/effort. No standalone runtime tier selector exists.

External Advisor states REQUIRED, PACKAGE_BLOCKED, WAITING_EXTERNAL and WAITING_HUMAN_DECISION block readiness, writer/reviewer dispatch and closure even with audit OFF. Use advisor_flow.py for request/pack/result/human-adoption; never invoke a native advisor.
