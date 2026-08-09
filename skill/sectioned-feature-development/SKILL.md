---
name: sectioned-feature-development
description: "Plan, implement, review, and integrate large or high-risk software changes as minimal bounded sections without review-created scope creep. Use when expected behavioral edits may exceed roughly 300 lines; more than three modules, packages, services, pages, or workflows are affected; persistence, schema, security, permissions, concurrency, public API, deployment, routing, or state ownership changes; the impact cone is hard to bound; or a previous whole-change review failed to converge. The workflow freezes product scope, uses one initial bounded review, delta-only repair verification, one final bounded review, proportional testing, and evidence-preserving hard-cap recovery instead of repeated full scans or automatic clean-room rebuilds."
---

# Sectioned Feature Development

Deliver one non-trivial change as a sequence of minimal, reviewable behavior sections. The governing invariant is:

> Review may discover defects in the approved change; it may not create a larger product, threat model, compatibility promise, governance system, or proof bureaucracy.

Use patchset-style review: one bounded discovery pass, repair-delta verification, then one independent bounded final pass. Preserve valid code and evidence across repairs, skill updates, and recovery.

## Authority and safety

- Follow repository-local instructions before this skill.
- Use one execution mode:
  - `PLAN_ONLY`: create or revise planning artifacts only.
  - `EXECUTE_NO_COMMIT`: implement and validate without branch or commit operations.
  - `EXECUTE_WITH_COMMITS`: create bounded branches/worktrees and make coherent implementation, repair, and recovery commits.
- A planning or review request alone does not authorize commits.
- If governing Custom Instructions explicitly delegate branch/commit authority to `$sectioned-feature-development`, that scoped delegation overrides a general no-commit rule only for this workflow's bounded feature/retry branches and coherent implementation, repair, and recovery commits.
- Never push, merge, create a pull request, rewrite published history, clean, delete user work, or discard unrelated changes unless separately authorized.
- Technical hard-cap diagnosis and bounded recovery do not require continuation approval. Stop only for a genuine owner decision: product semantics, supported environment, compatibility, migration meaning, durability, threat model, acceptable risk, or rollout policy.

## Trigger

Use this workflow when any condition holds:

- Expected behavioral edits are roughly more than 300 lines.
- More than three modules, packages, services, pages, or workflows are affected.
- The change crosses persistence, schema, money, time, units, security, permissions, tenancy, routing, concurrency, background jobs, public API, deployment, or shared-state boundaries.
- Architecture or state ownership changes.
- The impact cone is difficult to bound.
- A previous whole-change implementation or review loop failed to converge.

The thresholds only route work into this skill. Semantic ownership and reviewability dominate raw line count.

## Non-negotiable anti-expansion rules

1. **Current-diff causality:** a blocking finding must be caused by the current section diff, or be a pre-existing defect that the diff newly depends on, exposes, or makes reachable.
2. **Monotonic scope:** after the feature/section contract is frozen, implementation and review may simplify or narrow it but may not enlarge it without an explicit owner decision. Repetition by multiple reviewers does not create authority.
3. **No review-authored requirements:** reviewers cannot enlarge the feature contract, supported environment, threat model, compatibility promise, durability promise, or rollout obligation.
4. **No automatic mechanism growth:** a new registry, service, persistence layer, background worker, parser framework, global analyzer, CI governance rule, security control, or public configuration surface requires an explicit plan/repository anchor. Reviewer preference is not an anchor.
5. **No repeated full rediscovery:** each section gets one `INITIAL_BOUNDED` review. Repairs use `REPAIR_DELTA`. Acceptance uses one `FINAL_BOUNDED` review.
6. **No process-only rework:** workflow schema, artifact format, fingerprint, review template, or skill-version changes do not invalidate accepted code, tests, or review evidence.
7. **No evidence-only descendants:** do not create a new section solely to rebuild review lineage, move a test earlier in Git history, satisfy a new artifact format, or prove that accepted ancestors were “clean.”
8. **No automatic clean-room retry:** preserve correct current work. Restart from an older base only after a concrete diagnosis proves the implementation direction itself is wrong and cannot be simplified in place.
9. **Proportional validation:** targeted checks after repairs, section/package checks before final review, and broad repository/application checks at integration. Do not rerun the broadest suite after every local edit.
10. **Review is not audit:** unchanged code may be inspected only to establish causality, reachability, contract reality, or direct regression risk. Unrelated repository defects are out of scope.
11. **Inaction is valid:** a clean review may return no finding. Never manufacture work to justify a reviewer invocation.

## Durable artifacts

Use these paths unless repository rules define equivalents:

```text
.agent-work/
├── PLAN-FULL.md
├── PLAN.md
├── FEATURE-STATE.md
├── sections/
│   ├── S01-CONTRACT.md
│   ├── S01-HANDOFF.md
│   └── ...
├── reviews/
│   ├── S01-REVIEW.md
│   ├── S01-CANDIDATES.md       # transient; overwrite or delete
│   └── ...
├── replans/
│   └── S01-g01-DIAGNOSIS.md
└── plans/
    └── {YYYYMMDD-HHMM}_FULL.md
```

`PLAN-FULL.md`, the current section contract, and `FEATURE-STATE.md` are authoritative. `S01-REVIEW.md` is one compact ledger for initial findings, delta closures, final verification, and residual risk. Do not create separate durable RAW/ADMISSION/state commits for every reviewer call.

## Load references progressively

- Read [references/section-planning.md](references/section-planning.md) before creating or changing the section graph.
- Read [references/bounded-review.md](references/bounded-review.md) before the first section review or any repair loop.
- Read [references/scope-control.md](references/scope-control.md) when security, persistence, compatibility, generalized tooling, test infrastructure, or over-design is possible.
- Read [references/recovery-and-migration.md](references/recovery-and-migration.md) at a hard cap or when adopting this skill mid-feature.
- Read [references/integration-and-testing.md](references/integration-and-testing.md) before checkpoints, final integration, or broad validation.
- Read [references/artifact-schemas.md](references/artifact-schemas.md) when creating or updating artifacts.

## Core state machine

```text
PREFLIGHT
  -> FEATURE_SCOPE
  -> SECTION_GRAPH
  -> OPTIONAL_PLAN_CHECK
  -> FREEZE_ONE_SECTION
  -> IMPLEMENT_MINIMUM_CHANGE
  -> LOCAL_VALIDATE
  -> REVIEW_INTENSITY
       -> MECHANICAL -> CLEAN_A_FROM_DETERMINISTIC_CHECKS
       -> BOUNDED_OR_HIGH_RISK -> INITIAL_BOUNDED_REVIEW   # once per stable baseline
            -> no blockers ----------------------┐
            -> admitted blockers -> REPAIR_DELTA*│
                                                  v
                                         CLEAN_A_CLOSURE
                                                  |
                                                  v
                                         FINAL_BOUNDED_REVIEW
       -> clean --------------------------> SECTION_ACCEPTED
       -> new diff-caused blocker -> REPAIR_DELTA -> FINAL_BOUNDED_REVIEW
       -> owner decision -> BLOCK
       -> more than 5 repair waves -> HARD_CAP_DIAGNOSIS

HARD_CAP_DIAGNOSIS
  -> BACKUP_CURRENT_TIP
  -> @sol_max CLASSIFICATION
       -> CONTINUE_CURRENT
       -> SIMPLIFY_CURRENT
       -> SPLIT_REMAINING
       -> REBOUND_OWNER
       -> REPAIR_EVIDENCE
       -> RESTART_FROM_BASE              # last resort only
  -> MINIMAL_PLAN_UPDATE
  -> RESUME_WITH_PRESERVED_EVIDENCE

ALL_SECTIONS_ACCEPTED
  -> CROSS_SECTION_INTEGRATION_REVIEW
  -> FULL_FEATURE_VALIDATE
  -> MERGE_READINESS
  -> ARCHIVE
```

Advance only when the corresponding code-visible evidence exists. Agent declarations are not gates.

## Phase 0: Preflight and feature scope

1. Inspect repository rules, architecture sources, current branch, `git status`, relevant recent commits, build/test entry points, and available environment.
2. Freeze the exact `feature_base`.
3. Create `PLAN-FULL.md` from the bundled template and record only:
   - requested outcome and observable behavior;
   - existing repository invariants and authoritative constraints;
   - explicit non-goals and unsupported environments;
   - ownership/state boundaries;
   - compatibility, migration, rollout, rollback, and cleanup actually required;
   - feature acceptance criteria and tiered validation;
   - structural changes explicitly allowed by the requirement.
4. Do not add a universal threat model or generalized durability model. Record risk boundaries only when the feature or repository already makes them relevant.
5. If integration or an external seam is uncertain, schedule a minimal probe/walking skeleton before designing a complete registry, state machine, framework, or persistence system.
6. When the feature is remediation of an audit, freeze the accepted audit finding IDs before implementation. Section review verifies those repairs and the repair diff; it does not continue the repository audit. New unrelated pre-existing concerns go to a separate audit backlog.
7. In `EXECUTE_WITH_COMMITS`, create an isolated feature branch/worktree before product-code implementation.

### Mid-feature adoption

When this skill is introduced after work has started:

- preserve current product code, accepted sections, tests, and review conclusions;
- adopt the new workflow prospectively from the current section/head;
- do not migrate old review files merely to satisfy a new template;
- do not replay accepted predecessor reviews or checkpoints unless current product code changed their contract;
- treat missing new-format metadata as legacy format, not as evidence failure;
- use one bounded final review when the current section's prior coverage cannot be reconstructed economically.

## Phase 1: Divide into minimal behavior sections

Create the initial section graph before implementation. Prefer:

1. a walking skeleton or real seam probe when architecture depends on uncertain integration behavior;
2. vertical slices with one observable increment and one primary owner;
3. expand-migrate-contract stages only when compatibility actually requires them;
4. cleanup after consumers have moved and evidence proves the old path is unused.

Every section must define:

- one coherent goal and observable increment;
- exact dependency/predecessor relationship;
- expected changed owners, symbols, routes, workflows, and direct impact cone;
- explicit non-goals and deferred owners;
- existing invariants it must preserve;
- structural changes it is allowed to introduce;
- falsifiable acceptance criteria;
- targeted, section, and integration validation tiers;
- reset triggers that would make the section materially different.

A section is invalid when it is merely a directory/layer bucket, a generic governance initiative not requested by the feature, a test/evidence rehabilitation task whose tooling is not itself the user-requested outcome, or a vague “finish/integrate everything” bucket.

Use the helper when practical:

```bash
python {skill-dir}/scripts/section_plan.py validate .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py list .agent-work/PLAN-FULL.md
python {skill-dir}/scripts/section_plan.py extract \
  .agent-work/PLAN-FULL.md S01 --output .agent-work/PLAN.md
```

The validator checks durable markers, minimum headings, unique IDs, and dependency cycles. Its fingerprint is informational; a changed fingerprint alone never invalidates evidence.

### Plan check

Use at most one clean plan reviewer when the feature changes architecture/state ownership, crosses a genuinely high-risk boundary, or has an uncertain external seam. The reviewer checks contradictions, missing ownership, unbuildable ordering, and obvious over-design. It may not invent guarantees. Main-agent verification is sufficient for local corrections unless the behavior contract materially changes.

## Phase 2: Freeze and implement one section

For the next dependency-ready section:

1. Record exact `section_base` as the accepted predecessor head.
2. Extract only that section into `PLAN.md`.
3. Create `{ID}-CONTRACT.md` with goal, base, owners, direct impact cone, allowed structural changes, non-goals, acceptance criteria, and validation tiers.
4. Resolve real owner decisions before product code.
5. Choose review intensity: `MECHANICAL`, `BOUNDED`, or `HIGH_RISK`.
6. Update `FEATURE-STATE.md` with current section, base/head, status, review intensity, open findings, repair waves, and next action.

Review intensity:

- `MECHANICAL`: documentation/generated output/rename/local fixture or equally deterministic change with no behavioral, data, trust, concurrency, migration, public-contract, or state-owner boundary. Use deterministic checks plus one `FINAL_BOUNDED` review; skip separate initial discovery.
- `BOUNDED`: one coherent behavior owner with a bounded impact cone. Use normal initial/delta/final flow.
- `HIGH_RISK`: security/permission, persistence/migration, public schema/API, concurrency, destructive behavior, deployment, or state-owner change. Use the same flow with high-risk reviewers and explicit path evidence.

Default routing when available:

- ordinary implementation: [@sol_medium](subagent://sol_medium);
- high-risk implementation or repair: [@sol_high](subagent://sol_high);
- ordinary bounded initial/delta review: [@sol_high](subagent://sol_high);
- mechanical final review: [@sol_high](subagent://sol_high);
- high-risk initial or final review: fresh [@sol_xhigh](subagent://sol_xhigh);
- hard-cap diagnosis/recovery: [@sol_max](subagent://sol_max).

The implementer receives repository rules, feature outcome/invariants, `PLAN.md`, the section contract, exact base, and required checks. Require:

- the smallest code change satisfying the section contract;
- reuse of the existing owner/abstraction when it remains coherent;
- no future-section implementation;
- meaningful behavior, edge, and error regression tests;
- targeted checks first;
- one concise `{ID}-HANDOFF.md` with changed files, decisions, commands/results, limitations, and head.

If a new mechanism is not listed under allowed structural changes, stop and either use a local solution or obtain a real contract decision. Do not let an implementer “future-proof” the section.

In `EXECUTE_WITH_COMMITS`, commit the coherent implementation before review. Do not create separate commits for every state/ledger edit; archive review evidence with the next coherent repair or section-acceptance commit.

## Phase 3: Patchset-style section review

For `MECHANICAL`, use deterministic checks as Clean A and proceed directly to one `FINAL_BOUNDED` pass. If the reviewer finds a real semantic boundary, reclassify the section as `BOUNDED` or `HIGH_RISK` and run `INITIAL_BOUNDED`.

For delta verification, prefer reusing the initial reviewer session when available so reviewed coverage remains sticky. The repair agent must still be separate. If the reviewer session cannot be reused, pass the compact review ledger rather than reconstructing the whole feature. The final reviewer is always fresh.

### 3.1 Finding admission boundary

Classify every candidate as exactly one:

- `DIFF_CAUSED`: current section diff introduces the defect.
- `MERGE_BLOCKING_DEPENDENCY`: a pre-existing defect is newly depended on, exposed, or made reachable by the diff.
- `PREEXISTING_OUT_OF_SCOPE`: unrelated old defect; do not fix here.
- `SCOPE_PROPOSAL`: stronger product/security/durability/compatibility/governance promise; do not implement automatically.
- `DEFERRED_OWNER`: explicitly owned by a later section while the current intermediate state remains correct.
- `EVIDENCE_GAP`: an already-required behavior lacks adequate evidence; add only the smallest oracle.
- `NIT_DEBT`: non-blocking polish, preference, or bounded debt.

Only `DIFF_CAUSED`, `MERGE_BLOCKING_DEPENDENCY`, and a contract-required `EVIDENCE_GAP` block by default.

For maintainability, materiality requires the current diff to create or materially worsen an ownership split, circular dependency, duplicated authoritative path, unsafe state machine, or similarly concrete defect risk. Preference for a cleaner abstraction is `NIT_DEBT` or `SCOPE_PROPOSAL`.

A blocking finding must establish all five:

1. changed hunk or changed contract causing/newly relying on the issue;
2. reachable trigger in the frozen supported environment;
3. existing requirement, invariant, or repository rule violated;
4. material consequence;
5. smallest repair remains inside the current owner without adding an unapproved guarantee.

For security findings, additionally identify the current asset, actor/capability, entry point, trust boundary, and preconditions. A hypothetical new actor, deployment, tenant model, malicious same-UID process, arbitrary in-process object, or stronger attacker is `SCOPE_PROPOSAL` unless already authoritative.

The main agent owns admission. Reviewer prose is a candidate set, not a contract amendment. Do not copy rejected proposals into `PLAN-FULL.md`, descendants, tests, or repair prompts.

### 3.2 `INITIAL_BOUNDED`

Run exactly one initial full review over `section_base..section_head` plus the direct semantic impact cone. Use the bundled review request. The reviewer must:

- inspect all changed behavior once through relevant correctness/risk lenses;
- batch material root causes before repair;
- report only current-diff findings under the admission rules;
- avoid repository audit, future-proofing, and generic governance/tooling proposals;
- record reviewed coverage so unaffected conclusions can be retained.

Write the authoritative classification and coverage summary into `{ID}-REVIEW.md`. Use `{ID}-CANDIDATES.md` only as transient reviewer output; overwrite or delete it after triage.

If no blocker is admitted, `Clean A` is satisfied by the implementation evidence and initial bounded review. Proceed to `FINAL_BOUNDED`.

### 3.3 `REPAIR_DELTA`

Freeze admitted root-cause IDs and acceptance criteria. Batch compatible findings into the smallest coherent repair wave.

After each repair, review only:

- `previous_reviewed_head..current_head`;
- unresolved admitted finding IDs;
- direct callers/callees/contracts/tests whose prior conclusion the repair invalidated;
- new behavior introduced by the repair.

Retain all unaffected initial coverage. A delta reviewer may admit a new blocker only when the repair delta caused it, made it reachable, or invalidated the earlier evidence. It may not reopen the original section under a different lens.

Run targeted checks for the repaired owner. Update the single review ledger. When all admitted findings are closed and required targeted/section checks pass, record:

```text
Clean A — closure evidence satisfied
```

A repair wave is one coherent batch of admitted root-cause classes plus its code fix and delta verification. The initial reviewer call, final reviewer call, repeated wording, rejected scope proposals, and tool retries do not count as repair waves.

### 3.4 `FINAL_BOUNDED`

Use one fresh reviewer after `Clean A`. Give it the current complete section diff, frozen contract/non-goals, direct impact cone, current checks, and a concise list of closed root-cause IDs. Do not give it rejected scope proposals or prior persuasive narratives.

The final reviewer checks:

- the complete current diff against the frozen contract;
- the highest-risk changed path end to end;
- repair impact cones;
- accidental scope or mechanism growth;
- section/package evidence.

It must not perform a repository audit or require a stronger contract. If it finds no new blocking root-cause class, record:

```text
Clean B — independent final evidence satisfied
```

Then mark the section `SECTION_ACCEPTED`.

If it finds a new admissible blocker, repair it through `REPAIR_DELTA`, then rerun only `FINAL_BOUNDED`. Do not restart the entire initial discovery unless a reset trigger fires.

### 3.5 Full-reset triggers

Reset to a new `INITIAL_BOUNDED` baseline only when a repair goes beyond the frozen contract or invalidates most prior coverage by materially changing one of:

- public or serialized API/schema;
- authorization, tenant isolation, or trust boundary;
- persistence, migration, durability, or recovery contract;
- state ownership or concurrency semantics;
- destructive, deployment, rollout, or rollback semantics;
- supported environment or section goal;
- most of the section's behavior/architecture.

Do not reset because a plan/review template changed, a fingerprint changed, tests were added, line numbers moved, HEAD advanced by a local repair, a new skill version was installed, or another reviewer might inspect a different lens.

## Phase 4: Five-wave hard-cap recovery

Allow up to five admitted repair waves for one stable section boundary. The fifth wave is repaired and delta-verified normally. Enter hard-cap diagnosis only when:

- a sixth independent root-cause class would require another repair wave;
- a repair cannot close without changing the section goal/owner/architecture; or
- the loop is oscillating or repeatedly reopening the same root cause.

Do not trigger hard-cap recovery merely because the fifth reviewer invocation found a small local omission.

### 4.1 Preserve without discarding

1. Record current `section_base`, `section_head`, five waves, open findings, checks, and rejected scope proposals.
2. In `EXECUTE_WITH_COMMITS`, ensure coherent current work is committed without unrelated user changes.
3. Create a backup ref without switching:

```text
codex/backup/{feature-slug}-{section-id}-g{generation}-{YYYYMMDD-HHMMSS}
```

4. Write `{ID}-g{generation}-DIAGNOSIS.md` using the bundled template.

The backup is a recovery point, not a command to abandon current correct work.

### 4.2 Invoke `@sol_max`

Give a clean [@sol_max](subagent://sol_max):

- current section goal/contract, base/head, and diff summary;
- all admitted root-cause classes and repair results;
- current open blocker and test evidence;
- structural changes already present and their requirement anchors;
- rejected scope proposals in a clearly non-authoritative appendix;
- explicit instruction not to implement product code.

Require exactly one recovery classification:

- `CONTINUE_CURRENT`: architecture is sound; authorize one new bounded repair plan on current code.
- `SIMPLIFY_CURRENT`: remove review-created or unanchored mechanisms and return to the minimum sufficient design.
- `SPLIT_REMAINING`: split only unresolved product behavior into at most two independently shippable descendants while preserving already-correct current work.
- `REBOUND_OWNER`: move unresolved behavior to the correct existing owner/section and update only affected dependencies.
- `REPAIR_EVIDENCE`: fix the oracle/environment in the current section; do not create a test-only descendant.
- `RESTART_FROM_BASE`: last resort when the implementation direction or threat model is demonstrably wrong and in-place simplification would preserve most of the wrong design.

Technical recovery proceeds without asking whether to continue. Ask only when recovery requires a new product guarantee, supported environment, compatibility policy, threat model, migration meaning, or rollout decision.

### 4.3 Recovery constraints

- Default to `CONTINUE_CURRENT` or `SIMPLIFY_CURRENT`; preserve verified repairs.
- `SPLIT_REMAINING` may add at most two active descendants and may not create process/evidence-only sections.
- Do not re-review accepted predecessors or rebuild “clean evidence lineage.”
- Do not cherry-pick nothing by default; keep current valid code unless `RESTART_FROM_BASE` is justified.
- `RESTART_FROM_BASE` must state which architectural assumptions are wrong, which current mechanisms will be discarded, and why bounded reversion/simplification is insufficient.
- One automatic structural recovery (`SPLIT_REMAINING`, `REBOUND_OWNER`, or `RESTART_FROM_BASE`) is allowed per original section. A second structural recovery requires a real owner/architecture decision rather than blind recursive splitting. Non-structural `CONTINUE_CURRENT`, `SIMPLIFY_CURRENT`, or `REPAIR_EVIDENCE` may proceed automatically.
- Update only the affected section/dependency entries in `PLAN-FULL.md`. Do not rewrite the whole feature plan or invalidate unaffected fingerprints/evidence.

## Phase 5: Integration checkpoints and final gate

Run a targeted checkpoint only when a later section begins consuming a new public contract, schema, permission boundary, state owner, queue, deployment path, or compatibility stage.

Checkpoint review verifies composition and representative paths; it does not reopen every accepted local line. An accepted section is invalidated only when changed product code or observed combined behavior disproves its contract.

After all sections are accepted, run one fresh `$code-review` integration pass over `feature_base..feature_head`, using the bundled integration request. Focus only on:

- original feature outcome and non-goals;
- emergent cross-section API/schema/state/permission/ordering/error behavior;
- migration, compatibility, rollout, rollback, cleanup, and observability actually required;
- representative end-to-end paths;
- branch-scope integrity and residual risk.

Do not repeat local section review or upgrade the feature into a repository audit. Repair integration findings in bounded deltas and rerun only invalidated integration evidence.

Run the broadest deterministic suite/build/browser/application checks once at final integration unless repository rules require otherwise. State readiness as `mergeable`, `not-mergeable`, or `insufficient-evidence`.

## Phase 6: Archive and report

1. Update `FEATURE-STATE.md` with section base/head, Clean A/Clean B, admitted findings, repair waves, recovery decisions, checks, and residual risk.
2. Delete transient `PLAN.md` only after its section is accepted, replaced, or abandoned with durable state.
3. Overwrite/delete transient `*-CANDIDATES.md`; preserve the compact authoritative `*-REVIEW.md` ledger.
4. Archive `PLAN-FULL.md` to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md` after final reporting.
5. Do not create a separate commit for every review-state edit. Commit/archive process artifacts at coherent section acceptance, recovery, or final-feature boundaries.
6. Report in Chinese by default: feature result, section status, admitted defects fixed, scope proposals rejected/deferred, checks, recovery events, residual risk, merge readiness, and maintainability judgment.

## Final rules

- One implementer works on one current section at a time.
- One initial bounded review, delta-only repair verification, one final bounded review.
- Two evidence types are required: `Clean A` closure and `Clean B` independent final verification; two repeated full clean scans are not required.
- Only current-diff or newly depended-on material defects block.
- Review-created scope proposals never enter repair prompts or descendant plans without owner approval.
- Up to five repair waves; the fifth finding is repaired normally.
- Hard-cap recovery preserves valid current work and diagnoses before splitting or restarting.
- Skill/artifact schema changes never retroactively invalidate product evidence.
- Section acceptance is provisional; only the final cross-section gate establishes feature merge readiness.
