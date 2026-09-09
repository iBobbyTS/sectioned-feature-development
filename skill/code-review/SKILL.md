---
name: code-review
description: "Evidence-based review of a PR, commit range, section or repair delta. In delegated sectioned-feature-development mode, execute one bounded checkpoint, reconciliation or full pass and return candidates/coverage without taking over admission, implementation or acceptance."
---
# Code Review — 4.4.1

## Select execution context first

- `DELEGATED_PASS`: parent provides a frozen packet; read [delegated-pass.md](references/delegated-pass.md). Supports `sfd-delegated-review/4.2` and legacy `sfd-delegated-review/4.1` / atomic `sfd-delegated-review/4.0`. This path overrides standalone loops/acceptance below.
- `STANDALONE`: direct user review request; follow [standalone-workflow.md](references/standalone-workflow.md). Default review-only; no repairs without authorization.

No worktree writes, nested reviewers, changed requirements, invented test authority, or acceptance verdict in a delegated pass. Report candidates, causal evidence, checks, inspected boundaries and actual identity/head. A code-review invocation is one task, not a second orchestrator.

Load [review-coverage.md](references/review-coverage.md) for triggered correctness lenses and [ai-agent-risk-catalog.md](references/ai-agent-risk-catalog.md) only when relevant to the changed behavior. Historical review loop documentation is standalone-only.

## Role, provider and parent handoff

`$code-review` is this review method. [@code_reviewer](subagent://code_reviewer) is specifically the native Codex/Astra role. A ZCode/GLM reviewer is a direct ZAS MCP job; applying this method there does not make it the native role. Do not forward a native task to ZAS or relabel MCP output as native review. Return the actual route/tool-returned identity and result to main; never launch or authorize the next implementation. Main must wait for the required result, admission, delta/final coverage and tests before releasing dependent work.
