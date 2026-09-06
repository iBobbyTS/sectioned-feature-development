# 4.2 研究与事实边界

## 方法

本轮要求是从3.9恢复，不是重新猜模型排名。证据优先顺序：用户本轮授权 → 实际Git v3.9文件 → 上传4.1及其4.0历史研究 → 本批原始审计 → 有限当前官方API/配置核验。旧助手在聊天中的“已经实现/测试通过”不作为代码存在证明。

## 一手文件

- 真实v3.9 tag及完整保存副本：`baseline-v3.9/`。主Skill的原始495行和全部模板/refs/scripts可核对。
- 上传4.1源码：subsection、workflow调度器与负向测试；按授权移植，不把4.0的95行缩写根Skill作为起点。
- 上传4.0版本研究：保留在项目`docs/version-history/v4.0/`；模型分级/cheap explorer/Advisor/并行原则作为**继承设计假设**，不重新声称它们的相对性能已经得到本轮实验确认。
- ZCode功能说明：固定九个zcode_subagent工具、workspace调用方自管Git、send队列和终态拒收、cancel回收、plan权限模式不等于完整只读隔离。不得复活3.9旧工具名或拟议resume接口。
- 49包分型与40个流程阶段分析见同目录Audit报告。P05/P12/P17/P18/P22/P32/P34/P37直接支持本轮变更。

## 外部核验（2026-09-06）

### 官方文档，高可信、只证明公开配置/行为

1. OpenAI Codex Subagents：https://developers.openai.com/codex/subagents （本次重定向到 https://learn.chatgpt.com/docs/agent-configuration/subagents ）
   用于核查agent文件/角色配置与子代理职责；本项目配置使用上传4.x已采用的name、description、model、model_reasoning_effort、sandbox_mode、developer_instructions。无法据文档证明某用户账户有模型权限，或宿主实际提供了fresh上下文；这些要在执行时检查。
2. Git worktree：https://git-scm.com/docs/git-worktree
   官方说明linked worktree有各自工作目录/HEAD和部分共享Git metadata。因此4.0的并行隔离仍须检查共享契约、锁文件、数据库/端口等资源，不把不同目录当作语义独立证明。

### 继承研究，不当作本轮新实测

4.0研究里的成本/智能路由和Advisor/Orchestrator区分被按用户要求保留；没有新增一项依赖未知benchmark的自动降级策略。Advisor使用Astra xhigh，是独立上下文技术裁决，不是主线程更强版本的假定。主线程也是Astra时仍须fresh-context；无法证明隔离就阻塞，不使用“忽略前文”替代。

## 不做的外推

- 本批审计不包含matched task/model/effort对照，不能量化四档实现模型的最佳边界或节省百分比。
- 工作流文件变短不代表质量更高；未证明冗余的3.9条款保持。
- 零finding不能证明那轮review无价值；大LOC（尤其snapshot）不证明任务高复杂。
- 本地artifact哈希检查能发现缺失/篡改/陈旧，但不能证明文本是模型真实生成，也不能证明测试oracle正确。
- 40包不是40次重新执行的产品测试，本报告不重新签发这些项目的merge许可。
