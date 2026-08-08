# Feature State：<Feature Name>

## Current State

- Mode: `PLAN_ONLY | EXECUTE_NO_COMMIT | EXECUTE_WITH_COMMITS`
- Working path: `<path>`
- Active branch/worktree: `<branch/path or N/A>`
- Feature base: `<commit>`
- Current head: `<commit or diff fingerprint>`
- Current state: `<state>`
- Active section: `<Sxx / Sxx.n or none>`
- Parent lineage: `<none or Sxx -> Sxx.n>`
- Replan generation: `<0+>`
- Valid review rounds: `<0..5>`
- Review attempts: `<0+>`
- Clean streak: `<0..2>`
- Contract revision / plan fingerprint: `<...>`
- Assurance envelope revision: `<vN>`
- Next action: `<exact gate>`
- Last updated: `<timestamp>`

## Feature Contract Summary

- Goal: <...>
- Non-goals: <...>
- Global invariants: `INV-01`, `INV-02`
- Assurance exclusions: <...>
- Plan: `.agent-work/PLAN-FULL.md`

## Section Status and Lineage

| ID | Parent | State | Base | Head | Completed rounds | Clean streak | Replan gen | Contract | Handoff |
|---|---|---|---|---|---:|---:|---:|---|---|
| S01 | — | PLANNED | — | — | 0 | 0 | 0 | — | — |

Valid states: `PLANNED`, `CONTRACT_FROZEN`, `IMPLEMENTED`, `UNDER_REVIEW`, `REPAIRING`, `IN_SCOPE_REPLAN`, `SECTION_ACCEPTED`, `REPLACED_AFTER_HARD_CAP`, `SPLIT_AFTER_HARD_CAP`, `BLOCKED`.

## Requirement Coverage

| Requirement | Active section evidence | Integration evidence | Status |
|---|---|---|---|
| R-01 | — | — | planned |

## Review Admission Ledger

| Section/round | Raw review | Admission record | Valid? | Material admitted IDs | Non-authoritative proposals | Result | Clean streak |
|---|---|---|---|---|---|---|---:|
| — | — | — | — | — | — | — | 0 |

## Scope-change Ledger

| ID | Type | Proposed guarantee/boundary | Source | Status | Owner | Approved revision |
|---|---|---|---|---|---|---|
| — | — | — | — | — | — | — |

## Complexity Ledger

| Section | Mechanism | Requirement anchor | Simpler alternative | Removal condition | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## Decisions

| ID | Decision | Authority/source | Affected scope | Status |
|---|---|---|---|---|
| D-01 | <...> | <...> | Sxx | accepted/open |

## Checks and Evidence

| Time | Scope | Command/evidence | Result | Artifact |
|---|---|---|---|---|
| <...> | S01 | `<command>` | pass/fail/blocked | `<path>` |

## Hard-Cap Recoveries

| Parent | Diagnosis | Mode | Generation | Original base | Failed tip | Backup branch | Replacement/descendants | Retry path |
|---|---|---|---:|---|---|---|---|---|
| — | — | — | — | — | — | — | — | — |

## Integration Checkpoints

| ID | Included active sections/head | Contracts/paths | Admission result | Evidence |
|---|---|---|---|---|
| CP1 | — | — | planned | — |

## Evidence Invalidation Events

| ID | Time | Trigger | Old baseline | New baseline | Evidence invalidated |
|---|---|---|---|---|---|
| — | — | — | — | — | none |

## Deferred Work and Residual Risk

| ID | Item/risk | Required before merge? | Owner | Status/acceptance |
|---|---|---|---|---|
| — | — | — | — | none |
