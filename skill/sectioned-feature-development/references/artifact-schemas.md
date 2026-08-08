# Artifact Schemas and Lifecycle

This reference defines the durable Markdown artifacts and deterministic helper commands.

## Contents

1. [`PLAN-FULL.md`](#1-plan-fullmd)
2. [`PLAN.md`](#2-planmd)
3. [`FEATURE-STATE.md`](#3-feature-statemd)
4. [Section contract and handoff](#4-section-contract-and-handoff)
5. [Raw review and admission](#5-raw-review-and-admission)
6. [Scope-change records](#6-scope-change-records)
7. [Hard-cap records](#7-hard-cap-records)
8. [Archive lifecycle](#8-archive-lifecycle)
9. [Helper commands](#9-helper-commands)

## 1. `PLAN-FULL.md`

Authoritative source for feature promises, assurance envelope, requirement coverage, section graph, checkpoints, rollout/recovery, decisions, and approved scope changes.

Required markers:

```markdown
<!-- FEATURE-CONTEXT:START -->
...stable context...
<!-- FEATURE-CONTEXT:END -->

<!-- SECTION:S01:START -->
## S01 — Title
...
<!-- SECTION:S01:END -->
```

Hierarchical IDs such as `S03.1.1` are valid. Retired parents may remain in status/history tables, but active executable blocks and dependency edges must not be contradictory.

Each active section needs the exact headings accepted by `section_plan.py`, including `最低充分设计与复杂度预算`.

Fingerprint the complete plan whenever freezing a contract or approving a scope change.

## 2. `PLAN.md`

Transient packet generated from one validated plan and one active leaf. It contains:

- source path and SHA-256;
- extraction time;
- stable feature context;
- exactly one section block.

Do not append decisions or review notes. Put durable state in the designated artifacts.

## 3. `FEATURE-STATE.md`

Externalized orchestration state. Update before every handoff and after every mutation/review/admission.

Must record:

- execution mode, working path, branch/worktree;
- feature/section base and head;
- plan/contract/assurance revisions;
- active lineage and replan generation;
- review attempt, valid round, clean streak;
- raw/admission paths and classifications;
- scope-change and complexity ledgers;
- checks, decisions, checkpoints, hard-cap events;
- exact next action and residual risk.

If artifact and session disagree, repository reality plus authoritative artifacts win after explicit reconciliation.

## 4. Section contract and handoff

### `{ID}-CONTRACT.md`

Immutable for one attempt. Contains exact scope, direct impact cone, assurance envelope, complexity budget, acceptance criteria, evidence, deferred owners, and replan rules.

Changing a frozen promise requires a new revision/fingerprint and invalidation record. Hard-cap replacement creates new contracts; do not rewrite history to make failed reviews appear consistent.

### `{ID}-HANDOFF.md`

Evidence claim from implementer/repairer. Contains actual files/behavior, impact cone, checks, decisions, limitations, repair IDs, complexity receipt, and scope proposals. Reviewers verify it independently.

## 5. Raw review and admission

Naming:

```text
{ID}-SECTION-r01-RAW.md
{ID}-SECTION-r01-ADMISSION.md
{ID}-SECTION-r01-retry01-RAW.md          # evidence-failure retry if needed
{ID}-SECTION-r01-retry01-ADMISSION.md
FEATURE-INTEGRATION-r01-RAW.md
FEATURE-INTEGRATION-r01-ADMISSION.md
```

Raw review contains candidates and evidence. Admission contains authoritative class decisions. Never edit raw review to match admission.

Admission required top-level fields:

- mode/section/counting round/attempt;
- raw path and frozen revisions;
- reviewed base/head;
- valid-full-review flag;
- result/clean flag/streak.

Each finding block uses exact markers:

```markdown
<!-- FINDING:REV-001:START -->
### REV-001 — Title
...required fields...
<!-- FINDING:REV-001:END -->
```

`review_gate.py` validates class/boundary consistency and material evidence fields. `history` validates contiguous completed rounds, streak, acceptance, and hard cap.

## 6. Scope-change records

Path:

```text
.agent-work/scope-changes/SC-001.md
```

Required lifecycle:

1. `PROPOSED`: records current boundary, proposed promise, evidence, cost, and alternatives.
2. Owner decides `APPROVED` or `REJECTED`.
3. If approved, update exact plan text, fingerprints/contracts, coverage, evidence, and invalidation state.
4. If rejected, keep record non-authoritative and do not feed it to repair/recovery as a requirement.

A raw reviewer comment cannot be marked approved by the main agent unless existing governance already grants that authority.

## 7. Hard-cap records

Path:

```text
.agent-work/replans/{ID}-g{generation}-HARD-CAP.md
```

Must distinguish:

- five raw reviews;
- five admission decisions;
- material admitted root causes;
- rejected/non-authoritative proposals;
- code/check history;
- diagnosis and recovery mode;
- backup branch/failed tip/original base;
- replacement/descendant plan and retry path.

Do not say “five reviews found five defects” unless five defects were admitted.

## 8. Archive lifecycle

After final reporting:

1. reconcile final feature head/state/verdict;
2. ensure all active leaves and approved scope changes are represented;
3. remove transient `PLAN.md` only after durable records exist;
4. move `PLAN-FULL.md` to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md`;
5. preserve contracts, handoffs, raw/admission pairs, scope changes, hard-cap records, and named backup refs according to repository policy;
6. exclude `.DS_Store`, `__MACOSX`, `__pycache__`, `.pyc`, temporary outputs, and unrelated artifacts from a distributed skill/package.

## 9. Helper commands

```bash
# Validate plan markers, headings, hierarchical IDs, dependencies, and DAG
python scripts/section_plan.py validate .agent-work/PLAN-FULL.md

# List active section blocks
python scripts/section_plan.py list .agent-work/PLAN-FULL.md

# Extract one leaf
python scripts/section_plan.py extract \
  .agent-work/PLAN-FULL.md S03.1 --output .agent-work/PLAN.md

# Fingerprint
python scripts/section_plan.py fingerprint .agent-work/PLAN-FULL.md

# Safe archive copy; add --move only after finalization
python scripts/section_plan.py archive \
  .agent-work/PLAN-FULL.md --dest-dir .agent-work/plans

# Validate one admission
python scripts/review_gate.py validate \
  .agent-work/reviews/S03.1-SECTION-r01-ADMISSION.md

# Validate one section history and compute status
python scripts/review_gate.py history \
  '.agent-work/reviews/S03.1-SECTION-r*-ADMISSION.md'
```

Scripts refuse malformed markers, missing required headings, duplicate/self/unknown dependencies, dependency cycles, inconsistent admission class/boundary combinations, invalid clean results, duplicate/noncontiguous completed rounds, and more than five completed rounds.
