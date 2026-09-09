# Artifact lifecycle — agent-managed, not a receipt engine

## One authority per concern

This is mandatory execution behavior even audit OFF. Main owns scheduling and writes the canonical readable plan/state. Real tests and reviewer work, not JSON flags, justify acceptance. There is no requirement to create STATE.json, a machine schedule, synthetic launch receipt or plan approval digest.

```text
.agent-work/REQUIREMENTS.md
.agent-work/PLAN-FULL.md
.agent-work/FEATURE-STATE.md
.agent-work/sections/S01-TASK.md
.agent-work/sections/S01-HANDOFF.md
.agent-work/reviews/PLAN-REVIEW.md
.agent-work/reviews/S01-REVIEW.md
```

`PLAN.md`/`S01-CONTRACT.md` are optional extraction views if they help the actual worker. Do not hand-maintain a second independent business contract. Actual raw agent/check outputs may be stored under evidence/ and referenced once; their file extension and envelope are not execution gates. Per-parent TASK/HANDOFF/REVIEW, not a new directory tree for every child, carries subsection evidence.

## Bootstrap and plan

1. Confirm actual repository/feature/branch and preserve unrelated work. Exclude `.agent-work` once.
2. Save confirmed user requirements, superseded instructions and real examples; preserve original dialogue for audit when available, but give workers the self-contained confirmed contract rather than irrelevant chat.
3. Main writes complete PLAN-FULL before asking a reviewer to read it. Include models, dependencies, intermediate safety and acceptance. Write a short FEATURE-STATE with status PLANNED, actual base and next action.
4. Validate only IDs/dependencies/parenting/impl choices. A same-file plan that passes this basic check still needs semantic review.
5. For automatic activation wait for first-plan human approval; explicit implementation bypasses only that pause.

## Plan review and admission

Dispatch [@plan_reviewer](subagent://plan_reviewer) through the native Codex subagent mechanism. Keep all product implementers undispatched while any selected PLAN reviewer or required PLAN_DELTA is live. Wait for the actual returned result, read/save its original output and native ID in PLAN-REVIEW.md (or reference a saved output), then main adds candidate dispositions. If a high-complexity ZAS challenge is selected, invoke it directly through MCP and complete its result/admission too. A progress update, an early no-issues message, or a tool wait timeout is not a final result. The original result is not rewritten.

Ordinary corrections need no latest-hash APPROVED. Main can proceed when all admitted material issues are resolved and no owner decision is open. Material contract/owner/dependency changes get the one bounded PLAN_DELTA allowed by the planning policy. A formatting edit, new field label, timestamp or hash does not reopen review.

Already reviewed plans can resume from their actual current-feature evidence. Different feature names, outcomes or source bases are genuine mismatches; do not repair those by copying an old receipt into the new feature.

## Every executable unit

1. Main applies the dispatch handoff in activation-and-orchestration.md: PLAN review/admission closed; serial parent accepted or child checkpoint verified; required dependencies integrated; no conflicting live actor. Explicit reviewed-PLAN independence is the only parallel exception.
2. Write the unit TASK with real base/workspace, explicit planned role, parent invariant, edit/inspect boundaries, AC, checks and return instructions. Extracting is optional convenience, not a mandatory second check.
3. Actually spawn that implementer/repairer. Write the returned ID, role, workspace and task reference in FEATURE-STATE. No fake receipt JSON or stage-start command.
4. Wait for actual result; if it blocks, classify product/requirement/environment/actor failure. Never pretend main coding was delegated.
5. Save HANDOFF with changed paths, exact candidate, behavior, checks/exits/log refs and gaps. Commit only intended code/tests/docs when authorized.
6. Freeze candidate, select the existing logical slot provider, and dispatch either the native role OR the ZAS MCP job directly, never both by default. Record route + returned ID, wait/read/save the actual result, then main updates a single cumulative parent REVIEW ledger. No successor is released merely because the review was dispatched or its process finished.
7. On admitted defects, use a real delegated repairer, targeted tests and delta verification. On acceptance, record the actual justification and head. No script is asked to grant acceptance.
8. In parallel, integrate accepted worker commits serially into the feature branch; record integrated head before consumers start.

A worker can return Markdown. Do not make it emit a custom machine receipt solely to unlock the next phase. Content must be truthful and adequate: missing test/review evidence is not fixed by changing a label.

## Recovery and completion

After compaction or takeover, read current PLAN, FEATURE-STATE and active TASK/review. For every actor marked live or unresolved, consult its actual native-or-ZAS lifecycle before dispatch; unknown liveness is not implicit completion, and writing a new label cannot stop an actor. Read raw evidence only for the unresolved point; do not enumerate every historical workflow file. Preserve missing historical metadata as UNKNOWN. At hard cap, record the compact diagnosis and backup ref only when actually needed.

When implementation, required review and final checks are complete, append closure date/head/readiness to FEATURE-STATE and mark the PLAN closed without changing its approved business text. Preserve its old version when an explicit reopen is authorized. Default later requests get fresh classification.

Audit packaging uses these real artifacts. Audit OFF changes no above behavior. Audit helper failure does not invalidate already-established product evidence.

## Bounded recovery from format trouble

Do not spend an implementation session fixing installed Skill scripts or making old machine JSON agree with Markdown. Check whether the actual business plan, dependency order, roles and review evidence are clear. If yes, note the format discrepancy once and continue. If no, correct the smallest real ambiguity or obtain the necessary review; do not reconstruct an entire registry from other features.
