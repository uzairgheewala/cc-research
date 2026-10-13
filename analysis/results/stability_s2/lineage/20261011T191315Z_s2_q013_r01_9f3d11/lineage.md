# Edge lineage: 20261011T191315Z_s2_q013_r01_9f3d11

Dataset `/research/datasets/suite_q1s2/q013/q013.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 23 variables, 253 pairs. 20 bootstrap resamples.

Hyperparameters the LLM proposed that were not passed to the algorithm: ['background_knowledge']

## Gates

- A_S0_equals_state_converted_graph: **PASS**
- B_rebuilt_S2_equals_graph_into_KCI: **PASS**
- C_rebuilt_S3_equals_graph_into_cycle_step: **PASS**
- D_cycle_output_equals_state_revised_graph: **PASS**
- E_every_change_covered_by_step_evidence: **PASS**
- F_all_llm_answers_name_dataset_variables: **PASS**

## Edges by stage

| Stage | Adjacent pairs | adj P | adj R | adj F1 | true edges directed correctly | reversed | present, not directed | SHD vs CPDAG |
|---|---|---|---|---|---|---|---|---|
| S0 algorithm output | 26 | 0.81 | 0.54 | 0.65 | 6 | 2 | 13 | 40 |
| S1 after bootstrap edits | 10 | 1.00 | 0.26 | 0.41 | 5 | 2 | 3 | 35 |
| S2 after LLM review | 21 | 0.52 | 0.28 | 0.37 | 4 | 4 | 3 | 45 |
| S3 after KCI pruning | 18 | 0.61 | 0.28 | 0.39 | 4 | 4 | 3 | 42 |
| S4 final (after cycle step) | 18 | 0.61 | 0.28 | 0.39 | 4 | 4 | 3 | 42 |

Scored against: reference graph s2_01_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 16. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 23 calls, 253 distinct pairs answered out of 253, plus 23 self-pairs. Letters: {"A": 12, "B": 3, "C": 58, "D": 180}.
- LLM effect: added 11 (of which 11 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 1.
- KCI step removed 3. Cycle step changed 0.
- Final graph: 18 edges; set by {"llm": 9, "algorithm (unchanged)": 9}; 9 identical to the algorithm's output; 8 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| oven_leak_index->cooling_rate_C_per_s | llm | no | 1.00 |
| oven_leak_index->realized_peak_temp_C | llm | no | 1.00 |
| oven_leak_index->conv_speed_cm_min | algorithm (unchanged) | yes | 0.00 |
| component_thermal_mass_index->realized_ramp_rate_C_per_s | llm | no | 1.00 |
| component_thermal_mass_index->cooling_rate_C_per_s | llm | no | 1.00 |
| realized_ramp_rate_C_per_s ~~~ package_family_code | algorithm (unchanged) | yes | 0.00 |
| measured_void_fraction->true_void_fraction | llm | no | 1.00 |
| flux_lot_activity_index o-> oxygen_ppm | algorithm (unchanged) | yes | 0.00 |
| flux_lot_activity_index->residual_entrained_gas_mg | algorithm (unchanged) | yes | 0.15 |
| paste_solvent_mass_fraction->volatile_generation_cumulative_mg | llm | no | 1.00 |
| paste_solvent_mass_fraction->wetting_index | llm | no | 1.00 |
| paste_solvent_mass_fraction->true_void_fraction | algorithm (unchanged) | yes | 0.35 |
| peak_zone_setpoint_C->paste_solvent_mass_fraction | algorithm (unchanged) | yes | 0.15 |
| pad_finish <-> volatile_generation_cumulative_mg | algorithm (unchanged) | yes | 0.30 |
| volatile_generation_cumulative_mg->preheat_soak_setpoint_C | llm | yes | 0.00 |
| true_void_fraction->package_family_code | algorithm (unchanged) | yes | 0.00 |
| realized_peak_temp_C->conv_speed_cm_min | llm | no | 1.00 |
| peak_zone_setpoint_C->electrical_resistance_mOhm | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| oven_leak_index, measured_void_fraction | oven_leak_index <-> measured_void_fraction | oven_leak_index   measured_void_fraction (no edge) | oven_leak_index   measured_void_fraction (no edge) | oven_leak_index   measured_void_fraction (no edge) | oven_leak_index   measured_void_fraction (no edge) | oven_leak_index -> measured_void_fraction | (oven_leak_index, measured_void_fraction)=D |
| oven_leak_index, oxygen_ppm | oven_leak_index <-> oxygen_ppm | oven_leak_index   oxygen_ppm (no edge) | oven_leak_index   oxygen_ppm (no edge) | oven_leak_index   oxygen_ppm (no edge) | oven_leak_index   oxygen_ppm (no edge) | no edge | (oven_leak_index, oxygen_ppm)=D |
| oven_leak_index, cooling_rate_C_per_s | oven_leak_index   cooling_rate_C_per_s (no edge) | oven_leak_index   cooling_rate_C_per_s (no edge) | oven_leak_index->cooling_rate_C_per_s | oven_leak_index->cooling_rate_C_per_s | oven_leak_index->cooling_rate_C_per_s | no edge | (oven_leak_index, cooling_rate_C_per_s)=A |
| oven_leak_index, realized_peak_temp_C | oven_leak_index   realized_peak_temp_C (no edge) | oven_leak_index   realized_peak_temp_C (no edge) | oven_leak_index->realized_peak_temp_C | oven_leak_index->realized_peak_temp_C | oven_leak_index->realized_peak_temp_C | no edge | (oven_leak_index, realized_peak_temp_C)=A |
| component_thermal_mass_index, realized_ramp_rate_C_per_s | component_thermal_mass_index   realized_ramp_rate_C_per_s (no edge) | component_thermal_mass_index   realized_ramp_rate_C_per_s (no edge) | component_thermal_mass_index->realized_ramp_rate_C_per_s | component_thermal_mass_index->realized_ramp_rate_C_per_s | component_thermal_mass_index->realized_ramp_rate_C_per_s | no edge | (component_thermal_mass_index, realized_ramp_rate_C_per_s)=A |
| component_thermal_mass_index, TAL_s | component_thermal_mass_index o-> TAL_s | component_thermal_mass_index   TAL_s (no edge) | component_thermal_mass_index   TAL_s (no edge) | component_thermal_mass_index   TAL_s (no edge) | component_thermal_mass_index   TAL_s (no edge) | component_thermal_mass_index -> TAL_s | (component_thermal_mass_index, TAL_s)=C |
| component_thermal_mass_index, cooling_rate_C_per_s | component_thermal_mass_index   cooling_rate_C_per_s (no edge) | component_thermal_mass_index   cooling_rate_C_per_s (no edge) | component_thermal_mass_index->cooling_rate_C_per_s | component_thermal_mass_index->cooling_rate_C_per_s | component_thermal_mass_index->cooling_rate_C_per_s | no edge | (component_thermal_mass_index, cooling_rate_C_per_s)=A |
| realized_ramp_rate_C_per_s, true_void_fraction | true_void_fraction->realized_ramp_rate_C_per_s | realized_ramp_rate_C_per_s   true_void_fraction (no edge) | realized_ramp_rate_C_per_s   true_void_fraction (no edge) | realized_ramp_rate_C_per_s   true_void_fraction (no edge) | realized_ramp_rate_C_per_s   true_void_fraction (no edge) | no edge | (realized_ramp_rate_C_per_s, true_void_fraction)=D |
| measured_void_fraction, true_void_fraction | measured_void_fraction   true_void_fraction (no edge) | measured_void_fraction   true_void_fraction (no edge) | measured_void_fraction->true_void_fraction | measured_void_fraction->true_void_fraction | measured_void_fraction->true_void_fraction | no edge | (measured_void_fraction, true_void_fraction)=A |
| measured_void_fraction, realized_peak_temp_C | measured_void_fraction <-> realized_peak_temp_C | measured_void_fraction   realized_peak_temp_C (no edge) | measured_void_fraction   realized_peak_temp_C (no edge) | measured_void_fraction   realized_peak_temp_C (no edge) | measured_void_fraction   realized_peak_temp_C (no edge) | realized_peak_temp_C -> measured_void_fraction | (measured_void_fraction, realized_peak_temp_C)=D |
| measured_void_fraction, paste_batch_context | measured_void_fraction <-> paste_batch_context | measured_void_fraction   paste_batch_context (no edge) | measured_void_fraction   paste_batch_context (no edge) | measured_void_fraction   paste_batch_context (no edge) | measured_void_fraction   paste_batch_context (no edge) | paste_batch_context -> measured_void_fraction | (measured_void_fraction, paste_batch_context)=D |
| oxygen_ppm, nitrogen_flow_setpoint_slpm | oxygen_ppm   nitrogen_flow_setpoint_slpm (no edge) | oxygen_ppm   nitrogen_flow_setpoint_slpm (no edge) | nitrogen_flow_setpoint_slpm->oxygen_ppm | oxygen_ppm   nitrogen_flow_setpoint_slpm (no edge) | oxygen_ppm   nitrogen_flow_setpoint_slpm (no edge) | no edge | (oxygen_ppm, nitrogen_flow_setpoint_slpm)=B |
| oxygen_ppm, realized_peak_temp_C | oxygen_ppm <-> realized_peak_temp_C | oxygen_ppm   realized_peak_temp_C (no edge) | oxygen_ppm   realized_peak_temp_C (no edge) | oxygen_ppm   realized_peak_temp_C (no edge) | oxygen_ppm   realized_peak_temp_C (no edge) | realized_peak_temp_C -> oxygen_ppm | (oxygen_ppm, realized_peak_temp_C)=D |
| TAL_s, cooling_rate_C_per_s | TAL_s <-> cooling_rate_C_per_s | TAL_s   cooling_rate_C_per_s (no edge) | TAL_s   cooling_rate_C_per_s (no edge) | TAL_s   cooling_rate_C_per_s (no edge) | TAL_s   cooling_rate_C_per_s (no edge) | cooling_rate_C_per_s -> TAL_s | (TAL_s, cooling_rate_C_per_s)=D |
| microstructure_index, preheat_soak_setpoint_C | microstructure_index o-o preheat_soak_setpoint_C | microstructure_index   preheat_soak_setpoint_C (no edge) | microstructure_index   preheat_soak_setpoint_C (no edge) | microstructure_index   preheat_soak_setpoint_C (no edge) | microstructure_index   preheat_soak_setpoint_C (no edge) | preheat_soak_setpoint_C -> microstructure_index | (microstructure_index, preheat_soak_setpoint_C)=D |
| flux_lot_activity_index, peak_zone_setpoint_C | flux_lot_activity_index o-> peak_zone_setpoint_C | flux_lot_activity_index   peak_zone_setpoint_C (no edge) | flux_lot_activity_index   peak_zone_setpoint_C (no edge) | flux_lot_activity_index   peak_zone_setpoint_C (no edge) | flux_lot_activity_index   peak_zone_setpoint_C (no edge) | peak_zone_setpoint_C -> flux_lot_activity_index | (flux_lot_activity_index, peak_zone_setpoint_C)=D |
| cooling_rate_C_per_s, paste_batch_context | cooling_rate_C_per_s <-> paste_batch_context | cooling_rate_C_per_s   paste_batch_context (no edge) | cooling_rate_C_per_s   paste_batch_context (no edge) | cooling_rate_C_per_s   paste_batch_context (no edge) | cooling_rate_C_per_s   paste_batch_context (no edge) | no edge | (cooling_rate_C_per_s, paste_batch_context)=C |
| paste_solvent_mass_fraction, volatile_generation_cumulative_mg | paste_solvent_mass_fraction   volatile_generation_cumulative_mg (no edge) | paste_solvent_mass_fraction   volatile_generation_cumulative_mg (no edge) | paste_solvent_mass_fraction->volatile_generation_cumulative_mg | paste_solvent_mass_fraction->volatile_generation_cumulative_mg | paste_solvent_mass_fraction->volatile_generation_cumulative_mg | no edge | (paste_solvent_mass_fraction, volatile_generation_cumulative_mg)=A |
| paste_solvent_mass_fraction, wetting_index | paste_solvent_mass_fraction   wetting_index (no edge) | paste_solvent_mass_fraction   wetting_index (no edge) | paste_solvent_mass_fraction->wetting_index | paste_solvent_mass_fraction->wetting_index | paste_solvent_mass_fraction->wetting_index | wetting_index -> paste_solvent_mass_fraction | (paste_solvent_mass_fraction, wetting_index)=A |
| nitrogen_flow_setpoint_slpm, realized_peak_temp_C | nitrogen_flow_setpoint_slpm <-> realized_peak_temp_C | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | realized_peak_temp_C -> nitrogen_flow_setpoint_slpm | (nitrogen_flow_setpoint_slpm, realized_peak_temp_C)=D |
| nitrogen_flow_setpoint_slpm, peak_zone_setpoint_C | nitrogen_flow_setpoint_slpm <-> peak_zone_setpoint_C | nitrogen_flow_setpoint_slpm   peak_zone_setpoint_C (no edge) | nitrogen_flow_setpoint_slpm   peak_zone_setpoint_C (no edge) | nitrogen_flow_setpoint_slpm   peak_zone_setpoint_C (no edge) | nitrogen_flow_setpoint_slpm   peak_zone_setpoint_C (no edge) | peak_zone_setpoint_C -> nitrogen_flow_setpoint_slpm | (nitrogen_flow_setpoint_slpm, peak_zone_setpoint_C)=C |
| pad_finish, residual_entrained_gas_mg | pad_finish <-> residual_entrained_gas_mg | pad_finish   residual_entrained_gas_mg (no edge) | pad_finish   residual_entrained_gas_mg (no edge) | pad_finish   residual_entrained_gas_mg (no edge) | pad_finish   residual_entrained_gas_mg (no edge) | no edge | (pad_finish, residual_entrained_gas_mg)=D |
| volatile_generation_cumulative_mg, preheat_soak_setpoint_C | preheat_soak_setpoint_C->volatile_generation_cumulative_mg | preheat_soak_setpoint_C->volatile_generation_cumulative_mg | volatile_generation_cumulative_mg->preheat_soak_setpoint_C | volatile_generation_cumulative_mg->preheat_soak_setpoint_C | volatile_generation_cumulative_mg->preheat_soak_setpoint_C | preheat_soak_setpoint_C -> volatile_generation_cumulative_mg | (volatile_generation_cumulative_mg, preheat_soak_setpoint_C)=A |
| wetting_index, conv_speed_cm_min | conv_speed_cm_min->wetting_index | wetting_index   conv_speed_cm_min (no edge) | wetting_index   conv_speed_cm_min (no edge) | wetting_index   conv_speed_cm_min (no edge) | wetting_index   conv_speed_cm_min (no edge) | conv_speed_cm_min -> wetting_index | (wetting_index, conv_speed_cm_min)=C |
| true_void_fraction, residual_entrained_gas_mg | true_void_fraction->residual_entrained_gas_mg | true_void_fraction   residual_entrained_gas_mg (no edge) | true_void_fraction   residual_entrained_gas_mg (no edge) | true_void_fraction   residual_entrained_gas_mg (no edge) | true_void_fraction   residual_entrained_gas_mg (no edge) | no edge | (true_void_fraction, residual_entrained_gas_mg)=D |
| realized_peak_temp_C, conv_speed_cm_min | realized_peak_temp_C   conv_speed_cm_min (no edge) | realized_peak_temp_C   conv_speed_cm_min (no edge) | realized_peak_temp_C->conv_speed_cm_min | realized_peak_temp_C->conv_speed_cm_min | realized_peak_temp_C->conv_speed_cm_min | no edge | (realized_peak_temp_C, conv_speed_cm_min)=A |
| realized_peak_temp_C, peak_zone_setpoint_C | realized_peak_temp_C   peak_zone_setpoint_C (no edge) | realized_peak_temp_C   peak_zone_setpoint_C (no edge) | peak_zone_setpoint_C->realized_peak_temp_C | realized_peak_temp_C   peak_zone_setpoint_C (no edge) | realized_peak_temp_C   peak_zone_setpoint_C (no edge) | no edge | (realized_peak_temp_C, peak_zone_setpoint_C)=B |
| realized_peak_temp_C, preheat_soak_setpoint_C | realized_peak_temp_C   preheat_soak_setpoint_C (no edge) | realized_peak_temp_C   preheat_soak_setpoint_C (no edge) | preheat_soak_setpoint_C->realized_peak_temp_C | realized_peak_temp_C   preheat_soak_setpoint_C (no edge) | realized_peak_temp_C   preheat_soak_setpoint_C (no edge) | no edge | (realized_peak_temp_C, preheat_soak_setpoint_C)=B |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
