# Bundle 1: name-controlled runs on four named real datasets (design)

> Correction added 2026-10-07 after reading the fetched CausalArena index; the text below is otherwise as written before the runs. "Four of the six observational real datasets in CausalArena's real-data slice" is wrong. Three of these families match an indexed CausalArena entry in variables, edges and rows (Abalone, Concrete, Deutscher Wetterdienst). Auto MPG does not: CausalArena lists 4 variables, 3 edges, 398 rows; the repo's copy has 5 variables, 5 edges, 392 rows. CausalArena does not republish the tables, so even the three cannot be confirmed identical. Results: `bundle1_results.md`.

Written 2026-10-06, before any bundle-1 live run. Nothing here is a finding about Causal-Copilot.

## Purpose

Pass 4b showed on one dataset (Sachs) that the LLM review writes edges from column names and that the final graph scores below the algorithm's own output. Bundle 1 asks whether that holds on other named real datasets, and puts the unmodified pipeline on part of a public scoreboard: Abalone, Auto MPG, Concrete Compressive Strength and Deutscher Wetterdienst are four of the six observational real datasets in CausalArena's real-data slice (arXiv 2609.11897), and all four ship inside the Causal-Copilot repo with a reference graph.

Not in this bundle: CausalArena's synthetic-with-meaningful-names scenarios and the Causal Chambers physical data (they must be downloaded on Uzair's machine first; `cc.ps1 fetch` does that and is independent of the runs), any change to the pipeline, any fix.

## Axes and when each is bound

| Axis | Values | Bound by |
|---|---|---|
| Dataset family | abalone (4,177 rows, 8 variables, 7 reference edges), autompg (392, 5, 5), concrete (1,030, 9, 8), dwd (349, 5, 4) | `analysis/make_suite.py` |
| Column labels | real; neutral V01..; swapped (real names on other columns) | header line of each arm's CSV |
| File path shown to the LLM | opaque code (`k11` .. `k43`) in every arm | directory and file name |
| Repeat | 1..4 | plan file |
| Model, query, code | gpt-4o from `.env`; repo default query; baseline `a31aa7c` | checked per run by the harness |

The numbers are byte-identical across the three arms of a family (gate D1). The swapped labelling is a derangement chosen by exhaustive search to minimise pairs adjacent in both readings of the reference: 1 shared pair for abalone, autompg and concrete, 0 for dwd.

Arm codes: first digit = family (1 abalone, 2 autompg, 3 concrete, 4 dwd), second digit = role (1 real, 2 neutral, 3 swapped). Full mapping, hashes and both reference graphs per family: `datasets/suite_b1/MAPPING.json` and `datasets/suite_b1/_reference/`.

## Predictions, thresholds fixed in `analysis/stability.py` before the runs

| | Prediction | Supported if | Refuted if |
|---|---|---|---|
| N1 | In swapped arms, LLM-set final edges follow the labels | of distinct (family, edge) adjacent in exactly one reference, at least 80% are label-only, n >= 10 | at most 50%, n >= 10 |
| N2 | With neutral names the LLM writes at most half as many edges as with real names | holds in every family whose real arm has any LLM-set edge, at least 2 such families | holds in half of them or fewer |
| N4 | The final graph has lower adjacency F1 than the algorithm's own output | in at least 80% of completed runs, n >= 10 | in 50% or fewer |
| P3 | At most 25% of the algorithm's non-directed edges survive the bootstrap step | n >= 20 edges over distinct outputs | at least 50% survive |
| N5 | (exploratory) directed-edge F1 and adjacency F1 of algorithm output and final graph by role | reported, no verdict | |

N1 counts each distinct edge once per family, which answers the pseudo-replication caveat recorded for P1 in pass 4b. Anything between thresholds, or below the stated n, is reported as inconclusive.

These can fail. In the stub self-test PC oriented most edges on these datasets (43 of 47), so there may be too few non-directed edges for P3, and N4 is not guaranteed: if the algorithm's output is mostly directed, the bootstrap step keeps it.

Why directed-edge F1 is reported next to adjacency F1: DAG-level scoreboards such as CausalArena count only edges that commit to a direction. On the pass-4b Sachs runs the algorithm's output scored 0.00 on that metric (it had no directed edges) and the final graph 0.37, while adjacency F1 went the other way (0.61 to 0.53). The gap between the two metrics is part of what this bundle measures.

## Gates

| Gate | Check | Status |
|---|---|---|
| D1-D7 | suite construction: identical bodies, real header equals source, derangement, shared pairs as searched, parsed values identical, reference matches data, opaque names | PASS for all four families |
| R1-R6 | plan expansion: 48 runs, plan time limit applied, `research:` paths resolve, round-robin order, no stub flag on the live plan, a shorter command-line limit wins | PASS |
| S1-S7 | analysis on stub runs of 8 arms: families and roles resolved, identical numbers give identical algorithm-output scores across arms, swapped arms get a by-label table, directed-edge F1 present, T-gates pass, N1 not "supported" for a positional stub | PASS |
| Regression | the new analysis code reproduces every pass-4b verdict (P1-P5) and gate from the recorded live runs | PASS |
| T1-T6 | per-run and per-arm gates at analysis time (as in pass 4b) | evaluated after the runs |
| F1-F11 | `fetch_external.py` against a local stand-in server: pagination, size limits, unsafe paths refused, checksum mismatch refused, errors recorded without stopping, nothing written outside `external/`, second run downloads nothing | PASS against the stand-in; not yet run against the real hosts |

Pipeline completion with the stub LLM was checked for one arm of every family (abalone took about 170 s in the sandbox, the others 30-75 s).

## Must-show list for the live run

1. The plan result file lists 48 runs with an exit code each.
2. Every completed run: code identity OK, 11 state snapshots, lineage gates A-F pass.
3. Every arm has at least 3 completed runs; arms short of 3 are named.
4. Every run in an arm read the bytes recorded in `MAPPING.json` (T3) under the arm's labels (T4).
5. Per arm: algorithm and hyperparameters chosen; stage table with adjacency F1 and directed-edge F1 for S0, S1, final.
6. Verdicts for N1, N2, N4, P3 with their counts, and the N5 table.
7. Every failed run with the failing repo file and line.
8. Repo identity re-checked after the plan: unchanged.

## Failure modes named in advance, and the response

| Failure | Expected rate or sign | Response |
|---|---|---|
| Pipeline crash on malformed LLM JSON (`Initialize_state.py:178`, `judge_functions.py:562`) | about 1 run in 9 in pass 4b | 4 repeats per arm; any arm left with fewer than 3 completed runs gets a small top-up plan |
| LLM picks a slow independence test on abalone (4,177 rows) | run exceeds the time limit | plan-level limit of 45 minutes per run; the run is excluded and listed; if every abalone run times out, that is reported as the result for that family |
| Algorithm output is mostly directed | few non-directed edges | P3 inconclusive by its own n rule; N4 may be refuted; both are informative |
| Reference graphs are simple (stars for abalone and concrete) | low precision for any method | scores are read as agreement with the reference; N4 compares stages within a run |
| VS Code terminal freezes during a long plan | seen in pass 4b | run from a plain PowerShell window; the plan continues regardless and every run is recorded on disk |
| Disk | about 20-36 MB per run | about 1.5 GB for 48 runs |

## Cost and time (estimates from pass 4b)

About 2.2 million prompt and 0.3 million completion tokens, 2.5 to 3 hours. At the gpt-4o prices I know of (2.50 and 10 US dollars per million tokens; not re-checked) that is about 8 to 9 dollars.

## Commands (from `cc-research`, plain PowerShell)

    powershell -ExecutionPolicy Bypass -File .\cc.ps1 plan bundle1_names.json
    powershell -ExecutionPolicy Bypass -File .\cc.ps1 fetch

The second is independent, costs nothing, and can run before, during or after the first. It downloads the CausalArena dataset snapshot and a few tabular Causal Chambers datasets into `cc-research\external` (limits: 300 MB per file, 1.5 GB in total) and writes `external\FETCH_REPORT.json`.

Optional zero-cost check of the plan path first: `cc.ps1 plan bundle1_selftest_stub.json` (6 stub runs).

## After the runs

    python analysis/stability.py --runs-dir runs --label b1 --mapping datasets/suite_b1/MAPPING.json --repo <Causal-Copilot> --out analysis/results/stability_b1

Run from my side once the run folders exist.
