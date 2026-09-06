# Sectioned process audit v4

## Purpose and placement

Default LIVE; explicit `audit off` disables collection, not quality gates or advisor availability. This is observational evaluation, not a product audit or a new implementation phase.

Working data: `.agent-work/features/<feature_id>/runs/<run_id>/audit/`.
Canonical published ZIP: `~/Desktop/audit-pack/<repo>-<feature_id>-<run_id>-sfd-audit.zip`.
Only a pack with `artifact_type=sectioned-development-process-audit`, producer name `sectioned-feature-development`, schema version 4, matching feature/run identity, evidence manifest and declared coverage belongs in that published folder.

Runtime/conformance/product-safety/manual-advisor diagnostics belong elsewhere (for example `.agent-work/runtime-evidence/` or `~/Desktop/runtime-evidence/`). Reference a sanitized summary/hash from the process pack; don't nest arbitrary ZIPs or copy raw event dumps. Never delete or move the user's existing foreign packs automatically. Intake labels them EXCLUDED_AUXILIARY with reason; older multi-document workflow packs are LEGACY_PROCESS, not v4-compliant by inference.

## Minimal live events

Record only existing transitions: invocation/rejection/approval, requirements confirmed, explorer result, plan frozen/reviewed, section/model selection, agent dispatch/result/cancel, review reservation/result, finding admission, repair/escalation, validation, integration, advisor, completion/follow-up assessment and audit finalization.

Stable common keys: event_id, schema_version, feature_id, run_id, request_id, section_id, phase, timestamp, actor_id, parent_actor_id, capture=LIVE/RECONSTRUCTED, source_head, source_artifact/hash. Event families are open with explicit family; an unknown specific name is not automatically invalid.

### Model/task evaluation

For each actual attempt record requested and observed model/effort (unknown is null), profile, task type, analogue evidence, ambiguity, semantic path, state coupling, oracle strength, novelty, routing confidence, expected/actual changed owners, context manifest/bytes, failures, admitted/escaped defects, repair/escalation parent, cancelled work, validation cost and acceptance.

Track planner/explorer/reviewer/advisor cost as well as implementation. No cost entry for “no external paid API calls” proves zero local model cost. Never use an application's exported token totals as development telemetry.

Per-request usage is preferable. Preserve input/cache-read/cache-write/output/reasoning fields with provider semantics and raw-source provenance. Cached input may be a subset of input; reasoning may be included in output. Do not add them twice. Keep billed cost separately from a list-price estimate with rates, effective date, cache semantics, service tier and long-context tier. Missing rates/usage => UNKNOWN, not zero. Requested model != observed model.

### Parallel evaluation

Record DAG revision, ready set, task branch/base/workspace, resources, dependency acceptance/integration, start/end, cancellation/rework/conflicts and integrated-head evidence. Wall time is union of concurrent intervals; worker-seconds are their sum. Long gaps without evidence remain UNATTRIBUTED_GAP, not “user confirmation” or model compute. Track critical-path latency separately from aggregate cost.

### Review and advisor

Finding counts need actual ledgers; repair attempts consume budget even before successful closure. Record plan-detectable category (owner/representation/lifecycle/environment/implementation-only), missed oracle and minimal counterfactual, with inference labeled.

Independent review IDs, exact frozen snapshots, full-pass reservations, same-session delta or terminal gap, protocol failures and accepted evidence must be distinguishable. Advisor capture includes limited-context proof and unchanged request-template hash, not full parent history.

## Final pack

Required artifacts: `metadata.json`, `SUMMARY.md`, `REQUIREMENTS.md`, `PLAN-AUDIT.md`, `REVIEW-AUDIT.md`, `MODEL-TASK-AUDIT.md`, `PARALLEL-AUDIT.md`, `VALIDATION-AUDIT.md`, `ADVISOR-AUDIT.md`, `COST-METRICS.md`, `events.jsonl`, `EVIDENCE-MANIFEST.json`. Use NOT_APPLICABLE/UNKNOWN honestly in unused sections. Include plan revisions/state/review reports and relevant base/head source snapshots or record a code-evidence gap.

Only include manifest-authorized regular files under the staging directory; no symlink traversal, .git, raw sessions, credentials, env files, build/cache directories or nested ZIP. Record original request/grill provenance redacted as needed. Reading relevant `~/.codex/sessions` or `~/.codex-multi-2/sessions` is allowed for local reconstruction; filter exact feature/time/IDs and do not copy unrelated sessions. Audit tooling does not grant a network/upload capability.

`audit.py publish` validates identity/manifest, checks obvious secret patterns, builds atomically, verifies CRC and hashes, and reuses unchanged content at the canonical path. One bounded correction after a packaging failure; no timestamp retry cascade. Never call a new code reviewer or rerun product tests to improve the pack.

## Status axes

Pack: COMPLETE / COMPLETE_WITH_GAPS / INCOMPLETE.
Evidence: CONSISTENT / RESOLVABLE_DRIFT / CONFLICTED.
Telemetry: VALID / DEGRADED / INVALID.
Product: MERGEABLE / INSUFFICIENT_EVIDENCE / BLOCKED / INCOMPLETE.

Product defect or unavailable runtime does not mean audit conflict. CONFLICTED requires an unresolved material contradiction about requirements, identity, actual findings/closure, source head or acceptance. A corrected event count or parseable legacy name is drift. Keep conflicting source statements visible rather than making up a reconciled story.

## Evaluation discipline

Use separate quality/efficiency/routing-compliance results, not one weighted score. Insufficient code evidence is excluded from quality comparison. Human-discovered escaped defects and eventual corrected quality are separate. Do not maximize skill usage coverage: correct de-escalation is success.

Compare total cost per accepted task across matched task families, uncertainty/oracle tiers and difficulty tails. Production trials are not randomized benchmarks. State sample size, selection effects and missing data. A weak executor may cost more after premium review/repair; a long detailed plan may cost more than its cheap implementation saves. Update routing only after repeated evidence or a clear rule-level defect; don't reduce checks to hit a cost target.

## 4.1 subsection observations

Keep schema_version=4; producer.version=4.1 and workflow_revision=4.1 distinguish additive records. For subsection events record parent_section_id, subsection_id, lineage_id, checkpoint base/head, logical review ID and actual reviewer identity. Record joint-oracle coverage and invalidation before parent acceptance. All real child review, recheck, repair and synthesis costs roll up to the parent; lower logical full-pass count is not proof of lower cost or unchanged defect rate. Children never count as accepted features. No per-child audit ZIPs or parallel audit state machines.
