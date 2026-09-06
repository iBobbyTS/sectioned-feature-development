# 4.0.1：配套 code-review 修复

## 本次修改

新增 `skill/code-review/`。入口先判断 DELEGATED_PASS/STANDALONE；所有旧 section acceptance、repair-loop、ledger 文档明确只适用于 standalone。旧根流程移动到 standalone-workflow.md，风险/coverage 正文保留。

Delegated pass 复用现有 REVIEW-PACKET，返回 CLEAN / MATERIAL_CANDIDATES / INSUFFICIENT_EVIDENCE。Parent 仍管理 ONE/TWO、provider reservation、admission、repair waves、final/integration 和 advisor；不降低修复后的 fresh final 要求。

Sectioned 只补 protocol 标记和配套版本位置，不改阶段门禁。astra_high 只补执行该 delegated 协议的说明，不改模型或 effort。ZCode 工具、continuity policy、DAG、预算和关闭计划规则全部不变。

安装器默认安装两份 Skill 与原八个 agent。`--only code-review` 支持不碰原 4.0 即修复；`--replace` 先备份现有同名目录，确保原 standalone/本地改动可恢复。历史附录不安装、不重写。

## 不做

- 不增加 review round、test gate、协议验证器或任务模型路由。
- 不重开已经接受的 section，不迁移既有 review lineage。
- 不因版本升级重跑测试或把真实缺陷改判 clean。
- 不提供终态 ZCode resume，不把 task SUCCEEDED 当 CLEAN。

## 当前被阻塞任务如何继续

安装后让一个新 reviewer 实例读取新版 code-review，继续原冻结的 candidate/packet；仅因旧协议冲突而无有效结果的派发不计 clean，也不消耗 material repair wave。已有有效代码证据不重做；已打开的真实 finding 仍按原预算闭合。若宿主旧会话已经缓存旧 Skill，启动新会话并读取现有计划/状态，不重新规划。

## 交付

- 单独 code-review 4.0.1 ZIP：给原 4.0 用户最小替换。
- 完整 4.0.1 project ZIP：两份 Skill、安装器、agents、历史和回归测试。
- 4.0 → 4.0.1 project patch：审阅本次实际修改。

验证结果见 [VALIDATION.md](VALIDATION.md)。
