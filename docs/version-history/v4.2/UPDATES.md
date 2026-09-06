# 4.2 更新依据

每项修改要么来自本轮明确授权，要么有原始audit证明。不是从4.0继续做更大validator/framework；保留3.9的可解释操作职责，只用本地file/Git/receipt检查补先前执行链断点。

| ID | 修改 | 依据 | 具体结果 |
|---|---|---|---|
| R01 | 基线恢复 | 用户要求从3.9 + 真实tag | 保留原执行规程、13模板职责、11refs及audit/session/recovery工具；只把完整状态图搬到必读生命周期reference以保持根入口可阅读。不是删职责。 |
| M01 | 多section提交分支 | 用户明确1；P32 | >1父section或>1可执行子项强制独立branch + EXECUTE_WITH_COMMITS；明确no-commit冲突则问owner。 |
| M02 | 完成后新请求 | 用户明确2；P17 | CLOSURE保存旧plan/head，后续请求重新分类；显式重开才建新revision，不清旧lineage。 |
| M03 | subsection | 用户明确3；上传4.1 | 业务父section内按真实模块或模型推理负荷细分；串行checkpoint、父reconciliation、一次父final、共同repair预算。 |
| M04 | 角色重命名与分级 | 用户明确 | 九角色/六model-effort组合；所有运行Markdown使用subagent链接，配置/CLI用相同ID。 |
| M05 | Native Advisor | 用户明确继承4.0 | 请求合同保持原字节，fresh limited-context只读原生advisor；不继承全对话；audit OFF仍存在。旧manual pack脚本保留作历史工具，不默认执行。 |
| M06 | 并行 | 用户明确继承4.0；P37 | 独立父项read/write/contract/resource DAG，两writer起始值；候选不边写边审、集成串行验证mergedHEAD。替换全局串行锁是授权变化而非无据精简。 |
| E01 | 执行artifact联动 | 3.9职责恢复；P12/P18/P34/P37 | 主线程保存完整PLAN、实际spawn回执/报告、TASK/contract/handoff/ledger。STATE给调度，FEATURE-STATE完整渲染而非双份人工状态。单字符串不解锁新4.2执行。 |
| E02 | Audit纯流程命名空间 | 用户明确；9辅助包/P06/P07/P28 | 保留aux证据但不计独立样本；typed kind/producer/feature/run检查，原finalizer原子/幂等/receipt仍在。 |
| E03 | PLAN已有lens落到例子 | P05/P10/P15/P18/P24/P26/P27/P29 | 补生产调用链、precedence、交互时序、算法cardinality、validation环境，使用原3.9单PLAN及有限delta规则，不增通用轮次。 |
| S01 | 验证去重 | P22明确删除每节重复Django check；3.9已有复用条款 | 只复用相同相关输入/环境证据，targeted和final gate保留；没有因省token删除任何review义务。 |
| S02 | 事件词汇兼容 | 多包可解析trace仅未知事件而降级 | 保留3.9trace工具并增加open event family；明确语义缺口仍degraded，结构坏才invalid；不迁移/补造旧事件。 |

## 明确没有做的简化

没有删除PLAN-FULL、PLAN抽取、SECTION-CONTRACT、HANDOFF、PLAN-REVIEW、累计REVIEW ledger、FEATURE-STATE、hard-cap diagnosis、范围审查、安全威胁模型证明、reset正反例、DEFERRED_OWNER、五波上限或独立integration预算。
没有给每个subsection单独PLAN gate/ONE-TWO/final/recovery；也没有为了模型省钱把相互依赖的规则强行拆独立section。没有取消真实子代理，audit OFF不能关闭执行artifact。
没有将3.9恢复预算悄悄替换为4.0更抽象规则：保留一次非结构named额外波，或真实结构replacementfresh budget但继承recovery_used；子项/模型/重命名不算replacement。详见RETENTION。
没有因将root状态图移入reference而省略时序；root必读链接，diagram完整保留。没有保留两套可同时执行的ZCode接口；active adapter严格使用当前功能说明，旧协议只在历史证据。
安装项目包含配套code-review，不重演4.0遗漏安装的协议冲突。保留已有standalone审查用途；delegated上下文只给候选和证据，父层验收。

## 生效与迁移

新的4.2执行必须有真实本地artifact/调用ID。历史4.1/4.0计划仍可读取检查，但不能仅改version冒充4.2证明；当前active工作前瞻补真实能取得证据，已接受历史只记gap，不重跑旧实现/review。完整旧history保留在docs，runtime只安装当前两skill和九agent。
