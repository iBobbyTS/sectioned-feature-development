# 4.5.3 保留核验

以实际 4.5.2 项目 ZIP 为基线。原有 392 个文件全部保留，没有删除；新增 concern 目录索引及本次文档/测试，不复制旧 baseline。

- 九份运行脚本、原有工具测试、安装器：逐字不变。
- 完整 code-review（含委托协议）：逐字不变。
- 七份 Agent：name/model/effort/sandbox/description 不变；仅 plan_reviewer 的参考选择 developer instructions 更新，另六份逐字不变。
- domain/language/framework/runtime/platform 53 份技术指南及四份 concern：逐字不变；universal 的原有方法正文逐字保留，只改变标题和何时读取的入口说明。
- 4.5.2 根 Audit handoff 段、完整 audit-mode、ZAS audit、Advisor、预算和终态工具语义：保留。少数运行语句用明确名称替代位置指代。
- 所有已存在 docs/version-history 文件（包含历史 CSV）：逐字不变。
- 不新增运行 gate/JSON 调度/receipt/approval-hash。新增测试只在维护验证中运行。

完整输入哈希见 appendix/INPUT-HASHES.json，明确化清单见 WORDING_REVIEW.md。原历史测试的 current-version/default-reading 预期按本次授权更新；历史 fixture 作为历史案例保留，不伪装成当前读取顺序。
