# Codex Custom Instructions — V3.8 最小补丁

下面四项应写入全局 Custom Instructions；它们不是某个仓库的局部实现细节。

## 1. 收紧 `$sectioned-feature-development` 自动触发

放在现有的 `$sectioned-feature-development` 触发规则之后：

```markdown
- Merely reading, touching, or passing through a high-risk module does not make a change non-trivial: a local calculation change, an exact-reproduction fix touching at most two behavioral owners, a bounded one-off script, a read-only probe, or a mechanical change should proceed normally unless it materially changes that high-risk contract, crosses another trigger threshold, or its impact cone becomes difficult to bound.
```

并紧接着加入自动触发行为：

```markdown
- When `$sectioned-feature-development` is selected automatically rather than explicitly requested by me, first read the skill, immediately tell me why it triggered and the predicted scope, create and validate the first proportional `.agent-work/PLAN-FULL.md`, then stop before PLAN review and ask for approval using `[PLAN-FULL.md](/absolute/path/to/.agent-work/PLAN-FULL.md)`; do not print the plan body. If I explicitly invoke the skill, continue through completion without this routine approval pause unless a genuine owner or safety decision is required.
```

保留现有的正向触发条件。Skill 的 frontmatter `description` 同时保留同样的 non-trivial prerequisite、反例和显式/自动触发差异，因为 description 负责 Skill 路由，而 Custom Instructions 负责全局触发政策。

## 2. 固定分支基线授权

放在 `## Safety` 中现有的 scoped exception 后：

```markdown
- Under `$sectioned-feature-development`, creating the feature branch/worktree from `main` needs no separate approval. If the current branch is not `main`, do not use it as the base automatically; ask me to choose whether to branch from `main`, branch from the current branch, or first merge the current branch into `main` and then branch from updated `main`. This does not authorize merge, push, reset, cleanup, or disposal of either branch.
```

## 3. 永久禁止 `.agent-work` 进入 Git 历史

放在 `## Safety`：

```markdown
- Treat `.agent-work/**` as local agent operational state: never stage or commit it. Add `.agent-work/` to the repository-local `.git/info/exclude` when needed. If any `.agent-work` path is already tracked, do not untrack or rewrite it automatically; ask before removing it from tracking in a separate process-only commit.
```

并把“只说提交/commit”的命令改为排除该目录：

```markdown
- If I only say `提交` or `commit` without extra instructions, inspect the workspace, exclude temporary/output/system files and all `.agent-work/**` paths, then execute `git add -A -- . ':(exclude).agent-work/**' && git commit -m "type(scope): description" -m "detail"` directly with an appropriate Conventional Commit message; do not add post checks, status audits, or other commit preparation unless I explicitly ask for them.
```

## 4. 在“叠局部补丁”和“改基础 owner”之间请求一次有界选择

放在 `## Maintainability Guardrails`：

```markdown
- Before adding a second implementation of the same validation, normalization, routing, persistence, selection, or state-transition rule—or stacking local guards around a defect owned by shared infrastructure—identify the authoritative owner. If the smallest correct shared-owner fix would materially expand the current edit boundary, stop before coding and ask me to choose between that bounded foundational fix and the smallest local patch, explaining each option's residual risk. Do not interrupt for cosmetic helper extraction, a one-use abstraction, or unrelated refactoring.
```

## 是否需要修改仓库 AGENTS.md

- **不需要普遍修改每个仓库的 AGENTS.md。** 上述四项是用户级长期偏好，应放入全局 Custom Instructions。
- 若某个仓库的 AGENTS.md 自己包含更宽的 Skill 触发规则、要求提交 `.agent-work`，或强制局部 patch，则需在该仓库单独修正冲突。
- Skill 的 `description` 仍必须写触发条件与反例，因为 Agent 在读取 `SKILL.md` 之前通常先依赖 description 做召回/路由。
