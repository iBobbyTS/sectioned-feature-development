# Composable planning router

Read this page and [universal.md](universal.md) once in the existing PLAN-authoring/review phase. Select knowledge for the **changed behavior**, not a fixed project label. Do not preload the library. This is not a new trigger, reviewer, approval or dispatch gate.

## Four independent axes

| Axis | Question | Index / examples | Never infer |
|---|---|---|---|
| **Domain** | What engineering outcome is this change delivering? | [Domain index](domains/INDEX.md): frontend, backend, full-stack, desktop, mobile, CLI, SDK, systems, platform, data, ML, science, embedded, games | A domain does not select a language or framework. These are engineering domains, not invented industry/regulatory requirements. |
| **Language** | Which source/query/script/markup semantics actually change? | [Language index](languages/INDEX.md): JavaScript, TypeScript, Python, Java, C#, C/C++, Go, Rust, Swift, Kotlin, PHP, Ruby, Dart, SQL, shell, PowerShell, R, Lua, HTML/CSS | Language does not imply an app type, framework, OS or runtime. |
| **Adapter** | Which concrete dependency/runtime/platform changes the contract? | [Adapter index](adapters/INDEX.md), separated into **frameworks**, **runtimes**, **platforms** | A platform is not a language; a framework is not a domain. A tool installed on the host is not a dependency of the changed path. |
| **Concern** | Which cross-cutting semantics really change? | [data-evolution](concerns/data-evolution.md), [async-lifecycle](concerns/async-lifecycle.md), [external-integration](concerns/external-integration.md), [performance](concerns/performance.md) | Database reads do not automatically mean migration; an async keyword does not require lifecycle redesign. |

Indexes are lookup aids. Read only the entries needed to locate a guide; do not load every index and all of its linked files. Directly load a known guide when the current path already establishes its applicability.

## Selection and composition

1. Trace requirements → actual entry point → authoritative owner → state/output → direct consumers using repository rules, changed source and relevant manifests. Unrelated dependencies, the host OS and examples in a user message are not matches.
2. Select **all applicable** dimensions independently, then load only the smallest set of guides that answer unresolved planning questions. No requirement to select an entry from every axis. Do not compute a Cartesian product of language/domain combinations.
3. Prefer the domain that captures the whole outcome. Full-stack normally supplies the cross-layer path without automatically loading frontend AND backend; add a specialized domain only for a distinct unresolved boundary. A framework adapter already explains its runtime-specific rule; do not reread language basics or a second adapter merely to fill a category.
4. Add [boundary-handoff](boundary-handoff.md) once when producers/consumers or separate workers share a changed contract. Merge selected questions into **ONE PLAN** and one shared example per real boundary. Do not create one section, reviewer or test suite per guide.
5. Each adopted question needs existing authority, a concrete failure, actual owner/consumer and a falsifiable acceptance criterion. A playbook is **not requirement authority**. Recommendations without that link remain unadopted advice, not blockers.
6. In the existing PLAN, record concise `Planning routes`: `domains`, `languages`, `adapters` (with framework/runtime/platform kind), `concerns`, selected relative paths/reasons and material unknowns. Empty/unknown axes are allowed. No JSON, route validator, hash approval or separate report.
7. Use bundled knowledge by default. Search official source only for a concrete unresolved/version-sensitive seam that matters to the current design. Installed source/configuration wins over rolling documentation defaults. Do not upgrade dependencies, add a framework or modify the installed library just to conform to a playbook.

## Important non-matches

- Svelte and Java compose only when actual Svelte and Java owners participate; the example is not evidence that LMDO uses Java. A SvelteKit TypeScript application can be full-stack without Java, Spring or a separate backend process.
- Swift can implement a server; that does not select macOS or SwiftUI. Editing Python from a Mac does not select desktop-apps or macOS. Kotlin does not prove Android; C# does not prove ASP.NET; Rust does not prove Tokio.
- Python CLI, Python data pipeline and Python web service share a language guide but have different domains. SQL is a query language; the database engine/version is a separate fact. Bash and PowerShell have separate guides.
- Using an AI coding agent does not make the product an AI/ML application. Cloud deployment does not imply Kubernetes. C++ does not by itself select embedded or game development.
- TypeScript does not automatically load JavaScript as an additional checklist: select JavaScript for a runtime-semantic question it actually answers. An untouched framework elsewhere is not a reason to read its adapter.

More routes do not change model tiers, ONE/TWO, repair budgets, section count, dependency edges or parallelism. The knowledge library does not change the Sectioned trigger threshold.

## Unknown or partially matched technology

For any unknown/unlisted language, framework, runtime, platform or domain, use universal for the missing dimension and retain the independently established matches. Missing a playbook is not a blocker. For example, Svelte + an unknown backend still uses full-stack/Svelte and the real boundary contract; do not guess Java/Python to fill the gap.

Inspect the missing seam's source/types/fixtures, then consult the actual version's primary documentation or perform the smallest safe distinguishing probe only when material. Record coverage gaps for maintainers; do not pause product work to author a new guide.

Conflicting advice is resolved by current user authority, repository contracts, actual implementation and installed configuration—not by combining the strictest rule from every guide. Different owners may legitimately have different lifecycles; connect them with the shared contract rather than imposing one global abstraction.

## Review, handoff and re-routing

The existing independent PLAN reviewer reads this router/universal and only relevant selected guides. It independently checks applicability, missing dimensions and cross-boundary omissions in its one authorized pass; it does not start separate reviews for each axis. Give implementers task-relevant excerpts/links and resolved examples, not the whole library, all indexes or research chat.

Re-route only when a material owner/runtime/contract/requirement changes. PLAN_DELTA reloads only affected knowledge. Wording edits, model changes, retries and library reorganization do not reopen accepted work or demand a new approval hash. Audit observes selected/skipped axes and actual missed boundaries in existing artifacts; it does not run a route-completeness gate.

[Worked combinations](examples.md) and [sources/freshness](sources.md) are optional reference material.
