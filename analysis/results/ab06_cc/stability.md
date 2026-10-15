# Stability and name-versus-data report

Label `ab06cc`. Runs directory `runs`. 27 runs included in 27 arms; 4 excluded.

## Excluded runs

| Run | Arm | Reason |
|---|---|---|
| 20261014T000740Z_ab06cc_q041_r01_dd05cd | q041 | status NO SUMMARY; code identity None |
| 20261014T002211Z_ab06cc_q042_r01_4ad45c | q042 | status NO SUMMARY; code identity None |
| 20261014T021653Z_ab06cc_q071_r01_65042f | q071 | status FAILED |
| 20261014T035624Z_ab06cc_q101_r01_fdd5d4 | q101 | status FAILED |

## Arm `q011` (1 runs)

Family `s2_01`, role `real`. Column labels: component_thermal_mass_index, oven_leak_index, measured_void_fraction, realized_ramp_rate_C_per_s, TAL_s, oxygen_ppm, flux_lot_activity_index, microstructure_index, nitrogen_flow_setpoint_slpm, wetting_index, cooling_rate_C_per_s, volatile_generation_cumulative_mg, paste_solvent_mass_fraction, pad_finish, residual_entrained_gas_mg, true_void_fraction, conv_speed_cm_min, package_family_code, realized_peak_temp_C, electrical_resistance_mOhm, peak_zone_setpoint_C, paste_batch_context, preheat_soak_setpoint_C. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 23 | 0 | 0 | 23 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 26.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 13.0 (1 run) | n/a | n/a |
| S2 after LLM review | 41.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 41.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 41.0 (1 run) | n/a | n/a |

**LLM review decisions.** 253 pairs. Same decision in every run: 253. Same edge/no-edge call in every run: 253. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 40, C 205, D 8.

**Final edges.** 41 distinct edges appear in at least one run; 41 appear in every run. Set by: llm 37, algorithm (unchanged) 4. Per run: LLM-set edges 37.0 (1 run); final edges between pairs the algorithm did not connect 32.0 (1 run); LLM additions where at least 90% of resamples had no edge 30.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| component_thermal_mass_index->realized_ramp_rate_C_per_s | 1 |
| component_thermal_mass_index->microstructure_index | 1 |
| component_thermal_mass_index->wetting_index | 1 |
| component_thermal_mass_index->cooling_rate_C_per_s | 1 |
| component_thermal_mass_index->realized_peak_temp_C | 1 |
| component_thermal_mass_index->peak_zone_setpoint_C | 1 |
| component_thermal_mass_index->preheat_soak_setpoint_C | 1 |
| oven_leak_index->realized_ramp_rate_C_per_s | 1 |
| oven_leak_index->oxygen_ppm | 1 |
| oven_leak_index->cooling_rate_C_per_s | 1 |
| oven_leak_index->volatile_generation_cumulative_mg | 1 |
| oven_leak_index->realized_peak_temp_C | 1 |
| oven_leak_index->peak_zone_setpoint_C | 1 |
| oven_leak_index->preheat_soak_setpoint_C | 1 |
| measured_void_fraction->true_void_fraction | 1 |
| realized_ramp_rate_C_per_s->cooling_rate_C_per_s | 1 |
| realized_ramp_rate_C_per_s->realized_peak_temp_C | 1 |
| realized_ramp_rate_C_per_s->peak_zone_setpoint_C | 1 |
| realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | 1 |
| TAL_s->realized_peak_temp_C | 1 |
| oxygen_ppm->volatile_generation_cumulative_mg | 1 |
| flux_lot_activity_index->wetting_index | 1 |
| flux_lot_activity_index->volatile_generation_cumulative_mg | 1 |
| microstructure_index->wetting_index | 1 |
| microstructure_index->true_void_fraction | 1 |
| microstructure_index o-o realized_peak_temp_C | 1 |
| microstructure_index->electrical_resistance_mOhm | 1 |
| nitrogen_flow_setpoint_slpm->volatile_generation_cumulative_mg | 1 |
| nitrogen_flow_setpoint_slpm->residual_entrained_gas_mg | 1 |
| nitrogen_flow_setpoint_slpm->realized_peak_temp_C | 1 |
| wetting_index->paste_solvent_mass_fraction | 1 |
| cooling_rate_C_per_s->realized_peak_temp_C | 1 |
| volatile_generation_cumulative_mg->paste_solvent_mass_fraction | 1 |
| volatile_generation_cumulative_mg->residual_entrained_gas_mg | 1 |
| volatile_generation_cumulative_mg->realized_peak_temp_C | 1 |
| volatile_generation_cumulative_mg->peak_zone_setpoint_C | 1 |
| volatile_generation_cumulative_mg->preheat_soak_setpoint_C | 1 |
| paste_solvent_mass_fraction->true_void_fraction | 1 |
| realized_peak_temp_C->peak_zone_setpoint_C | 1 |
| realized_peak_temp_C->preheat_soak_setpoint_C | 1 |
| peak_zone_setpoint_C->preheat_soak_setpoint_C | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.85 (1 run) | 0.56 (1 run) | 0.68 (1 run) | 5.0 (1 run) | 2.0 (1 run) | 38.0 (1 run) | 0.71 (1 run) | 0.13 (1 run) | 0.22 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.33 (1 run) | 0.50 (1 run) | 5.0 (1 run) | 2.0 (1 run) | 34.0 (1 run) | 0.71 (1 run) | 0.13 (1 run) | 0.22 (1 run) |
| S2 after LLM review | 0.37 (1 run) | 0.38 (1 run) | 0.37 (1 run) | 7.0 (1 run) | 7.0 (1 run) | 58.0 (1 run) | 0.17 (1 run) | 0.18 (1 run) | 0.18 (1 run) |
| S3 after KCI pruning | 0.37 (1 run) | 0.38 (1 run) | 0.37 (1 run) | 7.0 (1 run) | 7.0 (1 run) | 58.0 (1 run) | 0.17 (1 run) | 0.18 (1 run) | 0.18 (1 run) |
| S4 final (after cycle step) | 0.37 (1 run) | 0.38 (1 run) | 0.37 (1 run) | 7.0 (1 run) | 7.0 (1 run) | 58.0 (1 run) | 0.17 (1 run) | 0.18 (1 run) | 0.18 (1 run) |

## Arm `q012` (1 runs)

Family `s2_01`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 23 | 0 | 0 | 23 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 27.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 10.0 (1 run) | n/a | n/a |
| S2 after LLM review | 9.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 9.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 9.0 (1 run) | n/a | n/a |

**LLM review decisions.** 253 pairs. Same decision in every run: 253. Same edge/no-edge call in every run: 253. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 3, C 30, D 220.

**Final edges.** 9 distinct edges appear in at least one run; 9 appear in every run. Set by: algorithm (unchanged) 6, llm 3. Per run: LLM-set edges 3.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V01 o-> V04 | 1 |
| V01 o-> V18 | 1 |
| V03 ~~~ V16 | 1 |
| V05->V08 | 1 |
| V10->V15 | 1 |
| V10->V19 | 1 |
| V12 <-> V13 | 1 |
| V22->V13 | 1 |
| V16 o-> V20 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.78 (1 run) | 0.54 (1 run) | 0.64 (1 run) | 3.0 (1 run) | 2.0 (1 run) | 43.0 (1 run) | 0.60 (1 run) | 0.08 (1 run) | 0.14 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.26 (1 run) | 0.41 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 38.0 (1 run) | 0.50 (1 run) | 0.05 (1 run) | 0.09 (1 run) |
| S2 after LLM review | 1.00 (1 run) | 0.23 (1 run) | 0.38 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 37.0 (1 run) | 0.75 (1 run) | 0.08 (1 run) | 0.14 (1 run) |
| S3 after KCI pruning | 1.00 (1 run) | 0.23 (1 run) | 0.38 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 37.0 (1 run) | 0.75 (1 run) | 0.08 (1 run) | 0.14 (1 run) |
| S4 final (after cycle step) | 1.00 (1 run) | 0.23 (1 run) | 0.38 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 37.0 (1 run) | 0.75 (1 run) | 0.08 (1 run) | 0.14 (1 run) |

## Arm `q013` (1 runs)

Family `s2_01`, role `swapped`. Column labels: oven_leak_index, component_thermal_mass_index, realized_ramp_rate_C_per_s, measured_void_fraction, oxygen_ppm, TAL_s, microstructure_index, flux_lot_activity_index, cooling_rate_C_per_s, paste_solvent_mass_fraction, nitrogen_flow_setpoint_slpm, pad_finish, volatile_generation_cumulative_mg, wetting_index, true_void_fraction, package_family_code, realized_peak_temp_C, conv_speed_cm_min, peak_zone_setpoint_C, residual_entrained_gas_mg, electrical_resistance_mOhm, preheat_soak_setpoint_C, paste_batch_context. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 2, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 23 | 0 | 0 | 23 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 2, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 25.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 11.0 (1 run) | n/a | n/a |
| S2 after LLM review | 49.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 49.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 49.0 (1 run) | n/a | n/a |

**LLM review decisions.** 253 pairs. Same decision in every run: 253. Same edge/no-edge call in every run: 253. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 49, C 194, D 10.

**Final edges.** 49 distinct edges appear in at least one run; 49 appear in every run. Set by: llm 47, algorithm (unchanged) 2. Per run: LLM-set edges 47.0 (1 run); final edges between pairs the algorithm did not connect 45.0 (1 run); LLM additions where at least 90% of resamples had no edge 44.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| oven_leak_index->component_thermal_mass_index | 1 |
| oven_leak_index->realized_ramp_rate_C_per_s | 1 |
| oven_leak_index->measured_void_fraction | 1 |
| oven_leak_index->microstructure_index | 1 |
| oven_leak_index->cooling_rate_C_per_s | 1 |
| oven_leak_index->volatile_generation_cumulative_mg | 1 |
| oven_leak_index->wetting_index | 1 |
| oven_leak_index->true_void_fraction | 1 |
| oven_leak_index->realized_peak_temp_C | 1 |
| oven_leak_index->peak_zone_setpoint_C | 1 |
| oven_leak_index->preheat_soak_setpoint_C | 1 |
| component_thermal_mass_index->realized_ramp_rate_C_per_s | 1 |
| component_thermal_mass_index->microstructure_index | 1 |
| component_thermal_mass_index->cooling_rate_C_per_s | 1 |
| component_thermal_mass_index->realized_peak_temp_C | 1 |
| component_thermal_mass_index->electrical_resistance_mOhm | 1 |
| realized_ramp_rate_C_per_s->cooling_rate_C_per_s | 1 |
| realized_ramp_rate_C_per_s->volatile_generation_cumulative_mg | 1 |
| realized_ramp_rate_C_per_s->realized_peak_temp_C | 1 |
| realized_ramp_rate_C_per_s->peak_zone_setpoint_C | 1 |
| realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | 1 |
| measured_void_fraction->microstructure_index | 1 |
| measured_void_fraction->wetting_index | 1 |
| measured_void_fraction->true_void_fraction | 1 |
| oxygen_ppm->volatile_generation_cumulative_mg | 1 |
| oxygen_ppm->realized_peak_temp_C | 1 |
| microstructure_index->pad_finish | 1 |
| microstructure_index->wetting_index | 1 |
| microstructure_index->true_void_fraction | 1 |
| microstructure_index->electrical_resistance_mOhm | 1 |
| cooling_rate_C_per_s->realized_peak_temp_C | 1 |
| cooling_rate_C_per_s->peak_zone_setpoint_C | 1 |
| cooling_rate_C_per_s->electrical_resistance_mOhm | 1 |
| cooling_rate_C_per_s->preheat_soak_setpoint_C | 1 |
| paste_solvent_mass_fraction->volatile_generation_cumulative_mg | 1 |
| paste_solvent_mass_fraction->wetting_index | 1 |
| paste_solvent_mass_fraction->true_void_fraction | 1 |
| pad_finish->wetting_index | 1 |
| pad_finish->true_void_fraction | 1 |
| volatile_generation_cumulative_mg->realized_peak_temp_C | 1 |
| wetting_index->true_void_fraction | 1 |
| package_family_code->paste_batch_context | 1 |
| realized_peak_temp_C->peak_zone_setpoint_C | 1 |
| realized_peak_temp_C->residual_entrained_gas_mg | 1 |
| realized_peak_temp_C->electrical_resistance_mOhm | 1 |
| realized_peak_temp_C->preheat_soak_setpoint_C | 1 |
| peak_zone_setpoint_C->electrical_resistance_mOhm | 1 |
| peak_zone_setpoint_C->preheat_soak_setpoint_C | 1 |
| electrical_resistance_mOhm->preheat_soak_setpoint_C | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.80 (1 run) | 0.51 (1 run) | 0.62 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 39.0 (1 run) | 0.60 (1 run) | 0.15 (1 run) | 0.24 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.28 (1 run) | 0.44 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 34.0 (1 run) | 1.00 (1 run) | 0.15 (1 run) | 0.27 (1 run) |
| S2 after LLM review | 0.18 (1 run) | 0.23 (1 run) | 0.20 (1 run) | 6.0 (1 run) | 3.0 (1 run) | 73.0 (1 run) | 0.12 (1 run) | 0.15 (1 run) | 0.14 (1 run) |
| S3 after KCI pruning | 0.18 (1 run) | 0.23 (1 run) | 0.20 (1 run) | 6.0 (1 run) | 3.0 (1 run) | 73.0 (1 run) | 0.12 (1 run) | 0.15 (1 run) | 0.14 (1 run) |
| S4 final (after cycle step) | 0.18 (1 run) | 0.23 (1 run) | 0.20 (1 run) | 6.0 (1 run) | 3.0 (1 run) | 73.0 (1 run) | 0.12 (1 run) | 0.15 (1 run) | 0.14 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.12 (1 run) | 0.08 (1 run) | 0.09 (1 run) | 0.0 (1 run) | 2.0 (1 run) | 61.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 50.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.24 (1 run) | 0.31 (1 run) | 0.27 (1 run) | 7.0 (1 run) | 5.0 (1 run) | 69.0 (1 run) | 0.14 (1 run) | 0.18 (1 run) | 0.16 (1 run) |
| S3 after KCI pruning | 0.24 (1 run) | 0.31 (1 run) | 0.27 (1 run) | 7.0 (1 run) | 5.0 (1 run) | 69.0 (1 run) | 0.14 (1 run) | 0.18 (1 run) | 0.16 (1 run) |
| S4 final (after cycle step) | 0.24 (1 run) | 0.31 (1 run) | 0.27 (1 run) | 7.0 (1 run) | 5.0 (1 run) | 69.0 (1 run) | 0.14 (1 run) | 0.18 (1 run) | 0.16 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 12 |
| data only | 7 |
| both | 0 |
| neither | 28 |

Direction among those: data: direction as in reference 4, data: reversed 3, labels: direction as in reference 7, labels: reversed 5.
Distinct edges: data only: microstructure_index->pad_finish, oven_leak_index->peak_zone_setpoint_C, oxygen_ppm->realized_peak_temp_C, pad_finish->true_void_fraction, paste_solvent_mass_fraction->wetting_index, peak_zone_setpoint_C->electrical_resistance_mOhm, wetting_index->true_void_fraction; labels only: component_thermal_mass_index->realized_peak_temp_C, component_thermal_mass_index->realized_ramp_rate_C_per_s, cooling_rate_C_per_s->realized_peak_temp_C, measured_void_fraction->true_void_fraction, microstructure_index->electrical_resistance_mOhm, pad_finish->wetting_index, paste_solvent_mass_fraction->volatile_generation_cumulative_mg, realized_peak_temp_C->peak_zone_setpoint_C, realized_peak_temp_C->residual_entrained_gas_mg, realized_ramp_rate_C_per_s->preheat_soak_setpoint_C, realized_ramp_rate_C_per_s->volatile_generation_cumulative_mg, volatile_generation_cumulative_mg->realized_peak_temp_C; neither: component_thermal_mass_index->cooling_rate_C_per_s, component_thermal_mass_index->electrical_resistance_mOhm, component_thermal_mass_index->microstructure_index, cooling_rate_C_per_s->electrical_resistance_mOhm, cooling_rate_C_per_s->peak_zone_setpoint_C, cooling_rate_C_per_s->preheat_soak_setpoint_C, electrical_resistance_mOhm->preheat_soak_setpoint_C, measured_void_fraction->microstructure_index, measured_void_fraction->wetting_index, microstructure_index->true_void_fraction, microstructure_index->wetting_index, oven_leak_index->component_thermal_mass_index, oven_leak_index->cooling_rate_C_per_s, oven_leak_index->microstructure_index, oven_leak_index->preheat_soak_setpoint_C, oven_leak_index->realized_peak_temp_C, oven_leak_index->realized_ramp_rate_C_per_s, oven_leak_index->true_void_fraction, oven_leak_index->volatile_generation_cumulative_mg, oven_leak_index->wetting_index, oxygen_ppm->volatile_generation_cumulative_mg, package_family_code->paste_batch_context, peak_zone_setpoint_C->preheat_soak_setpoint_C, realized_peak_temp_C->electrical_resistance_mOhm, realized_peak_temp_C->preheat_soak_setpoint_C, realized_ramp_rate_C_per_s->cooling_rate_C_per_s, realized_ramp_rate_C_per_s->peak_zone_setpoint_C, realized_ramp_rate_C_per_s->realized_peak_temp_C.

## Arm `q021` (1 runs)

Family `s2_02`, role `real`. Column labels: V16_unsafe_crossing_true, V17_observed_unsafe_label, V14_focal_walking_speed_mps, V23_abandonment_indicator, V9_group_size_at_decision, V8_visible_remaining_seconds, V24_start_decision_now, V1_countdown_policy_enabled, V11_time_pressure_index, V5_traffic_flow_rate_vpm, V18_vehicle_approach_speed_mps, V10_older_adult_share, V22_wait_time_until_walk_s, V19_ped_traverse_time_s, V6_arrival_time_within_cycle_s, V2_curb_extension_present, V21_near_conflict_flag, V4_illumination_weather_state, V7_timer_visibility_quality, V3_signal_cycle_length_s, V15_start_time_rel_phase_end_s. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 21 | 0 | 0 | 21 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 20.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 5.0 (1 run) | n/a | n/a |
| S2 after LLM review | 39.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 38.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 38.0 (1 run) | n/a | n/a |

**LLM review decisions.** 210 pairs. Same decision in every run: 210. Same edge/no-edge call in every run: 210. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 37, B 1, C 146, D 26.

**Final edges.** 38 distinct edges appear in at least one run; 38 appear in every run. Set by: llm 36, algorithm (unchanged) 2. Per run: LLM-set edges 36.0 (1 run); final edges between pairs the algorithm did not connect 28.0 (1 run); LLM additions where at least 90% of resamples had no edge 27.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V16_unsafe_crossing_true->V17_observed_unsafe_label | 1 |
| V16_unsafe_crossing_true->V21_near_conflict_flag | 1 |
| V17_observed_unsafe_label->V21_near_conflict_flag | 1 |
| V14_focal_walking_speed_mps->V11_time_pressure_index | 1 |
| V14_focal_walking_speed_mps->V19_ped_traverse_time_s | 1 |
| V23_abandonment_indicator->V11_time_pressure_index | 1 |
| V8_visible_remaining_seconds->V1_countdown_policy_enabled | 1 |
| V8_visible_remaining_seconds->V11_time_pressure_index | 1 |
| V8_visible_remaining_seconds->V22_wait_time_until_walk_s | 1 |
| V8_visible_remaining_seconds->V7_timer_visibility_quality | 1 |
| V24_start_decision_now->V1_countdown_policy_enabled | 1 |
| V24_start_decision_now->V11_time_pressure_index | 1 |
| V24_start_decision_now->V22_wait_time_until_walk_s | 1 |
| V24_start_decision_now->V7_timer_visibility_quality | 1 |
| V24_start_decision_now->V15_start_time_rel_phase_end_s | 1 |
| V1_countdown_policy_enabled->V11_time_pressure_index | 1 |
| V1_countdown_policy_enabled->V22_wait_time_until_walk_s | 1 |
| V1_countdown_policy_enabled->V7_timer_visibility_quality | 1 |
| V11_time_pressure_index->V22_wait_time_until_walk_s | 1 |
| V11_time_pressure_index->V19_ped_traverse_time_s | 1 |
| V11_time_pressure_index->V7_timer_visibility_quality | 1 |
| V5_traffic_flow_rate_vpm->V18_vehicle_approach_speed_mps | 1 |
| V5_traffic_flow_rate_vpm->V22_wait_time_until_walk_s | 1 |
| V5_traffic_flow_rate_vpm->V19_ped_traverse_time_s | 1 |
| V5_traffic_flow_rate_vpm->V21_near_conflict_flag | 1 |
| V18_vehicle_approach_speed_mps->V21_near_conflict_flag | 1 |
| V22_wait_time_until_walk_s->V7_timer_visibility_quality | 1 |
| V22_wait_time_until_walk_s->V3_signal_cycle_length_s | 1 |
| V19_ped_traverse_time_s->V2_curb_extension_present | 1 |
| V19_ped_traverse_time_s->V21_near_conflict_flag | 1 |
| V19_ped_traverse_time_s->V4_illumination_weather_state | 1 |
| V19_ped_traverse_time_s->V7_timer_visibility_quality | 1 |
| V6_arrival_time_within_cycle_s->V3_signal_cycle_length_s | 1 |
| V6_arrival_time_within_cycle_s->V15_start_time_rel_phase_end_s | 1 |
| V2_curb_extension_present->V21_near_conflict_flag | 1 |
| V21_near_conflict_flag->V4_illumination_weather_state | 1 |
| V21_near_conflict_flag->V7_timer_visibility_quality | 1 |
| V3_signal_cycle_length_s->V15_start_time_rel_phase_end_s | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.90 (1 run) | 0.47 (1 run) | 0.62 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 37.0 (1 run) | 0.86 (1 run) | 0.16 (1 run) | 0.27 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.13 (1 run) | 0.23 (1 run) | 4.0 (1 run) | 1.0 (1 run) | 35.0 (1 run) | 0.80 (1 run) | 0.11 (1 run) | 0.19 (1 run) |
| S2 after LLM review | 0.41 (1 run) | 0.42 (1 run) | 0.42 (1 run) | 9.0 (1 run) | 7.0 (1 run) | 52.0 (1 run) | 0.23 (1 run) | 0.24 (1 run) | 0.23 (1 run) |
| S3 after KCI pruning | 0.42 (1 run) | 0.42 (1 run) | 0.42 (1 run) | 9.0 (1 run) | 7.0 (1 run) | 51.0 (1 run) | 0.24 (1 run) | 0.24 (1 run) | 0.24 (1 run) |
| S4 final (after cycle step) | 0.42 (1 run) | 0.42 (1 run) | 0.42 (1 run) | 9.0 (1 run) | 7.0 (1 run) | 51.0 (1 run) | 0.24 (1 run) | 0.24 (1 run) | 0.24 (1 run) |

## Arm `q022` (1 runs)

Family `s2_02`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 21 | 0 | 0 | 21 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 22.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 6.0 (1 run) | n/a | n/a |
| S2 after LLM review | 7.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 7.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 7.0 (1 run) | n/a | n/a |

**LLM review decisions.** 210 pairs. Same decision in every run: 210. Same edge/no-edge call in every run: 210. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 3, B 1, D 206.

**Final edges.** 7 distinct edges appear in at least one run; 7 appear in every run. Set by: algorithm (unchanged) 5, llm 2. Per run: LLM-set edges 2.0 (1 run); final edges between pairs the algorithm did not connect 1.0 (1 run); LLM additions where at least 90% of resamples had no edge 1.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V01 o-> V06 | 1 |
| V03 o-> V12 | 1 |
| V03 o-> V14 | 1 |
| V05->V06 | 1 |
| V15->V05 | 1 |
| V06->V09 | 1 |
| V14->V16 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.82 (1 run) | 0.47 (1 run) | 0.60 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 40.0 (1 run) | 1.00 (1 run) | 0.08 (1 run) | 0.15 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.16 (1 run) | 0.27 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 36.0 (1 run) | 1.00 (1 run) | 0.08 (1 run) | 0.15 (1 run) |
| S2 after LLM review | 0.86 (1 run) | 0.16 (1 run) | 0.27 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 38.0 (1 run) | 0.50 (1 run) | 0.05 (1 run) | 0.10 (1 run) |
| S3 after KCI pruning | 0.86 (1 run) | 0.16 (1 run) | 0.27 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 38.0 (1 run) | 0.50 (1 run) | 0.05 (1 run) | 0.10 (1 run) |
| S4 final (after cycle step) | 0.86 (1 run) | 0.16 (1 run) | 0.27 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 38.0 (1 run) | 0.50 (1 run) | 0.05 (1 run) | 0.10 (1 run) |

## Arm `q023` (1 runs)

Family `s2_02`, role `swapped`. Column labels: V17_observed_unsafe_label, V14_focal_walking_speed_mps, V16_unsafe_crossing_true, V9_group_size_at_decision, V8_visible_remaining_seconds, V23_abandonment_indicator, V1_countdown_policy_enabled, V24_start_decision_now, V5_traffic_flow_rate_vpm, V11_time_pressure_index, V10_older_adult_share, V18_vehicle_approach_speed_mps, V19_ped_traverse_time_s, V22_wait_time_until_walk_s, V4_illumination_weather_state, V21_near_conflict_flag, V15_start_time_rel_phase_end_s, V7_timer_visibility_quality, V3_signal_cycle_length_s, V6_arrival_time_within_cycle_s, V2_curb_extension_present. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 21 | 0 | 0 | 21 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 22.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 10.0 (1 run) | n/a | n/a |
| S2 after LLM review | 40.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 40.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 40.0 (1 run) | n/a | n/a |

**LLM review decisions.** 210 pairs. Same decision in every run: 210. Same edge/no-edge call in every run: 210. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 38, C 138, D 34.

**Final edges.** 40 distinct edges appear in at least one run; 40 appear in every run. Set by: llm 36, algorithm (unchanged) 4. Per run: LLM-set edges 36.0 (1 run); final edges between pairs the algorithm did not connect 34.0 (1 run); LLM additions where at least 90% of resamples had no edge 33.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V17_observed_unsafe_label->V14_focal_walking_speed_mps | 1 |
| V17_observed_unsafe_label->V16_unsafe_crossing_true | 1 |
| V17_observed_unsafe_label->V23_abandonment_indicator | 1 |
| V17_observed_unsafe_label->V21_near_conflict_flag | 1 |
| V14_focal_walking_speed_mps->V19_ped_traverse_time_s | 1 |
| V14_focal_walking_speed_mps->V22_wait_time_until_walk_s | 1 |
| V16_unsafe_crossing_true->V23_abandonment_indicator | 1 |
| V16_unsafe_crossing_true->V5_traffic_flow_rate_vpm | 1 |
| V16_unsafe_crossing_true->V22_wait_time_until_walk_s | 1 |
| V16_unsafe_crossing_true->V21_near_conflict_flag | 1 |
| V8_visible_remaining_seconds->V1_countdown_policy_enabled | 1 |
| V8_visible_remaining_seconds->V22_wait_time_until_walk_s | 1 |
| V8_visible_remaining_seconds->V7_timer_visibility_quality | 1 |
| V23_abandonment_indicator->V1_countdown_policy_enabled | 1 |
| V23_abandonment_indicator->V5_traffic_flow_rate_vpm | 1 |
| V23_abandonment_indicator->V11_time_pressure_index | 1 |
| V23_abandonment_indicator->V22_wait_time_until_walk_s | 1 |
| V23_abandonment_indicator->V21_near_conflict_flag | 1 |
| V23_abandonment_indicator->V7_timer_visibility_quality | 1 |
| V1_countdown_policy_enabled->V24_start_decision_now | 1 |
| V1_countdown_policy_enabled->V19_ped_traverse_time_s | 1 |
| V1_countdown_policy_enabled->V22_wait_time_until_walk_s | 1 |
| V1_countdown_policy_enabled->V7_timer_visibility_quality | 1 |
| V24_start_decision_now->V11_time_pressure_index | 1 |
| V24_start_decision_now->V22_wait_time_until_walk_s | 1 |
| V24_start_decision_now->V7_timer_visibility_quality | 1 |
| V5_traffic_flow_rate_vpm->V22_wait_time_until_walk_s | 1 |
| V5_traffic_flow_rate_vpm->V21_near_conflict_flag | 1 |
| V11_time_pressure_index->V19_ped_traverse_time_s | 1 |
| V11_time_pressure_index->V22_wait_time_until_walk_s | 1 |
| V18_vehicle_approach_speed_mps->V19_ped_traverse_time_s | 1 |
| V18_vehicle_approach_speed_mps->V21_near_conflict_flag | 1 |
| V19_ped_traverse_time_s->V22_wait_time_until_walk_s | 1 |
| V22_wait_time_until_walk_s->V21_near_conflict_flag | 1 |
| V22_wait_time_until_walk_s->V15_start_time_rel_phase_end_s | 1 |
| V22_wait_time_until_walk_s->V7_timer_visibility_quality | 1 |
| V22_wait_time_until_walk_s->V3_signal_cycle_length_s | 1 |
| V4_illumination_weather_state->V7_timer_visibility_quality | 1 |
| V15_start_time_rel_phase_end_s->V6_arrival_time_within_cycle_s | 1 |
| V3_signal_cycle_length_s->V6_arrival_time_within_cycle_s | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.82 (1 run) | 0.47 (1 run) | 0.60 (1 run) | 8.0 (1 run) | 0.0 (1 run) | 35.0 (1 run) | 0.80 (1 run) | 0.21 (1 run) | 0.33 (1 run) |
| S1 after bootstrap edits | 0.90 (1 run) | 0.24 (1 run) | 0.38 (1 run) | 8.0 (1 run) | 0.0 (1 run) | 32.0 (1 run) | 0.89 (1 run) | 0.21 (1 run) | 0.34 (1 run) |
| S2 after LLM review | 0.23 (1 run) | 0.24 (1 run) | 0.23 (1 run) | 7.0 (1 run) | 2.0 (1 run) | 62.0 (1 run) | 0.17 (1 run) | 0.18 (1 run) | 0.18 (1 run) |
| S3 after KCI pruning | 0.23 (1 run) | 0.24 (1 run) | 0.23 (1 run) | 7.0 (1 run) | 2.0 (1 run) | 62.0 (1 run) | 0.17 (1 run) | 0.18 (1 run) | 0.18 (1 run) |
| S4 final (after cycle step) | 0.23 (1 run) | 0.24 (1 run) | 0.23 (1 run) | 7.0 (1 run) | 2.0 (1 run) | 62.0 (1 run) | 0.17 (1 run) | 0.18 (1 run) | 0.18 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 60.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 48.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.30 (1 run) | 0.32 (1 run) | 0.31 (1 run) | 6.0 (1 run) | 6.0 (1 run) | 61.0 (1 run) | 0.15 (1 run) | 0.16 (1 run) | 0.15 (1 run) |
| S3 after KCI pruning | 0.30 (1 run) | 0.32 (1 run) | 0.31 (1 run) | 6.0 (1 run) | 6.0 (1 run) | 61.0 (1 run) | 0.15 (1 run) | 0.16 (1 run) | 0.15 (1 run) |
| S4 final (after cycle step) | 0.30 (1 run) | 0.32 (1 run) | 0.31 (1 run) | 6.0 (1 run) | 6.0 (1 run) | 61.0 (1 run) | 0.15 (1 run) | 0.16 (1 run) | 0.15 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 12 |
| data only | 5 |
| both | 0 |
| neither | 19 |

Direction among those: data: direction as in reference 3, data: reversed 2, labels: direction as in reference 6, labels: reversed 6.
Distinct edges: data only: V17_observed_unsafe_label->V23_abandonment_indicator, V1_countdown_policy_enabled->V19_ped_traverse_time_s, V22_wait_time_until_walk_s->V15_start_time_rel_phase_end_s, V22_wait_time_until_walk_s->V21_near_conflict_flag, V8_visible_remaining_seconds->V1_countdown_policy_enabled; labels only: V14_focal_walking_speed_mps->V19_ped_traverse_time_s, V17_observed_unsafe_label->V16_unsafe_crossing_true, V18_vehicle_approach_speed_mps->V21_near_conflict_flag, V1_countdown_policy_enabled->V7_timer_visibility_quality, V22_wait_time_until_walk_s->V3_signal_cycle_length_s, V23_abandonment_indicator->V11_time_pressure_index, V23_abandonment_indicator->V22_wait_time_until_walk_s, V24_start_decision_now->V11_time_pressure_index, V24_start_decision_now->V22_wait_time_until_walk_s, V3_signal_cycle_length_s->V6_arrival_time_within_cycle_s, V4_illumination_weather_state->V7_timer_visibility_quality, V8_visible_remaining_seconds->V7_timer_visibility_quality; neither: V11_time_pressure_index->V19_ped_traverse_time_s, V11_time_pressure_index->V22_wait_time_until_walk_s, V14_focal_walking_speed_mps->V22_wait_time_until_walk_s, V15_start_time_rel_phase_end_s->V6_arrival_time_within_cycle_s, V16_unsafe_crossing_true->V21_near_conflict_flag, V16_unsafe_crossing_true->V23_abandonment_indicator, V17_observed_unsafe_label->V21_near_conflict_flag, V18_vehicle_approach_speed_mps->V19_ped_traverse_time_s, V19_ped_traverse_time_s->V22_wait_time_until_walk_s, V1_countdown_policy_enabled->V22_wait_time_until_walk_s, V1_countdown_policy_enabled->V24_start_decision_now, V22_wait_time_until_walk_s->V7_timer_visibility_quality, V23_abandonment_indicator->V1_countdown_policy_enabled, V23_abandonment_indicator->V21_near_conflict_flag, V23_abandonment_indicator->V7_timer_visibility_quality, V24_start_decision_now->V7_timer_visibility_quality, V5_traffic_flow_rate_vpm->V21_near_conflict_flag, V5_traffic_flow_rate_vpm->V22_wait_time_until_walk_s, V8_visible_remaining_seconds->V22_wait_time_until_walk_s.

## Arm `q031` (1 runs)

Family `s2_03`, role `real`. Column labels: prior_false_alarm_experience, assistance_request, attention_share_siren, departure_time_observed, assistance_fleet_vehicles, baseline_risk_tolerance, perceived_credibility_score, hazard_distance_at_t0, message_specificity_level, attention_share_sms, congestion_index_at_decision, sms_alert_enabled, handset_reachable, mobility_needs_index, siren_audibility_index, attention_share_neighbors, departure_time_true, attention_share_social, readiness_time_since_t0, hazard_approach_rate, vehicle_access, local_cumulative_departure_fraction, attention_share_news, pickup_eta_minutes, censor_indicator. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 27.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 9.0 (1 run) | n/a | n/a |
| S2 after LLM review | 38.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 37.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 37.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 36, B 2, C 239, D 23.

**Final edges.** 37 distinct edges appear in at least one run; 37 appear in every run. Set by: llm 37. Per run: LLM-set edges 37.0 (1 run); final edges between pairs the algorithm did not connect 31.0 (1 run); LLM additions where at least 90% of resamples had no edge 31.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| prior_false_alarm_experience->assistance_request | 1 |
| prior_false_alarm_experience->baseline_risk_tolerance | 1 |
| prior_false_alarm_experience->perceived_credibility_score | 1 |
| assistance_request->attention_share_siren | 1 |
| assistance_request->perceived_credibility_score | 1 |
| assistance_request->message_specificity_level | 1 |
| assistance_request->attention_share_sms | 1 |
| assistance_request->congestion_index_at_decision | 1 |
| assistance_request->sms_alert_enabled | 1 |
| assistance_request->handset_reachable | 1 |
| assistance_request->mobility_needs_index | 1 |
| assistance_request->siren_audibility_index | 1 |
| assistance_request->attention_share_neighbors | 1 |
| assistance_request->attention_share_social | 1 |
| readiness_time_since_t0->assistance_request | 1 |
| assistance_request->hazard_approach_rate | 1 |
| assistance_request->vehicle_access | 1 |
| assistance_request->attention_share_news | 1 |
| attention_share_siren->siren_audibility_index | 1 |
| departure_time_observed->congestion_index_at_decision | 1 |
| assistance_fleet_vehicles->congestion_index_at_decision | 1 |
| assistance_fleet_vehicles->vehicle_access | 1 |
| assistance_fleet_vehicles->local_cumulative_departure_fraction | 1 |
| baseline_risk_tolerance->perceived_credibility_score | 1 |
| perceived_credibility_score->message_specificity_level | 1 |
| hazard_distance_at_t0->congestion_index_at_decision | 1 |
| hazard_distance_at_t0->hazard_approach_rate | 1 |
| attention_share_sms->sms_alert_enabled | 1 |
| congestion_index_at_decision->hazard_approach_rate | 1 |
| congestion_index_at_decision->local_cumulative_departure_fraction | 1 |
| sms_alert_enabled->handset_reachable | 1 |
| handset_reachable->vehicle_access | 1 |
| mobility_needs_index->vehicle_access | 1 |
| departure_time_true->local_cumulative_departure_fraction | 1 |
| attention_share_social->attention_share_news | 1 |
| hazard_approach_rate->local_cumulative_departure_fraction | 1 |
| vehicle_access->local_cumulative_departure_fraction | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.74 (1 run) | 0.34 (1 run) | 0.47 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 61.0 (1 run) | 0.80 (1 run) | 0.07 (1 run) | 0.13 (1 run) |
| S1 after bootstrap edits | 0.89 (1 run) | 0.14 (1 run) | 0.24 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 56.0 (1 run) | 0.75 (1 run) | 0.05 (1 run) | 0.10 (1 run) |
| S2 after LLM review | 0.32 (1 run) | 0.21 (1 run) | 0.25 (1 run) | 2.0 (1 run) | 10.0 (1 run) | 82.0 (1 run) | 0.05 (1 run) | 0.03 (1 run) | 0.04 (1 run) |
| S3 after KCI pruning | 0.32 (1 run) | 0.21 (1 run) | 0.25 (1 run) | 2.0 (1 run) | 10.0 (1 run) | 81.0 (1 run) | 0.05 (1 run) | 0.03 (1 run) | 0.04 (1 run) |
| S4 final (after cycle step) | 0.32 (1 run) | 0.21 (1 run) | 0.25 (1 run) | 2.0 (1 run) | 10.0 (1 run) | 81.0 (1 run) | 0.05 (1 run) | 0.03 (1 run) | 0.04 (1 run) |

## Arm `q032` (1 runs)

Family `s2_03`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 31.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 13.0 (1 run) | n/a | n/a |
| S2 after LLM review | 13.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 13.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 13.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 2, B 1, C 1, D 296.

**Final edges.** 13 distinct edges appear in at least one run; 13 appear in every run. Set by: algorithm (unchanged) 13. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V02 <-> V19 | 1 |
| V03 <-> V10 | 1 |
| V03 <-> V16 | 1 |
| V03->V23 | 1 |
| V09 o-> V07 | 1 |
| V17->V08 | 1 |
| V09 o-> V22 | 1 |
| V10 o-> V15 | 1 |
| V10->V18 | 1 |
| V22->V11 | 1 |
| V15->V16 | 1 |
| V18->V16 | 1 |
| V19 <-> V24 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.71 (1 run) | 0.38 (1 run) | 0.49 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 64.0 (1 run) | 0.43 (1 run) | 0.05 (1 run) | 0.09 (1 run) |
| S1 after bootstrap edits | 0.62 (1 run) | 0.14 (1 run) | 0.23 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 61.0 (1 run) | 0.33 (1 run) | 0.03 (1 run) | 0.06 (1 run) |
| S2 after LLM review | 0.62 (1 run) | 0.14 (1 run) | 0.23 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 61.0 (1 run) | 0.33 (1 run) | 0.03 (1 run) | 0.06 (1 run) |
| S3 after KCI pruning | 0.62 (1 run) | 0.14 (1 run) | 0.23 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 61.0 (1 run) | 0.33 (1 run) | 0.03 (1 run) | 0.06 (1 run) |
| S4 final (after cycle step) | 0.62 (1 run) | 0.14 (1 run) | 0.23 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 61.0 (1 run) | 0.33 (1 run) | 0.03 (1 run) | 0.06 (1 run) |

## Arm `q033` (1 runs)

Family `s2_03`, role `swapped`. Column labels: assistance_request, prior_false_alarm_experience, departure_time_observed, attention_share_siren, baseline_risk_tolerance, assistance_fleet_vehicles, hazard_distance_at_t0, perceived_credibility_score, attention_share_sms, congestion_index_at_decision, message_specificity_level, mobility_needs_index, attention_share_neighbors, sms_alert_enabled, attention_share_social, local_cumulative_departure_fraction, hazard_approach_rate, attention_share_news, handset_reachable, siren_audibility_index, departure_time_true, pickup_eta_minutes, censor_indicator, vehicle_access, readiness_time_since_t0. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 2, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 2, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 30.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 8.0 (1 run) | n/a | n/a |
| S2 after LLM review | 41.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 41.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 41.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 39, C 237, D 24.

**Final edges.** 41 distinct edges appear in at least one run; 41 appear in every run. Set by: llm 37, algorithm (unchanged) 4. Per run: LLM-set edges 37.0 (1 run); final edges between pairs the algorithm did not connect 33.0 (1 run); LLM additions where at least 90% of resamples had no edge 31.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| assistance_request->prior_false_alarm_experience | 1 |
| assistance_request->attention_share_siren | 1 |
| assistance_request->baseline_risk_tolerance | 1 |
| assistance_request->hazard_distance_at_t0 | 1 |
| assistance_request->perceived_credibility_score | 1 |
| assistance_request->attention_share_sms | 1 |
| assistance_request->congestion_index_at_decision | 1 |
| assistance_request->message_specificity_level | 1 |
| assistance_request->mobility_needs_index | 1 |
| assistance_request->attention_share_neighbors | 1 |
| assistance_request->sms_alert_enabled | 1 |
| assistance_request->attention_share_social | 1 |
| assistance_request->local_cumulative_departure_fraction | 1 |
| assistance_request->hazard_approach_rate | 1 |
| assistance_request->attention_share_news | 1 |
| assistance_request->handset_reachable | 1 |
| assistance_request->siren_audibility_index | 1 |
| assistance_request->vehicle_access | 1 |
| departure_time_observed->congestion_index_at_decision | 1 |
| departure_time_observed->departure_time_true | 1 |
| departure_time_observed->censor_indicator | 1 |
| attention_share_siren->siren_audibility_index | 1 |
| baseline_risk_tolerance->mobility_needs_index | 1 |
| assistance_fleet_vehicles->vehicle_access | 1 |
| perceived_credibility_score->message_specificity_level | 1 |
| hazard_approach_rate->perceived_credibility_score | 1 |
| perceived_credibility_score->attention_share_news | 1 |
| attention_share_sms->sms_alert_enabled | 1 |
| congestion_index_at_decision <-> attention_share_social | 1 |
| congestion_index_at_decision->local_cumulative_departure_fraction | 1 |
| congestion_index_at_decision->departure_time_true | 1 |
| congestion_index_at_decision->pickup_eta_minutes | 1 |
| message_specificity_level->attention_share_news | 1 |
| mobility_needs_index->vehicle_access | 1 |
| attention_share_neighbors->attention_share_social | 1 |
| attention_share_social->attention_share_news | 1 |
| local_cumulative_departure_fraction->departure_time_true | 1 |
| hazard_approach_rate->attention_share_news | 1 |
| handset_reachable->vehicle_access | 1 |
| departure_time_true->pickup_eta_minutes | 1 |
| departure_time_true->censor_indicator | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.70 (1 run) | 0.36 (1 run) | 0.48 (1 run) | 1.0 (1 run) | 1.0 (1 run) | 66.0 (1 run) | 0.12 (1 run) | 0.02 (1 run) | 0.03 (1 run) |
| S1 after bootstrap edits | 0.50 (1 run) | 0.07 (1 run) | 0.12 (1 run) | 1.0 (1 run) | 1.0 (1 run) | 61.0 (1 run) | 0.17 (1 run) | 0.02 (1 run) | 0.03 (1 run) |
| S2 after LLM review | 0.20 (1 run) | 0.14 (1 run) | 0.16 (1 run) | 5.0 (1 run) | 2.0 (1 run) | 86.0 (1 run) | 0.12 (1 run) | 0.09 (1 run) | 0.10 (1 run) |
| S3 after KCI pruning | 0.20 (1 run) | 0.14 (1 run) | 0.16 (1 run) | 5.0 (1 run) | 2.0 (1 run) | 86.0 (1 run) | 0.12 (1 run) | 0.09 (1 run) | 0.10 (1 run) |
| S4 final (after cycle step) | 0.20 (1 run) | 0.14 (1 run) | 0.16 (1 run) | 5.0 (1 run) | 2.0 (1 run) | 86.0 (1 run) | 0.12 (1 run) | 0.09 (1 run) | 0.10 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.13 (1 run) | 0.07 (1 run) | 0.09 (1 run) | 0.0 (1 run) | 2.0 (1 run) | 84.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.25 (1 run) | 0.03 (1 run) | 0.06 (1 run) | 0.0 (1 run) | 2.0 (1 run) | 64.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.37 (1 run) | 0.26 (1 run) | 0.30 (1 run) | 3.0 (1 run) | 12.0 (1 run) | 81.0 (1 run) | 0.07 (1 run) | 0.05 (1 run) | 0.06 (1 run) |
| S3 after KCI pruning | 0.37 (1 run) | 0.26 (1 run) | 0.30 (1 run) | 3.0 (1 run) | 12.0 (1 run) | 81.0 (1 run) | 0.07 (1 run) | 0.05 (1 run) | 0.06 (1 run) |
| S4 final (after cycle step) | 0.37 (1 run) | 0.26 (1 run) | 0.30 (1 run) | 3.0 (1 run) | 12.0 (1 run) | 81.0 (1 run) | 0.07 (1 run) | 0.05 (1 run) | 0.06 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 12 |
| data only | 5 |
| both | 1 |
| neither | 19 |

Direction among those: data: direction as in reference 4, data: reversed 1, labels: direction as in reference 3, labels: reversed 9.
Distinct edges: both: assistance_request->hazard_distance_at_t0; data only: assistance_request->attention_share_news, assistance_request->congestion_index_at_decision, assistance_request->local_cumulative_departure_fraction, attention_share_social->attention_share_news, handset_reachable->vehicle_access; labels only: assistance_request->hazard_approach_rate, assistance_request->mobility_needs_index, assistance_request->perceived_credibility_score, assistance_request->vehicle_access, attention_share_siren->siren_audibility_index, attention_share_sms->sms_alert_enabled, departure_time_observed->departure_time_true, departure_time_true->censor_indicator, local_cumulative_departure_fraction->departure_time_true, message_specificity_level->attention_share_news, perceived_credibility_score->attention_share_news, perceived_credibility_score->message_specificity_level; neither: assistance_fleet_vehicles->vehicle_access, assistance_request->attention_share_neighbors, assistance_request->attention_share_siren, assistance_request->attention_share_sms, assistance_request->attention_share_social, assistance_request->baseline_risk_tolerance, assistance_request->handset_reachable, assistance_request->message_specificity_level, assistance_request->prior_false_alarm_experience, assistance_request->siren_audibility_index, assistance_request->sms_alert_enabled, attention_share_neighbors->attention_share_social, baseline_risk_tolerance->mobility_needs_index, congestion_index_at_decision->departure_time_true, congestion_index_at_decision->pickup_eta_minutes, departure_time_observed->congestion_index_at_decision, departure_time_true->pickup_eta_minutes, hazard_approach_rate->attention_share_news, mobility_needs_index->vehicle_access.

## Arm `q042` (1 runs)

Family `s2_04`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 25.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 9.0 (1 run) | n/a | n/a |
| S2 after LLM review | 10.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 10.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 10.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 5, B 2, C 19, D 274.

**Final edges.** 10 distinct edges appear in at least one run; 10 appear in every run. Set by: algorithm (unchanged) 7, llm 3. Per run: LLM-set edges 3.0 (1 run); final edges between pairs the algorithm did not connect 2.0 (1 run); LLM additions where at least 90% of resamples had no edge 2.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V02 o-> V12 | 1 |
| V12->V04 | 1 |
| V04->V17 | 1 |
| V06 <-> V17 | 1 |
| V09->V14 | 1 |
| V14->V10 | 1 |
| V10->V15 | 1 |
| V14->V15 | 1 |
| V14 <-> V17 | 1 |
| V15->V23 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.84 (1 run) | 0.53 (1 run) | 0.65 (1 run) | 4.0 (1 run) | 1.0 (1 run) | 40.0 (1 run) | 0.67 (1 run) | 0.10 (1 run) | 0.17 (1 run) |
| S1 after bootstrap edits | 0.89 (1 run) | 0.20 (1 run) | 0.33 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 0.80 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S2 after LLM review | 0.70 (1 run) | 0.17 (1 run) | 0.28 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 40.0 (1 run) | 0.43 (1 run) | 0.07 (1 run) | 0.13 (1 run) |
| S3 after KCI pruning | 0.70 (1 run) | 0.17 (1 run) | 0.28 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 40.0 (1 run) | 0.43 (1 run) | 0.07 (1 run) | 0.13 (1 run) |
| S4 final (after cycle step) | 0.70 (1 run) | 0.17 (1 run) | 0.28 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 40.0 (1 run) | 0.43 (1 run) | 0.07 (1 run) | 0.13 (1 run) |

## Arm `q043` (1 runs)

Family `s2_04`, role `swapped`. Column labels: thermostat_setpoint_c, outdoor_relative_humidity_pct, seat_operative_temperature_c, individual_thermal_sensitivity_index, total_skipped_items_count, room_attendance_rate, person_speed_trait_index, outdoor_temperature_c, time_share_section_b, assigned_seat_location_index, exam_version_difficulty_index, person_ability_theta, room_avg_temperature_c, seat_relative_humidity_pct, local_neighbor_density_index, hvac_mode, time_share_section_a, exam_start_time_offset_min, initial_time_budget_min, perceived_discomfort_index, seat_distance_to_vent_m, allowed_setpoint_range_c, total_score_points, time_lost_due_to_disruption_min, room_avg_relative_humidity_pct. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 27.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 5.0 (1 run) | n/a | n/a |
| S2 after LLM review | 49.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 49.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 49.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 49, C 246, D 5.

**Final edges.** 49 distinct edges appear in at least one run; 49 appear in every run. Set by: llm 48, algorithm (unchanged) 1. Per run: LLM-set edges 48.0 (1 run); final edges between pairs the algorithm did not connect 46.0 (1 run); LLM additions where at least 90% of resamples had no edge 44.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| thermostat_setpoint_c->seat_operative_temperature_c | 1 |
| thermostat_setpoint_c->individual_thermal_sensitivity_index | 1 |
| thermostat_setpoint_c->room_avg_temperature_c | 1 |
| thermostat_setpoint_c->seat_relative_humidity_pct | 1 |
| thermostat_setpoint_c->hvac_mode | 1 |
| thermostat_setpoint_c->perceived_discomfort_index | 1 |
| thermostat_setpoint_c->allowed_setpoint_range_c | 1 |
| thermostat_setpoint_c->room_avg_relative_humidity_pct | 1 |
| outdoor_relative_humidity_pct->seat_operative_temperature_c | 1 |
| outdoor_relative_humidity_pct->outdoor_temperature_c | 1 |
| outdoor_relative_humidity_pct->room_avg_temperature_c | 1 |
| outdoor_relative_humidity_pct->seat_relative_humidity_pct | 1 |
| outdoor_relative_humidity_pct->perceived_discomfort_index | 1 |
| outdoor_relative_humidity_pct->room_avg_relative_humidity_pct | 1 |
| seat_operative_temperature_c->individual_thermal_sensitivity_index | 1 |
| seat_operative_temperature_c->room_avg_temperature_c | 1 |
| seat_operative_temperature_c->seat_relative_humidity_pct | 1 |
| seat_operative_temperature_c->perceived_discomfort_index | 1 |
| seat_operative_temperature_c->room_avg_relative_humidity_pct | 1 |
| individual_thermal_sensitivity_index->room_avg_temperature_c | 1 |
| individual_thermal_sensitivity_index->seat_relative_humidity_pct | 1 |
| individual_thermal_sensitivity_index->perceived_discomfort_index | 1 |
| room_attendance_rate->total_score_points | 1 |
| outdoor_temperature_c->room_avg_temperature_c | 1 |
| outdoor_temperature_c->seat_relative_humidity_pct | 1 |
| outdoor_temperature_c->hvac_mode | 1 |
| outdoor_temperature_c->perceived_discomfort_index | 1 |
| outdoor_temperature_c->room_avg_relative_humidity_pct | 1 |
| time_share_section_b->seat_relative_humidity_pct | 1 |
| assigned_seat_location_index->seat_distance_to_vent_m | 1 |
| exam_version_difficulty_index->person_ability_theta | 1 |
| exam_version_difficulty_index->perceived_discomfort_index | 1 |
| exam_version_difficulty_index->total_score_points | 1 |
| person_ability_theta->perceived_discomfort_index | 1 |
| person_ability_theta->total_score_points | 1 |
| room_avg_temperature_c->seat_relative_humidity_pct | 1 |
| room_avg_temperature_c->hvac_mode | 1 |
| room_avg_temperature_c->perceived_discomfort_index | 1 |
| room_avg_temperature_c->allowed_setpoint_range_c | 1 |
| room_avg_temperature_c->room_avg_relative_humidity_pct | 1 |
| seat_relative_humidity_pct->perceived_discomfort_index | 1 |
| seat_relative_humidity_pct->room_avg_relative_humidity_pct | 1 |
| hvac_mode->perceived_discomfort_index | 1 |
| hvac_mode->allowed_setpoint_range_c | 1 |
| hvac_mode->room_avg_relative_humidity_pct | 1 |
| initial_time_budget_min->time_lost_due_to_disruption_min | 1 |
| perceived_discomfort_index->room_avg_relative_humidity_pct | 1 |
| allowed_setpoint_range_c->room_avg_relative_humidity_pct | 1 |
| total_score_points->time_lost_due_to_disruption_min | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.81 (1 run) | 0.55 (1 run) | 0.66 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 42.0 (1 run) | 1.00 (1 run) | 0.07 (1 run) | 0.14 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.12 (1 run) | 0.22 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 1.00 (1 run) | 0.07 (1 run) | 0.14 (1 run) |
| S2 after LLM review | 0.08 (1 run) | 0.10 (1 run) | 0.09 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 82.0 (1 run) | 0.06 (1 run) | 0.07 (1 run) | 0.07 (1 run) |
| S3 after KCI pruning | 0.08 (1 run) | 0.10 (1 run) | 0.09 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 82.0 (1 run) | 0.06 (1 run) | 0.07 (1 run) | 0.07 (1 run) |
| S4 final (after cycle step) | 0.08 (1 run) | 0.10 (1 run) | 0.09 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 82.0 (1 run) | 0.06 (1 run) | 0.07 (1 run) | 0.07 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.04 (1 run) | 0.03 (1 run) | 0.03 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 66.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 45.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.31 (1 run) | 0.38 (1 run) | 0.34 (1 run) | 10.0 (1 run) | 5.0 (1 run) | 65.0 (1 run) | 0.20 (1 run) | 0.25 (1 run) | 0.22 (1 run) |
| S3 after KCI pruning | 0.31 (1 run) | 0.38 (1 run) | 0.34 (1 run) | 10.0 (1 run) | 5.0 (1 run) | 65.0 (1 run) | 0.20 (1 run) | 0.25 (1 run) | 0.22 (1 run) |
| S4 final (after cycle step) | 0.31 (1 run) | 0.38 (1 run) | 0.34 (1 run) | 10.0 (1 run) | 5.0 (1 run) | 65.0 (1 run) | 0.20 (1 run) | 0.25 (1 run) | 0.22 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 15 |
| data only | 3 |
| both | 0 |
| neither | 30 |

Direction among those: data: direction as in reference 2, data: reversed 1, labels: direction as in reference 10, labels: reversed 5.
Distinct edges: data only: initial_time_budget_min->time_lost_due_to_disruption_min, outdoor_temperature_c->seat_relative_humidity_pct, person_ability_theta->perceived_discomfort_index; labels only: assigned_seat_location_index->seat_distance_to_vent_m, exam_version_difficulty_index->total_score_points, hvac_mode->room_avg_relative_humidity_pct, individual_thermal_sensitivity_index->perceived_discomfort_index, outdoor_relative_humidity_pct->room_avg_relative_humidity_pct, outdoor_temperature_c->room_avg_temperature_c, person_ability_theta->total_score_points, room_avg_temperature_c->allowed_setpoint_range_c, room_avg_temperature_c->hvac_mode, seat_operative_temperature_c->perceived_discomfort_index, seat_operative_temperature_c->room_avg_temperature_c, seat_relative_humidity_pct->perceived_discomfort_index, seat_relative_humidity_pct->room_avg_relative_humidity_pct, thermostat_setpoint_c->room_avg_temperature_c, total_score_points->time_lost_due_to_disruption_min; neither: allowed_setpoint_range_c->room_avg_relative_humidity_pct, exam_version_difficulty_index->perceived_discomfort_index, exam_version_difficulty_index->person_ability_theta, hvac_mode->allowed_setpoint_range_c, hvac_mode->perceived_discomfort_index, individual_thermal_sensitivity_index->room_avg_temperature_c, individual_thermal_sensitivity_index->seat_relative_humidity_pct, outdoor_relative_humidity_pct->outdoor_temperature_c, outdoor_relative_humidity_pct->perceived_discomfort_index, outdoor_relative_humidity_pct->room_avg_temperature_c, outdoor_relative_humidity_pct->seat_operative_temperature_c, outdoor_relative_humidity_pct->seat_relative_humidity_pct, outdoor_temperature_c->hvac_mode, outdoor_temperature_c->perceived_discomfort_index, outdoor_temperature_c->room_avg_relative_humidity_pct, perceived_discomfort_index->room_avg_relative_humidity_pct, room_attendance_rate->total_score_points, room_avg_temperature_c->perceived_discomfort_index, room_avg_temperature_c->room_avg_relative_humidity_pct, room_avg_temperature_c->seat_relative_humidity_pct, seat_operative_temperature_c->individual_thermal_sensitivity_index, seat_operative_temperature_c->room_avg_relative_humidity_pct, seat_operative_temperature_c->seat_relative_humidity_pct, thermostat_setpoint_c->allowed_setpoint_range_c, thermostat_setpoint_c->hvac_mode, thermostat_setpoint_c->individual_thermal_sensitivity_index, thermostat_setpoint_c->perceived_discomfort_index, thermostat_setpoint_c->room_avg_relative_humidity_pct, thermostat_setpoint_c->seat_operative_temperature_c, thermostat_setpoint_c->seat_relative_humidity_pct.

## Arm `q051` (1 runs)

Family `s2_05`, role `real`. Column labels: retail_list_price_dollars, cycle_gross_margin_dollars, lead_time_days, waste_units_disposed, stockout_days_count, demand_forecast_units_per_day, shelf_capacity_units, markdown_policy_schedule, credit_draw_amount_dollars, credit_line_offer_flag, interest_expense_dollars, reorder_point_units, interest_rate_apr, chosen_service_level, tentative_order_quantity_units, unit_wholesale_price, early_payment_choice, available_credit_dollars, cash_on_hand_dollars, on_hand_units_at_open. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 20 | 0 | 0 | 20 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 17.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 5.0 (1 run) | n/a | n/a |
| S2 after LLM review | 46.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 46.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 46.0 (1 run) | n/a | n/a |

**LLM review decisions.** 190 pairs. Same decision in every run: 190. Same edge/no-edge call in every run: 190. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 46, C 140, D 4.

**Final edges.** 46 distinct edges appear in at least one run; 46 appear in every run. Set by: llm 45, algorithm (unchanged) 1. Per run: LLM-set edges 45.0 (1 run); final edges between pairs the algorithm did not connect 34.0 (1 run); LLM additions where at least 90% of resamples had no edge 29.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| retail_list_price_dollars->cycle_gross_margin_dollars | 1 |
| retail_list_price_dollars->demand_forecast_units_per_day | 1 |
| retail_list_price_dollars->markdown_policy_schedule | 1 |
| retail_list_price_dollars->tentative_order_quantity_units | 1 |
| cycle_gross_margin_dollars->demand_forecast_units_per_day | 1 |
| cycle_gross_margin_dollars->markdown_policy_schedule | 1 |
| cycle_gross_margin_dollars->tentative_order_quantity_units | 1 |
| cycle_gross_margin_dollars->unit_wholesale_price | 1 |
| lead_time_days->stockout_days_count | 1 |
| lead_time_days->reorder_point_units | 1 |
| waste_units_disposed->stockout_days_count | 1 |
| waste_units_disposed->demand_forecast_units_per_day | 1 |
| waste_units_disposed->shelf_capacity_units | 1 |
| waste_units_disposed->markdown_policy_schedule | 1 |
| waste_units_disposed->reorder_point_units | 1 |
| waste_units_disposed->tentative_order_quantity_units | 1 |
| waste_units_disposed->on_hand_units_at_open | 1 |
| stockout_days_count->demand_forecast_units_per_day | 1 |
| stockout_days_count->reorder_point_units | 1 |
| stockout_days_count->tentative_order_quantity_units | 1 |
| stockout_days_count->on_hand_units_at_open | 1 |
| demand_forecast_units_per_day->reorder_point_units | 1 |
| demand_forecast_units_per_day->tentative_order_quantity_units | 1 |
| shelf_capacity_units->reorder_point_units | 1 |
| shelf_capacity_units->tentative_order_quantity_units | 1 |
| shelf_capacity_units->on_hand_units_at_open | 1 |
| markdown_policy_schedule->chosen_service_level | 1 |
| markdown_policy_schedule->tentative_order_quantity_units | 1 |
| credit_draw_amount_dollars->interest_expense_dollars | 1 |
| credit_draw_amount_dollars->available_credit_dollars | 1 |
| credit_draw_amount_dollars->cash_on_hand_dollars | 1 |
| credit_line_offer_flag->early_payment_choice | 1 |
| credit_line_offer_flag->available_credit_dollars | 1 |
| interest_expense_dollars->interest_rate_apr | 1 |
| interest_expense_dollars->available_credit_dollars | 1 |
| interest_expense_dollars->cash_on_hand_dollars | 1 |
| reorder_point_units->chosen_service_level | 1 |
| reorder_point_units->tentative_order_quantity_units | 1 |
| reorder_point_units->on_hand_units_at_open | 1 |
| interest_rate_apr->available_credit_dollars | 1 |
| interest_rate_apr->cash_on_hand_dollars | 1 |
| chosen_service_level->tentative_order_quantity_units | 1 |
| tentative_order_quantity_units->on_hand_units_at_open | 1 |
| early_payment_choice->available_credit_dollars | 1 |
| early_payment_choice->cash_on_hand_dollars | 1 |
| available_credit_dollars->cash_on_hand_dollars | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.76 (1 run) | 0.34 (1 run) | 0.47 (1 run) | 5.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 0.83 (1 run) | 0.13 (1 run) | 0.23 (1 run) |
| S1 after bootstrap edits | 0.80 (1 run) | 0.11 (1 run) | 0.19 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 36.0 (1 run) | 1.00 (1 run) | 0.08 (1 run) | 0.15 (1 run) |
| S2 after LLM review | 0.50 (1 run) | 0.61 (1 run) | 0.55 (1 run) | 9.0 (1 run) | 14.0 (1 run) | 54.0 (1 run) | 0.20 (1 run) | 0.24 (1 run) | 0.21 (1 run) |
| S3 after KCI pruning | 0.50 (1 run) | 0.61 (1 run) | 0.55 (1 run) | 9.0 (1 run) | 14.0 (1 run) | 54.0 (1 run) | 0.20 (1 run) | 0.24 (1 run) | 0.21 (1 run) |
| S4 final (after cycle step) | 0.50 (1 run) | 0.61 (1 run) | 0.55 (1 run) | 9.0 (1 run) | 14.0 (1 run) | 54.0 (1 run) | 0.20 (1 run) | 0.24 (1 run) | 0.21 (1 run) |

## Arm `q052` (1 runs)

Family `s2_05`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 20 | 0 | 0 | 20 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 18.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 4.0 (1 run) | n/a | n/a |
| S2 after LLM review | 3.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 3.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 3.0 (1 run) | n/a | n/a |

**LLM review decisions.** 190 pairs. Same decision in every run: 190. Same edge/no-edge call in every run: 190. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 1, C 11, D 178.

**Final edges.** 3 distinct edges appear in at least one run; 3 appear in every run. Set by: algorithm (unchanged) 3. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V02 <-> V15 | 1 |
| V09->V11 | 1 |
| V10 ~~~ V18 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.83 (1 run) | 0.39 (1 run) | 0.54 (1 run) | 2.0 (1 run) | 0.0 (1 run) | 39.0 (1 run) | 0.67 (1 run) | 0.05 (1 run) | 0.10 (1 run) |
| S1 after bootstrap edits | 0.75 (1 run) | 0.08 (1 run) | 0.14 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 38.0 (1 run) | 1.00 (1 run) | 0.03 (1 run) | 0.05 (1 run) |
| S2 after LLM review | 1.00 (1 run) | 0.08 (1 run) | 0.15 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 1.00 (1 run) | 0.03 (1 run) | 0.05 (1 run) |
| S3 after KCI pruning | 1.00 (1 run) | 0.08 (1 run) | 0.15 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 1.00 (1 run) | 0.03 (1 run) | 0.05 (1 run) |
| S4 final (after cycle step) | 1.00 (1 run) | 0.08 (1 run) | 0.15 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 1.00 (1 run) | 0.03 (1 run) | 0.05 (1 run) |

## Arm `q053` (1 runs)

Family `s2_05`, role `swapped`. Column labels: cycle_gross_margin_dollars, lead_time_days, retail_list_price_dollars, demand_forecast_units_per_day, waste_units_disposed, shelf_capacity_units, stockout_days_count, credit_draw_amount_dollars, markdown_policy_schedule, interest_expense_dollars, credit_line_offer_flag, interest_rate_apr, reorder_point_units, tentative_order_quantity_units, unit_wholesale_price, available_credit_dollars, cash_on_hand_dollars, chosen_service_level, on_hand_units_at_open, early_payment_choice. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 2, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 20 | 0 | 0 | 20 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 2, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 18.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 4.0 (1 run) | n/a | n/a |
| S2 after LLM review | 38.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 38.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 38.0 (1 run) | n/a | n/a |

**LLM review decisions.** 190 pairs. Same decision in every run: 190. Same edge/no-edge call in every run: 190. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 37, C 147, D 6.

**Final edges.** 38 distinct edges appear in at least one run; 38 appear in every run. Set by: llm 36, algorithm (unchanged) 2. Per run: LLM-set edges 36.0 (1 run); final edges between pairs the algorithm did not connect 33.0 (1 run); LLM additions where at least 90% of resamples had no edge 30.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| cycle_gross_margin_dollars->retail_list_price_dollars | 1 |
| cycle_gross_margin_dollars->demand_forecast_units_per_day | 1 |
| cycle_gross_margin_dollars->markdown_policy_schedule | 1 |
| lead_time_days->stockout_days_count | 1 |
| lead_time_days->reorder_point_units | 1 |
| lead_time_days->on_hand_units_at_open | 1 |
| retail_list_price_dollars->demand_forecast_units_per_day | 1 |
| retail_list_price_dollars->markdown_policy_schedule | 1 |
| retail_list_price_dollars->tentative_order_quantity_units | 1 |
| retail_list_price_dollars->on_hand_units_at_open | 1 |
| demand_forecast_units_per_day->stockout_days_count | 1 |
| demand_forecast_units_per_day->reorder_point_units | 1 |
| demand_forecast_units_per_day->tentative_order_quantity_units | 1 |
| demand_forecast_units_per_day->on_hand_units_at_open | 1 |
| shelf_capacity_units->reorder_point_units | 1 |
| shelf_capacity_units->tentative_order_quantity_units | 1 |
| shelf_capacity_units->unit_wholesale_price | 1 |
| shelf_capacity_units->on_hand_units_at_open | 1 |
| stockout_days_count->reorder_point_units | 1 |
| stockout_days_count->tentative_order_quantity_units | 1 |
| stockout_days_count->on_hand_units_at_open | 1 |
| credit_draw_amount_dollars->interest_expense_dollars | 1 |
| credit_draw_amount_dollars->credit_line_offer_flag | 1 |
| credit_draw_amount_dollars->available_credit_dollars | 1 |
| credit_draw_amount_dollars->cash_on_hand_dollars | 1 |
| markdown_policy_schedule->credit_line_offer_flag | 1 |
| interest_expense_dollars->credit_line_offer_flag | 1 |
| interest_expense_dollars->interest_rate_apr | 1 |
| interest_expense_dollars->available_credit_dollars | 1 |
| interest_expense_dollars->cash_on_hand_dollars | 1 |
| credit_line_offer_flag->available_credit_dollars | 1 |
| credit_line_offer_flag->cash_on_hand_dollars | 1 |
| interest_rate_apr->available_credit_dollars | 1 |
| interest_rate_apr->cash_on_hand_dollars | 1 |
| reorder_point_units->tentative_order_quantity_units | 1 |
| reorder_point_units->on_hand_units_at_open | 1 |
| tentative_order_quantity_units->on_hand_units_at_open | 1 |
| available_credit_dollars->cash_on_hand_dollars | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.83 (1 run) | 0.39 (1 run) | 0.54 (1 run) | 2.0 (1 run) | 0.0 (1 run) | 39.0 (1 run) | 1.00 (1 run) | 0.05 (1 run) | 0.10 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.11 (1 run) | 0.19 (1 run) | 2.0 (1 run) | 0.0 (1 run) | 36.0 (1 run) | 1.00 (1 run) | 0.05 (1 run) | 0.10 (1 run) |
| S2 after LLM review | 0.13 (1 run) | 0.13 (1 run) | 0.13 (1 run) | 3.0 (1 run) | 2.0 (1 run) | 68.0 (1 run) | 0.08 (1 run) | 0.08 (1 run) | 0.08 (1 run) |
| S3 after KCI pruning | 0.13 (1 run) | 0.13 (1 run) | 0.13 (1 run) | 3.0 (1 run) | 2.0 (1 run) | 68.0 (1 run) | 0.08 (1 run) | 0.08 (1 run) | 0.08 (1 run) |
| S4 final (after cycle step) | 0.13 (1 run) | 0.13 (1 run) | 0.13 (1 run) | 3.0 (1 run) | 2.0 (1 run) | 68.0 (1 run) | 0.08 (1 run) | 0.08 (1 run) | 0.08 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.06 (1 run) | 0.03 (1 run) | 0.04 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 55.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 42.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.42 (1 run) | 0.42 (1 run) | 0.42 (1 run) | 8.0 (1 run) | 8.0 (1 run) | 54.0 (1 run) | 0.21 (1 run) | 0.21 (1 run) | 0.21 (1 run) |
| S3 after KCI pruning | 0.42 (1 run) | 0.42 (1 run) | 0.42 (1 run) | 8.0 (1 run) | 8.0 (1 run) | 54.0 (1 run) | 0.21 (1 run) | 0.21 (1 run) | 0.21 (1 run) |
| S4 final (after cycle step) | 0.42 (1 run) | 0.42 (1 run) | 0.42 (1 run) | 8.0 (1 run) | 8.0 (1 run) | 54.0 (1 run) | 0.21 (1 run) | 0.21 (1 run) | 0.21 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 16 |
| data only | 3 |
| both | 0 |
| neither | 17 |

Direction among those: data: direction as in reference 1, data: reversed 2, labels: direction as in reference 8, labels: reversed 8.
Distinct edges: data only: credit_line_offer_flag->cash_on_hand_dollars, retail_list_price_dollars->demand_forecast_units_per_day, retail_list_price_dollars->tentative_order_quantity_units; labels only: credit_draw_amount_dollars->available_credit_dollars, credit_draw_amount_dollars->cash_on_hand_dollars, credit_draw_amount_dollars->interest_expense_dollars, credit_line_offer_flag->available_credit_dollars, cycle_gross_margin_dollars->demand_forecast_units_per_day, cycle_gross_margin_dollars->markdown_policy_schedule, cycle_gross_margin_dollars->retail_list_price_dollars, demand_forecast_units_per_day->reorder_point_units, demand_forecast_units_per_day->stockout_days_count, demand_forecast_units_per_day->tentative_order_quantity_units, interest_expense_dollars->interest_rate_apr, lead_time_days->stockout_days_count, reorder_point_units->tentative_order_quantity_units, shelf_capacity_units->tentative_order_quantity_units, stockout_days_count->on_hand_units_at_open, tentative_order_quantity_units->on_hand_units_at_open; neither: available_credit_dollars->cash_on_hand_dollars, credit_draw_amount_dollars->credit_line_offer_flag, demand_forecast_units_per_day->on_hand_units_at_open, interest_expense_dollars->available_credit_dollars, interest_expense_dollars->cash_on_hand_dollars, interest_expense_dollars->credit_line_offer_flag, interest_rate_apr->available_credit_dollars, interest_rate_apr->cash_on_hand_dollars, lead_time_days->on_hand_units_at_open, lead_time_days->reorder_point_units, reorder_point_units->on_hand_units_at_open, retail_list_price_dollars->markdown_policy_schedule, retail_list_price_dollars->on_hand_units_at_open, shelf_capacity_units->on_hand_units_at_open, shelf_capacity_units->reorder_point_units, stockout_days_count->reorder_point_units, stockout_days_count->tentative_order_quantity_units.

## Arm `q061` (1 runs)

Family `s2_06`, role `real`. Column labels: routing_weight_nearest_backup, rum_sampling_fraction, incident_error_rate, nearest_backup_capacity_rps, resolver_ttl_floor_seconds, baseline_latency_ms, serve_stale_enabled, resolver_class, failure_caching_level, stale_hit_probability_at_outage, cohort_request_rate_qps, consecutive_failure_threshold, ttl_config_seconds, failover_latency_seconds, selected_backup_pop, observed_incident_error_rate, probe_loss_jitter_rate, time_to_95p_adoption_seconds, primary_pop_outage, resolver_prefetch_threshold, detection_delay_seconds, observed_failover_latency_seconds, health_check_interval_seconds, ecs_present, client_region. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 2, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 2, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 20.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 6.0 (1 run) | n/a | n/a |
| S2 after LLM review | 37.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 37.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 37.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 37, C 253, D 10.

**Final edges.** 37 distinct edges appear in at least one run; 37 appear in every run. Set by: llm 35, algorithm (unchanged) 2. Per run: LLM-set edges 35.0 (1 run); final edges between pairs the algorithm did not connect 31.0 (1 run); LLM additions where at least 90% of resamples had no edge 27.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| routing_weight_nearest_backup->incident_error_rate | 1 |
| routing_weight_nearest_backup->nearest_backup_capacity_rps | 1 |
| routing_weight_nearest_backup->baseline_latency_ms | 1 |
| routing_weight_nearest_backup->observed_incident_error_rate | 1 |
| incident_error_rate->observed_incident_error_rate | 1 |
| nearest_backup_capacity_rps->observed_incident_error_rate | 1 |
| resolver_ttl_floor_seconds->stale_hit_probability_at_outage | 1 |
| resolver_ttl_floor_seconds->ttl_config_seconds | 1 |
| resolver_ttl_floor_seconds->resolver_prefetch_threshold | 1 |
| baseline_latency_ms->failover_latency_seconds | 1 |
| baseline_latency_ms->observed_incident_error_rate | 1 |
| baseline_latency_ms->observed_failover_latency_seconds | 1 |
| serve_stale_enabled->stale_hit_probability_at_outage | 1 |
| serve_stale_enabled->failover_latency_seconds | 1 |
| serve_stale_enabled->observed_incident_error_rate | 1 |
| serve_stale_enabled->detection_delay_seconds | 1 |
| serve_stale_enabled->observed_failover_latency_seconds | 1 |
| resolver_class->failure_caching_level | 1 |
| resolver_class->resolver_prefetch_threshold | 1 |
| failure_caching_level->stale_hit_probability_at_outage | 1 |
| failure_caching_level->failover_latency_seconds | 1 |
| failure_caching_level->resolver_prefetch_threshold | 1 |
| failure_caching_level->observed_failover_latency_seconds | 1 |
| stale_hit_probability_at_outage->observed_incident_error_rate | 1 |
| stale_hit_probability_at_outage->primary_pop_outage | 1 |
| consecutive_failure_threshold->failover_latency_seconds | 1 |
| consecutive_failure_threshold->observed_incident_error_rate | 1 |
| consecutive_failure_threshold->primary_pop_outage | 1 |
| consecutive_failure_threshold->observed_failover_latency_seconds | 1 |
| failover_latency_seconds->observed_failover_latency_seconds | 1 |
| observed_incident_error_rate->primary_pop_outage | 1 |
| observed_incident_error_rate->detection_delay_seconds | 1 |
| observed_incident_error_rate->observed_failover_latency_seconds | 1 |
| primary_pop_outage->detection_delay_seconds | 1 |
| primary_pop_outage->observed_failover_latency_seconds | 1 |
| resolver_prefetch_threshold->observed_failover_latency_seconds | 1 |
| detection_delay_seconds->health_check_interval_seconds | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.75 (1 run) | 0.32 (1 run) | 0.45 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 50.0 (1 run) | 0.67 (1 run) | 0.09 (1 run) | 0.15 (1 run) |
| S1 after bootstrap edits | 0.83 (1 run) | 0.11 (1 run) | 0.19 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 47.0 (1 run) | 0.75 (1 run) | 0.06 (1 run) | 0.12 (1 run) |
| S2 after LLM review | 0.19 (1 run) | 0.15 (1 run) | 0.17 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 73.0 (1 run) | 0.16 (1 run) | 0.13 (1 run) | 0.14 (1 run) |
| S3 after KCI pruning | 0.19 (1 run) | 0.15 (1 run) | 0.17 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 73.0 (1 run) | 0.16 (1 run) | 0.13 (1 run) | 0.14 (1 run) |
| S4 final (after cycle step) | 0.19 (1 run) | 0.15 (1 run) | 0.17 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 73.0 (1 run) | 0.16 (1 run) | 0.13 (1 run) | 0.14 (1 run) |

## Arm `q062` (1 runs)

Family `s2_06`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 20.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 6.0 (1 run) | n/a | n/a |
| S2 after LLM review | 13.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 13.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 13.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 10, B 3, C 98, D 189.

**Final edges.** 13 distinct edges appear in at least one run; 13 appear in every run. Set by: llm 9, algorithm (unchanged) 4. Per run: LLM-set edges 9.0 (1 run); final edges between pairs the algorithm did not connect 8.0 (1 run); LLM additions where at least 90% of resamples had no edge 7.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V04->V11 | 1 |
| V04->V18 | 1 |
| V05->V11 | 1 |
| V05->V18 | 1 |
| V06->V18 | 1 |
| V08->V07 | 1 |
| V08->V11 | 1 |
| V08->V18 | 1 |
| V08->V20 | 1 |
| V11->V18 | 1 |
| V20->V11 | 1 |
| V16->V20 | 1 |
| V20->V18 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.85 (1 run) | 0.36 (1 run) | 0.51 (1 run) | 5.0 (1 run) | 0.0 (1 run) | 47.0 (1 run) | 0.71 (1 run) | 0.11 (1 run) | 0.19 (1 run) |
| S1 after bootstrap edits | 0.83 (1 run) | 0.11 (1 run) | 0.19 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 46.0 (1 run) | 0.80 (1 run) | 0.09 (1 run) | 0.15 (1 run) |
| S2 after LLM review | 0.38 (1 run) | 0.11 (1 run) | 0.17 (1 run) | 5.0 (1 run) | 0.0 (1 run) | 52.0 (1 run) | 0.38 (1 run) | 0.11 (1 run) | 0.17 (1 run) |
| S3 after KCI pruning | 0.38 (1 run) | 0.11 (1 run) | 0.17 (1 run) | 5.0 (1 run) | 0.0 (1 run) | 52.0 (1 run) | 0.38 (1 run) | 0.11 (1 run) | 0.17 (1 run) |
| S4 final (after cycle step) | 0.38 (1 run) | 0.11 (1 run) | 0.17 (1 run) | 5.0 (1 run) | 0.0 (1 run) | 52.0 (1 run) | 0.38 (1 run) | 0.11 (1 run) | 0.17 (1 run) |

## Arm `q063` (1 runs)

Family `s2_06`, role `swapped`. Column labels: rum_sampling_fraction, routing_weight_nearest_backup, nearest_backup_capacity_rps, resolver_ttl_floor_seconds, incident_error_rate, serve_stale_enabled, baseline_latency_ms, cohort_request_rate_qps, consecutive_failure_threshold, ttl_config_seconds, failure_caching_level, resolver_class, failover_latency_seconds, stale_hit_probability_at_outage, probe_loss_jitter_rate, time_to_95p_adoption_seconds, selected_backup_pop, health_check_interval_seconds, observed_incident_error_rate, ecs_present, observed_failover_latency_seconds, detection_delay_seconds, client_region, primary_pop_outage, resolver_prefetch_threshold. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 2, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 2, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 20.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 4.0 (1 run) | n/a | n/a |
| S2 after LLM review | 25.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 25.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 25.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 25, C 266, D 9.

**Final edges.** 25 distinct edges appear in at least one run; 25 appear in every run. Set by: llm 25. Per run: LLM-set edges 25.0 (1 run); final edges between pairs the algorithm did not connect 20.0 (1 run); LLM additions where at least 90% of resamples had no edge 21.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| resolver_ttl_floor_seconds->baseline_latency_ms | 1 |
| resolver_ttl_floor_seconds->ttl_config_seconds | 1 |
| incident_error_rate->baseline_latency_ms | 1 |
| incident_error_rate->cohort_request_rate_qps | 1 |
| incident_error_rate->failover_latency_seconds | 1 |
| incident_error_rate->stale_hit_probability_at_outage | 1 |
| incident_error_rate->observed_incident_error_rate | 1 |
| incident_error_rate->observed_failover_latency_seconds | 1 |
| incident_error_rate->detection_delay_seconds | 1 |
| incident_error_rate->primary_pop_outage | 1 |
| serve_stale_enabled->stale_hit_probability_at_outage | 1 |
| baseline_latency_ms->cohort_request_rate_qps | 1 |
| baseline_latency_ms->observed_incident_error_rate | 1 |
| cohort_request_rate_qps->observed_incident_error_rate | 1 |
| consecutive_failure_threshold->observed_incident_error_rate | 1 |
| failover_latency_seconds->observed_failover_latency_seconds | 1 |
| stale_hit_probability_at_outage->observed_incident_error_rate | 1 |
| health_check_interval_seconds->detection_delay_seconds | 1 |
| observed_incident_error_rate->observed_failover_latency_seconds | 1 |
| observed_incident_error_rate->detection_delay_seconds | 1 |
| observed_incident_error_rate->primary_pop_outage | 1 |
| observed_failover_latency_seconds->detection_delay_seconds | 1 |
| observed_failover_latency_seconds->primary_pop_outage | 1 |
| detection_delay_seconds->primary_pop_outage | 1 |
| client_region->primary_pop_outage | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.75 (1 run) | 0.32 (1 run) | 0.45 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 50.0 (1 run) | 0.57 (1 run) | 0.09 (1 run) | 0.15 (1 run) |
| S1 after bootstrap edits | 0.75 (1 run) | 0.06 (1 run) | 0.12 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 47.0 (1 run) | 0.75 (1 run) | 0.06 (1 run) | 0.12 (1 run) |
| S2 after LLM review | 0.16 (1 run) | 0.09 (1 run) | 0.11 (1 run) | 1.0 (1 run) | 3.0 (1 run) | 67.0 (1 run) | 0.04 (1 run) | 0.02 (1 run) | 0.03 (1 run) |
| S3 after KCI pruning | 0.16 (1 run) | 0.09 (1 run) | 0.11 (1 run) | 1.0 (1 run) | 3.0 (1 run) | 67.0 (1 run) | 0.04 (1 run) | 0.02 (1 run) | 0.03 (1 run) |
| S4 final (after cycle step) | 0.16 (1 run) | 0.09 (1 run) | 0.11 (1 run) | 1.0 (1 run) | 3.0 (1 run) | 67.0 (1 run) | 0.04 (1 run) | 0.02 (1 run) | 0.03 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.15 (1 run) | 0.06 (1 run) | 0.09 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 61.0 (1 run) | 0.43 (1 run) | 0.06 (1 run) | 0.11 (1 run) |
| S1 after bootstrap edits | 0.25 (1 run) | 0.02 (1 run) | 0.04 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 49.0 (1 run) | 0.25 (1 run) | 0.02 (1 run) | 0.04 (1 run) |
| S2 after LLM review | 0.36 (1 run) | 0.19 (1 run) | 0.25 (1 run) | 4.0 (1 run) | 5.0 (1 run) | 60.0 (1 run) | 0.16 (1 run) | 0.09 (1 run) | 0.11 (1 run) |
| S3 after KCI pruning | 0.36 (1 run) | 0.19 (1 run) | 0.25 (1 run) | 4.0 (1 run) | 5.0 (1 run) | 60.0 (1 run) | 0.16 (1 run) | 0.09 (1 run) | 0.11 (1 run) |
| S4 final (after cycle step) | 0.36 (1 run) | 0.19 (1 run) | 0.25 (1 run) | 4.0 (1 run) | 5.0 (1 run) | 60.0 (1 run) | 0.16 (1 run) | 0.09 (1 run) | 0.11 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 9 |
| data only | 4 |
| both | 0 |
| neither | 12 |

Direction among those: data: direction as in reference 1, data: reversed 3, labels: direction as in reference 4, labels: reversed 5.
Distinct edges: data only: baseline_latency_ms->cohort_request_rate_qps, incident_error_rate->cohort_request_rate_qps, observed_incident_error_rate->observed_failover_latency_seconds, stale_hit_probability_at_outage->observed_incident_error_rate; labels only: client_region->primary_pop_outage, detection_delay_seconds->primary_pop_outage, failover_latency_seconds->observed_failover_latency_seconds, health_check_interval_seconds->detection_delay_seconds, incident_error_rate->baseline_latency_ms, incident_error_rate->detection_delay_seconds, incident_error_rate->observed_incident_error_rate, incident_error_rate->primary_pop_outage, incident_error_rate->stale_hit_probability_at_outage; neither: baseline_latency_ms->observed_incident_error_rate, cohort_request_rate_qps->observed_incident_error_rate, consecutive_failure_threshold->observed_incident_error_rate, incident_error_rate->failover_latency_seconds, incident_error_rate->observed_failover_latency_seconds, observed_failover_latency_seconds->detection_delay_seconds, observed_failover_latency_seconds->primary_pop_outage, observed_incident_error_rate->detection_delay_seconds, observed_incident_error_rate->primary_pop_outage, resolver_ttl_floor_seconds->baseline_latency_ms, resolver_ttl_floor_seconds->ttl_config_seconds, serve_stale_enabled->stale_hit_probability_at_outage.

## Arm `q072` (1 runs)

Family `s2_07`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 22 | 0 | 0 | 22 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 27.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 11.0 (1 run) | n/a | n/a |
| S2 after LLM review | 10.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 10.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 10.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 5, C 3, D 223.

**Final edges.** 10 distinct edges appear in at least one run; 10 appear in every run. Set by: algorithm (unchanged) 9, llm 1. Per run: LLM-set edges 1.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V01 o-o V21 | 1 |
| V02 ~~~ V10 | 1 |
| V10->V03 | 1 |
| V13 o-> V03 | 1 |
| V08->V11 | 1 |
| V09 o-> V12 | 1 |
| V09->V14 | 1 |
| V11->V21 | 1 |
| V12->V14 | 1 |
| V17->V22 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.78 (1 run) | 0.60 (1 run) | 0.68 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 36.0 (1 run) | 0.86 (1 run) | 0.17 (1 run) | 0.29 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.31 (1 run) | 0.48 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 31.0 (1 run) | 0.83 (1 run) | 0.14 (1 run) | 0.24 (1 run) |
| S2 after LLM review | 1.00 (1 run) | 0.29 (1 run) | 0.44 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 30.0 (1 run) | 1.00 (1 run) | 0.17 (1 run) | 0.29 (1 run) |
| S3 after KCI pruning | 1.00 (1 run) | 0.29 (1 run) | 0.44 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 30.0 (1 run) | 1.00 (1 run) | 0.17 (1 run) | 0.29 (1 run) |
| S4 final (after cycle step) | 1.00 (1 run) | 0.29 (1 run) | 0.44 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 30.0 (1 run) | 1.00 (1 run) | 0.17 (1 run) | 0.29 (1 run) |

## Arm `q073` (1 runs)

Family `s2_07`, role `swapped`. Column labels: attempted_trips_count, true_ems_heat_incidents, tree_canopy_pct, language_mismatch_rate, turnaways_count, indoor_time_above_safe_prop, neighborhood_heat_index, transit_vouchers_per_1000, social_isolation_rate, alerts_delivered_rate, outdoor_work_share, admitted_visits_count, effective_cooled_hours, distance_to_center_km, functional_capacity_day, effective_awareness_rate, hours_open, power_outage_rate, regional_heat_index_base, adjusted_heat_dose_index, observed_heat_calls, ac_ownership_rate. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 2, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 22 | 0 | 0 | 22 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 2, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 27.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 13.0 (1 run) | n/a | n/a |
| S2 after LLM review | 48.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 48.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 48.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 48, C 176, D 7.

**Final edges.** 48 distinct edges appear in at least one run; 48 appear in every run. Set by: llm 45, algorithm (unchanged) 3. Per run: LLM-set edges 45.0 (1 run); final edges between pairs the algorithm did not connect 39.0 (1 run); LLM additions where at least 90% of resamples had no edge 37.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| attempted_trips_count->transit_vouchers_per_1000 | 1 |
| true_ems_heat_incidents->neighborhood_heat_index | 1 |
| true_ems_heat_incidents->alerts_delivered_rate | 1 |
| true_ems_heat_incidents->admitted_visits_count | 1 |
| true_ems_heat_incidents->effective_awareness_rate | 1 |
| true_ems_heat_incidents->regional_heat_index_base | 1 |
| true_ems_heat_incidents->adjusted_heat_dose_index | 1 |
| true_ems_heat_incidents->observed_heat_calls | 1 |
| tree_canopy_pct->neighborhood_heat_index | 1 |
| tree_canopy_pct->effective_cooled_hours | 1 |
| tree_canopy_pct->regional_heat_index_base | 1 |
| tree_canopy_pct->adjusted_heat_dose_index | 1 |
| language_mismatch_rate->social_isolation_rate | 1 |
| language_mismatch_rate->alerts_delivered_rate | 1 |
| turnaways_count->functional_capacity_day | 1 |
| turnaways_count->hours_open | 1 |
| indoor_time_above_safe_prop->admitted_visits_count | 1 |
| indoor_time_above_safe_prop->adjusted_heat_dose_index | 1 |
| indoor_time_above_safe_prop->observed_heat_calls | 1 |
| neighborhood_heat_index->alerts_delivered_rate | 1 |
| neighborhood_heat_index->admitted_visits_count | 1 |
| neighborhood_heat_index->regional_heat_index_base | 1 |
| neighborhood_heat_index->adjusted_heat_dose_index | 1 |
| neighborhood_heat_index->observed_heat_calls | 1 |
| transit_vouchers_per_1000->outdoor_work_share | 1 |
| social_isolation_rate->alerts_delivered_rate | 1 |
| social_isolation_rate->admitted_visits_count | 1 |
| social_isolation_rate->effective_awareness_rate | 1 |
| social_isolation_rate->observed_heat_calls | 1 |
| alerts_delivered_rate->admitted_visits_count | 1 |
| alerts_delivered_rate->effective_awareness_rate | 1 |
| alerts_delivered_rate->adjusted_heat_dose_index | 1 |
| alerts_delivered_rate->observed_heat_calls | 1 |
| outdoor_work_share->admitted_visits_count | 1 |
| outdoor_work_share->observed_heat_calls | 1 |
| admitted_visits_count->observed_heat_calls | 1 |
| effective_cooled_hours->hours_open | 1 |
| effective_cooled_hours->adjusted_heat_dose_index | 1 |
| effective_cooled_hours->observed_heat_calls | 1 |
| effective_cooled_hours->ac_ownership_rate | 1 |
| functional_capacity_day->hours_open | 1 |
| effective_awareness_rate->observed_heat_calls | 1 |
| hours_open->ac_ownership_rate | 1 |
| power_outage_rate->observed_heat_calls | 1 |
| power_outage_rate->ac_ownership_rate | 1 |
| regional_heat_index_base->adjusted_heat_dose_index | 1 |
| regional_heat_index_base->observed_heat_calls | 1 |
| adjusted_heat_dose_index->observed_heat_calls | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.81 (1 run) | 0.63 (1 run) | 0.71 (1 run) | 9.0 (1 run) | 0.0 (1 run) | 32.0 (1 run) | 1.00 (1 run) | 0.26 (1 run) | 0.41 (1 run) |
| S1 after bootstrap edits | 0.92 (1 run) | 0.34 (1 run) | 0.50 (1 run) | 9.0 (1 run) | 0.0 (1 run) | 28.0 (1 run) | 1.00 (1 run) | 0.26 (1 run) | 0.41 (1 run) |
| S2 after LLM review | 0.21 (1 run) | 0.29 (1 run) | 0.24 (1 run) | 6.0 (1 run) | 4.0 (1 run) | 68.0 (1 run) | 0.12 (1 run) | 0.17 (1 run) | 0.14 (1 run) |
| S3 after KCI pruning | 0.21 (1 run) | 0.29 (1 run) | 0.24 (1 run) | 6.0 (1 run) | 4.0 (1 run) | 68.0 (1 run) | 0.12 (1 run) | 0.17 (1 run) | 0.14 (1 run) |
| S4 final (after cycle step) | 0.21 (1 run) | 0.29 (1 run) | 0.24 (1 run) | 6.0 (1 run) | 4.0 (1 run) | 68.0 (1 run) | 0.12 (1 run) | 0.17 (1 run) | 0.14 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.04 (1 run) | 0.03 (1 run) | 0.03 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 61.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 48.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.27 (1 run) | 0.37 (1 run) | 0.31 (1 run) | 7.0 (1 run) | 6.0 (1 run) | 63.0 (1 run) | 0.15 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S3 after KCI pruning | 0.27 (1 run) | 0.37 (1 run) | 0.31 (1 run) | 7.0 (1 run) | 6.0 (1 run) | 63.0 (1 run) | 0.15 (1 run) | 0.20 (1 run) | 0.17 (1 run) |
| S4 final (after cycle step) | 0.27 (1 run) | 0.37 (1 run) | 0.31 (1 run) | 7.0 (1 run) | 6.0 (1 run) | 63.0 (1 run) | 0.15 (1 run) | 0.20 (1 run) | 0.17 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 13 |
| data only | 7 |
| both | 0 |
| neither | 25 |

Direction among those: data: direction as in reference 3, data: reversed 4, labels: direction as in reference 7, labels: reversed 6.
Distinct edges: data only: indoor_time_above_safe_prop->observed_heat_calls, social_isolation_rate->admitted_visits_count, tree_canopy_pct->effective_cooled_hours, true_ems_heat_incidents->alerts_delivered_rate, true_ems_heat_incidents->effective_awareness_rate, true_ems_heat_incidents->neighborhood_heat_index, true_ems_heat_incidents->regional_heat_index_base; labels only: alerts_delivered_rate->effective_awareness_rate, attempted_trips_count->transit_vouchers_per_1000, effective_cooled_hours->adjusted_heat_dose_index, effective_cooled_hours->hours_open, functional_capacity_day->hours_open, indoor_time_above_safe_prop->adjusted_heat_dose_index, language_mismatch_rate->alerts_delivered_rate, neighborhood_heat_index->regional_heat_index_base, social_isolation_rate->effective_awareness_rate, tree_canopy_pct->neighborhood_heat_index, true_ems_heat_incidents->adjusted_heat_dose_index, true_ems_heat_incidents->observed_heat_calls, turnaways_count->functional_capacity_day; neither: adjusted_heat_dose_index->observed_heat_calls, admitted_visits_count->observed_heat_calls, alerts_delivered_rate->adjusted_heat_dose_index, alerts_delivered_rate->admitted_visits_count, alerts_delivered_rate->observed_heat_calls, effective_awareness_rate->observed_heat_calls, effective_cooled_hours->ac_ownership_rate, effective_cooled_hours->observed_heat_calls, indoor_time_above_safe_prop->admitted_visits_count, language_mismatch_rate->social_isolation_rate, neighborhood_heat_index->adjusted_heat_dose_index, neighborhood_heat_index->admitted_visits_count, neighborhood_heat_index->alerts_delivered_rate, neighborhood_heat_index->observed_heat_calls, outdoor_work_share->admitted_visits_count, power_outage_rate->ac_ownership_rate, power_outage_rate->observed_heat_calls, regional_heat_index_base->adjusted_heat_dose_index, regional_heat_index_base->observed_heat_calls, social_isolation_rate->alerts_delivered_rate, social_isolation_rate->observed_heat_calls, tree_canopy_pct->adjusted_heat_dose_index, tree_canopy_pct->regional_heat_index_base, true_ems_heat_incidents->admitted_visits_count, turnaways_count->hours_open.

## Arm `q081` (1 runs)

Family `s2_08`, role `real`. Column labels: baseline_salt_rejection, fouling_stock, membrane_age, osmotic_pressure_diff, cip_removal_fraction, concentration_polarization_index, true_permeate_salt, feed_salinity, antiscalant_effectiveness, intrinsic_permeability, achieved_recovery_ratio, assayed_sdi, recovery_ratio_target, required_tmp, specific_energy_consumption, feed_temperature, fouling_stock_prior, deposition_rate, observed_permeate_conductivity, daily_production_demand, achieved_permeate_flow_rate, pretreatment_fouling_potential. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 2, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 23 | 0 | 0 | 23 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 2, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 24.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 6.0 (1 run) | n/a | n/a |
| S2 after LLM review | 75.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 74.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 73.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 72, B 3, C 152, D 4.

**Final edges.** 73 distinct edges appear in at least one run; 73 appear in every run. Set by: llm 73. Per run: LLM-set edges 73.0 (1 run); final edges between pairs the algorithm did not connect 61.0 (1 run); LLM additions where at least 90% of resamples had no edge 55.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| baseline_salt_rejection->membrane_age | 1 |
| baseline_salt_rejection->true_permeate_salt | 1 |
| baseline_salt_rejection->observed_permeate_conductivity | 1 |
| fouling_stock->assayed_sdi | 1 |
| fouling_stock->specific_energy_consumption | 1 |
| fouling_stock->fouling_stock_prior | 1 |
| fouling_stock->deposition_rate | 1 |
| fouling_stock->pretreatment_fouling_potential | 1 |
| membrane_age->intrinsic_permeability | 1 |
| membrane_age->achieved_recovery_ratio | 1 |
| membrane_age->required_tmp | 1 |
| membrane_age->specific_energy_consumption | 1 |
| membrane_age->deposition_rate | 1 |
| membrane_age->observed_permeate_conductivity | 1 |
| membrane_age->achieved_permeate_flow_rate | 1 |
| osmotic_pressure_diff->concentration_polarization_index | 1 |
| osmotic_pressure_diff->achieved_recovery_ratio | 1 |
| osmotic_pressure_diff->observed_permeate_conductivity | 1 |
| osmotic_pressure_diff->achieved_permeate_flow_rate | 1 |
| cip_removal_fraction->achieved_recovery_ratio | 1 |
| cip_removal_fraction->observed_permeate_conductivity | 1 |
| cip_removal_fraction->achieved_permeate_flow_rate | 1 |
| concentration_polarization_index->achieved_recovery_ratio | 1 |
| concentration_polarization_index->specific_energy_consumption | 1 |
| concentration_polarization_index->deposition_rate | 1 |
| concentration_polarization_index->observed_permeate_conductivity | 1 |
| concentration_polarization_index->achieved_permeate_flow_rate | 1 |
| true_permeate_salt->feed_salinity | 1 |
| true_permeate_salt->observed_permeate_conductivity | 1 |
| feed_salinity->observed_permeate_conductivity | 1 |
| antiscalant_effectiveness->achieved_recovery_ratio | 1 |
| antiscalant_effectiveness->assayed_sdi | 1 |
| antiscalant_effectiveness->specific_energy_consumption | 1 |
| antiscalant_effectiveness->deposition_rate | 1 |
| antiscalant_effectiveness->observed_permeate_conductivity | 1 |
| antiscalant_effectiveness->achieved_permeate_flow_rate | 1 |
| antiscalant_effectiveness->pretreatment_fouling_potential | 1 |
| intrinsic_permeability->achieved_recovery_ratio | 1 |
| intrinsic_permeability->deposition_rate | 1 |
| intrinsic_permeability->observed_permeate_conductivity | 1 |
| intrinsic_permeability->achieved_permeate_flow_rate | 1 |
| achieved_recovery_ratio->recovery_ratio_target | 1 |
| deposition_rate->achieved_recovery_ratio | 1 |
| observed_permeate_conductivity->achieved_recovery_ratio | 1 |
| achieved_recovery_ratio->achieved_permeate_flow_rate | 1 |
| assayed_sdi->fouling_stock_prior | 1 |
| assayed_sdi->deposition_rate | 1 |
| assayed_sdi->observed_permeate_conductivity | 1 |
| assayed_sdi->pretreatment_fouling_potential | 1 |
| recovery_ratio_target->daily_production_demand | 1 |
| recovery_ratio_target->achieved_permeate_flow_rate | 1 |
| required_tmp->achieved_permeate_flow_rate | 1 |
| specific_energy_consumption->feed_temperature | 1 |
| specific_energy_consumption->fouling_stock_prior | 1 |
| specific_energy_consumption->deposition_rate | 1 |
| specific_energy_consumption->observed_permeate_conductivity | 1 |
| specific_energy_consumption->daily_production_demand | 1 |
| specific_energy_consumption->achieved_permeate_flow_rate | 1 |
| specific_energy_consumption->pretreatment_fouling_potential | 1 |
| feed_temperature->fouling_stock_prior | 1 |
| feed_temperature->deposition_rate | 1 |
| feed_temperature->observed_permeate_conductivity | 1 |
| feed_temperature->achieved_permeate_flow_rate | 1 |
| feed_temperature->pretreatment_fouling_potential | 1 |
| fouling_stock_prior->deposition_rate | 1 |
| fouling_stock_prior->observed_permeate_conductivity | 1 |
| fouling_stock_prior->achieved_permeate_flow_rate | 1 |
| fouling_stock_prior->pretreatment_fouling_potential | 1 |
| deposition_rate->observed_permeate_conductivity | 1 |
| deposition_rate->achieved_permeate_flow_rate | 1 |
| deposition_rate->pretreatment_fouling_potential | 1 |
| observed_permeate_conductivity->achieved_permeate_flow_rate | 1 |
| daily_production_demand->achieved_permeate_flow_rate | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.88 (1 run) | 0.53 (1 run) | 0.66 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 39.0 (1 run) | 0.80 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S1 after bootstrap edits | 0.83 (1 run) | 0.12 (1 run) | 0.22 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 38.0 (1 run) | 0.75 (1 run) | 0.07 (1 run) | 0.14 (1 run) |
| S2 after LLM review | 0.32 (1 run) | 0.60 (1 run) | 0.42 (1 run) | 7.0 (1 run) | 17.0 (1 run) | 86.0 (1 run) | 0.09 (1 run) | 0.17 (1 run) | 0.12 (1 run) |
| S3 after KCI pruning | 0.32 (1 run) | 0.60 (1 run) | 0.42 (1 run) | 7.0 (1 run) | 17.0 (1 run) | 85.0 (1 run) | 0.09 (1 run) | 0.17 (1 run) | 0.12 (1 run) |
| S4 final (after cycle step) | 0.33 (1 run) | 0.60 (1 run) | 0.42 (1 run) | 7.0 (1 run) | 17.0 (1 run) | 84.0 (1 run) | 0.10 (1 run) | 0.17 (1 run) | 0.12 (1 run) |

## Arm `q082` (1 runs)

Family `s2_08`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 22 | 0 | 0 | 22 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 23.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 10.0 (1 run) | n/a | n/a |
| S2 after LLM review | 10.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 10.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 10.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 2, B 3, D 226.

**Final edges.** 10 distinct edges appear in at least one run; 10 appear in every run. Set by: algorithm (unchanged) 8, llm 2. Per run: LLM-set edges 2.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V01 o-o V03 | 1 |
| V07->V04 | 1 |
| V08 o-> V04 | 1 |
| V05->V20 | 1 |
| V20->V06 | 1 |
| V12->V09 | 1 |
| V11 o-o V13 | 1 |
| V12->V22 | 1 |
| V16 <-> V22 | 1 |
| V20 o-o V21 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.83 (1 run) | 0.47 (1 run) | 0.60 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 41.0 (1 run) | 0.60 (1 run) | 0.07 (1 run) | 0.13 (1 run) |
| S1 after bootstrap edits | 0.80 (1 run) | 0.20 (1 run) | 0.32 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 39.0 (1 run) | 0.60 (1 run) | 0.07 (1 run) | 0.13 (1 run) |
| S2 after LLM review | 0.80 (1 run) | 0.20 (1 run) | 0.32 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 41.0 (1 run) | 0.20 (1 run) | 0.03 (1 run) | 0.04 (1 run) |
| S3 after KCI pruning | 0.80 (1 run) | 0.20 (1 run) | 0.32 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 41.0 (1 run) | 0.20 (1 run) | 0.03 (1 run) | 0.04 (1 run) |
| S4 final (after cycle step) | 0.80 (1 run) | 0.20 (1 run) | 0.32 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 41.0 (1 run) | 0.20 (1 run) | 0.03 (1 run) | 0.04 (1 run) |

## Arm `q083` (1 runs)

Family `s2_08`, role `swapped`. Column labels: fouling_stock, baseline_salt_rejection, osmotic_pressure_diff, membrane_age, concentration_polarization_index, cip_removal_fraction, feed_salinity, achieved_recovery_ratio, true_permeate_salt, antiscalant_effectiveness, assayed_sdi, intrinsic_permeability, required_tmp, recovery_ratio_target, feed_temperature, observed_permeate_conductivity, deposition_rate, fouling_stock_prior, daily_production_demand, pretreatment_fouling_potential, specific_energy_consumption, achieved_permeate_flow_rate. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 2, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 22 | 0 | 0 | 22 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 2, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 23.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 5.0 (1 run) | n/a | n/a |
| S2 after LLM review | 62.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 59.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 59.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 58, B 4, C 159, D 10.

**Final edges.** 59 distinct edges appear in at least one run; 59 appear in every run. Set by: llm 59. Per run: LLM-set edges 59.0 (1 run); final edges between pairs the algorithm did not connect 54.0 (1 run); LLM additions where at least 90% of resamples had no edge 52.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| fouling_stock->membrane_age | 1 |
| fouling_stock->deposition_rate | 1 |
| fouling_stock->fouling_stock_prior | 1 |
| baseline_salt_rejection->osmotic_pressure_diff | 1 |
| baseline_salt_rejection->feed_salinity | 1 |
| baseline_salt_rejection->observed_permeate_conductivity | 1 |
| osmotic_pressure_diff->concentration_polarization_index | 1 |
| osmotic_pressure_diff->feed_salinity | 1 |
| osmotic_pressure_diff->true_permeate_salt | 1 |
| osmotic_pressure_diff->observed_permeate_conductivity | 1 |
| osmotic_pressure_diff->specific_energy_consumption | 1 |
| osmotic_pressure_diff->achieved_permeate_flow_rate | 1 |
| membrane_age->deposition_rate | 1 |
| membrane_age->fouling_stock_prior | 1 |
| concentration_polarization_index->feed_salinity | 1 |
| concentration_polarization_index->achieved_recovery_ratio | 1 |
| concentration_polarization_index->true_permeate_salt | 1 |
| concentration_polarization_index->antiscalant_effectiveness | 1 |
| concentration_polarization_index->assayed_sdi | 1 |
| concentration_polarization_index->observed_permeate_conductivity | 1 |
| concentration_polarization_index->deposition_rate | 1 |
| concentration_polarization_index->pretreatment_fouling_potential | 1 |
| concentration_polarization_index->specific_energy_consumption | 1 |
| concentration_polarization_index->achieved_permeate_flow_rate | 1 |
| cip_removal_fraction->achieved_permeate_flow_rate | 1 |
| feed_salinity->true_permeate_salt | 1 |
| feed_salinity->observed_permeate_conductivity | 1 |
| achieved_recovery_ratio->true_permeate_salt | 1 |
| achieved_recovery_ratio->intrinsic_permeability | 1 |
| achieved_recovery_ratio->recovery_ratio_target | 1 |
| achieved_recovery_ratio->observed_permeate_conductivity | 1 |
| achieved_recovery_ratio->fouling_stock_prior | 1 |
| achieved_recovery_ratio->achieved_permeate_flow_rate | 1 |
| true_permeate_salt->intrinsic_permeability | 1 |
| true_permeate_salt->observed_permeate_conductivity | 1 |
| true_permeate_salt->achieved_permeate_flow_rate | 1 |
| antiscalant_effectiveness->observed_permeate_conductivity | 1 |
| antiscalant_effectiveness->deposition_rate | 1 |
| antiscalant_effectiveness->fouling_stock_prior | 1 |
| antiscalant_effectiveness->achieved_permeate_flow_rate | 1 |
| assayed_sdi->observed_permeate_conductivity | 1 |
| assayed_sdi->deposition_rate | 1 |
| assayed_sdi->fouling_stock_prior | 1 |
| assayed_sdi->pretreatment_fouling_potential | 1 |
| observed_permeate_conductivity->intrinsic_permeability | 1 |
| intrinsic_permeability->achieved_permeate_flow_rate | 1 |
| recovery_ratio_target->fouling_stock_prior | 1 |
| recovery_ratio_target->daily_production_demand | 1 |
| recovery_ratio_target->pretreatment_fouling_potential | 1 |
| recovery_ratio_target->achieved_permeate_flow_rate | 1 |
| feed_temperature->observed_permeate_conductivity | 1 |
| feed_temperature->specific_energy_consumption | 1 |
| feed_temperature->achieved_permeate_flow_rate | 1 |
| observed_permeate_conductivity->achieved_permeate_flow_rate | 1 |
| deposition_rate->fouling_stock_prior | 1 |
| deposition_rate->pretreatment_fouling_potential | 1 |
| fouling_stock_prior->achieved_permeate_flow_rate | 1 |
| daily_production_demand->achieved_permeate_flow_rate | 1 |
| specific_energy_consumption->achieved_permeate_flow_rate | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.83 (1 run) | 0.47 (1 run) | 0.60 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 41.0 (1 run) | 0.67 (1 run) | 0.10 (1 run) | 0.17 (1 run) |
| S1 after bootstrap edits | 0.80 (1 run) | 0.10 (1 run) | 0.18 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 38.0 (1 run) | 0.75 (1 run) | 0.07 (1 run) | 0.14 (1 run) |
| S2 after LLM review | 0.19 (1 run) | 0.30 (1 run) | 0.24 (1 run) | 6.0 (1 run) | 6.0 (1 run) | 84.0 (1 run) | 0.10 (1 run) | 0.15 (1 run) | 0.12 (1 run) |
| S3 after KCI pruning | 0.20 (1 run) | 0.30 (1 run) | 0.24 (1 run) | 6.0 (1 run) | 6.0 (1 run) | 81.0 (1 run) | 0.10 (1 run) | 0.15 (1 run) | 0.12 (1 run) |
| S4 final (after cycle step) | 0.20 (1 run) | 0.30 (1 run) | 0.24 (1 run) | 6.0 (1 run) | 6.0 (1 run) | 81.0 (1 run) | 0.10 (1 run) | 0.15 (1 run) | 0.12 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 63.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 45.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.31 (1 run) | 0.47 (1 run) | 0.37 (1 run) | 7.0 (1 run) | 12.0 (1 run) | 77.0 (1 run) | 0.11 (1 run) | 0.17 (1 run) | 0.14 (1 run) |
| S3 after KCI pruning | 0.29 (1 run) | 0.42 (1 run) | 0.34 (1 run) | 6.0 (1 run) | 11.0 (1 run) | 77.0 (1 run) | 0.10 (1 run) | 0.15 (1 run) | 0.12 (1 run) |
| S4 final (after cycle step) | 0.29 (1 run) | 0.42 (1 run) | 0.34 (1 run) | 6.0 (1 run) | 11.0 (1 run) | 77.0 (1 run) | 0.10 (1 run) | 0.15 (1 run) | 0.12 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 17 |
| data only | 12 |
| both | 0 |
| neither | 30 |

Direction among those: data: direction as in reference 6, data: reversed 6, labels: direction as in reference 6, labels: reversed 11.
Distinct edges: data only: achieved_recovery_ratio->achieved_permeate_flow_rate, achieved_recovery_ratio->fouling_stock_prior, achieved_recovery_ratio->true_permeate_salt, assayed_sdi->fouling_stock_prior, baseline_salt_rejection->feed_salinity, concentration_polarization_index->deposition_rate, concentration_polarization_index->pretreatment_fouling_potential, feed_temperature->specific_energy_consumption, fouling_stock_prior->achieved_permeate_flow_rate, intrinsic_permeability->achieved_permeate_flow_rate, observed_permeate_conductivity->achieved_permeate_flow_rate, true_permeate_salt->intrinsic_permeability; labels only: achieved_recovery_ratio->recovery_ratio_target, antiscalant_effectiveness->deposition_rate, assayed_sdi->pretreatment_fouling_potential, concentration_polarization_index->achieved_permeate_flow_rate, concentration_polarization_index->achieved_recovery_ratio, concentration_polarization_index->true_permeate_salt, daily_production_demand->achieved_permeate_flow_rate, deposition_rate->pretreatment_fouling_potential, feed_salinity->true_permeate_salt, feed_temperature->observed_permeate_conductivity, fouling_stock->deposition_rate, fouling_stock->fouling_stock_prior, osmotic_pressure_diff->concentration_polarization_index, osmotic_pressure_diff->feed_salinity, recovery_ratio_target->daily_production_demand, specific_energy_consumption->achieved_permeate_flow_rate, true_permeate_salt->observed_permeate_conductivity; neither: achieved_recovery_ratio->intrinsic_permeability, achieved_recovery_ratio->observed_permeate_conductivity, antiscalant_effectiveness->achieved_permeate_flow_rate, antiscalant_effectiveness->fouling_stock_prior, antiscalant_effectiveness->observed_permeate_conductivity, assayed_sdi->deposition_rate, assayed_sdi->observed_permeate_conductivity, baseline_salt_rejection->observed_permeate_conductivity, baseline_salt_rejection->osmotic_pressure_diff, cip_removal_fraction->achieved_permeate_flow_rate, concentration_polarization_index->antiscalant_effectiveness, concentration_polarization_index->assayed_sdi, concentration_polarization_index->feed_salinity, concentration_polarization_index->observed_permeate_conductivity, concentration_polarization_index->specific_energy_consumption, deposition_rate->fouling_stock_prior, feed_salinity->observed_permeate_conductivity, feed_temperature->achieved_permeate_flow_rate, fouling_stock->membrane_age, membrane_age->deposition_rate, membrane_age->fouling_stock_prior, observed_permeate_conductivity->intrinsic_permeability, osmotic_pressure_diff->achieved_permeate_flow_rate, osmotic_pressure_diff->observed_permeate_conductivity, osmotic_pressure_diff->specific_energy_consumption, osmotic_pressure_diff->true_permeate_salt, recovery_ratio_target->achieved_permeate_flow_rate, recovery_ratio_target->fouling_stock_prior, recovery_ratio_target->pretreatment_fouling_potential, true_permeate_salt->achieved_permeate_flow_rate.

## Arm `q091` (1 runs)

Family `s2_09`, role `real`. Column labels: patient_acuity_score, morning_HRV_rMSSD, actigraphy_wear_fraction, nurse_staffing_ratio, comfort_kit_adherence_index, arousal_threshold_index, perceived_lux_dose, comfort_bundle_offered, transfer_time_seconds, roommate_Lmax_spikes_count, cns_depressant_dose_index, planned_nursing_minutes, vital_sign_schedule_frequency, room_acoustic_reverberation_gain, perceived_noise_dose, nightly_alarm_count, night_lux_summary, alarm_quieting_bundle_state, alarm_related_LAeq, baseline_evening_pain_score, sleep_fragmentation_index, morning_pain_score. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 22 | 0 | 0 | 22 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 23.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 10.0 (1 run) | n/a | n/a |
| S2 after LLM review | 43.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 43.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 43.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 42, B 1, C 170, D 18.

**Final edges.** 43 distinct edges appear in at least one run; 43 appear in every run. Set by: llm 39, algorithm (unchanged) 4. Per run: LLM-set edges 39.0 (1 run); final edges between pairs the algorithm did not connect 30.0 (1 run); LLM additions where at least 90% of resamples had no edge 24.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| patient_acuity_score->nurse_staffing_ratio | 1 |
| patient_acuity_score->planned_nursing_minutes | 1 |
| patient_acuity_score->vital_sign_schedule_frequency | 1 |
| patient_acuity_score->nightly_alarm_count | 1 |
| nurse_staffing_ratio->planned_nursing_minutes | 1 |
| nurse_staffing_ratio->vital_sign_schedule_frequency | 1 |
| nurse_staffing_ratio->sleep_fragmentation_index | 1 |
| comfort_kit_adherence_index->comfort_bundle_offered | 1 |
| comfort_kit_adherence_index->planned_nursing_minutes | 1 |
| comfort_kit_adherence_index->perceived_noise_dose | 1 |
| comfort_kit_adherence_index->baseline_evening_pain_score | 1 |
| comfort_kit_adherence_index->sleep_fragmentation_index | 1 |
| comfort_kit_adherence_index->morning_pain_score | 1 |
| perceived_lux_dose->perceived_noise_dose | 1 |
| perceived_lux_dose->night_lux_summary | 1 |
| perceived_lux_dose->alarm_related_LAeq | 1 |
| perceived_lux_dose->sleep_fragmentation_index | 1 |
| comfort_bundle_offered->planned_nursing_minutes | 1 |
| comfort_bundle_offered->alarm_quieting_bundle_state | 1 |
| comfort_bundle_offered->baseline_evening_pain_score | 1 |
| comfort_bundle_offered->sleep_fragmentation_index | 1 |
| comfort_bundle_offered->morning_pain_score | 1 |
| roommate_Lmax_spikes_count->perceived_noise_dose | 1 |
| roommate_Lmax_spikes_count->alarm_related_LAeq | 1 |
| roommate_Lmax_spikes_count->sleep_fragmentation_index | 1 |
| cns_depressant_dose_index->baseline_evening_pain_score | 1 |
| cns_depressant_dose_index->sleep_fragmentation_index | 1 |
| cns_depressant_dose_index->morning_pain_score | 1 |
| room_acoustic_reverberation_gain->perceived_noise_dose | 1 |
| room_acoustic_reverberation_gain->alarm_related_LAeq | 1 |
| perceived_noise_dose->alarm_related_LAeq | 1 |
| perceived_noise_dose->sleep_fragmentation_index | 1 |
| alarm_quieting_bundle_state->nightly_alarm_count | 1 |
| nightly_alarm_count->alarm_related_LAeq | 1 |
| nightly_alarm_count->sleep_fragmentation_index | 1 |
| nightly_alarm_count->morning_pain_score | 1 |
| night_lux_summary->sleep_fragmentation_index | 1 |
| alarm_quieting_bundle_state->alarm_related_LAeq | 1 |
| alarm_quieting_bundle_state->sleep_fragmentation_index | 1 |
| alarm_related_LAeq->sleep_fragmentation_index | 1 |
| baseline_evening_pain_score->sleep_fragmentation_index | 1 |
| baseline_evening_pain_score->morning_pain_score | 1 |
| sleep_fragmentation_index->morning_pain_score | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.87 (1 run) | 0.57 (1 run) | 0.69 (1 run) | 8.0 (1 run) | 0.0 (1 run) | 30.0 (1 run) | 1.00 (1 run) | 0.23 (1 run) | 0.37 (1 run) |
| S1 after bootstrap edits | 0.90 (1 run) | 0.26 (1 run) | 0.40 (1 run) | 7.0 (1 run) | 0.0 (1 run) | 29.0 (1 run) | 1.00 (1 run) | 0.20 (1 run) | 0.33 (1 run) |
| S2 after LLM review | 0.42 (1 run) | 0.51 (1 run) | 0.46 (1 run) | 14.0 (1 run) | 4.0 (1 run) | 47.0 (1 run) | 0.33 (1 run) | 0.40 (1 run) | 0.36 (1 run) |
| S3 after KCI pruning | 0.42 (1 run) | 0.51 (1 run) | 0.46 (1 run) | 14.0 (1 run) | 4.0 (1 run) | 47.0 (1 run) | 0.33 (1 run) | 0.40 (1 run) | 0.36 (1 run) |
| S4 final (after cycle step) | 0.42 (1 run) | 0.51 (1 run) | 0.46 (1 run) | 14.0 (1 run) | 4.0 (1 run) | 47.0 (1 run) | 0.33 (1 run) | 0.40 (1 run) | 0.36 (1 run) |

## Arm `q092` (1 runs)

Family `s2_09`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 22 | 0 | 0 | 22 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 25.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 12.0 (1 run) | n/a | n/a |
| S2 after LLM review | 14.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 14.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 14.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 10, C 11, D 210.

**Final edges.** 14 distinct edges appear in at least one run; 14 appear in every run. Set by: algorithm (unchanged) 10, llm 4. Per run: LLM-set edges 4.0 (1 run); final edges between pairs the algorithm did not connect 2.0 (1 run); LLM additions where at least 90% of resamples had no edge 2.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V01->V11 | 1 |
| V01->V12 | 1 |
| V01->V16 | 1 |
| V21 o-> V02 | 1 |
| V03->V17 | 1 |
| V04 o-> V17 | 1 |
| V05->V15 | 1 |
| V05->V19 | 1 |
| V21 o-> V09 | 1 |
| V22 o-> V09 | 1 |
| V13->V17 | 1 |
| V15->V19 | 1 |
| V16->V19 | 1 |
| V17->V19 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.84 (1 run) | 0.60 (1 run) | 0.70 (1 run) | 7.0 (1 run) | 1.0 (1 run) | 32.0 (1 run) | 0.78 (1 run) | 0.20 (1 run) | 0.32 (1 run) |
| S1 after bootstrap edits | 0.83 (1 run) | 0.29 (1 run) | 0.43 (1 run) | 7.0 (1 run) | 0.0 (1 run) | 30.0 (1 run) | 0.88 (1 run) | 0.20 (1 run) | 0.33 (1 run) |
| S2 after LLM review | 0.71 (1 run) | 0.29 (1 run) | 0.41 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 33.0 (1 run) | 0.60 (1 run) | 0.17 (1 run) | 0.27 (1 run) |
| S3 after KCI pruning | 0.71 (1 run) | 0.29 (1 run) | 0.41 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 33.0 (1 run) | 0.60 (1 run) | 0.17 (1 run) | 0.27 (1 run) |
| S4 final (after cycle step) | 0.71 (1 run) | 0.29 (1 run) | 0.41 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 33.0 (1 run) | 0.60 (1 run) | 0.17 (1 run) | 0.27 (1 run) |

## Arm `q093` (1 runs)

Family `s2_09`, role `swapped`. Column labels: morning_HRV_rMSSD, patient_acuity_score, nurse_staffing_ratio, actigraphy_wear_fraction, arousal_threshold_index, comfort_kit_adherence_index, comfort_bundle_offered, perceived_lux_dose, roommate_Lmax_spikes_count, transfer_time_seconds, planned_nursing_minutes, cns_depressant_dose_index, room_acoustic_reverberation_gain, vital_sign_schedule_frequency, nightly_alarm_count, baseline_evening_pain_score, perceived_noise_dose, night_lux_summary, sleep_fragmentation_index, alarm_quieting_bundle_state, morning_pain_score, alarm_related_LAeq. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 22 | 0 | 0 | 22 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 25.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 15.0 (1 run) | n/a | n/a |
| S2 after LLM review | 46.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 45.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 45.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 45, B 1, C 183, D 2.

**Final edges.** 45 distinct edges appear in at least one run; 45 appear in every run. Set by: llm 39, algorithm (unchanged) 6. Per run: LLM-set edges 39.0 (1 run); final edges between pairs the algorithm did not connect 35.0 (1 run); LLM additions where at least 90% of resamples had no edge 36.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| morning_HRV_rMSSD->arousal_threshold_index | 1 |
| morning_HRV_rMSSD->cns_depressant_dose_index | 1 |
| morning_HRV_rMSSD->baseline_evening_pain_score | 1 |
| morning_HRV_rMSSD->sleep_fragmentation_index | 1 |
| morning_HRV_rMSSD->morning_pain_score | 1 |
| patient_acuity_score->nurse_staffing_ratio | 1 |
| patient_acuity_score->arousal_threshold_index | 1 |
| patient_acuity_score->planned_nursing_minutes | 1 |
| patient_acuity_score->cns_depressant_dose_index | 1 |
| patient_acuity_score->vital_sign_schedule_frequency | 1 |
| patient_acuity_score->nightly_alarm_count | 1 |
| patient_acuity_score->baseline_evening_pain_score | 1 |
| patient_acuity_score->sleep_fragmentation_index | 1 |
| patient_acuity_score->morning_pain_score | 1 |
| nurse_staffing_ratio->planned_nursing_minutes | 1 |
| arousal_threshold_index->nightly_alarm_count | 1 |
| arousal_threshold_index->sleep_fragmentation_index | 1 |
| comfort_kit_adherence_index->comfort_bundle_offered | 1 |
| comfort_kit_adherence_index->alarm_quieting_bundle_state | 1 |
| comfort_bundle_offered->alarm_quieting_bundle_state | 1 |
| roommate_Lmax_spikes_count->nightly_alarm_count | 1 |
| roommate_Lmax_spikes_count->perceived_noise_dose | 1 |
| roommate_Lmax_spikes_count->sleep_fragmentation_index | 1 |
| roommate_Lmax_spikes_count->alarm_related_LAeq | 1 |
| planned_nursing_minutes->vital_sign_schedule_frequency | 1 |
| planned_nursing_minutes->baseline_evening_pain_score | 1 |
| planned_nursing_minutes->sleep_fragmentation_index | 1 |
| planned_nursing_minutes->morning_pain_score | 1 |
| cns_depressant_dose_index->sleep_fragmentation_index | 1 |
| room_acoustic_reverberation_gain->nightly_alarm_count | 1 |
| room_acoustic_reverberation_gain->perceived_noise_dose | 1 |
| room_acoustic_reverberation_gain->sleep_fragmentation_index | 1 |
| room_acoustic_reverberation_gain->alarm_related_LAeq | 1 |
| nightly_alarm_count->perceived_noise_dose | 1 |
| nightly_alarm_count->sleep_fragmentation_index | 1 |
| nightly_alarm_count->alarm_related_LAeq | 1 |
| baseline_evening_pain_score->sleep_fragmentation_index | 1 |
| baseline_evening_pain_score->morning_pain_score | 1 |
| perceived_noise_dose->sleep_fragmentation_index | 1 |
| perceived_noise_dose->morning_pain_score | 1 |
| perceived_noise_dose->alarm_related_LAeq | 1 |
| night_lux_summary->sleep_fragmentation_index | 1 |
| sleep_fragmentation_index->morning_pain_score | 1 |
| sleep_fragmentation_index->alarm_related_LAeq | 1 |
| alarm_quieting_bundle_state->morning_pain_score | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.84 (1 run) | 0.60 (1 run) | 0.70 (1 run) | 8.0 (1 run) | 1.0 (1 run) | 31.0 (1 run) | 0.80 (1 run) | 0.23 (1 run) | 0.36 (1 run) |
| S1 after bootstrap edits | 0.87 (1 run) | 0.37 (1 run) | 0.52 (1 run) | 8.0 (1 run) | 1.0 (1 run) | 29.0 (1 run) | 0.80 (1 run) | 0.23 (1 run) | 0.36 (1 run) |
| S2 after LLM review | 0.22 (1 run) | 0.29 (1 run) | 0.25 (1 run) | 5.0 (1 run) | 5.0 (1 run) | 66.0 (1 run) | 0.11 (1 run) | 0.14 (1 run) | 0.12 (1 run) |
| S3 after KCI pruning | 0.20 (1 run) | 0.26 (1 run) | 0.23 (1 run) | 5.0 (1 run) | 4.0 (1 run) | 66.0 (1 run) | 0.11 (1 run) | 0.14 (1 run) | 0.12 (1 run) |
| S4 final (after cycle step) | 0.20 (1 run) | 0.26 (1 run) | 0.23 (1 run) | 5.0 (1 run) | 4.0 (1 run) | 66.0 (1 run) | 0.11 (1 run) | 0.14 (1 run) | 0.12 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.04 (1 run) | 0.03 (1 run) | 0.03 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 59.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 50.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.39 (1 run) | 0.51 (1 run) | 0.44 (1 run) | 14.0 (1 run) | 4.0 (1 run) | 50.0 (1 run) | 0.30 (1 run) | 0.40 (1 run) | 0.35 (1 run) |
| S3 after KCI pruning | 0.40 (1 run) | 0.51 (1 run) | 0.45 (1 run) | 14.0 (1 run) | 4.0 (1 run) | 49.0 (1 run) | 0.31 (1 run) | 0.40 (1 run) | 0.35 (1 run) |
| S4 final (after cycle step) | 0.40 (1 run) | 0.51 (1 run) | 0.45 (1 run) | 14.0 (1 run) | 4.0 (1 run) | 49.0 (1 run) | 0.31 (1 run) | 0.40 (1 run) | 0.35 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 18 |
| data only | 3 |
| both | 0 |
| neither | 18 |

Direction among those: data: reversed 3, labels: direction as in reference 14, labels: reversed 4.
Distinct edges: data only: nightly_alarm_count->sleep_fragmentation_index, patient_acuity_score->morning_pain_score, roommate_Lmax_spikes_count->alarm_related_LAeq; labels only: arousal_threshold_index->sleep_fragmentation_index, baseline_evening_pain_score->morning_pain_score, comfort_kit_adherence_index->comfort_bundle_offered, morning_HRV_rMSSD->morning_pain_score, morning_HRV_rMSSD->sleep_fragmentation_index, nightly_alarm_count->alarm_related_LAeq, nightly_alarm_count->perceived_noise_dose, nurse_staffing_ratio->planned_nursing_minutes, patient_acuity_score->cns_depressant_dose_index, patient_acuity_score->nightly_alarm_count, patient_acuity_score->planned_nursing_minutes, patient_acuity_score->vital_sign_schedule_frequency, perceived_noise_dose->alarm_related_LAeq, perceived_noise_dose->sleep_fragmentation_index, room_acoustic_reverberation_gain->alarm_related_LAeq, room_acoustic_reverberation_gain->nightly_alarm_count, roommate_Lmax_spikes_count->perceived_noise_dose, sleep_fragmentation_index->morning_pain_score; neither: alarm_quieting_bundle_state->morning_pain_score, cns_depressant_dose_index->sleep_fragmentation_index, comfort_bundle_offered->alarm_quieting_bundle_state, morning_HRV_rMSSD->arousal_threshold_index, night_lux_summary->sleep_fragmentation_index, patient_acuity_score->arousal_threshold_index, patient_acuity_score->baseline_evening_pain_score, patient_acuity_score->nurse_staffing_ratio, patient_acuity_score->sleep_fragmentation_index, perceived_noise_dose->morning_pain_score, planned_nursing_minutes->baseline_evening_pain_score, planned_nursing_minutes->morning_pain_score, planned_nursing_minutes->sleep_fragmentation_index, planned_nursing_minutes->vital_sign_schedule_frequency, room_acoustic_reverberation_gain->sleep_fragmentation_index, roommate_Lmax_spikes_count->nightly_alarm_count, roommate_Lmax_spikes_count->sleep_fragmentation_index, sleep_fragmentation_index->alarm_related_LAeq.

## Arm `q102` (1 runs)

Family `s2_10`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 4, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 20.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 9.0 (1 run) | n/a | n/a |
| S2 after LLM review | 10.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 10.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 10.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 3, B 2, D 295.

**Final edges.** 10 distinct edges appear in at least one run; 10 appear in every run. Set by: algorithm (unchanged) 9, llm 1. Per run: LLM-set edges 1.0 (1 run); final edges between pairs the algorithm did not connect 1.0 (1 run); LLM additions where at least 90% of resamples had no edge 1.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V02 o-o V14 | 1 |
| V02->V24 | 1 |
| V04 o-o V20 | 1 |
| V05->V19 | 1 |
| V07->V06 | 1 |
| V11->V06 | 1 |
| V20->V07 | 1 |
| V14->V11 | 1 |
| V16 o-o V20 | 1 |
| V23->V24 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.75 (1 run) | 0.33 (1 run) | 0.46 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 45.0 (1 run) | 0.75 (1 run) | 0.13 (1 run) | 0.23 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.20 (1 run) | 0.33 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 40.0 (1 run) | 0.83 (1 run) | 0.11 (1 run) | 0.20 (1 run) |
| S2 after LLM review | 0.90 (1 run) | 0.20 (1 run) | 0.33 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.71 (1 run) | 0.11 (1 run) | 0.19 (1 run) |
| S3 after KCI pruning | 0.90 (1 run) | 0.20 (1 run) | 0.33 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.71 (1 run) | 0.11 (1 run) | 0.19 (1 run) |
| S4 final (after cycle step) | 0.90 (1 run) | 0.20 (1 run) | 0.33 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.71 (1 run) | 0.11 (1 run) | 0.19 (1 run) |

## Arm `q103` (1 runs)

Family `s2_10`, role `swapped`. Column labels: v_review_staff, v_zoning_far, v_station_open, v_noise_complaints, v_platform_adoption, v_rent_true, v_permits_posted_obs, v_job_access_45m, v_permit_apps_true, v_noise_barrier, v_construction_cost_idx, v_walk_time_min, v_listing_coverage, v_measured_noise_dba, v_interest_rate_ann, v_vacancy_rate, v_spatial_spillover_idx, v_asking_rent_obs, v_true_noise_dba, v_permit_backlog, v_service_freq_tph, v_permit_approvals_true, v_season_regime, v_school_quality_score, v_reporting_delay_days. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 2, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-mini-2024-07-18.

**Same question, same answer?** A request is "the same" when the full prompt and settings are identical after masking timestamps.

| Stage | Distinct requests | Asked in 2+ runs | of which answered identically | Asked in every run |
|---|---|---|---|---|
| 01_init_query_parse | 1 | 0 | 0 | 1 |
| 04b_knowledge | 2 | 0 | 0 | 2 |
| 06a_filter | 1 | 0 | 0 | 1 |
| 06b_rerank | 1 | 0 | 0 | 1 |
| 06c_hyperparameters | 1 | 0 | 0 | 1 |
| 07b_refinement | 25 | 0 | 0 | 25 |
| 08a_report_graph_text | 1 | 0 | 0 | 1 |
| 08b_report | 5 | 0 | 0 | 5 |
| 09_discussion_init | 1 | 0 | 0 | 1 |

First stage at which two runs stop sending identical requests (one count per pair of runs): n/a (one run).

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: FCI {"alpha": 0.05, "depth": 2, "indep_test": "rcit"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 21.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 12.0 (1 run) | n/a | n/a |
| S2 after LLM review | 56.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 55.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 55.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 54, B 1, C 231, D 14.

**Final edges.** 55 distinct edges appear in at least one run; 55 appear in every run. Set by: llm 52, algorithm (unchanged) 3. Per run: LLM-set edges 52.0 (1 run); final edges between pairs the algorithm did not connect 47.0 (1 run); LLM additions where at least 90% of resamples had no edge 42.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| v_review_staff->v_permits_posted_obs | 1 |
| v_review_staff->v_permit_apps_true | 1 |
| v_review_staff->v_permit_backlog | 1 |
| v_review_staff->v_permit_approvals_true | 1 |
| v_zoning_far->v_rent_true | 1 |
| v_zoning_far->v_permits_posted_obs | 1 |
| v_zoning_far->v_permit_apps_true | 1 |
| v_zoning_far->v_construction_cost_idx | 1 |
| v_zoning_far->v_listing_coverage | 1 |
| v_zoning_far->v_vacancy_rate | 1 |
| v_zoning_far->v_asking_rent_obs | 1 |
| v_zoning_far->v_permit_backlog | 1 |
| v_zoning_far->v_permit_approvals_true | 1 |
| v_station_open->v_rent_true | 1 |
| v_station_open->v_job_access_45m | 1 |
| v_station_open->v_asking_rent_obs | 1 |
| v_station_open->v_service_freq_tph | 1 |
| v_noise_complaints->v_noise_barrier | 1 |
| v_noise_complaints->v_measured_noise_dba | 1 |
| v_noise_complaints->v_true_noise_dba | 1 |
| v_noise_complaints->v_permit_backlog | 1 |
| v_platform_adoption->v_job_access_45m | 1 |
| v_platform_adoption->v_service_freq_tph | 1 |
| v_rent_true->v_construction_cost_idx | 1 |
| v_measured_noise_dba->v_rent_true | 1 |
| v_rent_true->v_interest_rate_ann | 1 |
| v_rent_true->v_vacancy_rate | 1 |
| v_rent_true->v_asking_rent_obs | 1 |
| v_permits_posted_obs->v_permit_apps_true | 1 |
| v_permits_posted_obs->v_permit_backlog | 1 |
| v_permits_posted_obs->v_permit_approvals_true | 1 |
| v_job_access_45m->v_vacancy_rate | 1 |
| v_job_access_45m->v_asking_rent_obs | 1 |
| v_job_access_45m->v_service_freq_tph | 1 |
| v_permit_apps_true->v_permit_backlog | 1 |
| v_permit_apps_true->v_permit_approvals_true | 1 |
| v_noise_barrier->v_measured_noise_dba | 1 |
| v_noise_barrier->v_true_noise_dba | 1 |
| v_construction_cost_idx->v_vacancy_rate | 1 |
| v_construction_cost_idx->v_asking_rent_obs | 1 |
| v_construction_cost_idx->v_permit_backlog | 1 |
| v_construction_cost_idx->v_permit_approvals_true | 1 |
| v_listing_coverage->v_vacancy_rate | 1 |
| v_listing_coverage->v_asking_rent_obs | 1 |
| v_measured_noise_dba->v_vacancy_rate | 1 |
| v_measured_noise_dba->v_asking_rent_obs | 1 |
| v_measured_noise_dba->v_true_noise_dba | 1 |
| v_interest_rate_ann->v_vacancy_rate | 1 |
| v_interest_rate_ann->v_asking_rent_obs | 1 |
| v_vacancy_rate->v_asking_rent_obs | 1 |
| v_vacancy_rate->v_permit_backlog | 1 |
| v_spatial_spillover_idx->v_asking_rent_obs | 1 |
| v_asking_rent_obs->v_school_quality_score | 1 |
| v_permit_backlog->v_permit_approvals_true | 1 |
| v_season_regime->v_school_quality_score | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.76 (1 run) | 0.36 (1 run) | 0.48 (1 run) | 3.0 (1 run) | 2.0 (1 run) | 48.0 (1 run) | 0.50 (1 run) | 0.07 (1 run) | 0.12 (1 run) |
| S1 after bootstrap edits | 0.92 (1 run) | 0.24 (1 run) | 0.39 (1 run) | 3.0 (1 run) | 2.0 (1 run) | 44.0 (1 run) | 0.50 (1 run) | 0.07 (1 run) | 0.12 (1 run) |
| S2 after LLM review | 0.18 (1 run) | 0.22 (1 run) | 0.20 (1 run) | 8.0 (1 run) | 2.0 (1 run) | 84.0 (1 run) | 0.14 (1 run) | 0.18 (1 run) | 0.16 (1 run) |
| S3 after KCI pruning | 0.18 (1 run) | 0.22 (1 run) | 0.20 (1 run) | 8.0 (1 run) | 2.0 (1 run) | 83.0 (1 run) | 0.15 (1 run) | 0.18 (1 run) | 0.16 (1 run) |
| S4 final (after cycle step) | 0.18 (1 run) | 0.22 (1 run) | 0.20 (1 run) | 8.0 (1 run) | 2.0 (1 run) | 83.0 (1 run) | 0.15 (1 run) | 0.18 (1 run) | 0.16 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.10 (1 run) | 0.04 (1 run) | 0.06 (1 run) | 0.0 (1 run) | 1.0 (1 run) | 64.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.08 (1 run) | 0.02 (1 run) | 0.04 (1 run) | 0.0 (1 run) | 1.0 (1 run) | 56.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.34 (1 run) | 0.42 (1 run) | 0.38 (1 run) | 13.0 (1 run) | 6.0 (1 run) | 69.0 (1 run) | 0.23 (1 run) | 0.29 (1 run) | 0.26 (1 run) |
| S3 after KCI pruning | 0.33 (1 run) | 0.40 (1 run) | 0.36 (1 run) | 12.0 (1 run) | 6.0 (1 run) | 70.0 (1 run) | 0.22 (1 run) | 0.27 (1 run) | 0.24 (1 run) |
| S4 final (after cycle step) | 0.33 (1 run) | 0.40 (1 run) | 0.36 (1 run) | 12.0 (1 run) | 6.0 (1 run) | 70.0 (1 run) | 0.22 (1 run) | 0.27 (1 run) | 0.24 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 17 |
| data only | 8 |
| both | 0 |
| neither | 27 |

Direction among those: data: direction as in reference 6, data: reversed 2, labels: direction as in reference 12, labels: reversed 5.
Distinct edges: data only: v_interest_rate_ann->v_asking_rent_obs, v_interest_rate_ann->v_vacancy_rate, v_measured_noise_dba->v_vacancy_rate, v_noise_complaints->v_permit_backlog, v_permits_posted_obs->v_permit_backlog, v_rent_true->v_construction_cost_idx, v_vacancy_rate->v_permit_backlog, v_zoning_far->v_permit_approvals_true; labels only: v_job_access_45m->v_service_freq_tph, v_listing_coverage->v_asking_rent_obs, v_listing_coverage->v_vacancy_rate, v_noise_barrier->v_true_noise_dba, v_noise_complaints->v_true_noise_dba, v_permit_apps_true->v_permit_backlog, v_permit_backlog->v_permit_approvals_true, v_permits_posted_obs->v_permit_approvals_true, v_rent_true->v_asking_rent_obs, v_rent_true->v_interest_rate_ann, v_rent_true->v_vacancy_rate, v_review_staff->v_permit_approvals_true, v_review_staff->v_permit_backlog, v_station_open->v_job_access_45m, v_station_open->v_service_freq_tph, v_vacancy_rate->v_asking_rent_obs, v_zoning_far->v_permit_apps_true; neither: v_asking_rent_obs->v_school_quality_score, v_construction_cost_idx->v_asking_rent_obs, v_construction_cost_idx->v_permit_approvals_true, v_construction_cost_idx->v_permit_backlog, v_construction_cost_idx->v_vacancy_rate, v_job_access_45m->v_asking_rent_obs, v_job_access_45m->v_vacancy_rate, v_measured_noise_dba->v_asking_rent_obs, v_noise_barrier->v_measured_noise_dba, v_noise_complaints->v_measured_noise_dba, v_noise_complaints->v_noise_barrier, v_permit_apps_true->v_permit_approvals_true, v_permits_posted_obs->v_permit_apps_true, v_platform_adoption->v_job_access_45m, v_platform_adoption->v_service_freq_tph, v_review_staff->v_permit_apps_true, v_review_staff->v_permits_posted_obs, v_spatial_spillover_idx->v_asking_rent_obs, v_station_open->v_asking_rent_obs, v_station_open->v_rent_true, v_zoning_far->v_asking_rent_obs, v_zoning_far->v_construction_cost_idx, v_zoning_far->v_listing_coverage, v_zoning_far->v_permit_backlog, v_zoning_far->v_permits_posted_obs, v_zoning_far->v_rent_true, v_zoning_far->v_vacancy_rate.

## Predictions fixed before the data

- **N1**: {"what": "swapped arms, distinct (family, edge): LLM-set final edges adjacent in exactly one reference", "labels_only": 141, "data_only": 57, "neither": 225, "share_following_labels": 0.7121212121212122, "verdict": "INCONCLUSIVE"}
- **N2**: {"what": "mean LLM-set final edges per run, neutral names at most half of real names, per family", "families": {"s2_01": {"real": 37, "neutral": 3, "holds": true}, "s2_02": {"real": 36, "neutral": 2, "holds": true}, "s2_03": {"real": 37, "neutral": 0, "holds": true}, "s2_05": {"real": 45, "neutral": 0, "holds": true}, "s2_06": {"real": 35, "neutral": 9, "holds": true}, "s2_08": {"real": 73, "neutral": 2, "holds": true}, "s2_09": {"real": 39, "neutral": 4, "holds": true}}, "testable_families": 7, "held_in": 7, "verdict": "SUPPORTED"}
- **N4**: {"what": "runs whose final graph has lower adjacency F1 than the algorithm's own output", "runs": 27, "below": 26, "share": 0.9629629629629629, "verdict": "SUPPORTED"}
- **N5**: {"what": "exploratory: mean F1 by role over all runs, scored against the data-side reference or ground truth", "by_role": {"real": {"runs": 7, "directed_edge_f1_algorithm_output": 0.21987557464733626, "directed_edge_f1_final": 0.1851676542459173, "adjacency_f1_algorithm_output": 0.576370658080075, "adjacency_f1_final": 0.37846959248749124}, "neutral": {"runs": 10, "directed_edge_f1_algorithm_output": 0.1795316527928225, "directed_edge_f1_final": 0.14389830016239002, "adjacency_f1_algorithm_output": 0.5862208896822617, "adjacency_f1_final": 0.2959907346447318}, "swapped": {"runs": 10, "directed_edge_f1_algorithm_output": 0.20524239216373705, "directed_edge_f1_final": 0.11428229431783887, "adjacency_f1_algorithm_output": 0.5840165132305238, "adjacency_f1_final": 0.18378966437057465}}, "verdict": "exploratory"}
- **P3**: {"distinct_outputs_counted": 27, "nondirected_edges_in_algorithm_output": 458, "of_which_still_adjacent_after_bootstrap_step": 89, "share": 0.1943231441048035, "directed_edges": 175, "directed_still_adjacent": 142, "verdict": "SUPPORTED"}
- **P5**: {"arms": 27, "arms_with_more_than_one_algorithm": 0, "verdict": "exploratory"}

## Gates

- T1_no_arm_left_empty: **FAIL**
- T2_min_runs_per_arm: **PASS**
- T3_same_dataset_bytes: **PASS**
- T4_variable_names_match_arm: **PASS**
- T5_scores_recomputed_equal_lineage: **PASS**
- T6_one_model_snapshot_per_arm (report only): **PASS**
