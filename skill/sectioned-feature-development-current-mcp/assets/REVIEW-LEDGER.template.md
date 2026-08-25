# `<ID>` Review Ledger

## Scope and identities

- Feature ID:
- Section base:
- Current head:
- Contract:
- Original section lineage:
- Main/orchestrator task/session ID:
- Plan reviewer task/session ID:
- Implementer task/session ID:
- Repairer task/session ID(s):
- Initial/delta reviewer task/session ID:
- Final reviewer task/session ID:
- Role-separation check: `pass | fail | unknown`
- Sequence-barrier check: `pass | violation-recorded | unknown`
- Frozen reviewed product/test head:
- Allowed-to-edit owners/files/symbols/routes:
- Inspect-only dependency paths/direct impact cone:
- Explicitly excluded owners/mechanisms:
- Supported environment/non-goals:
- Cumulative repair waves used:
- Automatic recovery used:
- Review intensity:
- Review assurance requested/resolved:
- Assurance reasons/override:
- Exact product/test head covered by evidence:

## Initial bounded coverage

- Reviewer task/session ID and mode:
- Range:
- Changed files/symbols reviewed:
- Critical changed paths traced:
- Contracts/invariants reviewed:
- Risk lenses triggered:
- Checks/experiments:
- Explicit gaps:
- Causal inspection expansions beyond named cone:

## Findings

| ID | Class | Severity | Causality/path | Trigger | Authority / AC ID | Consequence | Allowed repair owner | Smallest bounded repair | Status |
|---|---|---|---|---|---|---|---|---|---|
| REV-001 | DIFF_CAUSED | Must Fix |  |  |  |  |  |  | open |

## Repair waves

### Wave 1

- Origin phase: `INITIAL_BOUNDED | REPAIR_DELTA | FINAL_BOUNDED | CHECKPOINT | INTEGRATION | RECOVERY`
- Finding IDs:
- Repairer task/session ID:
- Frozen repair owners:
- Repair range:
- Targeted checks:
- Delta reviewer task/session ID and result:
- Coverage invalidated/re-established:

## Clean A — closure evidence

- All admitted findings closed: `yes/no`
- Required targeted/section checks pass: `yes/no`
- Remaining evidence gaps:

## Final bounded review, when required

- Final reviewer task/session ID and mode:
- Reviewer is distinct from plan reviewer, writers, and initial/delta reviewer: `yes/no/unknown`
- Range / frozen head:
- Highest-risk changed path:
- Result: `clean | findings | insufficient-evidence`
- New admissible findings, if any:
- Scope/mechanism drift check:

## Clean evidence and acceptance

- Required evidence under `ONE | TWO`:
- Clean reviewer outcome(s) satisfied: `yes/no`
- Clean B satisfied, if required: `yes/no`
- Section status: `ACCEPTED | NOT_ACCEPTED | BLOCKED`
- Residual risk:

## Non-blocking notes

- PREEXISTING_OUT_OF_SCOPE:
- SCOPE_PROPOSAL:
- DEFERRED_OWNER:
- NIT_DEBT:
