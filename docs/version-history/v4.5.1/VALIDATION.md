# v4.5.1 验证记录

## 基线与实际执行

输入是本会话已交付的 `sectioned-feature-development-v4.5-project.zip`，311 个文件。没有使用另一历史项目替换基线；没有创建 previous-version baseline 副本。

| 检查 | 实际结果 |
|---|---|
| 输入 v4.5 项目 tests | 121/121 PASS |
| v4.5.1 项目 tests | 139/139 PASS |
| 保留 Skill 工具 tests | 15/15 PASS |
| 总离线 unittest | **154/154 PASS** |
| 两份 Skill Creator quick_validate | PASS |
| 基础 PLAN 模板 | VALID：2 sections、2 subsections；结构校验职责未变 |
| 当前文档相对路径、anchors、长 reference Contents | PASS |
| 七份 Agent TOML | 可解析；name/model/effort/sandbox 保持 |
| 安装器 dry-run | PASS：两份 Skill + 七份 Agent，未写真实 CODEX_HOME |

首次新测试执行时，本记录尚未生成，README 链接检查发现一处 missing VALIDATION.md。补齐实际记录后全部通过。独立 Markdown anchor 检查还发现 boundary-handoff 指向旧 examples heading；已保留原 LMDO failure 示例及其 anchor，并更新其中路由维度，没有修改共享 handoff 文件来隐藏问题。

## 新测试的真实含义

18 项新增维护者测试检查分类互斥、同语言多领域/同领域多语言、adapter 类型、旧知识迁移、负命中、未知回退与原文件保留；原 17 项 v4.5 知识测试保留其职责，更新了旧目录/版本期望。

新增 38 个组合场景，原 12 个场景按新路径迁移。这些是人工预期 fixture，只验证资料和例子可达、无明显自相矛盾，**不是模型已正确分类的实验**。没有增加产品运行时 router/registry/schema gate。

## 保留与明确迁移

- 输入311文件：290个逐字不变；16个本轮明确修改；5个混合domain文件迁移到typed guides，不是丢弃其职责。
- 输入205份历史文件逐字不变，包括旧版本的原始prompt、研究和本地保留记录。
- 九份运行脚本、五份保留工具测试、安装器和整个 code-review目录逐字不变。
- 七个模型/effort/sandbox配置不变；只改 plan_reviewer 的知识路由措辞，其他六份Agent文件逐字不变。
- universal、boundary-handoff、四份concern逐字不变。
- 不恢复 workflow.py/execution_artifacts.py/advisor_flow.py，不增加review pass、receipt或运行阶段。

`RETENTION.json` 是维护者发布核对记录，不是运行时 gate。

## 打包验证

最终完整项目与单独Skill各以正确目录为ZIP根，排除 `.git`、Python缓存、`.DS_Store` 和临时生成脚本。校验CRC、逐文件内容和Unix权限；patch在独立输入副本应用后与发行内容比对。具体大小/hash/数量记录在交付的 RELEASE-RECEIPT.json，不创建 `.sha256` 侧文件。

## 未执行或未证明

未调用真实Codex/ZAS/付费模型，未运行用户应用、跨语言服务、移动/桌面/嵌入式产品测试；未验证当前分类一定降低耗时/token或减少缺陷。本地测试不能证明Agent会正确命中所有维度。外部资料用于机制与覆盖依据，不是模型能力或性能排名。
