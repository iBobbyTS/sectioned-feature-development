# Sectioned Feature Development 4.3

基于上传的实际 **4.2.1 工作区**增量更新，继续保留从真实3.9恢复的执行产物、scope边界、review/repair/recovery、subsection、并行与审计职责。只改变本轮要求：实现角色命名、计划冻结模型、ZAS受控beta观测、人工外部Advisor。

## 执行链

保存确认需求 → **主线程编写并保存完整 PLAN-FULL** → 机械校验 → 实际委派独立 [@plan_reviewer](subagent://plan_reviewer) → 保存报告与admission → 按冻结模型派发section/subsection实现 → HANDOFF → bounded review／repair／delta → 父级reconciliation与验收 → DAG顺序集成和final gates → closure → audit与归档。

本次上传的本地版本已删除计划作者子代理；4.3保留这一修改，**不恢复不存在的计划作者角色**。主线程负责计划和工作流状态，仍不得替代真实implementer／repairer写产品或测试。审计OFF不关闭上述执行产物。

## 固定模型分级

| 子代理 | 模型 | effort | 既有使用边界 |
|---|---|---|---|
| [@impl_nano](subagent://impl_nano) | gpt-5.6-luna | xhigh | 规则已定、有范例和明确可判错测试 |
| [@impl_mini](subagent://impl_mini) | gpt-5.6-terra | high | 既有模式下的局部新行为 |
| [@impl_std](subagent://impl_std) | gpt-5.6-sol | medium | 默认非平凡实现 |
| [@impl_large](subagent://impl_large) | gpt-6-astra | medium | 尚不能安全拆解的结构推理 |
| [@plan_reviewer](subagent://plan_reviewer) | gpt-6-astra | xhigh | 独立计划审查 |
| [@code_reviewer](subagent://code_reviewer) | gpt-6-astra | high | 独立代码／集成审查 |
| [@code_explorer](subagent://code_explorer) | gpt-5.6-luna | xhigh | 有界只读定位 |

**七份原生Agent配置、六种model–effort组合。** 不新增模型性能结论，继承此前待验证的任务路由。

PLAN-FULL机器块中，每个section和每个subsection都必须显式写 `profile`，只能取上述四种实现角色之一；同时保留model_reason、task_features与验收。父section选级用于父级集成／修复责任，不代替子项自身分配。不得写AUTO、待定或等执行时选择。

任务提取绑定 `plan_sha256 + unit_id + profile`；实际派发角色及已知model/effort必须匹配。遇到确切under-routing只对未接受的剩余任务做有依据的计划修订与必要delta复核，再派发；不静默换模型，不清空原repair计数。

Grill Me界面选Astra high的既有建议保留为起始假设，不作为Skill运行门禁。新Agent默认接收完整已确认Requirements Contract，不灌入全部grill聊天。

## 4.2职责保持

- 多section或多个可执行subsection：独立feature branch + EXECUTE_WITH_COMMITS。
- Section按业务合同，subsection按内部模块增量／模型能力。子项串行，共用父合同、检查和repair lineage，无独立child验收预算。
- 独立父section可以在`./git-worktree`下并行，目录写入.gitignore；读写、契约与外部资源互相独立才允许。审查中的候选不可修改。
- 完成后保存closure；后续修改重新判断普通小改或新feature，除明确授权不重开旧PLAN。
- 继承ONE/TWO、scope admission、reset正反例、五波累计预算和一次结构recovery规则；本轮未简化任何未证明有问题的职责。

## ZAS：受控真实项目beta

当前源码的工具族是 **zcode_subagent_status/spawn/poll/list/send/respond/cancel/result/close**，不是旧的带agent前缀工具族。实际installed tools/list及status才是运行权威。

原生／GLM feature-wide full-review交替不变；delta不新增full pass。ZAS不是绝对可用的gate：记录每个物理attempt，基础设施失败不算产品缺陷或repair wave，不能静默跳过GLM slot并宣称完整异构审查。

- 当前activity只证明活跃，不证明任务推进；reasoning仅有计数，tool主要有ID与类别。
- send是队列，不是interrupt；terminal continuation当前不可用。
- cancel后必须确认 `TERMINAL + resources_reaped=true`，再读结果/close；未回收前不复用workspace。
- 旧Hook默认强安全保证不适用当前源码；plan模式也不能代替审查快照前后校验。
- 当前spawn不提供caller幂等键；响应丢失先按repository查任务，不直接重试创建。

4.3只有一份adapter，分能力运行：当前协议为 `BETA_BASELINE_LIMITED`；**待用户实施建议后**，只有工具目录和status同时声明`zas-observation/1`时，才调用新增只读observation接口。没有假装该接口已经存在。

主线程结合有界任务与公开行为证据判断语义空转。没有字符串相似度杀进程、daemon自动判错、额外monitor LLM或每次poll都跑review。详见[ZAS adapter](skill/sectioned-feature-development/references/zcode-mcp-adapter.md)、[进展监督](skill/sectioned-feature-development/references/zas-progress-supervision.md)。

**给ZAS开发Codex执行：**[独立优化方向与验收合同](docs/ZAS_OPTIMIZATION_DIRECTIONS.md)。项目不包含或改写ZAS产品源码、二进制。

## Advisor：恢复3.9人工外部交接

不安装、不调用原生advisor agent。原始`ADVISOR-REQUEST.template.md`字节保持；六个ADV触发条件恢复3.9规则。触发后停止实际writer/reviewer，冻结请求和Git，打包完整工作树＋Git（含linked-worktree metadata和bundle）到 `~/Desktop/advisor-pack/`，提供人类交接prompt后停下。

外部结果原文落盘；**收到结果不是采纳授权**。记录用户明确accept/reject/clarify，才能按限定范围续跑。秘密检测命中时阻止导出；历史Git秘密检测仍需人工检查，不声称自动认证全历史安全。不自动上传、merge、reset或清理用户工作。

Advisor独立于Audit开关。查看[外部Advisor流程](skill/sectioned-feature-development/references/advisor-escalation.md)。

## 安装

Python 3.11+、macOS/POSIX工具环境：

```bash
python3 scripts/install.py                                  # 只列目标
python3 scripts/install.py --apply --replace                # 备份后装两份Skill和七份Agent
python3 scripts/install.py --only code-review --apply --replace
```

尊重`CODEX_HOME`，默认`~/.codex`。不会自动改AGENTS.md、全局config或删除其他Agent。旧编号实现角色和旧原生Advisor文件不再被本Skill引用；需要一并移出可发现目录时，可显式加 `--retire-legacy-agents`，安装器先备份这五个确切名称，再移除；不会删除其他角色。

建议在当前feature关闭后切换4.3。不提供旧活动STATE/PLAN的自动迁移，也不靠新门禁重判旧accepted工作；确需中途切换，先停止真实actors并保留旧执行环境/证据，再做显式受控迁移，禁止只替换Skill后假定旧角色ID和计划hash自动有效。

配套code-review仍使用 `sfd-delegated-review/4.2` 委托协议，避免仅版本号变化制造无意义的review兼容阻塞；4.3不改变其review次数或验收权。

## Audit

只把本Skill的typed process audit放到 `~/Desktop/audit-pack/`。ZAS diagnose、runtime/conformance材料和Advisor全仓包放其他目录，只在流程包内引用必要脱敏证据。

增加 `ZAS-AUDIT.md`、物理attempt／逻辑review关联、capability/build/observed model、进展窗口、误报、cancel/reap/close、失败与cleanup独立结果、caller/API成本。未知不填0，无新audit包时不重复沿用旧统计。Audit OFF时进展监督与清理责任仍存在。

## 本轮文档

- [源码核查与旧协议差异](docs/version-history/v4.3/ZAS_SOURCE_REVIEW.md)
- [分析范围](docs/version-history/v4.3/AUDIT_PACK_ANALYSIS.md)
- [研究事实与可信度](docs/version-history/v4.3/RESEARCH.md)
- [修改依据](docs/version-history/v4.3/UPDATES.md)
- [验证与限制](docs/version-history/v4.3/VALIDATION.md)
- [3.9职责保留基线](docs/version-history/v4.2/RETENTION.md)

离线文件/Git/身份/测试检查不证明真实Codex、ZCode或模型一定正确；ZAS增强接口和公开reasoning可见性需在实际runtime上单独验证。
