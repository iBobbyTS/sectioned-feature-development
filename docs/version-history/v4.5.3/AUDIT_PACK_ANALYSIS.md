# 4.5.3 输入与范围分析

本轮没有新的 Audit Pack 或真实模型执行测试。依据为用户报告、实际 4.5.2 完整项目，以及其中有效的 Skill、模板、Agent developer instructions。之前的 rollout 结论不在本轮重新分析或补救。

## 问题 1：执行模式的间接指代

根 Skill 确实用 `requires the last mode` 代替 `EXECUTE_WITH_COMMITS`；frontmatter 只说 dedicated branch and commits，handoff 仅说 when authorized，parallel reference 只重申多 section。这些并非允许免提交，但拆分阅读时需要额外推导，容易误把分支本身当成已满足模式与提交责任。

实际恢复的是同一条已授权规则：业务 section 数量 >1 或 executable subsection 数量 >1，下一次产品/测试修改前必须选择 EXECUTE_WITH_COMMITS 和独立非 main 分支，并实际执行已有 coherent implementation/repair commits。PLAN_ONLY 可以写多单元计划，但不能写产品；显式 no-commit 冲突需要先解决。不新增“一节恰好一个 commit”或每子项强制独立 commit。

另检查两份运行 Skill、全部 references/templates、七份 Agent 和当前 README。记录了 17 处涉及执行决策的表达明确化；包含同一规则在多个入口的同步，不是 17 个独立缺陷或 17 次已证实事故。清晰的局部代词、技术示例里的 first/last、准确链接到规则的引用保留，详见 WORDING_REVIEW.md。

## 问题 2：universal-first 是实际入口要求，不只是 Agent 漏读

4.5.2 的 router 首句要求 read router and universal；universal 自称用于 every activated PLAN。根 Skill、section-planning、PLAN-review packet、README 和 plan_reviewer developer instructions 都重复这条入口。router 又允许直接跳到记得的 guide，Agent 明确写 Do not preload indexes；concern 只有四个直链而没有独立 INDEX。它们组合后不能确保作者知道当前资料覆盖范围。

4.5.3 改为四个短目录先读，再读实际匹配的专项文件；仅明确未覆盖的部分使用 universal。目录检查不同于读取所有知识文件，不强制四轴全命中，不做笛卡尔积。已有 guide 覆盖相同问题时去重，不适用维度不需要 fallback。独立 reviewer 使用同一顺序但不盲信作者列表。

## 保留边界

不增加运行脚本、dispatch gate、JSON 计划、receipt、审批 hash 或独立 Audit 报告。4.5.2 Audit 启动/恢复/交付段、全部 audit-mode、产品/审查预算、真实委派、原生/ZAS 区分、外部 Advisor 保留。已关闭任务不因更新重新规划；材料缺失保持 UNKNOWN，不补造阅读记录。
