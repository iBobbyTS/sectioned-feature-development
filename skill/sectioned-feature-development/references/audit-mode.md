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
- branch-base choice;
- plan frozen and reviewer lifecycle;
- section start and implementation completion;
- code reviewer lifecycle;
- finding admission/rejection/reopening;
- repair and delta closure;
- validation command family/result/code fingerprint;
- scope/owner decision;
- hard cap/recovery;
- first functionally complete head;
- final product/test head and readiness;
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

Several completed audits in the evaluation set were falsely made globally conflicted by finding-ID renumbering, under-recorded trace events, duplicate sequences, or stale wave counts. V3.7 treats those as degraded telemetry unless product evidence itself is contradictory.

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

Record `USER_EXPLICIT | CUSTOM_INSTRUCTIONS_AUTO | AGENT_DISCRETION`, exact trigger evidence, predicted versus actual scope/risk, and `JUSTIFIED | BORDERLINE | OVER_TRIGGERED | UNDER_TRIGGERED | UNKNOWN`. For automatic invocation, check whether merely touching a high-risk module was mistaken for changing its high-risk semantics.

### Counterfactual minimum

Describe the smallest reasonable implementation from the feature base and classify actual work as product-required, unavoidable correctness, reasonable maintainability, optional, plan-created, review-created, process-only, or pre-existing. Mark it `ADVISORY_INFERENCE`.

### PLAN audit

Cover requirement/Grill Me traceability, section proportionality, plan-created scope, triggered representation/lifecycle/inventory lenses, plan-review findings, rework avoided, and reviewer dispatch failures.

### Review audit

Cover initial/delta/final/integration passes, finding causality/authority/materiality, repairs and closure, repeated rediscovery, reviewer-created scope, repair budget, and unique defect yield.

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
