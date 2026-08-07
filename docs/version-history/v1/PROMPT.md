# you asked

message time: 2026-08-06 22:34:57

我在使用codex开发时遇到了一次更改大量代码后，每次review都能查出新问题，有时候重复十几次都没法收尾。你已经帮我优化过review了，但还是不行。我想到的办法是，大修改必须拆分，逐section implement+review，目前做下来效果还可以。我的 @Codex Custom Instructions.md ，里面的

```
- If it's a non-trivial change and edits may exceed 300 lines or more, must:
  - Use a git branch for it. 
  - Divide them into more reviewable sections. 
  - Write an implementation plan with sections properly divided into `.agent-work/PLAN-FULL.md`. 
  - Do the following to implement the non-trivial code change: {extract the current section from `.agent-work/PLAN-FULL.md`, write into `.agent-work/PLAN.md`; spawn a subagent using the `sol-medium` profile, ask it to implement `.agent-work/PLAN.md`; perform a commit; loop {use a clean `sol_xhigh` subagent to perform $code-review, result must be written to `.agent-work/reviews`; If no issue is found in the current round and the previous round: stop the loop; Use a `sol_high` subagent to fix the issue based on the document; commit the fix}; delete `.agent-work/PLAN.md`}. move `.agent-work/PLAN-FULL.md` to `.agent-work/plans/{YYYYMMDD-HHMM}_FULL.md`. 
```

是我新加的。

目前我的review skill发给你了，请你判断是否需要修改来适应大功能小模块review的需求。

请帮我把这个流程扩充成一个skill，帮我查找：

- 传统软件工程里开发大功能的流程
- AI Agent里开发大功能的流程
  - Agent 厂商发的博客或相关内容
  - 社区用户分享的经验

根据搜索结果和你的思考，查找更多你认为需要的资料。注意不要参考早于1年的ai agent相关资料，因为1年的模型和harness进化基本把早期的问题都解决掉了。

最后输出（都用markdown格式，skill需要符合 @skill-creator.zip规范）：

- skill (含附件)
- skill的研究过程和参考资料
