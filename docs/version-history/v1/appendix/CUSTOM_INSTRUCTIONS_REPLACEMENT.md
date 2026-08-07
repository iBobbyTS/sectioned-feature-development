# 建议替换到 Codex Custom Instructions 的大变更规则

用下面内容替换当前 `If it's a non-trivial change and edits may exceed 300 lines or more` 整段。详细 state machine 放入 skill，Custom Instructions 只保留触发、权限和不可违背的总规则。

```markdown
- For a non-trivial or high-risk change, use `$sectioned-feature-development` when any of the following applies: expected behavioral edits may exceed roughly 300 lines; more than 3 modules or workflows are affected; the change crosses persistence, schema, security, permissions, tenancy, routing, money, time, units, concurrency, background jobs, public API, deployment, or shared-state boundaries; the impact cone is difficult to bound; or a previous whole-change implementation/review failed to converge.
- A planning or review-only request does not authorize branch creation or commits. Resolve the skill mode as `PLAN_ONLY`, `EXECUTE_NO_COMMIT`, or `EXECUTE_WITH_COMMITS` from the user's explicit request and governing repository instructions.
- In an authorized implementation run:
  - Use a feature branch; use separate worktrees only for dependency-independent parallel sections.
  - Write the complete feature contract, requirement coverage, dependency graph, integration checkpoints, and reviewable sections to `.agent-work/PLAN-FULL.md`.
  - Prefer vertical behavior sections. Allow a separate enabling refactor only when it creates a tested seam required by named later sections.
  - Before each section, extract the stable feature context and current section to `.agent-work/PLAN.md`, freeze `.agent-work/sections/{SECTION_ID}-CONTRACT.md`, and record the exact section base.
  - Use the configured `sol-medium` profile for an ordinary implementation section and `sol_high` for architecture, migration, security, concurrency, or other high-risk implementation work.
  - Run meaningful targeted checks and write `.agent-work/sections/{SECTION_ID}-HANDOFF.md`; commit the coherent section only when commits are authorized.
  - Use a clean `sol_xhigh` reviewer with `$code-review` in `SECTION` mode for exactly one full discovery pass over the stable section range. Write results to `.agent-work/reviews/`.
  - Freeze accepted finding IDs and acceptance criteria. Use `sol_high` to repair only authorized `Agent-Fixable` findings. Review only the repair delta and invalidated impact cone in `DELTA` mode; run another full section review only after an explicit reset trigger.
  - Do not require two consecutive empty whole-section reviews. Accept a section when blocking findings are closed, required coverage and checks are complete or explicitly bounded, and repair closure has independent evidence.
  - Use a soft cap of 3 repair waves and a hard cap of 5. At the hard cap, stop and diagnose specification gap, weak oracle, architecture conflict, scope explosion, unstable base, environment gap, or model/harness limitation.
  - Do not start a dependent section while the current section is blocked. A `section-accepted` verdict is provisional and does not mean the whole feature is mergeable.
  - Run planned cross-section integration checkpoints. After all sections are accepted, use a clean `sol_xhigh` reviewer with `$code-review` in `INTEGRATION` mode over the complete feature range, focusing on original acceptance criteria, cross-section contracts, end-to-end behavior, migration, rollout/rollback, security, reliability, observability, and deferred-work closure.
  - Delete transient `.agent-work/PLAN.md` only after its durable contract, handoff, review, and state records exist. Move `.agent-work/PLAN-FULL.md` to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md` after final reporting.
- Stop whenever an accountable user decision is required for safe semantics, compatibility, migration, rollout, or risk acceptance.
```

## 为什么建议引用 skill，而不是继续扩大全局指令

- Skill 可以通过 `references/` 渐进加载详细规则，避免每次 Codex 任务都占用完整上下文。
- 模板与提取脚本可以随 workflow 单独版本化和验证。
- `code-review` 的 SECTION/DELTA/INTEGRATION 细节只在相关任务加载。
- 模型与 harness 继续进化时，可以修改 skill，而不用不断膨胀通用 Custom Instructions。
