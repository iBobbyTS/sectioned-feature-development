# 本轮 Audit Pack 分析（4.0）



## 范围与证据

六份输入均可读取，ZIP 完整性已检查。audit-packs.zip 含49个包：40个流程审计、9个ZCode runtime/conformance辅助包。下列是**流程与阶段结果审计**，不是对40个最终源码进行新的全面 code audit或merge认证。原始 ledger优先于摘要；推测可前置的机制明确为counterfactual，不保证提前发现每个bug。

本文件不复制认证信息、完整日志、业务记录、用户个人资料或本地绝对路径；仅保留任务名称、逻辑缺陷类别、相对证据来源。

## 采用 skill-doctor 的方法，避免它的激励偏差

阅读了附件 SKILL、efficiency/code-quality scorer及improvement指导；没有在不支持的宿主上声称运行 Warp doctor。采纳“按具体对话证据分别评质量与效率、缺证据不算质量失败、修改只针对可归因失败”。不采用覆盖率占比或加权总分来优化本Skill，否则正确地不触发sectioned也会被惩罚。最终修好与用户发现escaped defect分别记录，不能将其合成一个完成度分。

## 全批次直接结论

- 多section无commit是存在的流程违规；完成后往旧PLAN追加用户新要求也存在。4.0以机器检查和closed-feature边界修复，而不是再重复模型应当小心的提示。

- ZCode final convergence摘要说合规，但其原始S02/S03 ledger记录三次审查期间改HEAD。READY调度只能并行独立冻结workspace，绝不能并行修改同一candidate。

- owner/projection/权限载体、重复UI事件、cancel/restart/late-result、原子迁移、真实oracle先后顺序，适合在PLAN冻结；把这些变成针对性行为例子比扩大通用checklist有效。

- 许多后期修复是已批准PLAN未落实或测试只验证mock的实现错误；增加更多PLAN reviewer并不一定有用。应把原例→生产入口→测试路径交给合适实现者。

- 429与connectivity的阶段摘要文本相同，fixed-project-catalog计数互相冲突；不把这些数字放进平均repair/token统计。应用导出的token数据不是Agent开发usage。

- 新模型在本批数据中没有可比的实际分配结果，不能用它计算Astra/Luna/ Terra优劣或宣称4.0节省了多少。

## 40个流程样本逐项分析



### P01 — `API-sol-usage-export-sectioned-audit.zip`

**PLAN 阶段：** PLAN 捕获 SQL 投影、价格、备份和示例，tuple-union 修订走 delta。

**代码 review / repair / final：** 代码 REV-001–008 在三波中处理；最终 clean。

**可前置部分（推断）：** 导出列×公式×价格单位×异常数值的行为表可前移；不要把当前应用导出的使用量当作开发 token 成本。

**流程判断：** 流程适合只读财务导出边界。COST-METRICS 是产品数据，不纳入模型开发费用统计。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P02 — `AnyUpright-debug-app-flow-deescalation-sectioned-audit.zip`

**PLAN 阶段：** 自动触发后探测实际只有一个小脚本、无高风险语义改变，及时退回普通流程。

**代码 review / repair / final：** 没有正式 PLAN/code review；用户要求记录去升级过程。

**可前置部分（推断）：** 负触发规则在最初直接 owner 探索即可生效。

**流程判断：** 正确不使用 Skill 是成功样本；不因为 skill coverage 低而扣分。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P03 — `AnyUpright-fcp-motion-analysis-time-domain-sectioned-audit.zip`

**PLAN 阶段：** PLAN 发现 frame-source owner 与测试入口。

**代码 review / repair / final：** initial 修复 conversion fail-open、unknown host 当 Motion 和连接测试；final 修复同帧 tick 容差；两波后有界闭合。

**可前置部分（推断）：** PLAN 可列 host×time representation×conversion validity；具体浮点比较仍须实现后验证。

**流程判断：** 时间语义不是按 LOC 能决定模型的任务。缺现场宿主验证是 evidence gap，不是计划错误。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P04 — `codex-rosetta-availability-snapshot-cooldown-recovery-20260901-sectioned-audit.zip`

**PLAN 阶段：** 一个 availability snapshot/cooldown section。

**代码 review / repair / final：** PLAN/code 两轮 clean、零 repair。

**可前置部分（推断）：** 没有证据表明还需更深 PLAN；应保留状态时效性的明确 oracle。

**流程判断：** 零 finding 不能单独证明独立 review 浪费；可对比后续同类 ONE 样本。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P05 — `codex-rosetta-codex-cockpit-provider-health-sectioned-audit.zip`

**PLAN 阶段：** PLAN 已指出 app failover控制点、current-key probe、provider scope。

**代码 review / repair / final：** S01 先缺函数/fixture，后 S03 消费时才补 Admin route并再次复核；S02 health/error、claim-loser/generation、pre-upstream分类多次修复；S03 UI证据补齐。

**可前置部分（推断）：** 完整 editor→public route→probe→shared state→routing 路径应在 PLAN 冻结，避免 accepted S01 后补生产入口。S01 ledger 开闭顺序仍有陈旧文字，不能精确累计波数。

**流程判断：** 复杂度真实，遗漏 consumer seam 有前移收益；不要把重复 typed-fixture失败当作新架构需求。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P06 — `codex-rosetta-failover-429-cooldown-20260826-sectioned-audit.zip`

**PLAN 阶段：** 429 pack 的 PLAN-AUDIT 与 connectivity pack 文本完全相同。

**代码 review / repair / final：** REVIEW-AUDIT 同样声称 S01 两波、S02 一波；当前包不足以独立核实它们各自计数。

**可前置部分（推断）：** 429 与连接失败应分别列实际 response/retry/stream authority；必须由原始 finding 来源区分。

**流程判断：** 标为共享摘要/归因不足，不将两包的相同数字重复加总，也不据此判产品有错。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P07 — `codex-rosetta-failover-connectivity-cooldown-20260826-sectioned-audit.zip`

**PLAN 阶段：** connectivity pack 两节：transport分类→provider cooldown。

**代码 review / repair / final：** 摘要与上一包相同，只有需求输入指出 DNS/TCP/TLS 和 pre-body retry。

**可前置部分（推断）：** PLAN 最小状态表区分 connect/read/status/partial output 及 retry次数/owner。

**流程判断：** 需要原始 ledger 才能判断每阶段；不把摘要复制误作独立效率样本。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P08 — `codex-rosetta-glm53-catalog-update-20260902-sectioned-audit.zip`

**PLAN 阶段：** catalog/model新增，PLAN delta通过。

**代码 review / repair / final：** 发生若干代码修复，最终 deterministic完成；真实多轮外部行为未测。

**可前置部分（推断）：** 检查 catalog→descriptor→serialized tools→执行filter 的同一字段传播，不靠模型名字符串猜能力。

**流程判断：** 外部活体验收未执行应独立报告，未知 repair数不填零。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P09 — `codex-rosetta-remove-observability-diagnostics-sectioned-audit.zip`

**PLAN 阶段：** PLAN 捕获 packaging/shared logging/legacy schema/model alias；缩小删除面。

**代码 review / repair / final：** 两波 bounded repair，未重建诊断框架。

**可前置部分（推断）：** 精确删除清单及仍在用的 shared owner 明确可前置。

**流程判断：** 适合一条纵向删除边界，不按每种文件拆 section。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P10 — `lmdo-website-create-project-needs-score-sectioned-audit.zip`

**PLAN 阶段：** 单节 NO_COMMIT；PLAN 明确 checkbox missing/default/400反馈。

**代码 review / repair / final：** 代码后出现相同400内容跨关闭重开被误认为旧反馈，修复为事件/对象身份。

**可前置部分（推断）：** 用户操作轨迹“失败→关闭→重开→同样失败”比静态结果文本更适合作 acceptance oracle。

**流程判断：** 单节可 no-commit；这一例不需要把所有 UI 改动升级为重型计划。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P11 — `lmdo-website-dynamic-performance-groups-20260831-sectioned-audit.zip`

**PLAN 阶段：** 五节覆盖 schema、授权、board、invite、miniprogram。

**代码 review / repair / final：** S03/S04/S05与integration分别多波；已报告3/2/4/4，不代表可按时间精确归因。

**可前置部分（推断）：** 共享 membership identity/permission matrix 先冻结，再切消费者；不能同时改 shared contract 和下游。

**流程判断：** 真实跨系统任务，适合 Sol/Astra承担基础语义，消费者在契约稳定后才评估并行。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P12 — `lmdo-website-group-instrument-inline-management-20260903-sectioned-audit.zip`

**PLAN 阶段：** PLAN 七个 blocker、两个用户决定，已指出 responsible lead candidate/capability路由。

**代码 review / repair / final：** initial 仍发现编辑入口不可达、无 scoped member candidates、transaction内授权不足、UI形态和破坏操作测试缺失；final 有 stale remove popup。

**可前置部分（推断）：** 前3项至少部分是已写清 PLAN 未落实，不应重复增加同类长规则；必须在任务包绑定 AC→生产入口→行为测试。popup复发用重复操作轨迹。

**流程判断：** 模型/执行遵守问题与 PLAN 缺失要分开；四波并非全部证明需要更多 plan reviews。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P13 — `lmdo-website-group-to-lead-category-sectioned-audit.zip`

**PLAN 阶段：** 三节 auth→admin→consumer/schema；PLAN 补迁移allowlist、invite和fallback inventory。

**代码 review / repair / final：** 各节多波修复，integration clean。

**可前置部分（推断）：** 角色/分类替换先完成 actor×resource×state授权关系表和明确迁移原子边界。

**流程判断：** 任务真实复杂；用模型完成质量/返工成本评价，不使用“文件很多所以 Astra”捷径。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P14 — `lmdo-website-management-list-ui-20260826-sectioned-audit.zip`

**PLAN 阶段：** 两节管理列表，PLAN 曾把3个owner直接当TWO必需。

**代码 review / repair / final：** S01 stale theme test；S02权限空态/移动布局/evidence；完成后又修 Svelte snippet 被当children而非 action。

**可前置部分（推断）：** consumer实际渲染路径验证可前置；owner数本身不决定review次数。

**流程判断：** 完成后的 snippet修复应是新请求，不应追加旧 feature；保留第一次成果的关闭边界。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P15 — `lmdo-website-pinyin-user-search-sectioned-audit.zip`

**PLAN 阶段：** 最初三节漏三个 loader，PLAN修到四节；storyboard与score实体隔离。

**代码 review / repair / final：** S01 polyphonic search suffix指数状态改为有界KMP；中间节 clean；末尾机械ONE；GLM不可用由用户改Sol，integration staleoracle。

**可前置部分（推断）：** PLAN 对输入基数和最坏复杂度有明确边界比泛化“高风险”有效。

**流程判断：** 算法变化不因小文件而给最廉价实现。外部模型失败与代码缺陷分开。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P16 — `lmdo-website-pr104-must-fix-sectioned-audit.zip`

**PLAN 阶段：** 明确只做七项 Must Fix，七项保留out-of-scope。

**代码 review / repair / final：** migration两波、auth一波、integration两波；目标main包含72历史提交，不能算本任务成本。

**可前置部分（推断）：** authoritative range要排除main inherited work；trace修正事件50→51已解释，不应判真实sequence违规。

**流程判断：** scope有界。服务故障、未知deltaidentity不算新product repair。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P17 — `lmdo-website-project-detail-multipage-sectioned-audit.zip`

**PLAN 阶段：** 原计划三节 project detail迁移。

**代码 review / repair / final：** 完成后用户修改 shared shell/header，又把S04追加到旧PLAN；既有修复四finding三波。

**可前置部分（推断）：** Svelte shared renderer/permissionprojection路径可在 PLAN 标明。

**流程判断：** 直接支持“完成后新请求新评估”硬约束；不是把用户后续需求追溯成最初遗漏。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P18 — `lmdo-website-project-summary-inline-autosave-sectioned-audit.zip`

**PLAN 阶段：** 单节 autosave；PLAN已经要求single-flight、viewer权限、人员状态保留。

**代码 review / repair / final：** 四文件约303新增/74删除却五波repair：反馈normalize、switch pending、shared form污染、duplicate latestPOST。

**可前置部分（推断）：** 必须有 edit→save→switch→late response→new edit 的可执行事件轨迹与权威pending owner。

**流程判断：** 小diff仍可能推理困难；不能用Luna实现+Astra兜底当通用省钱策略。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P19 — `lmdo-website-remove-unassigned-performance-group-20260902-sectioned-audit.zip`

**PLAN 阶段：** 五节 sentinel removal；producerfreeze、用户授权DB重置、精确消费清单。

**代码 review / repair / final：** 约110k行删除主要旧snapshot，不代表手写复杂度；六波关键projection/锁顺序/template literal。

**可前置部分（推断）：** 先确认 authoritative state/lock owner，消费者不可并行修改同一关系。

**流程判断：** 降噪 generated churn，同时保留真正 destructive semantics 验证。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P20 — `lmdo-website-shared-personnel-management-20260825-sectioned-audit.zip`

**PLAN 阶段：** 四节共享人员能力；PLAN补表示、迁移、权限、删除路径，拒绝新idempotency承诺。

**代码 review / repair / final：** S01四波迁移/PG锁；S02局部state泄漏与layout；S03标识/标题/staletest；S04projection反馈。

**可前置部分（推断）：** 共享基础先接受；模型分级在稳定消费者边界做，不能强拆一次事务。

**流程判断：** 需要基础设施修正，不是每个消费者独立叠条件；已有反膨胀拒绝有价值。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P21 — [保密内容]

[保密内容]



### P22 — [保密内容]

[保密内容]



### P23 — [保密内容]

[保密内容]



### P24 — [保密内容]

[保密内容]



### P25 — [保密内容]

[保密内容]



### P26 — [保密内容]

[保密内容]



### P27 — [保密内容]

[保密内容]



### P28 — [保密内容]

[保密内容]



### P29 — [保密内容]

[保密内容]



### P30 — [保密内容]

[保密内容]



### P31 — [保密内容]

[保密内容]



### P32 — [保密内容]

[保密内容]



### P33 — [保密内容]

[保密内容]



### P34 — `zcode-mcp-case3-review-tool-guidance-sectioned-audit.zip`

**PLAN 阶段：** 两section，用户特别设置三波上限；真实runtime受控。

**代码 review / repair / final：** S01 在可用 PLAN review证据前启动实现；S02多findings三波，官方Case3两次timeout无artifact后Advisor。

**可前置部分（推断）：** 保留runtime成功/终态契约及验证先后顺序，禁止缺plan approval先写。

**流程判断：** 流程时序违规真实，官方runtime失效不是Reviewer质量差；专门conformance ZIP不混入过程数量。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P35 — `zcode-mcp-operational-general-agent-closure-20260827-sectioned-audit.zip`

**PLAN 阶段：** S06–S08 operational general agent闭合。

**代码 review / repair / final：** 12review调用，13findings/5waves；仅fake+Codex公开工具验证，官方ZCode未调用。

**可前置部分（推断）：** PLAN事先区分产品generic contract与官方运行证明，别把fake测试当model工作成功。

**流程判断：** 结构证据与experimental/unverified能力标签分离，不给未实测release背书。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P36 — `zcode-mcp-review-safety-progress-evidence-review-safety-progress-evidence-sectioned-audit.zip`

**PLAN 阶段：** 三section。PLAN补provenance owner、新ingress持久化、cursor兼容、plugin交付并削减broadgate。

**代码 review / repair / final：** S01 command option grammar/path/provenance反复delta，FINAL FB1–5修复；S02 F1–6；S03clean；trace早期非JSON为INVALID但产品证据不一定冲突。

**可前置部分（推断）：** PLAN应区分声明policy与effective Rust/JS执行路径、加载入口和provenance绑定。

**流程判断：** 这里工具权限控制是用户批准范围；不得机械当作以往harness过度安全模型删除。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P37 — `zcode-mcp-zcode-final-generic-agent-convergence-sectioned-audit.zip`

**PLAN 阶段：** 三section；PLAN纠正group_id替代契约和official-runtime/CleanB循环依赖。

**代码 review / repair / final：** 摘要称顺序合规，但原始 S02/S03 ledger记录三次writer在initial/delta review期间改变HEAD；多次Advisor closure后才完成。

**可前置部分（推断）：** plan precedence已捕获仍必须执行；每个review冻结独立候选，三处违规不能因最终clean抹除。

**流程判断：** 这是并行设计的安全反例：独立worktree可并行，不允许同一reviewed snapshot被写。只失效被改变的review，不重开整feature。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P38 — `zcode-mcp-zcode-generic-subagent-simplification-sectioned-audit.zip`

**PLAN 阶段：** 三section generic simplification；PLAN两个blocker修正，no追加fullreview。

**代码 review / repair / final：** S01一波、S02三波，S03 final因官方runtime证据缺口阻塞。

**可前置部分（推断）：** 在PLAN先声明 generic功能与官方runtime可证能力边界，不因live缺口重写已正确producer。

**流程判断：** 无hardcap但未完成，缺runtime不是转而无限同model思考的理由。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P39 — `zcode-mcp-zcode-runtime-cancellation-late-event-fencing-sectioned-audit.zip`

**PLAN 阶段：** 两section cancellation/late-event fencing。

**代码 review / repair / final：** source摘要有oldpending与finalclean冲突；实际官方两次semantic timeout无finalize，后Advisor#5停止。

**可前置部分（推断）：** cancelintent、deadline、reaped、terminal、finalization应是同一状态/证据模型；liveness不是semanticcompletion。

**流程判断：** 低频Advisor合理；时钟和活动counter增强不等于真实任务完成保证。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



### P40 — `zcode-mcp-zcode-subagent-mcp-20260825-sectioned-audit.zip`

**PLAN 阶段：** 从零通用子agent，五sections；PLAN7+2delta、拒绝两daemon/controlframework。

**代码 review / repair / final：** 约36finding、20waves；S02hardcap后人工闭合，18次live调用；旧同名contract被覆盖与早期估计偏小。

**可前置部分（推断）：** PLAN先验证真实runtime shape/成功oracle，持久化request-result生命周期先接受；不要把文档里的marker要求当runtime必需。

**流程判断：** 早期错误输入假设归用户已声明，不据此责备skill；后续收敛/失败计数不能清零。当前接口一律以本轮新功能说明为准。

证据：包内 `PLAN-AUDIT.md`、`REVIEW-AUDIT.md`、`SKILL-COMPLIANCE.md`；具备原始 ledger 时对照 ledger，统计缺失不填零。



## 9个过滤的辅助包

这些包可以证明具体runtime探测结果，但没有作为一次sectioned流程的完整边界与度量，不进入40个样本的统计。既不删除也不移动用户原文件；只在intake manifest标记。

- `zcode-mcp-advisor-three-case-evidence-final.zip`：runtime/conformance/完整事件辅助材料。

- `zcode-mcp-case3-complete-event-logs-auth-redacted.zip`：runtime/conformance/完整事件辅助材料。

- `zcode-mcp-case3-semantic-900s-full-analysis-logs-auth-redacted.zip`：runtime/conformance/完整事件辅助材料。

- `zcode-mcp-official-runtime-conformance-case-b.zip`：runtime/conformance/完整事件辅助材料。

- `zcode-mcp-official-runtime-conformance-case-c-final.zip`：runtime/conformance/完整事件辅助材料。

- `zcode-mcp-official-runtime-conformance-case-c-prompt-repaired.zip`：runtime/conformance/完整事件辅助材料。

- `zcode-mcp-official-runtime-conformance-case-c-retry.zip`：runtime/conformance/完整事件辅助材料。

- `zcode-mcp-official-runtime-conformance-case-c.zip`：runtime/conformance/完整事件辅助材料。

- `zcode-mcp-official-runtime-conformance.zip`：runtime/conformance/完整事件辅助材料。



## 原始 ledger交叉核对重点

- P05：`S01-REVIEW.md` / `S02-REVIEW.md` / `S03-REVIEW.md`：S01 Admin route因S03 consumer出现才重开；AR4文字有陈旧次序，不能据摘要机械计总波数。

- P12：`evidence/S01-INITIAL-REVIEW.md`、`evidence/S01-FINAL-REVIEW.md`：F001–F005以及重复popup行为，区分PLAN已知路径未实现与新发现。

- P37：`reviews-FINAL-S02-REVIEW.md` 和 `reviews-FINAL-S03-REVIEW.md` 各“Sequence gate violation”小节：S02 initial、S03 initial、S03 sticky delta三次候选移动；与SKILL-COMPLIANCE矛盾。

- P06/P07：相同摘要不是证明共同根因、不是可重复统计的两份完整stage ledger。

- P28：top-level 5/3 与 stage文档0/0并列保留，统计列UNKNOWN；产品等价性证据需另读原始测试，不因度量冲突否定产品。



## 推荐优先顺序

先修多section分支/closed-plan/候选冻结三条确定性问题；再替换过时ZCode契约与Advisor调用；随后以固定六组合的任务特征路由和两writer并行试运行收集数据。不要为了省钱去降低迁移、并发、协议等真实质量门槛。
