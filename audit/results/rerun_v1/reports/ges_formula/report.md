# Audit: ges@formula

Protocol v1.0 (thresholds 1.0, sha256 6fbded46952a...). Battery `ca-formula` v1 (development, 250 items, 50 scenario clusters; hash c4fede999ee0...).

System: `ges`; adapter ges v1; takes data; gives marks -- ->.

## L0: what it gets right (per arm; compare a row only with rows of the same regime)

| Arm | Regime | Runs | ok | Completion | Directed F1 (expectation rule, completed) | same, delivered | Adjacency F1 | DV-1 precision | DV-1 coverage | USD |
|---|---|---|---|---|---|---|---|---|---|---|
| released | D | 250 | 184 | 0.739 | 0.467 | 0.345 | 0.603 | 0.806 | 0.970 | 0.00 |
| shuffled | D | 250 | 182 | 0.731 | 0.468 | 0.342 | 0.602 | 0.803 | 0.969 | 0.00 |

References are simulated graphs (tier T1: exact (simulated)), so these numbers are accuracy.

## Findings (closed list, protocol v1)

| ID | Kind | Verdict | Effect [95% interval] | Label | Note |
|---|---|---|---|---|---|
| K01 | crash | **fires** | 132 of 498 runs: 0.265 [0.228, 0.306] | exploratory |  |
| K02 | no_better_than_null | **clear** | 0.093 [0.061, 0.126], 366 units | exploratory |  |
| K03 | cost_outlier | **not_run** | - | exploratory | needs a round of at least 3 LLM systems on the same battery |
| K04 | name_reliance | **not_run** | - | unknown | battery has no names arms |
| K05 | wrong_knowledge_harm | **not_run** | - | exploratory | battery has no names arms |
| K06 | layout_reliance | **clear** | -0.003 [-0.011, 0.004], 178 units | exploratory |  |
| K07 | knowledge_degrades_data | **not_checkable** | - | unknown | no data-only variant exposed, or not a hybrid of data and names |
| K08 | robustness_drop | **not_run** | - | exploratory | robustness transforms are defined (controls/transforms.py); not run in v1 |
| K09 | knowledge_ignored | **not_run** | - | exploratory | oracle and wrong suppliers are defined; not run in v1 |
| K10 | stage_deletes_supported_links | **not_checkable** | - | exploratory | no stage graphs (black box with no intermediate graph) |
| K11 | stage_follows_names | **not_checkable** | - | exploratory | needs stage traces and a T4 label reference for the swapped arm |
| K12 | stage_flips_data_direction | **not_checkable** | - | exploratory | no stage graphs |
| K13 | unsourced_claims | **not_checkable** | - | exploratory | the system exposes no per-edge source (L2 attribution is K10-K12) |
| K14 | overconfident | **not_checkable** | - | exploratory | the system states no confidence |
| K15 | never_abstains | **clear** | coverage 0.970, precision 0.806 (24608 committed claims, released arm) | exploratory |  |

## Typed gaps (what this audit could not say, and why)

- K03 cost_outlier: not run, needs a round of at least 3 LLM systems on the same battery
- K04 name_reliance: not run, battery has no names arms
- K05 wrong_knowledge_harm: not run, battery has no names arms
- K07 knowledge_degrades_data: not checkable, no data-only variant exposed, or not a hybrid of data and names
- K08 robustness_drop: not run, robustness transforms are defined (controls/transforms.py); not run in v1
- K09 knowledge_ignored: not run, oracle and wrong suppliers are defined; not run in v1
- K10 stage_deletes_supported_links: not checkable, no stage graphs (black box with no intermediate graph)
- K11 stage_follows_names: not checkable, needs stage traces and a T4 label reference for the swapped arm
- K12 stage_flips_data_direction: not checkable, no stage graphs
- K13 unsourced_claims: not checkable, the system exposes no per-edge source (L2 attribution is K10-K12)
- K14 overconfident: not checkable, the system states no confidence

Exploratory labels: the kind's threshold was registered on 2026-10-30, after these runs; such a finding is confirmatory only for runs recorded after thresholds_v1.json was hashed.

Runs: 500 recorded runs (manifest sha256 d9747b55b928...). Recompute everything: `python -m audit verify <this folder>/certificate.json`.
