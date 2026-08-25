# Audit Pack Analysis

本版本逐项分析约 30 个大小不一的 Audit Pack，并包含从零构建 ZCode review MCP 的开发记录。用户明确说明：ZCode 项目最早未先探测真实 runtime 形态、直接按现有开源项目假设开工，属于人工输入前提错误，不归因于 Skill 或 Advisor。

## 总体信号
- 大多数高风险任务的 PLAN/code review、delta closure、exact-head gate 有真实质量收益。
- 主要剩余浪费来自小任务 over-trigger、重复 broad validation、reviewer transport retry、process artifact 体积和 telemetry vocabulary drift。
- 当前 ZCode MCP 已是较成熟的 review-only durable job system，但缺通用 implementation subagent、稳定 same-session continuation 和更完整 component health。
- reviewer identity、provider provenance、exact head/report integrity 需要进入 durable state。

## 结论
保留核心质量门禁，加入异构 reviewer routing；高复杂度 PLAN 才增加 ZCode challenge；code full-pass 在 Sol/ZCode 间交替；Advisor 作为独立、低频、非 Audit 依赖的系统级裁决通道。
