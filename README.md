# Sectioned Feature Development 4.2

**基线：真实 v3.9 tag；不是继续缩写 4.0。** 未有审计证据或本轮明确授权的职责一律保留。

## 执行链

确认需求落盘 → 实际 [@plan_writer](subagent://plan_writer) 返回完整计划 → 主线程写 PLAN-FULL → 机械验证 → 独立 [@plan_reviewer](subagent://plan_reviewer) → 主线程保存报告并 admission → 逐业务 section / 串行 subsection 真实委派 → handoff → bounded review / admitted repair / delta → 父级验收 → 按 DAG 集成 → final gates → closure → audit。

文档中角色均使用 subagent 链接；链接不是调用证据，必须调用宿主工具并记录返回的真实 ID。Audit OFF 不会关闭这些执行产物。

## 保留与授权修改

保留 v3.9 的13份模板职责、完整 scope/security/repair/reset/recovery/integration 边界、计划提取、handoff、review ledger、audit/session/finalize 工具。多个 section 或多个可执行 subsection 必须独立分支+EXECUTE_WITH_COMMITS；已完成计划默认不重开。

Section 按业务验收划分；subsection 按父 section 内真实模块增量或不同推理负荷划分。子项串行，共享父合同、review和repair lineage；无 child acceptance、child PLAN gate或child final轮次。独立父项使用 git-worktree 目录和 .gitignore，可按读写/契约/资源约束并行；最大两writer的起始策略继承4.0，未宣称最优。

## 角色

| 名称 | 模型 | effort | 用途 |
|---|---|---|---|
| [@plan_writer](subagent://plan_writer) | gpt-6-astra | xhigh | 计划作者，只读返回完整草稿 |
| [@plan_reviewer](subagent://plan_reviewer) | gpt-6-astra | xhigh | 独立计划审查，不兼任作者 |
| [@implementer_1](subagent://implementer_1) | gpt-6-astra | medium | 尚不能安全拆解的结构推理 |
| [@implementer_2](subagent://implementer_2) | gpt-5.6-sol | medium | 默认非平凡实现 |
| [@implementer_3](subagent://implementer_3) | gpt-5.6-terra | high | 已有模式的局部新行为 |
| [@implementer_4](subagent://implementer_4) | gpt-5.6-luna | xhigh | 规则已确定、有范例和可判错oracle |
| [@code_reviewer](subagent://code_reviewer) | gpt-6-astra | high | 独立code/integration review |
| [@code_explorer](subagent://code_explorer) | gpt-5.6-luna | xhigh | 有界只读定位，不递归规划 |
| [@advisor](subagent://advisor) | gpt-6-astra | xhigh | 罕见、有限上下文独立裁决 |

这是继承4.0的可检验路由假设，不是新性能实验结论。不要把“安全代码”自动等同最大模型，或把“小diff”自动等同最低模型。一次明确under-routing后重评未解决部分，不逐档试错。Grill Me界面使用Astra high仍是合理起始选择，只在README记录，不自动改变用户设置。独立交接只给完整已确认Requirements Contract；原始grill对话留在provenance。

## 安装

```bash
python3 scripts/install.py                         # dry run
python3 scripts/install.py --apply --replace       # backups then install BOTH skills + nine agents
python3 scripts/install.py --only code-review --apply --replace
```

尊重 CODEX_HOME，默认 ~/.codex。安装器不改全局config或用户AGENTS.md，不删除旧名称agent或无关文件；本流程只使用上述新角色名。已有同名目标必须--replace并备份。Python>=3.11；本地状态锁/工具以macOS/POSIX为目标。

## 正常使用与恢复

显式要求使用Skill：默认执行到完成，但必须保存计划、真实派发和报告。自动触发：先宣布，首版PLAN-FULL完成后、PLAN review之前提供绝对链接让用户批准。当前非main分支按3.9的三选一授权。恢复旧功能只前瞻采用，不补造旧子代理、不重开accepted work来满足新schema。

根Skill的 [artifact生命周期](skill/sectioned-feature-development/references/artifact-lifecycle.md) 给出完整落盘/提取/派发/验收命令。STATE.json为机器事实；FEATURE-STATE.md由其渲染为完整可读状态，合同与原始review仍是语义证据。

## ZCode与Advisor

只使用附件定义的九个 zcode_subagent_* 工具。MCP不负责Git/worktree，send是队列、终态拒收，不虚构resume或read_only mode。Astra/GLM按feature-wide完整review序号轮换；checkpoint/delta不新增full pass，但每个真实调用进入audit。Advisor保留原请求合同，采用原生fresh-context实例；无法证明非继承上下文时阻塞，不能只提示“忽略前文”。

## Audit专属目录

只把本Skill的typed process audit放入 ~/Desktop/audit-pack/。代码审计、运行时实验、conformance和其他ZIP放别处，只作为辅助证据引用。原3.9分析维度与工具保留，新增模型/subsection/并行/Advisor字段；不能把telemetry gap升级成产品缺陷。

## 文档与验证

- [4.2 修改依据](docs/version-history/v4.2/UPDATES.md)
- [40个流程包与9个辅助包分析](docs/version-history/v4.2/AUDIT_PACK_ANALYSIS.md)
- [3.9职责保留清单](docs/version-history/v4.2/RETENTION.md)
- [研究与证据边界](docs/version-history/v4.2/RESEARCH.md)
- [验证记录](docs/version-history/v4.2/VALIDATION.md)

离线验证检查文件、Git、DAG、角色及反例，不证明真实Codex一定遵守，也未运行付费模型/用户ZCode端到端实验。
