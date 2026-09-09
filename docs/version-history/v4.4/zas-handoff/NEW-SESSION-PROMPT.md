# 给新 Codex 会话的执行 Prompt

使用已安装的 [$sectioned-feature-development](/Users/ibobby/.codex/skills/sectioned-feature-development/SKILL.md) 4.4，继续 ZAS 的 MCP 公共协议瘦身。附件是本次 Advisor 修订后的 PLAN-FULL 和自包含 REQUIREMENTS；它们是本次执行范围。不要继续前两个会话的格式修补，也不要把任务改成修 Skill。

## 先建立真实接管边界

在 `/Users/ibobby/Projects/zcode-mcp` 主 checkout 工作。先确认旧任务 `01a086d4-c5a1-7b60-b2ba-b5f155dc688d` 与 `01a0873b-fce6-7c33-a5ff-e7060d1e5dee` 及子代理没有仍在写入/审查；必要时用实际可用的任务工具停止这些明确属于本功能的任务，保存 partial work，不能仅清理状态字符串。没有任务工具时请我确认这两项已经停止。

核对实际 branch/HEAD/diff。已授权 feature branch 为 `codex/mcp-protocol-slim-20260909`，附件记录基线 `34a5012856a01c92c359baaa43caaea75716dc3b`。若已有新的相关产品提交，保留并核对，只继续未完成部分；遇到不相关 branch 或业务冲突才询问。禁止 reset、clean、丢弃用户工作或创建开发 worktree。本仓代码写入串行。

允许把当前功能旧 PLAN、REQUIREMENTS、FEATURE-STATE 复制备份到 `.agent-work/plans/mcp-public-contract-slim-20260909/pre-4.4/`（不覆盖既有备份），然后将本次附件保存为根部 `.agent-work/PLAN-FULL.md` 和 `.agent-work/REQUIREMENTS.md`。旧 STATE.json、历史 reviewer receipts 原地保留但不再消费。尤其 `.agent-work/evidence/plan-draft.md` 是上一个 single-service feature，不得拿它补本次 metadata。

## 执行

本 Prompt 批准新计划的二 section 边界、内部 TEXT 可保留的局部实现选择、以及各 section/subsection 的固定实现级别。不要重复 routine 人工 PLAN approval。

先运行一次 4.4 的基本 section 校验；不运行旧 `workflow.py`、`execution_artifacts.py`、`advisor_flow.py` 或 actor/approval/hash registry。实际安装版本仍是 4.3.1 时停止并告诉我需要先安装 4.4，不在本产品任务中修改已安装 Skill。

保留本功能已有原始 PLAN review。因本修订改变了 S03 的归属和 S02 的实现边界，派发一位独立 [@plan_reviewer](subagent://plan_reviewer) 只做一次 PLAN_DELTA，核对这两处及受影响依赖；不要重新全量探索设计。普通 plan-only 纠正由你 admission 并保存原报告，没有实质 blocker 就开始 S01，不能再追求最新 hash 的 reviewer APPROVED。

实际派发 PLAN 中的 [@impl_std](subagent://impl_std) / [@impl_large](subagent://impl_large)，主线程不自行编程。保持原生 [@code_reviewer](subagent://code_reviewer)；只有本来安排给 ZAS/GLM 的 review slot 使用 [@sol_xhigh](subagent://sol_xhigh) 替代。实现角色不替换。开发/review 期间不要调用修改中的 ZAS 服务；最后按计划进行一次受控真实 ZCode 生命周期验收。若本地缺少 sol_xhigh 配置，先核对已安装 agents，报告缺失，不自行杜撰模型配置。

完成两个业务 section、子项 checkpoint/父级 reconciliation、必要 final review、现有测试和最终 release/live gate。原 repair 预算、ONE/TWO、scope admission 保持。记录真实 Agent ID、候选 HEAD、检查结果和简洁 HANDOFF/REVIEW；不补造 JSON 回执，不扫描整个历史 .agent-work。

后续只有真实需求/授权/环境阻塞才停。元数据格式问题最多记录一次，不进入 Skill 修复循环。无关旧缺陷不扩入本功能。不要 merge main、push、清理分支或销毁活动数据库。完成后给出真实 readiness、未验证项和规范的单一 process audit；真实 ZAS 运行细节使用配对 `-zas.zip`，不得用新审计动作替代缺失的开发证据。
