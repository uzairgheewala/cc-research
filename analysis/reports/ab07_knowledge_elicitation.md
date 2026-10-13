# AB-07 Knowledge elicitation (A3): what can a model supply when it reads only names?

Ticket: AUD-48 (DEC-02 approved). Run 2026-10-13 by Uzair (`cc.ps1 tiers a3_tiers_requests.jsonl`).

The run made 914 calls on gpt-4o-2024-08-06: 900 requests, 18 invalid replies retried, and 4 abstentions. Token use was 212,572 prompt and 154,713 completion, about $2.08 at list price.

The pre-registration is `plans/a3_prereg.json`. The request file's sha256 matched it, and the scorer and thresholds were fixed before the calls.

- Scorer: `analysis/a3_score.py`, writing `analysis/results/a3/a3.json`.
- Exploratory follow-up, not pre-registered: `analysis/a3_orient_only.py`, writing `analysis/results/a3/a3_orient_only.json`.

## Where we are now

The model was shown only variable names, in random order. It was asked to sort them into causal tiers, from inputs to outcomes. This was done for:

- 50 public semantic scenarios and 50 public formula scenarios;
- three phrasings of the request;
- three name arms: real names, neutral names (V01..Vd) and moved names (real names permuted across variables).

## Pre-registered verdicts (consensus tiers over the three phrasings)

| | Claim | Threshold (support / refute) | Measured | Verdict |
|---|---|---|---|---|
| O1 | Real names order true edges correctly (semantic) | ≥ 70% correct and ≤ 10% contradicted / < 50% or > 25% | **69.4% correct, 12.1% contradicted**, 18.5% tied | **inconclusive** (just short on both) |
| O2 | Neutral names supply nothing | correct − contradicted ≤ 0.05 / > 0.15 | 0.000: the model puts every variable in one tier | **supported** |
| O3 | Moved names: the tiers follow the labels | by label as O1; by data, correct − contradicted ≤ 0.05 | by label 72.1% / 11.2%; by data −0.047 | **supported by data; by label inconclusive**, the same as O1 |
| O4 | Regression on the model's tiers reaches 0.634 (semantic) | ≥ 0.634 / ≤ 0.50 | **0.448** | **refuted** |
| O5 | The same on formula against 0.524 | ≥ 0.524 / ≤ 0.40 | **0.384** | **refuted** |

On formula, the real arm gives 70.4% correct and 13.1% contradicted. The dev and test halves agree within 0.04 on every figure.

Per phrasing, correct is 0.60-0.66 and contradicted 0.115-0.116 on semantic. The consensus over phrasings adds 3-9 points of correct order.

## What the numbers say

1. **The model knows the order the names suggest, and follows the names, not the data.**
   - With real names it orders 69-70% of true edges correctly and contradicts 12-13%.
   - With moved names the same answers score 72% "correct" against the labels' graph. Against the data they score worse than chance: 39% correct, 44% contradicted.
   - With neutral names it declines to order at all.

   This is name reliance measured directly, without any agent pipeline in between.
2. **Name knowledge alone does not beat data.** Regressing each variable on the variables in earlier tiers gives 0.448 (semantic) and 0.384 (formula). This is below GES on data alone (0.528 and 0.470). With oracle depth tiers, the same regression gives 0.714 and 0.615. The gap comes from the 18% of true edges the model leaves tied, which the regression cannot recover, and the 12% it contradicts.
3. **Used the way the ledger would use it, the knowledge helps, and wrong knowledge does bounded harm.** This analysis is exploratory and post hoc. Tiers may orient adjacencies a data method already found, but may never add or remove one.

| Semantic | Data only | + model tiers (orient only) | + oracle depth | + moved tiers (wrong knowledge) |
|---|---|---|---|---|
| PC, default rule: F1 / DV-1 precision | 0.356 / 0.662 | **0.485** / 0.716 | 0.613 / 0.762 | 0.301 / 0.653 |
| PC, maxP | 0.462 / 0.712 | 0.507 / 0.728 | 0.613 / 0.763 | 0.317 / 0.657 |
| GES (BIC) | 0.528 / 0.753 | **0.546** / **0.784** | 0.658 / 0.862 | 0.342 / 0.643 |

| Formula | Data only | + model tiers | + oracle depth | + moved tiers |
|---|---|---|---|---|
| PC, default rule | 0.298 / 0.733 | 0.427 / 0.765 | 0.541 / 0.797 | 0.247 / 0.714 |
| GES (BIC) | 0.467 / 0.806 | 0.510 / 0.821 | 0.603 / 0.900 | 0.318 / 0.698 |

- **Gains.** GES plus the model's tiers reaches 0.546 on semantic, against the published GIES at 0.552 and FoundCause at 0.634. On formula it reaches 0.510. Its decision-value precision rises from 0.753 to 0.784.
- **Ceiling.** Oracle tiers on the same skeleton reach 0.66, so the skeleton, not the orientation, now limits the score.
- **Harm.** Wrong knowledge (moved names) costs GES 0.19 F1 and 0.11 decision-value precision. The loss is bounded, because no connection was added (AB-09, T3). It is still large, which is the case for recording each direction's source and checking it against interventions (V4).

## What changes

- **L2.** Name reliance is now shown at the knowledge-supply level. With moved names the model's order follows the labels: its correct-minus-contradicted score is +0.61 against the labels and −0.05 against the data. This is independent of any agent's pipeline and holds on both families.
- **L4.** "Knowledge as tiers, never edges" is a real but modest lever with this model:
  - +0.02 to +0.04 F1 on GES;
  - +0.13 on PC with the default rule, mostly by repairing PC's conflict-rule errors;
  - +0.03 decision-value precision.

  It does not reach the best published semantic number. What the ledger would add over these numbers is the per-claim source, so that "+ moved tiers" is detectable rather than silent.
- **Tickets.** RQ-10..14 are answered:
  - RQ-10: no, narrowly (69.4% correct, 12.1% contradicted);
  - RQ-11: yes;
  - RQ-12: yes, by data;
  - RQ-13: no;
  - RQ-14: no.

  CAP-04, BLD-04 and TGT-07 are unblocked.
