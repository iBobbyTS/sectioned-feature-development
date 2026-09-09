# Sectioned Feature Development 4.4

基于完整 4.3.1 的定点减负版：**Agent 调度、真实执行证据、仅基础 section 结构校验**。没有回退模型分级、业务 section／内部 subsection、真实子代理、独立审查、修复预算、并行隔离或外部 Advisor。

## 执行顺序

主线程写完整 REQUIREMENTS 与 PLAN-FULL → 一次基础结构校验 → 实际独立 PLAN review → 主线程 admission → 保存当前 TASK 并真实委派 → HANDOFF／候选冻结 → bounded review／delta repair／必要 fresh final → 父级验收、集成与最终验证 → 关闭计划 → 规范 Audit。

自动触发仍在第一份 PLAN 后等人工批准；显式调用仅免这一暂停。Audit OFF 不免执行产物。大于一个业务 section 或一个可执行 subsection 必须独立分支与提交。已完成功能后新增需求重新评估。

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

七份配置逐字保留。任务—模型分级仍是待真实样本验证的策略，不是已证明成本最优。Grill Me 在界面使用 Astra high 仍是起始建议，只写在 README；确认后的自包含需求合同可单独交接，原访谈保留为审计 provenance。

## 安装

```bash
python3 scripts/install.py                      # dry run
python3 scripts/install.py --apply --replace    # 备份后完整替换两份 Skill 和七份 Agent
```

尊重 `$CODEX_HOME`（默认 `~/.codex`）；不覆盖 AGENTS.md/global config/无关 Agent。必须完整替换同名 Skill，不以增量覆盖留下旧 gate 脚本。安装器按确切目标先备份，因此这不授权清除产品仓库内容。

新会话读到 4.4 后，不再“升级”旧计划的 JSON schema。保存旧状态为历史，核对当前业务计划、相关真实 review 和 source/Git 一次，继续未接受部分。真实缺口仍需有界补证据，不能造回执。

## 文件

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
