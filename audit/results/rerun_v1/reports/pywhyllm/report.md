# Audit: pywhyllm

Protocol v1.0 (thresholds 1.0, sha256 6fbded46952a...). Battery `ca-ab06` v1 (development, 10 items, 10 scenario clusters; hash 561af73ae72f...).

System: `pywhyllm`; adapter pywhyllm v1; takes context, names; gives marks ->; per-edge source exposed.

## L0: what it gets right (per arm; compare a row only with rows of the same regime)

| Arm | Regime | Runs | ok | Completion | Directed F1 (expectation rule, completed) | same, delivered | Adjacency F1 | DV-1 precision | DV-1 coverage | USD |
|---|---|---|---|---|---|---|---|---|---|---|
| real | K | 10 | 5 | 1.000 | 0.314 | 0.314 | 0.369 | 0.545 | 1.000 | 5.00 |
| neutral | none | 10 | 0 | - | - | - | - | - | - | 0.00 |
| swapped | K | 10 | 4 | 0.800 | 0.114 | 0.091 | 0.244 | 0.435 | 1.000 | 4.95 |

References are simulated graphs (tier T1: exact (simulated)), so these numbers are accuracy.

## Findings (closed list, protocol v1)

| ID | Kind | Verdict | Effect [95% interval] | Label | Note |
|---|---|---|---|---|---|
| K01 | crash | **fires** | 1 of 10 runs: 0.100 [0.018, 0.404] | exploratory |  |
| K02 | no_better_than_null | **fires** | -0.122 [-0.261, 0.060], 5 units | exploratory |  |
| K03 | cost_outlier | **clear** | USD/run 0.995 vs round median 0.654: ratio 1.52 | exploratory |  |
| K04 | name_reliance | **inconclusive** | 0.202 [0.153, 0.249], 4 units | confirmatory |  |
| K05 | wrong_knowledge_harm | **not_checkable** | - | exploratory | names-only system: neutral names offer it nothing (regime none) |
| K06 | layout_reliance | **not_run** | - | exploratory | battery has no layout arms (columns were always shuffled) |
| K07 | knowledge_degrades_data | **not_checkable** | - | confirmatory | no data-only variant exposed, or not a hybrid of data and names |
| K08 | robustness_drop | **not_run** | - | exploratory | robustness transforms are defined (controls/transforms.py); not run in v1 |
| K09 | knowledge_ignored | **not_run** | - | exploratory | oracle and wrong suppliers are defined; not run in v1 |
| K10 | stage_deletes_supported_links | **not_checkable** | - | exploratory | no stage graphs (black box with no intermediate graph) |
| K11 | stage_follows_names | **not_checkable** | - | exploratory | needs stage traces and a T4 label reference for the swapped arm |
| K12 | stage_flips_data_direction | **not_checkable** | - | exploratory | no stage graphs |
| K13 | unsourced_claims | **clear** | unsourced 0, committed 1165 | exploratory |  |
| K14 | overconfident | **not_checkable** | - | exploratory | the system states no confidence |
| K15 | never_abstains | **fires** | coverage 1.000, precision 0.545 (345 committed claims, real arm) | exploratory |  |

## Typed gaps (what this audit could not say, and why)

- K05 wrong_knowledge_harm: not checkable, names-only system: neutral names offer it nothing (regime none)
- K06 layout_reliance: not run, battery has no layout arms (columns were always shuffled)
- K07 knowledge_degrades_data: not checkable, no data-only variant exposed, or not a hybrid of data and names
- K08 robustness_drop: not run, robustness transforms are defined (controls/transforms.py); not run in v1
- K09 knowledge_ignored: not run, oracle and wrong suppliers are defined; not run in v1
- K10 stage_deletes_supported_links: not checkable, no stage graphs (black box with no intermediate graph)
- K11 stage_follows_names: not checkable, needs stage traces and a T4 label reference for the swapped arm
- K12 stage_flips_data_direction: not checkable, no stage graphs
- K14 overconfident: not checkable, the system states no confidence

Exploratory labels: the kind's threshold was registered on 2026-10-30, after these runs; such a finding is confirmatory only for runs recorded after thresholds_v1.json was hashed.

Runs: 30 recorded runs (manifest sha256 828779ac615a...). Recompute everything: `python -m audit verify <this folder>/certificate.json`.
