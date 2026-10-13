# Free steps after the desk audits: engines, controlled re-score, sortability, decision value, cost, ledger format

Tickets: AUD-27, AUD-28, AUD-29, AUD-30, AUD-31, BLD-13
Written 2026-10-12. No model calls. Every number below is in the named result file; scripts are re-runnable.

## 1. AUD-27 Engine oracle check (`analysis/engine_oracle_check.py` -> `results/engine_oracle/oracle.json`)

PC and FCI given a perfect independence oracle (d-separation in the true DAG), 120 random DAGs (6-12 variables),
6 column orders each (720 runs per engine). A correct implementation returns the true equivalence class every time.

| Engine | PC exact | DAGs with the same output in every order | FCI skeleton exact |
|---|---|---|---|
| Causal-Copilot's copy of causal-learn | 460 / 720 | 56 / 120 | 531 / 720 |
| causal-learn 0.1.3.8 (PyPI) | 720 / 720 | 120 / 120 | 720 / 720 |
| causal-learn 0.1.4.8 (PyPI) | 720 / 720 | 120 / 120 | 720 / 720 |
| gCastle 1.0.4 PC, `original` | 456 / 720 | 56 / 120 | |
| gCastle 1.0.4 PC, `stable` | 460 / 720 | 56 / 120 | |
| gCastle 1.0.4 PC, `parallel` | 720 / 720 | 120 / 120 | |

Every error is an extra connection: a separating set that was never tested. This confirms AU6's code reading: the
defect is in Causal-Copilot's modified copy (not in causal-learn 0.1.3.8), and gCastle's default `original` and
`stable` settings have the same one-sided search. Causal-Copilot's PC gets 36% of perfect-information problems wrong.
Two further observations: the copy's FCI step gave 533 then 531 correct runs on identical inputs (not deterministic
under threads), and its d-separation test fails in joblib worker processes (a missing import), so Causal-Copilot cannot
run its own oracle test as shipped.

## 2. AUD-28 Controlled re-score (`analysis/rescore_controls.py`, `pc_upstream_run.py`, `pc_orientation_order.py`)

Every baseline we can run, released vs shuffled columns, paired by file, semantic and formula public halves
(`results/rescore/rescore.json`). Directed F1 under the expectation rule (undecided pairs at random):

| Method | Semantic released | Semantic shuffled | Formula released | Formula shuffled | Published (semantic / formula) |
|---|---|---|---|---|---|
| PC, upstream causal-learn | 0.356 | 0.426 | 0.298 | 0.349 | 0.333 / 0.220 |
| PC, Causal-Copilot copy | 0.335 | 0.428 | 0.304 | 0.356 | |
| GES (BIC) | 0.528 | 0.528 | 0.468 | 0.471 | 0.552 / 0.467 (GIES) |
| FCI | 0.358 | 0.361 | 0.311 | 0.318 | not on the board |
| DirectLiNGAM | 0.196 | 0.194 | 0.255 | 0.244 | 0.203 / 0.240 |
| NOTEARS | 0.146 | 0.146 | 0.169 | 0.168 | 0.203 / 0.185 |

Two layout effects, in opposite directions:
1. **The authors' rule reads the order** (undecided pairs drawn earlier column -> later). Gain on released files:
   GES +0.022 semantic, +0.021 formula; FCI +0.218 / +0.200 (not on the board).
2. **PC orients worse when the columns arrive in causal order.** Same skeleton in both arms (upstream PC S = 0.613 /
   0.613), but commit accuracy q 0.59 released vs 0.74 shuffled; shuffling helps on 175 of 185 paired semantic files.

Mechanism (`results/rescore/pc_orientation_order.json`, 112 semantic files, prediction written in the script before
the run): finite-sample collider decisions conflict, and PC's conflict rule resolves them in index order.

| Collider rule | q released | q shuffled | gap |
|---|---|---|---|
| default (uc_sepset, priority 2: keep existing colliders) | 0.592 | 0.740 | +0.148 |
| uc_sepset, priority 0 (overwrite) | 0.886 | 0.730 | -0.156 |
| maxP (uc_rule 1) | 0.827 | 0.828 | +0.001 |
| definite maxP (uc_rule 2) | 0.802 | 0.803 | +0.000 |

Prediction met (gap under 0.03 for both order-free rules). In causal column order, "keep the first collider" keeps the
wrong one and "overwrite" keeps the right one: either way the score reads the layout. With maxP, PC's directions are
right 83% of the time in any order, which by F1 = S x a (family means) gives about 0.46 on semantic files: above every
published row except FoundCause (0.634) and GIES (0.552), from a configuration change.

## 3. AUD-29 Sortability (`analysis/sortability_audit.py` -> `results/sortability/sortability.json`)

The release stores standardised columns, so varsortability is exactly 0.5 (no leak through scale). R2-sortability
(path-weighted, Reisach et al. 2023): semantic 0.545 (range 0.14-0.91), formula 0.603 (0.14-0.95); edge-only 0.570 /
0.597. CausalArena does not leak order through marginal statistics on average; individual scenarios do (up to 0.95).

## 4. AUD-30 Decision value (`analysis/decision_value.py` -> `results/decision_value/decision_value.json`)

For each released intervention target T and every other variable Y: does the learned graph say correctly whether
setting T moves Y? Committed claims: "yes" if Y is reachable by committed arrows, "no" if unreachable even through
undecided pairs; otherwise the method abstains. Checked against the true graph.

| Semantic | Coverage | Precision of committed claims | Ancestor AID (lower better) |
|---|---|---|---|
| Ceiling: true CPDAG | 0.925 | 1.000 | 0.098 |
| **Baseline: empty graph ("nothing moves")** | 1.000 | **0.643** | **0.260** |
| GES (BIC) | 0.951 | 0.753 | 0.266 |
| PC upstream, shuffled / released | 0.947 / 0.948 | 0.696 / 0.662 | 0.291 / 0.317 |
| PC Causal-Copilot copy, released | 0.946 | 0.643 | 0.332 |
| FCI | 0.408 | 0.712 | 0.657 |
| DirectLiNGAM | 1.000 | 0.653 | 0.283 |
| NOTEARS | 1.000 | 0.646 | 0.278 |

Formula: empty graph 0.704; GES 0.806; PC 0.733-0.755; LiNGAM 0.710; NOTEARS 0.703.

**Reading.** On the question a user actually asks of a causal graph, DirectLiNGAM, NOTEARS and Causal-Copilot's PC
(released order) are within 0.01 of answering "nothing moves" for every pair; upstream PC adds 0.02-0.05 and GES 0.11.
By the adjustment-identification distance only GES comes close to the empty graph, and no method beats it. The data-only ceiling is far above all of them (precision 1.000 at 92.5% coverage). This is
why F1 alone misleads: GES and PC differ by 0.17 F1 but the question that matters separates them by 0.06-0.09.
Caveats: AID is undefined for graphs with directed cycles (gadjid refused 20 of 225 upstream-PC and 40 of 250
copy-PC semantic graphs; their AID is averaged over the rest). The empty-graph and ceiling rows use all 250 files; each method row uses the files that method finished (225 for GES and upstream PC), so the comparison is not yet paired by file (AB-04 pairs it). Checking claims against the held-out interventional rows
instead of the true graph is unreliable here: the true DAG itself agrees with the data on only 70.6% of pairs, because
many released interventions move nothing detectable (BEN-09).

## 5. AUD-31 Cost of one Causal-Copilot run (`results/stability_s2/cost_per_run.json`)

The approved one-run cost check is answered by the 30 live BND-08 runs already logged: median $0.457 per run (range
0.270-0.567) at gpt-4o list prices, 36 model calls, 11.5 minutes; total $12.68 for 30 runs (3.32M prompt and 0.44M
completion tokens, from the API's own usage records). No new run was needed; nothing was spent.

## 6. BLD-13 Claim-ledger record format and verifier (`ledger/`)

`ledger/DESIGN.md` (objects, binding times, the failures the format prevents), `ledger/schema.py` and
`ledger/schema/ledger.schema.json` (JSON Schema), `ledger/verify.py` (checks V1-V8: schema, evidence closure, knowledge
never connects, interventions outrank knowledge, knowledge honoured, hash, order invariance, floor; and the limits it
cannot check), `tests/test_ledger_verify.py` (a toy ledger that passes and eight corruptions, each caught).

## What these change

1. The headline for the audit paper is no longer only "agents read names". Layout enters the scoreboard through three
   independent channels: the authors' orientation rule (+0.02 GES, +0.2 FCI), PC's conflict resolution (-0.07), and the
   agent's own engine copy (36% wrong with perfect information). A controlled scoreboard needs all three neutralised.
2. Decision value is where the field is weakest and the ceiling is highest: learned graphs barely beat "nothing moves";
   the data-only ceiling is near perfect. That gap, not the F1 gap, is the opening for the ledger.
3. The one-run cost check needs no spend; agent costs for the field audit are the open budget question.

## Erratum (2026-10-13)

Section 2 estimated PC with maxP at "about 0.46" from F1 = S x a applied to family means. AB-09 (T1) shows the identity is
exact per file, not for family means. The measured value is 0.462 on semantic (AB-01, `analysis/results/rescore_v2/`);
the estimate stands, but by measurement, not by the identity.
