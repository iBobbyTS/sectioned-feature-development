# Review protocol

## One parent state machine

The bundled `$code-review` 4.0.1 implements `sfd-delegated-review/4.1` and is installed alongside this skill. In delegated mode it is a single-pass reviewer engine. Parent supplies context=DELEGATED_PASS, exact base/head, requirements, scope, exclusions, pass ID, expected result and validation evidence. Reviewer returns candidates, coverage and gaps; it does not admit, repair, launch another reviewer or grow scope. No second orchestrator is hidden inside code-review.

## Providers and assurance

- PLAN author/reviewer: distinct `astra_xhigh` instances; high-complexity second challenge GLM.
- Feature code full-pass index starts at 1: odd=`astra_high`, even=ZCode `glm-5.3`. Reserve index before dispatch. Integration full reviews share this sequence.
- Infrastructure retries do not advance it. Delta checks and advisor calls do not consume it. A local follow-up outside this skill does not inherit the old feature's counter.
- `ONE`: a clean initial full pass accepts the section. When that pass admits a material defect, perform bounded repair-delta closure and one fresh final full pass. This retains the prior assurance requirement; routing changes are not a reason to silently remove independent verification.
- `TWO`: first pass/closure plus one fresh independent final pass. A material reset may require another full pass, but keeps the same cumulative budget and provider sequence.
- AUTO uses TWO for hard-to-observe failure paths, consequential state/protocol/migration interactions or incomplete local oracles; ONE for decisive local behavior/equivalence with no new semantic boundary. Record why. File count, model tier and absence of findings are not the decision rule.

External review policy defaults `required` for scheduled GLM passes. Model/runtime unavailability never silently substitutes a different model. User can explicitly permit `preferred` fallback to fresh Astra with a heterogeneity gap. A single ONE pass does not add an unnecessary GLM round.

## Finding admission

Candidate classes: DIFF_CAUSED, MERGE_BLOCKING_DEPENDENCY, EVIDENCE_GAP, PREEXISTING_OUT_OF_SCOPE, SCOPE_PROPOSAL, NIT_DEBT, OWNER_DECISION.

Only current-diff defects, necessary faulty dependencies on a required execution path, and missing already-required evidence normally block. Inspect a direct dependency only to prove the causal chain. Author-written tests, old plans and repeated reviewer assertions are not external authority.

Freeze finding ID, root cause, trigger, invariant, required outcome, repair owners and checks before repair. Don't add a framework/security promise to satisfy a speculative finding. Repeated forms of the same cause share lineage; newly introduced repair defects remain visible.

## Same-pass continuity

Send follow-up/falsification to the original native reviewer session where supported. ZCode `send` only queues while nonterminal; there is no documented terminal resume. See zcode reference. Never pretend a fresh agent is the originating reviewer. If native session is lost, record the gap and use bounded same-provider delta with explicit approval when strict continuity was required.

An independent full reviewer receives requirements, current diff, scope and required oracles without previous reviewer persuasion. For closure checks only, give frozen findings and closure criteria. They can independently disagree; main resolves by source/reproduction, not votes.

## Finite repair and recovery

A wave is an admitted material root cause followed by a real repair attempt; partial or failed closure still consumes its attempted wave. Do not count merely planned findings, model dispatch failures, audit edits or rejected suggestions. Do not undercount failed fixes by requiring closure before counting a wave.

Five waves per original section lineage (including final findings) are the ordinary limit. Diagnose once at impending sixth: simplify or bounded owner-level correction. Never reset the count by renaming the section, switching models, or opening a new final round. One structural recovery may repartition remaining work with inherited recovery-used status. A further convergence failure activates the advisor reference, not recursive replanning.

## Required packet output

Pass ID/provider/actual identity; exact candidate; inspected paths; tests reused/newly run/not runnable; candidate IDs and evidence; proposed classes; confidence/gaps; CLEAN/MATERIAL_CANDIDATES/INSUFFICIENT_EVIDENCE. Main alone decides section acceptance and feature readiness. Historical provider-specific verdict strings are normalized without claiming they are today's runtime enum.

## Subsection coverage under the same parent pass

`SUBSECTION_DELTA` covers a new bounded child increment and parent shared invariants; `PARENT_RECONCILIATION` finishes cumulative coverage at final HEAD. Both use the same logical primary pass and the available real originating reviewer, with explicit continuity gaps where unavoidable. They do not earn separate Clean A/B pairs. Parent ONE/TWO and final review rules remain unchanged; all repair attempts share the original lineage. See [subsections.md](subsections.md).

Compatibility: DELEGATED_PASS accepts legacy atomic `sfd-delegated-review/4.0`; new child packets use `sfd-delegated-review/4.1`.
