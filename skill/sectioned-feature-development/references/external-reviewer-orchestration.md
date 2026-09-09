# External Reviewer Orchestration

## Contents

- [Route identity](#route-identity)
- [Provider schedule](#provider-schedule)
- [High-complexity PLAN review](#high-complexity-plan-review)
- [Code-review session continuity](#code-review-session-continuity)
- [Stage barrier](#stage-barrier)
- [Failure handling](#failure-handling)

## Route identity

There are two disjoint execution routes:

| Route | Dispatch | Wait/result/control | Meaning |
|---|---|---|---|
| Native Codex | Native subagent mechanism selects [@plan_reviewer](subagent://plan_reviewer) or [@code_reviewer](subagent://code_reviewer) | Native host tools using the returned task/session ID | These named roles are native, not ZAS aliases |
| ZAS MCP | Direct `zcode_subagent_spawn` | `zcode_subagent_poll`, `zcode_subagent_result`, then applicable send/cancel/close with returned agent_id | External ZCode/GLM runtime, not a Codex native role |

`$code-review` is a provider-neutral instruction set. Giving it to a ZAS job does not turn that job into [@code_reviewer](subagent://code_reviewer). Likewise, a native task mentioning GLM or ZCode is not evidence that MCP ran. Never spawn [@code_reviewer](subagent://code_reviewer) to proxy another ZAS review: each slot has one actual reviewer, not a native-plus-external stack.

For each logical review slot, write planned provider, actual route, actual tool name and tool-returned ID together in the existing review ledger. Labels such as `native:<id>` and `zas:<id>` may disambiguate prose only; actual API calls use the original raw ID and schema, without these prefixes. Never send a native ID to ZAS lifecycle tools or a ZAS agent_id to native wait/follow-up tools. Requested model and independently observed model stay distinct/UNKNOWN where appropriate.

An unavailable native role does not authorize ZAS substitution, and an unavailable ZAS service does not authorize a native wrapper. Only explicit applicable user/repository authority may override the planned provider; keep planned and effective route plus authority visible, preserve the same logical slot, and keep subsequent delta on the effective reviewer route.

If the wrong route was launched, stop any remaining accidental actor through its actual route, preserve its output, and record REVIEW_ROUTE_MISMATCH. Its findings may be useful candidates, but it does not satisfy the intended independent provider slot. Use the correct route under the existing bounded retry policy, or stop if unavailable; do not relabel the result, create another numbered full slot, or reset a repair budget. Previously accepted work is not reopened solely due to this version.

## Provider schedule

The first code full-review slot uses [@code_reviewer](subagent://code_reviewer). PLAN authorship/review do not consume code full-review slots. Each later independent review session alternates provider: Astra → ZCode → Astra. Provider alternation is feature-local and persists across sections in readable FEATURE-STATE; no slot-reservation CLI is required. A repair verification is not a new independent session.

## High-complexity PLAN review

Use a second independent ZCode PLAN review only when at least two ordinary risk signals are present, or one critical signal plus another boundary: schema/migration; security/credentials/money; public protocol/compatibility; concurrency/retry/replay/process lifecycle; cross-runtime/process behavior; at least four behavioral owners; at least three product sections; unbounded impact cone; prior material incident or architecture recovery.

Sequence:
1. [@plan_reviewer](subagent://plan_reviewer) reviews the persisted PLAN-FULL for authority, necessity, owners, external seams, lifecycle/precedence, proportionality, and validation.
2. Wait for the native result, read/save it, then main admits findings and makes minimal plan-only corrections. No implementer may be spawned while this is pending.
3. If high-complexity, directly spawn a ZAS MCP job to independently review the corrected plan without the primary reviewer conclusions. This is not a second native plan/code reviewer. The global PLAN barrier remains closed until it returns and main completes admission.
4. If ZCode findings are admitted, correct the plan and use the same ZCode session for at most one delta verification only if it remains nonterminal and supports that operation; otherwise apply the explicitly recorded same-provider fresh-delta limitation below, or block under strict continuity.
5. No third independent PLAN reviewer. S01 (or any other product implementation) starts only after all selected PLAN passes and necessary delta closure are complete; early candidates, cancellations and timeout responses do not unlock it.

## Code-review session continuity

A `review_id` binds provider, stable agent identity, reviewed base/head, scope packet, findings, and closure. Send clarification, counter-evidence, and repair verification to the original reviewer when the actual harness supports it; record terminal continuity gaps rather than claiming identity reuse. Open a new independent session only for the next discovery/final evidence and use the next provider in the schedule.

## Stage barrier

Use the root/activation dispatch handoff, not a script. Persist only the actual active unit, route/ID, outstanding result, candidate and next permissible action in readable FEATURE-STATE. Plan review is a feature-wide barrier. Serial parent/subsection progression waits for full parent acceptance or checkpoint closure respectively; any dependent parent also waits for integration. An independent parent may overlap only if explicitly named as parallel in the already reviewed PLAN and isolated under parallel-execution.md. Do not confuse process completion or initial CLEAN with final acceptance.

If the writer starts too early, stop the real actor, preserve its partial work, and close the original prerequisite. Invalidate only review evidence whose input snapshot changed. No manufactured status update, automatic budget reset, extra section or global historical re-review.

## Failure handling

One external reviewer transport/runtime failure permits one bounded retry. A failed/missing artifact never counts as clean. If required assurance cannot be met, return insufficient evidence. Do not silently replace ZCode with the main agent.

## Subsection primary pass and actual current MCP

A decomposed business section assigns one primary logical code-review slot at its first checkpoint. Subsequent SUBSECTION_DELTA and PARENT_RECONCILIATION are continuations of that logical coverage, not additional full-review slots. Every physical call still counts in audit cost; same provider is not same session. The fresh parent FINAL consumes the next feature-wide slot. No independent final per child.

Use the actual lifecycle tools plus suspicion-only `zcode_subagent_observe` from zcode-mcp-adapter.md. Its send is queued and terminal tasks reject continuation. Record TERMINAL_CONTINUATION_UNSUPPORTED for an approved same-provider fresh delta; strict continuity blocks. Neither the MCP success status nor plan permission mode proves review cleanliness or read-only isolation.
