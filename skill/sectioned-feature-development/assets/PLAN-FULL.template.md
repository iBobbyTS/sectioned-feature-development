# PLAN-FULL — 示例业务功能

- Feature: example-feature
- Status: PLANNED
- Repository / feature base / target / current branch: 由实际 Git 填写
- Execution mode: EXECUTE_WITH_COMMITS
- Branch authority: 用户批准的独立 feature branch
- Invocation: USER_EXPLICIT
- Requirements: .agent-work/REQUIREMENTS.md

## 目标、权威与排除项

写原始业务结果、已确认修正、真实输入/反例、现有生产合同与最小充分实现。
不由 PLAN 自创需求，不为审核回执添加产品机制。

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
