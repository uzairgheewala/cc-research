# Interventions as link evidence (L5), on dev

Tickets: TGT-18, TGT-19, CAP-03

Pre-registration `plans/l5_prereg.json`, hashed before any of its numbers existed
(`manifests/evidence/l5_prereg_2026-10-19.sha256`; the prereg's hash is unchanged since 20:41Z, before the first
collection). Code `analysis/q2_l5.py` (helpers tested in `tests/test_q2_l16_l5.py`); post hoc diagnosis
`analysis/q2_l5_diag.py` (not pre-registered, labelled as such). Results `analysis/results/q2_v3/l5_dev.json`,
`l5_diag_dev.json`, per-link rows `l5_links_dev.jsonl.gz`. Dev split only (125 obs_int files per family); no test split
read; no kernel change; no model calls. One verdict line was corrected after the first evaluation: P-L5-2 had been
judged on cross-fitted cuts (none), while the prediction is about the rule at any threshold; it is now judged on the
grid, which refutes it. The manifest pins the corrected code. Written 2026-10-19.

## Where we are now

Three levers have hit the same wall at 1,000 observational rows: nothing separates a shadow (a link that only stands for
a path through a third variable) from a real but weak direct link. An intervention is the one source that separates them
by construction: under do(t), a shadow t ... y through m shows no shift in y once m is held fixed; a direct link does.
The question was whether CausalArena's released interventions are enough to act on.

**No. The principle shows up in the data, but the release is too thin to act on.** Each semantic file intervenes on about
four of its 17-25 variables (three of them effective), with about 40 rows each. Formula intervenes on about six, and only
one of those visibly moves its own target. So interventions can reach 20% of semantic false links and 13% of formula's. The
marginal test has the power to detect a mediated effect only a third of the time. Every rule falls short of the bar.

## Results (regime D+I, cross-fitted by scenario)

### Reach

| | semantic | formula |
|---|---|---|
| Released targets per file / effective | 3.8 / 2.9 | 5.9 / 1.2 |
| Ledger links / false | 5,406 / 2,042 | 5,523 / 2,675 |
| Testable links (an effective target at one end) | 1,013 | 674 |
| Testable false links (share of all false) | 414 (20.3%) | 345 (12.9%) |
| of which shadow / common cause / unrelated | 182 / 81 / 151 | 170 / 86 / 89 |
| Missed true links / with an effective-target end | 1,756 / 246 | 1,517 / 109 |

### Rules

| Rule | semantic | formula | Licence |
|---|---|---|---|
| S cut shadow (moved, and not moved given the mediator) | at most 36 cuts at any tau (0.67 right at 0.05) | at most 21 (0.33) | no: never 30 cuts at 0.80 in training |
| N cut (two effective targets, neither moves the other) | at most 20 cuts (0.75) | 37 cuts at 0.65 (tau 0.05) | no |
| A add missed link t -> y | 450 candidates, 9% true; 155 adds at alpha 0.01, 11% true | 177, 9% true | no |
| Confirm (moved given the mediator) | 431 links, 78% true (base rate among testable 59%) | 142, 75% true (49%) | support only |

### Why (post hoc diagnosis, not pre-registered)

| Testable links, semantic | Tests | t is an ancestor of y | do(t) moves y | Moved when it should | Moved with a mediator found | ...then gone given the mediator |
|---|---|---|---|---|---|---|
| true | 630 | 521 | 326 | 62% | 184 | 12 (7%) |
| shadow | 182 | 175 | 59 | 34% | 48 | 23 (48%) |
| common cause | 88 | 0 | 1 | - | 1 | 1 |
| unrelated | 159 | 0 | 2 | - | 2 | 0 |

Formula reads the same with less power: shadows move 20% of the time when they should, true links 52%.

In plain words:
1. **The separating signal is real.** Among moved links with a mediator in the ledger, the shift disappears given the
   mediator for 48% of shadows and only 7% of true links.
2. **Power is the bottleneck.** About 40 rows per target detect a mediated effect in only a third of shadows. Two thirds of
   shadows never reach the conditional test.
3. **For common-cause and unrelated false links, the informative signal is "no shift".** That is ambiguous: a true link
   pointing into the target (y -> t) gives no shift either. Rule N resolves this only when both ends are effective targets
   (46 / 55 links). An exploratory rule, not pre-registered, cuts when the ledger claims t -> y and do(t) leaves y
   unmoved. It fires 239 / 117 times and is right 65% / 71% of the time, also below the bar.
4. **Rule A fails as predicted.** Its candidate mediators are ledger neighbours, and the ledger misses a third of true
   links, so a residual shift usually means a missed mediator rather than a missed direct link (9-14% true).
5. **Writing the unit test exposed one more failure mode.** The observational regression of y on m absorbs part of a
   direct effect of t into m's coefficient, because m and t are correlated. A moderate direct effect can then look like a
   shadow at 40 rows (7% of moved true links above).

The five replicates of a scenario intervene on the same targets. Pooling them would give about 200 rows per target, which
fixes power, but not reach.

## Predictions

| | Verdict |
|---|---|
| P-L5-0 reach >= 20% semantic, <= 10% formula | **Partly**: 20.3% semantic (met); formula 12.9% (above 10%, below the 20% refutation line) |
| P-L5-1 rule S earns a cut licence on semantic | **Refuted**: never 30 cuts at 0.80 (best 36 cuts at 0.67) |
| P-L5-2 rule N right >= 0.80 wherever it has >= 30 cuts | **Refuted**: formula 37 cuts at 0.65 (tau 0.05), 32 at 0.69 (tau 0.1) |
| P-L5-3 rule A earns no add licence | **Supported**: 9-14% of adds true |
| P-L5-4 confirmed links true >= 90% on semantic | **Refuted**: 78% (base rate 59%) |
| P-L5-5 a licensed rule raises DV-1 precision | Not tested: no licence |

## What this changes

- **L5: TRIED on CausalArena.** No licence, and the cause is located: the release has few targets and few rows per
  target, not a test that cannot separate. CausalArena's interventions cannot break the shadow wall at this budget.
- **Where L5 can be tested properly** is a dataset with dense, effective interventions and real mediated paths. Causal
  Chambers has the dense interventions (53 single-target regimes, 100 rows each, in the BEN-10 sample), but every edge of
  its graph runs input -> output (longest path 1), so it has no shadows: it can test rules N and X only. GSK CausalBench
  has hundreds of knockdowns over hundreds of thousands of cells and real regulatory chains, and BEN-13 is the first step
  there. A pooled-replicate L5 on CausalArena (about 200 rows per target) is the cheap check that separates power from
  reach.
- The confirm signal raises a testable link's chance of being true from 59% to 78%. That is information B4's confidence
  model does not use yet. It is recorded as a candidate feature, not acted on.

## Where we're going

The two cheap follow-ups are a pooled-replicate L5 on CausalArena (power) and rules N and X on the Causal Chambers
sample (dense targets, no shadows). Both are free compute. The pooled one needs a new cache fill (engines on 4,000-row tables), so it waits for Uzair's go-ahead on the order.
