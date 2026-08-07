# Integration and Convergence Guide

Use this guide to distinguish local section acceptance from feature readiness, to run efficient integration gates, and to diagnose review loops that keep producing new issues.

## Contents

1. [Three review modes](#1-three-review-modes)
2. [Section acceptance gate](#2-section-acceptance-gate)
3. [Integration checkpoint design](#3-integration-checkpoint-design)
4. [Final integration review checklist](#4-final-integration-review-checklist)
5. [Reset triggers](#5-reset-triggers)
6. [Repair budgets](#6-repair-budgets)
7. [Diagnosing non-convergence](#7-diagnosing-non-convergence)
8. [Human oversight points](#8-human-oversight-points)
9. [Final readiness gate](#9-final-readiness-gate)

## 1. Three review modes

### SECTION

Purpose: determine whether one frozen section is internally correct, satisfies its contract, and preserves declared feature-level invariants.

Scope:

- Exact `section_base..section_head` range.
- Direct semantic impact cone.
- Relevant predecessor contracts.
- Current section tests and runtime evidence.

Verdict:

- `section-accepted`
- `section-blocked`
- `insufficient-evidence`

A section verdict never states whole-feature merge readiness.

### DELTA

Purpose: verify frozen finding closure and defects introduced by one repair wave.

Scope:

- Exact repair patch.
- Previously reviewed conclusions invalidated by the patch.
- Callers, contracts, tests, state, permissions, operations, and other edges in the repair impact cone.

DELTA review is the normal iteration primitive. It must not become a disguised whole-section rescan.

### INTEGRATION

Purpose: determine whether all accepted sections compose into the promised feature and whether the branch is ready to merge.

Scope:

- Full feature range for orientation.
- Requirement coverage and end-to-end behavior.
- Cross-section contracts and emergent interactions.
- Migration, rollout, rollback, operations, and cleanup.
- Final deterministic evidence.

The integration reviewer should not mechanically replay all low-risk local line review. It should target what section reviews could not prove in isolation.

## 2. Section acceptance gate

Accept a section only when all are true:

- Contract and base/head are stable and recorded.
- No unresolved `Must Fix` or unaccepted `Should Fix` remains.
- Any `Needs Decision` that affects safe behavior is resolved and written into the contract or feature state.
- Mandatory section risk lenses are reviewed or an evidence gap is explicit.
- Required targeted checks pass, or an external blocker and residual risk are explicit.
- Every repair finding has code-visible closure evidence and independent verification.
- Deferred work is assigned to a named later section rather than implied.
- The resulting repository state remains valid for users and developers.

Do not require a second empty full review. Once the section's coverage is complete and no open material finding remains, another stochastic rescan adds cost without a defined evidence target.

## 3. Integration checkpoint design

A checkpoint is smaller than final integration review and larger than a section review. It proves one dependency cluster.

Examples:

- New API producer + first real consumer.
- Schema expansion + dual-read/write behavior.
- Permission policy + UI/API enforcement.
- Background job producer + worker + retry/dead-letter behavior.
- Feature flag + old/new path parity.
- Parallel branches after combination.

Checkpoint packet:

```text
- Combined base/head
- Sections included
- Cross-section contracts under test
- Representative happy, negative, and partial-failure paths
- Commands and runtime evidence
- Rollback or disable path
- Known sections not yet included
```

Checkpoint outcome:

- `checkpoint-passed`
- `checkpoint-blocked`
- `checkpoint-insufficient-evidence`

A failed checkpoint may reopen an accepted section if its declared contract was wrong or incompletely implemented. Preserve the original review history and record why evidence was invalidated.

## 4. Final integration review checklist

### Original intent

- Does current behavior satisfy the original outcome rather than a later agent-generated reinterpretation?
- Are non-goals still respected?
- Is every requirement mapped to implementation and evidence?

### Cross-section contracts

- API request/response and error semantics.
- Schema versions, defaults, nullability, and migration order.
- State ownership, lifecycle, and invalid transitions.
- Authorization context and tenant/user scope propagation.
- Event ordering, retries, deduplication, and idempotency.
- Time, money, units, locale, and precision boundaries.
- Feature-flag state and legacy/new behavior parity.
- Cache invalidation and eventual-consistency assumptions.

### End-to-end paths

For each critical path, trace:

1. Entry condition.
2. Validation and authorization.
3. State mutation and side effects.
4. Partial failure and recovery.
5. User/operator-visible outcome.
6. Observability and audit evidence.
7. Rollback or disable behavior.

Include at least one negative path and one partial-failure path for each high-risk workflow.

### Release and migration

- Is every intermediate deployment state valid?
- Can old and new versions coexist where rollout requires it?
- Are migrations reversible, restartable, or otherwise safely bounded?
- Are backfills observable and idempotent?
- Is the contraction/removal criterion proven?
- Are feature flags owned and scheduled for removal?
- Is rollback possible after data or schema changes?

### Operations and non-functional behavior

- Logs, metrics, traces, audit records, and alert signals.
- Performance and cost under expected and boundary load.
- Resource cleanup, timeout, cancellation, and retry behavior.
- Security, privacy, secret handling, and abuse paths.
- Accessibility and complete UI states where applicable.
- Documentation, runbooks, configuration, and support workflows.

### Branch integrity

- Only feature-related changes are present.
- Generated artifacts are reproducible.
- Temporary scaffolding, debug code, and obsolete paths are removed or tracked.
- Tests have not been weakened to force a pass.
- Section commits and review evidence correspond to the actual head.

## 5. Reset triggers

Reset to a new full review baseline when any of these materially changes after full discovery:

- Public API or serialized contract.
- Database schema, migration order, or data ownership.
- Authentication, authorization, tenancy, or privacy semantics.
- Concurrency, ordering, retry, idempotency, or destructive behavior.
- Architecture, state owner, or dependency direction.
- Deployment, rollout, rollback, or feature-flag semantics.
- Section goal or acceptance criteria.
- Scope expands beyond the frozen contract.
- Base/head changes outside the tracked repair or integration operation.
- Review ledger, diff fingerprint, or evidence no longer matches the repository.
- A new systemic root-cause class invalidates broad prior conclusions.

Record the reset reason and which evidence is invalidated. A reset is not a failure; an unrecorded moving baseline is.

## 6. Repair budgets

Default per section and final integration gate:

- Soft cap: 3 repair waves.
- Hard cap: 5 repair waves.
- One repair wave should address the smallest coherent set of frozen root causes.
- A round counts as progress only when it closes a finding, proves a candidate false, adds a new evidence-backed root cause, or closes a coverage gap.

At the hard cap, block and diagnose. Do not ask only “continue?”

## 7. Diagnosing non-convergence

### New unrelated issues appear each full review

Likely causes:

- The review is repeatedly sampling an oversized scope.
- Coverage is not recorded, so reviewers revisit arbitrary areas.
- The baseline moves between rounds.
- Reviewer outputs contain low-signal or preference comments.

Response:

- Stop full rescans.
- Freeze one baseline and coverage ledger.
- Split the section if its impact cone remains feature-sized.
- Reclassify non-blocking polish.
- Use DELTA verification after repair.

### Repairs expose new defects in adjacent code

Likely causes:

- The original finding was a symptom, not the root cause.
- The repair changed a contract or state owner.
- The impact cone was under-mapped.

Response:

- Re-root-cause and deduplicate.
- Expand the impact cone once.
- Trigger a reset if semantics materially changed.
- Add an invariant or regression oracle before another repair.

### Fixes oscillate between two behaviors

Likely causes:

- Product semantics or compatibility policy is undefined.
- Two tests encode conflicting expectations.
- Multiple state owners exist.

Response:

- Stop and request a bounded decision.
- Identify the authoritative source.
- Consolidate ownership or update the feature contract.
- Do not let another agent choose implicitly.

### Reviewers approve superficial behavior but nested bugs remain

Likely causes:

- Acceptance criteria describe outputs but not interaction depth.
- Evaluator runs only happy paths.
- Runtime environment or fixtures are too weak.

Response:

- Add concrete test steps and hard thresholds.
- Trace negative and partial-failure paths.
- Use real UI/API/database state where practical.
- Add deterministic checks rather than more generic reviewers.

### Section passes locally but integration fails

Likely causes:

- Producer/consumer contracts were only assumed.
- Parallel agents invented incompatible semantics.
- Intermediate checkpoints were missing.
- Feature-level invariants were not included in section packets.

Response:

- Create or repair an explicit cross-section contract.
- Add a checkpoint before further sections.
- Reopen affected sections with recorded invalidated evidence.
- Reduce parallelism around the shared owner.

### Agent repeatedly broadens the change

Likely causes:

- Contract or non-goals are weak.
- The section is not independently implementable.
- The repository lacks a reusable entry point or clear boundary.

Response:

- Replan and narrow.
- Add an enabling refactor only if it creates the missing seam.
- Pass only the current section and global invariants.
- Reject unrelated cleanup.

### Tests pass but semantics remain uncertain

Likely causes:

- Tests reproduce the implementation rather than the requirement.
- Missing business decision.
- No external or end-to-end oracle.

Response:

- Mark `Needs Decision` or `insufficient-evidence`.
- Add behavior-level acceptance criteria.
- Do not increase review count as a substitute for an oracle.

## 8. Human oversight points

Human judgment has highest leverage at:

- Feature goal and non-goals.
- Architecture/state ownership when multiple valid choices exist.
- Compatibility and migration policy.
- Acceptable security, operational, and rollout risk.
- Plan gate for high-risk work.
- Final feature behavior and release decision.

Routine implementation, mechanical checks, bounded repairs, and evidence collection can be delegated more aggressively once those decisions are frozen.

## 9. Final readiness gate

Declare `mergeable` only when:

- All sections are accepted against their actual integrated heads.
- All planned checkpoints pass.
- No unresolved deferred item is required for the feature contract.
- Final integration review has no unresolved blocking finding.
- Full-feature deterministic checks pass or accepted blockers are explicit.
- Rollout, rollback, migration, flag lifecycle, and observability are ready.
- Residual risk is bounded and owned.

Otherwise declare `not-mergeable` or `insufficient-evidence`; do not soften the wording to imply completion.
