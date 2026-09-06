# Audit Mode

## Contents

1. [Purpose and defaults](#purpose-and-defaults)
2. [Evidence sources and session access](#evidence-sources-and-session-access)
3. [Exact requirement record](#exact-requirement-record)
4. [Live trace](#live-trace)
5. [Observational boundary](#observational-boundary)
6. [Completion obligation](#completion-obligation)
7. [Canonical pack workflow](#canonical-pack-workflow)
8. [Status model](#status-model)
9. [Conflict rules](#conflict-rules)
10. [Required analyses and files](#required-analyses-and-files)
11. [Mechanical consistency](#mechanical-consistency)
12. [Safety](#safety)
13. [Final response](#final-response)

## Purpose and defaults

Audit mode measures whether sectioned development improved correctness without creating avoidable planning, review, validation, or process work.

While this skill is under evaluation:

- default mode is `LIVE`;
- the user may explicitly request `audit off`;
- a request after work started uses `POST_HOC` for earlier events and `LIVE` from adoption onward;
- audit does not authorize or require more implementation, reviewers, tests, probes, or product scope.

Record the mode in `FEATURE-STATE.md` before planning. Initialize:

```text
.agent-work/audit/{feature-id}/
├── TRACE.jsonl
├── REQUIREMENTS.md
└── PACK-STATE.json
```

The audit working pack lives at:

```text
.agent-work/audit-packs/{feature-id}/current/
```

The one canonical ZIP lives at:

```text
~/Desktop/audit-pack/{repo}-{feature-id}-sectioned-audit.zip
```

A repeat finalization for the same feature/product head replaces that canonical file atomically after validation; it must not create another timestamped candidate ZIP.

## Evidence sources and session access

Use evidence in this order:

1. Git objects, source at exact base/head, and current tracked worktree;
2. original PLAN/contracts/handoffs/review ledgers and validation output;
3. live trace;
4. relevant Codex session records;
5. agent narrative summaries.

For audit reconstruction the agent may read relevant sessions under only:

```text
~/.codex/sessions
~/.codex-multi-2/sessions
```

Select candidate sessions by repository root, feature time window, branch/feature ID, and task text. Do not copy or summarize unrelated sessions. Do not include raw session files in the pack by default. Produce redacted derived files such as:

```text
session/HUMAN-MESSAGES.md
session/SESSION-TIMELINE.md
session/SESSION-SOURCES.md
```

Preserve timestamps, user messages affecting scope, agent/subagent lifecycle, reviewer interruption, command families, context compaction, and observable idle gaps. Remove credentials, injected system/developer instructions, unrelated repository tasks, and raw secret-bearing payloads.

Use `scripts/session_evidence.py` when its JSONL format matches the installed Codex session format. If it cannot parse a session, record the exact file and parser gap; do not fabricate reconstructed messages.

## Exact requirement record

An audit pack is not complete merely because `PLAN-FULL.md` summarizes the request. At feature activation maintain:

```text
.agent-work/audit/{feature-id}/REQUIREMENTS.md
```

It must contain:

1. exact original user message(s) that define the feature;
2. every later user correction or owner decision that changes scope or semantics;
3. Grill Me questions and the user's answers, grouped by decision chain;
4. a final resolved requirement list;
5. every superseded instruction and the message that superseded it;
6. named failing examples, counterexamples, expected outputs, and environment constraints;
7. source provenance: live capture, session file/message ID, or post-hoc reconstruction.

If Grill Me was not used, write `Grill Me: not used`. If the session source is unavailable, mark the missing verbatim evidence `UNKNOWN`; do not infer it from PLAN or code.

`PLAN-FULL.md` must reference this record and contain the resolved requirement/example matrix. The audit pack includes both the exact record and PLAN history.

## Live trace

Use `scripts/audit_trace.py`. Record major events only:

- audit/requirement initialization and user corrections;
- invocation source, trigger/negative evidence, activation announcement, and automatic-plan approval outcome;
- branch-base choice or late-trigger branch transition;
- stable agent/session role assignments;
- plan frozen and plan-review lifecycle;
- section start, implementation completion, and current section barrier;
- code-review lifecycle, cancellation, and any sequence-gate violation;
- finding admission/rejection/reopening;
- repair and delta closure;
- validation command family/result/code fingerprint;
- scope/foundational-owner decision;
- hard cap/recovery;
- first functionally complete head;
- final product/test head and readiness;
- `.agent-work` tracking/exclusion state;
- audit finalization start/failure/success metadata.

Do not trace every file read, grep, status check, progress message, or plan wording edit.

The trace helper uses a lock and unique record IDs. Sequence gaps, duplicate legacy sequences, unknown future event vocabulary, or missing lifecycle events are telemetry warnings unless they create an unresolved substantive contradiction.

A missing trace field never blocks product work. Record the gap and continue.

## Observational boundary

Audit mode must not:

- add plan or code reviewers;
- upgrade `ONE` to `TWO`;
- add acceptance criteria, tests, probes, analyzers, harnesses, or proof systems;
- rerun a command only to improve audit completeness;
- create a section, repair wave, hard-cap event, or owner decision;
- reopen accepted work;
- fix a product defect found during final audit;
- delay a product-ready conclusion except for generating the required audit artifact itself.

Product readiness and audit delivery are separate. A feature may be `mergeable` while workflow delivery remains `AUDIT_PENDING`.

## Completion obligation

When audit is active, the main agent must not send the final feature-completion response until one of these is true:

- `PACK-STATE.json` is `COMPLETE` and the canonical ZIP verifies; or
- one bounded correction attempt failed and the response explicitly reports `AUDIT_PACK_INCOMPLETE`, the preserved working-pack path, and the validator error.

Before implementation begins, set:

```text
audit_pack_required = yes
audit_pack_state = PENDING
```

At `feature_completed`, immediately transition to audit finalization. Context compaction does not remove this obligation; reread `FEATURE-STATE.md` and `PACK-STATE.json` before final reporting.

Do not rely on memory or a final checklist buried in prior context.

## Canonical pack workflow

### 1. Prepare once

Populate the working pack under:

```text
.agent-work/audit-packs/{feature-id}/current/
```

Do not create a new timestamped directory for each correction.

### 2. Deterministic preflight

Run:

```bash
python {skill-dir}/scripts/audit_finalize.py check \
  --repo . \
  --feature-id {feature-id} \
  --pack-dir .agent-work/audit-packs/{feature-id}/current \
  --trace .agent-work/audit/{feature-id}/TRACE.jsonl \
  --feature-base {feature-base} \
  --product-head {product-head}
```

The checker verifies required files, feature/head identity, manifest inputs, unsafe filenames/content markers, trace status, and pack-local source references. It emits errors before any ZIP is published.

### 3. One bounded correction

Correct only audit artifacts or collection mistakes. Do not rerun product review/tests or change product code. Run `check` once more.

If it still fails, stop as `AUDIT_PACK_INCOMPLETE`; do not generate a succession of partial ZIPs.

### 4. Atomic finalization

Run:

```bash
python {skill-dir}/scripts/audit_finalize.py finalize \
  --repo . \
  --feature-id {feature-id} \
  --pack-dir .agent-work/audit-packs/{feature-id}/current \
  --trace .agent-work/audit/{feature-id}/TRACE.jsonl \
  --feature-base {feature-base} \
  --product-head {product-head} \
  --desktop-root ~/Desktop/audit-pack
```

The finalizer:

- holds a feature-local lock;
- creates `PACK-METADATA.json` and `PACK-MANIFEST.sha256`;
- writes a temporary ZIP;
- verifies its manifest;
- atomically replaces the canonical ZIP;
- writes the sidecar SHA-256 and `PACK-STATE.json`;
- returns the existing canonical ZIP unchanged when the source fingerprint is identical.

Do not append another “pack generated” event and rebuild solely to make that event appear inside the ZIP. `PACK-METADATA.json` and `PACK-STATE.json` are the authoritative finalization record.

## Status model

Report separate axes.

### Pack status

```text
COMPLETE
COMPLETE_WITH_GAPS
INCOMPLETE
FAILED
```

### Telemetry status

```text
VALID
DEGRADED
INVALID
```

### Evidence consistency

```text
CONSISTENT
RESOLVABLE_DRIFT
CONFLICTED
```

### Product/readiness status

Use the workflow's normal functional and merge-readiness verdict independently.

A useful final combination is:

```text
Pack: COMPLETE_WITH_GAPS
Telemetry: DEGRADED
Evidence consistency: CONSISTENT
Product: MERGEABLE
```

Do not collapse all axes into one global `CONFLICTED` label.

## Conflict rules

Use `CONFLICTED` only when an unresolved contradiction can change at least one substantive conclusion and cannot be mechanically isolated:

- feature base/head/range identity;
- exact human requirement or supersession state;
- whether a material finding existed or was admitted;
- whether a repair changed product/test code and closed that finding;
- final product/test head covered by required evidence;
- source snapshot/patch identity;
- functional or merge-readiness verdict;
- cross-feature contamination that cannot be excluded from the current feature.

Use `RESOLVABLE_DRIFT` or telemetry `DEGRADED`, not `CONFLICTED`, for:

- stable finding IDs renamed while root cause, repair, and closure agree;
- trace sequence gaps/duplicates or unknown event names;
- missing reviewer lifecycle events when original ledgers exist;
- stale narrative counts when mechanical counts are available;
- duplicate audit-pack attempts;
- missing or compaction-sensitive token counters;
- stale process-only state fields;
- prior-feature artifacts that can be mechanically excluded;
- timestamp or branch-display drift that does not alter exact Git objects.

When a narrative count differs from a mechanical count, preserve both, use the mechanical value, and record `METADATA_DRIFT`.

Several completed audits in the evaluation set were falsely made globally conflicted by finding-ID renumbering, under-recorded trace events, duplicate sequences, or stale wave counts. V3.8 treats those as degraded telemetry unless product evidence itself is contradictory.

## Required analyses and files

The working pack contains at least:

```text
00-README.md
AUDIT-VERDICT.md
HUMAN-REQUIREMENTS.md
INVOCATION-AUDIT.md
COUNTERFACTUAL-MINIMUM.md
PLAN-AUDIT.md
SCOPE-AUDIT.md
REVIEW-AUDIT.md
VALIDATION-AUDIT.md
COST-METRICS.md
SKILL-COMPLIANCE.md
RECOMMENDATIONS.md

requirements/
  REQUIREMENTS.md
planning/
evidence/
git/
sources/base/
sources/head/
session/
trace/
```

### Human requirements

Include exact messages/decisions from `REQUIREMENTS.md`, final behavior, owner, evidence, and `SATISFIED | PARTIAL | NOT_SATISFIED | UNKNOWN`. Do not infer human authority from PLAN or reviewer prose.

### Invocation audit

Record `USER_EXPLICIT | CUSTOM_INSTRUCTIONS_AUTO | AGENT_DISCRETION`, exact trigger and negative evidence, predicted versus actual scope/risk, activation timing, user approval checkpoint when automatic, and `JUSTIFIED | BORDERLINE | OVER_TRIGGERED | UNDER_TRIGGERED | UNKNOWN`. For automatic invocation, check whether merely touching a high-risk module was mistaken for changing its high-risk semantics or whether the plan predicted far more sections/mechanisms than the final minimum implementation.

### Counterfactual minimum

Describe the smallest reasonable implementation from the feature base and classify actual work as product-required, unavoidable correctness, reasonable maintainability, optional, plan-created, review-created, process-only, or pre-existing. Mark it `ADVISORY_INFERENCE`.

### PLAN audit

Cover requirement/Grill Me traceability, section proportionality, necessity-first rejection of plan-created mechanisms, triggered representation/lifecycle/inventory/foundation lenses, plan-review findings, rework avoided, and reviewer dispatch failures.

### Review audit

Cover initial/delta/final/integration passes, stable reviewer IDs and role separation, section sequencing, finding causality/authority/materiality, repairs and closure, repeated rediscovery, reviewer-created scope, repair budget, and unique defect yield.

### Validation and cost

Mechanically group commands by code fingerprint. Separate targeted, section, feature, reproduction, and duplicate unchanged evidence. Separate wall-clock, active agent time, user absence, waiting, subagent runtime, and unattributed gaps. Do not present cumulative/compaction-sensitive token counters as exact feature cost.

### First functionally complete head

Identify it when evidence supports doing so, then classify later work as correctness, integration, required validation, maintenance, scope expansion, process-only, or audit-only.

## Mechanical consistency

Before conclusions verify:

- cited commits are in `git rev-list {feature_base}..{current_head}` or are explicitly process-only after product head;
- every counted finding points to an included original review artifact;
- every repair wave has an admitted finding, product/test repair, and closure;
- delivered product/test head equals required review/validation head;
- current feature artifacts are isolated;
- LOC, review calls, validations, branches, retries, and recovery are mechanically counted;
- source snapshots match claimed base/head blobs;
- requirement text provenance is present or marked missing;
- the canonical ZIP manifest verifies.

Do not mark the audit conflicted merely because trace telemetry is incomplete when Git and original ledgers establish the substantive facts.

## Safety

Never include:

- `.env`, credentials, tokens, cookies, auth state, browser profiles, private keys;
- secret-bearing command arguments or copied local configs containing secrets;
- `node_modules`, virtual environments, build outputs, caches, downloaded models/data;
- raw unrelated session history or full `.git` directories.

A local config may be represented by a redacted schema/diff summary when it is part of the feature; do not copy secret values.

## Final response

Report only:

```text
Pack status:
Telemetry status:
Evidence consistency:
Invocation source / assessment:
Feature base:
Final product/test head:
Current head:
Functional result:
Merge readiness:
Scope result:
Review efficiency:
Validation efficiency:
Skill result:

Mechanical facts:
- commits and LOC classes:
- plan/code review calls:
- admitted defects / repair waves / hard caps:
- broad validations / duplicate unchanged validations:
- git diff --check runs:
- active agent time / unattributed gaps:

Known evidence gaps:
Known substantive conflicts:
Canonical audit pack:
SHA-256:
```

Then stop. Do not fix an audit-discovered product issue or begin another section.


## V3.9 External reviewer and Advisor evidence

For every external review event record: provider (`SOL` or `ZCODE`), stable agent/session/review IDs, daemon instance, base/head, review kind, dispatch/completion/cancellation timestamps, continuation relationship, artifact hash, and differentiated MCP/daemon/ZCode/model error class.

For every Advisor escalation record: trigger ID, evidence predicate, freeze head/status, request/context-manifest hashes, native launch identity/timestamp, Advisor result verbatim/provenance, main admission (or human product/risk decision when required), and resulting bounded action. Advisor recording is required when Audit is on; escalation itself remains available when Audit is off.

## 4.2 process-only namespace and inherited model/subsection records

`~/Desktop/audit-pack/` and this skill's `.agent-work/audit-packs/` are reserved for this skill's process audits only. New packs require PROCESS-IDENTITY.json with kind `sectioned-development-process-audit`, producer `sectioned-feature-development`, feature_id, run_id, feature_base and source_head. A code/security audit, runtime conformance result, external Advisor repository export, screenshot archive or arbitrary ZIP is not a process sample. Place it outside these directories; the process pack may reference its hash/path as supporting evidence without copying it as a second audit. Do not delete/move legacy user archives; classify them during intake.

The canonical writer remains the retained v3.9 `audit_finalize.py`: atomic ZIP, manifest/CRC, exact Git base/head checks, local PACK-STATE, idempotent reuse and one bounded correction. The inherited `process_audit.py` offers typed/legacy intake and v4 compatibility; it does not replace the required v3.9 analyses or secretly export another pack.

Include all original v3.9 requirement/invocation/scope/counterfactual/review/cost/recovery analyses. Also include MODEL-TASK-AUDIT.md, PARALLEL-AUDIT.md, SUBSECTION-AUDIT.md and ADVISOR-AUDIT.md (NOT_APPLICABLE when absent). For each real subagent record role, actual actor/session, parent/child/lineage, task/diff hashes, requested vs observed model/effort, task features, input/result/launch receipt, check evidence, all attempts and error class. Low-tier failure, model escalation, review/repair/validation/Advisor costs all contribute to accepted-outcome cost. UNKNOWN is not zero.

For subsections distinguish logical parent review ID from real call count; checkpoint verification never becomes child acceptance. Record cross-child invalidations, joint-oracle results and cumulative repair before/after. For parallel work record planned/actual dependency DAG, read/write/contracts/resources, start/end, reservations, worktrees, overlap/conflict/abandoned work, serial integration order and merged-head defects; wall critical path is not worker-time sum. For native Advisor record bounded context/launch evidence, request/decision hash and main admission even when parent model equals Advisor model.

Audit OFF disables only telemetry/pack, not required PLAN, task, contract, handoff, reviews, real actors, recovery/closure evidence. Failed/missing measurements may degrade telemetry, but do not manufacture product repairs or rerun gates. Product-data token exports are not Agent development cost.
