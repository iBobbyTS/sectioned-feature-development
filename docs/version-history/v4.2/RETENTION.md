# 3.9职责保留与授权替换清单

原始基线完整位于`baseline-v3.9/`。文件级哈希见`RETENTION.json`。本表沿用人工清单35个编号，不将“合并文件”混淆成删除职责。

| 编号 | 职责 | 4.2处理 |
|---|---|---|
| A01 | Canonical工作集初始化 | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A02 | 独立Requirements与PLAN关联 | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A03 | 计划作者返回后落盘 | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A04 | PLAN review/result/admission | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A05 | 当前section提取合同 | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A06 | 真实首次委派与main禁产品写 | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A07 | 实现/修复handoff | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A08 | 累计review/admission/repair/closure | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A09 | 完整可续跑状态 | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A10 | 归档/瞬态清理 | 保留职责，补明确落盘/实际调用回执/文件引用/恢复操作；STATE提供机器事实，FEATURE-STATE完整渲染。 |
| A11 | 时序违规恢复 | 按授权4.0并行改为候选/父级屏障；独立父项可以隔离并行，当前review候选不允许写。 |
| B01 | 触发数值软参考 | 保留3.9规则与相应模板/reference/工具。 |
| B02 | 自动审批前探索边界 | 保留3.9规则与相应模板/reference/工具。 |
| B03 | audit remediation冻结finding集合 | 保留3.9规则与相应模板/reference/工具。 |
| B04 | 晚采用active合同scope清洗 | 保留3.9规则与相应模板/reference/工具。 |
| B05 | 安全finding threat-model证明 | 保留3.9规则与相应模板/reference/工具。 |
| B06 | 拒绝未授权持久化/治理/testframework | 保留3.9规则与相应模板/reference/工具。 |
| B07 | scope增长信号与先简化机制 | 保留3.9规则与相应模板/reference/工具。 |
| C01 | PLANfinding分类 | 保留3.9规则与相应模板/reference/工具。 |
| C02 | INITIAL/DELTA/FINAL检查范围 | 保留3.9规则与相应模板/reference/工具。 |
| C03 | stickycoverage | 保留3.9规则与相应模板/reference/工具。 |
| C04 | fullreview reset正反例 | 保留3.9规则与相应模板/reference/工具。 |
| C05 | DEFERRED_OWNER | 保留3.9规则与相应模板/reference/工具。 |
| C06 | 无artifact仅一次重试 | 保留3.9规则与相应模板/reference/工具。 |
| C07 | 三层验证时点 | 保留3.9规则与相应模板/reference/工具。 |
| D01 | hardcap快照backup诊断 | 保留3.9规则与相应模板/reference/工具。 |
| D02 | 六类recovery | 保留3.9规则与相应模板/reference/工具。 |
| D03 | 恢复额度与最多两个真实descendants | 保留3.9：五普通波；一次非结构恢复只给一命名额外波；真实结构替代可fresh5但recovery_used=true。子项/模型变化不刷新，原lineage可追踪。 |
| D04 | 独立integration累计预算 | 保留3.9规则与相应模板/reference/工具。 |
| E01 | agent-work排除检测 | 保留3.9规则与相应模板/reference/工具。 |
| E02 | traceinitappendvalidatesummary | 保留原工具；审计证明事件词汇漂移，添加开放family与模型/子项/并行/Advisor字段。 |
| E03 | session过滤脱敏导出 | 保留3.9规则与相应模板/reference/工具。 |
| E04 | audit触发scope反事实合规分析 | 保留3.9规则与相应模板/reference/工具。 |
| E05 | firstfunctional milestone成本 | 保留3.9规则与相应模板/reference/工具。 |
| E06 | finalizer幂等原子receiptGit核对 | 保留原finalizer；添加process-only身份与原始Git核对；没有另建默认打包流程。 |

## 明确授权替换而非声称原样保留

- 老模型角色→用户命名的九角色/六组合；原PLAN/full/delta/repair职责不删。
- 手工Pro Advisor默认调用→4.0原生有限上下文Advisor；原请求合同完全保留，旧完整仓库导出工具只历史备用。
- 全局单活跃section→4.0独立worktree DAG；同候选冻结不变。
- 旧MCP接口→上传真实九tool协议；终态无法resume如实记录，不假装恢复。
- 父PLAN/contract+当前节提取→增加4.1子项；业务section仍是唯一验收/预算单位。

## 机械联动的范围

新增检查只补本次回归：文件/哈希/真实返回ID对应关系、父候选冻结、已完成PLAN不可默认续写。它不能从文件内容认证供应商或验证业务正确性。既有3.9提示职责有保留，辅助检查不是新产品安全模型或第二套审查阶段。
