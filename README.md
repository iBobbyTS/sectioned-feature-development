# Sectioned Feature Development v3

## 设计理念

- 大功能按可独立实现、验证和 review 的行为 section 推进。
- PLAN/review 只能执行已有 authority，不得自行创造产品保证。
- review 关注当前 diff 和直接因果范围，repair 只验证 delta；质量优先，但避免重复 full rediscovery。
- 角色、Git、evidence 和 Audit 规则以本快照内 Skill 为准。

## 简要执行流程

`PLAN → IMPLEMENT → INITIAL_BOUNDED → REPAIR_DELTA* → FINAL_BOUNDED → integration`

## 安装

将 `skill/sectioned-feature-development/` 整体复制到 Codex Skill 目录（例如 `~/.codex/skills/sectioned-feature-development/`），完整替换同名旧目录，不要把不同版本的 references/assets 混合。

## 历史资料

`docs/version-history/` 包含从 v1 到 v3 的全部历史。每个历史版本包含原始 Prompt、Audit Pack 分析、外部研究、更新说明和按用户策略保留的 appendix。

`docs/CHANGE_LOG.md` 是截至本快照的累计流程变更记录。
