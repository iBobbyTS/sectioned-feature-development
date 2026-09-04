# Sectioned Feature Development 4.0

这是一个包含 Skill、Codex 子代理配置、验证脚本和版本研究记录的项目。目标是减少昂贵模型的重复探索和返工，同时保留原始需求、独立 review、精确候选快照和集成验收。

## 执行流程

确认 Requirements Contract → 按需 Luna explorer → Astra xhigh 计划 → 不同实例 Astra xhigh PLAN review → 必要时 GLM challenge → 按依赖图和任务结构分配实现 → Astra high / GLM 交替 full review、局部 delta 修复 → 串行集成与精确 HEAD 验证 → 关闭计划并生成流程 audit。

关键规则：多于一个 section 必须独立分支且 `EXECUTE_WITH_COMMITS`；完成后的用户修改重新评估，不自动追加旧 PLAN。可以并行的是独立 DAG 节点，不是任意两个 Agent；每个正在审查的工作区必须冻结。

## 安装

需要 Python 3.11+（TOML 验证）、本地 Codex 支持 standalone custom-agent TOML，以及已安装的 `$code-review`（在父流程内作为单次 delegated review 使用，不另开 repair loop）。本项目不覆盖你的 code-review Skill。ZCode 本版本按所附 macOS MCP 文档适配；不声称 Windows GLM 可用。

```bash
python3 scripts/install.py                    # dry-run，尊重 $CODEX_HOME
python3 scripts/install.py --apply            # 只安装到不存在的目标
python3 scripts/install.py --apply --replace  # 先备份确切目标，再完整替换
python3 -m unittest discover -s tests -v
```

安装位置：`$CODEX_HOME/skills/sectioned-feature-development/` 与 `$CODEX_HOME/agents/*.toml`；未设时使用 `~/.codex`。八份配置明确指定 name、description、model、model_reasoning_effort、sandbox_mode、developer_instructions，不覆盖其他 agent 或全局 config。安装器不删除旧的 differently-named v3 skill；确认不再使用后自行停用以避免同时触发。

[简化的 AGENTS.md](docs/AGENTS.example.md) 供人工替换/合并；安装器不会改它。保留语言、Git、Docker、CodeGraph、验证和 anti-loop 政策；详细编排只在 Skill 中定义。不要照搬“删除文件”而丢掉用户安全和授权规则。

启动新的 Codex 会话后核对这些模型/effort 和自定义 agent 确实加载。父级运行时 permission override 可能影响配置默认值，需检查实际权限。配置有效不等于账号可用；不支持时应报 `MODEL_CONFIG_UNAVAILABLE`，不能默默换模型。第一次正式使用前核验原生 fresh-context 子代理和 ZCode `system_status`。本发布只做了本地脚本/配置/场景测试，没有实际调用你机器上的 Codex 或 ZCode。

## 固定角色与模型

| 名称 | 配置 | 用途 |
|---|---|---|
| luna_xhigh | gpt-5.6-luna / xhigh | 有已验证范例、决策已给定、可判错 oracle 的实现 |
| terra_high | gpt-5.6-terra / high | 熟悉组件/路径，有限新增状态 |
| sol_medium | gpt-5.6-sol / medium | 默认非平凡实现；跨表示/状态语义 |
| astra_medium | gpt-6-astra / medium | 不能安全拆解的新结构或困难推理 |
| astra_high | gpt-6-astra / high | 独立 code review |
| astra_xhigh | gpt-6-astra / xhigh | 创建 PLAN；另一个实例 review PLAN |
| sfd_explorer | gpt-5.6-luna / xhigh | 有界只读 owner/caller/test 探索 |
| advisor | gpt-6-astra / xhigh | 低频隔离上下文技术裁决 |

总共六种 model–effort 组合，不给主 Agent 一个二十组合的选择菜单。这些路由是带依据的首版假设，不是 benchmark 已证明的能力分界。具体挑选依据和失败升级见 Skill 的 models reference；新 audit 统计首次实现、审查、修复、升级、集成的总成本和 escaped defects。

## Grill Me 与交接

用户在 UI 选择 **Astra high** 做 grill-me 是合理的初始设置：该阶段主要做材料理解、遗漏识别和人类语义决策，不需要默认 xhigh/max。没有 matched-effort 实验能证明 high 最优，后续记录问题质量、遗漏、澄清次数与 downstream rework即可。这个 UI 偏好只放 README，不进入执行 Skill 或自动配置。

确认后的 Requirements Contract **可以独立交给新 agent**，前提是包含原始目标、边界、准确反例、更正/取代、确认决定、假设、可测试 AC、planner discretion 和真实未决项。原 grill 对话只进入审计 provenance，不默认进入计划/实现/advisor。既有 PLAN 中未经用户确认的内容不能自动升级为要求。

## 当前 ZCode 适配边界

只调用文档中的九个 `zcode_subagent_*` 工具。MCP 不负责 Git/worktree/commit/patch；由编排层管理。`send` 是排队而非 interrupt；终态拒收，不能恢复同一个完成会话。取消后等待 TERMINAL + reaped。

因此普通澄清尽量同会话；终态后的 repair delta 默认使用**同 provider 新 agent + 原 finding 合同**并记录 continuity gap，不能声称 same-agent。需要绝对同会话语义时保持 `CONTINUITY_BLOCKED`，而不是伪造 `continue` 工具。plan permission mode 本身也不构成只读保证，必须隔离评审工作树并核对前后产品指纹。

## Advisor 与并行

保留原 `ADVISOR-REQUEST.template.md` 原始字节，调用名为 `advisor` 的原生子代理，不再要求人工问 Pro。即使主线程也是 Astra，advisor仍使用非继承新上下文，只读交接文件与必要源码。如果宿主不能证明无父对话继承，报告 `ADVISOR_CONTEXT_BLOCKED`；TOML 不含虚构的 context-isolation 参数。

并行从 `max_parallel_writers=2` 开始，PLAN 里记录读/写路径、语义契约、排他测试资源和顺序。先把 `/git-worktree/` 加入 `.gitignore` 再创建工作树。先接受共享基础，再并行消费者；在 feature 分支串行集成。该并发数是保守试运行设置，未经本项目性能实验，不是最优结论。

## Audit 与版本历史

只把本 Skill 的 typed **process audit** 放 `~/Desktop/audit-pack/`。产品安全审计、runtime/conformance、手工 advisor 证据不进入；不自动删现有外来包。LIVE audit默认开启，`audit off`不关闭质量/advisor机制。

[本轮逐包分析](docs/version-history/v4.0/AUDIT_PACK_ANALYSIS.md)、[外部研究](docs/version-history/v4.0/RESEARCH.md)、[证据→修改](docs/version-history/v4.0/UPDATES.md)、[原始请求](docs/version-history/v4.0/PROMPT.md)、[验证与未实测项](docs/version-history/v4.0/VALIDATION.md)。历史 Markdown 文档保留为历史资料，不自动加载，不代表当前规则。
