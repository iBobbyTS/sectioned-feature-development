# ZCode Subagent MCP 建议架构

## 1. Codex-facing contract

### General agent

`spawn_agent` 接收任务、repository/worktree、上下文文件、预算和期望 artifact；返回稳定 `agent_id`。Codex不获得 ZCode内部 bash/edit工具。

### Review agent

建议独立工具 `spawn_review`，而不是仅在 prompt里写“请 review”。参数包含：

- `review_kind`: `PLAN_INITIAL | PLAN_SECOND | CODE_INITIAL | CODE_FINAL | CODE_DELTA | INTEGRATION`;
- `base_ref`, `head_ref`;
- `scope_manifest`, `requirements_path`, `plan_path`;
- `finding_ledger_path`;
- `read_only=true`;
- `report_path`;
- `continuation_of`（同一次 review复核）。

返回同一 lifecycle object：`agent_id`, `review_id`, `daemon_id`, `provider`, `status`, `started_at`, `reviewed_head`, `artifact`, `error`.

### Lifecycle tools

- `list_agents`
- `get_agent`
- `send_agent_message`
- `wait_agent`
- `cancel_agent`
- `get_agent_result`
- `get_health`
- `get_capabilities`

## 2. Driver / daemon

- MCP server只负责协议和鉴权；daemon负责排队、持久状态和supervision；driver负责单个ZCode进程/协议适配。
- 每个 agent有稳定ID、工作目录、日志、预算和状态机。
- review使用 disposable worktree或只读索引；允许在隔离环境运行测试，但不允许修改主worktree产品文件。
- daemon crash后可恢复已完成结果和明确标记中断任务，不能把“未知”伪装成失败或clean。
- 健康状态分层：MCP transport、daemon、driver、zcode executable、model auth、agent task。
- protocol/capability version握手；Codex根据能力决定是否可做continuation、structured review或只做generic spawn。
- bounded retry/backoff；orphan cleanup；resource/concurrency limits。
- result schema validation和secret redaction。

## 3. Review continuity

同一个 `review_id` 的 finding澄清和repair verification必须发送给原 `agent_id`；新独立review创建新 `review_id`，并按 Sol→ZCode→Sol 交替。daemon应保留足够上下文，或允许Codex传入compact continuation packet，但不能把它伪装成同一个 reviewer。

## 4. Error taxonomy

`MCP_UNAVAILABLE`, `MCP_PROTOCOL_MISMATCH`, `DAEMON_UNAVAILABLE`, `DAEMON_RESTARTED`, `ZCODE_NOT_FOUND`, `ZCODE_START_FAILED`, `ZCODE_RUNTIME_FAILED`, `MODEL_AUTH_FAILED`, `AGENT_TIMEOUT`, `AGENT_CANCELLED`, `RESULT_INVALID`, `REPO_ACCESS_DENIED`, `WORKTREE_CONFLICT`.

## 5. Security boundary

Codex只能调用高层 agent tools。ZCode内部工具不进入MCP tool catalog。repo路径需allowlist，review默认只读，普通agent的写权限由daemon policy绑定到专用worktree。任何命令/编辑日志只作为内部审计信息，不作为Codex可调用工具。
