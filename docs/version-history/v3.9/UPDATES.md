# Updates

## 本版本如何从证据得到修改

- 高复杂度 PLAN：Sol 主 review 后增加独立 ZCode challenge；标准复杂度不增加第二 full PLAN pass。
- Code full review 在 Sol/ZCode 间按 pass 交替，第一次始终 Sol；同 pass 的复核保持原 reviewer。
- 当前 MCP 版显式处理 `resume=false`；enhanced 版设计通用 `zcode_agent_*` lifecycle、typed review mode、component health 和 structured errors。
- 外部 reviewer 的 provider/agent/session/job/base/head/report hash 进入 durable provenance。
- 新增低频 External Advisor escalation：只在二次收敛失败、高影响 reviewer 冲突、大规模已验证工作即将废弃、信任模型无法裁决、发布证据矛盾或外部系统形态 probe 后仍不确定时触发。
- 触发 Advisor 后停止开发，打包完整仓库（含 Git）并由 human 转交，不与 Audit 开关绑定。

## Validation 摘要

原交付中包含 validator / script test / ZIP integrity 等验证记录；本历史库按用户选择不保留独立 validation 原件，只保留结论：该版本在当时交付时通过了相应 Skill Creator/脚本/打包完整性检查。

## 未保留的包装文件

- `*.patch`
- package SHA/line-count/index 文件
- 独立 SKILL preview（已保留真实 skill tree）
- nested skill ZIP（已解包）
- raw audit inventory（已综合进分析）
