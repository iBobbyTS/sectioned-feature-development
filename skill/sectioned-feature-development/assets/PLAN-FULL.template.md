# Full Feature Plan

<!-- FEATURE-CONTEXT:START -->
## Feature Context

### Feature identity

- Feature ID / slug:
- Feature base or mid-feature adoption head:
- Starting branch and selected branch origin:
- Non-main branch choice authority, if applicable:
- Skill invocation source / timing:
- Trigger evidence, negative evidence, predicted owners/sections/behavioral LOC:
- Automatic invocation announcement / approval: `not-applicable | pending | approved | rejected | narrowed`
- Active artifacts belong only to this feature and remain untracked: `yes`
- Audit mode / trace / exact-requirements record:

### Original user request

- Exact request record: `.agent-work/audit/{feature-id}/REQUIREMENTS.md`
- Copy the request verbatim or quote the exact approved outcome.
- Grill Me / equivalent clarification questions and answers, or `not used`:
- Later corrections and superseded earlier guidance:

### Requirement, example, and correction traceability

| ID | Current instruction/example/correction | Supersedes | Acceptance criterion | Test or probe |
|---|---|---|---|---|
| REQ-001 |  | none | AC-F-001 |  |

### Minimum sufficient end-to-end outcome

- Smallest observable result that satisfies the request without optional completeness work.

### Scope authority map

- For each proposed outcome, option/UI/config surface, compatibility promise, support harness, or structural change: cite user intent, repository/current-production obligation, or an unavoidable correctness dependency. A plan/section/reviewer is not an authority source.

### Foundational-owner decisions

- Identify any requested behavior whose smallest correct implementation could be either a local patch or a bounded change to an existing shared owner.
- Record the current choice and authority: `not-applicable | local patch approved | shared owner approved | owner decision pending`.
- Do not propose a new generalized component merely to avoid the decision.

### Goal

One sentence describing the requested product outcome.

### Observable behavior

- User/operator-visible behavior that must become true.

### Constraints and invariants

- Existing repository/product invariants that remain authoritative.

### Non-goals and unsupported environments

- Explicitly excluded behavior, actors, deployments, compatibility, durability, or governance work.

### Ownership and state boundaries

- Existing owner(s) that must remain authoritative.

### Allowed structural changes

- List only new services, registries, persistence, workers, public surfaces, analyzers, or security controls explicitly required. Use `none` when no such mechanism is authorized.

### Audit-remediation scope, if applicable

- Accepted audit finding IDs: `none`
- Unrelated discoveries go to: separate audit backlog

### Feature acceptance criteria

- Falsifiable end-to-end acceptance criteria.

### Validation tiers

- Targeted:
- Section/package:
- Final integration/repository:

### Compatibility, migration, rollout, rollback, and cleanup

- Record only what the requested feature actually requires.
<!-- FEATURE-CONTEXT:END -->

## Plan Review Gate

- Status: `PENDING | APPROVED | BLOCKED`
- Reviewed PLAN-FULL SHA-256:
- Reviewer profile and stable task/session ID:
- Admitted `PLAN_BLOCKER` / `PLAN_SCOPE_EXPANSION` / `OWNER_DECISION` IDs:
- Corrections applied:
- `PLAN_DELTA` recheck: `not-required | pending | approved | blocked`

<!-- SECTION:S01:START -->
## S01 — First behavior slice

### Goal

One coherent observable behavior increment.

### Authority and necessity

- Authority anchor:
- Why required for the minimum end-to-end outcome:
- Why the existing owner/path cannot satisfy it more simply:
- Local-patch versus foundational-owner choice: `not-applicable | local patch | shared owner | owner decision pending`

### Dependencies

- Requires: `none`
- Base: exact accepted predecessor commit at execution time.

### Expected scope and direct impact cone

- Primary owner:
- Allowed-to-edit owners/files/symbols/routes/workflows:
- Inspect-only dependency paths/direct callers/callees/serializers/contracts/tests:
- Explicitly excluded owners/mechanisms:
- Unlisted dependencies may be inspected only through a recorded causal chain from a changed symbol; inspection does not authorize editing.

### Non-goals and deferred owner

- Explicit exclusions.
- Deferred behavior and named later section/owner, if any.

### Invariants

- Existing invariants touched by this section.

### Allowed structural changes

- `none`, or an explicit requirement-anchored mechanism.

### Review intensity

- `MECHANICAL | BOUNDED | HIGH_RISK`

### Review assurance

- Requested: `AUTO | ONE | TWO`
- Resolved: `ONE | TWO`
- Reasons / owner override / repository minimum:

### Acceptance criteria

- Falsifiable behavior and edge/error outcomes.

### Validation tiers

- Targeted:
- Section/package:
- Integration checkpoint, if triggered:

### Reset triggers

- Material API/schema/trust/state-owner/concurrency/deployment changes that would require a new initial review baseline.
<!-- SECTION:S01:END -->

<!-- SECTION:S02:START -->
## S02 — Second behavior slice

### Goal

One coherent observable behavior increment.

### Authority and necessity

- Authority anchor:
- Why required for the minimum end-to-end outcome:
- Why the existing owner/path cannot satisfy it more simply:
- Local-patch versus foundational-owner choice: `not-applicable | local patch | shared owner | owner decision pending`

### Dependencies

- Requires: `S01`
- Base: exact accepted predecessor commit at execution time.

### Expected scope and direct impact cone

- Primary owner:
- Allowed-to-edit owners/files/symbols/routes/workflows:
- Inspect-only dependency paths/direct callers/callees/serializers/contracts/tests:
- Explicitly excluded owners/mechanisms:
- Unlisted dependencies may be inspected only through a recorded causal chain from a changed symbol; inspection does not authorize editing.

### Non-goals and deferred owner

- Explicit exclusions.

### Invariants

- Existing invariants touched by this section.

### Allowed structural changes

- `none`.

### Review intensity

- `MECHANICAL | BOUNDED | HIGH_RISK`

### Review assurance

- Requested: `AUTO | ONE | TWO`
- Resolved: `ONE | TWO`
- Reasons / owner override / repository minimum:

### Acceptance criteria

- Falsifiable behavior and edge/error outcomes.

### Validation tiers

- Targeted:
- Section/package:
- Integration checkpoint, if triggered:

### Reset triggers

- Material changes that require a new initial review baseline.
<!-- SECTION:S02:END -->

## 4.2 executable schedule (additive to the v3.9 contract above)

The prose remains the behavior/authority contract; this block contains scheduling facts. Section IDs and dependencies must agree. Complete all placeholders. Before independent PLAN review, freeze this proposal with status FROZEN. Reviewer and admission operate on that exact file hash; only STATE/FEATURE-STATE become APPROVED, so approval does not itself mutate the reviewed plan. A completed plan is not edited to append later requests.

<!-- SFD_PLAN_V4 -->
```json
{
  "schema_version": 4,
  "workflow_revision": "4.2",
  "feature_id": "example-feature",
  "run_id": "example-run",
  "invocation_source": "USER_EXPLICIT",
  "status": "DRAFT",
  "execution_mode": "EXECUTE_WITH_COMMITS",
  "main_branch": "main",
  "feature_branch": "codex/example-feature",
  "base_ref": "0000000000000000000000000000000000000000",
  "branch_authority": "REPLACE_WITH_USER_OR_MAIN_RULE",
  "requirements_path": ".agent-work/REQUIREMENTS.md",
  "requirements_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "max_parallel_writers": 2,
  "worktree_parent": "git-worktree",
  "integration_order": [
    "S01",
    "S02"
  ],
  "stages": [
    {
      "id": "explore",
      "depends_on": [],
      "parallelism": "bounded-independent-queries",
      "profile": "code_explorer",
      "optional": true
    },
    {
      "id": "plan",
      "depends_on": [
        "explore"
      ],
      "parallelism": "serial",
      "profile": "plan_writer"
    },
    {
      "id": "plan-review",
      "depends_on": [
        "plan"
      ],
      "parallelism": "serial",
      "profile": "plan_reviewer"
    },
    {
      "id": "execute-dag",
      "depends_on": [
        "plan-review"
      ],
      "parallelism": "section-dag",
      "profile": "per-unit"
    },
    {
      "id": "integrate",
      "depends_on": [
        "execute-dag"
      ],
      "parallelism": "serial",
      "profile": "orchestrator"
    },
    {
      "id": "audit",
      "depends_on": [
        "integrate"
      ],
      "parallelism": "serial",
      "profile": "orchestrator",
      "optional": true
    }
  ],
  "checks": {
    "S01-focused": {
      "command": "REPLACE_WITH_EXISTING_COMMAND",
      "cwd": ".",
      "environment_id": "private-S01"
    },
    "S02-focused": {
      "command": "REPLACE_WITH_EXISTING_COMMAND",
      "cwd": ".",
      "environment_id": "private-S02"
    }
  },
  "sections": [
    {
      "id": "S01",
      "depends_on": [],
      "business_boundary": "Replace with independently consumed business outcome; NOT a model/layer label.",
      "owner": "core-rule",
      "lineage_id": "S01",
      "requirement_ids": [
        "REQ-001"
      ],
      "write_paths": [
        "src/S01",
        "tests/S01"
      ],
      "read_paths": [],
      "exclusive_resources": [],
      "mutates_contracts": [
        "base-contract"
      ],
      "consumes_contracts": [],
      "parallel_eligible": false,
      "parallel_reason": "Serial example; replace with proven independence only.",
      "profile": "implementer_2",
      "model_reason": "Replace with verified task evidence.",
      "task_features": {
        "analogue": "REPLACE_WITH_VERIFIED_OWNER",
        "ambiguity": "resolved",
        "semantic_hops": [
          "source",
          "consumer"
        ],
        "state_coupling": "local",
        "oracle_strength": "decisive",
        "novel_reasoning": false
      },
      "assurance": "TWO",
      "review_intensity": "BOUNDED",
      "check_ids": [
        "S01-focused"
      ],
      "oracle": "REPLACE_WITH_EXACT_REPRODUCTION",
      "acceptance": "REQ-001 required observable behavior",
      "delivery_mode": "ATOMIC"
    },
    {
      "id": "S02",
      "depends_on": [
        "S01"
      ],
      "business_boundary": "Replace with independently consumed business outcome; NOT a model/layer label.",
      "owner": "consumer-behavior",
      "lineage_id": "S02",
      "requirement_ids": [
        "REQ-001"
      ],
      "write_paths": [
        "src/S02",
        "tests/S02"
      ],
      "read_paths": [
        "src/S01"
      ],
      "exclusive_resources": [],
      "mutates_contracts": [],
      "consumes_contracts": [
        "base-contract"
      ],
      "parallel_eligible": false,
      "parallel_reason": "Serial example; replace with proven independence only.",
      "profile": "implementer_2",
      "model_reason": "Replace with verified task evidence.",
      "task_features": {
        "analogue": "REPLACE_WITH_VERIFIED_OWNER",
        "ambiguity": "resolved",
        "semantic_hops": [
          "source",
          "consumer"
        ],
        "state_coupling": "local",
        "oracle_strength": "decisive",
        "novel_reasoning": false
      },
      "assurance": "TWO",
      "review_intensity": "BOUNDED",
      "check_ids": [
        "S02-focused"
      ],
      "oracle": "REPLACE_WITH_EXACT_REPRODUCTION",
      "acceptance": "REQ-001 required observable behavior",
      "delivery_mode": "ATOMIC"
    }
  ]
}
```
<!-- /SFD_PLAN_V4 -->
