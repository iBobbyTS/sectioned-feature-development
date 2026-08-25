# External Reviewer Orchestration

## Contents

- [Provider schedule](#provider-schedule)
- [High-complexity PLAN review](#high-complexity-plan-review)
- [Code-review session continuity](#code-review-session-continuity)
- [Stage barrier](#stage-barrier)
- [Failure handling](#failure-handling)

## Provider schedule

The first independent review session uses Sol. Each later independent review session alternates provider: Sol → ZCode → Sol. Provider alternation is feature-local and persists across sections. A repair verification is not a new independent session.

## High-complexity PLAN review

Use a second independent ZCode PLAN review only when at least two ordinary risk signals are present, or one critical signal plus another boundary: schema/migration; security/credentials/money; public protocol/compatibility; concurrency/retry/replay/process lifecycle; cross-runtime/process behavior; at least four behavioral owners; at least three product sections; unbounded impact cone; prior material incident or architecture recovery.

Sequence:
1. Sol reviews PLAN-FULL for authority, necessity, owners, external seams, lifecycle/precedence, proportionality, and validation.
2. Main agent admits findings and makes minimal plan-only corrections.
3. If high-complexity, ZCode independently reviews the corrected plan without Sol conclusions.
4. If ZCode findings are admitted, correct the plan and use the same ZCode session for at most one delta verification.
5. No third independent PLAN reviewer.

## Code-review session continuity

A `review_id` binds provider, stable agent identity, reviewed base/head, scope packet, findings, and closure. Send clarification, counter-evidence, and repair verification to the original reviewer. Open a new independent session only for the next discovery/final evidence and use the next provider in the schedule.

## Stage barrier

Persist `active_section`, `active_writer_id`, `active_review_id`, `review_provider`, `reviewed_head`, and `next_allowed_phase`. No next-section implementation may begin until the current section is ACCEPTED, BLOCKED, or ABANDONED. If a writer starts early, stop it, preserve partial work without committing, mark `SEQUENCE_GATE_VIOLATION`, and close or invalidate only the affected review.

## Failure handling

One external reviewer transport/runtime failure permits one bounded retry. A failed/missing artifact never counts as clean. If required assurance cannot be met, return insufficient evidence. Do not silently replace ZCode with the main agent.
