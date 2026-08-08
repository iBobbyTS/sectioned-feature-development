# Updates

## 本版本如何从证据得到修改

- 把 reviewer 输出拆成 raw candidates 与 main-agent admission。
- 冻结 scope、assurance、threat model，未授权的新保证只能作为 proposal。
- Hard cap 先诊断 `DEFECT_DENSITY / ASSURANCE_BOUNDARY_DRIFT / ARCHITECTURE_BOUNDARY_FAILURE / CONTRACT_AMBIGUITY / EVIDENCE_FAILURE`。
- Recovery 支持 SPLIT/SIMPLIFY_REPLACE/REBOUND/REPAIR_EVIDENCE，限制递归 split。

## Validation 摘要

原交付中包含 validator / script test / ZIP integrity 等验证记录；本历史库按用户选择不保留独立 validation 原件，只保留结论：该版本在当时交付时通过了相应 Skill Creator/脚本/打包完整性检查。

## 未保留的包装文件

- `*.patch`
- package SHA/line-count/index 文件
- 独立 SKILL preview（已保留真实 skill tree）
- nested skill ZIP（已解包）
- raw audit inventory（已综合进分析）
