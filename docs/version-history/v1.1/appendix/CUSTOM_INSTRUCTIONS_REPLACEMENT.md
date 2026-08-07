# 建议替换到 Codex Custom Instructions 的规则

目标：Custom Instructions 只保留**触发条件、skill 路由和权限委托**。Section 拆分、计划格式、subagent profile、commit cadence、review/repair 收敛、integration gate、归档等流程细节全部由 `$sectioned-feature-development` 维护。

## 1. Safety：保留通用 no-commit，并增加窄范围授权

将当前：

```markdown
- Do not commit, push, or create pull requests unless I explicitly ask for that action.
```

替换为：

```markdown
- Do not commit, push, or create pull requests unless I explicitly ask for that action.
- Scoped exception: when `$sectioned-feature-development` is triggered for an implementation task, it is explicitly authorized to create/switch the feature branch and make the bounded implementation and repair commits required by that skill without separate per-commit approval. This exception does not authorize push, merge, pull-request creation, history rewriting, reset, clean, or deletion of user work.
```

这样仍然保留默认的“不得 commit”，但在进入该 workflow 时由 **Custom Instructions 自己明确授予例外**。Skill 内同时声明：只有存在这条 scoped delegation 时，才把它解释为 `EXECUTE_WITH_COMMITS`；skill 不能凭自身扩大权限。

## 2. Maintainability Guardrails：只保留触发条件 + skill 路由

删除当前从：

```markdown
- If it's a non-trivial change and edits may exceed 300 lines or more, must:
```

开始的详细实现流程，替换为：

```markdown
- For a non-trivial implementation, must use `$sectioned-feature-development` when any of the following applies: expected behavioral edits may exceed roughly 300 lines; more than 3 modules, packages, services, pages, or workflows are affected; the change crosses a high-risk semantic boundary; architecture or state ownership changes; the impact cone is difficult to bound; or a previous whole-change implementation/review failed to converge.
- When triggered, `$sectioned-feature-development` is the authoritative workflow; do not duplicate its implementation, review, repair, integration, commit-cadence, or archival procedure in these Custom Instructions.
```

## 3. 为什么触发条件同时写在 Custom Instructions 和 skill description

这是有意的双重触发，而不是应删除的重复：

- **Custom Instructions**：提供全局硬路由，确保满足条件的大功能不会被当成普通实现直接展开。
- **Skill frontmatter `description`**：是 skill 自身的匹配/召回入口；即使调用发生在其他上下文，skill 仍能根据同一组条件被正确选择。
- 两处应保持**同一判定语义**。流程细节则只存在于 skill body/references，避免真正的双份维护。

当前 `$sectioned-feature-development` 的 description 使用同一组触发条件：

1. expected behavioral edits may exceed roughly 300 lines；
2. more than 3 modules/packages/services/pages/workflows；
3. crosses a high-risk semantic boundary；
4. architecture or state ownership changes；
5. impact cone is difficult to bound；
6. previous whole-change implementation/review failed to converge。

这里的 300 行只是 trigger signal，不是风险定义；例如很小的权限、schema 或并发修改仍可能因高风险边界触发。
