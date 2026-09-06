# 4.1 修改推导与边界

| 证据/要求 | 本次改动 | 刻意不做 |
|---|---|---|
| 用户需要提前进一步拆实现，不能等LOC爆表 | optional SUBSECTIONS与明确内部合同/checkpoint | 不增加LOC门槛、不强制每节拆 |
| S04同一规则交叉条件仍需一起测试 | parent shared_invariants和joint_oracles | 不把每个错误分支拆独立section |
| domain→HTTP和其他真实increment合理 | 子节产品+测试+定向review，CHECKPOINT_VERIFIED | 不把child green称ACCEPTED或解锁外部依赖 |
| 以往复制full-review与repair预算导致长循环 | 一次primary coverage分批完成，parent final，original lineage总计 | 不给child另一套ONE/TWO、五波和advisor |
| 最终组合可能有局部测试漏掉的缺陷 | 最终candidate primary reconciliation、真实jointoracle、fresh final | 不以局部green简单求和代替整体校验 |
| 上传project缺当前code-review runtime目录 | 补齐可安装companion4.1并兼容4.0 packet | 不修改用户机器现有自定义文件、不只放历史appendix |
| PPPMS live提案已有源对齐修改与4个accepted | 45parent保持，仅四pending parent各添2child | 不覆盖B02、不恢复旧retention drift错误、不清旧budget/cursor |

## 文件与协议

- SKILL只增加核心两层语义和reference链接；细节在subsections.md。
- PLAN保留schema4标记；workflow_revision=4.1启用可选子结构，旧atomic计划仍能校验。
- workflow.py增加next-unit、acceptance-check、reserve-repair。既有ready仍按parent DAG，检查不同worktree/资源；没有让所有task并行。
- acceptance-check验证记录结构和（CLI模式）实际Git ancestry/artifact hashes；语义充分性、实际测试结果和scope admission仍由parent负责，不声称机器能“证明无bug”。
- review4.1明示SUBSECTION_DELTA包括新实现，不误当repair-only；PARENT_RECONCILIATION只完成主coverage，不能冒充fresh final。
- Audit继续一个parent/feature pack，新增child/lineage身份记录，不产生每child ZIP。每次实际模型调用均计成本。
- 模型/effort/九个ZCode工具、Advisor原请求模板、主要Git/完成后新请求策略全部保持。

## 迁移

4.0已接受section和点号ID都保持历史事实。活跃writer/reviewer先冻结；只给未开工或剩余内容增加checkpoint。版本、schema或模板变化本身不作废代码/测试。父级extra repair只能由具名advisor/owner authority授权，累计数字仍保留超过5的事实，禁止第六波被改名成child wave1。

## PPPMS

本包另交付完整PLAN-FULL和原requirements/legacyAC/validation/routeowner附件。四个parent原字段逐项相等，DAG和check registry原样保留；仅全局状态标成DRAFT、快照更新及subsection元数据增加。提出的4.1不是已在用户环境接受的计划，不将快照STATE当新bootstrap。

## 试运行评估

记录：first checkpoint反馈时间、累计读取/审核成本、parent jointoracle揭示缺陷、被后续改动invalidated的checkpoint、same-session真实可用性、parent总repair/重做量和外部遗漏。质量优先；若child增加负担却不能提前发现不同问题，应合回工作步骤，而不是不断拆深。
