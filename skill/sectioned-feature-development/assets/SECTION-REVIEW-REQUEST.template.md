# Section Review Request

Review the current section using `$code-review` as a **single-pass reviewer**. Do not repair code, start a review loop, delegate the review again, or change the section contract.

- Mode: `INITIAL_BOUNDED | REPAIR_DELTA | FINAL_BOUNDED`
- Working tree/repository:
- Section:
- Contract: `.agent-work/sections/<ID>-CONTRACT.md`
- Feature plan: `.agent-work/PLAN-FULL.md`
- Handoff: `.agent-work/sections/<ID>-HANDOFF.md`
- Review range:
- Previous reviewed head, for DELTA:
- Frozen finding IDs/acceptance criteria, for DELTA:
- Direct impact cone:
- Required checks:
- Transient output: `.agent-work/reviews/<ID>-CANDIDATES.md`

## Mandatory scope rule

Report only:

- `DIFF_CAUSED` defects introduced by the specified diff;
- `MERGE_BLOCKING_DEPENDENCY` defects that the diff newly depends on/exposes/makes reachable;
- contract-required `EVIDENCE_GAP`.

Unrelated old bugs, stronger product/security/durability/compatibility guarantees, new supported environments, generic frameworks, whole-repository analyzers, CI governance, future-proofing, style preferences, and named later-section work are non-blocking.

Every blocker must prove changed-hunk causality, reachable trigger, existing authority, material consequence, and a bounded repair. For security findings, also prove the current asset, actor/capability, entry point, trust boundary, and preconditions.

## Mode-specific boundary

- `INITIAL_BOUNDED`: review the complete section diff once; batch root causes and record coverage.
- `REPAIR_DELTA`: review only the repair range, frozen findings, and invalidated impact cone. Do not rescan unchanged original scope.
- `FINAL_BOUNDED`: independently verify the current complete diff, highest-risk changed path, repair impact cones, and accidental scope growth. Do not audit the repository or strengthen the contract.
