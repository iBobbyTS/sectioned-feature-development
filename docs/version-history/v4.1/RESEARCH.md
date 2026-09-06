# 4.1 研究与设计依据

查阅日期：2026-09-05。本轮是基于上传project/source的增量工作，不重新改变4.0的模型菜单、effort或当前ZCode接口。不采用旧模型结果代替新模型性能，没有新增模型性能承诺。

## 1. 传统小变更与接受单位

Google Engineering Practices — Small CLs（第一方工程规范）
https://google.github.io/eng-practices/review/developer/small-cls.html

文档把小变更定义为概念上自洽、包含相关测试、reviewer能够理解且提交后系统仍可工作，而不是一个强制行数。它建议提前规划分割，承认依赖栈与水平/垂直拆分，但提醒过小到看不见实际用途也会妨碍审查。

应用：保留section为共同业务接受单位，subsection可作为有具体消费者的内部增量；不按650行触发丢弃/压缩。本文并不照搬“review尚未结束就开始依赖实现”，因为本项目此前有审查快照被修改的实际问题。

## 2. Preparatory refactoring

Martin Fowler — An example of preparatory refactoring（作者原文，2015）
https://martinfowler.com/articles/preparatory-refactoring-example.html

文中区分改变结构和增加行为，以持续可验证的行为保持步骤逐渐形成最终变更。它是传统软件工程资料，不是早期Agent能力的依据。

应用：允许在parent未完成期间先交付真实内部primitive/domain并测试；不能把只有类型或虚假API成功的占位当成独立验收成果。真正必须同事务的副作用仍在一个整体内实现。

## 3. Stacked diffs

Graphite — Stacked diffs（工具作者第一方文档）
https://graphite.com/guides/stacked-diffs

借鉴的是“依赖增量可以分别阅读/验证而不要求把功能当成互不相关的PR”，不是引入Graphite工具、外部PR或发布依赖。4.1无需安装新服务。

## 4. 本项目证据比类比更强

S04 status/body交叉条件、S04.1 domain与HTTP、C01读接口的真实loader副作用、C07 publication与outbox，来源见同目录AUDIT_PACK_ANALYSIS和PPPMS提案。编号深度不证明边界好；相反同一规则被两套实现消费才是必须一起审的事实。

## 5. 设计选择与可否证性

- 只允许section→subsection一层，避免递归门禁。
- 有children父节仍使用原ONE/TWO；checkpoint是主review的逐段coverage，不是每次独立final。
- 完成时必须parent reconciliation和jointoracle；fresh final维持完整parentdiff视角。
- 不提升子节外部依赖权限。要提前被另一个parent消费，应明确提升为独立section并获得相应接受证据。
- 五波修复按original lineage共享，不按ID/reset/reviewer/session变化分配新预算。
- 子节串行同branch，不增加共享工作区并发。独立父节点按既有DAG隔离并行。

这些是针对本项目的设计判断，不是已发表benchmark结论。风险是增加checkpoint切换和局部review调用；收益假设是更早发现问题、较少昂贵的整节返工。后续按parent accepted outcome总成本、未发现缺陷、交互bug、真fresh final质量比较，而不是用逻辑full-pass数作为成本代理。
