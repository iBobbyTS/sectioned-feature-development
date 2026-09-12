# Concern planning index

Inspect this catalog once, alongside the domain, language and adapter catalogs, in each fresh PLAN-authoring/review context. Read the guides that match the changed semantics; do not read every guide or apply every risk to every task. This catalog is not product authority.

| Route | Select from evidence | Guide | Do not select merely because |
|---|---|---|---|
| Data evolution | The change affects persisted representation, migration, import/backfill, conversion, atomicity or compatibility of existing data. | [data-evolution.md](data-evolution.md) | Code reads a database without changing those semantics. |
| Async lifecycle | The change affects async ownership, pending/late results, cancellation, retries, cleanup or process lifetime. | [async-lifecycle.md](async-lifecycle.md) | An `async` keyword exists in untouched code. |
| External integration | The change crosses an actual service/SDK/device/agent/IPC contract, capability, auth or error boundary. | [external-integration.md](external-integration.md) | Development uses an AI assistant or a dependency is merely installed. |
| Performance and cardinality | The acceptance path has a concrete input-size, latency, memory, complexity or cost constraint. | [performance.md](performance.md) | Future growth can be imagined without a current workload or obligation. |

After inspecting all four catalogs and reading actual matches, use [universal](../universal.md) only for a named uncovered part. `NOT_APPLICABLE` is not a coverage gap. Do not add reviews, model tiers or performance infrastructure because a guide was listed.
