更新4.3版本

## subagent
### implementer命名
不要用现在的implementer_1, 2, 等；也不要恢复之前的luna, terra等名字。
改为impl_nano (luna), impl_mini (terra), impl_std (sol), impl_large (astra)
### section implementer选择
PLAN-FULL里必须写每个section/sub-section用的impl agent 级别，不要留在执行时决定。

## zcode
和codex内置reviewer的交替保持和原来一致。
下面是zcode-as-subagent的源代码，目前是完成开发，进入受控真实项目测试阶段，通过真实任务来优化后续开发方向（skill里这部分也不要把它当成绝对可用的mcp，把它当成测试版），请你分析一下：
1. ZAS应该增加哪些日志。
2. 本skill的audit流程要增加什么zcode相关的audit流程用于改进zcode mcp和整体生命周期管理。
3. 有没有MCP/CLI接口的优化建议？有的话另附一个优化方向文档，我去给codex执行，执行完我再在我的其他项目测试ZAS，把sectioned skill按照优化后的写。没有的话根据最新的zcode mcp协议，帮我把流程写入skill。
4. 有人用zcode搭配最新glm模型的时候，遇到glm陷入无限循环的问题。因此我对ZAS有个要求：调用方(如codex里的主agent)是否有接口通过mcp识别出这样的问题。比如读取zcode的公开reasoning delta(重复“我要先做这个，不对，我要先做那个，还是不对，让我再确认一下......”，不能用简单的文字重复相似度计算来做)，tool call内容(true, echo a, echo b)， read(多次重复读取同一个文件同一个片段)等

## advisor
改回3.9的外部advising流程。
