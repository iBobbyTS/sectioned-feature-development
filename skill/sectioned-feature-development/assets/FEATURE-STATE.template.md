# Feature State：<Feature Name>

## 1. Current State

- Mode: `PLAN_ONLY | EXECUTE_NO_COMMIT | EXECUTE_WITH_COMMITS`
- Working path: `<path>`
- Feature branch/worktree: `<branch/path or N/A>`
- Feature base: `<commit>`
- Current head: `<commit or diff fingerprint>`
- Current state: `<state>`
- Active section: `<Sxx or none>`
- Next action: `<exact next gate>`
- Last updated: `<timestamp>`

## 2. Feature Contract Summary

- Goal: <...>
- Non-goals: <...>
- Global invariants: `INV-01`, `INV-02`
- Plan: `.agent-work/PLAN-FULL.md`

## 3. Section Status

| ID | State | Base | Head | Contract | Handoff | Review verdict/file | Repair waves |
|---|---|---|---|---|---|---|---:|
| S01 | PLANNED | — | — | — | — | — | 0 |

## 4. Requirement Coverage

| Requirement | Section evidence | Integration evidence | Status |
|---|---|---|---|
| R-01 | — | — | planned |

## 5. Open Findings

| Finding | Severity/class | Section/gate | Frozen acceptance | Review file | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | none |

## 6. Decisions

| ID | Decision | Authority/source | Affected scope | Status |
|---|---|---|---|---|
| D-01 | <...> | <...> | Sxx | accepted/open |

## 7. Checks and Evidence

| Time | Scope | Command/evidence | Result | Artifact |
|---|---|---|---|---|
| <...> | S01 | `<command>` | pass/fail/blocked | `<path>` |

## 8. Integration Checkpoints

| ID | Included sections/head | Contracts/paths | Result | Evidence |
|---|---|---|---|---|
| CP1 | — | — | planned | — |

## 9. Reset Events

| ID | Time | Trigger | Old baseline | New baseline | Evidence invalidated |
|---|---|---|---|---|---|
| — | — | — | — | — | none |

## 10. Deferred Work and Residual Risk

| ID | Item/risk | Required before merge? | Owner | Status/acceptance |
|---|---|---|---|---|
| — | — | — | — | none |
