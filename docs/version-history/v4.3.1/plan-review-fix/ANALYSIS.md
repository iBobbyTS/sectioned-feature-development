# Skill 工作区、PLAN review 与 ZAS 单服务计划核验

## 结论

本轮不是“Skill 没变化，所以模型基本确定是假冒”这个二选一。真实结论是：**3.9 的防膨胀正文基本保留，但 4.x 的可执行验收与它发生冲突；本地又增加了一条无授权的双重 reviewer 义务；执行中也确实反复做了完整 PLAN review。** 这些事实足以解释目前问题的一部分，不能据此认证或否认第三方模型身份。

提供的是当前 4.3.1 的定点修正文件和 patch，不是新一轮大版本重写。没有修改 ZAS 或 LMDO 产品源码、它们的 PLAN/STATE、用户仓库 Git 历史或本机服务。

## 1. 输入与 Git

三份本次 ZIP 均可解压，Skill 的 `.git`、Git tag、工作区以及两个产品的源码/计划可读取。

| 对象 | HEAD | 分支 |
|---|---|---|
| Skill project | bebb8a09f6a941c79e9be6bbdd9d01baa68193eb | main |
| ZAS | e0f76e66740b9a93a43b2bfe2da33510f41ccd33 | codex/shared-mcp-lifecycle |
| LMDO | a0b9a85c7a91d56e715dac146e16e32748e6053a | feat/musician-instrument-reorder |

本次 ZIP 对部分 build/static/test 路径有省略。解压后的删除标记不自动视为用户或 Codex 真正删除了这些文件；必要源码用 Git object 交叉核对。未运行 macOS/Cargo/ZCode/Codex live 测试。

## 2. 工作区不是一批都应撤销的未知改动

Skill 工作区共20个 modified/untracked 文件。与实际已交付的 `sectioned-feature-development-v4.3.1-project.zip` 对照，15个逐字一致；5个含后续本地改动。逐项见 WORKTREE_PROVENANCE.json。匹配说明内容来源有明确对照，不证明到底由哪个 session 写入。

保留的15项主要是：运行 VERSION/openai.yaml、observe与ZAS-AUDIT协议、paired audit、identity/link模板、zas_evidence、zas_audit_pack、audit/advisor打包修订等。这些就是用户已批准的4.3.1，不应整体回滚。

5个混合文件为 SKILL.md、artifact-lifecycle.md、external-reviewer-orchestration.md、subsections.md、zcode-mcp-adapter.md：

- **撤销**“每次 code review 都必须内部 code_reviewer，ZCode 另做补充”的修改。它把原生→GLM交替改成了原生审查之外再补GLM，与原授权和执行器本身允许GLM占slot的行为冲突。
- **保留**同候选一次只有一个reviewer、实现/handoff完成后才派发、确认终态后才能重试等新增时序规则；不重新全局串行化独立父section。
- **保留**`zas diagnose`、结构化错误、SDK/JSON-RPC失败层级和磁盘/运行身份区分。这与上次单文件更新一致。

发现另一个不完整安装迹象：根 VERSION 仍为4.3，运行 VERSION 已为4.3.1；tests/test_v43_zas.py 仍期待已经移除的 check_window/额外公开推理授权/baseline fallback。原样执行项目测试：132项，1失败、12错误。修订只从原交付4.3.1同步这些测试、配套contract和版本，不把实现退回4.3来迁就旧测试。

## 3. 与真实3.9比较

基线为真实 `v3.9` tag `e21c9a3e525fa7d3da0fb71fc3eeb12cf25c591c`，不是后续报告对3.9的复述。

| 文件 | 3.9 | 上传版 | 结果 |
|---|---:|---:|---|
| references/section-planning.md | 285行 | 295行 | 前285行逐字一致；只有4.2阶段经验补充 |
| assets/PLAN-REVIEW-REQUEST.template.md | 104行 | 109行 | 前104行逐字一致；只有持久回执补充 |
| references/scope-control.md | 174行 | 174行 | 完全一致 |

必要性先于内部正确性、不能由PLAN创造authority、无全仓audit、一次主PLAN review、必要时一次delta、无递归full loop等均未消失。

**但文字相同不代表运行合同相同。** 4.x新引入的 execution_artifacts.record_plan() 原来要求原始 reviewer 同时满足 `result=APPROVED` 且 `plan_sha256==当前PLAN hash`。这与3.9“普通修正由主线程处理，机械校验后继续”冲突；主线程拒绝不成立的候选，或修正不改变边界的文本后，也无法落下有效gate，容易被迫再发review。

本补丁恢复主线程的admission职责，不删除独立review：

- 原始report及reviewed-plan snapshot必须保留；不改写NEEDS_CORRECTION为reviewer CLEAN。
- 所有候选有明确disposition、reason、evidence，所有实际未关闭finding仍阻塞。
- parent closure绑定原report hash、最终plan hash和实际改动区域。
- 已知machine boundary（feature/run、需求、owner、依赖、模型、执行模式等）发生变化会拒绝该快捷路径，要求真正的PLAN_DELTA。
- 未改变的旧exact APPROVED路径兼容，既有accepted工作不迁移。
- 检查不能理解任意自然语言，主线程仍须核查语义authority。它不是让主线程任意自批，也不是模型身份认证器。

仅靠状态字符串或不存在的report仍不能推进。Audit OFF时同样有效。没有新增review阶段、repair预算或proof framework。

## 4. ZAS各轮审查：必要问题与过度细化并存

当前feature保存7份完整PLAN review和1份PLAN_DELTA。另有早期未产出结果的尝试。后续R2–R7并没有变成真正的delta-only检查。Trace未完整覆盖后几轮，不能从文件mtime或轮数推算精确active time。

| 阶段 | 有价值的发现 | 过度细化/执行问题 |
|---|---|---|
| Primary | 连续MCP vs 单帧RPC、S01验收依赖S02、facade owner/测试遗漏、重启恢复路径 | reviewer把自己的候选写为admission；scope由parent负责 |
| Delta | endpoint定位、native payload交付、probe创建owner | 后续仍重开full review；有限delta没有真正约束调用者 |
| R2 | 计划schema/依赖解析错误、Codex-only更正、transport分层矛盾 | 机械校验应先于模型审查；新增文件尚不存在不等于计划不可执行 |
| R3–R4 | 保持canonical dispatch与error owner、真实Codex配置入口 | 要求提前冻结私有probe文件名、JSON字段/版本、精确Tokio/RMCP类型API；超出了“可实施计划”通常所需 |
| R5 | 新写入计划的CLI/类型/accept-loop矛盾会造成真实失败 | 部分错误是为满足前轮细节冻结要求而引入；越来越像PLAN里先写一版代码，再review那版伪代码 |
| R6 | check ID悬空；未连接时不能由不存在的MCP server返回ToolError | “两个调用方”可直接解释为两个Codex连接，不能自动等同扩张到Claude；不值得再触发全量发现 |
| R7 | 保存APPROVED并检查前述关闭项 | 状态仍指向旧run/hash；S01仍残留未来adaptor验收依赖 |

缺少实际编译能力、owner路线、并发/退出语义时，相关plan finding是合理的；不是所有“技术细节”都该忽略。关键分界是：**已有跨owner/公开消费者是否真的需要这一细节在实施前固定**。私有helper或probe字段通常留给implementer，错误由代码/测试检查，不要求整个实现预写在PLAN中。

例如 R5 将“S02执行S01拥有的脚本并写测试输出”等同于“修改S01源码owner”，需区分源码写权限与合法运行产物。重复污染同一输出目录是真问题；执行同一个既有脚本本身不是越权。

R3声称仓库强制每次Cargo先clean；本包AGENTS.md中没有找到该条。不能排除本机更高优先级配置另有规定，但在没有该authority前，不应把它当作已证明的仓库门禁。

## 5. 当前ZAS架构与scope

已确认的需求后来收窄为Codex-only；允许一个无状态stdio代理。当前方案为：

```text
Codex client -> per-client transparent stdio bridge
             -> one daemon-owned MCP Unix listener
             -> existing RpcService/Scheduler/Store
```

这将MCP server/tool router搬入唯一daemon，但不会消灭所有每客户端OS进程。现有Unix RPC保持单帧协议；MCP使用同daemon中的独立持续连接endpoint。这不是第二个daemon。

在该已确认合同下，两个业务section/四个subsection与范围匹配，无须第三个section，也无需新registry、重试系统、远程兼容或监控服务。两个有界live脚本分别验证daemon及真实Codex consumer，有业务验收依据；问题是把其内部schema提前绝对冻结并反复审查，而非脚本数量本身。

### 尚需一处边界修正

PLAN-FULL S01-B第131、135行要求透明adaptor的stderr+非零退出。adaptor实现属于S02-A；S01明令不改facade。这个S01验收仍依赖未来S02。

应将client/adaptor专属证据移到S02/集成，S01直接用MCP连接验证daemon的listener、并发、EOF、shutdown/recovery和持久任务。临时旧facade/new daemon handler共存是迁移中间态，应说明而不是立即要求两个section同时完成。

子项文本中的TWO只可描述父级风险，不新增每child独立final、PLAN review或budget。

### 执行状态仍未闭合

当前PLAN hash `2ef243bd...`、run r2，R7批准该hash。STATE却是run r1、旧hash `6b0e2118...`、NEEDS_CORRECTION、actors={}。不要只改一个APPROVED字符串；应保留原报告、查回真实派发回执，完成上述有界delta和parent admission，再启动S01。

## 6. LMDO

当前合同仍是同组乐器拖拽排序、既有权限、release保存、last-save-wins、成功静默、失败加载并定位组。审核持久化入口、权限、filtered-set和navigation行为均有依据。

现存PLAN-REVIEW只有237字节摘要，没有完整原始finding/reviewer回执，因此不能独立判定这些审查是否scope creep。当前能重现的是machine block把子项写成`children`而不是`subsections`，validator因此报“fewer than two real increments”；STATE.json缺失。先机械修正与补齐真实证据，不因格式错误再启动全量PLAN review，也不新造历史审查结果。

## 7. 模型真实性的证据边界

本机agent配置写`model=gpt-6-astra`只证明请求意图。当前附件没有足以认证实际供应商或实际后端模型的受信任运行信息。Codex允许选择provider/base URL与配置项；非官方服务返回相同model字符串也不提供模型权重证明。

官方参考（本轮查询）：https://developers.openai.com/codex/config-reference 。其中`model_provider`、`model_providers.<id>.base_url`、`model_reasoning_effort`可改变请求路径/设置。不能从模型自报、语气、慢/快、或“Skill文本没变”推定真伪。

要研究渠道可靠性，应冻结相同任务/源码/计划/effort/工具权限，比较官方与当前接口的多次独立结果，按无authority blocker、漏检、无效重审和最终正确性计数；保留脱敏有效配置与可核查上游身份。这样的对照能发现质量差异，仍不是单次行为鉴伪。本轮没有进行这个付费实验。

## 8. 修订范围与验证

本补丁只恢复原交替、保留正确本地时序/diagnostics、修复parent plan admission矛盾、补充PLAN充分性边界、更新同名plan reviewer developer instructions，并同步漏装的既有4.3.1测试/contract/version以及配套code-review标题/observe说明；不改变其委托协议。

没有新增模型组合、更多PLAN或code review、子项预算、Advisor架构、ZAS监听协议、自动语义loop classifier或Audit平台。没有修改已有版本历史。

验证详情见VALIDATION.md；实际模型/本机服务行为没有测试，不能承诺以后绝不发生模型执行偏差。
