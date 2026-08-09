# CHANGE LOG

记录 `sectioned-feature-development` 各历史版本在流程上的变化。时间采用“该版本最终纳入的最后一条用户指令时间”。

## v1 — 20260806-223457

建立首个大功能分段开发 Skill：以行为 section 拆分大修改，引入 PLAN-FULL/PLAN、section contract/handoff、SECTION/DELTA/INTEGRATION review 语义和 branch/commit 执行模式。

## v1.1 — 20260807-093926

把 Custom Instructions 收缩为触发路由；由上层指令显式授予 scoped branch/commit 例外；Custom Instructions 与 Skill description 保留一致触发条件。

## v2 — 20260807-095143

恢复“小 section 连续两次独立 clean”作为接受条件；去掉 soft cap；第 5 次 full SECTION review 仍不收敛时自动备份并由 sol_max 重拆当前 section，支持层级 section ID。

## v2.1 — 20260808-162346

针对 review scope 膨胀增加 finding admission、scope/assurance envelope 与 anti-overdesign 约束；hard-cap recovery 改为先诊断 split/simplify/rebound/evidence，而非机械继续强化 reviewer 创建的安全/治理模型。

## v3 — 20260809-133655

基于四个真实项目的过长 review 数据大幅简化收敛：每个稳定 section 只做一次 INITIAL_BOUNDED，repair 只做 REPAIR_DELTA，最后一次 FINAL_BOUNDED；hard cap 按 admitted repair wave，而不是 reviewer 次数；禁止 clean-lineage/evidence-only 重建。

## v3.1 — 20260809-161721

收紧 MERGE_BLOCKING_DEPENDENCY 因果、EVIDENCE_GAP authority anchor 和 edit-vs-inspect manifest；section repair budget 跨 initial/delta/final/recovery 累计；每个 original lineage 只允许一次自动 hard-cap recovery；integration 复用同一 admission boundary。
