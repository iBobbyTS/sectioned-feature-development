# Activation and orchestration responsibilities

## Trigger

Use the non-trivial prerequisite before risk labels. A small exact fix is not non-trivial merely because it touches a routing/persistence file. Record USER_EXPLICIT, CUSTOM_INSTRUCTIONS_AUTO or AGENT_DISCRETION and direct evidence. On automatic invocation, announce promptly, create the first proportional plan, and stop before review with an absolute file link. Explicit implementation continues unless a real safety/authority/capability blocker arises.

## Branch

Main may branch from main within the scoped skill delegation. On an unrelated non-main branch, ask whether to branch from main, from current, or merge current into main first; the choice does not authorize merge/push/cleanup. Continuing the already authorized feature branch needs no repeat choice. More than one business section or more than one executable subsection requires `EXECUTE_WITH_COMMITS` and a dedicated non-main feature branch before further product/test edits. Write the mode and authorized branch into PLAN-FULL and FEATURE-STATE; a no-commit conflict must be resolved before implementation. Preserve existing dirty work and never silently reset history.

Check local `.agent-work` exclusion once with Git or the helper. Already tracked files need separate cleanup authority. Do not put workflow state in product commits.

## Actual roles

Main writes requirements/PLAN/state, admits findings and integrates commits; it does not implement/repair product code or tests. Use the planned linked impl role. Main may perform expressly authorized worktree ignore setup and mechanical integration. Plan reviewer, implementer/repairer and fresh final reviewer are role-distinct real instances. The parent code reviewer may resume for delta only where the provider supports it.

No role/profile label substitutes for a real tool-returned task/session ID. Record actual IDs in plain state; do not invent harness authenticity by hashing a self-authored receipt. Unknown observed model remains unknown.

No machine ready/register gate exists. One orchestrator serializes decisions from actual results. Finish/cancel actual actors, not only labels. Required agent unavailability after one bounded retry is ORCHESTRATION_BLOCKED, not silent main-thread fallback.

## Dispatch handoff

Use this order before any actual implementation/repair dispatch. Record the conclusion in existing readable state/task text at real transitions, not at every poll.

1. **PLAN is closed for execution:** every selected PLAN pass has returned and main has read/saved its report, disposed of candidates, completed ordinary corrections, and finished any required PLAN_DELTA. "User approved", "review submitted", "reviewer still running", or an early CLEAN comment cannot authorize S01. Optional high-complexity GLM review, once selected, must finish too. Do not spawn an idle implementer early; that is already an implementation dispatch.
2. **The actual prerequisite is closed:** in serial execution the current parent is accepted under its ONE/TWO and checks; dependents additionally require its integration. Within one parent, the previous child must be CHECKPOINT_VERIFIED with no open admitted checkpoint defect. Merely completed code, an INITIAL clean, BLOCKED/ABANDONED state, or a cancelled reviewer does not release that dependency.
3. **The right actor is used:** select the planned native impl role for writing. Native reviews use the native [@plan_reviewer](subagent://plan_reviewer) or [@code_reviewer](subagent://code_reviewer); external reviews go directly through ZAS MCP. Log route + returned ID, not a guessed identity.
4. **No conflicting actor is live:** current-candidate review prohibits a writer. An independent parent can overlap only under [Parallel limits and violations](#parallel-limits-and-violations). If a prerequisite reviewer is live, wait on that reviewer; if it failed without usable evidence, apply the bounded retry/block policy, not fake acceptance.

Example handoff: "PLAN result read and admitted; S01 accepted at <head>, integrated at <head>; no conflicting actor; dispatch S02 to its planned native impl." During review: "S01 FINAL reviewer <route/id> still running; next action is wait, not S02 implementation."

A review report is an observation; only main admission plus required coverage/checks closes a boundary. Main may reject unsupported candidates and perform ordinary plan-only corrections without obtaining a new matching-hash APPROVED. These sequencing rules do not reintroduce that retired gate.

A current-unit repair is a permitted writer handoff only after the originating reviewer has returned and main has frozen admitted findings. It does not require the current parent to be accepted, and it does not authorize work on the next parent.

## Late activation

If initially local work becomes non-trivial, stop new writes, preserve current patch/tests and identify the real expanded boundary. On main, create feature branch retaining work; if commits already reached main, do not reset it. On non-main use existing explicit feature authority or ask base choice. Plan only coherent unaccepted/remaining work, not evidence-only replacements of accepted code.

Automatic late activation still pauses after saved PLAN before review. Explicit invocation does not waive a plan or delegated implementation. Do not require retroactive JSON metadata or new hashes for already accepted evidence.

## Parallel limits and violations

Default to serial. Independent parent overlap requires the reviewed PLAN to explicitly name the parents permitted to overlap and their dependency/path/contract/resource isolation. An existing prose list or pair is sufficient; no parallel-group JSON or new validator field is required. Do not infer permission from separate filenames, an omitted dependency, or spare model capacity, and do not retroactively declare work parallel after a premature spawn. Same-parent children remain serial. Worktrees do not isolate shared DBs, ports, caches or Git common metadata automatically.

If a writer starts early, interrupt that actual writer and wait for it to stop; do not merely change its state label or let it finish "to save work." Retain its partial diff uncommitted and do not reset/revert user work. Record SEQUENCE_GATE_VIOLATION and the real actors/candidate. If the reviewed plan or product candidate changed, that in-flight pass cannot bless the changed snapshot; retain useful findings and close only the affected gap. If no reviewed input changed, preserve its valid result. Close the original prerequisite first, then reassess the held partial diff against the final plan/head before resuming. Do not create another recovery section, replay the feature or reset budgets.

BLOCKED or ABANDONED is a stop, not a successful prerequisite. Main may separately schedule an explicitly independent parent within an approved parallel plan; it must not release a dependent successor.

## Completion and external hold

Do not finish while a requested subagent is still working; wait/cancel per host rules. Complete/blocked status reflects real results, not desired metadata. Advisor-triggered work remains stopped until external result plus human adoption. Audit cannot authorize a resume.
