# 4.5 — 2026-09-09

## 4.5.1 — 规划知识按领域／语言分离

- 原混合 domains 拆为独立工程 domains、languages、明确分类的 framework/runtime/platform adapters，并扩展常用覆盖；横切 concerns 不变。
- 选择实际变更路径，允许多个维度组合和部分未知，不要求全轴命中或加载全库。
- 迁移五个旧知识文件的职责，保留 shared boundary handoff、scope authority和原执行流程；只更新既有PLAN/reviewer/audit路由文字。
- 九份运行脚本、安装器、配套 code-review 与模型绑定不变；不增加门禁或review。


- 以当前上传4.4.1工作树为基线，保留 FINAL_ANSWER/completed 与 native/ZAS 序列规则。
- 新增可组合规划知识库：通用回退、共享边界、full-stack、Swift/macOS、Python、Rust、Svelte、Java及四类横切 concern。
- PLAN→producer HANDOFF→consumer TASK 传递同一具体请求/响应/状态样例；计划阶段标记 planned/source/observed，不伪造尚未执行的接口。
- 主线程与独立 PLAN reviewer 按需读取；资料不产生新需求、模型升级、section/reviewer或框架。九个运行脚本、安装器与code-review逐字不变。
- Audit复用现有文件记录路由、实际合同、遗漏类别与成本；没有新字段校验或额外运行。
- 七个agent绑定不变，仅plan_reviewer指令增加路由。历史资料保持，不复制previous-version baseline。
- 修正两项原输入已失败的历史归档测试，改核对真实输入哈希；无真实模型任务性能实验。

# 4.4.1 — 2026-09-09

- 明确 feature-wide PLAN 等待屏障、serial parent/child 真正闭合后的派发，以及预先批准的独立父级并行例外。
- 原生 code_reviewer/plan_reviewer 与 ZAS MCP 分离：描述层、实际 dispatch、ID/lifecycle、覆盖例外和错误路由恢复一致。
- 原结果保留、主线程 admission、普通 plan-only 修正、ONE/TWO/模型/预算/轮换均不改变；不恢复任何流程调度脚本。
- 交接与路由事实复用现有状态、任务、review 和 audit；安装器和九个运行脚本逐字保留。
- 仅指令/模板连线与离线回归，没有真实 Codex/ZAS 模型行为实验。

# 4.4 — 2026-09-09

Agent-managed scheduling replaces workflow/execution_artifacts/advisor_flow gates; only basic section structure validation remains. Required saved artifacts, delegation, review, budgets and tests remain. Existing deterministic packaging/safety helpers retained. See version-history/v4.4.

# 4.3.1 — 完整合并包（PLAN review 定点修订）

- 合入19项已交付修订，保留正确的上传工作区改动。
- 修复普通PLAN修正也必须重新取得exact-hash APPROVED的admission冲突；保留原报告与快照、候选处置及边界变化检查。
- 撤销无授权的“原生必做＋ZCode额外审查”，恢复原full-review交替；保留正确时序与新版诊断说明。
- 同步遗漏的4.3.1版本、README、ZAS合同、配套code-review和回归测试。
- 本次只生成完整分发包，未再修改运行脚本；原版本历史保持。

# 4.3 — 2026-09-07

## 4.3.1 — 用户确认的 ZAS 观察与配对审计

- observe仅用于疑似无意义循环；固定top3工具、各last5调用、无结果、200字符公开reasoning尾部。
- 本机确认唯一reasoning字段，默认采集；encrypted_content在新增采集/日志/导出路径主动排除；无opt-in模式。
- 五种判断仅写MCP description，不在ZAS/Skill脚本增加自动分类器。
- 详细ZAS证据从主包移至同目录xxx-zas.zip；typed identity+parent hash关联，失败后复用parent恢复。
- 不再创建.sha256文件，完整性hash保留在JSON；旧档案只读兼容，不重写历史。
- 先部署ZAS观测更新再用Skill；移除旧服务fallback，保留真实运行失败处理。
- 模型角色/计划profile、执行artifact、review交替与预算、subsection/并行、外部Advisor不变。


- 基于上传4.2.1工作区增量更新，保留主线程计划作者的本地决定。
- 实现角色改为impl_nano/mini/std/large；每section/subsection在PLAN冻结，派发匹配。
- 适配当前ZAS9个短名称工具，受控beta；提出能力门控的只读observation和语义进展监督。
- ZAS attempt/生命周期/误报进入过程审计，不改变review alternation或repair预算。
- 恢复3.9人工外部Advisor，保留请求合同与六个触发；增加外部结果采纳状态。
- 可选显式备份并移除旧编号Agent和原生Advisor；不改无关配置。

# 4.2 — v3.9-preserving reconstruction

- Start from actual v3.9 instead of continuing the reduced4.0 root. Preserve unproven duties.
- Restore persistent artifact/real delegation/plan-review/acceptance chain; audit OFF still needs execution evidence.
- Enforce multisection branch+commit and closed-feature follow-up.
- Adopt parent business sections and internal/module/model-load subsections, parent-level acceptance/budget.
- Retain authorized4.0 model tiers/native advisor/isolated parallelism with requested role names.
- Dedicated process-only audit namespace and all legacy analytical dimensions plus new model/subsection/parallel/Advisor telemetry.
- Ship companion code-review and installer together.

# Change Log

## 4.1 — 2026-09-05

- 可选单层subsections，将实现/review checkpoint与parent验收边界分离；禁止递归与LOC强拆。
- 共同不变量、一次累计primary coverage、parent joint reconciliation和独立final；不机械复制子节Clean A/B。
- 预算/authority/provider序号继承；subsection通过不解锁外部依赖。
- 添加child调度、metadata验收和累计repair工具/回归；schema4原子计划兼容。
- 补齐缺失的当前code-review目录并升级delegated4.1，保留4.0兼容；安装器能真实完整安装。
- PPPMS计划基于当前附件的active45节点而非先前初稿；四个pending parent各加两checkpoint，accepted/B02不重开。


## 4.0.1 — 2026-09-04

- 修复 4.0 漏打包 active code-review 的配套缺口；历史附录不作为运行依赖。
- 新增明确的 DELEGATED_PASS 与 STANDALONE 分流；delegated 不 admission、不 repair、不接受 section、不增加 reviewer。
- 对齐三种 pass signal、原 ONE/TWO、feature-wide Astra/GLM 序号和 terminal continuation gap；不改变 4.0 工作流语义。
- 安装器默认安装两份 Skill 和八个 agent；新增 --only code-review 供已安装 4.0 用户最小升级。
- 增加协议/安装回归测试；4.0 历史记录与已有脚本保持不变。

## 4.0 — 2026-09-04

- 单一当前 Skill 替代两套过时 MCP variant；配套八个 agent TOML、六个 model/effort组合。
- 多 section 强制 commits+feature branch；完成后请求重新评估，显式 reopen 才创建新revision。
- 保留 advisor 请求合同原字节，改成有限上下文的 native advisor；没有 fresh-context 能力不伪称隔离。
- 用依赖/资源/语义冲突图替代全局串行锁；独立工作树并行、候选冻结、串行集成。
- 只采用当前九个 ZCode 工具，明确终态 continuation 缺失、Git caller ownership与 plan-mode 边界。
- PLAN 加入可执行调度块、任务结构/模型选择证据和必要失败轨迹，保留 scope/repair门禁。
- Audit 采用 purpose+producer+identity+manifest鉴别；记录模型全流程成本、并行、advisor、continuity与跟进请求边界。
- AGENTS 保留政策，删除重复推理提示；借鉴 skill-doctor 的分维度证据，不优化 skill usage coverage 分数。
- 历史 docs 保留但不进入默认运行上下文。没有为了升级重开旧 section 或迁移旧产品证据。

---

## Historical changelog (as supplied)

# CHANGE LOG

记录 `sectioned-feature-development` 各历史版本在流程上的变化。时间采用“该版本最终纳入的最后一条用户指令时间”。

## v1 — 20260806-223457

建立首个大功能分段开发 Skill：以行为 section 拆分大修改，引入 PLAN-FULL/PLAN、section contract/handoff、SECTION/DELTA/INTEGRATION review 语义和 branch/commit 执行模式。

## v1.1 — 20260807-093926

把 Custom Instructions 收缩为触发路由；由上层指令显式授予 scoped branch/commit 例外；Custom Instructions 与 Skill description 保留一致触发条件。

## v2 — 20260807-095143

恢复“小 section 连续两次独立 clean”作为接受条件；去掉 soft cap；第 5 次 full SECTION review 仍不收敛时自动备份并由 sol_max 重拆当前 section，支持层级 section ID。

## v2.1 — 20260808-162346

针对 review scope 膨胀增加 finding admission、scope/assurance envelope 与 anti-overdesign 约束；hard-cap recovery 改为先诊断 split/simplify/rebound/evidence，而非机械继续强化 reviewer 创建的安全/治理模型。

## v3 — 20260809-133655

基于四个真实项目的过长 review 数据大幅简化收敛：每个稳定 section 只做一次 INITIAL_BOUNDED，repair 只做 REPAIR_DELTA，最后一次 FINAL_BOUNDED；hard cap 按 admitted repair wave，而不是 reviewer 次数；禁止 clean-lineage/evidence-only 重建。

## v3.1 — 20260809-161721

收紧 MERGE_BLOCKING_DEPENDENCY 因果、EVIDENCE_GAP authority anchor 和 edit-vs-inspect manifest；section repair budget 跨 initial/delta/final/recovery 累计；每个 original lineage 只允许一次自动 hard-cap recovery；integration 复用同一 admission boundary。

## v3.2 — 20260809-201037

新增 plan-authority/minimum-delivery guard：PLAN 和 section contract 只能记录 authority，不能创造 authority；每个新增机制必须锚定原始要求、repo rule、production contract 或 unavoidable correctness。

## v3.3 — 20260810-121928

新增编码前单次、fresh、read-only PLAN-FULL semantic review；最多一次 PLAN_DELTA recheck；保留原代码 review 状态机，禁止 plan-review clean streak、递归 reviewer 或 plan-review-only section。

## v3.4 — 20260811-125226

加入自适应 review assurance：AUTO | ONE | TWO；按语义风险而非纯 LOC 决定独立 clean evidence；强化原始失败样例/后续纠正到 AC/test 的映射、final-head evidence、外部 seam probe、validation evidence reuse 与 feature artifact isolation。

## v3.5 — 20260813-145021

把流程 Audit 作为独立观测能力接入 Skill reference：记录 invocation source、LIVE/POST_HOC trace、feature artifact 隔离与审计一致性；Audit 不新增开发/review gate。

## v3.7 — 20260817-092709

合并本地 Audit 改动：默认 LIVE audit、允许读取 Codex sessions、工作目录保留 .agent-work 且 canonical ZIP 输出到 Desktop；增加原始需求/Grill Me 记录、多轴 audit status、原子幂等 finalizer、branch-base authority、PLAN representation/lifecycle/inventory lenses 与验证证据复用。

## v3.8 — 20260820-084405

基于 27 个 feature audit 收紧自动触发：non-trivial prerequisite + bounded-local negative rules；区分用户显式/自动调用审批；增加 late activation、orchestrator-only 角色隔离、单 mutable-stage barrier、.agent-work 禁止入 Git、necessity-first PLAN review 和 foundation-choice gate。

## v3.9 — 20260825-005020

面向 ZCode/GLM 外部 subagent：高复杂度 PLAN 增加独立 ZCode challenge；code review 在 Sol/ZCode full pass 间交替；记录外部 reviewer identity/exact-head/integrity；增加低频 External Advisor escalation；同时保留 current-MCP 与 enhanced-ZCode-MCP 两个 Skill 变体。

> 注：没有独立可归档的 v3.6 snapshot；本地修改后来并入 v3.7，因此历史中不伪造 v3.6。
