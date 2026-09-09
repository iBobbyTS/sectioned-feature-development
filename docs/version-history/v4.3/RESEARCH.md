# 4.3 Research：事实、推断与外部资料

核查日期：2026-09-07。用户指定源码是本轮主要权威，外部资料只校准设计原则，不能覆盖实际ZAS协议。

## 证据分级

| 来源 | 支持的结论 | 可信度/限制 |
|---|---|---|
| 上传ZAS工作树与公共schema/facade/RPC/parser | 当前工具、参数、liveness字段、错误映射、terminal限制 | 对该工作树直接事实；不证明部署binary一致 |
| 上传Skill4.2.1与真实v3.9 Advisor文件 | 已有计划/委派/预算、删除plan_writer、本次回退边界 | 直接事实；本轮只恢复Advisor，不回退其他4.x功能 |
| ZAS diagnose/schema Node fixtures | 部分公开投影和诊断在本地fixture通过 | 不证明官方macOSruntime/model调用 |
| 用户报告GLM可能无限循环 | 需要可诊断的failure mode | 用户观察线索；本轮没有可直接复现的该incident轨迹 |
| 官方MCP tools规范 | 发现实际工具、typed output、tool执行错误与transport错误分开 | 一手文档；不是要求ZAS升级全部2026-07-28 transport |
| ZCode官方hooks/subagents | 可有native permission/hooks及可定制subagent行为 | 不证明本部署已启用hook，更不证明plan=强只读 |

## 外部资料（实际读取）

1. [MCP Tools — 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
   - `tools/list`暴露实际tool schema，不能只凭旧说明调用。
   - `outputSchema`与`structuredContent`可让客户端验证工具结果；这不是模型结构化输出的正确性证明。
   - transport/protocol错误与tool execution errors有不同语义。
   - 显式state handle适合跨调用关联；协议自身不替应用定义Agent生命周期。
   - 设计映射：保留agent_id；新observe独立只读tool；结构化component错误；不暴露原始ZCode工具。
2. [ZCode Hooks](https://zcode.z.ai/en/docs/hooks)
   - 官方提供工具前后及完成阶段hook能力。
   - 设计映射：仅在实际启用、来源明确时使用已有事件，不额外强制创建第二套权限系统；当前源码的opt-in行为优先。
3. [ZCode Subagents](https://zcode.z.ai/en/docs/subagents)
   - 官方有不同subagent权限/上下文配置。
   - 设计映射：配置与实际运行结果必须分开记录，不能用模式名称代替snapshot不变或独立身份的证据。

## 本轮自主设计，尚待真实测试

- `zas-observation/1`是本轮建议，不是现成ZAS协议。
- runtime-public reasoning仅在来源已证实且任务显式授权时收集。不存在公开内容时保留metadata与gap，禁止通过内部/private字段还原。
- 每次不进展诊断读取一次有界窗口，主Agent用任务、假设变化和实际效果分类；不增加monitor LLM或字符串相似度判决。
- “两次等价行动循环”“review阶段约5分钟观察检查点”是保守beta观察策略，不是超时/停滞的普适阈值；允许长分析、等待和合理重读，并记录误报数据。
- 默认50events/16KiB、上限100events/64KiB是初始容量提案，后续按实际延迟/截断/成本校准，不宣称已经benchmark。
- 模型分级沿用已有策略，未新增各模型能力比较；本轮只是改名并把选级冻结到PLAN。

## 明确不做

不增新的review轮数、不改feature-wide Astra/GLM轮换、不逐条poll做语义review、不以ZAS的runtime outcome替代CLEAN、不把日志gap当代码缺陷、不将Advisor调用或观测依赖Audit开关、不恢复旧MCP alias、不修改ZAS源码或binary。
