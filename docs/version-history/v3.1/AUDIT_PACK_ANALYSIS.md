# Audit Pack Analysis

证据来自三个仓库纠偏结果与源代码/session 的独立复核。V3 已消除最主要的 repeated full rediscovery，但仍存在终止性和 authority 漏洞。

## 真实问题
- `MERGE_BLOCKING_DEPENDENCY` 中“made reachable”过宽。
- `EVIDENCE_GAP` 可能把 reviewer 想要的更强 oracle 洗成 blocker。
- final/recovery repair 是否共享原 5-wave budget 不够明确。
- integration 没有完整复用 finding taxonomy 和 finite budget。
- active contract 可能已经被旧 reviewer 污染。

## 被拒绝的建议
把 manifest 变成绝对文件白名单会漏掉真实跨 owner serialization/composition defect，因此只限制 edit authority，inspection 仍需明确因果链。
