# Requirements — mcp-public-contract-slim-20260909

## 原始用户要求（原文与来源）

2026-09-09，提供的 10:08 rollout 第 5 行用户消息：

> 判断这些是否可以移除：
> zcode_subagent_status
> 返回api_surface、protocol_version、service_generation、capabilities.observation.protocol、runtime_source_verified、identity.daemon/facade.component, version, source_revision, source_dirty、identity.*.artifact.sha256、identity.*.artifact.source, captured_at_ms、identity.*.artifact.captured_at_ms、identity.runtime、identity.models.observed_response
> 
> zcode_subagent_poll
> task.input_identity.caller_prompt_sha256, reasoning_delta_bytes, text_delta_bytes, 
> 
> zcode_subagent_observe
> schema, agent_id, service_generation, count_scope, reasoning.char_count, reasoning.source, 
> 
> zcode_subagent_list
> tasks[].input_identity.caller_prompt_sha256
> 
> zcode_subagent_cancel
> task.input_identity.caller_prompt_sha256
> 
> zcode_subagent_result
> tasks.input_identity.caller_prompt_sha256
> 
> zcode_subagent_close
> tasks.input_identity.caller_prompt_sha256
> 
> 是否可以修改：
> agent_id改为increment 数字，避免超长随机字符串浪费token。

第 69 行用户消息：

> 需要考虑到的是：mcp调用方/文档和deamon是同步更新的，因此并不需要维护旧版本支持。有这个前提的话，你的评估会有变化吗？

第 81 行用户更正：

> 去掉开头的za_，改为10000000-99999999

同消息的工作流指令：

> [$sectioned-feature-development] 这里面提到zas的都用 [@sol_xhigh] 代替，避免开发时调用造成额外问题。最后做真实zcode调用验收。

后续第 377 行澄清的含义：只替代 ZAS reviewer，implementation 仍按原 impl 分级。第 469 行用户要求开始实现。最新 11:34 rollout 再次明确 PLAN review 已在外部完成，要求执行 S01。

## 解析后的当前合同

- 同步更新公共字段/类型/schema/docs/caller，无旧公共契约兼容。
- 八位递增 JSON integer，10000000–99999999；并发唯一、同库重启继续、不回绕。允许失败分配留 gap，不承诺 gapless 或按完成响应排序。
- 删除完整字段清单由 PLAN 第 2 节逐工具列出。`snapshot_seq` 是先前已审 PLAN 对 current snapshot 的补充删减，不是原消息逐字字段，现修订显式沿用。
- 内部 integrity digest、运维 identity/diagnose、encrypted_content 排除、既有脱敏和资源清理不删。
- 公共 task ID 改为 integer 不强制内部所有 TEXT/String 类型重构；不建别名系统或额外信任模型。
- 不自动清活动 DB；fresh 测试 DB 和部署数据处置分开。真实破坏性操作需另行授权。
- 实现按固定 impl 级别。GLM slot 暂由 sol_xhigh 代替。仅最终受控真实验收调用 ZCode。

## 自包含交接边界

本文件与 PLAN、仓库源码和当前 repo AGENTS 足够新会话执行。旧 single-service plan/reviewer 不是本任务 authority。原始 rollout 保留为 provenance，执行者不需要读无关系统提示或全部旧聊天。若实际源码与附件基线不同，先检查 drift，不覆盖正确新工作。
