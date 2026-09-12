# Planning composition examples

These are hypothetical routing examples and maintainer evaluation cases, not measured model outcomes and not facts about the user's repositories. Always use the actual changed source and requirements. Common entry: router + all four short catalogs, then the source-matched guides. Universal is loaded only for a named uncovered part; boundary-handoff is added only for a shared changed contract.

## Contents

- [Independent combinations](#independent-combinations)
- [Observed failure class, not a new LMDO requirement](#observed-failure-class-not-a-new-lmdo-requirement)
- [Full-stack seam: one contract, not independent mocks](#full-stack-seam-one-contract-not-independent-mocks)
- [Native UI plus helper: keep the invariant whole](#native-ui-plus-helper-keep-the-invariant-whole)
- [Partial match and fallback](#partial-match-and-fallback)
- [Domain knowledge is not scope authority](#domain-knowledge-is-not-scope-authority)

## Independent combinations

| Changed task | Domains | Languages | Adapters | Concerns when activated |
|---|---|---|---|---|
| Svelte TypeScript client + Java Spring controller | full-stack | TypeScript, Java | Svelte/SvelteKit, Spring; browser only for browser-specific semantics | external-integration or data-evolution only when those semantics change |
| Single-repo SvelteKit TypeScript reorder feature | full-stack | TypeScript | Svelte/SvelteKit | async-lifecycle for stale/rollback behavior; no inferred Java |
| React/Next server/client feature | full-stack | TypeScript | Next.js; React only for a separate state/effect question | actual cache/mutation or async concerns, not every concern |
| Vue/Nuxt component interaction only | web-frontend | TypeScript | Vue/Nuxt | relevant lifecycle; no backend guide for an untouched endpoint |
| Angular client + C# ASP.NET Core API | full-stack | TypeScript, C# | Angular, ASP.NET Core | actual changed API/data/async boundary |
| Python FastAPI endpoint | backend-services | Python | FastAPI | actual external/data concern; no Django assumption |
| Python CLI import | cli-automation | Python, SQL only if query semantics change | none unless an actual framework rule matters | data-evolution for changed import atomicity |
| Python Airflow data transformation | data-engineering | Python/SQL actually edited | use installed Airflow source for a missing adapter | replay/partition/scale concerns only as required |
| Python training/inference change | ai-ml | Python | actual ML framework via source or fallback | performance and data only if changed; not selected just because Codex writes code |
| R analysis package | scientific-computing; libraries-sdks if publication changes | R | none by default | numeric tolerance/reproducibility, performance only with a bound |
| Swift server route | backend-services | Swift | actual server framework via fallback | no macOS or SwiftUI unless it is a real target/owner |
| SwiftUI macOS UI controlling Rust helper | desktop-apps; systems-daemons if helper lifetime changes | Swift, Rust | SwiftUI/AppKit, macOS; Tokio only if actually used | async-lifecycle; one IPC contract |
| C# desktop editor | desktop-apps | C# | actual Windows UI framework via fallback | no ASP.NET just because the language is C# |
| Kotlin Android application | mobile-apps | Kotlin | Android | task/back-stack/process lifecycle when changed |
| Swift iOS/iPadOS scene | mobile-apps | Swift | Apple mobile; SwiftUI/AppKit only when that UI family is used | actual scene/task lifecycle, not Mac distribution |
| Flutter phone/tablet feature | mobile-apps | Dart | Flutter; OS adapter only for a native platform seam | async-lifecycle only if relevant |
| Go network service | backend-services | Go | actual service runtime via source | cancellation/backpressure only where changed |
| Rust synchronous reusable crate | libraries-sdks | Rust | none | no Tokio/async checklist |
| TypeScript command-line tool | cli-automation | TypeScript | Node.js when stream/process behavior matters | no web-frontend/React automatically |
| POSIX shell release automation | cli-automation or cloud-platform-devops | Bash/POSIX shell | actual host/toolchain source | error propagation/resource cleanup as required |
| PowerShell deployment command | cloud-platform-devops | PowerShell | actual host/remote API source | no Bash exit/pipeline assumptions |
| C firmware ISR change | embedded-iot | C | board/RTOS source via fallback | timing/ownership; desktop concurrency recipes do not transfer blindly |
| C++ game simulation update | games-realtime | C++ | engine source via fallback | frame/tick timing and performance only for concrete requirements |
| Lua host extension | libraries-sdks or actual host domain | Lua | real host binding source | no automatic games routing |
| PHP Laravel background job | backend-services | PHP | Laravel | queue transaction/retry semantics when changed |
| Ruby Rails write + callback | backend-services | Ruby | Rails | transaction/commit/external side effect boundary |
| HTML/CSS layout/semantic form change | web-frontend | HTML/CSS; JS only if changed | browser if layout/event semantics matter | no React/Svelte merely because dependencies exist |
| Elixir/OCaml or another unlisted backend | backend-services | universal fallback for unlisted language | actual framework/version source as needed | retain independently matched concerns |
| Unknown device/API used by a known language | actual domain if known | actual known language | universal fallback for unknown adapter | external-integration with a bounded probe |

A table row is not a mandatory load set: select the smallest applicable guides for the actual unresolved questions. Do not load full-stack, frontend and backend together just to label every layer.

## Observed failure class, not a new LMDO requirement


The supplied LMDO audit identified mismatched request keys/baseline, an incorrect visible-only assumption about the server response, and a named sibling reader still sorting by name. It does not establish the implementation of an unrelated project.

For that class of task, after inspecting all four catalogs, route **domain full-stack + the actual JavaScript/TypeScript language + Svelte/SvelteKit adapter + boundary-handoff**; use universal only for an additional named uncovered boundary; add data-evolution/async-lifecycle only for the actual transaction or interaction changes. Do not add Java: the user's Java example is not evidence of LMDO's backend.

A compact illustrative boundary entry could be:

```text
B1 — save visible-group order (PLANNED example; confirm actual source)
Authority: confirmed global ordering; named readers must agree.
Producer/consumer: real reorder action -> actual UI submit/decoder/render.
Input: groupIds=[B,A], baselineGroupIds=[A,B].
Transport: inspect whether actual path is SvelteKit form action or JSON endpoint.
Output: source-confirmed groups shape; distinguish GLOBAL_SET from VISIBLE_SET.
State: hidden/inactive groups follow confirmed policy, not inferred deletion.
Consumers: board UI + /dashboard/groups default read/sort behavior.
Check: two distinguishable groups, end insertion, successful response does not
       falsely roll back; a real failure restores prior view and retry works.
```

At PLAN time, confirm the existing request/response in source or label the example planned/unknown. Do not pretend this synthetic text is a captured wire response. At producer handoff, attach the actual redacted request/response fixture and the matching check/result. The UI worker tests its **real submission and decoding code** against that same fixture. A different mock shape in each layer is not contract evidence.

Keep one business parent, with server and UI checkpoints when useful. A user-named consumer that needs behavior changes is `EDIT`, not merely `inspect-only`. If it already satisfies the requirement, record `VERIFY_UNCHANGED` and its source/check; do not edit it just to fill a list. None of this authorizes a new API framework, security mechanism, or extra full review.

## Full-stack seam: one contract, not independent mocks

For a hypothetical Svelte/Java feature, the plan maps the actual client serializer, server controller/service, changed state, returned collection and all named readers. PLAN marks new examples PLANNED; producer HANDOFF supplies an observed or source-backed fixture; consumer TASK uses the same contract/fixture through its real request builder/decoder.

A successful backend write followed by client-side response rejection is one cross-boundary failure. It does not call for separate new features, a contract broker or an API redesign. Neither full-stack nor Java implies that LMDO uses Java.

## Native UI plus helper: keep the invariant whole

A Swift/Rust operation may have a UI request identity, an IPC frame, a Rust child lifetime and a late completion. Keep their shared correctness obligation in one business parent; internal modules/model workload can be subsections. macOS guidance only applies to the target application, not the developer's laptop. Do not introduce a supervisor or signing pipeline unless the change actually requires it.

## Partial match and fallback

Svelte + an unknown backend loads the known Svelte/full-stack knowledge and universal input→owner→output→consumer reasoning for the backend. Establish encoding and failure semantics from source or a small safe probe. Missing a language or framework file neither blocks planning nor justifies guessing another technology.

## Domain knowledge is not scope authority

A local import script may use the data-evolution concern without becoming a warehouse platform. A C++ patch may use performance reasoning without a benchmark platform. A machine-learning guide may suggest evaluating affected inputs without authorizing new product metrics. Match only the changed promise and preserve user-approved scope.
