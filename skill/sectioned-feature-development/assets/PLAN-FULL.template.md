# PLAN-FULL — 示例业务功能

- Feature: example-feature
- Status: PLANNED
- Repository / feature base / target / current branch: 由实际 Git 填写
- Execution mode: EXECUTE_WITH_COMMITS
- Mode rule: 多于一个业务 section 或多于一个可执行 subsection，必须在下一次产品/测试修改前使用 EXECUTE_WITH_COMMITS 和独立非 main feature branch；不得执行时自行省略提交。
- Branch authority: 用户批准的独立 feature branch
- Invocation: USER_EXPLICIT
- Requirements: .agent-work/REQUIREMENTS.md

## 目标、权威与排除项

写原始业务结果、已确认修正、真实输入/反例、现有生产合同与最小充分实现。
不由 PLAN 自创需求，不为审核回执添加产品机制。

## 规划知识路由与边界样例

- 四维目录已检查：domains/INDEX.md、languages/INDEX.md、adapters/INDEX.md、concerns/INDEX.md；不复制全目录。
- Domain / Language / Adapter / Concern：各写实际读取的命中文件与源码理由；未适用写 NOT_APPLICABLE，已有指南覆盖相同问题可写 COVERED_BY。
- Universal fallback：not needed，或明确尚未覆盖的技术/边界及理由；先保留并读取所有独立命中项，不能因一个未知后端就整项只用 universal。
- 多个模块合并到同一计划；选中资料不是新需求，不为每个模块新建 section、测试或 review。
- 真实边界（如无则省略）：权威 → producer/serializer → 输入样例 → 状态/响应 → 实际 consumer → 可判错检查。
- 样例来源：SOURCE_INSPECTED / OBSERVED / PLANNED / UNKNOWN；未实施接口不能伪装已运行。
- 明确需求点名的读者：EDIT / VERIFY_UNCHANGED / OUT_OF_SCOPE 及必要理由；生产者 HANDOFF 和消费者 TASK 复用同一份样例。

本段是人可读内容，没有新 JSON、路由校验器或审批门禁。一个局部改动不需要填满所有技术清单。

## 调度与最终验证

- 顺序：S01，然后 S02。
- 并行：本例串行；允许并行时明确路径、契约和测试资源无冲突。
- 最终测试/发布环境/尚未证明的组合路径：填具体行为，不建“收尾一切”的证据专用节。

## S01 — 第一项业务结果
- Implementer: [@impl_std](subagent://impl_std)
- Depends on: none

### 业务合同

- 权威、产出及实际 consumer：
- 修改 owner / inspect-only / exclusions：
- 不变量与安全中间态：
- 任务模型依据：范例、歧义、状态耦合、新推理、可判错测试。
- AC、targeted/section 检查：
- Review：BOUNDED，assurance ONE 或 TWO（计划作者明确选定）。

## S02 — 第二项业务结果
- Implementer: [@impl_large](subagent://impl_large)
- Depends on: S01

### 父级合同

- 完整业务结果、跨子项不变量、joint oracle：
- 拆分依据：真实内部模块或模型能力，不拆散同一验收合同。
- 父级 review/repair budget：共享原 lineage，不给子项新配额。
- Assurance：TWO。

### S02.A — 内部基础模块
- Implementer: [@impl_large](subagent://impl_large)
- Depends on: none

- 模型理由、改动边界、产出/consumer、安全中间态、具体检查：

### S02.B — 内部消费者
- Implementer: [@impl_std](subagent://impl_std)
- Depends on: S02.A

- 模型理由、改动边界、产出/consumer、安全中间态、具体检查：

## 集成与完成

父级 reconciliation 与必要 fresh final 通过才接受 S02。验证组装后的 product/test head，记录实际结果和缺口，然后关闭 PLAN。后续用户请求默认重新评估。
