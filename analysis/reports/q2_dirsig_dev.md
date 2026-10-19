# Direction signals that do not depend on colliders: two rounds on dev

Pre-registrations `plans/dirsig_prereg.json` (round 1) and `plans/dirsig2_prereg.json` (round 2), each hashed before its
numbers existed (`manifests/evidence/dirsig_prereg_2026-10-16.sha256`, `dirsig2_prereg_2026-10-16.sha256`). Code
`kernel/asym.py`, `kernel/asym_cond.py` (sign conventions tested on textbook cases: `tests/test_q2_asym.py`,
`tests/test_q2_asym_cond.py`), `analysis/q2_dirsig.py`, `q2_dirsig_diag.py`, `q2_dirsig2.py`. Results in
`analysis/results/q2_v3/dirsig*_dev.json`. Dev split only; no test split read; no kernel change; no model calls.
Written 2026-10-16.

## Where we are now

The question was whether a signal that reads direction from the shape of the data, rather than from collider patterns,
can point found links accurately enough to be acted on (a licence: 0.80 cross-fitted, on at least 10% of the links the
ledger leaves open). The headroom ladder put the prize at +0.05 answer precision and +0.06 F1 (reversed links), and
+0.15 coverage (open links).

**It cannot, on CausalArena at 1,000 rows.** Nine signals, two rounds, both families: no licence. At full yield they are
right 0.42-0.64 of the time. The diagnosis says why, and the reasons are classes, not tuning.

## Round 1: six pairwise signals (regime D, true found links)

| Signal | Semantic: all / top 10% by strength | Formula: all / top 10% | Licence |
|---|---|---|---|
| D4 linear non-Gaussian (entropy) | 0.52 / 0.49 | 0.50 / 0.39 | no |
| D5a additive noise (HSIC) | 0.55 / 0.56 | 0.50 / 0.56 | no |
| D5b regression error (RECI) | 0.57 / 0.46 | 0.61 / 0.68 | no |
| D5c information-geometric slope (IGCI) | 0.56 / 0.69 | 0.62 / 0.78 | no |
| D6 heteroscedastic noise | 0.57 / 0.50 | 0.60 / 0.63 | no |
| D10 conditional distribution similarity | 0.62 / 0.74 | 0.62 / 0.71 | no |

Where a signal confidently disagrees with a collider (top quarter), the collider is right 55-93% of the time.

Pooled replicates (5,000 rows): formula IGCI and D4 pass the licence rule (IGCI 131 of 153 acted links right, 0.86;
33 of 40 open links, 0.83; thresholds found in all five folds). The pre-registration asks for regime D, so this is a lead,
not a licence: 25 tables, 40 open links, Wilson lower end about 0.68 on the open ones. Semantic pooled: no pass.

### Predictions (round 1)

| | Verdict |
|---|---|
| P-DS1 no signal >= 0.80 without a threshold | **Supported** (best 0.69) |
| P-DS2 a licence in regime D | **Refuted** |
| P-DS3 nonlinear signals beat the linear one on continuous pairs | Supported, but all three are within 0.08 of a coin flip |
| P-DS4 more rows never lowers accuracy by more than 0.03 | **Supported** |
| P-DS5 colliders win confident disagreements | **Refuted by one cell**: formula pooled IGCI is right on 15 of 27; everywhere else the signal is right on 6-45% |

## Diagnosis: three failure classes (regime D, by property of the true child)

1. **Mass points.** When the child has at least 20% of its rows on one value (a clamp, a floor, zero inflation,
   a thresholded output), every signal is confidently wrong: semantic D4 0.04, D5a 0.24, D10 0.35 on 800 links (23% of
   true found links); formula 0.10-0.54 on 218. The signals read a mass point as "this is the cause".
2. **Other parents.** With one true parent, semantic D10 is 0.77 and D5a 0.70; with four or more, about 0.5. A pairwise
   signal treats every other parent as noise, and most children here have several.
3. **Mechanisms outside every model.** By the child's mechanism family (from the generator's execution plan),
   most signals do well on additive indices (0.78-0.82 for five of six), saturating responses and exogenous-looking
   children, and fail on count processes (0.38-0.55), thresholds (0.41-0.45 for four of six), measurement-error models
   (0.38-0.58), ratios and power laws (semantic).
   These families are most of the benchmark by design (its generator forbids mostly-additive mechanisms).

Where all assumptions hold (one parent, no mass point; 215 semantic links), D10 is 0.91 and D5a 0.85. The signals are
not broken; the benchmark sits outside their assumptions, and only the true graph tells us which links are inside.

## Round 2: the class fixes (gate on mass points; conditional signals; mass side)

| Signal | Semantic: ungated / gated / gated, 1 parent / gated, 2+ parents | Formula: same | Licence |
|---|---|---|---|
| D10 | 0.62 / 0.64 / 0.81 / 0.62 | 0.62 / 0.61 / 0.57 / 0.61 | no |
| D5a | 0.55 / 0.56 / 0.71 / 0.54 | 0.50 / 0.48 / 0.64 / 0.47 | no |
| C5a conditional additive noise | 0.55 / 0.58 / 0.77 / 0.55 | 0.47 / 0.42 / 0.54 / 0.41 | no |
| C6 conditional heteroscedastic | 0.51 / 0.50 / 0.64 / 0.48 | 0.42 / 0.37 / 0.48 / 0.36 | no |
| C5b conditional regression error | 0.60 / 0.62 / 0.51 / 0.63 | 0.62 / 0.65 / 0.52 / 0.66 | no (0.57 / 0.72 at 5-7% yield) |

The gate keeps 28% of semantic true found links and 72% of formula's. Of the 926 semantic links the ledger leaves
open, 227 pass it.

| Prediction | Verdict |
|---|---|
| P2-1 gating never lowers a round-1 signal by more than 0.02 | **Supported**; gains are 0.00-0.05 |
| P2-2 a licence in semantic D | **Refuted** |
| P2-3 no licence in formula D | **Supported** |
| P2-4 conditioning beats pairwise by >= 0.03 on multi-parent children | **Refuted**: +0.01 semantic, -0.07 formula |
| P2-5 the mass-point end is the child >= 75% | **Refuted, and reversed**: it is the child in 42% (semantic) / 35% (formula); the mass-point end is more often the parent (categorical and Bernoulli roots) |
| P2-6 gate reach 25-45% / 65-90% | **Supported** (28% / 72%) |

Why conditioning did not help: the conditioning sets come from the ledger, so they carry its errors. False neighbours
(shadows) and children hidden in open links enter the regression, and the six chosen by correlation miss the weak true
parents, which are exactly the ones the ledger misses. On formula, conditioning made the residual-dependence signals
worse than a coin (0.36-0.41): conditioning on undetected children reverses them.

## What this means for the architecture

- Direction errors are downstream of link errors in a second way. The collider route fails where links are wrong (fake
  colliders); the collider-free route fails where the conditioning sets, which are links, are wrong. Both point back to
  the skeleton.
- Route A for ER-4a through pairwise asymmetry is closed at 1,000 rows on this benchmark. The open direction sources are
  interventions (D7, used, with obs_int files on dev) and knowledge (D8, used at its measured size).
- One lead stays open: IGCI on pooled formula (0.86 on 153 acted links). It needs a family with an unread split before
  it can be acted on held out, and it is regime- and family-specific.
- Every one of these is now a measured row in `docs/design/q2_lever_map.md`, with the reason it does not carry a licence.

## Where we're going

The lever map's next rows are on links, which both rounds point back to: shadow ordering and resampling stability as
link filters, the discrete-aware test on the floor class, and interventions as link evidence.
