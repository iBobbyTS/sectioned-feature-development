# 4.4 修改依据与范围

## 核心决策

- 用户明确要求评估只保留基础 section 校验；latest rollout 实际零实施而陷入 format/requirements hash/receipt 匹配。本版采用 agent-managed orchestration。
- 不再安装 workflow.py、execution_artifacts.py、advisor_flow.py；精确旧代码/测试保存在本版历史，不加载进产品任务。
- 重写 section_plan.py 为只检查 section/subsection ID、依赖、父子归属及显式 impl 链接。允许普通自由 Markdown，错误批量报告，无 JSON/state/Git/approval 校验。list/extract 只是便利工具。
- PLAN-FULL 唯一业务合同，FEATURE-STATE 唯一可读进度；不再要求 STATE.json、机器 approval receipts 和每次 plan hash 对等。原始独立 review、main admission、真实派发/HANDOFF 与实际测试仍必须发生。
- 恢复旧批准计划时区分真实证据缺口和格式差异；不同 feature 的 plan-draft 不得借用。

## 保留的质量/授权行为

保留七个 agent 配置、固定每单元 impl、真实 delegated repair、ONE/TWO、feature-wide Astra/GLM slot、terminal continuity 限制、五波父级/集成预算、subsection checkpoint + parent reconciliation、独立父级 worktree 安全、final-head tests、低频外部 human Advisor、关闭后重评新请求。

保留 scope-control 正文、安全边界、reset 正反例和 private mechanism 必要性判断；没有因少脚本弱化产品 auth/durability/permission 约束。

## 保留但改变调用时机的工具

- Git exclude helper：入口一次，附加 --repo alias 修复日志中已出现的参数误用。
- audit trace/session：可选 capture，主要事件；日志缺字段不阻塞产品。没有 raw 内容时诚实记 gap。
- atomic audit finalizer、typed intake、paired ZAS、Advisor export：实际打包时用；文件 safety/manifest hash 属于传输完整性，不属于实施授权。
- ZAS wire helper：仅怀疑不合契约时用，不是每个 poll/gate。新增 --compact 模式对应本次拟实施的公共瘦身；明确不验证模型来源，不将删掉的字段补成虚假 provenance。

## ZAS PLAN

3 sections → 2 业务 sections + 同父串行子项；contract/tests/docs 随变更，release/live 保持 final gate。八位 JSON ID 不强制全库存储类型重写；不移除私有日志/完整性/已验证 reasoning selector。新会话只做实际边界 PLAN_DELTA，不为历史 schema 重新 full review。ZAS 产品源码本轮未改。

## 配套 code-review

保留 sfd-delegated-review/4.2 与 flat /4.0 的语义，新增普通 Markdown 包同样可用的说明；没有新 repair loop、没有改变 acceptance 或 provider schedule。无需因发行号变化重审历史。

## 测试处理透明性

退役的旧调度/receipt tests 不是失败后删掉来假装通过：它们专门验证本轮用户要求撤除的机器 gate，已完整归档。数据安全/ZIP/配对、安装与 code-review 语义测试保留；新增结构工具和 agent-managed 文档反例。详细 counts 见 VALIDATION，不把旧 178 与新总数作优劣比较。
