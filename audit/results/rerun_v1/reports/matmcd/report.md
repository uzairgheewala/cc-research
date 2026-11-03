# Audit: matmcd

Protocol v1.0 (thresholds 1.0, sha256 6fbded46952a...). Battery `ca-ab06` v1 (development, 10 items, 10 scenario clusters; hash 561af73ae72f...).

System: `matmcd`; adapter matmcd v1; takes context, data, names; gives marks -- ->; per-edge source exposed.

## L0: what it gets right (per arm; compare a row only with rows of the same regime)

| Arm | Regime | Runs | ok | Completion | Directed F1 (expectation rule, completed) | same, delivered | Adjacency F1 | DV-1 precision | DV-1 coverage | USD |
|---|---|---|---|---|---|---|---|---|---|---|
| real | D+K | 10 | 10 | 1.000 | 0.380 | 0.380 | 0.580 | 0.685 | 1.000 | 3.23 |
| neutral | D | 10 | 10 | 1.000 | 0.251 | 0.251 | 0.569 | 0.662 | 1.000 | 2.95 |
| swapped | D+K | 10 | 10 | 1.000 | 0.259 | 0.259 | 0.565 | 0.659 | 1.000 | 3.23 |

References are simulated graphs (tier T1: exact (simulated)), so these numbers are accuracy.

## Findings (closed list, protocol v1)

| ID | Kind | Verdict | Effect [95% interval] | Label | Note |
|---|---|---|---|---|---|
| K01 | crash | **clear** | 0 of 30 runs: 0.000 [0.000, 0.114] | exploratory |  |
| K02 | no_better_than_null | **fires** | 0.015 [-0.009, 0.040], 10 units | exploratory |  |
| K03 | cost_outlier | **clear** | USD/run 0.314 vs round median 0.654: ratio 0.48 | exploratory |  |
| K04 | name_reliance | **fires** | 0.122 [0.048, 0.189], 10 units | confirmatory |  |
| K05 | wrong_knowledge_harm | **clear** | -0.007 [-0.064, 0.038], 10 units | exploratory |  |
| K06 | layout_reliance | **not_run** | - | exploratory | battery has no layout arms (columns were always shuffled) |
| K07 | knowledge_degrades_data | **fires** | -0.034 [-0.066, 0.001], 10 units | confirmatory |  |
| K08 | robustness_drop | **not_run** | - | exploratory | robustness transforms are defined (controls/transforms.py); not run in v1 |
| K09 | knowledge_ignored | **not_run** | - | exploratory | oracle and wrong suppliers are defined; not run in v1 |
| K10 | stage_deletes_supported_links | **clear** | -0.001 [-0.008, 0.005], 10 units | exploratory | stage pc_only_initial -> final |
| K11 | stage_follows_names | **not_checkable** | - | exploratory | needs stage traces and a T4 label reference for the swapped arm |
| K12 | stage_flips_data_direction | **clear** | right to wrong 45, wrong to right 34 | exploratory | stage pc_only_initial -> final |
| K13 | unsourced_claims | **clear** | unsourced 0, committed 762 | exploratory |  |
| K14 | overconfident | **not_checkable** | - | exploratory | the system states no confidence |
| K15 | never_abstains | **fires** | coverage 1.000, precision 0.685 (779 committed claims, real arm) | exploratory |  |

## L2: what each stage does (real names)

| Stage | Adjacency F1 change [95%] | Right->wrong | Wrong->right |
|---|---|---|---|
| pc_only_initial -> final | -0.001 [-0.008, 0.005], 10 units | 45 | 34 |

## Typed gaps (what this audit could not say, and why)

- K06 layout_reliance: not run, battery has no layout arms (columns were always shuffled)
- K08 robustness_drop: not run, robustness transforms are defined (controls/transforms.py); not run in v1
- K09 knowledge_ignored: not run, oracle and wrong suppliers are defined; not run in v1
- K11 stage_follows_names: not checkable, needs stage traces and a T4 label reference for the swapped arm
- K14 overconfident: not checkable, the system states no confidence

Exploratory labels: the kind's threshold was registered on 2026-10-30, after these runs; such a finding is confirmatory only for runs recorded after thresholds_v1.json was hashed.

Runs: 30 recorded runs (manifest sha256 8a4d9e0703eb...). Recompute everything: `python -m audit verify <this folder>/certificate.json`.
