# Section Contract：<Sxx — Title>

## Identity and Baseline

- Feature: `<name>`
- Section: `<Sxx / Sxx.n>`
- Parent section / lineage: `<none or Sxx -> Sxx.n>`
- Replan generation: `<0+>`
- Contract revision: `1`
- Frozen at: `<timestamp>`
- Section base: `<commit or fingerprint>`
- Dependency heads: `<Syy=commit>`
- Plan fingerprint: `<sha256>`
- Assurance envelope revision: `<vN>`
- Implementer profile: `<profile>`
- Reviewer profile: `sol_xhigh`
- Acceptance rule: `2 consecutive CLEAN admissions within 5 completed full reviews`

## Goal and Observable Increment

- Goal: <one coherent outcome or enabling seam>
- Observable behavior: <...>

## Scope and Direct Semantic Impact Cone

- Expected files/symbols/workflows: <...>
- Authoritative owners modified: <...>
- Direct callers/consumers/contracts included: <finite named set>
- High-risk boundaries: <...>
- Permitted mechanical/generated changes: <...>
- Anything else requires `IN_SCOPE_REPLAN` or an approved scope-change record.

## Assurance Envelope

- Artifact role / supported deployment: <...>
- Protected assets: <...>
- Trusted actors/inputs: <...>
- Untrusted actors/inputs and capabilities: <...>
- Entry points / trust boundaries: <...>
- Required guarantees: <...>
- Explicit exclusions / non-guarantees: <...>
- Existing authoritative policy anchors: <...>

## Minimum-sufficient Design and Complexity Budget

| Mechanism allowed | Requirement/invariant anchor | Simpler alternative considered | Why insufficient | Removal/rollback condition |
|---|---|---|---|---|
| `<none or item>` | `<R/INV/path>` | <...> | <...> | <...> |

- New service/registry/configuration/framework not listed above: `forbidden pending replan`
- New threat actor/environment/guarantee: `forbidden pending owner-approved scope change`

## Non-goals and Named Deferred Work

- Non-goal: <...>
- Deferred item -> owner section: <... or none>

## Feature-level Invariants

- `INV-01`: <...>
- `INV-02`: <...>

## Section Acceptance Criteria

- `Sxx-AC-01`: <trigger, expected behavior, evidence>
- `Sxx-AC-02`: <negative/failure behavior>

## Verification

```bash
<command>
```

- Runtime/manual evidence: <...>
- Unavailable checks and blocker policy: <...>

## Compatibility, Rollout, and Recovery

- Intermediate state validity: <...>
- Compatibility/migration: <...>
- Feature flag/rollout: <...>
- Rollback/recovery: <...>
- Observability/audit: <...>

## Review and Scope-change Rules

- Raw reviewer candidates are not requirements.
- Main-agent admission uses the frozen contract and assurance envelope.
- A real defect whose smallest correct repair crosses this section is `IN_SCOPE_REPLAN`, not scope creep.
- A new feature/actor/environment/compatibility/durability guarantee is `SCOPE_PROPOSAL` until an owner approves `SC-*.md` and revisions are frozen.
- Open owner decisions before implementation: `none`; otherwise block.

## Replan / Hard-Cap Triggers

- Approved behavior/acceptance criteria or authoritative policy changes.
- Smallest correct repair crosses the direct impact cone.
- Implementation exceeds the complexity budget.
- Contract/evidence cannot produce a finite decision.
- Five completed full reviews without two clean admissions triggers automatic classified recovery.
