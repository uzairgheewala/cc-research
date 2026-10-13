# Bundles 2 to 5: design

> Superseded as the organising plan by `program_v2.md` (2026-10-07). Still current: section 3 (failure modes X1-X14), the agent runs of bundle 2 (now item A2), the gates. The statement in section 1 that 100%-type scores signal leakage is corrected in `error_budget_and_order.md`: the identifiable limit on these graphs is about 0.96.

Written 2026-10-07, after bundle 1 and before any bundle-2 run. Nothing in this file is a finding; findings are in `bundle1_results.md`. Each bundle ends in one live run on Uzair's machine and a must-show list that decides whether it worked.

## 1. What the remaining work has to establish

Bundle 1 and the external checks changed the question. A graph returned by an agent can come from three places: the numbers, the labels (variable names), or the layout (column order, file path). The measurements so far:

| Source | Evidence so far |
|---|---|
| Labels | With real names 91% of Causal-Copilot's final edges are written by the LLM review; with neutral names 0%; with names on the wrong columns 90%, and the graph follows the names. |
| Layout | In every released CausalArena sample file the columns are in a causal order (all 2,068 semantic, 1,714 formula and 50,421 synthetic edges checked run earlier -> later). A 20-line regression that reads the order scores 0.680 on the public semantic files, above every published row; 0.269 after a column shuffle. |
| Numbers | The algorithm's own output is degraded by the bootstrap step in all 12 bundle-1 arms. |

So the capstone's claim is no longer "the refinement makes graphs worse". It is: **current scores for causal-discovery agents do not say where the graph came from; under controls that do, Causal-Copilot's graph comes from the labels; here is a refinement stage that keeps the data's graph, labels every edge with its source, and is scored under those controls on a public scoreboard.** Bundles 2-5 are the shortest path to that.

| Bundle | Establishes | Live cost (estimate, replaced by a measurement before each run) | Target date |
|---|---|---|---|
| 1c | closes bundle 1 (top-up, Causal Chambers download) | 6 runs, about 35 min, about $1; download free | 9 Oct |
| 2 | the label and layout effects on a public scoreboard's own data, in its own units | 30 agent runs + 150 single calls; $15-40; 8-20 h unattended | 16 Oct |
| 3 | a refinement stage that does not fall below its algorithm; names used only where the data leave a direction open | replay free; about 30 short runs, under $10 | 30 Oct (Q1 checkpoint 2 Nov) |
| 4 | use of intervention data | free (no LLM) unless combined with bundle 3's name step | 13 Nov |
| 5 | scoreboard-format package, report, website, poster | none | 4 Dec (Q1 final) |

## 2. Axes, and when each is bound

| Axis | Values | Bound when, by what |
|---|---|---|
| Benchmark family | CausalArena semantic, public half (50 scenarios x 5 replicates); bundle 4 adds the obs+int files and Causal Chambers | fixed here |
| Scenario subset for agent runs | the first released scenario of each of the 10 domains, by numeric prefix of its folder name; replicate 0 | rule fixed here; list written by the suite builder and hashed before any run |
| Regime | observational (bundles 2-3); observational + interventional (bundle 4) | fixed here |
| Labels | real; neutral (`V01`..); swapped (real names on other columns) | suite builder, seeded |
| Column order | shuffled once per scenario by a seeded permutation, identical in all arms; the released order is used only in the no-LLM order checks | suite builder, seeded |
| File path shown to the agent | opaque code in every arm | suite builder |
| System | unmodified pipeline; plain PC (published configuration); names-only model; v1, v2, v3 of the new stage (bundles 3-4) | code identity checked per run |
| Endpoint | S0 algorithm output, S1 after the bootstrap step, **S3 before the cycle step (primary)**, S4 final when the run completes | fixed here, because 8 of 8 cycle-step entries crashed |
| Score | directed-edge precision, recall, F1 with undirected edges oriented at random per file (the published rule; reproduces the published PC F1: 0.335 against 0.333); adjacency F1; SHD reported but not compared with published SHD (does not reproduce: 37.5 against 33.5) | fixed here |
| Model | whatever `.env` names (gpt-4o); snapshot recorded per run, one snapshot per bundle required | run time; gate |
| Thresholds of every prediction | in code | before the live run, by file hash recorded in the plan note |

## 3. Failure modes named in advance

| # | Failure | How it would show | Guard |
|---|---|---|---|
| X1 | Cost or time grows faster than expected at 17-25 variables (253 pairs instead of 28) | stub run shows prompt size and wall time | the stub self-test measures both per scenario; the live plan is cut to the first 5 domains alphabetically if the measured total exceeds $50 or 24 h |
| X2 | Named-arm runs crash in the cycle step (8 of 8 so far) | no final graph | S3 is the primary endpoint and exists for every run that reaches refinement (`partial_stages.py`, gates Q1-Q3) |
| X3 | A run crashes before refinement (3 of 78 so far) or times out | no S3 | one rerun per missing (scenario, arm), once; a second failure is reported as missing, never replaced by another scenario |
| X4 | One scenario is pathologically slow (PC: 0.3 s median, 105 s worst) | timeout at 45 min | recorded as status `timeout`; counted in the denominator of every "k of 10" prediction as not meeting it |
| X5 | Our scorer differs from the scoreboard's | PC calibration | gate C1 (passes); SHD not compared until C2 passes |
| X6 | Column order leaks into the agent | none visible in scores | columns shuffled in every arm; no-LLM check that PC's score does not depend on order |
| X7 | A real name leaks into a neutral arm (path, default folder, template) | prompt scan | gate T7: every neutral-arm prompt before the final graph searched for every real name of the scenario; template matches must be identical in all arms |
| X8 | The swap test is confounded by graph shape (bundle 1: abalone's star) | "data-only" edges at chance level | permutation null: the count of data-only edges is compared with its distribution under 1,000 seeded random relabelings of the data-side reference |
| X9 | The semantic "truth" is itself model-written, so a model can recover it from names | names-only baseline scores high | measured on purpose (prediction M5); swapped arm separates names from data regardless |
| X10 | The public half differs from the unpublished half | cannot be seen | every comparison with a published number is stated as "public 50 against full 100" with the calibration tolerance |
| X11 | The pipeline's preprocessing changes the variables (drops or recodes columns of standardised or near-constant data) | column count differs | gate T4 (labels and count as intended) per run; a scenario failing it is reported, not patched |
| X12 | Choosing thresholds after seeing results | n/a | thresholds in code before the run; anything else is labelled exploratory |
| X13 | A d = 23 derangement cannot be searched exhaustively | n/a | seeded local search; the achieved overlap is reported and not called minimal; shared pairs are excluded from the swap test by construction |
| X14 | Model snapshot changes between arms | T6 | whole bundle rerun or stratified by snapshot; never pooled silently |

## 4. Bundle 1c (ready now)

Two commands, independent of each other.

1. `cc.ps1 plan bundle1_topup.json`: 3 more repeats each of `k11` and `k43`. Stopping rule fixed in the plan file: once, no second top-up; all completed runs enter the analysis under label `b1`. Must show: 6 exit codes; gate T2 passes or the arm is reported as still short; N1, N2, N4, P3 recomputed (verdicts may move; thresholds do not).
2. `cc.ps1 fetch`: Causal Chambers archives, sizes listed first. Must show: `FETCH_REPORT.json` lists the size of all 20 archives; `lt_interventions_standard_v1` extracted with CSV files, or a skip line stating the size it needs.

## 5. Bundle 2: label and layout effects on CausalArena's public semantic scenarios

### 5.1 Parts

| Part | LLM | Where it runs | What it produces |
|---|---|---|---|
| 2a Suite builder (`make_suite_ca.py`) | no | sandbox | 10 scenarios x 3 arms as CSV with shuffled columns, both references in the repo's convention, `MAPPING.json` (format 2, so `stability.py` and `partial_stages.py` work unchanged) |
| 2b Baseline rows | no | sandbox | plain PC (done: 0.335), order-reading regression (done: 0.680 / 0.269), PC under column shuffle |
| 2c Bootstrap-step replay | no | Uzair's machine, in the container, one command | S0 and S1 for PC on replicate 0 of all 50 scenarios, using the repo's own bootstrap functions; 20-minute limit per file |
| 2d Names-only baseline (`names_only.py`) | yes, 150 single calls | Uzair's machine | the model's edge list from variable names alone, for 50 scenarios, in three presentations: real names shuffled; real names in released order; neutral names in released order |
| 2e Agent runs | yes, 30 runs | Uzair's machine | unmodified pipeline on 10 scenarios x {real, neutral, swapped} |

Part 2d is a new kind of call: a script of mine, outside the repo, sending one request per scenario through the same key and model as the pipeline, recorded in the same format. The prompt is fixed in the script before the run and is in the must-show list. It is in the design because it is the only clean measure of what names alone are worth on this benchmark; it needs Uzair's explicit yes.

### 5.2 Predictions (thresholds go into code before the run)

| | Prediction | Supported if | Refuted if |
|---|---|---|---|
| M1 | The bootstrap step lowers adjacency F1 below the algorithm's own output (PC, 50 files, no LLM) | >= 80% of files | <= 50% |
| M2 | Names carry the agent's score: S3 directed-edge F1 with real names exceeds neutral names by at least 0.10 | >= 8 of 10 scenarios | <= 5 of 10 |
| M3 | In swapped arms LLM-set S3 edges follow the labels: of distinct (scenario, edge) adjacent in exactly one reference, the label-only share | >= 80%, n >= 30, and the data-only count not above the 95th percentile of the permutation null | <= 50% |
| M4 | Without names the agent is below its own toolbox: neutral-arm S3 directed-edge F1 below plain PC on the same file | >= 8 of 10 | <= 5 of 10 |
| M5 | Names alone reach a standard data-driven method: names-only (real names, shuffled) mean directed-edge F1 over 50 scenarios | >= 0.333 (published PC) | <= 0.252 (published random-order regression) |
| E1 | exploratory: real-name agent S3 against the published table (FoundCause 0.634, GIES 0.552) | reported | |
| E2 | exploratory: names-only in released order against shuffled; neutral names in released order (does the model read position?) | reported | |
| E3 | exploratory: share of S3 edges set by the LLM per arm; cycle-step entries and outcomes; runtime | reported | |

I do not know how M2 and M5 will come out. M5 in particular could fail: 23 variables and 41 edges is a harder recall task than an 8-variable star.

### 5.3 Gates

D1-D7 as in bundle 1, plus D8 (each reference equals the transpose of the released `g` and the edge list of `graph.json`), D9 (column permutation recorded; after it, the share of reference edges running earlier -> later is reported per scenario and is not 100%), D10 (swap overlap reported). C1 (scorer reproduces the published PC F1). R-gates for the plan. S-gates on a stub run of at least 2 scenarios x 3 arms, which also yields the cost and time measurement for X1. T1-T7 at analysis time. Q1-Q3 for the S3 endpoint.

### 5.4 Must-show list for the bundle-2 live run

1. Plan result: 30 exit codes; reruns under X3 listed.
2. Per run: code identity OK; model snapshot; reached S3 or the reason it did not.
3. T3, T4, T7 pass for every run; T6 one snapshot.
4. Table per scenario: S0, S1, S3 directed-edge F1 and adjacency F1 for the three arms; plain PC on the same file.
5. M1-M5 verdicts with their counts; E1-E3 tables.
6. Names-only: the exact prompt, 150 responses parsed or counted as unparseable, scores for the three presentations.
7. Cost and time measured, against the estimate.
8. Repo byte-identical to `a31aa7c` afterwards.

## 6. Bundle 3: a refinement stage that keeps what the data found

Built outside the repo; takes what the pipeline already records (algorithm output, the seven bootstrap frequency tables, the data) and returns a graph in which every edge has a recorded source. The pipeline is not modified.

**v1, no LLM.** Confidence is computed for "connected" (any edge type) separately from "direction". An adjacency of the algorithm's output is kept when connected in at least half of the resamples; an absent adjacency is added only when connected in at least 90% (the pipeline's own figure); the edge type is the commonest type among resamples, and a direction is committed only when that direction is the commonest type. These three numbers are fixed here and not tuned; a table at other values is labelled exploratory. Malformed model output cannot crash the stage because v1 has no model call.

Evaluation is by replay and costs nothing: development set = every bootstrap table already recorded (75 live runs that reached refinement, plus the offline cells with ground truth); test set = the 50 CausalArena files from part 2c, touched only after the rule is frozen.

| | Prediction | Supported if | Refuted if |
|---|---|---|---|
| R1 | v1 is not below the algorithm: adjacency F1 >= algorithm output - 0.02 | >= 90% of test files | < 70% |
| R2 | v1 is above the pipeline's bootstrap step (S1) on adjacency F1 | >= 90% of test files | < 70% |
| R3 | v1's directed-edge F1 (published rule) is not below the algorithm's | mean difference >= -0.01 | <= -0.05 |

**v2, names where the data are silent.** The model is asked only about pairs that v1 leaves adjacent and unoriented, three paraphrases each; an answer is used only if all three agree, it creates no cycle, and it does not contradict a separating set the algorithm recorded. Each such edge is stored with source "names". The stage validates the reply's structure, retries once, then abstains.

| | Prediction | Supported if | Refuted if |
|---|---|---|---|
| R4 | With neutral names v2 equals v1 | 0 name-sourced edges in >= 9 of 10 scenarios | > 2 scenarios with any |
| R5 | Wrong names do bounded damage: with swapped names, v2's adjacency F1 equals v1's (by construction) and its directed-edge F1 by data is within 0.05 of v1's | >= 8 of 10 | <= 5 of 10 |
| R6 | Right names help: with real names v2's directed-edge F1 exceeds v1's | >= 8 of 10 | <= 5 of 10 |

The reported table has two columns for v2, "data only" and "data + names", so a reader can see what the names bought.

Must show: replay tables for R1-R3 on development and test sets with the frozen thresholds' file hash; 30 short runs for R4-R6 with T-gates; zero crashes; every edge of every output graph carrying a source.

## 7. Bundle 4: interventions

Uses the released obs+int files (800 + 200 rows, 3-7 single-variable targets, flags per cell). v3 = v1 plus one rule: for a target T and a variable Y adjacent to T, Y's distribution is compared between rows where T was set and observational rows (Welch test, Holm correction at 1% within the file); a shift orients T -> Y, no shift orients Y -> T; standard propagation rules follow. No LLM.

Published methods gain little from the interventional rows on this family (TabCausal +0.025, GIES +0.016, CaScaLe +0.042 directed-edge F1).

| | Prediction | Supported if | Refuted if |
|---|---|---|---|
| R7 | v3 on obs+int exceeds v1 on the observational file of the same scenario by at least 0.05 directed-edge F1 (mean over 50 public scenarios, replicate 0) | >= 0.05 | <= 0.01 |

Causal Chambers (two physical systems, 32-38 variables) is added if the download succeeds, under our own stated sampling because CausalArena's sample is not republished. Known risk: the benchmark's authors report that PC timed out on both, so the full agent is not run there; v1 and v3 are, with a conditioning-set cap stated in advance.

## 8. Bundle 5: package and write-up

A results package in the scoreboard's format (`summary.csv`, prediction files, `manifest.json`), passing its validator, with rows for plain PC (the calibration row), the unmodified agent (real and neutral names), v1, v2 and v3, all on shuffled columns. The arm is carried in `config_note`, since the schema has no field for it. Whether to submit it, and whether to send the maintainers the column-order note, is Uzair's decision. Course deliverables: report, website, poster, public repository of `cc-research`.

## 9. What is deliberately not in the plan

- Running the published foundation models ourselves (GPU, checkpoints). Their numbers are quoted from the published table.
- Any change inside the `Causal-Copilot` tree.
- Tuning anything on the test files.
- A claim about the unpublished half of the benchmark.

## 10. Decisions needed from Uzair

1. Run the two bundle-1c commands.
2. Approve bundle 2 as designed, including part 2d (the names-only calls).
3. Whether to tell CausalArena's maintainers about the column order now, later, or not at all. A dated note would establish that the observation was made here; I can draft it, he would send it.
