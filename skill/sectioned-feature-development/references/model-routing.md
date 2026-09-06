# Task–model routing

This is a provisional policy to evaluate, not a factual capability boundary. Source/task-family and small real-world comparisons disagree; no matched per-item evaluation establishes the optimal six configurations for these repositories. Research and limitations are in `docs/version-history/v4.0/RESEARCH.md` of the project distribution.

## Fixed roster

| Profile | Model | Effort | Role |
|---|---|---|---|
| [@implementer_4](subagent://implementer_4) | gpt-5.6-luna | xhigh | Transform an already specified local rule using a demonstrated analogue and decisive tests |
| [@implementer_3](subagent://implementer_3) | gpt-5.6-terra | high | Implement a familiar component/path with limited new state and verifiable behavior |
| [@implementer_2](subagent://implementer_2) | gpt-5.6-sol | medium | Default non-trivial implementation with coupled repository semantics |
| [@implementer_1](subagent://implementer_1) | gpt-6-astra | medium | Implement novel structural reasoning or unresolved cross-owner behavior that cannot be decomposed safely |
| [@code_reviewer](subagent://code_reviewer) | gpt-6-astra | high | Independent code review and integration delta review |
| [@plan_writer](subagent://plan_writer) | gpt-6-astra | xhigh | Plan author only; independent plan reviewer is below |
| [@plan_reviewer](subagent://plan_reviewer) | gpt-6-astra | xhigh | Independent review of saved PLAN; never the writer instance |
| [@code_explorer](subagent://code_explorer) | gpt-5.6-luna | xhigh | Read-only code-location and direct dependency discovery |
| [@advisor](subagent://advisor) | gpt-6-astra | xhigh | Rare, fresh-context technical adjudication |

Nine role files, six model–effort combinations; no max or low variants. GLM is the separately configured external review provider.

## Decision features

Record before dispatch:
- `analogue`: exact existing example path, or none;
- `ambiguity`: resolved / bounded unknown / structural unknown;
- `semantic_hops`: the producer→normalizer→store→projection→consumer path actually touched;
- `state_coupling`: stateless / local transitions / shared async or transactional state;
- `oracle_strength`: decisive regression or equivalence / partial / missing;
- `novel_reasoning`: yes/no and why; algorithmic cardinality or undocumented protocol counts;
- predicted context scope and consequence of a false clean.

Use Luna only when the task does not require discovering a missing rule, all decisions are supplied, a concrete analogue exists and decisive tests can reject wrong behavior. A two-line concurrency fix with hidden invariants does not qualify merely because it is small. Conversely, a long mechanical representation migration may qualify after semantic decisions and atomicity are owned elsewhere and verified.

Use Terra for familiar local implementation with a stable canonical owner and bounded state. Use Sol when inference spans repository conventions, failure propagation, multiple representations or shared state. Use Astra medium when new architecture/algorithms/compatibility must be reasoned about as a whole or prior source evidence demonstrates a lower tier cannot solve it. A security label alone is not such evidence.

Do not write a huge line-by-line plan just to make Luna viable: include planner/reviewer cost in routing evaluation. Do not split one invariant among agents to meet a cheap-profile rule.

## Cheap explorer

One bounded query: named entry point + requested owner/consumer/test map + exclusions. Reuse repository CodeGraph policy before grep/file exploration. The explorer cannot write code, rewrite the plan, call reviewers, declare scope complete, or choose product semantics.

Return a small map with path/symbol/line, commit identity, claim→evidence, unknowns and suggested next read. Ordinarily no more than eight source pointers; if this would hide necessary evidence, report truncation and request a targeted second query. This is a context budget, not a hard correctness cutoff. Main reads only decisive/uncertain boundaries rather than repeating the whole search. Skip delegation when direct reading is cheaper.

## Escalation

First classify a failed attempt: model/semantic error, plan/requirement error, environment/tooling error, or missing evidence. Only the first supports changing implementation models. One bounded under-routing attempt is enough to reconsider; do not exhaust a Luna→Terra→Sol→Astra ladder. Reassign only the unsolved root cause and preserve valid work.

Log actual selected profile, reason, requested/observed model+effort, context bytes, attempt and parent IDs, findings, repair model/time/tokens, validation/integration cost and user-discovered escapes. Never report a requested model as observed when the harness does not expose it.

Evaluate quality first, then total cost per accepted outcome including failed attempts. Use matched task families/oracle strength and repeated isolated replay only when separately authorized. Do not experiment on production just to collect data.

## Subsection selection

A parent may delegate different serial internal increments to different existing profiles when the interface permits it; neither model changes nor child labels reset repair or review history. Keep inseparable rules with one capable owner. Do not downgrade merely because a child has fewer lines. Parent synthesis/final review retains the whole contract and risk.
