# Updates

## 本版本如何从证据得到修改

- Section acceptance 恢复连续两次 fresh full clean。
- 删除 soft cap；最多 5 次 full SECTION review。
- 第 5 轮仍不收敛时自动创建 `codex/backup/***` 并调用 sol_max 重拆当前 section。
- 支持层级 section ID，如 `S03.1`。

## Validation 摘要

原归档没有独立 validation 报告；保留实际 Skill 源码作为该版本事实源。

## 未保留的包装文件

- `*.patch`
- package SHA/line-count/index 文件
- 独立 SKILL preview（已保留真实 skill tree）
- nested skill ZIP（已解包）
- raw audit inventory（已综合进分析）
