# ZAS suspicion-only observation

## Invocation boundary

Use `zcode_subagent_observe` only when the caller suspects meaningless looping, not on every poll, at an elapsed-time checkpoint, after every review, or merely because reasoning/tool counts are high. Normal lifecycle monitoring remains `poll`; a long review, a known long command or pending permission alone does not justify observation.

State the concrete suspicion and current subgoal, then call with only `{"agent_id":"<actual-id>"}`. Read the five judgment meanings from the MCP tool description. They are instructions to the calling model, not a ZAS detector, server result or automatic action policy. No monitor model is added.

## Evidence supplied

The installed `zas-observation/1.1` interface returns at most three tool-name groups ranked by that Agent's lifetime call count, at most five recent calls per group, and the newest 200 Unicode characters of concatenated, verified runtime-public reasoning deltas. Calls include arguments, not outputs/results. One delta can contain many characters; the limit is not a delta/event count.

Public reasoning extraction is enabled by default. Its exact event selector and text key were verified against the installed local ZCode runtime as part of the ZAS implementation; only this allowlisted field is read. `encrypted_content` is excluded before collection/storage/export, recursively, and never decoded. No extra prompt, spawn flag or per-call collection authorization is required.

`zas_evidence.py snapshot` validates identity, bounds, ordering, source metadata and excluded fields only. It never determines progress, ranks hypotheses, scores repeated text or calls cancel.

## Caller decision and action

Compare the small returned snapshot with the actual task. A repeated read or `true`/`echo` may be legitimate; a 200-character reasoning tail cannot prove a loop by itself. Because outputs and file-version results are deliberately absent, do not infer tool success, no state change, or absence of all progress. A retention gap is missing evidence, not inactivity.

Save the suspicion, snapshot identifier and brief caller assessment only when it informs a decision. Healthy progress resumes ordinary polling. A concrete missing input uses an actual supported permission/queued-message path. When the caller decides a loop is established, cancel explicitly, wait for `TERMINAL + resources_reaped=true`, collect available result/gaps, close, and verify workspace/fingerprint before retry. `send` is queued, not an interrupt.

Do not repeatedly request the same unchanged snapshot. A changed snapshot alone is not a reason for routine observation; a continuing/new suspicion is needed. If evidence remains insufficient, record uncertainty rather than guessing. A pre-authorized budget stop must be labelled `BUDGET_STOP_UNPROVEN_LOOP`, not a proven loop.

No automatic cancel/spawn cycle. The inherited one-bounded-retry and review-slot rules remain; infrastructure/loop attempts are not product repair waves or automatic external-Advisor triggers.

## Audit boundary

When process audit is enabled, selected snapshots, caller assessments and cleanup receipts go to the paired `xxx-zas.zip` described in [ZAS audit](zas-audit.md). No full reasoning transcript, tool-result dump or separate checksum file is generated. Audit OFF does not disable normal control/cleanup or suspicion-only observation.
