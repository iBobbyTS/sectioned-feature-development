# V3.8 项目最简纠偏 Prompt

## 1. Cockpit — uncached input tokens（需要产品介入）

```text
使用 `$sectioned-feature-development` V3.8 重新处理当前任务。废弃当前尚未实施且明显膨胀的 PLAN，但保留其 audit 作为反例。

只规划两个产品 section：S01 修改现有 uncached-input 计算/写入语义并补 focused tests；S02 新增一次性的临时数据修正脚本，并只在临时数据库副本上验证。不得新增 per-row schema marker、长期 mixed-version contract、通用 migration framework、并发 schema-upgrade、产品化 CLI/options 或自动 recovery。只保留仓库现有安全规则明确要求的最小备份/事务措施。

本次为 USER_EXPLICIT，按 V3.8 由独立 implementer/reviewer执行至 exact final-head evidence；不要 push 或 merge。
```

## 2. Rosetta — OpenAI provider subtypes/pricing（无需产品介入）

```text
不要修改产品代码、测试或重跑 review。只在 audit 中保留已发生的 `SEQUENCE_GATE_VIOLATION`、S03 暂停/恢复过程和最终 exact-head evidence；不要为流程事故创建新 section或重新打开已接受 section。
```

## 3. Rosetta — credential rate adjustment（只需修正流程证据）

```text
不要修改产品代码或重跑 review。根据原始 Git/session 证据重新审计角色和分支流程：不能用 `/root/plan_review` 之类 profile alias 证明 agent 独立；无法证明的 main-thread implementation、plan/code reviewer identity 和 branch provenance 标为 `UNKNOWN` 或 `MATERIAL_DEVIATION`，不要伪造 compliance。产品 readiness 与流程合规分别报告。
```

## 4. Rosetta — ordinary provider rotation rate（无需介入）

当前 handoff 已确认共享 multiplier predicate 已收敛到 canonical config owner，单字段 dictionary helper 已删除并改为直接赋值。不要再次修改或重审。
