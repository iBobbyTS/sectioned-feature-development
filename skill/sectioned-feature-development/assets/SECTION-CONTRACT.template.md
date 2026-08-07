# Section Contract：<Sxx — Title>

## Identity and Baseline

- Feature: `<name>`
- Section: `<Sxx>`
- Contract revision: `1`
- Frozen at: `<timestamp>`
- Section base: `<commit or fingerprint>`
- Dependency heads: `<Syy=commit>`
- Plan fingerprint: `<sha256>`
- Implementer profile: `<profile>`
- Review profile: `<profile>`

## Goal

<one coherent outcome or enabling seam>

## Observable Behavior Increment

- <behavior>

## Scope and Semantic Boundaries

- Expected files/symbols/workflows: <...>
- Owners modified: <...>
- High-risk boundaries: <...>
- Explicitly permitted mechanical/generated changes: <...>

## Non-goals

- <...>

## Feature-level Invariants

- `INV-01`: <...>
- `INV-02`: <...>

## Section Acceptance Criteria

- `Sxx-AC-01`: <trigger, expected behavior, evidence>
- `Sxx-AC-02`: <negative or failure behavior>

## Verification

```bash
<command>
```

- Runtime/manual evidence: <...>
- Checks that may be unavailable and blocker policy: <...>

## Compatibility, Migration, Rollout, and Recovery

- Intermediate repository/runtime state: <valid because...>
- Compatibility/migration: <...>
- Feature flag/rollout: <...>
- Rollback/recovery: <...>
- Observability/audit: <...>

## Allowed Deferred Work

- <item -> named section; none if empty>

## Open Decisions

- `none` before implementation, otherwise block.

## Replan / Full-review Reset Triggers

- Acceptance criteria or behavior changes.
- Public contract/schema/permission/state owner/concurrency/destructive/rollout semantics change.
- Scope materially expands.
- Base/head changes outside tracked implementation or repair.
