# ZCode MCP 当前能力自动盘点

- 命中 ZCode/GLM/MCP 的文件：256
- 从源码/文档中自动识别的高层工具名（可能包含历史或测试定义）：
  - `review-ledger`：4 次命中
  - `zcode-review-ledger`：2 次命中
  - `zcode_review_message`：2 次命中

## 相关原始行（截断）

```text
ZCode-CLI-TUIµö»µîü.md: zcode有cli/tui吗
ZCode-CLI-TUIµö»µîü.md: 有，但要区分 **官方 ZCode** 和 **社区把 ZCode runtime 包成 CLI/TUI**。
ZCode-CLI-TUIµö»µîü.md: - **ZCode 官方产品本身仍主要是 Desktop/GUI**。我没有找到智谱官方发布的、类似 `claude` / `codex` 那种独立官方 CLI/TUI。
ZCode-CLI-TUIµö»µîü.md: - 但 **ZCode Desktop 内部其实自带了一套 agent runtime**，社区已经有人把它抽出来，做成真正可用的 CLI/TUI。最值得注意的是 `kingsword09/zcode-cli`：它直接提取 ZCode Desktop 里的官方 `resources/glm` runtime，然后补一个本地 TUI adapter。也就是说，**agent 核心、工具、session、plugin、MCP、provider 配置等仍然跑的是 ZCode 自己那套 runtime**，而不是重新写一个“模仿 ZCode 的 agent”。([GitHub](https://github.com/kingsword09/zcode-cli?utm_source=chatgpt.com))
ZCode-CLI-TUIµö»µîü.md: npm install -g zcode-app-cli@latest
ZCode-CLI-TUIµö»µîü.md: zcode
ZCode-CLI-TUIµö»µîü.md: zcode-app-cli launcher
ZCode-CLI-TUIµö»µîü.md: official zcode.cjs runtime
ZCode-CLI-TUIµö»µîü.md: local @zcode/tui adapter
ZCode-CLI-TUIµö»µîü.md: 这个项目最近还在活跃更新，npm 上目前能看到 `3.7.3-10`，而且明确说明是 **Unofficial terminal client for the official agent runtime shipped with ZCode Desktop**。([npm](https://www.npmjs.com/package/zcode-app-cli?utm_source=chatgpt.com))
ZCode-CLI-TUIµö»µîü.md: 另外还有一个 `gaozhi-ustc/zcode-tui`，也是走类似思路，通过 ZCode 的 `app-server`/runtime 提供 TUI，支持 session resume、model、thinking level、plugins 等：
ZCode-CLI-TUIµö»µîü.md: zcode
ZCode-CLI-TUIµö»µîü.md: zcode resume
ZCode-CLI-TUIµö»µîü.md: zcode --resume <sessionId>
ZCode-CLI-TUIµö»µîü.md: 它甚至保留了一个 legacy CLI fallback。([GitHub](https://github.com/gaozhi-ustc/zcode-tui?utm_source=chatgpt.com))
ZCode-CLI-TUIµö»µîü.md: 需要特别排除另一类项目：例如 `KiwiGaze/zcode-cli` 自己明确写了，**它只是一个独立的 GLM terminal coding agent，与 ZCode harness 无关**。这种东西虽然名字叫 zcode-cli，但对你前面想做的「把真正 ZCode harness 当成外部 reviewer」价值不大。([GitHub](https://github.com/KiwiGaze/zcode-cli?utm_source=chatgpt.com))
ZCode-CLI-TUIµö»µîü.md: 如果 `kingsword09/zcode-cli` 这条路线稳定，那么你**不一定需要让 ZCode Desktop 自己暴露 MCP**。可以直接：
ZCode-CLI-TUIµö»µîü.md: └─ external reviewer MCP/plugin
ZCode-CLI-TUIµö»µîü.md: zcode CLI
ZCode-CLI-TUIµö»µîü.md: official ZCode runtime
ZCode-CLI-TUIµö»µîü.md: 我接下来最值得帮你确认的是：**这个 ZCode runtime 有没有真正的 `-p/--print` / JSON / headless 模式，能不能稳定作为 Codex MCP backend 调用，而不是只能操作交互 TUI。** 现在搜索结果里已经能看到其他 ZCode runtime 项目存在 `-p "..." --json` 这种接口，但需要确认 `kingsword09` 这个“最接近官方 runtime”的版本具体暴露了哪些 non-interactive API。([GitHub](https://github.com/zmccyy/ZCode--CLI--agent/blob/main/docs/getting-started/quick-start.md?utm_source=chatgpt.com))
ZCode-CLI-TUIµö»µîü.md: 让GLM工作在另一个Agent里，这个agent供codex调用。之前查到Zcode可以作为类似app server扩展出来，如果能用官方的agent，自然比第三方的更放心。
ZCode-CLI-TUIµö»µîü.md: 1. 这两个Zcode扩展的项目是否适合拿来参考，自己重新做一个MCP，用于把Zcode暴露给Codex，在我目前的sectioned-feature-development里参与Plan Review和Code Review。重点：不是skill本身，是GLM在Zcode里运行的时候不止是要输出一个回答，而是要边审查边记录，最后生成报告，不是传统的禁止写文件的review mode。
ZCode-CLI-TUIµö»µîü.md: 2. 现有的把一个agent作为mcp暴露给另一个agent的项目都是怎么设计的，重点是：不是把这个agent的工具暴露给另一个agent，而是类似subagent的调度策略，codex用这个mcp spawn agent，查看它的进度，可以停止它、steer消息，获取输出，active agent管理等。
ZCode-CLI-TUIµö»µîü.md: 2. 执行报告（让本地agent下载对应的repo，然后写MCP）
ZCode-CLI-TUIµö»µîü.md: I’ll verify both ZCode extensions’ architecture, licensing, and reuse boundaries, then compare subagent-style MCP lifecycle designs and produce an implementation plan for sectioned-feature-development.
ZCode-CLI-TUIµö»µîü.md: Early findings favor `zcode-acp` for typed app-server semantics and a short-RPC design: `spawn` returns an ID, then `status/events/steer/stop/result` manage persistent sessions and file-backed evidence.
ZCode-CLI-TUIµö»µîü.md: The first version should treat steer as queued, not same-turn injection. Keep official ZCode reasoning separate from orchestration, and give reviewers only result/side-channel capabilities.
ZCode-CLI-TUIµö»µîü.md: 结论明确：**可以做，但不应直接把两个 TUI 项目改造成 MCP**。较稳妥的路线是：
ZCode-CLI-TUIµö»µîü.md: > 以 `zcode-acp` 的类型化 app-server driver 为协议基线，以 `zcode-cli` 验证运行时原生调度语义，以 `zcode-tui` 交叉核对会话和事件协议；在其上新建“持久化 daemon + 轻量 Codex MCP + ZCode 内部审查台账 MCP”。
ZCode-CLI-TUIµö»µîü.md: 这样实际执行审查的仍是**本地官方 ZCode Agent runtime + GLM**，自建部分只负责会话生命周期、权限、进度、停止、消息排队和报告持久化。
ZCode-CLI-TUIµö»µîü.md: # ZCode Agent-as-MCP 调研报告
ZCode-CLI-TUIµö»µîü.md: **目标模型：** 在官方 ZCode Agent runtime 内运行的 GLM
ZCode-CLI-TUIµö»µîü.md: | 是否直接 fork `zcode-cli` 做 MCP | **不建议** |
ZCode-CLI-TUIµö»µîü.md: | 是否直接 fork `zcode-tui` 做 MCP | **不建议** |
ZCode-CLI-TUIµö»µîü.md: | 最适合作为协议代码基线的项目 | **`jpalmae/zcode-acp`** |
ZCode-CLI-TUIµö»µîü.md: | 报告写入的推荐方式 | 给 ZCode 注入 job-scoped `review-ledger` MCP，由 daemon 实时渲染 Markdown |
ZCode-CLI-TUIµö»µîü.md: | 商业或团队正式部署 | 在获得 ZCode 接口授权或完成法律评估前，只做条件性采用 |
ZCode-CLI-TUIµö»µîü.md: ZCode 官方定位本身就是面向长时、多步骤软件工程任务优化的 Agent harness，并提供工具权限、模式、MCP 和运行控制能力；但官方文档目前描述的是 **ZCode 消费 MCP 工具**，没有公开描述“把 ZCode 自身作为 MCP Agent 服务暴露”的接口。社区项目使用的 `app-server` 因而应视为私有、未承诺兼容的接口。([ZCode](https://zcode.z.ai/en/docs/welcome))
ZCode-CLI-TUIµö»µîü.md: │ stdio MCP
ZCode-CLI-TUIµö»µîü.md: zcode-review-mcp
ZCode-CLI-TUIµö»µîü.md: zcode-reviewd
ZCode-CLI-TUIµö»µîü.md: │       *-GLM-RAW.md       Official ZCode app-server
ZCode-CLI-TUIµö»µîü.md: │                         Official ZCode Agent + GLM
ZCode-CLI-TUIµö»µîü.md: └────────────── review-ledger MCP ◄┘
ZCode-CLI-TUIµö»µîü.md: - **审查主体：** 官方 ZCode Agent runtime。
ZCode-CLI-TUIµö»µîü.md: - **模型：** ZCode 配置中的 GLM。
ZCode-CLI-TUIµö»µîü.md: - **外部 MCP：** 只给 Codex 提供 Agent 生命周期管理。
ZCode-CLI-TUIµö»µîü.md: - **内部 MCP：** 只给 ZCode 提供受控的审查记录通道。
ZCode-CLI-TUIµö»µîü.md: - **报告：** 由 daemon 持续渲染，不依赖 Agent 最终回答。
ZCode-CLI-TUIµö»µîü.md: ## 2. 三个 ZCode 社区项目的适用性
ZCode-CLI-TUIµö»µîü.md: 虽然用户最初提到的是两个 TUI 扩展，但调研后发现，真正最适合作为实现基线的是第三个项目 `zcode-acp`。
ZCode-CLI-TUIµö»µîü.md: ### 2.1 `kingsword09/zcode-cli`
ZCode-CLI-TUIµö»µîü.md: 官方 zcode.cjs runtime
ZCode-CLI-TUIµö»µîü.md: 本地 @zcode/tui adapter
ZCode-CLI-TUIµö»µîü.md: 其 README 和代码明确区分了 launcher/TUI 与官方 runtime；Agent、session、tool、plugin、MCP、认证和 provider 逻辑仍由 ZCode runtime 执行。它还暴露了非常有价值的原生调度语义：
ZCode-CLI-TUIµö»µîü.md: - 存在 `/tasks message`、`/tasks stop`、`/tasks resume` 等管理操作。([GitHub](https://github.com/kingsword09/zcode-cli))
ZCode-CLI-TUIµö»µîü.md: 1. ZCode runtime 的本地定位与启动。
ZCode-CLI-TUIµö»µîü.md: #### 不适合直接作为 MCP 基线的原因
ZCode-CLI-TUIµö»µîü.md: ### 2.2 `gaozhi-ustc/zcode-tui`
ZCode-CLI-TUIµö»µîü.md: node zcode.cjs app-server
ZCode-CLI-TUIµö»µîü.md: 与 ZCode runtime 交互，并实现或调用了以下会话操作：
ZCode-CLI-TUIµö»µîü.md: 它还处理了模型文本、reasoning、tool lifecycle、turn lifecycle、权限和用户输入等事件。([GitHub](https://github.com/gaozhi-ustc/zcode-tui))
ZCode-CLI-TUIµö»µîü.md: - 没有持久化 daemon、全局 active-agent registry 和可靠重启恢复。
ZCode-CLI-TUIµö»µîü.md: ### 2.3 `jpalmae/zcode-acp`
ZCode-CLI-TUIµö»µîü.md: `zcode-acp` 已经把 ZCode app-server 包装成 ACP adapter，并对协议进行了较完整的类型化建模。其代码覆盖：
ZCode-CLI-TUIµö»µîü.md: - 每个 ACP session 启动一个 `node zcode.cjs app-server`。
ZCode-CLI-TUIµö»µîü.md: - fake app-server 和协议测试。([GitHub](https://github.com/jpalmae/zcode-acp/blob/main/README.md))
ZCode-CLI-TUIµö»µîü.md: 这正是新 MCP 最难、也最容易写错的底层部分：**并发请求、事件顺序、权限请求和长 turn 生命周期不能共用一个阻塞循环。**
ZCode-CLI-TUIµö»µîü.md: `zcode-acp` 是 ACP adapter，不是 Agent 调度平台。它没有完整提供：
ZCode-CLI-TUIµö»µîü.md: - 持久 daemon。
ZCode-CLI-TUIµö»µîü.md: - 跨 MCP 重连的 active-agent registry。
ZCode-CLI-TUIµö»µîü.md: - 对当前 ZCode 版本的持续兼容矩阵。
ZCode-CLI-TUIµö»µîü.md: 项目自身也列出了若干兼容性和实现限制，例如部分 progress tail、session list、setMode、用户输入和 provider header 的处理尚不完整；其验证版本也落后于当前 ZCode 版本，因此必须重新运行兼容性测试。([GitHub](https://github.com/jpalmae/zcode-acp/blob/main/README.md))
ZCode-CLI-TUIµö»µîü.md: > **首选协议和 driver 基线，但必须在其外增加 daemon、MCP control plane、报告台账和安全策略。**
ZCode-CLI-TUIµö»µîü.md: | 多 Agent active registry | 由自建 daemon 实现 |
ZCode-CLI-TUIµö»µîü.md: | 持久化 event log | 由自建 daemon 实现 |
ZCode-CLI-TUIµö»µîü.md: 当前公开的 app-server 方法映射没有出现明确的 `turn/steer` 等价方法。已知 `session/send` 在已有 prompt 运行时可能返回 `PROMPT_ALREADY_RUNNING`，而 `zcode-cli` 的同 turn steering 来自内部 TUI adapter 路径。([GitHub](https://raw.githubusercontent.com/jpalmae/zcode-acp/main/src/zcode/protocol.rs))
ZCode-CLI-TUIµö»µîü.md: 1. daemon 持久化消息。
ZCode-CLI-TUIµö»µîü.md: ## 4. 现有 Agent-as-MCP 项目的设计模式
ZCode-CLI-TUIµö»µîü.md: ### 4.1 `omg.dev`：持久服务 + 轻量 MCP
ZCode-CLI-TUIµö»µîü.md: `omg.dev` 使用本地持久服务管理 session，MCP 只是外部入口；后台会话可以跨连接继续存活，并可从统一界面查看 session、消息和委派关系。([GitHub](https://github.com/BennyKok/omg.dev))
ZCode-CLI-TUIµö»µîü.md: - daemon 是状态所有者。
ZCode-CLI-TUIµö»µîü.md: - MCP server 本身不拥有 Agent 生命周期。
ZCode-CLI-TUIµö»µîü.md: - Codex MCP 重启后，任务继续存在。
ZCode-CLI-TUIµö»µîü.md: - MCP 只负责命令转发和结果序列化。
ZCode-CLI-TUIµö»µîü.md: - 并发超限后进入 `QUEUED`，而不是让 MCP 调用一直阻塞。
ZCode-CLI-TUIµö»µîü.md: 其 MCP conductor 使用了类似：
ZCode-CLI-TUIµö»µîü.md: 并加入 worktree 校验。([GitHub](https://github.com/quazardous/sailing/blob/main/docs/mcp_conductor.md))
ZCode-CLI-TUIµö»µîü.md: ### 4.4 `mcp-supersubagents`：任务句柄和双层输出
ZCode-CLI-TUIµö»µîü.md: 该项目使用后台 task ID、状态资源、message/cancel/answer 操作，并将短结果与大工件分离。([GitHub](https://github.com/yigitkonur/mcp-supersubagents))
ZCode-CLI-TUIµö»µîü.md: - MCP 返回小型摘要和 artifact locator。
ZCode-CLI-TUIµö»µîü.md: - 它使用的 GLM 路径并不等同于官方 ZCode Agent runtime。
ZCode-CLI-TUIµö»µîü.md: ### 4.5 `agent-teams-mcp`：客户端唤醒不是通用能力
ZCode-CLI-TUIµö»µîü.md: 该项目通过 Claude 专用 Stop hook 把 worker 回答重新注入主 Agent，以解决 MCP resource 更新不会自动让主 Agent继续行动的问题。([GitHub](https://github.com/jessepwj/agent-teams-mcp))
ZCode-CLI-TUIµö»µîü.md: 而不是假设 MCP 能主动向 Codex 发起新 turn。
ZCode-CLI-TUIµö»µîü.md: ## 5. 为什么不直接依赖 MCP Tasks 或 progress notification
ZCode-CLI-TUIµö»µîü.md: MCP 已定义异步 Tasks 扩展：工具可以返回 durable task handle，客户端随后轮询状态、处理 `input_required` 并在重连后继续访问。([Model Context Protocol](https://modelcontextprotocol.io/extensions/tasks/overview))
ZCode-CLI-TUIµö»µîü.md: 但截至本次调研，Codex 对 MCP progress notification 的接线仍存在公开缺口：服务端可能发出 progress，而 Codex 没有把它完整呈现到 Agent 层。([GitHub](https://github.com/openai/codex/issues/28003))
ZCode-CLI-TUIµö»µîü.md: 因此首版应采用普通 MCP tools 加显式 job ID：
```
