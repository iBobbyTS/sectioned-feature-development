# v4.5.1 外部研究与证据边界

研究日期：2026-09-09（America/Edmonton）。用户要求按常用语言和工程领域整理，故本次研究用于覆盖与具体机制，不重新研究模型选型或改动开发状态机。

## 覆盖依据

[Stack Overflow 2025 Technology](https://survey.stackoverflow.co/2025/technology) 分开列出 programming/scripting/markup languages、web technologies 等；[Developer roles](https://survey.stackoverflow.co/2025/developers) 显示不同工程工作类型。[GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) 提供实际仓库贡献者语言活动。

这些是不同口径：自报使用/职位，不等于独立市场普查；GitHub 贡献活动，不等于商业任务频率。没有把网页 write-in 子表当作全部语言排名，也没有宣称所选20份是严格全球Top20。覆盖兼顾常见Web/JVM/.NET、原生/系统、数据/ML、自动化和移动/嵌入式扩展；R/Lua等是重要领域的代表，不一定在所有总体榜单靠前。

Domain 是工程交付形态/任务领域，不是业务行业，也不是模型能力级别。14个domain用于跨语言规划；framework/runtime/platform由单独19个adapter承载。framework family内仍区分真实版本/API，例如Vue并不证明Nuxt、SwiftUI不证明AppKit；索引不是默认全加载清单。

## 主要机制来源与抽取

| 主题 | 主要第一方资料 | 提取的有限事实/知识 | 约束 |
|---|---|---|---|
| 语言 | 各语言官方手册、Dev.java、TypeScript、Rust book、Swift book、Kotlin、PHP、Ruby、Dart、R、Lua、PowerShell | 类型/异常/资源/异步/模块/实际运行入口 | 不从语言推出framework/domain/platform，不要求版本升级 |
| C/C++ | Clang UBSan、C++ Core Guidelines | undefined behavior诊断、资源/生命周期与接口设计 | 诊断不是完整证明；不默认增加全套sanitizer gate |
| Web | MDN、HTML标准、React/Next/Vue/Angular/Svelte官方文档 | 实际请求/解码、UI状态、SSR边界和生命周期 | 浏览器/框架规则只对当前实际路径适用 |
| Python frameworks | Django 5.2 transactions/migrations、FastAPI async | 框架事务/历史model、sync/async边界 | 无Django/FastAPI就不加载相关规则 |
| JVM/.NET | Spring transactions/rollback、ASP.NET Core DI | 实际代理入口、配置化rollback、依赖生命周期 | Java≠Spring；C#≠ASP.NET；mock不证明事务入口 |
| 原生/移动 | Swift concurrency、Apple model data/scenes/distribution、Android/Flutter官方文档 | 状态owner、任务/窗口/scene生存期、实际分发边界 | 当前源码与deployment target优先，框架建议不变成全面迁移 |
| Data/ML/science | Airflow best practices、PostgreSQL isolation示例、Google Rules of ML、PyTorch randomness源文件 | partition/replay、实际引擎语义、training-serving和可重复性限制 | SQL≠PostgreSQL；seed不代表跨环境bitwise一致；不建新平台 |
| Cloud/system/embedded/game | Kubernetes pod lifecycle、Node streams、Tokio select/process、Zephyr interrupts、Godot processing | shutdown/backpressure/cancellation、ISR限制、不同tick时钟 | 不从domain推出Kubernetes/RTOS/engine；检查实际实现 |
| Skill组织 | 当前OpenAI Build skills、Anthropic Skill best practices | 渐进加载、指令+按需reference | 不为路由创建机械状态机或更多review |

完整URL、来源类型和guide映射在 [sources.md](../../../skill/sectioned-feature-development/references/planning/sources.md) 和 appendix/SOURCES.json、KNOWLEDGE_INVENTORY.json。语言/领域指南的问题、组合规则和禁止扩张反例是工程综合设计，不是这些机构直接发布的统一分类法。

## 访问与时效限制

Agent资料沿用最近一年有日期报告或当前官方滚动文档；不为rolling docs编造首发日。传统语言/工程资料不限一年。资料中的latest/current是查询快照，仓库实际版本/设置优先，不能据文档更新依赖。

Apple部分页面为JavaScript壳，只采用可见官方索引内容支持的概念；Swift concurrency使用官方swift-book原始Markdown。Bash直接页面超时，使用官方索引片段，不声称完整抓取；PyTorch原.rst路径失败，改读官方main/docs/source/notes/randomness.md。C委员会PDF只发现链接，没有使用其正文。所有URL并非都重新批量抓取：v4.5已有出处保留，新增采用本轮实际查询的第一方资料。

## 为何不增加执行负担

知识库可以更大，单次上下文不应按总文件数增长。主线程先按真实功能选择最小domain/语言/adapter/concern；整套index、sources和examples不是默认worker输入。多个guide重复提出的rollback或consumer问题只在同一合同处理一次。

没有新增强制产物字段、每轴至少一个匹配、自动任务分類脚本或平台特定的强制测试栈。通用fallback在任何维度独立可用。正确不加载、承认未知与选择已有源码比“覆盖所有标签”更重要。

## 未证明的内容

未运行付费模型、实际Codex/ZAS、用户产品或跨语言应用；未测量省token/少review/降低返工比例。维护者组合fixture是人工预期，不是模型已通过的路由benchmark。下一批真实Audit才用于评估误推断、过度加载、missed boundary、late plan delta、修复和总成本。
