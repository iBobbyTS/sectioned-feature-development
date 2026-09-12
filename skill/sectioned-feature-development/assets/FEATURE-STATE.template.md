# Feature state — <feature-id>

- Status: PLANNED / EXECUTING / BLOCKED / COMPLETED
- Repository, branch, feature base, current candidate:
- Execution mode: PLAN_ONLY / EXECUTE_NO_COMMIT / EXECUTE_WITH_COMMITS (choose one; multiple business sections or executable subsections require EXECUTE_WITH_COMMITS):
- Dedicated feature branch and explicit base authority:
- Invocation source/timing and user approval when needed:
- Confirmed requirements / PLAN / original review references:
- PLAN passes selected / returned / outstanding; main admission and remaining owner decisions:
- Current unit and planned implementation role:
- Actual active actor(s): native-or-ZAS route + raw returned ID, role, unit, workspace, outstanding result:
- Last completed action and evidence:
- Next action and completed/unmet handoff prerequisite; named parallel exception if applicable:
- Full-review slot counter / planned provider / actual dispatch route / explicit override authority:
- Per-parent primary coverage, open finding IDs, repair attempts, recovery-used:
- Checkpoint/reconciliation and invalidated coverage, when children are used:
- Accepted parent head → integrated feature head:
- Final checks/head/readiness:
- Advisor hold/trigger/pack/result/human adoption/restart, when triggered:
- Audit mode: LIVE by default / OFF only with explicit user authority:
- Audit scope: current feature/run, evidence location, available source-session pointers:
- Audit delivery: PENDING / COMPLETE / INCOMPLETE / OFF:
- Audit next: preserve evidence while working; finalize after product closure, or actual blocker:
- Main ZIP: pending / actual delivered path; pack status and known gaps:
- ZAS companion: NOT_USED / pending / actual paired path; pairing gap if any:
- Audit attempt/correction or inability to invoke; preserved working path when incomplete:
- Closure date/head, or explicit reopen authority and preserved old plan:

Only record applicable facts at real transitions; do not rewrite state on every poll. Keep Audit mode, scope and delivery from activation through takeover and final handoff, even if other optional fields are omitted. Product COMPLETED does not erase Audit PENDING; Next is not none while packaging remains. For OFF, keep the explicit user instruction. A closed plan and its audit evidence must not absorb a later request. No fixed JSON schema, synthetic IDs or hash-matching admission. Review pending means wait on the actual actor, not launch the successor.
