# 本轮审计：逐包、逐阶段与可前移问题

## 证据和统计边界

输入49个子ZIP。40个含流程审计身份/需求/PLAN或review材料；9个为runtime/conformance/完整事件日志等辅助证据。分类按内容，不依赖名称。本轮不是对40个产品重新运行测试的merge认证。仅以原始report/Git/source/trace优先于总结；无法对齐的finding和波数不补造精确总数。无人工活动的墙钟空档不归为模型开发时间。

本轮不以流程行数、review数量或单次零发现推导删门禁。可证实的简化只有：相同证据的重复验证、成功的小任务不触发、未证明composition为空时不再增integration review，以及无关audit样本不重复计数。它们大部分已经被3.9允许，因此不新增一套精简流程。

## 每个流程包

### P01 — API-sol-usage-export-sectioned-audit

**阶段证据：** PLAN 已抓 SQL/projection、价格/备份和精确例子；实现与审查仍有8项发现、3波修复。

**划分/PLAN/执行结论：** 表示/计价规则与脚本数据目标可作为父业务合同，查询/导出步骤按需要做内部增量；不能把产品导出的 token 数据当开发成本。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P02 — AnyUpright-debug-app-flow-deescalation-sectioned-audit

**阶段证据：** 主动从 sectioned 降级到本地调试脚本；无正式代码 review。

**划分/PLAN/执行结论：** 负触发是成功，不是“未遵守skill”；保留3.9小改路径，不给成功降级补计划与审查。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P03 — AnyUpright-fcp-motion-analysis-time-domain-sectioned-audit

**阶段证据：** PLAN 冻结 host/time-domain；code review 发现未知host fail-open、frame tolerance等，两波修复。

**划分/PLAN/执行结论：** 可在PLAN列来源时钟→目标时域→未知host的拒绝策略，不能把缺失输入默认为可转换。保留代码回归。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P04 — codex-rosetta-availability-snapshot-cooldown-recovery-20260901-sectioned-audit

**阶段证据：** PLAN/code 均 clean，无 repair。

**划分/PLAN/执行结论：** 没有证据说明现有review多余；保持基线，不因零发现自动减轮次。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P05 — codex-rosetta-codex-cockpit-provider-health-sectioned-audit

**阶段证据：** PLAN已有控制面约定；早期section漏 production Admin route，直到后续consumer阶段补齐。S02 generation/error分类也返工；ledger时序不完全一致。

**划分/PLAN/执行结论：** 在PLAN按 producer→Admin route→probe→state→router写真实调用链；若中间层尚不可消费，使用同父subsection而非提前接受一个伪完整section。计数不强行调和。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P06 — codex-rosetta-failover-429-cooldown-20260826-sectioned-audit

**阶段证据：** 429 cooldown 与下一pack的 PLAN-AUDIT/REVIEW-AUDIT 出现相同内容。

**划分/PLAN/执行结论：** 存在跨包摘要污染，review数量与root cause不能按两份独立样本相加；只保留能定位到原artifact的结论。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P07 — codex-rosetta-failover-connectivity-cooldown-20260826-sectioned-audit

**阶段证据：** Connectivity cooldown 的阶段摘要与429包相同。

**划分/PLAN/执行结论：** 同上；数据冲突影响流程统计而非自动判产品错误。该样本不足以证明该增加/删除哪轮review。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P08 — codex-rosetta-glm53-catalog-update-20260902-sectioned-audit

**阶段证据：** Catalog配置、descriptor、serializer、filter的相互关系是主要边界；真实外部多轮模型验证未完成。

**划分/PLAN/执行结论：** PLAN列字段生产/默认/投影/过滤路径；未运行的live结果保持gap，不把缺日志写成零缺陷。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P09 — codex-rosetta-remove-observability-diagnostics-sectioned-audit

**阶段证据：** PLAN缩小到实际活跃logging/package aliases；两次有界修复。

**划分/PLAN/执行结论：** 先用可定位删除清单冻结scope；不要为了删除观测代码新建替代framework。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P10 — lmdo-website-create-project-needs-score-sectioned-audit

**阶段证据：** PLAN覆盖复选框默认和父行为；代码阶段发现400失败后关窗/重开、相同payload事件identity。

**划分/PLAN/执行结论：** PLAN用失败→关闭→重开→再提交的用户序列作为oracle，而不是只说“支持retry”。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P11 — lmdo-website-dynamic-performance-groups-20260831-sectioned-audit

**阶段证据：** 五个跨schema/auth/board/invite/miniprogram section；同一membership身份贯穿。

**划分/PLAN/执行结论：** 先冻结共同身份/权限合同；跨consumer的独立业务可以父项并行，但sharedowner需先接受，内部模块可subsection。现有总计存在歧义不精算。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P12 — lmdo-website-group-instrument-inline-management-20260903-sectioned-audit

**阶段证据：** PLAN曾抓7 blockers、2 owner decisions；实现仍遗漏已要求的scoped candidates、auth入口，final有stale popup。

**划分/PLAN/执行结论：** 大多不是少一次PLAN review，而是TASK没有消费已批准要求。用真实生产入口AC→任务→测试/Handoff追踪，保持review。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P13 — lmdo-website-group-to-lead-category-sectioned-audit

**阶段证据：** 三个权限/Admin/consumer/schema边界。

**划分/PLAN/执行结论：** PLAN先列授权矩阵与真实入口。相同语义规则不可在多个owner各自实现；consumer不能绕过未通过父合同。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P14 — lmdo-website-management-list-ui-20260826-sectioned-audit

**阶段证据：** 两个UI section；部分review深度由owner数量推断；完成后出现snippet consumer修正。

**划分/PLAN/执行结论：** 保留语义/oracle模型分级，不只按文件数。完成后的新用户变更重新分类，不把旧feature永远扩下去。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P15 — lmdo-website-pinyin-user-search-sectioned-audit

**阶段证据：** PLAN从3到4节因漏loader；代码阶段发现多音后缀组合指数增长，改为有界算法。

**划分/PLAN/执行结论：** owner inventory加最坏候选规模和复杂度上限可前移。GLM服务故障不是产品finding，更不是审查收益。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P16 — lmdo-website-pr104-must-fix-sectioned-audit

**阶段证据：** 原始7个must-fix、7个不做被冻结；长Git范围含72个历史commits。

**划分/PLAN/执行结论：** 只统计feature真实diff，不把main历史成本算本轮。保留audit-remediation finding-set冻结，拒绝持续全仓audit。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P17 — lmdo-website-project-detail-multipage-sectioned-audit

**阶段证据：** S01–S03完成后用户增加shared shell/header，旧PLAN追加S04。

**划分/PLAN/执行结论：** 直接支持closed-feature规则：新需求重新评估；除非显式重开，不修改旧PLAN验收边界。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P18 — lmdo-website-project-summary-inline-autosave-sectioned-audit

**阶段证据：** 约4文件却出现5波：normalization、navigation、重复POST、共享form和反馈状态。PLAN已有single-flight约定。

**划分/PLAN/执行结论：** 高耦合小diff不是廉价任务；优先给足推理能力。明确失败/重复/导航矩阵；不能靠拆更多独立section解决同一state machine。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P19 — lmdo-website-remove-unassigned-performance-group-20260902-sectioned-audit

**阶段证据：** 五节删除unused group；巨量删除含snapshot；多轮projection/lock/template修复。

**划分/PLAN/执行结论：** 不能把生成文件删除行数当推理复杂度。PLAN冻结consumer/deletioninventory及迁移后不变量，保留破坏性验证。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P20 — lmdo-website-shared-personnel-management-20260825-sectioned-audit

**阶段证据：** 四节；PLAN拒绝额外idempotence保证，保留canonical transaction/foundation选择；migration返工较多。

**划分/PLAN/执行结论：** 保留necessity-before-correctness。父业务共同transaction不能为便宜模型拆成独立验收；内部建模/迁移/消费者可串行checkpoint。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P21 — pppms-portal-native-acquisition-closeout-cleanup-sectioned-audit

**阶段证据：** 三条清理业务；PLAN移除宽泛compat shim、额外initial review和擅加--once保证；code零修复。

**划分/PLAN/执行结论：** PLAN必要性过滤已有效；不因此再取消原review。保留精确删除/保留owner清单。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P22 — pppms-portal-native-acquisition-dead-path-cleanup-sectioned-audit

**阶段证据：** 三节清理；PLAN明确11项删除及保留superclass hook/canonical primitives，移除重复每节Django broad check；代码全clean。

**划分/PLAN/执行结论：** 这是有直接审计依据的验证去重：保留final gate和targeted checks，不在每小节重复相同broad suite。不外推为删review职责。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P23 — pppms-portal-native-acquisition-performance-sectioned-audit

**阶段证据：** 四个admission/time/spatial/batchowner；真实失败覆盖rollback、seed response-loss、startup reconciliation、range eligibility，局部rebound曾扩大。

**划分/PLAN/执行结论：** PLAN用正常/丢响应/重启/回滚failure grid；同owner修复优先保留现实现，不用lineage/rebound反复重做。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P24 — pppms-portal-top-banner-only-operational-errors-sectioned-audit

**阶段证据：** 单纵向section；PLAN提前补per-owner recovery矩阵和必要check/build/restart；code4findings2waves，含dead field、文档冲突、live recovery证据。

**划分/PLAN/执行结论：** 父合同须区分全局banner与单page endpoint失败；各page自动/手动/remount恢复必须逐项，而不是全局声称“banner exclusive”。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P25 — pppms-portal-unified-operator-ui-sectioned-audit

**阶段证据：** 五路线UI、共享foundation；中途Header palette更正。Section与integration发现overflow/state/errorowner/旧oracle；最终live readiness区间仍不可观测。

**划分/PLAN/执行结论：** 要求更正只supersede对应Header。PLAN事先区分可由UI证明的结果与backend readiness；不可观测gate不得靠无限轮换等待策略硬凑green。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P26 — scsc-mms-datatable-041-migration-sectioned-audit

**阶段证据：** 五节DataTable migration；两次PLAN+delta抓request uniqueness/defaultsize20/participantinventory、未授权pagesize persistence、FSII API compatibility；后续retry与lifecycle证据返工。

**划分/PLAN/执行结论：** producer/consumer/liststate生命周期可在PLAN前移；无credentials的browser仍是环境gap。明确direction参数和旧prop移除inventory。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P27 — scsc-mms-dropdown-typeahead-member-select-20260827-sectioned-audit

**阶段证据：** 两节；PLAN补包同步顺序、member/temporary边界、native validity bridge；final REV-001后repair+delta。

**划分/PLAN/执行结论：** 跨包步骤需显式产物依赖，不能并行未发布producer与consumer；摘要信息有限，不推测REV-001根因。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P28 — scsc-mms-fixed-project-catalog-20260825-sectioned-audit

**阶段证据：** Verdict声称5findings3waves，PLAN/REVIEW却描述one-owner migration squash、0findings0waves。

**划分/PLAN/执行结论：** 实质统计冲突：仅可定位原始证据作参考，不给该pack编造统一结论或纳入defect yield。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P29 — scsc-mms-fsii-member-nonmember-parity-sectioned-audit

**阶段证据：** 两纵向节；PLAN移除persistence过度范围、补docs/requiredness roundtrip；S02五blockers+gap，一波修复再加survey-typevalidation，deltaA+freshB。

**划分/PLAN/执行结论：** 表单→API→持久化→读回所需/可选字段及runtime discriminator可前移；已有要求遗漏仍是执行问题。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P30 — scsc-mms-fsii-survey-filter-data-table-20260828-sectioned-audit

**阶段证据：** 单节；PLAN冻结正式包版本而非本地未发布版本、Edmonton year和docs。ONE initial clean，无额外final或integrationreview；feature browser gate仍完成。

**划分/PLAN/执行结论：** 保留已有ONE/验证分层，不再新增“轻量lane”。无发现不意味着此前review没必要。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P31 — scsc-mms-fsii-survey-modal-multiselect-20260903-sectioned-audit

**阶段证据：** 单节；PLAN补文档owner；initial a11y name缺陷一波，delta原reviewer+freshfinal；browsergap按冻结合同处理。

**划分/PLAN/执行结论：** 控件accessible name可作为UI AC具体例子；代码实现验证仍必须。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P32 — scsc-mms-member-nonmember-unification-20260902-sectioned-audit

**阶段证据：** 三节真实schema/consumer迁移，却EXECUTE_NO_COMMIT。PLAN补parent rebuild/name carrier/public validation；后续多轮及stale tests。

**划分/PLAN/执行结论：** 直接落实用户规则：多section或多可执行子项强制独立branch+commit。新schema/consumer需安全中间态和父级joint oracle。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P33 — scsc-mms-remove-child-member-website-contact-20260825-sectioned-audit

**阶段证据：** 一个原子迁移；PLAN reviewer两次无有效artifact后再派第三次；code two waves包括缺非目标数据保持oracle和fullsuite旧fixture。

**划分/PLAN/执行结论：** 保留一次基础设施重试上限；原子迁移同时证明目标删除与非目标不变。fullsuite缺口不等于再启动通用full rediscovery。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P34 — zcode-mcp-case3-review-tool-guidance-sectioned-audit

**阶段证据：** 两节、用户三波cap；S01实施早于PLAN approval；Case3多个runtime timeout未得final artifact转Advisor。

**划分/PLAN/执行结论：** 恢复真实plan gate和stage barrier。运行时活动不是语义完成；不把timeout当代码repair波。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P35 — zcode-mcp-operational-general-agent-closure-20260827-sectioned-audit

**阶段证据：** S06–S08流程闭合，12review/13findings/5waves主要据fake和公开工具；没有官方ZCode live证明。

**划分/PLAN/执行结论：** 设计/代码与真实runtime声明分开。使用来源和环境身份，不因模型final_text成功就宣称产品live通过。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P36 — zcode-mcp-review-safety-progress-evidence-review-safety-progress-evidence-sectioned-audit

**阶段证据：** 用户明确授权permission/hook安全与progress证据；PLAN补Rust/JS effectivepolicy/provenance/cursor/plugin seam，代码多边界修复，最后sectionclean。

**划分/PLAN/执行结论：** 安全工作是本feature的真实authority，不能按历史反过度设计经验一律删除。全链policy矩阵可前移，真实行为验证仍保留。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P37 — zcode-mcp-zcode-final-generic-agent-convergence-sectioned-audit

**阶段证据：** PLAN纠正group_id及live/cleanB循环；summary称顺序合规，S02/S03原review记载3次审查期间HEAD被writer推进。

**划分/PLAN/执行结论：** 按候选冻结+独立worktree，而不是全feature全局串行。审查期间写入只使受影响证据失效，禁止把summary当真实actor状态。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P38 — zcode-mcp-zcode-generic-subagent-simplification-sectioned-audit

**阶段证据：** 三节简化；PLAN2blockers；S01一波、S02三波、S03liveblocked。

**划分/PLAN/执行结论：** 保留未完成状态，不以“简化已做完/没触发hardcap”推断验收完成；无需补新机制。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P39 — zcode-mcp-zcode-runtime-cancellation-late-event-fencing-sectioned-audit

**阶段证据：** 两节cancel late-fencing；summary/原artifact pending-final有冲突，两次runtime语义超时没有final报告，转Advisor。

**划分/PLAN/执行结论：** 任务活跃、heartbeat和终态success分别记录；同generation取消/late-result矩阵宜前移，外部runtime故障单列。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

### P40 — zcode-mcp-zcode-subagent-mcp-20260825-sectioned-audit

**阶段证据：** 从零5节；PLAN7findings+2delta，拒绝二daemon；后续多reviews/repairs/livecalls且旧contract覆写。

**划分/PLAN/执行结论：** 用户已承认早期未probe的错误前提不归咎skill。新任务先真实有限probe；保留合同revision/authority，不因新接口推翻所有accepted lineage。

原始证据定位：`PLAN-AUDIT.md`；`REVIEW-AUDIT.md`；`AUDIT-VERDICT.md`。原包与artifact SHA-256见`AUDIT_INTAKE.json`。

## 辅助包：不算独立feature

- AUX01 `zcode-mcp-advisor-three-case-evidence-final`：保留原包身份与哈希，仅供真实runtime/事件证明；不纳入section、repair、review、模型成本独立样本。
- AUX02 `zcode-mcp-case3-complete-event-logs-auth-redacted`：保留原包身份与哈希，仅供真实runtime/事件证明；不纳入section、repair、review、模型成本独立样本。
- AUX03 `zcode-mcp-case3-semantic-900s-full-analysis-logs-auth-redacted`：保留原包身份与哈希，仅供真实runtime/事件证明；不纳入section、repair、review、模型成本独立样本。
- AUX04 `zcode-mcp-official-runtime-conformance`：保留原包身份与哈希，仅供真实runtime/事件证明；不纳入section、repair、review、模型成本独立样本。
- AUX05 `zcode-mcp-official-runtime-conformance-case-b`：保留原包身份与哈希，仅供真实runtime/事件证明；不纳入section、repair、review、模型成本独立样本。
- AUX06 `zcode-mcp-official-runtime-conformance-case-c`：保留原包身份与哈希，仅供真实runtime/事件证明；不纳入section、repair、review、模型成本独立样本。
- AUX07 `zcode-mcp-official-runtime-conformance-case-c-final`：保留原包身份与哈希，仅供真实runtime/事件证明；不纳入section、repair、review、模型成本独立样本。
- AUX08 `zcode-mcp-official-runtime-conformance-case-c-prompt-repaired`：保留原包身份与哈希，仅供真实runtime/事件证明；不纳入section、repair、review、模型成本独立样本。
- AUX09 `zcode-mcp-official-runtime-conformance-case-c-retry`：保留原包身份与哈希，仅供真实runtime/事件证明；不纳入section、repair、review、模型成本独立样本。

## 可以前移，但不能增加通用PLAN审查轮次

1. Producer–consumer完整性：P05、P13、P26、P27。计划给出真实生产route/serializer/consumer，不提前接受尚无consumer的半功能；有共同不变量则父section内设subsection。
2. Representation/precedence：P01、P03、P08、P29。default/null/missing/invalid/allowed domain与准确范围分开，明确权威数据源；不是遍历全仓schema。
3. Interaction lifecycle：P10、P12、P18、P24、P39。用重复提交、失败重试、关闭重开、导航、取消、迟到结果的具体用户序列；已有AC却没实现属于执行缺陷。
4. Cardinality/algorithm bounds：P15。输入规模和候选爆炸可以在计划阶段用小oracle否证，不靠大段抽象性能宣言。
5. Validation/环境边界：P22、P25、P30、P33–P40。预先区分可运行gate、凭据blocked、runtime活动与语义成功；不为缺环境建立替代oracle。

## 必须由执行链而非更长PLAN解决

P12/P18已有要求仍遗漏；P34计划未批就写；P37review HEAD被修改。由持久TASK、真实launch receipt、handoff、review冻结和父级admission处理。P06/P07/P28冲突数据不能用“再审一次代码”修复。
P17支持完成后新请求独立分类；P32支持多section commit模式。其余没有证明的3.9职责不删。
模型分级保留用户授权的4.0策略，但本批多数是旧Sol/all-Sol或未知effort，不能据此宣称Astra/Luna/Terra路由被实测验证。新Audit记录六项任务特征、真实模型、repair升级、全成本和escaped defects。
