Tickets: REP-07, BEN-07, BEN-11, CAP-17, BND-06

# BND-06 families: formula, synthetic sample, AVICI, CAP-17 package (2026-10-12)

This report continues `analysis/reports/bnd06_interim.md`, which covered the semantic family. All work ran in the cloud copy. It made no model or API calls. Unless a row says otherwise, numbers come from `analysis/results/methods/bnd06_families.json`, the `error_budget_*_{formula,synthetic100}.json` files, `bnd06_c1_recheck.json` and the logs under `analysis/results/methods/logs/`.

## 1. What ran

- **Families.**
  - Formula: all 250 public obs-only files (50 scenarios x 5 replicates).
  - Synthetic: the 100 files in `plans/synth_sample_100.txt`, one replicate (rep000) of each of 100 scenarios. They are exactly the 100 files in `scm/synthetic/data/synthetic_obs_only`; the run passes `--file-list` anyway.
- **Methods.** `causalarena_methods.py` ran `pc`, `gesbic`, `fci`, `lingam` and `notears` with the configuration documented in its docstring, which is unchanged.
- **Orders.** Each method ran in the released column order and in the shuffled order (`--shuffle-seed 20261010`: a per-file permutation `default_rng(20261010 + crc32(file name))`, mapped back before scoring, as in `plans/bnd06_prereg.json`).
- **Per-file limits.** The limit is `--file-timeout-s`:
  - Formula: 300 s for pc, fci, lingam and notears; 600 s for gesbic.
  - Synthetic: 300 s for every method, the limit `bnd06_interim.md` set for the sample.
  - A file that raises or times out is scored as an empty graph and flagged, as before.
- **Outputs.** `analysis/results/methods/<method>_formula_obs_{rel,shuf}.json` and `<method>_synthetic100_{rel,shuf}.json`. Each is a jobkit output, and its sha256 is in the worker log's `JOB-COMPLETE` line.
- **Environment.** Python 3.13.16, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, pandas 3.0.5, networkx 3.6.1, joblib 1.6.0, ges 1.1.0 and statsmodels 0.15.0, plus the causal-learn import dependencies pydot 4.0.1, momentchi2 0.1.8, graphviz 0.21 and tqdm 4.70.1. causal-learn is the Causal-Copilot vendored 0.1.3.8, put on the path with `PYTHONPATH=../Causal-Copilot/externals/causal-learn`. The machine has 2 cores and 7 GB RAM. Jobs ran under `logs/worker.sh`, which pops from the shared queues `logs/jobs_{A,B}.txt`; two or three workers ran in parallel.
- **Environment shim (code change).** ges 1.1.0 uses `np.Inf`, which NumPy 2 removed. Without a fix, every gesbic file failed with `AttributeError` and was silently scored as an empty graph (seen in a 2-file probe). `causalarena_methods.py` now sets `np.Inf = np.inf` before ges runs when the alias is missing. It is the same float. The semantic gesbic rows from BND-04 were produced elsewhere and are not affected by this change.
- **joblib (no change made).** The vendored PC/FCI use joblib with `n_jobs=4`. I tested sequential mode (`JOBLIB_MULTIPROCESSING=0`) on 5 semantic files:
  - PC gave identical output.
  - FCI differed on 1 of the 5 files: one extra `<->` pair, and F1 went from 0.393 to 0.354.
  - The parallel and sequential modes are therefore not equivalent for this FCI build. All runs kept the default (parallel) mode, the one the semantic runs used. Why sequential FCI differs is unexplained; I did not trace it.

Wall time per job, from the worker logs (`END ... wall_s`). Two or three jobs shared 2 cores, so these are not single-core timings. The sum of per-file method seconds is in `bnd06_families.json` (`sum_file_seconds`).

| Job | formula rel | formula shuf | synthetic100 rel | synthetic100 shuf |
|---|---|---|---|---|
| pc | 1792 s (+ about 9 min in a first queue, see note) | 2139 s | 1671 s | 1609 s |
| gesbic | 2775 s | 2472 s | 11562 s | 11615 s |
| fci | 59 s (+ about 9 min in a first queue) | 450 s | 2971 s | 2878 s |
| lingam | 470 s | 230 s | 1612 s | 1560 s |
| notears | 2026 s | 1563 s | 2143 s | 2047 s |

Note: `pc` and `fci` formula released order started under a first pair of fixed queues at 01:07 UTC. I stopped those queues at about 01:16 (`logs/formula_{A,B}.log`) and resumed the jobs under the shared-queue workers from their parts files, with the same code and settings. The in-flight file was rerun.

Failed files (each scored as an empty graph):

| Method | formula rel / shuf | synthetic100 rel / shuf |
|---|---|---|
| pc | 0 / 0 | 3 / 3 (all timeouts) |
| gesbic | 66 / 68: 65 / 67 `LinAlgError: Singular matrix` + 1 / 1 timeout | 29 / 29 (all timeouts: 20 of the 20 d = 100 files, 8 of the 23 d = 50 files, 1 of the 20 d = 30 files) |
| fci | 72 / 74 `ValueError: Data correlation matrix is singular` | 7 / 6 (all timeouts) |
| lingam | 0 / 0 | 0 / 0 |
| notears | 0 / 0 | 0 / 0 |

The formula failures are singular correlation matrices. This is consistent with some formula variables being exact functions of others, which I did not check per file.

## 2. Gate C1

**C1 holds, re-established from nothing in this environment (`bnd06_c1_recheck.json`).** I reran PC (vendored causal-learn, stable, Fisher-z, alpha 0.05) on all 250 public semantic obs-only files in released order (`pc_c1check_semantic_obs_rel.json`, 0 failed). The results:

- **Random rule.** Family mean F1 is 0.3346 and SHD 37.504. The published PC semantic obs-only row is F1 0.333 (std 0.150), and the tolerance is 0.0452, so F1 is within.
- **Authors' rule ("lower").** F1 is 0.3962 and SHD 35.428.
- **Match to earlier numbers.** All three numbers are identical to the earlier `bnd06_verdicts.json` values. The earlier environment is not recorded in this copy, so the claim is only that this environment reproduces those values exactly.
- **Scorer files.** `analysis/cc_graph.py` (sha256 5044b42f...) and `analysis/causalarena_io.py` (39f416b3...) have the same sha256 before and after this session. Neither was edited.

## 3. Order sensitivity: released vs shuffled columns

These are family mean directed F1 values: replicate-averaged per scenario, then averaged over scenarios. The random rule is order-free; the authors' rule "lower" reads the order the method saw. In every public file of all three families, every true edge runs from an earlier column to a later one (`causalarena_calibration/column_order_check.json`). So "lower" in released order reads the answer.

**Q4c was pre-registered for the semantic family only.** The verdict lines below apply the same thresholds and are **not pre-registered; same thresholds applied descriptively.** The thresholds are |difference| <= 0.02 for every method (supported) and > 0.05 for any method (refuted), using the random rule.

### Formula (250 files, 50 scenarios)

| Method | F1 released | F1 shuffled | difference (random rule) | same under "lower" |
|---|---|---|---|---|
| PC | 0.304 | 0.355 | **-0.051** | 0.398 vs 0.355 (+0.043) |
| GES (BIC) | 0.344 | 0.341 | +0.003 | 0.360 vs 0.340 (+0.021) |
| FCI | 0.223 | 0.224 | -0.002 | **0.369 vs 0.226 (+0.143)** |
| DirectLiNGAM | 0.255 | 0.244 | +0.010 | same |
| NOTEARS | 0.169 | 0.168 | +0.001 | same |

Descriptive verdict: REFUTED, because PC's |difference| of 0.0514 is over 0.05. The other four methods are within 0.02.

### Synthetic sample (100 files, 100 scenarios, one replicate each)

| Method | F1 released | F1 shuffled | difference (random rule) | same under "lower" |
|---|---|---|---|---|
| PC | 0.265 | 0.371 | **-0.106** | 0.340 vs 0.377 (-0.037) |
| GES (BIC) | 0.346 | 0.346 | +0.000 | 0.405 vs 0.349 (+0.056) |
| FCI | 0.345 | 0.348 | -0.003 | **0.554 vs 0.345 (+0.209)** |
| DirectLiNGAM | 0.195 | 0.195 | 0.000 | same |
| NOTEARS | 0.177 | 0.178 | -0.000 | same |

Descriptive verdict: REFUTED, because PC's |difference| of 0.106 is over 0.05. The other four methods are within 0.003.

The pattern is the same as on the semantic family:

- **PC is the only method that reads column order under the order-free rule.** It does better in shuffled order: by 0.051 on formula and 0.106 on synthetic, against 0.093 on semantic.
- **FCI's gain under the authors' rule is order leak.** Under "lower", FCI loses 0.143 (formula) and 0.209 (synthetic) when columns are shuffled, against 0.200 on semantic. GES shows a smaller version of the same effect: 0.021 on formula and 0.056 on synthetic.
- **LiNGAM and NOTEARS return DAGs, so the orientation rule does not apply to them.** Their released and shuffled values agree within 0.011.

### Where PC's order dependence comes from (side check, not pre-registered)

`pc_skeleton_order_check.py` ran PC (stable, Fisher-z, alpha 0.05) on every 10th public semantic file (25 files) in released and shuffled order, then compared skeletons after mapping the shuffled graph back.

| causal-learn build | files scored | files whose skeleton changes with column order | source |
|---|---|---|---|
| Causal-Copilot vendored 0.1.3.8 | 24 (1 timeout at 120 s) | 21 (mean 3.96 adjacencies differ) | `pc_skeleton_order_vendored.json` |
| upstream causal-learn 0.1.4.8 (pip) | 22 (3 raise "correlation matrix is singular") | 0 | `pc_skeleton_order_upstream.json` |

On the 22 files both builds scored, the vendored skeleton changes in 20 and the upstream skeleton in 0. So the order dependence comes from the vendored build, not from PC-stable as such.

A reading of the vendored code suggests the mechanism, but I have not tested it separately. In `externals/causal-learn/causallearn/utils/PCUtils/SkeletonDiscovery.py`, `skeleton_discovery` queues each unordered pair once, as `(x, y)` with `x < y`. `_process_node_pair` then draws conditioning sets from `adj(x) \ {y}` only, while textbook PC also tries subsets of `adj(y) \ {x}`. Which endpoint is `x` is decided by column order. In released (topological) order `x` is the earlier variable, so separating sets made of the later variable's parents are never tried.

This leaves the earlier result standing: RQ-16's 54% committed-direction accuracy for PC is a property of the Causal-Copilot build in released order.

## 4. Published rows (REP-07 extension)

The comparison is against the published obs-only cell of the same family in `external/causalarena/results/tables/main/*.csv`. The tolerance is 3 SE of our scenario mean, `3 * published scm_std / sqrt(n_ours) * sqrt((N - n_ours) / (N - 1))`:

- Formula: N = 100 published scenarios, n_ours = 50.
- Synthetic: N = 1000 published scenarios, n_ours = 100. The published scenario counts come from `results/tables/breakdown/*_representative.csv`.
- Synthetic caveat: our synthetic per-scenario values are single replicates, while the published scm_std is over 5-replicate means. The synthetic tolerance is therefore optimistic (too narrow).

Both orientation rules are shown. bnd06_summary.py's REP-07 comparison uses the authors' rule; C1 used the random rule.

### Formula obs-only

| Method (published name) | published F1 / SHD | tolerance F1 / SHD | ours, "lower": F1 (gap) / SHD (gap) | ours, random: F1 (gap) / SHD (gap) | within |
|---|---|---|---|---|---|
| PC (PC) | 0.220 / 31.10 | 0.049 / 2.04 | 0.398 (+0.178) / 31.02 (-0.08) | 0.304 (+0.084) / 33.67 (+2.57) | SHD only, "lower" rule |
| GES (GIES) | 0.467 / 36.67 | 0.037 / 4.24 | 0.360 (-0.107) / 35.62 (-1.05) | 0.344 (-0.123) / 36.23 (-0.44) | SHD only, both rules |
| DirectLiNGAM (LiNGAM) | 0.240 / 34.68 | 0.025 / 2.41 | 0.255 (+0.015) / 34.78 (+0.11) | same | F1 and SHD |
| NOTEARS (NOTEARS) | 0.185 / 35.19 | 0.024 / 2.21 | 0.169 (-0.016) / 34.70 (-0.50) | same | F1 and SHD |
| FCI | no published row | | | | |

Two gaps have a candidate explanation from the failing files. Neither explanation is pre-registered.

- **GES.** 66 of 250 formula files fail (singular matrix), in 18 of 50 scenarios. Dropping those 18 scenarios (`error_budget_gesbic_formula_excl_failed.json`, 32 scenarios, tolerance 0.055) gives F1 0.475 under the random rule (gap +0.008) and 0.499 under "lower" (gap +0.032). Both are within, and so is SHD. With the failures scored as empty graphs, F1 is 0.344. Whatever the published GIES (pcalg via R) did on these singular files, it did not score them as empty graphs at this rate. That is an inference, not checked.
- **PC.** The vendored build does not fail on singular files. In `_process_node_pair`, a `ValueError` from the Fisher-z test falls back to a KCI test (`backup_indep_test = CIT(data, method='kci')`), which also explains PC's slow formula files. Upstream causal-learn 0.1.4.8 raises on 72 of the 250 formula files, in 16 scenarios (`pc_upstream_failures_formula.json`). Setting those 72 files to empty graphs in our vendored rows gives F1 0.218 under the random rule (published 0.220, inside the 0.049 tolerance), with SHD 33.80 (gap +2.70, outside the 2.04 tolerance). Under "lower" it gives F1 0.282. This is a hybrid: vendored PC on the remaining files, and the two builds also differ in skeletons. It is consistent with the published PC formula row coming from a PC that fails on the singular files, but it does not establish that.
  - The same check on semantic: upstream raises on 25 files in 5 scenarios, and the hybrid F1 is 0.302 (random) against 0.333 published, within 0.045.
  - On the synthetic sample: upstream raises on none and times out on 4 at 300 s; the hybrid F1 is 0.262.

### Synthetic obs-only (100-file sample)

| Method (published name) | published F1 / SHD | tolerance F1 / SHD | ours, "lower": F1 (gap) / SHD (gap) | ours, random: F1 (gap) / SHD (gap) | within |
|---|---|---|---|---|---|
| PC (PC) | 0.307 / 115.37 | 0.034 / 42.4 | 0.340 (+0.033) / 119.98 (+4.61) | 0.265 (-0.042) / 122.77 (+7.40) | "lower": both; random: SHD only |
| GES (GIES) | 0.480 / 123.55 | 0.037 / 49.6 | 0.405 (-0.075) / 113.91 (-9.64) | 0.346 (-0.134) / 115.19 (-8.36) | SHD only, both rules |
| DirectLiNGAM (LiNGAM) | 0.207 / 109.59 | 0.035 / 40.5 | 0.195 (-0.012) / 110.95 (+1.36) | same | F1 and SHD |
| NOTEARS (NOTEARS) | 0.276 / 104.22 | 0.033 / 38.7 | 0.177 (-0.099) / 111.56 (+7.34) | same | SHD only |

The synthetic SHD tolerances are wide (about 40) because SHD on d = 100 graphs dominates the published scm_std.

**GES on the synthetic sample is limited by our implementation's speed.** 29 of the 100 files hit the 300 s limit in each order: every d = 100 file, 8 of the d = 50 files and 1 d = 30 file. The published runtime table (`results/tables/runtime/synthetic_main_runtime.csv`) gives GIES 2.78 s per row with no timeouts; that is pcalg via R, against our Python `ges` 1.1.0. Dropping the 29 timed-out scenarios gives F1 0.487 under the random rule against 0.480 published (`error_budget_gesbic_synthetic100_excl_failed.json`). That comparison is biased, because it drops exactly the large graphs, and its SHD (43.9) is not comparable to the published 123.6.

**NOTEARS' F1 gap is unexplained.** It is -0.099 on synthetic, within on formula (-0.016), and -0.057 on semantic (`bnd06_interim.md`). The solver is unchanged from the semantic runs.

## 5. Error budgets (released order, `method_error_budget.py --family ...`)

| File | failed | skeleton F1 | F1 random | F1 "lower" | committed-direction accuracy | cost of direction errors (skeleton F1 - F1 random) |
|---|---|---|---|---|---|---|
| error_budget_pc_formula.json | 0 | 0.543 | 0.304 | 0.398 | 0.585 | 0.239 |
| error_budget_gesbic_formula.json | 66 | 0.444 | 0.344 | 0.360 | 0.792 | 0.101 |
| error_budget_gesbic_formula_excl_failed.json (32 scenarios) | 66 (dropped) | 0.610 | 0.475 | 0.499 | 0.799 | 0.135 |
| error_budget_fci_formula.json | 72 | 0.391 | 0.223 | 0.369 | 0.794 | 0.169 |
| error_budget_lingam_formula.json | 0 | 0.448 | 0.255 | 0.255 | 0.561 | 0.194 |
| error_budget_notears_formula.json | 0 | 0.416 | 0.169 | 0.169 | 0.406 | 0.247 |
| error_budget_pc_synthetic100.json | 3 | 0.615 | 0.265 | 0.340 | 0.354 | 0.350 |
| error_budget_gesbic_synthetic100.json | 29 | 0.487 | 0.346 | 0.405 | 0.809 | 0.142 |
| error_budget_gesbic_synthetic100_excl_failed.json (71 scenarios) | 29 (dropped) | 0.686 | 0.487 | 0.571 | 0.809 | 0.200 |
| error_budget_fci_synthetic100.json | 7 | 0.600 | 0.345 | 0.554 | 0.814 | 0.255 |
| error_budget_lingam_synthetic100.json | 0 | 0.324 | 0.195 | 0.195 | 0.653 | 0.129 |
| error_budget_notears_synthetic100.json | 0 | 0.286 | 0.177 | 0.177 | 0.642 | 0.109 |

The Q4a/Q4b fields in these files carry the BND-04 thresholds. For formula and synthetic they are labelled `predictions_note`: not pre-registered for this family.

## 6. AVICI (DOM-11): stopped at the checkpoint download

The full record is in `analysis/results/methods/logs/avici_install.log`.

1. **Python 3.13 install fails.** `pip install --break-system-packages avici` on the main interpreter cannot resolve. avici 1.0.7 and 1.0.6 require `numpy<2`, which has no Python 3.13 wheel; 1.0.5 requires `tensorflow==2.9.1`; and 1.0.0 to 1.0.4 depend on the deprecated `sklearn` package. The binary-only dry run ends with `ResolutionImpossible`. A plain dry run was still resolving after 300 s, and I stopped it.
2. **Isolated Python 3.11 venv.** I created it in the session scratch directory and ran `uv pip install avici`, which installed avici 1.0.7. `import avici` then failed with `ImportError: cannot import name 'PositionalSharding' from 'jax.sharding'`, because uv picked jax 0.7.1 and avici has no upper bound. Pinning `jax==0.4.35 jaxlib==0.4.35 dm-haiku==0.0.13` made the import work, with numpy 1.26.4.
3. **The checkpoint download is blocked.** `avici.load_pretrained(download="scm-v0")` calls `huggingface_hub.hf_hub_download(repo_id="larslorch/avici", subfolder="scm-v0", ...)`, which fails with `httpx2.ProxyError: 403 Forbidden`. The session's egress proxy reports `connect_rejected` for `huggingface.co:443` ("gateway answered 403 to CONNECT"). That is a policy denial; I did not retry it or route around it.

**Outcome (typed): AVICI blocked by egress policy at the checkpoint download.** No avici method was added to `causalarena_methods.py`, so there are no AVICI rows and no comparison with the published AVICI row (semantic obs-only 0.278, formula obs-only 0.328).

To run it, the scm-v0 checkpoint (`scm-v0/kwargs.json`, `scm-v0/checkpoint_0300000.pkl`) has to reach the machine some other way, for example from the user's machine, and be loaded with `load_pretrained(checkpoint_dir=..., expects_counts=False)`.

## 7. CAP-17 package (`analysis/package_submission.py`; nothing submitted)

**Layout.**

- There is one package per method and column order, under `analysis/results/submission/<method>__{released,shuffled}/`. The validator rejects duplicate (method, family, graph, regime, repeat) keys and requires every row's method to equal `manifest.method_name`, so the shuffled control needs its own method name: `ccr-<Name>-colshuffled`.
- Each package has three parts:
  - `manifest.json`: the template fields plus `regime`, `controls`, `orientation_rule`, `shd_variant`, `nshd_definition`, `row_sources`, `families_missing` and `submitted: false`.
  - `summary.csv`: one row per file.
  - `predictions/<family>__<graph_key>__obs__rep<k>.npz`: `score_matrix`, `adjacency` and `node_order`, plus `committed` and `undecided`.

**Scoring rule.** Metrics use the random rule (the scoreboard rule). The packager rebuilds every adjacency with the same generator as `causalarena_io.directed_scores` and stops if any rescored F1 or SHD differs from the stored row. None differed. `nshd = shd / (d(d-1)/2)` is our own definition; the template does not define it. Timeout and failed rows leave their metrics blank, as the schema allows.

**Validator.** The validator (`external/causalarena/tools/validate_submission.py`, unmodified) passed all 10 packages with exit code 0. Its full output is in `analysis/results/submission/validator_output.txt`, and the index is in `packages.json`.

**Semantic rows are absent.** The semantic row files are not in this cloud copy, so `families_missing` lists `semantic` in every manifest. Rerunning `package_submission.py` where those files exist adds them, but that path is untested here.

## 8. Contracts and checks

- **Bytecode written under Causal-Copilot (housekeeping).** Importing the vendored causal-learn made Python write 56 new `.pyc` files into `../Causal-Copilot/externals/causal-learn/**/__pycache__`. No source file there changed: `SkeletonDiscovery.py` still has its 2026-05-15 mtime. I deleted the 56 session-created `.pyc` files (list in the session scratchpad). The 66 `.pyc` files that predate the session remain, but the `__pycache__` directory mtimes have changed. Future runs should set `PYTHONDONTWRITEBYTECODE=1`.
- **New `CONTRACT.json` files.**
  - `analysis/results/methods/CONTRACT.json`: there was none in this cloud copy. Merge it with the local copy if that one exists.
  - `analysis/results/submission/CONTRACT.json`.
  - Both name REP-07, BEN-07, BEN-11, CAP-17 and BND-06. `check_scores.py` reports "nonconforming: none" (`analysis/results/score_contract_report.json`).
- **The default paths of the generalised scripts are byte-identical, checked by running the pre-edit and post-edit copies side by side.**
  - `method_error_budget.py` (default `--family semantic`) on `pc_c1check_semantic_obs_rel.json`: sha256 1e9db043... for both outputs.
  - `bnd06_summary.py` (default arguments) on a directory of row files under the semantic names, with every file present and with one file missing: sha256 76a7d780... for both outputs.
  - The default code path in each script is the original lines, with the family-specific values looked up from the default.

## 9. Not done, and what is unexplained

- **AVICI:** blocked at the checkpoint download (section 6).
- **Unexplained:**
  - The NOTEARS F1 gap on synthetic (-0.099).
  - The PC formula SHD gap under the random rule (+2.57).
  - Why sequential-mode FCI differs from parallel-mode FCI.
  - What the published GIES and PC runs did on singular formula files. The candidate explanations above are consistent with the data but untested against the authors' code.
- **DOM-09 timing** was not attempted here. The wall times above come from a shared 2-core machine and are not a timing study.
