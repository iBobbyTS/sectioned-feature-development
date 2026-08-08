# Scope and Assurance Control

This reference defines how to keep implementation and review inside an approved feature/threat/compatibility envelope while still fixing real defects.

## Contents

1. [Three boundaries](#1-three-boundaries)
2. [Assurance envelope](#2-assurance-envelope)
3. [Scope-change authority](#3-scope-change-authority)
4. [Security finding admission](#4-security-finding-admission)
5. [Over-design signals](#5-over-design-signals)
6. [Correct response to drift](#6-correct-response-to-drift)
7. [Worked classifications](#7-worked-classifications)

## 1. Three boundaries

Keep three distinct boundaries frozen:

### Feature boundary

What behavior, users/operators, supported environments, and compatibility outcomes the feature promises.

### Section boundary

Which portion of that approved feature this implementation increment owns, including its direct impact cone and deferred owners.

### Assurance boundary

Which assets, actors, capabilities, entry points, trust boundaries, and guarantees this artifact must defend or preserve.

A reviewer may discover that code fails a frozen boundary. It may not silently redefine one. A stronger design is not automatically a more correct design.

## 2. Assurance envelope

Record:

- artifact role and deployment context;
- protected assets;
- trusted actors/inputs and their capabilities;
- untrusted actors/inputs and their capabilities;
- entry points/data flows/trust boundaries;
- required guarantees;
- explicit exclusions/non-guarantees;
- authoritative repository policy;
- triggers requiring owner approval.

The envelope must be proportional. Examples:

- A production multitenant upload service may need hostile-input, cross-tenant, symlink/path-rebinding, quota, and audit guarantees.
- A repo-local offline test harness using a private process-owned temporary directory may need deterministic output, ordinary I/O failure handling, private permissions, and atomic replacement, but not defense against arbitrary malicious same-process Python objects or same-UID filesystem attackers unless repository policy explicitly requires it.
- A one-shot migration utility may need resumability and data-integrity guarantees but not a permanent generalized orchestration service.

These are classification examples, not universal policies. Repository and owner decisions remain authoritative.

## 3. Scope-change authority

A proposed new guarantee must use `SC-*.md` when it changes any of:

- product-visible behavior;
- supported actor/environment;
- threat model or trust assumption;
- compatibility/durability promise;
- architecture/state ownership;
- migration/rollout policy;
- operational responsibility or service boundary.

Only an accountable owner can approve it. Approval must update:

- exact feature contract text;
- affected section contract revisions;
- plan fingerprint/coverage/dependencies;
- tests/oracles;
- invalidated review evidence and clean streak.

A reviewer can propose the change, but cannot approve it. A repair agent cannot create authority by implementing it first.

## 4. Security finding admission

A material security finding needs all of:

1. asset;
2. actor and capability;
3. supported deployment context;
4. entry point/data flow;
5. trust boundary;
6. reachable preconditions;
7. material consequence;
8. contract/repository-policy anchor;
9. evidence or falsifiable path;
10. smallest correct remedy and boundary effect.

Classify:

- `IN_SCOPE_REPAIR`: all above hold and repair stays within the section.
- `IN_SCOPE_REPLAN`: all above hold but the correct repair crosses a frozen section boundary.
- `OWNER_DECISION`: repository evidence cannot determine whether the actor/environment/guarantee is supported.
- `SCOPE_PROPOSAL`: it would add a useful but currently unapproved guarantee.
- `UNSUPPORTED_HYPOTHESIS`: trigger depends on an excluded or impossible actor/environment and no authoritative policy overrides that exclusion.
- `EVIDENCE_FAILURE`: the test harness cannot establish the claim.

“Security issue” is not a bypass around scope control. Equally, “out of section” is not a reason to ignore a real security defect inside the approved feature envelope.

## 5. Over-design signals

Strong signals include:

- each review round introduces a stronger attacker or environment;
- implementation adds registries, ownership ledgers, capability tokens, stable-handle layers, generalized policy engines, or configurable frameworks without contract anchors;
- tests simulate powers no supported actor has;
- repair complexity grows while user-visible behavior stays unchanged;
- raw reviewer comments are copied into `PLAN-FULL.md` as requirements;
- a narrow helper becomes responsible for arbitrary same-process malicious objects, same-UID attackers, all platform variants, or production-grade durability without owner approval;
- the plan recursively splits mechanisms created only by previous speculative repairs;
- passing criteria become “survive any imaginable race” rather than the frozen guarantee.

Use the complexity receipt to expose these mechanisms before review.

## 6. Correct response to drift

When drift is detected:

1. stop product-code repairs;
2. freeze the failed tip and preserve evidence;
3. compare current code/mechanisms to the original contract and assurance envelope;
4. classify raw review candidates separately from admitted findings;
5. identify mechanisms lacking durable anchors;
6. select `SIMPLIFY_REPLACE` rather than further splitting the inflated design;
7. restore/retry from the original section base;
8. create the smallest replacement contract and oracle;
9. keep rejected proposals in a non-authoritative ledger for optional later consideration.

Do not “simplify” by weakening an explicit repository invariant. Remove only unapproved or disproportional mechanisms.

## 7. Worked classifications

### Example A: real defect, local repair

Contract says a request must reject an unauthorized caller. Supported API path accepts one role due to inverted condition. Anchor, trigger, consequence, and test are direct; changing policy evaluator is local. Class: `IN_SCOPE_REPAIR`.

### Example B: real defect, cross-section repair

Schema producer serializes a field incompatible with an already-approved consumer contract. Correct repair requires coordinated producer/consumer migration. Class: `IN_SCOPE_REPLAN`, even if current section owns only producer code.

### Example C: useful stronger guarantee

A private offline harness writes to a process-owned `0700` directory. Reviewer asks for defense against an arbitrary same-UID process renaming every ancestor after descriptor checks. No repository policy or supported deployment requires this. Class: `SCOPE_PROPOSAL` or `UNSUPPORTED_HYPOTHESIS`, not a blocker.

### Example D: missing threat-model decision

The artifact may be reused by a production worker, but documentation and callers disagree. Whether same-tenant untrusted plugins are supported is unknowable. Class: `OWNER_DECISION`; ask the smallest bounded question.

### Example E: weak oracle

A test asserts a mock call but does not exercise the filesystem behavior used to claim atomic publication. Class: `EVIDENCE_FAILURE`; the completed review consumes its round, then repair the validation route before the next review.

### Example F: maintainability suggestion

Reviewer prefers extracting a one-use helper, but current code is clear and within local conventions. No material consequence. Class: `NIT_DEBT` or reject as preference.
