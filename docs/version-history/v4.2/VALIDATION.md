# 4.2 验证记录

## 范围

实际v3.9 tag为基线；运行99个项目/安装/执行链/继承4.1回归测试，以及15个保留3.9工具回归测试：**114/114 unittest通过**。另独立运行section_plan.py断言测试通过。完整用例名和原始日志SHA见OFFLINE_TEST_RESULTS.json。

- 两个Skill通过上传skill-creator的quick_validate。
- 完整旧PLAN模板通过section_plan.py和新workflow.py两项验证；2父section/DAG有效。
- 9个TOML agent、6个model–effort组合；测试解析配置、安装两Skill、backup、dry-run、不覆盖AGENTS/无关agent。
- 39个原3.9 skill文件都存在对应路径，13个原template职责未删除；原Advisor request字节/hash保持。
- 当前工作集初始化、PLAN作者结果落盘、独立review receipt、requirements实际文件/hash、TASK/contract/handoff、role/HEAD/evidence负向测试通过。
- 子checkpoint不是parent acceptance；缺joint oracle/parent reconciliation/fresh final不能接受；parent写入不影响独立worktree，但被review候选变动会invalidate。
- 多section/multi-child no-commit被拒绝；closed feature拒绝默认再批准；结构恢复保留lifetime counter而非child reset。
- Audit OFF仍创建执行artifact；LIVE初始化trace；process-only kind/producer/Git身份验证，foreign kind与stale head被拒；canonicalZIP原子/幂等/reentry测试通过。
- 活跃Markdown相对链接、anchor与长reference目录检查通过；Python运行脚本编译通过。

## 测试发现并修正的实际问题

1. 旧4.1 DAG测试误读新4.2模板：改用明确标注4.1的历史fixture，保留原测试而非降低4.2门禁。
2. 新测试把launch receipt和review result写到同一路径，正确触发hash mismatch：改成两个不同fixture文件名。
3. 新typed audit测试使用product_head而非source_head：按实际schema修正fixture，并增加stale-head拒绝测试。
4. 前置reservation需绑定实际spawn ID：增加显式替换自己的reservation与拒绝其他actor占用的逻辑及回归。
5. Root description超过skill-creator 1024字符：只缩短metadata重复措辞，不删除正文职责。

## 未经验证与限制

没有运行真实Codex/ZCode、任何付费模型或用户仓库test/live服务。所有actor/model结果是明确标注的合成fixture；本地hash/ID检查不能认证供应商，不能证明review语义正确或planner必然遵循。模型分层来自用户授权的4.0假设，不是本轮matched benchmark。

旧历史源码、文档、trace不能被事后伪造成4.2执行记录；新门禁前瞻生效，不因此重开accepted历史工作。完整旧state职责恢复不表示能阻止主模型绕过全部工具直接改文件，宿主权限仍需实际验证。

## 打包

项目ZIP以sectioned-feature-development/为唯一根。打包器随后校验CRC、逐文件SHA和Unix权限，排除.git、__pycache__、.pyc、.DS_Store、__MACOSX；无原始audit ZIP、session JSONL或用户credentials。结果计数见PACKAGE-VERIFICATION.json（项目外，避免自引用hash）。
