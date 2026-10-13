# Edge lineage: 20261011T194112Z_s2_q023_r01_4a0c60

Dataset `/research/datasets/suite_q1s2/q023/q023.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 21 variables, 210 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 22 | 0.82 | 0.47 | 0.60 | 4 | 1 | 13 | 40 |
| S1 after bootstrap edits | 6 | 0.83 | 0.13 | 0.23 | 3 | 1 | 1 | 37 |
| S2 after LLM review | 20 | 0.30 | 0.16 | 0.21 | 5 | 0 | 1 | 48 |
| S3 after KCI pruning | 20 | 0.30 | 0.16 | 0.21 | 5 | 0 | 1 | 48 |
| S4 final (after cycle step) | 20 | 0.30 | 0.16 | 0.21 | 5 | 0 | 1 | 48 |

Scored against: reference graph s2_02_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 16. Of the deleted, 9 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 21 calls, 210 distinct pairs answered out of 210, plus 21 self-pairs. Letters: {"A": 16, "B": 1, "C": 126, "D": 67}.
- LLM effect: added 16 (of which 15 where the resamples showed no edge at frequency >= 0.9), removed 2, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 20 edges; set by {"llm": 16, "algorithm (unchanged)": 4}; 4 identical to the algorithm's output; 16 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| V17_observed_unsafe_label->V16_unsafe_crossing_true | llm | no | 1.00 |
| V17_observed_unsafe_label o-> V23_abandonment_indicator | algorithm (unchanged) | yes | 0.05 |
| V14_focal_walking_speed_mps->V19_ped_traverse_time_s | llm | no | 1.00 |
| V16_unsafe_crossing_true->V21_near_conflict_flag | llm | no | 0.95 |
| V8_visible_remaining_seconds->V1_countdown_policy_enabled | llm | no | 0.85 |
| V4_illumination_weather_state->V8_visible_remaining_seconds | algorithm (unchanged) | yes | 0.00 |
| V23_abandonment_indicator->V5_traffic_flow_rate_vpm | algorithm (unchanged) | yes | 0.00 |
| V1_countdown_policy_enabled->V24_start_decision_now | llm | no | 1.00 |
| V1_countdown_policy_enabled->V11_time_pressure_index | llm | no | 1.00 |
| V1_countdown_policy_enabled->V22_wait_time_until_walk_s | llm | no | 1.00 |
| V1_countdown_policy_enabled->V7_timer_visibility_quality | llm | no | 1.00 |
| V5_traffic_flow_rate_vpm->V21_near_conflict_flag | llm | no | 1.00 |
| V10_older_adult_share->V19_ped_traverse_time_s | llm | no | 1.00 |
| V18_vehicle_approach_speed_mps->V21_near_conflict_flag | llm | no | 0.95 |
| V21_near_conflict_flag->V22_wait_time_until_walk_s | algorithm (unchanged) | yes | 0.00 |
| V22_wait_time_until_walk_s->V15_start_time_rel_phase_end_s | llm | no | 1.00 |
| V22_wait_time_until_walk_s->V3_signal_cycle_length_s | llm | no | 1.00 |
| V22_wait_time_until_walk_s->V6_arrival_time_within_cycle_s | llm | no | 1.00 |
| V4_illumination_weather_state->V7_timer_visibility_quality | llm | no | 1.00 |
| V15_start_time_rel_phase_end_s->V6_arrival_time_within_cycle_s | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| V17_observed_unsafe_label, V14_focal_walking_speed_mps | V17_observed_unsafe_label o-o V14_focal_walking_speed_mps | V17_observed_unsafe_label   V14_focal_walking_speed_mps (no edge) | V17_observed_unsafe_label   V14_focal_walking_speed_mps (no edge) | V17_observed_unsafe_label   V14_focal_walking_speed_mps (no edge) | V17_observed_unsafe_label   V14_focal_walking_speed_mps (no edge) | V17_observed_unsafe_label -> V14_focal_walking_speed_mps | (V17_observed_unsafe_label, V14_focal_walking_speed_mps)=D |
| V17_observed_unsafe_label, V16_unsafe_crossing_true | V17_observed_unsafe_label   V16_unsafe_crossing_true (no edge) | V17_observed_unsafe_label   V16_unsafe_crossing_true (no edge) | V17_observed_unsafe_label->V16_unsafe_crossing_true | V17_observed_unsafe_label->V16_unsafe_crossing_true | V17_observed_unsafe_label->V16_unsafe_crossing_true | no edge | (V17_observed_unsafe_label, V16_unsafe_crossing_true)=A |
| V14_focal_walking_speed_mps, V23_abandonment_indicator | V14_focal_walking_speed_mps o-> V23_abandonment_indicator | V14_focal_walking_speed_mps   V23_abandonment_indicator (no edge) | V14_focal_walking_speed_mps   V23_abandonment_indicator (no edge) | V14_focal_walking_speed_mps   V23_abandonment_indicator (no edge) | V14_focal_walking_speed_mps   V23_abandonment_indicator (no edge) | no edge | (V14_focal_walking_speed_mps, V23_abandonment_indicator)=C |
| V14_focal_walking_speed_mps, V19_ped_traverse_time_s | V14_focal_walking_speed_mps   V19_ped_traverse_time_s (no edge) | V14_focal_walking_speed_mps   V19_ped_traverse_time_s (no edge) | V14_focal_walking_speed_mps->V19_ped_traverse_time_s | V14_focal_walking_speed_mps->V19_ped_traverse_time_s | V14_focal_walking_speed_mps->V19_ped_traverse_time_s | no edge | (V14_focal_walking_speed_mps, V19_ped_traverse_time_s)=A |
| V16_unsafe_crossing_true, V5_traffic_flow_rate_vpm | V16_unsafe_crossing_true <-> V5_traffic_flow_rate_vpm | V16_unsafe_crossing_true   V5_traffic_flow_rate_vpm (no edge) | V16_unsafe_crossing_true   V5_traffic_flow_rate_vpm (no edge) | V16_unsafe_crossing_true   V5_traffic_flow_rate_vpm (no edge) | V16_unsafe_crossing_true   V5_traffic_flow_rate_vpm (no edge) | V16_unsafe_crossing_true -> V5_traffic_flow_rate_vpm | (V16_unsafe_crossing_true, V5_traffic_flow_rate_vpm)=C |
| V16_unsafe_crossing_true, V18_vehicle_approach_speed_mps | V16_unsafe_crossing_true->V18_vehicle_approach_speed_mps | V16_unsafe_crossing_true->V18_vehicle_approach_speed_mps | V16_unsafe_crossing_true   V18_vehicle_approach_speed_mps (no edge) | V16_unsafe_crossing_true   V18_vehicle_approach_speed_mps (no edge) | V16_unsafe_crossing_true   V18_vehicle_approach_speed_mps (no edge) | V18_vehicle_approach_speed_mps -> V16_unsafe_crossing_true | (V16_unsafe_crossing_true, V18_vehicle_approach_speed_mps)=C |
| V16_unsafe_crossing_true, V22_wait_time_until_walk_s | V16_unsafe_crossing_true <-> V22_wait_time_until_walk_s | V16_unsafe_crossing_true   V22_wait_time_until_walk_s (no edge) | V16_unsafe_crossing_true   V22_wait_time_until_walk_s (no edge) | V16_unsafe_crossing_true   V22_wait_time_until_walk_s (no edge) | V16_unsafe_crossing_true   V22_wait_time_until_walk_s (no edge) | V16_unsafe_crossing_true -> V22_wait_time_until_walk_s | (V16_unsafe_crossing_true, V22_wait_time_until_walk_s)=C |
| V16_unsafe_crossing_true, V21_near_conflict_flag | V16_unsafe_crossing_true   V21_near_conflict_flag (no edge) | V16_unsafe_crossing_true   V21_near_conflict_flag (no edge) | V16_unsafe_crossing_true->V21_near_conflict_flag | V16_unsafe_crossing_true->V21_near_conflict_flag | V16_unsafe_crossing_true->V21_near_conflict_flag | no edge | (V16_unsafe_crossing_true, V21_near_conflict_flag)=A |
| V9_group_size_at_decision, V2_curb_extension_present | V9_group_size_at_decision o-> V2_curb_extension_present | V9_group_size_at_decision   V2_curb_extension_present (no edge) | V9_group_size_at_decision   V2_curb_extension_present (no edge) | V9_group_size_at_decision   V2_curb_extension_present (no edge) | V9_group_size_at_decision   V2_curb_extension_present (no edge) | no edge | (V9_group_size_at_decision, V2_curb_extension_present)=C |
| V8_visible_remaining_seconds, V1_countdown_policy_enabled | V8_visible_remaining_seconds   V1_countdown_policy_enabled (no edge) | V8_visible_remaining_seconds   V1_countdown_policy_enabled (no edge) | V8_visible_remaining_seconds->V1_countdown_policy_enabled | V8_visible_remaining_seconds->V1_countdown_policy_enabled | V8_visible_remaining_seconds->V1_countdown_policy_enabled | V8_visible_remaining_seconds -> V1_countdown_policy_enabled | (V8_visible_remaining_seconds, V1_countdown_policy_enabled)=A |
| V8_visible_remaining_seconds, V18_vehicle_approach_speed_mps | V8_visible_remaining_seconds->V18_vehicle_approach_speed_mps | V8_visible_remaining_seconds   V18_vehicle_approach_speed_mps (no edge) | V8_visible_remaining_seconds   V18_vehicle_approach_speed_mps (no edge) | V8_visible_remaining_seconds   V18_vehicle_approach_speed_mps (no edge) | V8_visible_remaining_seconds   V18_vehicle_approach_speed_mps (no edge) | V8_visible_remaining_seconds -> V18_vehicle_approach_speed_mps | (V8_visible_remaining_seconds, V18_vehicle_approach_speed_mps)=C |
| V23_abandonment_indicator, V4_illumination_weather_state | V23_abandonment_indicator <-> V4_illumination_weather_state | V23_abandonment_indicator   V4_illumination_weather_state (no edge) | V23_abandonment_indicator   V4_illumination_weather_state (no edge) | V23_abandonment_indicator   V4_illumination_weather_state (no edge) | V23_abandonment_indicator   V4_illumination_weather_state (no edge) | V4_illumination_weather_state -> V23_abandonment_indicator | (V23_abandonment_indicator, V4_illumination_weather_state)=D |
| V1_countdown_policy_enabled, V24_start_decision_now | V1_countdown_policy_enabled   V24_start_decision_now (no edge) | V1_countdown_policy_enabled   V24_start_decision_now (no edge) | V1_countdown_policy_enabled->V24_start_decision_now | V1_countdown_policy_enabled->V24_start_decision_now | V1_countdown_policy_enabled->V24_start_decision_now | no edge | (V1_countdown_policy_enabled, V24_start_decision_now)=A |
| V1_countdown_policy_enabled, V11_time_pressure_index | V1_countdown_policy_enabled   V11_time_pressure_index (no edge) | V1_countdown_policy_enabled   V11_time_pressure_index (no edge) | V1_countdown_policy_enabled->V11_time_pressure_index | V1_countdown_policy_enabled->V11_time_pressure_index | V1_countdown_policy_enabled->V11_time_pressure_index | no edge | (V1_countdown_policy_enabled, V11_time_pressure_index)=A |
| V1_countdown_policy_enabled, V19_ped_traverse_time_s | V1_countdown_policy_enabled o-o V19_ped_traverse_time_s | V1_countdown_policy_enabled   V19_ped_traverse_time_s (no edge) | V1_countdown_policy_enabled   V19_ped_traverse_time_s (no edge) | V1_countdown_policy_enabled   V19_ped_traverse_time_s (no edge) | V1_countdown_policy_enabled   V19_ped_traverse_time_s (no edge) | V1_countdown_policy_enabled -> V19_ped_traverse_time_s | (V1_countdown_policy_enabled, V19_ped_traverse_time_s)=C |
| V1_countdown_policy_enabled, V22_wait_time_until_walk_s | V1_countdown_policy_enabled   V22_wait_time_until_walk_s (no edge) | V1_countdown_policy_enabled   V22_wait_time_until_walk_s (no edge) | V1_countdown_policy_enabled->V22_wait_time_until_walk_s | V1_countdown_policy_enabled->V22_wait_time_until_walk_s | V1_countdown_policy_enabled->V22_wait_time_until_walk_s | no edge | (V1_countdown_policy_enabled, V22_wait_time_until_walk_s)=A |
| V1_countdown_policy_enabled, V15_start_time_rel_phase_end_s | V1_countdown_policy_enabled o-o V15_start_time_rel_phase_end_s | V1_countdown_policy_enabled   V15_start_time_rel_phase_end_s (no edge) | V1_countdown_policy_enabled   V15_start_time_rel_phase_end_s (no edge) | V1_countdown_policy_enabled   V15_start_time_rel_phase_end_s (no edge) | V1_countdown_policy_enabled   V15_start_time_rel_phase_end_s (no edge) | V1_countdown_policy_enabled -> V15_start_time_rel_phase_end_s | (V1_countdown_policy_enabled, V15_start_time_rel_phase_end_s)=C |
| V1_countdown_policy_enabled, V7_timer_visibility_quality | V1_countdown_policy_enabled   V7_timer_visibility_quality (no edge) | V1_countdown_policy_enabled   V7_timer_visibility_quality (no edge) | V1_countdown_policy_enabled->V7_timer_visibility_quality | V1_countdown_policy_enabled->V7_timer_visibility_quality | V1_countdown_policy_enabled->V7_timer_visibility_quality | no edge | (V1_countdown_policy_enabled, V7_timer_visibility_quality)=A |
| V24_start_decision_now, V3_signal_cycle_length_s | V24_start_decision_now o-> V3_signal_cycle_length_s | V24_start_decision_now   V3_signal_cycle_length_s (no edge) | V24_start_decision_now   V3_signal_cycle_length_s (no edge) | V24_start_decision_now   V3_signal_cycle_length_s (no edge) | V24_start_decision_now   V3_signal_cycle_length_s (no edge) | V24_start_decision_now -> V3_signal_cycle_length_s | (V24_start_decision_now, V3_signal_cycle_length_s)=D |
| V5_traffic_flow_rate_vpm, V21_near_conflict_flag | V5_traffic_flow_rate_vpm   V21_near_conflict_flag (no edge) | V5_traffic_flow_rate_vpm   V21_near_conflict_flag (no edge) | V5_traffic_flow_rate_vpm->V21_near_conflict_flag | V5_traffic_flow_rate_vpm->V21_near_conflict_flag | V5_traffic_flow_rate_vpm->V21_near_conflict_flag | no edge | (V5_traffic_flow_rate_vpm, V21_near_conflict_flag)=A |
| V11_time_pressure_index, V10_older_adult_share | V11_time_pressure_index o-> V10_older_adult_share | V11_time_pressure_index   V10_older_adult_share (no edge) | V11_time_pressure_index   V10_older_adult_share (no edge) | V11_time_pressure_index   V10_older_adult_share (no edge) | V11_time_pressure_index   V10_older_adult_share (no edge) | V11_time_pressure_index -> V10_older_adult_share | (V11_time_pressure_index, V10_older_adult_share)=C |
| V10_older_adult_share, V19_ped_traverse_time_s | V10_older_adult_share   V19_ped_traverse_time_s (no edge) | V10_older_adult_share   V19_ped_traverse_time_s (no edge) | V10_older_adult_share->V19_ped_traverse_time_s | V10_older_adult_share->V19_ped_traverse_time_s | V10_older_adult_share->V19_ped_traverse_time_s | no edge | (V10_older_adult_share, V19_ped_traverse_time_s)=A |
| V10_older_adult_share, V21_near_conflict_flag | V10_older_adult_share <-> V21_near_conflict_flag | V10_older_adult_share   V21_near_conflict_flag (no edge) | V10_older_adult_share   V21_near_conflict_flag (no edge) | V10_older_adult_share   V21_near_conflict_flag (no edge) | V10_older_adult_share   V21_near_conflict_flag (no edge) | V21_near_conflict_flag -> V10_older_adult_share | (V10_older_adult_share, V21_near_conflict_flag)=D |
| V18_vehicle_approach_speed_mps, V21_near_conflict_flag | V18_vehicle_approach_speed_mps   V21_near_conflict_flag (no edge) | V18_vehicle_approach_speed_mps   V21_near_conflict_flag (no edge) | V18_vehicle_approach_speed_mps->V21_near_conflict_flag | V18_vehicle_approach_speed_mps->V21_near_conflict_flag | V18_vehicle_approach_speed_mps->V21_near_conflict_flag | no edge | (V18_vehicle_approach_speed_mps, V21_near_conflict_flag)=A |
| V19_ped_traverse_time_s, V15_start_time_rel_phase_end_s | V19_ped_traverse_time_s o-o V15_start_time_rel_phase_end_s | V19_ped_traverse_time_s   V15_start_time_rel_phase_end_s (no edge) | V19_ped_traverse_time_s   V15_start_time_rel_phase_end_s (no edge) | V19_ped_traverse_time_s   V15_start_time_rel_phase_end_s (no edge) | V19_ped_traverse_time_s   V15_start_time_rel_phase_end_s (no edge) | no edge | (V19_ped_traverse_time_s, V15_start_time_rel_phase_end_s)=C |
| V22_wait_time_until_walk_s, V15_start_time_rel_phase_end_s | V22_wait_time_until_walk_s   V15_start_time_rel_phase_end_s (no edge) | V22_wait_time_until_walk_s   V15_start_time_rel_phase_end_s (no edge) | V22_wait_time_until_walk_s->V15_start_time_rel_phase_end_s | V22_wait_time_until_walk_s->V15_start_time_rel_phase_end_s | V22_wait_time_until_walk_s->V15_start_time_rel_phase_end_s | V22_wait_time_until_walk_s -> V15_start_time_rel_phase_end_s | (V22_wait_time_until_walk_s, V15_start_time_rel_phase_end_s)=A |
| V22_wait_time_until_walk_s, V3_signal_cycle_length_s | V22_wait_time_until_walk_s   V3_signal_cycle_length_s (no edge) | V22_wait_time_until_walk_s   V3_signal_cycle_length_s (no edge) | V22_wait_time_until_walk_s->V3_signal_cycle_length_s | V22_wait_time_until_walk_s->V3_signal_cycle_length_s | V22_wait_time_until_walk_s->V3_signal_cycle_length_s | no edge | (V22_wait_time_until_walk_s, V3_signal_cycle_length_s)=A |
| V22_wait_time_until_walk_s, V6_arrival_time_within_cycle_s | V22_wait_time_until_walk_s   V6_arrival_time_within_cycle_s (no edge) | V22_wait_time_until_walk_s   V6_arrival_time_within_cycle_s (no edge) | V22_wait_time_until_walk_s->V6_arrival_time_within_cycle_s | V22_wait_time_until_walk_s->V6_arrival_time_within_cycle_s | V22_wait_time_until_walk_s->V6_arrival_time_within_cycle_s | no edge | (V22_wait_time_until_walk_s, V6_arrival_time_within_cycle_s)=A |
| V4_illumination_weather_state, V7_timer_visibility_quality | V4_illumination_weather_state   V7_timer_visibility_quality (no edge) | V4_illumination_weather_state   V7_timer_visibility_quality (no edge) | V4_illumination_weather_state->V7_timer_visibility_quality | V4_illumination_weather_state->V7_timer_visibility_quality | V4_illumination_weather_state->V7_timer_visibility_quality | no edge | (V4_illumination_weather_state, V7_timer_visibility_quality)=A |
| V4_illumination_weather_state, V6_arrival_time_within_cycle_s | V6_arrival_time_within_cycle_s o-> V4_illumination_weather_state | V4_illumination_weather_state   V6_arrival_time_within_cycle_s (no edge) | V4_illumination_weather_state   V6_arrival_time_within_cycle_s (no edge) | V4_illumination_weather_state   V6_arrival_time_within_cycle_s (no edge) | V4_illumination_weather_state   V6_arrival_time_within_cycle_s (no edge) | V6_arrival_time_within_cycle_s -> V4_illumination_weather_state | (V4_illumination_weather_state, V6_arrival_time_within_cycle_s)=C |
| V21_near_conflict_flag, V3_signal_cycle_length_s | V21_near_conflict_flag <-> V3_signal_cycle_length_s | V21_near_conflict_flag   V3_signal_cycle_length_s (no edge) | V21_near_conflict_flag   V3_signal_cycle_length_s (no edge) | V21_near_conflict_flag   V3_signal_cycle_length_s (no edge) | V21_near_conflict_flag   V3_signal_cycle_length_s (no edge) | V21_near_conflict_flag -> V3_signal_cycle_length_s | (V21_near_conflict_flag, V3_signal_cycle_length_s)=D |
| V15_start_time_rel_phase_end_s, V6_arrival_time_within_cycle_s | V15_start_time_rel_phase_end_s   V6_arrival_time_within_cycle_s (no edge) | V15_start_time_rel_phase_end_s   V6_arrival_time_within_cycle_s (no edge) | V15_start_time_rel_phase_end_s->V6_arrival_time_within_cycle_s | V15_start_time_rel_phase_end_s->V6_arrival_time_within_cycle_s | V15_start_time_rel_phase_end_s->V6_arrival_time_within_cycle_s | no edge | (V15_start_time_rel_phase_end_s, V6_arrival_time_within_cycle_s)=A |
| V7_timer_visibility_quality, V3_signal_cycle_length_s | V7_timer_visibility_quality o-> V3_signal_cycle_length_s | V7_timer_visibility_quality   V3_signal_cycle_length_s (no edge) | V7_timer_visibility_quality   V3_signal_cycle_length_s (no edge) | V7_timer_visibility_quality   V3_signal_cycle_length_s (no edge) | V7_timer_visibility_quality   V3_signal_cycle_length_s (no edge) | V7_timer_visibility_quality -> V3_signal_cycle_length_s | (V7_timer_visibility_quality, V3_signal_cycle_length_s)=C |
| V6_arrival_time_within_cycle_s, V2_curb_extension_present | V6_arrival_time_within_cycle_s o-> V2_curb_extension_present | V6_arrival_time_within_cycle_s o-> V2_curb_extension_present | V6_arrival_time_within_cycle_s   V2_curb_extension_present (no edge) | V6_arrival_time_within_cycle_s   V2_curb_extension_present (no edge) | V6_arrival_time_within_cycle_s   V2_curb_extension_present (no edge) | no edge | (V6_arrival_time_within_cycle_s, V2_curb_extension_present)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
