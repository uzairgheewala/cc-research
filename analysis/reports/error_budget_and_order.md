# Where the accuracy goes on CausalArena's public scenarios: ceilings, an error budget, and the value of order

Written 2026-10-07. Everything here is **measured** on the released files with no language model and no cost, by `analysis/error_budget.py`, `analysis/order_value.py`, `analysis/causalarena_sortability.py` and the earlier `causalarena_pc_calibration.py` / `causalarena_order_baseline.py`. Outputs: `analysis/results/error_budget/` and `analysis/results/causalarena_calibration/`. Scores are directed-edge F1 in the scoreboard's units; "published" means the benchmark's table over all 100 scenarios, of which 50 are public.

Terms. A *compelled* edge is one whose direction is the same in every graph that implies the same conditional independencies as the true graph; the rest are *undecided*. The *depth* of a variable is the length of the longest causal chain leading into it (inputs have depth 0).

## 1. Identifiability is not what limits scores here

A method that knew the true set of equivalent graphs exactly and oriented the undecided edges at random (the scoreboard's rule) would score (compelled + undecided / 2) / edges.

| Public family | Edges compelled | Ceiling, observational | Ceiling with the released intervention targets | Scenarios fully identified (obs / with interventions) | Best published |
|---|---|---|---|---|---|
| Semantic (50) | 91.8% | **0.957** (lowest scenario 0.844) | 0.974 | 6 / 13 of 50 | 0.634 |
| Formula (50) | 94.5% | **0.971** (lowest 0.897) | 0.993 | 12 / 33 of 50 | 0.524 |

Gate B1 (the equivalence-class routine equals the project's validated one on all 100 scenarios) and gate B2 (targets found in every interventional file) pass. The intervention figure is a lower bound: it uses only edges touching a target plus the standard propagation rules. Targets: 3.8 per semantic scenario on average, 69% of them inputs; 6.1 per formula scenario, 79% inputs.

**Correction to earlier text of mine.** I wrote that a 100% score on edge directions from observational data "is a sign of leakage". On these graphs the honest limit is about 0.96, not far below 1. The gap between the best published method (0.63) and the limit (0.96) is therefore almost entirely statistical and algorithmic. A score above the limit would still indicate outside information.

## 2. An error budget for plain PC (published configuration, 1,000 rows, public semantic)

| Hypothetical system | F1 | What was lost at this step |
|---|---|---|
| The true graph | 1.000 | |
| True equivalence class, undecided edges at random | 0.957 | identifiability: 0.04 |
| PC's own skeleton with every found edge oriented correctly | 0.611 | wrong skeleton: 0.35 |
| PC as scored | 0.335 | wrong or missing directions: 0.28 |

- Skeleton: precision 0.746, recall 0.522. PC misses about half the true connections.
- Directions: of the true connections PC found, 43.6% were directed correctly, 36.5% wrongly, 19.9% left undecided. **When PC commits to a direction it is right 54% of the time**, barely better than a coin, on graphs where 92% of directions are identifiable in principle.
- Which connections are missed (recall by number of causes of the effect variable): 1 cause 0.74, 2 causes 0.65, 3 causes 0.56, 4 causes 0.44, 5 causes 0.40, 6 or more 0.34. By mechanism family recall ranges from 0.42 (stock-and-flow) to 0.65 (linear); a single regression on the earlier columns finds 0.59-0.80 of the same edges. Reading (interpretation): the loss is mostly power, not exotic mechanisms. PC deletes an edge if any one of many conditioning sets makes the pair look independent, so variables with many causes offer many chances for a false deletion; a regression on candidate causes makes one joint decision per edge.

## 3. What knowledge of causal order is worth (oracle knowledge, taken from the true graph)

Each row gives the method a partial order of the variables as tiers, and nothing else. "PC re-oriented" keeps PC's skeleton and orients every connection between tiers earlier -> later. "Regression" regresses each variable on all variables in strictly earlier tiers (ordinary least squares, 1% level) and draws earlier -> later.

| Order knowledge given | Tiers (mean) | True edges it orders | PC re-oriented | Regression on earlier tiers |
|---|---|---|---|---|
| none | 1 | 0% | 0.335 | n/a |
| which variables are inputs (no cause in the system) | 2 | 45% | 0.470 | 0.386 |
| 3 depth bins | 3 | 53% | 0.468 | 0.399 |
| 5 depth bins | 5 | 73% | 0.524 | 0.535 |
| depth of every variable | 8.3 | 100% | 0.611 | **0.714** |
| (for comparison) the column order of the released files | 22.9 | 100% | n/a | 0.680 |

Published, same family: FoundCause 0.634, GIES 0.552, PC 0.333.

- Knowing only which variables are inputs lifts PC from 0.335 to 0.470.
- With the depth of each variable, a linear regression scores 0.714, above every published method. No published method was given this; the point is the size of the lever.
- The order is not sitting in the numbers in any easy form: R2-sortability (Reisach et al. 2023) is 0.57 on semantic and 0.60 on formula files (0.5 = no information), and the R2-SortnRegress baseline scores 0.314 and 0.287.

## 4. What follows

1. On this benchmark, at this sample size, accuracy is decided mainly by **where a method's knowledge of causal order comes from**. The three leak channels found so far are all order channels: column layout (total order, 0.680 for free), variable names (bundle 1: the language model writes 93% of the final edges when names are informative), and, for classical algorithms, fragile independence patterns (54% right).
2. A system has three legitimate sources of order: the numbers (hard: 54%), interventions (the released targets raise the ceiling only slightly, but each intervention reveals everything downstream of its target), and declared knowledge (for example "these variables are inputs", "this is a measurement of that"). The third is exactly what a language model reading names supplies, legitimately if it is declared and checkable, illegitimately if it is silent.
3. So the useful question for any causal-discovery system, agent or not, is: for each directed edge, which source supplied the direction? That is measurable from outside by controls (shuffle columns; neutralise or move names; withhold interventions) and can be made explicit inside a system.

## 5. Limits

- Public half only (50 of 100 scenarios per family); published numbers are over the full sets.
- The ceiling is for methods that use conditional independence. Methods that exploit the functional form of the mechanisms may identify more; none of the published ones is near the ceiling in any case.
- The order-value table uses oracle tiers. Who can supply such tiers correctly, and at what error rate, is not measured here.
- PC only. The same budget for GES, FCI and the pipeline's own choices is not yet computed.
