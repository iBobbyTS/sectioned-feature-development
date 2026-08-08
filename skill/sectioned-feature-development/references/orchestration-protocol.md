# Orchestration Protocol

This reference defines agent roles, context packets, state transitions, branch handling, and hard-cap recovery.

## Contents

1. [Role separation](#1-role-separation)
2. [Durable state](#2-durable-state)
3. [Normal section sequence](#3-normal-section-sequence)
4. [Repair sequence](#4-repair-sequence)
5. [Scope and evidence exceptions](#5-scope-and-evidence-exceptions)
6. [Five-round recovery](#6-five-round-recovery)
7. [Branch and worktree safety](#7-branch-and-worktree-safety)
8. [Context compaction](#8-context-compaction)

## 1. Role separation

### Main agent

Owns execution authority, contracts, section graph, finding admission, state transitions, user decisions, integration, and final report. It should not defer scope authority to reviewers.

### Implementer (`sol_medium` normally)

Implements exactly one extracted section using the minimum-sufficient design. Produces tests and handoff. Does not review/accept itself.

### Repair agent (`sol_high` for high-risk work)

Receives admitted agent-fixable finding IDs only. Repairs bounded root causes and updates evidence. It does not see rejected proposals as requirements.

### Raw reviewer (`sol_xhigh`)

Fresh context. Uses `$code-review` in `SECTION` or `INTEGRATION` mode. Produces candidates, not authoritative admission or final workflow verdict.

### Recovery planner (`sol_max`)

At hard cap, receives classified evidence and chooses only the requested recovery family: `SPLIT`, `SIMPLIFY_REPLACE`, or `REBOUND`. It modifies planning artifacts, not product code.

Do not combine planner, implementer, reviewer, repairer, merger, and completion judge into one overloaded subagent.

## 2. Durable state

Before every handoff update:

- feature and section base/head;
- active branch/worktree;
- contract/plan/assurance revision;
- valid round, attempt, and clean streak;
- current raw/admission paths;
- admitted finding IDs and next action;
- scope proposals and owner decisions;
- checks/results;
- replan lineage/recovery mode.

If chat/session memory disagrees with repository artifacts, reconcile against repository state and authoritative files before continuing.

## 3. Normal section sequence

1. Confirm dependency-ready leaf and exact predecessor head.
2. Extract `PLAN.md` deterministically.
3. Freeze section contract and fingerprints.
4. Spawn one implementer with minimum packet.
5. Inspect handoff and repository state; reject silent scope/complexity expansion.
6. Run targeted then broad required checks.
7. Commit coherent implementation when authorized.
8. Spawn fresh raw reviewer with `SECTION-REVIEW-REQUEST`.
9. Main agent writes admission record and runs `review_gate.py validate`.
10. Update `FEATURE-STATE.md`.
11. Clean → next fresh review; material → repair/replan/decision; evidence failure → fix evidence and retry attempt.
12. After two consecutive clean admissions, mark section provisionally accepted.

## 4. Repair sequence

Packet to repair agent:

- exact section contract and current head;
- admitted stable IDs only;
- accepted root-cause statement;
- required evidence and commands;
- explicit files/boundary if known;
- instruction not to implement future sections or proposals.

After repair:

- inspect diff for unrelated redesign;
- update complexity receipt;
- run checks;
- commit if authorized;
- reset clean streak;
- spawn a fresh full reviewer.

A repair that needs a new mechanism outside the complexity budget pauses for bounded replan. A repair that needs a new assurance guarantee uses scope-change authority.

## 5. Scope and evidence exceptions

### `IN_SCOPE_REPLAN`

Do not send to a local repair agent. Main agent updates affected section graph/contracts while preserving approved feature semantics. Create a fresh attempt/base as appropriate.

### `OWNER_DECISION`

Ask the smallest bounded question. Continue independent work that does not prejudge the answer when safe.

### `EVIDENCE_FAILURE`

Consume the current review round and reset the clean streak. Repair the test environment, oracle, fixture, or baseline before the next fresh review. Record why the candidate conclusion is unsupported.

### `SCOPE_PROPOSAL`

Log in scope-change ledger. Do not implement or feed to `sol_max` as a requirement unless owner approves.

## 6. Five-round recovery

After round 5 without two clean admissions:

1. Freeze current head and state.
2. Ensure only section-owned work is included in an authorized snapshot commit.
3. Create backup ref without switching:

```bash
git branch "codex/backup/<feature>-<section>-g<gen>-<timestamp>" <failed_tip>
```

4. Write hard-cap artifact with raw/admission pairs.
5. Diagnose using admitted evidence, not raw comment volume.
6. Invoke `sol_max` with one recovery mode.
7. Main agent validates/normalizes revised `PLAN-FULL.md` and DAG.
8. Retire failed parent attempt.
9. Create retry branch/worktree from original parent `section_base`.
10. Carry durable artifacts only; re-derive product code.
11. Extract first ready replacement/descendant and resume normal sequence.

### Mode selection

- `SPLIT`: multiple genuine in-scope defect classes/behaviors are coupled.
- `SIMPLIFY_REPLACE`: implementation/review drift inflated guarantees or mechanisms; remove them and define the smallest proportional replacement.
- `REBOUND`: state/contract ownership is wrong and must be redistributed.
- `OWNER_DECISION`: missing semantics; block only for that decision.
- `REPAIR_EVIDENCE`: oracle/environment is the bottleneck.

Automatic technical recovery never needs continuation approval. Recursive `SPLIT` may create descendants only through depth 3. If another split would create depth 4+, preserve the failed attempt and require `REBOUND` of the nearest unstable parent/feature boundary or `SIMPLIFY_REPLACE`; do not deepen the lineage.

## 7. Branch and worktree safety

- Never reset/delete unrelated work.
- Prefer creating backup refs without checkout.
- Use isolated retry worktree if current tree has unrelated user changes.
- Do not cherry-pick failed product commits by default.
- Do not merge/push/create PR without separate authority.
- Record actual branch/worktree paths and heads before handoffs.
- Use deterministic integration order for parallel leaves.

A backup branch is evidence and recovery, not an active continuation branch.

## 8. Context compaction

After compaction or context doubt, reread:

1. repository instructions;
2. `PLAN-FULL.md`;
3. `FEATURE-STATE.md`;
4. active `PLAN.md` and section contract;
5. latest handoff;
6. latest raw/admission pair;
7. hard-cap/scope-change record if active.

Do not reconstruct state from summaries when durable artifacts exist.
