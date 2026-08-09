# Updates

## 本版本如何从证据得到修改

- 用 `INITIAL_BOUNDED → REPAIR_DELTA* → FINAL_BOUNDED` 取代 repair 后反复 full review。
- Clean A 表示 admitted findings closure；Clean B 表示一次 fresh bounded final。
- Hard cap 改按 admitted repair wave 累计。
- 禁止 evidence-only/process-only descendant、clean lineage 重建和自动从旧 base 重做。
- Validation 分为 targeted、section/package、feature integration。

## Validation 摘要

原交付中包含 validator / script test / ZIP integrity 等验证记录；本历史库按用户选择不保留独立 validation 原件，只保留结论：该版本在当时交付时通过了相应 Skill Creator/脚本/打包完整性检查。

## 未保留的包装文件

- `*.patch`
- package SHA/line-count/index 文件
- 独立 SKILL preview（已保留真实 skill tree）
- nested skill ZIP（已解包）
- raw audit inventory（已综合进分析）
