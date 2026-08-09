# Updates

## 本版本如何从证据得到修改

- 收紧 `MERGE_BLOCKING_DEPENDENCY`：必须位于当前 acceptance 必需路径且由 diff 新依赖/激活/序列化/暴露。
- `EVIDENCE_GAP` 必须引用已有 AC 或 repo required gate。
- Scope manifest 区分 allowed-to-edit 与 inspect-only causal path。
- section repair budget 跨 initial/delta/final/checkpoint/recovery 累计。
- 每个 original lineage 最多一次自动 hard-cap recovery；integration 也有有限累计 budget。

## Validation 摘要

原交付中包含 validator / script test / ZIP integrity 等验证记录；本历史库按用户选择不保留独立 validation 原件，只保留结论：该版本在当时交付时通过了相应 Skill Creator/脚本/打包完整性检查。

## 未保留的包装文件

- `*.patch`
- package SHA/line-count/index 文件
- 独立 SKILL preview（已保留真实 skill tree）
- nested skill ZIP（已解包）
- raw audit inventory（已综合进分析）
