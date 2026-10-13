# Pass 4b: run-to-run stability and the name-versus-data test (design; live runs pending)

Status: this file is the design as written before the live runs. The runs happened on 2026-10-06; results are in `pass4b_results.md`. Nothing in this file is a finding about Causal-Copilot.

## Questions

1. If the same command is run again on the same data, how much of the result is the same: the algorithm chosen, the hyperparameters, the LLM's per-pair answers, the final edges?
2. Do the edges the LLM review writes follow the column names or the numbers?

## Axes, fixed before the runs

| Axis | Values | Bound when |
|---|---|---|
| Data | sachs numbers (853 rows, 11 columns); Linear_Gaussian; LiNG 10 nodes | plan file |
| File path seen by the LLM | contains "sachs"; neutral | dataset directory |
| Column labels | real, on their own columns; neutral V01..V11; real but moved to other proteins' columns | header line of the CSV |
| Repeat | 1..5 (3 for LiNG) | plan file |
| Model, query, code | gpt-4o as in `.env`; repo default query; baseline `a31aa7c` | checked per run by the harness |

Not varied in this pass: the model, the query wording, the temperature (repo default), the number of bootstrap resamples.

## Arms

| Arm | File | Path says "sachs" | Labels | Runs |
|---|---|---|---|---|
| sachs | `datasets/sachs/sachs.csv` (byte-identical copy of the repo file) | yes | real, aligned | 5 |
| d01 | `datasets/d01/d01.csv` | no | real, aligned | 5 |
| d02 | `datasets/d02/d02.csv` | no | V01..V11 | 5 |
| d03 | `datasets/d03/d03.csv` | no | real, deranged | 5 |
| Linear_Gaussian | repo dataset, ground truth | n/a | X1..X5 | 5 |
| LiNG 10 nodes | repo dataset, ground truth | n/a | X0..X9 | 3 |

28 runs, interleaved round-robin so that time of day is not confounded with arm. Plan file: `plans/pass4b_stability.json`.

The four sachs arms contain the same numbers: everything after the header line is byte-identical (gate D1). In d03 no label sits on its own column, and the labelling was chosen by an exhaustive deterministic search to minimise the number of pairs that are adjacent both in the reference graph read by label and in the reference graph read by data. The minimum is 1 pair of 19; a labelling with 0 does not exist for this graph. Mapping, hashes and both reference graphs: `datasets/MAPPING.json`, `datasets/_reference/`.

## What each comparison isolates

- sachs versus d01: the effect of the word "sachs" in the path, with names and numbers held fixed.
- d01 versus d02: the effect of meaningful names, with path and numbers held fixed.
- d03: names and numbers disagree, so an edge that matches the by-label reference and not the by-data reference was written from the names.
- Linear_Gaussian and LiNG: names carry no domain meaning and the truth is known, so they give the stability picture without domain knowledge.

## Predictions, with thresholds fixed in `stability.py` before any live data

| | Prediction | Supported if | Refuted if |
|---|---|---|---|
| P1 | In d03, LLM-set final edges follow the labels, not the data | among such edges adjacent in exactly one reference, at least 80% are label-only, n >= 10 | at most 50%, n >= 10 |
| P2 | Without meaningful names the LLM writes far fewer edges | mean LLM-set edges per run in d02 is at most half of d01 | otherwise |
| P3 | The bootstrap step deletes the algorithm's non-directed edges in live runs as it does offline | at most 25% of them remain adjacent, n >= 20 edges over distinct outputs | at least 50% remain |
| P4 | (exploratory) "sachs" in the path changes final adjacency F1 | reported, no verdict | |
| P5 | (exploratory) the chosen algorithm is not the same in every repeat | reported, no verdict | |

P3 was first written as "fewer than half of all adjacencies survive in every run". The stub self-test showed that form mixes directed edges, which survive, with non-directed ones, so it was restated by edge type before any live repeat existed. Anything between the two thresholds is reported as inconclusive.

What would count against the working picture from pass 4a: P1 refuted would mean the LLM review is responding to something in the numbers (through the statistics pasted into its prompt) and not only to names; P2 refuted would mean the review adds edges even with no semantic cue.

## Gates in `stability.py`

| Gate | Check | Blocking |
|---|---|---|
| T1 | each included run completed, passed code identity, and passed lineage gates A-F; excluded runs are listed with the reason | yes, if an arm is left empty |
| T2 | each arm has at least 3 included runs | yes |
| T3 | every run in an arm read the same dataset bytes, equal to the hash in `MAPPING.json` | yes |
| T4 | the variable names the pipeline saw equal the arm's labels | yes |
| T5 | accuracy recomputed from the stage matrices equals `lineage.py`'s | yes |
| T6 | one served model snapshot per arm | reported only |

## Self-test already done (stub LLM, no cost, sandbox)

Six stub runs across d02, d03 and LiNG, plus one run that failed for an unrelated reason (two pipelines at once exhausted the sandbox's memory), were analysed with `stability.py`. Known-answer checks, all passed:
- every request repeated across stub runs received the identical answer (the stub is deterministic);
- the failed run was excluded and listed with its reason;
- T2 failed, correctly, because one arm had a single run;
- d02 and d03 scored identically against the by-data reference at S0 (same numbers, different labels);
- P1 was not "supported" (the stub answers by position, so its edges should follow neither names nor data);
- one bootstrap table per algorithm choice in every arm.

Output: `results/stability_selftest_stub/stability.md`. The plan runner's new `research:` dataset prefix and `interleave` switch were exercised by the same self-test (`plans/selftest_stub.json`).

## Cost and time, estimated from the golden runs

A sachs run used about 66,000 prompt and 7,700 completion tokens and took about 2 minutes 10 seconds; a Linear_Gaussian run about 33,000 and 5,300. For 28 runs that is roughly 1.7 million prompt tokens, 0.2 million completion tokens and about one hour. At the gpt-4o list prices I know of (2.50 and 10 US dollars per million tokens, which may have changed) that is around 6 dollars. Disk: about 20-36 MB per run, under 1 GB in total.

## After the runs

    python analysis/stability.py --runs-dir runs --label p4b --mapping datasets/MAPPING.json --repo <Causal-Copilot> --out analysis/results/stability_p4b

I run this from my side once the run folders exist; it needs no API access.
