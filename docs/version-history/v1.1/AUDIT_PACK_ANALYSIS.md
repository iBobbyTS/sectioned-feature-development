# Audit Pack Analysis

本版本没有正式 Audit Pack；依据是 v1 交付后的用户政策反馈。用户指出全局 Custom Instructions 不应复制完整 sectioned workflow，只应保留触发规则，并且触发语义最好同时存在于 Custom Instructions 和 Skill description。

## 发现
- 触发规则与执行流程混在上层指令会造成双重状态机和维护困难。
- Skill 不能自称覆盖更高层 no-commit；应由上层指令显式授权 scoped exception。
- Skill description 是自动召回入口，仅依赖 Custom Instructions 不够稳。

## 结论
把 routing policy 与 workflow implementation 分层，减少配置漂移。
