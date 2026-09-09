# ZAS adapter — 4.3.1 installed observation contract

## Contents
- [Installed contract](#installed-contract)
- [Lifecycle](#lifecycle)
- [Suspicion-only observe](#suspicion-only-observe)
- [Review result and audit](#review-result-and-audit)

## Installed contract

The user installs the updated ZAS implementation before using this Skill. Require all ten tools: `zcode_subagent_status`, `zcode_subagent_spawn`, `zcode_subagent_poll`, `zcode_subagent_list`, `zcode_subagent_send`, `zcode_subagent_respond`, `zcode_subagent_cancel`, `zcode_subagent_result`, `zcode_subagent_close`, and `zcode_subagent_observe`.

Status declares `capabilities.observation.protocol="zas-observation/1.1"`, `public_reasoning_default=true`, `runtime_source_verified=true`, and defaults `{top_tools:3,recent_calls_per_tool:5,reasoning_chars:200}`. Confirm catalog/status once per service generation. Missing or contradictory declarations are an installation contract error; stop and report `ZAS_INSTALLATION_CONTRACT_MISMATCH`. There is no old-server, metadata-only or baseline-beta fallback in this version. This prerequisite does not claim runtime/auth/model reliability; actual task failures still need normal handling.

The existing nine lifecycle contracts remain: spawn uses repository/prompt with optional permission_mode/write_manifest; poll uses agent_id/after_revision/timeout_ms (maximum 5000); list is repository-scoped; send takes message_id/content and is queued; respond uses actual request_id and allow/deny; cancel/close use actual agent_id; result uses offset/limit. Do not send removed model/group/named-check/budget fields or invent aliases. Omit absent optional values instead of sending null.

Spawn remains non-idempotent unless the separately installed lifecycle schema explicitly adds a caller key: reconcile a lost response with repository-scoped list rather than blindly duplicating work. Observation adds no spawn observation_mode, opt-in consent flag or new permission tier.

Preserve the feature-wide native/ZCode full-review sequence and existing acceptance exactly. Infrastructure failures are physical attempts of the reserved slot, not code findings or clean outcomes. One bounded corrected retry remains governed by the existing rule; provider substitution still needs explicit authority.

## Lifecycle

1. Reserve the existing review slot; freeze the review packet and immutable candidate worktree. ZAS does not own Git.
2. Run status/catalog preflight. A daemon-status query does not prove model authorization. Do not add a paid "hi" test to every section; the actual review attempt is the actual task.
3. Spawn with `permission_mode=plan`, no write_manifest, and a prompt containing the exact task/contract/source paths plus required review output. Plan mode's product intent is read-only; it is not proof of absence of mutation. Compare product/test fingerprints afterward.
4. Poll using returned next_revision, honoring max_wait_ms. Reasoning/text revisions can arrive immediately, so do not busy-poll or rewrite the same snapshots. The host may use bounded waits; elapsed time does not authorize an observe call by itself. Poll does not read a durable observation timeline.
5. Handle real permissions under the frozen contract. `unsupported_input` is not answerable by inventing decision=answer; record/block that capability gap. Never broaden permission just to finish a review.
6. If progress is questionable, use [progress supervision](zas-progress-supervision.md). Active events and model deltas only prove liveness.
7. Read result through all offset/limit segments after result_available. Require a stable total_bytes, monotone next_offset and complete=true. The base lifecycle MCP does not guarantee a result hash even though internal RPC does; compute a caller-side hash and label its provenance, not a server attestation.
If the task is terminal but result_available remains false, record RESULT_UNAVAILABLE, collect the bounded diagnostic once, and close/reap; do not wait indefinitely or treat absent text as CLEAN.

8. Store raw safe result and actual IDs; parent evaluates code-review protocol, exact candidate identity and admission independently. COMPLETED is runtime completion, not CLEAN.
9. Close and verify task `closed=true` and `resources_reaped=true`. If cancelling, first wait for phase TERMINAL + resources_reaped, capture any result/gaps, then close. A cleanup failure blocks workspace reuse but is not a code finding.

### Terminal continuation

The source documents failed app-server cold resume even on ZCode Desktop 3.11.2 / bundled CLI 0.16.5. `closed=false` and old COMPLETED result do not prove a new message ran. Do not use terminal send or official CLI --resume as an automatic workaround. Use a new same-provider task with the frozen findings/repair delta; record same_session=false and TERMINAL_CONTINUATION_UNSUPPORTED. Strict same-session requests remain blocked. Do not count this fresh delta call as a new full-review slot.

### Diagnostics

Product-owned tool execution failures return `isError=true`, the existing bounded text in `content`, and `structuredContent.error`. Prefer the actual error object's `code` and `message`; preserve `component`, `operation`, `request_id`, `agent_id`, and `cleanup` only when present. Do not invent missing context or assume undeclared fields such as `retryable` or `message_id`. Distinguish `runtime_command_failed`, `daemon_unavailable`, `persistence`, `protocol_error`, and `conflict` with the actual `WORKSPACE_BUSY` or `MESSAGE_ID_CONFLICT` message. A generic `unavailable` or a runtime command rejection does not prove the daemon is down. Keep the first failure separate from cleanup and do not restart the service merely to retry a runtime rejection.

SDK pre-handler argument-decoding failures may remain text-only `isError` responses without `structuredContent.error`; outer JSON-RPC protocol errors retain their own semantics. Preserve the original bounded response rather than requiring every failure to have the product-owned envelope. A successful poll/result call can report a terminal FAILED/CANCELLED task: tool-call success is not task success or a clean review.

On a real failure, `zas diagnose --agent <id> --output <local-dir>` is the installed CLI diagnostic path. Keep it outside the process-audit output namespace until selected/redacted references are imported. Read only the relevant agent record, not unrelated global logs. The source already preserves operation/remote_code/remote_message separately from cleanup_result; do not add a duplicate recorder. When checking a deployment, distinguish status's self-reported running daemon/facade identity from diagnose's packaged disk artifacts; a matching disk binary alone does not prove a running process has been restarted.

## Suspicion-only observe

Call `zcode_subagent_observe` with only `agent_id` **only when the caller suspects meaningless looping**. Follow the five judgment descriptions published by that tool, not an automatic ZAS classifier. Normal health/permissions/completion use poll; observe is neither heartbeat nor automatic periodic inspection.

The response contains at most three tool-name groups ranked by that Agent's lifetime invocation count; each has its latest at most five actual invocation IDs/arguments and no results. Public reasoning deltas are concatenated in runtime order, then only the newest 200 Unicode characters are returned. One delta is not one character. Status, snapshot sequence and coverage flags make missing information explicit.

The exact public reasoning event selector and text key were confirmed on the local runtime by the ZAS implementation. Extraction is enabled by default and allowlists only that confirmed field. Recursively exclude `encrypted_content` before observation storage/logging/export; never decode it or infer text from alternate/private fields. There is no extra user/caller authorization switch.

Use `zas_evidence.py capabilities` and `snapshot` for schema/provenance/bounds only. The helper does not prove the local runtime probe happened, determine semantic progress or cancel anything. The implementation's probe receipt supplies the provenance; tests here use labelled synthetic fixtures.

## Review result and audit

Lifecycle outcome, semantic review result and observation/cleanup quality remain separate. Do not count task COMPLETED or a hash-valid response as CLEAN. Do not infer tool success from a call-only snapshot. Preserve meaningful gaps and allow the caller to stop on an already-authorized budget without claiming proven looping.

Detailed ZAS attempts, selected observations and diagnostic receipts are exported to the paired `xxx-zas.zip`, not embedded as a second full payload in `xxx.zip`. The main process pack holds a small identity link and workflow aggregates. See [ZAS audit](zas-audit.md). Neither path creates a `.sha256` file.
