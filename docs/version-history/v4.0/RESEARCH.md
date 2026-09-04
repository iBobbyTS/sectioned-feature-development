# 4.0 外部研究记录

检索日期：2026-09-04。区分附件事实、官方声明、厂商实验、社区实测与本项目推断。未把官方高分当成当前六个 model–effort 配置的真实仓库通过率；未执行任何付费模型对照或用户机器上的 Codex/ZCode。

## 1. GPT-6 Astra：使用它自己的资料

**R01 官方模型与发布材料**
- https://openai.com/index/gpt-6-astra/
- https://developers.openai.com/api/docs/models/gpt-6-astra

事实：模型 ID `gpt-6-astra`；公开输入/输出价 $10/$50 每百万 tokens，支持 low/medium/high/xhigh/max。模型页另外列缓存、长上下文和速度档计费；不能把所有请求都用10/50粗算。发布页包含 agentic coding / migration / long-context 评估，支持把Astra作为复杂任务候选，但其中最大成绩不是本项目medium/high/xhigh的匹配实验。

证据强度：模型ID/支持effort/当日标价高；发布基准在厂商环境内有意义，对本项目分工的外推中等或低。本文不拿Sol结果替代Astra能力。

**R02 Max Stoiber 提醒**
- https://x.com/mxstbr/status/2095598944604541065

搜索片段可见重新写 AGENTS.md 的建议；原帖全文抓取失败，不能确认全部上下文，也不依此核实任职。项目采纳的是“重写为少量政策，不重复流程”的设计，而不是执行 `rm AGENTS.md`。保留用户明确的语言、Git、Docker、CodeGraph、anti-loop和授权约束。出处完整性有限，推荐依据还包括附件本身明显重复的规则。

## 2. Sol/Terra/Luna：不按总分排序

**R03 官方发布与模型文档**
- https://openai.com/index/gpt-5-6/
- https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/
- https://developers.openai.com/api/docs/models/gpt-5.6-sol
- https://developers.openai.com/api/docs/models/gpt-5.6-terra
- https://developers.openai.com/api/docs/models/gpt-5.6-luna

官方任务族成绩并非所有场景同序。例如代码debugging中Terra接近Sol，而某些长上下文项目差距更大；图遍历也有与一般档位不一致的次序。它们提示要区分任务结构、长上下文依赖和推理需求，不能推导“安全代码一定Astra、边界清楚一定Luna”。

本次追查官方benchmark描述、开放代码比较、工程用户样本；没有取得覆盖三模型、目标effort和真实仓库patch的统一逐题完整数据。因此不声称有已验证的 per-task routing classifier。

**R04 Sonar 自有对照实验**
- https://www.sonarsource.com/blog/openai-gpt-5-6-sol-and-terra/

4,444个Java任务，来自HumanEval/MBPP/ComplexCodeEval，模型同用medium，Luna未参与。文中功能通过率Sol81.99%、Terra79.96%；还按并发、资源、密码配置等类别给出静态分析密度。密度不能替代真实错误率，文中部分叙述与表格措辞不完全一致；本项目只使用已明确的方法和类别信号，不据此宣布某模型不适合所有并发/安全代码。没有获得每题可复现patch与人工复核集。

证据强度：一级实验报告，中等；编程语言、harness、effort和静态分析器限制明显。

**R05 单项目 implementation-only 多配置实验（正向反例）**
- https://www.reddit.com/r/codex/comments/1vembjz/testing_56_luna_vs_terra_medium_vs_sol_medium_for/

作者用同一个约3,378词计划、11 stories、Java/TypeScript两仓库任务，每配置三次。报告 Luna xhigh/max各3/3无缺陷，medium 0/3、high1/3；Terra medium/Sol medium也0/3。作者强调较短计划下Luna不稳定。这支持“任务与计划结构会改变相对表现”，但单任务、小样本、缺独立复现，不能证明Luna普遍优于Sol，也不能忽略制作长计划的成本。它没有测试本次terra_high/astra_medium组合。

**R06 实际失效类别（反向样本）**
- https://www.reddit.com/r/LLMDevs/comments/1v1ardg/gpt56_solterraluna_week_is_anyone_else_rethinking/
- https://community.openai.com/t/gpt-5-6-sol-vs-terra-what-are-you-seeing-in-real-development-during-these-first-days/1386726

用户报告Luna遗漏锁/decorator、Terra替换业务异常语义、长session反复分析且声称修好仍错。属于初级现场报告，样本与effort不齐全；价格/二手benchmark评论不作为事实引用。有效教训是为实际行为建立可判错oracle，并统计后续返工，而不是凭“便宜”选模型。

### 4.0 路由结论（本项目推断）

采用用户建议的四实现档与两个Astra计划/review档，另两角色复用已有组合。按 analogue、ambiguity、semantic hops、state coupling、oracle strength、novel reasoning记录理由。Luna需明确例子和可拒错输出；Terra用于现有模式的局部新实现；Sol为非平凡默认；Astra medium负责尚不能安全拆解的困难结构推理。全部是首版可否证假设，不是本次研究证明的任务能力边界。

不采用逐档试错瀑布。下路由一次显露语义能力不足即跳到适合模型，保留正确成果；基础设施故障不升级模型。后续比较**accepted outcome总成本**，含planner、explorer、初次实现、所有失败、review、repair、advisor、validation、integration。高价review无法免费补偿弱实现。

## 3. Cheap explorer

**R07 OpenAI Builder Guide（完整正文阅读）**
- https://openai.com/index/builders-guide-to-gpt-5-6/

文中推荐按实际任务选择模型/effort并利用较小模型的探索环节。PlayerZero的Luna code exploration客户案例报告成本/延迟改善，但没有本任务可复现逐题数据；不把案例百分比写成我们的收益承诺。

**R08 Claude 原生子代理/Explore**
- https://code.claude.com/docs/en/sub-agents
- https://claude.com/blog/subagents-in-claude-code

官方强调独立上下文保留主线程注意力、read-only Explore与便宜模型的角色隔离。4.0复用Luna xhigh做 `sfd_explorer`，而不新加 low/medium 档：一个明确问题、有限直接owner/test映射、来源指针、未知项；不递归发散，不替规划作设计，不认为它已经证明完整影响锥。小改直接读文件更便宜时不派发。

## 4. Anthropic 两篇指定文章

**R09 Optimizing for cost and intelligence — 全文与方法/限制部分已阅读**
- https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence

文章覆盖context/tool/output/caching、effort、升级/降级、Advisor和Orchestrator，以及benchmark方法。关键不是价格等级类比：应计失败与重试后的每个成功任务成本。其Advisor实验收益随能力差与consult频率改变；部分orchestrator实验更便宜但质量也下降，不能作为“质量不降”的证据。内部SWE-bench Pro子集与公开leaderboard不直接可比，effort、样本、缓存计价不同也不能拼表比较。

**R10 Advisor tool**
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool

官方服务端advisor接收executor的完整对话作为引用上下文，并且不具备自己的工具。**这与用户本次要求不同。** 4.0只借鉴稀缺专家在瓶颈介入，不照抄完整transcript传递或例行“前后各咨询”。原生 `advisor` 需要新上下文，并可读交接文件和当前必要源码；主线程也是Astra时不宣称跨模型能力提升。

### 本项目架构选择

- Orchestrator：适用于明确可以独立完成的仓库子任务和噪声很大的只读探索，不能让便宜worker承担仍未定义的共享不变量。
- Advisor：罕见且高影响的技术裁决；已有合同仍不变，调用从人工Pro变为原生advisor实例。
- Reviewer：持续验证本diff，但不承担产品owner或advisor决策职能。
- Human：业务语义、兼容/风险取舍、破坏性Git/发布权限，不被advisor替代。

## 5. Codex 自定义 agents 配置与上下文限制

**R11 官方 agents 文档**
- https://developers.openai.com/codex/subagents （检索时重定向到 https://learn.chatgpt.com/docs/agent-configuration/subagents）
- https://developers.openai.com/codex/agent-configuration/agents-md

当前文档支持 standalone TOML；必填name、description、developer_instructions，可指定model、model_reasoning_effort、sandbox_mode。project与global agents有不同位置；同名可覆盖built-in，因此使用 `sfd_explorer`，不覆盖默认explorer。

文档说明父运行时权限可影响子代理。TOML不是上下文清洗或严格隔离的保证，也没有文档化可直接写入TOML的 `fork_context` 配置。4.0要求在实际spawn工具支持的参数上声明不继承并保存launch evidence；无法证明就返回ADVISOR_CONTEXT_BLOCKED。不得发明模型、effort或工具参数。

## 6. Agent-native 并行开发

**R12 Cursor 原始研究（2026-01-14）**
- https://cursor.com/blog/scaling-agents

平级共享锁导致等待与任务回避，之后将planner/worker职责分开。它支持协调责任分离，但其大规模实验不是本项目分支门禁的直接成功率验证。4.0不复制无限递归planner或共享分支多writer。

**R13 Anthropic C compiler 实验（2026-02-05）**
- https://www.anthropic.com/engineering/building-c-compiler

16agents各自环境/clone、任务claim、合流；作者强调测试与环境设计和prototype局限。不能把“模型可处理冲突”当作省略冲突审查的依据。

**R14 Git 官方 worktree 文档**
- https://git-scm.com/docs/git-worktree

worktree提供独立checkout/index，但共享common Git metadata。4.0使用独立worktree+明确read/write/contract/resource依赖；版本化共享contract先接受再启动consumer。集成由主线程串行；绿分支不自动证明绿组合。

初始parallel上限2是本项目保守试运行参数；没有claim它最优。Audit记录因果DAG、排队/执行/等待、critical path、worker总时间、冲突和重复工作，之后再调并发。

## 7. 附件事实（不用旧Web资料覆盖）

**A01 当前 ZCode 功能说明**：九个`zcode_subagent_*`工具、workspace调用方负责、同canonicalworkspace一活跃agent、send排队且terminal拒收、cancel异步reap、没有Git结果、plan模式不等于read_only。直接决定当前适配，不能沿用旧zcode_review_continue或base_ref字段。

**A02 skill-doctor**：本地证据、多维度评分、缺代码证据排除于质量平均、针对失败改动。只借方法，不运行unsupported harness，不搬来renderer/评分曲线/skill coverage激励。

**A03 grill-me**：最终confirmed contract可以交接；但“既有plan settled statements视为requirements”的表述需谨慎，本Skill仍要求authority溯源。独立合同不是允许缺失关键语义。

**A04 audit corpus**：49入、40过程、9辅助。细分见同目录AUDIT_PACK_ANALYSIS.md，不在研究里重复消耗token复述全部日志。

## 8. 证据等级与剩余未知

| 问题 | 可支持的结论 | 不能支持的结论 |
|---|---|---|
| Astra官方资料 | 当前型号/价/effort、厂商任务族能力 | 本项目astra_medium与high/xhigh的已验证Pareto最优 |
| Sonar | 同任务同medium的aggregate与缺陷类别 | Luna表现、真实多代理分支成本、每题正确能力分类 |
| 社区对照 | 特定任务×计划×effort存在明显交互 | 3/3意味着稳定100%、可复制到所有repo |
| Anthropic架构实验 | 条件化成本/质量取舍、失败尾部重要 | Fable=Astra、Opus=Sol数值可直接迁移 |
| 并行原始报告 | 独立子任务、协调与测试是关键 | 仅mkdir多个worktree就不会竞争/质量下降 |
| 当前附件 | 当前MCP契约与实际阶段问题 | 用户本地模型可用性/真实运行成功 |

本发布没有实际模型采样、GLM运行、用户数据库/浏览器/host验证。交付中的测试是workflow/schema/packaging/配置和场景回归，不是模型性能benchmark。
