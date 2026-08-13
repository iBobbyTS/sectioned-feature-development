# Audit Pack Analysis

本版本基于九个新 feature audit。核心 review/repair 状态机没有再次出现旧式 scope 无限膨胀；重复出现的是审计重建不可靠。

## 主要问题
- invocation source 经常无法确定，无法判断 agent 是否 over-trigger。
- 上一个 feature 的 PLAN/review artifact 会污染下一个 feature 的 process diff。
- final-head evidence 与 state summary 有时不一致。
- reviewer lifecycle 丢失；post-hoc 很难区分 dispatch、取消、重试和真正 completion。
- compaction 后 token counter 不适合直接求和。

## 结论
需要轻量 LIVE/POST_HOC audit ledger 和 feature artifact isolation，但 Audit 必须是观测层，不得增加开发 gate。
