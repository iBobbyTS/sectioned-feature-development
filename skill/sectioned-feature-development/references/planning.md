# Requirements and executable planning

## Portable grill-me output

A fresh planner can consume the confirmed final Requirements Contract without the interview. It must contain the goal, actors, in/out scope, required and rejected behavior, edge/error/conflict/recovery semantics, existing-data compatibility, exact examples/corrections, acceptance oracles, confirmed decisions, assumptions, planner discretion and genuinely unresolved blockers. Include confirmation provenance and requirement IDs; mark superseded guidance explicitly.

Keep raw grill dialogue in the audit-only provenance store. Do not turn a prior PLAN statement into human authority just because grill-me called it settled. When the contract omits a high-impact semantic decision, return to the user; when it omits a discoverable source fact, investigate it. Do not conduct a second full grill interview automatically.

## Plan author packet

Confirmed contract; repository rules; current base/branch; source/owner map; constraints; relevant test commands; exclusions. No old reviewer narrative or full session logs. `astra_xhigh` authors a Chinese PLAN-FULL with the template's machine block and concise behavior sections.

Separate by independently verifiable outcome, not by directories or model names. Shared producers/contracts/migrations land before dependent consumers. Split different difficulty only where an interface is already valid and the extra review/integration cost is smaller than the delegated work. Never split schema/atomic-state semantics just to create parallel workers.

Every section specifies:
- requirement IDs, invariant and canonical owner;
- `depends_on`, approved base rule, expected deliverable and acceptance;
- exact `write_paths` and read dependencies (relative paths or directory prefixes, not ambiguous globs);
- mutated/consumed contracts and exclusive test resources;
- whether parallel execution is permitted and why;
- selected implementation profile, observable routing features and confidence;
- targeted check IDs and failure-state oracle;
- review assurance and merge/integration obligations.

Every phase has a concurrency policy: discovery may parallelize independent questions; plan author/reviewer are sequential; independent ready sections may parallelize; a section's writer/reviewer never overlap; feature-branch integration is serialized.

## PLAN review lenses

Fresh `astra_xhigh`, read-only, checks in order:
1. Minimum sufficient outcome: delete unsupported mechanisms before hardening them.
2. Complete authority/examples/corrections and negative scope.
3. Canonical producer→normalizer→persistence→API→UI reachability; no missing loader, permission carrier, renderer, named-check or cleanup consumer.
4. Applicable failure transitions: repeated identical errors, cancel/reopen, request replacement, stale result, restart, stop-vs-completion precedence. Define a concrete regression trace, not a generic lifecycle framework.
5. Representation/domain/accuracy/default/override/missing/null semantics; algorithmic worst-case input cardinality where relevant.
6. Feasibility/order of validation: run the smallest real environment probe before making a runtime/browser gate a predecessor; a gate requiring final acceptance cannot itself be a prerequisite for that acceptance.
7. Dependency/resource/write isolation and selected model justification. Same filename-freeze is not semantic independence.

Fix bounded PLAN defects once; delta-recheck only affected boundaries. High-complexity GLM challenge uses the corrected plan without the first reviewer's persuasive narrative. No recursive full plan review. Implementation-level mistakes remain code-review work; do not pretend every code bug could have been forecast.

## Foundation choice

If a local patch would duplicate a semantic rule or patch several consumers around an inadequate producer, present the smallest canonical-owner refactor versus the safe local patch and its debt. Ask the user only when this changes authorized scope, compatibility, migration or risk. A local pure-helper extraction inside approved owners does not need a new design approval.

## Closed feature

Freeze final plan/hash and completion boundary in STATE.json. A later request gets a new request ID, requirement delta and trigger assessment. An explicitly requested reopen creates a new plan revision retaining the old hash and acceptance evidence; it does not silently append to the old file or reset counters. A newly discovered defect before completion remains within the active repair process.
