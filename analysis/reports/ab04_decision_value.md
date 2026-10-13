# AB-04 Decision-value scoreboard across benchmarks, with the usefulness threshold

Ticket: AUD-36. Written 2026-10-13. No model calls.

Scripts:
- `analysis/decision_value_v2.py`: CausalArena, paired by file.
- `analysis/dv_chambers_sachs.py`: Causal Chambers and Sachs.
- `analysis/ab04_figures.py`: the figures.

Results are in `analysis/results/decision_value_v2/`.

## Where we are now

AUD-30 asked one question of each learned graph: "if I set T, does Y move?". This bundle asks it on five benchmarks:

- CausalArena semantic, formula and synthetic;
- Causal Chambers' light tunnel, with physical ground truth and real interventions;
- Sachs, whose consensus truth is weak.

It closes AUD-30's caveat: every baseline is now computed on exactly the files the method finished.

It also adds three measures:
- the replicate-agreement risk-coverage curve;
- DV-2 target choice;
- a stylised usefulness threshold.

## DV-1, released columns (precision of committed claims; baselines paired by file)

| Benchmark | Method | Coverage | Precision | Empty graph, same files | **Lift** | True CPDAG (ceiling) |
|---|---|---|---|---|---|---|
| CA semantic | PC, Causal-Copilot copy | 0.946 | 0.643 | 0.643 | **+0.000** | 1.000 |
| | PC upstream, default | 0.948 | 0.662 | 0.647 | +0.015 | 1.000 |
| | PC upstream, maxP | 0.937 | 0.712 | 0.647 | +0.065 | 1.000 |
| | GES (BIC) | 0.951 | 0.753 | 0.647 | +0.106 | 1.000 |
| | GIES with targets (D+I) | 1.000 | 0.753 | 0.643 | +0.110 | 1.000 |
| | FCI | 0.408 | 0.712 | 0.647 | +0.065 | 1.000 |
| | DirectLiNGAM / NOTEARS | 1.000 | 0.653 / 0.646 | 0.643 | +0.010 / +0.003 | 1.000 |
| CA formula | PC copy / upstream | 0.95 | 0.729 / 0.733 | 0.704 / 0.708 | +0.025 / +0.026 | 1.000 |
| | PC upstream, maxP | 0.946 | 0.760 | 0.708 | +0.053 | 1.000 |
| | GES (BIC) | 0.970 | 0.806 | 0.712 | +0.094 | 1.000 |
| | GIES with targets (D+I) | 1.000 | 0.851 | 0.704 | **+0.147** | 1.000 |
| | DirectLiNGAM / NOTEARS | 1.000 | 0.710 / 0.703 | 0.704 | +0.006 / −0.001 | 1.000 |
| CA synthetic (every variable a target) | PC copy / upstream | 0.92-0.94 | 0.630 / 0.646 | 0.756 / 0.748 | **−0.126 / −0.102** | 1.000 |
| | PC upstream, maxP | 0.928 | 0.745 | 0.746 | −0.001 | 1.000 |
| | GES (BIC) | 0.946 | 0.758 | 0.799 | −0.041 | 1.000 |
| | DirectLiNGAM / NOTEARS | 1.000 | 0.776 | 0.775 | +0.001 | 1.000 |
| Causal Chambers (light tunnel, 20 measured variables, 11 targets) | PC default | 0.990 | 0.841 | 0.813 | +0.027 | 1.000 at 0.990 coverage |
| | PC maxP | 0.928 | 0.887 | 0.813 | +0.073 | |
| | GES | 0.971 | 0.916 | 0.813 | **+0.103** | |
| | GIES with targets | 1.000 | 0.885 | 0.813 | +0.072 | |
| | DirectLiNGAM / NOTEARS | 1.000 | 0.871 / 0.813 | 0.813 | +0.057 / 0.000 | |
| Sachs (consensus, 11 variables) | PC / PC maxP / GES | 0.82-0.87 | 0.833 / 0.856 / 0.856 | 0.800 | +0.033 / +0.056 / +0.056 | 1.000 at 0.436 coverage |
| | DirectLiNGAM / NOTEARS | 1.000 | 0.773 / 0.782 | 0.800 | −0.027 / −0.018 | |

### Checks against real interventions (Causal Chambers only)

This is the share of committed claims that agree with a Welch test on the real interventional rows:

- true DAG: 0.928;
- GES: 0.961;
- GIES: 0.909;
- PC maxP: 0.912;
- empty graph: 0.857.

GES agrees with the physical interventions *more* than the true graph does. Some true effects are too weak to detect in 100 rows, which is the same pattern as BEN-09 on CausalArena.

## Predictions

These were written before the runs, in `plans/audit_dag.json`.

**P6.** At most two of the reproduced methods beat the empty graph by more than 0.05 on every benchmark. It is refuted if four or more do. "Reproduced methods" means rows that reproduce published methods: PC, GES/GIES, GIES with targets, LiNGAM and NOTEARS.

| Benchmark | Reproduced methods beating "nothing moves" by > 0.05 | P6 | Counting our variants too (PC maxP, FCI) |
|---|---|---|---|
| CA semantic | GES, GIES (2) | supported | 5: refuted |
| CA formula | GES, GIES (2) | supported | 4: refuted |
| CA synthetic | none | supported | 1 (FCI, at 13% coverage) |
| Causal Chambers | GES, GIES, LiNGAM (3) | **inconclusive** | 4 with PC maxP |
| Sachs | GES (1; +0.056) | supported, weak truth | 2 with PC maxP |

**P7.** The true-CPDAG ceiling exceeds the best method by at least 0.15 on every benchmark. It is refuted if the gap is under 0.05 anywhere.

| Benchmark | Gap to ceiling | P7 |
|---|---|---|
| semantic | 0.247 | supported |
| formula | 0.149 (GIES with targets) | inconclusive by 0.001 |
| synthetic | 0.224 | supported |
| Causal Chambers | 0.084 (GES) | **inconclusive** |
| Sachs | 0.144 | inconclusive; the ceiling commits on only 44% of pairs |

**Reading.** L3 ("most methods are within 0.05 of 'nothing moves' while the identifiable ceiling is at least 0.15 above the best") holds on CausalArena semantic and synthetic. It holds narrowly on formula. It does **not** hold cleanly on Causal Chambers, the one benchmark with physical truth: there, GES and GIES clear the empty graph by 0.07-0.10 and come within 0.08 of the ceiling.

L3 should therefore be stated as a CausalArena result with a physical-benchmark contrast, not as a field-wide law. This is the kill criterion's narrowing written in the DAG ("L3 becomes a CausalArena-specific note") in its partial form. Causal Chambers is a single 1,000-row file with a 20-variable measured graph, so its interval is wide.

## DV-2: choosing a target to move a named outcome

For each outcome Y moved by at least one target, the method picks uniformly among the targets it claims move Y.

| Benchmark | Method | Answers | Success when answering | Random target |
|---|---|---|---|---|
| semantic | GIES with targets / GES | 0.84 / 0.73 | 0.87 / 0.88 | 0.70 |
| semantic | PC upstream / PC maxP | 0.28 / 0.41 | 0.88 / 0.92 | 0.70 |
| formula | GIES with targets / GES | 0.93 / 0.76 | 0.88 / 0.83 | 0.59 |
| synthetic (every variable a target) | GES / PC upstream / PC maxP | 0.71 / 0.55 / 0.61 | 0.47 / 0.34 / 0.55 | 0.26-0.29 |

On CausalArena the released targets are mostly upstream variables, so a random target already succeeds 59-70% of the time. Methods gain 0.15-0.25 when they answer, but PC answers for only a quarter to two-fifths of outcomes. On synthetic, where every variable is a target, success when answering is 0.34-0.55.

## Usefulness threshold (stylised)

Acting on a "yes" claim gains g when right and costs c when wrong. Acting beats doing nothing (the empty graph) when precision_yes > c / (g + c). Value per pair relative to doing nothing, at c = g:

| Benchmark | Ceiling (true CPDAG) | Best method | Its value | Share of the ceiling's value captured |
|---|---|---|---|---|
| semantic | 0.328 | GIES with targets | 0.110 | 33% (GES 29%, PC maxP 16%, PC upstream 3%, PC copy below 0) |
| formula | 0.269 | GIES with targets | 0.148 | 55% (GES 32%, PC maxP 12%) |
| synthetic | 0.207 | FCI | 0.004 | 2%. GES, PC and PC copy are **below doing nothing** at c = g |

Clearing the threshold at c/g = 2 needs precision_yes above 0.67. On CausalArena:

- PC maxP and GES clear it on both semantic and formula;
- GIES with targets clears it on formula only (0.74; 0.66 on semantic).

At c/g = 4 (precision above 0.8), only near-silent methods (FCI) and the ceilings clear it on CausalArena. On Chambers, PC maxP, GES and LiNGAM clear it.

This is the practical version of "when does a tool become useful": on CausalArena, a learned graph is worth acting on only if wrong actions cost no more than about twice what right ones gain.

## Risk-coverage

`risk_coverage.png` ranks claims by replicate agreement, i.e. how many of a scenario's 5 independent files give the same claim. This is a stability score, not a calibrated probability. On semantic and formula, the most-agreed 10-20% of claims are 0.80-0.92 precise for GES and GIES, against 0.64-0.70 for the empty graph. Agreement therefore carries real signal, which is the input a calibrated abstention layer (BLD-05) would use. On synthetic, the curves for PC fall below the empty graph past 30% coverage.

`f1_vs_dv.png` plots controlled F1 against DV-1 lift. F1 orders methods only loosely by decision value:

- PC (default rule) reaches 0.40 F1 with a lift of −0.10 on synthetic;
- FCI reaches 0.32-0.37 F1 with the second-largest lift on formula.

## Gates and caveats

- **Claims checked against truth; baselines on exactly the files each method finished: met.**
- **Data-checked agreement** is reported only where interventions are physical (Chambers), with the true DAG's own agreement (0.928) as its ceiling.
- **Synthetic** has no released interventions: every variable is a target there, so its numbers are not directly comparable with semantic and formula.
- **Sachs** is a weak benchmark. Its consensus graph has no v-structures, so the CPDAG ceiling abstains on 56% of pairs, and the 853-row observational file has no interventions.
- **The usefulness threshold** is a stylised two-outcome decision, not a cost model of any real user. AB-10 interviews should supply real cost ratios.
