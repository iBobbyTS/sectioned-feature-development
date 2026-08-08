# Section Planning Guide

Use this reference to turn a large feature into independently implementable and mergeable increments without manufacturing abstractions merely to make the plan look modular.

## Contents

1. [Plan around outcomes](#1-plan-around-outcomes)
2. [Preferred section patterns](#2-preferred-section-patterns)
3. [Minimum-sufficient design](#3-minimum-sufficient-design)
4. [Section quality gate](#4-section-quality-gate)
5. [Dependency and ownership graph](#5-dependency-and-ownership-graph)
6. [Cross-section defects](#6-cross-section-defects)
7. [Parallel work](#7-parallel-work)
8. [Hard-cap recovery planning](#8-hard-cap-recovery-planning)
9. [Anti-patterns](#9-anti-patterns)

## 1. Plan around outcomes

A section is one self-contained behavior increment or one enabling seam needed by named later increments. It is not a folder, layer, agent allocation, or arbitrary line-count bucket.

Write the observable result first, then identify the minimum code path required to make it real and testable. A valid section normally has:

- one principal outcome;
- one finite set of owners/contracts;
- a valid intermediate repository/runtime state;
- a falsifiable oracle;
- explicit non-goals and deferred owners;
- a rollback or recovery path appropriate to its risk.

Prefer a smaller section when review would otherwise switch among unrelated workflows, threat models, data owners, or failure semantics. Do not make a section so small that it introduces an unused API or abstraction whose meaning cannot be reviewed in use.

## 2. Preferred section patterns

### Walking skeleton

Use when integration feasibility is uncertain. Build the thinnest real end-to-end path through intended boundaries, with a concrete validation route. Avoid production-scale breadth, generic frameworks, or polish.

### Vertical behavior slice

Default choice. Implement one behavior through only the layers necessary to expose and verify it. It may touch multiple modules; conceptual unity matters more than file count.

### Enabling refactor

Use only when a named later behavior cannot be implemented safely without a seam, authoritative owner, or characterization coverage. Preserve behavior and keep the refactor independently reviewable. Do not bundle broad cleanup.

### Expand–migrate–contract

Use for incompatible schemas, APIs, events, or shared state:

1. expand with a compatible new path;
2. migrate consumers/data/traffic incrementally;
3. contract only after evidence proves the old path is unused.

Name the contraction criterion before expansion so temporary dual paths do not become permanent.

### Branch by abstraction

Use for gradual implementation replacement when a stable seam already has semantic value. Introduce/verify the seam, route existing behavior through it, add the replacement, migrate, switch authority, then remove the old path and temporary seam when no longer needed.

Do not create an abstraction solely because large-feature guidance mentions this pattern.

### Feature-flagged increment

Use when deploy and exposure must be decoupled. Record owner, default behavior, on/off test matrix, rollout cohort, kill switch, and removal section. A flag does not excuse an invalid intermediate state or untested hidden path.

## 3. Minimum-sufficient design

For every nontrivial mechanism, write a complexity-budget row:

| Mechanism | Current anchor | Simpler alternative | Why insufficient | Removal condition |
|---|---|---|---|---|

A current anchor is one of:

- approved requirement or acceptance criterion;
- feature/section invariant;
- authoritative repository policy or existing public contract;
- demonstrated compatibility/migration constraint;
- reachable failure/security consequence inside the frozen assurance envelope.

The following are not anchors by themselves:

- “more robust”;
- “future-proof”;
- “industry best practice” without applicability evidence;
- a reviewer preference;
- a hypothetical actor/environment excluded by the contract;
- avoiding a possible future rewrite;
- making a section look architecturally complete.

Prefer existing extension points and local code until evidence justifies a shared helper, service, registry, configurable policy, persistence layer, generalized framework, or new security mechanism.

## 4. Section quality gate

### Coherence

- Can the goal be stated without unrelated “and also” clauses?
- Does one behavior or enabling seam explain the diff?
- Are structural moves and behavior changes separated when practical?

### Independence

- Are predecessor heads and runtime assumptions explicit?
- Can the section be implemented without inventing future contracts?
- Can it be reverted without reverting unrelated accepted work?

### Testability

- Is there a deterministic oracle for the main outcome?
- Are supported negative, boundary, and partial-failure paths named?
- Does the validation environment actually exercise the relevant trust boundary?

### Reviewability

- Can a fresh reviewer understand intent from the contract packet?
- Is the direct semantic impact cone finite and named?
- Are generated, mechanical, migration, and semantic changes distinguishable?

### Integrability

- Does the system remain buildable and operational after the section?
- Are compatibility and temporary states explicit?
- Is the next consumer or checkpoint named?

### Proportionality

- Does every new mechanism have an approved anchor?
- Is the assurance envelope proportional to artifact role and supported deployment?
- Are non-goals concrete enough to reject attractive generalizations?

## 5. Dependency and ownership graph

Use explicit edges:

- `requires`: implementation cannot start until predecessor acceptance;
- `integrates-with`: independently buildable work needing a checkpoint;
- `migrates-from`: a consumer/data move depends on an expanded path;
- `contracts`: cleanup follows migration evidence;
- `conflicts-with`: sections share an owner/contract and cannot proceed independently.

The graph must be acyclic. A cycle usually means the boundary is wrong or a common contract/walking-skeleton section is missing.

Avoid parallel sections that both modify the same schema, permission owner, state machine, central coordinator, migration, or public contract.

## 6. Cross-section defects

Do not confuse scope control with defect denial.

A candidate is `IN_SCOPE_REPLAN` when:

- approved behavior or an authoritative invariant is genuinely violated;
- the trigger is reachable in the supported model;
- the smallest correct repair crosses the current section boundary.

The main agent must preserve the finding, revise the section graph in bounded form, invalidate affected evidence, and retry. It must not classify the problem as scope creep merely because the repair touches another section.

By contrast, adding a new guarantee, threat actor, environment, compatibility promise, or generalized product is a `SCOPE_PROPOSAL` until approved.

## 7. Parallel work

Parallelize only when:

- dependencies are accepted;
- semantic owners/contracts are distinct;
- worktrees and generated artifacts are isolated;
- integration order and checkpoint are predetermined;
- conflicts can be resolved without choosing new semantics.

Parallel work increases throughput but also integration states and review load. Sequential execution is the safe default when boundaries are uncertain.

## 8. Hard-cap recovery planning

Use the five admitted review rounds as empirical evidence. Diagnose before choosing a recovery shape:

- `DEFECT_DENSITY` → split by behavior/root cause/oracle;
- `ASSURANCE_BOUNDARY_DRIFT` → simplify and replace, deleting unapproved mechanisms;
- `ARCHITECTURE_BOUNDARY_FAILURE` → rebound owners/contracts;
- `CONTRACT_AMBIGUITY` → obtain the exact owner decision;
- `EVIDENCE_FAILURE` → repair the oracle/environment.

Do not automatically split every failure. Recursive splitting of an inflated design preserves the wrong problem. `SIMPLIFY_REPLACE` may yield one smaller replacement leaf rather than multiple descendants.

Retry from the failed parent section's original base and re-derive code. Carrying repeatedly repaired code forward defeats the purpose of changing the boundary.

## 9. Anti-patterns

- One section per directory or technical layer.
- “Build a reusable framework” before a concrete second/third use.
- Review-discovered hypotheses copied into requirements without admission.
- Security controls against actors excluded by the supported deployment model.
- A final section named “integrate everything.”
- Feature flags without owners/removal criteria.
- Data migration, cutover, and old-path deletion in one opaque section.
- Splitting after implementation but keeping the same coupled code state.
- Treating more tests as proof when the tests encode an inflated contract.
- Using line count as the sole section boundary.
