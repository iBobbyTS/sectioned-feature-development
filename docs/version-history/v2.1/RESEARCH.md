# Research

## 研究范围

以下资料是该版本原研究/分析中明确出现并用于流程设计的外部依据。可信度评价针对“能否支持流程原则”，不是对具体项目代码的直接证明。

| Source | 提取事实 | 可信度 |
|---|---|---|
| [Google Code Review Standard](https://google.github.io/eng-practices/review/reviewer/standard.html) | 更强的 polish/guarantee 不应自动成为 blocker。 | 高 |
| [Anthropic — Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | planner/generator/evaluator 分离有价值，但 evaluator feedback 也可能推动复杂度增长。 | 高 |
| [OpenAI — Harness engineering](https://openai.com/index/harness-engineering/) | 应通过清晰边界和最小 building block 控制长期 Agent 工作。 | 高 |

## 使用方式

外部资料只用于形成通用流程原则；具体 blocker、scope 和 merge readiness 仍以用户要求、repository rule、Git/source 和实际验证为准。
