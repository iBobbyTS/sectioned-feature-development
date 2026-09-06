# 来源与证据边界

本轮是已上传协议之间的兼容修复，没有引入外部新研究、最新模型断言或新 MCP 能力。

## 原始来源

1. `code-review.zip`：SKILL.md、section-review-protocol.md、review-loop-protocol.md、ledger-templates.md，作为用户当前安装行为的文本依据。
2. 原 4.0 项目：active `references/reviews.md`、`assets/REVIEW-PACKET.template.md`、`references/zcode.md`、`agents/astra_high.toml`、`scripts/install.py` 和原测试。
3. 附件 `skill-creator.zip`：渐进式 reference、Skill metadata 与 openai.yaml 生成校验。

以上是直接文件证据，不是由历史会话总结反推。用户机器上的实际 dispatch、权限、模型可用性和旧会话已加载的缓存尚未实测。

## 修复推断

单纯在 Sectioned 中写“忽略旧 code-review”会保留互相矛盾的独立文档。正确的最小修复是在 code-review 首先确定执行上下文，将旧 standalone acceptance/loop 与 delegated single-pass 分开，并把真正的 companion 纳入安装目标。

新 delegated 文档采用 4.0 已有三种 signal 与候选分类，不引入第二套 admission 状态机、机器 gate 或 reviewer。离线测试验证文件/协议连线和真实临时安装行为，不能证明 LLM 执行一定遵循它。
