# 4.4 验证记录

## 基线与执行范围

- 基于提供的完整 4.3.1 项目生成新副本，不修改上传 ZAS 产品源码、PLAN、Git或运行服务。
- 实际 v3.9 tag：`e21c9a3e525fa7d3da0fb71fc3eeb12cf25c591c`，比较 current-mcp 分支包。
- 主改动是撤除流程调度证据引擎，而不是减少实际开发/审查/测试义务。

## 已执行

| 检查 | 结果 |
|---|---|
| 活动项目 unittest | **89/89 PASS**，最终一次约 17.3 秒 |
| 保留 Skill 工具 unittest | **15/15 PASS**：Advisor 1、Git exclusion 3、session extraction 1、trace 6、audit finalize 4 |
| 合计离线 unittest | **104/104 PASS**，不与旧版数量作质量排名 |
| 两份 Skill Creator quick_validate | PASS |
| 新 PLAN-FULL 模板基础校验 | PASS：2 sections、2 subsections |
| 本次 ZAS PLAN-FULL 基础校验 | PASS：2 sections、2 subsections |
| 活动/当前版本 Markdown 相对链接、anchor、长 reference TOC | PASS |
| 七份 Agent TOML | 解析 PASS，内容 SHA 与输入逐字相同 |
| Advisor 原始请求合同及 scope-control | 保留回归测试 PASS |
| 安装器 dry-run、备份替换、作用域 | inherited installation tests PASS |
| 活动 Python 脚本编译 | PASS |
| 旧三类 scheduler 及 schedule JSON 模板从安装目录移除 | PASS；历史副本保留 |
| ZIP CRC、文件内容、Unix mode | PASS；完整项目 392 个文件，ZAS 交接包 3 个文件，解包安装 dry-run PASS |

一次将全部工具串在一个容器命令运行的验证遇到 180 秒 runner timeout。其已输出步骤与日志保留；之后分别运行各套工具测试，15 项全部通过。未把超时结果冒充成功，也没有跳过测试。

## 测试变更的解释

旧 workflow/receipt/registry 驱动测试验证的正是本次撤除政策，已与精确旧实现归档。保留产品无关的打包安全、配对完整性、安装、委托 review 语义等测试；新增只检查基础结构和 agent-managed 职责是否明确的测试。文字断言不能证明 Agent 实际遵循。

## 未执行与限制

没有实际 Codex 原生 subagent、付费模型、GLM/ZCode/MCP、Cargo、macOS 部署、LaunchAgent、live-agent 或真实数据库操作。输入 ZAS 压缩包不含 .git，因此基线/分支身份来自 rollout，不是对用户当前 checkout 的认证；新 session 必须核对真实状态。

新计划是根据现有源码与用户已确认范围给出的 Advisor 修订，不是产品已实现或 MERGEABLE 证明。因它调整了 section 所属及 ID 实现范围，Prompt 明确安排一次只查变化的 PLAN_DELTA；没有为文件格式或版本升级增加审查。

没有统计实验可证明新流程一定减少多少时间/token、或模型合规率完全不变。后续应同时看阶段遗漏/escaped defects与 process-only成本。确定性归档/安全脚本仍有自己的格式/完整性检查，但不控制写代码、派发、review或验收权限。
