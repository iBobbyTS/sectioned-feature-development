# Branches, parallel execution and integration

## Branch contract

`len(sections)>1` implies `EXECUTE_WITH_COMMITS`, a non-main dedicated feature branch and coherent implementation/repair commits. This also holds after late adoption or a plan revision adds a second section. Conflicting no-commit instructions stop execution before further edits.

Preserve dirty user work. From main, branch creation is authorized; from another branch, obtain the user's base choice. Never reset main to move accidentally committed work. Record original base/current adoption head and ask only for destructive history changes.

`.agent-work` is locally excluded and never committed. Do not force-add tracked legacy workflow files. For parallel work, add `/git-worktree/` to `.gitignore` before creating `./git-worktree`; preserve other ignore rules. This infrastructure setup is an explicit user requirement, not a new product feature.

## Ready-node scheduling

Use one orchestrator as schedule/state writer. Call `workflow.py ready` before dispatch. Workers do not edit the scheduler's state or choose siblings.

A section is ready when all prerequisites are accepted and integrated on the feature branch. A sibling can run concurrently only if:
- both are explicitly marked parallel-eligible;
- neither depends transitively on the other;
- no write/write or write/read path overlap;
- no mutated/consumed contract collision;
- no shared mutable DB/schema/port/output/cache/credential test resource;
- each has a distinct canonical worktree/branch and a concrete validation environment.

Read-only shared source is safe if no active worker changes its contract. Unknown interference means serial, not optimistic parallelism. Start with two writers; resource capacity, not model price alone, limits concurrency.

## Worktree procedure

1. Record feature base/head, reserve section and branch names.
2. Ensure ignore entry, then `mkdir -p ./git-worktree`. Main may make this expressly authorized `.gitignore` setup edit and a narrow setup commit before worker dispatch; freeze worker bases after that commit. Use canonical scope paths, not symlink aliases.
3. `git worktree add -b <section-branch> ./git-worktree/<run-id>-<section-id> <accepted-feature-head>`.
4. Pass the absolute worktree path, base SHA and task packet to exactly one writer.
5. Review a committed immutable candidate in a separate detached snapshot where practical; check product diff/fingerprint before and after review. Workflow files/results are local or returned to parent.
6. Main serializes accepted section commits into the feature branch in PLAN integration order using normal local merge/cherry-pick. This is internal feature integration, not merge to main.
7. If the target feature head changed on a sibling's direct impact cone, rerun composition checks. A conflict requiring semantic changes returns to the relevant owner; don't silently accept an automatic conflict resolution.
8. Preserve worktrees unless cleanup was separately authorized. Do not run broad reset/clean/remove commands to tidy evidence.

Different worktrees still share Git common metadata, and tests may share external state. Branch separation alone proves neither test isolation nor semantic independence.

## Stage barrier

For a section: IMPLEMENT → CHECK → frozen REVIEW → admitted REPAIR → CHECK → DELTA → optional independent FINAL → ACCEPTED → INTEGRATED.

No writer changes the reviewed snapshot. But S02 may implement while independent S01 is under review in another worktree. S03 that consumes S01 waits for acceptance+integration, not merely code availability. Plan review finishes before any dependent product implementation.

Reserve global full review indexes deterministically before parallel dispatch. Failed dispatch retries keep the same reservation. Delta checks keep their original review ID. Actual agent IDs/provider errors and cancellation/reap status are recorded.

## Acceptance and completion

Reviewer output is not admission. Main verifies findings/checks/provenance and applicable ONE/TWO evidence at the candidate head. Empty findings do not override missing required checks.

Merged candidate checks prove composition. Keep a final `unproven_composition` list; an empty list means no extra integration reviewer, not permission to omit required build/live gates. Relevant interface/state/environment changes invalidate evidence; a doc-only audit edit does not.

Broad suites once per appropriate stable gate. If logs truncate, save original output and summarize mechanically, not rerun the entire suite merely to recount tests. No old green check can bless later unreviewed product edits.

A blocked environment is reported separately from product defects. Feature closure stores final head, plan digest and outcome. `workflow.py follow-up` will never authorize appending a completed plan without an explicit user reopen request.
