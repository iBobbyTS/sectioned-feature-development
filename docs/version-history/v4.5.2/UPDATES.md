# 4.5.1 → 4.5.2

## 本次修订

| 修改 | 文件 | 目的 |
|---|---|---|
| 将 Audit 放回根执行入口与完成链，列明实际三种交付结果 | `skill/sectioned-feature-development/SKILL.md` | 防止被当作可选附录或在 Next:none 时丢失 |
| Bootstrap、阶段证据、takeover、closure 明确继承 Audit | `references/artifact-lifecycle.md` | 主线程持续负责，同一 feature 不因 session 变化遗忘 |
| 将一行 Audit 概括展开为模式、范围、待办、主包／伴随包和真实障碍 | `assets/FEATURE-STATE.template.md` | 普通文本即可，不引入机器字段验证 |
| 恢复初始化／接管／最终回复规定，并与现有轻量 trace 规则一致 | `references/audit-mode.md` | 原始证据保存一次、单次 artifact correction、失败诚实报告 |
| 4.5.2 版本、README 和 CHANGE_LOG | 项目元数据 | 说明安装与前瞻采用，不重审历史任务 |
| 新增15项说明/连接/保留测试，更新旧版本断言 | `tests/` | 约束文档回归而不添加运行时 gate |
| 修复两项输入已有失败的测试 | `test_project.py`、`test_v441_handoffs.py` | 对齐输入提交753c9ff已做的 poll→wait 与两份文档hash，非产品改动 |

## 明确保留

- 九份运行工具及其五份测试、安装器、七份 Agent TOML、完整配套 code-review 均不改。
- 所有规划 domain/language/adapter/concern 文件与既有 refs/template 的其他职责不改。
- 真实委派、FINAL_ANSWER + completed、原生/ZAS 分离、ONE/TWO、累计repair、subsections、并行、外部人工Advisor均不变。
- 所有旧版本历史与三份 dirty CSV逐字保留。不复制新的 previous-version baseline，只保存输入哈希和修改列表。
- 主包/真实ZAS同名配对、typed身份、原子幂等finalizer、无SHA侧文件、有限纠错保持。
- 本次不生成任何历史 feature 的补救 Audit Pack，不重跑其产品、review 或模型任务。

## 新版最终交付的最小形式

```text
Product/readiness: <真实结论>
Audit: COMPLETE — <实际主ZIP，必要时配对ZIP与已知gap>
```

或者明确 OFF 的用户依据，或 AUDIT_PACK_INCOMPLETE 的真实障碍、实际尝试/无法调用原因与保留目录。状态回复/人工等待/中断只保留PENDING，不每回合打包。

## 安装

从完整项目根目录：

```bash
python3 scripts/install.py
python3 scripts/install.py --apply --replace
```

已安装完整4.5.1时也可备份后用单独Skill ZIP完整替换主Skill目录；现有安装器不提供 `--only sectioned-feature-development` 选项，本版不增加安装器逻辑。不要只替换根SKILL.md而遗漏三个对应文件。安装器尊重CODEX_HOME并备份既有目标，不修改全局AGENTS或产品仓库。

## 验证含义

离线测试检查说明内容、链接、保护范围和已有脚本回归；没有真实Codex/GLM运行。它们不能代替后续任务中对Audit遵从率的观察。
