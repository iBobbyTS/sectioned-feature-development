# Research

## 研究范围

以下资料是该版本原研究/分析中明确出现并用于流程设计的外部依据。可信度评价针对“能否支持流程原则”，不是对具体项目代码的直接证明。

| Source | 提取事实 | 可信度 |
|---|---|---|
| [OpenAI — Build Code Review with Codex SDK](https://developers.openai.com/cookbook/examples/codex/build_code_review_with_codex_sdk) | code review 应聚焦当前 diff 引入的 actionable issue，避免 nit。 | 高 |
| [Ponytail](https://github.com/DietrichGebert/ponytail) | 社区实践把 current-diff review 与 whole-repository audit 明确区分。 | 中 |
| [Superpowers issue #1120](https://github.com/obra/superpowers/issues/1120) | 缺少 complexity gate 时，小任务也会触发多 agent 流程并放大成本。 | 中（社区 issue） |
| [Superpowers issue #1538](https://github.com/obra/superpowers/issues/1538) | reviewer 无明确 BASE/HEAD 时可能进行 open-ended repo crawl。 | 中 |
| [Superpowers issue #1481](https://github.com/obra/superpowers/issues/1481) | 重复 review workflow 会对同一 diff 再次 review。 | 中 |

## 使用方式

外部资料只用于形成通用流程原则；具体 blocker、scope 和 merge readiness 仍以用户要求、repository rule、Git/source 和实际验证为准。
