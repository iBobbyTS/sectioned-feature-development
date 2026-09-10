# Sectioned Feature Development 4.5.1

本版纠正 4.5 的知识分类：**domain 与 language 独立，框架／运行时／平台再放入 adapters**。覆盖范围不再局限于用户举例；仅改规划资料与接线，不增加脚本机械校验、流程阶段、review 轮数或模型组合。

## 四轴组合式规划

入口是 [router](skill/sectioned-feature-development/references/planning/router.md)。先读 universal，然后按当前变更的真实证据选择各轴；无需每轴都选，不读取全库，也不生成语言×领域组合模板。

| 轴 | 现有覆盖 | 文件入口 |
|---|---|---|
| **工程领域 domain：14 类** | Web 前端、后端服务、全栈、桌面应用、移动应用、CLI/自动化、库/SDK、系统/常驻服务、云平台/DevOps、数据工程、AI/ML、科学计算、嵌入式/IoT、游戏/实时应用 | [domains](skill/sectioned-feature-development/references/planning/domains/INDEX.md) |
| **语言 language：20 份指南** | JavaScript、TypeScript、Python、Java、C#、C、C++、Go、Rust、Swift、Kotlin、PHP、Ruby、Dart、SQL、Bash/POSIX shell、PowerShell、R、Lua、HTML/CSS | [languages](skill/sectioned-feature-development/references/planning/languages/INDEX.md) |
| **技术适配 adapter：19 份** | Frameworks：Svelte/SvelteKit、React、Next.js、Vue/Nuxt、Angular、Django、FastAPI、Spring、ASP.NET Core、Rails、Laravel、Flutter、SwiftUI/AppKit；Runtimes：Node.js、Tokio；Platforms：macOS、Apple mobile、Android、browser | [adapters](skill/sectioned-feature-development/references/planning/adapters/INDEX.md) |
| **横切 concern：4 份** | data-evolution、async-lifecycle、external-integration、performance | 在 router 中按实际改变的语义选择 |

这里的 domain 是工程任务领域，不是金融/医疗等业务行业；行业语义与合规仍由真实需求和仓库 authority 输入，不能从资料名推断。语言目录同时容纳查询、脚本、标记/样式语言，**不是声称 HTML/CSS/SQL 都是通用编程语言**。覆盖是结合公开开发者调查、仓库活动和领域代表性设计的常用集合，不是精确排名，也不等于只支持这些技术。

### 组合示例

- Svelte + Java 全栈：`full-stack` + 实际 JavaScript/TypeScript 和 Java + `svelte-sveltekit`；只有真实使用 Spring 才加 `spring`。
- SvelteKit 单仓全栈：`full-stack` + 实际 JavaScript/TypeScript + `svelte-sveltekit`，**不推断 Java 后端**。LMDO 也不因用户的例子变成 Java 项目。
- Swift/Rust macOS 应用：`desktop-apps` + `swift`/`rust` + 实际 UI/macOS/Tokio adapter；Tokio 不是 Rust 的默认。
- Python CLI、数据 pipeline、后端服务分别选择不同 domain；共用 `python`，并不默认 Django。
- Kotlin 后端不加载 Android；TypeScript CLI 不加载 React/browser；未知 Elixir 后端继续走 backend + universal fallback。

完整例子与负例见 [examples](skill/sectioned-feature-development/references/planning/examples.md)。每个轴独立命中；full-stack 不自动加载全部 frontend/backend 内容。框架 guide 已能回答的问题，不为标签完整再读语言基础。资料只提供问题和证据方法，不能创造新要求、测试平台、服务或 review pass。

### 保留生产者／消费者交接

PLAN 仍区分 SOURCE_INSPECTED / OBSERVED / PLANNED / UNKNOWN；producer HANDOFF 返回实际 fixture 或精确源码/测试；consumer TASK 使用同一合同和真实 serializer/decoder。用户点名的 reader 必须归入 EDIT 或 VERIFY_UNCHANGED，不能以 inspect-only 漏掉实际需求。

分类调整不重开 accepted PLAN。旧标签/文件路径在新任务中使用迁移后的资料，历史记录原样保留，不要求重新取得 approval hash。详见 [迁移与职责去向](docs/version-history/v4.5.1/MIGRATION.md)。

## 执行顺序

主线程写完整 REQUIREMENTS 与 PLAN-FULL → 一次基础结构校验 → 实际独立 PLAN review → 主线程 admission → 保存当前 TASK 并真实委派 → HANDOFF／候选冻结 → bounded review／delta repair／必要 fresh final → 父级验收、集成与最终验证 → 关闭计划 → 规范 Audit。

自动触发仍在第一份 PLAN 后等人工批准；显式调用仅免这一暂停。Audit OFF 不免执行产物。大于一个业务 section 或一个可执行 subsection 必须独立分支与提交。已完成功能后新增需求重新评估。

## 4.4.1 的两项强化

**先等真实 review 返回，再由主线程 admission，最后才派下一实现。** PLAN review（含已选择的 GLM challenge 和真正必要的 delta）是全 feature 的前置条件；不能边审边 spawn S01。串行 S01 还在 initial/delta/final 或必要测试阶段时，不能 spawn S02。子项必须等上一 checkpoint 闭合；BLOCKED/ABANDONED/取消不是依赖满足。

仅保留已审计划明确列出的独立父 section 并行例外：不同工作树、依赖已集成、路径/契约/共享资源不冲突。没有明确说明就串行；不能因为不同文件、缺少依赖标签或 reviewer 在等待而临时推断可并行。

**[@code_reviewer](subagent://code_reviewer) 永远是原生 Codex/Astra 角色，不是 ZCode 的别名。** 原生 slot 走 Codex native subagent 派发与等待；GLM slot 由主线程直接调用 ZAS MCP spawn/poll/result。`$code-review` 只是两者复用的审查方法。不能在每个 slot 先跑原生再补 ZAS，不能用 native reviewer 包一层 MCP 转发，也不能把两类 ID 混用。

每次实际交接只在已有状态/TASK/REVIEW 中写清「已闭合前提、仍活跃对象、实际 route/ID」。不恢复 STATE.json、actor registry、approval-hash 或 ready 脚本。已完成的历史 section 不因升级重开；当前活跃任务先确认真实 actor 状态，再应用这些规则。

## 去掉什么，保留什么

不再安装 `workflow.py`、`execution_artifacts.py`、`advisor_flow.py`，不要求 PLAN 内 SFD_PLAN_V4 JSON、不要求 STATE.json、actor 注册或 hash-matching approval/ready/accept 收据。历史决策与验证记录保留，不在当前项目复制 previous-version baseline。

保留人可读 PLAN／FEATURE-STATE／TASK／HANDOFF／REVIEW，以及真实 ID、Git candidate、实际测试与 review 结果。主线程必须基于它们做调度，不能用“agent-managed”作为跳过委派或审查的许可。

只对 IDs、依赖 DAG、父子归属及每单元明确 impl 级别进行基本结构校验。脚本是读写确定性文件/安全打包的工具，不是一个程序化项目管理系统。原子 Audit／ZAS 配对／Advisor Git 导出／本地 ignore 工具保留，仅在对应操作发生时使用。

## 角色

- [@impl_nano](subagent://impl_nano)：Luna xhigh。
- [@impl_mini](subagent://impl_mini)：Terra high。
- [@impl_std](subagent://impl_std)：Sol medium。
- [@impl_large](subagent://impl_large)：Astra medium。
- [@plan_reviewer](subagent://plan_reviewer)：Astra xhigh；主线程作者与审查者不共用实例。
- [@code_reviewer](subagent://code_reviewer)：Astra high。
- [@code_explorer](subagent://code_explorer)：Luna xhigh，只做有界证据地图。

七个角色及全部 model/effort/sandbox 配置保持。本版只有 plan_reviewer 的知识路由措辞按新分类调整；其余六份角色逐字保留。任务—模型分级仍是待真实样本验证的策略，不是已证明成本最优。Grill Me 在界面使用 Astra high 仍是起始建议，只写在 README；确认后的自包含需求合同可单独交接，原访谈保留为审计 provenance。

## 安装

```bash
python3 scripts/install.py                      # dry run
python3 scripts/install.py --apply --replace    # 备份后完整替换两份 Skill 和七份 Agent
```

**必须更新完整项目中的两份 Skill 和七份 Agent，不只替换根 SKILL.md。** 描述层的 native/ZAS 区分位于 agent TOML，旧会话可能已缓存旧配置，优先在更新后使用新会话。

尊重 `$CODEX_HOME`（默认 `~/.codex`）；不覆盖 AGENTS.md/global config/无关 Agent。必须完整替换同名 Skill，不以增量覆盖留下旧 gate 脚本。安装器按确切目标先备份，因此这不授权清除产品仓库内容。

新会话读到 4.5.1 后，不再“升级”旧计划的 JSON schema。保存旧状态为历史，核对当前业务计划、相关真实 review 和 source/Git 一次，继续未接受部分。真实缺口仍需有界补证据，不能造回执。

## 文件

- [4.5.1 输入分析](docs/version-history/v4.5.1/AUDIT_PACK_ANALYSIS.md)
- [4.5.1 外部研究与覆盖依据](docs/version-history/v4.5.1/RESEARCH.md)
- [4.5.1 修改与保留](docs/version-history/v4.5.1/UPDATES.md)
- [4.5.1 验证记录](docs/version-history/v4.5.1/VALIDATION.md)

- [4.5 输入与审计分析](docs/version-history/v4.5/AUDIT_PACK_ANALYSIS.md)
- [4.5 外部研究与限制](docs/version-history/v4.5/RESEARCH.md)
- [4.5 修改依据](docs/version-history/v4.5/UPDATES.md)
- [4.5 验证记录](docs/version-history/v4.5/VALIDATION.md)
- [规划库来源目录](skill/sectioned-feature-development/references/planning/sources.md)（维护时按需，不默认加载给所有 worker）

此前版本：

- [4.4.1 修改依据与边界](docs/version-history/v4.4.1/UPDATES.md)
- [4.4.1 验证与未验证项](docs/version-history/v4.4.1/VALIDATION.md)

以下保留 4.4 原研究和历史交接，ZAS 的旧交接不是本次新增产品计划：

- [本轮分析与三份 rollout](docs/version-history/v4.4/AUDIT_PACK_ANALYSIS.md)
- [官方与社区研究](docs/version-history/v4.4/RESEARCH.md)
- [逐项修改及职责保留](docs/version-history/v4.4/UPDATES.md)
- [脚本对比](docs/version-history/v4.4/SCRIPT-INVENTORY.json)
- [验证与未验证边界](docs/version-history/v4.4/VALIDATION.md)
- [ZAS 新计划](docs/version-history/v4.4/zas-handoff/PLAN-FULL.md)
- [ZAS 新会话 Prompt](docs/version-history/v4.4/zas-handoff/NEW-SESSION-PROMPT.md)

## ZAS 协议

当前 4.3.1 公开协议与本次计划的 compact 公共契约分别可按实际 tools/list 使用；不是要求 ZAS 保持两个版本。保留的 adapter 不再要求新版刻意删除的 version/source/identity 回显。可选 wire 检查器 `--compact` 只验证 3/5/200、有界结构和 encrypted_content 排除，不能证明模型身份、推理正确或任务有进展。开发 ZAS 自身时按任务明确的 native-review override，不调用修改中的服务审查它自己。

## 审计与限制

流程包 `~/Desktop/audit-pack/xxx.zip`、真实 ZAS attempts 配对 `xxx-zas.zip`；外部 Advisor 在另一个目录。无 `.sha256` 侧文件。工具只保证其有限确定性工作，不保证 Agent 会遵守流程。下一批实际样本必须同时看真实漏审/跳过委派/逃逸缺陷与过程成本，不能用离线测试冒充模型行为实验。

## 新规划层的验证边界

新测试检查文件路由、组合用例、fallback、模板/角色连线与旧执行规则保留；不运行一个机械路由器，也不能据此宣称模型会正确选择全部资料。下一批 Audit 在原 PLAN/TASK/HANDOFF/REVIEW 中记录命中理由、共享合同、late consumer fixes和实际读取/搜索成本，区分计划遗漏与已经写明但没有实施。不额外创建 Audit gate 或为了测量再运行 reviewer。
