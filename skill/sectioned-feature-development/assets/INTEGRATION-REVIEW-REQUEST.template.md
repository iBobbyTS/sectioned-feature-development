# Feature Integration Review Request

Use `$code-review` as one fresh `INTEGRATION` pass only when cross-section/runtime/process composition remains unproven. A single-section feature whose bounded review covered the complete feature path should skip this reviewer and run only the required feature gate.

- Feature ID:
- Feature base:
- Feature head:
- Feature plan:
- Accepted section summary:
- Original feature acceptance criteria:
- Repository-required gates:
- Integration repair waves used: `<N>/5`
- Integration automatic recovery used: `no | yes`
- Required end-to-end checks:
- Output:

Review only what local section reviews could not prove:

- original feature outcome and non-goals;
- emergent cross-section API/schema/state/permission/ordering/error behavior;
- required migration, compatibility, rollout, rollback, cleanup, and observability;
- representative end-to-end paths;
- branch-scope integrity.

Use the same classes and blocking proof as section review. Admit only:

- feature-diff-caused composition defects;
- a necessary merge-blocking dependency on a real feature acceptance path;
- an evidence gap tied to an existing feature acceptance criterion or repository-required gate.

Cross-section composition creates no authority to add stronger product/security/durability/compatibility/observability/rollout promises, routes, analyzers, governance, or browser flows. Do not repeat local section review, audit unrelated repository code, or reopen an accepted section without concrete combined-behavior evidence.

Any admitted integration repair counts toward the single cumulative integration budget; rerunning this gate does not reset it. Tier 3 checks verify existing criteria only.
