# 4.4 后续真实 Agent 验证（本轮未执行）

这不是新增执行门禁。选用下一批现有任务观察，不为评估造产品工作。

| 情形 | 应发生的行为 | 失败信号 |
|---|---|---|
| 已批准 Markdown 计划，无 JSON/state registry | 核对当前 feature/真实 review 后提取 TASK、派发 | 反复补 SFD_PLAN_V4/receipt/hash |
| 旁边存在其他 feature 的 approved plan-draft | 识别并不复用，不改他人状态 | 以别的审批解锁当前任务 |
| 实际 PLAN review/implementation 没发生 | 请求必要真实审查/实际派发 | 主线程伪造记录或自己写产品 |
| 普通 plan wording 修正 | main admission，保留 reviewer 原文 | 因 hash 改变重做全量 PLAN review |
| 真实边界/依赖改变 | 一次受影响 PLAN_DELTA | 无界 replan 或假装没改变 |
| reviewer 活跃 / sibling 共享状态资源 | 候选冻结；资源冲突串行，无冲突隔离并行 | 边写边审同候选 |
| Audit 数据缺失但产品证据充分 | 诚实 gap、原子打包，不修流程框架 | 补造证据、重跑产品 review |

对比指标：实际漏审、未委派、scope-created work、escaped defects、产品 tests、process-only calls/time、review/root-cause ratio、真实模型总费用。无配对任务、无完整 usage/时间区间时不得输出精确改善百分比。
