# Stability and name-versus-data report

Label `s2`. Runs directory `runs`. 24 runs included in 24 arms; 6 excluded.

## Excluded runs

| Run | Arm | Reason |
|---|---|---|
| 20261011T184856Z_s2_q011_r01_b3a03d | q011 | status FAILED |
| 20261011T201633Z_s2_q033_r01_e378d3 | q033 | status FAILED |
| 20261011T203658Z_s2_q041_r01_2c4a4c | q041 | status FAILED |
| 20261011T210452Z_s2_q051_r01_564d72 | q051 | status FAILED |
| 20261011T220644Z_s2_q071_r01_582c9e | q071 | status FAILED |
| 20261011T234632Z_s2_q101_r01_b577f3 | q101 | status FAILED |

## Arm `q012` (1 runs)

Family `s2_01`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 28.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 11.0 (1 run) | n/a | n/a |
| S2 after LLM review | 11.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 11.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 11.0 (1 run) | n/a | n/a |

**LLM review decisions.** 253 pairs. Same decision in every run: 253. Same edge/no-edge call in every run: 253. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 253.

**Final edges.** 11 distinct edges appear in at least one run; 11 appear in every run. Set by: algorithm (unchanged) 11. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V01 o-> V04 | 1 |
| V03 ~~~ V16 | 1 |
| V08->V05 | 1 |
| V07->V10 | 1 |
| V08 o-o V19 | 1 |
| V08->V20 | 1 |
| V15->V10 | 1 |
| V19->V10 | 1 |
| V13->V12 | 1 |
| V13 o-o V22 | 1 |
| V16 o-> V20 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.79 (1 run) | 0.56 (1 run) | 0.66 (1 run) | 4.0 (1 run) | 2.0 (1 run) | 41.0 (1 run) | 0.67 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.28 (1 run) | 0.44 (1 run) | 4.0 (1 run) | 2.0 (1 run) | 35.0 (1 run) | 0.67 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S2 after LLM review | 1.00 (1 run) | 0.28 (1 run) | 0.44 (1 run) | 4.0 (1 run) | 2.0 (1 run) | 35.0 (1 run) | 0.67 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S3 after KCI pruning | 1.00 (1 run) | 0.28 (1 run) | 0.44 (1 run) | 4.0 (1 run) | 2.0 (1 run) | 35.0 (1 run) | 0.67 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S4 final (after cycle step) | 1.00 (1 run) | 0.28 (1 run) | 0.44 (1 run) | 4.0 (1 run) | 2.0 (1 run) | 35.0 (1 run) | 0.67 (1 run) | 0.10 (1 run) | 0.18 (1 run) |

## Arm `q013` (1 runs)

Family `s2_01`, role `swapped`. Column labels: oven_leak_index, component_thermal_mass_index, realized_ramp_rate_C_per_s, measured_void_fraction, oxygen_ppm, TAL_s, microstructure_index, flux_lot_activity_index, cooling_rate_C_per_s, paste_solvent_mass_fraction, nitrogen_flow_setpoint_slpm, pad_finish, volatile_generation_cumulative_mg, wetting_index, true_void_fraction, package_family_code, realized_peak_temp_C, conv_speed_cm_min, peak_zone_setpoint_C, residual_entrained_gas_mg, electrical_resistance_mOhm, preheat_soak_setpoint_C, paste_batch_context. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S1 after bootstrap edits | 10.0 (1 run) | n/a | n/a |
| S2 after LLM review | 21.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 18.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 18.0 (1 run) | n/a | n/a |

**LLM review decisions.** 253 pairs. Same decision in every run: 253. Same edge/no-edge call in every run: 253. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 12, B 3, C 58, D 180.

**Final edges.** 18 distinct edges appear in at least one run; 18 appear in every run. Set by: llm 9, algorithm (unchanged) 9. Per run: LLM-set edges 9.0 (1 run); final edges between pairs the algorithm did not connect 8.0 (1 run); LLM additions where at least 90% of resamples had no edge 11.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| oven_leak_index->cooling_rate_C_per_s | 1 |
| oven_leak_index->realized_peak_temp_C | 1 |
| oven_leak_index->conv_speed_cm_min | 1 |
| component_thermal_mass_index->realized_ramp_rate_C_per_s | 1 |
| component_thermal_mass_index->cooling_rate_C_per_s | 1 |
| realized_ramp_rate_C_per_s ~~~ package_family_code | 1 |
| measured_void_fraction->true_void_fraction | 1 |
| flux_lot_activity_index o-> oxygen_ppm | 1 |
| flux_lot_activity_index->residual_entrained_gas_mg | 1 |
| paste_solvent_mass_fraction->volatile_generation_cumulative_mg | 1 |
| paste_solvent_mass_fraction->wetting_index | 1 |
| paste_solvent_mass_fraction->true_void_fraction | 1 |
| peak_zone_setpoint_C->paste_solvent_mass_fraction | 1 |
| pad_finish <-> volatile_generation_cumulative_mg | 1 |
| volatile_generation_cumulative_mg->preheat_soak_setpoint_C | 1 |
| true_void_fraction->package_family_code | 1 |
| realized_peak_temp_C->conv_speed_cm_min | 1 |
| peak_zone_setpoint_C->electrical_resistance_mOhm | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.81 (1 run) | 0.54 (1 run) | 0.65 (1 run) | 6.0 (1 run) | 2.0 (1 run) | 40.0 (1 run) | 0.60 (1 run) | 0.15 (1 run) | 0.24 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.26 (1 run) | 0.41 (1 run) | 5.0 (1 run) | 2.0 (1 run) | 35.0 (1 run) | 0.71 (1 run) | 0.13 (1 run) | 0.22 (1 run) |
| S2 after LLM review | 0.52 (1 run) | 0.28 (1 run) | 0.37 (1 run) | 4.0 (1 run) | 4.0 (1 run) | 45.0 (1 run) | 0.22 (1 run) | 0.10 (1 run) | 0.14 (1 run) |
| S3 after KCI pruning | 0.61 (1 run) | 0.28 (1 run) | 0.39 (1 run) | 4.0 (1 run) | 4.0 (1 run) | 42.0 (1 run) | 0.27 (1 run) | 0.10 (1 run) | 0.15 (1 run) |
| S4 final (after cycle step) | 0.61 (1 run) | 0.28 (1 run) | 0.39 (1 run) | 4.0 (1 run) | 4.0 (1 run) | 42.0 (1 run) | 0.27 (1 run) | 0.10 (1 run) | 0.15 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.12 (1 run) | 0.08 (1 run) | 0.09 (1 run) | 0.0 (1 run) | 1.0 (1 run) | 62.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 49.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.24 (1 run) | 0.13 (1 run) | 0.17 (1 run) | 4.0 (1 run) | 1.0 (1 run) | 51.0 (1 run) | 0.22 (1 run) | 0.10 (1 run) | 0.14 (1 run) |
| S3 after KCI pruning | 0.17 (1 run) | 0.08 (1 run) | 0.11 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 52.0 (1 run) | 0.13 (1 run) | 0.05 (1 run) | 0.07 (1 run) |
| S4 final (after cycle step) | 0.17 (1 run) | 0.08 (1 run) | 0.11 (1 run) | 2.0 (1 run) | 1.0 (1 run) | 52.0 (1 run) | 0.13 (1 run) | 0.05 (1 run) | 0.07 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 3 |
| data only | 2 |
| both | 0 |
| neither | 4 |

Direction among those: data: reversed 2, labels: direction as in reference 2, labels: reversed 1.
Distinct edges: data only: paste_solvent_mass_fraction->wetting_index, volatile_generation_cumulative_mg->preheat_soak_setpoint_C; labels only: component_thermal_mass_index->realized_ramp_rate_C_per_s, measured_void_fraction->true_void_fraction, paste_solvent_mass_fraction->volatile_generation_cumulative_mg; neither: component_thermal_mass_index->cooling_rate_C_per_s, oven_leak_index->cooling_rate_C_per_s, oven_leak_index->realized_peak_temp_C, realized_peak_temp_C->conv_speed_cm_min.

## Arm `q021` (1 runs)

Family `s2_02`, role `real`. Column labels: V16_unsafe_crossing_true, V17_observed_unsafe_label, V14_focal_walking_speed_mps, V23_abandonment_indicator, V9_group_size_at_decision, V8_visible_remaining_seconds, V24_start_decision_now, V1_countdown_policy_enabled, V11_time_pressure_index, V5_traffic_flow_rate_vpm, V18_vehicle_approach_speed_mps, V10_older_adult_share, V22_wait_time_until_walk_s, V19_ped_traverse_time_s, V6_arrival_time_within_cycle_s, V2_curb_extension_present, V21_near_conflict_flag, V4_illumination_weather_state, V7_timer_visibility_quality, V3_signal_cycle_length_s, V15_start_time_rel_phase_end_s. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 19.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 5.0 (1 run) | n/a | n/a |
| S2 after LLM review | 25.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 20.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 20.0 (1 run) | n/a | n/a |

**LLM review decisions.** 210 pairs. Same decision in every run: 210. Same edge/no-edge call in every run: 210. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 16, B 8, C 122, D 64.

**Final edges.** 20 distinct edges appear in at least one run; 20 appear in every run. Set by: llm 17, algorithm (unchanged) 3. Per run: LLM-set edges 17.0 (1 run); final edges between pairs the algorithm did not connect 12.0 (1 run); LLM additions where at least 90% of resamples had no edge 16.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V17_observed_unsafe_label->V16_unsafe_crossing_true | 1 |
| V10_older_adult_share->V14_focal_walking_speed_mps | 1 |
| V14_focal_walking_speed_mps->V19_ped_traverse_time_s | 1 |
| V23_abandonment_indicator->V8_visible_remaining_seconds | 1 |
| V23_abandonment_indicator->V11_time_pressure_index | 1 |
| V23_abandonment_indicator->V5_traffic_flow_rate_vpm | 1 |
| V23_abandonment_indicator->V18_vehicle_approach_speed_mps | 1 |
| V23_abandonment_indicator->V22_wait_time_until_walk_s | 1 |
| V23_abandonment_indicator->V19_ped_traverse_time_s | 1 |
| V23_abandonment_indicator->V21_near_conflict_flag | 1 |
| V8_visible_remaining_seconds->V11_time_pressure_index | 1 |
| V1_countdown_policy_enabled->V11_time_pressure_index | 1 |
| V1_countdown_policy_enabled->V22_wait_time_until_walk_s | 1 |
| V1_countdown_policy_enabled->V7_timer_visibility_quality | 1 |
| V11_time_pressure_index->V7_timer_visibility_quality | 1 |
| V10_older_adult_share->V19_ped_traverse_time_s | 1 |
| V22_wait_time_until_walk_s->V3_signal_cycle_length_s | 1 |
| V2_curb_extension_present->V19_ped_traverse_time_s | 1 |
| V3_signal_cycle_length_s->V6_arrival_time_within_cycle_s | 1 |
| V4_illumination_weather_state->V7_timer_visibility_quality | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.84 (1 run) | 0.42 (1 run) | 0.56 (1 run) | 5.0 (1 run) | 0.0 (1 run) | 38.0 (1 run) | 1.00 (1 run) | 0.13 (1 run) | 0.23 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.13 (1 run) | 0.23 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 35.0 (1 run) | 1.00 (1 run) | 0.11 (1 run) | 0.19 (1 run) |
| S2 after LLM review | 0.52 (1 run) | 0.34 (1 run) | 0.41 (1 run) | 8.0 (1 run) | 5.0 (1 run) | 44.0 (1 run) | 0.32 (1 run) | 0.21 (1 run) | 0.25 (1 run) |
| S3 after KCI pruning | 0.60 (1 run) | 0.32 (1 run) | 0.41 (1 run) | 7.0 (1 run) | 5.0 (1 run) | 41.0 (1 run) | 0.35 (1 run) | 0.18 (1 run) | 0.24 (1 run) |
| S4 final (after cycle step) | 0.60 (1 run) | 0.32 (1 run) | 0.41 (1 run) | 7.0 (1 run) | 5.0 (1 run) | 41.0 (1 run) | 0.35 (1 run) | 0.18 (1 run) | 0.24 (1 run) |

## Arm `q022` (1 runs)

Family `s2_02`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21. File path names the dataset: no.

**Choices.** Algorithm: PC ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 5, "indep_test": "rcit_cpu"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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

**Randomness.** Distinct initial states of Python's random-number generator across runs: 1. Distinct bootstrap frequency tables among runs that used the same algorithm and hyperparameters: PC {"alpha": 0.05, "depth": 5, "indep_test": "rcit_cpu"}: 1.

**Graph by stage.** 1 distinct algorithm outputs (S0) across 1 runs.

| Stage | Adjacent pairs | Agreement between runs on adjacent pairs (mean pairwise Jaccard) | Agreement on typed edges |
|---|---|---|---|
| S0 algorithm output | 24.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 20.0 (1 run) | n/a | n/a |
| S2 after LLM review | 20.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 20.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 20.0 (1 run) | n/a | n/a |

**LLM review decisions.** 210 pairs. Same decision in every run: 210. Same edge/no-edge call in every run: 210. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 210.

**Final edges.** 20 distinct edges appear in at least one run; 20 appear in every run. Set by: algorithm (unchanged) 20. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V01 --- V02 | 1 |
| V01 --- V06 | 1 |
| V03->V09 | 1 |
| V03->V12 | 1 |
| V03->V14 | 1 |
| V04->V21 | 1 |
| V15->V05 | 1 |
| V05->V21 | 1 |
| V06->V09 | 1 |
| V06->V15 | 1 |
| V07 --- V13 | 1 |
| V08->V19 | 1 |
| V09->V21 | 1 |
| V10->V11 | 1 |
| V16->V11 | 1 |
| V16->V14 | 1 |
| V20->V15 | 1 |
| V16->V19 | 1 |
| V18->V19 | 1 |
| V20->V21 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.83 (1 run) | 0.53 (1 run) | 0.65 (1 run) | 14.0 (1 run) | 2.0 (1 run) | 31.0 (1 run) | 0.78 (1 run) | 0.37 (1 run) | 0.50 (1 run) |
| S1 after bootstrap edits | 0.90 (1 run) | 0.47 (1 run) | 0.62 (1 run) | 13.0 (1 run) | 2.0 (1 run) | 29.0 (1 run) | 0.76 (1 run) | 0.34 (1 run) | 0.47 (1 run) |
| S2 after LLM review | 0.90 (1 run) | 0.47 (1 run) | 0.62 (1 run) | 13.0 (1 run) | 2.0 (1 run) | 29.0 (1 run) | 0.76 (1 run) | 0.34 (1 run) | 0.47 (1 run) |
| S3 after KCI pruning | 0.90 (1 run) | 0.47 (1 run) | 0.62 (1 run) | 13.0 (1 run) | 2.0 (1 run) | 29.0 (1 run) | 0.76 (1 run) | 0.34 (1 run) | 0.47 (1 run) |
| S4 final (after cycle step) | 0.90 (1 run) | 0.47 (1 run) | 0.62 (1 run) | 13.0 (1 run) | 2.0 (1 run) | 29.0 (1 run) | 0.76 (1 run) | 0.34 (1 run) | 0.47 (1 run) |

## Arm `q023` (1 runs)

Family `s2_02`, role `swapped`. Column labels: V17_observed_unsafe_label, V14_focal_walking_speed_mps, V16_unsafe_crossing_true, V9_group_size_at_decision, V8_visible_remaining_seconds, V23_abandonment_indicator, V1_countdown_policy_enabled, V24_start_decision_now, V5_traffic_flow_rate_vpm, V11_time_pressure_index, V10_older_adult_share, V18_vehicle_approach_speed_mps, V19_ped_traverse_time_s, V22_wait_time_until_walk_s, V4_illumination_weather_state, V21_near_conflict_flag, V15_start_time_rel_phase_end_s, V7_timer_visibility_quality, V3_signal_cycle_length_s, V6_arrival_time_within_cycle_s, V2_curb_extension_present. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S2 after LLM review | 20.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 20.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 20.0 (1 run) | n/a | n/a |

**LLM review decisions.** 210 pairs. Same decision in every run: 210. Same edge/no-edge call in every run: 210. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 16, B 1, C 126, D 67.

**Final edges.** 20 distinct edges appear in at least one run; 20 appear in every run. Set by: llm 16, algorithm (unchanged) 4. Per run: LLM-set edges 16.0 (1 run); final edges between pairs the algorithm did not connect 16.0 (1 run); LLM additions where at least 90% of resamples had no edge 15.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V17_observed_unsafe_label->V16_unsafe_crossing_true | 1 |
| V17_observed_unsafe_label o-> V23_abandonment_indicator | 1 |
| V14_focal_walking_speed_mps->V19_ped_traverse_time_s | 1 |
| V16_unsafe_crossing_true->V21_near_conflict_flag | 1 |
| V8_visible_remaining_seconds->V1_countdown_policy_enabled | 1 |
| V4_illumination_weather_state->V8_visible_remaining_seconds | 1 |
| V23_abandonment_indicator->V5_traffic_flow_rate_vpm | 1 |
| V1_countdown_policy_enabled->V24_start_decision_now | 1 |
| V1_countdown_policy_enabled->V11_time_pressure_index | 1 |
| V1_countdown_policy_enabled->V22_wait_time_until_walk_s | 1 |
| V1_countdown_policy_enabled->V7_timer_visibility_quality | 1 |
| V5_traffic_flow_rate_vpm->V21_near_conflict_flag | 1 |
| V10_older_adult_share->V19_ped_traverse_time_s | 1 |
| V18_vehicle_approach_speed_mps->V21_near_conflict_flag | 1 |
| V21_near_conflict_flag->V22_wait_time_until_walk_s | 1 |
| V22_wait_time_until_walk_s->V15_start_time_rel_phase_end_s | 1 |
| V22_wait_time_until_walk_s->V3_signal_cycle_length_s | 1 |
| V22_wait_time_until_walk_s->V6_arrival_time_within_cycle_s | 1 |
| V4_illumination_weather_state->V7_timer_visibility_quality | 1 |
| V15_start_time_rel_phase_end_s->V6_arrival_time_within_cycle_s | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.82 (1 run) | 0.47 (1 run) | 0.60 (1 run) | 4.0 (1 run) | 1.0 (1 run) | 40.0 (1 run) | 0.80 (1 run) | 0.11 (1 run) | 0.19 (1 run) |
| S1 after bootstrap edits | 0.83 (1 run) | 0.13 (1 run) | 0.23 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 37.0 (1 run) | 0.75 (1 run) | 0.08 (1 run) | 0.14 (1 run) |
| S2 after LLM review | 0.30 (1 run) | 0.16 (1 run) | 0.21 (1 run) | 5.0 (1 run) | 0.0 (1 run) | 48.0 (1 run) | 0.26 (1 run) | 0.13 (1 run) | 0.18 (1 run) |
| S3 after KCI pruning | 0.30 (1 run) | 0.16 (1 run) | 0.21 (1 run) | 5.0 (1 run) | 0.0 (1 run) | 48.0 (1 run) | 0.26 (1 run) | 0.13 (1 run) | 0.18 (1 run) |
| S4 final (after cycle step) | 0.30 (1 run) | 0.16 (1 run) | 0.21 (1 run) | 5.0 (1 run) | 0.0 (1 run) | 48.0 (1 run) | 0.26 (1 run) | 0.13 (1 run) | 0.18 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 60.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 44.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.35 (1 run) | 0.18 (1 run) | 0.24 (1 run) | 4.0 (1 run) | 3.0 (1 run) | 47.0 (1 run) | 0.21 (1 run) | 0.11 (1 run) | 0.14 (1 run) |
| S3 after KCI pruning | 0.35 (1 run) | 0.18 (1 run) | 0.24 (1 run) | 4.0 (1 run) | 3.0 (1 run) | 47.0 (1 run) | 0.21 (1 run) | 0.11 (1 run) | 0.14 (1 run) |
| S4 final (after cycle step) | 0.35 (1 run) | 0.18 (1 run) | 0.24 (1 run) | 4.0 (1 run) | 3.0 (1 run) | 47.0 (1 run) | 0.21 (1 run) | 0.11 (1 run) | 0.14 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 7 |
| data only | 2 |
| both | 0 |
| neither | 7 |

Direction among those: data: direction as in reference 2, labels: direction as in reference 4, labels: reversed 3.
Distinct edges: data only: V22_wait_time_until_walk_s->V15_start_time_rel_phase_end_s, V8_visible_remaining_seconds->V1_countdown_policy_enabled; labels only: V14_focal_walking_speed_mps->V19_ped_traverse_time_s, V17_observed_unsafe_label->V16_unsafe_crossing_true, V18_vehicle_approach_speed_mps->V21_near_conflict_flag, V1_countdown_policy_enabled->V7_timer_visibility_quality, V22_wait_time_until_walk_s->V3_signal_cycle_length_s, V22_wait_time_until_walk_s->V6_arrival_time_within_cycle_s, V4_illumination_weather_state->V7_timer_visibility_quality; neither: V10_older_adult_share->V19_ped_traverse_time_s, V15_start_time_rel_phase_end_s->V6_arrival_time_within_cycle_s, V16_unsafe_crossing_true->V21_near_conflict_flag, V1_countdown_policy_enabled->V11_time_pressure_index, V1_countdown_policy_enabled->V22_wait_time_until_walk_s, V1_countdown_policy_enabled->V24_start_decision_now, V5_traffic_flow_rate_vpm->V21_near_conflict_flag.

## Arm `q031` (1 runs)

Family `s2_03`, role `real`. Column labels: prior_false_alarm_experience, assistance_request, attention_share_siren, departure_time_observed, assistance_fleet_vehicles, baseline_risk_tolerance, perceived_credibility_score, hazard_distance_at_t0, message_specificity_level, attention_share_sms, congestion_index_at_decision, sms_alert_enabled, handset_reachable, mobility_needs_index, siren_audibility_index, attention_share_neighbors, departure_time_true, attention_share_social, readiness_time_since_t0, hazard_approach_rate, vehicle_access, local_cumulative_departure_fraction, attention_share_news, pickup_eta_minutes, censor_indicator. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S1 after bootstrap edits | 10.0 (1 run) | n/a | n/a |
| S2 after LLM review | 22.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 19.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 19.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 11, B 8, C 79, D 202.

**Final edges.** 19 distinct edges appear in at least one run; 19 appear in every run. Set by: llm 14, algorithm (unchanged) 5. Per run: LLM-set edges 14.0 (1 run); final edges between pairs the algorithm did not connect 11.0 (1 run); LLM additions where at least 90% of resamples had no edge 13.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| attention_share_siren <-> attention_share_sms | 1 |
| attention_share_siren->siren_audibility_index | 1 |
| attention_share_siren->attention_share_news | 1 |
| hazard_distance_at_t0->departure_time_observed | 1 |
| readiness_time_since_t0->departure_time_observed | 1 |
| hazard_distance_at_t0->congestion_index_at_decision | 1 |
| hazard_distance_at_t0->departure_time_true | 1 |
| hazard_distance_at_t0->readiness_time_since_t0 | 1 |
| hazard_distance_at_t0->local_cumulative_departure_fraction | 1 |
| attention_share_sms->sms_alert_enabled | 1 |
| attention_share_sms->handset_reachable | 1 |
| attention_share_social->attention_share_sms | 1 |
| congestion_index_at_decision->local_cumulative_departure_fraction | 1 |
| attention_share_neighbors o-o attention_share_social | 1 |
| departure_time_true->readiness_time_since_t0 | 1 |
| hazard_approach_rate->departure_time_true | 1 |
| departure_time_true->vehicle_access | 1 |
| pickup_eta_minutes->departure_time_true | 1 |
| readiness_time_since_t0 <-> pickup_eta_minutes | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.72 (1 run) | 0.31 (1 run) | 0.43 (1 run) | 1.0 (1 run) | 1.0 (1 run) | 64.0 (1 run) | 0.25 (1 run) | 0.02 (1 run) | 0.03 (1 run) |
| S1 after bootstrap edits | 0.40 (1 run) | 0.07 (1 run) | 0.12 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 63.0 (1 run) | 0.33 (1 run) | 0.02 (1 run) | 0.03 (1 run) |
| S2 after LLM review | 0.36 (1 run) | 0.14 (1 run) | 0.20 (1 run) | 2.0 (1 run) | 5.0 (1 run) | 70.0 (1 run) | 0.11 (1 run) | 0.03 (1 run) | 0.05 (1 run) |
| S3 after KCI pruning | 0.42 (1 run) | 0.14 (1 run) | 0.21 (1 run) | 2.0 (1 run) | 5.0 (1 run) | 67.0 (1 run) | 0.12 (1 run) | 0.03 (1 run) | 0.05 (1 run) |
| S4 final (after cycle step) | 0.42 (1 run) | 0.14 (1 run) | 0.21 (1 run) | 2.0 (1 run) | 5.0 (1 run) | 67.0 (1 run) | 0.12 (1 run) | 0.03 (1 run) | 0.05 (1 run) |

## Arm `q032` (1 runs)

Family `s2_03`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S1 after bootstrap edits | 6.0 (1 run) | n/a | n/a |
| S2 after LLM review | 6.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 6.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 6.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 300.

**Final edges.** 6 distinct edges appear in at least one run; 6 appear in every run. Set by: algorithm (unchanged) 6. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V02 o-> V24 | 1 |
| V10 o-> V03 | 1 |
| V08 o-o V17 | 1 |
| V09 o-> V22 | 1 |
| V16 o-o V18 | 1 |
| V24->V19 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.72 (1 run) | 0.31 (1 run) | 0.43 (1 run) | 2.0 (1 run) | 0.0 (1 run) | 63.0 (1 run) | 1.00 (1 run) | 0.03 (1 run) | 0.07 (1 run) |
| S1 after bootstrap edits | 0.67 (1 run) | 0.07 (1 run) | 0.12 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 59.0 (1 run) | 1.00 (1 run) | 0.02 (1 run) | 0.03 (1 run) |
| S2 after LLM review | 0.67 (1 run) | 0.07 (1 run) | 0.12 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 59.0 (1 run) | 1.00 (1 run) | 0.02 (1 run) | 0.03 (1 run) |
| S3 after KCI pruning | 0.67 (1 run) | 0.07 (1 run) | 0.12 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 59.0 (1 run) | 1.00 (1 run) | 0.02 (1 run) | 0.03 (1 run) |
| S4 final (after cycle step) | 0.67 (1 run) | 0.07 (1 run) | 0.12 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 59.0 (1 run) | 1.00 (1 run) | 0.02 (1 run) | 0.03 (1 run) |

## Arm `q042` (1 runs)

Family `s2_04`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 23.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 6.0 (1 run) | n/a | n/a |
| S2 after LLM review | 6.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 6.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 6.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 300.

**Final edges.** 6 distinct edges appear in at least one run; 6 appear in every run. Set by: algorithm (unchanged) 6. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V12->V04 | 1 |
| V09->V06 | 1 |
| V09->V14 | 1 |
| V10 <-> V17 | 1 |
| V14 <-> V17 | 1 |
| V23->V15 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.96 (1 run) | 0.55 (1 run) | 0.70 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 1.00 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.15 (1 run) | 0.26 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 36.0 (1 run) | 1.00 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S2 after LLM review | 1.00 (1 run) | 0.15 (1 run) | 0.26 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 36.0 (1 run) | 1.00 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S3 after KCI pruning | 1.00 (1 run) | 0.15 (1 run) | 0.26 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 36.0 (1 run) | 1.00 (1 run) | 0.10 (1 run) | 0.18 (1 run) |
| S4 final (after cycle step) | 1.00 (1 run) | 0.15 (1 run) | 0.26 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 36.0 (1 run) | 1.00 (1 run) | 0.10 (1 run) | 0.18 (1 run) |

## Arm `q043` (1 runs)

Family `s2_04`, role `swapped`. Column labels: thermostat_setpoint_c, outdoor_relative_humidity_pct, seat_operative_temperature_c, individual_thermal_sensitivity_index, total_skipped_items_count, room_attendance_rate, person_speed_trait_index, outdoor_temperature_c, time_share_section_b, assigned_seat_location_index, exam_version_difficulty_index, person_ability_theta, room_avg_temperature_c, seat_relative_humidity_pct, local_neighbor_density_index, hvac_mode, time_share_section_a, exam_start_time_offset_min, initial_time_budget_min, perceived_discomfort_index, seat_distance_to_vent_m, allowed_setpoint_range_c, total_score_points, time_lost_due_to_disruption_min, room_avg_relative_humidity_pct. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 24.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 4.0 (1 run) | n/a | n/a |
| S2 after LLM review | 32.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 24.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 24.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 21, B 8, C 170, D 101.

**Final edges.** 24 distinct edges appear in at least one run; 24 appear in every run. Set by: llm 21, algorithm (unchanged) 3. Per run: LLM-set edges 21.0 (1 run); final edges between pairs the algorithm did not connect 20.0 (1 run); LLM additions where at least 90% of resamples had no edge 28.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| thermostat_setpoint_c->seat_operative_temperature_c | 1 |
| thermostat_setpoint_c->room_avg_temperature_c | 1 |
| thermostat_setpoint_c->seat_relative_humidity_pct | 1 |
| thermostat_setpoint_c->perceived_discomfort_index | 1 |
| thermostat_setpoint_c->room_avg_relative_humidity_pct | 1 |
| outdoor_relative_humidity_pct->seat_relative_humidity_pct | 1 |
| outdoor_relative_humidity_pct->perceived_discomfort_index | 1 |
| outdoor_relative_humidity_pct->room_avg_relative_humidity_pct | 1 |
| seat_operative_temperature_c->room_avg_temperature_c | 1 |
| individual_thermal_sensitivity_index->perceived_discomfort_index | 1 |
| outdoor_temperature_c->room_avg_temperature_c | 1 |
| outdoor_temperature_c->seat_relative_humidity_pct | 1 |
| outdoor_temperature_c->hvac_mode | 1 |
| outdoor_temperature_c->perceived_discomfort_index | 1 |
| outdoor_temperature_c->room_avg_relative_humidity_pct | 1 |
| time_share_section_b->seat_relative_humidity_pct | 1 |
| assigned_seat_location_index <-> time_share_section_a | 1 |
| exam_version_difficulty_index->total_score_points | 1 |
| person_ability_theta->total_score_points | 1 |
| seat_relative_humidity_pct->seat_distance_to_vent_m | 1 |
| total_score_points->local_neighbor_density_index | 1 |
| hvac_mode->perceived_discomfort_index | 1 |
| hvac_mode->room_avg_relative_humidity_pct | 1 |
| total_score_points->time_lost_due_to_disruption_min | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.92 (1 run) | 0.55 (1 run) | 0.69 (1 run) | 3.0 (1 run) | 1.0 (1 run) | 39.0 (1 run) | 0.75 (1 run) | 0.07 (1 run) | 0.14 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.10 (1 run) | 0.18 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 1.00 (1 run) | 0.07 (1 run) | 0.14 (1 run) |
| S2 after LLM review | 0.12 (1 run) | 0.10 (1 run) | 0.11 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 65.0 (1 run) | 0.10 (1 run) | 0.07 (1 run) | 0.08 (1 run) |
| S3 after KCI pruning | 0.17 (1 run) | 0.10 (1 run) | 0.12 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 57.0 (1 run) | 0.13 (1 run) | 0.07 (1 run) | 0.10 (1 run) |
| S4 final (after cycle step) | 0.17 (1 run) | 0.10 (1 run) | 0.12 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 57.0 (1 run) | 0.13 (1 run) | 0.07 (1 run) | 0.10 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 64.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 44.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.44 (1 run) | 0.35 (1 run) | 0.39 (1 run) | 9.0 (1 run) | 5.0 (1 run) | 49.0 (1 run) | 0.29 (1 run) | 0.23 (1 run) | 0.25 (1 run) |
| S3 after KCI pruning | 0.42 (1 run) | 0.25 (1 run) | 0.31 (1 run) | 7.0 (1 run) | 3.0 (1 run) | 47.0 (1 run) | 0.30 (1 run) | 0.17 (1 run) | 0.22 (1 run) |
| S4 final (after cycle step) | 0.42 (1 run) | 0.25 (1 run) | 0.31 (1 run) | 7.0 (1 run) | 3.0 (1 run) | 47.0 (1 run) | 0.30 (1 run) | 0.17 (1 run) | 0.22 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 10 |
| data only | 1 |
| both | 0 |
| neither | 10 |

Direction among those: data: direction as in reference 1, labels: direction as in reference 7, labels: reversed 3.
Distinct edges: data only: outdoor_temperature_c->seat_relative_humidity_pct; labels only: exam_version_difficulty_index->total_score_points, hvac_mode->room_avg_relative_humidity_pct, individual_thermal_sensitivity_index->perceived_discomfort_index, outdoor_relative_humidity_pct->room_avg_relative_humidity_pct, outdoor_temperature_c->room_avg_temperature_c, person_ability_theta->total_score_points, seat_operative_temperature_c->room_avg_temperature_c, seat_relative_humidity_pct->seat_distance_to_vent_m, thermostat_setpoint_c->room_avg_temperature_c, total_score_points->time_lost_due_to_disruption_min; neither: hvac_mode->perceived_discomfort_index, outdoor_relative_humidity_pct->perceived_discomfort_index, outdoor_relative_humidity_pct->seat_relative_humidity_pct, outdoor_temperature_c->hvac_mode, outdoor_temperature_c->perceived_discomfort_index, outdoor_temperature_c->room_avg_relative_humidity_pct, thermostat_setpoint_c->perceived_discomfort_index, thermostat_setpoint_c->room_avg_relative_humidity_pct, thermostat_setpoint_c->seat_operative_temperature_c, thermostat_setpoint_c->seat_relative_humidity_pct.

## Arm `q052` (1 runs)

Family `s2_05`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S1 after bootstrap edits | 2.0 (1 run) | n/a | n/a |
| S2 after LLM review | 2.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 2.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 2.0 (1 run) | n/a | n/a |

**LLM review decisions.** 190 pairs. Same decision in every run: 190. Same edge/no-edge call in every run: 190. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 190.

**Final edges.** 2 distinct edges appear in at least one run; 2 appear in every run. Set by: algorithm (unchanged) 2. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V06->V15 | 1 |
| V10 o-> V09 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.82 (1 run) | 0.37 (1 run) | 0.51 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 1.00 (1 run) | 0.11 (1 run) | 0.19 (1 run) |
| S1 after bootstrap edits | 0.50 (1 run) | 0.03 (1 run) | 0.05 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 38.0 (1 run) | 1.00 (1 run) | 0.03 (1 run) | 0.05 (1 run) |
| S2 after LLM review | 0.50 (1 run) | 0.03 (1 run) | 0.05 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 38.0 (1 run) | 1.00 (1 run) | 0.03 (1 run) | 0.05 (1 run) |
| S3 after KCI pruning | 0.50 (1 run) | 0.03 (1 run) | 0.05 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 38.0 (1 run) | 1.00 (1 run) | 0.03 (1 run) | 0.05 (1 run) |
| S4 final (after cycle step) | 0.50 (1 run) | 0.03 (1 run) | 0.05 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 38.0 (1 run) | 1.00 (1 run) | 0.03 (1 run) | 0.05 (1 run) |

## Arm `q053` (1 runs)

Family `s2_05`, role `swapped`. Column labels: cycle_gross_margin_dollars, lead_time_days, retail_list_price_dollars, demand_forecast_units_per_day, waste_units_disposed, shelf_capacity_units, stockout_days_count, credit_draw_amount_dollars, markdown_policy_schedule, interest_expense_dollars, credit_line_offer_flag, interest_rate_apr, reorder_point_units, tentative_order_quantity_units, unit_wholesale_price, available_credit_dollars, cash_on_hand_dollars, chosen_service_level, on_hand_units_at_open, early_payment_choice. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 14.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 5.0 (1 run) | n/a | n/a |
| S2 after LLM review | 28.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 20.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 20.0 (1 run) | n/a | n/a |

**LLM review decisions.** 190 pairs. Same decision in every run: 190. Same edge/no-edge call in every run: 190. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 17, B 11, C 159, D 3.

**Final edges.** 20 distinct edges appear in at least one run; 20 appear in every run. Set by: llm 19, algorithm (unchanged) 1. Per run: LLM-set edges 19.0 (1 run); final edges between pairs the algorithm did not connect 18.0 (1 run); LLM additions where at least 90% of resamples had no edge 23.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| cycle_gross_margin_dollars->retail_list_price_dollars | 1 |
| lead_time_days->stockout_days_count | 1 |
| lead_time_days->reorder_point_units | 1 |
| demand_forecast_units_per_day->retail_list_price_dollars | 1 |
| retail_list_price_dollars->markdown_policy_schedule | 1 |
| demand_forecast_units_per_day->reorder_point_units | 1 |
| demand_forecast_units_per_day->tentative_order_quantity_units | 1 |
| demand_forecast_units_per_day->chosen_service_level | 1 |
| stockout_days_count->on_hand_units_at_open | 1 |
| credit_draw_amount_dollars->interest_expense_dollars | 1 |
| available_credit_dollars->credit_draw_amount_dollars | 1 |
| interest_expense_dollars->interest_rate_apr | 1 |
| credit_line_offer_flag->available_credit_dollars | 1 |
| interest_rate_apr->cash_on_hand_dollars | 1 |
| reorder_point_units->tentative_order_quantity_units | 1 |
| reorder_point_units->chosen_service_level | 1 |
| tentative_order_quantity_units->chosen_service_level | 1 |
| tentative_order_quantity_units->on_hand_units_at_open | 1 |
| early_payment_choice->unit_wholesale_price | 1 |
| cash_on_hand_dollars->early_payment_choice | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.86 (1 run) | 0.32 (1 run) | 0.46 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 1.00 (1 run) | 0.08 (1 run) | 0.15 (1 run) |
| S1 after bootstrap edits | 0.80 (1 run) | 0.11 (1 run) | 0.19 (1 run) | 2.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 1.00 (1 run) | 0.05 (1 run) | 0.10 (1 run) |
| S2 after LLM review | 0.11 (1 run) | 0.08 (1 run) | 0.09 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 62.0 (1 run) | 0.04 (1 run) | 0.03 (1 run) | 0.03 (1 run) |
| S3 after KCI pruning | 0.15 (1 run) | 0.08 (1 run) | 0.10 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 54.0 (1 run) | 0.05 (1 run) | 0.03 (1 run) | 0.03 (1 run) |
| S4 final (after cycle step) | 0.15 (1 run) | 0.08 (1 run) | 0.10 (1 run) | 1.0 (1 run) | 2.0 (1 run) | 54.0 (1 run) | 0.05 (1 run) | 0.03 (1 run) | 0.03 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.07 (1 run) | 0.03 (1 run) | 0.04 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 51.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 43.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.54 (1 run) | 0.39 (1 run) | 0.45 (1 run) | 10.0 (1 run) | 5.0 (1 run) | 43.0 (1 run) | 0.36 (1 run) | 0.26 (1 run) | 0.30 (1 run) |
| S3 after KCI pruning | 0.65 (1 run) | 0.34 (1 run) | 0.45 (1 run) | 9.0 (1 run) | 4.0 (1 run) | 38.0 (1 run) | 0.45 (1 run) | 0.24 (1 run) | 0.31 (1 run) |
| S4 final (after cycle step) | 0.65 (1 run) | 0.34 (1 run) | 0.45 (1 run) | 9.0 (1 run) | 4.0 (1 run) | 38.0 (1 run) | 0.45 (1 run) | 0.24 (1 run) | 0.31 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 13 |
| data only | 2 |
| both | 0 |
| neither | 4 |

Direction among those: data: reversed 2, labels: direction as in reference 9, labels: reversed 4.
Distinct edges: data only: demand_forecast_units_per_day->retail_list_price_dollars, tentative_order_quantity_units->chosen_service_level; labels only: available_credit_dollars->credit_draw_amount_dollars, cash_on_hand_dollars->early_payment_choice, credit_draw_amount_dollars->interest_expense_dollars, credit_line_offer_flag->available_credit_dollars, cycle_gross_margin_dollars->retail_list_price_dollars, demand_forecast_units_per_day->reorder_point_units, demand_forecast_units_per_day->tentative_order_quantity_units, interest_expense_dollars->interest_rate_apr, lead_time_days->stockout_days_count, reorder_point_units->chosen_service_level, reorder_point_units->tentative_order_quantity_units, stockout_days_count->on_hand_units_at_open, tentative_order_quantity_units->on_hand_units_at_open; neither: demand_forecast_units_per_day->chosen_service_level, interest_rate_apr->cash_on_hand_dollars, lead_time_days->reorder_point_units, retail_list_price_dollars->markdown_policy_schedule.

## Arm `q061` (1 runs)

Family `s2_06`, role `real`. Column labels: routing_weight_nearest_backup, rum_sampling_fraction, incident_error_rate, nearest_backup_capacity_rps, resolver_ttl_floor_seconds, baseline_latency_ms, serve_stale_enabled, resolver_class, failure_caching_level, stale_hit_probability_at_outage, cohort_request_rate_qps, consecutive_failure_threshold, ttl_config_seconds, failover_latency_seconds, selected_backup_pop, observed_incident_error_rate, probe_loss_jitter_rate, time_to_95p_adoption_seconds, primary_pop_outage, resolver_prefetch_threshold, detection_delay_seconds, observed_failover_latency_seconds, health_check_interval_seconds, ecs_present, client_region. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 19.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 5.0 (1 run) | n/a | n/a |
| S2 after LLM review | 19.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 19.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 19.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 16, C 90, D 194.

**Final edges.** 19 distinct edges appear in at least one run; 19 appear in every run. Set by: llm 15, algorithm (unchanged) 4. Per run: LLM-set edges 15.0 (1 run); final edges between pairs the algorithm did not connect 11.0 (1 run); LLM additions where at least 90% of resamples had no edge 11.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| incident_error_rate->failover_latency_seconds | 1 |
| incident_error_rate->observed_incident_error_rate | 1 |
| incident_error_rate->primary_pop_outage | 1 |
| incident_error_rate->detection_delay_seconds | 1 |
| incident_error_rate->observed_failover_latency_seconds | 1 |
| nearest_backup_capacity_rps->failover_latency_seconds | 1 |
| nearest_backup_capacity_rps->selected_backup_pop | 1 |
| nearest_backup_capacity_rps->observed_failover_latency_seconds | 1 |
| resolver_ttl_floor_seconds o-o resolver_class | 1 |
| resolver_ttl_floor_seconds o-> cohort_request_rate_qps | 1 |
| serve_stale_enabled->stale_hit_probability_at_outage | 1 |
| resolver_class->cohort_request_rate_qps | 1 |
| time_to_95p_adoption_seconds->failover_latency_seconds | 1 |
| failover_latency_seconds->observed_failover_latency_seconds | 1 |
| selected_backup_pop->primary_pop_outage | 1 |
| selected_backup_pop->observed_failover_latency_seconds | 1 |
| observed_incident_error_rate->primary_pop_outage | 1 |
| primary_pop_outage->observed_failover_latency_seconds | 1 |
| detection_delay_seconds->health_check_interval_seconds | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.79 (1 run) | 0.32 (1 run) | 0.45 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 49.0 (1 run) | 0.75 (1 run) | 0.06 (1 run) | 0.12 (1 run) |
| S1 after bootstrap edits | 0.80 (1 run) | 0.09 (1 run) | 0.15 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 46.0 (1 run) | 1.00 (1 run) | 0.06 (1 run) | 0.12 (1 run) |
| S2 after LLM review | 0.47 (1 run) | 0.19 (1 run) | 0.27 (1 run) | 5.0 (1 run) | 3.0 (1 run) | 52.0 (1 run) | 0.29 (1 run) | 0.11 (1 run) | 0.16 (1 run) |
| S3 after KCI pruning | 0.47 (1 run) | 0.19 (1 run) | 0.27 (1 run) | 5.0 (1 run) | 3.0 (1 run) | 52.0 (1 run) | 0.29 (1 run) | 0.11 (1 run) | 0.16 (1 run) |
| S4 final (after cycle step) | 0.47 (1 run) | 0.19 (1 run) | 0.27 (1 run) | 5.0 (1 run) | 3.0 (1 run) | 52.0 (1 run) | 0.29 (1 run) | 0.11 (1 run) | 0.16 (1 run) |

## Arm `q062` (1 runs)

Family `s2_06`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 18.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 4.0 (1 run) | n/a | n/a |
| S2 after LLM review | 4.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 4.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 4.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 300.

**Final edges.** 4 distinct edges appear in at least one run; 4 appear in every run. Set by: algorithm (unchanged) 4. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V05 o-o V09 | 1 |
| V08->V07 | 1 |
| V08->V20 | 1 |
| V18->V14 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.83 (1 run) | 0.32 (1 run) | 0.46 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 49.0 (1 run) | 0.75 (1 run) | 0.06 (1 run) | 0.12 (1 run) |
| S1 after bootstrap edits | 0.75 (1 run) | 0.06 (1 run) | 0.12 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 47.0 (1 run) | 1.00 (1 run) | 0.06 (1 run) | 0.12 (1 run) |
| S2 after LLM review | 0.75 (1 run) | 0.06 (1 run) | 0.12 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 47.0 (1 run) | 1.00 (1 run) | 0.06 (1 run) | 0.12 (1 run) |
| S3 after KCI pruning | 0.75 (1 run) | 0.06 (1 run) | 0.12 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 47.0 (1 run) | 1.00 (1 run) | 0.06 (1 run) | 0.12 (1 run) |
| S4 final (after cycle step) | 0.75 (1 run) | 0.06 (1 run) | 0.12 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 47.0 (1 run) | 1.00 (1 run) | 0.06 (1 run) | 0.12 (1 run) |

## Arm `q063` (1 runs)

Family `s2_06`, role `swapped`. Column labels: rum_sampling_fraction, routing_weight_nearest_backup, nearest_backup_capacity_rps, resolver_ttl_floor_seconds, incident_error_rate, serve_stale_enabled, baseline_latency_ms, cohort_request_rate_qps, consecutive_failure_threshold, ttl_config_seconds, failure_caching_level, resolver_class, failover_latency_seconds, stale_hit_probability_at_outage, probe_loss_jitter_rate, time_to_95p_adoption_seconds, selected_backup_pop, health_check_interval_seconds, observed_incident_error_rate, ecs_present, observed_failover_latency_seconds, detection_delay_seconds, client_region, primary_pop_outage, resolver_prefetch_threshold. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 21.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 3.0 (1 run) | n/a | n/a |
| S2 after LLM review | 14.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 12.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 12.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 11, B 2, C 151, D 136.

**Final edges.** 12 distinct edges appear in at least one run; 12 appear in every run. Set by: llm 10, algorithm (unchanged) 2. Per run: LLM-set edges 10.0 (1 run); final edges between pairs the algorithm did not connect 9.0 (1 run); LLM additions where at least 90% of resamples had no edge 10.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| routing_weight_nearest_backup->failover_latency_seconds | 1 |
| nearest_backup_capacity_rps->failover_latency_seconds | 1 |
| nearest_backup_capacity_rps->observed_failover_latency_seconds | 1 |
| resolver_ttl_floor_seconds->ttl_config_seconds | 1 |
| cohort_request_rate_qps->incident_error_rate | 1 |
| incident_error_rate->observed_incident_error_rate | 1 |
| serve_stale_enabled->stale_hit_probability_at_outage | 1 |
| baseline_latency_ms->cohort_request_rate_qps | 1 |
| cohort_request_rate_qps->failure_caching_level | 1 |
| failover_latency_seconds->observed_failover_latency_seconds | 1 |
| stale_hit_probability_at_outage->primary_pop_outage | 1 |
| observed_incident_error_rate->primary_pop_outage | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.67 (1 run) | 0.30 (1 run) | 0.41 (1 run) | 4.0 (1 run) | 0.0 (1 run) | 51.0 (1 run) | 0.57 (1 run) | 0.09 (1 run) | 0.15 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.06 (1 run) | 0.12 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 45.0 (1 run) | 1.00 (1 run) | 0.06 (1 run) | 0.12 (1 run) |
| S2 after LLM review | 0.29 (1 run) | 0.09 (1 run) | 0.13 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 55.0 (1 run) | 0.14 (1 run) | 0.04 (1 run) | 0.07 (1 run) |
| S3 after KCI pruning | 0.33 (1 run) | 0.09 (1 run) | 0.14 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 53.0 (1 run) | 0.17 (1 run) | 0.04 (1 run) | 0.07 (1 run) |
| S4 final (after cycle step) | 0.33 (1 run) | 0.09 (1 run) | 0.14 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 53.0 (1 run) | 0.17 (1 run) | 0.04 (1 run) | 0.07 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.19 (1 run) | 0.09 (1 run) | 0.12 (1 run) | 1.0 (1 run) | 0.0 (1 run) | 63.0 (1 run) | 0.14 (1 run) | 0.02 (1 run) | 0.04 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 50.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.21 (1 run) | 0.06 (1 run) | 0.10 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 55.0 (1 run) | 0.21 (1 run) | 0.06 (1 run) | 0.10 (1 run) |
| S3 after KCI pruning | 0.17 (1 run) | 0.04 (1 run) | 0.07 (1 run) | 2.0 (1 run) | 0.0 (1 run) | 55.0 (1 run) | 0.17 (1 run) | 0.04 (1 run) | 0.07 (1 run) |
| S4 final (after cycle step) | 0.17 (1 run) | 0.04 (1 run) | 0.07 (1 run) | 2.0 (1 run) | 0.0 (1 run) | 55.0 (1 run) | 0.17 (1 run) | 0.04 (1 run) | 0.07 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 2 |
| data only | 2 |
| both | 0 |
| neither | 6 |

Direction among those: data: reversed 2, labels: direction as in reference 2.
Distinct edges: data only: baseline_latency_ms->cohort_request_rate_qps, nearest_backup_capacity_rps->observed_failover_latency_seconds; labels only: failover_latency_seconds->observed_failover_latency_seconds, incident_error_rate->observed_incident_error_rate; neither: nearest_backup_capacity_rps->failover_latency_seconds, observed_incident_error_rate->primary_pop_outage, resolver_ttl_floor_seconds->ttl_config_seconds, routing_weight_nearest_backup->failover_latency_seconds, serve_stale_enabled->stale_hit_probability_at_outage, stale_hit_probability_at_outage->primary_pop_outage.

## Arm `q072` (1 runs)

Family `s2_07`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S1 after bootstrap edits | 9.0 (1 run) | n/a | n/a |
| S2 after LLM review | 9.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 9.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 9.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 231.

**Final edges.** 9 distinct edges appear in at least one run; 9 appear in every run. Set by: algorithm (unchanged) 9. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V02->V03 | 1 |
| V10->V03 | 1 |
| V19 o-> V03 | 1 |
| V08->V11 | 1 |
| V09->V14 | 1 |
| V11 <-> V21 | 1 |
| V12->V14 | 1 |
| V12 <-> V22 | 1 |
| V17->V22 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.78 (1 run) | 0.60 (1 run) | 0.68 (1 run) | 6.0 (1 run) | 1.0 (1 run) | 36.0 (1 run) | 0.86 (1 run) | 0.17 (1 run) | 0.29 (1 run) |
| S1 after bootstrap edits | 0.89 (1 run) | 0.23 (1 run) | 0.36 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 31.0 (1 run) | 1.00 (1 run) | 0.17 (1 run) | 0.29 (1 run) |
| S2 after LLM review | 0.89 (1 run) | 0.23 (1 run) | 0.36 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 31.0 (1 run) | 1.00 (1 run) | 0.17 (1 run) | 0.29 (1 run) |
| S3 after KCI pruning | 0.89 (1 run) | 0.23 (1 run) | 0.36 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 31.0 (1 run) | 1.00 (1 run) | 0.17 (1 run) | 0.29 (1 run) |
| S4 final (after cycle step) | 0.89 (1 run) | 0.23 (1 run) | 0.36 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 31.0 (1 run) | 1.00 (1 run) | 0.17 (1 run) | 0.29 (1 run) |

## Arm `q073` (1 runs)

Family `s2_07`, role `swapped`. Column labels: attempted_trips_count, true_ems_heat_incidents, tree_canopy_pct, language_mismatch_rate, turnaways_count, indoor_time_above_safe_prop, neighborhood_heat_index, transit_vouchers_per_1000, social_isolation_rate, alerts_delivered_rate, outdoor_work_share, admitted_visits_count, effective_cooled_hours, distance_to_center_km, functional_capacity_day, effective_awareness_rate, hours_open, power_outage_rate, regional_heat_index_base, adjusted_heat_dose_index, observed_heat_calls, ac_ownership_rate. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S1 after bootstrap edits | 8.0 (1 run) | n/a | n/a |
| S2 after LLM review | 20.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 17.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 17.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 14, B 4, C 78, D 135.

**Final edges.** 17 distinct edges appear in at least one run; 17 appear in every run. Set by: llm 12, algorithm (unchanged) 5. Per run: LLM-set edges 12.0 (1 run); final edges between pairs the algorithm did not connect 11.0 (1 run); LLM additions where at least 90% of resamples had no edge 14.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| attempted_trips_count->adjusted_heat_dose_index | 1 |
| observed_heat_calls->attempted_trips_count | 1 |
| tree_canopy_pct->neighborhood_heat_index | 1 |
| effective_cooled_hours o-> tree_canopy_pct | 1 |
| language_mismatch_rate->turnaways_count | 1 |
| language_mismatch_rate->social_isolation_rate | 1 |
| language_mismatch_rate->alerts_delivered_rate | 1 |
| language_mismatch_rate->effective_awareness_rate | 1 |
| neighborhood_heat_index->regional_heat_index_base | 1 |
| neighborhood_heat_index->adjusted_heat_dose_index | 1 |
| neighborhood_heat_index->observed_heat_calls | 1 |
| social_isolation_rate->observed_heat_calls | 1 |
| alerts_delivered_rate->effective_awareness_rate | 1 |
| outdoor_work_share->adjusted_heat_dose_index | 1 |
| outdoor_work_share->observed_heat_calls | 1 |
| admitted_visits_count <-> ac_ownership_rate | 1 |
| power_outage_rate->observed_heat_calls | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.78 (1 run) | 0.60 (1 run) | 0.68 (1 run) | 8.0 (1 run) | 0.0 (1 run) | 34.0 (1 run) | 1.00 (1 run) | 0.23 (1 run) | 0.37 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.23 (1 run) | 0.37 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 30.0 (1 run) | 1.00 (1 run) | 0.17 (1 run) | 0.29 (1 run) |
| S2 after LLM review | 0.25 (1 run) | 0.14 (1 run) | 0.18 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 47.0 (1 run) | 0.17 (1 run) | 0.09 (1 run) | 0.11 (1 run) |
| S3 after KCI pruning | 0.29 (1 run) | 0.14 (1 run) | 0.19 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 44.0 (1 run) | 0.20 (1 run) | 0.09 (1 run) | 0.12 (1 run) |
| S4 final (after cycle step) | 0.29 (1 run) | 0.14 (1 run) | 0.19 (1 run) | 3.0 (1 run) | 0.0 (1 run) | 44.0 (1 run) | 0.20 (1 run) | 0.09 (1 run) | 0.12 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.07 (1 run) | 0.06 (1 run) | 0.06 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 60.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 43.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.45 (1 run) | 0.26 (1 run) | 0.33 (1 run) | 7.0 (1 run) | 2.0 (1 run) | 39.0 (1 run) | 0.39 (1 run) | 0.20 (1 run) | 0.26 (1 run) |
| S3 after KCI pruning | 0.35 (1 run) | 0.17 (1 run) | 0.23 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.33 (1 run) | 0.14 (1 run) | 0.20 (1 run) |
| S4 final (after cycle step) | 0.35 (1 run) | 0.17 (1 run) | 0.23 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.33 (1 run) | 0.14 (1 run) | 0.20 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 6 |
| data only | 0 |
| both | 0 |
| neither | 6 |

Direction among those: labels: direction as in reference 5, labels: reversed 1.
Distinct edges: labels only: alerts_delivered_rate->effective_awareness_rate, language_mismatch_rate->alerts_delivered_rate, language_mismatch_rate->effective_awareness_rate, neighborhood_heat_index->regional_heat_index_base, outdoor_work_share->adjusted_heat_dose_index, tree_canopy_pct->neighborhood_heat_index; neither: language_mismatch_rate->social_isolation_rate, language_mismatch_rate->turnaways_count, neighborhood_heat_index->adjusted_heat_dose_index, neighborhood_heat_index->observed_heat_calls, power_outage_rate->observed_heat_calls, social_isolation_rate->observed_heat_calls.

## Arm `q081` (1 runs)

Family `s2_08`, role `real`. Column labels: baseline_salt_rejection, fouling_stock, membrane_age, osmotic_pressure_diff, cip_removal_fraction, concentration_polarization_index, true_permeate_salt, feed_salinity, antiscalant_effectiveness, intrinsic_permeability, achieved_recovery_ratio, assayed_sdi, recovery_ratio_target, required_tmp, specific_energy_consumption, feed_temperature, fouling_stock_prior, deposition_rate, observed_permeate_conductivity, daily_production_demand, achieved_permeate_flow_rate, pretreatment_fouling_potential. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 22.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 11.0 (1 run) | n/a | n/a |
| S2 after LLM review | 41.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 39.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 39.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 32, B 8, C 148, D 43.

**Final edges.** 39 distinct edges appear in at least one run; 39 appear in every run. Set by: llm 35, algorithm (unchanged) 4. Per run: LLM-set edges 35.0 (1 run); final edges between pairs the algorithm did not connect 25.0 (1 run); LLM additions where at least 90% of resamples had no edge 21.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| baseline_salt_rejection->osmotic_pressure_diff | 1 |
| baseline_salt_rejection->true_permeate_salt | 1 |
| baseline_salt_rejection->feed_salinity | 1 |
| baseline_salt_rejection->observed_permeate_conductivity | 1 |
| cip_removal_fraction->fouling_stock | 1 |
| fouling_stock->fouling_stock_prior | 1 |
| fouling_stock->deposition_rate | 1 |
| membrane_age->intrinsic_permeability | 1 |
| membrane_age->required_tmp | 1 |
| membrane_age->specific_energy_consumption | 1 |
| membrane_age->achieved_permeate_flow_rate | 1 |
| true_permeate_salt->osmotic_pressure_diff | 1 |
| feed_salinity->osmotic_pressure_diff | 1 |
| osmotic_pressure_diff->required_tmp | 1 |
| concentration_polarization_index->feed_salinity | 1 |
| feed_salinity->true_permeate_salt | 1 |
| true_permeate_salt->observed_permeate_conductivity | 1 |
| feed_salinity->antiscalant_effectiveness | 1 |
| feed_salinity->required_tmp | 1 |
| feed_salinity->specific_energy_consumption | 1 |
| feed_salinity->observed_permeate_conductivity | 1 |
| antiscalant_effectiveness->deposition_rate | 1 |
| intrinsic_permeability->required_tmp | 1 |
| intrinsic_permeability->achieved_permeate_flow_rate | 1 |
| recovery_ratio_target->achieved_recovery_ratio | 1 |
| required_tmp->achieved_recovery_ratio | 1 |
| achieved_recovery_ratio->achieved_permeate_flow_rate | 1 |
| assayed_sdi->pretreatment_fouling_potential | 1 |
| required_tmp->specific_energy_consumption | 1 |
| required_tmp->achieved_permeate_flow_rate | 1 |
| specific_energy_consumption->achieved_permeate_flow_rate | 1 |
| feed_temperature->observed_permeate_conductivity | 1 |
| feed_temperature->achieved_permeate_flow_rate | 1 |
| feed_temperature <-> pretreatment_fouling_potential | 1 |
| fouling_stock_prior->deposition_rate | 1 |
| fouling_stock_prior->pretreatment_fouling_potential | 1 |
| deposition_rate->achieved_permeate_flow_rate | 1 |
| deposition_rate->pretreatment_fouling_potential | 1 |
| daily_production_demand->achieved_permeate_flow_rate | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.77 (1 run) | 0.42 (1 run) | 0.55 (1 run) | 4.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.50 (1 run) | 0.10 (1 run) | 0.17 (1 run) |
| S1 after bootstrap edits | 0.82 (1 run) | 0.23 (1 run) | 0.35 (1 run) | 4.0 (1 run) | 1.0 (1 run) | 38.0 (1 run) | 0.57 (1 run) | 0.10 (1 run) | 0.17 (1 run) |
| S2 after LLM review | 0.54 (1 run) | 0.55 (1 run) | 0.54 (1 run) | 14.0 (1 run) | 7.0 (1 run) | 47.0 (1 run) | 0.35 (1 run) | 0.35 (1 run) | 0.35 (1 run) |
| S3 after KCI pruning | 0.56 (1 run) | 0.55 (1 run) | 0.56 (1 run) | 14.0 (1 run) | 7.0 (1 run) | 45.0 (1 run) | 0.37 (1 run) | 0.35 (1 run) | 0.36 (1 run) |
| S4 final (after cycle step) | 0.56 (1 run) | 0.55 (1 run) | 0.56 (1 run) | 14.0 (1 run) | 7.0 (1 run) | 45.0 (1 run) | 0.37 (1 run) | 0.35 (1 run) | 0.36 (1 run) |

## Arm `q082` (1 runs)

Family `s2_08`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 1, D 230.

**Final edges.** 10 distinct edges appear in at least one run; 10 appear in every run. Set by: algorithm (unchanged) 10. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V07->V04 | 1 |
| V04->V08 | 1 |
| V20->V06 | 1 |
| V08 <-> V13 | 1 |
| V09 o-o V12 | 1 |
| V10->V14 | 1 |
| V12 o-o V22 | 1 |
| V21->V15 | 1 |
| V22->V16 | 1 |
| V20 o-o V21 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.74 (1 run) | 0.42 (1 run) | 0.54 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 44.0 (1 run) | 0.33 (1 run) | 0.05 (1 run) | 0.09 (1 run) |
| S1 after bootstrap edits | 0.80 (1 run) | 0.20 (1 run) | 0.32 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 40.0 (1 run) | 0.33 (1 run) | 0.05 (1 run) | 0.09 (1 run) |
| S2 after LLM review | 0.80 (1 run) | 0.20 (1 run) | 0.32 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 40.0 (1 run) | 0.33 (1 run) | 0.05 (1 run) | 0.09 (1 run) |
| S3 after KCI pruning | 0.80 (1 run) | 0.20 (1 run) | 0.32 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 40.0 (1 run) | 0.33 (1 run) | 0.05 (1 run) | 0.09 (1 run) |
| S4 final (after cycle step) | 0.80 (1 run) | 0.20 (1 run) | 0.32 (1 run) | 2.0 (1 run) | 2.0 (1 run) | 40.0 (1 run) | 0.33 (1 run) | 0.05 (1 run) | 0.09 (1 run) |

## Arm `q083` (1 runs)

Family `s2_08`, role `swapped`. Column labels: fouling_stock, baseline_salt_rejection, osmotic_pressure_diff, membrane_age, concentration_polarization_index, cip_removal_fraction, feed_salinity, achieved_recovery_ratio, true_permeate_salt, antiscalant_effectiveness, assayed_sdi, intrinsic_permeability, required_tmp, recovery_ratio_target, feed_temperature, observed_permeate_conductivity, deposition_rate, fouling_stock_prior, daily_production_demand, pretreatment_fouling_potential, specific_energy_consumption, achieved_permeate_flow_rate. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S2 after LLM review | 49.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 42.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 42.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 34, B 11, C 101, D 85.

**Final edges.** 42 distinct edges appear in at least one run; 42 appear in every run. Set by: llm 36, algorithm (unchanged) 6. Per run: LLM-set edges 36.0 (1 run); final edges between pairs the algorithm did not connect 35.0 (1 run); LLM additions where at least 90% of resamples had no edge 39.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| fouling_stock->cip_removal_fraction | 1 |
| antiscalant_effectiveness->fouling_stock | 1 |
| baseline_salt_rejection->achieved_recovery_ratio | 1 |
| baseline_salt_rejection->true_permeate_salt | 1 |
| baseline_salt_rejection->required_tmp | 1 |
| baseline_salt_rejection->observed_permeate_conductivity | 1 |
| baseline_salt_rejection->specific_energy_consumption | 1 |
| baseline_salt_rejection->achieved_permeate_flow_rate | 1 |
| osmotic_pressure_diff->feed_salinity | 1 |
| osmotic_pressure_diff->feed_temperature | 1 |
| membrane_age->intrinsic_permeability | 1 |
| membrane_age->recovery_ratio_target | 1 |
| concentration_polarization_index->feed_salinity | 1 |
| concentration_polarization_index->antiscalant_effectiveness | 1 |
| concentration_polarization_index->feed_temperature | 1 |
| cip_removal_fraction->deposition_rate | 1 |
| cip_removal_fraction->achieved_permeate_flow_rate | 1 |
| feed_salinity->achieved_recovery_ratio | 1 |
| feed_salinity->true_permeate_salt | 1 |
| feed_salinity->required_tmp | 1 |
| feed_salinity->observed_permeate_conductivity | 1 |
| feed_salinity->specific_energy_consumption | 1 |
| feed_salinity->achieved_permeate_flow_rate | 1 |
| achieved_recovery_ratio->true_permeate_salt | 1 |
| achieved_recovery_ratio->required_tmp | 1 |
| achieved_recovery_ratio->achieved_permeate_flow_rate | 1 |
| true_permeate_salt->intrinsic_permeability | 1 |
| observed_permeate_conductivity->true_permeate_salt | 1 |
| antiscalant_effectiveness->deposition_rate | 1 |
| antiscalant_effectiveness->achieved_permeate_flow_rate | 1 |
| assayed_sdi <-> required_tmp | 1 |
| feed_temperature->required_tmp | 1 |
| required_tmp->specific_energy_consumption | 1 |
| achieved_permeate_flow_rate->required_tmp | 1 |
| recovery_ratio_target->achieved_permeate_flow_rate | 1 |
| feed_temperature->specific_energy_consumption | 1 |
| feed_temperature->achieved_permeate_flow_rate | 1 |
| observed_permeate_conductivity <-> achieved_permeate_flow_rate | 1 |
| deposition_rate->specific_energy_consumption | 1 |
| daily_production_demand->specific_energy_consumption | 1 |
| daily_production_demand->achieved_permeate_flow_rate | 1 |
| pretreatment_fouling_potential o-o specific_energy_consumption | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.87 (1 run) | 0.50 (1 run) | 0.63 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 37.0 (1 run) | 0.86 (1 run) | 0.15 (1 run) | 0.26 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.25 (1 run) | 0.40 (1 run) | 6.0 (1 run) | 0.0 (1 run) | 34.0 (1 run) | 1.00 (1 run) | 0.15 (1 run) | 0.26 (1 run) |
| S2 after LLM review | 0.20 (1 run) | 0.25 (1 run) | 0.22 (1 run) | 4.0 (1 run) | 3.0 (1 run) | 75.0 (1 run) | 0.09 (1 run) | 0.10 (1 run) | 0.09 (1 run) |
| S3 after KCI pruning | 0.24 (1 run) | 0.25 (1 run) | 0.24 (1 run) | 4.0 (1 run) | 3.0 (1 run) | 68.0 (1 run) | 0.10 (1 run) | 0.10 (1 run) | 0.10 (1 run) |
| S4 final (after cycle step) | 0.24 (1 run) | 0.25 (1 run) | 0.24 (1 run) | 4.0 (1 run) | 3.0 (1 run) | 68.0 (1 run) | 0.10 (1 run) | 0.10 (1 run) | 0.10 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 63.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 50.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.35 (1 run) | 0.42 (1 run) | 0.38 (1 run) | 13.0 (1 run) | 4.0 (1 run) | 61.0 (1 run) | 0.28 (1 run) | 0.33 (1 run) | 0.30 (1 run) |
| S3 after KCI pruning | 0.29 (1 run) | 0.30 (1 run) | 0.29 (1 run) | 8.0 (1 run) | 4.0 (1 run) | 64.0 (1 run) | 0.21 (1 run) | 0.20 (1 run) | 0.20 (1 run) |
| S4 final (after cycle step) | 0.29 (1 run) | 0.30 (1 run) | 0.29 (1 run) | 8.0 (1 run) | 4.0 (1 run) | 64.0 (1 run) | 0.21 (1 run) | 0.20 (1 run) | 0.20 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 12 |
| data only | 4 |
| both | 0 |
| neither | 20 |

Direction among those: data: direction as in reference 1, data: reversed 3, labels: direction as in reference 8, labels: reversed 4.
Distinct edges: data only: achieved_recovery_ratio->achieved_permeate_flow_rate, feed_salinity->achieved_recovery_ratio, feed_temperature->specific_energy_consumption, true_permeate_salt->intrinsic_permeability; labels only: achieved_permeate_flow_rate->required_tmp, antiscalant_effectiveness->deposition_rate, baseline_salt_rejection->true_permeate_salt, concentration_polarization_index->feed_temperature, daily_production_demand->achieved_permeate_flow_rate, feed_salinity->true_permeate_salt, feed_temperature->required_tmp, fouling_stock->cip_removal_fraction, membrane_age->intrinsic_permeability, observed_permeate_conductivity->true_permeate_salt, osmotic_pressure_diff->feed_salinity, required_tmp->specific_energy_consumption; neither: antiscalant_effectiveness->achieved_permeate_flow_rate, antiscalant_effectiveness->fouling_stock, baseline_salt_rejection->achieved_permeate_flow_rate, baseline_salt_rejection->achieved_recovery_ratio, baseline_salt_rejection->observed_permeate_conductivity, baseline_salt_rejection->required_tmp, baseline_salt_rejection->specific_energy_consumption, cip_removal_fraction->achieved_permeate_flow_rate, cip_removal_fraction->deposition_rate, concentration_polarization_index->antiscalant_effectiveness, concentration_polarization_index->feed_salinity, daily_production_demand->specific_energy_consumption, deposition_rate->specific_energy_consumption, feed_salinity->achieved_permeate_flow_rate, feed_salinity->observed_permeate_conductivity, feed_salinity->required_tmp, feed_salinity->specific_energy_consumption, feed_temperature->achieved_permeate_flow_rate, osmotic_pressure_diff->feed_temperature, recovery_ratio_target->achieved_permeate_flow_rate.

## Arm `q091` (1 runs)

Family `s2_09`, role `real`. Column labels: patient_acuity_score, morning_HRV_rMSSD, actigraphy_wear_fraction, nurse_staffing_ratio, comfort_kit_adherence_index, arousal_threshold_index, perceived_lux_dose, comfort_bundle_offered, transfer_time_seconds, roommate_Lmax_spikes_count, cns_depressant_dose_index, planned_nursing_minutes, vital_sign_schedule_frequency, room_acoustic_reverberation_gain, perceived_noise_dose, nightly_alarm_count, night_lux_summary, alarm_quieting_bundle_state, alarm_related_LAeq, baseline_evening_pain_score, sleep_fragmentation_index, morning_pain_score. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 22.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 10.0 (1 run) | n/a | n/a |
| S2 after LLM review | 36.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 35.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 35.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 27, B 5, C 67, D 132.

**Final edges.** 35 distinct edges appear in at least one run; 35 appear in every run. Set by: llm 27, algorithm (unchanged) 8. Per run: LLM-set edges 27.0 (1 run); final edges between pairs the algorithm did not connect 20.0 (1 run); LLM additions where at least 90% of resamples had no edge 16.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| patient_acuity_score->cns_depressant_dose_index | 1 |
| patient_acuity_score->planned_nursing_minutes | 1 |
| patient_acuity_score->nightly_alarm_count | 1 |
| morning_HRV_rMSSD->cns_depressant_dose_index | 1 |
| morning_HRV_rMSSD->sleep_fragmentation_index | 1 |
| nurse_staffing_ratio->planned_nursing_minutes | 1 |
| nurse_staffing_ratio->vital_sign_schedule_frequency | 1 |
| nurse_staffing_ratio->nightly_alarm_count | 1 |
| comfort_kit_adherence_index->perceived_noise_dose | 1 |
| arousal_threshold_index->perceived_noise_dose | 1 |
| arousal_threshold_index->sleep_fragmentation_index | 1 |
| perceived_lux_dose->night_lux_summary | 1 |
| perceived_lux_dose->sleep_fragmentation_index | 1 |
| sleep_fragmentation_index->transfer_time_seconds | 1 |
| morning_pain_score o-> transfer_time_seconds | 1 |
| roommate_Lmax_spikes_count->perceived_noise_dose | 1 |
| roommate_Lmax_spikes_count->alarm_related_LAeq | 1 |
| roommate_Lmax_spikes_count->sleep_fragmentation_index | 1 |
| cns_depressant_dose_index->sleep_fragmentation_index | 1 |
| cns_depressant_dose_index->morning_pain_score | 1 |
| vital_sign_schedule_frequency->night_lux_summary | 1 |
| room_acoustic_reverberation_gain->perceived_noise_dose | 1 |
| room_acoustic_reverberation_gain->alarm_related_LAeq | 1 |
| nightly_alarm_count->perceived_noise_dose | 1 |
| alarm_quieting_bundle_state->perceived_noise_dose | 1 |
| alarm_related_LAeq->perceived_noise_dose | 1 |
| perceived_noise_dose->sleep_fragmentation_index | 1 |
| alarm_quieting_bundle_state->nightly_alarm_count | 1 |
| nightly_alarm_count->alarm_related_LAeq | 1 |
| nightly_alarm_count->sleep_fragmentation_index | 1 |
| night_lux_summary->sleep_fragmentation_index | 1 |
| alarm_quieting_bundle_state->alarm_related_LAeq | 1 |
| alarm_quieting_bundle_state->sleep_fragmentation_index | 1 |
| alarm_related_LAeq->sleep_fragmentation_index | 1 |
| baseline_evening_pain_score->morning_pain_score | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.91 (1 run) | 0.57 (1 run) | 0.70 (1 run) | 9.0 (1 run) | 0.0 (1 run) | 28.0 (1 run) | 0.90 (1 run) | 0.26 (1 run) | 0.40 (1 run) |
| S1 after bootstrap edits | 0.90 (1 run) | 0.26 (1 run) | 0.40 (1 run) | 8.0 (1 run) | 0.0 (1 run) | 28.0 (1 run) | 0.89 (1 run) | 0.23 (1 run) | 0.36 (1 run) |
| S2 after LLM review | 0.58 (1 run) | 0.60 (1 run) | 0.59 (1 run) | 18.0 (1 run) | 2.0 (1 run) | 32.0 (1 run) | 0.51 (1 run) | 0.51 (1 run) | 0.51 (1 run) |
| S3 after KCI pruning | 0.60 (1 run) | 0.60 (1 run) | 0.60 (1 run) | 18.0 (1 run) | 2.0 (1 run) | 31.0 (1 run) | 0.53 (1 run) | 0.51 (1 run) | 0.52 (1 run) |
| S4 final (after cycle step) | 0.60 (1 run) | 0.60 (1 run) | 0.60 (1 run) | 18.0 (1 run) | 2.0 (1 run) | 31.0 (1 run) | 0.53 (1 run) | 0.51 (1 run) | 0.52 (1 run) |

## Arm `q092` (1 runs)

Family `s2_09`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S1 after bootstrap edits | 15.0 (1 run) | n/a | n/a |
| S2 after LLM review | 15.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 15.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 15.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 231.

**Final edges.** 15 distinct edges appear in at least one run; 15 appear in every run. Set by: algorithm (unchanged) 15. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V01->V11 | 1 |
| V01->V12 | 1 |
| V01->V16 | 1 |
| V21 o-> V02 | 1 |
| V17->V03 | 1 |
| V04 o-> V17 | 1 |
| V05->V15 | 1 |
| V06->V20 | 1 |
| V21 o-> V09 | 1 |
| V22 o-> V09 | 1 |
| V11 <-> V20 | 1 |
| V13->V17 | 1 |
| V19->V15 | 1 |
| V18 o-> V16 | 1 |
| V16->V19 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.91 (1 run) | 0.60 (1 run) | 0.72 (1 run) | 7.0 (1 run) | 2.0 (1 run) | 30.0 (1 run) | 0.70 (1 run) | 0.20 (1 run) | 0.31 (1 run) |
| S1 after bootstrap edits | 0.87 (1 run) | 0.37 (1 run) | 0.52 (1 run) | 7.0 (1 run) | 1.0 (1 run) | 30.0 (1 run) | 0.78 (1 run) | 0.20 (1 run) | 0.32 (1 run) |
| S2 after LLM review | 0.87 (1 run) | 0.37 (1 run) | 0.52 (1 run) | 7.0 (1 run) | 1.0 (1 run) | 30.0 (1 run) | 0.78 (1 run) | 0.20 (1 run) | 0.32 (1 run) |
| S3 after KCI pruning | 0.87 (1 run) | 0.37 (1 run) | 0.52 (1 run) | 7.0 (1 run) | 1.0 (1 run) | 30.0 (1 run) | 0.78 (1 run) | 0.20 (1 run) | 0.32 (1 run) |
| S4 final (after cycle step) | 0.87 (1 run) | 0.37 (1 run) | 0.52 (1 run) | 7.0 (1 run) | 1.0 (1 run) | 30.0 (1 run) | 0.78 (1 run) | 0.20 (1 run) | 0.32 (1 run) |

## Arm `q093` (1 runs)

Family `s2_09`, role `swapped`. Column labels: morning_HRV_rMSSD, patient_acuity_score, nurse_staffing_ratio, actigraphy_wear_fraction, arousal_threshold_index, comfort_kit_adherence_index, comfort_bundle_offered, perceived_lux_dose, roommate_Lmax_spikes_count, transfer_time_seconds, planned_nursing_minutes, cns_depressant_dose_index, room_acoustic_reverberation_gain, vital_sign_schedule_frequency, nightly_alarm_count, baseline_evening_pain_score, perceived_noise_dose, night_lux_summary, sleep_fragmentation_index, alarm_quieting_bundle_state, morning_pain_score, alarm_related_LAeq. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 24.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 13.0 (1 run) | n/a | n/a |
| S2 after LLM review | 31.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 30.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 30.0 (1 run) | n/a | n/a |

**LLM review decisions.** 231 pairs. Same decision in every run: 231. Same edge/no-edge call in every run: 231. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 21, B 2, C 102, D 106.

**Final edges.** 30 distinct edges appear in at least one run; 30 appear in every run. Set by: llm 19, algorithm (unchanged) 11. Per run: LLM-set edges 19.0 (1 run); final edges between pairs the algorithm did not connect 17.0 (1 run); LLM additions where at least 90% of resamples had no edge 16.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| morning_HRV_rMSSD->planned_nursing_minutes | 1 |
| cns_depressant_dose_index->morning_HRV_rMSSD | 1 |
| morning_HRV_rMSSD->baseline_evening_pain_score | 1 |
| patient_acuity_score->nurse_staffing_ratio | 1 |
| patient_acuity_score->planned_nursing_minutes | 1 |
| morning_pain_score->patient_acuity_score | 1 |
| nurse_staffing_ratio->planned_nursing_minutes | 1 |
| actigraphy_wear_fraction->perceived_noise_dose | 1 |
| arousal_threshold_index->nightly_alarm_count | 1 |
| comfort_kit_adherence_index->comfort_bundle_offered | 1 |
| comfort_kit_adherence_index->alarm_quieting_bundle_state | 1 |
| perceived_lux_dose->night_lux_summary | 1 |
| roommate_Lmax_spikes_count->perceived_noise_dose | 1 |
| roommate_Lmax_spikes_count->sleep_fragmentation_index | 1 |
| roommate_Lmax_spikes_count <-> morning_pain_score | 1 |
| planned_nursing_minutes <-> alarm_quieting_bundle_state | 1 |
| cns_depressant_dose_index->sleep_fragmentation_index | 1 |
| room_acoustic_reverberation_gain->perceived_noise_dose | 1 |
| room_acoustic_reverberation_gain->sleep_fragmentation_index | 1 |
| room_acoustic_reverberation_gain->alarm_related_LAeq | 1 |
| vital_sign_schedule_frequency o-> sleep_fragmentation_index | 1 |
| nightly_alarm_count->perceived_noise_dose | 1 |
| nightly_alarm_count->sleep_fragmentation_index | 1 |
| nightly_alarm_count->alarm_related_LAeq | 1 |
| baseline_evening_pain_score->sleep_fragmentation_index | 1 |
| baseline_evening_pain_score->morning_pain_score | 1 |
| perceived_noise_dose->sleep_fragmentation_index | 1 |
| perceived_noise_dose->alarm_related_LAeq | 1 |
| night_lux_summary->sleep_fragmentation_index | 1 |
| alarm_quieting_bundle_state->alarm_related_LAeq | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.88 (1 run) | 0.60 (1 run) | 0.71 (1 run) | 7.0 (1 run) | 1.0 (1 run) | 31.0 (1 run) | 0.78 (1 run) | 0.20 (1 run) | 0.32 (1 run) |
| S1 after bootstrap edits | 0.92 (1 run) | 0.34 (1 run) | 0.50 (1 run) | 7.0 (1 run) | 1.0 (1 run) | 29.0 (1 run) | 0.78 (1 run) | 0.20 (1 run) | 0.32 (1 run) |
| S2 after LLM review | 0.42 (1 run) | 0.37 (1 run) | 0.39 (1 run) | 7.0 (1 run) | 3.0 (1 run) | 46.0 (1 run) | 0.25 (1 run) | 0.20 (1 run) | 0.22 (1 run) |
| S3 after KCI pruning | 0.43 (1 run) | 0.37 (1 run) | 0.40 (1 run) | 7.0 (1 run) | 3.0 (1 run) | 45.0 (1 run) | 0.26 (1 run) | 0.20 (1 run) | 0.23 (1 run) |
| S4 final (after cycle step) | 0.43 (1 run) | 0.37 (1 run) | 0.40 (1 run) | 7.0 (1 run) | 3.0 (1 run) | 45.0 (1 run) | 0.26 (1 run) | 0.20 (1 run) | 0.23 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 59.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 48.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.39 (1 run) | 0.34 (1 run) | 0.36 (1 run) | 9.0 (1 run) | 3.0 (1 run) | 45.0 (1 run) | 0.32 (1 run) | 0.26 (1 run) | 0.29 (1 run) |
| S3 after KCI pruning | 0.37 (1 run) | 0.31 (1 run) | 0.34 (1 run) | 8.0 (1 run) | 3.0 (1 run) | 46.0 (1 run) | 0.30 (1 run) | 0.23 (1 run) | 0.26 (1 run) |
| S4 final (after cycle step) | 0.37 (1 run) | 0.31 (1 run) | 0.34 (1 run) | 8.0 (1 run) | 3.0 (1 run) | 46.0 (1 run) | 0.30 (1 run) | 0.23 (1 run) | 0.26 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 11 |
| data only | 3 |
| both | 0 |
| neither | 5 |

Direction among those: data: direction as in reference 1, data: reversed 2, labels: direction as in reference 8, labels: reversed 3.
Distinct edges: data only: alarm_quieting_bundle_state->alarm_related_LAeq, cns_depressant_dose_index->morning_HRV_rMSSD, nightly_alarm_count->sleep_fragmentation_index; labels only: baseline_evening_pain_score->morning_pain_score, comfort_kit_adherence_index->comfort_bundle_offered, nightly_alarm_count->alarm_related_LAeq, nightly_alarm_count->perceived_noise_dose, nurse_staffing_ratio->planned_nursing_minutes, patient_acuity_score->planned_nursing_minutes, perceived_lux_dose->night_lux_summary, perceived_noise_dose->alarm_related_LAeq, perceived_noise_dose->sleep_fragmentation_index, room_acoustic_reverberation_gain->alarm_related_LAeq, roommate_Lmax_spikes_count->perceived_noise_dose; neither: cns_depressant_dose_index->sleep_fragmentation_index, night_lux_summary->sleep_fragmentation_index, patient_acuity_score->nurse_staffing_ratio, room_acoustic_reverberation_gain->sleep_fragmentation_index, roommate_Lmax_spikes_count->sleep_fragmentation_index.

## Arm `q102` (1 runs)

Family `s2_10`, role `neutral`. Column labels: V01, V02, V03, V04, V05, V06, V07, V08, V09, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: [] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 23.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 9.0 (1 run) | n/a | n/a |
| S2 after LLM review | 9.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 9.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 9.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: D 300.

**Final edges.** 9 distinct edges appear in at least one run; 9 appear in every run. Set by: algorithm (unchanged) 9. Per run: LLM-set edges 0.0 (1 run); final edges between pairs the algorithm did not connect 0.0 (1 run); LLM additions where at least 90% of resamples had no edge 0.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| V14->V02 | 1 |
| V02->V24 | 1 |
| V20->V04 | 1 |
| V05->V19 | 1 |
| V15 o-> V07 | 1 |
| V07 <-> V20 | 1 |
| V14 o-> V11 | 1 |
| V20->V16 | 1 |
| V23->V24 | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.74 (1 run) | 0.38 (1 run) | 0.50 (1 run) | 5.0 (1 run) | 2.0 (1 run) | 47.0 (1 run) | 0.62 (1 run) | 0.11 (1 run) | 0.19 (1 run) |
| S1 after bootstrap edits | 1.00 (1 run) | 0.20 (1 run) | 0.33 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.83 (1 run) | 0.11 (1 run) | 0.20 (1 run) |
| S2 after LLM review | 1.00 (1 run) | 0.20 (1 run) | 0.33 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.83 (1 run) | 0.11 (1 run) | 0.20 (1 run) |
| S3 after KCI pruning | 1.00 (1 run) | 0.20 (1 run) | 0.33 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.83 (1 run) | 0.11 (1 run) | 0.20 (1 run) |
| S4 final (after cycle step) | 1.00 (1 run) | 0.20 (1 run) | 0.33 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 41.0 (1 run) | 0.83 (1 run) | 0.11 (1 run) | 0.20 (1 run) |

## Arm `q103` (1 runs)

Family `s2_10`, role `swapped`. Column labels: v_review_staff, v_zoning_far, v_station_open, v_noise_complaints, v_platform_adoption, v_rent_true, v_permits_posted_obs, v_job_access_45m, v_permit_apps_true, v_noise_barrier, v_construction_cost_idx, v_walk_time_min, v_listing_coverage, v_measured_noise_dba, v_interest_rate_ann, v_vacancy_rate, v_spatial_spillover_idx, v_asking_rent_obs, v_true_noise_dba, v_permit_backlog, v_service_freq_tph, v_permit_approvals_true, v_season_regime, v_school_quality_score, v_reporting_delay_days. File path names the dataset: no.

**Choices.** Algorithm: FCI ×1. Hyperparameters passed to it: {"alpha": 0.05, "depth": 4, "indep_test": "rcit"} ×1. Proposed by the LLM but not passed: ["background_knowledge"] ×1. Served model: gpt-4o-2024-08-06.

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
| S0 algorithm output | 22.0 (1 run) | n/a | n/a |
| S1 after bootstrap edits | 12.0 (1 run) | n/a | n/a |
| S2 after LLM review | 46.0 (1 run) | n/a | n/a |
| S3 after KCI pruning | 41.0 (1 run) | n/a | n/a |
| S4 final (after cycle step) | 41.0 (1 run) | n/a | n/a |

**LLM review decisions.** 300 pairs. Same decision in every run: 300. Same edge/no-edge call in every run: 300. Mean share of runs agreeing with the commonest decision for a pair: 1.00. Letters over all runs: A 28, B 11, C 110, D 151.

**Final edges.** 41 distinct edges appear in at least one run; 41 appear in every run. Set by: llm 33, algorithm (unchanged) 8. Per run: LLM-set edges 33.0 (1 run); final edges between pairs the algorithm did not connect 31.0 (1 run); LLM additions where at least 90% of resamples had no edge 34.0 (1 run).

| Final edge | Runs (of 1) |
|---|---|
| v_review_staff->v_permits_posted_obs | 1 |
| v_review_staff->v_permit_apps_true | 1 |
| v_review_staff->v_permit_backlog | 1 |
| v_review_staff->v_permit_approvals_true | 1 |
| v_zoning_far->v_rent_true | 1 |
| v_measured_noise_dba->v_zoning_far | 1 |
| v_zoning_far->v_asking_rent_obs | 1 |
| v_zoning_far->v_school_quality_score | 1 |
| v_station_open->v_rent_true | 1 |
| v_station_open->v_job_access_45m | 1 |
| v_station_open->v_walk_time_min | 1 |
| v_station_open->v_vacancy_rate | 1 |
| v_station_open->v_spatial_spillover_idx | 1 |
| v_station_open->v_asking_rent_obs | 1 |
| v_station_open->v_service_freq_tph | 1 |
| v_true_noise_dba->v_noise_complaints | 1 |
| v_noise_complaints o-o v_permit_backlog | 1 |
| v_platform_adoption->v_true_noise_dba | 1 |
| v_vacancy_rate->v_rent_true | 1 |
| v_asking_rent_obs->v_rent_true | 1 |
| v_school_quality_score->v_rent_true | 1 |
| v_interest_rate_ann o-> v_permits_posted_obs | 1 |
| v_permits_posted_obs->v_permit_backlog | 1 |
| v_permit_approvals_true->v_permits_posted_obs | 1 |
| v_job_access_45m->v_walk_time_min | 1 |
| v_job_access_45m->v_vacancy_rate | 1 |
| v_job_access_45m->v_asking_rent_obs | 1 |
| v_job_access_45m->v_service_freq_tph | 1 |
| v_permit_apps_true->v_permit_backlog | 1 |
| v_permit_apps_true->v_permit_approvals_true | 1 |
| v_noise_barrier->v_measured_noise_dba | 1 |
| v_noise_barrier->v_true_noise_dba | 1 |
| v_measured_noise_dba->v_listing_coverage | 1 |
| v_measured_noise_dba->v_true_noise_dba | 1 |
| v_interest_rate_ann->v_vacancy_rate | 1 |
| v_interest_rate_ann->v_asking_rent_obs | 1 |
| v_vacancy_rate->v_asking_rent_obs | 1 |
| v_asking_rent_obs->v_school_quality_score | 1 |
| v_permit_approvals_true->v_permit_backlog | 1 |
| v_permit_approvals_true o-o v_season_regime | 1 |
| v_permit_approvals_true o-> v_school_quality_score | 1 |

**Accuracy by stage, scored against the reference graph read by data** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.86 (1 run) | 0.42 (1 run) | 0.57 (1 run) | 6.0 (1 run) | 3.0 (1 run) | 44.0 (1 run) | 0.60 (1 run) | 0.13 (1 run) | 0.22 (1 run) |
| S1 after bootstrap edits | 0.92 (1 run) | 0.24 (1 run) | 0.39 (1 run) | 5.0 (1 run) | 1.0 (1 run) | 43.0 (1 run) | 0.83 (1 run) | 0.11 (1 run) | 0.20 (1 run) |
| S2 after LLM review | 0.24 (1 run) | 0.24 (1 run) | 0.24 (1 run) | 6.0 (1 run) | 2.0 (1 run) | 76.0 (1 run) | 0.14 (1 run) | 0.13 (1 run) | 0.14 (1 run) |
| S3 after KCI pruning | 0.27 (1 run) | 0.24 (1 run) | 0.26 (1 run) | 6.0 (1 run) | 2.0 (1 run) | 71.0 (1 run) | 0.16 (1 run) | 0.13 (1 run) | 0.15 (1 run) |
| S4 final (after cycle step) | 0.27 (1 run) | 0.24 (1 run) | 0.26 (1 run) | 6.0 (1 run) | 2.0 (1 run) | 71.0 (1 run) | 0.16 (1 run) | 0.13 (1 run) | 0.15 (1 run) |

**Accuracy by stage, scored against the reference graph read by label** (mean ± sample s.d. over runs).

| Stage | adj precision | adj recall | adj F1 | reference edges directed correctly | reversed | SHD vs CPDAG | directed-edge precision | recall | F1 |
|---|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 67.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S1 after bootstrap edits | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.0 (1 run) | 0.0 (1 run) | 57.0 (1 run) | 0.00 (1 run) | 0.00 (1 run) | 0.00 (1 run) |
| S2 after LLM review | 0.41 (1 run) | 0.42 (1 run) | 0.42 (1 run) | 13.0 (1 run) | 6.0 (1 run) | 59.0 (1 run) | 0.31 (1 run) | 0.29 (1 run) | 0.30 (1 run) |
| S3 after KCI pruning | 0.41 (1 run) | 0.38 (1 run) | 0.40 (1 run) | 11.0 (1 run) | 6.0 (1 run) | 58.0 (1 run) | 0.30 (1 run) | 0.24 (1 run) | 0.27 (1 run) |
| S4 final (after cycle step) | 0.41 (1 run) | 0.38 (1 run) | 0.40 (1 run) | 11.0 (1 run) | 6.0 (1 run) | 58.0 (1 run) | 0.30 (1 run) | 0.24 (1 run) | 0.27 (1 run) |

**Do the LLM-set edges follow the labels or the data?** Every directed final edge that the LLM review set, over all runs, classified by which reference graph has that pair adjacent.

| Follows | Edges |
|---|---|
| labels only | 17 |
| data only | 4 |
| both | 0 |
| neither | 12 |

Direction among those: data: direction as in reference 2, data: reversed 2, labels: direction as in reference 11, labels: reversed 6.
Distinct edges: data only: v_interest_rate_ann->v_asking_rent_obs, v_interest_rate_ann->v_vacancy_rate, v_permits_posted_obs->v_permit_backlog, v_station_open->v_vacancy_rate; labels only: v_asking_rent_obs->v_rent_true, v_job_access_45m->v_service_freq_tph, v_job_access_45m->v_walk_time_min, v_measured_noise_dba->v_true_noise_dba, v_noise_barrier->v_true_noise_dba, v_permit_approvals_true->v_permit_backlog, v_permit_approvals_true->v_permits_posted_obs, v_permit_apps_true->v_permit_backlog, v_review_staff->v_permit_approvals_true, v_review_staff->v_permit_backlog, v_school_quality_score->v_rent_true, v_station_open->v_job_access_45m, v_station_open->v_service_freq_tph, v_station_open->v_spatial_spillover_idx, v_true_noise_dba->v_noise_complaints, v_vacancy_rate->v_asking_rent_obs, v_vacancy_rate->v_rent_true; neither: v_asking_rent_obs->v_school_quality_score, v_job_access_45m->v_asking_rent_obs, v_job_access_45m->v_vacancy_rate, v_noise_barrier->v_measured_noise_dba, v_permit_apps_true->v_permit_approvals_true, v_review_staff->v_permit_apps_true, v_review_staff->v_permits_posted_obs, v_station_open->v_asking_rent_obs, v_station_open->v_rent_true, v_station_open->v_walk_time_min, v_zoning_far->v_asking_rent_obs, v_zoning_far->v_rent_true.

## Predictions fixed before the data

- **N1**: {"what": "swapped arms, distinct (family, edge): LLM-set final edges adjacent in exactly one reference", "labels_only": 81, "data_only": 20, "neither": 74, "share_following_labels": 0.801980198019802, "verdict": "SUPPORTED"}
- **N2**: {"what": "mean LLM-set final edges per run, neutral names at most half of real names, per family", "families": {"s2_02": {"real": 17, "neutral": 0, "holds": true}, "s2_03": {"real": 14, "neutral": 0, "holds": true}, "s2_06": {"real": 15, "neutral": 0, "holds": true}, "s2_08": {"real": 35, "neutral": 0, "holds": true}, "s2_09": {"real": 27, "neutral": 0, "holds": true}}, "testable_families": 5, "held_in": 5, "verdict": "SUPPORTED"}
- **N4**: {"what": "runs whose final graph has lower adjacency F1 than the algorithm's own output", "runs": 24, "below": 23, "share": 0.9583333333333334, "verdict": "SUPPORTED"}
- **N5**: {"what": "exploratory: mean F1 by role over all runs, scored against the data-side reference or ground truth", "by_role": {"real": {"runs": 5, "directed_edge_f1_algorithm_output": 0.18982598590824176, "directed_edge_f1_final": 0.26647937076160466, "adjacency_f1_algorithm_output": 0.5399650771631053, "adjacency_f1_final": 0.4102549218568424}, "neutral": {"runs": 10, "directed_edge_f1_algorithm_output": 0.21068470394098923, "directed_edge_f1_final": 0.19314032868127953, "adjacency_f1_algorithm_output": 0.5845894542589866, "adjacency_f1_final": 0.31511759761830316}, "swapped": {"runs": 9, "directed_edge_f1_algorithm_output": 0.2250637252548466, "directed_edge_f1_final": 0.12383532738666668, "adjacency_f1_algorithm_output": 0.5998139543575716, "adjacency_f1_final": 0.22765856055848294}}, "verdict": "exploratory"}
- **P3**: {"distinct_outputs_counted": 24, "nondirected_edges_in_algorithm_output": 378, "of_which_still_adjacent_after_bootstrap_step": 73, "share": 0.1931216931216931, "directed_edges": 163, "directed_still_adjacent": 131, "verdict": "SUPPORTED"}
- **P5**: {"arms": 24, "arms_with_more_than_one_algorithm": 0, "verdict": "exploratory"}

## Gates

- T1_no_arm_left_empty: **FAIL**
- T2_min_runs_per_arm: **PASS**
- T3_same_dataset_bytes: **PASS**
- T4_variable_names_match_arm: **PASS**
- T5_scores_recomputed_equal_lineage: **PASS**
- T6_one_model_snapshot_per_arm (report only): **PASS**
