# Audit: vashishtha

Protocol v1.0 (thresholds 1.0, sha256 6fbded46952a...). Battery `ca-ab06` v1 (development, 10 items, 10 scenario clusters; hash 561af73ae72f...).

System: `vashishtha`; adapter vashishtha v1; takes context, data, names; gives marks -- ->; per-edge source exposed.

## L0: what it gets right (per arm; compare a row only with rows of the same regime)

| Arm | Regime | Runs | ok | Completion | Directed F1 (expectation rule, completed) | same, delivered | Adjacency F1 | DV-1 precision | DV-1 coverage | USD |
|---|---|---|---|---|---|---|---|---|---|---|
| real | D+K | 10 | 5 | 1.000 | 0.426 | 0.426 | 0.603 | 0.720 | 0.994 | 6.09 |
| neutral | D | 10 | 0 | - | - | - | - | - | - | 0.00 |
| swapped | D+K | 10 | 5 | 1.000 | 0.406 | 0.406 | 0.603 | 0.718 | 0.988 | 6.50 |

References are simulated graphs (tier T1: exact (simulated)), so these numbers are accuracy.

## Findings (closed list, protocol v1)

| ID | Kind | Verdict | Effect [95% interval] | Label | Note |
|---|---|---|---|---|---|
| K01 | crash | **clear** | 0 of 10 runs: 0.000 [0.000, 0.278] | exploratory |  |
| K02 | no_better_than_null | **clear** | 0.053 [0.025, 0.081], 5 units | exploratory |  |
| K03 | cost_outlier | **clear** | USD/run 1.259 vs round median 0.654: ratio 1.92 | exploratory |  |
| K04 | name_reliance | **clear** | 0.020 [-0.007, 0.046], 5 units | confirmatory |  |
| K05 | wrong_knowledge_harm | **inconclusive** | - | exploratory |  |
| K06 | layout_reliance | **not_run** | - | exploratory | battery has no layout arms (columns were always shuffled) |
| K07 | knowledge_degrades_data | **clear** | 0.002 [-0.006, 0.013], 5 units | confirmatory |  |
| K08 | robustness_drop | **not_run** | - | exploratory | robustness transforms are defined (controls/transforms.py); not run in v1 |
| K09 | knowledge_ignored | **not_run** | - | exploratory | oracle and wrong suppliers are defined; not run in v1 |
| K10 | stage_deletes_supported_links | **clear** | 0.000 [0.000, 0.000], 5 units | exploratory | stage pc_only -> final |
| K11 | stage_follows_names | **not_checkable** | - | exploratory | needs stage traces and a T4 label reference for the swapped arm |
| K12 | stage_flips_data_direction | **inconclusive** | - | exploratory | no direction flips on true adjacencies |
| K13 | unsourced_claims | **clear** | unsourced 0, committed 200 | exploratory |  |
| K14 | overconfident | **not_checkable** | - | exploratory | the system states no confidence |
| K15 | never_abstains | **fires** | coverage 0.994, precision 0.720 (343 committed claims, real arm) | exploratory |  |

## L2: what each stage does (real names)

| Stage | Adjacency F1 change [95%] | Right->wrong | Wrong->right |
|---|---|---|---|
| pc_only -> final | 0.000 [0.000, 0.000], 5 units | 0 | 0 |

## Typed gaps (what this audit could not say, and why)

- K06 layout_reliance: not run, battery has no layout arms (columns were always shuffled)
- K08 robustness_drop: not run, robustness transforms are defined (controls/transforms.py); not run in v1
- K09 knowledge_ignored: not run, oracle and wrong suppliers are defined; not run in v1
- K11 stage_follows_names: not checkable, needs stage traces and a T4 label reference for the swapped arm
- K14 overconfident: not checkable, the system states no confidence

Exploratory labels: the kind's threshold was registered on 2026-10-30, after these runs; such a finding is confirmatory only for runs recorded after thresholds_v1.json was hashed.

Runs: 30 recorded runs (manifest sha256 691b6bcff186...). Recompute everything: `python -m audit verify <this folder>/certificate.json`.
