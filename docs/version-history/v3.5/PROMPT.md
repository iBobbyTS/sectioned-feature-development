# you asked

message time: 2026-08-13 14:50:21

这是最新的一些审计数据。
codex-rosetta：增加search失败单一请求循环锁
rosetta-增加url轮换：参考search provider，仅502才轮换，使用相同的锁。
rosetta-key轮换：使用url轮换的机制做key轮换，须确保使用相同的组件，不重复实现。
rosetta-模型的provider配置从标量改为向量，支持后续扩展：本轮只模型组config里数据类型的写入、读取修改，不做切换逻辑，不做多provider支持，不做UI修改。
[保密内容]
[保密内容]
[保密内容]
[保密内容]
cockpit-增加启动时端口切换提示：启动时的功能

1. 分析一下skill是否需要更新。
2. 之后是不是要在skill里直接包含audit部分，默认不审计，用户主动开启审计，读取单独的审计文档，边做边保存记录。
3. audit pack里需要包含启动sectioned-development是用户主动提起skill还是agent自己决定。之后分析的时候判断那些自动决定使用的时候有没有把简单问题复杂化。
4. audit prompt直接放到skill的reference里，不要单独一个markdown了。
