# ZAS 源码核查：本轮实际工作区

## 身份与范围

- ZAS HEAD：`4e011ae5eaf5e0c46cccf5a36cbb379e181c90be`。
- 采用ZIP内工作树，包含未提交的diagnose/runtime mapping修改；不是只读HEAD版本。
- Skill HEAD：`25d587ae5fe172206d7de40364f18834cfa10edc`，实际4.2.1。
- 两份reviewer TOML的本地文本改动与历史AUDIT_INTAKE.csv原样保留。
- 没有修改、编译或替换ZAS产品源码/原生binary；没有执行macOS/ZCode/GLM真实任务。

## 1. 真实API与旧文档差异

权威：`schema/zcode-subagent-public-api.json`、`crates/zcode-subagent-mcp/src/server.rs`、`crates/zcode-subagent-mcp/src/lib.rs`。

当前9工具为：status/spawn/poll/list/send/respond/cancel/result/close，统一前缀`zcode_subagent_`。旧`zcode_subagent_agent_*`、system_status、review_*不能继续调用。

spawn使用repository/prompt/permission_mode/write_manifest；不是workspace/model/group_id/idempotency_key/named-check/budget合同。当前无caller幂等键，schema明确spawn非幂等。不能照旧description盲目携带参数。

list按repository；poll用after_revision/timeout_ms，最大5000ms。result按offset/limit读取，最大81920bytes；公开outcome为COMPLETED而非旧SUCCEEDED。公开task为resources_reaped而非reaped。Respond只有allow/deny与reason；unsupported_input不得虚构answer响应。

文档schema把list可选字段写成nullable，而实际facade的optional_non_null路径拒绝显式null；4.3采用保守可运行形态：没有值就省略。此差异宜由ZAS后续统一schema与parser，但不增加兼容alias。

## 2. 现有activity的证据边界

`crates/zcode-agentd/src/lib.rs`：

- `PassiveActiveTool`（约99行）只有tool_call_id和kind。
- `PassiveActivityWindow`（约115行）有reasoning/text delta计数/bytes、tool/read/bash计数。
- `PassiveActivitySnapshot`及tracker保存运行时/请求/输出时钟、bounded text tail、latest_progress、active_tools、60秒窗口、telemetry_degraded。
- `parse_activity_message`（约550–575行）：reasoning_delta只设置`ReasoningDelta { bytes }`；text_delta才保留实际文本。
- `parse_tool_activity`（约720–770行）：映射scheduled/started/completed/failed和toolCallId/type，不投影命令参数、read路径或range。

因此调用方现在可以看见“仍然产出token/工具事件”，不能通过MCP看到用户问题中完整的公开reasoning内容、`true/echo a/echo b`命令序列或相同文件片段的多次读取。pending permission可能带summary，但不等价完整工具历史。

计数/尾部窗口主要为当前运行中的内存activity。重启或retention后缺少记录不表示没有动作。不要把统计window当durable observation ledger。

## 3. Poll与终态

`crates/zcode-agentd/src/rpc.rs` 的`task_poll`（约869–933行）：revision取activity revision与durable last_event_seq的max；任何activity revision、pending request或terminal都会提前返回。因此timeout_ms=5000不是“固定每5秒返回”，高delta任务会触发快速响应。Caller需要避免无意义重复poll/重复写全快照；不是停掉持续有进展的任务。

`docs/recovery.md` 保存了app-server cold resume的受控失败证据：ZCode Desktop3.11.2、bundled CLI0.16.5；resume/subscribe成功后session/send仍被runtime拒绝。保留旧completed结果只是可读历史，不能证明新消息执行。对照CLI路径成功不构成自动切换接口的授权。

cancel要求实际停止与回收；close独立标记/清理历史，不删除用户工作。review候选由Sectioned管理，ZAS不提供Git snapshot/branch/patch语义。

## 4. 已经改善的诊断，不重复建议

`crates/zcode-subagent-mcp/src/lib.rs:public_error/public_transport_error`已经将runtime_command_failed与daemon_unavailable分开。WORKSPACE_BUSY、MESSAGE_ID_CONFLICT、protocol_error、timeout、persistence/internal也保留不同prefix。

`crates/zcode-agentd/src/lib.rs:record_runtime_failure`及diagnostic sink已经覆盖第一失败原因与cleanup结果。`cli/main.mjs`已有agent_id/session_id/stage/error_code/message/stderr_tail/operation/remote_code/remote_message/cleanup_result，并对16KiB输出做字段感知截断。`diagnose --agent ... --output ...`是实际存在的有限导出。

仍缺的是统一typed MCP错误对象与部署/correlation字段，而不是错误分类从零开始。建议沿现有代码加projection和bounded observation，不创建第二daemon或新monitor。

## 5. 内部已有但未公开的数据

`TaskView`在RPC层包含session_id/turn_id，PublicTask剔除；RPC result有result_sha256，MCP结果投影未输出。建议作为可选字段保留实际值；没有这些字段时Sectioned不得虚构session或server hash。当前只能对最终文本计算caller-side hash。

## 6. 受控beta结论

当前已适合继续有界真实任务测试的观察起点，但本轮不是新的完整release认证。运行控制、诊断和清理能力已有真实实现；语义空转诊断通道还不足。新增能力应独立发现、独立测试，失败不得被当成业务finding，也不应污染产品repair预算。

具体实施见`docs/ZAS_OPTIMIZATION_DIRECTIONS.md`；只有其中P0能力实际实现并通过schema/capability检查，4.3才会进入ENHANCED_OBSERVATION。
