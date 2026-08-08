# Section Handoff：<Sxx — Title>

## Baseline

- Section / lineage: `<Sxx / parent -> child>`
- Replan generation: `<0+>`
- Section base: `<commit or fingerprint>`
- Current head: `<commit or fingerprint>`
- Contract / plan fingerprint: `<paths and hashes>`
- Assurance envelope revision: `<vN>`
- Commit(s): `<ids or N/A>`
- Handoff type: `IMPLEMENTATION | REPAIR | REIMPLEMENTATION`

## Behavior Implemented

- <acceptance criterion -> implementation evidence>

## Changed Scope and Actual Impact Cone

| File/symbol/workflow | Change | Requirement anchor | Why inside frozen boundary |
|---|---|---|---|
| `<path>` | <...> | `Sxx-AC-xx / INV-xx` | <...> |

- Direct callers/consumers/contracts inspected: <...>
- Expected-but-unchanged scope: <...>

## Complexity Receipt

| Mechanism introduced/retained | Requirement anchor | Simpler alternative | Why insufficient | Removal/rollback condition |
|---|---|---|---|---|
| `<item or none>` | <...> | <...> | <...> | <...> |

- Unplanned abstractions/settings/services/registries: `none | list + replan artifact`
- New assurance guarantees or threat actors: `none | SC-xxx`

## Decisions and Assumptions

| Item | Decision/assumption | Authority/evidence |
|---|---|---|
| <...> | <...> | <...> |

## Verification Evidence

| Command/evidence | Result | Criterion/finding |
|---|---|---|
| `<command>` | pass/fail/blocked | Sxx-AC-01 |

## Repair Record

| Finding ID | Admission class | Repair summary | Files | Check |
|---|---|---|---|---|
| REV-xxx | IN_SCOPE_REPAIR | <...> | `<...>` | `<...>` |

## Scope Proposals and Rejected Generalizations

| ID/raw candidate | Proposal | Status | Why non-authoritative/current action |
|---|---|---|---|
| — | — | — | — |

## Known Limitations and Deferred Work

- <item -> named owner section or explicit blocker>

## Reviewer Note

This handoff is a claim. Independently inspect the repository and raw diff; do not treat its design rationale as authority to expand scope.
