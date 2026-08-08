# Audit Pack Analysis

证据来自实际 rollout/session：reviewer 逐轮扩大安全模型，主 agent 将建议直接升级为 material finding，repair 实现额外防御机制，下一轮 reviewer 再以这些新机制为基线继续推导，最终 hard cap 拆分了本不应存在的机制。

## 已确认失控链
`review suggestion → contract/assurance expansion → repair → review new mechanism → more guarantees → hard-cap split`。

## 根因
- reviewer 同时拥有 discovery 和事实上的 requirement-creation 权。
- threat model / assurance boundary 没被冻结。
- hard cap 默认 split，未区分 scope drift、architecture failure、contract ambiguity 和 evidence failure。

## 结论
必须由 main agent admission；reviewer 只能产候选。新增保证需要外部 authority；hard-cap recovery 先分类，再决定 split/simplify/rebound/evidence。
