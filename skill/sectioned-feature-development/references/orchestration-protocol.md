# Orchestration Protocol

Use this protocol when an orchestrator delegates section planning, implementation, code review, repair, and final verification to separate agent contexts.

## Contents

1. [Roles](#1-roles)
2. [Context packets](#2-context-packets)
3. [Profile routing](#3-profile-routing)
4. [Orchestration algorithm](#4-orchestration-algorithm)
5. [Section lifecycle](#5-section-lifecycle)
6. [Commit discipline](#6-commit-discipline)
7. [Worktrees and parallel agents](#7-worktrees-and-parallel-agents)
8. [Decision handling](#8-decision-handling)
9. [State integrity](#9-state-integrity)

## 1. Roles

### Orchestrator

Owns the feature contract, state machine, artifact integrity, dependency graph, authorization, and stop decisions. It must not treat subagent prose as evidence without inspecting the resulting repository state and recorded checks.

### Plan reviewer

Challenges the full plan before implementation when risk or ambiguity warrants it. It checks section boundaries, dependencies, global invariants, validation oracles, compatibility, rollout, rollback, and missing integration gates. It does not implement.

### Section implementer

Receives one frozen section contract and the minimum feature context needed to preserve global invariants. It implements, tests, records evidence, and stops. It does not broaden scope or declare the feature mergeable.

### Section discovery reviewer

Receives a clean context and performs one full `SECTION` review against a stable section base/head. It creates evidence-backed findings and coverage records. It does not repair during discovery.

### Repair agent

Receives only frozen, authorized finding IDs, acceptance criteria, section contract, and exact repair base. It makes the smallest coherent repair and records checks. It cannot close its own findings.

### Delta verifier

Reviews only the repair patch and invalidated impact cone. It verifies finding closure and new defects introduced by the repair. It does not rescan the stable section without a reset trigger.

### Integration reviewer

Receives the feature base/head, original feature contract, section summary, cross-section contracts, deferred-work ledger, and final evidence. It reviews feature-level behavior and interactions rather than replaying every local line review.

### Decision owner

The user or accountable maintainer who resolves business semantics, compatibility policy, accepted risk, migration behavior, rollout decisions, and other non-inferable choices.

## 2. Context packets

Keep packets explicit and small enough to remain salient.

### Implementer packet

```text
- Working path
- Repository instructions and relevant architecture sources
- Feature goal, non-goals, and global invariants
- Current section ID and frozen contract path
- Exact section base
- Required checks and evidence paths
- Commit authorization and profile routing
- Explicit instruction not to modify future sections
```

Do not include the entire previous review transcript. Include only accepted decisions that changed authoritative artifacts.

### Independent section-review packet

```text
Review mode: SECTION
Working path: {path}
Section: {ID}
Range: {section_base}..{section_head}
Feature contract: .agent-work/PLAN-FULL.md
Section contract: .agent-work/sections/{ID}-CONTRACT.md
Handoff: .agent-work/sections/{ID}-HANDOFF.md
Output: .agent-work/reviews/{ID}-SECTION-r01.md
Use: $code-review
```

Do not seed suspected findings or previous persuasive conclusions into the first discovery reviewer.

### Repair packet

```text
Working path: {path}
Section: {ID}
Repair base: {reviewed_head}
Authorized findings: {IDs}
Frozen finding ledger: {review_file_or_ledger}
Frozen acceptance criteria: {criteria}
Section contract: {contract_path}
Required checks: {commands}
Output handoff: {handoff_path}
Do not fix unlisted findings or broaden scope.
```

### Delta-verification packet

```text
Review mode: DELTA
Working path: {path}
Section: {ID}
Repair range: {repair_base}..{repair_head}
Frozen findings: {IDs and ledger path}
Review only the repair delta, invalidated impact cone, and reopened conclusions.
Output: .agent-work/reviews/{ID}-DELTA-rNN.md
Use: $code-review
```

### Integration-review packet

```text
Review mode: INTEGRATION
Working path: {path}
Feature range: {feature_base}..{feature_head}
Feature contract and requirement matrix: .agent-work/PLAN-FULL.md
Feature state: .agent-work/FEATURE-STATE.md
Section contracts/handoffs: .agent-work/sections/
Prior review index: .agent-work/reviews/
Focus: cross-section contracts, end-to-end behavior, deferred work, migration,
rollout/rollback, security, reliability, operations, and full acceptance.
Output: .agent-work/reviews/FEATURE-INTEGRATION-r01.md
Use: $code-review
```

The integration reviewer may read prior ledgers after forming an independent view of the current feature state. Do not preload prior rationalizations as the framing.

## 3. Profile routing

Use project-configured profile names. If the governing instructions define the following aliases, route by default as follows:

- Ordinary section implementation: `sol-medium`.
- High-risk implementation or plan repair: `sol_high`.
- Independent section and integration discovery review: clean `sol_xhigh`.
- Authorized repair: `sol_high`.
- Delta verification: `sol_xhigh` or another independent high-reasoning reviewer.

Escalate based on semantic risk, not line count. Do not spend the highest profile on mechanical extraction or formatting.

## 4. Orchestration algorithm

```text
mode = resolve_authority()
state = initialize_feature_state()
feature_base = freeze_feature_base()
plan = write_and_validate_full_plan()

if plan_requires_review(plan):
    plan_review = clean_plan_review(plan)
    resolve_plan_findings_or_block()

for section in dependency_order(plan):
    ensure_predecessors_accepted(section)
    section_base = current_integrated_head()
    extract_plan(section)
    freeze_contract(section, section_base)

    implementation = run_implementer(section)
    inspect_handoff_and_repository(implementation)
    run_required_local_checks(section)
    commit_if_authorized(section)
    section_head = current_head()

    review = clean_section_review(section_base, section_head)
    repair_waves = 0

    while review.has_blocking_findings():
        if review.needs_decision():
            record_blocker_and_stop()

        if repair_waves >= 5:
            diagnose_convergence_failure_and_stop()

        findings = freeze_smallest_coherent_fixable_wave(review)
        repair_base = current_head()
        run_repair_agent(findings)
        inspect_repair_and_checks()
        commit_if_authorized(findings)
        repair_head = current_head()
        repair_waves += 1

        if reset_triggered(repair_base, repair_head, section.contract):
            record_reset_reason()
            section_base = rebaseline_section_preserving_history()
            review = clean_section_review(section_base, current_head())
        else:
            review = delta_verify(repair_base, repair_head, findings)

    accept_section_provisionally()
    update_feature_state()
    remove_transient_plan_after_durable_record()

    if integration_checkpoint_triggered(section):
        run_targeted_integration_checkpoint()
        resolve_checkpoint_failure_or_reset()

ensure_all_sections_accepted_and_deferred_items_resolved()
integration_review = clean_feature_integration_review(feature_base, current_head())
repair_integration_findings_with_same_delta_protocol()
run_full_feature_validation()
archive_plan_and_report()
```

## 5. Section lifecycle

Use these states in `FEATURE-STATE.md`:

```text
PLANNED
READY
CONTRACT_FROZEN
IMPLEMENTING
LOCAL_VALIDATION
SECTION_REVIEW
DECISION_BLOCKED
REPAIRING
DELTA_VERIFY
SECTION_ACCEPTED
INTEGRATION_BLOCKED
SUPERSEDED
ABANDONED
```

Allowed primary transitions:

```text
PLANNED -> READY
READY -> CONTRACT_FROZEN
CONTRACT_FROZEN -> IMPLEMENTING
IMPLEMENTING -> LOCAL_VALIDATION
LOCAL_VALIDATION -> SECTION_REVIEW
SECTION_REVIEW -> SECTION_ACCEPTED | DECISION_BLOCKED | REPAIRING
REPAIRING -> DELTA_VERIFY
DELTA_VERIFY -> SECTION_ACCEPTED | DECISION_BLOCKED | REPAIRING | SECTION_REVIEW(reset)
SECTION_ACCEPTED -> INTEGRATION_BLOCKED when a checkpoint disproves compatibility
```

A section may become `SUPERSEDED` only through an explicit replan that records replacement sections and preserves history.

## 6. Commit discipline

When commits are authorized:

- One implementation commit per coherent section is the default.
- Add one repair commit per coherent repair wave.
- Include the section ID in the subject, for example:

```text
feat(upload): S03 add idempotent chunk recovery
fix(upload): S03 close REV-004 and REV-006
```

- Keep generated changes, formatting-only churn, and unrelated cleanup out unless inseparable and documented.
- Do not amend or squash during the workflow unless explicitly requested; stable commit boundaries are review evidence.
- Do not commit a failed section merely to make progress. If a checkpoint commit is needed for recovery, label it clearly and do not mark the section accepted.

When commits are not authorized, record content fingerprints or exact working-tree diff commands in `FEATURE-STATE.md` so the review range remains reproducible.

## 7. Worktrees and parallel agents

Use a separate worktree per parallel section. Record:

- Worktree path.
- Branch.
- Common accepted base.
- Section ID.
- Files/owners expected to change.
- Integration order.
- Integration checkpoint.

Do not run parallel sections when both touch:

- The same database migration sequence.
- The same public API or shared type contract.
- The same authorization policy.
- The same state machine or coordinator.
- The same generated source of truth.
- The same release flag semantics.

After integrating a parallel section, review the actual merge or cherry-pick delta and run the planned checkpoint. A section reviewed only in isolation is not evidence that the combined head is correct.

## 8. Decision handling

A `Needs Decision` record must contain:

- The exact ambiguity.
- Why code or repository evidence cannot resolve it.
- Affected section and feature criteria.
- Safe options with tradeoffs.
- Default behavior only when an authoritative policy already establishes one.
- Work that can continue without prejudging the decision.

Do not ask broad questions such as “How should this work?” Ask the smallest bounded decision that unblocks a safe implementation.

## 9. State integrity

At every transition, update `FEATURE-STATE.md` before handing work to a new agent context.

Record:

- Feature and section base/head.
- Current state and next action.
- Accepted decisions and source.
- Open findings and review file.
- Checks run and exact result.
- Deferred items and owner section.
- Reset reason and invalidated evidence.
- Residual risk.

If chat history and the artifact disagree, stop and reconcile against repository reality. Do not silently choose the more convenient version.
