# Activation and Orchestration

## Contents

1. [Trigger decision](#trigger-decision)
2. [Invocation-source behavior](#invocation-source-behavior)
3. [Automatic-trigger approval gate](#automatic-trigger-approval-gate)
4. [Late activation after underestimation](#late-activation-after-underestimation)
5. [Branch transition](#branch-transition)
6. [Local operational artifacts](#local-operational-artifacts)
7. [Role separation](#role-separation)
8. [Single-active-section barrier](#single-active-section-barrier)
9. [Sequence-violation recovery](#sequence-violation-recovery)
10. [Audit events](#audit-events)

## Trigger decision

Apply the **non-trivial prerequisite first**. A task does not enter this workflow merely because it reads, writes, or passes through a persistence, routing, security, concurrency, process-lifecycle, or other high-risk module.

Use the workflow when the requested or discovered implementation is non-trivial and at least one is true:

- behavioral edits are likely to exceed roughly 300 lines;
- more than three behavioral owners/modules/services/pages/workflows must change;
- the change materially changes semantics or ownership at a persistence/schema, security/auth/permission, money/time/unit, routing/failover, concurrency/retry/process-lifecycle, public API/protocol, deployment, or shared-state boundary;
- architecture/state ownership changes;
- the direct impact cone cannot be bounded economically;
- a prior whole-change implementation/review failed to converge.

Normally do **not** trigger for:

- one local calculation or formatting correction;
- a narrow bug fix with an exact reproduction and at most two owners;
- a one-off temporary repair/report script whose data target and side effects are already bounded;
- a read-only inventory or probe;
- work that merely happens inside a high-risk module without changing the high-risk contract;
- a mechanical rename, fixture, generated output, or documentation change.

A local task may still trigger when it is destructive/irreversible, introduces a new persisted representation, changes public compatibility, adds shared concurrency/retry semantics, or proves impossible to bound after inspection.

At activation record:

- `invocation_source`: `USER_EXPLICIT | CUSTOM_INSTRUCTIONS_AUTO | AGENT_DISCRETION`;
- `invocation_timing`: `FEATURE_START | MID_FEATURE`;
- exact trigger evidence;
- predicted owners, sections, behavioral LOC band, and risk boundary;
- negative evidence considered before triggering.

## Invocation-source behavior

### `USER_EXPLICIT`

The user named this skill or directly requested this workflow.

- Continue through plan review, implementation, bounded review, integration, audit finalization, and reporting without routine approval pauses.
- Stop only for a genuine owner decision, required non-main branch-base selection, already-tracked `.agent-work` handling, unavailable required subagent capability, or another explicit safety boundary.
- User invocation authorizes the workflow, not scope expansion, merge, push, history rewriting, or deletion.

### `CUSTOM_INSTRUCTIONS_AUTO` or `AGENT_DISCRETION`

Before lengthy planning:

1. Read this skill and the relevant references.
2. Immediately tell the user that the workflow is being activated.
3. State the invocation source, exact trigger, predicted size/owners/section count, and why normal local development is insufficient.
4. Perform one bounded owner exploration pass: repository rules, the direct implementation owner, direct callers/consumers, and existing focused tests. Do not inventory unrelated modules or design optional migration/recovery/proof machinery before approval.
5. Create and mechanically validate the first `PLAN-FULL.md`. When predicted work is at most two owners and roughly at most 150 behavioral lines, the provisional graph should normally contain at most two product sections; exceeding that requires a concrete unavoidable dependency explanation in the approval summary.
6. If the plan cannot be bounded after that pass, stop with the unresolved owner/seam questions instead of continuing open-ended planning.
7. Stop **before** dispatching the plan reviewer.
8. Do not print the plan body. Provide a short proportionality summary and one link in this form:

```markdown
[PLAN-FULL.md](/absolute/path/to/repo/.agent-work/PLAN-FULL.md)
```

9. Ask the user to approve, reject, or narrow the plan.

After approval, run the plan-review gate and continue to completion without another routine approval pause. If preflight shows the initial trigger was disproportionate, de-escalate to the normal local workflow, tell the user, and do not create a ceremonial sectioned plan.

## Automatic-trigger approval gate

The approval checkpoint evaluates **whether to use this workflow and whether the initial section graph is proportionate**. It is not a line-by-line design approval and does not replace the independent plan review.

The checkpoint must include only:

- trigger evidence and invocation source;
- predicted behavioral owners and LOC band;
- proposed section count/titles and why each section is unavoidable;
- the minimum end-to-end outcome;
- any proposed new foundational mechanism;
- unresolved assumptions that were deliberately not researched further before approval;
- the absolute PLAN-FULL link.

Do not dispatch the plan reviewer, implementer, or product-code editor until the user approves. Corrections requested by the user are incorporated before plan review and recorded as owner authority.

## Late activation after underestimation

Re-evaluate workflow fit at three checkpoints:

1. after initial source/owner exploration;
2. when the implementation estimate or actual diff first crosses a trigger;
3. before the first commit or code review if ownership/impact has expanded.

When a task initially treated as local grows into this workflow:

1. Stop product/test edits at the next safe point; do not continue “just one more patch.”
2. Announce late activation, invocation source, new trigger evidence, and current work state.
3. Preserve correct current work; record `adoption_head`, changed owners, tests, and unresolved work.
4. Resolve the branch transition below.
5. Build `PLAN-FULL.md` only for the active unaccepted and remaining work. Do not replay completed local work or create clean-lineage/evidence sections.
6. If activation is automatic, stop before plan review for the automatic-trigger approval gate.
7. After approval/plan review, delegate remaining implementation and repairs under the normal role and sequence rules.

Late activation is prospective. It does not invalidate tests or correct code merely because they predate the skill.

## Branch transition

In `EXECUTE_WITH_COMMITS`:

### Current branch is `main`

- If product work is uncommitted, create/switch to the feature branch from the current `main` state; Git carries the worktree changes. No extra branch approval is required.
- If feature commits already exist on local `main`, create a safety feature ref at current HEAD immediately. Do not reset/rewrite `main`. Ask the user whether to leave the commits on `main`, restore `main` after the safety branch, or use another repository-approved integration path.

### Current branch is not `main`

Do not infer that branch as the feature base. Ask the user to choose:

1. branch from `main`;
2. branch from the current branch;
3. merge the current branch into `main`, then branch from updated `main`.

Preserve uncommitted work. Branch selection does not authorize merge/push/cleanup.

## Local operational artifacts

`.agent-work/**` is local operational state, not repository history.

- Never stage or commit `.agent-work/**`.
- Before writing artifacts, run the bundled `ensure_agent_work_untracked.py` or perform the equivalent check.
- When no `.agent-work` path is tracked, add `.agent-work/` to `.git/info/exclude` if an equivalent local exclusion does not already exist.
- Do not commit a `.gitignore` change solely for this workflow unless the user requests a repository-wide policy.
- If any `.agent-work` path is already tracked, do not run `git rm --cached`, rewrite history, or silently preserve new tracked changes. Stop and ask whether to untrack it in a separate process-only commit.
- Stage product/test/user-document files explicitly; do not rely on broad staging that could capture local operational files.

Audit packs may copy these local artifacts, but Git commits may not.

## Role separation

The main agent is the **orchestrator and admission owner**. Under this workflow it may inspect source, write/update local `.agent-work` artifacts, dispatch agents, admit/reject findings, and make branch/commit decisions. It must not edit product code or tests.

Required separation:

- Each section implementation uses a delegated implementer subagent.
- Repairs use a delegated repair subagent; it must be distinct from every reviewer.
- The plan reviewer is read-only and may not implement, repair, or perform any code review for the same feature.
- The initial reviewer is distinct from the implementer and repairer. It may be reused for `REPAIR_DELTA` to retain coverage.
- The final reviewer is fresh and distinct from the plan reviewer, implementer, repairer, and initial/delta reviewer.
- A reviewer may not begin implementation, and an implementer may not self-admit findings.

Record stable task/session IDs in `FEATURE-STATE.md` and the audit trace. A generic profile label such as `root`, `sol_high`, or `reviewer` is not sufficient identity.

If required subagent execution is unavailable, do not silently fall back to main-thread product coding. Report `ORCHESTRATION_BLOCKED` and ask for explicit fallback authorization. A local main-agent inspection is provisional and cannot become PLAN approval, Clean A, or Clean B.

## Single-active-section barrier

Exactly one product-writing section may be active.

- Do not start section `S(n+1)` until `S(n)` is `ACCEPTED`, `BLOCKED`, or `ABANDONED` with durable local state.
- While an initial/delta/final reviewer is active, freeze the reviewed product/test head. No agent may edit that range until the reviewer completes or is explicitly cancelled.
- A finding must be admitted after reviewer completion before a repair agent starts.
- A repair must complete and its delta review close before final review starts.
- Do not parallelize dependent product sections. Read-only research on a genuinely independent future seam is allowed only when it cannot modify the plan/contract or product range being reviewed.

Before every dispatch, verify and record:

```text
active_section
active_writer_id
active_reviewer_id
reviewed_head
next_allowed_phase
```

The dispatcher must refuse an action inconsistent with `next_allowed_phase`.

## Sequence-violation recovery

If later implementation starts before the current section/review gate closes:

1. Stop/cancel the later writer immediately.
2. Preserve its partial work without committing it into the reviewed section.
3. Record `SEQUENCE_GATE_VIOLATION`, affected paths, writer ID, reviewer ID, and heads.
4. If the reviewed head changed, invalidate only that in-flight review attempt—not previously accepted evidence—and restart the bounded review at the correct current head.
5. Finish or formally block/abandon the earlier section.
6. Re-evaluate the partial later work against the now-accepted predecessor before resuming; do not assume it remains valid.

A sequence violation is a workflow defect, not authority to create a recovery section or full replan.

## Audit events

When audit is active, record at least:

- `skill_activation_announced`;
- `auto_plan_approval_requested` and `auto_plan_approved/rejected`;
- `late_trigger_detected`;
- `branch_transition_selected`;
- `agent_role_assigned` with stable task/session ID;
- `reviewer_started`, `reviewer_completed`, or `reviewer_cancelled`;
- `sequence_gate_violation`;
- `orchestration_blocked`;
- `.agent-work` tracking/exclusion status.

These events observe the workflow. Missing telemetry does not change product correctness, but it prevents claiming full role/sequence compliance.
