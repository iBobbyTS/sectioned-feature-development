# Planning library source catalog

## Contents

- [Use and evidence levels](#use-and-evidence-levels)
- [Local requested basis](#local-requested-basis)
- [Traditional engineering](#traditional-engineering)
- [Agentic planning and skill design](#agentic-planning-and-skill-design)
- [Stack and runtime sources](#stack-and-runtime-sources)
- [Freshness and non-adoption rules](#freshness-and-non-adoption-rules)

## Use and evidence levels

Researched 2026-09-09 (America/Edmonton). This is a maintainers' catalog, not mandatory context for each worker. Sources inform bounded questions; none grants authority to enlarge a feature.

- **Primary documentation**: strong evidence for a documented API/default in that version, not proof that the current repository uses it.
- **Vendor engineering report/cookbook**: primary account of a workflow, not a controlled measurement of this Skill or a universal mandate.
- **Local audit/source**: evidence for the attached run or file only; absence of source is not a product defect.
- **Our synthesis**: route composition, short handoff examples and applicability exclusions. These are proposed improvements awaiting real-project evaluation.

## Local requested basis

| ID | Requested source | Extracted contribution / boundary |
|---|---|---|
| L01 | Attached `adaptive-debugging.zip`, `SKILL.md`, `references/core/routing-and-complexity.md`, related domain playbooks | Core evidence method plus all causal-domain matches; progressive loading and negative examples. Reuse the architecture, not its debugging trigger, attempt cap, diagnostic session script or every domain. |
| L02 | Attached/current LMDO two-task audit, original rollout, and `ANALYSIS.md` / `EVIDENCE.md` | Actual contract/consumer mismatches motivate shared producer/consumer examples and owner classification. Not a new product requirement or backend-language claim. |
| L03 | Supplied ZAS public-contract-slim audit; two-task analysis | Sparse summary lacks source/plan/test detail; no inference of mergeability, runtime behavior or cost. Supports honest unknown/provenance handling only. |
| L04 | Actual uploaded `sectioned-feature-development(6).zip`, v4.4.1 working tree | Preserve current workflow, local completed + FINAL_ANSWER rule, lightweight validator, task/model/parallel/review/Advisor policies and historical files. |

## Traditional engineering

| ID | Primary source | Narrow fact / adopted principle | Not adopted |
|---|---|---|---|
| G01 | [Google: Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) | Prefer self-contained behavior and relevant tests; include real usage when needed to establish a new API. | No arbitrary new line-count gate or weakening of parent acceptance. |
| G02 | [Google: CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html) | Preserve what/why and relevant context for later readers. | Not a second requirements database. |
| G03 | [Fowler: Preparatory refactoring](https://martinfowler.com/articles/preparatory-refactoring-example.html), 2015-01-05 | A bounded enabling refactor can make the requested change simpler. | Not a general infrastructure rewrite mandate. |
| G04 | [Pact: Writing consumer tests](https://docs.pact.io/consumer) | Exercise the application's actual API client, not only a test's handcrafted generic HTTP call. | No requirement to install Pact, a broker or a new testing framework. |
| G05 | [OpenAPI 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) | Request/response/media-type/schema/examples can describe a wire contract. | No automatic OpenAPI/codegen/schema migration. |
| G06 | [Google: What to look for in review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | Design, functionality and tests matter; known unfinished behavior is not delegated to reviewers to implement. | Not open-ended whole-repo discovery. |

Traditional sources are not subject to the one-year agent-material cutoff.

## Agentic planning and skill design

Only recent dated reports or currently served first-party documentation were used. Rolling docs have no invented publication date.

| ID | Primary source / date | Adopted fact or practice | Transfer limit |
|---|---|---|---|
| A01 | [OpenAI: Build skills](https://developers.openai.com/codex/skills/), current docs; redirects to ChatGPT Learn | Skills package instructions and selectively loaded references; scripts are optional. | No new runtime route/approval validator. |
| A02 | [OpenAI: Execution plans](https://developers.openai.com/cookbook/articles/codex_exec_plans), current cookbook | Durable self-contained plans describe observable outcomes, context and validation. | Do not copy exhaustive novice instructions/pseudocode or add mandatory receipt state. |
| A03 | [OpenAI: Codex best practices](https://developers.openai.com/codex/learn/best-practices), current docs | Ground complex work in repository context and inspectable plans. | No claimed speedup or mandatory preplanning for trivial changes. |
| A04 | [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), 2025-11-26 | Incremental feature progress and realistic verification help avoid premature completion. | Do not expand one request into a large feature list or require new live environments. |
| A05 | [Anthropic: Skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), current docs | Progressive disclosure and freedom matched to task fragility. | This library supplies judgment aids, not a second rigid workflow. |
| A06 | [Anthropic: Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps), 2026-03-24 | Explicit planning/implementation/evaluation responsibilities can expose distinct failure modes. | Do not add an evaluator stage or new review budget here. |
| A07 | [Anthropic: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents), 2026-01-09 | Real task evaluation matters for the model+harness combination. | Offline file/contract tests cannot prove lower review cost or fewer escapes. |

## Stack and runtime sources

All are first-party docs/source, read or queried at research time. Use the repository's actual version/configuration before applying a default. Planning questions in domain files are our synthesis around these mechanics.

| ID | Source | Documented mechanic relevant to planning |
|---|---|---|
| N01 | [Apple: Model data](https://developer.apple.com/documentation/swiftui/model-data) | Data ownership and view dependency/state representation. |
| N02 | [Apple: Managing model data](https://developer.apple.com/documentation/SwiftUI/Managing-model-data-in-your-app) | Observation support is deployment/API dependent; existing models need not be migrated. |
| N03 | [Swift book: Concurrency, official source](https://raw.githubusercontent.com/swiftlang/swift-book/main/TSPL.docc/LanguageGuide/Concurrency.md) | Actor isolation, task relationships and cooperative cancellation. |
| N04 | [Apple: Developer ID](https://developer.apple.com/developer-id/) | Signing/notarization and distribution are distinct delivery checks when that path changes. |
| P01 | [Python: asyncio tasks](https://docs.python.org/3/library/asyncio-task.html) | Structured task cancellation and why swallowing cancellation can break task-group semantics. |
| P02 | [Django 5.2: Transactions](https://docs.djangoproject.com/en/5.2/topics/db/transactions/) | Atomic blocks, on-commit effects and in-memory state versus database rollback. |
| P03 | [Django 5.2: Migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/) | Historical models and database-specific migration behavior. |
| P04 | [PyPA: pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) | Project/build/entry-point metadata determines actual installation behavior. |
| R01 | [Tokio: select!](https://docs.rs/tokio/latest/tokio/macro.select.html) | Losing branches are cancelled; operation cancellation safety matters. |
| R02 | [Tokio: process Command](https://docs.rs/tokio/latest/tokio/process/struct.Command.html) | Dropping a child handle does not kill it by default; explicit lifecycle responsibility matters. |
| R03 | [Cargo: features](https://doc.rust-lang.org/cargo/reference/features.html) | Feature resolution/additivity can change build behavior across consumers. |
| S01 | [SvelteKit: Form actions](https://svelte.dev/docs/kit/form-actions) | ActionResult/custom enhancement decoding differs from ordinary endpoint JSON. |
| S02 | [SvelteKit: State management](https://svelte.dev/docs/kit/state-management) | Shared server state and reused components create request/navigation lifetime concerns. |
| S03 | [SvelteKit: Loading data](https://svelte.dev/docs/kit/load) | Load data dependencies, invalidation and serialization constrain consumer refresh. |
| J01 | [Spring: Transactional annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html) | Default proxy interception does not apply to self-invocation. |
| J02 | [Spring: Rollback rules](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html) | Exception rollback defaults may be changed by explicit configuration. |
| D01 | [PostgreSQL: Transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | Per-statement snapshots at Read Committed differ from a globally frozen read view. |

## Freshness and non-adoption rules

Some Apple/Swift pages render JavaScript-only bodies in the research reader. The Swift concurrency claims were checked against the official book repository source; Apple model-state pages were available through official documentation search excerpts. Do not present unavailable page bodies as fully read.

`latest`, `current`, Python, SvelteKit and Spring documentation can evolve. The bundle is a planning knowledge snapshot, not a version compatibility guarantee. A pinned repository source/default wins over these examples. Look up only the unresolved material seam, using primary versioned sources; do not re-browse the whole catalog at every PLAN.

No community anecdote or aggregate benchmark is used to change model tiers, review assurance, phase count, hard caps, provider alternation or budgets. The proposed route combinations need forward evaluation on real tasks; no performance improvement is claimed as measured.

## 4.5.1 independent taxonomy and broader coverage

Researched 2026-09-09. Coverage is a curated starter set, not a world ranking or complete encyclopedia. Domain means an engineering/product task category, not a language, vendor framework, OS or commercial industry. Survey popularity is only a breadth signal; task suitability is not inferred from it. Rolling sources have no invented publication date. The source-version examples do not upgrade a repository. New guides are planning synthesis; no model-routing or defect-reduction experiment was run.

| ID | Primary source | Evidence and limits |
|---|---|---|
| survey-tech | [Stack Overflow 2025 technology survey](https://survey.stackoverflow.co/2025/technology) | Primary survey; broad coverage signal, not an unbiased census or a route oracle. |
| survey-roles | [Stack Overflow 2025 developer roles](https://survey.stackoverflow.co/2025/developers) | Primary survey; role categories inform domain coverage; no market-share claim. |
| octoverse | [GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) | Primary repository-activity report; contributor activity is not job/task frequency. |
| small-cl | [Google small changes](https://google.github.io/eng-practices/review/developer/small-cls.html) | Traditional engineering guidance, not a quantitative rule for section size. |
| pact | [Pact consumer guidance](https://docs.pact.io/consumer) | Actual consumer code versus a test-only client; no mandatory Pact adoption. |
| semver | [Semantic Versioning 2.0.0](https://semver.org/) | Applies if the project adopts this versioning contract; not authority to add compatibility. |
| js | [MDN promises](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises) | Language/host asynchronous composition and cancellation distinction. |
| ts | [TypeScript narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html) | Static refinement; inspect runtime validation separately. |
| python | [Python asyncio tasks](https://docs.python.org/3/library/asyncio-task.html) | Current standard-library snapshot; actual interpreter version governs. |
| pyproject | [Python packaging pyproject](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) | Metadata and installed entry-point planning. |
| java | [Dev.java exceptions](https://dev.java/learn/exceptions/) | Language exception/resource handling; not a Spring contract. |
| csharp | [C# asynchronous programming](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/) | Task composition and observation; actual target framework governs. |
| c | [Clang UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) | Examples of runtime UB detection; not complete proof or a required new sanitizer gate. |
| cpp | [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) | Ownership/RAII/interface guidance, not mandatory repository modernization. |
| go | [Go context](https://go.dev/blog/context) | Go cancellation/deadline propagation; does not prescribe a server architecture. |
| rust | [Rust ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html) | Language resource ownership; no inference about Tokio. |
| cargo | [Cargo features](https://doc.rust-lang.org/cargo/reference/features.html) | Supported build configurations, not a Cartesian test mandate. |
| swift | [Swift book concurrency source](https://raw.githubusercontent.com/swiftlang/swift-book/main/TSPL.docc/LanguageGuide/Concurrency.md) | Official source used because rendered docs are a JavaScript shell. |
| kotlin | [Kotlin coroutines basics](https://kotlinlang.org/docs/coroutines-basics.html) | Coroutine structure; actual kotlinx.coroutines dependency/configuration governs. |
| php | [PHP type juggling](https://www.php.net/manual/en/language.types.type-juggling.php) | Conversion contexts and version sensitivity. |
| ruby | [Ruby IO](https://ruby-doc.org/3.4.1/IO.html) | Reference API; deployed Ruby version governs. |
| dart | [Dart concurrency](https://dart.dev/language/concurrency) | Event loop/isolate distinction; not a Flutter requirement. |
| sql | [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) | One database example only; never generalize its defaults to all SQL engines. |
| shell | [GNU Bash manual](https://www.gnu.org/software/bash/manual/html_node/Shell-Syntax.html) | Official indexed manual text; direct page fetch timed out. POSIX versus Bash is explicitly distinguished. |
| pwsh | [PowerShell pipelines](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines) | Object pipelines and native-command boundaries; host/version matter. |
| r | [R language definition](https://cran.r-project.org/doc/manuals/r-release/R-lang.html) | Vector, missing-value and evaluation semantics. |
| lua | [Lua 5.4 manual](https://www.lua.org/manual/5.4/manual.html) | Specific reference; LuaJIT/Luau/host variants must be separately confirmed. |
| html | [HTML forms specification](https://html.spec.whatwg.org/multipage/forms.html) | Browser form semantics; CSS/layout checks remain concrete browser evidence. |
| svelte | [SvelteKit form actions](https://svelte.dev/docs/kit/form-actions) | Form/action result encoding, not interchangeable with arbitrary JSON. |
| svelte-state | [SvelteKit state](https://svelte.dev/docs/kit/state-management) | Request and navigation state boundaries. |
| react | [React effects](https://react.dev/learn/you-might-not-need-an-effect) | Derived state and avoiding redundant effects. |
| next | [Next.js server/client components](https://nextjs.org/docs/app/getting-started/server-and-client-components) | Router/version-specific server/client boundary. |
| vue | [Vue SSR](https://vuejs.org/guide/scaling-up/ssr.html) | Request isolation and hydration; Nuxt-specific APIs require installed-version evidence. |
| angular | [Angular lifecycle](https://angular.dev/guide/components/lifecycle) | Component initialization/update/destruction; not a change-detection migration mandate. |
| django | [Django 5.2 transactions](https://docs.djangoproject.com/en/5.2/topics/db/transactions/) | Atomic/on_commit and in-memory state distinction. |
| django-migration | [Django 5.2 migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/) | Historical model state; inherited verified v4.5 source. |
| fastapi | [FastAPI async](https://fastapi.tiangolo.com/async/) | Sync/async framework boundary; inspect actual dependency and client behavior. |
| spring | [Spring declarative transactions](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html) | Proxy interception/self-invocation; configured rollback rules still need inspection. |
| spring-rollback | [Spring rollback rules](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/rolling-back.html) | Inherited v4.5 source; configuration/version qualify defaults. |
| aspnet | [ASP.NET Core DI](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/dependency-injection) | Actual service lifetime and scope boundary. |
| rails | [Rails callbacks](https://guides.rubyonrails.org/active_record_callbacks.html) | Callback/transaction placement; not proof of external-effect atomicity. |
| laravel | [Laravel 12 queues](https://laravel.com/framework/docs/12.x/queues) | Job execution/retry/commit ordering in a versioned framework. |
| flutter | [Flutter architecture guide](https://docs.flutter.dev/app-architecture/guide) | State/data responsibilities; recommendations are not obligatory migrations. |
| swiftui | [Apple SwiftUI model data](https://developer.apple.com/documentation/SwiftUI/Model-data) | Official indexed text supports source-of-truth/state/binding claims; dynamic page fetch was limited. |
| apple-distribution | [Apple Developer ID distribution](https://developer.apple.com/developer-id/) | Inherited v4.5 source; packaging/entitlements only when changed. |
| apple-scenes | [Apple UIKit scenes](https://developer.apple.com/documentation/uikit/scenes) | Official indexed text describes UI instances/lifecycle; no beta API adoption. |
| android | [Android app architecture](https://developer.android.com/topic/architecture) | Process/component lifecycle and state ownership; no mandatory app rewrite. |
| node | [Node streams](https://nodejs.org/api/stream.html) | Completion/backpressure/resource ownership; not a language definition. |
| tokio | [Tokio select](https://docs.rs/tokio/latest/tokio/macro.select.html) | Operation-specific cancellation safety. |
| tokio-process | [Tokio process Command](https://docs.rs/tokio/latest/tokio/process/struct.Command.html) | kill_on_drop is configurable; child lifecycle not proved by handle drop. |
| kubernetes | [Kubernetes pod lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/) | Deployment lifecycle example only; Kubernetes is not assumed. |
| airflow | [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html) | Partitioned/retriable tasks as one implementation example. |
| ml | [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) | Pipeline/metric and training-serving concerns; not a requirement for a new ML platform. |
| pytorch | [PyTorch reproducibility source](https://raw.githubusercontent.com/pytorch/pytorch/main/docs/source/notes/randomness.md) | Official source fallback for redirected HTML; toolchain/device limits apply. |
| zephyr | [Zephyr interrupts](https://docs.zephyrproject.org/latest/kernel/services/interrupts.html) | ISR context restrictions as one RTOS example, not all devices. |
| godot | [Godot idle/physics processing](https://docs.godotengine.org/en/stable/tutorials/scripting/idle_and_physics_processing.html) | Different update clocks as one engine example. |
| openai-skills | [OpenAI build skills](https://developers.openai.com/codex/skills/) | Current official progressive-disclosure guidance; not evidence of this Skill performance. |
| claude-skills | [Anthropic skill authoring](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | Current official variation/reference guidance; not a new workflow requirement. |

### Fetch limitations

Rendered Apple/Swift pages were partly JavaScript shells; use official indexed text and the Swift-book source for the limited claims stated. Bash direct HTML fetch timed out; only the official indexed manual text was available. PyTorch HTML redirected; the official repository randomness.md source was read instead. A C committee PDF was discovered but not used in the final guides; Clang documentation supports only diagnostic examples, not all language-lawyer claims. Domain checklists and route expected outputs are our engineering design, not empirical performance results.
