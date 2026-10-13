# AB-02 / AB-12 data scouting (AUD-34, AUD-43)

Written 2026-10-12. Everything here was verified on primary pages; nothing was downloaded. The machine-readable version is `AB02_AB12_data_scouting.json`. Rows already typed in `AU2_benchmarks.*` are referenced, not re-typed. Where a size is "not stated", no page we could read gave it, and we do not guess.

## Recommendation

### AB-02: a second scoreboard (not CausalArena)

**1. Bayesys repository + Constantinou et al. 2021 (fit 3).** This is the only candidate that clearly meets all three conditions.

- **Released data:** fixed CSVs, `DATA/<NET>_DATA.csv` with 100k rows. The study scored the first 0.1k to 1000k rows. There are also noise-variant ZIPs.
- **Ground truth:** `graphs/DAGtrue_<NET>.csv`, plus MAGs for the latent-variable variants.
- **Published scores:** per algorithm × network × noise × sample size, for F1, SHD, BSF, precision and recall. They are in appendix tables D1–D5 of [arXiv 2005.09020](https://arxiv.org/abs/2005.09020) and in the raw file `http://constantinou.info/downloads/bayesys/results/results_noisyPaper.xlsx`.
- **Methods scored:** PC-Stable, FGES, FCI, GFCI and RFCI-BSC (all via Tetrad r-causal 1.1.1), plus 10 others.
- **Order-effect reference:** a companion paper on the same networks, Kitson & Constantinou ([2206.08952](https://arxiv.org/abs/2206.08952)). It moved columns from worst order (reverse-topological) to optimal (topological) and measured the F1 change: +0.036 for PC-Stable and +0.412 for HC. Their generated data defaults to alphabetical order.
- **Caveats:**
  - The header order of the released Bayesys CSVs is not documented, so check it on download.
  - The primary host `constantinou.info` is outside the sandbox allowlist. Use the Zenodo mirror [7682867](https://zenodo.org/record/7682867), whose contents are unread (HTTP 429), or have Uzair fetch the files by hand.
  - Variable names are meaningful and partly memorised (Asia, Alarm), so do not use this set for LLM arms.
  - Licence: CC BY-SA 4.0 (repository report).

**2. gCastle PCIC 2021 real alarm datasets (fit 2).**

- **Files:** three tarballs on GitHub, which the sandbox can reach. Each holds `Alarm.csv` and `DAG.npy`; 24V and 25V also hold `Topology.npy`. The md5 sums are pinned in `castle.datasets.builtin_dataset`.
- **Published scores:** the `gcastle-hub/dataset` README has an F1 table. PC scores 0.4299 / 0.2270 / 0.1923 and GES 0.3393 / 0.3054 / 0.2008 on 18V / 24V / 25V. PCMCI, THP and five other methods are also in the table.
- **Licence:** MIT.
- **Risks:**
  - The data is an event sequence, so PC/GES need an event-to-table binning step. That step is undocumented, which makes reproduction uncertain.
  - Variable order is an anonymised alarm-ID index, and its relation to causal order is unknown.
- **Bonus:** `Topology.npy` is a declared device topology, which bridges to AB-12.

**Alternate: CIPCaD-Bench (fit 2).**

- It covers Tennessee Eastman (33 variables × 1,500 rows) and a food plant (17 variables × 23,132 rows).
- PC, GES and FCI are scored, but the full per-method table is only an image (Fig. 4).
- The repo shows no licence.

### AB-12: RCA vertical probe

**Primary: PetShop** ([2311.04806](https://arxiv.org/abs/2311.04806); [repo](https://github.com/amazon-science/petshop-root-cause-analysis), archived 2025-11-11; data CC BY 4.0, code Apache-2.0). It is the only candidate that releases a declared call graph.

- **Contents:**
  - `scenario/graph.csv`: an X-Ray service-call adjacency matrix.
  - `noissue/metrics.csv`: a normal period, which lets abstention be scored.
  - 68 issues split into `train/` and `test/`, each with `metrics.csv` and `target.json`.
- **Published baselines:** top-3 recall for graph-requiring methods (traversal, CIRCA, counterfactual) and graph-free ones (ε-diagnosis, RCD, correlation). The authors note that every method also names root causes during normal operation, which is exactly the abstention gap.
- **Not evaluated:** BARO and PC-PageRank, so we would add them ourselves.
- **Smallest slice:** the low-traffic scenario (26 issues) plus `noissue`.

**Second slice: RCAEval RE1-OB.**

- **File:** 31.0 MB on Zenodo [14590730](https://zenodo.org/records/14590730), with 125 cases.
- **Published baselines:** the ASE'24 companion paper ([2408.13729](https://arxiv.org/abs/2408.13729), Table 5) gives Avg@5 on the same Online Boutique data:

  | Method | Avg@5 on Online Boutique (cpu / mem / disk / delay / loss) |
  |---|---|
  | PC-PageRank | 0.34 / 0.15 / 0.32 / 0.33 / 0.38 |
  | BARO | 0.94 / 0.99 / 0.87 / 0.99 / 0.60 |

  The same table has 19 other methods, including FCI-, fGES-, Granger- and LiNGAM-PageRank, CIRCA, RCD and CausalRCA. CIRCA was run on a PC-built graph because no call graph was available.
- **Loader:** `pip install RCAEval[default]` (v1.8.0, 2026-09-29).
- **No topology file is released.** Either write the declared graph from the Online Boutique architecture, or derive it from traces in RE3-OB (190.8 MB, 30 cases).

### Download plan

| What | URL | Size |
|---|---|---|
| Bayesys data + DAGs (ASIA, ALARM, SPORTS, PROPERTY; N variant first) | https://zenodo.org/record/7682867, or http://www.constantinou.info/DOWNLOADS/Bayesys/DATA/ and /graphs/ (off-allowlist) | not stated; check the Zenodo file list first |
| Bayesys raw scores | http://constantinou.info/downloads/bayesys/results/results_noisyPaper.xlsx (off-allowlist, manual) | not stated (one XLSX) |
| gCastle alarm sets | https://raw.githubusercontent.com/gcastle-hub/dataset/master/alarm/{18V_55N_Wireless,24V_439N_Microwave,25V_474N_Microwave}.tar.gz | not stated (md5 pinned) |
| PetShop | https://github.com/amazon-science/petshop-root-cause-analysis | not read |
| RCAEval RE1-OB | https://zenodo.org/records/14590730/files/RE1-OB.zip | 31.0 MB |
| (optional) RCAEval RE3-OB, traces | https://zenodo.org/records/14590730/files/RE3-OB.zip | 190.8 MB |
| Loaders | `RCAEval[default]==1.8.0`, `fse-baro==0.2.2`, `gcastle==1.0.4` | packages |

## AB-02 candidates

The three conditions:

- **c1:** the exact scored files are released, with ground-truth graphs.
- **c2:** per-method scores are published.
- **c3:** PC, GES or FCI is among the scored methods.

| Candidate | c1 | c2 | c3 | Column order | Licence | Fit |
|---|---|---|---|---|---|---|
| Bayesys + Constantinou 2021 | yes | yes (D1–D5 + XLSX) | PC-Stable, FGES, FCI | undocumented; generated bnlearn data defaults to alphabetical | CC BY-SA 4.0 | **3** |
| gCastle PCIC 2021 alarm | yes (event data) | yes (README F1) | PC, GES | alarm-ID index, unknown vs causal order | MIT | **2** |
| CIPCaD-Bench | yes | image only (Fig. 4) | PC, GES, FCI | unknown | none shown | 2 |
| Causal Chambers | yes | plot (Fig. 5a) + notebook | GES | named, instrument order; depth-1 graphs | CC BY 4.0 | 2 |
| CausalBN-Bench (Zhou, "LLM CausalBench") | not confirmed (26 GB, mostly prompts) | SHD only (Table VI) | PC, GES | unknown | CC BY 4.0 | 1 |
| CSuite | yes | no discovery scores on CSuite | PC scored elsewhere | X0..Xn; check triangularity | MIT (archived) | 1 |
| causalAssembly | partial (regenerated per run) | plots only | PC-stable | likely topological (paper orders by layer and causal order) | AGPL-3.0 | 1 |
| CausalTime | data page blocked | Table 3 AUROC | PCMCI only | first N columns causal, next N residual | not stated | 1 |
| CausalRivers | yes | Tables 3/7/8 + leaderboard | PCMCI only | station IDs | dl-de/by-2-0 | 1 |
| CausalBench-GSK (Chevalley) | no true graph | yes | PC, GES, GIES | n/a | Apache-2.0 / CC BY 4.0 | 1 |
| OCDB | anonymous link | Table 3 | none | not read | not stated | 0 |
| cdt datasets | yes | no table | — | see AU2 | MIT | 0 |
| bnlearn as used by Kıcıman et al. | no (own samples) | no PC/GES/FCI rows | — | alphabetical | varies | 0 |
| NeurIPS 2023 CSL (csl_espk) | truth release unconfirmed | none found | — | alarm IDs | MIT | 0 |

## AB-12 candidates

| Candidate | Data and size | Declared topology | Metrics | Baselines with numbers | Licence | Loader |
|---|---|---|---|---|---|---|
| **PetShop** | GitHub repo; byte size not read; 68 issues, 41 components | **yes**, `graph.csv` (X-Ray) | top-1/top-3 recall | traversal, CIRCA, counterfactual, ε-diagnosis, RCD, correlation (Table 3) | CC BY 4.0 data | none (repo scripts) |
| **RCAEval** | Zenodo zips: RE1-OB 31.0 MB, RE1-SS 79.1 MB, RE1-TT 279.7 MB, RE2-OB 1.2 GB, RE2-SS 245.6 MB, RE2-TT 2.8 GB, RE3-OB 190.8 MB, RE3-SS 101.5 MB, RE3-TT 241.7 MB (5.2 GB zipped, ~38 GB unzipped); HF Parquet 3.4 GB | no (traces in RE2/RE3 OB and TT) | AC@k, Avg@k (+Chance@5, Lift@5) | WWW'25 Table 6 (RE2-TT): BARO 0.80, CIRCA 0.46, CausalRCA 0.43, RCD 0.13. ASE'24 Table 5: PC-PageRank vs BARO vs 19 others | MIT (README/HF) vs CC BY 4.0 (Zenodo): conflict | `pip install RCAEval[default]` 1.8.0; `fse-baro` 0.2.2 |
| Nezha | in repo, size not stated; OB 56 faults, TT 45 faults | no (raw traces) | AS@k, AIS@k | Nezha only | MIT | none |
| LEMMA-RCA | HF preprocessed: Product Review 6.66 GB, Cloud Computing 4.74 GB; raw 765/540 GB | no | PR@K, MAP@K, MRR | PC-based, CIRCA, ε-Diagnosis, RCD, BARO, Nezha (Tables 3–6) | CC BY-ND 4.0 (HF metadata says BY-NC: conflict) | none |
| Fang et al. 2025 (TrainTicket, 1,430 cases) | release location not found | not stated | Top@k, Avg@k, MRR | BARO Top@1 0.36, MicroRCA 0.37, CausalRCA 0.22, SimpleRCA 0.28 | not found | ClickHouse schema |
| AgenticOpsEval RCA100 / AIOps2025 (Jun 2026) | aiops.cn GitLab (off-allowlist); 3.4 GB / 11.9 GB | RCA100 only | composite, agent-oriented | none | RCA100 CC BY-NC-SA 4.0 | none |
| OpenRCA (second-hand) | ~64 GB | no | Accuracy@k | PC, FCI, Granger, LiNGAM all 0 on Market CB1 (via 2607.13548) | not read | not read |

**Why PetShop and RE1-OB together.** AB-12 compares three things: RCA on a learned graph, RCA on the declared topology, and abstention.

- **PetShop** supplies the declared graph and a normal period on which to score abstention. Its published numbers already show graph-requiring methods (CIRCA, traversal) beating graph-free ones on latency faults. CIRCA also collapses to 0.00 on high-traffic availability faults, a failure we should foresee.
- **RE1-OB** supplies the published learned-graph baseline: PC-PageRank at 0.15–0.38 Avg@5 against BARO at 0.60–0.99, on one small system. Together the two cover both arms at under ~50 MB of known size, plus PetShop's unread repo size.

## Not read

| Source | Why |
|---|---|
| Zenodo 7682867 | HTTP 429; told not to retry |
| Bayesys results XLSX | binary, not opened |
| PetShop `dataset/` tree and gcastle-hub `alarm/` tree | robots.txt; the GitHub API is not enabled for this session |
| causaltime.cc dataset page | robots.txt |
| CausalRivers leaderboard | rendered by JavaScript |
| BARO paper experiments section | truncated fetch |
| 2510.04711 Data Availability section | outside the fetched window |
| CIPCaD Fig. 4 | image |
| LEMMA-RCA "Original" HF sizes | not opened |
| OpenRCA primary sources | not opened |
| causalAssembly `data/` folder | not listed |
| IDI baseline table | not read |

Full list with reasons: `not_read` in the JSON.
