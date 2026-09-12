# 4.5.2 — 原规则恢复与证据可信度

本次是基于已提供源码和已完成分析的局部文档修订，没有引入新的外部最佳实践或再次网络研究。

| 来源 | 用法 | 可信边界 |
|---|---|---|
| 上传工作树 HEAD 753c9ff / VERSION 4.5.1 | 确定当前部署说明、实际脚本与保留基线 | 文件事实；不能证明运行时模型身份或执行结果 |
| 同仓 v3.9 `skill/sectioned-feature-development-current-mcp/SKILL.md` 第42–45、114、170–171行 | 恢复激活读取、采集、续跑和最终 Audit 职责 | 原规则的直接证据；不原样恢复旧模型、MCP或调度设计 |
| 当前 audit-mode.md 的 Purpose、Completion obligation、4.4 capture | 保留 LIVE、轻量真实采集、原子幂等封包、单次有界修正 | 指令规定；不等于模型已经执行 |
| 上一轮 ANALYSIS/EVIDENCE/METRICS | 确认启动、接管和完成交接实际遗漏 | 二次利用已完成文件分析，不重复算四个独立失败 |
| 用户本轮指令 | 不补救旧任务，只更新后续 Skill | 直接授权 |
| 提供的 skill-creator | frontmatter、渐进读取、目录与校验规则 | 打包规范；非模型行为验证 |

## 取舍

1. 恢复 Audit 的前置阅读和简明待办；整份 reference 每 fresh context 读一次，不每次 dispatch 重读。
2. 真实结果可保存在已有 HANDOFF/REVIEW/evidence；trace 是便利工具，不是每次推进的审批系统。
3. 产品就绪与 Audit 交付独立。关闭业务 PLAN 不可消除 PENDING，但审计失败也不虚构产品缺陷。
4. 完整性 hash 留给既有归档工具；不新增 .sha256 侧文件、不新增 JSON state 或 actor registry。
5. 当前 ZAS poll→wait 的用户源码修改原样保留；只修复两项还期待旧接口/旧hash的离线测试。没有改变 ZAS 运行协议。
6. 七个 Agent、code-review、规划知识与 review/repair/parallel/Advisor 语义逐字保留。
