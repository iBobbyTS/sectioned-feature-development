# 4.3.1 完整合并包

## 来源与优先级

1. 基线：`sectioned-feature-development(5).zip` 中的实际工作区，不是其Git HEAD。
2. 定点修订：`sfd-4.3.1-plan-review-fix-files.zip` 的全部19个 `project-overlay/` 文件。合入前后逐一验证其CHANGED-FILES.json中的SHA-256。
3. 文档补齐：此前正式 `sectioned-feature-development-v4.3.1-project.zip` 的README、CHANGE_LOG和ZAS_OPTIMIZATION_DIRECTIONS；不以旧发布包覆盖修订后的运行文件。
4. `docs/contracts/zas-observation-v1.schema.json` 已被1.1合同取代，原字节保存在本目录 `superseded/`，当前合同目录仅使用正式1.1。
5. 本目录保存定点修订分析、原验证记录及本次重新验证记录；已有版本历史不修改。

## 包含

两份完整Skill、七份原生Agent、安装器、所有执行／审计脚本及模板、项目与工具测试、现有版本历史。默认安装命令仍是 `python3 scripts/install.py --apply --replace`，使用已有备份机制。

## 不包含

本包为可安装项目分发，不是完整Git仓库备份。不包含`.git`、`.agent-work`、其他项目源码、macOS资源叉、Python缓存或临时构建文件；没有创建`.sha256`侧文件。输入ZIP与用户原有工作区未被修改。

## 范围

本次没有再次修改PLAN/review逻辑。模型分级、section/subsection、ONE/TWO、repair预算、并行、ZAS观察协议及外部Advisor沿用已经批准的4.3.1与定点修订。
