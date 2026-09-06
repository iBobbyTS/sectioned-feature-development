# Current zcode-as-subagent adapter

Authority: user-supplied `zcode-as-subagent功能说明.md` (record its SHA-256 in the project release). This replaces all legacy zcode_review_*, zcode_agent_* and zcode_system_* designs. Do not add undocumented fields/tools.

## Exact tools

- `zcode_subagent_system_status`
- `zcode_subagent_agent_spawn`
- `zcode_subagent_agent_poll`
- `zcode_subagent_agent_list`
- `zcode_subagent_agent_send`
- `zcode_subagent_agent_respond`
- `zcode_subagent_agent_cancel`
- `zcode_subagent_agent_result`
- `zcode_subagent_agent_close`

Status is read-only and does not call a model. `model_auth=UNKNOWN` is not an authentication failure. Windows operations are unsupported; do not claim a portable working GLM reviewer there. Runtime/path and hooks belong to the product, not this skill.

## Caller owns Git

Spawn requires an existing absolute `workspace`, `prompt`, and `idempotency_key`. It does not create/checkout/snapshot/commit/restore Git. `repo_context` is a hint, not a path permission or snapshot. One active agent per canonical workspace; use isolated review worktrees, not symlink aliases, for parallelism.

Use `permission_mode="plan"`, `model="glm-5.3"`, a stable `group_id`, explicit context paths and an idempotency key unique to semantic input (run/section/review/attempt/candidate). The API supports build/edit/plan/yolo; it has no read_only/workspace_write parameter. Plan mode and prompts alone do not prove read-only enforcement. Preserve a before/after product fingerprint and reject review evidence if a reviewer mutated product/test files. Do not run ZCode on the only dirty user worktree.

Named check IDs must exist in that installation. Discover from actual supported configuration; do not invent `unit-tests`, add arbitrary shell fields, or mark a check required without confirming it exists. Main/native test execution can supply equivalent existing gate evidence when those commands cannot run in the external runtime; missing required evidence is not clean.

## Lifecycle

1. Status preflight once; refresh only on relevant failure/generation change.
2. Spawn with documented schema. Persist returned `agent_id` before retrying.
3. Poll with `after_revision=0`, then use returned `next_revision`; bounded long-poll timeout. Activity counters are liveness, not semantic success.
4. Respond only to pending `request_id`, using allow/deny/answer. Never fabricate pending requests to keep a session alive.
5. On result_available, fetch result. Collect all artifact chunks by offset/next_offset and verify `total_bytes`/SHA-256 before using them.
6. Close; after cancel wait for TERMINAL + reaped=true. Cancel is not steer or resumable interruption.

`agent_list` must be scoped by workspace or group_id. WORKSPACE_BUSY returns the real active_agent_id; inspect it, do not cancel unrelated work or spin repeated spawn calls. Repeat same idempotency key only for the same semantic input.

## Review and continuity

Review mode is a workflow prompt/output contract layered on this **general** API, not a new MCP tool or undocumented schema field. Return candidates and source/check evidence as final_text or artifact; main writes its review ledger and independently records Git identity. Result has no base_commit/head_commit/patch guarantee.

`agent_send` queues, does not interrupt generation, and returns REJECTED_TERMINAL after terminal. Thus:
- nonterminal clarification may use the same agent;
- do not modify its live reviewed workspace while it reads;
- after terminal and repair, exact-session reuse is unavailable in the supplied contract;
- default compatibility policy `same_provider_delta_with_gap` creates a fresh GLM agent on the repaired snapshot with frozen findings only, logs `same_session=false / TERMINAL_CONTINUATION_UNSUPPORTED`, and does not advance the full-pass counter;
- if user requires strict originating-agent continuity, stop `CONTINUITY_BLOCKED` rather than claiming compliance or inventing resume.

The compatibility policy preserves bounded review, but is not identical to same-session verification. Record it for evaluation. An external successful task is not automatically a clean review.

## Errors

Use actual structured codes: DAEMON_UNAVAILABLE, PROTOCOL_VERSION_MISMATCH, INVALID_WORKSPACE, INVALID_PERMISSION_MODE, MODEL_UNAVAILABLE, WORKSPACE_BUSY, IDEMPOTENCY_CONFLICT, TASK_NOT_FOUND, TASK_TERMINAL, REQUEST_NOT_FOUND, RESPONSE_NOT_ALLOWED, POLICY_DENIED, HOOK_PROVENANCE_INVALID, BUDGET_EXCEEDED, RESULT_NOT_AVAILABLE, ARTIFACT_NOT_FOUND/RANGE_INVALID, UNSUPPORTED_PLATFORM, INTERNAL_ERROR.

Distinguish infrastructure, permission, model, semantic result and evidence failure. Retry at most one explicitly transient dispatch error after status/identity reconciliation. Do not burn product repair budget on MCP outages. Do not expose inner ZCode tools or credentials to Codex.
