# 六个项目下一步 Prompt

## 1. Deck：余额查询与 Sub2API 底座

```text
使用最新版 `$sectioned-feature-development` V3.4，从当前最终 HEAD 做一个 bounded closure，不重开已接受的 Sub2API 底座设计，也不新增 source graph/credential framework。

修复 `DeckConfigurationStore.sanitizeLegacyCredentialsForUnmatchedLayout` 对 balance-only legacy credential 的遗漏：legacy plaintext 检测、claimed credential IDs、每个 data-source configuration 的 hydration/write-back，以及 migrated credential ID tracking 都必须覆盖 `allSub2APIDataSourceConfigurations`，并正确写回各自的 capacity/balance slot。增加一个 layout mismatch + 仅 balance source 含 legacy plaintext bearer 的回归，证明凭据进入 Keychain、plaintext 被清除、credential index 完整。

随后在实际最终 product/test HEAD 上运行 `UlanziDeckSwiftTests` 和必要 build；对 `2fab56d..HEAD` 及本修复做一次 fresh `FINAL_BOUNDED`，只检查最终 endpoint、显示/interval 语义和 credential migration，不重审整体架构。若 clean，提交并报告 merge readiness；不要 push/merge，等待确认。
```

## 2. Deck：今日消费

```text
先基于已经修复并合入的余额/Sub2API 底座继续；不要复制或重新设计认证/source graph。

在所有取消/移除 `sub2APIDailyCostFetchTasks` 的路径同步清除对应 `sub2APIDailyCostRequestIDs`，包括切换时区、runtime cleanup、pause 和配置变更；补 focused lifecycle test，保持现有 request UUID stale-result fencing。

按仓库规则处理当前运行中的 App：不要擅自终止用户进程；请我关闭或在安全的独立测试环境运行。随后执行今日消费 targeted tests、完整 `UlanziDeckSwiftTests` 和必要 build，并取得一次 fresh `FINAL_BOUNDED`。本 section 涉及 async cancellation/timezone，保留现有 initial/repair evidence，final clean 即完成双证据。不要新增时区框架、历史/趋势或跨 endpoint 合并。完成后停止，不 push/merge。
```

## 3. Cockpit：订阅显示错误

```text
保留当前 worktree 中 `quota.py` 与 `test_backend.py` 的 expiry-aware 两文件修复，不重开 malformed JSON、entitlement shape 或新的订阅模型。

把用户的原始故障样本冻结为验收：过期 upstream Pro 5x 且 token 为 Free 时必须显示 Free；future upstream plan 仍优先；missing/invalid expiry 使用 token fallback。对当前最终两文件 diff 运行 focused tests，并调用一个 fresh `FINAL_BOUNDED`，只验证该已知样本、future/missing expiry 和现有 fallback，不重新做 INITIAL 或全仓 audit。

若 clean，提交该修复；未发生产品/test 变化时复用已有 full backend/package evidence，最多做一次必要 final gate。然后报告 merge readiness，不 push/merge。
```

## 4. Cockpit：turn 绑定

```text
当前 turn-binding feature 已有一致 audit、完整测试和最终 gate，属于 MERGEABLE。不要重新规划或增加 reviewer。

先检查目标分支是否在 `turn_routing.py`、Responses proxy 或 registry consumer 上发生实质 drift；若没有，直接合并并安全清理 feature worktree/branch/专属临时 refs。若有 drift，只做一次 bounded composition check，不重开完整 section。不要 push。
```

## 5. Rosetta：搜索 provider 管理重构

```text
当前搜索 provider 管理重构的产品代码已达到 MERGEABLE。不要再修改 provider architecture、failure policy、quota/cooldown、sticky state 或 UI，也不要新增 code review。

以 Git/source 为准确认目标分支仍等于 feature base或没有相关 owner drift。将当前 feature 的 PLAN/state/review ledger 与旧 DeepSeek feature artifact 分离归档或明确标记为 legacy；这是 process-only cleanup，不能改变产品 evidence 或触发重审。

随后合并 feature，保留 audit pack，安全清理专属 worktree/branch/临时 refs。不要 push。
```

## 6. [保密内容]
