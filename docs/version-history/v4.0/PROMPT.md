# Sectioned Feature Development
先确保你可以访问我上传的文件，再继续任务，否则直接结束回答。

## 本轮audit pack分析
有部分干扰pack可能要过滤掉，本次更新完的skill也要明确，使用这个skill时，只有本skill要求的audit方法才放入这个文件夹，其他目的的audit的不要进入。

## Skill 进化
关注warp的skill doctor(skill-doctor.zip)，它可能可以给你的分析做出参考。
分析本轮audit pack里每阶段的review结果，有没有可以在section划分或plan review部分提前避免的。

## 人工确认的必要修改
1. >1 section必须使用EXECUTE_WITH_COMMITS和单独分支。
2. 完成后如果用户有提出修改，不得重新打开之前的PLAN-FULL补section，除非用户明确要求，否则直接重新评估是否需要开新的sectioned-development还是可以直接修的小改动。

## grill-me
grill-me的结果是否可以单独使用，不带grill部分的上下文给新的agent？

## 新可用模型
### gpt-6-astra
gpt-6-astra发布：价格来到了$10/50，不再适合作为所有阶段都使用，应该明确对不同阶段的任务进行分级。请你上网搜索gpt-6-astra的资料，现阶段还比较少，不要拿上代旗舰gpt-5.6-sol代替，允许你做出合理推测并在我接下来的流程里验证。
OpenAI工程师Max Stoiber提醒：建议删除现有的Agents.md，然后重头编写。因为GPT-6的指令遵循能力太强了，任何冗余的指令都会削弱它的表现。我认为我的AGENTS.md值得简化之前为了约束模型的部分，保留流程约束（如语言、git、codegraph等）

### zcode (glm-5.3)
我仍然希望使用外部glm补充review视角，zcode-as-subagent现在开发好，codex可以spawn, poll, interrupt, 安排zcode和gpt reviewer间隔。文档在zcode-as-subagent功能说明.md

## Subagent分级
### 模型能力边界分析
继续搜索gpt-5.6-sol, gpt-5.6-terra, gpt-5.6-luna的能力边界、它们不同reasoning effort的能力，根据本skill的不同阶段，分析最适合的组合。不要设置大量组合，如(astra, sol, terra, luna)*(low, medium, high, xhigh, max)=20种组合给Orchestrator选，只选择必要的组合。注意一点，过于复杂的任务给luna/terra去执行，之后再给astra review，可能会留下更多问题，导致成本反而比sol执行高（上网搜索有没有类似的报告或社区讨论）。因此section的划分除了功能，可能还要根据复杂度划开，让适合的模型去执行。我自己的想法是luna_xhigh, terra_high, sol_medium, astra_medium 这4个负责实现，astra_high负责code review，astra_xhigh负责plan创建和review。grill-me用户自己在界面里选择astra high，请你确认一下astra high是否合适，写到readme里，不需要进入skill。
不要凭直觉写luna用于有明确边界的任务，astra用于安全相关的高危任务，这样的依据可能无效。去看terra，luna的benchmark时，不要只看最终分数，尽量找benchmark里每一题的情况，没有的话可以靠社区实测反馈来确定各模型的能力边界。如果实在找不到，允许使用你认为的最好的方案或者我前面说的那种传统分类，然后确保audit流程输出的pack可以用于分析任务-模型分类结果用于之后的分析。

### cheap explorer
https://openai.com/index/builders-guide-to-gpt-5-6/
这里面提到了luna做code exploration step，claude code也会主动让haiku做code explore。查一下ai服务商给的报告、社区讨论以及其他agent，怎么设计低成本explorer。

### Codex subagent 配置
Codex目前可用的是在$CODEX_HOME（通常~/.codex）/agents里定义subagent的模型、思考深度、description(给主模型看)、developer_instructions(给subagent的developer类型消息)，请你帮我设计好和本skill配套的agents。

## Agent 开发架构
Anthropic比OpenAI早发布$50级别模型，已经有官方指引了，学习何时使用Fable(对应GPT-5.6-Astra)，何时使用Opus(对应GPT-5.6-Sol)，请你完整阅读这篇文章。
https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence
介绍了Advisor和Orchestrator两种架构，学习它的思想。

本skill原定的Advisor是gpt-5.6-sol-pro，需要用户去手动询问。现在改成gpt-6-astra为advisor，交接合同文件不变，改用subagent，你需要研究claude code的advisor strategy (可以参考 https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool )，并定义advisor subagent，名字就叫advisor，不需要带gpt, astra等。
考虑到主agent也是astra的情况，advisor所有情况只能看到有限的上下文，避免被干扰，它需要独立根据advisor交接文档和项目实际情况做出决策。


## 并行开发
上网搜索coding场景多subagent并行开发的技术报告、博客等，学习并行开发的原理原则（传统人工开发的并行开发可以参考，但需要考虑到agent-native的执行状况），在PLAN阶段分析可并行执行的步骤，如果可并行的话，`mkdir -p ./git-worktree`，并确保它在.gitignore里；把每阶段是否可并行、互相依赖关系完整写在PLAN-FULL里，确保可执行。

##Audit流程
新加入的流程也都要进入审计包，用于下次分析。

## 输出
按照项目形式，不再是单个skill。接下来是4.0版本。
sectioned-feature-development
	skill/sectioned-feature-development
	docs/
		CHANGE_LOG.md （流程上进行了什么修改）
		version-history/{version_number}/
			PROMPT.md （用户原始prompt原样写入）
			AUDIT_PACK_ANALYSIS.md (AUDIT_PACK的分析，不得包含敏感信息，可以包含项目的逻辑、流程缺陷等非敏感用于分析的信息。)
			RESEARCH.md (根据PROMPT和AUDIT_PACK_ANALYSIS搜索的外部资料、提取的事实和可信度(比如博客/技术报告/社区讨论))
			UPDATES.md (如何通过AUDIT_PACK和RESEARCH得出本次的修改)
	agents/
		所有定义的subagent
	README.md 简要的执行流程、设计理念、和安装方法。
