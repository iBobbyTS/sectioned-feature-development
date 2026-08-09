# Audit Pack Analysis

本版本依据 [保密内容]、Codex Cockpit、Codex Rosetta、[保密内容] 四个中等规模真实开发日志重新设计。四个项目均出现远高于普通开发的流程放大。

## 跨项目信号
- repair 后反复 fresh full review，重复扫描稳定范围。
- reviewer-created security/durability/compatibility/governance 被纳入产品合同。
- 为获得连续 clean，旧证据、lineage、process artifact 被反复重建。
- hard cap 按 review 次数而非独立 root-cause repair 计数，导致局部小 finding 触发结构 recovery。
- full suite/build/diff-check 在局部 repair 后频繁重复。

## 结论
主要问题不是 section 仍太大，而是父 orchestration 强制 repeated full rediscovery。V3 改为 `INITIAL_BOUNDED → REPAIR_DELTA* → FINAL_BOUNDED`，并让 hard cap 统计 admitted repair wave。
