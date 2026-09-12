# 4.5.3 修改与使用

## 1. 明确执行对象，不让 Agent 反推列表位置

根 Skill/frontmatter/activation/parallel/TASK 交接与 PLAN/STATE 模板直接使用 `EXECUTE_WITH_COMMITS`。多业务 section 或多可执行 subsection 的计划，实施前必须位于已授权独立非 main feature branch，并执行既有 coherent implementation/repair commits。显式 no-commit 冲突不能静默降级。

检查运行指令后明确化 17 处职责表达，详情见 [WORDING_REVIEW](WORDING_REVIEW.md)。如 FINAL_ANSWER 的优先级、允许调级的错误类别、未实现既有要求的分类、最小机制取舍，直接写对象，不引用“后者/最后一个”。不是删除所有代词，也不改变原有权限与预算。

## 2. 规划资料顺序

```text
router
→ domain / language / adapter / concern 四份短目录
→ 与实际变更匹配的专用指南
→ 仅对明确未覆盖的部分读取 universal（否则不读取）
→ 合成一份 PLAN，沿原有一轮独立 review 继续
```

补 `concerns/INDEX.md`，原四份 concern 正文不动。作者与原生 plan_reviewer 都执行目录检查；外部 PLAN challenge packet 同步该要求。已完整读取的当前上下文不反复读取；PLAN_DELTA 仅处理受影响路径。无需让 implementer 重读全库。

在现有 PLAN 路由段记录实际命中/无关/重叠覆盖和 fallback，不新增报告、JSON 或路由脚本。检查所有目录不是每维度必须选文件；不是把所有语言/框架读一遍。

## 3. 保留

- 九份运行脚本、安装器、整个 code-review 保持不变。
- 七份 Agent 的 name/model/effort/sandbox/description 保持；仅 plan_reviewer 的规划参考读取指令改变。
- 所有已存在版本历史和本地 CSV 原样保留；不复制 previous-version baseline。
- 4.5.2 的 Audit handoff 原文与完整 audit-mode 保持，不回到收尾后忘记封包的状态。
- 模型分级、Astra/GLM 轮换、PLAN/code review 次数、repair/recovery、subsection、并行、Advisor、ZAS wait 不变。

## 安装

使用完整项目现有安装器 `python3 scripts/install.py --apply --replace`，同时更新主 Skill 和 plan_reviewer.toml。不改用户 AGENTS.md、全局 config 或无关 Agent。单独 Skill 包不包含个人 agents 目录文件，需同时安装配套 plan_reviewer.toml。

新版只前瞻使用，不为新路由字段重开 accepted PLAN，也不为补记录添加历史 review/test。
