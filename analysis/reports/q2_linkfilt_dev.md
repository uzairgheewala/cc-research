# Link filters: shadow ordering (L8) and resampling stability (L7), on dev

Pre-registration `plans/linkfilt_prereg.json`, hashed before its numbers existed
(`manifests/evidence/linkfilt_prereg_2026-10-16.sha256`). Code `kernel/linkfilt.py` (tested on a chain with its shadow:
`tests/test_q2_linkfilt.py`), `analysis/q2_linkfilt.py`; post hoc diagnosis `analysis/q2_linkfilt_diag.py` (not
pre-registered, labelled as such). Results `analysis/results/q2_v3/linkfilt*_dev.json`. Dev split only; no test split
read; no kernel change; no model calls. L7 needed 500 new resample engines (25 first-replicate dev files x 10 resamples x
2 families, B4's draws; 64 minutes on two cores). Written 2026-10-16.

## Where we are now

The question was whether a filter can withdraw the ledger's false links, above all its shadows, precisely enough to be
acted on (licence: cross-fitted cut precision >= 0.80 and at least 10% of false links cut). The headroom ladder put
removing false links at +0.03 answer precision, +0.12 coverage and +0.14 directed F1.

**Formula: yes, twice. Semantic: no.** Both filters earn a licence on formula and neither does on semantic, and the reason
is one structural fact about the two families, which the ledger cannot see.

## Results (regime D, cross-fitted by scenario)

| Filter | Family | Cut-offs chosen (5 folds) | Cuts | Cut precision | False links cut | True links lost | Licence |
|---|---|---|---|---|---|---|---|
| L8a triangle order, Spearman | semantic | none passes | 0 | (0.63-0.71 at every cut-off) | - | - | no |
| L8a | formula | 0.5-0.7 | 838 | **0.81** | **25%** | 5.6% | **yes** |
| L8b triangle order, mutual information | semantic | none passes | 0 | (0.64-0.68) | - | - | no |
| L8b | formula | 0.5 in 2 folds | 348 | 0.73 | 9% | 3.2% | no |
| L7 stability (25 files) | semantic | 0.3 in 4 folds | 28 | 0.75 | 5% | 1.0% | no |
| L7 | formula | 0.6-0.7 | 252 | **0.81** | **38%** | 8.4% | **yes** |
| L7 or L8a (secondary) | formula | | 333 | 0.78 | 49% | | (below the bar) |

What the licensed cuts remove (formula): L8a cuts 297 shadows, 96 common-cause and 284 unrelated false links, and 161
true; L7 cuts 104 shadows, 38 common-cause and 61 unrelated, and 49 true.

Answer level (graph with the cuts removed, no re-orientation):

| | DV-1 precision | Coverage | Directed F1 |
|---|---|---|---|
| formula, ledger -> L8a cuts (125 files) | 0.843 -> 0.852 | 0.755 -> 0.772 | 0.435 -> 0.446 |
| formula, ledger -> L7 cuts (25 files) | 0.847 -> 0.847 | 0.754 -> 0.830 | 0.430 -> 0.452 |

Cutting false links mostly turns abstentions into right "no" answers: coverage rises at equal or slightly higher
precision. Directions that relied on a cut link were left as they were, so a re-derived ledger could differ either way.

Stability: true links have median stability 1.0; shadows 0.7; common-cause 0.9 / 0.8; unrelated 0.6 / 0.5. A random
true link is more stable than a random false link 76% / 74% of the time.

## Predictions

| | Verdict |
|---|---|
| P-LF0 shadows sit in ledger triangles (>= 40%) | **Supported**: 82% / 83% |
| P-LF1 L8a earns no licence | **Refuted** on formula (0.81, 25%); held on semantic |
| P-LF2 mutual information as precise as Spearman (within 0.03) | **Refuted** on formula (0.73 vs 0.81); on semantic neither passes (0.68 vs 0.71 at the tightest cut-off) |
| P-LF3 stability separates true from false (AUC >= 0.70) | **Supported**: 0.76 / 0.74 |
| P-LF4 shadows more stable than unrelated false links (>= 0.10) | **Supported**: +0.10 (at the boundary) / +0.20 |
| P-LF5 L7 earns a licence somewhere | **Supported** (formula) |
| P-LF6 a licensed filter raises DV-1 precision and F1 by >= 0.01 | **Partly**: F1 +0.011 / +0.022 (met); DV-1 precision +0.009 / +0.000 (short of the claim, not lowered, so the refutation clause is not triggered); coverage +0.017 / +0.076 |

## Diagnosis: why semantic resists (post hoc)

At cut-off 0.7, L8a would cut 348 true semantic links. **288 of them (83%) sit in a real triangle**: a genuine direct link
next to a genuine path through a third variable, weaker than both links of the path. Cut precision is the same for
continuous, discrete and clamped pairs (0.62-0.69), so this is structure, not measurement. In the truth, 55% of semantic
links sit in a triangle against 35% of formula's: semantic scenarios are written with direct and mediated effects of the
same cause side by side, formula scenarios mostly as chains of formulas.

This is the same wall a third time. Conditional independence tests could not separate a shadow from a weak direct link;
pairwise direction signals failed where the conditioning sets (links) were wrong; and triangle ordering cannot separate
a shadow from a real direct link that is weaker than the path beside it.

## The open architectural question: a licence needs an observable condition

The licences hold per family, and a real dataset carries no family label. Through the ledger the two families look the
same: 68% vs 70% of found links in a triangle, mean degree 4.0 vs 4.0. The difference that matters (real triangles, 55%
vs 35%) is invisible. The ledger's triangle share predicts per-scenario cut precision only weakly (correlation 0.38;
0.34-0.41 within a family). So neither filter can be acted on in a family-agnostic kernel yet. Two ways forward, both
to be designed before anything is built:

1. An observable applicability condition, found and pre-registered on dev, then confirmed on a family with an unread
   split.
2. A declared one: a typed knowledge statement about the domain ("mechanisms are chains of formulas; few direct effects
   alongside mediated ones") that licenses the filter. That fits thesis T3 (knowledge decides what data cannot) without
   letting knowledge add or remove a link itself. The filter does the cutting; the statement only licenses it.

## What changes in the lever map

- L8: TRIED. Licence on formula (Spearman version); not on semantic; no observable condition yet.
- L7: TRIED (25 files per family). Licence on formula; not on semantic; same condition problem.
- L8b: TRIED, below L8a.
- New row: L16, applicability conditions for link filters (observable or declared). UNMEASURED.

## Where we're going

Before any of this enters the kernel: decide between an observable condition and a declared one. In parallel, the two
remaining link rows are cheap: the discrete-aware test on the 459 semantic floor misses (L2d), and interventions as link
evidence (L5), which is the one source that can tell a real direct link from a shadow by construction.
