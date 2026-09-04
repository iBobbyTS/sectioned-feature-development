# 4.0 修改如何得出

## 必改项

| 输入证据 | 修改 | 不做什么 |
|---|---|---|
| 用户要求；P32 三section/no-commit | schema验证与dispatch前actual branch check强制multi-section commits+dedicated branch | 不把用户no-commit静默覆盖；冲突时停止 |
| P17/P14 完成后改旧PLAN | closed-feature SHA+request identity，follow-up重新评估 | 不把新要求追溯成旧功能漏做；显式reopen保留原revision |
| P37 原始ledger三次review时写HEAD | 每candidate冻结，独立worktree并行，dependent等待accepted+integrated | 不再用“全局一次只能一个agent”挡住独立工作 |
| 9个runtime/conformance混在folder | typed artifact_type/producer/schema/identity/manifest，legacy单列 | 不删除/移动用户旧包，不将其计为额外feature |

## 质量优先的成本改动

- R01–R06：保留用户的六model–effort组合；模型选择按任务结构+oracle，默认非平凡Sol。一次under-routing失败后重新路由，不逐档重试，也不假设Astra review免费兜底。
- R07/R08：Luna explorer只做能压缩主context的定向读取；明显小改跳过explorer。没有自动全库分析或多层sub-explorer。
- R09：不复制可能降低质量的廉价orchestrator设置；统计complete-outcome cost和失败尾部，缓存语义/费用来源分开。
- R12/R13/P20：共享基础先接受，独立消费者才并行；不为分级拆开一次事务或同一state transition。初始2writer可配置但非benchmark最优值。
- P33/P31：运行受影响包含tests后再花finalreview，截断logs用原始保存结果计数，不反复全量重跑。

保持原 ONE/TWO 的质量边界：ONE 初审直接 clean 可结束；若接纳 material finding，delta 闭合后仍需 fresh final。模型分级和并行并不自动降低独立 assurance。

## PLAN review针对性前移

P05、P12、P15、P18、P20、P25等反复揭示：真实生产入口/loader/权限载体、default/override、重复交互、cancel/late result、算法基数和环境gate顺序是高价值前置项。4.0在plan packet要求相应实例/oracle，只在触及时启用，不增加全仓扫描或第三轮PLAN review。

对于PLAN已明确但实现仍漏做的P12等，不靠重复相同指令修复；将AC与生产入口/测试直接交付implementer并核对。对实现级小wrapper、不影响行为的偏好，继续NIT，不升级审查范围。

## Advisor转换

- `ADVISOR-REQUEST.template.md`与输入版逐字节一致；只增加独立context manifest。
- model改为原生`advisor`/Astra xhigh，名字不含model。
- 不继承parent full chat，尤其主线程也是Astra时；不能通过developer instruction假装擦除已有历史。
- 保留低频trigger，不把advisor当第三个固定review。技术decisions在现有authority内由parent吸收，业务/风险/破坏性授权仍问human。
- 不再要求正常advisor交接先打完整仓库/Git ZIP。必要实际source通过frozenworkspace访问；原始手工Pro协议归历史资料。

## 当前ZCode，不做前版本架构幻想

删除所有过时工具名/假设，使用实际九工具。外部review是prompt/result契约，不是新增MCP mode字段。无terminal续接则明示gap，严格same-agent需求时blocked。MCP不给Git snapshot/patch/read_only guarantee，caller用独立Git候选与前后hash守住质量。

## Audit与Doctor

- Doctor的分维度证据方法进入审计；不采用加权总分、skill coverage目标或没有现场模型实验的完成百分比。
- P01产品usage不进入开发token；P06/P07复制摘要/P28矛盾计数不合成准确总计。
- 新audit记模型/effort请求与观测、路由特征、并行/等待/重做、advisor limitedcontext、GLMcontinuity、followup边界与自身audit开销。
- 已尝试却失败的repair仍计attempt/wave，避免旧“必须先闭合才计数”导致超过hardcap不自知。
- `.agent-work`不入Git。Routine process pack不含原始session/secret/full Git；只允许声明manifest文件。

## AGENTS与项目组织

- 把执行流程留在Skill；AGENTS只保留全局政策和工具约束，安装器不覆盖用户AGENTS。
- 一份current Skill、8份TOML，6个model/effort组合；不覆盖默认explorer，使用sfd_explorer。
- 历史Markdown研究保留供追溯，不作为4.0执行输入；不带旧仓库.git或用户audit ZIP。
- 本次提供单元/临时Git/worktree/安装/包装tests；没有把“配置能解析”冒称“模型已真实验证”。

## 下轮最重要的验证

1. 按任务特征对比Luna/Terra/Sol/Astra首次通过、escaped defect和总成本；重点看最难尾部，不只平均值。
2. Explorer返回内容是否真正减少父线程重复读，而不是额外一层。
3. 并行critical path是否缩短；冲突、资源干扰和merged-head缺陷是否增加。
4. Fresh advisor是否真的无父历史并能检查源代码；同Astra父线程时是否提供新证据而不是复述。
5. GLM终态delta gap比例与用户期望；需要真正resume时应改MCP产品，而不是skill伪造能力。
