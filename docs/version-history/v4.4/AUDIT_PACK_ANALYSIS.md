# 本轮流程分析：机械调度阻塞与 ZAS PLAN

## 证据边界

读取本轮归档的当前 ZAS 源码/.agent-work 和三份 2026-09-09 rollout；基线 Skill 为实际完整 4.3.1 包。3.9 来自真实 tag `e21c9a3e525fa7d3da0fb71fc3eeb12cf25c591c` 的 current-mcp 变体，不用旧回复的行数/文件名替代实际内容。本轮归档没有 ZAS `.git`，不能声称证明当前工作区 clean 或完整 source-history 关系。

当前资料是源码/会话快照，不是完整新 feature 的结束 Audit Pack。本次不做 ZAS merge 认证。原始系统提示、无关记忆和模型私有 analysis 不进入交付文档；引用只取用户请求、工具动作/结果、实际源码与公开报告。

## 观察到的执行阻塞

最新 11:34 rollout 的可见范围为 17:35:05Z–17:43:01Z，约 7 分 56 秒墙钟跨度。共 19 个 response-item tool calls；没有实际 subagent 派发、产品代码修改或产品测试。这里的 wall span 不是精确 active time，更不能推算每次以后都浪费同样时间。

可见调用中反复出现本地 exclude、section validator、workflow validator 与 execution ready。包括读取脚本在内的 command payload 提及次数：workflow.py 6、execution_artifacts.py 4、section_plan.py 2、ensure helper 2；这些不是各脚本真实执行次数，不互相求和为独立调用总量。完整机械摘要在 ROLLOUT-METRICS.json。

重要原始位置（最新 rollout）：
- 行 50/53：ready 返回要求精确 marked PLAN v4 schedule。
- 行 57、85、97：修改 PLAN 的 marker / base_ref，尚未产品实施。
- 行 90/93：格式修正后进入 exact base_ref 错误。
- 行 102/105：随后进入 requirements SHA-256 required。
- 行 109 以后：读取整个 workflow 脚本，转而查 plan-draft/旧 hash。

提交的 PLAN-FULL 有人可读的业务内容，但 machine block 是 stages 而不是 sections，也没有执行器要求的 checks、requirements_sha256 等字段。旧 `plan-draft.md` 则属于 mcp-single-service-lifecycle-20260908，不能拿来补 mcp-public-contract-slim-20260909 的批准证据。这同时暴露出两个问题：过重 schema 带来流程修复循环；旧 feature artifact 污染不能用简单改名/hash 来解决。

## 相比 3.9 新增了什么

见 SCRIPT-INVENTORY.json。3.9 有 6 个生产辅助脚本；当前 4.3.1 有 12 个。新增 workflow.py 561 行、execution_artifacts.py 450 行、advisor_flow.py 105 行，共 1116 行机器调度/回执状态逻辑。它们要求计划双表示、actor 注册、stage binding、approve/ready/accept、hash-linked 原始输出与派生状态。

新增的 process_audit、zas_audit_pack、zas_evidence 则是 pack/wire 操作，不应与调度器混同。Git exclude、真测试、原子压缩、secret 前检、manifest 完整性不等于产品实施前必须通过十几份自造 JSON。

3.9 也有计划 validator、检查和 audit 脚本，不能把它说成完全无脚本。变化是从辅助确定性操作，变成“不断证明执行流程自己合法”的控制面。

## 责任判断

原来为了修复 4.0 丢 PLAN/委派链，4.2–4.3.1 把职责恢复成了强机器回执系统。这是 Skill 设计的过度补偿，不只是模型没认真遵守。最新日志还包含 CLI 参数误用和追错旧文件的执行偏差。改成 agent-managed 后仍可能跳步骤，因此保留清楚的原始文件交接、真实工具 ID 和独立 review，不能宣传质量风险归零。

## ZAS PLAN 的具体修订

1. 原 S03 把 schema/docs/tests 和 release/live 验收独立为产品节。前者分别随 S01/S02 的真实合同完成，后者属于 final integration gate。改成两业务 section，消除“不完整 contract 先 accepted、以后补消费者”的边界。
2. S02 中公共八位 JSON integer 不必预先强制全库 TEXT/String→INTEGER。当前 Store.tasks.agent_id 是 TEXT，相关外键也是 TEXT；在唯一持久分配路径产生数字，再由单一公共边界返回整数即可满足要求。允许内部保存同一数字的十进制表示，但不引入随机旧 ID→新 ID 的 alias registry。
3. 保留同库重启不倒退、并发唯一、有限范围耗尽、不回收已分配 ID；不要求 gapless、并发响应有序或新增 capability/security 模型。
4. 明确公开删除字段不删除私有 RPC version、prompt integrity、diagnose 和内部 reasoning-source 验证。保留原已审 current-snapshot 方案对 snapshot_seq 的删除，并标明它不是原用户逐字清单。
5. 只在主 checkout 串行，遵从本仓 no-worktree；不把 generic parallel Skill 反过来覆盖 repo 规则。
6. user override 仅将 would-be ZAS review slots 替换为 sol_xhigh，实现仍是 impl_std/impl_large；最后真实 ZCode 验收不冒充开发 reviewer。
7. 无旧公共契约兼容不等于自动删除用户当前 DB。使用 isolated fresh test DB，实际 reset 需要独立授权。
8. 新会话核对真实 branch/drift，保存旧材料但不消费旧 JSON gate；只对本次两处实际边界变化做一次 PLAN_DELTA，不重开 full PLAN 发现循环。

## 可前移与不能前移的问题

PLAN 可以提前避免证据专用 S03、消费者过晚接入、内部类型强制大改、并发分配和部署数据权限混淆。计划不应提前指定所有私有函数/表/输出文件名。格式修补应通过一个简单 structural helper 一次指出，而不是再加一层 reviewer。

## 其他独立成本来源

当前会话的通用 AGENTS 要求每次 Cargo 编译前 cargo clean；它会放弃增量编译结果，是独立于 Skill 的成本政策。本次不擅自撤销。用户可以以后单独决定仅在 cache suspect/工具链变化时 clean；本版计划仍遵守现有规则。

## 结论

将机械流程校验收缩为基本 section 结构，是本次直接证据支持的简化；不是因为文章说“信任模型”就删除质量门禁。采用者应监测实际跳过 review/delegation 和 escaped defects，必要时修最小具体失败点，不重建通用审批引擎。
