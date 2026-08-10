# 三项目下一步 Prompt

## [保密内容]

## codex-cockpit：合并与清理

```text
当前“特殊用途账号（搜索）” feature 已达到 MERGEABLE。不要重新规划、重开 S01–S03、增加 reviewer 或扩展账号生命周期模型。

以当前 Git/source 和 final gate 为准，将 `codex/special-purpose-accounts` 合并到目标分支。只有目标分支在相关 pool/routing/API-key/Tauri owners 上出现实质 drift 时，才重跑一次既有 final gate；否则直接使用已有 backend、frontend、Rust 和 macOS package evidence。

确认 feature commits 已从目标分支可达后，保留 audit pack，安全清理该 feature 的 worktree、feature branch 和专属临时 refs。不要 push；不要把 Windows package 或 Apple notarization补成当前 merge blocker。
```

## codex-rosetta：完成剩余 S04/S05

```text
使用最新版 `$sectioned-feature-development` V3.3，保留并冻结已接受的 S03.3；不要重开 adapter/evidence proportionality work，也不要迁移旧 review artifact。

只更新剩余 S04/S05 的 PLAN-FULL，并在编码前调用一个 fresh read-only plan reviewer完成 V3.3 PLAN gate。它只检查：原始“选择已配置的 DeepSeek 官方 API”是否端到端闭环、当前官方 Responses/web_search contract、现有 config/Admin/candidate/UI/i18n/docs owners、依赖顺序和 scope proportionality。不得新增 registry、provider framework、proof/evidence harness、安全模型、compatibility program 或 broad validation。

计划通过后完成整个剩余 feature：
- S04 在现有 config/Admin/candidate owners 中加入一个已配置、启用、官方 origin、恰好一个 credential 的 DeepSeek row；模型保持当前官方 Responses API 支持的 `deepseek-v4-flash`；masked round-trip，不公开内部 capability。
- S05 复用现有 Network Search UI、i18n、双语文档和 compatibility owners；不新增 route 或第二套配置路径。
- 最终运行 repository 既有 required gates，并在凭据/环境可用时通过公共 `/v1/alpha/search` 路径做一次隔离、受界的真实 DeepSeek `web_search` 调用。

真实凭据或环境不可用时，完成 deterministic work 后将 feature 标为 `insufficient-evidence` 并停止；不得创建替代 proof publisher、socket sandbox、analyzer 或额外 browser/API harness。完成 S04、S05 和 final integration 后停止，不 push、不 merge，生成下一份 audit pack。
```
