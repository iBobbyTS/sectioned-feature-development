# Section Planning

## Contents

1. [Purpose](#purpose)
2. [Choose the first slice](#choose-the-first-slice)
3. [A valid section](#a-valid-section)
4. [Structural allowance](#structural-allowance)
5. [Boundaries and deferred work](#boundaries-and-deferred-work)
6. [Invalid section patterns](#invalid-section-patterns)
7. [Plan-review criteria](#plan-review-criteria)
8. [Examples](#examples)

## Purpose

Sectioning reduces cognitive and integration risk only when each section represents one coherent behavior increment. Splitting by directory, layer, or evidence artifact can make the plan longer without making the change safer.

The plan should answer:

- What did the user actually request, in their own words?
- What is the smallest end-to-end behavior that satisfies it?
- What observable behavior becomes true after this section?
- Which external authority makes this section necessary, and why is a smaller existing path insufficient?
- Which existing owner is responsible?
- What exact code and semantic impact cone may change?
- Which behavior is deliberately not part of this section?
- What evidence is sufficient to accept it?

## Choose the first slice

When an external seam or architecture assumption is uncertain, begin with the smallest real probe or walking skeleton that can falsify the assumption.

Examples:

- Observe the actual request metadata shape before building a registry around it.
- Exercise one canonical provider call before creating a general provider framework.
- Modify one representative route and reload flow before building a whole-repository URL analyzer.
- Prove the current persistence owner and failure behavior before introducing an outbox or journal.

A probe should produce durable knowledge or a minimal production path. It should not become a second framework.

## A valid section

A section should normally have:

- one primary behavior owner;
- one coherent outcome;
- one authority anchor outside the plan itself and a necessity statement tied to the minimum feature outcome;
- one bounded changed contract;
- one frozen scope manifest separating allowed-to-edit owners from inspect-only dependency paths and explicit exclusions;
- one direct semantic impact cone;
- one review intensity (`MECHANICAL`, `BOUNDED`, or `HIGH_RISK`);
- one set of targeted tests;
- no undocumented dependency on a future section for correctness.

A section may touch multiple files and layers when those edits are required for one vertical behavior. File count alone does not define reviewability.

The section graph is not allowed to create its own requirements. A downstream section cannot be justified only because an upstream plan promised a new UI, proof harness, compatibility layer, status surface, or generalized mechanism. Trace it back to user intent, a current repository/production obligation, or a demonstrated correctness dependency; otherwise remove it from the feature.

Prefer sections such as:

- “Parse and normalize the quota signal at the existing API boundary.”
- “Keep one turn bound to its selected account until a confirmed quota terminal signal.”
- “Remove report month/year from the page URL while preserving reload defaults.”
- “Expose DeepSeek's single-query capability through the existing provider projection.”

Avoid sections such as:

- “Backend changes.”
- “Security hardening.”
- “Build a generalized URL governance system.”
- “Rehabilitate review evidence.”
- “Final cleanup and everything else.”

## Structural allowance

Every section contract includes an **Allowed structural changes** list. This is an authorization boundary, not a prediction.

List only mechanisms required by the approved behavior, for example:

```text
- Extend the existing AccountRegistry with one per-turn affinity map.
- Add one provider capability enum value and reuse the existing projection path.
- Add explicit route-level regression tests in the existing test module.
```

When the list is empty, the implementer may make local edits and small local helpers inside the allowed-to-edit manifest but may not add a new service, registry, persistence layer, background worker, parser framework, global analyzer, CI policy, public config surface, or security subsystem.

A reviewer cannot add an item to this list or expand the allowed-to-edit manifest. It may inspect an unlisted dependency only through a recorded causal chain from changed code. A required new mechanism or repair owner is either:

- already implied by an authoritative repository contract and accepted by the main agent; or
- a product/architecture decision for the owner.

## Boundaries and deferred work

Write non-goals as concrete exclusions, not generic “out of scope” prose.

Good examples:

- No multi-process durability or restart persistence.
- No replay after downstream bytes have been emitted.
- No same-UID hostile process model.
- No whole-repository source analyzer or permanent CI prohibition.
- No public Admin DTO exposure until S04.

Deferred work must have a named later owner and a correct intermediate state. A reviewer may block on deferred work only when the current state is already incorrect or unsafe before the later section runs.

## Invalid section patterns

### Process-only section

Do not create a section only to:

- migrate PLAN or review schema;
- recompute fingerprints;
- copy legacy review files;
- move a test earlier in Git ancestry;
- obtain a “clean lineage”;
- re-prove accepted predecessor behavior unchanged by product code.

### Governance expansion

A local feature does not automatically authorize a repository-wide analyzer, policy, registry, or CI guard. Prefer explicit regression tests for the changed routes/owners.

### Threat-model expansion

A test harness, local script, single-user tool, or private directory does not automatically require protection against arbitrary in-process objects, same-UID hostile processes, multi-tenant access, or malicious filesystem rebinding.

### Layer-only split

Splitting “models,” “services,” and “UI” into separate sections may leave each section semantically incomplete. Prefer a vertical behavior slice unless compatibility staging requires a layer boundary.

## Plan-review criteria

Use one plan review only when architecture, state ownership, or a high-risk boundary is genuinely uncertain. The reviewer checks:

- every requirement has an owner and acceptance oracle;
- dependencies are acyclic;
- the first slice falsifies uncertain seams early;
- structural allowances are requirement-anchored;
- non-goals exclude foreseeable scope expansion;
- no section exists solely for process/evidence;
- testing is tiered rather than full-suite-per-edit;
- final integration covers only emergent cross-section behavior.

After local plan corrections, the main agent verifies them. Run another plan review only when the behavior contract or architecture materially changed.

## Examples

### Account quota switching

Better sequence:

1. Probe actual metadata and terminal signal path.
2. Add minimal per-turn affinity in the existing owner.
3. Add safe switch/replay only for confirmed quota exhaustion before output.
4. Integrate with UI/status if requested.

Do not start with a generalized scheduler, parser framework, persistent registry, or hostile-input model unless required.

Settings/status UI belongs in the feature only when explicitly requested or required by an existing repository product convention. A backend switch mechanism does not automatically authorize a configuration surface or monitoring dashboard.

### Hosted-search provider integration

Better sequence:

1. Exercise one official provider request/response seam.
2. Normalize the minimum result/citation/error contract in the existing provider owner.
3. Activate it through the existing configuration/public path required for actual use.
4. Add focused behavior tests and the repository's existing integration gate.

Do not create a standalone evidence publisher, hostile-object parser, credential-reconstruction proof system, custom compatibility program, or general provider framework unless an external authority independently requires it.

### URL state removal

Better sequence:

1. Remove internal UI state from representative routes.
2. Preserve explicit allowlisted functional query parameters.
3. Add route-level regressions and one browser flow.
4. Integrate across remaining named routes.

Do not add a whole-tree source detector or permanent URL grammar/CI governance system unless the owner requested that separate feature.
