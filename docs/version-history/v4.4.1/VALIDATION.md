# 4.4.1 验证记录

## 已执行

| 检查 | 结果 |
|---|---|
| 项目 unittest | **104 passed**（原 89 项 + 本轮 15 项） |
| 保留的 Skill 工具 unittest | **15 passed** |
| 总计 | **119 passed** |
| 基础 PLAN 结构 | 2 sections / 2 subsections，PASS |
| 两份 Skill frontmatter、name/description/长度 | PASS |
| 当前 Markdown 相对链接、anchor、长 reference 目录 | PASS |
| 七份 Agent TOML | PASS；name/model/effort/sandbox 与基线相同 |
| 安装 dry-run | PASS；临时目录中的实际安装/替换/备份由原测试覆盖 |
| 历史与非目标政策文件 hash 对比 | PASS |
| 全部 9 份运行脚本、原工具测试、安装器 hash 对比 | **逐字不变** |
| 发行 ZIP | 399 files；完成 CRC、逐文件内容及 Unix mode 校验 |

## 本轮新增检查的真实含义

新增 15 项是指令/配置连线、协议片段、保留项和版本检查。它们确保同一包的根 Skill、角色 description/developer 指令、任务/审查模板没有丢掉或矛盾地表达本轮要求，且没有复活旧调度器。

它们不是一个新的 runtime 执行状态机，也不安装到产品任务的派发步骤。首轮新增静态断言有一项使用了 `never` 而正文为等义的 `not`；已修正断言与正文对应，再完整运行上述测试通过，没有因此修改产品语义或删掉测试。

## 未执行、不能声称

- 未运行真实 Codex native subagent、ZCode/GLM、ZAS MCP 或付费模型。
- 未证明模型永不提早派发、永不混淆身份；仍需下一批真实日志观察。
- 未修改 ZAS 源码、全局 config、用户 AGENTS.md、现有项目 PLAN 或 Git 历史。
- 本轮没有新的原始违规 rollout；不能计算发生率或把已批准隔离并行误报为违规。

## 交付安全

完整项目不含本轮缓存、`.git` 或 `.agent-work`。没有创建 SHA256 侧文件；内部 BASELINE.json 只用于发行保留检查，不是执行权限证明。旧版本历史逐字保留；不要求迁移旧状态或重新审查已接受 section。
