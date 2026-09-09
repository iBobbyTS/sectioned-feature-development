# Delegated single-pass review

- context: DELEGATED_PASS
- protocol: sfd-delegated-review/4.2
- feature/run/section/pass ID / full-pass index (delta: original pass):
- provider/profile/instance/session or agent_id:
- scope: INITIAL_BOUNDED / REPAIR_DELTA / FINAL_BOUNDED / INTEGRATION
- exact base/head or single-section no-commit fingerprint:
- approved requirements/AC, exclusions, owner paths and review snapshot:
- assurance ONE/TWO and required evidence:
- reused check evidence with head/environment/command digest:
- delta only: admitted root causes, closure criteria, repair range and invalidated cone:
- external only: terminal/session-continuity status; fingerprint pre/post:

Read actual relevant code; report causally reachable, material defects and uncertainty. Do not implement, rewrite the contract, run a second review loop or decide feature acceptance. Return pass identity, coverage, candidates with evidence, checks and gaps. The parent performs admission and applies repair budgets.

Return pass_signal CLEAN / MATERIAL_CANDIDATES / INSUFFICIENT_EVIDENCE. The installed companion code-review delegated protocol applies; no section acceptance or standalone repair loop.

## Optional subsection fields (parent inherits all authority)
- unit_kind: SECTION | SUBSECTION
- parent_section_id / subsection_id / lineage_id:
- parent base / previous checkpoint / current candidate:
- pending parent behavior and safe intermediate state:
- shared invariant IDs / targeted checkpoint checks / joint parent oracle:
- logical parent primary review ID / actual reviewer IDs / continuity status:
- output: CHECKPOINT_VERIFIED only after parent admission; not ACCEPTED, not new budget.

Compatibility: DELEGATED_PASS accepts legacy atomic `sfd-delegated-review/4.0`; new child packets use `sfd-delegated-review/4.2`.

## 4.4 packet representation

Return readable Markdown with the actual requested scope, identities, head, evidence and gaps. No machine receipt schema, registry or plan-hash equality is required. Any hash field in the template is optional archival identity unless a real immutable artifact transfer requires it. Missing evidence is still a gap; missing JSON formatting is not. Main owns admission/scheduling, never the reviewer.
