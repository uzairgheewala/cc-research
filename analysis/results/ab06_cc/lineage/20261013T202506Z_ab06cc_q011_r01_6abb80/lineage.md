# Edge lineage: 20261013T202506Z_ab06cc_q011_r01_6abb80

Dataset `/research/datasets/suite_q1s2/q011/q011.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 23 variables, 253 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 26 | 0.85 | 0.56 | 0.68 | 5 | 2 | 15 | 38 |
| S1 after bootstrap edits | 13 | 1.00 | 0.33 | 0.50 | 5 | 2 | 6 | 34 |
| S2 after LLM review | 41 | 0.37 | 0.38 | 0.37 | 7 | 7 | 1 | 58 |
| S3 after KCI pruning | 41 | 0.37 | 0.38 | 0.37 | 7 | 7 | 1 | 58 |
| S4 final (after cycle step) | 41 | 0.37 | 0.38 | 0.37 | 7 | 7 | 1 | 58 |

Scored against: reference graph s2_01_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 13. Of the deleted, 7 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 23 calls, 253 distinct pairs answered out of 253, plus 23 self-pairs. Letters: {"A": 40, "C": 205, "D": 8}.
- LLM effect: added 35 (of which 30 where the resamples showed no edge at frequency >= 0.9), removed 7, re-oriented 2.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 41 edges; set by {"algorithm (unchanged)": 4, "llm": 37}; 4 identical to the algorithm's output; 32 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| component_thermal_mass_index->realized_ramp_rate_C_per_s | algorithm (unchanged) | yes | 0.00 |
| component_thermal_mass_index->microstructure_index | llm | no | 0.95 |
| component_thermal_mass_index->wetting_index | llm | no | 1.00 |
| component_thermal_mass_index->cooling_rate_C_per_s | llm | no | 1.00 |
| component_thermal_mass_index->realized_peak_temp_C | llm | no | 1.00 |
| component_thermal_mass_index->peak_zone_setpoint_C | llm | no | 1.00 |
| component_thermal_mass_index->preheat_soak_setpoint_C | llm | no | 1.00 |
| oven_leak_index->realized_ramp_rate_C_per_s | llm | no | 1.00 |
| oven_leak_index->oxygen_ppm | llm | yes | 0.00 |
| oven_leak_index->cooling_rate_C_per_s | llm | no | 1.00 |
| oven_leak_index->volatile_generation_cumulative_mg | llm | no | 1.00 |
| oven_leak_index->realized_peak_temp_C | llm | no | 1.00 |
| oven_leak_index->peak_zone_setpoint_C | llm | no | 1.00 |
| oven_leak_index->preheat_soak_setpoint_C | llm | no | 1.00 |
| measured_void_fraction->true_void_fraction | llm | yes | 0.00 |
| realized_ramp_rate_C_per_s->cooling_rate_C_per_s | llm | no | 1.00 |
| realized_ramp_rate_C_per_s->realized_peak_temp_C | llm | no | 1.00 |
| realized_ramp_rate_C_per_s->peak_zone_setpoint_C | llm | no | 1.00 |
| realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | llm | yes | 0.05 |
| TAL_s->realized_peak_temp_C | llm | no | 1.00 |
| oxygen_ppm->volatile_generation_cumulative_mg | llm | no | 1.00 |
| flux_lot_activity_index->wetting_index | algorithm (unchanged) | yes | 0.50 |
| flux_lot_activity_index->volatile_generation_cumulative_mg | llm | no | 1.00 |
| microstructure_index->wetting_index | llm | no | 1.00 |
| microstructure_index->true_void_fraction | llm | no | 1.00 |
| microstructure_index o-o realized_peak_temp_C | algorithm (unchanged) | yes | 0.00 |
| microstructure_index->electrical_resistance_mOhm | algorithm (unchanged) | yes | 0.20 |
| nitrogen_flow_setpoint_slpm->volatile_generation_cumulative_mg | llm | no | 1.00 |
| nitrogen_flow_setpoint_slpm->residual_entrained_gas_mg | llm | no | 1.00 |
| nitrogen_flow_setpoint_slpm->realized_peak_temp_C | llm | no | 1.00 |
| wetting_index->paste_solvent_mass_fraction | llm | no | 1.00 |
| cooling_rate_C_per_s->realized_peak_temp_C | llm | no | 0.65 |
| volatile_generation_cumulative_mg->paste_solvent_mass_fraction | llm | yes | 0.15 |
| volatile_generation_cumulative_mg->residual_entrained_gas_mg | llm | no | 0.95 |
| volatile_generation_cumulative_mg->realized_peak_temp_C | llm | no | 0.80 |
| volatile_generation_cumulative_mg->peak_zone_setpoint_C | llm | no | 1.00 |
| volatile_generation_cumulative_mg->preheat_soak_setpoint_C | llm | no | 1.00 |
| paste_solvent_mass_fraction->true_void_fraction | llm | no | 1.00 |
| realized_peak_temp_C->peak_zone_setpoint_C | llm | yes | 0.00 |
| realized_peak_temp_C->preheat_soak_setpoint_C | llm | no | 1.00 |
| peak_zone_setpoint_C->preheat_soak_setpoint_C | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| component_thermal_mass_index, microstructure_index | component_thermal_mass_index   microstructure_index (no edge) | component_thermal_mass_index   microstructure_index (no edge) | component_thermal_mass_index->microstructure_index | component_thermal_mass_index->microstructure_index | component_thermal_mass_index->microstructure_index | no edge | (component_thermal_mass_index, microstructure_index)=A |
| component_thermal_mass_index, wetting_index | component_thermal_mass_index   wetting_index (no edge) | component_thermal_mass_index   wetting_index (no edge) | component_thermal_mass_index->wetting_index | component_thermal_mass_index->wetting_index | component_thermal_mass_index->wetting_index | no edge | (component_thermal_mass_index, wetting_index)=A |
| component_thermal_mass_index, cooling_rate_C_per_s | component_thermal_mass_index   cooling_rate_C_per_s (no edge) | component_thermal_mass_index   cooling_rate_C_per_s (no edge) | component_thermal_mass_index->cooling_rate_C_per_s | component_thermal_mass_index->cooling_rate_C_per_s | component_thermal_mass_index->cooling_rate_C_per_s | no edge | (component_thermal_mass_index, cooling_rate_C_per_s)=A |
| component_thermal_mass_index, package_family_code | component_thermal_mass_index o-o package_family_code | component_thermal_mass_index o-o package_family_code | component_thermal_mass_index   package_family_code (no edge) | component_thermal_mass_index   package_family_code (no edge) | component_thermal_mass_index   package_family_code (no edge) | package_family_code -> component_thermal_mass_index | (component_thermal_mass_index, package_family_code)=C |
| component_thermal_mass_index, realized_peak_temp_C | component_thermal_mass_index   realized_peak_temp_C (no edge) | component_thermal_mass_index   realized_peak_temp_C (no edge) | component_thermal_mass_index->realized_peak_temp_C | component_thermal_mass_index->realized_peak_temp_C | component_thermal_mass_index->realized_peak_temp_C | component_thermal_mass_index -> realized_peak_temp_C | (component_thermal_mass_index, realized_peak_temp_C)=A |
| component_thermal_mass_index, peak_zone_setpoint_C | component_thermal_mass_index   peak_zone_setpoint_C (no edge) | component_thermal_mass_index   peak_zone_setpoint_C (no edge) | component_thermal_mass_index->peak_zone_setpoint_C | component_thermal_mass_index->peak_zone_setpoint_C | component_thermal_mass_index->peak_zone_setpoint_C | no edge | (component_thermal_mass_index, peak_zone_setpoint_C)=A |
| component_thermal_mass_index, preheat_soak_setpoint_C | component_thermal_mass_index   preheat_soak_setpoint_C (no edge) | component_thermal_mass_index   preheat_soak_setpoint_C (no edge) | component_thermal_mass_index->preheat_soak_setpoint_C | component_thermal_mass_index->preheat_soak_setpoint_C | component_thermal_mass_index->preheat_soak_setpoint_C | no edge | (component_thermal_mass_index, preheat_soak_setpoint_C)=A |
| oven_leak_index, realized_ramp_rate_C_per_s | oven_leak_index   realized_ramp_rate_C_per_s (no edge) | oven_leak_index   realized_ramp_rate_C_per_s (no edge) | oven_leak_index->realized_ramp_rate_C_per_s | oven_leak_index->realized_ramp_rate_C_per_s | oven_leak_index->realized_ramp_rate_C_per_s | no edge | (oven_leak_index, realized_ramp_rate_C_per_s)=A |
| oven_leak_index, oxygen_ppm | oven_leak_index o-> oxygen_ppm | oven_leak_index   oxygen_ppm (no edge) | oven_leak_index->oxygen_ppm | oven_leak_index->oxygen_ppm | oven_leak_index->oxygen_ppm | oven_leak_index -> oxygen_ppm | (oven_leak_index, oxygen_ppm)=A |
| oven_leak_index, cooling_rate_C_per_s | oven_leak_index   cooling_rate_C_per_s (no edge) | oven_leak_index   cooling_rate_C_per_s (no edge) | oven_leak_index->cooling_rate_C_per_s | oven_leak_index->cooling_rate_C_per_s | oven_leak_index->cooling_rate_C_per_s | no edge | (oven_leak_index, cooling_rate_C_per_s)=A |
| oven_leak_index, volatile_generation_cumulative_mg | oven_leak_index   volatile_generation_cumulative_mg (no edge) | oven_leak_index   volatile_generation_cumulative_mg (no edge) | oven_leak_index->volatile_generation_cumulative_mg | oven_leak_index->volatile_generation_cumulative_mg | oven_leak_index->volatile_generation_cumulative_mg | no edge | (oven_leak_index, volatile_generation_cumulative_mg)=A |
| oven_leak_index, realized_peak_temp_C | oven_leak_index   realized_peak_temp_C (no edge) | oven_leak_index   realized_peak_temp_C (no edge) | oven_leak_index->realized_peak_temp_C | oven_leak_index->realized_peak_temp_C | oven_leak_index->realized_peak_temp_C | no edge | (oven_leak_index, realized_peak_temp_C)=A |
| oven_leak_index, peak_zone_setpoint_C | oven_leak_index   peak_zone_setpoint_C (no edge) | oven_leak_index   peak_zone_setpoint_C (no edge) | oven_leak_index->peak_zone_setpoint_C | oven_leak_index->peak_zone_setpoint_C | oven_leak_index->peak_zone_setpoint_C | no edge | (oven_leak_index, peak_zone_setpoint_C)=A |
| oven_leak_index, preheat_soak_setpoint_C | oven_leak_index   preheat_soak_setpoint_C (no edge) | oven_leak_index   preheat_soak_setpoint_C (no edge) | oven_leak_index->preheat_soak_setpoint_C | oven_leak_index->preheat_soak_setpoint_C | oven_leak_index->preheat_soak_setpoint_C | no edge | (oven_leak_index, preheat_soak_setpoint_C)=A |
| measured_void_fraction, residual_entrained_gas_mg | measured_void_fraction o-o residual_entrained_gas_mg | measured_void_fraction   residual_entrained_gas_mg (no edge) | measured_void_fraction   residual_entrained_gas_mg (no edge) | measured_void_fraction   residual_entrained_gas_mg (no edge) | measured_void_fraction   residual_entrained_gas_mg (no edge) | no edge | (measured_void_fraction, residual_entrained_gas_mg)=C |
| measured_void_fraction, true_void_fraction | measured_void_fraction ~~~ true_void_fraction | measured_void_fraction ~~~ true_void_fraction | measured_void_fraction->true_void_fraction | measured_void_fraction->true_void_fraction | measured_void_fraction->true_void_fraction | true_void_fraction -> measured_void_fraction | (measured_void_fraction, true_void_fraction)=A |
| measured_void_fraction, electrical_resistance_mOhm | measured_void_fraction o-> electrical_resistance_mOhm | measured_void_fraction   electrical_resistance_mOhm (no edge) | measured_void_fraction   electrical_resistance_mOhm (no edge) | measured_void_fraction   electrical_resistance_mOhm (no edge) | measured_void_fraction   electrical_resistance_mOhm (no edge) | no edge | (measured_void_fraction, electrical_resistance_mOhm)=C |
| realized_ramp_rate_C_per_s, cooling_rate_C_per_s | realized_ramp_rate_C_per_s   cooling_rate_C_per_s (no edge) | realized_ramp_rate_C_per_s   cooling_rate_C_per_s (no edge) | realized_ramp_rate_C_per_s->cooling_rate_C_per_s | realized_ramp_rate_C_per_s->cooling_rate_C_per_s | realized_ramp_rate_C_per_s->cooling_rate_C_per_s | no edge | (realized_ramp_rate_C_per_s, cooling_rate_C_per_s)=A |
| realized_ramp_rate_C_per_s, conv_speed_cm_min | realized_ramp_rate_C_per_s <-> conv_speed_cm_min | realized_ramp_rate_C_per_s   conv_speed_cm_min (no edge) | realized_ramp_rate_C_per_s   conv_speed_cm_min (no edge) | realized_ramp_rate_C_per_s   conv_speed_cm_min (no edge) | realized_ramp_rate_C_per_s   conv_speed_cm_min (no edge) | conv_speed_cm_min -> realized_ramp_rate_C_per_s | (realized_ramp_rate_C_per_s, conv_speed_cm_min)=C |
| realized_ramp_rate_C_per_s, realized_peak_temp_C | realized_ramp_rate_C_per_s   realized_peak_temp_C (no edge) | realized_ramp_rate_C_per_s   realized_peak_temp_C (no edge) | realized_ramp_rate_C_per_s->realized_peak_temp_C | realized_ramp_rate_C_per_s->realized_peak_temp_C | realized_ramp_rate_C_per_s->realized_peak_temp_C | no edge | (realized_ramp_rate_C_per_s, realized_peak_temp_C)=A |
| realized_ramp_rate_C_per_s, peak_zone_setpoint_C | realized_ramp_rate_C_per_s   peak_zone_setpoint_C (no edge) | realized_ramp_rate_C_per_s   peak_zone_setpoint_C (no edge) | realized_ramp_rate_C_per_s->peak_zone_setpoint_C | realized_ramp_rate_C_per_s->peak_zone_setpoint_C | realized_ramp_rate_C_per_s->peak_zone_setpoint_C | no edge | (realized_ramp_rate_C_per_s, peak_zone_setpoint_C)=A |
| realized_ramp_rate_C_per_s, preheat_soak_setpoint_C | preheat_soak_setpoint_C o-> realized_ramp_rate_C_per_s | realized_ramp_rate_C_per_s   preheat_soak_setpoint_C (no edge) | realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | preheat_soak_setpoint_C -> realized_ramp_rate_C_per_s | (realized_ramp_rate_C_per_s, preheat_soak_setpoint_C)=A |
| TAL_s, microstructure_index | microstructure_index->TAL_s | microstructure_index->TAL_s | TAL_s   microstructure_index (no edge) | TAL_s   microstructure_index (no edge) | TAL_s   microstructure_index (no edge) | TAL_s -> microstructure_index | (TAL_s, microstructure_index)=C |
| TAL_s, conv_speed_cm_min | TAL_s <-> conv_speed_cm_min | TAL_s   conv_speed_cm_min (no edge) | TAL_s   conv_speed_cm_min (no edge) | TAL_s   conv_speed_cm_min (no edge) | TAL_s   conv_speed_cm_min (no edge) | conv_speed_cm_min -> TAL_s | (TAL_s, conv_speed_cm_min)=C |
| TAL_s, realized_peak_temp_C | TAL_s   realized_peak_temp_C (no edge) | TAL_s   realized_peak_temp_C (no edge) | TAL_s->realized_peak_temp_C | TAL_s->realized_peak_temp_C | TAL_s->realized_peak_temp_C | realized_peak_temp_C -> TAL_s | (TAL_s, realized_peak_temp_C)=A |
| oxygen_ppm, nitrogen_flow_setpoint_slpm | nitrogen_flow_setpoint_slpm o-> oxygen_ppm | oxygen_ppm   nitrogen_flow_setpoint_slpm (no edge) | oxygen_ppm   nitrogen_flow_setpoint_slpm (no edge) | oxygen_ppm   nitrogen_flow_setpoint_slpm (no edge) | oxygen_ppm   nitrogen_flow_setpoint_slpm (no edge) | nitrogen_flow_setpoint_slpm -> oxygen_ppm | (oxygen_ppm, nitrogen_flow_setpoint_slpm)=C |
| oxygen_ppm, volatile_generation_cumulative_mg | oxygen_ppm   volatile_generation_cumulative_mg (no edge) | oxygen_ppm   volatile_generation_cumulative_mg (no edge) | oxygen_ppm->volatile_generation_cumulative_mg | oxygen_ppm->volatile_generation_cumulative_mg | oxygen_ppm->volatile_generation_cumulative_mg | no edge | (oxygen_ppm, volatile_generation_cumulative_mg)=A |
| flux_lot_activity_index, volatile_generation_cumulative_mg | flux_lot_activity_index   volatile_generation_cumulative_mg (no edge) | flux_lot_activity_index   volatile_generation_cumulative_mg (no edge) | flux_lot_activity_index->volatile_generation_cumulative_mg | flux_lot_activity_index->volatile_generation_cumulative_mg | flux_lot_activity_index->volatile_generation_cumulative_mg | flux_lot_activity_index -> volatile_generation_cumulative_mg | (flux_lot_activity_index, volatile_generation_cumulative_mg)=A |
| flux_lot_activity_index, paste_batch_context | flux_lot_activity_index o-o paste_batch_context | flux_lot_activity_index o-o paste_batch_context | flux_lot_activity_index   paste_batch_context (no edge) | flux_lot_activity_index   paste_batch_context (no edge) | flux_lot_activity_index   paste_batch_context (no edge) | paste_batch_context -> flux_lot_activity_index | (flux_lot_activity_index, paste_batch_context)=C |
| microstructure_index, wetting_index | microstructure_index   wetting_index (no edge) | microstructure_index   wetting_index (no edge) | microstructure_index->wetting_index | microstructure_index->wetting_index | microstructure_index->wetting_index | no edge | (microstructure_index, wetting_index)=A |
| microstructure_index, true_void_fraction | microstructure_index   true_void_fraction (no edge) | microstructure_index   true_void_fraction (no edge) | microstructure_index->true_void_fraction | microstructure_index->true_void_fraction | microstructure_index->true_void_fraction | no edge | (microstructure_index, true_void_fraction)=A |
| nitrogen_flow_setpoint_slpm, volatile_generation_cumulative_mg | nitrogen_flow_setpoint_slpm   volatile_generation_cumulative_mg (no edge) | nitrogen_flow_setpoint_slpm   volatile_generation_cumulative_mg (no edge) | nitrogen_flow_setpoint_slpm->volatile_generation_cumulative_mg | nitrogen_flow_setpoint_slpm->volatile_generation_cumulative_mg | nitrogen_flow_setpoint_slpm->volatile_generation_cumulative_mg | no edge | (nitrogen_flow_setpoint_slpm, volatile_generation_cumulative_mg)=A |
| nitrogen_flow_setpoint_slpm, residual_entrained_gas_mg | nitrogen_flow_setpoint_slpm   residual_entrained_gas_mg (no edge) | nitrogen_flow_setpoint_slpm   residual_entrained_gas_mg (no edge) | nitrogen_flow_setpoint_slpm->residual_entrained_gas_mg | nitrogen_flow_setpoint_slpm->residual_entrained_gas_mg | nitrogen_flow_setpoint_slpm->residual_entrained_gas_mg | no edge | (nitrogen_flow_setpoint_slpm, residual_entrained_gas_mg)=A |
| nitrogen_flow_setpoint_slpm, realized_peak_temp_C | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | nitrogen_flow_setpoint_slpm->realized_peak_temp_C | nitrogen_flow_setpoint_slpm->realized_peak_temp_C | nitrogen_flow_setpoint_slpm->realized_peak_temp_C | no edge | (nitrogen_flow_setpoint_slpm, realized_peak_temp_C)=A |
| wetting_index, paste_solvent_mass_fraction | wetting_index   paste_solvent_mass_fraction (no edge) | wetting_index   paste_solvent_mass_fraction (no edge) | wetting_index->paste_solvent_mass_fraction | wetting_index->paste_solvent_mass_fraction | wetting_index->paste_solvent_mass_fraction | no edge | (wetting_index, paste_solvent_mass_fraction)=A |
| wetting_index, residual_entrained_gas_mg | residual_entrained_gas_mg->wetting_index | residual_entrained_gas_mg->wetting_index | wetting_index   residual_entrained_gas_mg (no edge) | wetting_index   residual_entrained_gas_mg (no edge) | wetting_index   residual_entrained_gas_mg (no edge) | wetting_index -> residual_entrained_gas_mg | (wetting_index, residual_entrained_gas_mg)=C |
| wetting_index, realized_peak_temp_C | realized_peak_temp_C->wetting_index | realized_peak_temp_C->wetting_index | wetting_index   realized_peak_temp_C (no edge) | wetting_index   realized_peak_temp_C (no edge) | wetting_index   realized_peak_temp_C (no edge) | realized_peak_temp_C -> wetting_index | (wetting_index, realized_peak_temp_C)=C |
| cooling_rate_C_per_s, conv_speed_cm_min | cooling_rate_C_per_s o-> conv_speed_cm_min | cooling_rate_C_per_s   conv_speed_cm_min (no edge) | cooling_rate_C_per_s   conv_speed_cm_min (no edge) | cooling_rate_C_per_s   conv_speed_cm_min (no edge) | cooling_rate_C_per_s   conv_speed_cm_min (no edge) | conv_speed_cm_min -> cooling_rate_C_per_s | (cooling_rate_C_per_s, conv_speed_cm_min)=C |
| cooling_rate_C_per_s, realized_peak_temp_C | cooling_rate_C_per_s   realized_peak_temp_C (no edge) | cooling_rate_C_per_s   realized_peak_temp_C (no edge) | cooling_rate_C_per_s->realized_peak_temp_C | cooling_rate_C_per_s->realized_peak_temp_C | cooling_rate_C_per_s->realized_peak_temp_C | realized_peak_temp_C -> cooling_rate_C_per_s | (cooling_rate_C_per_s, realized_peak_temp_C)=A |
| volatile_generation_cumulative_mg, paste_solvent_mass_fraction | paste_solvent_mass_fraction->volatile_generation_cumulative_mg | paste_solvent_mass_fraction->volatile_generation_cumulative_mg | volatile_generation_cumulative_mg->paste_solvent_mass_fraction | volatile_generation_cumulative_mg->paste_solvent_mass_fraction | volatile_generation_cumulative_mg->paste_solvent_mass_fraction | paste_solvent_mass_fraction -> volatile_generation_cumulative_mg | (volatile_generation_cumulative_mg, paste_solvent_mass_fraction)=A |
| volatile_generation_cumulative_mg, residual_entrained_gas_mg | volatile_generation_cumulative_mg   residual_entrained_gas_mg (no edge) | volatile_generation_cumulative_mg   residual_entrained_gas_mg (no edge) | volatile_generation_cumulative_mg->residual_entrained_gas_mg | volatile_generation_cumulative_mg->residual_entrained_gas_mg | volatile_generation_cumulative_mg->residual_entrained_gas_mg | volatile_generation_cumulative_mg -> residual_entrained_gas_mg | (volatile_generation_cumulative_mg, residual_entrained_gas_mg)=A |
| volatile_generation_cumulative_mg, realized_peak_temp_C | volatile_generation_cumulative_mg   realized_peak_temp_C (no edge) | volatile_generation_cumulative_mg   realized_peak_temp_C (no edge) | volatile_generation_cumulative_mg->realized_peak_temp_C | volatile_generation_cumulative_mg->realized_peak_temp_C | volatile_generation_cumulative_mg->realized_peak_temp_C | realized_peak_temp_C -> volatile_generation_cumulative_mg | (volatile_generation_cumulative_mg, realized_peak_temp_C)=A |
| volatile_generation_cumulative_mg, electrical_resistance_mOhm | volatile_generation_cumulative_mg <-> electrical_resistance_mOhm | volatile_generation_cumulative_mg   electrical_resistance_mOhm (no edge) | volatile_generation_cumulative_mg   electrical_resistance_mOhm (no edge) | volatile_generation_cumulative_mg   electrical_resistance_mOhm (no edge) | volatile_generation_cumulative_mg   electrical_resistance_mOhm (no edge) | no edge | (volatile_generation_cumulative_mg, electrical_resistance_mOhm)=C |
| volatile_generation_cumulative_mg, peak_zone_setpoint_C | volatile_generation_cumulative_mg   peak_zone_setpoint_C (no edge) | volatile_generation_cumulative_mg   peak_zone_setpoint_C (no edge) | volatile_generation_cumulative_mg->peak_zone_setpoint_C | volatile_generation_cumulative_mg->peak_zone_setpoint_C | volatile_generation_cumulative_mg->peak_zone_setpoint_C | no edge | (volatile_generation_cumulative_mg, peak_zone_setpoint_C)=A |
| volatile_generation_cumulative_mg, preheat_soak_setpoint_C | volatile_generation_cumulative_mg   preheat_soak_setpoint_C (no edge) | volatile_generation_cumulative_mg   preheat_soak_setpoint_C (no edge) | volatile_generation_cumulative_mg->preheat_soak_setpoint_C | volatile_generation_cumulative_mg->preheat_soak_setpoint_C | volatile_generation_cumulative_mg->preheat_soak_setpoint_C | no edge | (volatile_generation_cumulative_mg, preheat_soak_setpoint_C)=A |
| paste_solvent_mass_fraction, true_void_fraction | paste_solvent_mass_fraction   true_void_fraction (no edge) | paste_solvent_mass_fraction   true_void_fraction (no edge) | paste_solvent_mass_fraction->true_void_fraction | paste_solvent_mass_fraction->true_void_fraction | paste_solvent_mass_fraction->true_void_fraction | no edge | (paste_solvent_mass_fraction, true_void_fraction)=A |
| paste_solvent_mass_fraction, paste_batch_context | paste_solvent_mass_fraction o-o paste_batch_context | paste_solvent_mass_fraction o-o paste_batch_context | paste_solvent_mass_fraction   paste_batch_context (no edge) | paste_solvent_mass_fraction   paste_batch_context (no edge) | paste_solvent_mass_fraction   paste_batch_context (no edge) | paste_batch_context -> paste_solvent_mass_fraction | (paste_solvent_mass_fraction, paste_batch_context)=C |
| pad_finish, package_family_code | pad_finish o-o package_family_code | pad_finish   package_family_code (no edge) | pad_finish   package_family_code (no edge) | pad_finish   package_family_code (no edge) | pad_finish   package_family_code (no edge) | package_family_code -> pad_finish | (pad_finish, package_family_code)=C |
| residual_entrained_gas_mg, true_void_fraction | residual_entrained_gas_mg o-o true_void_fraction | residual_entrained_gas_mg   true_void_fraction (no edge) | residual_entrained_gas_mg   true_void_fraction (no edge) | residual_entrained_gas_mg   true_void_fraction (no edge) | residual_entrained_gas_mg   true_void_fraction (no edge) | residual_entrained_gas_mg -> true_void_fraction | (residual_entrained_gas_mg, true_void_fraction)=C |
| residual_entrained_gas_mg, electrical_resistance_mOhm | residual_entrained_gas_mg o-> electrical_resistance_mOhm | residual_entrained_gas_mg   electrical_resistance_mOhm (no edge) | residual_entrained_gas_mg   electrical_resistance_mOhm (no edge) | residual_entrained_gas_mg   electrical_resistance_mOhm (no edge) | residual_entrained_gas_mg   electrical_resistance_mOhm (no edge) | no edge | (residual_entrained_gas_mg, electrical_resistance_mOhm)=C |
| true_void_fraction, electrical_resistance_mOhm | true_void_fraction o-> electrical_resistance_mOhm | true_void_fraction o-> electrical_resistance_mOhm | true_void_fraction   electrical_resistance_mOhm (no edge) | true_void_fraction   electrical_resistance_mOhm (no edge) | true_void_fraction   electrical_resistance_mOhm (no edge) | true_void_fraction -> electrical_resistance_mOhm | (true_void_fraction, electrical_resistance_mOhm)=C |
| realized_peak_temp_C, peak_zone_setpoint_C | realized_peak_temp_C o-o peak_zone_setpoint_C | realized_peak_temp_C   peak_zone_setpoint_C (no edge) | realized_peak_temp_C->peak_zone_setpoint_C | realized_peak_temp_C->peak_zone_setpoint_C | realized_peak_temp_C->peak_zone_setpoint_C | peak_zone_setpoint_C -> realized_peak_temp_C | (realized_peak_temp_C, peak_zone_setpoint_C)=A |
| realized_peak_temp_C, preheat_soak_setpoint_C | realized_peak_temp_C   preheat_soak_setpoint_C (no edge) | realized_peak_temp_C   preheat_soak_setpoint_C (no edge) | realized_peak_temp_C->preheat_soak_setpoint_C | realized_peak_temp_C->preheat_soak_setpoint_C | realized_peak_temp_C->preheat_soak_setpoint_C | no edge | (realized_peak_temp_C, preheat_soak_setpoint_C)=A |
| peak_zone_setpoint_C, preheat_soak_setpoint_C | peak_zone_setpoint_C   preheat_soak_setpoint_C (no edge) | peak_zone_setpoint_C   preheat_soak_setpoint_C (no edge) | peak_zone_setpoint_C->preheat_soak_setpoint_C | peak_zone_setpoint_C->preheat_soak_setpoint_C | peak_zone_setpoint_C->preheat_soak_setpoint_C | no edge | (peak_zone_setpoint_C, preheat_soak_setpoint_C)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
