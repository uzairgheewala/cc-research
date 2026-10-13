# Edge lineage: 20261011T192513Z_s2_q021_r01_dfa292

Dataset `/research/datasets/suite_q1s2/q021/q021.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 21 variables, 210 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 19 | 0.84 | 0.42 | 0.56 | 5 | 0 | 11 | 38 |
| S1 after bootstrap edits | 5 | 1.00 | 0.13 | 0.23 | 4 | 0 | 1 | 35 |
| S2 after LLM review | 25 | 0.52 | 0.34 | 0.41 | 8 | 5 | 0 | 44 |
| S3 after KCI pruning | 20 | 0.60 | 0.32 | 0.41 | 7 | 5 | 0 | 41 |
| S4 final (after cycle step) | 20 | 0.60 | 0.32 | 0.41 | 7 | 5 | 0 | 41 |

Scored against: reference graph s2_02_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 14. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 21 calls, 210 distinct pairs answered out of 210, plus 21 self-pairs. Letters: {"A": 16, "B": 8, "C": 122, "D": 64}.
- LLM effect: added 22 (of which 16 where the resamples showed no edge at frequency >= 0.9), removed 2, re-oriented 0.
- KCI step removed 5. Cycle step changed 0.
- Final graph: 20 edges; set by {"llm": 17, "algorithm (unchanged)": 3}; 4 identical to the algorithm's output; 12 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V17_observed_unsafe_label->V16_unsafe_crossing_true | llm | yes | 0.00 |
| V10_older_adult_share->V14_focal_walking_speed_mps | llm | yes | 0.00 |
| V14_focal_walking_speed_mps->V19_ped_traverse_time_s | algorithm (unchanged) | yes | 0.00 |
| V23_abandonment_indicator->V8_visible_remaining_seconds | llm | no | 1.00 |
| V23_abandonment_indicator->V11_time_pressure_index | llm | no | 0.90 |
| V23_abandonment_indicator->V5_traffic_flow_rate_vpm | llm | no | 0.90 |
| V23_abandonment_indicator->V18_vehicle_approach_speed_mps | llm | no | 0.95 |
| V23_abandonment_indicator->V22_wait_time_until_walk_s | llm | no | 1.00 |
| V23_abandonment_indicator->V19_ped_traverse_time_s | llm | no | 1.00 |
| V23_abandonment_indicator->V21_near_conflict_flag | llm | no | 0.60 |
| V8_visible_remaining_seconds->V11_time_pressure_index | algorithm (unchanged) | yes | 0.00 |
| V1_countdown_policy_enabled->V11_time_pressure_index | llm | no | 1.00 |
| V1_countdown_policy_enabled->V22_wait_time_until_walk_s | llm | no | 1.00 |
| V1_countdown_policy_enabled->V7_timer_visibility_quality | llm | yes | 0.00 |
| V11_time_pressure_index->V7_timer_visibility_quality | llm | no | 0.95 |
| V10_older_adult_share->V19_ped_traverse_time_s | llm | no | 0.90 |
| V22_wait_time_until_walk_s->V3_signal_cycle_length_s | llm | no | 1.00 |
| V2_curb_extension_present->V19_ped_traverse_time_s | algorithm (unchanged) | yes | 0.00 |
| V3_signal_cycle_length_s->V6_arrival_time_within_cycle_s | llm | yes | 0.00 |
| V4_illumination_weather_state->V7_timer_visibility_quality | llm | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V16_unsafe_crossing_true, V17_observed_unsafe_label | V16_unsafe_crossing_true o-o V17_observed_unsafe_label | V16_unsafe_crossing_true   V17_observed_unsafe_label (no edge) | V17_observed_unsafe_label->V16_unsafe_crossing_true | V17_observed_unsafe_label->V16_unsafe_crossing_true | V17_observed_unsafe_label->V16_unsafe_crossing_true | V16_unsafe_crossing_true -> V17_observed_unsafe_label | (V16_unsafe_crossing_true, V17_observed_unsafe_label)=B |
| V16_unsafe_crossing_true, V8_visible_remaining_seconds | V16_unsafe_crossing_true o-> V8_visible_remaining_seconds | V16_unsafe_crossing_true o-> V8_visible_remaining_seconds | V16_unsafe_crossing_true   V8_visible_remaining_seconds (no edge) | V16_unsafe_crossing_true   V8_visible_remaining_seconds (no edge) | V16_unsafe_crossing_true   V8_visible_remaining_seconds (no edge) | V8_visible_remaining_seconds -> V16_unsafe_crossing_true | (V16_unsafe_crossing_true, V8_visible_remaining_seconds)=C |
| V16_unsafe_crossing_true, V21_near_conflict_flag | V16_unsafe_crossing_true   V21_near_conflict_flag (no edge) | V16_unsafe_crossing_true   V21_near_conflict_flag (no edge) | V21_near_conflict_flag->V16_unsafe_crossing_true | V16_unsafe_crossing_true   V21_near_conflict_flag (no edge) | V16_unsafe_crossing_true   V21_near_conflict_flag (no edge) | no edge | (V16_unsafe_crossing_true, V21_near_conflict_flag)=B |
| V17_observed_unsafe_label, V8_visible_remaining_seconds | V17_observed_unsafe_label o-> V8_visible_remaining_seconds | V17_observed_unsafe_label   V8_visible_remaining_seconds (no edge) | V17_observed_unsafe_label   V8_visible_remaining_seconds (no edge) | V17_observed_unsafe_label   V8_visible_remaining_seconds (no edge) | V17_observed_unsafe_label   V8_visible_remaining_seconds (no edge) | no edge | (V17_observed_unsafe_label, V8_visible_remaining_seconds)=D |
| V14_focal_walking_speed_mps, V10_older_adult_share | V14_focal_walking_speed_mps o-o V10_older_adult_share | V14_focal_walking_speed_mps   V10_older_adult_share (no edge) | V10_older_adult_share->V14_focal_walking_speed_mps | V10_older_adult_share->V14_focal_walking_speed_mps | V10_older_adult_share->V14_focal_walking_speed_mps | V10_older_adult_share -> V14_focal_walking_speed_mps | (V14_focal_walking_speed_mps, V10_older_adult_share)=B |
| V23_abandonment_indicator, V8_visible_remaining_seconds | V23_abandonment_indicator   V8_visible_remaining_seconds (no edge) | V23_abandonment_indicator   V8_visible_remaining_seconds (no edge) | V23_abandonment_indicator->V8_visible_remaining_seconds | V23_abandonment_indicator->V8_visible_remaining_seconds | V23_abandonment_indicator->V8_visible_remaining_seconds | no edge | (V23_abandonment_indicator, V8_visible_remaining_seconds)=A |
| V23_abandonment_indicator, V24_start_decision_now | V23_abandonment_indicator   V24_start_decision_now (no edge) | V23_abandonment_indicator   V24_start_decision_now (no edge) | V24_start_decision_now->V23_abandonment_indicator | V23_abandonment_indicator   V24_start_decision_now (no edge) | V23_abandonment_indicator   V24_start_decision_now (no edge) | no edge | (V23_abandonment_indicator, V24_start_decision_now)=B |
| V23_abandonment_indicator, V11_time_pressure_index | V23_abandonment_indicator   V11_time_pressure_index (no edge) | V23_abandonment_indicator   V11_time_pressure_index (no edge) | V23_abandonment_indicator->V11_time_pressure_index | V23_abandonment_indicator->V11_time_pressure_index | V23_abandonment_indicator->V11_time_pressure_index | V11_time_pressure_index -> V23_abandonment_indicator | (V23_abandonment_indicator, V11_time_pressure_index)=A |
| V23_abandonment_indicator, V5_traffic_flow_rate_vpm | V23_abandonment_indicator   V5_traffic_flow_rate_vpm (no edge) | V23_abandonment_indicator   V5_traffic_flow_rate_vpm (no edge) | V23_abandonment_indicator->V5_traffic_flow_rate_vpm | V23_abandonment_indicator->V5_traffic_flow_rate_vpm | V23_abandonment_indicator->V5_traffic_flow_rate_vpm | no edge | (V23_abandonment_indicator, V5_traffic_flow_rate_vpm)=A |
| V23_abandonment_indicator, V18_vehicle_approach_speed_mps | V23_abandonment_indicator   V18_vehicle_approach_speed_mps (no edge) | V23_abandonment_indicator   V18_vehicle_approach_speed_mps (no edge) | V23_abandonment_indicator->V18_vehicle_approach_speed_mps | V23_abandonment_indicator->V18_vehicle_approach_speed_mps | V23_abandonment_indicator->V18_vehicle_approach_speed_mps | no edge | (V23_abandonment_indicator, V18_vehicle_approach_speed_mps)=A |
| V23_abandonment_indicator, V22_wait_time_until_walk_s | V23_abandonment_indicator   V22_wait_time_until_walk_s (no edge) | V23_abandonment_indicator   V22_wait_time_until_walk_s (no edge) | V23_abandonment_indicator->V22_wait_time_until_walk_s | V23_abandonment_indicator->V22_wait_time_until_walk_s | V23_abandonment_indicator->V22_wait_time_until_walk_s | V22_wait_time_until_walk_s -> V23_abandonment_indicator | (V23_abandonment_indicator, V22_wait_time_until_walk_s)=A |
| V23_abandonment_indicator, V19_ped_traverse_time_s | V23_abandonment_indicator   V19_ped_traverse_time_s (no edge) | V23_abandonment_indicator   V19_ped_traverse_time_s (no edge) | V23_abandonment_indicator->V19_ped_traverse_time_s | V23_abandonment_indicator->V19_ped_traverse_time_s | V23_abandonment_indicator->V19_ped_traverse_time_s | no edge | (V23_abandonment_indicator, V19_ped_traverse_time_s)=A |
| V23_abandonment_indicator, V21_near_conflict_flag | V23_abandonment_indicator   V21_near_conflict_flag (no edge) | V23_abandonment_indicator   V21_near_conflict_flag (no edge) | V23_abandonment_indicator->V21_near_conflict_flag | V23_abandonment_indicator->V21_near_conflict_flag | V23_abandonment_indicator->V21_near_conflict_flag | no edge | (V23_abandonment_indicator, V21_near_conflict_flag)=A |
| V9_group_size_at_decision, V6_arrival_time_within_cycle_s | V6_arrival_time_within_cycle_s->V9_group_size_at_decision | V6_arrival_time_within_cycle_s->V9_group_size_at_decision | V9_group_size_at_decision   V6_arrival_time_within_cycle_s (no edge) | V9_group_size_at_decision   V6_arrival_time_within_cycle_s (no edge) | V9_group_size_at_decision   V6_arrival_time_within_cycle_s (no edge) | V6_arrival_time_within_cycle_s -> V9_group_size_at_decision | (V9_group_size_at_decision, V6_arrival_time_within_cycle_s)=C |
| V8_visible_remaining_seconds, V1_countdown_policy_enabled | V8_visible_remaining_seconds   V1_countdown_policy_enabled (no edge) | V8_visible_remaining_seconds   V1_countdown_policy_enabled (no edge) | V1_countdown_policy_enabled->V8_visible_remaining_seconds | V8_visible_remaining_seconds   V1_countdown_policy_enabled (no edge) | V8_visible_remaining_seconds   V1_countdown_policy_enabled (no edge) | no edge | (V8_visible_remaining_seconds, V1_countdown_policy_enabled)=B |
| V8_visible_remaining_seconds, V22_wait_time_until_walk_s | V8_visible_remaining_seconds   V22_wait_time_until_walk_s (no edge) | V8_visible_remaining_seconds   V22_wait_time_until_walk_s (no edge) | V22_wait_time_until_walk_s->V8_visible_remaining_seconds | V8_visible_remaining_seconds   V22_wait_time_until_walk_s (no edge) | V8_visible_remaining_seconds   V22_wait_time_until_walk_s (no edge) | no edge | (V8_visible_remaining_seconds, V22_wait_time_until_walk_s)=B |
| V8_visible_remaining_seconds, V6_arrival_time_within_cycle_s | V8_visible_remaining_seconds <-> V6_arrival_time_within_cycle_s | V8_visible_remaining_seconds   V6_arrival_time_within_cycle_s (no edge) | V8_visible_remaining_seconds   V6_arrival_time_within_cycle_s (no edge) | V8_visible_remaining_seconds   V6_arrival_time_within_cycle_s (no edge) | V8_visible_remaining_seconds   V6_arrival_time_within_cycle_s (no edge) | V6_arrival_time_within_cycle_s -> V8_visible_remaining_seconds | (V8_visible_remaining_seconds, V6_arrival_time_within_cycle_s)=C |
| V8_visible_remaining_seconds, V3_signal_cycle_length_s | V8_visible_remaining_seconds   V3_signal_cycle_length_s (no edge) | V8_visible_remaining_seconds   V3_signal_cycle_length_s (no edge) | V3_signal_cycle_length_s->V8_visible_remaining_seconds | V8_visible_remaining_seconds   V3_signal_cycle_length_s (no edge) | V8_visible_remaining_seconds   V3_signal_cycle_length_s (no edge) | V3_signal_cycle_length_s -> V8_visible_remaining_seconds | (V8_visible_remaining_seconds, V3_signal_cycle_length_s)=B |
| V24_start_decision_now, V22_wait_time_until_walk_s | V24_start_decision_now o-o V22_wait_time_until_walk_s | V24_start_decision_now   V22_wait_time_until_walk_s (no edge) | V24_start_decision_now   V22_wait_time_until_walk_s (no edge) | V24_start_decision_now   V22_wait_time_until_walk_s (no edge) | V24_start_decision_now   V22_wait_time_until_walk_s (no edge) | V24_start_decision_now -> V22_wait_time_until_walk_s | (V24_start_decision_now, V22_wait_time_until_walk_s)=D |
| V24_start_decision_now, V21_near_conflict_flag | V24_start_decision_now o-o V21_near_conflict_flag | V24_start_decision_now   V21_near_conflict_flag (no edge) | V24_start_decision_now   V21_near_conflict_flag (no edge) | V24_start_decision_now   V21_near_conflict_flag (no edge) | V24_start_decision_now   V21_near_conflict_flag (no edge) | V24_start_decision_now -> V21_near_conflict_flag | (V24_start_decision_now, V21_near_conflict_flag)=D |
| V1_countdown_policy_enabled, V11_time_pressure_index | V1_countdown_policy_enabled   V11_time_pressure_index (no edge) | V1_countdown_policy_enabled   V11_time_pressure_index (no edge) | V1_countdown_policy_enabled->V11_time_pressure_index | V1_countdown_policy_enabled->V11_time_pressure_index | V1_countdown_policy_enabled->V11_time_pressure_index | no edge | (V1_countdown_policy_enabled, V11_time_pressure_index)=A |
| V1_countdown_policy_enabled, V22_wait_time_until_walk_s | V1_countdown_policy_enabled   V22_wait_time_until_walk_s (no edge) | V1_countdown_policy_enabled   V22_wait_time_until_walk_s (no edge) | V1_countdown_policy_enabled->V22_wait_time_until_walk_s | V1_countdown_policy_enabled->V22_wait_time_until_walk_s | V1_countdown_policy_enabled->V22_wait_time_until_walk_s | no edge | (V1_countdown_policy_enabled, V22_wait_time_until_walk_s)=A |
| V1_countdown_policy_enabled, V7_timer_visibility_quality | V1_countdown_policy_enabled o-> V7_timer_visibility_quality | V1_countdown_policy_enabled   V7_timer_visibility_quality (no edge) | V1_countdown_policy_enabled->V7_timer_visibility_quality | V1_countdown_policy_enabled->V7_timer_visibility_quality | V1_countdown_policy_enabled->V7_timer_visibility_quality | V1_countdown_policy_enabled -> V7_timer_visibility_quality | (V1_countdown_policy_enabled, V7_timer_visibility_quality)=A |
| V11_time_pressure_index, V7_timer_visibility_quality | V11_time_pressure_index   V7_timer_visibility_quality (no edge) | V11_time_pressure_index   V7_timer_visibility_quality (no edge) | V11_time_pressure_index->V7_timer_visibility_quality | V11_time_pressure_index->V7_timer_visibility_quality | V11_time_pressure_index->V7_timer_visibility_quality | V7_timer_visibility_quality -> V11_time_pressure_index | (V11_time_pressure_index, V7_timer_visibility_quality)=A |
| V5_traffic_flow_rate_vpm, V18_vehicle_approach_speed_mps | V5_traffic_flow_rate_vpm o-> V18_vehicle_approach_speed_mps | V5_traffic_flow_rate_vpm   V18_vehicle_approach_speed_mps (no edge) | V5_traffic_flow_rate_vpm   V18_vehicle_approach_speed_mps (no edge) | V5_traffic_flow_rate_vpm   V18_vehicle_approach_speed_mps (no edge) | V5_traffic_flow_rate_vpm   V18_vehicle_approach_speed_mps (no edge) | V5_traffic_flow_rate_vpm -> V18_vehicle_approach_speed_mps | (V5_traffic_flow_rate_vpm, V18_vehicle_approach_speed_mps)=C |
| V18_vehicle_approach_speed_mps, V2_curb_extension_present | V18_vehicle_approach_speed_mps <-> V2_curb_extension_present | V18_vehicle_approach_speed_mps   V2_curb_extension_present (no edge) | V18_vehicle_approach_speed_mps   V2_curb_extension_present (no edge) | V18_vehicle_approach_speed_mps   V2_curb_extension_present (no edge) | V18_vehicle_approach_speed_mps   V2_curb_extension_present (no edge) | V2_curb_extension_present -> V18_vehicle_approach_speed_mps | (V18_vehicle_approach_speed_mps, V2_curb_extension_present)=C |
| V10_older_adult_share, V19_ped_traverse_time_s | V10_older_adult_share   V19_ped_traverse_time_s (no edge) | V10_older_adult_share   V19_ped_traverse_time_s (no edge) | V10_older_adult_share->V19_ped_traverse_time_s | V10_older_adult_share->V19_ped_traverse_time_s | V10_older_adult_share->V19_ped_traverse_time_s | no edge | (V10_older_adult_share, V19_ped_traverse_time_s)=A |
| V22_wait_time_until_walk_s, V21_near_conflict_flag | V22_wait_time_until_walk_s o-o V21_near_conflict_flag | V22_wait_time_until_walk_s   V21_near_conflict_flag (no edge) | V22_wait_time_until_walk_s   V21_near_conflict_flag (no edge) | V22_wait_time_until_walk_s   V21_near_conflict_flag (no edge) | V22_wait_time_until_walk_s   V21_near_conflict_flag (no edge) | no edge | (V22_wait_time_until_walk_s, V21_near_conflict_flag)=C |
| V22_wait_time_until_walk_s, V3_signal_cycle_length_s | V22_wait_time_until_walk_s   V3_signal_cycle_length_s (no edge) | V22_wait_time_until_walk_s   V3_signal_cycle_length_s (no edge) | V22_wait_time_until_walk_s->V3_signal_cycle_length_s | V22_wait_time_until_walk_s->V3_signal_cycle_length_s | V22_wait_time_until_walk_s->V3_signal_cycle_length_s | V3_signal_cycle_length_s -> V22_wait_time_until_walk_s | (V22_wait_time_until_walk_s, V3_signal_cycle_length_s)=A |
| V6_arrival_time_within_cycle_s, V3_signal_cycle_length_s | V3_signal_cycle_length_s->V6_arrival_time_within_cycle_s | V6_arrival_time_within_cycle_s   V3_signal_cycle_length_s (no edge) | V3_signal_cycle_length_s->V6_arrival_time_within_cycle_s | V3_signal_cycle_length_s->V6_arrival_time_within_cycle_s | V3_signal_cycle_length_s->V6_arrival_time_within_cycle_s | V3_signal_cycle_length_s -> V6_arrival_time_within_cycle_s | (V6_arrival_time_within_cycle_s, V3_signal_cycle_length_s)=B |
| V2_curb_extension_present, V7_timer_visibility_quality | V2_curb_extension_present <-> V7_timer_visibility_quality | V2_curb_extension_present   V7_timer_visibility_quality (no edge) | V2_curb_extension_present   V7_timer_visibility_quality (no edge) | V2_curb_extension_present   V7_timer_visibility_quality (no edge) | V2_curb_extension_present   V7_timer_visibility_quality (no edge) | V2_curb_extension_present -> V7_timer_visibility_quality | (V2_curb_extension_present, V7_timer_visibility_quality)=C |
| V4_illumination_weather_state, V7_timer_visibility_quality | V4_illumination_weather_state o-> V7_timer_visibility_quality | V4_illumination_weather_state   V7_timer_visibility_quality (no edge) | V4_illumination_weather_state->V7_timer_visibility_quality | V4_illumination_weather_state->V7_timer_visibility_quality | V4_illumination_weather_state->V7_timer_visibility_quality | V4_illumination_weather_state -> V7_timer_visibility_quality | (V4_illumination_weather_state, V7_timer_visibility_quality)=A |
| V3_signal_cycle_length_s, V15_start_time_rel_phase_end_s | V3_signal_cycle_length_s o-o V15_start_time_rel_phase_end_s | V3_signal_cycle_length_s   V15_start_time_rel_phase_end_s (no edge) | V3_signal_cycle_length_s   V15_start_time_rel_phase_end_s (no edge) | V3_signal_cycle_length_s   V15_start_time_rel_phase_end_s (no edge) | V3_signal_cycle_length_s   V15_start_time_rel_phase_end_s (no edge) | no edge | (V3_signal_cycle_length_s, V15_start_time_rel_phase_end_s)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
