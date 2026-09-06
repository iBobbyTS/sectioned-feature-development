# 4.1 验证记录

## 已执行

- 完整项目 unittest：**70/70 PASS**，原始记录在 `VALIDATION-TESTS.txt`。
- 两个当前Skill（sectioned-feature-development/code-review）均通过提供的Skill Creator quick_validate；两个openai.yaml由其生成器重建。
- Python compileall、8个TOML解析、6组model/effort固定组合、活动Markdown内部链接均通过。
- Advisor请求模板与上传原项目逐字节保持；见ADVISOR_CONTRACT_PRESERVATION.json。
- 原子schema4计划继续可用；带点号的历史ID不会自动变child。
- 真实临时Git/worktree验证隔离、branch与ignore；review预留幂等；child预算继承、不能第六次换名reset。
- Child parent绑定、单层限制、scope子集、same-parent依赖、共同oracle覆盖、CHECKPOINT与父ACCEPTED分离均有负例。
- Parent验收必须覆盖完整checkpoint链、源parentbase、共同oracle、无openfinding及适用freshfinal。CLI还核对Git ancestry与实际artifact文件hash；metadata本身不能证明测试真实性。
- Installer dry-run/新装/明确replace备份/只更新code-review/拒绝symlink与保留无关用户配置测试通过。原ZIP缺currentcompanion的打包问题在本次补齐。

## PPPMS提案

- 45父section，四父各2child；原parent字段全部逐项相等，DAG、integration_order、check registry未改变。
- Requirements原字节保持：`7e515fa766e7c546f9a291dcef7a64c7111a483981cf515be6b7f0852dbdd50d`。
- 所有parent read_paths在输入源码ZIP中存在；新增Rusttarget仍为计划，不当成已实现。
- 演练证明B02仍active时C03.u1因共享Cargo锁冲突不能启动；B02假设接受后可提议C03.u1，但C04不能通过子节提前解锁。
- 计划仍DRAFT，不生成可覆盖实际STATE的bootstrap；原current cursor/recovery/model override必须在本地合并时保持。

## 验证中修正

首次67项出现3个交付/fixture问题：继承测试引用旧history目录名、README版本替换形成不存在的链接、原资源冲突fixture缩小parent读取范围却未同步示例child。修正后68通过；随后加上parent openfinding阻塞和original lineage count继承两项，最终70通过。另对parent checkpoint无遗漏链、真实artifacthash/Git ancestry新增负例。没有把失败隐藏成产品通过。

## 未执行与限制

没有运行PPPMS Rust/Python/DB/live产品测试，没有调用用户Codex/ZCode或测量模型表现、没有真实多代理成本对照。工具测试是workflow/schema/metadata/临时Git与安装检查，不是无bug证明或更低token承诺。当前ZCode仍无终态resume，same-session差异照实记录。

ZIP CRC、成员内容与Unixmode、MANIFEST逐文件SHA在打包步骤校验；archive摘要在外部.sha256，不写入自指循环manifest。
