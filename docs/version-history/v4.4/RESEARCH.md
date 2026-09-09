# 4.4 Research：流程型 Skill 的自由度与确定性工具

检索/阅读日期：2026-09-09。用户要求外部研究；本轮 AI 经验材料采用近一年内容（或当前官方文档）。不引用旧模型 benchmark 推断新模型能力，不将社区抱怨当受控实验。

| 来源 | 日期/类型 | 可提取事实与可信度 | 对本次设计的含义 |
|---|---|---|---|
| OpenAI Build skills：https://developers.openai.com/codex/skills/ （当前转向 https://learn.chatgpt.com/docs/build-skills） | 当前官方文档，高 | Skills 可由指令及可选脚本构成；默认偏 instruction-first，确定性/外部工具需求才用脚本；渐进加载 | 不需为所有流程行为写执行器；保留确定性文件/归档工具 |
| Anthropic Skill authoring best practices：https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices | 当前官方文档，高 | 自由度取决于任务脆弱性；代码 review 可以给高自由度；易错确定性操作、验证与 utility scripts 有价值 | semantic admission/DAG 调度由 Agent；基本 DAG/原子压缩/真实测试保持确定性 |
| Effective harnesses for long-running agents：https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents | 2025-11-26，厂商工程文章，中高 | 跨 context 需要进度与状态文件、Git 和逐步实现/测试证据 | 不能再次删除 PLAN、HANDOFF、REVIEW 和实际委派链；少脚本不等于没记录 |
| Superpowers #781：https://github.com/obra/superpowers/issues/781 | 2026-03-17，使用者问题报告，有限 | 用户抱怨审批重、规划久；标为待复现而非已证明普遍缺陷 | 与本轮现象相似，但以本轮 rollout 作因果证据 |
| Superpowers #528：https://github.com/obra/superpowers/issues/528 | 2026-02-22，使用者问题报告，有限 | 有模型跳过 spec/code review 的报告 | 移除 gate 有遗漏风险，保留显式责任、真实返回及后续验证；不承诺零风险 |
| Superpowers #1900：https://github.com/obra/superpowers/issues/1900 | 2026-07-03，项目问题讨论，有限 | 测试技能文档/结构不等于测到真实行为质量 | 文本断言和本地单测不能证明模型会遵守，不用测试数量作为质量保证 |

## 综合推断

官方建议不是“完全不要脚本”，而是按职责选择自由度。本次不删除领域测试、权限/数据安全验证、Git 操作保护或 artifact 传输完整性。删除的是跟实际产品成功间接关联、可以被自造回执满足、且已造成反复格式修复的 orchestration gate。

Agent 自行调度依然意味着明确顺序和职责：保存完整 PLAN → 独立审查 → 真正实施/测试 → delta/final → 集成。只是不再将这个顺序编译为另一套 JSON 状态机。在部分未知业务条件下，人可读理由比增加 schema 字段更适合裁决；对归档原子性、ZIP 路径安全、并发编号、最终真实代码检查，确定性工具仍是正确层次。

## 未采用的证据

读取过 Anthropic 2024-12 的 Building effective agents，但早于用户要求的近一年窗口，没有将它作为本次 AI workflow 结论依据。此前关于模型身份、价格和优劣的结论未重新测量，本版保持角色配置，不新作能力承诺。

## 验证计划

离线可证明：结构解析不依赖 JSON/state/receipts；基本 ID/DAG/profile 错误仍能一次报告；安全打包/安装/配对不回归；旧必需质量职责仍明确存在。离线不能证明：模型执行合规不变、总 token 一定下降、实际产品缺陷率相同。下一轮应记录等价业务任务的跳过阶段、原始发现/修复、最终质量、process-only command/time 和 escaped defects；没有配对样本不要填百分比改善。
