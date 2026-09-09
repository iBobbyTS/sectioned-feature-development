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
10. [Development audit records](#development-audit-records)
11. [Archival rules](#archival-rules)

## Design goals

Artifacts exist to survive context compaction and coordinate agents. They must not become a second product or proof system.

Use these principles:

- one authoritative file per concern;
- append/update instead of generating duplicate per-round state;
- product behavior, not workflow formatting, determines validity;
- historical hashes/fingerprints aid orientation; new4.2 file-linkage checks block missing/stale current execution inputs, never retroactively invalidate accepted historical work;
- transient reviewer candidates are disposable;
- keep all workflow/process artifacts local and untracked; product-history commits contain only intended product, test, migration, and user-facing documentation changes.

## PLAN-FULL.md

Required feature fields:

- feature ID, invocation source/timing, exact trigger/negative evidence, predicted scale, and automatic-invocation approval state;
- original user request plus later corrections/superseded guidance;
- requirement/example/correction traceability matrix;
- minimum sufficient end-to-end outcome;
- scope authority map for proposed outcomes/mechanisms;
- foundational-owner decisions where a local patch and bounded shared-owner fix are both plausible;
- goal and observable behavior;
- authoritative constraints/invariants;
- non-goals/unsupported environments;
- ownership/state boundaries;
- feature acceptance;
- tiered validation;
- explicitly allowed structural changes;
- one pre-implementation plan-review gate status, stable reviewer task/session ID, and reviewed plan fingerprint.

Required section fields:

- goal;
- external authority anchor and necessity statement;
- local-patch versus shared-foundational-owner decision when applicable;
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

Use durable `FEATURE-CONTEXT` and `SECTION:{ID}` markers so extraction is deterministic. The additive SFD_PLAN_V4 block drives scheduling without replacing these narrative obligations. `FROZEN` records reviewed bytes; approval is in the state and canonical review ledger.

## PLAN.md

Generated from `PLAN-FULL.md` for one current section. Include:

- source plan path and informational hash;
- full feature context;
- selected section only;
- explicit warning that PLAN-FULL remains authoritative.

A changed source hash does not invalidate completed work by itself.

## Plan review ledger

Keep one `.agent-work/reviews/PLAN-REVIEW.md` with:

- original request, minimum outcome, plan path/fingerprint, stable reviewer task/session ID, and review scope;
- necessity-first disposition for every proposed section/mechanism, then a candidate table using `PLAN_BLOCKER`, `PLAN_SCOPE_EXPANSION`, `OWNER_DECISION`, or `PLAN_NIT`;
- authority/source evidence, concrete failure, affected section, and minimum plan-only correction for blockers;
- main-agent admission and corrections;
- validator result and final `APPROVED | BLOCKED` verdict;
- optional one-time `PLAN_DELTA` scope/result when a material plan boundary changed.

Do not create RAW/ADMISSION pairs, a clean streak, or a section whose only output is plan-review evidence. The ledger records a gate; it does not create product authority.

## FEATURE-STATE.md

Keep compact:

- feature ID, base/adoption head, starting branch/chosen branch base, execution mode, artifact isolation, `.agent-work` tracking state, invocation source/timing, exact trigger and negative evidence, predicted scale, automatic-invocation announcement/approval, and audit mode/requirement/trace/pack-state paths;
- PLAN-FULL review status, stable plan-reviewer ID, reviewed fingerprint, optional PLAN_DELTA result, and open owner decisions;
- current section/base/head/status, original lineage, intensity, assurance, and foundational-vs-local decision;
- frozen scope manifest;
- required clean evidence for the resolved assurance and exact reviewed/tested head;
- open finding IDs and cumulative repair-wave count;
- current checks and evidence gaps;
- recovery generation/backup and automatic-recovery-used flag;
- stable main/implementer/repairer/initial-delta/final reviewer task/session IDs, active writer/reviewer, frozen reviewed head, next allowed phase, and any sequence-gate violation;
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
- stable implementer and orchestrator task/session IDs;
- changed files/symbols;
- behavior implemented;
- tests/checks with results;
- decisions and limitations;
- structural changes used and their anchors;
- known non-blocking deferred work.

Keep it concise enough for a reviewer to orient without reconstructing the whole session.

## Review ledger

One `{ID}-REVIEW.md` contains:

1. scope/base/head/contract plus stable role task/session IDs and role-separation/sequence-barrier result;
2. resolved assurance and initial coverage summary, including any causal inspection expansion outside the named cone;
3. admitted findings table with acceptance-criterion/repository-gate authority and repair-owner decision;
4. repair waves, repairer/delta-reviewer IDs, and delta closure;
5. Clean A status;
6. final bounded result, frozen head, and final-reviewer identity/distinctness when required;
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
- the main orchestrator (plan author) classification and rationale;
- minimal plan changes;
- preserved code/evidence;
- restart base only when `RESTART_FROM_BASE`.

## Development audit records

While this skill is under evaluation, audit defaults to `LIVE`; only an explicit `audit off` disables it. Keep:

```text
.agent-work/audit/{feature-id}/
├── TRACE.jsonl
├── REQUIREMENTS.md
└── PACK-STATE.json
```

`REQUIREMENTS.md` preserves exact original user messages, Grill Me questions/answers or equivalent clarification, later corrections, named examples, final resolved requirements, and `SUPERSEDED` guidance with provenance. PLAN summaries are not substitutes.

`TRACE.jsonl`, generated with `scripts/audit_trace.py`, records only major phase/reviewer/finding/repair/validation/finalization events and the current Git/diff identity. Its first record includes invocation source/timing, exact trigger evidence, feature base/branch, skill version, and audit activation source. Sequence gaps or unknown future events degrade telemetry but do not invalidate product evidence.

`PACK-STATE.json` is the durable delivery gate for the one canonical pack. The working pack remains under `.agent-work/audit-packs/{feature-id}/current/`; `scripts/audit_finalize.py` atomically publishes one deterministic ZIP under `~/Desktop/audit-pack/` and is idempotent for unchanged source evidence.

Audit records are observational: they create no product authority, review finding, test, repair wave, or acceptance gate. A late audit labels reconstructed events `POST_HOC`. Never log secrets or copy unrelated/raw session history. See `references/audit-mode.md`.

## Archival rules

- Archive PLAN-FULL and compact ledgers locally at final feature completion under the recorded feature ID. Before freezing a different feature's base, preserve prior feature-owned active artifacts under their own local archive and initialize clean active artifacts. Never use Git reset or delete unrelated/user work for this isolation.
- Preserve accepted section contracts, handoffs, compact review ledgers, and hard-cap diagnoses.
- Delete/overwrite transient candidates and extracted PLAN.md when safe.
- Never stage or commit `.agent-work/**`; archive/update it locally at section acceptance, hard-cap recovery, or final feature boundaries.
- A newer artifact schema applies prospectively and does not require migration of completed work.
- Do not mix commits/findings/reviews from another feature ID into current state or audit metrics.
