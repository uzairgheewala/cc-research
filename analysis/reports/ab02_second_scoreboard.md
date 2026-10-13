# AB-02 Second scoreboard: do the layout and conflict channels exist elsewhere?

Ticket: AUD-34 (also BEN-07). Updated 2026-10-13 with Bayesys. No model calls.

**Status: done.**

- **Reproduction gate: passed.** At the alpha the main runs used (0.05), 16 of 31 published PC-Stable and FCI cells reproduce within the pre-stated tolerance: 10 of 15 for PC and 6 of 16 for FCI. Three PC cells match exactly.
- **P3 is supported.**
- **P4 is inconclusive.**
- **New finding: Bayesys's own scoring is almost blind to column order.** Under its half-credit F1, shuffling the columns moves PC, maxP and FCI by at most 0.03. The layout leak exists in the files, but the published table does not reward it, because Bayesys never breaks ties by column index.
- **Engine exception:** causal-learn's GES on PROPERTY scores 0.07-0.09 lower on the released order than on shuffled orders.

## Where we are now

| Candidate | Released files + truth | Published per-method numbers | Status |
|---|---|---|---|
| **Bayesys** (Constantinou et al. 2021; CC BY-SA 4.0) | yes. `bayesys_datasets.zip`, sha256 `48f8bb32483428956fef56c7a379d7cdf0784c0819c9064aa69e490699907b1e`, downloaded by Uzair on 13 Oct | `results_noisyPaper.xlsx` (sha256 `8d49c693...6899`), downloaded by Uzair on 13 Oct | reproduced (gate passed); layout and re-score measured |
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
- maxP does not reduce the spread of the expectation-rule F1 across column orders (mean range 0.22 vs 0.26 on ASIA, 0.14 vs 0.13 on SPORTS). Most of that spread is the rule's coin flips, because each arm draws its own seed. The deterministic half-credit score below shows the true order effect, and it is close to zero.

So the conflict-rule channel is a CausalArena-scale effect and should not be claimed as universal.

## Reproduction against the published table (the gate)

**Producer and outputs.** `analysis/ab02_bayesys_repro.py`, writing `analysis/results/ab02/bayesys_repro.json` and `bayesys_repro_runs.jsonl`.

**What is compared.** The published side is `results_noisyPaper.xlsx`, Experiment N (no noise): PC-Stable, FCI and FGES from rcausal 1.1.1 (Tetrad). Our side is causal-learn 0.1.4.8 run on the released column order. Both use Bayesys's half-credit precision and recall: a true adjacency with the wrong or no orientation counts 0.5.

**Criteria**, written before any comparison was computed:

- A cell reproduces if |ΔF1| ≤ 0.05 and |Δedges| ≤ max(1, 10% of the true edges).
- The gate needs two PC-Stable or FCI cells to reproduce under one alpha.
- The workbook does not state an alpha, so two were declared up front: 0.05 (what the main runs used) and 0.01 (Tetrad's usual default). Having two alphas is a freedom, and it is stated here.

| Alpha | Cells compared | Reproduced | Median abs. ΔF1 |
|---|---|---|---|
| **0.05** | 31 | **16** (PC 10 of 15; FCI 6 of 16) | 0.048 |
| 0.01 | 31 | 10 | 0.082 |

**Gate: passed at alpha 0.05**, the setting the main runs already used, so no setting was chosen to fit.

- **PC.** Exact matches (same edge count, ΔF1 ≤ 0.001) on ASIA 0.1k, SPORTS 0.1k and SPORTS 10k. FORMED 0.1k is within 0.003.
- **FCI.** FCI matches less often (6 of 16). Our scoring turns PAG marks into committed or undecided pairs, and Bayesys's conversion is not documented.
- **GES against FGES** (reported, not part of the gate). Five cells match exactly: ASIA 1k and 10k; SPORTS 0.1k, 1k and 10k. ASIA 0.1k and ALARM 10k are also within tolerance.
- **Gaps.** PATHFINDER PC has no published value (recorded FAIL). PATHFINDER 1k and 10k were not run here for compute reasons.

### Re-score: what column order does to the published metric

The released-versus-shuffled difference in half-credit F1 is computed from `bayesys.json`, with five shuffled orders per cell:

| Method | Largest abs. change over 17 cells | Cells moving by more than 0.01 |
|---|---|---|
| PC (default rule) | 0.030 (PROPERTY 1k: released 0.566 vs shuffled 0.596; ASIA 10k: 0.500 vs 0.529) | 2 |
| maxP | 0.000 | 0 |
| FCI | 0.008 | 0 |
| GES (BDeu; ≤ 40 variables, so 12 cells) | **0.087** (PROPERTY 0.1k, 1k and 10k: released lower by 0.082, 0.073, 0.087) | 3 |

Two things follow from this table:

- **Bayesys's half-credit scoring removes the layout channel.** An undirected or reversed edge both earn 0.5, so how a method breaks ties barely matters. The published Bayesys rows are therefore not inflated by the topological column order of ASIA, SPORTS and PATHFINDER. This contrasts with CausalArena: there, the scoreboard's forced-choice rule rewards an index tie-break by up to +0.30 (AB-01).
- **The engine channel shows up instead.** causal-learn's GES is order-dependent on PROPERTY under this metric. That is an implementation property, the same class of defect as AB-03.

## gCastle alarm sets (unchanged)

Results are in `analysis/results/ab02/alarm_order.json`. The alarm ids are not in causal order: tau between −0.22 and 0.02, with an edge share of 0.45-0.73. PC was not reproduced (0.22-0.32 against a published 0.430), so by the gate there is no re-score claim on this benchmark.

## Gates

- **Reproduce before claiming anything about published numbers.**
  - gCastle: not reproduced, so no claim.
  - Bayesys: **passed** (16 of 31 cells at alpha 0.05; criteria stated above, before the comparison).
- **Every downloaded file has a sha256 recorded:** the Bayesys zip, the results workbook, and the alarm sets in `alarm_order.json`.

## What changes

- **L1, second scoreboard.** Settled, and narrower than hoped:
  - **The layout exists on Bayesys.** Three of six networks are released in topological order.
  - **Bayesys's metric does not reward the layout.** Under half credit, the published table moves by at most 0.03 when columns are shuffled.
  - **The scoring rule determines the effect.** The layout channel needs an index tie-break, which CausalArena's forced-choice scoring supplies and Bayesys's half credit does not.
  - **The engine channel (GES on PROPERTY, −0.07 to −0.09) shows on both benchmarks.**
- **Paper claim, scoped.** "Whether a benchmark's column layout inflates its leaderboard depends on its scoring rule. CausalArena's forced-choice rule rewards an index tie-break by up to +0.30 F1. Bayesys's half-credit rule is robust to it (≤ 0.03), though three of its six networks are released in topological order. Order-dependent engines move scores under both."
- **Recommendation to benchmark authors** (EXT-01): either shuffle the columns of released files or score with a rule that is invariant to tie-breaking.

## Where we're going

AB-02 is closed. Two things remain:

- **AB-16:** the L1 claim above goes into the wedge memo in its scoped form.
- **EXT-01:** the recommendation to benchmark authors is now backed by two benchmarks.
