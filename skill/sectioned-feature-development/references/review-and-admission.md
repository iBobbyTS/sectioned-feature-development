# Review and Admission Guide

Use this reference to separate broad defect discovery from the authoritative decision about what the current feature must change.

## Contents

1. [Why two stages](#1-why-two-stages)
2. [Raw reviewer packet](#2-raw-reviewer-packet)
3. [Admission taxonomy](#3-admission-taxonomy)
4. [Materiality test](#4-materiality-test)
5. [Review rounds and clean streak](#5-review-rounds-and-clean-streak)
6. [Repairs and replans](#6-repairs-and-replans)
7. [Deduplication](#7-deduplication)
8. [Calibration examples](#8-calibration-examples)

## 1. Why two stages

A fresh reviewer should be free to inspect code independently, but its output is a set of candidates, not a change order. Agents often produce plausible suggestions that are false positives, duplicates, intent-misaligned, preference-driven, or outside the approved scope.

The two stages are:

1. **Raw review:** fresh `$code-review` agent reports evidence-backed candidates without knowing prior conclusions.
2. **Admission:** main agent classifies each candidate against frozen contracts, repository authority, supported deployment, and the actual diff.

This avoids two opposite failures:

- blindly implementing every reviewer suggestion;
- suppressing real defects merely because their repair is inconvenient or cross-sectional.

## 2. Raw reviewer packet

Give only:

- repository-local rules needed to interpret the change;
- exact base/head and working path;
- feature contract and current section contract;
- implementation handoff as a non-authoritative claim;
- validation outputs/current repository state;
- review criteria and output path.

Do not give:

- full originating session history;
- previous clean verdicts or “final confirmation” framing;
- previous reviewer arguments;
- rejected scope proposals;
- repair-agent persuasion;
- desired answer.

Freshness reduces confirmation bias and prevents the reviewer from role-playing as the feature owner.

## 3. Admission taxonomy

### `IN_SCOPE_REPAIR`

Frozen obligation is violated; smallest correct repair stays inside section.

### `IN_SCOPE_REPLAN`

Frozen obligation is violated; smallest correct repair crosses section boundary. Preserve as material and revise the graph/evidence.

### `OWNER_DECISION`

A non-inferable product, risk, compatibility, migration, rollout, or threat-model choice controls correctness.

### `EVIDENCE_FAILURE`

Review or tests cannot support the conclusion due to a missing or invalid oracle, environment, or baseline. The conclusion is evidence-invalid, but a completed full review with raw and admission artifacts still consumes its counting round.

### `DEFERRED_OWNER`

Valid work already belongs to a named later section and current intermediate state remains correct.

### `SCOPE_PROPOSAL`

Adds a new guarantee, supported actor/environment, feature, compatibility/durability promise, or generalization. Record separately; do not repair unless approved.

### `UNSUPPORTED_HYPOTHESIS`

No reachable supported trigger or evidence. It may be technically imaginable but is not a defect in the approved system.

### `NIT_DEBT`

Optional polish, education, style preference, or bounded debt that does not prevent acceptance.

## 4. Materiality test

A material candidate must state:

1. approved anchor;
2. reachable supported trigger;
3. material consequence;
4. evidence or falsifiable path;
5. smallest correct remedy;
6. boundary effect.

Reject vague forms:

- “could be unsafe” without actor/capability/path;
- “more robust to…” without a supported guarantee;
- “might break callers” without a named caller/contract;
- “should be abstracted” without demonstrated duplication/ownership need;
- “best practice” without applicability and consequence;
- “future use may…” without approved future use.

Repository invariants can be anchors even when the user prompt omitted them. Conversely, generic best practices do not override explicit repository scope.

## 5. Review rounds and clean streak

One completed counting round requires:

- a fresh full section review over the recorded base/head and direct impact cone;
- stable contract/plan/assurance revisions;
- complete raw and admission artifacts.

`EVIDENCE_FAILURE` consumes the round and resets the clean streak. Fix the evidence route before the next fresh review. A dispatch/tool failure that produces no raw review or admission artifact may retry the same round.

A `CLEAN` admission means no `IN_SCOPE_REPAIR`, `IN_SCOPE_REPLAN`, or `OWNER_DECISION` remains from that full review. Non-authoritative proposals, unsupported hypotheses, nits, and correctly deferred items do not break the streak.

Two consecutive clean completed rounds provisionally accept the section. A material admission resets streak to zero. There is no soft cap; five completed rounds without acceptance trigger classified recovery.

The second clean reviewer must not be told that the first was clean.

## 6. Repairs and replans

Send repair agents only admitted, agent-fixable findings. Include stable IDs, frozen acceptance, exact evidence, and boundary limits.

After repair:

- update handoff/head;
- run relevant deterministic checks;
- commit coherently when authorized;
- run a fresh full review;
- do not count a targeted DELTA check as a clean round.

For `IN_SCOPE_REPLAN`:

- freeze current attempt/evidence;
- revise only affected section/dependency edges;
- invalidate reviews whose assumptions changed;
- preserve feature/assurance promises unless an approved scope change exists;
- retry from a clean appropriate base.

## 7. Deduplication

Group symptoms under one root cause when they share:

- the same violated invariant;
- the same faulty owner/contract;
- the same missing state transition;
- the same missing validation oracle;
- the same unsupported threat-model expansion.

A new symptom of a closed root cause may justify reopening it if evidence shows the repair incomplete. Rewording the same concern is not a new finding.

Maintain separate ledgers for:

- admitted defects;
- owner decisions;
- scope proposals;
- unsupported hypotheses;
- nits/debt.

Never use raw comment count as defect count.

## 8. Calibration examples

### Blocker

A supported user can bypass an approved permission check through a concrete route; failing test reproduces it. Admit.

### Cross-section blocker

A migration section writes a representation that an accepted reader cannot consume. The correct repair requires coordinated migration. Admit as `IN_SCOPE_REPLAN`.

### Non-blocking proposal

Reviewer suggests a general plugin framework because future integrations may exist. No approved requirement. `SCOPE_PROPOSAL`.

### Unsupported security hypothesis

Attack requires arbitrary malicious code already executing inside the same trusted process, while the artifact is explicitly internal/test-only and repository policy does not require such isolation. `UNSUPPORTED_HYPOTHESIS` or proposal.

### Evidence failure

Reviewer cannot run the platform-specific integration test and infers failure solely from a mock. Mark `EVIDENCE_FAILURE`; the round is consumed, but the next action repairs the evidence route rather than product code.

### Deferred owner

Current expand phase intentionally keeps old and new paths; cleanup is assigned to `S04` and current state is compatible. `DEFERRED_OWNER`.

### Nit

Naming preference not established by style guide and no comprehension defect. `NIT_DEBT`.
