# Causal-Copilot research ledger (DSC 180A/B, D04)

Living record. Update in place; never silently drift. Labels: PAPER CLAIM / README CLAIM / CODE VERIFIED (static read unless "executed" or "live") / PARTIAL / DIVERGENT / UNCLEAR.
Baseline: repo main at a31aa7c (2026-05-15, 638 commits). Paper: arXiv 2504.13263v2 (21 Apr 2025).
Last update: 2026-10-07 late (turn 14). Bundle 1 is closed (54 runs, 45 completed; verdicts unchanged by the top-up). Causal Chambers data downloaded. New no-LLM measurements: identifiable ceilings, an error budget for PC, the value of order knowledge. Uzair asked to restructure and go "much farther and much deeper"; proposal written as `analysis/reports/program_v2.md` (order provenance; claim ledger; four tracks). WAITING on Uzair: adopt or redirect program v2; approve the knowledge-elicitation calls (A3); decision on telling CausalArena's maintainers about the column order.

Companion project docs:
- `claude/causal-copilot-ceiling-and-positioning.md`: what "perfect" can mean, measurement axes, ladder, value, paper shapes.
- `claude/causal-vs-worldreset-weighing.md`: course constraints from the slides, weighing against the forecasting project.
- `claude/benchmark-targets.md`: CausalBench, CausalArena, Causal Chambers, CausalRivers; numbers to beat.
- `claude/shared-doc-causal-section-plan.md`: structure plan for the Causal Discovery section of the shared mentor document.
- `claude/shared-doc-causal-section-draft.md`: the section text, draft v2 (2026-10-07).
- `claude/bundle1-results.md` and `claude/bundles-2-5-design.md`: copies of the two reports written in turn 13 (originals in `cc-research/analysis/reports/`). The second is superseded as the organising plan.
- `claude/program-v2-order-provenance.md` and `claude/error-budget-and-order.md`: copies of the two reports written in turn 14.

Where the detail lives (Uzair's folder `DSC 180A/cc-research/`): `analysis/README.md` is the index; reports in `analysis/reports/` (pass3, pass4a, pass4b_design, pass4b_results, pass5, pass6, pass7, bundle1_design, bundle1_results, bundle2_onward_design, error_budget_and_order, program_v2); results in `analysis/results/`; five unedited literature agent reports in `analysis/literature/agent_reports/`.

## Environment facts
- Local tree at Documents/UCSD/Fall 2027/DSC 180A/Causal-Copilot is a GitHub zip unpack: full working tree, 1,332 files, NO .git.
- Identity (executed, re-checked in turn 9): byte-identical to commit a31aa7c (0 missing, 0 changed, 0 unexpected extra files) apart from the Windows-unpacked name of `externals/pyCausalFS/CBD/output/indicator.txt`.
- Baseline manifest: `cc-research/manifests/baseline_a31aa7c.sha256`; its own sha256 is 725e06274856c2187c2a650b1a7217968d633c03baca292609d505e4429fbacf (hard-coded in harness/cc_common.py). Every run verifies the tree first.
- `.env` in repo root: LLM_PROVIDER=openai, LLM_MODEL=gpt-4o; the key is set (by Uzair). Claude must never open or print this file.
- Files a run writes into the repo: `output/<data>/<timestamp>/...` and `causal_discovery/context/hp_rerank_prompt_test.txt`. Nothing else (confirmed live, 30 runs).
- Docker images on Uzair's machine: `causal-copilot-cpu:a31aa7c` (base) and `cc-research:a31aa7c-1` (runtime). Served model snapshot in every live run so far: gpt-4o-2024-08-06.
- `cc-research/runs` holds 85 run folders (84 live, 1 stub). `cc-research/external/` holds the CausalArena snapshot (1.57 GB) and 8 extracted Causal Chambers datasets (115 MB).
- Code identity re-checked after the top-up (2026-10-07): all 1,332 tracked files match the manifest; no run left an unexpected file.
- Claude's sandbox on Uzair's machine: Python 3.10.12, 2 CPU, 3.9 GB RAM, no PyTorch (mock only), each shell call limited to 180 s, background processes die with the call. Reachable: PyPI, github.com. Blocked: api.openai.com, huggingface.co, causalchamber.org and its S3 bucket. Two pipelines at once exhaust its memory. Its speed varies a lot (in turn 9 a 30 s stub run later took over 150 s with nothing else changed), and the mount of the DSC 180A folder dropped once and came back; a killed `timeout` can leave orphan child processes. A venv, a repo copy and dev copies exist under the sandbox home; they may vanish with the session, and everything needed is also in `cc-research/`.
- Cloud container: cannot reach GitHub, Hugging Face or causalchamber.org; not usable for running the repo. A local copy of this ledger is kept at /home/claude/ledger.md for patching (session-scoped).
- Rules: no git commands that touch the index on mounted repos. Investigation only so far; no refactor, no behaviour change to Causal-Copilot; analysis artifacts live outside the repo. Claude cannot delete files in the mounted folder.

## Course constraints (from `L0 - Intro.pdf`)
- Domain fixed for two quarters; both projects are inside D04. TA for D04: Nate. TA check-ins 19-23 Oct and 20-25 Nov 2026.
- Quarter 1 project (50%): replication-style exploration; checkpoint Mon 2 Nov, final Fri 4 Dec 2026.
- Quarter 2 proposal (15%): written proposal, weekly schedule, 2-3 minute pitch; mentor approves. Quarter 2 project in groups of 2-4 chosen by the mentor; deliverables: public repo, website, PDF report, poster; showcase 2nd week of March 2027.
- Participation 15%, of which 10% is mentor-assigned.

## Harness (`cc-research/`, version 3)
- `cc.ps1`: build | preflight [nollm] | dryrun | golden | plan <file> | fetch | queue | stop | shell. `fetch` ran on Uzair's machine on 2026-10-07 (works).
- `harness/`: cc_common.py, cc_trace.py, preflight.py, run_traced.py, run_plan.py, stub_llm.py, fetch_external.py. Mounted into the container, so edits take effect without a rebuild.
- Plans: datasets under the repo or `research:datasets/...`; `"interleave"`; `"run_timeout_s"` (300..10800, can only shorten the limit).
- `fetch_external.py`: downloads the CausalArena snapshot (Hugging Face, LAMDA-Tabular/CausalArena, CC-BY-4.0) and a few tabular Causal Chambers datasets plus their directory.yaml into `external/`, with size limits, checksum checks and `external/FETCH_REPORT.json`. First real run (2026-10-07): 6,364 CausalArena files fetched; all 5 Causal Chambers archives failed because one shared size allowance was used up by CausalArena. Fixed in turn 13: allowance per source (CausalArena 300 MB/file, 1.5 GB; Causal Chambers 800 MB/file, 2.5 GB), Causal Chambers first, archive sizes requested before download and written to the report, CausalArena synthetic samples excluded by default (`--skip-regex`). Checks F1-F18 pass against the stand-in server. Rerun by Uzair 2026-10-07 20:53 UTC: 0 errors; extracted lt_interventions_standard_v1 (59 CSV), lt_validate_v1 (29), wt_validate_v1 (28), wt_intake_impulse_v1 (5), wt_bernoulli_v1 (3), wt_walks_v1 (28), wt_changepoints_v1 (10), lt_malus_v1 (12). Archive sizes of all 20 datasets are in `external/FETCH_REPORT.json` (tabular ones 0.1-49 MB; image ones 46 MB-4.8 GB, not fetched).
- A run directory holds: SUMMARY.txt/summary.json, meta.json (incl. dataset_identity), llm_calls.jsonl (each record has `api`: a LIST of SDK-level request/response records), events.jsonl + artifacts/*.pkl, state/NN_<stage>.pkl|json, rng_initial_states.pkl, console.log, pipeline_output/. About 20-36 MB per run.
- Loading artifacts/state pickles needs the repo root and externals/causal-learn on sys.path.
- A failed run is recorded with the failing repo file:line and the plan continues.

## Analysis tools (`cc-research/analysis/`) and gates
- `lineage.py`: per-edge lineage of one run; gates A-F. Passed for all 27 completed live runs.
- `refinement_offline.py` + two report scripts: refinement steps without the LLM; gate S1.
- `llm_inventory_scan.py` / `_build.py`: gates G1-G4.
- `encoding_consumers.py`: micro-tests per edge code.
- `make_datasets.py`: pass 4b datasets (gates D1-D5). `make_suite.py`: bundle-1 suite (gates D1-D7).
- `stability.py`: cross-run stability and name-versus-data, per arm and per dataset family (roles real / neutral / swapped); gates T1-T6; predictions P1-P5 (pass 4b) and N1, N2, N4, N5 (families) with thresholds fixed in code; reproduces every pass-4b verdict (regression check, turn 9).
- `partial_stages.py` (turn 13): scores through S3 for every run that reached refinement, including cycle-step crashes; cycle-step call log; gates Q1-Q3.
- `causalarena_io.py`, `causalarena_pc_calibration.py`, `causalarena_order_baseline.py` (turn 13): reader and scorer for CausalArena files (their `g[i,j]=1` means column i causes column j, the transpose of the repo's convention), PC calibration (gates C1, C2), column-order check.
- `error_budget.py`, `order_value.py`, `causalarena_sortability.py` (turn 14): ceilings per scenario and the PC budget (gates B1, B2 pass), value of oracle tier knowledge, R2-sortability and R2-SortnRegress.
- `cc_graph.py`: encoding helpers, CPDAG of a DAG, scoring. Since turn 9 `score` also returns directed-edge precision/recall/F1 against the true DAG (the convention of DAG-level scoreboards).

## Bundled datasets (data/dataset)
- Ground truth + symbolic names: Linear_Gaussian (n=1000, p=5), Linear_Nongaussian, 2024..._Linear-Non-gaussian (n=1000, p=10), NetSim, Finance1-9, fMRI, Cad.
- Reference graph + semantic names: sachs (n=853, p=11, 19 edges), Abalone (4177, 8; star Age -> 7), Auto_mpg (392, 5; 5 edges), CCS_Data (1030, 9; star 8 -> Compressive strength), DWD (349, 5; 4 edges). For all of them `ref[i,j]==1` means j -> i (checked edge by edge). CORRECTED turn 13: Abalone (8/7/4,177), Concrete (9/8/1,030) and DWD (5/4/349) match an entry of CausalArena's real-data index in variables/edges/rows; Auto MPG does NOT (CausalArena: 4 variables, 3 edges, 398 rows). CausalArena does not republish the real tables, so identity cannot be confirmed.
- No truth: Ozone, earthquakes, heart_disease, onlineshop. Time series: sim_ts.
- Loader caveat: a directory path needs `--data_mode simulated`; with a CSV path ground truth is not loaded.

## FACTS (code verified at a31aa7c)
F1. Entry points: `main.py` (CLI, discovery only, 8 steps), `web_demo/demo.py` (Gradio, full pipeline), `web_demo/demo_inf.py`, `causal_inference/main.py`.
F2. State: `GlobalState` = UserData, Statistics, Logging, Algorithm, Inference, Results. Mutated in place. Persisted only by the web demo.
F3. LLM choke point: `llm/llm_client.py::LLMClient.chat_completion`; default model gpt-4o-mini; temperature default 0.0; JSON mode is `json_object` only (no schema enforcement).
F4. Core discovery-path LLM calls in order: query->JSON (Initialize_state.py:158); domain knowledge prose x2 (preprocess/dataset.py:121,138); filter (filter.py:33); rerank (rerank.py:103); hyperparameters (hyperparameter_selector.py:104); per-node edge review (judge_functions.py:288); cycle breaking (judge_functions.py:556); report prose; discussion.
F5. Knowledge memory = text/JSON files in `causal_discovery/context/`, all consumed as prompt text.
F6. Algorithm inventory mismatch: wrappers `__all__` lists 27 names, 25 imported, 20 have profiles. No wrapper uses interventional data except CD-NOD through a domain index.
F7. Graph encoding: M[i,j]=1 means j->i; 2 undirected, 3 bidirected, 4 o->, 5 o-, 6 o-o, 7 associated. Symmetric marks stored in one cell only; which cell depends on the wrapper.
F8. Postprocess order (`Judge.quality_judge`): bootstrap (boot_num=20, `random.choices`, main process on the CLI) -> buckets on DIRECTED-edge frequency only (>=0.9 add, <=0.1 delete) -> LLM review -> marginal KCI pruning (a KCI test for EVERY pair on the full data) -> LLM cycle break.
F8a. The bootstrap resamples are the same every run: importing the pipeline imports `semopy` (via lingam), whose `model_generation/parameters.py:22` calls `random.seed(123)`. Confirmed live (one initial generator state in all 28 pass-4b runs; XGES gave one bootstrap table across repeats). numpy's generator is not seeded: FCI with `rcit` gave 2-3 distinct outputs across 3-5 runs on byte-identical data.
F9. Every unordered pair incl. self-pairs is queued for LLM review (executed, offline, live). Cause: judge_functions.py:236.
F10. `fixed_pairs = []` (judge.py:88) is never populated.
F11. The edge-review prompt carries no bootstrap probabilities on the first pass (judge.py:95 passes None), so the LLM review sees names and knowledge text, not data.
F12. `results.prior_knowledge` is written and never read.
F13. hyperparameter_selector.py:110 keeps only primary params. Live: on every run with real protein names the LLM proposed `background_knowledge`; dropped with no trace. Not proposed with neutral names.
F14. No LLM error-recovery loop.
F15. KCI pruning and cycle removals are not recorded in state. LLM A/B/C answers are in `results.llm_errors` (D answers are not).
F16. Tests: 3 string-presence asserts; CI = ruff + pytest + compileall.
F17. `benchmarking_integrated.py` scores `results.converted_graph` and never calls Judge.
F18. Benchmark data dir `simulated_data/heavy_benchmarking_v6` is not in the repo.
F19. `results.revised_metrics` is never assigned; the revised graph is never scored by the code.
F20. Any A/B answer from the edge review is applied as a directed edge, even where the algorithm found no adjacency.
F21. `kci_pruning` removes only edges stored in cells with row index < column index.
F22. Environment bugs (not research gaps): psutil missing from requirements_cpu.txt; `report/report_generation.py:9` imports latexmk at import time.
F23. (micro-tests) each non-directed code (2-7) is deleted by the bootstrap step even at 100% resample frequency; code 7 is not counted by the tally and reaches the LLM as an empty sentence; a triangle of undirected edges in mixed cells triggers the LLM cycle helper.
F24. `Judge.evaluation` (judge.py:232-259) uses causal-learn metrics for PC, FCI, GES, CDNOD and a flat cell comparison for all others; the same undirected edge scored SHD 0 / F1 1.0 from PC and SHD 1 / F1 0 from XGES.
F25. `causal_inference/inference.py:65` builds its graph from `results.revised_graph`.
F26. LLM inventory: 51 request-issuing call sites; 88 logical LLM points; 29 decision points (12 unchecked, 14 not examined, 3 partial check); 3 points edit the graph directly. Gates G1-G4 pass.
F27. The knowledge prompt contains the dataset file path; the elicited knowledge prose is pasted into the filter, rerank, hyperparameter and edge-review prompts.
F28. (live) Crash points on malformed LLM JSON: `Initialize_state.py:178` (`KeyError: 'linearity'` when the query-parse call returns `{}`; 2 of 28 runs on a byte-identical request) and `judge_functions.py:562` (`KeyError: 'nodes'`; 1 run, cycle Plcg->PIP3->PIP2->Plcg created by LLM-added edges).
F28a. (live, all 78 runs) The cycle step has crashed every time it was entered: 8 of 8 (1 in pass 4b, 7 in bundle 1). The prompt names no key; the code reads `response['nodes']`; the model answered `edge_to_remove` (5) or `nodes_to_remove` (3). The init crash (`'linearity'`) occurred 3 times in 78 runs.
F28b. (code + live) `check_cycle` (judge_functions.py:566-575) clears the mirror cell of every 1 and then treats EVERY remaining non-zero cell as an arrow, whatever its code. In 4 of the 7 bundle-1 cases the cycle exists only under that reading; committed directions alone are acyclic.
F29. (live) The identical first request (28 runs, same snapshot and fingerprint, temperature 0) received three different answers: full JSON x24, two fields null x2, `{}` x2.
F30. (live) The knowledge text named the "Sachs dataset" in 4 of 4 runs whose path contained "sachs", and in 0 of 9 runs with real protein names but a neutral path. With neutral names it was "No Knowledge" in 5 of 5.

## LIVE RUNS
Golden (one run each): Linear_Gaussian -> XGES, correct undirected edge deleted by the bootstrap step, final graph empty. sachs -> FCI, all 10 edges deleted, LLM wrote 6 directed edges, final adjacency F1 0.40 vs 0.62.

Pass 4b (2026-10-06 13:44-15:23 UTC): 28 runs, 25 completed, 3 failed (F28). 1,434,644 prompt + 170,413 completion tokens, 97 min. Gates T1-T5 pass.
- P1 SUPPORTED (d03: 27 LLM-set edges follow labels only, 0 data only, 10 neither; by distinct edge 6 / 0 / 2, below the n=10 the rule asked for). P2 SUPPORTED (LLM-set edges per run: d02 0, d01 6.3). P3 SUPPORTED (18 of 119 non-directed edges survive = 15%; directed 7 of 7). P4 exploratory: 0.53 with "sachs" in the path (n=4) vs 0.44 without (n=3), not separable. P5: algorithm and hyperparameters never varied within an arm.
- Adjacency F1, S0 -> S1 -> final: sachs 0.61 -> 0.17 -> 0.53; d01 0.63 -> 0.19 -> 0.44; d02 0.62 -> 0.10 -> 0.10; d03 (by data) 0.60 -> 0.11 -> 0.01, by label final 0.41; Linear_Gaussian 1.00 -> 0.00 -> 0.00; LiNG 0.33 -> 0.12 -> 0.12. Final below S0 in 25 of 25 completed runs.
- Directed-edge F1 on the sachs arm (DAG-level scoreboard convention): algorithm output 0.00, final 0.37. The two metrics move in opposite directions.
- Orientation: sachs arm final has 4.8 reference edges directed correctly and 1.8 reversed per run; distance to reference CPDAG 19.8 -> 16.2; d03 20.2 -> 26.4.
- d03 every run: the same seven textbook edges written between labels whose data belong to other proteins. d02: D for all 275 pair questions.
- Stability: LLM edge answers identical across runs for 33/55 (sachs), 35/55 (d01), 41/55 (d03) pairs. Named arms diverge at the filter stage because the knowledge prose differs every run.

## OFFLINE EXPERIMENT (no LLM; wrapper-default hyperparameters)
- Seed 0: 113 cells, 96 completed. Seeds 1-2: 140 cells, all completed.
- Survival through the bootstrap step, seed 0: directed 96%, undirected 16%, o-o 12%, bidirected 12%, circle-arrow 25%.
- Adjacency F1 S0 -> S1: PC 0.86->0.44, GES 0.88->0.35, GRaSP 0.88->0.34, XGES 0.87->0.43, FGES 0.82->0.40, FCI 0.85->0.30, DirectLiNGAM 0.76->0.76. Worse in 50 of 51 CPDAG/PAG combinations in every seed; never better.

## BUNDLE 1 (live 2026-10-06/07; CLOSED; report `analysis/reports/bundle1_results.md`, section 0 has the final numbers)
- Suite `datasets/suite_b1/`: families abalone, autompg, concrete, dwd; arms real / neutral / swapped on byte-identical numbers; opaque codes k11..k43. Column order as in the repo's files (not shuffled).
- 54 runs (48 + 6 top-up), 45 completed, 9 failed (8 cycle step, 1 init). gpt-4o-2024-08-06 throughout. FCI chosen in every completed run. Tokens: 2,360,826 + 310,725 prompt, 254,233 + 34,929 completion.
- FINAL verdicts: N1 INCONCLUSIVE (19 label-only, 7 data-only = 73%, 13 neither); N2 SUPPORTED (LLM-set edges per run real vs neutral: 18.6 / 0, 2.75 / 0, 8 / 0, 3.25 / 0); N4 INCONCLUSIVE (final adjacency F1 below algorithm output in 31 of 45: neutral 16/16, swapped 10/13, real 5/16); P3 INCONCLUSIVE (100 of 336 non-directed edges survive the bootstrap step = 29.8%; directed 66 of 101 = 65%). Gates T1-T6 and Q1-Q3 all pass. The top-up changed no verdict.
- By role, algorithm output -> final: real (16 runs) adjacency F1 0.51 -> 0.68, directed-edge F1 0.09 -> 0.68; neutral (16) 0.51 -> 0.20, 0.08 -> 0.02; swapped (13) 0.50 -> 0.26, 0.04 -> 0.07. Share of final edges set by the LLM: real 141 of 152 (93%), neutral 0 of 58, swapped 112 of 125 (90%).
- Per family, adjacency F1 S0 -> S1 -> final (real arm): abalone 0.28 -> 0.20 -> 0.53; autompg 0.74 -> 0.62 -> 0.81; concrete 0.28 -> 0.05 -> 0.94; dwd 0.75 -> 0.24 -> 0.55. S0 -> S1 falls in all 12 arms. Swapped arms scored by label (adjacency / directed): abalone 0.49 / 0.49, autompg 1.00 / 1.00, concrete 0.88 / 0.86, dwd 0.49 / 0.38.
- Neutral arms: the LLM answered D to every pair in every run.
- Survivor-bias check (S3 exists for 53 of 54 runs): real-name S3 means over all runs 0.655 adjacency / 0.644 directed versus 0.684 / 0.679 completed-only; no conclusion changes. S3 is the primary endpoint from now on.
- Cycle step over all 84 live runs: entered 9 times, crashed 9 times (keys returned: `edge_to_remove` 5, `nodes_to_remove` 4). Crashes in total: 12 of 84.
- Neutral-arm prompt scan (first 48 runs): 332 requests, no real name before the final graph except fixed template text present in every arm.
- N1 weakness (post hoc): all abalone data-only edges touch the label `Length`, which sat on the Age column, the hub of a star-shaped reference.
- SUPERSEDED CLAIM: "final below the algorithm's output in every run" (pass 4b, 25 of 25) holds for Sachs and unnamed data, not in general. Accurate statement: the bootstrap step degrades the algorithm's graph in every arm; with informative names the LLM then replaces it with a graph written from the names; without usable names the damaged graph is final.

## CAUSALARENA SNAPSHOT (fetched 2026-10-07; `cc-research/external/causalarena/`)
- Public release = half of each family: 500 synthetic configs, 50 semantic scenarios (10 domains x 5; 17-25 variables, 26-67 edges, mean 22.9 / 41.4), 50 formula scenarios. Per scenario 5 replicates x {obs-only: 1,000 rows; obs+int: 800 + 200 rows, 3-7 single-variable targets, per-cell flags in `x[:, :, 1]`}. Values standardised; raw scale in metadata. Published tables average over 100 semantic scenarios; no per-scenario results are published.
- Real tables are not republished (index only); Causal Chambers entries cite `causalchamber.ground_truth.edges` but not how the 8,000 + 2,000 rows were drawn.
- Paper (2609.11897v1) Appendix B, read directly on 2026-10-07: PC = stable PC, Fisher-z, alpha 0.05; for PC and GIES undirected edges are "randomly oriented with a fixed per-file seed" before directed-edge F1 and SHD; one-hour budget per graph row; PC timed out on both Causal Chambers datasets and two PetShop sets; `RandomRegress` = "fixed-seed random-order regression baseline"; semantic and formula scenarios built with an "agentic construction workflow" plus "human and LLM-assisted review"; no LLM method or agent among the 18 methods.
- Published F1 (full set), semantic obs-only: FoundCause 0.634, GIES 0.552, CDFM 0.434, TabCausal 0.422, CDIS 0.403, PC 0.333, RandomRegress 0.252. Formula obs-only: FoundCause 0.524, TabCausal 0.472, GIES 0.467, RandomRegress 0.196. Obs+int gains are small (TabCausal +0.025, GIES +0.016, CaScaLe +0.042 on semantic).
- Scorer calibration (measured, 250 public semantic obs files, published PC configuration): F1 0.335 vs published 0.333 (gate C1 PASS, tolerance 0.045); SHD 37.5 vs 33.5 (gate C2 FAIL, tolerance 2.8; cause unknown: definition or public/non-public difference). PC runtime 0.3 s median, 93-105 s on one scenario (sleep_apnea).
- COLUMN ORDER LEAK (measured): in every released sample file checked, every true edge runs from an earlier column to a later column (semantic 2,068 of 2,068 distinct edges; formula 1,714 of 1,714; synthetic 50,421 of 50,421 in 481 files). The exporter stores variables in a causal order (it differs from the node order in `graph.json`). A naive regression on earlier columns (OLS, 1% level, fixed before running) scores directed-edge F1 0.680 on public semantic and 0.575 on public formula, above every published row; with seeded column shuffle 0.269 and 0.215 (published RandomRegress: 0.252, 0.196). Lasso/BIC variant 0.642; 36 of 50 scenarios individually above 0.634. Not shown: that any published method used the order (the paper does not say whether wrappers shuffle columns). Not yet reported to the maintainers (Uzair's decision).
- CEILINGS AND ERROR BUDGET (measured turn 14, no LLM; `analysis/reports/error_budget_and_order.md`): share of true edges compelled in the equivalence class 91.8% (semantic) / 94.5% (formula); identifiable ceiling under the scoreboard's rule 0.957 / 0.971 (lowest scenario 0.844 / 0.897); with the released targets at least 0.974 / 0.993. Targets per scenario 3.8 / 6.1, 69% / 79% of them inputs. PC budget on public semantic: 1.000 -> 0.957 (identifiability) -> 0.611 (PC's skeleton with perfect directions; skeleton precision 0.746, recall 0.522) -> 0.335 (as scored). Of the true adjacencies PC finds: 43.6% directed right, 36.5% wrong, 19.9% undecided; committed directions right 54.4% of the time. PC adjacency recall by number of causes of the effect: 0.74 (1), 0.65, 0.56, 0.44, 0.40, 0.34 (6+).
- VALUE OF ORDER (oracle tiers from the true graph): PC re-oriented 0.335 (none) / 0.470 (inputs vs rest) / 0.468 (3 depth bins) / 0.524 (5 bins) / 0.611 (full depth); linear regression on strictly earlier tiers 0.386 / 0.399 / 0.535 / 0.714 (full depth, above every published row). R2-sortability 0.571 (semantic), 0.603 (formula); R2-SortnRegress 0.314 / 0.287.
- CORRECTION: earlier statement "100% on directions from observational data is a sign of leakage" is too strong for these graphs; the honest limit is about 0.96.
- From the literature check (second-hand): no GitHub repository with the evaluation code was found; the replay sampler intervenes only on pre-declared targets and writes columns in `node_order` with no shuffle; the leaderboard Space lists the paper's 18 methods only; AVICI and Arrow are order-equivariant by construction and FoundCause's abstract says "permutation-invariant" encoder, so the column-order leak probably does not explain the top rows.
- Submission: `summary.csv` + `manifest.json` + optional predictions; validator `tools/validate_submission.py`; route = pull request or discussion on the Hugging Face dataset.

## CAUSAL CHAMBERS (downloaded 2026-10-07; `cc-research/external/causal_chambers/`)
- lt_interventions_standard_v1: one CSV per experiment, 1,000 rows each, 46 columns incl. an `intervention` flag; per the dataset README (second-hand) a 10,000-row reference with all actuators randomised plus single-target shifts on colours, polarisers, LEDs and sensor parameters. lt_validate_v1 / wt_validate_v1: one two-level randomised experiment per manipulable variable (29 / 28).
- Second-hand from the literature check (verify before use): ground-truth edge X -> Y means intervening on X changes Y for some setting of the other inputs; the standard Mk1 graphs are ONE LAYER deep (light tunnel 38 variables / 57 edges / 29 parents; wind tunnel 32 / 42 / 21; every parent a manipulable input), so order is trivial once the controls are known and the difficulty is power, nonlinearity and sensor-sensor confounding. A paid Remote Lab (`causalchamber.lab`, subscriber credentials, Mk2 chambers with up to 99 variables) allows new experiments; no price published; no agent result on chamber graphs was found. Published discovery results: authors' notebook GES precision .55-.60 / recall .56-.62 on a 20-variable subgraph; CDFM paper F1 CDFM .727, TabCausal .603, GES .426, PC .281.

## PROGRAM v2 (proposal 2026-10-07, `analysis/reports/program_v2.md`; NOT YET ADOPTED)
- Organising question: for each directed edge a system reports, where did the direction come from (numbers, interventions, declared knowledge, or undeclared layout/names)?
- Theses T1-T6: T1 order source explains most directed-edge accuracy; T2 deployed agents take order from names/layout; T3 a system holding order as a typed, sourced partial order is never below its data-only self, boundedly harmed by wrong knowledge, and (target, not promise) at or above the published best per declared regime; T4 calibrated, checkable claims with abstention; T5 interventional answers with identification status; T6 experiment choice beats random on recorded real experiments.
- Regimes D / D+I / D+K / D+I+K; controls: columns always shuffled, names real / neutral / moved, knowledge supplier none / oracle / each model, interventions withheld / released / chosen.
- System: a claim ledger outside the repo (OrderEvidence with a closed list of sources, OrderLedger, PartialOrder, AdjacencyEvidence, Claim, Regime; stages K0-K7; invariants I1-I7 incl. permutation equivariance and "knowledge never creates a connection"). The LLM only supplies tiers, never edges.
- Tracks: A measurement (A1 budgets for more methods; A2 Causal-Copilot audit on 10 CausalArena scenarios = old bundle 2 runs; A3 knowledge elicitation, about 900 short calls); B ledger (B1 data-only, B2 interventions, B3 knowledge tiers, B4 confidence/calibration); C decisions (queries, experiment choice); D writing/theory.
- Predictions O1-O5 for A3 (thresholds in the report). Gates: G1 16 Oct, G2 2 Nov, G3 4 Dec, G4 March.
- Extensions listed, not planned: E1 field-wide audit of other agents/methods, E2 public agent track, E3 real experiments via the Remote Lab, E4 learned fusion (pretrained network taking unreliable tier statements), E5 hidden confounders / time series / scale.
- Bundles 2-5 (`bundle2_onward_design.md`) are superseded as the organising plan; their failure-mode list and the agent runs (now A2) remain.

## PAPER-vs-CODE
D1. "not permitted to override high-confidence decisions made by the bootstrap procedure" -> DIVERGENT, seen live in every named arm.
D2. "Moderate-confidence edges are passed to the LLM" -> DIVERGENT (all pairs, every run).
D3. "LLM interprets error messages and iteratively revises" -> DIVERGENT (F14, F28).
D4. "Rule-Guided LLM for Filtering" -> PARTIAL.
D5. User constraints respected -> PARTIAL/DIVERGENT (F12, F13).
D6. "re-execute relevant portions after user input" -> PARTIAL.
D7. Code-only steps absent from paper: marginal KCI pruning, LLM cycle breaking.
D8. "logs each transformation step ... audit or revert" -> UNCLEAR; lineage had to be reconstructed from outside.
D9. Bootstrap confidence for "each potential causal relationship" -> CODE consults only the directed form.
Caveat: the code is ~13 months newer than paper v2.

## INFERENCES
I1. Paper Table 2 probably measures selection + execution, not refinement (F17, F19).
I2. The refinement stage is written as if every algorithm returned a DAG.
I3. On Sachs with gpt-4o the LLM review is recall of textbook relations keyed on variable names. With the path fixed, identical numbers score 0.44 / 0.10 / 0.01 depending only on the header line. By construction (F11) the review cannot follow the data; what is notable is that the pipeline lets it overrule the data.
I4. The largest measured damage comes from a deterministic rule (the bootstrap edit), which is also what hands the graph to the LLM.
I5. The elicited knowledge prose is the main hidden channel and the first point of run-to-run divergence.
I6. Method selection was the stable part.
I8. (after bundle 1) With informative names the final graph is essentially the LLM's graph (about 90% of final edges), whether the names are on the right columns or not; the data's contribution to the final graph is small in every arm.
I9. Scores for agents on current scoreboards cannot separate three sources of a graph: numbers, labels, layout. CausalArena's released files leak direction through column order; an agent sees columns in order.
I10. (turn 14) The leak channels found so far are all channels for causal ORDER: layout gives a total order for free, names give the LLM its order, and classical algorithms guess it (54%). On CausalArena's public scenarios the identifiable limit is 0.96 and oracle depth plus a linear regression gives 0.71, so where a system gets its order decides its score.
I7. DAG-only scoring rewards writing directed edges from recall and penalises an honest "direction unknown" (sachs: 0.00 -> 0.37 directed-edge F1 while adjacency F1 fell).

## LITERATURE (V = checked by Claude, A = agent-reported or read through a summarising tool)
- V: Zheng et al. 2606.23608; Kitson & Constantinou 2608.27472; Kumar et al. 2608.23660; CausalSteward 2607.01936; Li & Russo UAI 2026; Srivastava et al. 2510.16530.
- V (turn 13, Appendix B and sections 4.2-4.5 read directly; tables read from the released CSVs): CausalArena 2609.11897; see the snapshot section. Note: the "best real-data F1 0.39 / 0.46" figures are confirmed from `real_method_summary.csv` (CDFM 0.391 over 13 datasets observational; TabCausal 0.462 over 7 with interventions).
- A (turns 6-8): CausalArena 2609.11897 (18 methods, no LLMs or agents, no relabelling control, DAG-level directed-edge F1; best real-data F1 0.39 observational / 0.46 with interventions; Hugging Face dataset and leaderboard); GSK CausalBench 2210.17283 and its 2023 challenge 2308.15395 (no truth graph; winners were simple effect estimators); Causal Chambers 2404.11341 (physical truth; ground-truth edge lists ship in the `causalchamber` PyPI package, light tunnel 38 variables / wind tunnel 32); CausalRivers 2503.17452; FutureSim 2605.15188; amortised discovery with prior-fitted networks 2512.11840.
- A (turn 14, four agent reports saved as `analysis/literature/agent_reports/cluster6..9_*.md`): CARE (Dong et al., arXiv 2511.16016) ALREADY uses original / anonymised / permuted names for model-assisted discovery, so the name-moving control is not new; our addition is layout control, stage attribution, a deployed agent, a public scoreboard. Vashishtha et al. (arXiv 2310.15117): order, not edges, is the right thing to ask an imperfect expert. Kitson & Constantinou (arXiv 2206.08952): column order moves hill-climbing F1 by 0.41 (algorithm sensitivity, not a file leak). ACI (Magliacane et al. 2016): scored ancestral claims from tests, interventions and background knowledge, under 12 variables. Logic/argumentation methods stop at about 9-15 variables (Russo et al. 2024; Li & Russo 2026). GENESIS (2608.03868) and Zheng et al. own the "auditable/provenance" vocabulary without a checker. CauScientist (2601.13614): LLM edits accepted only if interventional BIC improves. ACDB (2609.31675) and CausaLab (2605.26029): agents choosing interventions on 3-7 variables; classical baselines beat the models. CausalDS (2607.08093): data-in causal queries with scored abstention and intervals on small motifs. Bootstrap frequencies are not reliably calibrated (Debeire 2024; Banerjee et al. 2025). Faltenbacher et al. (2502.14719) is the nearest thing to an error decomposition for PC.
- Not found by those searches: a benchmark shown to leak directions through column order; a three-way control (numbers, names, layout); an error budget separating identifiability, skeleton and direction loss; machine-checked derivations per claim; one system fusing tests, interventions and labelled model knowledge at 20-40 variables; an agent on the Causal Chambers Remote Lab; a query benchmark at 20-40 variables with identifiability labels, bounds and scored experiment proposals.
- Open as far as the search reached: per-edge provenance surviving to the output; PAG marks as first-class types; calibration inside the decision; memorisation as a run-time signal; an agent on a public causal-discovery scoreboard; a relabelling control on such a scoreboard; any published ablation of Causal-Copilot's refinement stage.
- Terminology: "elicit once, reify with provenance, then verify" in place of "intensional -> extensional".

## OPEN QUESTIONS
Q2. Refinement effect on other semantic datasets (bundle 1), other models, memorisation-resistant graphs.
Q3. What produced paper Table 2. NOT to be asked of the authors (Uzair, 2026-10-06); answer from code and our own runs or report as unknown.
Q5. Torch-based and time-series wrappers not run.
Q6. Other upstream branches. Q7. Causal inference path mostly unread. Q8. Varsortability of simulated data. Q9. (2,1) cell pairs from Markov-blanket wrappers.
Q10. Does "sachs" in the path change accuracy (P4)?
Q11. ANSWERED turn 13: the semantic scenarios come with sample files (see snapshot section).
Q13. Why our SHD differs from the published PC SHD (definition, or public vs non-public half); needs their evaluation code.
Q14. Do CausalArena's wrappers shuffle columns before calling a method? Unknown from paper and snapshot; no code repository found; several top methods are order-equivariant by construction (second-hand).
Q17. Can a model reading names supply correct tiers on CausalArena's scenarios, and what does it do with neutral or moved names (A3, predictions O1-O5)?
Q18. Does the PC error-budget pattern (direction near chance, large gain from oracle tiers, recall falling with number of causes) hold for GES, FCI and the pretrained models that run on CPU?
Q15. How much are names alone worth on model-written semantic scenarios (bundle 2, M5)?
Q16. Sizes of the Causal Chambers archives (reported by the next `cc.ps1 fetch`).
Q12. Will the mentor allow a causal group of 2-3, and is "replicate, measure, then strengthen Causal-Copilot" in scope for Quarter 2?

## HYPOTHESES
None adopted. The "extensionalization" hypothesis survives only in a narrower conditional form (reification with provenance gives auditability and replay, not correctness; deterministic rules need the same scrutiny as the LLM; one inference is weaker than agreement across several).

## DECISIONS (Uzair)
- 2026-10-05: split execution model; gpt-4o; no API budget cap; Docker Desktop + WSL2.
- 2026-10-06: do not count on any answer from Prof. Huang's group.
- 2026-10-06: after weighing against WorldReset, proceed with the causal project toward "benchmark plus fix" (target scoreboard: CausalArena real slice and Causal Chambers); bundle 1 approved. Uzair called the plan "solid"; treated as a working direction, not a final commitment.
- 2026-10-07 (later): ran the top-up plan and the re-fetch. Asked to restructure the approach: "I want to take things much farther and much deeper than you are currently thinking of". Program v2 proposed in response; his reaction not yet known.
- 2026-10-07: asked for the bundle-1 analysis and the design of the future bundles. No decision yet on: bundle-2 design, the names-only calls, telling CausalArena's maintainers about the column order.
- 2026-10-06: primary near-term use of the research: flesh out the Causal Discovery side of the shared mentor document to recruit at least one teammate; also personal record.

## STATUS and what is needed
- 2026-10-09: goals-by-category tracker posted as 16 messages in the private Slack channel #cd-tracker (C0C7Q2CA2G7; only Uzair is a member). Uzair chose private over #causal-discovery, whose members include bih007 (very likely Prof. Huang), Xinyue Wang (xiw159) and five forecasting students. Copy: `claude/goals-by-category.md`, `cc-research/GOALS_by_category_slack.txt`. Slack messages cannot be edited from here; status changes go in as new posts or a canvas.
- Nothing is blocked on a command right now. Decisions (Uzair): (1) adopt, redirect or enlarge program v2, and which of the listed extensions E1-E5 he wants in scope; (2) approve A3 (about 900 short calls asking a model for tiers from names; prompt to be shown to him first); (3) whether to tell CausalArena's maintainers about the column order.
- Then Claude, no LLM needed: A1 error budgets for GES and FCI on the public files; B1 data-only ledger with invariants I1-I4, I7; suite builder with seeded column shuffle; the A3 script with thresholds fixed in code and a stub self-test; a `cc.ps1` command for compute-only jobs on Uzair's machine (the sandbox's 180-second limit is the bottleneck for larger analyses).
- Shared-document section: draft v3 saved as `claude/shared-doc-causal-section-draft.md` (final bundle-1 counts, corrected ceiling paragraph, error budget, CARE added). Its "Proposed project" part still describes the old plan and waits on decision (1).
- Later: tracks B2-B4, C, D; research atlas; Quarter 2 proposal.
