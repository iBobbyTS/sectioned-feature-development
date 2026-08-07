# Artifact Schemas and Lifecycle

This reference defines the durable artifacts used by the workflow and the deterministic helper script.

## Contents

1. [`PLAN-FULL.md`](#1-plan-fullmd)
2. [`PLAN.md`](#2-planmd)
3. [`FEATURE-STATE.md`](#3-feature-statemd)
4. [`{ID}-CONTRACT.md`](#4-id-contractmd)
5. [`{ID}-HANDOFF.md`](#5-id-handoffmd)
6. [Review files](#6-review-files)
7. [Archive lifecycle](#7-archive-lifecycle)
8. [Helper script commands](#8-helper-script-commands)

## 1. `PLAN-FULL.md`

Purpose: authoritative feature contract, requirement coverage, dependency graph, integration gates, and all section specifications.

Required top-level content:

- Feature metadata and exact base.
- Goal, user/operator behavior, non-goals, and global invariants.
- Authoritative sources and hard constraints.
- Full acceptance criteria and validation commands.
- Ownership/state-boundary map.
- Requirement coverage matrix.
- Section index and dependency graph.
- Integration checkpoint plan.
- Rollout, rollback, migration, flag, observability, and cleanup plan.
- Decision and deferred-work ledgers.

Use these exact markers so `scripts/section_plan.py` can extract stable context:

```markdown
<!-- FEATURE-CONTEXT:START -->
...feature context required by every section...
<!-- FEATURE-CONTEXT:END -->

<!-- SECTION:S01:START -->
## S01 — Title
...
<!-- SECTION:S01:END -->
```

Each section block must contain these headings:

```markdown
### 目标
### 行为增量
### 依赖
### 预计范围
### 非目标
### 全局不变量
### 验收标准
### 验证命令
### 发布与恢复
### 延后项
```

English aliases are accepted by the helper script, but plans should follow the user's default language.

## 2. `PLAN.md`

Purpose: transient execution packet for exactly one section.

Generated content should include:

- Source plan path and SHA-256 fingerprint.
- Extraction time.
- Feature context block.
- Exactly one section block.

Do not append unrelated scratch notes. Put durable decisions in `FEATURE-STATE.md` or the section contract.

Delete `PLAN.md` only after the section is accepted or abandoned and its contract, handoff, review, and state records are durable.

## 3. `FEATURE-STATE.md`

Purpose: externalized state across agents, context resets, and repair rounds.

Required records:

- Feature base/current head and execution mode.
- Current state and next action.
- Section status table with base/head.
- Requirement coverage status.
- Decisions and authority.
- Open findings and review locations.
- Checks run/not run.
- Integration checkpoints.
- Reset events and invalidated evidence.
- Deferred items and residual risk.

Update it before every context handoff.

## 4. `{ID}-CONTRACT.md`

Purpose: immutable agreement for one ordinary section baseline.

Required records:

- Section and feature identifiers.
- Frozen base and dependency heads.
- Goal, behavior, non-goals, and global invariants.
- Scope and semantic boundaries.
- Acceptance criteria and verification commands.
- Compatibility, migration, rollout, rollback, and observability.
- Allowed deferred work.
- Replan/reset triggers.
- Open decisions; must be empty before implementation.

If the contract changes materially, create a revision record, update `PLAN-FULL.md`, and reset the section review baseline.

## 5. `{ID}-HANDOFF.md`

Purpose: implementation or repair evidence for the next context.

Required records:

- Base/head or diff fingerprint.
- Files and behavior changed.
- Decisions made and source.
- Commands run with exact outcome.
- Manual/runtime evidence.
- Known limitations and deferred work.
- Suggested impact-cone edges.
- Commit ID when authorized.

A handoff is a claim to verify, not proof by itself.

## 6. Review files

Naming:

```text
{ID}-SECTION-r01.md
{ID}-DELTA-r02.md
{ID}-RESET-r03.md
FEATURE-INTEGRATION-r01.md
FEATURE-INTEGRATION-DELTA-r02.md
```

Every review file should record:

- Review mode.
- Exact base/head.
- Contract and feature-invariant paths.
- Coverage and critical paths.
- Findings with stable IDs.
- Checks and evidence.
- Reset decision.
- Verdict.

Use the ledger format supplied by `$code-review` when available.

## 7. Archive lifecycle

After final reporting:

1. Ensure `FEATURE-STATE.md` points to the actual final head and review verdict.
2. Ensure no active section still depends on transient `PLAN.md` content.
3. Remove transient `PLAN.md`.
4. Move `PLAN-FULL.md` to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md`.
5. Preserve section contracts, handoffs, and review evidence unless repository policy specifies a different retention rule.

The helper script supports safe validation, listing, extraction, fingerprinting, and archiving.

## 8. Helper script commands

```bash
# Validate feature/section headings, markers, IDs, references, and dependency DAG
python scripts/section_plan.py validate .agent-work/PLAN-FULL.md

# List sections and titles
python scripts/section_plan.py list .agent-work/PLAN-FULL.md

# Create transient PLAN.md containing feature context and one section
python scripts/section_plan.py extract \
  .agent-work/PLAN-FULL.md S03 --output .agent-work/PLAN.md

# Print SHA-256 fingerprint
python scripts/section_plan.py fingerprint .agent-work/PLAN-FULL.md

# Copy to timestamped archive (safe default)
python scripts/section_plan.py archive \
  .agent-work/PLAN-FULL.md --dest-dir .agent-work/plans

# Move instead of copy only after finalization
python scripts/section_plan.py archive \
  .agent-work/PLAN-FULL.md --dest-dir .agent-work/plans --move
```

The script refuses duplicate section IDs, missing feature/section markers or headings, self/unknown dependencies, dependency cycles, and overwrite of an existing output or archive.
