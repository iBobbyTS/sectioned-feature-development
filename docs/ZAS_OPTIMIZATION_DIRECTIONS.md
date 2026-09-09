# ZAS 4.3.1 改进执行合同

本文件替代 4.3 的观察接口提案。用户确认先完成本包描述的 ZAS 开发，再正式使用 Sectioned 4.3.1。保留现有 facade → 单 daemon/Store → driver → 本机官方 ZCode 结构及九个生命周期工具；本轮只补公开观察、关联诊断与配套导出，不加入 Sectioned 的计划、review admission、模型分配、Git 管理或自动循环判断。

## 1. 已确认的四项变更

1. 本机确认公开 reasoning delta 的准确事件类型与文本键，只允许该路径；主动排除 `encrypted_content`，默认收集并供 observe 返回，不增加授权开关。
2. 增加 `zcode_subagent_observe`，仅在调用方怀疑无意义循环时调用。默认 top 3 工具、每类最近最多 5 次调用、无工具结果、最新 200 个 reasoning 字符。五种判断只存在于 MCP description，供调用模型判断。
3. 一个功能的流程包为 `xxx.zip` 时，ZAS 证据单独为 `xxx-zas.zip`，同目录、同 feature/run。无 `.sha256` 文件；校验值留在 JSON。它不是第二个 feature 样本。
4. Skill 只描述更新后的安装契约，没有旧 ZAS 未更新的正常降级路径。安装不匹配是配置错误；真实 runtime 故障仍按已有生命周期处理。

## 2. 先在本机确认 reasoning 精确来源

执行机器是用户的 macOS/ZCode 环境。本交接包没有访问该机器，**不得把本文或合成 fixture 的路径当作已验证真实键名**。

在 `/Applications/ZCode.app/Contents/Resources/glm/zcode.cjs` 对应的实际本机 runtime 上运行一个短、正常的隔离任务，观察 app-server 公开事件与 GUI 所展示推理的对应关系。只读确认实际 event discriminator 路径/值和文本 delta 的 JSON pointer、是否分块、一次 delta 是否含多个字符。不修改 runtime binary、不解密 opaque payload、不从隐藏字段猜测。

填写 `zas-public-reasoning-source.template.json`：真实 runtime version、event_discriminator_pointer/value、delta_pointer、证据路径和确认时间，状态改为 `VERIFIED_RUNTIME_PUBLIC`。保留最小脱敏真实事件 fixture，公开测试其对应关系。证据中不保存 `encrypted_content` 的实际值。runtime 升级导致形态不匹配时报告来源不匹配，不动态寻找任意看起来像 reasoning 的键。

### 提取顺序

1. 在新增 observation/diagnose/export 路径的任何写盘和日志之前，递归移除名为 `encrypted_content` 的键及整个值；嵌套对象与数组同样处理，禁止 base64/JSON 解码其值。
2. 匹配本机已确认的精确事件 selector，只读取已确认文本 delta pointer，必须是字符串。
3. 不回退到 `analysis`、`summary`、未知 `text`、private/opaque 字段或递归模糊查找；不改变运行 ZCode 所需的原有协议逻辑。
4. 按事件顺序拼接已确认公开文本，复用既有安全脱敏，再取最新 200 个 Unicode scalar/code point；不是 200 字节、不是 200 token，也不是 200 个事件。一次 delta 可含几百字符。
5. 公共文本通道默认开启；不增加 `observation_mode`、`detail=public_content`、`public_content_authorized` 或每次授权确认。observe 读取不触发新的模型调用。

没有 reasoning 事件时文本为空，并保留已验证来源身份。若事件掉失、buffer 丢失或来源已变化，要保留 gap/coverage 或返回实际错误；不能伪装完整空序列。现有 credential/路径脱敏仍生效，但不把公开 GLM 推理本身当作保密内容。

## 3. 观察存储：有界事实，不存工具结果

沿用已有 runtime event decoder、Store 与 bounded sink。不要增加全量永久 journal、第二 daemon、监控 LLM、相似度检测器、loop score 或自动 cancel。

### 工具统计与选择

- 统计范围明确为 **指定 agent_id 当前任务生命周期**，不是全 daemon、多个 Agent 或最后一次 poll 窗口。
- 用实际 `tool_call_id`（包括必要的 turn 身份）统计唯一调用；scheduled/started/argument-update 是同一次调用的阶段，不重复计数。不同 ID 的相同命令/读取必须保留，不按内容去重。
- 每类工具保留最近至多 5 次调用的 ID、序号和脱敏参数；arguments streaming/update 可补全同一记录，不改变次数与原调用序号。
- top 3 按调用总次数降序；同次数按最近调用序号降序，再按工具名排序。组内最近调用按序号降序。
- read 参数包含实际 path/range；bash 参数包含实际 command/cwd。缺失参数记录空对象或既有缺口，不运行工具获取补充信息。
- **observe 不保存或返回工具结果**：没有 output/result/stdout/stderr/exit result/status摘要。工具调用失败原因仍可通过原有独立 diagnose/lifecycle 查询，不塞入该快照。
- 复用现有 arguments 脱敏和大小限制，返回 truncation/redaction 信息。缺少调用结果时调用方不能断言文件未变化、命令成功或没有任何有效进展。
- 服务重启后计数/最近调用从已有持久记录恢复，或明确 coverage 不完整；不得把重置后的计数说成 lifetime 完整值。

## 4. MCP 与 CLI 合同

新增只读工具 `zcode_subagent_observe`；当前九工具不改名。**完整机器工具定义和五种判断的唯一描述见 `zas-observe-tool.json`。** 将其中 description 原样用于 tools/list，不把判断规则实现成 Rust/JS 分支，也不向响应增加 classification、loop_score 或 action。

输入固定且最小：

```json
{"agent_id":"actual-agent-id"}
```

不加入翻页游标、每次 opt-in 或 include_results 参数。本轮固定默认 3/5/200，未来如需更大窗口由新需求决定，不提前做配置矩阵。

响应见 `zas-observation-v1.1.schema.json`，包含：

- schema、agent_id、service_generation、snapshot_seq；
- count_scope=agent_lifetime；
- tools 数组最多 3 组，每组 call_count 和最近最多 5 次调用；
- reasoning.text 最多 200 Unicode 字符、实际 char_count、truncated 和本机 verified source；
- coverage：工具历史与推理窗口完整性及 dropped_events。

`reasoning.source.delta_pointer` 必须与本机核验清单一致。算法不能用示例路径代替真值。响应不带任何工具输出、progress label 或决策。

status 增加确定契约：

```json
{
  "capabilities": {
    "observation": {
      "protocol": "zas-observation/1.1",
      "public_reasoning_default": true,
      "runtime_source_verified": true,
      "defaults": {"top_tools":3,"recent_calls_per_tool":5,"reasoning_chars":200}
    }
  }
}
```

由现有 CLI parser 增加同语义命令：

```text
zcode-as-subagent observe --json '{"agent_id":"actual-agent-id"}'
```

CLI、MCP 共用同一个 daemon 查询/投影；不执行内部工具。不将 observation 内容主动推到普通 poll。完成本地 source 验证和真实查询后才能发布上述 capability。用户会先部署本改动再使用 Skill；本轮不保留 v1 metadata-only 兼容模式或假开关。

## 5. 描述层的判断与生命周期

MCP description 中保留五类调用方判断：`PROGRESSING`、`EXPECTED_WAIT`、`NEEDS_CLARIFICATION`、`NO_PROGRESS_LOOP`、`INSUFFICIENT_OBSERVABILITY`。描述中说明仅在怀疑循环时调用，用任务语义理解参数和公开推理；重复文字、read 或 echo 不能单独定罪。

ZAS只返回证据，没有状态机把这些标签写入任务 outcome、自动取消或自动修改预算。主线程可以据此继续、明确缺口、调用实际 cancel；send 仍是排队，不是 interrupt。terminal continuation、取消后 resources_reaped、close 和工作区释放沿用现有事实，不因为增加 observe 就声称已经修好 resume。

诊断异常不能阻塞 cancel/reap/final-state。一次 observe 超时或字段不足也不把原任务自动判 FAILED。

## 6. 日志与错误投影

保留4.3已有且合理的增量：第一失败原因与cleanup分开；operation/request/message/agent/session/turn关联；实际部署build/runtime身份；现有内部错误以稳定结构化 code 投影。不要重做已有诊断sink、16KiB bounded diagnose、runtime_command_failed/daemon_unavailable区分。

observation 的工具参数与公开文本只保留有界 buffer/所需投影，不在每个日志中复制；encrypted_content 在所有新增输出路径一律排除。不生成外部 `.sha256` 文件。既有 JSON receipts 中的 hashes可保留。

## 7. 成对审计交接

ZAS不承担Sectioned feature命名或复制Git；调用方已有agent_id和生命周期结果，由Sectioned包内 `zas_audit_pack.py`负责配对导出。

```text
~/Desktop/audit-pack/xxx.zip      # 主流程包
~/Desktop/audit-pack/xxx-zas.zip  # 只装这个feature/run的ZAS证据
```

主包有小型 `ZAS-LINK.json`；子包有 `ZAS-IDENTITY.json`，含与主包相同的feature/run、主ZIP文件名与确切digest。无循环hash引用。ZAS-AUDIT、物理attempt ledger、实际调用过的observe快照和相关diagnose receipts只在子包；主包保留aggregate成本与必要trace关联。

没有ZAS调用则不创建空子包。独立ZAS runtime/conformance包仍不能冒充配对包进入该目录。无 `.sha256` sidecar，内部 JSON manifest足够；打包不是额外模型任务。

## 8. 必须的实现测试与真实验收

### Parser/Store/Projection

1. 本机真实fixture只允许精确selector+key；同event的其他字段、错误selector、encrypted_content及其任意嵌套值不贡献文本、不进入新增输出。
2. 默认observe不传授权flag也返回已验证公开文本；不能增加用户确认回路。
3. 多个delta合并取最后200字符；单delta超过200、中文和emoji、重复相同文本、空delta、分块边界都正确。
4. 多于3类工具按count排序；同count用recency/name确定；每类最多最近5调用；工具结果字段全不返回。
5. 相同tool ID生命周期更新只算一次，不同ID同内容逐次保留；参数补全不重计数。
6. read路径/range、bash true/echo等参数真实可见；不读取文件结果或执行新命令补证据；长参数有截断标志。
7. 跨agent隔离；重启/丢失真实coverage；同快照重复查询幂等；observe不能改变task revision/outcome或cancel。
8. 暴露的五标签只在description/文档，不在响应schema/服务端分类器；工具与CLI输出一致。
9. 结构化错误保持第一失败，不因cleanup丢失；保留既有生命周期测试。
10. 配对审计文件命名/identity/parent digest/无SHA侧文件验收由Sectioned工具执行，无需在ZAS新建audit平台。

### 本机真实验收（不是离线fixture的替代）

- 正常只读任务：source清单与公开GUI文本对应；observe默认有最新公开片段。
- 有read/bash调用的短任务：tool参数存在、结果不出现、top3/last5限额正确。
- 用明确标注的测试fixture产生重复调用，确认ZAS只记录事实，不自行判断或终止。
- 真实cancel/reap/close与传输断开仍正确；不把同任务终态结果当作新send成功。

交付实际运行版本/构建身份、source核验清单、脱敏真实fixture、tools/list/status样例、单元/CLI/真实任务结果及未解决事项。不要声称合成测试已证明模型能可靠判断循环。

## 9. 给ZAS Codex的执行顺序

先核验本机reasoning来源 → 增量修改decoder/已有Store projection → 实现observe与description及CLI → 关联现有诊断错误 → 跑focused和真实短任务 → 更新文档/schema与安装版本。不要新增monitor、通用reasoning路由、review mode、第二daemon、终态resume workaround或Sectioned业务依赖。
