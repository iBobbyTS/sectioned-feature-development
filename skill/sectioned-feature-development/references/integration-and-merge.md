# Integration and Merge Guide

Use this reference to move accepted sections into an integrated, reviewable, and safely mergeable feature without reopening local scope or treating section commits as final authorization.

## Contents

1. [Three levels of readiness](#1-three-levels-of-readiness)
2. [Incremental integration](#2-incremental-integration)
3. [Compatibility patterns](#3-compatibility-patterns)
4. [Integration review](#4-integration-review)
5. [Merge-readiness gate](#5-merge-readiness-gate)
6. [Merge execution](#6-merge-execution)
7. [Rollback and cleanup](#7-rollback-and-cleanup)

## 1. Three levels of readiness

### Section accepted

Two consecutive clean admitted full reviews plus required local evidence. Provisional only.

### Feature mergeable

All active leaves compose on the actual feature head, cross-section contracts pass, required deferred work is closed, final integration admission has no material blockers, and combined checks pass.

### Merge authorized

User/project governance separately authorizes push, PR creation, and/or merge. Technical readiness never implies this authority.

## 2. Incremental integration

Run checkpoints when a contract becomes consumable:

- schema/API/event version;
- permission or state owner;
- queue/background-job path;
- migration stage;
- feature flag/rollout path;
- combined dependency cluster.

At a checkpoint, verify composition and representative end-to-end paths. Do not replay all local implementation. Accepted local evidence is invalidated only by a concrete combined behavior that disproves its contract assumptions.

For stacked sections:

- record predecessor head for every leaf;
- keep each commit/build state valid;
- update dependent branches when predecessor semantics change;
- review the actual combined head before final readiness;
- avoid hiding cross-section changes in conflict resolution.

## 3. Compatibility patterns

### Expand–migrate–contract

Merge compatible expansion first, then consumers/data, then removal after evidence. Each stage should have its own rollback and monitoring signal.

### Branch by abstraction

Keep old/new implementations behind a stable semantic seam, migrate gradually, then remove temporary code. Do not retain the abstraction if it no longer provides value.

### Feature flags

Use only when deployment/exposure or rollback needs it. Test relevant states, name owner and expiry, and remove after rollout. A flag itself creates operational and maintenance obligations.

### Schema/data migrations

Prefer backward-compatible deploy order. Separate schema expansion, dual read/write or backfill, cutover, and contraction when risk requires it. Define restart/idempotency and recovery evidence.

## 4. Integration review

Use one fresh `$code-review` `INTEGRATION` review plus main-agent admission. Focus on emergent properties:

- original outcome/non-goals/coverage;
- producer-consumer contracts;
- ordering, partial failure, retry, and idempotency;
- combined authorization and state ownership;
- migration/compatibility/flag lifecycle;
- rollout, rollback, observability, performance, security, privacy, and operations inside the frozen assurance envelope;
- branch-scope integrity and current combined tests.

The reviewer must show a reachable cross-section trigger. “Review security again” is too broad. The admission taxonomy remains the same; new threat actors or environments are scope proposals.

An admitted integration defect may require a bounded cross-section repair. Rerun only invalidated integration evidence plus required combined checks; do not mechanically reset all section reviews.

## 5. Merge-readiness gate

Before reporting `mergeable`, verify:

### Scope and contract

- feature head contains only approved feature/recovery changes;
- all requirements map to final evidence;
- non-goals and assurance exclusions have not drifted;
- all approved scope changes are incorporated and versioned;
- no raw reviewer proposal was implemented without authority.

### Code and architecture

- ownership/dependency directions are coherent;
- temporary compatibility paths have owners and exit criteria;
- complexity receipts match current mechanisms;
- debug/scaffolding/dead failed-attempt code is absent;
- generated artifacts are reproducible.

### Validation

- targeted section tests and full combined suite pass on latest head;
- migration/recovery/flag states are tested as applicable;
- required static/type/lint/security checks pass;
- evidence corresponds to latest commit, not an earlier head;
- unavailable checks are explicit and justify `insufficient-evidence` when material.

### Operations

- rollout and rollback commands/owners are clear;
- metrics/logs/alerts cover the risk-bearing path;
- flags/migrations/temporary seams have cleanup plans;
- documentation/config/support workflow is updated when required.

Report:

- `mergeable`: all required gates satisfied;
- `not-mergeable`: an admitted blocker remains;
- `insufficient-evidence`: correctness may be plausible but a required oracle/check is unavailable.

## 6. Merge execution

When separately authorized:

1. update to latest protected target or use repository merge queue;
2. run/check required validation against the actual merge candidate/merge group;
3. preserve logical commit structure or squash according to repository policy;
4. verify approvals/CODEOWNERS/branch protections;
5. merge via the repository-approved mechanism;
6. confirm resulting target head and CI status;
7. avoid bypassing protections unless explicitly authorized for an emergency.

On busy branches, a merge queue can validate the change with the latest target and queued changes. A previously green feature branch is not sufficient evidence if the merge candidate differs.

## 7. Rollback and cleanup

Rollback must match the change type:

- ordinary code: revert coherent section/feature commit;
- flagged behavior: disable first, then repair/revert;
- compatible migration: stop/cut traffic and use defined reverse/forward recovery;
- destructive schema/data change: use rehearsed backup/restore or forward fix;
- branch-by-abstraction: switch authority back while both implementations remain valid.

After rollout:

- close observability window;
- remove expired flags/seams/dual paths;
- archive plan/state/review evidence;
- capture follow-up debt separately rather than reopening the completed feature;
- delete backup branches only under repository/user policy, not automatically.
