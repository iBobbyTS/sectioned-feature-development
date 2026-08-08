# Hard-Cap Recovery：<Section ID — Title>

## Failed Attempt

- Feature / parent lineage: `<...>`
- Replan generation: `<n>`
- Original section base: `<commit>`
- Failed tip: `<commit>`
- Backup branch: `codex/backup/<...>`
- Failed working path: `<path>`
- Contract / plan fingerprints: `<...>`
- Assurance envelope revision: `<vN>`
- Hard cap: `5 completed full SECTION reviews`
- Required acceptance: `2 consecutive CLEAN admissions`

## Five Completed Review Rounds

| Round | Reviewed head | Raw review | Admission | Material admitted findings | Non-authoritative proposals | Repair commit | Result |
|---:|---|---|---|---|---|---|---|
| 1 | `<sha>` | `<path>` | `<path>` | `<IDs/none>` | `<IDs/none>` | `<sha/—>` | `<...>` |
| 2 | `<sha>` | `<path>` | `<path>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 3 | `<sha>` | `<path>` | `<path>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 4 | `<sha>` | `<path>` | `<path>` | `<...>` | `<...>` | `<...>` | `<...>` |
| 5 | `<sha>` | `<path>` | `<path>` | `<...>` | `<...>` | `<...>` | `hard-cap` |

## Classified Nonconvergence

- Primary diagnosis: `DEFECT_DENSITY | ASSURANCE_BOUNDARY_DRIFT | ARCHITECTURE_BOUNDARY_FAILURE | CONTRACT_AMBIGUITY | EVIDENCE_FAILURE`
- Evidence from admitted findings: <...>
- Raw proposals explicitly excluded from requirements: <...>
- Recurrent root causes: <...>
- Contract/oracle defects: <...>
- Complexity inflation inventory: <mechanisms added without durable requirement anchors>

## Recovery Mode

- Mode: `SPLIT | SIMPLIFY_REPLACE | REBOUND | OWNER_DECISION | REPAIR_EVIDENCE`
- Why this mode follows from the diagnosis: <...>
- Failed product-code commits to carry forward: `none by default`
- Frozen predecessors/user-owned semantics: <...>

## @sol_max Request

Use only admitted findings as required recovery evidence. Put rejected scope proposals in a separate non-authoritative appendix. Modify only this section lineage and affected dependency/coverage edges. Do not implement product code or promote a proposal into a requirement.

For `SIMPLIFY_REPLACE`, explicitly delete/avoid unapproved mechanisms and replace the inflated section with the smallest proportional leaf set; one replacement leaf is allowed.

## Replacement / Descendants

| ID | Goal | Depends on | Independent oracle | Complexity reduction | Review-risk reduction |
|---|---|---|---|---|---|
| `<Sxx.1 or SxxR>` | <...> | <...> | <...> | <...> | <...> |

## Retry

- Parent state: `SPLIT_AFTER_HARD_CAP | REPLACED_AFTER_HARD_CAP`
- Retry starts from: `<original parent section base>`
- Retry branch/worktree: `<codex/retry/...>`
- First ready active leaf: `<...>`
- Failed implementation/repair commits cherry-picked: `no`
- Recursion depth after recovery: `<0+>`
- Depth rule: `SPLIT may create depth <=3; depth 4+ must REBOUND or SIMPLIFY_REPLACE without continuation approval`
