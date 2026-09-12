# Language planning index

Inspect this catalog once, alongside the other three catalogs, in each fresh PLAN-authoring/review context. Select all applicable **changed** paths and read their relevant guides, not every installed technology or linked file. This index is not a product checklist or requirement source.

| Route | Select from evidence | Guide |
|---|---|---|
| Bash / POSIX shell | Changed shell scripts or shell command composition. | [bash-posix-shell.md](bash-posix-shell.md) |
| C | Changed C translation units, headers or a C ABI boundary. | [c.md](c.md) |
| C++ | Changed C++ objects/templates, ownership, concurrency or binary interface. | [cpp.md](cpp.md) |
| C# | Changed C# logic or .NET-facing public types. | [csharp.md](csharp.md) |
| Dart | Changed Dart library, async stream/future or isolate boundary. | [dart.md](dart.md) |
| Go | Changed Go package, executable or concurrency contract. | [go.md](go.md) |
| HTML / CSS (markup and style languages) | Changed HTML semantics, form controls, styles or layout selectors. | [html-css.md](html-css.md) |
| Java | Actual Java source, class/module API or Java runtime behavior is changed. | [java.md](java.md) |
| JavaScript | Changed JavaScript logic, Promise/callback composition or module boundary. | [javascript.md](javascript.md) |
| Kotlin | Changed Kotlin source, coroutine/Flow contract or Java interop. | [kotlin.md](kotlin.md) |
| Lua | Changed Lua code or a Lua embedding boundary. | [lua.md](lua.md) |
| PHP | Changed PHP request, command, package or long-lived worker source. | [php.md](php.md) |
| PowerShell | Changed .ps1/.psm1 or PowerShell command/parameter logic. | [powershell.md](powershell.md) |
| Python | Changed Python application, library, CLI or job source. | [python.md](python.md) |
| R | Changed R analysis/package/statistical transformation. | [r.md](r.md) |
| Ruby | Changed Ruby method/module, IO, extension boundary or package. | [ruby.md](ruby.md) |
| Rust | Changed Rust crate, binary, trait/serde contract or FFI owner. | [rust.md](rust.md) |
| SQL | SQL queries, schema/constraint expressions or database-visible semantics are changed. | [sql.md](sql.md) |
| Swift | Changed Swift source, actor/task, value/reference or public module boundary. | [swift.md](swift.md) |
| TypeScript | Changed .ts/.tsx source or a public declaration/generic contract. | [typescript.md](typescript.md) |

After inspecting all four catalogs and reading actual matches, use [universal](../universal.md) only for a named uncovered part. Retain independent matches; a non-applicable dimension does not need fallback. A guide selects questions, not architecture, model tier, section count or extra tests.
