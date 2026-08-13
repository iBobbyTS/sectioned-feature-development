# Optional Process Audit Mode

## Contents

1. [Purpose and activation](#purpose-and-activation)
2. [Invocation provenance](#invocation-provenance)
3. [Live trace](#live-trace)
4. [Events to record](#events-to-record)
5. [Observational boundary](#observational-boundary)
6. [Final read-only audit](#final-read-only-audit)
7. [Mechanical consistency gates](#mechanical-consistency-gates)
8. [Required analyses](#required-analyses)
9. [Audit pack layout](#audit-pack-layout)
10. [Safety and final response](#safety-and-final-response)

## Purpose and activation

Audit mode measures whether sectioned development was proportionate: why the skill was activated, what the user actually requested, what PLAN/review added or removed, where time/tokens/validation were spent, and whether the workflow created avoidable work.

Audit is `OFF` by default. Enable it only when the user explicitly asks to audit, collect workflow data, or run with audit mode. The agent must not enable audit merely because the feature is complex.

Use one mode:

- `LIVE`: the user enables audit before or during development. Initialize an append-only trace and record major events as work proceeds.
- `POST_HOC`: the user asks after the feature/stage ends. Do not invent live records; reconstruct from Git/artifacts/session evidence and label every reconstructed item.

When the user enables `LIVE`, run:

```bash
python {skill-dir}/scripts/audit_trace.py init \
  .agent-work/audit/{feature-id}/TRACE.jsonl \
  --feature-id {feature-id} \
  --skill-version V3.5 \
  --invocation-source {USER_EXPLICIT|CUSTOM_INSTRUCTIONS_AUTO|AGENT_DISCRETION} \
  --invocation-timing {FEATURE_START|MID_FEATURE} \
  --trigger-evidence "{exact user statement or matched rule}" \
  --audit-enabled-by "{exact user audit request}" \
  --feature-base {sha} \
  --repo .
```

Do not commit every trace append. Preserve it with coherent section/final process artifacts or leave it uncommitted when repository rules exclude audit data.

## Invocation provenance

The audit must distinguish how `$sectioned-feature-development` started:

- `USER_EXPLICIT`: the user named the skill or directly required this workflow.
- `CUSTOM_INSTRUCTIONS_AUTO`: the user requested the feature normally, and a mandatory Custom Instructions trigger activated the skill.
- `AGENT_DISCRETION`: no explicit user request or mandatory trigger required it; the agent chose the workflow.

Also record:

- invocation timing: `FEATURE_START` or `MID_FEATURE`;
- exact user text/rule that triggered it;
- predicted signals at activation: estimated behavioral LOC, owner/module count, semantic boundaries, impact-cone uncertainty, prior review failure;
- resolved review assurance and its reasons.

At final audit, compare predicted signals with actual product/test diff and behavior. Classify activation:

- `JUSTIFIED` — actual scope/risk supported sectioned development;
- `BORDERLINE` — useful but workflow burden was high relative to the change;
- `OVER_TRIGGERED` — an automatically selected workflow made a small bounded task materially more complex without useful findings;
- `UNDER_TRIGGERED` — the task was treated as small but later required sectioning/recovery;
- `UNKNOWN` — evidence is insufficient.

Do not call explicit user selection an agent trigger error. You may still assess whether the resulting plan/review depth was proportionate.

## Live trace

The trace is a measurement log, not another workflow ledger. Record major events only. Do not log every file read, grep, status check, or conversational update.

Append with:

```bash
python {skill-dir}/scripts/audit_trace.py append \
  .agent-work/audit/{feature-id}/TRACE.jsonl \
  --event {event} \
  --phase {phase} \
  --summary "{short factual summary}" \
  --repo . \
  --actor {main|implementer|reviewer|planner|user|tool} \
  --profile {profile-or-none} \
  --field key=value
```

Validate periodically and before packing:

```bash
python {skill-dir}/scripts/audit_trace.py validate \
  .agent-work/audit/{feature-id}/TRACE.jsonl

python {skill-dir}/scripts/audit_trace.py summary \
  .agent-work/audit/{feature-id}/TRACE.jsonl \
  --output .agent-work/audit/{feature-id}/TRACE-SUMMARY.json
```

The script records current branch, HEAD, tracked-diff SHA-256, and status SHA-256. This allows repeated checks on unchanged code to be identified mechanically.

## Events to record

Record these when they occur:

- `user_requirement` — original requirement or later explicit correction/decision;
- `plan_frozen` — PLAN-FULL validated, including plan fingerprint and section count;
- `plan_review_dispatched`, `plan_review_completed`, `review_cancelled`;
- `section_started`, `implementation_completed`;
- `review_dispatched`, `review_completed`;
- `finding_admitted`, `finding_rejected`;
- `repair_completed` — one coherent repair wave and finding IDs;
- `validation_completed` — command family, result, duration if known, and whether targeted/section/broad;
- `scope_change` — approved narrowing/expansion and authority;
- `owner_decision`;
- `hard_cap`, `recovery_completed`;
- `functional_head` — first head where the original user-visible outcome was substantially complete;
- `feature_completed` — final product/test head and readiness;
- `audit_note` — bounded measurement caveat;
- `audit_pack_generated`.

For reviewer lifecycle, record dispatch ID/profile, mode, reviewed base/head, result, candidate/admitted counts, and interruption/timeout. For validation, record the exact command family and result but redact secret-bearing arguments and environment values.

## Observational boundary

Audit mode must not:

- add plan or code reviewers;
- change `ONE`/`TWO` assurance;
- add acceptance criteria, tests, probes, analyzers, or proof systems;
- rerun a command only to improve audit completeness;
- create a section, repair wave, hard-cap event, or owner decision;
- block implementation because a trace field is missing;
- fix defects found during the final audit.

A trace or audit-format failure is process metadata, not product evidence failure. Record the gap and continue the underlying workflow.

## Final read-only audit

At the requested feature/stage stopping point, stop modifying product code, tests, plans, contracts, reviews, and Git history. Do not call implementers or reviewers. Do not rerun tests merely for the audit.

Create:

```text
.agent-work/audit-packs/{YYYYMMDD-HHMM}-sectioned-audit/
```

Then zip it as:

```text
.agent-work/audit-packs/{YYYYMMDD-HHMM}-sectioned-audit.zip
```

Use the live trace as the primary event source. Use Git and original artifacts as the source of truth for code ranges and review findings. If trace and source disagree, preserve the conflict; do not silently reconcile it.

## Mechanical consistency gates

Before drawing conclusions, verify:

### Feature range

Every feature commit cited must belong to:

```bash
git rev-list {feature_base}..HEAD
```

A commit outside that range is `OUT_OF_FEATURE_RANGE` and excluded from feature metrics.

### Findings and repair waves

Every counted finding must point to an included original review artifact with reviewed base/head, class, admission, repair diff/commit, and closure. Missing evidence makes it `UNVERIFIED_FINDING`.

A repair wave counts only when all three exist:

```text
admitted material finding + product/test repair diff + closure evidence
```

Process-document edits, fingerprint changes, or reviewer restarts are not repair waves.

### Final-head evidence

The delivered product/test head must equal the head covered by required review and validation. Later process/docs-only commits are listed separately.

### Cross-feature isolation

Every PLAN, review, finding, commit, and test result must belong to the current feature ID/range. If prior-feature artifacts entered the diff or audit:

```text
CROSS_FEATURE_CONTAMINATION
AUDIT_STATUS = CONFLICTED
```

Exclude contaminated lines/events from isolated metrics while preserving raw values.

### Counts

Mechanically derive commits, changed paths, LOC classes, reviewer artifacts, repair waves, validation commands, hard caps, retries, and branch/worktree events. If a narrative value conflicts with Git/trace/artifacts, report both values and mark the audit `CONFLICTED`.

### Time and tokens

Separate:

- `WALL_CLOCK_SPAN`;
- `ACTIVE_AGENT_TIME` when directly observable;
- `IDLE_OR_USER_ABSENCE`;
- `WAITING_FOR_USER`;
- `WAITING_FOR_TOOL`;
- `SUBAGENT_RUNTIME`;
- `UNATTRIBUTED_GAP`.

Never treat a long gap between events as agent effort without evidence. Cumulative/compaction-sensitive token counters are retained as raw telemetry but not presented as exact feature cost.

## Required analyses

### Human requirements

Create `HUMAN-REQUIREMENTS.md` with original user text, later explicit corrections, superseded guidance, final behavior, owner, evidence, and `SATISFIED | PARTIAL | NOT_SATISFIED | UNKNOWN`. Do not infer human authority from PLAN or reviewers.

### Invocation audit

Create `INVOCATION-AUDIT.md` containing:

- invocation source/timing and exact evidence;
- predicted trigger signals;
- actual product/test LOC, behavioral owners, semantic boundaries, sections, assurance, findings, and repairs;
- `JUSTIFIED | BORDERLINE | OVER_TRIGGERED | UNDER_TRIGGERED | UNKNOWN`;
- for automatic invocation, whether the agent confused merely touching/reading a high-risk boundary with materially changing its semantics;
- counterfactual normal-workflow cost for a small bounded task.

### Counterfactual minimum

Create `COUNTERFACTUAL-MINIMUM.md`: describe the smallest reasonable implementation from the feature base, then classify actual work as `REQUIRED_PRODUCT`, `UNAVOIDABLE_CORRECTNESS`, `REASONABLE_MAINTAINABILITY`, `OPTIONAL_IMPROVEMENT`, `PLAN_CREATED_SCOPE`, `REVIEW_CREATED_SCOPE`, `PROCESS_ONLY`, or `LEGACY_PREEXISTING`. Mark this analysis `ADVISORY_INFERENCE`.

### PLAN audit

Create `PLAN-AUDIT.md` covering requirement traceability, section proportionality, PLAN-created scope, plan-review findings, rework avoided, plan-review dispatch/retry cost, and whether a clean plan review added measurable value.

### Review audit

Create `REVIEW-AUDIT.md` covering each initial/delta/final/integration pass, finding causality/authority/materiality, repair and closure, repeated full rediscovery, accepted-section reopening, reviewer-created scope, repair budget, interrupted/duplicate reviewer dispatches, and unique defect yield from FINAL review.

### Scope audit

Create `SCOPE-AUDIT.md` listing every new service, registry, state machine, worker, persistence layer, parser/analyzer, CI rule, security control, proof/evidence harness, compatibility layer, public API/config/UI surface, and observability mechanism. Record who introduced it, authority, necessity, extra work caused, and whether it remains.

### Validation audit

Create `VALIDATION-AUDIT.md`. For each command family record count, exact code fingerprints, targeted/section/broad classification, result, duration if known, and whether it was `TARGETED_AFTER_CHANGE`, `SECTION_GATE`, `FEATURE_GATE`, `REPRODUCTION`, `DUPLICATE_UNCHANGED_EVIDENCE`, or `UNKNOWN`.

At minimum count focused tests, full suites, lint/check/typecheck, formatter, build/package, browser/E2E, migration generation, `git diff --check`, and CodeGraph. Do not call repository-internal duplicate steps agent reruns unless the agent invoked the outer gate repeatedly.

### Cost and functional-first audit

Create `COST-METRICS.md` with product/test/harness/user-doc/process-doc LOC, ratios, commits, reviewer/repair/recovery counts, time/token evidence, and the first functionally complete head. Classify work after that head as correctness, integration, validation, maintenance, scope expansion, process-only, or audit-only.

### Skill compliance and version signal

Create `SKILL-COMPLIANCE.md` and `AUDIT-VERDICT.md`. Distinguish:

- skill design defect;
- execution deviation;
- repository/environment issue;
- feature implementation bug;
- audit data conflict.

Do not recommend a skill update from one ordinary implementation bug. Use `STRONG_SKILL_DEFECT_SIGNAL` only when the same workflow failure repeats across features, the skill explicitly requires the waste/error, or correct compliance still makes it unavoidable.

## Audit pack layout

Include at least:

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

trace/
  TRACE.jsonl                  # live mode, when available
  TRACE-SUMMARY.json
planning/
evidence/
git/
sources/base/
sources/head/
session/                       # redacted or derived timeline
```

`planning/` includes PLAN-FULL, PLAN, state, contracts, handoffs, and review ledgers. `git/` includes base/head/status/branch/log/diff-stat/numstat/name-status and binary feature/worktree patches. `sources/` includes changed product/test/harness files and direct correctness dependencies at base/head, preserving repository-relative paths.

Do not copy an entire `.git` directory, unrelated session history, or all repository source.

## Safety and final response

Never include `.env`, credentials, tokens, cookies, browser profiles, private keys, authentication state, secret command arguments, `node_modules`, virtual environments, build outputs, caches, downloaded data/models, or unrelated logs. Redact sensitive session material while preserving timestamps, lifecycle events, command families, result codes, token counters, interruptions, and idle gaps.

Before zipping, validate the trace, verify all cited commits/findings, run only read-only Git/file checks, and generate SHA-256. Do not fix audit-discovered product defects or start a new section.

Final response must report only:

```text
Audit status:
Invocation source:
Invocation assessment:
Feature base:
Final product/test head:
Current HEAD:
Functional result:
Merge readiness:
Scope result:
Review efficiency:
Validation efficiency:
Skill result:

Mechanical facts:
- commits:
- product/test/harness/process LOC:
- plan/code review calls:
- admitted defects / repair waves / hard caps:
- broad validations / duplicate unchanged validations:
- git diff --check runs:
- active agent time / unattributed gaps:

Known evidence gaps:
Known conflicts:
Audit pack:
SHA-256:
```

Then stop.
