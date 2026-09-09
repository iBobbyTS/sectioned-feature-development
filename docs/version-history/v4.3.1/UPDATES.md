# 4.3 → 4.3.1

| 用户确认 | 本轮实现 | 未改变的内容 |
|---|---|---|
| 公开reasoning默认允许、排除encrypted_content | 精确runtime selector/key核验合同；默认采集；递归排除字段；删除opt-in参数；合成测试不冒充真实键名 | 不解密、不读取其他私有字段，不增加权限框架 |
| observe只在疑似循环调用，3/5/200、无结果 | tools/list完整description；固定小型response schema；caller-side shape validator；五类判断只在描述层 | 无自动detector/cancel、无额外review、poll不变 |
| xxx.zip + xxx-zas.zip，无SHA文件 | typed companion、parent引用、独立JSON manifest、同名幂等重试；旧finalizer追加--zas-pack-dir；移除checksum sidecar | 不增加feature计数；已有内部hash校验和Git/plan身份保留 |
| 先部署ZAS再用Skill | 新contract是安装前提，错误部署显式阻塞 | 真实runtime失败照常处理；不声明任何服务绝对可靠 |

7个agent TOML、实现profile冻结、DAG/subsection/repair预算、feature-wide reviewer alternation、完整执行artifact链、原ADVISOR-REQUEST及外部human advising不变。配套code-review仍使用sfd-delegated-review/4.2；4.3.1只追加调用方observe/配对审计说明，不改其acceptance。

工作流schema与PLAN workflow_revision保持4.3，避免仅patch版本变化导致活动计划hash或验收迁移。文档/包版本为4.3.1。

无新runtime binary或MCP server代码；单独执行包供ZAS仓库Codex实施，再由用户进行真实部署测试。
