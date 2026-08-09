# Artifact Schemas

## Contents

1. [Design goals](#design-goals)
2. [PLAN-FULL.md](#plan-fullmd)
3. [PLAN.md](#planmd)
4. [FEATURE-STATE.md](#feature-statemd)
5. [Section contract](#section-contract)
6. [Section handoff](#section-handoff)
7. [Review ledger](#review-ledger)
8. [Hard-cap diagnosis](#hard-cap-diagnosis)
9. [Archival rules](#archival-rules)

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

- goal and observable behavior;
- authoritative constraints/invariants;
- non-goals/unsupported environments;
- ownership/state boundaries;
- feature acceptance;
- tiered validation;
- explicitly allowed structural changes.

Required section fields:

- goal;
- dependencies;
- expected scope/direct impact cone;
- non-goals/deferred owner;
- invariants;
- allowed structural changes;
- acceptance criteria;
- targeted/section/integration validation;
- reset triggers.

Use durable `FEATURE-CONTEXT` and `SECTION:{ID}` markers so extraction is deterministic.

## PLAN.md

Generated from `PLAN-FULL.md` for one current section. Include:

- source plan path and informational hash;
- full feature context;
- selected section only;
- explicit warning that PLAN-FULL remains authoritative.

A changed source hash does not invalidate completed work by itself.

## FEATURE-STATE.md

Keep compact:

- feature base/head and execution mode;
- current section/base/head/status;
- Clean A/Clean B status;
- open finding IDs and repair-wave count;
- current checks and evidence gaps;
- recovery generation/backup if any;
- next action and owner decisions;
- accepted/deferred sections summary.

Do not reproduce every reviewer narrative.

## Section contract

Freeze:

- section ID/title/base;
- outcome and changed contract;
- primary owner and direct impact cone;
- explicit non-goals/deferred owner;
- allowed structural changes;
- acceptance criteria;
- validation tiers;
- reset triggers.

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
2. initial coverage summary;
3. admitted findings table;
4. repair waves and delta closure;
5. Clean A status;
6. final bounded result;
7. Clean B/acceptance status;
8. residual risk and non-blocking proposals.

Use stable IDs. Do not create separate durable admission files. The main agent's classification in this ledger is authoritative.

`{ID}-CANDIDATES.md` is transient reviewer output. Overwrite or delete it after the ledger is updated.

## Hard-cap diagnosis

Record:

- base/head and backup ref;
- five repair waves;
- open/root recurring causes;
- rejected scope proposals separately;
- current architecture/structural mechanisms;
- `@sol_max` classification and rationale;
- minimal plan changes;
- preserved code/evidence;
- restart base only when `RESTART_FROM_BASE`.

## Archival rules

- Archive PLAN-FULL at final feature completion.
- Preserve accepted section contracts, handoffs, compact review ledgers, and hard-cap diagnoses.
- Delete/overwrite transient candidates and extracted PLAN.md when safe.
- Avoid per-round process commits. Commit/archive artifacts at section acceptance, hard-cap recovery, or final feature boundaries.
- A newer artifact schema applies prospectively and does not require migration of completed work.
