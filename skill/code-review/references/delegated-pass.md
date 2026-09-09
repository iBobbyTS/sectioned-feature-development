# Delegated review — 4.1

`context=DELEGATED_PASS`; protocols `sfd-delegated-review/4.2`, `sfd-delegated-review/4.1` and flat-packet compatibility `sfd-delegated-review/4.0`.

Parent owns scope admission, repair assignment, budgets, review/provider scheduling, acceptance and integration. Return one signal: CLEAN, MATERIAL_CANDIDATES, INSUFFICIENT_EVIDENCE. CLEAN refers only to the requested pass/range, never automatic parent acceptance.

## Exact scope

- INITIAL_BOUNDED / FINAL_BOUNDED: specified whole parent base→candidate and direct impact cone.
- REPAIR_DELTA: frozen findings, repair diff and invalidated impact only.
- SUBSECTION_DELTA: **new implementation** in one bounded child plus parent invariants and previously reviewed interfaces. This is not repair-only review. Use explicit parent/child IDs, safe intermediate behavior and planned consumer. Unimplemented later child is not a defect unless this checkpoint already exposes wrong public behavior or violates the stated invariant.
- PARENT_RECONCILIATION: complete primary coverage at final parent head; inspect cross-child interactions, changed prior paths, real consumer and joint oracles. Earlier local clean records do not prove composition. Do not mechanically reread every unchanged line or accept from a checklist alone.

Within one parent primary logical pass, repeated checkpoints are not a new counted full pass. Their real model calls still count as cost. Later independent parent final is a fresh full pass; the parent owns provider alternation.

## Assurance (parent-owned, not reviewer authority)

ONE with material repair closes the originating pass **and requires one fresh final full pass**. TWO requires covered primary/closure **plus a fresh independent final full pass**. Child CHECKPOINT_VERIFIED does not earn either independent final or external dependency readiness; no per-child ONE/TWO or budget. All repair attempts roll up to the original lineage.

## Causality and evidence

Each material candidate must identify changed code/contract cause, supported reachable trigger, existing requirement/production authority, concrete consequence and smallest bounded repair. Non-goals and speculative security/compatibility preferences remain proposals. Inspect unchanged dependencies only along the exact causal path. Test-only proof infrastructure needs existing acceptance authority, not reviewer taste.

If the frozen candidate changes during review, stop and report invalid evidence; preserve useful observations, don't bless the new head. Independent sibling writers in isolated worktrees are not a violation. Missing stable reviewer identity or exact candidate evidence produces INSUFFICIENT_EVIDENCE, not clean.

A successful external task or hash-valid artifact is not automatically a clean review. Verify the semantic report and distinguish requested model from observed provider telemetry.

## Continuity

Use the real original reviewer session for bounded follow-up when possible. Current ZCode terminal agents cannot receive new messages: record `same_session=false` and `TERMINAL_CONTINUATION_UNSUPPORTED` for approved same-provider fresh delta fallback; strict continuity returns `CONTINUITY_BLOCKED`. Do not invent resume tools or silently replace a reviewer while claiming continuity.

## Return

Pass ID, logical parent pass, actual agent/session, provider/requested-vs-observed model, parent/child IDs, exact base/head, coverage and pending behavior, checks reused/newly run/gaps, candidate evidence and proposed classification, checkpoint invalidations and joint-oracle result where applicable. No edits, repairs, commits, other subagents or final section acceptance.

## ZAS observation in 4.3.1

Review scope, result signals and provider alternation are unchanged. Only the parent caller invokes the installed zcode_subagent_observe when it suspects meaningless looping; the five judgment definitions belong to that MCP description, not this review state machine. Observe includes calls without results and a verified public reasoning tail by default, never encrypted_content. Detailed telemetry is stored in the feature's paired xxx-zas.zip.

## Agent-managed parent (4.4)

The parent now schedules from readable files. Existing sfd-delegated-review/4.2 (and flat /4.0) denotes the same pass semantics, not a required JSON envelope. Plain Markdown with scope, actual identity, candidate head, evidence and candidates is valid. Do not demand registry, signed receipts, STATE.json, extra hashes or workflow.py approval. This does not weaken scope, ONE/TWO, fresh reviewers, candidate immutability or real tests.
