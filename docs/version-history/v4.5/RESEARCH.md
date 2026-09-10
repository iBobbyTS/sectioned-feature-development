# v4.5 规划知识研究

研究日期：2026-09-09（America/Edmonton）。研究对象是规划与交接知识，而不是重新选择模型、MCP transport 或调度架构。

## 1. 研究方法与可信度

先读所附 adaptive-debugging 的 core routing、evidence 和相关领域 playbook，再对本项目实际 PLAN/任务/交接/审查路径定位插入点。外部查询包括：小而自洽的变更、可执行计划、progressive disclosure、API consumer contract tests、SvelteKit action/state/load、Swift/macOS state/cancellation/distribution、Python async/Django transactions/migrations/packaging、Rust cancellation/process/features、Spring transactions、PostgreSQL isolation。

采用官方文档、官方源码和厂商工程报告。官方文档用于确认特定机制；厂商经验用于提出方法，不作为本 Skill 的成本/正确率实验证明。组合规则、命中负例、最小边界例子是本版的工程综合设计，待真实任务验证。

Agent 资料遵守最近一年限制：2025-09-09 之后的有日期报告，以及本次访问的当前官方文档。滚动文档不能证明最初发布日，故标为 current snapshot；传统工程资料不受一年限制。没有使用上代模型 benchmark 推导本次路由效果。

完整来源清单及逐模块映射：[规划库来源目录](../../../skill/sectioned-feature-development/references/planning/sources.md)。该目录是可选维护资料，不要求每个 Agent 阅读。

## 2. 传统开发中的规划事实及采用范围

### 自洽的小变更，而不是按文件层拆分

[Google Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) 支持可单独理解的行为与相关测试；[CL description](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) 强调保存 what/why。本版采用业务父 section 与真实 consumer 闭环，不增加固定行数门禁，也不把“能独立编译”当作“独立业务验收”。

[Fowler preparatory refactoring](https://martinfowler.com/articles/preparatory-refactoring-example.html) 提供了先做有限使能修改再完成功能的例子。本版仍使用已有 foundation-choice：不自动重构，不把库中提及的架构变为要求。

### 契约要经过实际消费者

[Pact consumer guidance](https://docs.pact.io/consumer) 明确区分测试真实应用 API client 与测试中另写 HTTP 调用。[OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) 提供请求/响应/media type/example 表达方式。本版只借用具体输入输出的表达与验证思想，不要求安装 Pact、生成 schema 或 broker。

推论：两个分别使用不一致 fixture 的测试都通过，不证明跨层业务可用；实际 serializer/decoder 和命名 reader 必须在共享例子中出现。此推论同时有上一 LMDO 过程证据支持。

## 3. Agentic planning 与知识组织

[OpenAI Skills](https://developers.openai.com/codex/skills/) 当前文档采用任务指令、可选资源和渐进加载；[Execution Plans](https://developers.openai.com/cookbook/articles/codex_exec_plans) 强调自包含、可持续更新、可观察结果；[Codex best practices](https://developers.openai.com/codex/learn/best-practices) 强調复杂任务需要明确上下文与计划。采用可读计划和按需模块，拒绝恢复 STATE/receipt/approval hash 调度器，也不复制面向新手的逐行实现说明。

[Anthropic Effective harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)（2025-11-26）展示持久进度、增量 feature 和实际验证；[Skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) 强调渐进披露与匹配任务的自由度。采用同一计划与少量相关知识；不扩展 feature 列表、不为每个技术模块派发 reviewer。

[Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)（2026-03-24）及[Agent evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)（2026-01-09）用于提醒责任与评估边界：本地断言只能检查文件/配置连接，不证明模型实际少出错或更省 token。本版不因这些文章增加新的 evaluation stage。

## 4. 技术类型重点（事实与推导分开）

| 模块 | 来源支持的机制 | 规划时的综合应用 | 不默认要求 |
|---|---|---|---|
| Swift/macOS | Swift actor/task/cooperative cancellation；SwiftUI model state；distribution 签名 | state/source owner、窗口任务生命周期、取消/过期完成、实际 helper/发布路径 | MVVM/Observation/actor 全面迁移、新 entitlement |
| Python | asyncio cancellation；Django atomic/on_commit/historical models；pyproject entry points | 真实 framework/version、事务与内存/外部副作用、CLI 安装入口和临时数据 | Django 或 asyncio 作为每个 Python 项目的前提 |
| Rust | Tokio select cancellation safety、Child drop 默认不杀进程；Cargo features | owner/drop/resource responsibility、实际 feature target、取消后副作用 | 默认新 actor/supervisor/runtime |
| Svelte | form action 与 JSON endpoint 的响应区别；server state/navigation reuse/load invalidation | 真正的请求/解码路径、派生排序、pending/rollback、二项交互例子 | 改用新 API、重做状态框架或全站 UI |
| Full stack | 可表达的 wire example、真实 client contract testing | 一次端到端 trace 与直接读者归属 | 固定后端语言、拆成 layer-only sections |
| Java/JVM | Spring 代理事务 self-invocation 与 rollback 配置 | 实際 controller/DTO/service/error path；仅出现 Spring 时应用 | 用户举例被当成 LMDO 架构事实 |
| Data | PostgreSQL statement snapshot、Django migration state | 当前引擎事务/迁移语义的边界例子 | 所有 DB 采用 PostgreSQL 语义、自动 journal/outbox |

引用详见来源目录 N/P/R/S/J/D。Django 5.2 是本次明确可查的 reference，不是要求项目升级到它。Tokio/Python/Svelte/Spring 当前文档是快照，不把默认行为覆盖掉仓库的实际版本与显式配置。

Apple 部分页面在网页工具中为 JavaScript 壳；只采用可见官方搜索摘要所支持的 model-state/deployment 概念。Swift concurrency 改读官方 swift-book 原始文档，不声称读到了不可用网页的全部内容。

## 5. 组合、回退与权限边界

默认 core：router + universal。然后独立选择 application/stack/concern，多命中按同一 producer/consumer seam 去重。Java 示例只在真正的 JVM source/build 证据下命中；SvelteKit-only 应命中 full-stack+svelte，不凭空加 Java。

未支持技术使用 universal 的 input→owner→output→consumer 方法，并复用适用 concern。只有影响当前设计且无法从源码确定的未知点才进行版本定向搜索/最小 probe。缺一篇领域文件不是 blocker，也不是在产品仓库里安装新 playbook 的理由。

每项采纳都要映射现有 authority、具体失败、owner 与可判错 AC。没有 authority 的“最佳实践”仍可拒绝。模块数不决定 model tier、ONE/TWO、section 数或并行度。

## 6. 明确没有证明的内容

- 未做相同 feature 的 4.4.1/4.5 付费模型对照；不能报告节省百分比。
- 未运行真实 Swift/macOS、Rust/Java server 或 LMDO/现有 ZAS 应用测试。
- 离线路由样本的 expected labels 是人工设计验收，不是 Agent 已经正确路由的结果。
- 新模块数少于 adaptive-debugging 的全部领域是刻意范围选择；不是提供完整技术百科。

下一批过程包应比较遗漏路径、共享 fixture 一致性、已写未实现、读取/搜索成本、late-plan-delta、repair 与 escaped defects，而非只统计命中率。正确不加载模块也算正确行为。
