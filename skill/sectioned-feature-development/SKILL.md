---
name: sectioned-feature-development
description: "Plan, delegate, review and deliver non-trivial changes as business sections with optional internal subsections. Use for roughly over 300 behavioral lines, over three owners, changed persistence/security/concurrency/routing/public-protocol/state semantics, an unclear impact cone or failed whole-change convergence. Merely touching a risky module does not trigger a small exact fix. Activate prospectively if work grows. Explicit invocation skips routine human plan approval, never a saved PLAN, independent review or real subagents. Automatic activation is announced and pauses after the first saved plan. More than one section or executable subsection requires EXECUTE_WITH_COMMITS and a dedicated non-main branch. Closed plans stay closed unless explicitly reopened. The agent schedules from readable artifacts; only basic section structure is mechanically checked, not JSON state, actor receipts or approval hashes. Preserves model tiers, safe parallelism, Astra/GLM reviews, external human Advisor and process audits."
---

# Sectioned Feature Development 4.5.3

## Core execution contract

**The main agent schedules; scripts do not grant permission to proceed.** Keep the reviewed business contract, real delegated work, tests and independent review. Do not make a new workflow programming project out of an implementation task.

1. Main reads the task and repository rules, identifies the actual feature/base/branch, and records the Audit mode, evidence scope and delivery pending state under **Audit handoff — required, not an extra product gate** **before planning or resumed dispatch**. Main writes a complete canonical `.agent-work/PLAN-FULL.md` and maintains one concise `FEATURE-STATE.md`.
2. Run `section_plan.py validate` once for the first plan and after structural changes to IDs, dependencies, parents or planned implementation roles. It checks only that structure. Ordinary wording edits do not require another run.
3. Obtain an actual independent PLAN review, save its result once, and record main's candidate admission. Ordinary plan-only corrections do not require a new reviewer APPROVED at a matching hash.
4. For each ready section/subsection, save a bounded TASK, **actually spawn the planned implementer**, wait for its real result, save a HANDOFF, and freeze the product candidate before review.
5. Main admits real findings; a delegated worker repairs them; reviewers verify the bounded delta and required independent final evidence. Record real IDs and checks, not fabricated schema receipts.
6. Accept the parent only with required coverage, closed findings and tests. Integrate accepted work, validate the final product head and close the business plan. When Audit is enabled, keep delivery PENDING until the canonical pack/pair is complete or a real delivery obstacle is explicitly reported; only then send the final feature-delivery response.

This applies with audit OFF, one section, and explicit invocation. **There is no runtime `workflow.py`, `execution_artifacts.py`, `advisor_flow.py`, STATE.json, SFD_PLAN_V4 schedule or ready/register/approve/accept CLI.** Do not restore them or edit a product plan to satisfy their historical formats.

## Audit handoff — required, not an extra product gate

**Audit remains LIVE by default; only an explicit user `audit off` disables it.** User-explicit invocation, one section, no-commit mode, a `continue` request, an environment gap or a new session never silently opts out.

- **Activate / take over:** before planning or resumed dispatch, read [audit-mode.md](references/audit-mode.md) once in this context. In existing FEATURE-STATE record `Audit mode: LIVE`, `Audit delivery: PENDING`, current feature/run, evidence location and available source-session pointers. For OFF, retain the user's explicit authority. Reuse existing current-feature evidence; a missing Audit line is not permission to turn it off.
- **Preserve at real transitions:** save the actual request/Grill Me corrections, reviewer and worker results, candidate/check references, model attempts and scope decisions once in the existing artifacts or trace. Main owns the one final pack; workers return evidence, not their own audit packs. Keep unknown history UNKNOWN/RECONSTRUCTED rather than inventing LIVE events. Do not log every read/poll or add product work for telemetry.
- **Resume:** carry the same feature's Audit mode, scope, source sessions and pending delivery across continuation/compaction/takeover. Inspect only missing relevant evidence. Status replies and interruptions preserve PENDING; they do not require a fresh ZIP each turn.
- **Finish:** close the business PLAN at its actual delivered candidate, but retain `Audit delivery: PENDING` and `Next: finalize current-feature audit` until the packaging outcome is known. Never write `Next: none` while Audit is pending. Use the existing atomic finalizer, with at most one bounded artifact-only correction after failure. Keep working evidence when reporting a real obstacle; do not fabricate a finalizer failure or silently call it complete.
- **Final feature-delivery reply:** state product readiness separately and include **Audit COMPLETE** with the actual main ZIP and required companion; **Audit OFF** with explicit user authority; or **AUDIT_PACK_INCOMPLETE** with the real obstacle, actual attempt/correction (or why invocation was impossible) and preserved working directory. A COMPLETE_WITH_GAPS pack may be delivered with its gaps stated. A missing/stale required companion is incomplete, not complete.

Only this skill's process pack belongs at `~/Desktop/audit-pack/xxx.zip`; actual ZAS attempts use `xxx-zas.zip`. No actual ZAS means NOT_USED, not an empty companion. No `.sha256` sidecars. A later request is new work by default: it neither erases the original pending audit nor inherits its earlier CLEAN as evidence for new code. Preserve the closed boundary and prior evidence without reopening the old PLAN for packaging.

Only the basic section structure check is a routine **process validator**. Retained safe-file/pack/session/trace/ZAS utilities run only for their corresponding operation, never to schedule or admit code. Audit OFF does not waive execution artifacts; Audit gaps never require another reviewer, test, repair, Advisor or ZAS call. Do not restore JSON state, actor receipts, approval hashes or ready/register/approve gates.

## Stop before dispatch — review completion is not acceptance

- **Native terminal event:** a native subagent `Message Type: MESSAGE` is progress only, regardless of whether its text says “final”, `CLEAN`, or states a conclusion. Treat the result as returned only after receiving `Message Type: FINAL_ANSWER` and confirming the native task reached `completed` (`subAgentActivity.kind=completed` or an equivalent native status). If an earlier `MESSAGE` conflicts with `FINAL_ANSWER`, `FINAL_ANSWER` controls; never release a barrier or dispatch a dependent actor from the earlier message.
- **Global PLAN barrier:** before spawning any product/test implementer (including S01 or a parallel worker), every PLAN pass selected by policy for this revision must have actually returned: primary review, selected GLM challenge, and any genuinely required PLAN_DELTA. Main must read/save the results and resolve or evidence-back reject the material candidates. A submitted job, progress message, early candidate, poll timeout, or human approval of the plan is not completion. Do not pre-spawn a writer to scaffold, prepare tests, or "work while review finishes."
- **Serial parent barrier:** S01 implementation complete or initial review CLEAN is not S01 accepted. Wait through applicable repair/delta, parent reconciliation, required final review and checks; main records acceptance, and any dependency is integrated, before dispatching S02. BLOCKED, ABANDONED or cancelled review does not satisfy a dependency. A bounded repair of the current unit is allowed after its reviewer returns and main admits the findings; it does not release a successor.
- **Serial child barrier:** do not dispatch the next same-parent subsection until the current checkpoint review has returned, its material findings/delta are closed, and main records CHECKPOINT_VERIFIED. Parent acceptance still follows the existing assurance rules.
- **Parallel exception is explicit, never inferred:** only named independent parents already authorized to overlap in the reviewed PLAN may overlap implementation/review in separate worktrees with no path/contract/resource conflict. Different files, missing dependency labels, or a waiting reviewer do not grant that authority. No plan-stage overlap; no same-parent child overlap. Repository no-parallel rules win.
- **Before each real dispatch**, identify the completed prerequisite, any still-live reviewer/writer, and the exact native-or-ZAS route in the existing FEATURE-STATE/TASK/REVIEW record. A short prose handoff is enough; no new file, JSON schema, hash gate or command. If a required review is still running, wait on that actual actor instead of dispatching, editing status to "done", or asking for routine human approval.

## Native role and ZAS MCP are different execution routes

| Required work | Actual route | Identity and follow-up |
|---|---|---|
| Native PLAN review | Native Codex subagent mechanism selecting [@plan_reviewer](subagent://plan_reviewer) | Tool-returned native task/session ID; native wait/follow-up tools |
| Native code-review slot | Native Codex subagent mechanism selecting [@code_reviewer](subagent://code_reviewer) | Tool-returned native task/session ID; native wait/follow-up tools |
| ZCode/GLM review slot or selected PLAN challenge | Direct ZAS MCP `zcode_subagent_spawn`, followed by `zcode_subagent_wait` / `zcode_subagent_result` | ZAS-returned agent_id; ZAS lifecycle tools |

**[@code_reviewer](subagent://code_reviewer) always means the native Codex role, never ZCode and never a wrapper that delegates to ZAS.** `$code-review` names the shared review instructions, not the provider. Do not satisfy a native slot with an MCP job, send a native ID to ZAS, or call a native reviewer merely to forward work to ZAS. Provider substitution requires explicit applicable user/repository authority and is recorded as an override, never an alias.

## How much to read

Read this root file once per fresh context. Then load only the reference for the phase actually being performed; finish reading a selected reference, but do not preload every reference.

- Bootstrapping, handoffs, resumption and closure: [artifact lifecycle](references/artifact-lifecycle.md).
- Trigger, late adoption, branch and actor responsibilities: [activation](references/activation-and-orchestration.md).
- Authoring or materially changing a plan: [section planning](references/section-planning.md), then the [composable planning router](references/planning/router.md) and only its applicable files. The universal file is the unmatched-dimension fallback; do not preload the library.
- First code review/repair: [bounded review](references/bounded-review.md).
- Security, compatibility or mechanism-growth candidate: [scope control](references/scope-control.md).
- Subsections / parallel work only when used: [subsections](references/subsections.md), [parallel execution](references/parallel-execution.md).
- Profile selection / external review: [model routing](references/model-routing.md), [reviewer routing](references/external-reviewer-orchestration.md).
- Actual ZAS call only: [ZAS adapter](references/zcode-mcp-adapter.md); observe only on suspicion, using [progress supervision](references/zas-progress-supervision.md).
- Hard cap / external Advisor only when triggered: [recovery](references/recovery-and-migration.md), [Advisor](references/advisor-escalation.md).
- Final integration: [integration and tests](references/integration-and-testing.md).
- Audit at activation/takeover and finalization: [audit](references/audit-mode.md), read once per fresh context before planning/resumed dispatch; reread relevant completion instructions at final handoff. Read [ZAS companion](references/zas-audit.md) only for actual ZAS use. Do not reread the full reference at every dispatch.

## Composable planning knowledge, not additional authority

During existing PLAN authoring, first read [planning/router.md](references/planning/router.md) and **all four short catalogs**: [domains](references/planning/domains/INDEX.md), [languages](references/planning/languages/INDEX.md), [adapters](references/planning/adapters/INDEX.md), [concerns](references/planning/concerns/INDEX.md). Then read the guides matched to the actual changed path **before drafting their plan decisions**. Only after these matches are inspected may `universal.md` cover a specifically named uncovered part. Never skip catalogs or available specialized guides by choosing universal first. Catalog inspection does not mean reading every linked file or forcing a match on every axis. Reuse complete reads within the same planning context. Domains/languages remain independent; full-stack + Svelte + Java is valid only with actual source evidence.

Merge the selected questions into one PLAN. For a changed boundary, carry one concrete source-inspected/observed or explicitly planned request/response example through producer, real consumer and checks. Classify named consumers as EDIT, VERIFY_UNCHANGED or OUT_OF_SCOPE based on the approved outcome. Producer HANDOFF supplies the actual example; consumer TASK consumes that same contract rather than guessing keys, filtering or decoder semantics.

The existing independent PLAN reviewer independently inspects the four catalogs, reads relevant matched guides, and checks the selected evidence and missing seams in its one authorized pass. Record the actual four-axis selections and any named universal fallback in the existing PLAN routing paragraph, not a new report. Domain count never creates a new section, model tier, reviewer, framework or acceptance criterion. Missing labels are not blockers without a concrete authority-backed failure. No routing script, JSON schedule, receipt, approval hash, routine web research or new gate is introduced. Details stay in the applicable references and existing PLAN/TASK/HANDOFF; accepted work is not reopened for this release.

## Authority, activation and Git

- Repository instructions take precedence, including a primary-checkout-only or no-parallel restriction.
- For `USER_EXPLICIT` implementation, proceed without routine human plan approval. Automatic invocation must be announced with actual trigger evidence, then stop after saving the first proportional PLAN-FULL and provide `[PLAN-FULL.md](/absolute/repo/.agent-work/PLAN-FULL.md)` before plan review.
- User clarification, risky new scope, unsupported environment or missing required subagent can still block. A planning/review request alone does not authorize implementation or commits.
- Execution modes: `PLAN_ONLY` permits planning/review only; `EXECUTE_NO_COMMIT` permits authorized implementation without commits; `EXECUTE_WITH_COMMITS` requires the approved coherent implementation/repair commits. A multi-unit plan may be prepared in `PLAN_ONLY`; product/test implementation must obey the following requirement. More than one business section **or more than one executable subsection** requires `EXECUTE_WITH_COMMITS` and a dedicated non-main feature branch **before the next product/test edit**. Record the selected mode and branch explicitly in PLAN-FULL and FEATURE-STATE. Do not treat an existing feature branch, a plan-only request or an explicit no-commit instruction as permission to omit the execution-mode decision; resolve any conflict before implementation.
- From main, scoped feature branch creation needs no extra approval. From another branch, ask the user to choose branching from `main`, branching from the current branch, or merging the current branch into `main` before branching, unless continuing the already authorized feature branch. Never reset main to relocate commits.
- Do not merge to main, push, create PRs, rewrite history, clean or discard user work without separate authorization. Accepted worker integration into the feature branch is allowed under the approved parallel plan.
- Keep `.agent-work` locally excluded and untracked. Inspect once at entry; use ordinary Git or `ensure_agent_work_untracked.py .` (also accepts `--repo .`). If tracked, preserve files and request a separate index-cleanup decision. Do not repeat this check at every handoff.
- Later requests after completion are new work: classify as local fix or new sectioned feature. Reopen a closed plan only on explicit authority; preserve history and budgets.

## One plan and readable state

Use `assets/PLAN-FULL.template.md`. The only parseable fields are section/subsection heading IDs, `Implementer` links and `Depends on`; all business decisions are readable Markdown, not duplicated JSON.

Each unit states its business/increment outcome, existing authority, owner/edit boundary, inspect-only dependencies, exclusions, invariants, concrete acceptance examples, checks, explicit planned implementation role/reason and dependency. The feature states branch/mode, integration order, any parallel restrictions, original corrections and final acceptance.

Every parent and every child must choose one before plan review:
[@impl_nano](subagent://impl_nano), [@impl_mini](subagent://impl_mini), [@impl_std](subagent://impl_std), [@impl_large](subagent://impl_large).
Do not infer a child's role, choose it during dispatch, or split an invariant merely to use a cheap model.

```bash
python {skill-dir}/scripts/section_plan.py validate .agent-work/PLAN-FULL.md
# Optional conveniences, not additional gates:
python {skill-dir}/scripts/section_plan.py list .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py extract .agent-work/PLAN-FULL.md S01 --output .agent-work/PLAN.md
```

Validation never approves a plan or proves a real agent/test ran. If a helper fails due to tooling/legacy syntax, inspect the same basic structure manually once, record the tool gap, and continue only when the real contract is clear. Do not debug the Skill, rewrite old evidence, or seek unrelated drafts in the product task. Genuine dependency cycles, missing implementation choices or unclear business obligations must still be resolved.

## PLAN review and proportionality

Main authors and saves the plan. Actually dispatch a fresh [@plan_reviewer](subagent://plan_reviewer) with confirmed requirements, the saved plan, direct source seams and exclusions. Do not give it prior reviewer conclusions as desired answers.

Necessity comes before hardening: challenge an unrequested marker, migration, compatibility layer, registry, journal, proof tool or framework before enumerating its edge cases. Use minimal-counterfactual, production-route/consumer, representation/precedence, state/lifecycle and bounded-input-cardinality lenses only when the task activates them. Private helper spelling, arbitrary probe filenames and a not-yet-created file with an explicit creation owner are not blockers without real consumer authority.

Candidates: `PLAN_BLOCKER`, `PLAN_SCOPE_EXPANSION`, `OWNER_DECISION`, `PLAN_NIT`. Main writes its admission and bounded corrections alongside the untouched original report. A reviewer NEEDS_CORRECTION is compatible with main proceeding once every material issue is actually resolved or evidence-backed rejected; do not forge reviewer approval.

Default: one native PLAN full review. Keep the existing optional second independent GLM challenge for genuinely high complexity (hard-to-bound impact/architecture change or multiple coupled high-risk/runtime/ownership boundaries), not every multi-section task. If material boundary changes require a recheck, request **one PLAN_DELTA** covering only those changes; no full-review clean streak or recursive PLAN committee. Formatting/hashes/state synchronization never trigger re-review. Unresolved product authority remains a real blocker.

## Freeze and delegate

Main persists the relevant TASK (or extracted PLAN plus CONTRACT) with unit, planned role, actual base, owner/non-goal boundaries, AC/checks, workspace and return instructions. Do not create duplicate contracts when the TASK already contains them.

Actually invoke the native tool for that role and save the returned task/session ID and result reference in FEATURE-STATE/HANDOFF. A clickable role, requested model, JSON claim or renamed alias is not a dispatch. Parent does not write product code/tests; only explicit authorized setup and mechanical Git integration are parent exceptions. If required subagents cannot be created, retry the same bounded dispatch at most once, then `ORCHESTRATION_BLOCKED` rather than silent main-thread implementation.

Workers do not maintain parent state or accept their own work. Main saves their real result once, actual diff/head/checks and residual gaps. Requested and observed models are separate; unavailable observed metadata is UNKNOWN, not a task blocker by itself.

For a serial parent: IMPLEMENT → CHECK → frozen REVIEW → admitted REPAIR → CHECK → DELTA → required FINAL → ACCEPTED → INTEGRATED. No writer may modify the reviewed candidate; wait for review termination and main admission before repairs. If violated, stop the writer, preserve partial work, invalidate only the contaminated pass, and return to the appropriate boundary.

Independent parents may overlap only in separately authorized worktrees with no dependency/path/contract/resource collision. Sibling subsections are serial. A prerequisite unlocks consumers only when accepted and integrated. Main keeps this schedule in readable state, not a reservation database.

## Review and repair

Use `DELEGATED_PASS` with the companion code-review. `sfd-delegated-review/4.2` and flat compatibility `sfd-delegated-review/4.0` describe pass semantics, not a required JSON envelope. Plain Markdown containing the same information is valid.

- Native full reviewer: fresh [@code_reviewer](subagent://code_reviewer); logical full-review slots alternate **native → ZCode GLM → native** across the feature. First is native. Delta/checkpoint/retry/advisor calls do not create new full slots.
- Record planned provider, actual dispatch route and raw returned ID together for each logical review slot; a role/profile name or model self-description is not route evidence. Delta/retry does not advance the full-review counter.
- The original reviewer owns same-pass falsification and supported delta follow-up. Fresh full passes have new identities. A terminal ZCode task cannot be resumed; same-provider fresh delta uses explicit `same_session=false / TERMINAL_CONTINUATION_UNSUPPORTED`, or blocks if strict continuity was required. Repository/user provider overrides are explicit and do not change implementation assignments.
- `ONE`: clean initial can accept; with material repair, close findings via delta and require one fresh final full pass.
- `TWO`: primary coverage/closure plus fresh independent final. Never two repeated whole-change scans after each repair.
- Resolve AUTO by semantic risk, retaining TWO for material migration/persistence, credentials/money/security, shared concurrency/retry/cancellation/process lifecycle, public compatibility/routing and broad coupled ownership. Small exact fixes not changing those semantics can be ONE. Mechanical work can use deterministic checks plus one final pass.
- Subsection checkpoints verify local increments; they do not accept the parent or grant extra clean rounds/budgets. Parent reconciliation covers interactions and joint oracles before the parent's ordinary final requirement.
- Every blocking candidate needs changed-diff causality, supported reachability, prior authority, material consequence and bounded repair. Main can reject scope proposals even from repeated reviewers.
- Freeze finding IDs/criteria/repair owner before a delegated repair. Review only its delta and invalidated cone afterward. Save one cumulative ledger plus actual outputs; no normalized receipt empire.

## Hard cap, integration, completion

All admitted repair attempts share the original parent lineage's five ordinary waves, including checkpoint/final repairs; failed fixes count. Skill/model/run/child changes do not reset this. At the sixth independent root cause, preserve current tip and request one fresh bounded diagnosis under the retained recovery reference. One nonstructural recovery adds one named attempt; a genuinely replaced acceptance boundary may get a new five-wave window once, inheriting recovery-used. No recursive splitting or reimplementation for ledger purity. Integration has its own cumulative budget, not double-counted parent repairs.

External human Advisor remains a rare independent path even audit OFF. Apply the retained ADV triggers, stop real actors, export the repository/Git through the safety helper, then wait for the external result and human adoption. No native advisor role; no automatic upload. Record the decision/restart scope in readable state, not an approval script.

Before final integration, list `unproven_composition`; only a nonempty concrete list warrants another integration reviewer. Targeted checks follow affected changes, section/package checks cover the frozen candidate, final feature checks cover the assembled product. Reuse unchanged-head/environment evidence; a new reviewer does not mean fresh CI. Later product/test edits require closure of the changed range, not repeating accepted history.

Close with exact delivered head, real review/check references, known environment/product gaps and remaining owner decisions. Record product COMPLETED separately from Audit delivery; preserve the current-feature workset until the required pack is delivered or retain its exact location for an incomplete handoff. Archive only under applicable file-operation authority. Never leave the old plan open merely to accommodate a future request.

## Brownfield continuation

For a new session on an existing approved feature: inspect the current requirements, PLAN, actual source/Git and the relevant original reviewer result once. Also inherit its Audit mode, scope, evidence pointers and pending delivery before resuming; a new session is not a new feature or implicit audit off. Do not reconstruct unrelated historical tasks. Preserve valid code and findings. If only old JSON/receipt formats are absent, write a concise handoff note and proceed under this version; do not manufacture approval, actor IDs or old hashes. If the report belongs to another feature, do not reuse it. Missing genuine review coverage calls for the smallest necessary independent pass; metadata translation alone never does.

## Non-negotiable anti-expansion rules

1. **Current-diff causality:** a blocking finding must be caused by the current section diff, or be a pre-existing defect that the diff necessarily depends on, activates, serializes, or exposes on an acceptance path. Merely passing through the same entry point or discovering an old defect nearby is insufficient.
2. **No contract bootstrapping:** a plan or section contract records authority; it does not create authority. Every new outcome, option, UI/config surface, compatibility promise, proof harness, or structural mechanism must trace to the original user request, a repository-required obligation/current production contract, or a demonstrably unavoidable correctness dependency. “The plan says so” is never sufficient.
3. **Monotonic scope:** after the feature/section contract is frozen, implementation and review may simplify or narrow it but may not enlarge it without an explicit owner decision. Repetition by multiple reviewers does not create authority.
4. **No review-authored requirements:** reviewers cannot enlarge the feature contract, supported environment, threat model, compatibility promise, durability promise, or rollout obligation.
5. **No automatic mechanism growth:** a new registry, service, persistence layer, background worker, parser framework, global analyzer, CI governance rule, security control, public configuration surface, or standalone proof harness requires an external authority anchor. Reviewer preference or another plan section is not an anchor.
6. **No repeated full rediscovery:** each behavioral section gets at most one `INITIAL_BOUNDED` review. Repairs use `REPAIR_DELTA`. A fresh `FINAL_BOUNDED` is required after repair and for dual-evidence assurance, but is omitted when one-evidence assurance is satisfied by a clean initial review.
7. **No process-only rework:** workflow schema, artifact format, fingerprint, review template, or skill-version changes do not invalidate accepted code, tests, or review evidence.
8. **No evidence-only descendants:** do not create a new section solely to rebuild review lineage, move a test earlier in Git history, satisfy a new artifact format, or prove that accepted ancestors were “clean.”
9. **No automatic clean-room retry:** preserve correct current work. Restart from an older base only after a concrete diagnosis proves the implementation direction itself is wrong and cannot be simplified in place.
10. **Proportional validation:** targeted checks after repairs, section/package checks before final review, and broad repository/application checks at integration. Do not rerun the broadest suite after every local edit.
11. **Review is not audit:** unchanged code may be inspected only to establish causality, reachability, contract reality, or direct regression risk. Unrelated repository defects are out of scope.
12. **Inaction is valid:** a clean review may return no finding. Never manufacture work to justify a reviewer invocation.
13. **Finite cumulative budgets:** section and integration repair waves count across initial, delta, final, and recovery phases. Entering a new review phase or choosing `CONTINUE_CURRENT` never resets a counter.
14. **Exact requirement examples are contracts:** every user-supplied failing example, expected counterexample, and correction must map to an acceptance criterion and test/probe before plan approval. Later corrections mark conflicting earlier guidance `SUPERSEDED`; retain superseded guidance as provenance only, not as an active requirement.
15. **Final-head evidence:** the delivered product/test head must equal the head covered by required final review and validation. Later process/docs-only commits are harmless; later product/test changes require only bounded closure for the changed range.
16. **Feature isolation:** one feature ID owns one local active PLAN, state, review ledger, and audit range. Starting a new feature archives or resets prior local artifacts; never append unrelated work to an old ledger or commit `.agent-work`.
17. **Reusable validation evidence:** an unchanged code range may reuse an identical successful check. A fresh reviewer means independent analysis, not automatic rerunning of the same CI command.
18. **Exact requirement provenance:** retain the original user messages, Grill Me questions/answers or equivalent requirement clarification, later corrections, and superseded guidance as audit evidence. A summarized PLAN is not a substitute for the original request record.
19. **Audit status is multi-axis:** telemetry gaps, sequence gaps, stale counts, renumbered finding IDs, or other process metadata drift do not make product evidence conflicted when Git/source/review conclusions remain mechanically reconcilable. Reserve `CONFLICTED` for unresolved contradictions that can change scope, finding/repair identity, final-head evidence, or readiness.
20. **One canonical audit pack:** when audit is active, finalization is idempotent and atomic. Never emit a series of timestamped candidate ZIPs; update the canonical feature/head ZIP only after validation succeeds.
21. **Role isolation:** the main agent orchestrates and admits findings but does not edit product code/tests. Plan reviewers never implement or code-review; implementers/repairers never review; final reviewers are fresh and role-distinct.
22. **Candidate/parent barrier:** never write the reviewed parent candidate or release dependent work while its reviewer, admitted finding, repair, or acceptance gate is active. The authorized 4.x parallel extension permits only independent parents in separately reserved worktrees; it does not relax this per-parent barrier.
23. **Necessity before correctness:** plan review must first challenge whether a proposed marker, migration, registry, backup/rollback contract, harness, or shared mechanism is required. Do not improve the internal design of unanchored plan-created scope.
24. **Foundation decision without silent widening:** when a local patch would create a second authoritative rule or leave sibling callers wrong, stop for a bounded owner choice between the shared foundational fix and the local patch. Cosmetic extraction or a single-use helper is non-blocking.
