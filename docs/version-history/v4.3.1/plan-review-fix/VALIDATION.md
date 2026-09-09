# 本轮验证

## 原始输入

- Skill HEAD: `bebb8a09f6a941c79e9be6bbdd9d01baa68193eb`；以实际dirty工作区而非HEAD作为补丁基线。
- v3.9 tag: `e21c9a3e525fa7d3da0fb71fc3eeb12cf25c591c`。
- 原样项目测试：132项，1失败、12错误。错误集中在已升级4.3.1实现与旧4.3测试契约不一致。
- 未将ZIP省略的ZAS/LMDO文件视为真实删除；未修改输入工作区。

## 修订结果

- 项目 unittest：**163/163通过**，包含12项本次新回归。
- 保留的Skill工具 unittest：**15/15通过**。
- 合计：**178项离线 unittest通过**。
- 新回归覆盖：既有exact approval兼容、main拒绝不成立candidate不伪造clean、普通改动保留原reviewed hash与原report、裸APPROVED无法绕过、漏处置candidate阻塞、report/snapshot/后续plan篡改阻塞、模型/owner变更要求独立delta、owner decision不自动闭合、review仍active时不得approve。
- 两份Skill均通过Skill Creator validator。
- 主SKILL.md：483行；active Skill相对链接存在性检查通过。
- 七份Agent TOML解析通过；仅plan_reviewer的developer instruction改变，模型/effort不变。
- 原历史文档全部逐字保留。
- PLAN模板机械校验通过。
- 以实际上传工作区执行 `git apply --check` 通过；未执行apply到原输入。
- ZIP CRC通过；overlay逐文件与修订副本一致，manifest记录before/after SHA；无.sha256侧文件。

## 不应夸大的部分

这些测试使用临时Git仓库和明确标注的合成reviewer回执，不是真实Astra/GLM调用。脚本关联文件、已记录的actor ID和hash，不能鉴别第三方服务实际运行的模型，也不能机械证明所有自然语言计划修改都保持语义边界。

未运行ZAS Cargo/macOS/LaunchAgent/Codex/GLM，也未运行LMDO浏览器。当前项目意见来自源码、Git、计划与报告；不是两个产品实现后的merge认证。

本次没有增加通用新gate系统或自动PLAN审查循环。重复full PLAN review继续受原有有限政策约束；新增parent admission路径修复“普通改动也必须新的reviewer APPROVED”的具体逻辑冲突。实际Agent仍必须遵守派发规程。
