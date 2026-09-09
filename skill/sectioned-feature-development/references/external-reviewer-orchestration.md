# External Reviewer Orchestration

## Contents

- [Provider schedule](#provider-schedule)
- [High-complexity PLAN review](#high-complexity-plan-review)
- [Code-review session continuity](#code-review-session-continuity)
- [Stage barrier](#stage-barrier)
- [Failure handling](#failure-handling)

## Provider schedule

The first code full-review slot uses [@code_reviewer](subagent://code_reviewer). PLAN authorship/review do not consume code full-review slots. Each later independent review session alternates provider: Astra → ZCode → Astra. Provider alternation is feature-local and persists across sections in readable FEATURE-STATE; no slot-reservation CLI is required. A repair verification is not a new independent session.

## High-complexity PLAN review

Use a second independent ZCode PLAN review only when at least two ordinary risk signals are present, or one critical signal plus another boundary: schema/migration; security/credentials/money; public protocol/compatibility; concurrency/retry/replay/process lifecycle; cross-runtime/process behavior; at least four behavioral owners; at least three product sections; unbounded impact cone; prior material incident or architecture recovery.

Sequence:
1. [@plan_reviewer](subagent://plan_reviewer) reviews the persisted PLAN-FULL for authority, necessity, owners, external seams, lifecycle/precedence, proportionality, and validation.
2. Main agent admits findings and makes minimal plan-only corrections.
3. If high-complexity, ZCode independently reviews the corrected plan without the primary reviewer conclusions.
4. If ZCode findings are admitted, correct the plan and use the same ZCode session for at most one delta verification only if it remains nonterminal and supports that operation; otherwise apply the explicitly recorded same-provider fresh-delta limitation below, or block under strict continuity.
5. No third independent PLAN reviewer.

## Code-review session continuity

A `review_id` binds provider, stable agent identity, reviewed base/head, scope packet, findings, and closure. Send clarification, counter-evidence, and repair verification to the original reviewer when the actual harness supports it; record terminal continuity gaps rather than claiming identity reuse. Open a new independent session only for the next discovery/final evidence and use the next provider in the schedule.

## Stage barrier

Persist `active_section`, `active_writer_id`, `active_review_id`, `review_provider`, `reviewed_head`, and `next_allowed_phase`. No dependent implementation may begin before its prerequisite is accepted and integrated. An independent parent may run only in another worktree under the path/contract/resource checks in `parallel-execution.md`; a writer never mutates an active review snapshot. If a writer starts early, stop it, preserve partial work without committing, mark `SEQUENCE_GATE_VIOLATION`, and close or invalidate only the affected review.

## Failure handling

One external reviewer transport/runtime failure permits one bounded retry. A failed/missing artifact never counts as clean. If required assurance cannot be met, return insufficient evidence. Do not silently replace ZCode with the main agent.

## Subsection primary pass and actual current MCP

A decomposed business section assigns one primary logical code-review slot at its first checkpoint. Subsequent SUBSECTION_DELTA and PARENT_RECONCILIATION are continuations of that logical coverage, not additional full-review slots. Every physical call still counts in audit cost; same provider is not same session. The fresh parent FINAL consumes the next feature-wide slot. No independent final per child.

Use the actual lifecycle tools plus suspicion-only `zcode_subagent_observe` from zcode-mcp-adapter.md. Its send is queued and terminal tasks reject continuation. Record TERMINAL_CONTINUATION_UNSUPPORTED for an approved same-provider fresh delta; strict continuity blocks. Neither the MCP success status nor plan permission mode proves review cleanliness or read-only isolation.
