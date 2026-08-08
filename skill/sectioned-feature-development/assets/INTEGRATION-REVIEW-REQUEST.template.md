# Feature Integration Raw Review Request

- Review mode: `INTEGRATION`
- Working path: `<path>`
- Feature: `<name>`
- Feature base/head: `<base>..<head>`
- Feature contract: `.agent-work/PLAN-FULL.md`
- Feature state: `.agent-work/FEATURE-STATE.md`
- Assurance envelope revision: `<vN>`
- Active section artifacts: `.agent-work/sections/`
- Review/admission index: `.agent-work/reviews/`
- Output: `.agent-work/reviews/FEATURE-INTEGRATION-r01-RAW.md`
- Review skill: `$code-review`

## Required Focus

- Original full-feature goal, non-goals, and requirement coverage.
- Cross-section API/schema/state/permission/order/error contracts.
- End-to-end happy, negative, and partial-failure paths.
- Migration, compatibility, flags, rollout, rollback, cleanup, and latest combined checks.
- Security, privacy, reliability, performance, observability, and operations only inside the frozen assurance envelope.
- Deferred-work closure and branch-scope integrity.

## Calibration

Do not replay every accepted local line. Do not reopen the threat model or supported environment without a concrete reachable cross-section trigger and authoritative anchor. Report raw candidates using the same evidence fields as section review. A separate main-agent admission record determines whether each candidate is material, deferred, a scope proposal, unsupported, or non-blocking.
