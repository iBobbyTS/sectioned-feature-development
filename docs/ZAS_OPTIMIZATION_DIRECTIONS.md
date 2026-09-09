# ZAS 受控测试优化方向：公开行为可观测性与生命周期

**给ZAS开发Codex执行的合同。** 依据用户上传的2026-09-07 13:22源码工作区；HEAD为`4e011ae`，包含未提交诊断与恢复修改。不是全面重写，不假定本文件的接口已经实现。配套Sectioned4.3通过能力协商启用增强路径。

## 1. 保持不变的边界

ZAS继续是跨harness的通用subagent中间层：MCP facade → 单daemon/Store → driver → 官方ZCode。不得把Sectioned的PLAN、review admission、模型路由、Git分支、worktree管理塞进ZAS。

不新增monitor LLM、第二daemon、全局行为评估引擎、文本相似度loop detector、永久审计平台或任意内部工具代理。MCP只查询已发生的公开行为事实，不向Codex暴露可调用的ZCode read/edit/bash句柄。没有被runtime公开提供的内容，保持不可见，禁止提取隐藏推理。

## 2. 当前已完成，不要重复开发

- `PassiveActivitySnapshot/Window`已有liveness、model请求/delta时钟、text tail和read/bash/tool计数。
- 当前dirty源码已将`runtime_command_failed`与socket层`daemon_unavailable`区分，保留WORKSPACE_BUSY和MESSAGE_ID_CONFLICT。
- 分Agent runtime失败记录已保留stage、operation、remote_code/message、stderr tail、cleanup_result。
- 已有单writer有界diagnostic sink、轮转、drop计数与16KiB输出约束。
- 已有`diagnose --agent ... --output ...`，不创建替代的全局日志系统。
- send是队列；terminal resume在已测试的app-server路径不可用。不要把closed=false或旧COMPLETED结果当成resume成功。

## 3. 本轮必须补齐的事实通道

### P0-A：沿现有事件流保存有界 observation window

在现有runtime event decoder/Store/diagnostic通道上增加一份每Agent的有界公开观察窗口。优先复用已有持久Store事件序列，不做重复全量journal。

| 事实 | 最小字段 | 作用 |
|---|---|---|
| 生命周期 | service_generation、agent_id、已有session/turn ID、stage、start/end、monotonic duration | 区分任务恢复、服务重启和新任务 |
| 模型请求 | request ID（实际存在时）、开始/结束、requested/observed model、delta时钟、真实usage | 长推理和等待，不从字数估算token |
| 工具调用 | tool_call_id、tool_name、start/end/status、safe semantic summary | 识别有效动作、失败重试和空操作 |
| 文件读取 | workspace-relative path、start_line/count或byte range、实际捕获的version/hash | 区分同片段反复读与文件变更后的合法重读 |
| 命令 | 脱敏command preview、cwd相对路径、exit/timeout/cancel、有限结果类别或摘要 | 看见`true/echo`等动作与是否获得新事实，而不是只知道bash次数 |
| 工作流输出 | runtime-public assistant progress、完成声明、artifact/check引用 | 可供主Agent判断是否收敛；声明本身不证明正确 |
| 公开推理 | 明确由runtime公开给用户的reasoning excerpt/summary，带source/visibility | 作为犹豫/反复计划的辅助证据，不作为唯一停止依据 |
| 观测质量 | first/last seq、stream ID、missing/loss/redaction/truncation | 明确“没有证据”和“没有发生”不同 |

读取版本/哈希只能来自已经捕获的read结果或已有snapshot，不额外扫描整个workspace。缺失写unknown/null。不能为了判断空转额外运行被观察的命令。

对传输层重复的同source event ID去重；不要按内容去重，否则真实的重复`read/true`行为会消失。不要逐token写盘：按模型请求和时间/字节上限合并公开文本，保留起止seq、事件次数、truncated标志。

存储可设每Agent与全局两个容量上限，旧窗口淘汰后必须有gap。诊断backpressure不得阻塞cancel/reap/final outcome。沿用已有sink/drop机制，不因为日志不可用就中止健康任务。

### P0-B：一个只读MCP观察接口 + 同语义CLI

**新增工具建议：`zcode_subagent_observe`。目前源码不存在。** 原9个工具保持；轻量poll不变成巨大日志响应。

建议status增加：

```json
{
  "capabilities": {
    "observation": {
      "protocol": "zas-observation/1",
      "metadata": true,
      "public_content": true,
      "max_events": 100,
      "max_bytes": 65536
    }
  }
}
```

`public_content=true`仅在该runtime版本的公开事件来源已确认且通道真的实现时声明，不表示每次任务都已授权收集。

建议spawn增加可选`observation_mode: metadata | public_content`，默认metadata。`public_content`由用户/调用方显式授权，读取时的detail不能提高创建时的采集级别。来源不明/private/opaque reasoning不收集，明确标记unsupported。

输入：

```json
{
  "agent_id": "agent-id",
  "after_seq": 120,
  "stream_id": "stream-epoch",
  "limit": 50,
  "max_bytes": 16384,
  "detail": "metadata"
}
```

只按明确agent_id读取。`after_seq`为exclusive。`next_seq`是服务端消费的最大原始seq，不必等于最后一条返回事件（过滤/脱敏也可能推进游标）。

输出示例：

```json
{
  "schema": "zas-observation/1",
  "agent_id": "agent-id",
  "stream_id": "stream-epoch",
  "first_available_seq": 100,
  "next_seq": 122,
  "has_more": false,
  "gap": {"present": false, "reason": null},
  "loss": {"dropped_events": 0, "redacted_fields": 0, "truncated_events": 0},
  "events": [
    {
      "seq": 121,
      "kind": "tool_started",
      "visibility": "metadata",
      "source": "runtime.session_event",
      "source_event_id": "event-id",
      "turn_id": "turn-id",
      "tool_call_id": "tool-id",
      "summary": {
        "tool_name": "read",
        "path": "src/example.rs",
        "start_line": 40,
        "line_count": 60,
        "observed_version": null
      }
    }
  ]
}
```

调用方带旧stream_id时，重启/保留窗口变化必须返回明确gap/reset信息；不能用空events冒充“这段时间什么也没做”。未知事件类型保留事实与有限summary，不当成fatal protocol错误。

公开文本使用`visibility=runtime_public`和`content`，且必须由收集授权与runtime来源共同控制；metadata返回不带content。脱敏policy对路径、token、cookie、命令参数同样生效。错误或敏感原始stderr不默认进入observation。

CLI与MCP共用同一daemon命令/类型：

```text
zcode-as-subagent observe --json '<同一input object>'
```

这条是新增建议，不是当前可调用命令。可沿用现有CLI读取stdin JSON的形态，最终以实际parser为准。

JSON Schema草案：`docs/contracts/zas-observation-v1.schema.json`。应用层schema独立于MCP协议版本；不要求为了此扩展升级整套MCP transport。

### P0-C：结构化错误与部署身份

现有错误分类已经改善，下一步是暴露结构化而不是再做一次分类器。保留兼容的bounded text，同时为工具执行失败提供`isError=true`与可验证structuredContent/outputSchema：

```json
{
  "error": {
    "code": "RUNTIME_COMMAND_FAILED",
    "component": "runtime",
    "operation": "session_send",
    "retriable": false,
    "request_id": "request-id",
    "agent_id": "agent-id",
    "message": "Bounded public explanation",
    "cleanup": {"state": "REAPED", "error_code": null}
  }
}
```

不要将cleanup失败覆盖第一原因；对socket unavailable、daemon busy、runtime rejected、auth/model已确认失败、权限请求、结果校验失败分别记录。只有runtime确实返回认证/模型错误时才填对应code，不能由猜测推断。

status/diagnose增加实际部署daemon/facade build、source revision/dirty/build hash（若能从构建注入）、runtime path/version、service_generation、effective configured model与observed model来源。没有实际模型响应时observed保持unknown。

内部RPC已有session_id/turn_id和result_sha256，建议以稳定可选字段投影到公开MCP，避免调用方误把自己的hash或role alias当成server证明。只扩现有projection，不引入新的session owner。

## 4. 本轮建议暂缓的内容

- terminal resume修复：已经有失败证据，仍可独立研究，但不是观测功能前置条件；不加假continue工具。
- spawn caller correlation/idempotency：有明确改进价值，但可在P0后独立加最小字段/Store映射；现阶段调用方按repository list消歧，不盲重试。
- 全部工具事件无损永久存档、分布式tracing平台、另一套日志安全框架、daemon自动loop判决：不做。
- 按每次poll提高reasoning effort或启动额外monitor model：不做。
- 活跃revision高频返回优化：先测caller polling成本，再选择poll coalesce/compact summary；不能为了省轮询漏掉permissions、terminal或cancel事件。

## 5. 谁来判断“无限循环”

**ZAS提供事实，Codex主Agent用当前任务语义裁决。** 服务端不得把相似度、token数量、重复read次数或两次echo直接转换为自动cancel。

可能形成停滞证据的组合：

- 同一未解决子目标；
- 两个完成的行动/分析循环之间没有新的观测、排除假设、有效结果或状态变化；
- command/read窗口支持确实在重复既有事实；
- 没有合理等待、文件修改、上下文压缩、用户更正或新假设解释；
- runtime-public reasoning持续改口可作为辅助，但不是唯一依据。

合理反例必须保留：分析性review不产生代码也可以推进；重复读取发生在文件变更或新问题后可以有价值；同一个长命令输出很多行不应视为循环；心跳或明确等待可以包含echo；缺工具参数或公开reasoning时只能报告不足可观察。

Caller输出五类：`PROGRESSING / EXPECTED_WAIT / NEEDS_CLARIFICATION / NO_PROGRESS_LOOP / INSUFFICIENT_OBSERVABILITY`。等待时间阈值是检查点，不是定罪线。受控预算停止但证据不足时标记`BUDGET_STOP_UNPROVEN_LOOP`。

确认loop后：保存决定性窗口和判断依据 → cancel → 等待TERMINAL+resources_reaped → result/close → 一次有界纠偏重试或阻塞。不使用send来假装中断当前turn，不跨generation复用无效cursor，不因频繁heartbeat取消既有任务预算。

## 6. 测试与验收

先做deterministic parser/Store/facade/CLI测试，再在隔离真实repo验证。不得因为是beta就要求用户先跑不可控长任务。

### 必须的合约用例

1. 同一source event从两个channel投递不会重复计数；两个不同event ID的相同read必须保留。
2. read path/range/version与实际payload一致；未知version不伪造；命令preview脱敏不丢动作类别。
3. metadata模式不返回公开文本；public_content授权和runtime来源验证缺一不可；private字段不会被别名绕过。
4. 长stream分块/合并保持顺序；分页不重读不漏读；过滤窗口有正确next_seq；UTF-8截断合法。
5. retention、restart、writer queue丢弃显式gap/loss，不返回假完整空窗口。
6. 诊断队列满、磁盘满、单事件超大不阻塞cancel、reap、permission或最终状态；错误不覆盖第一原因。
7. observe和diagnose不调用模型、不执行新工具、不修改workspace，不泄漏其他Agent任务。
8. 当前9工具仍兼容；新capability仅在实现后发布，旧服务不接受新增spawn参数。
9. structuredError覆盖runtime拒绝、socket失联、权限、timeout、cleanup失败，保留稳定code。
10. MCP result hash/session可选投影与实际Store匹配，无字段时调用方正确记录gap。

### 真实beta任务矩阵（人工标注，不声称离线测试能判模型语义）

- 正常进展但无代码改动的review；长分析；长编译；等待权限；真实取消。
- 两个不同命令但没有新信息的空转；同路径同range未变版本反复读；公开犹豫但最终推进；压缩后合理重读；修改后重读。
- daemon/facade断开后重连；runtime rejected；观察窗口丢失；terminal-send rejection。

为每例保存caller判断、支持event range、最终人工标签、是否误取消、是否漏放、额外token/latency、资源是否回收。无法取到精确费用/时长写unknown。通过后再给其他项目启用增强观察。

## 7. 给Codex的执行边界

从本次上传工作树已有diagnose修复继续，不重做日志系统。先确认decoder中哪些字段是runtime确实公开输出；如缺公开reasoning，做metadata链路并明确gap，不能自行逆向隐藏内容。实现P0-A/B/C和对应tests，复用现有Store/diagnostic/lifecycle组件。更新公开schema、generated documentation和CLI；不新增review mode、工具代理或Sectioned业务依赖。完成后提供接口例子、source/build identity与受控实测结果，供Sectioned4.3按能力启用。
