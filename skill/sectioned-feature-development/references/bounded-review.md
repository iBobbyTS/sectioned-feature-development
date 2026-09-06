# Bounded Patchset Review

## Contents

1. [Review roles](#review-roles)
2. [Review assurance](#review-assurance)
3. [Causality boundary](#causality-boundary)
4. [Finding classes](#finding-classes)
5. [Blocking proof](#blocking-proof)
6. [Initial bounded review](#initial-bounded-review)
7. [Repair-delta review](#repair-delta-review)
8. [Final bounded review](#final-bounded-review)
9. [Sticky coverage](#sticky-coverage)
10. [Reset rules](#reset-rules)
11. [Review packets](#review-packets)

## Review roles

The parent `$sectioned-feature-development` orchestrator owns scope, admission, repair waves, and acceptance. Each `$code-review` invocation is a **single review pass**. Do not let the child reviewer start its own repair loop, ask to continue after a cap, rewrite the section contract, or delegate the same review again.

The plan reviewer must never code-review the same feature. The initial reviewer is distinct from the implementer/repairer and may be reused only for delta closure. The final reviewer is fresh and distinct from the plan reviewer, implementer, repairer, and initial/delta reviewer. Record stable task/session IDs; a profile label alone is not identity. The main agent may admit findings but may not implement or repair product code.

A reviewer runs against a frozen product/test head. No writer may edit the reviewed range until the reviewer completes or is explicitly cancelled. Do not start a later section until the current section is accepted, blocked, or abandoned.

Use:

- `INITIAL_BOUNDED`: one discovery pass over the stable section diff.
- `REPAIR_DELTA`: closure of frozen findings and repair-caused risk.
- `FINAL_BOUNDED`: one independent final pass over the current diff.
- `INTEGRATION`: emergent cross-section behavior only.

## Review assurance

Review intensity selects breadth/model; review assurance selects how much independent evidence is required. Record `ONE`, `TWO`, or `AUTO -> <resolved>` in the plan, contract, state, request, and ledger.

### `ONE`

- One clean independent bounded reviewer outcome is sufficient.
- A clean `INITIAL_BOUNDED` may accept a bounded/high-risk section after required checks.
- If initial review finds blockers, close them with `REPAIR_DELTA`, then require one fresh clean `FINAL_BOUNDED`; the earlier non-clean initial does not force another clean pass.
- Mechanical sections use deterministic checks plus one `FINAL_BOUNDED`.

### `TWO`

- Preserve two evidence types: `Clean A` from initial/closure evidence plus fresh `Clean B` from `FINAL_BOUNDED`.
- It does not require two repeated full clean scans after a repair.

### Choosing assurance

An explicit owner `ONE`/`TWO` choice wins unless repository policy mandates stronger evidence. Otherwise `AUTO` resolves to `TWO` for persistence/schema/migration; money/security/auth/permissions/credentials; shared-state concurrency, retry/replay/cancellation/background/process lifecycle; business-critical time/date eligibility; public API/protocol compatibility or irreversible external side effects; routing/failover/quota/sticky ownership; two or more runtime/process boundaries or three or more behavioral owners; a hard-to-bound cone; or material incident risk. Use `ONE` otherwise.

A small local fix can remain `ONE` inside a sensitive module when it touches at most two owners, adds no schema/public contract/persistence/state mutation/retry/concurrency, has an exact regression reproduction, and is roughly at most 80 behavioral lines. Record reasons; do not infer assurance from repository size or total test count.

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

Discard or downgrade a candidate when one field is missing. If a genuine blocker requires editing a new owner, the reviewer reports the causal chain and stops; only the main agent may amend the manifest or rebound ownership. If the repair would create a second authoritative semantic rule or leave sibling callers wrong, report a bounded foundational-versus-local owner decision rather than silently widening. Cosmetic helper extraction remains non-blocking.

For security findings also require:

- protected asset;
- current actor and capability;
- entry point/data flow;
- trust boundary;
- preconditions;
- supported deployment.

Do not assume arbitrary same-UID attackers, malicious in-process Python objects, multi-tenant operation, hostile filesystem rebinding, multi-process writers, or untrusted archives unless authoritative project evidence supports them.

## Initial bounded review

Run at most once per stable section baseline.

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

Run after all admitted findings are closed and section/package checks pass when any repair occurred, when assurance is `TWO`, or for a mechanical section. Omit it only when a bounded/high-risk `ONE` section has a clean initial review and no later product/test change.

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

It reports only a new `DIFF_CAUSED`, tightly proven `MERGE_BLOCKING_DEPENDENCY`, or acceptance-criterion-anchored `EVIDENCE_GAP`. Any resulting repair counts toward the same cumulative five-wave section budget. A clean final pass is sufficient. Under `ONE` after repair, it is the single required clean reviewer outcome; under `TWO`, it is `Clean B`. Do not require another full clean pass.

## Sticky coverage

Record reviewed coverage in the section ledger:

- changed files and symbols;
- critical paths;
- contracts and invariants;
- triggered risk lenses;
- tests/experiments;
- explicit gaps.

Coverage remains valid until a repair changes the underlying evidence. Preserve unaffected entries across delta reviews and final review.

A new reviewer does not invalidate existing coverage merely because it has a different context or may choose another lens. A fresh reviewer also does not require rerunning identical successful validation against the same code head; independent analysis and CI rerun are separate decisions.

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

## Final-head evidence

Before section or feature readiness, record the exact product/test head covered by the required clean reviewer outcome and checks. Later process/docs-only commits do not invalidate it. Any later product/test change requires a bounded review/check closure for only the changed range; it does not reopen accepted predecessors or the full initial review.

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

## Delegated companion contract

The installed companion uses `context=DELEGATED_PASS`, protocol `sfd-delegated-review/4.2` (legacy `sfd-delegated-review/4.1` and `sfd-delegated-review/4.0` are readable for active historical packets). Parent alone owns admission/acceptance; reviewer returns CLEAN, MATERIAL_CANDIDATES, or INSUFFICIENT_EVIDENCE. ONE with an admitted material repair requires delta closure plus a fresh final full pass; TWO requires covered baseline/closure plus fresh independent final evidence. `unproven_composition` controls whether another integration reviewer is needed, not whether required checks run.
