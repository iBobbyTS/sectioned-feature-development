# Section Raw Review Request

- Review mode: `SECTION`
- Working path: `<path>`
- Section: `<Sxx / Sxx.n>`
- Counting round: `<1..5>`
- Review attempt: `<1+>`
- Range: `<section_base>..<section_head>`
- Feature contract: `.agent-work/PLAN-FULL.md`
- Section contract: `.agent-work/sections/<ID>-CONTRACT.md`
- Implementation handoff: `.agent-work/sections/<ID>-HANDOFF.md`
- Output: `.agent-work/reviews/<ID>-SECTION-r<NN>-RAW.md`
- Review skill: `$code-review`

## Independent Context Rule

Use the current contract, repository-local rules needed to interpret it, repository state, diff, and evidence. Do not request or consume the originating session transcript, previous clean verdicts, previous reviewer persuasion, or rejected scope proposals before forming candidates.

## Review Objective

Find evidence-backed defects against:

1. frozen section acceptance criteria;
2. feature invariants and authoritative repository policy;
3. reachable supported behavior inside the frozen assurance envelope;
4. direct semantic impact cone named by the contract;
5. tests/evidence needed to prove those obligations.

Review discovers defects; it does not create requirements. Do not silently strengthen the threat model, supported environment, compatibility/durability promise, architecture, or product scope.

## Candidate Format

For each candidate include:

- stable candidate ID and severity;
- exact contract/repository anchor;
- reachable trigger in the supported environment;
- material consequence;
- evidence or falsifiable evidence path;
- smallest correct remedy;
- whether that remedy stays inside the section or requires cross-section replan;
- for security: asset, actor, capability, entry point/data flow, trust boundary, preconditions, and supported deployment context.

Mark optional polish/generalization explicitly. Do not issue the workflow's final admission or section-accepted verdict; the main agent performs that gate separately.
