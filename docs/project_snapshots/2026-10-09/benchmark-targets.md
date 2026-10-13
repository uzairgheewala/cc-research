# Benchmark targets for the causal project

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

## Original note (2026-10-06, discussion draft; superseded where the update above says so)

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
