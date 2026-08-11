# Artifact Schemas

## Contents

1. [Design goals](#design-goals)
2. [PLAN-FULL.md](#plan-fullmd)
3. [PLAN.md](#planmd)
4. [Plan review ledger](#plan-review-ledger)
5. [FEATURE-STATE.md](#feature-statemd)
6. [Section contract](#section-contract)
7. [Section handoff](#section-handoff)
8. [Review ledger](#review-ledger)
9. [Hard-cap diagnosis](#hard-cap-diagnosis)
10. [Archival rules](#archival-rules)

## Design goals

Artifacts exist to survive context compaction and coordinate agents. They must not become a second product or proof system.

Use these principles:

- one authoritative file per concern;
- append/update instead of generating duplicate per-round state;
- product behavior, not workflow formatting, determines validity;
- hashes/fingerprints aid orientation only;
- transient reviewer candidates are disposable;
- commit evidence at coherent boundaries, not after every edit.

## PLAN-FULL.md

Required feature fields:

- feature ID;
- original user request plus later corrections/superseded guidance;
- requirement/example/correction traceability matrix;
- minimum sufficient end-to-end outcome;
- scope authority map for proposed outcomes/mechanisms;
- goal and observable behavior;
- authoritative constraints/invariants;
- non-goals/unsupported environments;
- ownership/state boundaries;
- feature acceptance;
- tiered validation;
- explicitly allowed structural changes;
- one pre-implementation plan-review gate status and reviewed plan fingerprint.

Required section fields:

- goal;
- external authority anchor and necessity statement;
- dependencies;
- frozen scope manifest: allowed-to-edit owners/files/symbols/routes, inspect-only dependency paths, and excluded mechanisms;
- direct impact cone;
- non-goals/deferred owner;
- invariants;
- allowed structural changes;
- acceptance criteria;
- targeted/section/integration validation;
- reset triggers;
- review intensity and review assurance (`ONE | TWO | AUTO -> resolved`) with reasons.

Use durable `FEATURE-CONTEXT` and `SECTION:{ID}` markers so extraction is deterministic.

## PLAN.md

Generated from `PLAN-FULL.md` for one current section. Include:

- source plan path and informational hash;
- full feature context;
- selected section only;
- explicit warning that PLAN-FULL remains authoritative.

A changed source hash does not invalidate completed work by itself.

## Plan review ledger

Keep one `.agent-work/reviews/PLAN-REVIEW.md` with:

- original request, minimum outcome, plan path/fingerprint, reviewer identity, and review scope;
- candidate table using `PLAN_BLOCKER`, `PLAN_SCOPE_EXPANSION`, `OWNER_DECISION`, or `PLAN_NIT`;
- authority/source evidence, concrete failure, affected section, and minimum plan-only correction for blockers;
- main-agent admission and corrections;
- validator result and final `APPROVED | BLOCKED` verdict;
- optional one-time `PLAN_DELTA` scope/result when a material plan boundary changed.

Do not create RAW/ADMISSION pairs, a clean streak, or a section whose only output is plan-review evidence. The ledger records a gate; it does not create product authority.

## FEATURE-STATE.md

Keep compact:

- feature ID, base/head, execution mode, and artifact-isolation status;
- PLAN-FULL review status, reviewed fingerprint, optional PLAN_DELTA result, and open owner decisions;
- current section/base/head/status, original lineage, intensity, and assurance;
- frozen scope manifest;
- required clean evidence for the resolved assurance and exact reviewed/tested head;
- open finding IDs and cumulative repair-wave count;
- current checks and evidence gaps;
- recovery generation/backup and automatic-recovery-used flag;
- integration repair-wave/recovery counters;
- next action and owner decisions;
- accepted/deferred sections summary.

Do not reproduce every reviewer narrative.

## Section contract

Freeze:

- feature ID and section ID/title/base;
- outcome and changed contract;
- external authority anchor, minimum-outcome necessity, and why a smaller existing path is insufficient;
- frozen allowed-to-edit owners, inspect-only dependency paths, excluded mechanisms, and direct impact cone;
- explicit non-goals/deferred owner;
- allowed structural changes;
- acceptance criteria;
- validation tiers;
- review intensity/assurance and the AUTO/override rationale;
- reset triggers;
- review intensity and review assurance (`ONE | TWO | AUTO -> resolved`) with reasons.

Ordinary repair does not modify the contract. A material contract change is a reset or owner decision.

## Section handoff

Record:

- base/head;
- changed files/symbols;
- behavior implemented;
- tests/checks with results;
- decisions and limitations;
- structural changes used and their anchors;
- known non-blocking deferred work.

Keep it concise enough for a reviewer to orient without reconstructing the whole session.

## Review ledger

One `{ID}-REVIEW.md` contains:

1. scope/base/head/contract;
2. resolved assurance and initial coverage summary, including any causal inspection expansion outside the named cone;
3. admitted findings table with acceptance-criterion/repository-gate authority and repair-owner decision;
4. repair waves and delta closure;
5. Clean A status;
6. final bounded result when required;
7. clean evidence/acceptance status under `ONE` or `TWO`, with exact reviewed/tested head;
8. residual risk and non-blocking proposals.

Use stable IDs. Do not create separate durable admission files. The main agent's classification in this ledger is authoritative.

`{ID}-CANDIDATES.md` is transient reviewer output. Overwrite or delete it after the ledger is updated.

## Hard-cap diagnosis

Record:

- base/head and backup ref;
- original section lineage, automatic-recovery-used state, and cumulative repair waves;
- open/root recurring causes;
- rejected scope proposals separately;
- current architecture/structural mechanisms;
- `@sol_max` classification and rationale;
- minimal plan changes;
- preserved code/evidence;
- restart base only when `RESTART_FROM_BASE`.

## Archival rules

- Archive PLAN-FULL and compact ledgers at final feature completion under the recorded feature ID; reset/archive active artifacts before a different feature starts.
- Preserve accepted section contracts, handoffs, compact review ledgers, and hard-cap diagnoses.
- Delete/overwrite transient candidates and extracted PLAN.md when safe.
- Avoid per-round process commits. Commit/archive artifacts at section acceptance, hard-cap recovery, or final feature boundaries.
- A newer artifact schema applies prospectively and does not require migration of completed work.
- Do not mix commits/findings/reviews from another feature ID into current state or audit metrics.
