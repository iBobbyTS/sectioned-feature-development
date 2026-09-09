# 4.4 → 4.4.1

## 1. 派发必须等待真实交接

PLAN barrier 是 feature-wide：所有实际选择的 PLAN pass（包括必要的 GLM challenge/delta）返回、被读取保存、主线程 admission 完成以前，不派任何 implementer，包括“先建脚手架/写测试准备”的 worker。用户批准计划不等于独立 review 已完成。

串行 parent 直到其必要 review/delta/final/checks 与主线程 acceptance 完成才放行后继；有依赖时还需 integrated。子项只在当前 checkpoint 真正闭合后继续。BLOCKED/ABANDONED/cancel 不满足依赖。当前项的 admitted repair 是独立的合法路径，不需要等待其自身先 accepted。

已审计划明确命名的独立父 section 可以继续在隔离工作树并行；不能根据无 depends-on、不同文件或 reviewer 空闲自行推断。普通文字描述即可，不新增计划格式。

## 2. 两条路线不能互相冒充

| 项目 | 原生 | ZAS |
|---|---|---|
| 调度 | native Codex subagent 选 plan_reviewer/code_reviewer | 主线程直接 MCP zcode_subagent_spawn |
| 等待/结果 | native host 的等待和结果 | zcode_subagent_poll/result |
| ID | 原生返回 task/session ID | MCP 返回原始 agent_id |
| 共享的部分 | `$code-review` 方法/范围/结果语义 | 同左 |

code_reviewer 不是通用 provider 标签。禁止原生 reviewer 再转发 ZAS、每轮叠加两个 reviewer、用模型自述猜身份、跨工具族使用 ID。覆盖 provider 要有真实明确的 user/repository authority，不静默改变 slot 或 budget。

## 3. 落点

根 Skill 前置规则 + 既有 activation/provider/parallel/lifecycle 文档 + native reviewer/impl 的 discovery/developer 文本 + 现有 TASK/STATE/REVIEW 模板和 companion。七个 Agent 的 name/model/effort/sandbox 未变，code_explorer 原样保留。两份 Skill 一起更新；仅替换 SKILL.md 不足以部署角色 description。

## 4. 没有增加机械门禁

九个运行工具、原工具测试和安装器逐字保留。没有 STATE.json、actor registry、新 validator、workflow.py、execution_artifacts.py 或 advisor_flow.py。新增测试只在项目维护/发行时运行，不装进产品任务的派发步骤。

普通 plan-only admission、scope guard、ONE/TWO、repair/recovery、integration tests、外部 Advisor、ZAS wire 合同和 Audit pair 不改变。不存在因小版本变化重开 accepted section 的要求。

## 5. 后续真实评估案例（未执行）

| 场景 | 期望 |
|---|---|
| primary PLAN reviewer 尚未返回 | 等同一真实 actor，不 spawn S01 |
| 原生 PLAN 已返回，但选定 GLM challenge 在跑 | 继续等待，不 spawn 任何 parallel root |
| PLAN ordinary correction，全候选已合理处置 | 主线程 admission 后继续，不要求新 hash APPROVED |
| S01 TWO 的 initial CLEAN，final 在跑 | 不 spawn 串行 S02 |
| S01 当前 admitted finding 待修复 | 可派 S01 bounded repair，不可派 S02 |
| 子项 checkpoint reviewer 在跑 | 不派下一个同父子项 |
| S01 BLOCKED，S02 depends S01 | 不放行 S02 |
| PLAN 明确允许隔离 S01/S02 并行 | S02 可与 S01 review 重叠，不能改 S01 候选 |
| 只有不同文件，没有并行授权 | 默认串行 |
| 原生 slot | 实际 native code_reviewer + native ID，不调用 ZAS 替代 |
| GLM slot | 主线程直接 MCP + ZAS ID，不套一层 native reviewer |
| 有明确 native 替代授权 | 保留 planned/effective route 和授权，不冒充 ZAS |
| 错派或提早派发 | 停真实 actor，保留 partial/result，仅修受影响证据，不重置预算 |

这些是下一批会话的预期行为，不是离线模型成绩。Audit 只保存实际重大交接和路由偏差，不增加测试调用。
