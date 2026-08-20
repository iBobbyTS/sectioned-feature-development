# Research

## 研究范围

以下资料是该版本原研究/分析中明确出现并用于流程设计的外部依据。可信度评价针对“能否支持流程原则”，不是对具体项目代码的直接证明。

| Source | 提取事实 | 可信度 |
|---|---|---|
| [OpenAI — Using PLANS.md for multi-hour problem solving](https://developers.openai.com/cookbook/articles/codex_exec_plans) | 长期实现前审查 plan 可以降低错误方向的后续成本。 | 高 |
| [OpenAI — Build Code Review with Codex SDK](https://developers.openai.com/cookbook/examples/codex/build_code_review_with_codex_sdk) | 只报告当前 PR 引入的 actionable issue。 | 高 |
| [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Agent 行为取决于 model+harness；持久化状态和角色边界重要。 | 高 |
| [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | 评估 Agent 时应区分 outcome、trace 和 harness，不应把偏差只归因模型。 | 高 |
| [Google — Navigating a CL in review](https://google.github.io/eng-practices/review/reviewer/navigate.html) | 应先判断整体设计方向，避免在错误设计上继续堆实现。 | 高 |
| [Superpowers issue #1120](https://github.com/obra/superpowers/issues/1120) | 小任务无 complexity gate 时多代理流程成本可显著膨胀。 | 中 |
| [Superpowers issue #1538](https://github.com/obra/superpowers/issues/1538) | 未限定 review 范围会导致长时间开放式 crawl。 | 中 |
| [Superpowers issue #1803](https://github.com/obra/superpowers/issues/1803) | 独立 adversarial plan review 能抓到自审遗漏的 silent failure。 | 中 |

## 使用方式

外部资料只用于形成通用流程原则；具体 blocker、scope 和 merge readiness 仍以用户要求、repository rule、Git/source 和实际验证为准。
