# ZAS progress supervision — evidence, not string similarity

## Contents
- [Separate liveness and progress](#separate-liveness-and-progress)
- [When to inspect](#when-to-inspect)
- [Semantic assessment](#semantic-assessment)
- [Intervention](#intervention)
- [Capture policy](#capture-policy)

## Separate liveness and progress

This protocol governs the caller's beta runtime control, regardless of audit mode. It does not increase section/review counts. ZAS reports observations; the main agent judges progress against the current task. No cosine/edit-distance/text-repetition threshold is a loop detector or termination authority.

Current poll provides 60-second reasoning/text byte/event counts, tool kind/count, request clocks, latest assistant text and active tools. It omits reasoning content, tool arguments and read ranges, and its passive snapshot may be unavailable after restart. Therefore it can identify activity/waiting, not reliably identify semantic loops. An active stream may loop; a quiet stream may be legitimate computation or external waiting.

The enhanced observation endpoint is separately proposed, not assumed installed. It returns only already-public runtime content and structured tool facts, with gaps and redaction. Never infer private/hidden reasoning, decrypt opaque payloads, scrape credentials, or recover suppressed provider messages. Public reasoning excerpts are optional corroboration, not mandatory evidence.

## When to inspect

At launch, record the bounded subgoal, expected evidence/check, supported waits and a task-appropriate progress checkpoint. A checkpoint is an observation time, not an automatic timeout. A suggested beta starting point for code-review observation is five minutes; use a longer justified checkpoint for a known long test or analysis. This is not a universal safety limit.

Inspect a bounded window when either:
- two completed, materially equivalent action/analysis cycles address the same unresolved subgoal without a cited new fact or changed state; or
- the planned progress checkpoint arrives while activity continues but no result can yet be tied to the expected evidence.

Pending permission, known long-running checks, backoff/retry waiting and context-recovery reads must be classified before suspecting a loop. Do not repeatedly inspect the identical event window: advance the observation cursor; deduplicate delivery IDs, not semantic texts. Routine healthy polling does not launch another model or ask for a self-report.

## Semantic assessment

Compare the task to a short sequence of observations and return one category with event IDs and a brief factual explanation:

- `PROGRESSING`: a new source fact, disproved hypothesis, meaningful artifact/test result, or completed analysis reduces uncertainty. Code need not change during review.
- `EXPECTED_WAIT`: an actual long command/permission/network/model wait has a known purpose and no proven deadlock.
- `NEEDS_CLARIFICATION`: a concrete missing decision or input prevents progress.
- `NO_PROGRESS_LOOP`: consecutive cycles revisit the same decision or equivalent actions without new information or state change, and legitimate verification/waiting explanations have been ruled out.
- `INSUFFICIENT_OBSERVABILITY`: missing/truncated content, lost stream, unknown read range/content version, or counters alone do not support a semantic conclusion.

Record the subgoal, observations considered, new information (or absence), relevant state changes, ruled-out alternative, expected next evidence, confidence and chosen action. This is a short evidence-backed assessment, not a request for hidden chain-of-thought.

Examples:
- Repeated public "first A / no, first B / recheck A" only suggests indecision. Corroborate with unchanged task facts/tool sequence and absence of a resolved hypothesis; the text itself cannot prove a loop.
- `true`, `echo a`, `echo b` may be a legitimate shell/stream/protocol fixture. They are unproductive only when unrelated to the agreed subgoal and repeatedly substituted for the next meaningful step.
- Re-reading the same file range can be valid after a write, context compaction, new hypothesis or reviewer recheck. Distinguish different ranges, versions and purposes. Missing fingerprints mean UNKNOWN, not unchanged.
- A successful test rerun after a repair is progress. A byte-identical result repeated without a state change or new oracle may be redundant but is not automatically a reason to kill the Agent.

## Intervention

1. `PROGRESSING` / `EXPECTED_WAIT`: continue and move to the next checkpoint; do not retain verbose duplicate content.
2. `NEEDS_CLARIFICATION`: answer an actual supported pending request or send one bounded queued clarification for a running Agent. Send is not an interrupt and may not break a looping current turn.
3. `NO_PROGRESS_LOOP`: preserve the bounded public evidence and parent assessment, then cancel through the real MCP control. Do not wait indefinitely for a queued self-correction. Observe TERMINAL + resources_reaped, save result/partial gaps, close, and verify workspace/fingerprint before any retry.
4. `INSUFFICIENT_OBSERVABILITY`: do not label a loop. Request the supported scoped diagnostic once or stop as a time/budget/observation blocker according to the already-authorized caller policy. Distinguish `BUDGET_STOP_UNPROVEN_LOOP` from a proven no-progress intervention.

No automatic repeated cancel/spawn cycle. One justified changed-packet retry may remain in the same logical provider slot under the existing retry cap. If the beta cannot supply the required review, report insufficient evidence; seek explicit authorization before using a different provider. A runtime loop does not consume a product repair wave or itself trigger external Advisor; ADV thresholds still apply.

## Capture policy

Default logs are metadata-only. Detailed public-content observation is explicit for the controlled beta task and bounded by events/bytes/retention. Store selected windows used for decisions once, not every poll or the entire model stream. Exclude secrets, raw unrelated tool output and unsupported/private reasoning. Dropped/redacted/truncated evidence is a telemetry gap, not proof of no progress.

When audit is enabled, preserve false-positive opportunities too: continued work that later succeeds, reassessment, model/runtime identity, interventions and total time/cost. Do not run new tests/tasks merely to collect a loop dataset.
