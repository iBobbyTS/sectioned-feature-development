# PLAN-FULL — ZAS MCP 公共协议瘦身与八位递增任务 ID

- Feature: mcp-public-contract-slim-20260909
- Revision: 4.4-new-session-takeover-20260909
- Status: ADVISOR_REVISED，待新会话完成本页指定的有界 PLAN_DELTA 后执行
- Invocation: USER_EXPLICIT；用户已要求实现，不重复例行人工 PLAN 审批。
- Repository: /Users/ibobby/Projects/zcode-mcp
- Evidence base: 34a5012856a01c92c359baaa43caaea75716dc3b（来自当前附件与 rollout；开始时以实际 Git 核对）
- Authorized feature branch: codex/mcp-protocol-slim-20260909
- Execution mode: EXECUTE_WITH_COMMITS
- Requirements: .agent-work/REQUIREMENTS.md；原始用户消息见随附 REQUIREMENTS.md 的来源索引。
- 本计划只授权原公共输出删减和任务 ID 修改，不授权新架构、信任模型、历史数据销毁或额外兼容层。

## 0. 新会话接管，不修旧执行器

仅主 checkout、串行代码写入；遵守本仓 AGENTS，不建立开发 worktree。不要启动任何正在开发的 ZAS 作为 reviewer。

先确认旧会话没有活跃 writer/reviewer；确认实际 branch、HEAD、diff。附件只证明已记录的基线与计划状态，不证明此刻服务和工作区仍未变化。保留全部已有正确代码和用户修改；若当前仍只是计划/状态修改，从 S01 开始。若出现新产品提交，检查其与本合同的关系，只计划未完成部分，不重置、不重放。

旧的 `.agent-work/evidence/plan-draft.md` 及其 APPROVED 回执属于 `mcp-single-service-lifecycle-20260908`，不得作为本功能的计划或验收。当前功能的 PLAN review 原文及 P1–P4 disposition 保留。旧 STATE.json 不再参与调度，不需要重建 actor/receipt/hash 数据。

本修订把 S03 的契约与测试分别归回 S01/S02，把 release/live check 归最终集成；并允许在唯一分配器和边界上改 ID，而不是预先强制全库 String/TEXT→INTEGER。新会话只需一位独立 [@plan_reviewer](subagent://plan_reviewer) 对这些变化及受影响依赖做一次 PLAN_DELTA。不是新的 full discovery；不得为了 private helper、文件名或 JSON 调度格式继续审 R2/R3。普通文字修正由主线程 admission。

## 1. 原始业务目标与权威

1. 删除下表中的重复 MCP 公共字段，减少调用上下文。内部诊断、准备完整性、Store/RPC 私有字段不因公开输出删减而删除。
2. 去掉原任务 ID 的前缀与长随机字符串，公开为 10000000–99999999 的 JSON integer，按持久分配次序递增，不是随机八位数或数字字符串。
3. 调用方、文档和 daemon 同步更新，不做旧公共契约的兼容 alias、双响应或旧客户端探测。
4. 原生 reviewer 保持原角色；本来分配给 ZAS/GLM 的 review slot 改为 [@sol_xhigh](subagent://sol_xhigh)。实现仍使用本计划固定 impl 角色，不把所有工作改为 sol_xhigh。
5. 最终做一次受控真实 MCP/ZCode 生命周期验收；开发中不以修改中的服务进行 reviewer 调用。

## 2. 精确公共删减与保留边界

路径相对于对应工具的公共返回体；先核对当前真实 schema/DTO 的嵌套。把用户原文中的 tasks/task 命名差异解释为“每个实际公共 task projection”，不是新增返回结构。

| 工具/表面 | 本轮移除 | 保留，不顺带瘦身 |
|---|---|---|
| status | api_surface、protocol_version、service_generation；capabilities.observation.protocol、runtime_source_verified；已列 daemon/facade build/version/source/artifact/capture identity、runtime identity、observed-response model identity | components、frame limits、max_wait_ms、maturity、observation 3/5/200 defaults、public_reasoning_default；未列且有业务用途字段 |
| poll | 每个 task.input_identity.caller_prompt_sha256；activity 的 reasoning_delta_bytes/text_delta_bytes | revision/next_revision、事件次数、时间、phase/outcome、pending requests、result_available、resources_reaped 与其他有用活动字段 |
| observe | schema、echoed agent_id、service_generation、count_scope、reasoning.char_count、reasoning.source；沿用已审 PLAN 的 current-snapshot 精简决定，移除 snapshot_seq | top 3 工具各最近 5 次调用（不带结果）、reasoning.text 最新 200 Unicode 字符、truncated、coverage 与调用内部 seq/ID |
| list/cancel/result/close，及其他复用 task 投影的公共响应 | task.input_identity.caller_prompt_sha256；若对象删后确为空，可一并删空壳 | workspace/permission identity、任务状态、pagination、cleanup/reap 结果和未列字段 |
| 所有输入/输出中表示 ZAS task ID 的位置 | 长随机/带前缀的公开 task ID 表示 | 字段名不改；改为同一八位 JSON integer，包括列表、状态、错误和 WORKSPACE_BUSY 等关联 task ID |

若 `identity` 是单纯由上述全部删除项组成的壳，删壳；不要凭“省 token”删除不在范围内的 component health、错误分类或私有 RPC version。

原 PLAN 额外删 snapshot_seq 的依据来自已审 current-snapshot 设计，不宣称它是用户逐字列出的字段。内部 sequence 与事件去重仍保留；客户端不比较跨 daemon generation 的 snapshot 顺序。

公开不重复发送 reasoning 来源，不等于取消内部已验证的精确 runtime selector、encrypted_content 排除、有界脱敏或 coverage。status 不回显 build 身份，不等于删除 `zas diagnose` 的运维证据。

## 3. 关键设计限制与不变量

- 复用现有 public DTO/schema/handler 和 Store/task submission owner，不增加新的通用 projection registry、IDL、双协议路由或安全框架。
- **八位任务编号的唯一分配权在持久 Store 创建路径。** 使用现有事务/锁边界实现递增与并发唯一性。确切表/私有函数名由实现者决定。
- 内部 TEXT 主外键、Rust String 可以继续存储该同一数字 ID 的十进制表示；这不是随机旧 ID 到新 ID 的别名映射。不要为 JSON integer 目标先重写所有 task/event/message/session 字段类型。
- 如果当前约束使局部边界实现确实不安全，先给出具体源码证据与最小必要变更，再按现有 bounded owner 决策处理；不默默改成全库大迁移。
- 成功分配的 ID 在同一持久任务数据库内单调增加，不回收已分配编号；重启后不能退回起点。失败/事务回滚是否留空号不作新保证；不要求并发响应返回顺序也排序。
- 起始 10000000，最大 99999999，耗尽时显式失败，不回绕、不随机重试。只对公共 task ID 校验类型/范围；request_id、message_id、ZCode session/turn/runtime IDs 保持现有身份语义。
- 不维护旧公共 ID 格式兼容，也**不自动删除用户活动数据库**。开发/自动测试用隔离 fresh DB；若部署确需 reset，说明受影响数据并只请求这一项授权。
- 保留 workspace collision、message 幂等性、pending-request 关联、restart recovery、result 分页、cancel/reap/close 和 first-failure vs cleanup。
- 保留项目现有安全/权限边界；不增加“ID 可猜测”威胁模型或 capability tokens。

## 4. 分段、模型与调度

| 业务 section | 子项 | 结果 | 计划实现者 | 依赖/并行 |
|---|---|---|---|---|
| S01 | 无 | 精简公共响应，schema/直接调用方/文档同步 | impl_std | 无；串行 |
| S02 | A | 唯一持久递增分配路径 | impl_large | S01；子项串行 |
| S02 | B | 所有公共 task ID 输入/输出、CLI/调用方闭环 | impl_std | S02.A |
| S02 父级 | reconciliation/repair | 数字 ID 的完整业务验收 | impl_large | 所有子项完成 |

本仓不允许开发 worktrees/并行写入，因此这里所有单元串行。模型分配在此固定；不依据执行时价格或文件数量另选。两个 section 均为 TWO，仍只一个 primary pass 加必要 fresh final，不为每个子项加 final/budget。

逻辑 full-review slots 仍按 feature-wide 原生/GLM 序列计数，但本轮 GLM slot 使用用户指定 [@sol_xhigh](subagent://sol_xhigh) 代替。checkpoint、repair delta、基础设施重试不推进 full slot。真实 ZAS 调用只在最终验收。

## S01 — 公共响应精简的完整交付
- Implementer: [@impl_std](subagent://impl_std)
- Depends on: none

### Outcome / authority

实现第 2 节精确字段删减；`tools/list` output schema、实际 `tools/call` response、共享公共 task projection、Node/插件/文档消费者同时一致。本节不改变 ID 生成或类型。

### Owner / scope

主要修改 `crates/zcode-agentd/src/mcp.rs` 的公共 DTO/投影/schema；`rpc.rs` 只做实际公共边界必要调整。同步 `schema/zcode-subagent-public-api.json`、`schema/zas-observation-v1.1.schema.json`、实际 CLI/插件消费者、对应 focused tests 与 docs。内部 preparation digest、identity/diagnose、RPC version 不作删除目标。

### Model basis

现有同类 DTO/schema 与 projection 范例充分；跨几个公共表面但不涉及新状态机。impl_std 负责一次完整映射，避免低级别局部删字段漏掉实际输出/生成契约。

### Acceptance / checks

- 精确列举删除字段，分别在 schema 和真实 handler 输出断言缺席；保留字段有正向断言。
- 同一公共 task 对象不能在 poll 已精简，却在 list/cancel/result/close/error 继续泄漏原字段。
- 内部 prompt integrity、diagnose 和 lifecycle tests 不退化；observe 仍 3/5/200、无工具结果、无 encrypted_content。
- 更新实际消费这些被删除字段的测试/调用方，而非删测试来隐藏失败；不新建泛用合同生成框架。
- 在 repo 中复用现有 Rust MCP/observation/contract 与 Node tests，先 targeted，候选稳定后 section/package 检查；既有 `npm run check`。
- 接受中间态：公共字段已瘦身，task ID 暂仍原表示；只在 feature branch，不发布中间态。

### Review

BOUNDED，TWO。冻结 candidate 后审完整 S01 diff 与直接影响范围；只修本 diff 引入的问题。HANDOFF 包括删/留字段表的实际实现位置和检查证据。

## S02 — 持久八位递增 task ID 与公共生命周期
- Implementer: [@impl_large](subagent://impl_large)
- Depends on: S01

### Parent outcome / scope

在同一个任务身份下实现持久递增分配与 JSON integer 公共表示，贯通 spawn/status/poll/observe/send/respond/cancel/result/list/close、错误关联及 CLI；ZCode runtime/session/message IDs 不变。保留所有工作区、队列、权限和资源回收关系。

主要 owner 为 `crates/zcode-agent-store/src/lib.rs` 的提交事务、`crates/zcode-agentd/src/rpc.rs` 的创建路径、`mcp.rs` 的公共转换及 CLI/schema 直接消费者。Preparation/runtime 仅调整真实 task ID 传递所需路径，不另起架构重构。

父级 HIGH_RISK / TWO；所有子项共享父级 repair lineage。S02 未 accepted 前，不把任何子项当成外部可发布合同。

### S02.A — 唯一持久分配与任务创建
- Implementer: [@impl_large](subagent://impl_large)
- Depends on: none

- 在实际 submission transaction/Store owner 上实现唯一递增源，范围固定；复用现有 SQLite 并发和 workspace fencing。
- 不从可删除 rows 的 MAX 推断可安全复用 ID；无需泛用租约/跨库编号服务。
- 可保留 TEXT/十进制内部键，移除生产随机 task ID 生成路径；旧随机 public ID compatibility 不新增。
- Tests：第一值和边界、并发提交不撞号、reopen 同 DB 后继续递增、耗尽明确失败、workspace conflict/失败路径不破坏关联。不要为耗尽测试创建九千万条记录，直接用 bounded fixture 设置边界。
- 中间态：分配/存储正确，现有字符串投影仍能承载数字文本；未完成 JSON integer 公共合同，不发布。
- 模型依据：原子提交、分配持久性、失败路径和关联需要共同推理，由 impl_large 保持一个 owner。
- SUBSECTION_DELTA checkpoint 仅验证这个增量和父级不变量，不单独 final/accept。

### S02.B — 公共数字表示与消费者闭环
- Implementer: [@impl_std](subagent://impl_std)
- Depends on: S02.A

- 在公共边界使用同一小型转换/校验路径，将任务 ID 返回为 JSON integer，并让接收 task ID 的 MCP 参数使用 integer/range schema。
- Node CLI 的文本 argv 转为明确有效整数再发送；不要将它与 JSON 字符串兼容层混淆。更新直接调用方/插件说明和示例。
- task ID 的 nested/error/list/pending context 全部一致；其他 request/message/session/turn identity 不变。避免多个分散 validator 漂移。
- Tests：所有 task-ID 入口/投影 roundtrip；bool/fraction/out-of-range/wrong type 拒绝；invalid/not-found 区分沿用现有边界；workspace conflict 的 active agent ID 同类型；result 分页、permission correlation、cancel/close 等不退化。
- 模型依据：分配规则已由 A 固定，现有边界转换/消费者范例可复用；impl_std 负责完整传播。
- 完成后运行 parent reconciliation：从 create 到 query/send/respond/result/cancel/reap/close 的同一任务身份闭环与重启不回退；随后父级 fresh final。

## 5. 最终集成、真实验收和停止条件（不是 S03）

1. 所有 parent accepted 后，核对合并后的真实 product/test HEAD。只对尚未证明的跨 owner 路径安排 integration review；空列表不增加 reviewer。
2. 运行当前 repository-required deterministic gates，保留真实命令/退出码/输出。优先按 crate/测试范围组织 targeted → stable package → final；相同输入环境的成功证据可复用。
3. 按现有 AGENTS，Cargo 编译前执行 `cargo clean`，除非用户另行明确允许保留 cache。本计划不擅自改变该全局要求；它不是新增 Skill gate。
4. Release 构建只针对最终候选一次；按 AGENTS 校验 source/release/distributed daemon payload、0755、codesign、LaunchAgent 实际路径与当前日志时间。不要拿旧 binary 或旧 error log 作为新结果。
5. 重启会影响已有任务：先确认无无关活动任务，遇到需清库/停用户任务时仅请求该授权。不自动删除持久数据。
6. 使用现有 live-agent 规程，在受控 fixture workspace 做实际 MCP/ZCode `spawn → poll → result → close`，验证八位整数 roundtrip、精简输出、最终结果和 resources_reaped；沿用直接相关的 cancel/restart 检查，无需重跑整个历史评估矩阵。
7. 若 tests/live-agent 文件在实际 checkout 缺失，报告具体缺失来源；不从附件中不存在的脚本推断它已可运行，也不为此创建新的通用 runner。
8. 保存失败和环境阻塞，不把 offline fixtures 写成 live PASS。真实运行不可用时报告 INSUFFICIENT_EVIDENCE，不能编造或无限 probe。
9. 完成代码和必需证据后关闭本计划，不 merge main、不 push、不删除分支/工作树。Audit 使用同一个 feature 的实际证据，主包 `xxx.zip` 与真实 ZAS attempt 的 `xxx-zas.zip` 配对，不输出 SHA256 文件。

## 6. 明确不做

- 不修旧 Skill 的 JSON 调度块、STATE.json、approve/register/ready 收据或历史 evidence。
- 不重开“单 daemon”已完成 feature，不沿用其 APPROVED 来证明本次协议。
- 不增加 auth、ID 难猜保证、旧客户端支持、老 ID 别名、数据库双写、通用 migration 框架或任务恢复承诺。
- 不把 PRIVATE implementation spelling、命令别名、测试输出文件名变成 PLAN blocker。
- 不把 schema/docs/tests/release 另算证据专用 section；它们随实际业务变更或最终 gate 完成。
