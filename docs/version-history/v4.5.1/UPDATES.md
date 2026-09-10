# v4.5.1 修改依据与保留

| 用户确认/证据 | 本次修改 | 不改变的东西 |
|---|---|---|
| domain 与 language 必须分离 | 14 工程 domain、20 语言/语言族目录 | 原业务 section/subsection 划分原则 |
| 用户列举只是例子 | 结合公开使用/角色/仓库活动扩展常用覆盖 | 不把调查排名用作模型等级或项目架构建议 |
| 框架和平台仍不能混成领域 | 19 adapters，明确 frameworks/runtimes/platforms 三类 | 不要求存在依赖就加载所有资料 |
| 同一语言跨领域、同一领域跨语言 | 独立路由、部分匹配与有证据的负例 | 一份 PLAN、一次既有 review、同一边界一份 fixture |
| 新旧知识职责需完整保留 | 五个混合文件拆分/迁移、MIGRATION 对照 | universal/boundary/four concerns 逐字保留 |
| 可执行连接要同步 | 根 Skill、PLAN 请求/模板、PLAN reviewer、Audit route notes、README 和维护者测试更新 | 九份运行脚本、安装器、companion、七角色模型绑定均不变 |

没有恢复 workflow.py、execution_artifacts.py 或 advisor_flow.py；没有新的 runtime router、registry、验证 gate、review pass、JSON receipt 或审计文件要求。新增 JSON 只在维护者的研究/测试资料中，不参与产品执行。

项目历史不改写，不复制 previous-version baseline。原 v4.5 测试中的固定旧目录期望更新为新分类，原回归职责仍检查；原12个组合例子迁移了引用，另增加独立维度反例。测试只能证明文件/配置/预期案例完整，不证明 Agent 实际选择正确。
