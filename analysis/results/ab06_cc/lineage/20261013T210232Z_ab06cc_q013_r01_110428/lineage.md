# Edge lineage: 20261013T210232Z_ab06cc_q013_r01_110428

Dataset `/research/datasets/suite_q1s2/q013/q013.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 2}. 23 variables, 253 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 25 | 0.80 | 0.51 | 0.62 | 6 | 1 | 13 | 39 |
| S1 after bootstrap edits | 11 | 1.00 | 0.28 | 0.44 | 6 | 0 | 5 | 34 |
| S2 after LLM review | 49 | 0.18 | 0.23 | 0.20 | 6 | 3 | 0 | 73 |
| S3 after KCI pruning | 49 | 0.18 | 0.23 | 0.20 | 6 | 3 | 0 | 73 |
| S4 final (after cycle step) | 49 | 0.18 | 0.23 | 0.20 | 6 | 3 | 0 | 73 |

Scored against: reference graph s2_01_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 14. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 23 calls, 253 distinct pairs answered out of 253, plus 23 self-pairs. Letters: {"A": 49, "C": 194, "D": 10}.
- LLM effect: added 47 (of which 44 where the resamples showed no edge at frequency >= 0.9), removed 9, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 49 edges; set by {"llm": 47, "algorithm (unchanged)": 2}; 3 identical to the algorithm's output; 45 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| oven_leak_index->component_thermal_mass_index | llm | no | 1.00 |
| oven_leak_index->realized_ramp_rate_C_per_s | llm | no | 1.00 |
| oven_leak_index->measured_void_fraction | algorithm (unchanged) | yes | 0.00 |
| oven_leak_index->microstructure_index | llm | no | 0.95 |
| oven_leak_index->cooling_rate_C_per_s | llm | no | 1.00 |
| oven_leak_index->volatile_generation_cumulative_mg | llm | no | 1.00 |
| oven_leak_index->wetting_index | llm | no | 0.85 |
| oven_leak_index->true_void_fraction | llm | no | 1.00 |
| oven_leak_index->realized_peak_temp_C | llm | no | 1.00 |
| oven_leak_index->peak_zone_setpoint_C | llm | no | 0.90 |
| oven_leak_index->preheat_soak_setpoint_C | llm | no | 1.00 |
| component_thermal_mass_index->realized_ramp_rate_C_per_s | llm | no | 1.00 |
| component_thermal_mass_index->microstructure_index | llm | no | 1.00 |
| component_thermal_mass_index->cooling_rate_C_per_s | llm | no | 1.00 |
| component_thermal_mass_index->realized_peak_temp_C | llm | no | 1.00 |
| component_thermal_mass_index->electrical_resistance_mOhm | llm | no | 1.00 |
| realized_ramp_rate_C_per_s->cooling_rate_C_per_s | llm | no | 1.00 |
| realized_ramp_rate_C_per_s->volatile_generation_cumulative_mg | llm | no | 1.00 |
| realized_ramp_rate_C_per_s->realized_peak_temp_C | llm | no | 1.00 |
| realized_ramp_rate_C_per_s->peak_zone_setpoint_C | llm | no | 1.00 |
| realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | llm | no | 1.00 |
| measured_void_fraction->microstructure_index | llm | no | 1.00 |
| measured_void_fraction->wetting_index | llm | no | 0.95 |
| measured_void_fraction->true_void_fraction | llm | no | 1.00 |
| oxygen_ppm->volatile_generation_cumulative_mg | llm | no | 1.00 |
| oxygen_ppm->realized_peak_temp_C | llm | yes | 0.00 |
| microstructure_index->pad_finish | llm | no | 1.00 |
| microstructure_index->wetting_index | llm | no | 0.95 |
| microstructure_index->true_void_fraction | llm | no | 1.00 |
| microstructure_index->electrical_resistance_mOhm | llm | no | 1.00 |
| cooling_rate_C_per_s->realized_peak_temp_C | llm | no | 1.00 |
| cooling_rate_C_per_s->peak_zone_setpoint_C | llm | no | 1.00 |
| cooling_rate_C_per_s->electrical_resistance_mOhm | llm | no | 0.90 |
| cooling_rate_C_per_s->preheat_soak_setpoint_C | llm | no | 1.00 |
| paste_solvent_mass_fraction->volatile_generation_cumulative_mg | llm | no | 1.00 |
| paste_solvent_mass_fraction->wetting_index | llm | no | 1.00 |
| paste_solvent_mass_fraction->true_void_fraction | algorithm (unchanged) | yes | 0.45 |
| pad_finish->wetting_index | llm | no | 1.00 |
| pad_finish->true_void_fraction | llm | no | 0.95 |
| volatile_generation_cumulative_mg->realized_peak_temp_C | llm | no | 1.00 |
| wetting_index->true_void_fraction | llm | no | 1.00 |
| package_family_code->paste_batch_context | llm | no | 1.00 |
| realized_peak_temp_C->peak_zone_setpoint_C | llm | no | 1.00 |
| realized_peak_temp_C->residual_entrained_gas_mg | llm | no | 1.00 |
| realized_peak_temp_C->electrical_resistance_mOhm | llm | no | 1.00 |
| realized_peak_temp_C->preheat_soak_setpoint_C | llm | no | 0.95 |
| peak_zone_setpoint_C->electrical_resistance_mOhm | llm | yes | 0.00 |
| peak_zone_setpoint_C->preheat_soak_setpoint_C | llm | no | 1.00 |
| electrical_resistance_mOhm->preheat_soak_setpoint_C | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| oven_leak_index, component_thermal_mass_index | oven_leak_index   component_thermal_mass_index (no edge) | oven_leak_index   component_thermal_mass_index (no edge) | oven_leak_index->component_thermal_mass_index | oven_leak_index->component_thermal_mass_index | oven_leak_index->component_thermal_mass_index | no edge | (oven_leak_index, component_thermal_mass_index)=A |
| oven_leak_index, realized_ramp_rate_C_per_s | oven_leak_index   realized_ramp_rate_C_per_s (no edge) | oven_leak_index   realized_ramp_rate_C_per_s (no edge) | oven_leak_index->realized_ramp_rate_C_per_s | oven_leak_index->realized_ramp_rate_C_per_s | oven_leak_index->realized_ramp_rate_C_per_s | no edge | (oven_leak_index, realized_ramp_rate_C_per_s)=A |
| oven_leak_index, microstructure_index | oven_leak_index   microstructure_index (no edge) | oven_leak_index   microstructure_index (no edge) | oven_leak_index->microstructure_index | oven_leak_index->microstructure_index | oven_leak_index->microstructure_index | no edge | (oven_leak_index, microstructure_index)=A |
| oven_leak_index, cooling_rate_C_per_s | oven_leak_index   cooling_rate_C_per_s (no edge) | oven_leak_index   cooling_rate_C_per_s (no edge) | oven_leak_index->cooling_rate_C_per_s | oven_leak_index->cooling_rate_C_per_s | oven_leak_index->cooling_rate_C_per_s | no edge | (oven_leak_index, cooling_rate_C_per_s)=A |
| oven_leak_index, volatile_generation_cumulative_mg | oven_leak_index   volatile_generation_cumulative_mg (no edge) | oven_leak_index   volatile_generation_cumulative_mg (no edge) | oven_leak_index->volatile_generation_cumulative_mg | oven_leak_index->volatile_generation_cumulative_mg | oven_leak_index->volatile_generation_cumulative_mg | no edge | (oven_leak_index, volatile_generation_cumulative_mg)=A |
| oven_leak_index, wetting_index | oven_leak_index   wetting_index (no edge) | oven_leak_index   wetting_index (no edge) | oven_leak_index->wetting_index | oven_leak_index->wetting_index | oven_leak_index->wetting_index | no edge | (oven_leak_index, wetting_index)=A |
| oven_leak_index, true_void_fraction | oven_leak_index   true_void_fraction (no edge) | oven_leak_index   true_void_fraction (no edge) | oven_leak_index->true_void_fraction | oven_leak_index->true_void_fraction | oven_leak_index->true_void_fraction | no edge | (oven_leak_index, true_void_fraction)=A |
| oven_leak_index, realized_peak_temp_C | oven_leak_index   realized_peak_temp_C (no edge) | oven_leak_index   realized_peak_temp_C (no edge) | oven_leak_index->realized_peak_temp_C | oven_leak_index->realized_peak_temp_C | oven_leak_index->realized_peak_temp_C | no edge | (oven_leak_index, realized_peak_temp_C)=A |
| oven_leak_index, conv_speed_cm_min | oven_leak_index o-o conv_speed_cm_min | oven_leak_index o-o conv_speed_cm_min | oven_leak_index   conv_speed_cm_min (no edge) | oven_leak_index   conv_speed_cm_min (no edge) | oven_leak_index   conv_speed_cm_min (no edge) | conv_speed_cm_min -> oven_leak_index | (oven_leak_index, conv_speed_cm_min)=C |
| oven_leak_index, peak_zone_setpoint_C | oven_leak_index   peak_zone_setpoint_C (no edge) | oven_leak_index   peak_zone_setpoint_C (no edge) | oven_leak_index->peak_zone_setpoint_C | oven_leak_index->peak_zone_setpoint_C | oven_leak_index->peak_zone_setpoint_C | oven_leak_index -> peak_zone_setpoint_C | (oven_leak_index, peak_zone_setpoint_C)=A |
| oven_leak_index, preheat_soak_setpoint_C | oven_leak_index   preheat_soak_setpoint_C (no edge) | oven_leak_index   preheat_soak_setpoint_C (no edge) | oven_leak_index->preheat_soak_setpoint_C | oven_leak_index->preheat_soak_setpoint_C | oven_leak_index->preheat_soak_setpoint_C | no edge | (oven_leak_index, preheat_soak_setpoint_C)=A |
| component_thermal_mass_index, realized_ramp_rate_C_per_s | component_thermal_mass_index   realized_ramp_rate_C_per_s (no edge) | component_thermal_mass_index   realized_ramp_rate_C_per_s (no edge) | component_thermal_mass_index->realized_ramp_rate_C_per_s | component_thermal_mass_index->realized_ramp_rate_C_per_s | component_thermal_mass_index->realized_ramp_rate_C_per_s | no edge | (component_thermal_mass_index, realized_ramp_rate_C_per_s)=A |
| component_thermal_mass_index, TAL_s | component_thermal_mass_index o-> TAL_s | component_thermal_mass_index   TAL_s (no edge) | component_thermal_mass_index   TAL_s (no edge) | component_thermal_mass_index   TAL_s (no edge) | component_thermal_mass_index   TAL_s (no edge) | component_thermal_mass_index -> TAL_s | (component_thermal_mass_index, TAL_s)=D |
| component_thermal_mass_index, microstructure_index | component_thermal_mass_index   microstructure_index (no edge) | component_thermal_mass_index   microstructure_index (no edge) | component_thermal_mass_index->microstructure_index | component_thermal_mass_index->microstructure_index | component_thermal_mass_index->microstructure_index | no edge | (component_thermal_mass_index, microstructure_index)=A |
| component_thermal_mass_index, cooling_rate_C_per_s | component_thermal_mass_index   cooling_rate_C_per_s (no edge) | component_thermal_mass_index   cooling_rate_C_per_s (no edge) | component_thermal_mass_index->cooling_rate_C_per_s | component_thermal_mass_index->cooling_rate_C_per_s | component_thermal_mass_index->cooling_rate_C_per_s | no edge | (component_thermal_mass_index, cooling_rate_C_per_s)=A |
| component_thermal_mass_index, realized_peak_temp_C | component_thermal_mass_index   realized_peak_temp_C (no edge) | component_thermal_mass_index   realized_peak_temp_C (no edge) | component_thermal_mass_index->realized_peak_temp_C | component_thermal_mass_index->realized_peak_temp_C | component_thermal_mass_index->realized_peak_temp_C | no edge | (component_thermal_mass_index, realized_peak_temp_C)=A |
| component_thermal_mass_index, electrical_resistance_mOhm | component_thermal_mass_index   electrical_resistance_mOhm (no edge) | component_thermal_mass_index   electrical_resistance_mOhm (no edge) | component_thermal_mass_index->electrical_resistance_mOhm | component_thermal_mass_index->electrical_resistance_mOhm | component_thermal_mass_index->electrical_resistance_mOhm | no edge | (component_thermal_mass_index, electrical_resistance_mOhm)=A |
| realized_ramp_rate_C_per_s, cooling_rate_C_per_s | realized_ramp_rate_C_per_s   cooling_rate_C_per_s (no edge) | realized_ramp_rate_C_per_s   cooling_rate_C_per_s (no edge) | realized_ramp_rate_C_per_s->cooling_rate_C_per_s | realized_ramp_rate_C_per_s->cooling_rate_C_per_s | realized_ramp_rate_C_per_s->cooling_rate_C_per_s | no edge | (realized_ramp_rate_C_per_s, cooling_rate_C_per_s)=A |
| realized_ramp_rate_C_per_s, volatile_generation_cumulative_mg | realized_ramp_rate_C_per_s   volatile_generation_cumulative_mg (no edge) | realized_ramp_rate_C_per_s   volatile_generation_cumulative_mg (no edge) | realized_ramp_rate_C_per_s->volatile_generation_cumulative_mg | realized_ramp_rate_C_per_s->volatile_generation_cumulative_mg | realized_ramp_rate_C_per_s->volatile_generation_cumulative_mg | no edge | (realized_ramp_rate_C_per_s, volatile_generation_cumulative_mg)=A |
| realized_ramp_rate_C_per_s, true_void_fraction | true_void_fraction->realized_ramp_rate_C_per_s | realized_ramp_rate_C_per_s   true_void_fraction (no edge) | realized_ramp_rate_C_per_s   true_void_fraction (no edge) | realized_ramp_rate_C_per_s   true_void_fraction (no edge) | realized_ramp_rate_C_per_s   true_void_fraction (no edge) | no edge | (realized_ramp_rate_C_per_s, true_void_fraction)=C |
| realized_ramp_rate_C_per_s, package_family_code | realized_ramp_rate_C_per_s ~~~ package_family_code | realized_ramp_rate_C_per_s ~~~ package_family_code | realized_ramp_rate_C_per_s   package_family_code (no edge) | realized_ramp_rate_C_per_s   package_family_code (no edge) | realized_ramp_rate_C_per_s   package_family_code (no edge) | package_family_code -> realized_ramp_rate_C_per_s | (realized_ramp_rate_C_per_s, package_family_code)=C |
| realized_ramp_rate_C_per_s, realized_peak_temp_C | realized_ramp_rate_C_per_s   realized_peak_temp_C (no edge) | realized_ramp_rate_C_per_s   realized_peak_temp_C (no edge) | realized_ramp_rate_C_per_s->realized_peak_temp_C | realized_ramp_rate_C_per_s->realized_peak_temp_C | realized_ramp_rate_C_per_s->realized_peak_temp_C | no edge | (realized_ramp_rate_C_per_s, realized_peak_temp_C)=A |
| realized_ramp_rate_C_per_s, peak_zone_setpoint_C | realized_ramp_rate_C_per_s   peak_zone_setpoint_C (no edge) | realized_ramp_rate_C_per_s   peak_zone_setpoint_C (no edge) | realized_ramp_rate_C_per_s->peak_zone_setpoint_C | realized_ramp_rate_C_per_s->peak_zone_setpoint_C | realized_ramp_rate_C_per_s->peak_zone_setpoint_C | no edge | (realized_ramp_rate_C_per_s, peak_zone_setpoint_C)=A |
| realized_ramp_rate_C_per_s, preheat_soak_setpoint_C | realized_ramp_rate_C_per_s   preheat_soak_setpoint_C (no edge) | realized_ramp_rate_C_per_s   preheat_soak_setpoint_C (no edge) | realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | realized_ramp_rate_C_per_s->preheat_soak_setpoint_C | no edge | (realized_ramp_rate_C_per_s, preheat_soak_setpoint_C)=A |
| measured_void_fraction, microstructure_index | measured_void_fraction   microstructure_index (no edge) | measured_void_fraction   microstructure_index (no edge) | measured_void_fraction->microstructure_index | measured_void_fraction->microstructure_index | measured_void_fraction->microstructure_index | no edge | (measured_void_fraction, microstructure_index)=A |
| measured_void_fraction, wetting_index | measured_void_fraction   wetting_index (no edge) | measured_void_fraction   wetting_index (no edge) | measured_void_fraction->wetting_index | measured_void_fraction->wetting_index | measured_void_fraction->wetting_index | no edge | (measured_void_fraction, wetting_index)=A |
| measured_void_fraction, true_void_fraction | measured_void_fraction   true_void_fraction (no edge) | measured_void_fraction   true_void_fraction (no edge) | measured_void_fraction->true_void_fraction | measured_void_fraction->true_void_fraction | measured_void_fraction->true_void_fraction | no edge | (measured_void_fraction, true_void_fraction)=A |
| measured_void_fraction, realized_peak_temp_C | measured_void_fraction <-> realized_peak_temp_C | measured_void_fraction   realized_peak_temp_C (no edge) | measured_void_fraction   realized_peak_temp_C (no edge) | measured_void_fraction   realized_peak_temp_C (no edge) | measured_void_fraction   realized_peak_temp_C (no edge) | realized_peak_temp_C -> measured_void_fraction | (measured_void_fraction, realized_peak_temp_C)=C |
| measured_void_fraction, paste_batch_context | measured_void_fraction <-> paste_batch_context | measured_void_fraction   paste_batch_context (no edge) | measured_void_fraction   paste_batch_context (no edge) | measured_void_fraction   paste_batch_context (no edge) | measured_void_fraction   paste_batch_context (no edge) | paste_batch_context -> measured_void_fraction | (measured_void_fraction, paste_batch_context)=C |
| oxygen_ppm, flux_lot_activity_index | oxygen_ppm o-o flux_lot_activity_index | oxygen_ppm o-o flux_lot_activity_index | oxygen_ppm   flux_lot_activity_index (no edge) | oxygen_ppm   flux_lot_activity_index (no edge) | oxygen_ppm   flux_lot_activity_index (no edge) | oxygen_ppm -> flux_lot_activity_index | (oxygen_ppm, flux_lot_activity_index)=C |
| oxygen_ppm, volatile_generation_cumulative_mg | oxygen_ppm   volatile_generation_cumulative_mg (no edge) | oxygen_ppm   volatile_generation_cumulative_mg (no edge) | oxygen_ppm->volatile_generation_cumulative_mg | oxygen_ppm->volatile_generation_cumulative_mg | oxygen_ppm->volatile_generation_cumulative_mg | no edge | (oxygen_ppm, volatile_generation_cumulative_mg)=A |
| oxygen_ppm, realized_peak_temp_C | oxygen_ppm->realized_peak_temp_C | oxygen_ppm   realized_peak_temp_C (no edge) | oxygen_ppm->realized_peak_temp_C | oxygen_ppm->realized_peak_temp_C | oxygen_ppm->realized_peak_temp_C | realized_peak_temp_C -> oxygen_ppm | (oxygen_ppm, realized_peak_temp_C)=A |
| TAL_s, cooling_rate_C_per_s | TAL_s <-> cooling_rate_C_per_s | TAL_s   cooling_rate_C_per_s (no edge) | TAL_s   cooling_rate_C_per_s (no edge) | TAL_s   cooling_rate_C_per_s (no edge) | TAL_s   cooling_rate_C_per_s (no edge) | cooling_rate_C_per_s -> TAL_s | (TAL_s, cooling_rate_C_per_s)=C |
| TAL_s, paste_solvent_mass_fraction | TAL_s <-> paste_solvent_mass_fraction | TAL_s   paste_solvent_mass_fraction (no edge) | TAL_s   paste_solvent_mass_fraction (no edge) | TAL_s   paste_solvent_mass_fraction (no edge) | TAL_s   paste_solvent_mass_fraction (no edge) | TAL_s -> paste_solvent_mass_fraction | (TAL_s, paste_solvent_mass_fraction)=C |
| microstructure_index, pad_finish | microstructure_index   pad_finish (no edge) | microstructure_index   pad_finish (no edge) | microstructure_index->pad_finish | microstructure_index->pad_finish | microstructure_index->pad_finish | microstructure_index -> pad_finish | (microstructure_index, pad_finish)=A |
| microstructure_index, wetting_index | microstructure_index   wetting_index (no edge) | microstructure_index   wetting_index (no edge) | microstructure_index->wetting_index | microstructure_index->wetting_index | microstructure_index->wetting_index | no edge | (microstructure_index, wetting_index)=A |
| microstructure_index, true_void_fraction | microstructure_index   true_void_fraction (no edge) | microstructure_index   true_void_fraction (no edge) | microstructure_index->true_void_fraction | microstructure_index->true_void_fraction | microstructure_index->true_void_fraction | no edge | (microstructure_index, true_void_fraction)=A |
| microstructure_index, electrical_resistance_mOhm | microstructure_index   electrical_resistance_mOhm (no edge) | microstructure_index   electrical_resistance_mOhm (no edge) | microstructure_index->electrical_resistance_mOhm | microstructure_index->electrical_resistance_mOhm | microstructure_index->electrical_resistance_mOhm | no edge | (microstructure_index, electrical_resistance_mOhm)=A |
| microstructure_index, preheat_soak_setpoint_C | microstructure_index o-o preheat_soak_setpoint_C | microstructure_index   preheat_soak_setpoint_C (no edge) | microstructure_index   preheat_soak_setpoint_C (no edge) | microstructure_index   preheat_soak_setpoint_C (no edge) | microstructure_index   preheat_soak_setpoint_C (no edge) | preheat_soak_setpoint_C -> microstructure_index | (microstructure_index, preheat_soak_setpoint_C)=C |
| flux_lot_activity_index, peak_zone_setpoint_C | flux_lot_activity_index o-o peak_zone_setpoint_C | flux_lot_activity_index o-o peak_zone_setpoint_C | flux_lot_activity_index   peak_zone_setpoint_C (no edge) | flux_lot_activity_index   peak_zone_setpoint_C (no edge) | flux_lot_activity_index   peak_zone_setpoint_C (no edge) | peak_zone_setpoint_C -> flux_lot_activity_index | (flux_lot_activity_index, peak_zone_setpoint_C)=C |
| cooling_rate_C_per_s, realized_peak_temp_C | cooling_rate_C_per_s   realized_peak_temp_C (no edge) | cooling_rate_C_per_s   realized_peak_temp_C (no edge) | cooling_rate_C_per_s->realized_peak_temp_C | cooling_rate_C_per_s->realized_peak_temp_C | cooling_rate_C_per_s->realized_peak_temp_C | no edge | (cooling_rate_C_per_s, realized_peak_temp_C)=A |
| cooling_rate_C_per_s, peak_zone_setpoint_C | cooling_rate_C_per_s   peak_zone_setpoint_C (no edge) | cooling_rate_C_per_s   peak_zone_setpoint_C (no edge) | cooling_rate_C_per_s->peak_zone_setpoint_C | cooling_rate_C_per_s->peak_zone_setpoint_C | cooling_rate_C_per_s->peak_zone_setpoint_C | no edge | (cooling_rate_C_per_s, peak_zone_setpoint_C)=A |
| cooling_rate_C_per_s, electrical_resistance_mOhm | cooling_rate_C_per_s   electrical_resistance_mOhm (no edge) | cooling_rate_C_per_s   electrical_resistance_mOhm (no edge) | cooling_rate_C_per_s->electrical_resistance_mOhm | cooling_rate_C_per_s->electrical_resistance_mOhm | cooling_rate_C_per_s->electrical_resistance_mOhm | no edge | (cooling_rate_C_per_s, electrical_resistance_mOhm)=A |
| cooling_rate_C_per_s, preheat_soak_setpoint_C | cooling_rate_C_per_s   preheat_soak_setpoint_C (no edge) | cooling_rate_C_per_s   preheat_soak_setpoint_C (no edge) | cooling_rate_C_per_s->preheat_soak_setpoint_C | cooling_rate_C_per_s->preheat_soak_setpoint_C | cooling_rate_C_per_s->preheat_soak_setpoint_C | no edge | (cooling_rate_C_per_s, preheat_soak_setpoint_C)=A |
| cooling_rate_C_per_s, paste_batch_context | cooling_rate_C_per_s <-> paste_batch_context | cooling_rate_C_per_s   paste_batch_context (no edge) | cooling_rate_C_per_s   paste_batch_context (no edge) | cooling_rate_C_per_s   paste_batch_context (no edge) | cooling_rate_C_per_s   paste_batch_context (no edge) | no edge | (cooling_rate_C_per_s, paste_batch_context)=C |
| paste_solvent_mass_fraction, volatile_generation_cumulative_mg | paste_solvent_mass_fraction   volatile_generation_cumulative_mg (no edge) | paste_solvent_mass_fraction   volatile_generation_cumulative_mg (no edge) | paste_solvent_mass_fraction->volatile_generation_cumulative_mg | paste_solvent_mass_fraction->volatile_generation_cumulative_mg | paste_solvent_mass_fraction->volatile_generation_cumulative_mg | no edge | (paste_solvent_mass_fraction, volatile_generation_cumulative_mg)=A |
| paste_solvent_mass_fraction, wetting_index | paste_solvent_mass_fraction   wetting_index (no edge) | paste_solvent_mass_fraction   wetting_index (no edge) | paste_solvent_mass_fraction->wetting_index | paste_solvent_mass_fraction->wetting_index | paste_solvent_mass_fraction->wetting_index | wetting_index -> paste_solvent_mass_fraction | (paste_solvent_mass_fraction, wetting_index)=A |
| paste_solvent_mass_fraction, peak_zone_setpoint_C | peak_zone_setpoint_C->paste_solvent_mass_fraction | peak_zone_setpoint_C->paste_solvent_mass_fraction | paste_solvent_mass_fraction   peak_zone_setpoint_C (no edge) | paste_solvent_mass_fraction   peak_zone_setpoint_C (no edge) | paste_solvent_mass_fraction   peak_zone_setpoint_C (no edge) | peak_zone_setpoint_C -> paste_solvent_mass_fraction | (paste_solvent_mass_fraction, peak_zone_setpoint_C)=C |
| nitrogen_flow_setpoint_slpm, realized_peak_temp_C | nitrogen_flow_setpoint_slpm o-> realized_peak_temp_C | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | nitrogen_flow_setpoint_slpm   realized_peak_temp_C (no edge) | realized_peak_temp_C -> nitrogen_flow_setpoint_slpm | (nitrogen_flow_setpoint_slpm, realized_peak_temp_C)=C |
| pad_finish, volatile_generation_cumulative_mg | volatile_generation_cumulative_mg->pad_finish | volatile_generation_cumulative_mg->pad_finish | pad_finish   volatile_generation_cumulative_mg (no edge) | pad_finish   volatile_generation_cumulative_mg (no edge) | pad_finish   volatile_generation_cumulative_mg (no edge) | volatile_generation_cumulative_mg -> pad_finish | (pad_finish, volatile_generation_cumulative_mg)=C |
| pad_finish, wetting_index | pad_finish   wetting_index (no edge) | pad_finish   wetting_index (no edge) | pad_finish->wetting_index | pad_finish->wetting_index | pad_finish->wetting_index | no edge | (pad_finish, wetting_index)=A |
| pad_finish, true_void_fraction | pad_finish   true_void_fraction (no edge) | pad_finish   true_void_fraction (no edge) | pad_finish->true_void_fraction | pad_finish->true_void_fraction | pad_finish->true_void_fraction | pad_finish -> true_void_fraction | (pad_finish, true_void_fraction)=A |
| pad_finish, residual_entrained_gas_mg | pad_finish <-> residual_entrained_gas_mg | pad_finish   residual_entrained_gas_mg (no edge) | pad_finish   residual_entrained_gas_mg (no edge) | pad_finish   residual_entrained_gas_mg (no edge) | pad_finish   residual_entrained_gas_mg (no edge) | no edge | (pad_finish, residual_entrained_gas_mg)=C |
| volatile_generation_cumulative_mg, realized_peak_temp_C | volatile_generation_cumulative_mg   realized_peak_temp_C (no edge) | volatile_generation_cumulative_mg   realized_peak_temp_C (no edge) | volatile_generation_cumulative_mg->realized_peak_temp_C | volatile_generation_cumulative_mg->realized_peak_temp_C | volatile_generation_cumulative_mg->realized_peak_temp_C | no edge | (volatile_generation_cumulative_mg, realized_peak_temp_C)=A |
| volatile_generation_cumulative_mg, residual_entrained_gas_mg | residual_entrained_gas_mg->volatile_generation_cumulative_mg | volatile_generation_cumulative_mg   residual_entrained_gas_mg (no edge) | volatile_generation_cumulative_mg   residual_entrained_gas_mg (no edge) | volatile_generation_cumulative_mg   residual_entrained_gas_mg (no edge) | volatile_generation_cumulative_mg   residual_entrained_gas_mg (no edge) | no edge | (volatile_generation_cumulative_mg, residual_entrained_gas_mg)=C |
| volatile_generation_cumulative_mg, preheat_soak_setpoint_C | preheat_soak_setpoint_C->volatile_generation_cumulative_mg | preheat_soak_setpoint_C->volatile_generation_cumulative_mg | volatile_generation_cumulative_mg   preheat_soak_setpoint_C (no edge) | volatile_generation_cumulative_mg   preheat_soak_setpoint_C (no edge) | volatile_generation_cumulative_mg   preheat_soak_setpoint_C (no edge) | preheat_soak_setpoint_C -> volatile_generation_cumulative_mg | (volatile_generation_cumulative_mg, preheat_soak_setpoint_C)=C |
| wetting_index, true_void_fraction | wetting_index   true_void_fraction (no edge) | wetting_index   true_void_fraction (no edge) | wetting_index->true_void_fraction | wetting_index->true_void_fraction | wetting_index->true_void_fraction | wetting_index -> true_void_fraction | (wetting_index, true_void_fraction)=A |
| wetting_index, conv_speed_cm_min | wetting_index o-o conv_speed_cm_min | wetting_index o-o conv_speed_cm_min | wetting_index   conv_speed_cm_min (no edge) | wetting_index   conv_speed_cm_min (no edge) | wetting_index   conv_speed_cm_min (no edge) | conv_speed_cm_min -> wetting_index | (wetting_index, conv_speed_cm_min)=C |
| true_void_fraction, package_family_code | true_void_fraction->package_family_code | true_void_fraction->package_family_code | true_void_fraction   package_family_code (no edge) | true_void_fraction   package_family_code (no edge) | true_void_fraction   package_family_code (no edge) | true_void_fraction -> package_family_code | (true_void_fraction, package_family_code)=C |
| true_void_fraction, residual_entrained_gas_mg | true_void_fraction->residual_entrained_gas_mg | true_void_fraction   residual_entrained_gas_mg (no edge) | true_void_fraction   residual_entrained_gas_mg (no edge) | true_void_fraction   residual_entrained_gas_mg (no edge) | true_void_fraction   residual_entrained_gas_mg (no edge) | no edge | (true_void_fraction, residual_entrained_gas_mg)=C |
| package_family_code, paste_batch_context | package_family_code   paste_batch_context (no edge) | package_family_code   paste_batch_context (no edge) | package_family_code->paste_batch_context | package_family_code->paste_batch_context | package_family_code->paste_batch_context | no edge | (package_family_code, paste_batch_context)=A |
| realized_peak_temp_C, peak_zone_setpoint_C | realized_peak_temp_C   peak_zone_setpoint_C (no edge) | realized_peak_temp_C   peak_zone_setpoint_C (no edge) | realized_peak_temp_C->peak_zone_setpoint_C | realized_peak_temp_C->peak_zone_setpoint_C | realized_peak_temp_C->peak_zone_setpoint_C | no edge | (realized_peak_temp_C, peak_zone_setpoint_C)=A |
| realized_peak_temp_C, residual_entrained_gas_mg | realized_peak_temp_C   residual_entrained_gas_mg (no edge) | realized_peak_temp_C   residual_entrained_gas_mg (no edge) | realized_peak_temp_C->residual_entrained_gas_mg | realized_peak_temp_C->residual_entrained_gas_mg | realized_peak_temp_C->residual_entrained_gas_mg | no edge | (realized_peak_temp_C, residual_entrained_gas_mg)=A |
| realized_peak_temp_C, electrical_resistance_mOhm | realized_peak_temp_C   electrical_resistance_mOhm (no edge) | realized_peak_temp_C   electrical_resistance_mOhm (no edge) | realized_peak_temp_C->electrical_resistance_mOhm | realized_peak_temp_C->electrical_resistance_mOhm | realized_peak_temp_C->electrical_resistance_mOhm | no edge | (realized_peak_temp_C, electrical_resistance_mOhm)=A |
| realized_peak_temp_C, preheat_soak_setpoint_C | realized_peak_temp_C   preheat_soak_setpoint_C (no edge) | realized_peak_temp_C   preheat_soak_setpoint_C (no edge) | realized_peak_temp_C->preheat_soak_setpoint_C | realized_peak_temp_C->preheat_soak_setpoint_C | realized_peak_temp_C->preheat_soak_setpoint_C | no edge | (realized_peak_temp_C, preheat_soak_setpoint_C)=A |
| peak_zone_setpoint_C, electrical_resistance_mOhm | peak_zone_setpoint_C o-o electrical_resistance_mOhm | peak_zone_setpoint_C   electrical_resistance_mOhm (no edge) | peak_zone_setpoint_C->electrical_resistance_mOhm | peak_zone_setpoint_C->electrical_resistance_mOhm | peak_zone_setpoint_C->electrical_resistance_mOhm | electrical_resistance_mOhm -> peak_zone_setpoint_C | (peak_zone_setpoint_C, electrical_resistance_mOhm)=A |
| peak_zone_setpoint_C, preheat_soak_setpoint_C | peak_zone_setpoint_C   preheat_soak_setpoint_C (no edge) | peak_zone_setpoint_C   preheat_soak_setpoint_C (no edge) | peak_zone_setpoint_C->preheat_soak_setpoint_C | peak_zone_setpoint_C->preheat_soak_setpoint_C | peak_zone_setpoint_C->preheat_soak_setpoint_C | no edge | (peak_zone_setpoint_C, preheat_soak_setpoint_C)=A |
| electrical_resistance_mOhm, preheat_soak_setpoint_C | electrical_resistance_mOhm   preheat_soak_setpoint_C (no edge) | electrical_resistance_mOhm   preheat_soak_setpoint_C (no edge) | electrical_resistance_mOhm->preheat_soak_setpoint_C | electrical_resistance_mOhm->preheat_soak_setpoint_C | electrical_resistance_mOhm->preheat_soak_setpoint_C | no edge | (electrical_resistance_mOhm, preheat_soak_setpoint_C)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
