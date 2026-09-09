# 本轮输入与问题核查

## 证据范围

本轮输入为用户提供的完整 `sectioned-feature-development-v4.4-project.zip` 和两项运行现象描述。本轮没有新的完整执行 rollout 或独立 audit pack；不能统计违规频率、断定所有 S01/S02 重叠都是违规，或认证模型身份。

## 从 4.4 安装文件能够确认的弱点

1. 根 Skill 已要求独立 PLAN review，但没有在靠前的派发边界明确列出“所有已选择的 PLAN pass 的真实结果 + 主线程 admission 完成以前，任何 impl 都不 spawn”。
2. `parallel-execution.md` 写着 “Plan review finishes before any dependent product implementation”，其中 dependent 容易使没有先前节点的 S01/parallel root 被误认为例外。
3. `bounded-review.md` 的“accepted, blocked, or abandoned”没有就地解释：blocked/abandoned 不是成功依赖，不能解锁下游。
4. 原 native reviewer TOML 的 description 只定义审查职责，没有明示“原生 Codex 角色，绝非 ZAS 别名”；共享 `$code-review` 方法与执行 provider 可以被混淆。
5. 4.4 本来允许已批准的独立父 section 跨工作树并行。该能力保留；未经计划明确授权的临时并行、同父子项越序和 PLAN 未闭合就实施，才是本次约束对象。

## 修改边界

只强化父线程操作顺序、角色 discovery/developer 指令、现有 task/review handoff 和审计字段。没有新增运行脚本、状态 schema、actor 注册、hash approval、ready gate、review pass、产品测试要求或新 MCP 工具。

产品语义、真实 ZAS 协议、3/5/200 observe、模型档位、Astra/GLM feature-wide 轮换、父级 repair/recovery、外部 Advisor 及旧版本历史保留。没有修改或重审 ZAS 产品项目，也没有重写上一轮 ZAS PLAN。
