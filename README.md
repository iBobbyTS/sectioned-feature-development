# Sectioned Feature Development v3.9

## 设计理念

- 大功能按可独立实现、验证和 review 的行为 section 推进。
- PLAN/review 只能执行已有 authority，不得自行创造产品保证。
- review 关注当前 diff 和直接因果范围，repair 只验证 delta；质量优先，但避免重复 full rediscovery。
- 角色、Git、evidence 和 Audit 规则以本快照内 Skill 为准。

## 简要执行流程

`PLAN-FULL → Sol PLAN review → (high complexity: ZCode challenge) → section implement → Sol/ZCode alternating full reviews with same-reviewer delta closure → conditional integration → audit/advisor if triggered`

## 安装

该版本保留两个历史 Skill 变体：

- `skill/sectioned-feature-development-current-mcp/`：适配当时已有 review-only ZCode MCP。
- `skill/sectioned-feature-development-enhanced-zcode-mcp/`：面向建议中的通用 ZCode subagent MCP。

选择需要的目录复制到 Codex Skill 目录，并按实际环境决定安装哪一版。目录名用于历史区分；Skill 内部文件保持当时交付内容。

## 历史资料

`docs/version-history/` 包含从 v1 到 v3.9 的全部历史。每个历史版本包含原始 Prompt、Audit Pack 分析、外部研究、更新说明和按用户策略保留的 appendix。

`docs/CHANGE_LOG.md` 是截至本快照的累计流程变更记录。
