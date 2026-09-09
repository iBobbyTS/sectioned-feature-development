# External Advisor Escalation — restored 3.9 contract

## Contents
- [Purpose and exact trigger rules](#purpose-and-exact-trigger-rules)
- [Non-triggers](#non-triggers)
- [Freeze and package](#freeze-and-package)
- [Human handoff](#human-handoff)
- [Result intake](#result-intake)
- [Audit](#audit)

## Purpose and exact trigger rules

The Advisor is outside the Codex runtime. The human obtains its decision and returns it. Do not spawn a native advisor, invoke a second reviewer as a substitute, or select the Advisor's provider/model. This mechanism is independent of audit and remains active with audit OFF.

Restore the six v3.9 triggers without widening them:

1. `ADV-01 SECOND_CONVERGENCE_FAILURE`: an original section lineage consumed its one automatic hard-cap recovery; the replacement reaches another hard cap or requires a sixth independent material repair wave.
2. `ADV-02 HIGH_IMPACT_REVIEWER_CONFLICT`: native and ZCode reviewers independently recommend mutually exclusive architecture, trust/persistence/public-compatibility boundary, scope authority or merge verdict, and one bounded probe/test cannot resolve it. The historical contract's “Sol position” field records the actual current GPT reviewer identity explicitly.
3. `ADV-03 LARGE_VALIDATED_WORK_DISCARD`: restart-from-base or major-owner rebound would discard roughly 20% or more of validated feature implementation; the cause is not an ordinary local bug.
4. `ADV-04 UNRESOLVED_TRUST_OR_CONSISTENCY_MODEL`: two materially different security, credential, durability or concurrency models remain plausible; both over- and under-design have serious consequences; repository/user authority does not choose one.
5. `ADV-05 RELEASE_EVIDENCE_CONTRADICTION`: source/Git, deterministic checks and independent reviewers disagree about final-HEAD release readiness, and one same-environment deterministic rerun cannot reconcile it.
6. `ADV-06 EXTERNAL_SYSTEM_SHAPE_UNRESOLVED`: after one bounded real probe, external protocol/agent/harness shape is still unknown and continuing would lock in a costly or irreversible architecture.

## Non-triggers

No escalation for a normal bug, first finding, first hard cap, one ZAS outage/loop/cancellation, missing credential/environment, simple merge conflict, pre-existing baseline failure, a product decision directly answerable by the user, low-cost local refactor, or one model's preference. Beta ZAS diagnostics alone do not create a system-level decision. Ask the owner directly for ordinary business semantics.

## Freeze and package

1. Persist a filled copy of the byte-preserved `assets/ADVISOR-REQUEST.template.md` with trigger facts and a precise question, not a persuasive preselected answer.
2. Main records ADVISOR_REQUIRED and the requested decision in FEATURE-STATE.md. Stop writers/reviewers using actual lifecycle tools; do not merely clear their IDs. Record final partial results. Confirm no actors remain active before packaging.
3. Freeze HEAD, dirty patch, requirements, PLAN-FULL, contracts, ledger and relevant ZAS observations. Audit OFF still requires these execution records.
4. Run the retained `advisor_pack.py` export helper directly: full current worktree (including ignored workflow state), normal `.git` or linked-worktree/common Git metadata, and a portable bundle when available. Tracked source is not silently excluded as “build output”. Preserve symlinks without following them. Do not mutate Git, reset, clean, or upload.
5. Block on detected secret-like files/content; report paths only and ask the human. The scanner is best-effort and cannot certify compressed Git history is free of secrets. The human reviews sharing before forwarding. Never silently strip relevant evidence and call the pack complete.
Before the request snapshot, allow active actors to stop and persist their final partial work; if HEAD changes afterward, packaging blocks and the request must be explicitly refreshed rather than silently using a stale decision packet.

6. Canonical ZIP: `~/Desktop/advisor-pack/{repo}-{feature}-{trigger}.zip`; working request/receipt under `.agent-work/advisor/{request-id}/`. This is NOT a sectioned process-audit ZIP and never goes into `~/Desktop/audit-pack/`.
7. Respond only with the paused state, path/hash, and handoff prompt (or precise packaging blocker). Do not continue normal development while waiting.

```bash
# Save the completed original request template here first:
# .agent-work/advisor/ADV-S01-001/ADVISOR-REQUEST.md
python {skill-dir}/scripts/advisor_pack.py --repo /abs/repo \
  --feature <feature-id> --trigger ADV-04 --request ADV-S01-001
```
Main sets WAITING_EXTERNAL only after real actors stop and the export verifies. No workflow approval script is used.


## Human handoff

```text
请将附件交给外部 Advisor，只读检查完整仓库、Git、已确认需求、PLAN、review 和测试证据。
当前触发：<TRIGGER_ID>；冻结 HEAD：<HEAD>。
需要裁决的唯一问题：<EXACT_DECISION>。
请返回 DECISION、关键证据、最小安全边界、否决方案及理由、保留的有效工作、后续顺序、停止/再次升级条件和不确定性。
不要直接改代码、扩大产品需求或代替 human owner 接受业务/风险/破坏性操作。
```

The skill need only know that an external Advisor exists; no model name is embedded in routing.

## Result intake

Save the result verbatim as `ADVISOR-RESULT.md` in the request directory; main records the actual provenance. Record provenance/model only when actually provided. Receiving advice keeps the feature blocked at `WAITING_HUMAN_DECISION`.

The human explicitly accepts, rejects, or requests clarification. Save the actual human message and its decision/provenance with the request. Main applies only that authorized disposition. A model-authored approval is not human authority; no receipt schema or adopt CLI is required.

Apply only the accepted bounded action; preserve accepted sections, history and original repair counters. Do not restart a clean streak, reset a budget, silently reopen a completed PLAN or infer merge/reset/push authority. A technical recommendation needing a plan revision still follows the existing bounded PLAN delta process.

## Audit

If enabled, capture trigger facts, request hash, frozen code identity, ZIP/manifest hashes, secret/package gaps, raw returned result, human adoption, applied action and resumed outcome. Keep advisor ZIP external; reference its metadata instead of nesting a full repository in the process audit. If disabled, retain the request/result/adoption locally; do not enable audit merely because the Advisor is needed.
