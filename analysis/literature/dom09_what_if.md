# DOM-09: what is practical for "what if we set X?" at 20-40 variables

Tickets: DOM-09, BND-06, BLD-07

Retrieved 2026-10-12. Sources are the papers' own pages (links below); this note states what each method needs and returns.
Descriptions are from the papers' abstracts and our reading; no quotes are used.

## Methods

| Method | Input graph | Returns | Cost at 20-40 variables | Source |
|---|---|---|---|---|
| IDA (local) | CPDAG (PC / GES output) | for each (X, Y), the multiset of possible total effects, one per parent set of X allowed by the class; linear Gaussian | one regression per candidate parent set; cheap | Maathuis, Kalisch, Buehlmann, Ann. Statist. 37(6A), 2009; [arXiv 0810.4214](https://arxiv.org/abs/0810.4214) |
| Generalized adjustment criterion | CPDAG, MAG or PAG | whether an adjustment set exists for (X, Y) in the whole class (amenability), and all such sets | graph search; cheap at this size | Perkovic, Textor, Kalisch, Maathuis, JMLR 18, 2018; [jmlr.org/papers/v18/16-319](https://jmlr.org/papers/v18/16-319.html) |
| Optimal adjustment set | CPDAG (amenable pairs) | the adjustment set with the smallest asymptotic variance among valid ones, linear models | graph operations; cheap | Henckel, Perkovic, Maathuis, JRSSB 84(2), 2022; [arXiv 1907.02435](https://arxiv.org/abs/1907.02435) |
| LV-IDA (bounds with latent variables) | PAG (FCI output) | sets of possible effects that allow hidden common causes | grows with the number of circle marks around X | Malinsky and Spirtes, CMU technical report ([pdf](https://www.cmu.edu/dietrich/philosophy/docs/tech-reports/194_-malinsky.pdf)); title and venue not re-read in this pass |

What Causal-Copilot offers instead (AUD-12, `analysis/reports/bnd03/aud12_effect_estimation.md`): effect estimation is reachable
only from the web demo, and it treats `<->` and `o->` as parents when choosing confounders (inference.py:242-246). None of
the methods above is used.

## Timing on one 25-variable scenario

`analysis/dom09_ida_timing.py` -> `analysis/results/dom09/ida_timing.json`: local IDA on the CPDAG PC returned for
backup_frequency_ransomware_loss (semantic, dev split; 1,000 rows; 20 committed arrows, 6 undecided pairs).
- All 600 ordered pairs take 0.06 s in total on Uzair's machine; at most 2 candidate parent sets per X.
- 312 of 600 pairs (52%) have a single possible value within the class; the rest have two.
- The true parent set of X is among the candidates for only 7 of 25 variables: PC's skeleton misses true parents, so the
  class itself is wrong far more often than the class is ambiguous. On this benchmark, what-if accuracy is bounded by
  skeleton recall (BEN-04: skeleton recall 0.52 for PC on semantic), not by computation.

## Consequence for Q2 (BLD-07)

At 20-40 variables, computing what-if answers is not the obstacle; every method above runs in well under a second per
scenario. The useful output is the identification status per (X, Y) (identified, a small set of values, or not
identifiable), which the generalized adjustment criterion gives, plus IDA's multiset when it is not identified. Accuracy
depends on the graph; an evaluation should score effects against the SCM's interventional data (the obs+int files and
Causal Chambers interventions), not against regression on a recovered graph.
