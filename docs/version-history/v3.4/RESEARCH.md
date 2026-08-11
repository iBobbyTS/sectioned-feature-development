# Research

## 研究范围

以下资料是该版本原研究/分析中明确出现并用于流程设计的外部依据。可信度评价针对“能否支持流程原则”，不是对具体项目代码的直接证明。

| Source | 提取事实 | 可信度 |
|---|---|---|
| [Google Code Review Standard](https://google.github.io/eng-practices/review/reviewer/standard.html) | review 深度应与风险匹配，非关键 polish 不应阻塞。 | 高 |
| [OpenAI Codex Code Review Cookbook](https://developers.openai.com/cookbook/examples/codex/build_code_review_with_codex_sdk) | 优先严重、可行动的 current-diff issue。 | 高 |
| [Microsoft Copilot Plan Agent](https://learn.microsoft.com/en-us/visualstudio/ide/copilot-plan-agent?view=visualstudio) | 计划和实现可分开，并根据任务复杂度调整工作量。 | 高 |

## 使用方式

外部资料只用于形成通用流程原则；具体 blocker、scope 和 merge readiness 仍以用户要求、repository rule、Git/source 和实际验证为准。
