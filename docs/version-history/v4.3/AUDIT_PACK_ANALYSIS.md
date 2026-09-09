# 4.3 本轮输入与审计分析范围

## 本轮没有新的feature过程审计包

本轮提供的是Skill项目源码与ZAS项目源码，不是上一轮49包的新一轮数据。因此不重复计算历史review/repair/token比例，不声称重新运行40个业务项目，也不从“用户报告有人遇到GLM无限循环”推断当前ZAS已产生了可复现的相同incident。

分析依据：本次实际Skill4.2.1工作区、ZAS源码工作区、已有unit fixtures、实际v3.9 Advisor reference与原请求合同。两个源码ZIP的hash、HEAD和未提交文件摘要保存在`SOURCE_BASELINE.json`。历史v4.2文件按原样保留。

## 直接确认的问题

| 问题 | 依据 | 4.3处理 |
|---|---|---|
| 当前Skill与ZAS工具名/参数已经不同 | 当前source schema和facade catalog，而非旧功能摘要 | 更新当前9工具adapter，禁止猜旧alias或不存在的字段 |
| 现有activity不能输出语义停滞所需事实 | reasoning只投影bytes/count；tool只投影ID/type；缺可回放参数/读取range | 提议有界公开observation能力，主Agent结合任务判断 |
| diagnostic链路已有本地修复 | runtime_command_failed与daemon transport分开、agent diagnose、bounded writer | 保留，不重复发明日志体系 |
| 模型名字需要语义化、且在计划阶段锁定 | 用户本轮明确要求 | impl四级名称、每parent/child profile必填、TASK与真实dispatch匹配 |
| Advisor应从原生回到外部 | 用户本轮明确要求 | 恢复ADV01–06、人类交接、repo+Git、原文决策+采纳、Audit独立 |
| 本地plan_writer已删除，旧fixture却仍假定存在 | 上传HEAD25d587a与8份原agent配置；baseline99 tests有2个问题 | 保留主线程计划作者；修其持久计划交接和测试，不重新添加agent |

## 不作的推断

- 不能把high reasoning count、持续tool事件、wall time长自动判为模型循环。
- 不能把MCP tool可列出等同model/auth已验证。
- 不能把源码工作区中的新逻辑等同部署二进制一定包含它。
- 不能把queued send当作interrupt，或旧terminal结果当作新turn完成。
- 不能把observation缺失判为产品repair，也不能把runtime COMPLETED判为review CLEAN。

## 下一轮需要的试验数据

以feature/section/subsection/逻辑review slot/物理attempt关联：记录ZAS能力与部署identity、caller读取的决定性窗口、人工/主Agent语义分类、cancel/reap/close、任务最终结果和纠偏后的结果。特别统计误取消的健康长任务、遗漏的空转、观测窗口丢失、诊断本身开销和无效重试。不加新review、不重做已有业务验收，不以日志齐全为产品合并条件。
