# Research

## 研究范围

以下资料是该版本原研究/分析中明确出现并用于流程设计的外部依据。可信度评价针对“能否支持流程原则”，不是对具体项目代码的直接证明。

| Source | 提取事实 | 可信度 |
|---|---|---|
| [OpenAI Exec Plans](https://developers.openai.com/cookbook/articles/codex_exec_plans) | 复杂任务可先形成 living execution plan，在长实现前接受审阅。 | 高 |
| [Microsoft Copilot Plan Agent](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-plan-agent?view=visualstudio) | 只读探索生成计划并交由后续 implementation。 | 高（厂商文档） |
| [Anthropic long-running harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | planner/initializer 与 coding agent 分离并持久化状态。 | 高 |
| [Superpowers plan document reviewer](https://github.com/obra/superpowers/blob/main/skills/writing-plans/plan-document-reviewer-prompt.md) | 社区存在独立 plan document reviewer 模式。 | 中 |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | bounded review 与 whole-repo audit 的边界可类推到 PLAN review。 | 中 |

## 使用方式

外部资料只用于形成通用流程原则；具体 blocker、scope 和 merge readiness 仍以用户要求、repository rule、Git/source 和实际验证为准。
