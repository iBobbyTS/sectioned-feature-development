帮我从3.9版skill开始，只有audit记录证明必须改的才简化，未证明问题的不得简化。
这两点是我人工确认需要改的：
1. >1 section必须使用EXECUTE_WITH_COMMITS和单独分支。
2. 完成后如果用户有提出修改，不得重新打开之前的PLAN-FULL补section，除非用户明确要求，否则直接重新评估是否需要开新的sectioned-development还是可以直接修的小改动。

3. 按照4.1的修改使用sub-section的概念。

有部分干扰pack可能要过滤掉，本次更新完的skill也要明确，使用这个skill时，只有本skill要求的audit方法才放入这个文件夹，其他目的的audit的不要进入。
分析本轮audit pack里每阶段的review结果，有没有可以在section划分或plan review部分提前避免的。
当时分析出来的astra/sol/terra/luna任务分级保留（section按照业务分，subsection按照2点分：1. 应该在section内细分的模块, 2. 模型能力）；
使用plan\_writer, plan\_reviewer, implementer\_1 (astra medium), implementer\_2 (sol medium), implementer\_3 (terra high), implementer\_4 (luna xhigh), code\_reviewer, code\_explorer 来给subagent命名；不要用之前的luna\_xhigh, astra\_high等。subagent仍使用现在的表示方式比如 [@astra_high](subagent://astra_high) ，不要用`astra_high`. subagent的audit保留。
advisor架构继续使用4.0的；
并行开发也继承4.0的（如果当时skill不完整，可以用当时的调查和分析来补充新版skill）
