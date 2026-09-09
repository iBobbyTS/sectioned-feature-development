# Section Review Request

Review the current section using `$code-review` as a **single-pass reviewer**. Do not repair code, start a review loop, delegate the review again, or change the section contract.

## Identity and sequence barrier

- Planned provider and actual native-or-ZAS route/tool (native code_reviewer is never a ZAS alias):
- Reviewer raw task/session or ZAS agent_id:
- Main/orchestrator task/session ID:
- Plan reviewer task/session ID:
- Implementer task/session ID:
- Repairer task/session ID, if any:
- Reviewer is role-distinct as required for this mode: `yes`
- No product writer touches this frozen candidate: `yes`; any other live parent has explicit parallel authority and isolation:
- Frozen reviewed product/test head:
- Main-owned next action after actual result and admission; successor remains blocked until required acceptance:

## Review packet

- Mode: `INITIAL_BOUNDED | REPAIR_DELTA | FINAL_BOUNDED`
- Working tree/repository:
- Feature ID:
- Section:
- Review intensity: `MECHANICAL | BOUNDED | HIGH_RISK`
- Review assurance: `ONE | TWO`
- Contract: `.agent-work/sections/<ID>-CONTRACT.md`
- Feature plan: `.agent-work/PLAN-FULL.md`
- Handoff: `.agent-work/sections/<ID>-HANDOFF.md`
- Review range:
- Previous reviewed head, for DELTA:
- Frozen finding IDs/acceptance criteria/repair owners, for DELTA:
- Allowed-to-edit owners/files/symbols/routes:
- Inspect-only dependency paths/direct impact cone:
- Explicitly excluded owners/mechanisms:
- Cumulative repair waves used: `<N>/5`
- Automatic recovery used: `no | yes`
- Required checks:
- Transient output: `.agent-work/reviews/<ID>-CANDIDATES.md`

## Mandatory scope rule

Report only:

- `DIFF_CAUSED` defects introduced by the specified diff;
- `MERGE_BLOCKING_DEPENDENCY` defects on a necessary acceptance path whose faulty behavior the diff newly depends on, activates, serializes, or publicly exposes;
- `EVIDENCE_GAP` tied to an exact acceptance criterion or repository-required gate that existed before this review.

Incidental traversal through a shared entry point, proximity to changed code, unrelated old bugs, stronger product/security/durability/compatibility guarantees, new supported environments, generic frameworks, whole-repository analyzers, CI governance, future-proofing, style preferences, and named later-section work are non-blocking.

Every blocker must prove changed-hunk causality, reachable trigger, existing authority, material consequence, and a bounded repair. For security findings, also prove the current asset, actor/capability, entry point, trust boundary, and preconditions.

The manifest bounds edits, not causal inspection. To inspect an unlisted dependency, record the exact data/control/serialization/contract chain from a changed symbol and stop at the candidate; do not fan out recursively. Inspection does not authorize changing a new owner. Report that need to the main agent.

For maintainability findings, identify whether the diff creates a second authoritative implementation or leaves sibling callers inconsistent. A shared foundational fix is an owner decision, not automatic scope. Cosmetic helper extraction or a one-use abstraction preference is `NIT_DEBT`.

## Mode-specific boundary

- `INITIAL_BOUNDED`: review the complete section diff once using only risk lenses triggered by the frozen contract; batch root causes and record coverage. A clean result lets main accept an assurance-`ONE` bounded/high-risk section after required checks; the reviewer itself never accepts. Assurance `TWO` still proceeds to final.
- `REPAIR_DELTA`: review only the repair range, frozen findings, and invalidated impact cone. Do not rescan unchanged original scope.
- `FINAL_BOUNDED`: required after any repair, for assurance `TWO`, and for mechanical sections; omitted only after a clean initial assurance-`ONE` bounded/high-risk section. This is not another open-ended discovery pass. Verify the current diff against the contract, highest-risk changed path, repair impact cones, and accidental scope growth. Do not audit the repository or strengthen the contract.

Any admitted repair from any mode counts toward the same cumulative five-wave section budget.

## 4.2 durable handoff

The reviewer returns a result to the parent; the parent saves the complete report at the frozen output path, hashes it, and records actual dispatch/session identity before admission. No output path or missing actual report means INSUFFICIENT_EVIDENCE, never an implicit clean. The reviewer does not edit workflow state or accept a section. The companion context is DELEGATED_PASS.
Include parent_section_id, optional subsection_id, original_lineage_id, review_id, mode, base/head, checks, candidates and coverage invalidations. SUBSECTION_DELTA does not create child acceptance; PARENT_RECONCILIATION completes the cumulative primary pass.

## 4.4 packet representation

Return readable Markdown with the actual requested scope, identities, head, evidence and gaps. No machine receipt schema, registry or plan-hash equality is required. Any hash field in the template is optional archival identity unless a real immutable artifact transfer requires it. Missing evidence is still a gap; missing JSON formatting is not. Main owns admission/scheduling, never the reviewer.
