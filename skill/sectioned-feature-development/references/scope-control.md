# Scope and Over-Design Control

## Contents

1. [Authority hierarchy](#authority-hierarchy)
2. [Active-contract sanitation](#active-contract-sanitation)
3. [Minimum sufficient design](#minimum-sufficient-design)
4. [Security and threat models](#security-and-threat-models)
5. [Persistence and recovery](#persistence-and-recovery)
6. [Generic governance and analyzers](#generic-governance-and-analyzers)
7. [Testing infrastructure](#testing-infrastructure)
8. [Scope-growth signals](#scope-growth-signals)
9. [Correction protocol](#correction-protocol)

## Authority hierarchy

Use this order:

1. explicit user-approved behavior and decisions;
2. repository-local rules and current production contracts;
3. accepted feature and section contracts;
4. current code/tests as evidence of established behavior;
5. reviewer suggestions.

Reviewer suggestions cannot override levels 1–4. They are candidates to classify, not requirements to implement. The approved scope is monotonic during implementation/review: it may be narrowed or simplified, but it may grow only through an explicit owner decision. Repeated reviewer agreement does not create authority.

## Active-contract sanitation

When adopting this skill mid-feature, preserve accepted code and evidence but inspect the active, unaccepted contract before continuing. For every guarantee, oracle, structural allowance, supported actor/environment, and blocker, record its authority at levels 1–4 above.

- Keep anchored items.
- Downgrade reviewer-authored, unanchored items to `SCOPE_PROPOSAL` and remove them from repair/test obligations.
- Do not reopen accepted sections merely because a newer workflow uses different artifacts.
- Do not let an old over-expanded contract manufacture a new `EVIDENCE_GAP`.

This is contract sanitation, not a new audit or plan-review cycle.

## Minimum sufficient design

For audit-remediation features, freeze the accepted audit finding IDs before implementation. Code review verifies the repair diff; unrelated pre-existing findings return to a separate audit backlog instead of expanding the active feature.


A design is sufficient when it satisfies the frozen behavior and repository obligations with the smallest coherent ownership change.

Before adding a mechanism, ask:

- Which approved requirement needs it?
- Which existing owner cannot satisfy that requirement locally?
- What simpler existing path was considered?
- Does this mechanism create another API, lifecycle, state machine, migration, or failure mode?
- Will the feature remain correct if the mechanism is omitted?

If the last answer is yes, omit it.

Complexity estimates are diagnostic, not validity gates. Exceeding an estimate triggers a simplification check, not automatic rollback or clean-room retry.

## Security and threat models

Security review must match the actual artifact and deployment.

Freeze only:

- asset;
- current actor/capability;
- entry point and trust boundary;
- supported deployment/concurrency model;
- guarantees already required.

Examples of likely scope proposals rather than blockers:

- protecting a private test harness against arbitrary malicious in-process objects;
- defending a single-user local directory against a same-UID hostile process;
- adding multi-tenant isolation to a non-multi-tenant tool;
- adding multi-process writer coordination to a single-writer service;
- sanitizing arbitrary exception object graphs when the component never receives secrets;
- hardening against arbitrary malicious archive formats when inputs are internal/trusted.

Use ordinary secure defaults proportional to the artifact—private permissions, atomic replace, static error messages, cleanup—without turning them into a general capability/security framework.

## Persistence and recovery

Do not infer transaction journals, outboxes, manifests, restart recovery, or historical reconstruction from a local consistency bug.

Add persistence/recovery machinery only when:

- an authoritative requirement requires restart durability or multi-step atomicity;
- the existing repository architecture already uses that mechanism for the same owner;
- a simpler local transaction/ordering fix cannot satisfy the contract.

A reviewer may identify data loss or corruption caused by the diff. It may not silently upgrade the product to stronger durability or recovery semantics.

## Generic governance and analyzers

A feature-specific regression does not automatically justify:

- whole-tree static source inventory;
- custom AST or grammar framework;
- runtime detector/coordinator;
- global CI prohibition;
- permanent policy registry;
- repository-wide “future regression prevention” system.

Prefer:

- explicit tests for changed routes/owners;
- existing lint/static tools;
- one representative integration/browser flow;
- documentation in the existing owner.

A generalized governance system is a separate feature requiring explicit scope, ownership, rollout, and maintenance commitment.

## Testing infrastructure

Tests should prove current behavior, not become a new product.

Do not add a test-only section or generalized sandbox merely to satisfy review evidence. Keep the smallest oracle with the behavior section.

A test-only change should not force broad product re-review unless it changes shared setup, global fixtures, build behavior, or production code generation.

Do not require a test commit to appear before a product commit in Git history. Current code plus current deterministic results are the evidence.

## Scope-growth signals

Stop and classify when any appears:

- section count grows because reviewers propose new guarantees;
- a local change creates a new registry/service/framework not in the plan;
- tests or review artifacts exceed the product diff in complexity;
- repeated work is about fingerprints, lineage, provenance, or template compliance rather than behavior;
- reviewers discuss unsupported actors/environments more than current users/flows;
- a local route/service fix turns into whole-repository governance;
- accepted predecessor sections are reopened without product-code change;
- a small fifth-round omission triggers full rearchitecture or clean-room rebuild.

## Correction protocol

When scope drift is detected:

1. Freeze the user-approved outcome and current correct behavior.
2. Classify each added mechanism as requirement-anchored or review-created.
3. Remove or simplify review-created mechanisms before splitting them into more sections.
4. Restore the proportional environment/threat model.
5. Preserve validated product fixes that remain aligned.
6. Re-run only tests/review invalidated by the simplification.
7. Record rejected proposals as non-blocking notes; do not add them to descendant plans.

Use `SIMPLIFY_CURRENT` at hard cap when over-design is the dominant cause.
