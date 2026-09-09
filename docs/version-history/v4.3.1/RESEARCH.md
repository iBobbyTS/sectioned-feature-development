# 4.3.1 依据与未知项

这是用户明确确认后的契约补丁，不是新一轮外部研究。没有用网页、旧模型材料或旧功能说明替换附件源码/4.3项目的协议。

## 已确认事实

- 当前输入4.3项目能完整读取；已完成ZIP CRC与文件枚举。
- 4.3包含metadata/public_content授权分支、cursor分页观察、主包内ZAS证据及checksum输出代码，本轮逐项修改。
- 用户确认公开GLM reasoning在GUI可见，要求默认读取；用户明确要求排除encrypted_content、仅一个实测字段。
- 用户确认先完成ZAS更新，再使用新Skill，因此取消旧服务fallback。

## 不可在本环境确认

用户本机macOS的官方ZCode runtime不可从此容器执行。因此准确event discriminator和text delta pointer没有被推断或编造。交接包要求在用户机器进行短真实任务核验，保存最小脱敏fixture与来源清单。reference/tests只用带明确标签的合成事件。

## 设计选择（不是外部实测结论）

- 工具次数按当前agent任务生命周期唯一调用ID累计，非整个daemon；并列按最近调用再按名称确定，保证结果稳定。
- 200char按Unicode code point计数，先按顺序拼接delta再截尾。
- observe仅传agent_id，避免把确定的3/5/200需求扩成可调观测框架。
- companion绑定确切parent ZIP hash，main只引用filename/feature/run，避免循环digest。
- 每个ZIP单独原子替换；两文件不伪装为一个原子事务。PAIR_INCOMPLETE允许复用已完成主包。
- 五类判词只在MCP description；验证器只检查数据，不判断语义。

以上选择全部通过本地合同/文件/Git回归验证，不证明模型循环判断能力、真实ZAS implementation或runtime权限可靠性。
