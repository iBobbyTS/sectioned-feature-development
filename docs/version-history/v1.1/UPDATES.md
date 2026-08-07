# Updates

## 本版本如何从证据得到修改

- Custom Instructions 只保留触发规则和 scoped commit 授权，不复制流程。
- Skill description 与 Custom Instructions 使用同一触发语义。
- 明确 Skill 只有在上层显式授权 scoped exception 时才能在实现流程中 commit。

## Validation 摘要

原交付中包含 validator / script test / ZIP integrity 等验证记录；本历史库按用户选择不保留独立 validation 原件，只保留结论：该版本在当时交付时通过了相应 Skill Creator/脚本/打包完整性检查。

## 未保留的包装文件

- `*.patch`
- package SHA/line-count/index 文件
- 独立 SKILL preview（已保留真实 skill tree）
- nested skill ZIP（已解包）
- raw audit inventory（已综合进分析）
