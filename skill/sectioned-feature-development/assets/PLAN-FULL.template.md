# 完整实施计划：<Feature Name>

- 创建时间：<YYYY-MM-DD HH:MM TZ>
- 工作模式：`PLAN_ONLY | EXECUTE_NO_COMMIT | EXECUTE_WITH_COMMITS`
- 仓库：`<path>`
- Feature branch/worktree：`<branch or N/A>`
- Feature base：`<commit>`
- 计划版本：`v1`
- 当前状态：`PLANNING`

<!-- FEATURE-CONTEXT:START -->
## Feature Contract

### 一句话目标

<完成后系统新增或改变的唯一核心结果。>

### 用户/操作者可观察行为

- <行为 1>
- <行为 2>

### 非目标

- <明确不做什么；包括不支持的环境、攻击者、兼容承诺或泛化方向。>

### 全局不变量

- `INV-01`：<始终保持的业务/数据/状态事实>
- `INV-02`：<安全、权限、兼容或恢复不变量>

### 硬约束与权威来源

| ID | 约束 | 权威来源 |
|---|---|---|
| C-01 | <约束> | `<repo path / issue / accepted decision>` |

### 完整功能验收标准

- `R-01`：<行为级、可证伪标准>
- `R-02`：<行为级、可证伪标准>

### 完整功能验证命令

```bash
<command>
```

### Ownership / State Boundary

| Boundary | Authoritative owner | Consumers | Risk |
|---|---|---|---|
| <state/decision> | `<module>` | `<modules>` | `<risk>` |

### Assurance Envelope

- Artifact role / deployment context: <production path, internal tool, test harness, migration utility, etc.>
- Protected assets: <data/state/availability/secrets/etc.>
- Trusted actors/inputs and capabilities: <...>
- Untrusted actors/inputs and capabilities: <...>
- Entry points and trust boundaries: <...>
- Required guarantees: <...>
- Explicit exclusions / non-guarantees: <...>
- Existing authoritative security/privacy policy: `<paths or none>`
- Owner-decision triggers: <what new actor/environment/guarantee requires approval>

### Compatibility / Migration / Rollout / Rollback

- 支持环境：<...>
- 兼容策略：<...>
- 迁移策略：<...>
- 发布/开关：<...>
- 回滚/恢复：<...>
- 可观测性：<...>
- 临时机制清理条件：<...>

### Scope-change Authority

只有 `.agent-work/scope-changes/SC-*.md` 中状态为 `APPROVED` 的记录，才可扩展上述功能或 assurance boundary。Reviewer 评论、repair 方案和聊天记录均不是授权来源。
<!-- FEATURE-CONTEXT:END -->

## Requirement Coverage Matrix

| Requirement | Primary section(s) | Section oracle | Integration oracle | Status |
|---|---|---|---|---|
| R-01 | S01 | <test/check> | CP1 / FINAL | planned |
| R-02 | S02 | <test/check> | FINAL | planned |

## Section Index and Dependency Graph

| ID | Parent | Replan gen | Title | Type | Depends on | Integrates with | Risk | Status |
|---|---|---:|---|---|---|---|---|---|
| S01 | — | 0 | <title> | vertical | — | CP1 | medium | planned |
| S02 | — | 0 | <title> | expand/migrate/contract | S01 | CP1 | high | planned |

```text
S01 -> S02 -> CP1 -> FINAL
```

## Integration Checkpoints

### CP1 — <name>

- Included sections: `S01`, `S02`
- Contracts proved: <...>
- Critical paths: <...>
- Commands/evidence: <...>
- Rollback/disable path: <...>
- Frozen assurance envelope revision: `v1`

## Plan Gate

- [ ] Every requirement maps to section and integration evidence.
- [ ] Dependency graph is acyclic.
- [ ] Every high-risk boundary has one owner, proportional assurance envelope, and oracle.
- [ ] Every new mechanism maps to a current requirement/repository invariant and has a simpler alternative analysis.
- [ ] Speculative generality, unsupported attackers/environments, and future-proofing are explicit non-goals unless approved.
- [ ] Every section is independently implementable, testable, reviewable, and leaves a valid intermediate state.
- [ ] Cross-section contracts and checkpoints are explicit.
- [ ] Refactor and behavior are separated or inseparability is justified.
- [ ] Rollout, rollback, migration, observability, and cleanup are covered.
- [ ] No final “integrate everything” bucket remains.

## Sections

<!-- SECTION:S01:START -->
## S01 — <Section Title>

### 目标

<本 section 唯一主要结果。>

### 行为增量

- <完成后可观察、可验证的行为。>

### 依赖

- Requires: `none`
- Integrates with: `CP1 | none`
- Expected predecessor head: `<filled when contract freezes>`

### 预计范围

- Lineage: `original`
- Replan generation: `0`
- Files/symbols/workflows: `<expected scope>`
- Direct semantic impact cone: `<named callers/consumers/contracts only>`
- Semantic boundaries: `<persistence/security/API/etc.>`
- Estimated behavioral size: `<range>`
- Risk: `low | medium | high`
- Split/replan trigger: <when this section is no longer one finite behavior increment>

### 最低充分设计与复杂度预算

| Proposed mechanism | Requirement/invariant anchor | Simpler alternative | Why insufficient | Removal/rollback condition |
|---|---|---|---|---|
| `<mechanism or none>` | `R-xx / INV-xx / repo path` | <...> | <...> | <...> |

- New services/registries/settings/frameworks allowed: `<none or named items>`
- New assurance guarantees allowed: `<none or copied from feature envelope>`

### 非目标

- <当前 section 明确不处理的内容。>

### 全局不变量

- `INV-01`
- <section-specific invariant>

### 验收标准

- `S01-AC-01`：<触发、期望结果、证据>
- `S01-AC-02`：<边界或失败行为>

### 验证命令

```bash
<targeted test/lint/typecheck/runtime command>
```

保留证据：<log, response, migration result, etc.>

### 发布与恢复

- Intermediate state validity: <...>
- Compatibility/migration: <...>
- Flag/rollout: <...>
- Rollback/recovery: <...>
- Observability: <...>

### 延后项

- <none or assign to a named existing section>
<!-- SECTION:S01:END -->

<!-- SECTION:S02:START -->
## S02 — <Section Title>

### 目标

<本 section 唯一主要结果。>

### 行为增量

- <...>

### 依赖

- Requires: `S01`
- Integrates with: `CP1`
- Expected predecessor head: `<filled when contract freezes>`

### 预计范围

- Lineage: `original`
- Replan generation: `0`
- Files/symbols/workflows: `<...>`
- Direct semantic impact cone: `<...>`
- Semantic boundaries: `<...>`
- Estimated behavioral size: `<...>`
- Risk: `high`
- Split/replan trigger: <...>

### 最低充分设计与复杂度预算

| Proposed mechanism | Requirement/invariant anchor | Simpler alternative | Why insufficient | Removal/rollback condition |
|---|---|---|---|---|
| `<mechanism or none>` | `R-xx / INV-xx / repo path` | <...> | <...> | <...> |

- New services/registries/settings/frameworks allowed: `<none or named items>`
- New assurance guarantees allowed: `<none or copied from feature envelope>`

### 非目标

- <...>

### 全局不变量

- `INV-01`

### 验收标准

- `S02-AC-01`：<...>

### 验证命令

```bash
<command>
```

### 发布与恢复

- Intermediate state validity: <...>
- Compatibility/migration: <...>
- Flag/rollout: <...>
- Rollback/recovery: <...>
- Observability: <...>

### 延后项

- <none or named section>
<!-- SECTION:S02:END -->

## Decisions

| ID | Question | Owner/source | Status | Affected artifacts |
|---|---|---|---|---|
| D-01 | <...> | <...> | open/accepted | <...> |

## Scope-change Ledger

| ID | Proposed boundary change | Status | Owner decision | Plan/contract revision |
|---|---|---|---|---|
| — | — | — | — | — |

## Deferred Work

| ID | Item | Owner section | Required before merge? | Status |
|---|---|---|---|---|
| DW-01 | <...> | S02 | yes/no | planned |
