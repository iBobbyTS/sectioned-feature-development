# Bounded Patchset Review

## Contents

1. [Review roles](#review-roles)
2. [Causality boundary](#causality-boundary)
3. [Finding classes](#finding-classes)
4. [Blocking proof](#blocking-proof)
5. [Initial bounded review](#initial-bounded-review)
6. [Repair-delta review](#repair-delta-review)
7. [Final bounded review](#final-bounded-review)
8. [Sticky coverage](#sticky-coverage)
9. [Reset rules](#reset-rules)
10. [Review packets](#review-packets)

## Review roles

The parent `$sectioned-feature-development` orchestrator owns scope, admission, repair waves, and acceptance. Each `$code-review` invocation is a **single review pass**. Do not let the child reviewer start its own repair loop, ask to continue after a cap, rewrite the section contract, or delegate the same review again.

Use:

- `INITIAL_BOUNDED`: one discovery pass over the stable section diff.
- `REPAIR_DELTA`: closure of frozen findings and repair-caused risk.
- `FINAL_BOUNDED`: one independent final pass over the current diff.
- `INTEGRATION`: emergent cross-section behavior only.

## Causality boundary

A section review asks:

> What material defect did this diff introduce, newly depend on, expose, or make reachable?

It does not ask:

> What else could be improved anywhere in the section, module, feature, or repository?

Unchanged code may be read to prove:

- execution reachability;
- the real contract or owner;
- direct callers/callees and side effects;
- regression impact;
- whether a proposed abstraction duplicates an existing one.

Unrelated defects in unchanged code are `PREEXISTING_OUT_OF_SCOPE`.

## Finding classes

### `DIFF_CAUSED`

The current section diff creates an incorrect behavior, regression, unsafe transition, contract mismatch, or material maintainability defect.

### `MERGE_BLOCKING_DEPENDENCY`

The defect existed before, but a necessary acceptance path now depends on, activates, serializes, or publicly exposes its faulty behavior. Incidental traversal through a shared entry point, proximity to changed code, or merely becoming easier to notice is insufficient. Repair only the smallest dependency needed for safe merge.

### `PREEXISTING_OUT_OF_SCOPE`

The defect existed before and current behavior does not depend on or change its reachability. It does not block this section.

### `SCOPE_PROPOSAL`

The concern requires a new product promise, supported environment, threat actor, durability/compatibility guarantee, generic framework, global analyzer, CI policy, or future-proofing mechanism. It is non-blocking unless the owner approves it.

### `DEFERRED_OWNER`

The behavior is assigned to a named later section and the current intermediate state remains correct.

### `EVIDENCE_GAP`

An already-required behavior lacks adequate evidence. Cite the exact acceptance-criterion ID or repository-required gate that existed before the review. The repair is the smallest test/oracle necessary to prove it—not a generalized harness or sandbox. A reviewer preference for stronger proof is `SCOPE_PROPOSAL` or `NIT_DEBT`.

### `NIT_DEBT`

Style, preference, polish, or bounded debt with no material merge risk.

## Blocking proof

A blocking finding must include:

| Field | Required evidence |
|---|---|
| Causality | Changed hunk/contract or repair delta that creates/newly relies on the issue |
| Reachability | Concrete trigger in the frozen supported environment |
| Authority | Existing requirement, invariant, repository rule, or established behavior |
| Materiality | Correctness, security, data, reliability, compatibility, or maintainability consequence |
| Bounded repair | Smallest fix remains inside the frozen allowed-to-edit owners and adds no unapproved guarantee |

Discard or downgrade a candidate when one field is missing. If a genuine blocker requires editing a new owner, the reviewer reports the causal chain and stops; only the main agent may amend the manifest or rebound ownership.

For security findings also require:

- protected asset;
- current actor and capability;
- entry point/data flow;
- trust boundary;
- preconditions;
- supported deployment.

Do not assume arbitrary same-UID attackers, malicious in-process Python objects, multi-tenant operation, hostile filesystem rebinding, multi-process writers, or untrusted archives unless authoritative project evidence supports them.

## Initial bounded review

Run once per stable section baseline.

The reviewer receives:

- exact `BASE..HEAD`;
- feature outcome and non-goals;
- section contract;
- frozen scope manifest: allowed-to-edit owners, inspect-only dependency paths, excluded mechanisms, and direct impact cone;
- relevant repository rules;
- required checks;
- output path for transient candidates.

The reviewer should:

1. inspect the entire current diff once;
2. select only risk lenses triggered by the changed behavior;
3. trace at least one critical changed path for medium/high-risk sections;
4. generate and falsify hypotheses before reporting;
5. batch root causes before repair;
6. record the files/symbols/contracts/path families reviewed;
7. for any inspection beyond the named cone, record the exact data/control/serialization/contract chain from a changed symbol and stop at the candidate—do not fan out recursively.

It must not:

- audit the repository;
- search for unrelated historical bugs;
- demand future-proofing;
- add a new threat model or compatibility promise;
- turn route-level regression into a generic analyzer;
- turn local persistence into an outbox/journal unless required;
- implement or repair findings itself.

## Repair-delta review

After repair, review only:

```text
PREVIOUS_REVIEWED_HEAD..CURRENT_HEAD
+ open finding acceptance criteria
+ conclusions invalidated by the repair
+ direct new behavior introduced by the repair
```

A delta reviewer may admit a new root cause only if the delta causes it, activates it on a necessary acceptance path, or invalidates earlier evidence. “I looked at another unchanged area this time” is not sufficient. The repair agent may edit only frozen repair owners; a needed new owner returns to the main agent before code changes.

The delta report should answer:

- Is each frozen finding closed?
- Did the repair introduce a direct regression?
- Which previous coverage entries became invalid?
- Which targeted checks prove closure?

Do not rescan the original section. Do not reset because HEAD changed.

## Final bounded review

Run after all admitted findings are closed and section/package checks pass.

Use a fresh reviewer. Give it:

- current complete section diff;
- frozen contract and non-goals;
- direct impact cone;
- current validation results;
- concise closed finding IDs and changed owners.

Do not give it rejected hypotheses or persuasive reviewer narratives.

The final reviewer is not another open-ended discovery pass. It verifies only:

- contract correctness of the final diff;
- one highest-risk end-to-end changed path;
- repair impact cones;
- accidental mechanism/scope growth;
- test sufficiency proportional to the section.

It reports only a new `DIFF_CAUSED`, tightly proven `MERGE_BLOCKING_DEPENDENCY`, or acceptance-criterion-anchored `EVIDENCE_GAP`. Any resulting repair counts toward the same cumulative five-wave section budget. A clean final pass is sufficient; do not require a second full clean pass.

## Sticky coverage

Record reviewed coverage in the section ledger:

- changed files and symbols;
- critical paths;
- contracts and invariants;
- triggered risk lenses;
- tests/experiments;
- explicit gaps.

Coverage remains valid until a repair changes the underlying evidence. Preserve unaffected entries across delta reviews and final review.

A new reviewer does not invalidate existing coverage merely because it has a different context or may choose another lens.

## Reset rules

Reset to another initial bounded review only when a repair materially changes:

- public/serialized API or schema;
- authorization, tenant isolation, or trust boundary;
- persistence, migration, durability, or recovery contract;
- state ownership or concurrency semantics;
- destructive/deployment/rollback behavior;
- supported environment or section goal;
- most of the section's architecture/behavior.

Do not reset for:

- local bug fixes;
- added targeted tests;
- line movement;
- plan/review schema changes;
- fingerprints;
- skill updates;
- different reviewer preference;
- evidence files moving in Git history.

## Review packets

Use the bundled `SECTION-REVIEW-REQUEST.template.md`. Key mode-specific instructions:

### Initial

```text
Mode: INITIAL_BOUNDED
Perform one single-pass diff review. Do not repair. Report only current-diff material defects.
```

### Delta

```text
Mode: REPAIR_DELTA
Review only REPAIR_BASE..HEAD, frozen finding IDs, and invalidated impact cone. Do not reopen unchanged scope.
```

### Final

```text
Mode: FINAL_BOUNDED
Independently verify the current complete diff and highest-risk changed path. Do not audit the repository or strengthen the contract.
```
