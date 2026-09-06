---
name: sectioned-feature-development
description: "Use optional subsections for implementation checkpoints under one parent contract, budget and acceptance. Deliver genuinely non-trivial software changes through an approved requirements contract, reviewable sections, task-based agent selection, bounded reviews, and verified integration. Use for substantial behavioral work, multiple semantic owners, changed persistence/protocol/state/lifecycle contracts, an unclear impact cone, or a whole-change attempt that failed to converge; do not activate merely because a small edit touches a high-risk file. Activate prospectively if a small task grows. Explicit invocation proceeds without routine plan approval; automatic invocation is announced and pauses after the first PLAN-FULL. After completion, reassess follow-up requests as new work rather than appending to the closed plan."
---

# Sectioned Feature Development — 4.1.1

Deliver the approved outcome, not a larger system. The main agent owns admission and integration; delegated agents perform bounded work. This skill describes workflow, not model capability guarantees.

## Read only the current phase

- Parent sections and internal checkpoints: [subsections.md](references/subsections.md)
- Planning and portable requirements: [planning.md](references/planning.md)
- Task/model selection and cheap exploration: [models.md](references/models.md)
- Branches, dependency scheduling and integration: [execution.md](references/execution.md)
- Bounded review and finding closure: [reviews.md](references/reviews.md)
- Exact current ZCode MCP: [zcode.md](references/zcode.md)
- Rare, isolated native advisor: [advisor.md](references/advisor.md)
- Default-on process audit: [audit.md](references/audit.md)

Use `assets/PLAN-FULL.template.md`; its marked JSON block is the executable schedule. Use `scripts/workflow.py validate` and `ready` to check it. These are workflow checks, not a sandbox or proof of correctness.

## Invariants

1. User requirements and current repository contracts supply authority. PLAN, reviewer preference and audit do not create it.
2. A material finding needs changed-diff causality, a reachable supported path, an existing requirement, a concrete consequence and a bounded repair.
3. `.agent-work/` stays local/untracked. Never force-stage it. Preserve unrelated user work and already accepted evidence.
4. **More than one section, or a single section with multiple executable subsections, requires `EXECUTE_WITH_COMMITS` and a dedicated feature branch.** If no-commit instructions conflict, stop for a decision. Do not silently downgrade the workflow.
5. From `main`, creating an authorized feature branch needs no separate approval. From another branch, ask whether to base on main, that branch, or first merge it into main. Worker branches within an already authorized feature are not a new feature-base decision.
6. Parent may serialize local worker commits into the authorized feature branch. This does not authorize merge into main, push, PR creation, reset, clean, deletion or published-history rewriting.
7. A reviewer sees a frozen candidate. No writer mutates that review workspace. Independent, approved DAG siblings may run in different worktrees; a consumer waits for all prerequisites to be accepted **and integrated**.
8. Use stable actual agent/session IDs. Plan author, plan reviewer, implementer and independent code reviewer are different instances; the same model does not mean the same instance.
9. No repeated full rediscovery after each fix. Delta verification preserves the originating review scope and cumulative repair count.
10. `COMPLETED` closes the plan. Later user edits receive a new request assessment, not appended sections, unless the user explicitly requests reopening.

## 1. Intake and requirements

Read repository rules and the named behavior. A small exact fix with direct tests may use normal development; file names, repository size and generated LOC alone are not triggers.

Record invocation source (`USER_EXPLICIT`, `CUSTOM_INSTRUCTIONS_AUTO`, `AGENT_DISCRETION`) and trigger evidence. For automatic activation, read this skill, immediately announce the decision, build the first proportional PLAN-FULL, then pause **before PLAN review** with an absolute Markdown file link. Explicit implementation invocation continues without this routine pause.

Capture the confirmed Requirements Contract, examples, superseded instructions and unresolved decisions. A confirmed grill-me contract may stand alone; do not send the whole interview to executors. Unconfirmed plan text is not human authority. Keep verbatim source messages in the audit-only record.

If a local task grows, stop new writes, preserve existing work, establish the authorized branch, and plan only unaccepted/remaining behavior. Do not rewrite main or replay valid work to manufacture clean history.

## 2. Explore and plan

Use `sfd_explorer` only when a bounded search would materially reduce expensive context loading. It returns source pointers, facts, unknowns and direct owner paths, not a design or acceptance verdict. Skip it for obvious local edits.

Use `astra_xhigh` as a plan author, and a **fresh** `astra_xhigh` as plan reviewer. Give each a bounded packet rather than the whole chat. Plan by atomic behavior first, then by materially different reasoning difficulty where a real interface permits separation. Never split an atomic migration/state transition simply to assign a cheaper model.

A section is the acceptance boundary, not a LOC bucket. Before assigning a large section to an implementer, check for meaningful internal product increments. Use optional one-level subsections with targeted checkpoint review and a shared parent contract, budget and final acceptance; do not split cross-cases of one rule or turn test-only steps into product nodes. See [subsections.md](references/subsections.md).

Every section records requirements, canonical owners, dependency IDs, explicit paths, read/write contracts, resource isolation, tests, model profile and reason. Every stage records whether it can run concurrently. See planning/models references for the targeted review lenses and supported profiles.

For high-complexity plans (unresolved cross-runtime composition, a changed state/representation model spanning several owners, or a previous structural recovery), add one independent GLM plan challenge after the Astra plan is corrected. Not every sensitive file requires this pass. Maximum two full PLAN passes; only changed boundaries may receive one delta recheck. No clean streak.

Validate the plan before dispatch. If section count grows above one, establish commit mode and a dedicated branch **before the next product edit**. A substantive plan correction invalidates only affected approvals; process formatting does not invalidate product evidence.

## 3. Prepare execution

For a parallel plan, ensure `/git-worktree/` is in repository `.gitignore`, then `mkdir -p ./git-worktree`. Give each ready writer a separate branch/worktree under that directory and a base containing accepted prerequisites. No shared checkout, no shared mutable database/cache/port, no worker Git-index concurrency.

Start with at most two concurrent writers as a rollout setting, not a proven optimum. Use more only after explicit local capacity/evidence supports it. If no independent ready pair exists, run serially; do not manufacture parallelism.

Select one implementation profile per section: `luna_xhigh`, `terra_high`, `sol_medium`, or `astra_medium`. Selection is based on source-grounded task structure and oracle strength, not an assumed benchmark hierarchy. Unknown complexity defaults to `sol_medium` or further bounded discovery; novel unresolved structural reasoning may justify `astra_medium`.

Main agent writes workflow state and integrates; it does not silently replace a failed delegated implementer. Distinguish service/environment failure from semantic implementation failure. If one bounded attempt demonstrates under-routing, jump to a suitable model rather than trying all tiers in sequence. Preserve good code; changing models does not reset repair budgets.

## 4. Implement, review, repair

Dispatch only ready DAG nodes with their task packet. Run targeted checks before spending on independent review. Commit each coherent implementation/fix when in commit mode. Freeze the candidate commit (or exact uncommitted fingerprint for an authorized single-section no-commit task).

Decomposed sections run each child as implement + targeted tests + scoped review (`SUBSECTION_DELTA`) on the parent branch. One parent primary reviewer accumulates coverage; after the last child, `PARENT_RECONCILIATION` must close the whole invariant matrix at the final candidate. Child status is CHECKPOINT_VERIFIED, never section acceptance or a new budget. The fresh final review remains at parent level. Atomic sections keep their existing path.

Code review uses `astra_high` and external `glm-5.3`, alternating **feature-wide full-pass reservations**, beginning with Astra. Reserve a pass index before dispatch so concurrent reviews cannot race. PLAN and advisor calls have separate counters; delta checks and infrastructure retries do not advance the full-pass counter.

`ONE`: a clean initial full review accepts the section; if it finds material defects, close repairs through bounded delta verification and require one fresh final full review. `TWO`: one covered baseline/closure plus a fresh independent final full pass. Choose TWO where hidden failure states, weak oracles or composition risk justify independence; a high-risk filename or zero findings alone decides nothing. User/repository assurance requirements remain authoritative.

Checkpoint/delta/reconciliation calls do not advance the full-pass counter, but every actual model invocation is recorded. A parent primary slot reserved at its first checkpoint becomes CLEAN only after parent reconciliation.

The reviewer invokes the bundled `$code-review` with `context=DELEGATED_PASS` and protocol `sfd-delegated-review/4.1` as a single-pass contract: scope, candidate findings, coverage, exact head and gaps only. It may not spawn another review loop, change requirements, repair or accept the section. Use the companion installed `code-review` 4.1; historical docs are not runtime skills. If a stale installed version still conflicts, report the loaded path/protocol instead of silently nesting workflows.

Main admits findings. Same-review verification goes back to its reviewer when the actual session supports it. The current ZCode API cannot resume a terminal agent; follow its explicit continuity policy rather than inventing a continuation tool. New full passes use fresh instances.

At most five admitted material repair waves per original section lineage, shared by every child checkpoint and parent reconciliation/final. Subdivision never resets that count. At the limit, diagnose once: simplify current work, repair within the real owner, split only remaining independent work, or request the rare advisor. No automatic chain of new five-wave budgets and no evidence-only section.

## 5. Integrate and complete

Accept a section only with closed admitted findings, satisfied assurance, completed required checks and exact-head provenance. Integrate accepted sibling commits in the planned deterministic order on the feature branch. If integration changes product semantics or resolves a conflict, review the integration delta and rerun affected checks; isolated green branches do not prove composition.

Before release/readiness, verify the original outcome and negative scope, then run the required full gate once on the integrated product/test head. Reuse evidence only when head/input/config/dependency/environment fingerprints still cover it. Missing required browser/live evidence remains an evidence gap, not a new framework request.

Record `COMPLETED` and freeze the final plan/hash, or accurately stop as `BLOCKED`/`INCOMPLETE`. A post-completion user request gets a new request ID and fresh trigger assessment. Explicit reopening creates a new revision retaining the old one; it does not erase previous budgets or records.

## 6. Advisor and audit

`advisor` is a fresh `gpt-6-astra` subagent, not a manual Pro chat. It receives only the unchanged Advisor Request contract, a small evidence manifest and access to the relevant frozen source. It never inherits the full parent conversation. Lack of a verifiable fresh-context launch is `ADVISOR_CONTEXT_BLOCKED`, not permission to fake isolation. See advisor reference for rare triggers and decision admission.

Process audit is LIVE by default, disable only on explicit `audit off`. Capture lifecycle/model/routing/cost facts at existing boundaries, not every read. Missing audit details do not add product gates. Only this skill's typed process-audit ZIPs may be published to `~/Desktop/audit-pack/`; runtime/conformance/product/advisor evidence stays elsewhere and is referenced by sanitized hash.

Before the final response, publish one canonical process pack, or report an audit-only failure after one bounded correction. Report product readiness, model/context/continuity gaps, maintainability and the audit path separately. Never claim actual model/runtime validation from script tests alone.

Compatibility: DELEGATED_PASS accepts legacy atomic `sfd-delegated-review/4.0`; new child packets use `sfd-delegated-review/4.1`.
