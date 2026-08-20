---
name: sectioned-feature-development
description: "Plan, pre-review, delegate, review, integrate, and audit non-trivial software changes as minimal bounded sections without plan-created or review-created scope creep. Use when the work is non-trivial and likely exceeds roughly 300 behavioral lines, affects more than three behavioral owners, materially changes persistence/schema/security/auth/concurrency/routing/public-API/process-lifecycle/state semantics, has a hard-to-bound impact cone, or previously failed to converge. Merely touching a high-risk module is insufficient for a local calculation, narrow exact-reproduction fix, bounded one-off script, or mechanical change. Also activate prospectively when initially small work grows beyond these bounds. User-explicit invocation proceeds without routine approval pauses; automatic invocation must be announced and pause after the first PLAN-FULL, before plan review, for user approval."
---

# Sectioned Feature Development
**Workflow revision:** V3.8
Deliver one non-trivial change as a sequence of minimal, reviewable behavior sections. The governing invariant is:

> Review may discover defects in the approved change; it may not create a larger product, threat model, compatibility promise, governance system, or proof bureaucracy.

Use patchset-style review with proportional assurance: one bounded discovery pass, delta-only repair verification, and an independent final pass only when required by the selected assurance level or by a repair. Preserve valid code and evidence across repairs, skill updates, and recovery.

## Authority and safety

- Follow repository-local instructions before this skill.
- Use one execution mode:
  - `PLAN_ONLY`: create or revise planning artifacts only.
  - `EXECUTE_NO_COMMIT`: implement and validate without branch or commit operations.
  - `EXECUTE_WITH_COMMITS`: create bounded branches/worktrees and make coherent implementation, repair, and recovery commits.
- A planning or review request alone does not authorize commits.
- If governing Custom Instructions explicitly delegate branch/commit authority to `$sectioned-feature-development`, that scoped delegation overrides a general no-commit rule only for this workflow's bounded feature/retry branches and coherent implementation, repair, and recovery commits.
- Never push, merge, create a pull request, rewrite published history, clean, delete user work, or discard unrelated changes unless separately authorized.
- In `EXECUTE_WITH_COMMITS`, creating/switching to an isolated feature branch or worktree **from `main`** needs no additional approval. If the current branch is not `main`, do not branch from it without an explicit user choice: branch from `main`; branch from the current branch; or first merge the current branch into `main` and then branch from updated `main`. Preserve uncommitted user work and do not infer that choice. If the repository has no `main`, use a repository-declared default branch only when local rules make it the clear main-equivalent; otherwise ask.
- Branch creation authority does not authorize merge, push, PR creation, history rewriting, or disposal of the source branch/worktree.
- `.agent-work/**` is local operational state. Never stage or commit it. Ensure a local `.git/info/exclude` entry before writing artifacts; if any path is already tracked, stop and ask before untracking it.
- Technical hard-cap diagnosis and bounded recovery do not require continuation approval. Stop only for a genuine owner decision: product semantics, supported environment, compatibility, migration meaning, durability, threat model, acceptable risk, or rollout policy.

## Trigger and activation
Apply a **non-trivial prerequisite** before the risk signals. Use this workflow when the requested or discovered implementation is non-trivial and any condition holds:

- expected behavioral edits are roughly more than 300 lines;
- more than three behavioral owners/modules/services/pages/workflows are affected;
- the change materially changes semantics or ownership at persistence/schema, money/time/units, security/auth/permissions, routing/failover, concurrency/retry/process lifecycle, public API/protocol, deployment, or shared-state boundaries;
- architecture/state ownership changes, the impact cone is difficult to bound, or a previous whole-change loop failed to converge.

Do not trigger merely because work reads, writes, or passes through a high-risk module. A local calculation, narrow exact-reproduction fix, bounded one-off script, read-only probe, or mechanical change normally proceeds without this workflow unless it actually changes the high-risk contract or grows beyond the threshold.

Record `invocation_source` as `USER_EXPLICIT`, `CUSTOM_INSTRUCTIONS_AUTO`, or `AGENT_DISCRETION`, exact trigger/negative evidence, predicted owners/sections/LOC band, and `FEATURE_START | MID_FEATURE`. Re-evaluate after source exploration and before the first commit/review; activate prospectively if underestimated work grows.

- `USER_EXPLICIT`: proceed through the workflow without a routine plan-approval pause; stop only at a genuine decision/safety boundary.
- automatic activation: read this skill, immediately tell the user why it triggered, perform one bounded direct-owner exploration pass, create/validate the first proportional `PLAN-FULL.md`, then stop **before plan review**. Do not print the plan; provide `[PLAN-FULL.md](/absolute/path/.agent-work/PLAN-FULL.md)` plus a concise proportionality summary and request approval. Do not spend the approval phase designing optional migration/recovery/proof machinery or performing open-ended repository inventory.

Read [references/activation-and-orchestration.md](references/activation-and-orchestration.md) for exact activation, late-adoption, branch-transition, role-separation, and section-barrier rules.

## Development audit mode
While this skill is under evaluation, audit is `LIVE` by default. Disable it only when the user explicitly requests `audit off`; a late request uses `POST_HOC`. At activation read [references/audit-mode.md](references/audit-mode.md), initialize the append-only trace and exact requirement record, and keep audit observational: it adds no reviewer, test, acceptance criterion, repair, or implementation scope.

For audit reconstruction, the agent is authorized to read only the relevant Codex session files under `~/.codex/sessions` and `~/.codex-multi-2/sessions`. Select by repository path, feature time window, and feature/task evidence; do not copy unrelated sessions or raw secret-bearing payloads. The working pack remains under `.agent-work`; the one canonical ZIP is finalized atomically under `~/Desktop/audit-pack/`.

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
14. **Exact requirement examples are contracts:** every user-supplied failing example, expected counterexample, and correction must map to an acceptance criterion and test/probe before plan approval. Later corrections mark conflicting earlier guidance `SUPERSEDED`; do not preserve both.
15. **Final-head evidence:** the delivered product/test head must equal the head covered by required final review and validation. Later process/docs-only commits are harmless; later product/test changes require only bounded closure for the changed range.
16. **Feature isolation:** one feature ID owns one local active PLAN, state, review ledger, and audit range. Starting a new feature archives or resets prior local artifacts; never append unrelated work to an old ledger or commit `.agent-work`.
17. **Reusable validation evidence:** an unchanged code range may reuse an identical successful check. A fresh reviewer means independent analysis, not automatic rerunning of the same CI command.
18. **Exact requirement provenance:** retain the original user messages, Grill Me questions/answers or equivalent requirement clarification, later corrections, and superseded guidance as audit evidence. A summarized PLAN is not a substitute for the original request record.
19. **Audit status is multi-axis:** telemetry gaps, sequence gaps, stale counts, renumbered finding IDs, or other process metadata drift do not make product evidence conflicted when Git/source/review conclusions remain mechanically reconcilable. Reserve `CONFLICTED` for unresolved contradictions that can change scope, finding/repair identity, final-head evidence, or readiness.
20. **One canonical audit pack:** when audit is active, finalization is idempotent and atomic. Never emit a series of timestamped candidate ZIPs; update the canonical feature/head ZIP only after validation succeeds.
21. **Role isolation:** the main agent orchestrates and admits findings but does not edit product code/tests. Plan reviewers never implement or code-review; implementers/repairers never review; final reviewers are fresh and role-distinct.
22. **Single-active-section barrier:** do not start the next section or any product edit while the current section has an active reviewer, open finding, repair, or unsatisfied acceptance gate.
23. **Necessity before correctness:** plan review must first challenge whether a proposed marker, migration, registry, backup/rollback contract, harness, or shared mechanism is required. Do not improve the internal design of unanchored plan-created scope.
24. **Foundation decision without silent widening:** when a local patch would create a second authoritative rule or leave sibling callers wrong, stop for a bounded owner choice between the shared foundational fix and the local patch. Cosmetic extraction or a single-use helper is non-blocking.

## Durable artifacts
Use these paths unless repository rules define equivalents:

```text
.agent-work/
├── PLAN-FULL.md
├── PLAN.md
├── FEATURE-STATE.md
├── sections/
│   ├── S01-CONTRACT.md
│   ├── S01-HANDOFF.md
│   └── ...
├── reviews/
│   ├── PLAN-REVIEW.md
│   ├── S01-REVIEW.md
│   ├── S01-CANDIDATES.md       # transient; overwrite or delete
│   └── ...
├── replans/
│   └── S01-g01-DIAGNOSIS.md
├── audit/
│   └── {feature-id}/
│       ├── TRACE.jsonl
│       ├── REQUIREMENTS.md
│       └── PACK-STATE.json
├── audit-packs/
│   └── {feature-id}/current/      # validated working pack; ZIP is external
└── plans/
    └── {YYYYMMDD-HHMM}_FULL.md
```

`PLAN-FULL.md`, the current section contract, and `FEATURE-STATE.md` are authoritative for one recorded feature ID. `PLAN-REVIEW.md` records the one pre-implementation plan gate; it does not create product authority. `S01-REVIEW.md` is one compact ledger for initial findings, delta closures, final verification, and residual risk. Do not create separate durable RAW/ADMISSION/state commits for every reviewer call.

## Load references progressively
- Read [references/activation-and-orchestration.md](references/activation-and-orchestration.md) at activation, late trigger, branch transition, or any subagent/section sequencing decision.
- Read [references/section-planning.md](references/section-planning.md) before creating or changing the section graph and before the mandatory pre-implementation plan review.
- Read [references/bounded-review.md](references/bounded-review.md) before the first section review or any repair loop.
- Read [references/scope-control.md](references/scope-control.md) when security, persistence, compatibility, generalized tooling, test infrastructure, or over-design is possible.
- Read [references/recovery-and-migration.md](references/recovery-and-migration.md) at a hard cap or when adopting this skill mid-feature.
- Read [references/integration-and-testing.md](references/integration-and-testing.md) before checkpoints, final integration, or broad validation.
- Read [references/artifact-schemas.md](references/artifact-schemas.md) when creating or updating artifacts.
- Read [references/audit-mode.md](references/audit-mode.md) at activation while default audit is on, again before canonical pack finalization, or when the user requests post-hoc audit.

## Core state machine

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
  -> @sol_max CLASSIFICATION
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

## Phase 0: Preflight and feature scope

1. Inspect repository rules, architecture sources, current branch, `git status`, relevant commits, build/test entry points, and environment. Apply the non-trivial trigger decision before creating workflow artifacts. Record invocation source/timing, exact trigger and negative evidence, predicted scale, and whether the user approved an automatic invocation.
2. Resolve branch provenance and late-trigger transition under `references/activation-and-orchestration.md`. Branch directly from `main` without another approval; from a non-`main` branch ask the required three-way base question. Preserve current correct work and never silently inherit an unrelated feature branch.
3. Ensure `.agent-work/**` is untracked and locally excluded using the bundled script. Archive/reset prior feature artifacts **locally**, initialize clean local active artifacts, freeze the exact base/adoption head, and initialize live audit unless disabled. Do not create a process commit for `.agent-work`.
4. Record the original user request verbatim, every Grill Me or equivalent clarification question/answer, later corrections, named failing examples/counterexamples, and the smallest end-to-end observable outcome in the feature audit requirement record. Build a requirement-example matrix mapping each current instruction/example to an acceptance criterion and test/probe. Mark conflicting earlier guidance `SUPERSEDED`; do not silently keep both or turn implementation ideas/reviewer suggestions into requirements.
5. Before sectioning, build a compact authority map. Every proposed outcome, acceptance criterion, option/UI/config surface, support harness, compatibility promise, and structural change must cite one of:
   - the original user request or a later explicit owner decision;
   - a repository-required gate/rule or current production contract;
   - an unavoidable correctness dependency, with a causal explanation of why the smaller existing path cannot satisfy the requested outcome.
   Remove items whose only authority is the draft plan, another section, a reviewer, or a desire for stronger proof.
6. Create `PLAN-FULL.md` from the bundled template and record only:
   - requested outcome and observable behavior;
   - existing repository invariants and authoritative constraints;
   - explicit non-goals and unsupported environments;
   - ownership/state boundaries;
   - compatibility, migration, rollout, rollback, and cleanup actually required;
   - feature acceptance criteria and tiered validation;
   - structural changes explicitly allowed by the requirement.
7. Apply a minimum-feature-closure check: if the user-visible result works without an optional setting/status surface, compatibility layer, standalone evidence publisher, generalized hardening, or repository-wide governance mechanism, omit it unless an authority anchor explicitly requires it.
8. Do not add a universal threat model or generalized durability model. Record risk boundaries only when the feature or repository already makes them relevant.
9. If authentication, endpoint, response shape, protocol, integration, or another external seam is not authoritative in repository docs/source, run the smallest real probe before freezing dependent sections. Do not design around an assumed API contract.
10. When the feature is remediation of an audit, freeze the accepted audit finding IDs before implementation. Section review verifies those repairs and the repair diff; it does not continue the repository audit. New unrelated pre-existing concerns go to a separate audit backlog.
11. In `EXECUTE_WITH_COMMITS`, create an isolated feature branch/worktree before product-code implementation.

### Mid-feature adoption

When underestimated work crosses a trigger, stop product edits at a safe point, announce late activation, preserve current correct work, resolve the branch transition, and freeze `adoption_head`. Plan/review only active unaccepted and remaining work. Do not replay completed local work, migrate old review formats, or create clean-lineage/evidence sections. Automatic late activation uses the same pre-plan-review user approval gate. See [references/activation-and-orchestration.md](references/activation-and-orchestration.md) and [references/recovery-and-migration.md](references/recovery-and-migration.md).

## Phase 1: Divide into minimal behavior sections

Create the initial section graph before implementation. Prefer:

1. a walking skeleton or real seam probe when architecture depends on uncertain integration behavior;
2. vertical slices with one observable increment and one primary owner;
3. expand-migrate-contract stages only when compatibility actually requires them;
4. cleanup after consumers have moved and evidence proves the old path is unused.

Every section must define:

- one coherent goal and observable increment;
- an external authority anchor and a short necessity statement explaining why this section is required for the minimum end-to-end outcome and why a simpler existing owner/path is insufficient;
- exact dependency/predecessor relationship;
- a frozen scope manifest: allowed-to-edit owners/files/symbols/routes, inspect-only dependency paths, and explicitly excluded owners/mechanisms;
- a direct impact cone starting from changed symbols and acceptance paths;
- explicit non-goals and deferred owners;
- existing invariants it must preserve;
- structural changes it is allowed to introduce;
- falsifiable acceptance criteria;
- targeted, section, and integration validation tiers;
- reset triggers that would make the section materially different;
- review assurance: explicit `ONE`/`TWO` owner choice, or `AUTO` with the resolved value and reasons.

A section is invalid when it is justified only by another plan/contract, is merely a directory/layer bucket, is a generic governance initiative not requested by the feature, is a test/evidence rehabilitation task whose tooling is not itself the user-requested outcome, or is a vague “finish/integrate everything” bucket.

Use the helper when practical:

```bash
python {skill-dir}/scripts/section_plan.py validate .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py list .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py extract \
  .agent-work/PLAN-FULL.md S01 --output .agent-work/PLAN.md
```

The validator checks durable markers, minimum headings, unique IDs, and dependency cycles. Its fingerprint is informational; a changed fingerprint alone never invalidates evidence.

### Mandatory pre-implementation plan review

After `PLAN-FULL.md` passes mechanical validation and before the first product-code section begins, dispatch one fresh read-only plan reviewer using the bundled request. This gate is mandatory for `EXECUTE_*`; in `PLAN_ONLY`, run it when the requested deliverable includes a reviewed plan. For mid-feature adoption, review only the active unaccepted and future remaining plan.

The reviewer compares the original request, authority map, repository rules/current contracts, relevant source seams, PLAN-FULL, exclusions, and validation tiers. It reviews in this order:

- **necessity first:** reject/defer an unanchored marker, migration, backup/rollback contract, registry, harness, analyzer, or shared mechanism before reviewing its internal edge cases;
- requirement/example/correction traceability and minimum sufficient closure;
- missing/conflicting owners, contracts, dependency edges, external seams, and unbuildable ordering;
- whether local patches duplicate an authoritative semantic rule or leave sibling callers wrong, requiring a bounded foundational-vs-local owner decision;
- unauthorized sections/guarantees/proof machinery/broad validation and disproportionate section/test granularity;
- triggered lenses in `references/section-planning.md`: representation (missing/null/zero/sentinel/browser round-trip), precedence/fallback validity, lifecycle/failure-state closure, and bounded owner inventory.

Classify candidates as `PLAN_BLOCKER`, `PLAN_SCOPE_EXPANSION`, `OWNER_DECISION`, or `PLAN_NIT`. A blocker must cite existing authority, concrete repository/source evidence, the failure if unchanged, and the smallest plan-only correction. The reviewer may not edit code/tests, invent a requirement, design a larger replacement architecture, or start an implementation/review loop.

The main agent admits or rejects candidates and records the result in `.agent-work/reviews/PLAN-REVIEW.md`. Apply ordinary plan-only corrections locally, rerun the mechanical validator, and proceed without another full plan review. Permit exactly one fresh `PLAN_DELTA` recheck only when an admitted correction materially changes the feature outcome, section graph, primary owner, public contract, state/trust/persistence boundary, or external seam. The recheck covers only the changed plan region and its dependency consequences. There is no clean streak, hard-cap recovery, recursive reviewer chain, or process-only section for plan review. If a material blocker remains after the delta recheck, stop for the real owner/technical decision rather than implementing speculatively.

## Phase 2: Freeze and implement one section

Only after the plan review gate is `APPROVED`, and only when no other section/reviewer/writer is active, take the next dependency-ready section. The main agent remains orchestrator/admission owner and must not edit product code/tests.

1. Record exact `section_base` as the accepted predecessor head and assert the single-active-section barrier.
2. Extract only that section into `PLAN.md`.
3. Create `{ID}-CONTRACT.md` with goal, base, frozen scope manifest, direct impact cone, allowed structural changes, non-goals, acceptance criteria, validation tiers, and review assurance.
4. Resolve real owner decisions before product code.
5. Choose review intensity: `MECHANICAL`, `BOUNDED`, or `HIGH_RISK`.
6. Resolve review assurance: use explicit owner choice `ONE` or `TWO`; otherwise use `AUTO` as defined below. Record the resolved value and reasons.
7. Assign a delegated implementer with a stable task/session ID; record all role IDs, current barrier state, base/head, intensity, assurance, findings, waves, and `next_allowed_phase` in `FEATURE-STATE.md`.

Review intensity:

Review assurance controls independent evidence, not review breadth:

- `ONE`: one clean independent bounded reviewer outcome is sufficient. For `BOUNDED/HIGH_RISK`, a clean `INITIAL_BOUNDED` accepts the section; if the initial review finds blockers, close them through `REPAIR_DELTA` and require one fresh `FINAL_BOUNDED`.
- `TWO`: preserve dual evidence: `Clean A` from initial/closure evidence plus a fresh `FINAL_BOUNDED` (`Clean B`). It never means two repeated full scans after repair.
- Explicit user choice overrides `AUTO` unless a repository-required rule mandates stronger assurance. Record the override and residual risk.
- `AUTO` resolves to `TWO` when the section changes persistence/schema/migration; money/security/auth/permissions/credentials; shared-state concurrency, retry/replay/cancellation/background/process lifecycle; business-critical time/date eligibility; public API/protocol compatibility or irreversible external side effects; routing/failover/quota/sticky ownership; two or more runtime/process boundaries or three or more behavioral owners; or has a hard-to-bound impact cone/material incident risk. Otherwise use `ONE`.
- A small local fix may resolve to `ONE` even inside a high-risk module when it changes at most two owners, adds no schema/public contract/persistence/state mutation/retry/concurrency, has an exact reproduction, and the behavioral diff is roughly at most 80 lines.

- `MECHANICAL`: documentation/generated output/rename/local fixture or equally deterministic change with no behavioral, data, trust, concurrency, migration, public-contract, or state-owner boundary. Use deterministic checks plus one `FINAL_BOUNDED` review; skip separate initial discovery.
- `BOUNDED`: one coherent behavior owner with a bounded impact cone. Use normal initial/delta/final flow.
- `HIGH_RISK`: security/permission, persistence/migration, public schema/API, concurrency, destructive behavior, deployment, or state-owner change. Use the same flow with high-risk reviewers and explicit path evidence.

Role identity and sequencing are mandatory; profile choice is secondary. The plan reviewer cannot code-review this feature, the main agent cannot implement/repair, and the final reviewer must be distinct from every writer and the initial/delta reviewer. If the required subagent cannot be created, stop as `ORCHESTRATION_BLOCKED` instead of silently coding in the main thread.

Default routing when available:

- pre-implementation plan review: fresh [@sol_xhigh](subagent://sol_xhigh), or [@sol_high](subagent://sol_high) for clearly bounded non-high-risk plans;
- ordinary implementation: [@sol_medium](subagent://sol_medium);
- high-risk implementation or repair: [@sol_high](subagent://sol_high);
- ordinary bounded initial/delta review: [@sol_high](subagent://sol_high);
- mechanical final review: [@sol_high](subagent://sol_high);
- high-risk initial or final review: fresh [@sol_xhigh](subagent://sol_xhigh);
- hard-cap diagnosis/recovery: [@sol_max](subagent://sol_max).

Dispatch one delegated implementer only after recording that no reviewer is active. The implementer receives repository rules, feature outcome/invariants, `PLAN.md`, the section contract, exact base, and required checks. Require:

- the smallest code change satisfying the section contract;
- reuse of the existing owner/abstraction when it remains coherent;
- no future-section implementation;
- meaningful behavior, edge, and error regression tests;
- targeted checks first;
- one concise `{ID}-HANDOFF.md` with changed files, decisions, commands/results, limitations, and head.

If a new mechanism is not listed under allowed structural changes, stop and either use a local solution or obtain a real contract decision. The repair agent may edit only the allowed-to-edit manifest. If a real blocker requires another owner, return to the main agent for one explicit causal scope decision or owner rebound; the reviewer/repair agent may not enlarge scope. Do not let an implementer “future-proof” the section.

In `EXECUTE_WITH_COMMITS`, stage only intended product/test/user-document files and commit the coherent implementation before review. Never stage or commit `.agent-work` artifacts.

## Phase 3: Patchset-style section review

For `MECHANICAL`, run deterministic checks and one `FINAL_BOUNDED`; mechanical review is always single-evidence. If it reveals a real semantic boundary, reclassify before acceptance. For `BOUNDED/HIGH_RISK`, follow the resolved `ONE`/`TWO` assurance semantics below.

Freeze the reviewed product/test head before every reviewer dispatch; no product writer may run until that reviewer completes or is cancelled. Prefer reusing the initial reviewer session for delta verification so coverage remains sticky. The repair agent must be separate. If that reviewer cannot be reused, pass the compact review ledger rather than reconstructing the feature. The final reviewer is fresh and distinct from the plan reviewer, every writer, and the initial/delta reviewer. A reviewer dispatch that returns no usable artifact may be retried once with the same bounded packet or an approved fallback profile; repeated dispatches do not create evidence and must stop as `insufficient-evidence` rather than forming a wait/retry loop.

### 3.1 Finding admission boundary

Classify every candidate as exactly one:

- `DIFF_CAUSED`: current section diff introduces the defect.
- `MERGE_BLOCKING_DEPENDENCY`: a pre-existing defect lies on a necessary acceptance path and the diff newly depends on, activates, serializes, or publicly exposes its faulty behavior. Incidental traversal, shared entry points, or proximity are insufficient.
- `PREEXISTING_OUT_OF_SCOPE`: unrelated old defect; do not fix here.
- `SCOPE_PROPOSAL`: stronger product/security/durability/compatibility/governance promise; do not implement automatically.
- `DEFERRED_OWNER`: explicitly owned by a later section while the current intermediate state remains correct.
- `EVIDENCE_GAP`: an already-required behavior lacks adequate evidence; cite the exact pre-review acceptance criterion or repository-required gate and add only the smallest oracle. A reviewer preference for stronger proof is not an evidence gap.
- `NIT_DEBT`: non-blocking polish, preference, or bounded debt.

Only `DIFF_CAUSED`, `MERGE_BLOCKING_DEPENDENCY`, and a contract-required `EVIDENCE_GAP` block by default.

For maintainability, materiality requires the current diff to create or materially worsen an ownership split, circular dependency, duplicated authoritative path, unsafe state machine, or similarly concrete defect risk. When a local repair would establish a second source of truth or leave sibling callers wrong, return one bounded foundational-vs-local owner decision; do not silently widen. Preference for helper extraction or a cleaner single-use abstraction is `NIT_DEBT`.

A blocking finding must establish all five:

1. changed hunk or changed contract causing/newly relying on the issue;
2. reachable trigger in the frozen supported environment;
3. existing requirement, invariant, or repository rule violated;
4. material consequence;
5. smallest repair remains inside the current owner without adding an unapproved guarantee.

For security findings, additionally identify the current asset, actor/capability, entry point, trust boundary, and preconditions. A hypothetical new actor, deployment, tenant model, malicious same-UID process, arbitrary in-process object, or stronger attacker is `SCOPE_PROPOSAL` unless already authoritative.

The main agent owns admission. Reviewer prose is a candidate set, not a contract amendment. Do not copy rejected proposals into `PLAN-FULL.md`, descendants, tests, or repair prompts.

The scope manifest bounds edits, not causal inspection. A reviewer may inspect an unlisted dependency only by recording a concrete data/control/serialization/contract chain from a changed symbol to the candidate. That chain authorizes inspection only; editing a new owner requires the main-agent decision above. This preserves genuine cross-owner findings without permitting an open-ended audit.

### 3.2 `INITIAL_BOUNDED`

Run exactly one initial full review over `section_base..section_head` plus the direct semantic impact cone. Use the bundled review request. The reviewer must:

- inspect all changed behavior once through risk lenses triggered by the frozen contract;
- batch material root causes before repair;
- report only current-diff findings under the admission rules;
- avoid repository audit, future-proofing, and generic governance/tooling proposals;
- record reviewed coverage so unaffected conclusions can be retained;
- record any inspection beyond the named cone as an exact causal dependency chain; do not fan out recursively from that dependency.

Write the authoritative classification and coverage summary into `{ID}-REVIEW.md`. Use `{ID}-CANDIDATES.md` only as transient reviewer output; overwrite or delete it after triage.

If no blocker is admitted, the implementation evidence plus initial review satisfies `Clean A`. Under `ONE`, mark the section accepted after required section checks; under `TWO`, proceed to `FINAL_BOUNDED`.

### 3.3 `REPAIR_DELTA`

After the reviewer has completed, freeze admitted root-cause IDs, acceptance-criterion IDs, allowed repair owners, and closure checks. Dispatch a delegated repair agent distinct from all reviewers; batch compatible findings into the smallest coherent repair wave.

After each repair, review only:

- `previous_reviewed_head..current_head`;
- unresolved admitted finding IDs;
- direct callers/callees/contracts/tests whose prior conclusion the repair invalidated;
- new behavior introduced by the repair.

Retain all unaffected initial coverage. A delta reviewer may admit a new blocker only when the repair delta caused it, activated it on a necessary acceptance path, or invalidated the earlier evidence. It may not reopen the original section under a different lens.

The repair agent may modify only frozen repair owners. If closure requires a new owner, stop the repair and return to the main agent for a causal scope decision. Run targeted checks for the repaired owner. Update the single review ledger. When all admitted findings are closed and required targeted/section checks pass, record:

```text
Clean A — closure evidence satisfied
```

A repair wave is one coherent batch of admitted root-cause classes plus its code fix and delta verification. Any admitted repair arising from initial, delta, final, checkpoint, or integration review counts toward the applicable cumulative budget. Reviewer calls, repeated wording, rejected scope proposals, and tool retries do not count.

### 3.4 `FINAL_BOUNDED`

Use one fresh reviewer after any repair, or after clean initial evidence when assurance is `TWO`. Give it the current complete section diff, frozen contract/non-goals, direct impact cone, current checks, and a concise list of closed root-cause IDs. Do not give it rejected scope proposals or prior persuasive narratives.

`FINAL_BOUNDED` is not a second open-ended discovery pass. It checks only:

- the complete current diff against the frozen contract;
- the highest-risk changed path end to end;
- repair impact cones;
- accidental scope or mechanism growth;
- section/package evidence.

It must not perform a repository audit or require a stronger contract. If it finds no new blocking root-cause class, record:

```text
Clean B — independent final evidence satisfied
```

Then mark the section `SECTION_ACCEPTED`, clear active writer/reviewer IDs, and release the section barrier. Only now may the next section start. This reviewer provides the single required clean outcome for repaired `ONE` sections and `Clean B` for `TWO` sections.

If it finds a new admissible blocker, that repair uses the same cumulative section-wave budget. Repair it through `REPAIR_DELTA`, then rerun only `FINAL_BOUNDED`. Do not restart the entire initial discovery unless a reset trigger fires.

### 3.5 Full-reset triggers

Reset to a new `INITIAL_BOUNDED` baseline only when a repair goes beyond the frozen contract or invalidates most prior coverage by materially changing one of:

- public or serialized API/schema;
- authorization, tenant isolation, or trust boundary;
- persistence, migration, durability, or recovery contract;
- state ownership or concurrency semantics;
- destructive, deployment, rollout, or rollback semantics;
- supported environment or section goal;
- most of the section's behavior/architecture.

Do not reset because a plan/review template changed, a fingerprint changed, tests were added, line numbers moved, HEAD advanced by a local repair, a new skill version was installed, or another reviewer might inspect a different lens.

## Phase 4: Five-wave hard-cap recovery

Allow up to five admitted repair waves for one stable section boundary, cumulatively across initial, delta, and final phases. The fifth wave is repaired and delta-verified normally. The counter never resets while that boundary remains stable. Enter hard-cap diagnosis only when:

- a sixth independent root-cause class would require another repair wave;
- a repair cannot close without changing the section goal/owner/architecture; or
- the loop is oscillating or repeatedly reopening the same root cause.

Do not trigger hard-cap recovery merely because the fifth reviewer invocation found a small local omission.

### 4.1 Preserve without discarding

1. Record current `section_base`, `section_head`, five waves, open findings, checks, and rejected scope proposals.
2. In `EXECUTE_WITH_COMMITS`, ensure coherent current work is committed without unrelated user changes.
3. Create a backup ref without switching:

```text
codex/backup/{feature-slug}-{section-id}-g{generation}-{YYYYMMDD-HHMMSS}
```

4. Write `{ID}-g{generation}-DIAGNOSIS.md` using the bundled template.

The backup is a recovery point, not a command to abandon current correct work.

### 4.2 Invoke `@sol_max`

Give a clean [@sol_max](subagent://sol_max):

- original section lineage, whether its single automatic recovery event is already used, current goal/contract, base/head, and diff summary;
- all admitted root-cause classes and repair results;
- current open blocker and test evidence;
- structural changes already present and their requirement anchors;
- rejected scope proposals in a clearly non-authoritative appendix;
- explicit instruction not to implement product code.

Require exactly one recovery classification:

- `CONTINUE_CURRENT`: architecture is sound; authorize exactly one named recovery repair wave on current code, then go directly to `FINAL_BOUNDED`.
- `SIMPLIFY_CURRENT`: remove review-created or unanchored mechanisms in exactly one named recovery wave, then go directly to `FINAL_BOUNDED`.
- `SPLIT_REMAINING`: split only unresolved product behavior into at most two independently shippable descendants while preserving already-correct current work.
- `REBOUND_OWNER`: move unresolved behavior to the correct existing owner/section and update only affected dependencies.
- `REPAIR_EVIDENCE`: fix one contract-anchored oracle/environment gap in one named recovery wave; do not create a test-only descendant.
- `RESTART_FROM_BASE`: last resort when the implementation direction or threat model is demonstrably wrong and in-place simplification would preserve most of the wrong design.

Technical recovery proceeds without asking whether to continue. Ask only when recovery requires a new product guarantee, supported environment, compatibility policy, threat model, migration meaning, or rollout decision.

### 4.3 Recovery constraints

- Default to `CONTINUE_CURRENT` or `SIMPLIFY_CURRENT`; preserve verified repairs.
- One automatic hard-cap recovery event is allowed per original section lineage, regardless of classification. It never grants another general five-wave cycle.
- A non-structural recovery authorizes one named recovery wave only. If its repair or following `FINAL_BOUNDED` reveals another independent blocker, stop and report the unresolved technical/owner decision; do not start another automatic recovery.
- A structural replacement may receive a fresh five-wave budget because its boundary changed, but it inherits `automatic_recovery_used = yes`; another hard cap stops rather than recursively recovering.
- `SPLIT_REMAINING` may add at most two active descendants and may not create process/evidence-only sections.
- Do not re-review accepted predecessors or rebuild “clean evidence lineage.”
- Do not cherry-pick nothing by default; keep current valid code unless `RESTART_FROM_BASE` is justified.
- `RESTART_FROM_BASE` must state which architectural assumptions are wrong, which current mechanisms will be discarded, and why bounded reversion/simplification is insufficient.
- If the unresolved set consists only of reviewer-created tooling, generalized oracles, or process artifacts without an exact acceptance-criterion anchor, structural recovery is prohibited; use `SIMPLIFY_CURRENT`, a truly contract-anchored `REPAIR_EVIDENCE`, or stop.
- Update only the affected section/dependency entries in `PLAN-FULL.md`. Do not rewrite the whole feature plan or invalidate unaffected fingerprints/evidence.

## Phase 5: Integration checkpoints and final gate

Run a targeted checkpoint only when a later section begins consuming a new public contract, schema, permission boundary, state owner, queue, deployment path, or compatibility stage.

Checkpoint review verifies composition and representative paths; it does not reopen every accepted local line. It uses the same finding classes, five-part blocking proof, scope authority, and cumulative repair accounting as section review. An accepted section is invalidated only when changed product code or observed combined behavior disproves its contract.

After all sections are accepted, record an `unproven_composition` list before dispatching any integration reviewer. Run one fresh `$code-review` integration pass over `feature_base..feature_head` only when that list contains a concrete cross-section/runtime/process behavior not already proven by exact-head section/package/consumer evidence. If the list is empty—including after exact package publication plus consumer install/tests/build—reuse the evidence and run only the required feature gate; do not add a redundant integration reviewer. Focus only on:

- original feature outcome and non-goals;
- emergent cross-section API/schema/state/permission/ordering/error behavior;
- migration, compatibility, rollout, rollback, cleanup, and observability actually required;
- representative end-to-end paths;
- branch-scope integrity and residual risk.

Integration composition creates no new authority to add product scope, deployment models, threat models, durability, observability, rollout promises, routes, analyzers, or browser flows. Admit only feature-diff-caused composition defects, necessary merge-blocking dependencies, or evidence gaps tied to an existing feature acceptance criterion/repository gate.

Do not repeat local section review or upgrade the feature into a repository audit. Use one cumulative integration budget of at most five repair waves across checkpoint/final integration; it never resets when final evidence is rerun. After that, allow at most one bounded `@sol_max` diagnosis/recovery event for the feature integration boundary; if the next bounded repair/final pass does not close, stop as `not-mergeable` or for a genuine owner decision.

Run the broadest deterministic suite/build/browser/application checks once at final integration unless repository rules require otherwise. Reuse identical successful evidence for the same code head; rerun only when the relevant product/test range changed or the prior run is not trustworthy. These checks verify the already-listed feature acceptance criteria and repository-required gates; they do not create new acceptance scope. State readiness as `mergeable`, `not-mergeable`, or `insufficient-evidence`.

## Phase 6: Archive and report

1. Verify exact final-head equality: required review/check evidence covers the delivered product/test head. If later product/test changes exist, close only that range before readiness. Update `FEATURE-STATE.md` with section base/head, assurance, evidence, findings, waves, recovery, checks, and residual risk.
2. Delete transient `PLAN.md` only after its section is accepted, replaced, or abandoned with durable state.
3. Overwrite/delete transient `*-CANDIDATES.md`; preserve the compact authoritative `*-REVIEW.md` ledger.
4. Archive the feature-ID-specific `PLAN-FULL.md` and compact ledgers to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md` after final reporting; preserve/archive the old feature-owned active artifacts before initializing a different feature.
5. Keep all process/review/audit artifacts local under `.agent-work`; never stage or commit them. Product-history commits contain only intended product, test, migration, and user-facing documentation changes.
6. Unless audit was explicitly disabled, finalize the read-only pack from the live trace, exact requirement/Grill Me record, Git, sessions, and original artifacts according to `references/audit-mode.md`. Product readiness remains independent, but workflow delivery is `AUDIT_PENDING` until the canonical pack validates and `PACK-STATE.json` is `COMPLETE`. Use the deterministic finalizer; do not create multiple timestamped ZIPs, rerun review/tests, or fix audit-discovered product defects.
7. Report in Chinese by default: feature result, section status, admitted defects fixed, scope proposals rejected/deferred, checks, recovery events, residual risk, merge readiness, maintainability judgment, and the canonical audit-pack path/SHA-256. If finalization fails after one bounded correction attempt, report `AUDIT_PACK_INCOMPLETE` with the preserved work directory instead of improvising more packs.
