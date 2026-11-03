# Audit: causal_copilot@ab06cc

Protocol v1.0 (thresholds 1.0, sha256 6fbded46952a...). Battery `q1s2` v1 (development, 10 items, 10 scenario clusters; hash 540a0d89b2a4...).

System: `causal_copilot@ab06cc`; adapter causal_copilot v1; takes context, data, names; gives marks -- -> <-> mixed o- o-> o-o ~.

## L0: what it gets right (per arm; compare a row only with rows of the same regime)

| Arm | Regime | Runs | ok | Completion | Directed F1 (expectation rule, completed) | same, delivered | Adjacency F1 | DV-1 precision | DV-1 coverage | USD |
|---|---|---|---|---|---|---|---|---|---|---|
| real | D+K | 10 | 8 | 0.800 | 0.197 | 0.157 | 0.382 | - | - | 0.00 |
| neutral | D | 10 | 10 | 1.000 | 0.192 | 0.192 | 0.296 | - | - | 0.00 |
| swapped | D+K | 10 | 10 | 1.000 | 0.116 | 0.116 | 0.184 | - | - | 0.00 |

References are simulated graphs (tier T1: exact (simulated)), so these numbers are accuracy.

## Findings (closed list, protocol v1)

| ID | Kind | Verdict | Effect [95% interval] | Label | Note |
|---|---|---|---|---|---|
| K01 | crash | **fires** | 2 of 30 runs: 0.067 [0.018, 0.213] | exploratory |  |
| K02 | no_better_than_null | **not_checkable** | - | exploratory | no released intervention targets in this battery |
| K03 | cost_outlier | **not_run** | - | exploratory | needs a round of at least 3 LLM systems on the same battery |
| K04 | name_reliance | **clear** | 0.094 [0.042, 0.145], 10 units | exploratory | measured on S3 |
| K05 | wrong_knowledge_harm | **clear** | 0.030 [-0.019, 0.084], 10 units | exploratory | measured on S3 |
| K06 | layout_reliance | **not_run** | - | exploratory | battery has no layout arms (columns were always shuffled) |
| K07 | knowledge_degrades_data | **not_checkable** | - | exploratory | no ok run exposes the data-only variant with DV-1 targets |
| K08 | robustness_drop | **not_run** | - | exploratory | robustness transforms are defined (controls/transforms.py); not run in v1 |
| K09 | knowledge_ignored | **not_run** | - | exploratory | oracle and wrong suppliers are defined; not run in v1 |
| K10 | stage_deletes_supported_links | **fires** | -0.282 [-0.341, -0.219], 10 units | exploratory | stage S0 -> S1 |
| K11 | stage_follows_names | **fires** | n 198, labels only 141, data only 57 | exploratory |  |
| K12 | stage_flips_data_direction | **fires** | right to wrong 14, wrong to right 1 | exploratory | stage S1 -> S2 |
| K13 | unsourced_claims | **not_checkable** | - | exploratory | the system exposes no per-edge source (L2 attribution is K10-K12) |
| K14 | overconfident | **not_checkable** | - | exploratory | the system states no confidence |
| K15 | never_abstains | **not_checkable** | - | exploratory | no DV-1 targets in this battery |

## L2: what each stage does (real names)

| Stage | Adjacency F1 change [95%] | Right->wrong | Wrong->right |
|---|---|---|---|
| S0 -> S1 | -0.282 [-0.341, -0.219], 10 units | 0 | 0 |
| S1 -> S2 | 0.077 [-0.002, 0.157], 10 units | 14 | 1 |
| S2 -> S3 | 0.002 [0.000, 0.003], 10 units | 0 | 0 |
| S3 -> S4 | 0.000 [0.000, 0.001], 8 units | 0 | 0 |

## Typed gaps (what this audit could not say, and why)

- K02 no_better_than_null: not checkable, no released intervention targets in this battery
- K03 cost_outlier: not run, needs a round of at least 3 LLM systems on the same battery
- K06 layout_reliance: not run, battery has no layout arms (columns were always shuffled)
- K07 knowledge_degrades_data: not checkable, no ok run exposes the data-only variant with DV-1 targets
- K08 robustness_drop: not run, robustness transforms are defined (controls/transforms.py); not run in v1
- K09 knowledge_ignored: not run, oracle and wrong suppliers are defined; not run in v1
- K13 unsourced_claims: not checkable, the system exposes no per-edge source (L2 attribution is K10-K12)
- K14 overconfident: not checkable, the system states no confidence
- K15 never_abstains: not checkable, no DV-1 targets in this battery

Exploratory labels: the kind's threshold was registered on 2026-10-30, after these runs; such a finding is confirmatory only for runs recorded after thresholds_v1.json was hashed.

Runs: 31 recorded runs (manifest sha256 647f83030c72...). Recompute everything: `python -m audit verify <this folder>/certificate.json`.
