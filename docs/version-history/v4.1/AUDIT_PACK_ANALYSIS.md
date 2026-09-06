# 4.1 本轮证据分析

## 使用的输入与范围

读取本轮上传的 `sectioned-feature-development.zip`、`pppms-section-sizing-review.zip` 及其解压文本，并对照仍在本会话可访问的 `pppms-portal-audit-20260905-0951.zip` 中当前active PLAN、STATE、source和阶段ledger。没有重新把早期项目所有历史包计作本轮样本，没有运行Rust/Python产品测试，没有把先前assistant总结当唯一证据。

已核对快照：feature branch `codex/rust-backend-compute-node`，HEAD `4f122c7e321af20013a5890973e0da82d5a5db80`；S04.1.2/C01/B00/C02 accepted+integrated，B02 IMPLEMENTING，C03 PENDING。live HEAD可能更新，4.1提案不能覆盖实时STATE。

## S04和create lineage不是一个同质“太大的section”

- S04客户端两波分别处理成功status+body timeout、失败status+body timeout。这是一张状态×读取结果矩阵，而不是两个独立产品合同。
- 原S04.1存在domain、HTTP/request处理等真实内部增量；拆成S04.1.1与S04.1.2有合理技术切面，但原先由LOC cap驱动压缩/恢复不合理。
- domain拆出后仍有多轮数值/词法/错误顺序问题，说明“新编号”不消除同一规则的困难。
- HTTP拆出后仍发生validator接受字段名空白、extractor不消费它的问题。再把两个函数独立验收会增加漂移；应复用同一解析结果，在parent合同下联测。

结论不是“不能拆实现”，而是“不能把共同不变量拆成互不负责的验收合同”。4.1把实现颗粒和接受边界分开。

## 为什么不是再加一套完整child流程

本项目此前scope膨胀、evidence-only descendants、重建clean lineage都显示：每个编号带独立PLAN+CleanA/B+5波budget会复制流程并掩盖累计失败。subsection只能有一个checkpoint状态；预算、外部依赖、完成和full final留在parent。

为保护质量，累积child coverage后必须在final parent candidate检查joint oracle和实际consumer，fresh final仍看完整parent diff。局部green不等于整体通过，不用“sum of clean”冒充integration。

## PPPMS四个明确切面

| Parent | 内部checkpoint | 不拆开的不变量 |
|---|---|---|
| C03 | 基础场/单位/seed → 事件与完整采样 | 同一seed/量化/单位和sensor组合；不要求NumPy随机字节流一致 |
| B03 | 精确表示/canonical identity → DailyShape与receipt事务 | receipt和业务写入原子性；不把identity数值套用create-only例外 |
| C07 | analysis候选 → publication/frozen JSON/outbox | sourceidentity/trend推进、发布后payload冻结和重试恢复；不新加exactly-once承诺 |
| B20 | worker/current/history读 → 历史重建domain | 同一interval/source日期规则、只读GET、原函数各自事务，不新加全局事务 |

45个父节点不变；8个内部checkpoint，不改41条未完成父节的产品义务（其中B02正在执行）。前一轮“如果全做独立split则49节点”的提案没有当作已实施事实。本次明确替换为四个parent的内部实现计划。

## 还发现的交付完整性缺口

本轮Skill项目的installer/tests已引用当前`skill/code-review`与4.0.1 delegated协议，但ZIP中当前运行目录不存在，只有历史appendix和独立旧code-review附件。本次补齐真正可安装的companion4.1；standalone逻辑保留到reference，DELEGATED_PASS优先，支持旧4.0和新4.1 packet。不声称用户机器上的installed code-review缺失。

## 证据限制

checkpoint设计、review累计覆盖和预算门禁已经做离线回归，但未进行新模型运行/实际GLM续接/新PPPMS实现。不能从逻辑full-pass数下降推导token节省，所有实际checkpoint调用和修复仍须计入audit。原始contract和source派生需求不因本次命名变化被删减。
