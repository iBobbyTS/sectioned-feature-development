# ZAS beta audit within the process audit

## Contents
- [Separation](#separation)
- [One attempt record](#one-attempt-record)
- [Progress and lifecycle evidence](#progress-and-lifecycle-evidence)
- [Interpretation](#interpretation)

## Separation

ZAS is an external beta runtime under controlled real-project testing. Runtime monitoring is necessary even with audit OFF; that does not silently re-enable audit. When audit is LIVE, record only facts from the actual task. Do not spawn extra probes or run test tasks to improve this record.

`~/Desktop/audit-pack/` receives ONLY the sectioned process pack. Include ZAS-AUDIT.md and ZAS-RUNS.jsonl inside it. Standalone ZAS diagnose/compatibility/live-test packs go to a different purpose directory, such as `~/Desktop/zas-diagnostics/`; the process pack references selected evidence/hash and does not count them as extra features.

## One attempt record

Use `assets/ZAS-ATTEMPT.template.json`. Fields may be null/UNKNOWN with a reason; never invent IDs or observed versions. Capture once per physical attempt:

- feature/run, parent/child/original lineage, logical review slot and physical attempt;
- native/ZCode scheduled provider, task and plan hashes, exact base/candidate/worktree fingerprint;
- actual MCP returned agent_id, server service_generation/API schema, deployed ZAS build/version and runtime/CLI/model version if exposed;
- capability profile: BASELINE_LIMITED or ENHANCED_OBSERVATION; actual source of that claim;
- spawn request/response, non-idempotent unknown outcome reconciliation, WORKSPACE_BUSY ownership handling;
- planned versus actual reviewer model, observed UNKNOWN when only server default is known;
- poll/observe cursors, output bytes/calls, distinct snapshots, duplicates avoided, reconnect/gaps;
- permission request/response effective policy, queued send disposition and eventual delivery evidence;
- lifecycle outcome and semantic review result separately, full result pages/hash (caller vs server provenance);
- cancellation request, terminal time, resources_reaped time, close confirmation, release/workspace check;
- protocol/runtime/auth/semantic-task failure classification, first failure vs cleanup outcome;
- raw result/check/handoff/admission references and any partial/invalidated evidence.

No model prompt secrets, raw unrelated runtime transcripts, private reasoning or global log dumps. Bounded already-public excerpts used for semantic judgement are allowed only under the authorized content policy. Hash/reference each selected window once, including dropped/redacted/truncated counts.

## Progress and lifecycle evidence

For a supervision decision, preserve:

- trigger: scheduled checkpoint or repeated no-new-information cycles, not raw string similarity;
- current task subgoal and expected next artifact/evidence;
- considered event IDs, same/different read ranges or observed content version, tool effect/result summaries and optional authorized public reasoning;
- classification PROGRESSING / EXPECTED_WAIT / NEEDS_CLARIFICATION / NO_PROGRESS_LOOP / INSUFFICIENT_OBSERVABILITY;
- alternatives ruled out, brief evidence-backed explanation and uncertainty;
- action: continue, clarify, cancel, budget stop, or blocked;
- eventual outcome and human correction/false-positive label when available.

Do not report an empty/truncated observation window as proof of no progress. Do not treat no file modifications as a stalled review. Transport retries and session replacements count as physical calls/cost, not new independent clean evidence or product repairs.

## Interpretation

Separate cost and defects among:

1. tested application defect (admitted under existing review causality);
2. task packet/PLAN misconfiguration;
3. model no-progress/semantic reasoning problem;
4. ZAS adapter/lifecycle/control error;
5. upstream ZCode runtime/protocol/model rejection;
6. host environment/credentials;
7. telemetry gap.

If evidence does not select one, report UNRESOLVED rather than blame GLM or restart daemon blindly. Summarize cleanup leaks, cancel latency, progress-monitor false positives, observation volume, retry outcomes, same-session gaps, and final usable independent-review rate. These measurements inform later ZAS work; audit does not automatically create a new section or change the tested application.

External Advisor events are a different record: raw human-returned decision and human adoption, not a ZAS review or native subagent call.

Use `assets/ZAS-ATTEMPT.template.json` for one physical attempt. The new trace family is `zas`; append only material lifecycle/supervision events, not every poll. `zas_evidence.py` validates capability/window metadata but intentionally returns semantic_progress=NOT_INFERRED. Parent judgment and later human labels remain separately recorded.
