# v4.5 验证记录

## 实际输入

- 上传项目 `sectioned-feature-development(6).zip`：VERSION 4.4.1、HEAD 50b3d43 的工作树。
- 保留本地 FINAL_ANSWER + completed 规则，以及历史 v4.2 CSV 未提交内容。
- 没有使用另一个完整 release 的旧文件覆盖这个输入。
- 没有创建 previous-version baseline 副本。

## 原输入的测试状态

未修改前运行项目测试：104 项，1 failure + 1 error。两项都要求输入已按 AGENTS 删除的旧 baseline 目录存在。日志在 `appendix/BASELINE-TEST-RESULT.txt`。

本版修改历史测试的证据来源为实际输入哈希；保持运行脚本不存在/存在、角色绑定、原生/ZAS隔离、顺序、review与安装备份等原断言。版本断言更新为4.5。没有改变 runtime 代码来迁就测试。

## 最终执行

| 验证 | 实际结果 |
|---|---|
| `python -m unittest discover -s tests` | **121/121 PASS**（原104项职责测试＋17项新知识/接线/保留测试） |
| 保留 Skill tools 的 `unittest discover` | **15/15 PASS** |
| 总 unittest | **136/136 PASS** |
| 基础 section validator 验证更新模板 | **2 sections / 2 subsections VALID** |
| 两份 Skill Creator `quick_validate.py` | **PASS** |
| 安装器 dry-run | **PASS**，两份 Skill＋七份 Agent；未改真实 CODEX_HOME |
| 当前 skill/README/v4.5 Markdown 相对路径与 anchors | **PASS** |
| 长 references 的目录、root <500行 | **PASS**，主 SKILL 177 行 |
| 七份 TOML | **PASS**；name/model/effort/sandbox 不变 |
| 15篇规划资料 | **6 stack/application＋4 concern＋router/universal/boundary/examples/sources** |

原始项目/tool测试输出保存在 appendix。一次把 tools 测试、plan validate 和后续 validator 串在一起的 shell 达到容器超时；tools 15项与plan检查已经完成，后续两份 Skill validator 和 install dry-run 分别单独执行成功。没有把未执行项当作通过。

## 保留检查

- 输入281文件全部仍有对应位置；无删除。
- 265个输入文件逐字保持，16个有本轮明确改动。
- 192份输入历史文件逐字保持（包括 dirty CSV）。
- 九个运行脚本、五份工具测试及安装器不变。
- 配套 `code-review` 全目录不变；委托验收协议不因主项目发布号升级。
- 除plan_reviewer增加知识路由指令外，另六份Agent文件不变；七个角色绑定都不变。
- `RETENTION.json` 与 appendix 输入哈希可用于本轮差异核对；不是运行时审批条件。

## 打包

分发前排除 `.git`、`__pycache__`、`.pyc`、`.DS_Store`、`__MACOSX`；使用项目目录为ZIP根。ZIP做CRC和逐文件内容/Unix mode round-trip核对。不生成`.sha256`侧文件。实际包大小和内容核对回执在发行工作目录保存，最终回复只提供经验证的成品。

## 没有执行

- 没有真实Codex或ZAS子代理调用，没有付费模型比较。
- 没有运行LMDO、Swift/macOS、Python web app、Rust或Java应用的产品测试。
- 12个组合场景只检查预期配置完整性；没有自动判定模型是否真的正确选路由。
- 未测量省token、减少review、降低返工的百分比。

这些离线结果证明文件/配置连线和旧职责保留，不证明模型绝不跳步、扩大scope或选错模块。后续按真实已有工作中的证据评价，不能额外制造审查和测试来填本轮数据。
