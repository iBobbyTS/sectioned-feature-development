# 4.3.1 验证记录

## 执行范围与结果

**SFD 166 项 unittest 通过**：项目151项、保留工具15项；此外原 `section_plan.py` 独立断言通过。ZAS执行包的合成契约reference另有12项测试通过，单独计数，不计作真实MCP/runtime测试。

项目按模块完成验证：

| 模块 | 测试数 | 结果 |
|---|---:|---|
| test_audit | 13 | PASS |
| test_project | 6 | PASS |
| test_restored_artifacts | 29 | PASS |
| test_review_compatibility | 8 | PASS |
| test_subsections | 26 | PASS |
| test_v43_execution | 19 | PASS |
| test_v43_zas（更新为4.3.1观察契约） | 20 | PASS |
| test_workflow | 18 | PASS |
| test_v431_audit_pair | 12 | PASS |
| 工具test_advisor_pack | 1 | PASS |
| 工具test_audit_finalize | 4 | PASS |
| 工具test_audit_trace | 6 | PASS |
| 工具test_ensure_agent_work_untracked | 3 | PASS |
| 工具test_session_evidence | 1 | PASS |

一次全目录测试命令与一次工具组合命令触发容器总执行时间限制；随后按模块完整跑完全部测试，不将截断运行算作成功。首轮active-doc-links因本轮VALIDATION文件尚未生成而失败，补齐真实文档后6项项目结构测试通过。一次workflow CLI使用错误的--plan参数，改为实际positional语法后通过，没有修改工具来掩盖误调用。

## 重点覆盖

- 升级后的10工具/observation1.1/默认公开推理是安装契约，旧服务不是正常fallback。
- 无opt-in参数仍允许已验证公开字段；encrypted_content嵌套字段拒绝进入选定证据。
- 固定top3工具/每类last5调用/无结果、200 Unicode字符（不是字节或delta数）、按真实调用ID去重但保留不同调用的相同内容。
- 五种语义标签仅出现在MCP description，不在响应schema、server参考投影或Skill自动分类器。
- xxx.zip与xxx-zas.zip配对、identity/run/parent hash验证、幂等复用、子包失败后保留主包、修正后只补子包、错误run或错误父包拒绝。
- 主包不可嵌入详细ZAS-AUDIT；typed intake不将ZAS companion计为第二个feature。
- 不生成.sha256侧文件或新SHA清单；JSON manifests/receipts仍校验完整性；旧SHA manifest只读验证。
- 外部Advisor仍需人工采纳、Git/linked-worktree包与未授权动作限制没有弱化。

## 静态与结构

- 两份Skill通过附件Skill Creator quick_validate。
- PLAN通过section_plan与workflow两层校验；workflow_revision保持4.3。
- 当前Markdown链接/anchor、长reference目录通过。
- Python AST、7份TOML、JSON、JSON Schema通过检查。
- Skill和ZAS执行包的tool description/response schema/source template字节一致。
- 原151份版本历史、7份agent配置、核心workflow/execution_artifacts/section_plan/advisor_flow和ADVISOR-REQUEST字节保持。
- ZIP发布前验证CRC、成员内容与Unix权限；不含__pycache__、pyc、DS_Store或新.sha256文件。

## 明确未做

没有修改ZAS生产源码、编译/部署ZAS binary或运行真实Codex/ZCode/GLM。无法在此容器连接用户本机macOS runtime，因此没有确认其准确reasoning event selector/text key。执行包中的来源清单是必须本机实测填实的交付项；reference用合成字段，不是生产键名。

离线测试证明契约与打包操作，不证明真实模型是否循环、不会误判或运行时始终可靠。
