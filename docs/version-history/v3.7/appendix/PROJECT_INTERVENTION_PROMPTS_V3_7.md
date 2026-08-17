# Minimal Existing-Project Prompts

## Codex 0.147 adaptation — required

```text
继续当前 S04，但不要修改产品代码或扩大 scope。先准确列出我需要完成的认证刷新和 GUI Browser executor/judge 创建步骤；我完成后，只重跑原 blocked live cells并更新现有 ledger。所有 mandatory cells 和 deterministic gates 未通过前，不升级版本、不发布，也不要生成多个 audit 包；最终仅用 V3.7 canonical finalizer 输出一个包。
```

## Context-window limits — audit only

```text
不要修改或重审产品代码。按 V3.7 将现有 PLAN、review、Git/source 和 session evidence补成一次 POST_HOC audit，并用 canonical finalizer只生成 `~/Desktop/audit-pack/{repo}-{feature-id}-sectioned-audit.zip`。若证据缺失，标为 gap，不补跑测试。
```

## URL/key rotation — only when a merge decision is needed

```text
不要修改轮换功能或修复无关 baseline。机械区分最终 gate 中 feature-caused 与 pre-existing failures；若只剩 pre-existing failures，报告 conditional merge readiness并询问我是否允许在该 repository policy 下合并，禁止把 baseline cleanup纳入本 feature。
```

## [保密内容]
