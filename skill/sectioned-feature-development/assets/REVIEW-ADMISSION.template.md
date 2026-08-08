# Review Admission：<Section> r<NN>

- Mode: `SECTION | INTEGRATION`
- Section: `<Sxx / FEATURE>`
- Counting round: `<1..5 or N/A>`
- Review attempt: `<1+>`
- Raw review: `<path>`
- Contract revision: `<n>`
- Plan fingerprint: `<sha256>`
- Assurance envelope revision: `<vN>`
- Reviewed base: `<commit>`
- Reviewed head: `<commit>`
- Evidence-valid conclusion: `yes | no`
- Result: `CLEAN | MATERIAL_FINDINGS | OWNER_DECISION | EVIDENCE_FAILURE`
- Clean admission: `yes | no`
- Clean streak after: `<0..2>`

## Candidate Decisions

<!-- FINDING:REV-001:START -->
### REV-001 — <Title>

- Raw severity: `Must Fix | Should Fix | Needs Decision | Suggestion`
- Domain: `correctness | security | privacy | compatibility | reliability | performance | maintainability | testing | operations | other`
- Admission class: `IN_SCOPE_REPAIR | IN_SCOPE_REPLAN | OWNER_DECISION | EVIDENCE_FAILURE | DEFERRED_OWNER | SCOPE_PROPOSAL | UNSUPPORTED_HYPOTHESIS | NIT_DEBT`
- Contract/repository anchor: `<R/AC/INV/path or none>`
- Reachable supported trigger: `<trigger or none>`
- Material consequence: `<consequence or none>`
- Evidence / falsifiable path: `<evidence or none>`
- Smallest correct remedy: `<remedy or none>`
- Boundary effect: `inside-section | cross-section | owner-decision | evidence-only | deferred | new-scope | none`
- Named deferred owner: `<section or none>`
- Security asset: `<asset or N/A>`
- Security actor and capability: `<actor/capability or N/A>`
- Security entry point / data flow: `<... or N/A>`
- Security trust boundary and preconditions: `<... or N/A>`
- Supported deployment context: `<... or N/A>`
- Decision rationale: `<why this class follows from frozen evidence>`
- Scope-change record: `<SC-xxx or none>`
<!-- FINDING:REV-001:END -->

## Round Summary

- Material admitted IDs: `<list or none>`
- Non-authoritative scope proposals: `<list or none>`
- Unsupported/nit/deferred IDs: `<list or none>`
- Evidence invalidated: `<none or exact evidence>`
- Next action: `<fresh review | repair IDs | bounded replan | owner decision | repair evidence>`
