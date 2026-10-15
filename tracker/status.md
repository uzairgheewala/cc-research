# Tracker status (verified 2026-10-15T17:25:04Z)

Legend: ✅ done · 👀 in progress (or reopened) · ⏳ to-do · 🔴 blocked · 🔵 open. Evidence levels V0-V4: see README.md.


## 0 Quarter 1 deliverables

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| DLV-01 | ✅ | Q1 dataset suite: the datasets Causal-Copilot is run on, frozen, with a card per dataset | V3 |  |
| DLV-02 | ✅ | Q1 runs: Causal-Copilot run unmodified on every suite dataset under name controls, fully recorded | V3 |  |
| DLV-03 | 👀 | Q1 exploration: what Causal-Copilot does to the graph on these datasets, stage by stage | V2 |  |
| DLV-04 | ✅ | Q1 refinement research: a refinement step that never falls below its own algorithm on these datasets | V3 |  |
| DLV-05 | ⏳ | Q1 checkpoint (Mon 2 Nov) | V0 |  |
| DLV-06 | ⏳ | Q1 final: replication-style report on Causal-Copilot over the Q1 datasets (Fri 4 Dec) | V0 |  |

## 1 Replication

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| REP-01 | ✅ | Run Causal-Copilot a31aa7c unmodified end to end with GPT-4o, fully recorded | V3 |  |
| REP-02 | ✅ | Code untouched before and after every run (1,332 files byte-identical) | V3 |  |
| REP-03 | 👀 | Reproduce the paper's headline claims (arXiv 2504.13263) | V3 |  |
| REP-04 | ✅ | Check the paper's text against the code (divergences D1-D9) | V3 |  |
| REP-05 | ✅ | Reproduce CausalArena's published PC baseline (scorer calibration, F1) | V3 |  |
| REP-06 | ✅ | Explain why SHD does not reproduce (ours 37.5, published 33.5) | V3 |  |
| REP-07 | 👀 | Reproduce more published CausalArena rows: GES/GIES, FCI, LiNGAM, NOTEARS, AVICI, CDFM (CPU) | V3 |  |
| REP-08 | ✅ | Reproduce the R2-sortability analysis (Reisach et al. 2023) on CausalArena | V3 |  |
| REP-09 | ✅ | Reproduce the Causal Chambers authors' GES baseline and CDFM's chamber score | V3 |  |
| REP-10 | ⏳ | Reproduce CARE's moved-names control on one classic graph | V0 |  |
| REP-11 | 👀 | Reproduce Kitson & Constantinou's Sachs numbers (0.61 / 0.40 / 0.73) | V3 |  |
| REP-12 | 🔵 | Reproduce CausalSteward's external score for Causal-Copilot (F1 0.08 at 53 variables) | V2 |  |
| REP-13 | ✅ | Re-read every second-hand literature claim before it enters the report | V3 |  |

## 2 Domain exploration

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| DOM-01 | ✅ | Theory baseline: identifiability, finite samples, untestable assumptions; what 'perfect' means | V3 |  |
| DOM-02 | ✅ | Literature map in 9 clusters | V3 |  |
| DOM-03 | ✅ | Benchmark landscape and what '100%' means on each | V3 |  |
| DOM-04 | ✅ | Nearest prior work for each claim we might make | V3 |  |
| DOM-05 | ✅ | Commercial landscape, first pass | V3 |  |
| DOM-06 | ✅ | Weighing against the WorldReset forecasting project | V3 |  |
| DOM-07 | 👀 | Deep reads: CausalDS, CARE, CausalArena appendices B-C, ACI scoring, Li & Russo implementation | V2 |  |
| DOM-08 | ✅ | Choose a calibration method for bootstrap confidence | V3 |  |
| DOM-09 | ✅ | What is practical for 'what if we set X?' at 20-40 variables (IDA, adjustment on CPDAG/PAG, bounds) | V3 |  |
| DOM-10 | ✅ | Active experiment-design baselines: which to implement | V3 |  |
| DOM-11 | ✅ | Pretrained discovery models: order-invariance by design, CPU checkpoints | V3 |  |
| DOM-12 | ✅ | Hidden common causes, time series, 100+ variables | V3 |  |

## 3 Audit: Causal-Copilot

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| AUD-01 | ✅ | Architecture map: 8-step CLI path, state object, LLM call points, storage | V3 |  |
| AUD-02 | ✅ | LLM dependency map: 51 call sites, 88 logical points, 29 decisions, 3 graph-writing points | V3 |  |
| AUD-03 | ✅ | Edge lineage tool: every final edge traced to the step that set it | V3 |  |
| AUD-04 | ✅ | Refinement audit without the LLM: bootstrap step deletes non-directed edges | V3 |  |
| AUD-05 | ✅ | Name controls on 5 datasets: real 93% / neutral 0% / moved 90% of final edges written by the LLM | V3 |  |
| AUD-06 | ✅ | Reliability: 12 of 84 runs crashed; cycle step failed 9 of 9; one request got 3 answers | V3 |  |
| AUD-07 | ✅ | Stability: algorithm choice stable; edge decisions vary; bootstrap seeded by accident; numpy unseeded | V3 |  |
| AUD-08 | ✅ | Survivor-bias check: crashed runs do not change conclusions | V3 |  |
| AUD-09 | ✅ | Leak scan of neutral-name arms: no real name in any prompt before the final graph | V3 |  |
| AUD-10 | ✅ | Causal-Copilot on CausalArena's named scenarios (10 x real/neutral/moved, columns shuffled) [A2] | V3 |  |
| AUD-11 | ✅ | Behaviour at 20-40 variables: cost, runtime, crash rate | V3 |  |
| AUD-12 | ✅ | Effect-estimation module (causal_inference/) | V3 |  |
| AUD-13 | ✅ | Second model besides GPT-4o | V3 |  |
| AUD-14 | 👀 | Torch-based and time-series wrappers, web-demo path, report quality | V3 |  |
| AUD-15 | ✅ | Upstream branches newer than a31aa7c | V3 |  |
| AUD-18 | ✅ | Field audit: every causal-discovery system, its regimes, order source and evaluation controls | V3 |  |
| AUD-19 | ✅ | Benchmark audit: ground-truth origin, scored views and leak channels of every benchmark | V3 |  |
| AUD-20 | ✅ | Theory audit: identifiability, sample and experiment bounds per cell of Q x R x W | V3 |  |
| AUD-21 | ✅ | Own-benchmark audit: requirements, pitfalls and candidate designs | V3 |  |
| AUD-22 | ✅ | Commercial audit: who buys causal analysis, for which decision, with which guarantee | V3 |  |
| AUD-23 | ✅ | Engine audit: libraries, capabilities, defects; build vs reuse for the ledger | V3 |  |
| AUD-24 | ✅ | Value-of-accuracy audit: how graph errors become decision errors | V3 |  |
| AUD-25 | ✅ | Packaging audit: delivery modes, output requirements, regulator needs, user complaints | V3 |  |
| AUD-26 | ✅ | Audit synthesis: where the open room is, what makes a tool worth using, build vs reuse | V3 |  |
| AUD-27 | ✅ | Engine oracle check: PC and FCI under a perfect independence oracle, every engine copy | V3 |  |
| AUD-28 | ✅ | Controlled re-score: released vs shuffled columns for every runnable baseline; PC conflict-rule mechanism | V3 |  |
| AUD-29 | ✅ | Sortability of the CausalArena release (varsortability, R2-sortability) | V3 |  |
| AUD-30 | ✅ | Decision value (DV-1) and adjustment-identification distance for every baseline, with ceilings and the empty-graph baseline | V3 |  |
| AUD-31 | ✅ | Cost of one Causal-Copilot run (the approved one-run cost check) | V3 |  |
| AUD-32 | ✅ | Audit program DAG: research landscape, commercial landscape, wedge and paper | V3 |  |
| AUD-33 | ✅ | AB-01 Controlled scoreboard, CausalArena complete (all families, D and D+I, corrected leaderboard) | V3 |  |
| AUD-34 | ✅ | AB-02 Second scoreboard: layout and conflict channels on other public benchmarks | V3 |  |
| AUD-35 | ✅ | AB-03 Engine forensics: perfect-oracle and determinism checks for every engine agents call | V3 |  |
| AUD-36 | ✅ | AB-04 Decision-value scoreboard across benchmarks, with the usefulness threshold | V3 |  |
| AUD-37 | ✅ | AB-05 LIVE (small): agent probes, install and one-run cost per agent ($5 cap) | V3 |  |
| AUD-38 | ✅ | AB-06 LIVE: field audit of LLM-using systems under names x layout controls | V3 |  |
| AUD-39 | ✅ | AB-08 Name-reliance benchmark with a rho dial (decoupled semantics, B2) | V3 |  |
| AUD-40 | ✅ | AB-09 Theory pack: identity, error budget, bounded harm, conflict-rule order dependence, DV ceiling | V3 |  |
| AUD-41 | 🔴 | AB-10 Practitioner interviews (C1) | V3 |  |
| AUD-42 | ✅ | AB-11 Competitive teardown: open tools hands-on, closed tools by documented claims | V3 |  |
| AUD-43 | ✅ | AB-12 Vertical probe: root-cause analysis | V3 |  |
| AUD-44 | ✅ | AB-13 Regulation and standards map: requirement -> ledger field | V3 |  |
| AUD-45 | ✅ | AB-14 Market map and three vertical briefs (RCA, marketing, pharma RWE), with public demand evidence | V3 |  |
| AUD-46 | ✅ | AB-15 Positioning closure: novelty matrix for L1-L5 | V3 |  |
| AUD-47 | ✅ | AB-17 Paper skeleton and pre-registration manifest | V3 |  |
| AUD-48 | ✅ | AB-07 LIVE: knowledge elicitation run (A3, DEC-02): tiers, three phrasings, three name arms | V3 |  |

## 15 Decisions

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| DEC-05 | ✅ | AB-16 Wedge decision: paper spine, venue and the Q2 build | V3 |  |

## 4 Audit: benchmarks and data

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| BEN-01 | ✅ | CausalArena public release inspected (families, files, graph convention) | V3 |  |
| BEN-02 | ✅ | Column-order leak: every true edge runs earlier column -> later column in every released file | V3 |  |
| BEN-03 | ✅ | Identifiable ceilings 0.957 / 0.971 (obs); at least 0.974 / 0.993 with released interventions | V3 |  |
| BEN-04 | ✅ | Error budget for PC: 1.000 -> 0.957 -> 0.611 -> 0.335; directions right 54% | V3 |  |
| BEN-05 | ✅ | Value of oracle order knowledge (inputs only: 0.470; full depth + regression: 0.714) | V3 |  |
| BEN-06 | ✅ | Repo datasets vs CausalArena index: Auto MPG does not match | V3 |  |
| BEN-07 | 👀 | Do CausalArena's wrappers shuffle columns; are top methods affected? | V3 |  |
| BEN-08 | ✅ | SHD definition mismatch (see REP-06) | V3 |  |
| BEN-09 | ✅ | Replay sampler: which declared interventions are interventions in name only | V3 |  |
| BEN-10 | ✅ | Causal Chambers: map 8 datasets to ground-truth graphs; check 'one layer deep'; build obs+int sample | V3 |  |
| BEN-11 | 👀 | Error budgets for GES, FCI, pretrained models; formula and synthetic families | V3 |  |
| BEN-12 | ✅ | Reliability of real-data reference graphs | V3 |  |

## 5 Targets

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| TGT-01 | ⏳ | Semantic, numbers only: reach 0.634 (FoundCause); GIES 0.552; ceiling 0.957 | V2 |  |
| TGT-02 | ⏳ | Semantic, numbers + interventions: reach 0.568 (GIES); ceiling >= 0.974 | V2 |  |
| TGT-03 | ⏳ | Formula, numbers only: reach 0.524 (FoundCause); ceiling 0.971 | V2 |  |
| TGT-04 | ⏳ | Formula, numbers + interventions: reach >= 0.534 (TabCausal; check other rows); ceiling >= 0.993 | V2 |  |
| TGT-05 | ⏳ | Real data: 0.391 observational (CDFM); 0.462 with interventions (TabCausal, 7 sets) | V2 |  |
| TGT-06 | 👀 | Causal Chambers alone: 0.727 reported by CDFM (second-hand; check subset) | V3 |  |
| TGT-07 | ⏳ | Numbers + declared knowledge: >= 0.634 semantic, >= 0.524 formula, columns shuffled | V0 |  |
| TGT-08 | 🔵 | Derived requirement: skeleton F1 x direction accuracy >= 0.634 (e.g. 0.80 x 0.79) | V2 |  |
| TGT-09 | ✅ | Never below the system's own data-only output | V3 |  |
| TGT-10 | ✅ | Zero change when columns are shuffled | V3 |  |
| TGT-11 | ✅ | Bounded harm when names are wrong | V3 |  |
| TGT-12 | ✅ | Calibration better than raw bootstrap frequencies on held-out scenarios | V3 |  |
| TGT-13 | ✅ | Zero crashes from malformed model output | V3 |  |
| TGT-14 | ⏳ | Within the scoreboard's 1-hour budget per graph | V0 |  |
| TGT-15 | ⏳ | Held-out interventional predictions better than regression on all variables | V0 |  |
| TGT-16 | ⏳ | Experiment choice better than random on recorded Causal Chambers experiments | V0 |  |

## 6 Required capabilities

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| CAP-01 | ⏳ | Skeleton recall at variables with many causes (joint test per candidate edge) | V0 |  |
| CAP-02 | ⏳ | Direction from the numbers (PC: 54%) | V0 |  |
| CAP-03 | ✅ | Use intervention data | V3 |  |
| CAP-04 | ✅ | Declared knowledge as tiers, never edges | V3 |  |
| CAP-05 | ✅ | Invariance to column order | V3 |  |
| CAP-06 | ✅ | Keep 'direction unknown' edges | V3 |  |
| CAP-07 | 👀 | Calibrated confidence per claim | V3 |  |
| CAP-08 | ✅ | Abstention / selective claims | V3 |  |
| CAP-09 | ✅ | Provenance per edge with an independent checker | V3 |  |
| CAP-10 | ✅ | Robustness to malformed model output | V3 |  |
| CAP-11 | ✅ | Determinism (same inputs, same ledger hash) | V3 |  |
| CAP-12 | ⏳ | Runtime at 20-40 variables | V0 |  |
| CAP-13 | ⏳ | Nonlinear and mixed-type dependence | V0 |  |
| CAP-14 | ⏳ | Hidden common causes (PAG marks) | V0 |  |
| CAP-15 | ⏳ | 'What if we set X?' with identification status and bounds | V0 |  |
| CAP-16 | ⏳ | Choose the next experiment | V0 |  |
| CAP-17 | ✅ | Scoreboard packaging (CPDAG->DAG rule, summary.csv, validator) | V3 |  |
| CAP-18 | ⏳ | Cost per run measured at 25 variables | V0 |  |

## 7 Research questions

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| RQ-01 | ✅ | P1-P3 (pass 4b, Sachs): supported | V3 |  |
| RQ-02 | ✅ | N2 (bundle 1): supported | V3 |  |
| RQ-03 | ✅ | N1, N4, P3 (bundle 1): tested, inconclusive | V3 |  |
| RQ-04 | 🔵 | T1 Order source explains most directed-edge accuracy | V2 |  |
| RQ-05 | ✅ | T2 Deployed agents take order from names and layout | V3 |  |
| RQ-06 | 🔵 | T3 Typed, sourced partial order: never below data-only, bounded harm, best published per regime (target) | V2 |  |
| RQ-07 | 🔵 | T4 Calibrated, machine-checkable claims with abstention | V2 |  |
| RQ-08 | 🔵 | T5 What-if answers with identification status | V2 |  |
| RQ-09 | 🔵 | T6 Experiment choice beats random on recorded experiments | V2 |  |
| RQ-10 | ✅ | O1 Real names: >=70% of true edges ordered correctly, <=10% contradicted | V3 |  |
| RQ-11 | ✅ | O2 Neutral names give no order information | V3 |  |
| RQ-12 | ✅ | O3 Moved names: tiers follow the labels | V3 |  |
| RQ-13 | ✅ | O4 Regression on model tiers reaches 0.634 (semantic) | V3 |  |
| RQ-14 | ✅ | O5 Same for formula vs 0.524 | V3 |  |
| RQ-15 | 🔵 | Do LLM-written semantic graphs inflate name-based scores? | V0 |  |
| RQ-16 | ✅ | Does PC's error pattern hold for other algorithms? | V3 |  |
| RQ-17 | ✅ | Do results hold for a second model? | V2 |  |

## 8 Build

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| BLD-01 | ✅ | Recording harness and analysis tools | V3 |  |
| BLD-02 | ✅ | B1 data-only claim ledger with invariants I1-I4, I7 | V3 |  |
| BLD-03 | ✅ | B2 interventions as order evidence | V3 |  |
| BLD-04 | ✅ | B3 declared knowledge as tiers | V3 |  |
| BLD-05 | ✅ | B4 confidence, calibration, selective output | V3 |  |
| BLD-06 | ✅ | Drop-in replacement for Causal-Copilot's refinement stage | V3 |  |
| BLD-07 | ⏳ | C1 what-if answers with identification status and bounds | V0 |  |
| BLD-08 | ⏳ | C2 next-experiment choice from recorded pool | V0 |  |
| BLD-09 | ⏳ | Scoreboard-format export | V0 |  |
| BLD-10 | ✅ | Evidence tracker for this list (catalogue, verify, Slack List mirror) | V3 |  |
| BLD-11 | ✅ | Correlation layer: typed links between dev tickets, prod items, evidence, runs, docs and Slack; agent contract | V3 |  |
| BLD-12 | ✅ | Prod list in the dev encoding (groups and pass-through rows) and the Slack relay for milestones, summaries and artifacts | V3 |  |
| BLD-13 | ✅ | Claim-ledger record format, JSON Schema and verifier (V1-V8) | V3 |  |
| BLD-14 | ✅ | Claim ledger v0.2: plan and deviations, assumptions, lineage, reviews, question; verifier reports every check | V3 |  |

## 9 Evaluation protocol

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| EVL-01 | ✅ | Every score states its regime (D / D+I / D+K / D+I+K) | V3 |  |
| EVL-02 | ✅ | Controls on every score (columns shuffled; names real/neutral/moved; supplier; interventions) | V3 |  |
| EVL-03 | ✅ | Metric set: F1, skeleton P/R, direction accuracy, coverage, calibration, interventional error, cost | V3 |  |
| EVL-04 | ✅ | Predictions and thresholds fixed in code before every live run | V3 |  |
| EVL-05 | ✅ | Development / held-out split by scenario number before any tuning | V3 |  |
| EVL-06 | ✅ | Stage-by-stage scoring of any pipeline | V3 |  |
| EVL-07 | ✅ | Must-show list and gates for every live step | V3 |  |

## 10 Infrastructure

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| INF-01 | ✅ | Harness v3, Docker image, cc.ps1 commands, stub LLM, plan runner, fetcher | V3 |  |
| INF-02 | ✅ | Analysis tools with gates | V3 |  |
| INF-03 | ✅ | External data on disk (CausalArena 1.57 GB; 8 Causal Chambers datasets) | V3 |  |
| INF-04 | ✅ | Compute-job command on Uzair's machine (sandbox caps steps at 180 s) | V3 |  |
| INF-05 | ✅ | Unit tests for our code; caching by content hash | V3 |  |
| INF-06 | ⏳ | Public repository preparation (no keys, licences, no redistribution, run-record size) | V0 |  |
| INF-07 | ⏳ | One command reproduces every number in the report | V0 |  |

## 11 Course

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| CRS-01 | ⏳ | TA check-in 1 (TA: Nate) | V0 |  |
| CRS-02 | ⏳ | Quarter 1 checkpoint | V0 |  |
| CRS-03 | ⏳ | TA check-in 2 | V0 |  |
| CRS-04 | ⏳ | Quarter 1 final (50%) | V0 |  |
| CRS-05 | ⏳ | Quarter 2 proposal: written proposal, weekly schedule, 2-3 min pitch (15%) | V0 |  |
| CRS-06 | ⏳ | Quarter 2 deliverables: public repo, website, PDF report, poster; showcase 2nd week of March 2027 | V0 |  |
| CRS-07 | ⏳ | Decision gate G1 | V0 |  |

## 12 Team and communication

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| TEAM-01 | 👀 | Causal Discovery section for the shared mentor document | V1 |  |
| TEAM-02 | ✅ | Plain-language explainer for meetings, saved as a file | V3 |  |
| TEAM-03 | ⏳ | Recruit at least one teammate | V0 |  |
| TEAM-04 | ⏳ | Ask the mentor: group of 2-3 in Q2? Scope of 'replicate, measure, strengthen'? | V0 |  |
| TEAM-05 | ✅ | Do not count on answers from Prof. Huang's group | V3 |  |
| TEAM-06 | ⏳ | Weekly status post | V0 |  |
| TEAM-07 | ✅ | Tailored public goals post in #causal-discovery | V3 |  |

## 13 External outputs

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| EXT-01 | 🔵 | Note to CausalArena's maintainers about column order | V2 |  |
| EXT-02 | ⏳ | Scoreboard submission package with regime and controls stated | V0 |  |
| EXT-03 | 🔵 | Bug report to Causal-Copilot upstream (cycle-step key; empty startup answer) | V0 |  |
| EXT-04 | ⏳ | Paper: evaluations track or workshop | V0 |  |
| EXT-05 | ⏳ | Course website, poster, report | V0 |  |

## 14 Stretch

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| STR-01 | ✅ | E1 Field-wide audit of agents and LLM-assisted methods | V3 |  |
| STR-02 | 🔵 | E2 Public agent track | V0 |  |
| STR-03 | 🔵 | E3 Real experiments via the Causal Chambers remote lab | V0 |  |
| STR-04 | 🔵 | E4 Learned fusion (pretrained network with unreliable tier statements) | V0 |  |
| STR-05 | 🔵 | E5 Hidden confounders, time series, 100+ variables | V0 |  |
| STR-06 | 🔵 | Product angle: auditable causal analyst | V2 |  |

## 15 Decisions

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| DEC-01 | ✅ | Adopt, redirect or enlarge program v2; which of E1-E5 in scope | V3 |  |
| DEC-02 | ✅ | Approve the tier-elicitation test (~900 short calls through Uzair's key) | V3 |  |
| DEC-03 | 🔵 | Whether to tell CausalArena's maintainers about the column order | V0 |  |
| DEC-04 | ✅ | Connect Slack; tracker in private #cd-tracker | V3 |  |

## 15 Risks

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| RSK-01 | 🔵 | LLM-written semantic graphs make names 'work' for the wrong reason (guard: formula + Causal Chambers alongside) | V0 |  |
| RSK-02 | 🔵 | Data-only system may not reach GIES 0.552 (guard: claim targets only where they hold) | V0 |  |
| RSK-03 | 🔵 | Scope too large for one person (guard: decision gates; tracks shrink in fixed order) | V0 |  |
| RSK-04 | 🔵 | Prior work closes the gap first (guard: dated measurements; positioning kept current) | V0 |  |
| RSK-05 | 🔵 | Benchmark files change (guard: dated result; shuffling stays a required control) | V0 |  |
| RSK-06 | 🔵 | Model snapshot changes mid-study (guard: snapshot per call; one per comparison) | V0 |  |
| RSK-07 | 🔵 | Thresholds tuned after seeing results (guard: thresholds in code, hashed plans, held-out split) | V0 |  |
| RSK-08 | 🔵 | Sandbox limits 180 s per step (guard: compute command on Uzair's machine) | V0 |  |

## 16 Bundles

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| BND-01 | ✅ | Ground rules and infrastructure: compute jobs, score contract, frozen splits, ticket hygiene | V3 |  |
| BND-02 | 👀 | Primary sources: literature re-reads, deep reads, method choices | V2 |  |
| BND-03 | 👀 | Paper and code audit: headline claims, methods text, untouched modules, upstream drift | V3 |  |
| BND-04 | ✅ | G1 input: GES and FCI error budgets, SHD definition (no LLM) | V3 |  |
| BND-05 | ✅ | Freeze the Quarter 1 dataset suite | V3 |  |
| BND-06 | 👀 | Remaining baselines, order sensitivity, scoreboard package (no LLM) | V2 |  |
| BND-07 | ✅ | Causal Chambers and intervention audit (no LLM) | V2 |  |
| BND-08 | ✅ | LIVE: Causal-Copilot on CausalArena's named scenarios (old bundle 2) | V3 |  |
| BND-09 | ✅ | Refinement v1 (no LLM): develop and freeze on the dev split | V3 |  |
| BND-10 | ✅ | Refinement v1: held-out test | V3 |  |
| BND-11 | ✅ | LIVE: Refinement v2, names only where the data are silent | V3 |  |
| BND-12 | 👀 | LIVE: second model and external replications | V2 |  |
| BND-13 | ⏳ | Quarter 1 checkpoint package (2 Nov) | V0 |  |
| BND-14 | ⏳ | Quarter 1 final: report, package, one-command reproduction (4 Dec) | V0 |  |

## 12 Team and communication

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| TEAM-08 | ✅ | Atlas v2: the site as a guided sequence of pages (four acts, thirteen pages) | V3 |  |

## 15 Decisions

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| DEC-06 | ✅ | Approve the Atlas v2 page sequence (and whether the market page is public) | V3 |  |

## 13 External outputs

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| EXT-06 | 🔵 | Note to Vashishtha et al. maintainers: triplet answers cut off at 300 tokens (91% of votes lost on gpt-4o-mini) | V3 |  |

## 10 Infrastructure

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| INF-08 | ✅ | Transient OSError EIO on the Docker bind mount: harness writes retry | V3 |  |
| INF-09 | ✅ | Provider quota exhaustion is an infrastructure stop, not an agent failure | V3 |  |

## 5 Targets

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| TGT-18 | 👀 | DV-1 precision > 0.80 at >= 50% coverage, both families, held out (landmark ER-2) | V3 |  |
| TGT-19 | 👀 | Accuracy landmark ER-4a: data-only F1 above GES (route A), or knowledge tiers lift > 0.03 (route B) | V3 |  |
| TGT-20 | 👀 | RCA through the ledger: AC@3 >= 0.90 at coverage >= 0.5 on PetShop held out (landmark ER-4b) | V3 |  |

## 8 Build

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| BLD-15 | ✅ | Audit adapter: other systems' outputs read as typed claims with violation classes | V3 |  |

## 13 External outputs

| ID | | Item | Level | Problems |
|---|---|---|---|---|
| EXT-07 | 🔵 | Note to causal-learn maintainers: PC's Meek step can return a directed cycle (stale ancestor matrix) | V3 |  |
