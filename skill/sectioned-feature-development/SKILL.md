---
name: sectioned-feature-development
description: "Plan and execute large, risky, or multi-module software changes as reviewable sections with durable feature state, per-section contracts, isolated implementation and review, bounded repair deltas, integration checkpoints, and a final cross-section review. Use when a feature or refactor may exceed roughly 300 behavioral lines, touches more than three modules, crosses a high-risk semantic boundary, or repeatedly fails to converge under whole-change review."
---

# Sectioned Feature Development

Develop one large feature as a sequence of bounded, evidence-backed sections. Preserve a stable feature contract across sections, review each section once at full scope, verify repairs only through their delta and invalidated impact cone, and reserve merge readiness for a final cross-section integration gate.

## Boundary and authority

- Follow repository-local instructions before this skill.
- Use this skill for one feature, refactor, migration, or architectural transition. Do not use it as a periodic repository audit.
- Determine the requested mode before changing files:
  - `PLAN_ONLY`: research and write artifacts; do not create a branch, edit product code, or commit.
  - `EXECUTE_NO_COMMIT`: implement and validate, but leave commits to the user.
  - `EXECUTE_WITH_COMMITS`: create the authorized branch or worktree and make bounded section commits.
- A planning or review request does not authorize commits. Treat branch creation and commits as authorized only when the user or governing project instructions explicitly authorize them.
- Never push, merge, open a pull request, rewrite history, reset, clean, or delete user work unless separately authorized.
- Stop before implementation or repair when product semantics, compatibility policy, migration behavior, rollout risk, or another accountable decision is unresolved.

## Trigger

Use the workflow when any condition holds:

- Expected behavioral edits are roughly more than 300 lines.
- More than three modules, packages, services, pages, or workflows are affected.
- The change crosses persistence, schema, money, time, units, security, permissions, tenancy, routing, concurrency, background jobs, public API, deployment, or shared-state boundaries.
- The architecture or state owner changes.
- The impact cone is difficult to bound.
- A previous whole-change implementation or review loop failed to converge.

The line threshold is only a trigger. A 40-line authorization change may need this workflow; a large generated-file update may not.

## Required artifacts

Use these paths unless repository rules define an equivalent location:

```text
.agent-work/
├── PLAN-FULL.md                 # authoritative feature plan and section graph
├── PLAN.md                      # transient current-section execution packet
├── FEATURE-STATE.md             # durable state, decisions, coverage, and heads
├── sections/
│   ├── S01-CONTRACT.md
│   ├── S01-HANDOFF.md
│   └── ...
├── reviews/
│   ├── S01-SECTION-r01.md
│   ├── S01-DELTA-r02.md
│   ├── FEATURE-INTEGRATION-r01.md
│   └── ...
└── plans/
    └── {YYYYMMDD-HHMM}_FULL.md
```

Copy templates from `assets/` when creating these artifacts. Keep `PLAN-FULL.md` and `FEATURE-STATE.md` authoritative; chat history is not project state.

## Load references progressively

- Read [references/section-planning.md](references/section-planning.md) before dividing the feature.
- Read [references/orchestration-protocol.md](references/orchestration-protocol.md) before delegating implementation, review, or repair.
- Read [references/integration-and-convergence.md](references/integration-and-convergence.md) before accepting a section, diagnosing a loop, or starting the final integration gate.
- Read [references/artifact-schemas.md](references/artifact-schemas.md) when creating, validating, extracting, or archiving artifacts.

## State machine

```text
PREFLIGHT
  -> FEATURE_CONTRACT
  -> SECTION_PLAN
  -> PLAN_GATE
  -> SECTION_CONTRACT
  -> IMPLEMENT
  -> LOCAL_VALIDATE
  -> SECTION_REVIEW
  -> {DECISION_BLOCK | REPAIR -> DELTA_VERIFY | SECTION_ACCEPTED}
  -> INTEGRATION_CHECKPOINT when triggered
  -> next SECTION_CONTRACT
  -> FEATURE_INTEGRATION_REVIEW
  -> {DECISION_BLOCK | REPAIR -> DELTA_VERIFY | FINAL_VALIDATE}
  -> ARCHIVE_AND_REPORT
```

Do not advance merely because an agent says it is done. Advance only when the artifact and evidence gate for the state is satisfied.

## Phase 0: Preflight and feature contract

1. Inspect repository rules, architecture sources, current branch, `git status`, relevant recent commits, build/test entry points, and available validation environment.
2. Record the exact feature base commit. Do not plan against a moving or ambiguous base.
3. Use the repository's code-index or graph tool before broad text search when project instructions require it.
4. Write the feature contract in `PLAN-FULL.md`:
   - One-sentence outcome.
   - User-visible or operator-visible behavior.
   - Explicit non-goals.
   - Global invariants that every section must preserve.
   - Hard constraints and authoritative sources.
   - Full-feature acceptance criteria and verification commands.
   - Compatibility, migration, rollout, rollback, flag, and observability requirements.
5. Identify ownership and state boundaries before choosing files or abstractions.
6. If direct implementation would materially worsen a god object, ambiguous state owner, fragile state machine, circular dependency, duplicated semantic boundary, or under-tested core path, add the smallest enabling refactor with protective characterization tests. Do not hide speculative cleanup inside feature sections.
7. In `EXECUTE_WITH_COMMITS`, create a feature branch. Use isolated worktrees only for genuinely independent parallel sections.

## Phase 1: Divide the feature

Create `PLAN-FULL.md` before product-code implementation.

Prefer this order:

1. A walking-skeleton or contract-proving section when architecture or integration is uncertain.
2. Coherent vertical behavior slices that cross only the layers needed to deliver and verify one outcome.
3. Compatibility or migration sections using expand–migrate–contract or branch-by-abstraction where needed.
4. Cleanup or contraction only after all consumers have moved and evidence proves the old path is unused.

Every section must have a stable ID such as `S01` and include:

- Goal and observable behavior increment.
- Dependencies and predecessor head.
- Expected files, symbols, workflows, and semantic boundaries.
- Non-goals and explicitly deferred work.
- Global invariants touched.
- Acceptance criteria with an executable or inspectable oracle.
- Validation commands and evidence to retain.
- Compatibility, rollout, recovery, and cleanup implications.
- Size/risk estimate and split trigger.

A section is valid only if one implementer can complete it, one reviewer can understand it, and its behavior can be verified without relying on undocumented future work. Prefer vertical slices; allow horizontal enabling work only when it establishes a tested seam required by later slices.

Use `scripts/section_plan.py` to validate the plan and extract the active section when practical:

```bash
python {skill-dir}/scripts/section_plan.py validate .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py list .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py extract \
  .agent-work/PLAN-FULL.md S01 --output .agent-work/PLAN.md
```

## Phase 2: Plan gate

Before implementing `S01`, and after any material replan, verify:

- Every full-feature acceptance criterion maps to one or more sections and to a final integration check.
- Dependencies form an explicit acyclic graph.
- No section relies on an unstated schema, API, permission, state-ownership, or rollout decision.
- Each high-risk boundary has a single source of truth and a test oracle.
- Cross-section contracts and integration checkpoints are named.
- Refactors are separated from behavior changes unless inseparable and justified.
- Parallel sections do not modify the same owner, contract, migration, or state machine.
- The final section is not a vague “integrate everything” dump.

For a high-risk or ambiguous plan, use one clean plan reviewer before code. The reviewer challenges slicing, dependencies, invariants, testability, rollout, and rollback; it does not implement.

## Phase 3: Freeze the current section

For the next ready section:

1. Record `section_base` as the exact accepted predecessor head.
2. Extract the section into `.agent-work/PLAN.md`.
3. Create `.agent-work/sections/{ID}-CONTRACT.md` from the template.
4. Resolve or block every open contract question before code.
5. Update `FEATURE-STATE.md` to `CONTRACT_FROZEN` with the section ID, base, dependencies, risk, and expected verification.

The section contract is immutable during ordinary implementation. A material change to acceptance criteria, public contract, schema, state owner, authorization, concurrency, destructive behavior, or rollout semantics requires an explicit replan and review-baseline reset.

## Phase 4: Implement and locally validate

Delegate one current section, not the whole feature.

- Give the implementer repository rules, feature goal and global invariants, the current section contract, relevant architecture sources, and the exact base. Do not preload prior reviewers' persuasive narratives.
- Default to the configured medium implementation profile for ordinary sections. Escalate architecture, migration, security, concurrency, or other high-risk sections to the configured high profile.
- Require the smallest implementation that satisfies the frozen contract.
- Add or update meaningful tests. Cover behavior, edge cases, error paths, and regression risk; do not add execution-only assertions.
- Run the section's targeted checks before broad checks.
- Record changed files, decisions, commands, results, limitations, and current head in `{ID}-HANDOFF.md`.
- In `EXECUTE_WITH_COMMITS`, commit the coherent implementation with the section ID in the message. Keep unrelated cleanup out of the commit.

Do not start the next section while the current section has failed required validation, unresolved contract questions, or unreviewed code.

## Phase 5: Section review and bounded repair

Use a clean reviewer with `$code-review` in `SECTION` mode. The review range is exactly `section_base..section_head`, plus only the semantically necessary impact cone.

The review packet must include:

- Section ID, base, and head.
- Section contract and feature-level invariants.
- Dependency and deferred-work declarations.
- Implementation handoff and validation evidence.
- Review output path under `.agent-work/reviews/`.

Review rules:

1. Perform one broad `SECTION` discovery pass for the stable section baseline.
2. Classify findings as `Needs Decision`, `Agent-Fixable`, or `External Blocker`; freeze stable IDs and acceptance criteria.
3. Stop immediately when a human decision is required for a safe repair.
4. Send only authorized, frozen `Agent-Fixable` findings to a separate repair agent.
5. Commit one coherent repair wave when commits are authorized.
6. Re-review only the repair delta and invalidated impact cone in `DELTA` mode.
7. Run a new full section pass only when a reset trigger materially changes the baseline or semantics.

Do **not** require two consecutive empty whole-section reviews. Accept the section when there are no unresolved blocking findings, mandatory coverage is complete or explicitly bounded, required checks pass or blockers are recorded, and repair closure has code-visible evidence.

Use a normal soft cap of three repair waves and a hard cap of five. At the hard cap, block and diagnose the cause instead of running another generic review.

A section verdict is one of:

- `section-accepted`
- `section-blocked`
- `insufficient-evidence`

`section-accepted` is provisional. It does not mean the whole feature is mergeable.

## Phase 6: Integration checkpoints and parallel work

Run a targeted integration checkpoint when any of these occurs:

- A public contract, schema, permission model, state owner, queue, deployment path, or feature flag is introduced or changed.
- A dependency cluster is complete.
- Two previously independent branches are combined.
- The next section assumes behavior produced by multiple accepted sections.
- The plan explicitly marks a checkpoint.

At a checkpoint, verify cross-section contracts and representative end-to-end paths without reopening every accepted line.

Parallelize only sections that:

- Have all dependencies accepted.
- Do not write the same semantic owner or contract.
- Have isolated branches/worktrees and deterministic integration order.
- Can be validated independently.

After integration, rebase review evidence on the actual combined head. If the combination changes semantics outside declared contracts, trigger an integration reset.

## Phase 7: Final feature integration gate

After all sections are accepted and all deferred items are resolved or explicitly approved, use a clean reviewer with `$code-review` in `INTEGRATION` mode over `feature_base..feature_head`.

This is not another line-by-line replay of every section. It must challenge:

- Full-feature behavior against the original contract.
- Cross-section API, schema, state, permission, ordering, and error contracts.
- End-to-end critical paths and combined edge cases.
- Migration, compatibility, rollout, rollback, flag lifecycle, and cleanup.
- Observability, performance, security, privacy, operational readiness, and documentation.
- Requirement coverage, deferred-work closure, and branch-scope integrity.

Repair integration findings through the same frozen-finding and `DELTA` protocol. Reset only when semantics or the baseline materially change.

Then run the deterministic full-feature validation suite. State final readiness as:

- `mergeable`
- `not-mergeable`
- `insufficient-evidence`

## Phase 8: Archive and report

1. Update `FEATURE-STATE.md` with every section base/head, verdict, review file, checks, decisions, resets, and residual risk.
2. Delete transient `.agent-work/PLAN.md` only after its section is accepted or explicitly abandoned and its durable artifacts exist.
3. Move `.agent-work/PLAN-FULL.md` to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md` after final reporting. Use the helper script or an equivalent safe move.
4. Keep contracts, handoffs, and review evidence unless repository policy says otherwise.
5. Report in Chinese by default:
   - Feature outcome and final readiness.
   - Section table with heads and verdicts.
   - Findings repaired by stable ID.
   - Decisions and reset events.
   - Checks run and not run.
   - Residual risk, rollout/rollback status, and recommended follow-up.
   - Maintainability judgment covering ownership boundaries, complexity, tests, and cleanup.

## Non-negotiable convergence rules

- One stable baseline gets one full discovery pass; repairs get delta verification.
- A clean reviewer is not a substitute for a frozen contract and deterministic checks.
- A repair agent cannot close its own findings by explanation.
- New scope discovered during a section is added through an explicit replan, not silently absorbed.
- Section-local success cannot override a feature-level invariant.
- No next section while the current section is blocked.
- No feature-level merge verdict before the final integration gate.
- Repeated new findings after the hard cap are a process signal: re-specify, add an oracle, split the section, redesign the boundary, stabilize the base, or obtain a human decision.
