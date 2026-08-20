# Updates

## 本版本如何从证据得到修改

- 自动触发增加 non-trivial prerequisite 与 bounded-local negative rules。
- 自动调用：读取 Skill 后立即告知触发原因，首版 PLAN-FULL 完成后、PLAN review 前让用户审批；用户显式调用默认执行到底。
- 增加 late activation：初始误判为小任务时保留现有工作并前瞻进入 branch/section 流程。
- main agent 变成 orchestrator-only；plan reviewer、implementer、repairer、initial/delta reviewer、final reviewer 角色隔离。
- 增加单 mutable-stage barrier，阻止 review 未结束时启动下一 writer。
- `.agent-work` 使用本地 exclude，禁止进入 Git。
- PLAN review 必要性优先；新增 foundation-choice gate。

## Validation 摘要

原交付中包含 validator / script test / ZIP integrity 等验证记录；本历史库按用户选择不保留独立 validation 原件，只保留结论：该版本在当时交付时通过了相应 Skill Creator/脚本/打包完整性检查。

## 未保留的包装文件

- `*.patch`
- package SHA/line-count/index 文件
- 独立 SKILL preview（已保留真实 skill tree）
- nested skill ZIP（已解包）
- raw audit inventory（已综合进分析）
