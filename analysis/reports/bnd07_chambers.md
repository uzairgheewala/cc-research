Tickets: BEN-10, REP-09, BND-07

# BND-07: Causal Chambers mapping, one-layer-deep check, obs+int sample, GES baseline (2026-10-12)

All work ran in the cloud copy (`/home/claude/work/ccr/cc-research`). It made no LLM or API calls, and `Causal-Copilot` was not touched.

**The main limitation is that none of the 8 dataset archives could be downloaded.** The egress proxy refuses the host. Because of this, every result below that needs the data is either missing or built only from the authors' published material, and each one says which. The scripts are written to run on the data once the zips are present; they were tested on synthetic zips (section 7).

## 1. Fetch

- **Data.** `analysis/chambers_fetch.py` tried every `causal_chambers/*` entry of `external/FETCH_REPORT.json`: `directory.yaml` and 8 zips from `https://causalchamber.s3.eu-central-1.amazonaws.com/downloadables/`.
  - All 9 failed with `URLError(OSError('Tunnel connection failed: 403 Forbidden'))`.
  - The proxy's own reason, read with a raw CONNECT, was `request blocked: no rule or allowlist entry allows host "causalchamber.s3.eu-central-1.amazonaws.com"`.
  - Source: `analysis/results/chambers/fetch_status.json`. No sha256 could be checked, and no file exists in `external/causal_chambers/`.
  - I did not look for mirrors of the zips.
- **Documentation.** 26 files came from `raw.githubusercontent.com`, which the proxy allows. They are the 8 dataset READMEs and `variables.csv` files, both validation config tables, three generator scripts, `regimes_targets.py`, and the authors' paper-repository notebooks `case_studies/causal_discovery_iid.ipynb` and `causal_validation.ipynb`. All are in `external/causal_chambers_docs/`, with URL and sha256 in `DOCS_FETCH.json`. No reference hash exists for these files.
- **Paper.** The arXiv HTML of 2404.11341v2 was read through the web-fetch tool. Its text stops in Appendix IV, so the Appendix V text and its Tables 5-8 were not read. The validation procedure and its p-values were taken from the authors' notebook instead.

## 2. Mapping (BEN-10)

Source: `analysis/results/chambers/mapping.json` and `mapping_table.csv`, produced by `analysis/chambers_map.py`.

- **Chamber and configuration.** These come from each README's "Dataset Description" table. All 8 datasets say "standard".
- **Graph.** `causalchamber.ground_truth.main.graph(chamber, 'standard')` from package 0.2.8. The subpackage re-exports only `graph` and `latex_name`; `variables` and `edges` are in `.main`.
- **Columns.** These come from each dataset's `variables.csv`. Every graph variable is a column in every dataset (`graph_variables_missing_from_columns` is empty for all 8).
- **Row counts.** These are the N stated in the README or config table. None were observed, because no zip was available.

| Dataset | Chamber / config | Graph (vars / edges) | Columns not in graph | Experiments (obs / int) | Intervention targets | Rows stated |
|---|---|---|---|---|---|---|
| lt_interventions_standard_v1 | lt / standard | 38 / 57 | timestamp config counter flag intervention camera v_board v_reg | 59 (1 / 58) | single target per experiment, 29 distinct inputs | 68,000 (10,000 reference + 58 x 1,000) |
| lt_validate_v1 | lt / standard | 38 / 57 | same 8 | 29 (0 / 29) | one input each, two-level randomized | 4,300 (N from lt_validation_configs.csv) |
| lt_malus_v1 | lt / standard | 38 / 57 | same 8 | 12 (0 / 12) | pol_1, pol_2 randomized; colour fixed per experiment | 12,000 |
| wt_validate_v1 | wt / standard | 32 / 42 | timestamp config counter flag intervention | 28 (0 / 28) | one input each (21 distinct), two-level randomized | 23,450 (N from wt_standard_validation_configs.csv) |
| wt_intake_impulse_v1 | wt / standard | 32 / 42 | same 5 | 5 (0 / 5) | load_in impulse; hatch random per impulse | not stated unambiguously ("a total of 5000 impulses", 50 rows each) |
| wt_bernoulli_v1 | wt / standard | 32 / 42 | same 5 | 3 (0 / 3) | load_in, load_out set or randomized | 405,000 (5,000 + 2 x 2,000 x 100) |
| wt_changepoints_v1 | wt / standard | 32 / 42 | same 5 | pattern load_in_seed_* (10 seeds) | load_in | not stated |
| wt_walks_v1 | wt / standard | 32 / 42 | same 5 | 5 patterns: random walks, sinusoid/square waves, regime_jumps_single / _multi | time series; regime_jumps have 32 regimes each, regime 0 the reference, targets from regimes_targets.py | 10,000 per walk run; 320,000 per regime_jumps experiment |

**Notes on the mapping:**
- For the two validation datasets, the experiment names derived from the config tables are exactly the names the authors' notebook prints from `available_experiments()`: 29 for lt and 28 for wt (`experiment_names_vs_authors_notebook`).
- The lt_interventions README names the O_1 and O_2 experiments `uniform_osr_1_*` and `uniform_osr_2_*`. In the package, O_1 and O_2 are `latex_name('osr_angle_1')` and `latex_name('osr_angle_2')`, so the mapping takes the targets to be those columns.
- Several sensor-parameter rows of that README list more than one symbol (for example "We set O_1, O_2, O_C = 2"). The mapping takes the single target named in the experiment name and flags this. It has not been checked against the files.
- In every dataset except lt_interventions_standard_v1 and the regime_jumps experiments, every experiment is an intervention, and there is no observational reference.
- Each README's MD5 is recorded in `mapping.json` (`zip.readme_md5`). The FETCH_REPORT sha256 is the checksum the scripts enforce.

## 3. "One layer deep" (BEN-10)

Source: `analysis/results/chambers/one_layer_deep.json`, produced by `analysis/chambers_validate.py`.

- **Structure.** Both standard graphs have longest directed path 1 (`structure`).
  - Every edge runs from a manipulable input to a measured output, and no output has children.
  - Light tunnel: 29 edge sources. Wind tunnel: 21.
  - For every intervened input, children = descendants. So "children vs descendants" coincide, and a non-descendant is any variable that is not a child.
- **What the check means operationally.**
  - Each `validate_<X>` experiment randomizes one input X between two values xA and xB (column `flag` = 0 or 1, drawn per measurement, per `generators/binary_interventions.py`). It holds every other input at the values in the config table.
  - Our check KS-tests every graph variable Z ≠ X between the flag = 0 and flag = 1 rows, with Holm correction at 1% over all tests in a dataset.
  - "One layer deep" means the validation covers exactly the input → output edges, and the graph has no deeper layer.
  - The reference rows are the flag = 0 arm of the same experiment. These datasets contain no observational experiment, so KS "vs observational rows" is not possible.
  - Wind-tunnel edges that have a dedicated experiment (`validate_load_out_pressure_intake`, `validate_hatch_rpms` and so on) are judged on that experiment, as in the authors' notebook (cell 43).
- **Our check on the data (part A): not run.** Both validation zips are absent.
- **The authors' printed p-values (part B).** The notebook prints KS p-values for the edges only, as LaTeX table rows. Those were parsed, mapped back to columns with `latex_name` within each chamber, and Holm-corrected at 1% over the printed edges.

| Graph | Edges printed (= graph edges) | Children that shift (Holm 1%) | Children that do not | Largest p |
|---|---|---|---|---|
| lt standard | 57 (yes) | 57 | none | 6.8e-12 (l_31 → vis_3) |
| wt standard | 42 (yes) | 41 | load_out → pressure_intake, p = 0.082 | 0.082 |

- The next-largest wind-tunnel p-values are 1.7e-5 (osr_downwind → pressure_downwind), 8e-7 (osr_upwind → pressure_upwind), 2.7e-7 (load_out → mic) and 2.5e-7 (load_in → pressure_intake).
- The edge load_out → pressure_intake fails even though its dedicated experiment has 3,000 rows (notebook cell 50 prints `3000`).
- **Non-descendants that shift: not available.** The authors give non-edge p-values only as a heatmap image, and our own test needs the data.
- **Limitations.**
  - Each edge is tested at one fixed setting of the other inputs.
  - Absent edges are not tested in the published tables.
  - Output → output effects cannot be randomized, and the graphs contain none.
  - A shift in a non-descendant would mean either an omitted effect or a contradiction; it could not be told apart from drift without more design.

## 4. Obs+int sample (BEN-10)

`analysis/chambers_sample.py` builds the sample; the rule is in its docstring and in `analysis/results/chambers/sample/README.md`.

- **Rule.**
  - Source: lt_interventions_standard_v1, with the 38 graph variables.
  - Regime 0 is 1,000 rows drawn without replacement from `uniform_reference`.
  - Then, for every other README-listed experiment in sorted name order, up to 100 rows are drawn without replacement.
  - A single `numpy.random.default_rng(20261012)` makes all the draws, and kept rows stay in file order.
  - Targets come from `mapping.json`.
  - The flag `in_authors_a2` marks the authors' 20 task-a2 experiments.
- **Status: not built.** The zip is absent. The folder holds `true_graph_lt_standard.csv` (57 edges, from the package) and `sample_status.json`, which gives the reason.

## 5. REP-09: the authors' GES baseline

`analysis/rep09_ges.py` produces `analysis/results/chambers/rep09_ges.json`.

- **Where the paper reports it.** https://arxiv.org/abs/2404.11341 (v2), Fig. 5, panel a, task a1, and Appendix I.
  - Fig. 5 caption: "GES and PCMCI+ return a set of 12 and 5 plausible graphs".
  - Appendix I, a1: "we take 10000 observations from a subset of the variables".
  - Appendix I, a1: "As score for the algorithm, we use the BIC score with a Gaussian likelihood."
  - The numbers appear only inside the figure. The notebook prints them for the figure (`causal_discovery_iid.ipynb`, cell 27).
- **Protocol, pinned from the notebook.**
  - Data: lt_interventions_standard_v1 / `uniform_reference`, 10,000 rows, raw values (cells 18-19).
  - Variables: 20 (cell 14): red green blue current ir_1-3 vis_1-3 pol_1 pol_2 angle_1 angle_2 l_11 l_12 l_21 l_22 l_31 l_32.
  - Truth: the induced subgraph `graph('lt','standard').loc[vars, vars]` (cell 15), 39 edges.
  - Method: `ges.fit_bic(X, phases=['forward','backward','turning'])` with ges 1.1.0 (cell 23).
  - Metric: directed-edge precision TP/(TP+FP) and recall TP/P for each DAG in the CPDAG (`sempler.utils.all_dags`, cells 10 and 27).

| Quantity | Reported (authors, notebook cell 27) | Ours |
|---|---|---|
| DAGs in the estimated class | 12 | not run (no data) |
| Precision per DAG | .60 .57 .57 .55, repeated three times; range 0.55-0.60 | not run |
| Recall per DAG | .62 .59 .59 .56, repeated three times; range 0.56-0.62 | not run |
| Truth subgraph from package 0.2.8 = authors' printed truth (cell 15 TikZ) | n/a | yes, 39 edges |
| Authors' estimated CPDAG (cell 25 TikZ: 36 directed, 4 undirected) re-scored with our metric code | n/a | 12 DAGs; exactly the printed precision and recall lists |
| CDFM chamber score | 0.727 (second-hand; see below) | not reproduced |

- **REP-09 verdict: not tested.** The data are unavailable in this workspace (`verdict` in `rep09_ges.json`).
  - The pre-stated rule is: supported if every DAG's precision lies in [0.545, 0.605] and recall in [0.555, 0.625]; refuted otherwise, unless explained.
  - The data-free check pins the truth graph and the metric: re-scoring the authors' own CPDAG reproduces their numbers. What remains is the GES run itself.
  - The authors used causalchamber 0.1.1, NumPy 1.24.4 and Python 3.8.10/3.10.12; this workspace has 0.2.8, NumPy 2.5.3 and Python 3.13.16. Their truth subgraph matches the 0.2.8 graph exactly.
- **CDFM.**
  - The value 0.727 is second-hand. The project ledger records "CDFM .727, TabCausal .603, GES .426, PC .281" on Causal Chambers.
  - CDFM's arXiv 2607.11508v1 has a "Causal Chamber" subsection under 6.3 Real-world Benchmark, according to its HTML table of contents. The table itself could not be read with the fetch tool: the HTML was truncated and the PDF returned no text. So the metric, chamber subset and variables are not pinned.
  - **Not reproduced.**
    - The data are blocked.
    - DOM-11 (`analysis/literature/bnd02/dom11_pretrained_models.md`) lists the checkpoint as published on HF `DMIRLAB/CDFM` with a CPU device option. A direct request to `https://huggingface.co/DMIRLAB/CDFM` from this workspace got a 403 on CONNECT, so the checkpoint cannot be loaded here.
    - This differs from the ticket's premise that the checkpoint is unavailable. The block is environmental, not a CPU limitation.
  - CDFM's GES row (.426) uses CDFM's own protocol and is not comparable with the authors' range.

## 6. Contract and checks

- `analysis/results/chambers/CONTRACT.json`:
  - tickets BEN-10, REP-09, BND-07
  - regime D, split "not applicable", supplier `causal_chambers`
  - per-file entries; only `rep09_ges.json` is score-bearing
  - `metric_defs` and `orientation_rule` follow the authors' per-DAG enumeration
- `python analysis/check_scores.py` reports: `chambers ok`, nonconforming none, 3,750 rows checked. It rewrote `analysis/results/score_contract_report.json`.
- `pyflakes` reports nothing on the 5 new scripts.

## 7. Testing without the data

A scratch harness (not in the repo) built synthetic zips for lt_validate_v1, wt_validate_v1 and lt_interventions_standard_v1, linear-Gaussian on the package graphs. It redirected `chambers_io` to them. On these zips, all three data paths ran:

- Part A produced KS tests, Holm and the edge → experiment assignment. The dedicated wind-tunnel experiments resolved correctly.
- The sample builder produced 1,200 rows over 3 regimes, and `uniform_osr_1_weak` mapped to target `osr_angle_1`.
- GES ran through the `np.Inf` shim and enumerated the class, and the verdict logic executed.

These synthetic numbers mean nothing about the chambers and are not reported as results.

## 8. Versions

Python 3.13.16, numpy 2.5.3, scipy 1.18.1, pandas 3.0.5, causalchamber 0.2.8 (wheel in `external/causalchamber_pkg`, installed with `--no-deps`, plus termcolor and tqdm), ges 1.1.0, sempler 0.2.13 (the authors' pinned version, installed from PyPI for `all_dags`).

## 9. Not done, and why

| Item | Reason | What unblocks it |
|---|---|---|
| Download and sha256 check of the 8 zips and directory.yaml | proxy: no allowlist entry for `causalchamber.s3.eu-central-1.amazonaws.com` | allowlist the host, or copy the zips (already on Uzair's machine per the project ledger) into `external/causal_chambers/` |
| Observed row counts and experiment lists in `mapping.json` | no zips | rerun `chambers_map.py` |
| One-layer-deep check on the data (part A: children, non-descendants) | no validation zips | rerun `chambers_validate.py` |
| Obs+int sample files | no lt_interventions zip | rerun `chambers_sample.py` |
| GES run and REP-09 verdict | no lt_interventions zip | rerun `rep09_ges.py` (about 10,000 x 20; expected to take seconds to minutes) |
| CDFM 0.727 | data blocked; huggingface.co blocked; CDFM's chamber protocol not pinned | read CDFM Sec. 6.3 table; allow HF |
| Appendix V text and Tables 5-8 | arXiv HTML text truncated before Appendix V | read the PDF or the Nature version |

## 10. Data run on Uzair's machine (2026-10-12): this section supersedes the "not done" rows above that depended on the data

The datasets were already on Uzair's machine, extracted by `harness/fetch_external.py` on 7 Oct (each zip's sha256 was verified
against `external/FETCH_REPORT.json` at download; the zips were not kept). `chambers_io.py` now reads the extracted folders
(status "extracted") when no zip is present; the 174 CSVs read are hashed in `manifests/evidence/chambers_extracted_2026-10-12.sha256`.
Run on Uzair's machine: Python 3.10.12, numpy 2.2.6, scipy 1.15.3, pandas 2.3.3, ges 1.1.0, sempler 0.2.13, causalchamber 0.2.8.

- Mapping (`analysis/results/chambers/mapping.json`): every dataset re-run with observed rows per experiment.
- One layer deep, our check on the data (`one_layer_deep.json`, part A; KS between the two `flag` groups of each validate
  experiment, Holm at 1% over all tests of a dataset):
  - light tunnel: 57 of 57 children shift; 0 of 1,016 non-descendant tests shift.
  - wind tunnel: 40 of 42 children shift; 0 of 774 non-descendant tests shift. Not shifting: load_out -> pressure_intake
    (p = 0.082, as in the authors' printed table) and osr_downwind -> pressure_downwind (p = 1.7e-5; significant alone, not
    after Holm over 868 tests; the authors' table, corrected per edge, counts it).
  - No shift anywhere contradicts the graphs (no non-descendant moves).
- Obs+int sample built: `analysis/results/chambers/sample/obs_int_sample.{csv,npz}`, 6,200 rows over 53 regimes (1,000
  uniform_reference rows plus up to 100 per other experiment, seed 20261012).
- REP-09 SUPPORTED (`rep09_ges.json`): GES (BIC, forward/backward/turning) on uniform_reference, 10,000 rows, the authors' 20
  variables returns a CPDAG identical to the authors'; its 12 DAGs give precision 0.55-0.60 and recall 0.564-0.615, inside the
  reported 0.55-0.60 / 0.56-0.62.
- CDFM 0.727: still not reproduced (checkpoint only on huggingface.co, blocked; its chamber protocol not pinned).
