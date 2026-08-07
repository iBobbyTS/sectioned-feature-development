# Research

## 研究范围

以下资料是该版本原研究/分析中明确出现并用于流程设计的外部依据。可信度评价针对“能否支持流程原则”，不是对具体项目代码的直接证明。

| Source | 提取事实 | 可信度 |
|---|---|---|
| [Google Engineering Practices — Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) | 小而自洽的 change 更易深入 review、回滚和减少方向错误浪费。 | 高（稳定工程规范） |
| [Google Engineering Practices — Code Review Standard](https://google.github.io/eng-practices/review/reviewer/standard.html) | review 目标是持续改善 code health，不是无限追求完美。 | 高 |
| [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | 长任务应持久化状态、一次推进有限 feature，并留下 Git/progress handoff。 | 高（厂商工程文章） |
| [OpenAI — Harness engineering](https://openai.com/index/harness-engineering/) | 大目标拆成 design/code/review/test building blocks，plans 作为一等 artifact。 | 高（厂商工程文章） |
| [OpenAI — Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) | 长期任务使用 plan、milestones、acceptance criteria 和 validation commands。 | 高 |
| [GitHub Spec Kit](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) | Specify → Plan → Tasks → Implement，任务应可单独实现、测试和 review。 | 高/中（厂商博客） |
| [Superpowers workflow](https://blog.fsck.com/2025/10/09/superpowers/) | 社区采用 brainstorm→plan→task subagent→review 的 staged workflow。 | 中（社区经验） |

## 使用方式

外部资料只用于形成通用流程原则；具体 blocker、scope 和 merge readiness 仍以用户要求、repository rule、Git/source 和实际验证为准。
