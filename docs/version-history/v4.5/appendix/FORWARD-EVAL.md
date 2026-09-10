# v4.5 后续真实任务评估（不在开发流程新增 gate）

`tests/fixtures/planning-routing-v45.json` 的 12 个组合是人工预期场景，不是模型实测。

下一次原本就要开发的项目中，保存已经发生的 PLAN/TASK/HANDOFF/review 证据即可：

1. 命中是否由实际源码支持，有没有因装有某依赖而多读无关领域；未匹配框架是否正常使用 universal。
2. 一份真实跨层样例是否实际到达 consumer；是否调用真实 decoder/客户端逻辑，而非两个不同 mock。
3. 明确要求的 reader 是否在 PLAN 就被分配；未改的 reader 是否有真实 unchanged 依据。
4. 新 finding 是路由遗漏、规划遗漏、已有计划未实现、一般实现错误，还是无法验证。
5. 额外资料读取/定向查证，与 late PLAN_DELTA、repair、漏检和重复验证同时看。不能只看路由命中率或初始规划时间。

仅在对比任务/修改范围、模型/provider、环境及验证条件足够接近时比较成本。缺少部分 usage 不记成零；不能把等待用户的空档算成规划耗时。没有对照时只能报告个案，不声称百分比提升。

禁止为填评估表新增 reviewer、重新打开 closed PLAN、再跑一次实现/测试、恢复脚本门禁或导出无关/隐藏内容。已有 audit 开关和 main/ZAS 配对政策保持。
