# 4.3 Validation

## 输入基线

Skill使用上传4.2.1工作树HEAD25d587a，保留两份reviewer本地修改及旧history。输入baseline运行99项project测试：97通过、1失败、1错误；两项分别为已删除plan_writer后的旧agent计数和不存在的历史Advisor模板路径。不是本轮ZAS产品缺陷。

## 本轮验证

- Project unittest：132/132 PASS（含原回归与本轮新增），见同目录PROJECT-TESTS.txt。
- 保留Skill工具unittest：15/15 PASS；单独section_plan断言脚本通过。两组共147项unittest。
- ZAS原源码的diagnose/public-schema Node fixtures：17/17 PASS，无源码修改。
- 两份Skill用附件skill-creator quick_validate检查。
- Python编译、JSON/TOML解析、Markdown本地链接与长reference目录检查。
- 原v3.9 Advisor请求合同保持365字节、SHA-256相同。
- 当前scope/review/recovery/parallel和全feature review-provider cursor不因重命名、ZAS失败或Advisor而重置。

新回归包括：所有父/子项显式profile；错模型/effort/role或旧TASK禁止write；main作者不等于main implementer；Audit OFF仍受外部Advisor barrier；结果未采纳不解锁；人类采纳保留预算；clarification保留原文；普通/linked-worktree完整Git与bundle；secret命中阻止export；ZAS工具+capability双重协商；stream/cursor/gap/visibility/loss校验；重复实际动作不按文本去重；空观察不判无进展；旧Agent显式备份迁移。

## 未执行/不能据此声称

没有在用户macOS执行Codex、官方ZCode、真实GLM任务或任何付费模型调用；没有构建或更新ZAS binary；没有实现建议的observe端点。离线JSON窗口只校验来源声明/游标/结构，不能认证provider或自动证明语义停滞。压缩Git历史中的secret仅人工评估，不宣称扫描已认证全历史安全。

PLAN-FULL模板校验通过；proposed observation JSON Schema与样例通过结构验证。早期history文件、两份本地reviewer修改、365字节Advisor合同逐字节保持。共52份当前Markdown完成本地链接/anchor与长reference目录检查。最终ZIP校验清单另记录。阶段中一次工具测试组合命令超过容器调用时限；其中15个unit实际已打印OK，剩余section_plan脚本随后单独执行通过，没有将未运行算通过。
