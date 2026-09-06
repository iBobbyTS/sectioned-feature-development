# 4.0.1 验证记录

## 已执行

- 全部项目单元测试：**43/43 PASS**，其中原 35 项继续通过，新增 8 项配套协议/安装回归。
- 两份 active Skill 的 Skill Creator quick_validate：PASS。
- Python compileall：PASS。
- Active Markdown 路径、heading anchor 和长 reference Contents：PASS（27 个文件）。
- 原 4.0 及更早版本历史文件：103 个保持逐字节不变。
- 原 Sectioned 的两个运行脚本 workflow.py / process_audit.py：逐字节不变。
- 原 advisor 请求合同的 SHA-256 回归：PASS。
- 原八个 agent / 六种 model-effort组合：PASS；astra_high 只更新 delegated 协议指引。

## 安装回归

在临时 CODEX_HOME 中实际执行了安装器：

- 默认 dry-run 不写文件；完整安装同时部署两份 Skill 和八个 agent。
- 同名目标存在且未 --replace 时拒绝覆盖。
- --only code-review 的 dry-run 只列 companion。
- --only code-review --apply --replace 备份旧 code-review 及其本地自定义文件。
- 更新后保留原 Sectioned 4.0、其他 agent、AGENTS.md 和 config.toml。
- symlink target 拒绝替换，不触碰其指向的用户文件。

第一次纳入旧 standalone reference 时，链接测试把其 `{skill path}` 示例占位符当成真实路径；已将占位符与真实链接分开检查。随后移除自动生成 TOC 中误收的 code-block 示例标题，并完成最终测试与 anchor 校验。

## 证据限制

这次验证的是协议文字、文件引用、安装行为与原流程脚本回归，**不是实际 LLM reviewer 的指令遵循实验**。没有调用用户电脑上的 Codex、ZCode 或模型服务；不能声称升级保证了原生会话缓存立即刷新或所有未来 reviewer 自动正确执行。

## 包结构

单独 code-review ZIP 的根目录是 `code-review/`；完整项目 ZIP 的根目录是 `sectioned-feature-development/`。两包均只含文件，不打包 __pycache__、pyc、.DS_Store 或 __MACOSX。

打包后校验 ZIP CRC、逐文件内容及权限、项目 MANIFEST。ZIP SHA-256 位于对应 `.zip.sha256` sidecar（不写入自身归档，避免循环哈希）。

原始测试输出见 [VALIDATION-TESTS.txt](VALIDATION-TESTS.txt)。
