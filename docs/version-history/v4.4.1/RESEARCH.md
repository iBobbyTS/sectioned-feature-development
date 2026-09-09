# 4.4.1 依据与不确定性

本轮是基于已提供 4.4 源文件的定点合同修订，未新增外部研究或供应商能力假设。

## 使用的依据

- 用户确认的问题：PLAN 尚未返回时派实现、串行 section 未审完就派后继、将 ZAS 当 native code_reviewer。
- 4.4 根 Skill、activation/artifact/parallel/bounded-review/provider references，以及现有 Agent TOML、TASK/REVIEW/STATE 模板。
- 4.4 已经明确的轻量原则：Agent 调度，只有 section 结构需要日常脚本检查；普通计划修正不要求最新 hash 的 reviewer APPROVED。

## 设计选择

- 使用明确的 wait/read/admit/dispatch 顺序，避免“先启动再检查”与 speculative scaffold；短交接记录复用现有文件。
- native 角色名绑定 native 工具路径，ZAS 直接由主线程走 MCP。共享 review 方法不共享执行身份；实际 route/tool 返回 ID 比角色或模型自述可靠。
- 对应 false-positive：预先明确批准的独立父 section 跨工作树重叠合法。不同文件或未写 dependency 不足以证明批准。
- 失败处理保留原始报告、partial work 和预算，纠正受影响范围，不制造重复 full review 或重新规划。

## 未验证

没有实际启动 Codex、ZCode、GLM、MCP 服务或付费模型。离线测试只能保证本包内部指令、配置、安装和保留项一致，不能保证模型始终遵守，更不能认证第三方提供的模型身份。
