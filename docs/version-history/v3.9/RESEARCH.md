# Research

## 研究范围

以下资料是该版本原研究/分析中明确出现并用于流程设计的外部依据。可信度评价针对“能否支持流程原则”，不是对具体项目代码的直接证明。

| Source | 提取事实 | 可信度 |
|---|---|---|
| [OpenAI Codex documentation](https://developers.openai.com/codex/) | Codex 适合工具驱动的代码实现和验证，外部 agent 应暴露高层 lifecycle 而非内部工具。 | 高 |
| [OpenAI Codex MCP](https://developers.openai.com/codex/mcp/) | Codex 支持 MCP 集成，适合高层 tool/control surface。 | 高 |
| [OpenAI execution plans](https://developers.openai.com/cookbook/articles/codex_exec_plans) | 复杂长任务使用显式 plan artifact。 | 高 |
| [MCP Specification](https://modelcontextprotocol.io/specification/) | MCP 定义 tools/lifecycle 等协议边界；长任务应保留明确能力协商和生命周期。 | 高（标准） |
| [MCP lifecycle](https://modelcontextprotocol.io/specification/latest/basic/lifecycle) | 客户端/服务端 lifecycle 与 capability negotiation 应显式建模。 | 高 |
| [MCP tools](https://modelcontextprotocol.io/specification/latest/server/tools) | 工具应提供明确 schema/structured result，而不是透传内部执行细节。 | 高 |
| [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 长任务需要明确角色、可恢复状态和 durable handoff。 | 高 |
| [Anthropic — Building a multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | 多 agent 体系需要清晰 orchestration、独立任务和结果聚合。 | 高 |
| [Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) | 大功能仍应保持可独立理解和 review 的小变更。 | 高 |
| [Superpowers issue #1120](https://github.com/obra/superpowers/issues/1120) | complexity gate 对防止小任务过度编排很重要。 | 中 |

## 使用方式

外部资料只用于形成通用流程原则；具体 blocker、scope 和 merge readiness 仍以用户要求、repository rule、Git/source 和实际验证为准。
