# Updates

## 本版本如何从证据得到修改

- 加入 invocation provenance：USER_EXPLICIT / CUSTOM_INSTRUCTIONS_AUTO / AGENT_DISCRETION。
- 加入可选 LIVE/POST_HOC audit trace 和内置 `references/audit-mode.md`。
- 新 feature 前隔离上一 feature 的 active artifacts。
- Audit 只观测，不改变 review assurance、测试或 scope。

## Validation 摘要

原归档没有独立 validation 报告；保留实际 Skill 源码作为该版本事实源。

## 未保留的包装文件

- `*.patch`
- package SHA/line-count/index 文件
- 独立 SKILL preview（已保留真实 skill tree）
- nested skill ZIP（已解包）
- raw audit inventory（已综合进分析）
