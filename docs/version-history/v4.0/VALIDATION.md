# 4.0 验证记录

## 已执行

- 六份本轮附件均读取；四个 ZIP 逐项 CRC 检查通过。
- 49 个 intake ZIP 分为 40 个流程样本和 9 个辅助 runtime/conformance 包，保留文件哈希与分类原因。
- `python -m unittest discover -s tests -v`：**35/35 PASS**。原始结果见同目录 `VALIDATION-TESTS.txt`。
- Python 脚本 compileall：通过。
- 八份 agents TOML 解析通过；包含 name、description、developer_instructions、model、model_reasoning_effort、sandbox_mode；总计六种 model–effort 组合。未伪造 `fork_context` TOML 字段。
- SKILL frontmatter：name/description，有效 YAML；description 723字符，正文文件95行。
- 活动 Skill/README Markdown 内部文件链接、PLAN-FULL 标记/schema/DAG 与模板校验：通过。历史文档不追认过时规则或外链。
- `ADVISOR-REQUEST.template.md` 与本轮输入原文件 **365字节完全一致**，SHA-256：`4e237e1da8d1e40be6eb87d47ed578a7ece15cd65ede184d7384242bcb078cdb`。
- Installer 默认 dry-run不写入；临时CODEX_HOME下apply、已存在目标拒绝、明确replace备份、保留AGENTS/unrelated文件均测试通过。
- 发布 ZIP 使用一个根目录 `sectioned-feature-development/`，包含项目与输入已有的历史Markdown，不包含历史仓库Git/用户审计ZIP/凭据/缓存。文件清单见根目录MANIFEST.sha256；解压后逐文件hash/Unix权限与目录内容核对、CRC检查通过。

## 行为测试覆盖

多section no-commit/main阻塞；单section no-commit；DAG与stage循环；路径越界/glob/未知check；先accepted再integrated的依赖；独立兄弟节点并行；审查期间独立workspace可继续但dependent不能；读写/契约/测试资源冲突；临时真实Git分支、worktree、ignore；review index并发原子预留和幂等；advisor阻塞；已完成plan与用户follow-up处理。

Audit覆盖typed purpose、身份、manifest hash、同路径幂等发布、内容变化须显式replace、源码identity、跨feature事件、重复事件、危险路径/symlink/secret/nestedZIP、legacy/aux过滤。`verify`也独立重验payload身份，不只比ZIP哈希。

## 验证中修正

最初33项中32通过，1项仅因VALIDATION.md尚未创建导致文档链接失败。补齐该文件；另在代码检查中发现ZIP verify只比较hash、没有复核events/source identity，已复用同一校验并新增两项回归。最终35项通过。没有隐藏失败或把未执行的测试算作通过。

## 未实测且不能由这些测试证明

- 真实Codex版本的模型/effort账户可用性、实际采样质量、套餐/账单成本；
- 实际原生spawn能否提供可核验的非继承上下文；TOML本身不能证明advisor隔离；
- 用户macOS上的ZCode daemon/Hook/named-check可用性及GLM真实review质量；
- 终态ZCode不能续接这一契约边界不会被工作流消除；
- 多agent真实项目的速度/质量、数据库/端口隔离、语义冲突与集成成功率；
- 新模型路由是否降低总成本且不增加escaped defects。

本发布提供可执行配置、流程校验和供试运行的路由假设，**不是已完成的模型/并行性能实验**。本轮审计是阶段过程与证据核查，不是40项目的重新全面代码审计或merge认证。
