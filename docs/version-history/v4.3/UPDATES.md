# 4.3 更新依据与保留边界

## 本轮授权变更

| 变更 | 依据 | 实际位置 |
|---|---|---|
| 编号实现Agent → impl_nano/mini/std/large | 用户明确要求 | agents、PLAN/TASK、role registry、tests、README |
| 所有父/子项计划阶段固定profile | 用户明确要求，不允许运行时任意选级 | PLAN机器块、workflow.validate、TASK profile/hash、stage_start |
| ZAS受控beta与实际短工具名 | 本次schema+facade与旧adapter不同 | zcode-mcp-adapter、ZAS source review |
| 有界公开行为观测建议 | activity只保留计数/类别，缺语义判断事实 | 独立ZAS优化文档、proposed schema、capability-gated adapter |
| 任务语义停滞与运行活跃分开 | 用户明确拒绝字符串相似度检测 | zas-progress-supervision、zas_evidence、测试 |
| ZAS全物理attempt与cleanup审计 | 用户要求改进ZAS与总体lifecycle | zas-audit、attempt模板、trace zas family |
| 外部Advisor回退 | 用户明确要求3.9流程 | 原六ADV、原请求模板、advisor_flow/pack、人类adoption |

## 本地修改与最小兼容修正

上传实际为4.2.1而非最初4.2交付：plan_writer已由本地commit删除。保留主线程计划作者，补齐与实际文件一致的落盘/验收测试；不重新添加它。两份reviewer本地文本及旧历史数据保留。

基线99项project测试中的失败为agent数/原生advisor已过期，另一个错误为旧测试引用不存在的历史Advisor模板路径。修正测试指向当前7角色和实际v3.9原模板证据；没有用删除旧回归覆盖来使结果变绿。

配套code-review发布文件仍随项目提供，单轮输出、assurance、continuation、parent admission不变；委托协议保留4.2避免只因版本号强迫重做审查。原测试覆盖继续执行。

## 不变项

3.9恢复的13模板职责、artifact lifecycle、PLAN review独立性、scope/security具体边界、HANDOFF、review ledger、五波计数、一次结构recovery、integration独立责任、验证复用、session提取、原子幂等process audit保留。

4.x section/subsection分工、同父子项串行、独立父项worktree并行、父级repair lineage、multi-section提交要求、completed计划不自动重开、原生/GLM轮换都保留。此轮不引入新的总体简化。

## 运行兼容

当前ZAS源代码只支持BASELINE_LIMITED。用户实施优化后，工具列表与capability都匹配才开启ENHANCED_OBSERVATION；public_content需独立collection授权。缺能力可继续普通bounded review但记gap；明确要求验证新观测能力的测试必须blocked，不能伪装成功。

Advisor默认外部交接，无原生advisor；收到结果保留阻塞直到真实用户采纳。打包目录与process audit严格分开。完整Git带潜在历史敏感信息，自动scanner不提供全历史安全承诺。
