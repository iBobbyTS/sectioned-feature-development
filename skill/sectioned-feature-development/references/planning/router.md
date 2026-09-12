# Composable planning router

Use this router in the existing PLAN-authoring/review phase. **Read all four short indexes first; read matching specialized guides next; use [universal.md](universal.md) only for an identified uncovered part.** Do not preload the library. This is a reference-selection instruction, not a new trigger, reviewer, approval or dispatch gate.

## Four independent axes — inspect the catalogs first

Before drafting PLAN-FULL, read these four catalog files once in the current planning context, even if a familiar guide is already known:

| Axis | Question | Required catalog | Never infer |
|---|---|---|---|
| **Domain** | What engineering outcome is this change delivering? | [domains/INDEX.md](domains/INDEX.md) | These are engineering domains, not invented industry/regulatory requirements. Domain does not select language/framework. |
| **Language** | Which source/query/script/markup semantics actually change? | [languages/INDEX.md](languages/INDEX.md) | Language does not imply domain, framework, OS or runtime. |
| **Adapter** | Which actual framework/runtime/platform changes the contract? | [adapters/INDEX.md](adapters/INDEX.md) | Host-installed tools are not automatically dependencies of the changed path. |
| **Concern** | Which cross-cutting semantics actually change? | [concerns/INDEX.md](concerns/INDEX.md) | Database reads do not automatically mean migration; an async keyword does not require lifecycle redesign. |

**Catalog inspection is mandatory; loading every linked guide is not.** Inspect every listed entry in the four bounded catalogs, then select from actual requirements, source and dependency evidence. Reading only this router, relying on remembered filenames, or opening universal without checking the catalogs does not satisfy reference selection. If an index is missing or stale, inspect that dimension's directory once and record the coverage gap; do not silently classify the whole task as universal-only.

## Selection and composition

1. Trace requirements → actual entry point → authoritative owner → state/output → direct consumers. Assess the four catalogs against this changed path, not the entire repository inventory or a stack guessed from the user's examples.
2. Select **all applicable** dimensions independently. Read the matched specialized guides before writing their corresponding plan decisions; do not skip an applicable guide because the task seems familiar or universal is shorter. Use the **smallest set of guides** that covers the actual planning questions. No requirement to select an entry from every axis. Do not compute a Cartesian product of language/domain combinations.
3. Keep the distinction between a gap and a non-match: `NOT_APPLICABLE` means the changed path has no such boundary; it does not require universal. `COVERED_BY <guide>` means an already-read specialized guide covers the same question; do not duplicate a checklist. `UNMATCHED <specific boundary>` is a fallback candidate, not a reason to discard other matches.
4. Prefer a domain that covers the whole outcome. Full-stack does not automatically load frontend AND backend. TypeScript does not automatically add JavaScript; a relevant framework guide can cover its overlapping runtime question. Do not omit an independently relevant language, platform or concern that supplies a different rule.
5. After reading the matched guides, use **universal only for the uncovered part**: name the missing domain/language/adapter/concern or the concrete question the existing guides do not cover. Retain every independent match. Universal is not an unconditional first read, substitute for specialized guidance, or permission to invent a stack. If no specialized guide applies after catalog inspection, universal may supply the whole plan.
6. Add [boundary-handoff](boundary-handoff.md) once when producers/consumers or separate workers share a changed contract. Merge selected questions into **ONE PLAN** and one shared example per real boundary; no section, reviewer or test suite per guide. Existing section-planning and scope-control rules remain the common authority, even when universal is not needed.
7. In the existing PLAN `Planning routes` paragraph record the four-axis assessment, paths actually read, source-based selection reasons, material non-matches/overlap, and `Universal fallback: not needed` or the exact uncovered part. A compact table/bullet group is enough. Do not copy the catalogs, count library files per task, or create another report. No JSON, route validator, hash approval or separate report.
8. Use bundled knowledge by default. Consult primary documentation or a safe probe only for a concrete unresolved/version-sensitive seam that affects the current design. Installed source/configuration wins over rolling documentation defaults. Do not upgrade dependencies, add a framework or modify the library just to conform to a playbook.

Each adopted question still needs existing authority, a concrete failure, an actual owner/consumer and a falsifiable acceptance criterion. A playbook is **not requirement authority**. Unanchored advice remains unadopted advice, not a blocker.

## Important non-matches

- Svelte and Java compose only when actual Svelte and Java owners participate; the example is not evidence that LMDO uses Java. A SvelteKit TypeScript application can be full-stack without Java, Spring or a separate backend process.
- Swift can implement a server; that does not select macOS or SwiftUI. Editing Python from a Mac does not select desktop-apps or macOS. Kotlin does not prove Android; C# does not prove ASP.NET; Rust does not prove Tokio.
- Python CLI, Python data pipeline and Python web service share a language guide but have different domains. SQL is a query language; the database engine/version is a separate fact. Bash and PowerShell have separate guides.
- Using an AI coding agent does not make the product an AI/ML application. Cloud deployment does not imply Kubernetes. C++ does not select embedded or games by itself. An untouched framework elsewhere is not a match.

More routes do not change model tiers, ONE/TWO, repair budgets, section count, dependency edges or parallelism. The library does not change the Sectioned trigger threshold.

## Unknown or partially matched technology

Missing a playbook is not a blocker. Svelte + an unknown backend retains full-stack, the actual frontend language and Svelte guidance; only the uncovered backend boundary uses universal. Do not guess Java/Python to fill the gap. A missing guide for one axis never cancels matches in another axis.

Inspect source/types/fixtures for the missing seam, then use primary documentation or the smallest safe distinguishing probe only when material. Record the gap for maintainers; do not pause product work to author a new guide.

Resolve conflicting advice through current user authority, repository contracts, actual code and installed configuration—not the strictest combination of every guide. Connect different owners through a shared contract instead of imposing one global abstraction.

## Review, handoff and re-routing

The independent PLAN reviewer performs the same **four-catalog inspection**, then reads only relevant selected guides and any guide the author actually missed. Do not treat the author's list as the whole library; verify selection against source. Use universal only for the review's named uncovered part. Keep this in the existing single pass; no reviewer per axis.

When the author skipped an applicable reference, read it in the current pass and report any concrete authority-backed plan defect; do not demand cosmetic route labels, a new full review or a product requirement solely to prove that a file was read. Give implementers resolved task-relevant excerpts/links and shared examples, not the whole library, all indexes or research chat.

Reuse catalogs/guides already read completely in the current planning context; do not reread them per section or dispatch. A fresh planning/review context must inspect the four catalogs once. PLAN_DELTA reloads only changed routes, affected knowledge and invalidated boundaries. Re-route when material owners/runtime/contracts/requirements change, not for wording edits, retries or library reorganizations. No reopening accepted work or new approval hash.

Audit observes the actual selected/skipped/fallback boundaries in existing artifacts and must not run a route-completeness gate or add calls for telemetry. [Worked combinations](examples.md) and [sources/freshness](sources.md) remain optional.
