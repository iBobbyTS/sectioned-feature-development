# Updates

## 本版本如何从证据得到修改

- 新增 `review_assurance = AUTO | ONE | TWO`。
- AUTO 根据 migration/security/concurrency/routing/time eligibility/public protocol 等语义风险选择 TWO；精确局部小修可 ONE。
- 强制用户失败样例、反例、后续 correction 映射到 AC/test，并标记 superseded guidance。
- 外部 API/auth/protocol 不确定时先做最小 probe。
- 同 HEAD/environment 的 validation evidence 可复用；final review/test 必须覆盖交付 HEAD。
- 隔离 feature artifacts，减少跨 feature 污染。

## Validation 摘要

原交付中包含 validator / script test / ZIP integrity 等验证记录；本历史库按用户选择不保留独立 validation 原件，只保留结论：该版本在当时交付时通过了相应 Skill Creator/脚本/打包完整性检查。

## 未保留的包装文件

- `*.patch`
- package SHA/line-count/index 文件
- 独立 SKILL preview（已保留真实 skill tree）
- nested skill ZIP（已解包）
- raw audit inventory（已综合进分析）
