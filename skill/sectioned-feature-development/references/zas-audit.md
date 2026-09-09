# ZAS audit — paired with the process pack

## Purpose

Record actual ZAS review attempts, control failures, caller observations and resource cleanup for later ZAS and Sectioned analysis. This is observational: no extra reviewer, test, model call, observation call or repair is run solely to populate the audit.

## Two archives, one feature

If the process archive is `~/Desktop/audit-pack/xxx.zip`, the associated ZAS archive is exactly `~/Desktop/audit-pack/xxx-zas.zip`. It is not an independent feature/sample. All ZAS attempts of that feature/run share this one companion; do not create one ZIP per Agent or timestamp.

The main ZIP retains ordinary workflow evidence, aggregate costs and a small `ZAS-LINK.json`. Detailed ZAS reports, the attempt ledger, selected observations and lifecycle/diagnostic receipts live only in the companion. Minimal ZAS lifecycle events already present in the process trace need not be removed; never duplicate the full payloads.

If ZAS was not used, write `status=NOT_USED` and `companion_filename=null` in the main link; do not publish an empty companion. Standalone runtime/conformance/diagnostic archives remain outside this reserved folder. The paired companion is the only added exception and must carry typed association, not just a filename suffix.

## Working artifacts

Keep under `.agent-work`:

```text
.agent-work/audit-packs/{feature-id}/current/ZAS-LINK.json
.agent-work/audit-packs/{feature-id}/zas/
  ZAS-IDENTITY.json
  ZAS-AUDIT.md
  ZAS-RUNS.jsonl
  observations/    # only snapshots actually inspected because of suspicion
  receipts/        # safe result/diagnostic/control evidence
```

The companion identity has `kind=sectioned-development-zas-audit`, `producer=sectioned-feature-development`, and the same feature_id/run_id as the main pack. The finalizer adds parent filename, parent exact ZIP hash and source HEAD. The main link does not include the companion hash, avoiding a circular digest dependency.

No `.sha256` file is created, beside or inside the new packs. Integrity values remain in existing JSON manifests/receipts; hashes are metadata, not additional output files. Do not delete historical checksum files or rewrite prior archives merely for this change.

## Attempt contents

Use `assets/ZAS-ATTEMPT.template.json`, one row per physical attempt, including failed spawn before an Agent ID exists. Record only actual values:

- feature/run, business section/subsection/lineage, logical review slot and physical attempt ID;
- actual Agent/session/turn/request/message IDs where exposed, source provenance and deployed generation/build;
- requested/observed model/effort as available; configuration is not an observed model;
- frozen candidate/head/plan/task fingerprints and read-only-result comparison;
- lifecycle transitions, permission waits, message disposition, result completeness and first failure;
- suspicion, `snapshot_seq`, selected tool calls/200-character reasoning tail, caller assessment/action and uncertainty;
- cancel/reap/close timing and result, workspace release, retry/fallback and later human correction;
- measured counts/time/tokens or UNKNOWN, never invented zero.

The five assessment definitions exist in the MCP description only. ZAS supplies facts; it must not emit an automatic semantic label, loop score or cancellation recommendation. Retain the caller's short assessment as caller-originated evidence, not as a daemon verdict.

No hidden/private/encrypted payloads or tool outputs are part of observe snapshots. Do not crawl unrelated session/log directories. Reuse the existing bounded diagnose path only for a concrete failure; do not export logs for every healthy task. Lifetime counters and rolling windows must not be summed as independent work.

## Finalization and recovery

Prepare main link and companion staging before finalization. Use the existing canonical command with one added argument when ZAS was used:

```bash
python {skill-dir}/scripts/audit_finalize.py finalize \
  --repo . --feature-id {feature-id} \
  --pack-dir .agent-work/audit-packs/{feature-id}/current \
  --trace .agent-work/audit/{feature-id}/TRACE.jsonl \
  --feature-base {base} --product-head {head} \
  --desktop-root ~/Desktop/audit-pack \
  --zas-pack-dir .agent-work/audit-packs/{feature-id}/zas
```

The parent is published first and the companion is bound to its exact bytes. Each ZIP is atomically replaced, but the two paths are not falsely described as one filesystem transaction. If companion finalization fails, retain the valid parent and record `PAIR_INCOMPLETE`. Rerun the same command after one bounded artifact-only correction; reuse the parent unchanged and finish the same `xxx-zas.zip`. Do not generate a new timestamp, re-run models, or call the pair complete while one member is missing/stale.

A separate `zas_audit_pack.py finalize --parent-zip ... --pack-dir ...` can re-publish only companion evidence. Validate with `zas_audit_pack.py verify --parent-zip ... --zip ...`. A parent replacement makes an old companion stale until re-bound from the same feature/run evidence.

## Intake and analysis

`process_audit.py intake` marks a ZAS archive `ZAS_COMPANION_CANDIDATE`, never `PROCESS` or another feature. Validate kind/producer/feature/run, exact parent filename/hash and internal JSON manifest before association. A missing/wrong/stale parent is a pairing gap; do not guess by title. Keep the main and companion costs linked, count each physical attempt once.

Separate application defects, task/PLAN issues, caller model judgment, ZAS lifecycle/control faults, ZCode runtime rejection, host environment and telemetry gaps. Diagnose only what evidence supports. Advisor handoffs remain a different artifact purpose and keep their existing external/human workflow.
