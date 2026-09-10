# v4.5 修改与依据

| 修改 | 直接依据 | 本版边界 |
|---|---|---|
| 在原 PLAN 阶段挂接 composable router | 用户要求；adaptive-debugging causal-domain 组合 | 不是新触发器、新 phase 或新脚本 |
| universal 与未知技术回退 | 用户明确要求未命中也可用 | 不猜框架；仅必要时查版本 source |
| full-stack + stack + concern 去重 | 多组合示例，非 Java 的 LMDO 说明 | 一个 PLAN/边界例子，不按模块叠 reviewer |
| boundary contract 贯穿 PLAN/TASK/HANDOFF | LMDO 请求字段和全局/可见集合错配 | 实际客户端/decoder消费同一 fixture；不强制 Pact/OpenAPI |
| named consumer 编辑/验证归属 | 原始 /dashboard/groups 要求未落实到计划 | 不强制改不需要修改的 reader |
| Swift/Python/Rust/Svelte/Java 指引 | 官方 runtime/framework docs 与用户类型 | 只应用实际版本和激活语义，禁止泛化框架改造 |
| 四个 concern（data/async/external/performance） | 可横跨语言的已有 failure/oracle 规则 | 知识可拼装，控制/预算不新增 |
| PLAN reviewer读匹配资料 | 主计划不能成为无人核对的路由结论 | 当前单 pass，no module-count clean streak；主线程仍 admission |
| Audit 记录路由与前移效果 | 后续任务-知识使用评估 | 复用现有 PLAN/REVIEW/成本，无新强制报告、重跑或模型 |
| 修正两项历史归档测试依赖 | 原输入删 baseline，AGENTS 明确不需副本 | 验证真实输入历史哈希，不重建历史副本 |

## 保留项

- 九个运行脚本、基础 section validator、安装器：逐字保留。
- 两份 Skill 都随完整项目交付；`code-review` 全部字节不变，继续原委托协议，不为版本号重开任务。
- 七个 native agent 名称/model/effort/sandbox 不变；仅 plan_reviewer 的 instruction 追加知识路由。其余六份配置逐字保留。
- 原 HEAD 增加的 FINAL_ANSWER + completed 规则保持。
- 所有输入历史文件（包括 v4.2 CSV 工作区修改）保持。
- 业务 section/内部 subsection/模型分配、串行屏障与显式并行、Astra/GLM alternation、repair/recovery/integration预算、外部人工 Advisor、关闭计划后新任务判断不变。
- Audit 默认 LIVE、主/xxx-zas.zip配对、无 SHA 侧文件、运行故障与产品缺陷分离不变。

## 没有做

不改两个被审项目的产品代码；不修改 ZAS MCP；不恢复 workflow.py/execution_artifacts.py/advisor_flow.py；不发明 Java 后端；不新增额外 PLAN/code review 或 runtime route checker；不将资料清单完成度变成新的 acceptance gate。

完整改动和输入保留摘要见 RETENTION.json；没有 previous-version baseline 副本。
