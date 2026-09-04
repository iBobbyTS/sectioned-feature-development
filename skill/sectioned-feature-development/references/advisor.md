# Native advisor — independent adjudication

The advisor is `advisor` (`gpt-6-astra`, xhigh). It is not a third routine reviewer or a manual ChatGPT Pro task. It remains available when audit is off. Model superiority is not the trigger, especially when the main agent also uses Astra; the benefit sought is a fresh bounded evidence view.

## Rare triggers

Preserve the prior handoff contract and trigger intent:
- ADV-01: an original lineage used one structural recovery and again cannot converge within its cumulative boundary.
- ADV-02: independent valid reviews retain incompatible, materially consequential conclusions on the same frozen proposition after one shared targeted reproduction.
- ADV-03: the only proposed next action discards a substantial coherent accepted design/section; a local defect is not sufficient.
- ADV-04: two unresolved trust/consistency/state-owner models have materially different complexity or safety consequences and existing authority/probes do not select one.
- ADV-05: source, deterministic evidence and review conclusions still contradict release readiness after one comparable rerun.
- ADV-06: bounded real probing leaves external system shape uncertain, and proceeding commits to an expensive/irreversible architecture.

No escalation for ordinary findings, first hard cap, a simple owner product question, tool outage, credentials, audit gaps or incidental nits. Do not request an advisor before and after every task.

## Isolated context

Keep `assets/ADVISOR-REQUEST.template.md` byte-for-byte unchanged. Fill it as a request, not a persuasive answer. The legacy “Sol position” field may describe the current GPT review position explicitly; don't silently relabel source claims. Add `ADVISOR-CONTEXT.json` beside it:

```json
{"request_id":"ADV-request-id","source_commit":"exact-sha","fresh_context_required":true,"inherit_parent_history":false,"allowed_documents":["ADVISOR-REQUEST.md","REQUIREMENTS-CONTRACT.md"],"source_paths":["relevant/owner"],"excluded_context":["full-parent-chat","raw-rollouts","other-feature-plans","unrelated-review-narrative"],"expansion_policy":"one-targeted-evidence-request"}
```

Launch through a native fresh-context subagent facility, using the actual tool schema. When `fork_context` exists, request false; **do not assume this field exists** and do not add it to TOML. Verify the launch metadata/context manifest. Read-only sandbox prevents writes but does not remove inherited context. A prompt telling an inherited agent to “ignore history” is not isolation. If the harness cannot establish a noninherited context, return ADVISOR_CONTEXT_BLOCKED; do not simulate a successful isolated consultation.

Provide the request, confirmed requirements and actual frozen source/worktree. No whole-repository ZIP or raw transcript is required. Initial evidence is concise and claim-specific; the advisor can inspect actual relevant code/tests and ask once for additional named source evidence. Never deny necessary source access just to meet an arbitrary token cap. Do not attach all previous reasoning by default.

## Decision protocol

Freeze affected writers/reviewers and set advisor state REQUIRED. Dispatch a fresh `advisor` instance even when the parent is Astra. It must independently determine the minimum safe technical boundary and return:

- request ID and exact source head;
- decision / evidence vs assumptions / rejected alternatives;
- preserved work, permitted and forbidden scope;
- needed checks and exact resume phase;
- unresolved human-owned product/risk choices.

Allowed technical dispositions: CONTINUE_CURRENT, SIMPLIFY_CURRENT, REPLAN_REMAINING, REBOUND_OWNER, STOP_FOR_OWNER_DECISION, NEED_EVIDENCE. RESTART_FROM_BASE is a recommendation only; it never authorizes destructive Git. Advisor cannot implement, launch subagents, merge, expand requirements, or turn a suggestion into authority.

Save response verbatim with actor/model/effort/context hashes. Main admits the bounded technical decision automatically if within existing authority; ask the human only for genuine product/risk/destructive changes. Resume only affected work with inherited budgets and accepted evidence. No recursive advisor-on-advisor or multiple competing advice calls on unchanged facts.

When audit is on, include trigger facts, request/template digest, allowed/actual context manifest, instance provenance, exact source, decision, main admission, resumed outcome and all advisor token/time costs. Audit cannot trigger a consultation.
