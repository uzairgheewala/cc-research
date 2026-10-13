# Edge lineage: 20261011T233701Z_s2_q093_r01_b34927

Dataset `/research/datasets/suite_q1s2/q093/q093.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 24 | 0.88 | 0.60 | 0.71 | 7 | 1 | 13 | 31 |
| S1 after bootstrap edits | 13 | 0.92 | 0.34 | 0.50 | 7 | 1 | 4 | 29 |
| S2 after LLM review | 31 | 0.42 | 0.37 | 0.39 | 7 | 3 | 3 | 46 |
| S3 after KCI pruning | 30 | 0.43 | 0.37 | 0.40 | 7 | 3 | 3 | 45 |
| S4 final (after cycle step) | 30 | 0.43 | 0.37 | 0.40 | 7 | 3 | 3 | 45 |

Scored against: reference graph s2_09_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 11. Of the deleted, 6 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 21, "B": 2, "C": 102, "D": 106}.
- LLM effect: added 19 (of which 16 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 1.
- KCI step removed 1. Cycle step changed 0.
- Final graph: 30 edges; set by {"algorithm (unchanged)": 11, "llm": 19}; 11 identical to the algorithm's output; 17 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| morning_HRV_rMSSD->planned_nursing_minutes | algorithm (unchanged) | yes | 0.10 |
| cns_depressant_dose_index->morning_HRV_rMSSD | llm | no | 0.60 |
| morning_HRV_rMSSD->baseline_evening_pain_score | algorithm (unchanged) | yes | 0.10 |
| patient_acuity_score->nurse_staffing_ratio | llm | no | 1.00 |
| patient_acuity_score->planned_nursing_minutes | llm | no | 1.00 |
| morning_pain_score->patient_acuity_score | algorithm (unchanged) | yes | 0.05 |
| nurse_staffing_ratio->planned_nursing_minutes | llm | no | 0.85 |
| actigraphy_wear_fraction->perceived_noise_dose | algorithm (unchanged) | yes | 0.10 |
| arousal_threshold_index->nightly_alarm_count | algorithm (unchanged) | yes | 0.00 |
| comfort_kit_adherence_index->comfort_bundle_offered | llm | no | 1.00 |
| comfort_kit_adherence_index->alarm_quieting_bundle_state | algorithm (unchanged) | yes | 0.00 |
| perceived_lux_dose->night_lux_summary | llm | no | 0.95 |
| roommate_Lmax_spikes_count->perceived_noise_dose | llm | no | 0.95 |
| roommate_Lmax_spikes_count->sleep_fragmentation_index | llm | no | 0.95 |
| roommate_Lmax_spikes_count <-> morning_pain_score | algorithm (unchanged) | yes | 0.05 |
| planned_nursing_minutes <-> alarm_quieting_bundle_state | algorithm (unchanged) | yes | 0.00 |
| cns_depressant_dose_index->sleep_fragmentation_index | llm | no | 1.00 |
| room_acoustic_reverberation_gain->perceived_noise_dose | algorithm (unchanged) | yes | 0.00 |
| room_acoustic_reverberation_gain->sleep_fragmentation_index | llm | no | 1.00 |
| room_acoustic_reverberation_gain->alarm_related_LAeq | llm | no | 1.00 |
| vital_sign_schedule_frequency o-> sleep_fragmentation_index | algorithm (unchanged) | yes | 0.00 |
| nightly_alarm_count->perceived_noise_dose | llm | no | 1.00 |
| nightly_alarm_count->sleep_fragmentation_index | llm | yes | 0.00 |
| nightly_alarm_count->alarm_related_LAeq | llm | no | 1.00 |
| baseline_evening_pain_score->sleep_fragmentation_index | algorithm (unchanged) | yes | 0.05 |
| baseline_evening_pain_score->morning_pain_score | llm | no | 1.00 |
| perceived_noise_dose->sleep_fragmentation_index | llm | no | 1.00 |
| perceived_noise_dose->alarm_related_LAeq | llm | no | 1.00 |
| night_lux_summary->sleep_fragmentation_index | llm | yes | 0.45 |
| alarm_quieting_bundle_state->alarm_related_LAeq | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| morning_HRV_rMSSD, cns_depressant_dose_index | morning_HRV_rMSSD   cns_depressant_dose_index (no edge) | morning_HRV_rMSSD   cns_depressant_dose_index (no edge) | cns_depressant_dose_index->morning_HRV_rMSSD | cns_depressant_dose_index->morning_HRV_rMSSD | cns_depressant_dose_index->morning_HRV_rMSSD | morning_HRV_rMSSD -> cns_depressant_dose_index | (morning_HRV_rMSSD, cns_depressant_dose_index)=B |
| morning_HRV_rMSSD, room_acoustic_reverberation_gain | morning_HRV_rMSSD o-o room_acoustic_reverberation_gain | morning_HRV_rMSSD   room_acoustic_reverberation_gain (no edge) | morning_HRV_rMSSD   room_acoustic_reverberation_gain (no edge) | morning_HRV_rMSSD   room_acoustic_reverberation_gain (no edge) | morning_HRV_rMSSD   room_acoustic_reverberation_gain (no edge) | morning_HRV_rMSSD -> room_acoustic_reverberation_gain | (morning_HRV_rMSSD, room_acoustic_reverberation_gain)=D |
| patient_acuity_score, nurse_staffing_ratio | patient_acuity_score   nurse_staffing_ratio (no edge) | patient_acuity_score   nurse_staffing_ratio (no edge) | patient_acuity_score->nurse_staffing_ratio | patient_acuity_score->nurse_staffing_ratio | patient_acuity_score->nurse_staffing_ratio | no edge | (patient_acuity_score, nurse_staffing_ratio)=A |
| patient_acuity_score, planned_nursing_minutes | patient_acuity_score   planned_nursing_minutes (no edge) | patient_acuity_score   planned_nursing_minutes (no edge) | patient_acuity_score->planned_nursing_minutes | patient_acuity_score->planned_nursing_minutes | patient_acuity_score->planned_nursing_minutes | no edge | (patient_acuity_score, planned_nursing_minutes)=A |
| patient_acuity_score, alarm_related_LAeq | alarm_related_LAeq o-> patient_acuity_score | patient_acuity_score   alarm_related_LAeq (no edge) | patient_acuity_score   alarm_related_LAeq (no edge) | patient_acuity_score   alarm_related_LAeq (no edge) | patient_acuity_score   alarm_related_LAeq (no edge) | alarm_related_LAeq -> patient_acuity_score | (patient_acuity_score, alarm_related_LAeq)=D |
| nurse_staffing_ratio, planned_nursing_minutes | nurse_staffing_ratio   planned_nursing_minutes (no edge) | nurse_staffing_ratio   planned_nursing_minutes (no edge) | nurse_staffing_ratio->planned_nursing_minutes | nurse_staffing_ratio->planned_nursing_minutes | nurse_staffing_ratio->planned_nursing_minutes | no edge | (nurse_staffing_ratio, planned_nursing_minutes)=A |
| actigraphy_wear_fraction, cns_depressant_dose_index | actigraphy_wear_fraction o-o cns_depressant_dose_index | actigraphy_wear_fraction   cns_depressant_dose_index (no edge) | actigraphy_wear_fraction   cns_depressant_dose_index (no edge) | actigraphy_wear_fraction   cns_depressant_dose_index (no edge) | actigraphy_wear_fraction   cns_depressant_dose_index (no edge) | actigraphy_wear_fraction -> cns_depressant_dose_index | (actigraphy_wear_fraction, cns_depressant_dose_index)=D |
| arousal_threshold_index, perceived_lux_dose | arousal_threshold_index o-o perceived_lux_dose | arousal_threshold_index   perceived_lux_dose (no edge) | arousal_threshold_index   perceived_lux_dose (no edge) | arousal_threshold_index   perceived_lux_dose (no edge) | arousal_threshold_index   perceived_lux_dose (no edge) | perceived_lux_dose -> arousal_threshold_index | (arousal_threshold_index, perceived_lux_dose)=D |
| comfort_kit_adherence_index, comfort_bundle_offered | comfort_kit_adherence_index   comfort_bundle_offered (no edge) | comfort_kit_adherence_index   comfort_bundle_offered (no edge) | comfort_kit_adherence_index->comfort_bundle_offered | comfort_kit_adherence_index->comfort_bundle_offered | comfort_kit_adherence_index->comfort_bundle_offered | no edge | (comfort_kit_adherence_index, comfort_bundle_offered)=A |
| comfort_kit_adherence_index, planned_nursing_minutes | comfort_kit_adherence_index <-> planned_nursing_minutes | comfort_kit_adherence_index   planned_nursing_minutes (no edge) | comfort_kit_adherence_index   planned_nursing_minutes (no edge) | comfort_kit_adherence_index   planned_nursing_minutes (no edge) | comfort_kit_adherence_index   planned_nursing_minutes (no edge) | planned_nursing_minutes -> comfort_kit_adherence_index | (comfort_kit_adherence_index, planned_nursing_minutes)=D |
| comfort_kit_adherence_index, morning_pain_score | comfort_kit_adherence_index <-> morning_pain_score | comfort_kit_adherence_index   morning_pain_score (no edge) | comfort_kit_adherence_index   morning_pain_score (no edge) | comfort_kit_adherence_index   morning_pain_score (no edge) | comfort_kit_adherence_index   morning_pain_score (no edge) | comfort_kit_adherence_index -> morning_pain_score | (comfort_kit_adherence_index, morning_pain_score)=D |
| comfort_bundle_offered, roommate_Lmax_spikes_count | comfort_bundle_offered o-> roommate_Lmax_spikes_count | comfort_bundle_offered   roommate_Lmax_spikes_count (no edge) | comfort_bundle_offered   roommate_Lmax_spikes_count (no edge) | comfort_bundle_offered   roommate_Lmax_spikes_count (no edge) | comfort_bundle_offered   roommate_Lmax_spikes_count (no edge) | no edge | (comfort_bundle_offered, roommate_Lmax_spikes_count)=C |
| perceived_lux_dose, night_lux_summary | perceived_lux_dose   night_lux_summary (no edge) | perceived_lux_dose   night_lux_summary (no edge) | perceived_lux_dose->night_lux_summary | perceived_lux_dose->night_lux_summary | perceived_lux_dose->night_lux_summary | no edge | (perceived_lux_dose, night_lux_summary)=A |
| roommate_Lmax_spikes_count, perceived_noise_dose | roommate_Lmax_spikes_count   perceived_noise_dose (no edge) | roommate_Lmax_spikes_count   perceived_noise_dose (no edge) | roommate_Lmax_spikes_count->perceived_noise_dose | roommate_Lmax_spikes_count->perceived_noise_dose | roommate_Lmax_spikes_count->perceived_noise_dose | no edge | (roommate_Lmax_spikes_count, perceived_noise_dose)=A |
| roommate_Lmax_spikes_count, sleep_fragmentation_index | roommate_Lmax_spikes_count   sleep_fragmentation_index (no edge) | roommate_Lmax_spikes_count   sleep_fragmentation_index (no edge) | roommate_Lmax_spikes_count->sleep_fragmentation_index | roommate_Lmax_spikes_count->sleep_fragmentation_index | roommate_Lmax_spikes_count->sleep_fragmentation_index | no edge | (roommate_Lmax_spikes_count, sleep_fragmentation_index)=A |
| roommate_Lmax_spikes_count, alarm_related_LAeq | alarm_related_LAeq o-> roommate_Lmax_spikes_count | alarm_related_LAeq o-> roommate_Lmax_spikes_count | roommate_Lmax_spikes_count   alarm_related_LAeq (no edge) | roommate_Lmax_spikes_count   alarm_related_LAeq (no edge) | roommate_Lmax_spikes_count   alarm_related_LAeq (no edge) | alarm_related_LAeq -> roommate_Lmax_spikes_count | (roommate_Lmax_spikes_count, alarm_related_LAeq)=C |
| transfer_time_seconds, nightly_alarm_count | transfer_time_seconds o-> nightly_alarm_count | transfer_time_seconds   nightly_alarm_count (no edge) | transfer_time_seconds   nightly_alarm_count (no edge) | transfer_time_seconds   nightly_alarm_count (no edge) | transfer_time_seconds   nightly_alarm_count (no edge) | transfer_time_seconds -> nightly_alarm_count | (transfer_time_seconds, nightly_alarm_count)=C |
| cns_depressant_dose_index, sleep_fragmentation_index | cns_depressant_dose_index   sleep_fragmentation_index (no edge) | cns_depressant_dose_index   sleep_fragmentation_index (no edge) | cns_depressant_dose_index->sleep_fragmentation_index | cns_depressant_dose_index->sleep_fragmentation_index | cns_depressant_dose_index->sleep_fragmentation_index | no edge | (cns_depressant_dose_index, sleep_fragmentation_index)=A |
| room_acoustic_reverberation_gain, sleep_fragmentation_index | room_acoustic_reverberation_gain   sleep_fragmentation_index (no edge) | room_acoustic_reverberation_gain   sleep_fragmentation_index (no edge) | room_acoustic_reverberation_gain->sleep_fragmentation_index | room_acoustic_reverberation_gain->sleep_fragmentation_index | room_acoustic_reverberation_gain->sleep_fragmentation_index | no edge | (room_acoustic_reverberation_gain, sleep_fragmentation_index)=A |
| room_acoustic_reverberation_gain, alarm_related_LAeq | room_acoustic_reverberation_gain   alarm_related_LAeq (no edge) | room_acoustic_reverberation_gain   alarm_related_LAeq (no edge) | room_acoustic_reverberation_gain->alarm_related_LAeq | room_acoustic_reverberation_gain->alarm_related_LAeq | room_acoustic_reverberation_gain->alarm_related_LAeq | no edge | (room_acoustic_reverberation_gain, alarm_related_LAeq)=A |
| nightly_alarm_count, perceived_noise_dose | nightly_alarm_count   perceived_noise_dose (no edge) | nightly_alarm_count   perceived_noise_dose (no edge) | nightly_alarm_count->perceived_noise_dose | nightly_alarm_count->perceived_noise_dose | nightly_alarm_count->perceived_noise_dose | no edge | (nightly_alarm_count, perceived_noise_dose)=A |
| nightly_alarm_count, sleep_fragmentation_index | sleep_fragmentation_index->nightly_alarm_count | sleep_fragmentation_index->nightly_alarm_count | nightly_alarm_count->sleep_fragmentation_index | nightly_alarm_count->sleep_fragmentation_index | nightly_alarm_count->sleep_fragmentation_index | sleep_fragmentation_index -> nightly_alarm_count | (nightly_alarm_count, sleep_fragmentation_index)=A |
| nightly_alarm_count, alarm_quieting_bundle_state | nightly_alarm_count   alarm_quieting_bundle_state (no edge) | nightly_alarm_count   alarm_quieting_bundle_state (no edge) | alarm_quieting_bundle_state->nightly_alarm_count | nightly_alarm_count   alarm_quieting_bundle_state (no edge) | nightly_alarm_count   alarm_quieting_bundle_state (no edge) | no edge | (nightly_alarm_count, alarm_quieting_bundle_state)=B |
| nightly_alarm_count, alarm_related_LAeq | nightly_alarm_count   alarm_related_LAeq (no edge) | nightly_alarm_count   alarm_related_LAeq (no edge) | nightly_alarm_count->alarm_related_LAeq | nightly_alarm_count->alarm_related_LAeq | nightly_alarm_count->alarm_related_LAeq | no edge | (nightly_alarm_count, alarm_related_LAeq)=A |
| baseline_evening_pain_score, perceived_noise_dose | baseline_evening_pain_score <-> perceived_noise_dose | baseline_evening_pain_score   perceived_noise_dose (no edge) | baseline_evening_pain_score   perceived_noise_dose (no edge) | baseline_evening_pain_score   perceived_noise_dose (no edge) | baseline_evening_pain_score   perceived_noise_dose (no edge) | baseline_evening_pain_score -> perceived_noise_dose | (baseline_evening_pain_score, perceived_noise_dose)=C |
| baseline_evening_pain_score, night_lux_summary | baseline_evening_pain_score <-> night_lux_summary | baseline_evening_pain_score   night_lux_summary (no edge) | baseline_evening_pain_score   night_lux_summary (no edge) | baseline_evening_pain_score   night_lux_summary (no edge) | baseline_evening_pain_score   night_lux_summary (no edge) | night_lux_summary -> baseline_evening_pain_score | (baseline_evening_pain_score, night_lux_summary)=C |
| baseline_evening_pain_score, morning_pain_score | baseline_evening_pain_score   morning_pain_score (no edge) | baseline_evening_pain_score   morning_pain_score (no edge) | baseline_evening_pain_score->morning_pain_score | baseline_evening_pain_score->morning_pain_score | baseline_evening_pain_score->morning_pain_score | no edge | (baseline_evening_pain_score, morning_pain_score)=A |
| perceived_noise_dose, sleep_fragmentation_index | perceived_noise_dose   sleep_fragmentation_index (no edge) | perceived_noise_dose   sleep_fragmentation_index (no edge) | perceived_noise_dose->sleep_fragmentation_index | perceived_noise_dose->sleep_fragmentation_index | perceived_noise_dose->sleep_fragmentation_index | no edge | (perceived_noise_dose, sleep_fragmentation_index)=A |
| perceived_noise_dose, alarm_related_LAeq | perceived_noise_dose   alarm_related_LAeq (no edge) | perceived_noise_dose   alarm_related_LAeq (no edge) | perceived_noise_dose->alarm_related_LAeq | perceived_noise_dose->alarm_related_LAeq | perceived_noise_dose->alarm_related_LAeq | no edge | (perceived_noise_dose, alarm_related_LAeq)=A |
| night_lux_summary, sleep_fragmentation_index | night_lux_summary <-> sleep_fragmentation_index | night_lux_summary   sleep_fragmentation_index (no edge) | night_lux_summary->sleep_fragmentation_index | night_lux_summary->sleep_fragmentation_index | night_lux_summary->sleep_fragmentation_index | no edge | (night_lux_summary, sleep_fragmentation_index)=A |
| alarm_quieting_bundle_state, alarm_related_LAeq | alarm_quieting_bundle_state   alarm_related_LAeq (no edge) | alarm_quieting_bundle_state   alarm_related_LAeq (no edge) | alarm_quieting_bundle_state->alarm_related_LAeq | alarm_quieting_bundle_state->alarm_related_LAeq | alarm_quieting_bundle_state->alarm_related_LAeq | alarm_quieting_bundle_state -> alarm_related_LAeq | (alarm_quieting_bundle_state, alarm_related_LAeq)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
