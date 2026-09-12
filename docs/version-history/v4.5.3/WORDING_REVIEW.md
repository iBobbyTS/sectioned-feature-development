# 有效指令的模糊指代核查

范围：两份安装 Skill 的 Markdown/TOML/YAML、七份 Agent、当前 README/AGENTS 与项目规则；不改历史 PROMPT、旧版本报告、脚本中的数组/时间逻辑。关键词扫描后按职责逐项判断。

共明确化 **17 处**涉及执行决策的语句，含同一规则的多个入口；仅 `requires the last mode` 是用户本轮直接指出的漏要求实例，其余为同类可读性风险，并非已证实的独立故障。

| # | 文件 | 原表达 | 明确后的对象／条件 |
|---:|---|---|---|
| 1 | `skill/sectioned-feature-development/SKILL.md` | requires the last mode and a dedicated non-main feature branch before further code edits. Resolve an explicit no-commit conflict with the owner. | requires `EXECUTE_WITH_COMMITS` and a dedicated non-main feature branch **before the next product/test edit**. Record the selected mode and branch explicitly in PLAN-FULL and FEATURE-STATE. Do not treat an existing feature branch, a plan-only request or an explicit no-commit instruction as permission to omit the execution-mode decision; resolve any conflict before implementation. |
| 2 | `skill/sectioned-feature-development/SKILL.md` | Multiple sections/subsections require a dedicated branch and commits. | More than one section or executable subsection requires EXECUTE_WITH_COMMITS and a dedicated non-main branch. |
| 3 | `skill/sectioned-feature-development/SKILL.md` | as specified below **before planning or resumed dispatch** | under **Audit handoff — required, not an extra product gate** **before planning or resumed dispatch** |
| 4 | `skill/sectioned-feature-development/SKILL.md` | If an earlier `MESSAGE` conflicts with `FINAL_ANSWER`, the latter controls | If an earlier `MESSAGE` conflicts with `FINAL_ANSWER`, `FINAL_ANSWER` controls |
| 5 | `skill/sectioned-feature-development/SKILL.md` | ask the user's three-way base choice unless this is continuation on the already authorized feature branch | ask the user to choose branching from `main`, branching from the current branch, or merging the current branch into `main` before branching, unless continuing the already authorized feature branch |
| 6 | `skill/sectioned-feature-development/SKILL.md` | Later corrections mark conflicting earlier guidance `SUPERSEDED`; do not preserve both. | Later corrections mark conflicting earlier guidance `SUPERSEDED`; retain superseded guidance as provenance only, not as an active requirement. |
| 7 | `skill/sectioned-feature-development/references/scope-control.md` | If the last answer is yes, omit it. | If the feature remains correct without the proposed mechanism, omit that mechanism. |
| 8 | `skill/sectioned-feature-development/references/model-routing.md` | Only the first supports changing implementation models. | Only a model/semantic error supports changing implementation models; plan/requirement errors, environment/tooling errors and missing evidence do not by themselves justify changing the implementation model. |
| 9 | `skill/sectioned-feature-development/references/section-planning.md` | the latter is not solved by extending the plan indefinitely. | `PLAN_ALREADY_REQUIRED_BUT_NOT_IMPLEMENTED` is not solved by extending the plan indefinitely. |
| 10 | `skill/sectioned-feature-development/references/section-planning.md` | the latter needs the exact requirement and production test in the task packet, not more plan reviewers. | `PLAN_ALREADY_REQUIRED_BUT_NOT_IMPLEMENTED` needs the exact requirement and production test in the task packet, not more plan reviewers. |
| 11 | `skill/sectioned-feature-development/references/activation-and-orchestration.md` | under the explicit parallel exception below. | under Parallel limits and violations (#parallel-limits-and-violations). |
| 12 | `skill/sectioned-feature-development/references/recovery-and-migration.md` | on non-`main`, ask the three-way base choice; | on an unrelated non-`main` branch, ask the user to choose a base: `main`, the current branch, or `main` after an explicitly authorized merge; continuing an already authorized feature branch needs no repeat choice; |
| 13 | `skill/sectioned-feature-development/references/activation-and-orchestration.md` | Multiple business sections or multiple executable children require committed work on a dedicated non-main branch. | More than one business section or more than one executable subsection requires `EXECUTE_WITH_COMMITS` and a dedicated non-main feature branch before further product/test edits. Write the mode and authorized branch into PLAN-FULL and FEATURE-STATE; a no-commit conflict must be resolved before implementation. |
| 14 | `skill/sectioned-feature-development/references/parallel-execution.md` | `len(sections)>1` implies `EXECUTE_WITH_COMMITS`, a non-main dedicated feature branch and coherent implementation/repair commits. This also holds after late adoption or a plan revision adds a second section. | More than one business section **or more than one executable subsection** requires `EXECUTE_WITH_COMMITS`, a dedicated non-main feature branch and coherent implementation/repair commits. This also holds after late adoption or a plan revision crosses either threshold. |
| 15 | `skill/sectioned-feature-development/references/artifact-lifecycle.md` | Commit only intended code/tests/docs when authorized. | In `EXECUTE_WITH_COMMITS`, make the coherent implementation/repair commits required by the approved workflow, containing only intended product code/tests/docs. Do not skip these commits merely because the work is already on a feature branch. In `EXECUTE_NO_COMMIT`, do not commit; that mode cannot execute more than one business section or more than one executable subsection. |
| 16 | `skill/sectioned-feature-development/SKILL.md` | - `PLAN_ONLY`, `EXECUTE_NO_COMMIT`, and `EXECUTE_WITH_COMMITS` remain. | - Execution modes: `PLAN_ONLY` permits planning/review only; `EXECUTE_NO_COMMIT` permits authorized implementation without commits; `EXECUTE_WITH_COMMITS` requires the approved coherent implementation/repair commits. A multi-unit plan may be prepared in `PLAN_ONLY`; product/test implementation must obey the following requirement. |
| 17 | `README.md` | 大于一个业务 section 或一个可执行 subsection 必须独立分支与提交。 | 业务 section 数量 >1 **或**可执行 subsection 数量 >1，必须在下一次产品/测试修改前使用 `EXECUTE_WITH_COMMITS` 和独立非 main feature branch，并按原有 coherent implementation/repair 节奏提交；这不是新增“每节恰好一个 commit”的要求。 |

## 扫描后保留的表达

- source catalog 的来源编号、技术用例中的 first/last，以及术语原文不做机械替换。
- “两个包属于同一个 feature/run”等对象紧邻而明确的 both 保留。
- code-review 的 DELEGATED_PASS/standalone 分支已直接命名，不因出现 below 就改验收规则。
- 明确链接的局部规则引用不展开成重复清单；Audit 同段定义的结果与对象保持。
- 所有历史和新 PROMPT 中的原始引文原样保留。

## 扫描结果的含义

没有以正则替代语义检查，不宣称枚举了自然语言所有可能歧义。此次对职责选择有影响的对象被直接命名，不新增自动 linter 给每个产品任务运行。完整修改可由项目 patch 对照。
