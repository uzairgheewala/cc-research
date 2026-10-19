# Benchmark targets for the causal project

## Update 2026-10-19: GSK CausalBench revisited (role changed, verdict on the leaderboard unchanged)

Read in chat on 19 Oct from the primary sources (CausalBench, Communications Biology 2025; CausalBench Challenge report, CLeaR 2025 / arXiv 2308.15395; Large Perturbation Model, GSK, arXiv 2503.23535). Numbers are as printed in those papers; nothing here was run by us. Dev ticket: BEN-13.

- **Verdict on the 6 Oct note stands for the leaderboard.** As a board to top with Causal-Copilot as it is, CausalBench is still the wrong target: no interventional path at genome scale, PC/FCI/GES do not scale there, and the winners are per-pair statistics that need no agent.
- **New role: the scale-and-interventions leg for the ledger (Rung 3 below), and the large real testbed for lever L5.** The lever map's recurring wall (nothing at 1,000 rows separates a mediated shadow from a weak direct link) is the same open problem the CausalBench organizers name (their metric cannot separate direct from indirect effects). Interventions are the one source that separates them by construction; CausalBench is where that is tested at scale on real knockdowns.

### Current bar (full intervention set; mean Wasserstein higher is better, FOR lower is better; trade-off set by edge budget)
| Cell line | Best Wasserstein | Best FOR | Balanced point |
|---|---|---|---|
| K562 | 0.590 MeanDifference top-1k (FOR 0.170) | 0.126 GRNBoost (W 0.133) | MeanDifference top-5k 0.442 / 0.143; Guanlab top-5k 0.386 / 0.138 |
| RPE1 | 0.712 MeanDifference top-1k (FOR 0.122) | 0.072 Guanlab top-5k (W 0.350) | MeanDifference top-5k 0.384 / 0.078 |
- Biological evaluation (CORUM/STRING F1): Guanlab top-5k 0.223 K562 / 0.257 RPE1 (Communications Biology table 1).
- 50% interventions (LPM paper, table 4): LPM+Guanlab FOR 0.150 K562 / 0.087 RPE1 (best), W 0.318 / 0.274. Its "NoPerturb+Guanlab" control reaches FOR 0.161 / 0.091.
- 25% interventions: SparseRC (the only identifiability-grounded entry) ranks much higher than at 100%.
- Run time: BetterBoost ~12 h, Guanlab top-1k ~3 h on K562 (wall clock, as published).

### Shortcut channels (our reading; to be measured by BEN-13)
1. **Metric echo.** MeanDifference ranks pairs by the perturbed-vs-control shift; the Wasserstein metric scores the same shift on held-out cells. Topping it tests replication of total effects, not a graph.
2. **Edge placement.** On RPE1 the no-change imputation control gets FOR 0.091 vs LPM's 0.087; part of the FOR gain may come from spreading edges onto unperturbed genes, not from learned biology.
3. **Name recall on the biological metric.** CORUM/STRING reward known co-membership; CATRAN scores well there via co-expression (organizers' attribution). An LLM reading gene names would gain there without data. The statistical metric is immune to names; the biological one is not. Same recall-vs-reasoning contrast as our label-shuffle test.
4. **No direct/indirect separation** (organizers' own caveat).

### Landmark rungs
- **Rung 1, leaderboard (necessary, not sufficient).** One frozen method, one edge budget, both lines: K562 W > 0.442 at FOR <= 0.143; RPE1 W > 0.384 at FOR <= 0.078; at 50% interventions FOR below 0.150 / 0.087 without losing W. Reachable by per-pair statistics.
- **Rung 2, the organizers' open problems.** Effects for genes whose knockdowns were withheld (scored on those knockdowns), and a demonstrated direct-vs-mediated separation (needs a new test, likely combinatorial knockdowns), while staying on the Rung 1 frontier. Main-track method claim if principled.
- **Rung 3, reliability (our angle).** Every pair typed by evidence (knockdown + held-out replication / co-expression / name or literature recall); each type's held-out hit rate matches its stated confidence; a gene-label shuffle shows which part of each score depends on names. No entry reports this.

### How it combines with the other targets
- CausalArena under controls: names and column order. Causal Chambers: experimentally validated truth (guards against LLM-drafted references). CausalBench: scale, real interventions, recall-immune statistical metric. One frozen system clearing all three is the cross-benchmark claim; CausalMan / PetShop add the buyer story (RCA).
- Build cost: Causal-Copilot has no interventional path and does not scale to thousands of genes; the kernel's B2 shift test (Welch, single-target rows) is the small-scale version of the winning principle. A small development gene subset is needed to keep iteration time low.

### First step (BEN-13, no new engine)
Reproduce two published rows per cell line; re-score with (a) the edge-placement control and (b) a names-only baseline on both metrics under a gene-label permutation; report how much of each published score each shortcut channel accounts for. Data download and long runs on Uzair's machine (sandbox egress blocks the data host).

---

## Update 2026-10-07: what was measured on the fetched CausalArena release

The CausalArena dataset snapshot is now on Uzair's machine (`cc-research/external/causalarena/`). Facts read from the files and measured on them; details in `cc-research/analysis/reports/bundle1_results.md` section 7.

- **What is public.** Half of each generated family: 500 synthetic configurations, 50 "semantic" scenarios (10 domains x 5, 17-25 variables, 26-67 edges), 50 formula scenarios; 5 replicate sample files per scenario and regime (observational 1,000 rows; observational + interventional 800 + 200). Published tables average over 100 semantic scenarios; no per-scenario results. Real tables are indexed, not republished.
- **Correction.** Of the four repo datasets used in bundle 1, three match a CausalArena real-data entry in size (Abalone, Concrete, Deutscher Wetterdienst). Auto MPG does not (CausalArena: 4 variables, 3 edges, 398 rows; repo: 5, 5, 392). Earlier text saying "four" is wrong.
- **Numbers to compare with, semantic observational (directed-edge F1, full set):** FoundCause 0.634, GIES 0.552, CDFM 0.434, TabCausal 0.422, PC 0.333, random-order regression 0.252. Real data: 0.391 observational (CDFM, 13 datasets), 0.462 with interventions (TabCausal, 7 datasets).
- **Scoring rule (paper, Appendix B).** Directed-edge F1; for PC and GIES undirected edges are oriented at random with a per-file seed. PC is stable PC, Fisher-z, alpha 0.05. Our scorer reproduces the published PC F1 on the public half (0.335 against 0.333). SHD does not reproduce (37.5 against 33.5); do not compare SHD yet.
- **Column order leak.** In every released sample file checked, every true edge runs from an earlier column to a later column (semantic 2,068 of 2,068; formula 1,714 of 1,714; synthetic 50,421 of 50,421). A naive regression on earlier columns scores 0.680 on the public semantic files and 0.575 on formula, above every published row; 0.269 and 0.215 after a seeded column shuffle. Not shown: that any published method used the order. Consequence: column order is a leak channel next to names; every evaluation of ours shuffles columns. Whether to tell the maintainers is Uzair's decision.
- **What "beating the benchmark" now means.** A top score on the released files can be had by reading the layout, and (bundle 1) on small named datasets by reading the names. A defensible result is a score reported under controls that remove both, with the contribution of each source shown.
- **Targets, revised.** Primary: CausalArena public semantic scenarios (released data, published baselines, validator, submission route). Secondary: its obs+int files (published methods gain only +0.02 to +0.04 from interventions) and Causal Chambers (archives not yet downloaded; the benchmark's authors report PC timing out there; their sample is not republished, so only our own stated sampling is possible).

---

## Original note (2026-10-06, discussion draft; superseded where the updates above say so)

Answers Uzair's question: what is CausalBench, is there a benchmark to break or beat, what would 100% mean, and how the existing system could get there. Sources were read through a summarising fetch tool; check numbers against the PDFs before quoting. No decision recorded.

### Two different things are called CausalBench
- GSK CausalBench (Chevalley et al., arXiv 2210.17283): gene-network inference from single-cell CRISPR perturbation data. Two cell lines, K562 (162,751 cells, 622 intervened genes) and RPE1 (162,733 cells, 383 intervened genes). A method outputs a list of directed gene pairs. There is NO ground-truth graph. Scoring: (a) statistical, on held-out interventional data: mean Wasserstein distance between a predicted child's distribution with and without intervention on the predicted parent (higher is better), and false omission rate (lower is better); (b) biological: precision/recall against CORUM and STRING. Findings: most classical methods do not scale; methods given interventional data did not beat observational ones.
- CausalBench challenge 2023 (arXiv 2308.15395): winners were simple and non-graphical: mean difference between perturbed and control cells, a LightGBM pair classifier, GRNBoost plus a KS test. Authors' own caveat: the Wasserstein metric does not separate direct from indirect effects.
- A separate "CausalBench" (arXiv 2404.06349) tests LLM causal-learning ability on standard graphs. Not read in detail.

### What "100%" would mean
- On GSK CausalBench there is no 100%: no truth graph, two metrics that trade off. Topping it means estimating total intervention effects at scale, which is closer to differential-expression statistics than to causal discovery.
- Its biological metric scores agreement with literature-derived databases, so a model that recalls gene interactions from names would score well there without using the data. Its statistical metric uses held-out interventions and cannot be gamed by names. That contrast is the same recall-versus-reasoning point as our label-shuffle test.
- In general, 100% directed-edge accuracy from observational data alone is above the identifiability ceiling. It is legitimately reachable only where every variable can be intervened on or strong assumptions hold; otherwise it signals leakage or recall.

### Why GSK CausalBench is the wrong target for Causal-Copilot
- Scale: hundreds to thousands of genes; the PC/FCI/GES family it selects does not scale there (CausalSteward already reports Causal-Copilot at F1 0.078 on 53 nodes and 0.014 on 186).
- Causal-Copilot has no wrapper that uses interventional data, apart from CD-NOD through a domain index.
- The winning recipe does not need an agent.

### Better targets
| Benchmark | Truth | Size | State of the art (as read) | Fit |
|---|---|---|---|---|
| CausalArena (arXiv 2609.11897, Sept 2026) | synthetic, "semantic" and formula-based structural models, plus real data (Sachs, Causal Chambers, PetShop, six CD-CSG sets incl. Abalone, Auto MPG, DWD, Ozone) | small to medium | best directed-edge F1 by regime 0.39-0.63; real data 0.39 observational, 0.46 with interventions; 18 methods, no LLMs and no agents; no relabelling test; DAG-level directed scoring | Best scoreboard to place Causal-Copilot and a fixed variant on. Also a novelty threat to "yet another benchmark": build on it, do not duplicate it |
| Causal Chambers (arXiv 2404.11341) | physical devices; graph validated by randomised experiments | 32 and 41 variables | GES gets linear effects, misses nonlinear ones; PCMCI+ low recall | Right size; real truth; interventions available; names are physical quantities, so legitimate knowledge could help and the shuffle test can tell |
| CausalRivers (arXiv 2503.17452) | river network, 1000+ nodes, time series | large | simple baselines match or beat causal methods | Time-series only; lower priority |
| CausalMan (via CausalSteward) | simulated manufacturing | 53 and 186 nodes | Causal-Copilot F1 0.078 / 0.014 | A known weak spot to improve on |
| Sachs | contested reference | 11 | memorised | Use only with name controls |

### Path from the existing system
1. Place the unmodified pipeline on CausalArena's real-data and semantic slices plus Causal Chambers, scoring each stage, with original / neutral / shuffled names. (Harness and lineage tools exist; needs dataset adapters.)
2. Refinement that is never worse than its algorithm: keep stable non-directed edges, score against the equivalence class as well as the DAG.
3. LLM consulted only on adjacent-but-unoriented pairs, answers labelled, accepted only if they survive the shuffle test and agreement across prompts.
4. An interventional path (currently absent): use intervention experiments to orient and to check edges, and report a held-out-intervention score in the CausalBench style, which is immune to name recall.
Numbers to beat, as read: CausalArena real data 0.39 (observational) and 0.46 (with interventions) directed-edge F1. Whether a fixed Causal-Copilot reaches them is unknown.

### Positioning consequence
CausalArena narrows shape A (pure evaluation paper). What it lacks, by its own description, is agents, a relabelling control, and stage attribution. Shape B should use CausalArena's suites as the dataset pool and contribute those three things plus the fix.
