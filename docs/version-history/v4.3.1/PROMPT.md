annotation 1:
```
不提取隐藏推理。 公开 reasoning 需要确认 runtime 来源，并由调用方明确授权收集；private、opaque 或来源不明的内容保持不可用。
```
user:
主动排除encrypted_content，通过本机zcode runtime确认reasoning delta的准确键名，只允许提取这个。observe默认允许提取，zcode里运行的glm本身是开放权重模型，推理过程也不是隐藏的，在GUI里都能看到，所以不存在泄密。

annotation 2:
```
zcode_subagent_observe
```
user:
确认增加这个工具，描述为“仅在怀疑zcode subagent陷入无意义循环时才调用检查最近推理和工具调用过程”。你说的5种判断放在mcp描述层，让模型根据推理和工具判断，不要进入zas自动判断。
默认提供调用最多的3个工具各最近的最多5次的工具调用（不包含结果）+最新200char的reasoning delta(一个delta可能包含多个char)。

annotation 3:
```
新增 ZAS-AUDIT.md、每个物理 attempt 的记录模板，以及 zas trace family。
```
user:
改为：假设某个功能的audit pack在~/Desktop/audit-pack/xxx.zip，zcode的audit pack放到~/Desktop/audit-pack/xxx-zas.zip
另外，不需要创建sha256文件了。

comment 4:
不要在skill里做zas未更新的假设，我确认我会先完成zcode的开发再正式使用这个skill。

帮我根据这4个先完成4.3.1版本skill和更新后的zas改进执行包。
