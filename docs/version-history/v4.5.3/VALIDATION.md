# 4.5.3 验证记录

## 实际运行

- 172 项项目 unittest：分组运行通过，包括新增 18 项明确措辞/目录优先/部分 fallback/保留检查。
- 15 项保留工具 unittest：全部取得实际 OK 结果。
- 合计 187 个不同测试通过；去重测试身份及对应原始日志见 appendix/TEST-RESULTS.json。
- 部分合并运行达到了外层工具时间预算；没有把中断当通过。已完成的测试证据保留，余项单独执行后确认。没有为通过测试改写任何运行脚本。
- 初版两个检查失败分别来自尚未写好的验证文档链接、测试对新措辞/历史 hash 预期未更新；最终项目测试已全部通过，核心顺序/Audit/预算检查没有删减。

## 静态核验

两份 Skill Creator 校验、JSON/TOML/YAML 解析、基础 PLAN 结构检查、当前 Markdown 相对路径与 anchor 检查、四份 catalog 与实际 57 份专用指南一致性、无 universal-first 活动入口、原始文件保留检查已通过。

安装器的临时目录安装/替换/备份/显式退役/符号链接拒绝测试通过；安装器本身未改。

## 验证边界

没有运行真实 Codex/ZAS/GLM 任务或付费模型对照。8 个新组合场景为人工预期 fixture，不是模型行为实测。离线断言不能保证 Agent 一定提交或正确选择全部资料，也不能宣称净 token/时间节省。

本版需要同步主 Skill 与 plan_reviewer.toml，不需要更新 companion code-review 协议；新规则不重开历史 accepted PLAN。

## 包装

完整项目 414 个文件、主 Skill 120 个文件。两个 ZIP 均完成 CRC、逐文件 bytes/hash 和 Unix 权限核对。Git patch 已在 4.5.2 精确副本上 check/apply，并与 4.5.3 工作树逐文件比较。无 .git、.agent-work、__pycache__、.pyc 或新 .sha256 侧文件。
