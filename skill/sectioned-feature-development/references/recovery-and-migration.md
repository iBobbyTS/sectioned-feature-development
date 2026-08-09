# Recovery and Workflow Migration

## Contents

1. [What the hard cap measures](#what-the-hard-cap-measures)
2. [Hard-cap evidence packet](#hard-cap-evidence-packet)
3. [Recovery classifications](#recovery-classifications)
4. [Preservation rules](#preservation-rules)
5. [Automatic recovery limit](#automatic-recovery-limit)
6. [Adopting a new skill version mid-feature](#adopting-a-new-skill-version-mid-feature)
7. [Legacy evidence](#legacy-evidence)

## What the hard cap measures

The cap measures **repair waves**, not reviewer calls.

One repair wave is:

1. one or more compatible admitted root-cause classes;
2. one coherent repair;
3. targeted validation;
4. delta review closing or reopening those IDs.

Reviewer invocations, repeated comments, rejected scope proposals, plan formatting corrections, and tool retries do not count. Any admitted repair arising from initial, delta, final, checkpoint, or integration review does count toward the applicable cumulative budget.

The fifth wave is allowed to complete. The counter does not reset when entering final review or choosing a non-structural recovery. Recovery begins only before a sixth wave or when the current wave proves the section architecture/contract cannot close locally.

## Hard-cap evidence packet

Before invoking `@sol_max`, collect:

- feature outcome and non-goals;
- original section lineage and whether its one automatic recovery event is already used;
- section goal, base, head, frozen scope manifest, and direct impact cone;
- current diff summary;
- five repair waves and stable finding IDs;
- which findings were closed and what recurred;
- current open blocker;
- tests and environment gaps;
- new mechanisms introduced and their requirement anchors;
- rejected scope proposals in a non-authoritative appendix;
- current branch/worktree and backup ref.

Do not send rejected proposals intermixed with admitted requirements.

## Recovery classifications

### `CONTINUE_CURRENT`

Use when architecture/ownership is sound and one named local root cause remains. Authorize exactly one recovery repair wave against current code, then go directly to `FINAL_BOUNDED`. It does not create another general five-wave cycle.

### `SIMPLIFY_CURRENT`

Use when review-created mechanisms, stronger threat models, generalized tooling, or excessive proof infrastructure dominate. Delete/simplify unanchored mechanisms in one named recovery wave, preserve requirement-aligned fixes, then go directly to `FINAL_BOUNDED`.

### `SPLIT_REMAINING`

Use when unresolved behavior genuinely contains two independent product increments. Preserve completed correct code and split only remaining work into at most two active descendants.

### `REBOUND_OWNER`

Use when the unresolved behavior belongs to another existing owner or section. Move the responsibility and update only affected dependencies.

### `REPAIR_EVIDENCE`

Use when product behavior appears correct but one acceptance-criterion-anchored oracle/environment is broken. Fix that evidence in one named recovery wave; do not create an evidence-only descendant.

### `RESTART_FROM_BASE`

Use only when the implementation direction, state owner, or threat model is demonstrably wrong and in-place simplification would retain most of the wrong design. State:

- wrong assumptions;
- code/mechanisms to discard;
- why reversion/simplification is insufficient;
- exact restart base;
- valid fixes/evidence that can still be reused conceptually.

## Preservation rules

- Create `codex/backup/***` as a recovery ref, not an active development requirement.
- Keep current correct commits by default.
- Do not require a pristine ancestry for tests/reviews.
- Do not replay accepted predecessors unless changed product code invalidated their contract.
- Do not copy rejected scope proposals into new contracts.
- Do not rewrite the full plan when only one section/dependency changes.
- Do not add a descendant solely for a test, checkpoint, review format, or provenance record.
- If all unresolved items are reviewer-created tooling, generalized oracles, or process artifacts without an exact acceptance anchor, structural recovery is forbidden; simplify/delete them or stop.

## Automatic recovery limit

One automatic hard-cap recovery event is allowed per original section lineage, regardless of classification.

- Non-structural recovery (`CONTINUE_CURRENT`, `SIMPLIFY_CURRENT`, `REPAIR_EVIDENCE`) authorizes exactly one named recovery wave followed by `FINAL_BOUNDED`. Another independent blocker stops the lineage; do not diagnose/recover again automatically.
- Structural recovery (`SPLIT_REMAINING`, `REBOUND_OWNER`, `RESTART_FROM_BASE`) may establish a genuinely new boundary with a fresh five-wave budget, but the replacement inherits `automatic_recovery_used = yes`. If it reaches another hard cap, stop rather than recursively growing `S03.1.1.1...`.

This limit prevents technical recovery from becoming a new feature graph or a hidden sequence of five-wave cycles.

## Adopting a new skill version mid-feature

A skill update is a workflow change, not a product change.

When adopting mid-feature:

1. Read existing PLAN/state/review artifacts and current Git state.
2. Map the current section into the closest new state without rewriting history.
3. Preserve accepted sections and closed findings.
4. Continue with delta review when a repair is already in progress.
5. Use one final bounded review if prior coverage is unclear.
6. Sanitize only the active, unaccepted contract: trace each guarantee, oracle, and structural allowance to user intent, repository rules, or established product behavior; downgrade unanchored reviewer-authored items to `SCOPE_PROPOSAL`.
7. Add only the minimum fields needed for future continuation.
8. Do not create migration sections, plan-review loops, legacy admission copies, or “clean lineage” worktrees.

If an old plan lacks new optional headings, note them in current state and continue. Do not run a strict validator that retroactively fails accepted work.

## Legacy evidence

Evidence remains valid when:

- the product code and relevant contract are unchanged;
- the test still runs against current code or its result remains directly applicable;
- the review range and conclusion can be understood;
- no reset trigger materially changed the behavior.

Legacy evidence may be summarized in the compact review ledger. It does not need to be copied into a new RAW/ADMISSION format or recommitted.

Only actual product/contract changes invalidate evidence.
