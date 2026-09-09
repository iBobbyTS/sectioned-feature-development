# Sectioned Feature Development 4.4.1

基于 4.4 的时序与身份澄清补丁：**Agent 调度、真实执行证据、仅基础 section 结构校验**。没有回退模型分级、业务 section／内部 subsection、真实子代理、独立审查、修复预算、并行隔离或外部 Advisor。

## 执行顺序

主线程写完整 REQUIREMENTS 与 PLAN-FULL → 一次基础结构校验 → 实际独立 PLAN review → 主线程 admission → 保存当前 TASK 并真实委派 → HANDOFF／候选冻结 → bounded review／delta repair／必要 fresh final → 父级验收、集成与最终验证 → 关闭计划 → 规范 Audit。

自动触发仍在第一份 PLAN 后等人工批准；显式调用仅免这一暂停。Audit OFF 不免执行产物。大于一个业务 section 或一个可执行 subsection 必须独立分支与提交。已完成功能后新增需求重新评估。

## 4.4.1 的两项强化

**先等真实 review 返回，再由主线程 admission，最后才派下一实现。** PLAN review（含已选择的 GLM challenge 和真正必要的 delta）是全 feature 的前置条件；不能边审边 spawn S01。串行 S01 还在 initial/delta/final 或必要测试阶段时，不能 spawn S02。子项必须等上一 checkpoint 闭合；BLOCKED/ABANDONED/取消不是依赖满足。

仅保留已审计划明确列出的独立父 section 并行例外：不同工作树、依赖已集成、路径/契约/共享资源不冲突。没有明确说明就串行；不能因为不同文件、缺少依赖标签或 reviewer 在等待而临时推断可并行。

**[@code_reviewer](subagent://code_reviewer) 永远是原生 Codex/Astra 角色，不是 ZCode 的别名。** 原生 slot 走 Codex native subagent 派发与等待；GLM slot 由主线程直接调用 ZAS MCP spawn/poll/result。`$code-review` 只是两者复用的审查方法。不能在每个 slot 先跑原生再补 ZAS，不能用 native reviewer 包一层 MCP 转发，也不能把两类 ID 混用。

每次实际交接只在已有状态/TASK/REVIEW 中写清「已闭合前提、仍活跃对象、实际 route/ID」。不恢复 STATE.json、actor registry、approval-hash 或 ready 脚本。已完成的历史 section 不因升级重开；当前活跃任务先确认真实 actor 状态，再应用这些规则。

## 去掉什么，保留什么

不再安装 `workflow.py`、`execution_artifacts.py`、`advisor_flow.py`，不要求 PLAN 内 SFD_PLAN_V4 JSON、不要求 STATE.json、actor 注册或 hash-matching approval/ready/accept 收据。历史实现与退役测试保存在版本记录，不进入安装目录。

保留人可读 PLAN／FEATURE-STATE／TASK／HANDOFF／REVIEW，以及真实 ID、Git candidate、实际测试与 review 结果。主线程必须基于它们做调度，不能用“agent-managed”作为跳过委派或审查的许可。

只对 IDs、依赖 DAG、父子归属及每单元明确 impl 级别进行基本结构校验。脚本是读写确定性文件/安全打包的工具，不是一个程序化项目管理系统。原子 Audit／ZAS 配对／Advisor Git 导出／本地 ignore 工具保留，仅在对应操作发生时使用。

## 角色

- [@impl_nano](subagent://impl_nano)：Luna xhigh。
- [@impl_mini](subagent://impl_mini)：Terra high。
- [@impl_std](subagent://impl_std)：Sol medium。
- [@impl_large](subagent://impl_large)：Astra medium。
- [@plan_reviewer](subagent://plan_reviewer)：Astra xhigh；主线程作者与审查者不共用实例。
- [@code_reviewer](subagent://code_reviewer)：Astra high。
- [@code_explorer](subagent://code_explorer)：Luna xhigh，只做有界证据地图。

七个角色及全部 model/effort/sandbox 配置保持。六份执行/审查角色只强化职责描述和交接指令，code_explorer 逐字保留。任务—模型分级仍是待真实样本验证的策略，不是已证明成本最优。Grill Me 在界面使用 Astra high 仍是起始建议，只写在 README；确认后的自包含需求合同可单独交接，原访谈保留为审计 provenance。

## 安装

```bash
python3 scripts/install.py                      # dry run
python3 scripts/install.py --apply --replace    # 备份后完整替换两份 Skill 和七份 Agent
```

**必须更新完整项目中的两份 Skill 和七份 Agent，不只替换根 SKILL.md。** 描述层的 native/ZAS 区分位于 agent TOML，旧会话可能已缓存旧配置，优先在更新后使用新会话。

尊重 `$CODEX_HOME`（默认 `~/.codex`）；不覆盖 AGENTS.md/global config/无关 Agent。必须完整替换同名 Skill，不以增量覆盖留下旧 gate 脚本。安装器按确切目标先备份，因此这不授权清除产品仓库内容。

新会话读到 4.4.1 后，不再“升级”旧计划的 JSON schema。保存旧状态为历史，核对当前业务计划、相关真实 review 和 source/Git 一次，继续未接受部分。真实缺口仍需有界补证据，不能造回执。

## 文件

- [4.4.1 修改依据与边界](docs/version-history/v4.4.1/UPDATES.md)
- [4.4.1 验证与未验证项](docs/version-history/v4.4.1/VALIDATION.md)

以下保留 4.4 原研究和历史交接，ZAS 的旧交接不是本次新增产品计划：

- [本轮分析与三份 rollout](docs/version-history/v4.4/AUDIT_PACK_ANALYSIS.md)
- [官方与社区研究](docs/version-history/v4.4/RESEARCH.md)
- [逐项修改及职责保留](docs/version-history/v4.4/UPDATES.md)
- [脚本对比](docs/version-history/v4.4/SCRIPT-INVENTORY.json)
- [验证与未验证边界](docs/version-history/v4.4/VALIDATION.md)
- [ZAS 新计划](docs/version-history/v4.4/zas-handoff/PLAN-FULL.md)
- [ZAS 新会话 Prompt](docs/version-history/v4.4/zas-handoff/NEW-SESSION-PROMPT.md)

## ZAS 协议

当前 4.3.1 公开协议与本次计划的 compact 公共契约分别可按实际 tools/list 使用；不是要求 ZAS 保持两个版本。4.4 adapter 不再要求新版刻意删除的 version/source/identity 回显。可选 wire 检查器 `--compact` 只验证 3/5/200、有界结构和 encrypted_content 排除，不能证明模型身份、推理正确或任务有进展。开发 ZAS 自身时按任务明确的 native-review override，不调用修改中的服务审查它自己。

## 审计与限制

流程包 `~/Desktop/audit-pack/xxx.zip`、真实 ZAS attempts 配对 `xxx-zas.zip`；外部 Advisor 在另一个目录。无 `.sha256` 侧文件。工具只保证其有限确定性工作，不保证 Agent 会遵守流程。下一批实际样本必须同时看真实漏审/跳过委派/逃逸缺陷与过程成本，不能用离线测试冒充模型行为实验。
