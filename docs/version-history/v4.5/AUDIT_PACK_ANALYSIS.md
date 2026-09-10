# v4.5：本轮输入与规划问题分析

## 输入范围

本次不是重新做两个项目的产品审计，也没有要求生成新 ZAS 产品计划。以本轮 adaptive-debugging 附件、当前上传 Skill 项目、上一轮两任务的原始证据和分析为依据。没有把历史其他项目或未上传源码补成当前证据。

本轮没有新的运行 audit pack。`AUDIT_INTAKE.csv` 将项目基线、架构参考、已分析过程证据、证据不足的 ZAS pack 分开；不将每份参考资料当作一次新开发样本。

## 可归因的两个前移问题

### 真实 producer/consumer 合同没有随实现交接

LMDO 记录中的 UI 发送字段与服务器期望的 `groupIds`、`baselineGroupIds` 不一致；另一修复又把服务器返回的全局 groups 当成只含可见组的集合，造成成功写入被 UI 判失败。

可以前移：PLAN 中标明实际输入、编码/decoder、响应集合范围和重要失败行为；server HANDOFF 交付真实 fixture 或精确源/test 引用；UI TASK 必须使用这一份合同，不能两边各自构造一个相似 mock。

不能过度推断：本次不指定该项目必须改成 JSON API、OpenAPI、Pact 或另一种事务策略。计划阶段未实现的接口样例必须写 PLANNED，不能伪装成真实网络观测。

### 明确需求中的 reader 被错误归入 inspect-only

原始要求已经点名 `/dashboard/groups` 应采用全局顺序，但最初计划没有把实际需要修改的消费者归入业务验收，直到 final review 后才补 PLAN_DELTA。

可以前移：按 EDIT / VERIFY_UNCHANGED / OUT_OF_SCOPE 对直接、已命名消费者作有证据的归属；不是要求每个 reader 都必须改代码。父 section 保持业务闭环，server/UI 可为内部子项，不为跨栈资料各开一节。

## 不归因给 PLAN 的问题

上一轮还记录了已知行为/测试未完成就送审、错误等待/空命令、约 9.7 秒终态交接越序，以及最终候选缺独立 delta。这些不能靠新增技术栈 PLAN 模块解决。本轮不改 native/ZAS lifecycle、不增加验证脚本、不删除实质 review，也不宣称新知识库已经修复这些宿主或执行偏差。

ZAS 公共合同瘦身 pack 只有摘要和本地路径指向，缺实际 source/review/test 证据。不得把其声称完成当作已独立验证，也不据包小推断低 overhead。本轮仅沿用“证据不能是本机路径占位”的审计原则。

## adaptive-debugging 的可迁移结构

| 参考的实际设计 | 在 PLAN 中如何采用 | 不采用什么 |
|---|---|---|
| 统一 evidence 核心 | universal planning：真实结果、路径、未知、最小证据 | 不复制 root-cause debug 全流程 |
| 同时命中多个 causal domains | application + stack + concern 独立维度 | 不把项目归为唯一模板 |
| 有明显的低复杂度反例 | 路由到具体变更，不因 manifest 包名全选 | 不改变 Sectioned 启动条件 |
| input → transformation → output 两侧证据 | 共享 boundary example 与 producer/consumer handoff | 不建立新合同 registry 或 hash 门禁 |
| 未知要有区分性 probe | 只研究影响当前决策的未知 seam | 不默认每次在线重做全部研究 |

## 基线事实与保留

实际上传项目 VERSION=4.4.1，HEAD=50b3d43，已含 `Message Type: FINAL_ANSWER` 与 completed 双重原生终态要求。另有历史 `v4.2/AUDIT_INTAKE.csv` 工作区改动；本版保持其字节，不按旧 release 覆盖。

项目 AGENTS.md 明确不需要 previous-version baseline。输入已经移除这类目录，导致原 104 项项目测试在未修改前有两个历史归档断言失败。4.5 改为检查本次真实输入的历史文件哈希，不恢复冗余 baseline 目录；产品/流程规则断言保留。详细原始测试结果放在 appendix。

## 改进边界

新增知识必须能回答一个既有业务边界的问题，而非创造新问题。每个 playbook 都包含正/负命中、具体规划关注点、最小证据和不应扩大事项。路由信息复用 PLAN，观测信息复用现有 Audit，运行脚本、section validator、安装器、review 轮换与预算不改。
