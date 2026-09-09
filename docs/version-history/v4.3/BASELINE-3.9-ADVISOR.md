# External Advisor Escalation

## Contents

- [Purpose](#purpose)
- [Trigger rules](#trigger-rules)
- [Non-triggers](#non-triggers)
- [Freeze and package](#freeze-and-package)
- [Human handoff prompt](#human-handoff-prompt)
- [Result intake](#result-intake)

## Purpose

The Advisor is a low-frequency, read-only decision authority for system-level ambiguity after local repository exploration, Sol/ZCode review, and deterministic evidence have already reduced the problem to a precise decision. It is independent of Audit mode.

## Trigger rules

Trigger exactly one `ADVISOR_REQUIRED` state when any rule is proven:

1. `ADV-01 SECOND_CONVERGENCE_FAILURE`: an original section lineage already consumed its one automatic hard-cap recovery, and the replacement reaches another hard cap or would require a sixth independent material repair wave.
2. `ADV-02 HIGH_IMPACT_REVIEWER_CONFLICT`: Sol and ZCode independently recommend mutually exclusive architecture, trust/persistence/public-compatibility boundary, scope authority, or merge verdict, and one bounded probe/test cannot resolve it.
3. `ADV-03 LARGE_VALIDATED_WORK_DISCARD`: the next proposed action is restart-from-base or major-owner rebound that would discard roughly 20% or more of validated feature implementation, and the cause is not an ordinary local bug.
4. `ADV-04 UNRESOLVED_TRUST_OR_CONSISTENCY_MODEL`: two materially different security, credential, durability, or concurrency models remain plausible; both over- and under-design have serious consequences; repository/user authority does not choose one.
5. `ADV-05 RELEASE_EVIDENCE_CONTRADICTION`: source/Git, deterministic checks, and independent reviewers disagree about the final HEAD in a way that changes release readiness, and one same-environment deterministic rerun cannot reconcile it.
6. `ADV-06 EXTERNAL_SYSTEM_SHAPE_UNRESOLVED`: after one bounded real probe, the external protocol/agent/harness shape is still unknown and continuing would lock in a costly or irreversible architecture.

## Non-triggers

Do not trigger for a normal bug, first finding, first hard cap, one reviewer/MCP failure, missing credential/environment, simple merge conflict, pre-existing baseline failure, business semantics directly answerable by the user, low-cost local refactor, or one model's preference. Ask the user directly for owner decisions.

## Freeze and package

On trigger:
1. Stop writers/reviewers and do not continue the normal answer.
2. Freeze HEAD/status/PLAN/contracts/review ledgers/ZCode logs and write `ADVISOR-REQUEST.md`.
3. Run `scripts/advisor_pack.py`. It packages the repository working tree, `.git`, `.agent-work`, tracked and relevant untracked product files; excludes build/cache. It first blocks on secret-like paths or detected private-key/token patterns.
4. Canonical output: `~/Desktop/advisor-pack/{repo}-{feature}-{trigger}.zip`.
5. Reply only with package path/hash and the human handoff prompt.

## Human handoff prompt

```text
请作为外部 Pro Advisor 只读审查附件中的完整仓库、Git 历史、PLAN、review 和测试证据。当前触发：<TRIGGER_ID>。
需要你裁决的唯一问题：<EXACT_DECISION>.
请输出：DECISION、关键证据、推荐的最小安全边界、被否决方案及原因、下一步执行顺序、停止/再次升级条件、仍存在的不确定性。不要直接修改代码，不要扩大产品需求；业务语义仍由 human owner 决定。
```

## Result intake

Save the Advisor response verbatim as `.agent-work/advisor/{request-id}/ADVISOR-RESULT.md`; record model/provenance when known, human acceptance/rejection, and the resulting bounded action. Advisor advice is not self-authorizing. When Audit is on, include trigger evidence, package hash, result, and adoption decision in the Audit Pack.
