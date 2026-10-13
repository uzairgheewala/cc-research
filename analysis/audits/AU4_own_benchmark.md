# AU4: a benchmark of our own

Tickets: AUD-21, STR-02, EVL-02
Written 2026-10-12 by an audit agent; sources read on that date.

**Where we are now:** this is a desk audit. It extends the earlier notes cluster8, cluster9, cluster2, cluster7, dom07, dom08 and dom10 and does not redo them. Typed table: 20 requirement rows, in `AU4_own_benchmark.json`. Effort figures are **our estimates**. Numbers are labelled as follows:
- `measured (ours)`: from audit_context.md. These were not re-verified here.
- `reported`: from the authors' own page.
- `via prior note X`: read in an earlier project note and not re-opened today.

---

## 1. Question

What would a benchmark need in order to measure three things without the leaks known in existing benchmarks?
- **(a) Order provenance:** where a system's edge directions come from (data, interventions, names or knowledge, or column layout).
- **(b) Calibration:** whether its claims are calibrated and whether it can abstain.
- **(c) Decision value:** whether better graphs lead to better decisions (effects, choice of experiments).

We also ask which designs already exist or have been proposed, and what building one would cost.

## 2. Method

**Starting point.** We began from the seven earlier notes above. We then ran 22 web searches (listed at the end) and opened 45 primary pages: arXiv abs or HTML pages, proceedings pages, GitHub and Hugging Face pages, and CRAN pages.

**Inclusion rule.** A source was included if it does at least one of these:
- documents a benchmark artefact or leak;
- proposes an evaluation protocol, metric or checklist for causal discovery;
- supplies ground truth from physics, a simulator or experiments;
- implements an LLM-specific control;
- scores calibration, abstention, interventional prediction or experiment choice.

**Caveat.** All reads went through a fetch tool that summarises pages. Re-check exact numbers against the PDFs before quoting them in the paper.

## 3. Findings

### 3.1 Known leaks and artefacts, and who is exposed

| Pitfall | Evidence (source, read 2026-10-12 unless marked) | Benchmarks exposed |
|---|---|---|
| **Varsortability** | Marginal variance tends to rise along the causal order in generic ANMs. A sort-and-regress baseline matches continuous methods, and those methods fail on standardised data. Standardising leaves an exploitable covariance pattern. ([Reisach et al. 2021](https://arxiv.org/abs/2102.13647); NeurIPS 2021 per prior note cluster8, not re-verified) | Most ER/SF ANM suites |
| **R2-sortability** | R2 is scale-invariant, so standardising does not remove this shortcut. R2-SortnRegress can match or beat established methods. The authors want R2-sortability made an explicit assumption, because "its prevalence in real-world data is unknown". ([Reisach et al. 2023](https://arxiv.org/abs/2303.18211)) | Standardised synthetic suites |
| **Standardisation fix** | iSCMs standardise inside generation. They are not var-sortable by construction and are mostly not R2-sortable. ([Ormaniec et al.](https://arxiv.org/abs/2406.11601)) | n/a (this is a remedy) |
| **Scale / units** | NOTEARS lacks scale-invariance: rescaling, for example metres to centimetres, can largely alter the graph. ([Kaiser & Sipos](https://arxiv.org/abs/2104.05441)) | Any suite with arbitrary units |
| **Column order** | Variable order can matter more than sample size or hyperparameters. ([Kitson & Constantinou](https://arxiv.org/abs/2206.08952)) Reported via prior note cluster8: worst-to-best order moves hill-climbing F1 by 0.412, versus 0.161 for a 100x sample increase. Measured (ours): an index-order regression scores 0.680 on CausalArena semantic files and 0.269 when columns are shuffled. | **CausalArena.** Columns follow `node_order`, which was topological in the scenarios we checked. The replay sampler has no shuffle. The "liberal" rule orients undecided edges from the smaller to the larger index (prior note dom07; [TabCausal code](https://github.com/LAMDA-Tabular/TabCausal)). |
| **LLM-written graphs** | CausalArena's semantic and formula SCMs come from a "staged agentic construction workflow" with "Human and LLM-assisted review". Quality was checked with an "LLM-judge quality rubric" on 20 scenarios (3.80 to 4.48). Nodes are "labeled by what they mean". ([CausalArena HTML §4.2, 4.4, 5.4](https://arxiv.org/html/2609.11897v1)) | CausalArena. **Our inference:** an LLM agent with real names can score by sharing the authoring LLM's priors. |
| **Memorisation of famous networks** | LLMs are near-perfect on BNLearn and far worse on graphs published after their training cutoff. ([Srivastava et al.](https://arxiv.org/abs/2510.16530)) Reported via prior note cluster8: Asia 0.93 vs post-cutoff Alzheimer's 0.56. Sachs ground truth is "not definitive", and results have "peaked at an SHD of around 12". ([Brouillard et al.](https://arxiv.org/html/2412.01953v2)) | Agent papers scored on bnlearn graphs: ALCM, MATMCD, CauScientist, CEA (prior note cluster2) |
| **Name leakage** | LLMs "mostly rely on the semantic meaning of variable names". ([CARE](https://arxiv.org/abs/2511.16016)) Reported via prior note cluster8: Asia scores 1.000 with original names, 0.00-0.08 with random names, about 0.15 with permuted names. Measured (ours): Causal-Copilot 0.306 / 0.232 / 0.142 (real / neutral / swapped). | CausalArena (semantic names, no control arm); all bnlearn agent papers |
| **Metric choice** | Interventional measures on empirical data give "substantially different" results from structural ones. ([Gentzel et al.](https://arxiv.org/abs/1910.05387)) SID scores implied intervention distributions and accepts CPDAGs. ([Peters & Bühlmann](https://arxiv.org/abs/1306.1043)) AID generalises SID, extends it to CPDAGs and causal orders, and is orders of magnitude faster. ([Henckel et al.](https://arxiv.org/abs/2402.08616)) Separation distances capture what link-based distances miss. ([Wahl & Runge](https://arxiv.org/abs/2402.04952)) Precision and recall can be very large under random guessing, so they need negative controls. ([Petersen](https://arxiv.org/abs/2412.10039v1)) Many metrics for Bayesian discovery track posterior quality poorly. ([Karimi Mamaghan et al.](https://arxiv.org/abs/2406.03209)) | **CausalArena** uses directed P/R/F1 and SHD only. In its code a reversal counts as 1 (prior note dom07). |
| **CPDAG-to-DAG conversion** | The conversion rule is rarely stated. CausalArena's "liberal" rule depends on the index, and it drops bidirected entries (prior note dom07). Causal-Copilot's evaluator orients non-directed edges from the truth (our scope_note). ACDB scores skeleton, DAG and efficiency as separate layers. ([ACDB](https://arxiv.org/abs/2609.31675)) | CausalArena, Causal-Copilot's paper numbers |
| **Real-data metric practice** | 167 papers reviewed. Structural metrics appear in 100% of simulated-data studies. Interventional metrics appear in 9.1% (simulated) and 7.5% (real). When real data contain interventions, interventional metrics go unused 89% of the time. ([Brouillard et al. §4, Table 1](https://arxiv.org/html/2412.01953v2)) | The field |

### 3.2 Proposals and protocols for benchmarking causal discovery

- **Reproducible workflow.** [benchpress](https://arxiv.org/abs/2107.03863) is a Snakemake workflow configured by a JSON file. It wraps BiDAG, bnlearn, causal-learn, gCastle, pcalg, TETRAD and others. It addresses reproducibility, not leaks.
- **Interventional and empirical evaluation.**
  - [Gentzel, Garant, Jensen](https://arxiv.org/abs/1910.05387) argue for interventional measures on empirical data. Venue not shown on the abs page; NeurIPS 2019 per prior note cluster9.
  - [Brouillard et al.](https://arxiv.org/html/2412.01953v2) recommend interventional metrics on unseen interventions and pseudo-real data.
- **Decision-theoretic evaluation.** [Eigenmann, Mukherjee, Maathuis, UAI 2020](https://proceedings.mlr.press/v124/eigenmann20a.html) define causal risk plus sample quantities computable from data. The abstract does not say how the method works without a ground-truth graph; we did not read the full paper.
- **Realism via semi-synthetic data.** [causalAssembly](https://arxiv.org/html/2306.10816v2) uses 98 features from 15,581 parts across 10 processes.
  - Ground truth: within-process edges come from experts and physics. Cross-process edges were learned by SpAM pruning and then treated as truth.
  - Data are generated with distributional random forests.
  - It reports varsortability and uses SHD, SID and F1. Default methods fail to beat an empty graph on SHD for the full line.
  - It has no interventions.
- **Assumption violations.** [Montagna et al.](https://arxiv.org/html/2310.13387v2) simulate confounding, measurement error, unfaithfulness, autocorrelated (non-iid) data, post-nonlinear and non-Gaussian settings across more than 60,000 datasets. Metrics are FNR, FPR, F1 and an order-based FNR. The generators are in the `causally` library. [CausalCompass](https://causalcompass.readthedocs.io/en/latest/) does the same for time series (8 scenarios, including standardisation).
- **Negative controls.** [Petersen](https://arxiv.org/abs/2412.10039v1) gives exact random-guess distributions for skeleton metrics.
- **Error sources without ground truth.** [Faltenbacher et al.](https://arxiv.org/abs/2502.14719) define coherency scores for PC that flag assumption violations and small-sample errors.
- **Faithfulness.** [Olko et al.](https://arxiv.org/abs/2502.16056) argue that faithfulness violations at typical sample sizes cap neural discovery.
- **Data traits.** [Niu et al.](https://arxiv.org/abs/2407.13054) benchmark 29 algorithms and show that data traits decide the winner.
- **Combined metrics.**
  - [OCDB](https://arxiv.org/html/2406.04598v1) proposes a structure distance that is fair between DAGs and CPDAGs, and a causal-effect distance.
  - [Velev & Lessmann](https://arxiv.org/abs/2409.19377) propose a six-dimensional "distance to optimal solution".
- **Calibration of edge frequencies.**
  - [Banerjee, Andrews, Kummerfeld](https://arxiv.org/html/2503.15436v1) score resampled edge frequencies by Brier score and ECE. They find no resampling technique wins everywhere.
  - Friedman et al. and Jabbari et al. show that bootstrap frequencies are not calibrated (prior note dom08).
- **Benchmarks that already carry part of our target:**
  - [CausalDS](https://arxiv.org/abs/2607.08093) treats abstention as "a first-class scored outcome", runs agents in a sandbox, and has a verbalisation-swap ablation (prior notes dom07, cluster2).
  - [ACDB](https://arxiv.org/abs/2609.31675) gives agents a budgeted intervention API and scores in layers.
    - Reported: PC with greedy active orientation 42.7% directed F1; Sonnet 4.6 31.7%; GPT-5.4 22.9%; random DAG 23.6%.
    - The PC agent under-commits, and the LLMs over-commit.
  - [CausaLab](https://arxiv.org/abs/2605.26029): reported 92% task accuracy with edge F1 0.471, observational only, 6 nodes.
  - [BoxingGym](https://arxiv.org/abs/2501.01540) scores experimental design by expected information gain.
- **Experiment-choice baselines with code** (prior note dom10): `pcalg::opt.target` (OptSingle and OptUnb) and [CBED](https://github.com/yannadani/cbed). CBED's CPU feasibility is unverified.

### 3.3 Sources of physical and simulated ground truth

| Source | Ground truth origin | Interventions | Relevance / limits |
|---|---|---|---|
| [Causal Chambers](https://arxiv.org/abs/2404.11341) ([repo](https://github.com/juangamella/causal-chamber): Nature Machine Intelligence 2025 per README; data CC BY 4.0) | Physics, empirically validated. Prior note cluster7: each edge is checked by a randomised two-level experiment. | Yes; many single-target shift datasets | Mk1 standard graphs are depth-1 (actuator to sensor), so orientation is trivial once actuators are known (cluster7, computed from the package). That makes the chambers a sharp **name-leak test**, but a weak orientation test. |
| Chambers Mk2 / Remote Lab | `lt_spice_v1` uses Light Tunnel Mk2 "linked_leds" ([repo](https://github.com/juangamella/causal-chamber)). The Remote API is in `causalchamber` 0.2.8, MIT licence ([PyPI](https://pypi.org/project/causalchamber/)). | Chosen in real time (cluster7: about 10-12 Hz; subscriber credentials; fees per order form; no public price) | The only source we found for **chosen interventions on a real system**. Cost and limits are unknown. |
| [causalAssembly](https://arxiv.org/html/2306.10816v2) | Experts and physics, plus SpAM-learned cross-process edges | No | Realistic marginals; some truth edges are learned |
| [CausalMan](https://arxiv.org/html/2502.12707v1) (Zenodo, CC BY 4.0, per prior note rep12) | Physics-based simulator; latent projection | Yes | 53 or 186 observed nodes; bidirected edges are encoded as pairs |
| [CausalPlayground](https://arxiv.org/html/2405.13092v1) (MIT) | Sampled SCMs, confounders optional | Yes, via a Gymnasium environment | Name and order randomisation are not mentioned. A ready interactive shell. |
| [SERGIO](https://www.biorxiv.org/content/10.1101/716811.full.pdf) | GRNs sampled from E. coli and yeast networks via GeneNetWeaver | Master-regulator knockout is stated as "easily simulated", not validated | Gene-regulation slice; cycles were broken |
| [CausalBench (GSK)](https://arxiv.org/abs/2210.17283) | No truth graph; real single-cell perturbations | Yes (real) | Interventional evaluation. Methods that use interventions did not beat observational ones. |
| [Neuropathic pain simulator](https://arxiv.org/abs/1906.01732) | Expert pathology graph | No | Famous, with partial LLM memorisation (prior note cluster2) |
| [CausalRivers](https://arxiv.org/abs/2503.17452v1), [ESS industrial](https://arxiv.org/abs/2310.18654) | River metadata (666 + 494 stations); expert graph | No | Time series. Out of our iid scope. |
| [CausalVerse](https://arxiv.org/html/2510.14049v2), [CausalWorld](https://arxiv.org/abs/2010.04296v2) | Rendered and robotic simulators | Yes | Representation learning and RL. Not tabular discovery. |
| "SimCausal" | Not found as a discovery simulator. The nearest is the R package [simcausal](https://cran.r-universe.dev/simcausal) (Sofrygin, van der Laan, Neugebauer). | Yes | Longitudinal effect-estimation simulation |
| Robotics or circuit testbeds for tabular discovery | Not found by these searches | | |

### 3.4 Controls specific to LLMs

| Control | Where it exists | Gap |
|---|---|---|
| Anonymised names | CARE "Random"; [Kitson & Constantinou 2026](https://arxiv.org/abs/2608.27472) (obfuscation, via prior note cluster8; today's abs read did not show it); DMCD (X1..Xn) | None crosses it with column layout. |
| Names permuted across columns | CARE "Permuted" (data unchanged) | Only for CARE's own fine-tuned model family |
| Counterfactual relabelling (names that imply a plausible but different graph) | Not found as a graded dial. CausalDS's verbalisation swap is the nearest, but for story-graph tasks. ABAPC-LLM's CauseNet mapping gives meaningful names on novel graphs ([Li & Russo](https://arxiv.org/html/2602.16481v1)). | **Open.** |
| Post-cutoff graphs | Srivastava et al. | Small number of graphs |
| Recognition probes (node, edge, subgraph or row completion) | Srivastava et al.; Kıcıman et al. (prior note cluster2) | Not built into any discovery leaderboard |

### 3.5 What no benchmark found here combines

None of the benchmarks found combines all five of the following:
1. Shuffled layout as a measured factor.
2. A real / neutral / swapped name factor on identical data.
3. Withheld / released / chosen interventions at 20-40 variables.
4. Per-edge calibration and abstention scoring.
5. Decision-level scoring (held-out interventional prediction, effect queries, experiment value).

Coverage of the closest benchmarks:
- CausalArena: (3) partly, with released interventions only.
- CausalDS: (2) partly, and an abstention variant of (4) for effects.
- ACDB: (3) at 4-7 nodes, and (5) as efficiency.
- CARE: (2) only.

## 4. Typed table (summary; full rows with evidence in the JSON)

The total if everything is built is about **21 person-weeks (our estimate)**. The designs in §5 take subsets of it.

| # | Requirement | Prevents | Fails in | Effort (our est.) |
|---|---|---|---|---|
| R01 | Shuffled columns, hidden key, layout-probe baseline | Directions read from layout (0.680 vs 0.269, ours) | CausalArena, bnlearn suites | 0.5 pw |
| R02 | Real / neutral / swapped / counterfactual names on identical data | Directions read from names (0.306 / 0.232 / 0.142, ours; CARE) | CausalArena, bnlearn agent papers | 1.5 pw |
| R03 | Report var- and R2-sortability; iSCM slice; rescaling arm | Sortability and scale shortcuts | Most synthetic suites; CausalArena semantic not analysed | 1 pw |
| R04 | No famous graphs in scored set; recognition probe | Memorisation | ALCM, MATMCD, CEA, CauScientist | 1 pw |
| R05 | Ground-truth origin typed per instance | LLM-authored-graph circularity | CausalArena, CausalDS | 0.5 pw |
| R06 | Identifiable target; order-independent conversion; per-instance ceiling | Index-based orientation bias; unfair DAG scoring | CausalArena, Causal-Copilot evaluator | 1 pw |
| R07 | SHD convention, AID/SID, separation distance, negative controls | Metric-driven rankings | CausalArena | 0.5 pw |
| R08 | Declared and enforced regime D / D+I / D+I chosen / D+K; sandbox | Hidden knowledge use | CausalArena, most agent papers | 1 pw |
| R09 | Per-edge attribution across arms; provenance-honesty score | Unattributed directions | All found | 1 pw |
| R10 | Three-state probabilities; Brier/ECE; risk-coverage; abstention credit | Overconfident claims | CausalArena (score_matrix accepted, not scored) | 1.5 pw |
| R11 | Held-out interventional prediction | Graphs that look right but predict wrong | CausalArena, bnlearn | 2 pw |
| R12 | Budgeted intervention API; regret vs OptSingle/CBED/random | Unmeasured experiment choice | CausalArena (fixed targets), ACDB small | 2.5 pw |
| R13 | Identification-gated effect queries; bounds and abstain credit | Decision errors hidden by F1 | All discovery benchmarks | 2 pw |
| R14 | Physical / validated-truth slice | Generator artefacts | Pooled real-data scores in CausalArena | 1.5 pw |
| R15 | World axes declared and stratified | Assumption mismatch hidden | CausalArena semantic, agent papers | 1 pw |
| R16 | Baseline floor pack (empty, random, sortnregress, layout probe, name-only, true-depth) | Shortcut wins unnoticed | CausalArena (RandomRegress only) | 0.5 pw |
| R17 | ≥5 runs, scenario CIs, rank stability | Rank flips | Most agent papers | 0.25 pw |
| R18 | Private regenerated split; canaries | Contamination | bnlearn; CausalArena held-out half not server-scored | 0.5 pw |
| R19 | Deterministic harness, scorer hashes | Irreproducible configs | CausalArena (appendix unreadable) | 1 pw |
| R20 | Dev-only tuning; default and tuned rows | Tuning on truth | Common | 0.25 pw |

## 5. Three designs we could build in 4-8 weeks

The arms are shared across designs:
- **Layout (L):** as released / shuffled (k = 3 permutations).
- **Names (N):** real / neutral / swapped, plus counterfactual in B2.
- **Interventions (I):** withheld / released / chosen.

Effort and cost figures in this section are our estimates.

### B1 "ArenaShuffle": a control overlay on CausalArena (about 4 weeks)

- **Generator / data:** CausalArena's public 50 semantic and 50 formula scenarios, re-sampled with its replay sampler. The data are CC BY 4.0 per the [HF card](https://huggingface.co/datasets/LAMDA-Tabular/CausalArena). The sampler would be extended to allow arbitrary targets and to shuffle columns.
- **Ground-truth origin:** CausalArena SCMs, typed "LLM-assisted authored" (R05). Latent nodes are dropped via `mask`, as their scorer does.
- **Controls:**
  - L: released vs shuffled.
  - N: real, neutral, swapped.
  - I: withheld (1,000 observational rows); released (their 800 + 200 split); chosen (budget of B single-node interventions, of 200 rows each, through the extended sampler).
- **Scored views:**
  - Forced-choice directed F1 under an order-independent rule.
  - Skeleton F1.
  - Direction accuracy on compelled edges.
  - Abstention rate on non-compelled edges.
  - Precision at 50% and 80% coverage, and ECE/Brier, both from `score_matrix` or bootstrap frequencies.
  - Interventional prediction error on 3 held-out targets per scenario, using a fixed linear-Gaussian estimator fitted on the submitted graph.
  - Experiment-choice value (compelled fraction gained per intervention) against `pcalg::opt.target` and random targets.
- **Build:** R01, R02 (without the counterfactual arm), R05-R10, R11 (fixed estimator), R12-lite, R16, R17, plus a light R19. About 4 person-weeks.
- **Compute:** classical methods are CPU-cheap.
  - Agent run count per agent = scenarios x replicates x arms x seeds.
  - The minimum useful grid is 25 x 1 x 6 x 3 = 450 runs: real/neutral/swapped names x released/shuffled layout, interventions withheld.
  - API cost per Causal-Copilot run is not in our notes, so this needs a one-run cost probe before committing.
- **What it shows that CausalArena cannot:**
  - How much of each published score survives shuffling and neutral names.
  - Each method's direction accuracy split by source (data, names, layout, interventions).
  - Whether `score_matrix` confidences are calibrated.
  - Whether a better F1 gives better interventional prediction.
  - All of this on CausalArena's own scenarios, so it is directly comparable to the published leaderboard.

### B2 Decoupled-semantics generator (6-8 weeks)

- **Generator:** our own SCM generator.
  - 20-40 variables, iSCM-standardised so var- and R2-sortability sit near 0.5 (reported for iSCMs; to be measured per instance).
  - Mixed mechanisms, and a hidden-confounder arm through the `causally` or CausalPlayground generators.
  - Private seeds; a held-out split regenerated per round.
- **Names:** mapped by subgraph isomorphism onto CauseNet, as ABAPC-LLM does, so names are meaningful but the graph is new.
- **Counterfactual relabel dial:** names are drawn from a second CauseNet subgraph that agrees with the data graph on a fraction ρ ∈ {1.0, 0.7, 0.4} of orientations.
- **Ground-truth origin:** the sampled SCM, which is exact.
- **Controls:**
  - L shuffled always, with one "released order = topological" arm kept as a leak demonstrator.
  - N: real, neutral, swapped, counterfactual(ρ).
  - I: withheld / released / chosen through a Gymnasium-style API with a budget.
- **Scored views:** everything in B1, plus:
  - Identification-gated effect queries (R13), with credit for intervals and for abstaining on non-identifiable queries.
  - Decision regret for "pick the best single intervention for target Y".
  - The **name-reliance curve**: F1 as a function of ρ.
- **What it shows that CausalArena cannot:**
  - A continuous measure of how much a system trusts names over data.
  - Calibration and abstention measured against exact identifiability.
  - Decision value: effects and experiments.
  - None of it can be solved by sortability, layout or memorisation.
- **Effort:** about 7 person-weeks. The generator is 2, the counterfactual names 1.5, the API and baselines 2, and the effect queries and scorer 1.5.

### B3 Physical slice (4-6 weeks)

- **Data:** public Causal Chambers datasets, CC BY 4.0. Candidates:
  - `lt_interventions_standard_v1`: a reference set plus single-target shifts.
  - `lt_validate_v1` and `wt_validate_v1`.
  - `lt_spice_v1`: Mk2 linked LEDs, for deeper graphs.
  - Optionally causalAssembly station subsets (observational only).
  - Optionally Remote Lab runs for chosen interventions, which need a subscription with no public price.
- **Ground-truth origin:** physics, plus randomised validation experiments. For causalAssembly: experts and physics, plus learned cross-process edges, typed as such.
- **Controls:**
  - L shuffled.
  - N: real physical names (`red`, `pol_1`, `current`) vs neutral vs swapped. Actuator names alone reveal the roots of the depth-1 Mk1 graphs, so this is the cleanest real-data name-leak test available.
  - I: withheld vs released (recorded shifts), with chosen only through the Remote Lab.
- **Scored views:**
  - Skeleton F1 and direction accuracy.
  - Calibration.
  - Held-out interventional prediction on recorded shift datasets. This is the real-data version of R11 and the item Brouillard et al. say is almost never done.
- **What it shows that CausalArena cannot:** results on validated physical truth, with real interventional evaluation, separated from pooled "real-data" averages.
- **Limit:** orientation is easy in Mk1 once actuators are known, so B3 complements B1/B2 and cannot stand alone.
- **Effort:** about 4 person-weeks without the Remote Lab.

**Recommended order:** B1 first. It is cheapest, reuses our existing measurements, and is comparable to the published leaderboard. Then B2 as the paper-grade contribution, with B3 as the real-data check.

## 6. Who would use it, and is a public track plausible?

**Likely users (our judgment):**
- Authors of LLM agents and hybrids that are currently evaluated on named bnlearn graphs (Causal-Copilot, CausalSteward, CEA, ALCM, CauScientist).
- Authors of pretrained models that claim permutation invariance (FoundCause abstract; AVICI, Arrow). They gain a direct test of the claim.
- Reviewers who need a leak-free comparison.
- The CausalArena maintainers themselves.

**Plausibility of a public track.** A public track is plausible if submission stays cheap. CausalArena already accepts a `manifest.json` (which includes "supported regimes"), a `summary.csv`, and optional per-graph `.npz` files with `score_matrix`, `adjacency` and `node_order`. It also uses maintainer validation and a static HF Space ([HF card](https://huggingface.co/datasets/LAMDA-Tabular/CausalArena)). A controlled track could reuse that format and add:
1. A declared regime (D / D+I released / D+I chosen / D+K).
2. Arms generated server-side, so the permutation key and name mapping are never released.
3. A required `score_matrix` for calibration.

**Two tiers:**
- **File tier.** Static methods download permuted and renamed data and upload outputs. The arms are hidden because each submitter receives one random arm assignment per scenario.
- **Agent tier.** Agents run in a sandbox we host. This costs API spend per submission, so it needs a sponsor or a submitter-pays model. A self-run agent tier needs logs and seeds and is easier to game.

**Partner option.** Proposing the overlay to the CausalArena maintainers as an official "controlled" track is the low-cost route. Running our own Space is the fallback.

## 7. Risks

1. **New shortcuts in our generator.** iSCM, CauseNet mapping and counterfactual names could each introduce artefacts. Mitigation: run the R16 baseline pack and report both sortabilities on every release.
2. **The swap arm penalises legitimate knowledge.** Using names is valid in the D+K regime. The benchmark must present name sensitivity as provenance, not as an error, or it will be read as anti-LLM.
3. **Counterfactual names may be detectably implausible.** LLMs may spot fake stories, which would confound the ρ dial. Mitigation: human plausibility checks, plus a "which story is real" probe.
4. **Small effective n.** With 25-50 scenarios, calibration and CIs are coarse (prior note dom08: the scenario is the unit).
5. **Cost.** Agent arms multiply runs by 6-18x. Causal-Copilot's per-run cost is unmeasured in our notes. Remote Lab fees are unknown.
6. **Being scooped or overlapping.** CausalArena could add shuffling. CausalDS and ACDB already cover parts. The novelty claim is the combination plus provenance attribution. Re-check the literature at submission time.
7. **Licensing and redistribution.** CausalArena data are CC BY 4.0 and the chamber data are CC BY 4.0, both of which permit derivatives with attribution. CauseNet's licence was not checked.
8. **Maintenance.** A leaderboard needs an owner after the capstone. Without one, publish it as a frozen benchmark plus a scorer package instead.
9. **Truth uncertainty in physical data.** Chamber absent edges mean "no significant effect found" (prior note cluster7), and causalAssembly cross-process edges are learned. Score those edges in a separate stratum.

## 8. What this changes for the project

1. **E2 (public agent track):** start from B1 rather than a new benchmark. It reuses CausalArena's submission format and our existing measurements. The ask to the maintainers is "server-side arms + declared regime + scored `score_matrix`".
2. **The claim ledger's evaluation contract:**
   - Adopt R06 + R10 + R09 as the primary scored views: skeleton F1, direction accuracy on compelled edges, abstention on non-compelled edges, Brier/ECE, and per-edge provenance across arms.
   - Report forced-choice F1 only as a secondary view, under the expectation rule.
3. **Rescore everything we report** with the order-independent conversion rule and AID next to SHD (both reversal conventions). Add the R16 floor pack to every table, including the layout probe and true-depth regression.
4. **Interventional prediction is the cheapest decision-value metric** to add (R11), because the sampler already intervenes. Do it before effect queries or experiment choice.
5. **Use Causal Chambers as the real-data name-leak demonstration** (B3), not as an orientation benchmark.
6. **B2 is the paper-grade contribution.** The ρ-dial name-reliance curve is not found in prior work.
7. **Ticket:** AUD-21 should close on (a) the B1 spec and scorer interface, and (b) a one-run API cost probe for Causal-Copilot, which gates the agent-tier budget.

## 9. Open questions

- Are all 100 published CausalArena scenarios in topological `node_order`? So far one or a few have been checked (prior note dom07).
- Do the CausalArena maintainers score the held-out half server-side? The HF card does not say.
- What do the Remote Lab fees and rate limits look like for a semester of chosen interventions?
- How does the CPDAG ceiling change when interventions are chosen? This feeds the per-instance ceiling in R06.
- What is CauseNet's licence, and how good is its coverage for 20-40-node subgraph mapping?
- Can counterfactual name sets be made indistinguishable from real ones by an LLM judge? This needs a pilot.
- Does Eigenmann et al.'s data-computable risk work without truth, so it could serve as a real-data metric? We only read the abstract.

## 10. Not read

- **SERGIO PMC page:** reCAPTCHA. The bioRxiv full text was read instead, but its title and venue metadata were not shown.
- **Causal Chambers Remote Lab terms, pricing and Mk2 ground-truth documentation:** only the landing page was read. Details come from prior note cluster7.
- **CausalArena appendices B and C:** the fetch truncates before them, as also noted in dom07.
- **Brouillard et al., final 8k characters:** truncated.
- **Montagna et al., Appendix I.3 (score-sortability):** not in the fetched text.
- **Kaiser & Sipos:** experiment details and the journal version (a search result points to Neural Processing Letters) were not opened.
- **Gentzel et al. venue:** the proceedings page was not opened.
- **CausalTime:** not searched.
- **Causal-Audit (arXiv 2604.02488):** the publication date was not shown.
- **Kitson & Constantinou 2026, obfuscation details:** today's abs read did not show them. They rest on prior notes cluster8 and cluster2.

## 11. Searches run (2026-10-12)

1. Kaiser Sipos unsuitability of NOTEARS causal graph discovery dimensional quantities scale
2. Eigenmann Mukherjee Maathuis evaluation of causal structure learning algorithms via risk estimation UAI 2020
3. CausalPlayground synthetic data generation causal discovery reinforcement learning arXiv
4. CausalVerse benchmark causal representation learning simulator ground truth
5. SimCausal simulator causal discovery benchmark
6. simcausal R package Sofrygin simulation causal DAG
7. SERGIO single-cell gene regulatory network simulator benchmark causal discovery interventions
8. causal discovery benchmark LLM-generated causal graphs synthetic data realism critique semantic scenarios
9. LLM-generated structural causal models synthetic benchmark realistic variable names data generation causal discovery 2025
10. CausalRivers real-world river discharge causal discovery benchmark ground truth
11. robot arm or electronic circuit physical testbed ground truth causal discovery benchmark interventions dataset
12. CausalWorld robotic manipulation benchmark causal structure transfer Ahmed 2020
13. Causal Chambers Mk2 light tunnel remote lab Gamella 2025 2026 new chambers
14. causalchamber remote lab quickstart python API real-time experiments chambers subscribers
15. conformal prediction causal discovery edge sets coverage guarantee structure learning
16. causal discovery benchmark downstream causal effect estimation error graph metric correlation interventional evaluation 2025
17. CPDAG to DAG evaluation convention directed F1 undirected edges scoring causal discovery benchmark comparison
18. LLM causal discovery variable names conflict with data counterfactual relabeling swapped names test memorization benchmark
19. best practices checklist benchmarking causal discovery algorithms recommendations evaluation pitfalls 2024 2025 arXiv
20. "causal discovery" benchmark leaderboard public submission declared assumptions held-out test server
21. causal discovery benchmark anonymized variable names column permutation invariance test LLM agents 2026
22. selective causal discovery abstain edges risk coverage calibrated edge confidence benchmark

**Where we're going:** settle B1's scorer interface. That means the three-state probability file, the expectation-rule forced-choice F1, and AID with both SHD conventions. Then run a one-run cost probe for Causal-Copilot and draft the maintainer ask for a controlled CausalArena track.
