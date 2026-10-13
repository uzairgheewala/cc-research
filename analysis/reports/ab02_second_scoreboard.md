# AB-02 Second scoreboard: do the layout and conflict channels exist elsewhere?

Ticket: AUD-34 (also BEN-07). Updated 2026-10-13 with Bayesys. No model calls.

**Status.** P3 is decided. P4 is mixed. The reproduction gate (two published Bayesys cells matched) is still open, because the published per-method scores (`results_noisyPaper.xlsx`) are not yet in `external/bayesys/`. Until then there is no claim about the published Bayesys numbers. Everything below compares our own runs on the released files.

## Where we are now

| Candidate | Released files + truth | Published per-method numbers | Status |
|---|---|---|---|
| **Bayesys** (Constantinou et al. 2021; CC BY-SA 4.0) | yes. `bayesys_datasets.zip`, sha256 `48f8bb32483428956fef56c7a379d7cdf0784c0819c9064aa69e490699907b1e`, downloaded by Uzair on 13 Oct | `results_noisyPaper.xlsx`, not yet downloaded | layout and re-score measured; reproduction **open** |
| **gCastle PCIC 2021 alarm** (MIT) | yes | README (PC, GES) | order measured (not causal); reproduction **not achieved**, so no claim |
| CIPCaD-Bench | partly | figure only | fallback, not needed |

## Bayesys: what was measured

**Data.** Six networks, using the Experiment 1 (no noise) training files at 0.1k, 1k and 10k rows as released. They are discrete and string valued, coded to integers in order of first appearance. The truth is each network's `GroundTruth.csv`.

**Methods.** All from causal-learn 0.1.4.8:

- PC (stable, G-squared, alpha 0.05), with the default collider rule and with maxP;
- FCI (G-squared; PAG marks: only tail-arrowhead counts as committed);
- GES with BDeu, on networks of at most 40 variables.

**Arms.** The released column order, and five shuffled orders.

**Producer and outputs.** `analysis/ab02_bayesys.py` writes `analysis/results/ab02/bayesys_runs.jsonl` (one line per run) and `bayesys.json`.

**Compute limits.** These are recorded, not findings.

- PATHFINDER (109 variables, some with 60+ states) was run at 0.1k for PC, maxP and FCI, and at 1k for PC only. PC took 740-770 s per run at 1k on our two shared CPUs. maxP exceeded the 900 s limit at 1k (one recorded timeout). 10k was not attempted.
- FORMED and PATHFINDER have no GES runs (more than 40 variables).

### Layout: the released column order (P3)

| Network | Variables | Edges | Share of true edges earlier column → later column | Kendall tau (column index, depth) |
|---|---|---|---|---|
| ASIA | 8 | 8 | **1.000** | **0.83** |
| SPORTS | 9 | 15 | **0.867** | **0.73** |
| PATHFINDER | 109 | 195 | **1.000** | 0.19 |
| FORMED | 88 | 138 | 0.674 | −0.07 |
| ALARM | 37 | 46 | 0.478 | 0.14 |
| PROPERTY | 27 | 31 | 0.452 | −0.22 |

**P3** (at least one release lists columns in an order correlated with causal order, tau > 0.3; refuted if all are below 0.1) is **supported**.

- **ASIA, SPORTS and PATHFINDER are released in a topological order.** Every true edge in ASIA and PATHFINDER runs from an earlier column to a later one.
- **PATHFINDER's tau is low only because it is shallow.** It has a single root, and 51 of 109 variables sit at depth 1, so depth barely varies, but its column order is still topological.
- **ALARM and PROPERTY are not ordered.** Their share is near 0.5.

### What an "earlier column → later column" rule is worth (descriptive)

This is the authors' index rule from CausalArena: undecided pairs are oriented from the earlier column to the later one. The gain is that rule on the released order, minus the expectation rule averaged over the five shuffled orders. It is averaged over sizes.

| Network | Share | PC | maxP | FCI | GES |
|---|---|---|---|---|---|
| ASIA | 1.000 | +0.21 | +0.21 | +0.30 | +0.11 |
| SPORTS | 0.867 | +0.11 | +0.15 | +0.21 | +0.05 |
| FORMED | 0.674 | +0.06 | +0.08 | +0.14 | n/a |
| PATHFINDER | 1.000 | +0.04 | +0.05 | +0.07 | n/a |
| ALARM | 0.478 | +0.04 | +0.03 | +0.00 | +0.01 |
| PROPERTY | 0.452 | +0.00 | +0.03 | −0.00 | −0.05 |

- **The gain tracks the layout.** Spearman rho between share and the mean gain over the six networks is +0.75 (p 0.08; six points, descriptive).
- **PATHFINDER's gain is small in absolute terms** because the skeleton is small at these sizes (F1 0.04-0.12). Relative to the shuffled score, the gain at 0.1k is +67% (PC) to +137% (maxP).

**What this means for L1.** The layout channel exists on a second, widely used benchmark. Any pipeline that breaks ties by column index, or is order dependent, gets a free +0.04 to +0.30 on the topologically ordered Bayesys networks, and nothing on the others. This was measured with our engines, not against the published table.

### PC's conflict rule under the released order (P4)

**What we measured.** q is the share of committed arrows on true adjacencies that point the right way. The gap is q averaged over the shuffled orders minus q on the released order, with PC's default rule. We measured it on the three networks whose columns follow causal order.

| Network | 0.1k | 1k | 10k |
|---|---|---|---|
| ASIA | n/a (no committed arrow on a true edge) | 0.00 | **+0.20** (released: 2 committed arrows, 1 right) |
| SPORTS | 0.00 | 0.00 | 0.00 |
| PATHFINDER | +0.05 | −0.03 (released better) | not run |

**P4** (the effect appears wherever columns follow causal order; refuted if |Δq| < 0.03 there) is **inconclusive: it appears on 2 of 3 networks.** SPORTS shows no gap at any size. The ASIA gap rests on two committed arrows. On PATHFINDER the gap is +0.05 at 0.1k and reverses at 1k (−0.03).

The first version of the summariser averaged all cells (mean 0.032) and would have said "supported". That reading does not match the wording in `plans/audit_dag.json` ("wherever"). The verdict now follows the wording, and both numbers are kept in `bayesys.json`.

**Why the two scoreboards differ.** The conflict-rule effect is much weaker here than on CausalArena (AB-01). Two reasons:

- The Bayesys networks are small or shallow, so PC commits few arrows (2-9 on ASIA and SPORTS).
- maxP does not reduce the spread across column orders here. The mean range over five orders is 0.22 vs 0.26 on ASIA and 0.14 vs 0.13 on SPORTS. This range also contains the expectation rule's coin flips.

So the conflict-rule channel is a CausalArena-scale effect and should not be claimed as universal.

## gCastle alarm sets (unchanged)

Results are in `analysis/results/ab02/alarm_order.json`. The alarm ids are not in causal order: tau between −0.22 and 0.02, with an edge share of 0.45-0.73. PC was not reproduced (0.22-0.32 against a published 0.430), so by the gate there is no re-score claim on this benchmark.

## Gates

- **Reproduce before claiming anything about published numbers.**
  - gCastle: not reproduced, so no claim.
  - Bayesys: open until `results_noisyPaper.xlsx` is in `external/bayesys/`. The gate is that our PC and FCI match two published cells within the paper's reported spread. Bayesys's published F1 gives half credit to a wrongly oriented or undirected true adjacency, and we report that measure next to ours (`F1_bayesys_half_credit`). Bayesys used Tetrad's PC-Stable and FCI, while we use causal-learn's. If the gate fails, the layout table above still stands, because it is a property of the released files, not of a score.
- **Every downloaded file has a sha256 recorded** (the Bayesys zip above; the alarm sets in `alarm_order.json`).

## What changes

- **L1, second scoreboard.**
  - The layout channel is confirmed on Bayesys: three of six networks are released in topological order, and an index rule gains up to +0.30 there and nothing elsewhere.
  - The conflict-rule channel is not confirmed outside CausalArena.
  - The engine channel (AB-03) does not depend on any benchmark.
- **Paper claim, scoped.** "Two public structure-learning benchmarks release columns in causal order for some or all graphs. A tie-break by column index, or an order-dependent method, is rewarded there." The claim about the published Bayesys numbers waits for the reproduction.

## Where we're going

When `results_noisyPaper.xlsx` is in place, `ab02_bayesys.py` gets a `--published` reader. It will compare our released-order PC-Stable and FCI cells with the published ones. If the gate passes, the table is re-scored with the index rule and with shuffling.
