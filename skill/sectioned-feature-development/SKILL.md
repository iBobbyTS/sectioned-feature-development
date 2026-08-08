---
name: sectioned-feature-development
description: "Plan, implement, review, and integrate large or high-risk software changes as bounded sections while preventing review-created scope creep and over-engineering. Use when expected behavioral edits may exceed roughly 300 lines; more than three modules, packages, services, pages, or workflows are affected; persistence, schema, security, permissions, concurrency, deployment, public API, state ownership, or another high-risk boundary changes; the impact cone is hard to bound; or a previous whole-change implementation/review failed to converge. The workflow freezes feature and assurance boundaries, requires minimum-sufficient designs, uses fresh section reviewers plus a separate finding-admission gate, accepts a section after two consecutive clean admitted reviews, and automatically backs up and invokes @sol_max for bounded recovery after five completed review rounds."
---

# Sectioned Feature Development

Develop one large change as a sequence of independently understandable behavior increments. Freeze what the feature promises before code, keep review subordinate to that promise, and admit reviewer findings only when they prove a defect inside the approved scope. Review discovers defects; it does not create requirements.

## Authority and safety

- Follow repository-local instructions before this skill.
- Use one execution mode:
  - `PLAN_ONLY`: create and validate planning artifacts only.
  - `EXECUTE_NO_COMMIT`: implement and validate without branch/commit operations.
  - `EXECUTE_WITH_COMMITS`: create bounded feature/retry branches or worktrees and make coherent implementation/repair/snapshot commits.
- A planning or review request alone does not authorize commits.
- If governing Custom Instructions explicitly delegate branch/commit authority to `$sectioned-feature-development`, that scoped delegation overrides a general no-commit rule only for this workflow's bounded feature/retry branches and implementation, repair, and recovery commits.
- Never push, merge, create a pull request, rewrite published history, clean, delete user work, or discard unrelated changes unless separately authorized.
- Stop for a real owner decision: product semantics, supported environment, compatibility, durability, threat model, acceptable risk, migration meaning, or rollout policy. Do not stop merely because the five-round recovery protocol triggered.

## Trigger

Use this workflow when any condition holds:

- Expected behavioral edits are roughly more than 300 lines.
- More than three modules, packages, services, pages, or workflows are affected.
- The change crosses persistence, schema, money, time, units, security, permissions, tenancy, routing, concurrency, background jobs, public API, deployment, or shared-state boundaries.
- Architecture or state ownership changes.
- The impact cone is difficult to bound.
- A previous whole-change implementation or review loop failed to converge.

The thresholds route work into this skill; semantic risk and reviewability dominate line count.

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
│   ├── S01-SECTION-r01-RAW.md
│   ├── S01-SECTION-r01-ADMISSION.md
│   └── ...
├── scope-changes/
│   └── SC-001.md                 # only when a boundary change is proposed
├── replans/
│   └── S01-g01-HARD-CAP.md
└── plans/
    └── {YYYYMMDD-HHMM}_FULL.md
```

`PLAN-FULL.md`, frozen section contracts, and `FEATURE-STATE.md` are authoritative. Chat/session history and reviewer prose are not.

## Load references progressively

- Read [references/section-planning.md](references/section-planning.md) before creating or changing the section graph.
- Read [references/scope-and-assurance-control.md](references/scope-and-assurance-control.md) before freezing a high-risk boundary, admitting findings, or correcting over-design.
- Read [references/review-and-admission.md](references/review-and-admission.md) before the first section review.
- Read [references/orchestration-protocol.md](references/orchestration-protocol.md) before delegating implementation, repair, or hard-cap recovery.
- Read [references/integration-and-merge.md](references/integration-and-merge.md) before checkpoints, final integration review, or merge-readiness reporting.
- Read [references/artifact-schemas.md](references/artifact-schemas.md) when creating, validating, or archiving artifacts.

## Core state machine

```text
PREFLIGHT
  -> FEATURE_CONTRACT_AND_ASSURANCE_ENVELOPE
  -> SECTION_GRAPH
  -> PLAN_GATE
  -> FREEZE_ONE_SECTION
  -> IMPLEMENT_MINIMUM_SUFFICIENT_DESIGN
  -> LOCAL_VALIDATE
  -> COMMIT_IF_AUTHORIZED
  -> FRESH_RAW_SECTION_REVIEW
  -> MAIN_AGENT_ADMISSION_GATE
       -> CLEAN -> next fresh review
       -> IN_SCOPE_REPAIR -> repair -> validate -> next fresh review
       -> IN_SCOPE_REPLAN -> bounded replan -> retry
       -> OWNER_DECISION -> block for that decision
       -> EVIDENCE_FAILURE -> repair evidence path; round still counts
  -> TWO_CONSECUTIVE_CLEAN_ADMISSIONS -> SECTION_ACCEPTED
  -> CHECKPOINT_WHEN_TRIGGERED
  -> NEXT_SECTION
  -> FINAL_INTEGRATION_REVIEW_AND_ADMISSION
  -> FULL_FEATURE_VALIDATE
  -> MERGE_READINESS_REPORT
  -> ARCHIVE

AFTER_FIVE_COMPLETED_FULL_SECTION_REVIEWS_WITHOUT_ACCEPTANCE
  -> BACKUP_FAILED_TIP
  -> CLASSIFY_ADMITTED_NONCONVERGENCE
  -> @sol_max RECOVERY: SPLIT | SIMPLIFY_REPLACE | REBOUND
  -> VALIDATE_REVISED_PLAN
  -> RETRY_FROM_FAILED_PARENT_SECTION_BASE
```

Advance only when the corresponding artifact and evidence gate is satisfied.

## Phase 0: Preflight and feature contract

1. Inspect repository rules, architecture sources, current branch, `git status`, relevant recent commits, build/test entry points, and validation environment.
2. Freeze the exact `feature_base`.
3. Create `PLAN-FULL.md` from the bundled template and record:
   - exact outcome and observable behavior;
   - explicit non-goals;
   - feature invariants and authoritative constraints;
   - full acceptance criteria and validation oracles;
   - ownership/state boundaries;
   - supported compatibility, durability, concurrency, deployment, migration, rollout, rollback, and cleanup model;
   - an **assurance envelope**: artifact role, protected assets, trusted inputs/actors, untrusted inputs/actors and capabilities, entry points/trust boundaries, required guarantees, explicit exclusions/non-guarantees, and triggers that require a new owner-approved model.
4. Separate an existing repository obligation from a proposed new guarantee. Existing policy and directly necessary correctness/security consequences remain in scope even if not copied into the prompt.
5. In `EXECUTE_WITH_COMMITS`, create an isolated feature branch/worktree before product-code implementation.

## Phase 1: Divide the feature

Create the initial section graph before implementation. Prefer:

1. a walking skeleton or contract proof when integration is uncertain;
2. vertical behavior slices with one observable increment;
3. expand-migrate-contract or branch-by-abstraction stages for compatibility-sensitive transitions;
4. cleanup/contraction only after consumers have moved and evidence proves the old path is unused.

Every section must have:

- one coherent outcome;
- explicit dependencies and predecessor head;
- expected files/symbols/workflows and a bounded direct semantic impact cone;
- non-goals and named deferred owners;
- touched feature invariants;
- falsifiable acceptance criteria and exact evidence;
- rollout/recovery implications;
- a **minimum-sufficient design and complexity budget** mapping every new abstraction, service, registry, configuration surface, persistence mechanism, or security control to an approved requirement or repository invariant;
- a split/replan trigger.

A section is invalid if it is merely a directory/layer bucket, needs undocumented future work to be correct, or gives a reviewer no finite way to decide completion.

Validate and extract with:

```bash
python {skill-dir}/scripts/section_plan.py validate .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py list .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py extract \
  .agent-work/PLAN-FULL.md S01 --output .agent-work/PLAN.md
```

Hierarchical recovery IDs such as `S03.1` and `S03.1.1` are valid.

## Phase 2: Plan gate

Before implementation, verify:

- every feature requirement maps to section and integration evidence;
- dependencies are explicit and acyclic;
- every high-risk boundary has one owner, one proportional assurance envelope, and an oracle;
- every proposed mechanism has a current requirement anchor and a simpler alternative was considered;
- speculative generality, future-proofing, unsupported attackers/environments, and generic frameworks are excluded unless explicitly approved;
- refactor and behavior are separated unless inseparable;
- no section is a vague final integration bucket;
- each section can plausibly converge within five completed full reviews.

Use one clean plan reviewer for ambiguous/high-risk plans. Give it the feature contract, repository constraints, plan, and plan-review criteria only—not the originating session history. It may identify contradictions or unbuildable boundaries; it may not invent new feature promises.

## Phase 3: Freeze one section

For the next dependency-ready section:

1. Record `section_base` as the exact accepted predecessor head.
2. Extract exactly that section to `PLAN.md`.
3. Create `{ID}-CONTRACT.md` from the bundled template.
4. Freeze contract revision, plan fingerprint, assurance envelope, impact cone, complexity budget, acceptance criteria, and validation commands.
5. Resolve genuine owner decisions before code.
6. Update `FEATURE-STATE.md`: lineage, base, active path, review round `0`, clean streak `0`, expected checks, and scope-proposal ledger.

Only an approved scope-change record may expand feature/section guarantees. Reviewer comments and repair-agent preferences never do so automatically.

## Phase 4: Implement and validate the minimum sufficient design

Default routing when profiles exist:

- ordinary implementation: [@sol_medium](subagent://sol_medium);
- high-risk implementation or repair: [@sol_high](subagent://sol_high);
- fresh section review: [@sol_xhigh](subagent://sol_xhigh);
- hard-cap recovery planning: [@sol_max](subagent://sol_max).

The implementer receives repository rules, the frozen feature/section packet, exact `section_base`, and required checks. It receives no authority to implement future sections or expand the assurance envelope.

Require:

- the smallest reversible design satisfying the frozen contract;
- reuse of existing authoritative extension points before new parallel abstractions;
- meaningful behavior, boundary, failure, and regression tests inside the supported model;
- targeted checks before broad checks;
- a handoff containing the actual impact cone and a **complexity receipt**: each nontrivial mechanism, its requirement anchor, simpler alternative, why that alternative was insufficient, and removal/rollback condition.

Stop and replan before continuing if implementation requires a new persistent abstraction, service, setting, generalized framework, threat actor, durability guarantee, concurrency model, or supported environment absent from the contract. Do not silently build it.

In `EXECUTE_WITH_COMMITS`, commit the coherent implementation before review.

## Phase 5: Fresh review plus finding admission

One counting round contains two distinct artifacts:

1. a fresh `$code-review` `SECTION` review over `section_base..section_head` and the bounded direct impact cone, written to `...-RAW.md`;
2. a main-agent admission decision for every candidate, written to `...-ADMISSION.md` and validated by `review_gate.py`.

Use the bundled `SECTION-REVIEW-REQUEST` template. Give each reviewer only the current contract packet, repository rules needed to interpret it, raw diff/repository state, and output path. Do not send session history, previous clean verdicts, prior reviewer persuasion, or rejected scope proposals.

The admission classes are:

- `IN_SCOPE_REPAIR`: approved behavior/invariant is violated; smallest correct repair remains inside the section.
- `IN_SCOPE_REPLAN`: approved behavior/invariant is violated, but the smallest correct repair crosses the frozen section boundary. This is material and must not be dismissed as scope creep.
- `OWNER_DECISION`: correctness depends on a non-inferable product/risk/compatibility/threat-model decision.
- `EVIDENCE_FAILURE`: the oracle/environment cannot support the conclusion; repair evidence, not product code.
- `DEFERRED_OWNER`: valid work already assigned to a named later section and current intermediate state remains valid.
- `SCOPE_PROPOSAL`: useful idea that adds a new guarantee, threat actor, environment, compatibility/durability promise, feature, or generalization.
- `UNSUPPORTED_HYPOTHESIS`: no reachable trigger/evidence inside the supported model.
- `NIT_DEBT`: optional polish or bounded debt.

Admit a material finding only when it states:

1. the approved contract/repository anchor;
2. a reachable trigger in the supported environment;
3. a material consequence;
4. evidence or a falsifiable evidence path;
5. the smallest correct remedy and its boundary effect.

For security findings, also require asset, actor, capability, entry point/data flow, trust boundary, preconditions, and supported deployment context. An explicitly excluded actor or environment yields `SCOPE_PROPOSAL` or `UNSUPPORTED_HYPOTHESIS`, not a blocker—unless authoritative repository policy already makes it required.

Validate one admission and the accumulated history:

```bash
python {skill-dir}/scripts/review_gate.py validate \
  .agent-work/reviews/S01-SECTION-r01-ADMISSION.md
python {skill-dir}/scripts/review_gate.py history \
  .agent-work/reviews/S01-SECTION-r*-ADMISSION.md
```

### Acceptance and repair loop

- Every completed fresh full section review with a raw review and admission artifact consumes one of the five rounds. A dispatch/tool failure that produces no review artifact may retry the same round.
- `CLEAN` admission increments `clean_streak`.
- `IN_SCOPE_REPAIR`, `IN_SCOPE_REPLAN`, `OWNER_DECISION`, or `EVIDENCE_FAILURE` resets `clean_streak` to zero.
- `EVIDENCE_FAILURE` consumes the round but directs work to the oracle/environment rather than product code.
- `DEFERRED_OWNER`, `SCOPE_PROPOSAL`, `UNSUPPORTED_HYPOTHESIS`, and `NIT_DEBT` do not break a clean streak.
- Two consecutive fresh evidence-valid `CLEAN` admissions accept the section provisionally.
- A repair agent receives only admitted agent-fixable findings. It does not receive rejected candidates as requirements and cannot accept its own work.
- After repair, run checks and another fresh full section review. Targeted DELTA checks may verify a repair internally but do not count as clean rounds.
- Deduplicate symptoms under stable root-cause IDs.
- There is no soft cap and no round 6.

## Phase 6: Automatic five-round recovery

After five completed full section reviews without two consecutive clean admissions:

1. Record `failed_tip`, `section_base`, contract/plan fingerprints, all raw/admission files, admitted repairs, rejected scope proposals, checks, and review heads.
2. In commit-authorized mode, make a bounded snapshot commit if needed; never absorb unrelated user work.
3. Without asking permission, create:

```text
codex/backup/{feature-slug}-{section-id}-g{generation}-{YYYYMMDD-HHMMSS}
```

Point it at `failed_tip`; prefer creating the ref without switching branches.
4. Write the hard-cap artifact and classify **admitted** nonconvergence:
   - `DEFECT_DENSITY`: repeated defects inside the frozen contract;
   - `ASSURANCE_BOUNDARY_DRIFT`: raw reviewers repeatedly proposed stronger guarantees/actors/environments and orchestration or implementation partially followed them;
   - `ARCHITECTURE_BOUNDARY_FAILURE`: the approved section owns too many coupled semantics;
   - `CONTRACT_AMBIGUITY`: an owner decision is genuinely missing;
   - `EVIDENCE_FAILURE`: the oracle/environment is inadequate.
5. Do not treat the raw count of reviewer comments as defect density. Scope proposals are evidence of drift, not descendant requirements.

For `DEFECT_DENSITY`, `ASSURANCE_BOUNDARY_DRIFT`, or `ARCHITECTURE_BOUNDARY_FAILURE`, invoke a clean [@sol_max](subagent://sol_max) automatically:

- `SPLIT` for true in-scope defect density while the resulting descendants stay at depth `3` or shallower;
- `SIMPLIFY_REPLACE` for assurance/scope drift—remove unapproved mechanisms and replace the current section with the smallest proportional descendant set, which may be one replacement leaf;
- `REBOUND` when ownership or integration boundaries are wrong, or when another `SPLIT` would create depth `4+`.

Give `@sol_max` the current section, original `section_base`, feature contract, five raw/admission pairs, round-by-round **admitted** findings, rejected scope proposals in a separate non-authoritative appendix, backup ref, and required recovery mode. It must modify only the current section lineage and affected dependency/coverage edges; accepted predecessors and user-owned semantics remain frozen. It must not implement code or promote proposals into requirements.

If another `SPLIT` would create depth `4+`, do not request continuation approval and do not deepen the lineage. Preserve the failed attempt, then require `@sol_max` to `REBOUND` the nearest unstable parent/feature ownership boundary or `SIMPLIFY_REPLACE` the lineage. `CONTRACT_AMBIGUITY` blocks only for the missing owner decision. `EVIDENCE_FAILURE` repairs the oracle/environment rather than splitting product code.

Validate the revised plan, retire the failed parent attempt, and retry from that parent's original `section_base` on a new branch/worktree. Do not cherry-pick failed implementation/repair commits by default; carry only durable orchestration artifacts and explicitly re-derived code.

## Phase 7: Integration checkpoints

Run a targeted checkpoint when a public contract, schema, permission model, state owner, queue, deployment path, feature flag, or dependency cluster becomes consumable by later sections.

Verify cross-section composition and representative end-to-end behavior. Do not reopen accepted local implementation without a concrete combined trigger that violates the frozen feature contract. Apply the same finding-admission and assurance-boundary rules.

Parallelize only dependency-ready sections with distinct semantic owners/contracts, isolated worktrees, and deterministic integration order.

## Phase 8: Final integration and merge readiness

After all active leaves are accepted and required deferred work is closed, run one clean `$code-review` `INTEGRATION` review over `feature_base..feature_head`, followed by a main-agent admission record.

Focus on evidence section reviews cannot establish alone:

- original feature behavior, non-goals, and requirement coverage;
- cross-section API/schema/state/permission/order/error contracts;
- end-to-end and partial-failure paths;
- migration, compatibility, flags, rollout, rollback, cleanup, observability, performance, security, privacy, and operations **inside the frozen feature assurance envelope**;
- branch-scope integrity and latest combined checks.

Do not replay every accepted local line or reopen the threat model without a concrete supported cross-section trigger. Repair admitted integration defects in bounded scope and rerun the invalidated integration evidence.

Report `mergeable`, `not-mergeable`, or `insufficient-evidence`. Section acceptance is never merge authorization. Push, PR creation, and merge still require their own authority. See [references/integration-and-merge.md](references/integration-and-merge.md) for stacked changes, feature flags, expand/contract, merge queues, rollback, and final gates.

## Phase 9: Archive and report

1. Update `FEATURE-STATE.md` with active/retired lineage, base/head, review rounds, clean streak, admission classes, scope proposals, recovery mode, checks, decisions, integration verdict, and residual risk.
2. Delete transient `PLAN.md` only after its section is accepted, replaced, split, or explicitly abandoned and durable artifacts exist.
3. Move `PLAN-FULL.md` to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md` after final reporting.
4. Keep contracts, handoffs, raw reviews, admission records, scope changes, and hard-cap evidence unless repository policy says otherwise.
5. Report in Chinese by default: feature result, section lineage/status, admitted defects repaired, rejected scope expansions, hard-cap recoveries, checks, decisions, integration result, residual risk, and maintainability judgment.

## Non-negotiable rules

- One implementer owns one extracted section/descendant at a time.
- Feature, assurance, and section boundaries are frozen before implementation.
- Review candidates do not become requirements until the main-agent admission gate accepts them.
- Review finds defects; it does not create a stronger threat model, environment, compatibility promise, durability guarantee, or generalized product.
- Real in-scope defects requiring cross-section repair are `IN_SCOPE_REPLAN`, not rejected scope creep.
- Every counting review uses a fresh reviewer context and a minimal packet.
- Two consecutive clean admitted full section reviews are required for provisional section acceptance.
- Five completed full review rounds is a hard cap; there is no soft cap and no round 6.
- Hard-cap recovery backs up the failed tip and automatically invokes `@sol_max` without continuation approval; recursive `SPLIT` stops at depth `3`, after which recovery must `REBOUND` or `SIMPLIFY_REPLACE` instead of deepening the lineage.
- Recovery uses admitted findings as requirements and keeps rejected proposals non-authoritative.
- Scope-drift recovery simplifies/replaces; it does not recursively preserve the inflated design.
- Retry starts from the failed parent's original base, not its repeatedly repaired code.
- Section acceptance cannot replace the final integration and merge-readiness gate.
