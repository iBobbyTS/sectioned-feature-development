# Sectioned Feature Development 4.3.1

**完整合并包：包含已交付的 PLAN admission／防膨胀定点修订。** 基于上传实际工作区，合入19个修订文件并同步正式4.3.1的发布文档；不是原先未含该补丁的4.3.1 ZIP。版本号和现有工作流保持4.3.1。

[本次合并记录](docs/version-history/v4.3.1/plan-review-fix/ASSEMBLY.md) · [定点修订分析](docs/version-history/v4.3.1/plan-review-fix/ANALYSIS.md) · [本次重新验证](docs/version-history/v4.3.1/plan-review-fix/ASSEMBLY-VALIDATION.md)

基于上传的实际 **4.3 项目**增量更新，继续保留从真实3.9恢复的执行产物、scope边界、review/repair/recovery、subsection、并行与审计职责。4.3.1只改变观察契约与审计输出；4.3的实现角色、计划冻结、review轮换、repair预算、并行和外部Advisor均不变。

## 执行链

保存确认需求 → **主线程编写并保存完整 PLAN-FULL** → 机械校验 → 实际委派独立 [@plan_reviewer](subagent://plan_reviewer) → 保存报告与admission → 按冻结模型派发section/subsection实现 → HANDOFF → bounded review／repair／delta → 父级reconciliation与验收 → DAG顺序集成和final gates → closure → audit与归档。

本次上传的本地版本已删除计划作者子代理；4.3保留这一修改，**不恢复不存在的计划作者角色**。主线程负责计划和工作流状态，仍不得替代真实implementer／repairer写产品或测试。审计OFF不关闭上述执行产物。

## 已合入的 PLAN review 定点修订

- 恢复原生与ZCode的full-review交替；不额外要求每个ZCode slot再做一遍原生review。
- 普通plan-only修正／候选拒绝可由主线程保存原reviewer报告、已审快照与逐项admission后继续；不伪造reviewer CLEAN。已知owner、依赖、模型、需求等边界变化仍要求真正的PLAN_DELTA。
- PLAN reviewer先检查必要性和可实施性；不把私有类型、probe输出schema或尚未创建的新文件机械地变成重复全量审查的理由。
- 保留同候选writer/reviewer时序、真实委派和精确HEAD证据；诊断使用`zas diagnose`，按`structuredContent.error`与SDK／JSON-RPC错误层级分别处理。

本次只是合并已经交付的修订，没有增加review阶段、修改模型组合、重置repair预算或更改ZAS产品代码。

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

## ZAS：更新后安装契约

先完成[ZAS改进执行合同](docs/ZAS_OPTIMIZATION_DIRECTIONS.md)，再使用4.3.1。保留既有九个生命周期工具，新增 `zcode_subagent_observe`；要求 `zas-observation/1.1`。Skill不提供未更新ZAS的正常降级路径，安装不匹配时直接报告配置错误。实际模型/运行时失败仍按既有规则处理，不假定服务永不出错。

observe只在主Agent怀疑无意义循环时调用，不作为定时检查或每次poll附加调用。默认输出本Agent调用最多的3类工具，各最近最多5次调用参数（无结果），加已确认公开reasoning delta合并后的最新200个Unicode字符。默认允许读取已验证公开字段；准确selector/key在本机runtime实测确认；encrypted_content在采集/日志/导出前递归排除。没有额外同意开关。

五种判断只放在[MCP工具描述](docs/contracts/zas-observe-tool.json)，由调用模型结合当前任务解释；ZAS无语义检测器、相似度分数或自动cancel。没有工具结果时也不能推断命令成功或文件未变化。

原生／GLM交替和物理attempt计数不变。send仍是队列，terminal continuation并未因本更新获得修复。取消后核验 `TERMINAL + resources_reaped`，再result/close；ZAS不替调用方管理Git。

本文和离线fixture不声称确认了用户本机的准确reasoning键名。该确认是ZAS执行包的首个实施与发布验收项，不是假设或通用回退提取器。

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

建议在当前feature关闭、ZAS升级完成后切换4.3.1。不提供旧活动STATE/PLAN的自动迁移，也不靠新门禁重判旧accepted工作；确需中途切换，先停止真实actors并保留旧执行环境/证据，再做显式受控迁移，禁止只替换Skill后假定旧角色ID和计划hash自动有效。

配套code-review仍使用 `sfd-delegated-review/4.2` 委托协议，避免仅版本号变化制造无意义的review兼容阻塞；4.3.1不改变其review次数或验收权。

## Audit

若流程包为 `~/Desktop/audit-pack/xxx.zip`，本feature/run全部ZAS证据放进 `~/Desktop/audit-pack/xxx-zas.zip`。主包只保留小型ZAS-LINK和必要workflow aggregates；子包有typed identity、attempt ledger、实际读取过的observe快照与必要诊断。

配对子包不是新的feature/sample。未用ZAS不生成空包；无关runtime/conformance和Advisor全库包仍在其他目录。先发布主包再绑定其确切hash发布子包；失败写PAIR_INCOMPLETE，重复finalize复用主包，不能不断换时间戳。

不生成 `.sha256` 文件；JSON manifest和receipt中的校验值保留。Audit OFF不关闭运行控制/清理，也不要求收集额外观察。

## 本轮文档

- [源码核查与旧协议差异](docs/version-history/v4.3.1/ZAS_SOURCE_REVIEW.md)
- [分析范围](docs/version-history/v4.3.1/AUDIT_PACK_ANALYSIS.md)
- [研究事实与可信度](docs/version-history/v4.3.1/RESEARCH.md)
- [修改依据](docs/version-history/v4.3.1/UPDATES.md)
- [验证与限制](docs/version-history/v4.3.1/VALIDATION.md)
- [3.9职责保留基线](docs/version-history/v4.2/RETENTION.md)

离线文件/Git/身份/测试检查不证明真实Codex、ZCode或模型一定正确；本机runtime键名与接口实现须由ZAS开发阶段的真实验收证明。
