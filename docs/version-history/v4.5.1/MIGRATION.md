# 4.5 → 4.5.1 规划知识迁移

恢复/迁移的是知识职责，不是要求重做历史 PLAN。已接受工作不重审，不迁移旧 route 标签作为新的执行 gate。

| 原路径 | 新归属 | 保留的实质知识 |
|---|---|---|
| domains/full-stack.md | 保持在 domains | 完整跨层业务路径、同一 request/response 与直接 reader |
| domains/swift-macos.md | languages/swift.md；domains/desktop-apps.md；adapters/frameworks/swiftui-appkit.md；adapters/platforms/macos.md | task/actor/cancellation 与语言；view/model/window 与框架；分发/签名与平台分离，仍禁止默认重构 |
| domains/python.md | languages/python.md；adapters/frameworks/django.md；相关实际 domain | asyncio/资源/打包留语言；atomic/on_commit/历史模型只在 Django；一次脚本不升级成迁移平台 |
| domains/rust.md | languages/rust.md；adapters/runtimes/tokio.md；实际 domain | ownership/Cargo target/features；operation-specific cancellation、child wait/reap/drop 配置和失效轨迹 |
| domains/java.md | languages/java.md；adapters/frameworks/spring.md；full-stack/domain | JDK/API/exception/resource；Spring proxy self-invocation/rollback配置，不把所有 JVM 当 Java/Spring |
| domains/svelte.md | adapters/frameworks/svelte-sveltekit.md | 原详细 action/decoder/server state/navigation/consumer 内容保留，改轴与相对链接 |

通用方法、boundary-handoff 和原四份 concern 逐字保留。`sources.md` 保留原来源记录并追加分类扩展证据。原目录中五个混合文件被迁移，不留下会让 agent继续错误选轴的运行 redirect。

新增 guides 不能作为 automatic framework adoption。例如 FastAPI/Python 与 Django/Python 分开，Rust 同步 library 不需要 Tokio，Swift service 不需要 macOS。初次实施只修改当前命中知识；不回填全部历史档案。
