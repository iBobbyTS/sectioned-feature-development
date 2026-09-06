# 本轮输入与冲突核验

本轮没有重新进行产品 code audit 或分析旧 feature pack。输入是用户上传的 `code-review.zip` 与上一轮交付的 `sectioned-feature-development-v4.0-project.zip`。

## 可复核事实

- 原 4.0 包含 138 个文件；只有 `skill/sectioned-feature-development/` 是 active skill。
- 原安装器 `scripts/install.py::targets` 只安装该 Skill 和八个 agent。
- 旧 code-review 只存在于 `docs/version-history/v1/appendix`、`v1.1/appendix`，不会被安装。
- 原 README 明文要求已安装 code-review，同时声明不覆盖它；这与 4.0 依赖的协议未配套检验，属于本次交付遗漏。

## 协议冲突

| 位置 | 上传 code-review | 原 sectioned 4.0 |
|---|---|---|
| reviewer authority | SECTION 可返回 section-accepted；integration 可返回 mergeable | 只返回候选/coverage/gaps，parent 单独 admission 与 acceptance |
| repair 后 ONE | 通常 DELTA 成功即可，fresh final 可选 | admitted defect 后 delta closure 加一份 fresh final full pass |
| TWO | 一次 coverage-complete clean 可接受，禁止双空 full | covered baseline/closure 加 fresh independent final |
| integration | 每个完整 feature 必须 final INTEGRATION | 仅 unproven_composition 非空时派 reviewer；必要检查仍执行 |
| reset | 旧 ledger/fingerprint 矛盾可要求 full reset | parent 决定；不能仅因流程元数据或有界 repair head 变化重开 |
| reviewer 内部流程 | 自带 repair、soft/hard cap、final lifecycle | 一个 parent 状态机，reviewer 不另开循环 |

原有风险/覆盖目录仍有复用价值；这次不删减这些证据检查，而是隔离不同执行上下文的权限。
