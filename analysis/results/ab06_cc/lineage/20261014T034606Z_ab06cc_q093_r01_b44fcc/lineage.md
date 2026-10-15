# Edge lineage: 20261014T034606Z_ab06cc_q093_r01_b44fcc

Dataset `/research/datasets/suite_q1s2/q093/q093.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 25 | 0.84 | 0.60 | 0.70 | 8 | 1 | 12 | 31 |
| S1 after bootstrap edits | 15 | 0.87 | 0.37 | 0.52 | 8 | 1 | 4 | 29 |
| S2 after LLM review | 46 | 0.22 | 0.29 | 0.25 | 5 | 5 | 0 | 66 |
| S3 after KCI pruning | 45 | 0.20 | 0.26 | 0.23 | 5 | 4 | 0 | 66 |
| S4 final (after cycle step) | 45 | 0.20 | 0.26 | 0.23 | 5 | 4 | 0 | 66 |

Scored against: reference graph s2_09_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 10. Of the deleted, 4 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 45, "B": 1, "C": 183, "D": 2}.
- LLM effect: added 37 (of which 36 where the resamples showed no edge at frequency >= 0.9), removed 6, re-oriented 3.
- KCI step removed 1. Cycle step changed 0.
- Final graph: 45 edges; set by {"llm": 39, "algorithm (unchanged)": 6}; 6 identical to the algorithm's output; 35 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| morning_HRV_rMSSD->arousal_threshold_index | llm | no | 1.00 |
| morning_HRV_rMSSD->cns_depressant_dose_index | algorithm (unchanged) | yes | 0.60 |
| morning_HRV_rMSSD->baseline_evening_pain_score | algorithm (unchanged) | yes | 0.00 |
| morning_HRV_rMSSD->sleep_fragmentation_index | llm | no | 1.00 |
| morning_HRV_rMSSD->morning_pain_score | llm | no | 1.00 |
| patient_acuity_score->nurse_staffing_ratio | llm | no | 1.00 |
| patient_acuity_score->arousal_threshold_index | llm | no | 1.00 |
| patient_acuity_score->planned_nursing_minutes | llm | no | 1.00 |
| patient_acuity_score->cns_depressant_dose_index | llm | no | 1.00 |
| patient_acuity_score->vital_sign_schedule_frequency | llm | no | 1.00 |
| patient_acuity_score->nightly_alarm_count | llm | no | 1.00 |
| patient_acuity_score->baseline_evening_pain_score | llm | no | 1.00 |
| patient_acuity_score->sleep_fragmentation_index | llm | no | 1.00 |
| patient_acuity_score->morning_pain_score | llm | yes | 0.20 |
| nurse_staffing_ratio->planned_nursing_minutes | llm | no | 0.95 |
| arousal_threshold_index->nightly_alarm_count | algorithm (unchanged) | yes | 0.00 |
| arousal_threshold_index->sleep_fragmentation_index | llm | no | 1.00 |
| comfort_kit_adherence_index->comfort_bundle_offered | llm | no | 1.00 |
| comfort_kit_adherence_index->alarm_quieting_bundle_state | algorithm (unchanged) | yes | 0.00 |
| comfort_bundle_offered->alarm_quieting_bundle_state | llm | no | 1.00 |
| roommate_Lmax_spikes_count->nightly_alarm_count | llm | no | 1.00 |
| roommate_Lmax_spikes_count->perceived_noise_dose | llm | no | 1.00 |
| roommate_Lmax_spikes_count->sleep_fragmentation_index | llm | no | 0.90 |
| roommate_Lmax_spikes_count->alarm_related_LAeq | llm | yes | 0.00 |
| planned_nursing_minutes->vital_sign_schedule_frequency | llm | no | 1.00 |
| planned_nursing_minutes->baseline_evening_pain_score | llm | no | 1.00 |
| planned_nursing_minutes->sleep_fragmentation_index | llm | no | 1.00 |
| planned_nursing_minutes->morning_pain_score | llm | no | 1.00 |
| cns_depressant_dose_index->sleep_fragmentation_index | llm | no | 1.00 |
| room_acoustic_reverberation_gain->nightly_alarm_count | llm | no | 1.00 |
| room_acoustic_reverberation_gain->perceived_noise_dose | algorithm (unchanged) | yes | 0.00 |
| room_acoustic_reverberation_gain->sleep_fragmentation_index | llm | no | 1.00 |
| room_acoustic_reverberation_gain->alarm_related_LAeq | llm | no | 1.00 |
| nightly_alarm_count->perceived_noise_dose | llm | no | 1.00 |
| nightly_alarm_count->sleep_fragmentation_index | llm | yes | 0.05 |
| nightly_alarm_count->alarm_related_LAeq | llm | no | 1.00 |
| baseline_evening_pain_score->sleep_fragmentation_index | algorithm (unchanged) | yes | 0.05 |
| baseline_evening_pain_score->morning_pain_score | llm | no | 1.00 |
| perceived_noise_dose->sleep_fragmentation_index | llm | no | 1.00 |
| perceived_noise_dose->morning_pain_score | llm | no | 1.00 |
| perceived_noise_dose->alarm_related_LAeq | llm | no | 1.00 |
| night_lux_summary->sleep_fragmentation_index | llm | yes | 0.50 |
| sleep_fragmentation_index->morning_pain_score | llm | no | 1.00 |
| sleep_fragmentation_index->alarm_related_LAeq | llm | no | 1.00 |
| alarm_quieting_bundle_state->morning_pain_score | llm | no | 0.95 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| morning_HRV_rMSSD, arousal_threshold_index | morning_HRV_rMSSD   arousal_threshold_index (no edge) | morning_HRV_rMSSD   arousal_threshold_index (no edge) | morning_HRV_rMSSD->arousal_threshold_index | morning_HRV_rMSSD->arousal_threshold_index | morning_HRV_rMSSD->arousal_threshold_index | no edge | (morning_HRV_rMSSD, arousal_threshold_index)=A |
| morning_HRV_rMSSD, planned_nursing_minutes | morning_HRV_rMSSD->planned_nursing_minutes | morning_HRV_rMSSD->planned_nursing_minutes | morning_HRV_rMSSD   planned_nursing_minutes (no edge) | morning_HRV_rMSSD   planned_nursing_minutes (no edge) | morning_HRV_rMSSD   planned_nursing_minutes (no edge) | morning_HRV_rMSSD -> planned_nursing_minutes | (morning_HRV_rMSSD, planned_nursing_minutes)=C |
| morning_HRV_rMSSD, room_acoustic_reverberation_gain | morning_HRV_rMSSD o-o room_acoustic_reverberation_gain | morning_HRV_rMSSD   room_acoustic_reverberation_gain (no edge) | morning_HRV_rMSSD   room_acoustic_reverberation_gain (no edge) | morning_HRV_rMSSD   room_acoustic_reverberation_gain (no edge) | morning_HRV_rMSSD   room_acoustic_reverberation_gain (no edge) | morning_HRV_rMSSD -> room_acoustic_reverberation_gain | (morning_HRV_rMSSD, room_acoustic_reverberation_gain)=C |
| morning_HRV_rMSSD, sleep_fragmentation_index | morning_HRV_rMSSD   sleep_fragmentation_index (no edge) | morning_HRV_rMSSD   sleep_fragmentation_index (no edge) | morning_HRV_rMSSD->sleep_fragmentation_index | morning_HRV_rMSSD->sleep_fragmentation_index | morning_HRV_rMSSD->sleep_fragmentation_index | no edge | (morning_HRV_rMSSD, sleep_fragmentation_index)=A |
| morning_HRV_rMSSD, morning_pain_score | morning_HRV_rMSSD   morning_pain_score (no edge) | morning_HRV_rMSSD   morning_pain_score (no edge) | morning_HRV_rMSSD->morning_pain_score | morning_HRV_rMSSD->morning_pain_score | morning_HRV_rMSSD->morning_pain_score | no edge | (morning_HRV_rMSSD, morning_pain_score)=A |
| patient_acuity_score, nurse_staffing_ratio | patient_acuity_score   nurse_staffing_ratio (no edge) | patient_acuity_score   nurse_staffing_ratio (no edge) | patient_acuity_score->nurse_staffing_ratio | patient_acuity_score->nurse_staffing_ratio | patient_acuity_score->nurse_staffing_ratio | no edge | (patient_acuity_score, nurse_staffing_ratio)=A |
| patient_acuity_score, arousal_threshold_index | patient_acuity_score   arousal_threshold_index (no edge) | patient_acuity_score   arousal_threshold_index (no edge) | patient_acuity_score->arousal_threshold_index | patient_acuity_score->arousal_threshold_index | patient_acuity_score->arousal_threshold_index | no edge | (patient_acuity_score, arousal_threshold_index)=A |
| patient_acuity_score, planned_nursing_minutes | patient_acuity_score   planned_nursing_minutes (no edge) | patient_acuity_score   planned_nursing_minutes (no edge) | patient_acuity_score->planned_nursing_minutes | patient_acuity_score->planned_nursing_minutes | patient_acuity_score->planned_nursing_minutes | no edge | (patient_acuity_score, planned_nursing_minutes)=A |
| patient_acuity_score, cns_depressant_dose_index | patient_acuity_score   cns_depressant_dose_index (no edge) | patient_acuity_score   cns_depressant_dose_index (no edge) | patient_acuity_score->cns_depressant_dose_index | patient_acuity_score->cns_depressant_dose_index | patient_acuity_score->cns_depressant_dose_index | no edge | (patient_acuity_score, cns_depressant_dose_index)=A |
| patient_acuity_score, vital_sign_schedule_frequency | patient_acuity_score   vital_sign_schedule_frequency (no edge) | patient_acuity_score   vital_sign_schedule_frequency (no edge) | patient_acuity_score->vital_sign_schedule_frequency | patient_acuity_score->vital_sign_schedule_frequency | patient_acuity_score->vital_sign_schedule_frequency | no edge | (patient_acuity_score, vital_sign_schedule_frequency)=A |
| patient_acuity_score, nightly_alarm_count | patient_acuity_score   nightly_alarm_count (no edge) | patient_acuity_score   nightly_alarm_count (no edge) | patient_acuity_score->nightly_alarm_count | patient_acuity_score->nightly_alarm_count | patient_acuity_score->nightly_alarm_count | no edge | (patient_acuity_score, nightly_alarm_count)=A |
| patient_acuity_score, baseline_evening_pain_score | patient_acuity_score   baseline_evening_pain_score (no edge) | patient_acuity_score   baseline_evening_pain_score (no edge) | patient_acuity_score->baseline_evening_pain_score | patient_acuity_score->baseline_evening_pain_score | patient_acuity_score->baseline_evening_pain_score | no edge | (patient_acuity_score, baseline_evening_pain_score)=A |
| patient_acuity_score, sleep_fragmentation_index | patient_acuity_score   sleep_fragmentation_index (no edge) | patient_acuity_score   sleep_fragmentation_index (no edge) | patient_acuity_score->sleep_fragmentation_index | patient_acuity_score->sleep_fragmentation_index | patient_acuity_score->sleep_fragmentation_index | no edge | (patient_acuity_score, sleep_fragmentation_index)=A |
| patient_acuity_score, morning_pain_score | patient_acuity_score <-> morning_pain_score | patient_acuity_score <-> morning_pain_score | patient_acuity_score->morning_pain_score | patient_acuity_score->morning_pain_score | patient_acuity_score->morning_pain_score | morning_pain_score -> patient_acuity_score | (patient_acuity_score, morning_pain_score)=A |
| patient_acuity_score, alarm_related_LAeq | alarm_related_LAeq o-> patient_acuity_score | patient_acuity_score   alarm_related_LAeq (no edge) | patient_acuity_score   alarm_related_LAeq (no edge) | patient_acuity_score   alarm_related_LAeq (no edge) | patient_acuity_score   alarm_related_LAeq (no edge) | alarm_related_LAeq -> patient_acuity_score | (patient_acuity_score, alarm_related_LAeq)=C |
| nurse_staffing_ratio, planned_nursing_minutes | nurse_staffing_ratio   planned_nursing_minutes (no edge) | nurse_staffing_ratio   planned_nursing_minutes (no edge) | nurse_staffing_ratio->planned_nursing_minutes | nurse_staffing_ratio->planned_nursing_minutes | nurse_staffing_ratio->planned_nursing_minutes | no edge | (nurse_staffing_ratio, planned_nursing_minutes)=A |
| nurse_staffing_ratio, perceived_noise_dose | perceived_noise_dose->nurse_staffing_ratio | perceived_noise_dose->nurse_staffing_ratio | nurse_staffing_ratio   perceived_noise_dose (no edge) | nurse_staffing_ratio   perceived_noise_dose (no edge) | nurse_staffing_ratio   perceived_noise_dose (no edge) | no edge | (nurse_staffing_ratio, perceived_noise_dose)=C |
| actigraphy_wear_fraction, cns_depressant_dose_index | actigraphy_wear_fraction o-> cns_depressant_dose_index | actigraphy_wear_fraction   cns_depressant_dose_index (no edge) | actigraphy_wear_fraction   cns_depressant_dose_index (no edge) | actigraphy_wear_fraction   cns_depressant_dose_index (no edge) | actigraphy_wear_fraction   cns_depressant_dose_index (no edge) | actigraphy_wear_fraction -> cns_depressant_dose_index | (actigraphy_wear_fraction, cns_depressant_dose_index)=C |
| actigraphy_wear_fraction, perceived_noise_dose | actigraphy_wear_fraction o-> perceived_noise_dose | actigraphy_wear_fraction o-> perceived_noise_dose | actigraphy_wear_fraction   perceived_noise_dose (no edge) | actigraphy_wear_fraction   perceived_noise_dose (no edge) | actigraphy_wear_fraction   perceived_noise_dose (no edge) | no edge | (actigraphy_wear_fraction, perceived_noise_dose)=C |
| arousal_threshold_index, perceived_lux_dose | arousal_threshold_index o-o perceived_lux_dose | arousal_threshold_index   perceived_lux_dose (no edge) | arousal_threshold_index   perceived_lux_dose (no edge) | arousal_threshold_index   perceived_lux_dose (no edge) | arousal_threshold_index   perceived_lux_dose (no edge) | perceived_lux_dose -> arousal_threshold_index | (arousal_threshold_index, perceived_lux_dose)=C |
| arousal_threshold_index, sleep_fragmentation_index | arousal_threshold_index   sleep_fragmentation_index (no edge) | arousal_threshold_index   sleep_fragmentation_index (no edge) | arousal_threshold_index->sleep_fragmentation_index | arousal_threshold_index->sleep_fragmentation_index | arousal_threshold_index->sleep_fragmentation_index | no edge | (arousal_threshold_index, sleep_fragmentation_index)=A |
| comfort_kit_adherence_index, comfort_bundle_offered | comfort_kit_adherence_index   comfort_bundle_offered (no edge) | comfort_kit_adherence_index   comfort_bundle_offered (no edge) | comfort_kit_adherence_index->comfort_bundle_offered | comfort_kit_adherence_index->comfort_bundle_offered | comfort_kit_adherence_index->comfort_bundle_offered | no edge | (comfort_kit_adherence_index, comfort_bundle_offered)=A |
| comfort_kit_adherence_index, planned_nursing_minutes | comfort_kit_adherence_index <-> planned_nursing_minutes | comfort_kit_adherence_index   planned_nursing_minutes (no edge) | comfort_kit_adherence_index   planned_nursing_minutes (no edge) | comfort_kit_adherence_index   planned_nursing_minutes (no edge) | comfort_kit_adherence_index   planned_nursing_minutes (no edge) | planned_nursing_minutes -> comfort_kit_adherence_index | (comfort_kit_adherence_index, planned_nursing_minutes)=C |
| comfort_kit_adherence_index, morning_pain_score | comfort_kit_adherence_index <-> morning_pain_score | comfort_kit_adherence_index   morning_pain_score (no edge) | comfort_kit_adherence_index   morning_pain_score (no edge) | comfort_kit_adherence_index   morning_pain_score (no edge) | comfort_kit_adherence_index   morning_pain_score (no edge) | comfort_kit_adherence_index -> morning_pain_score | (comfort_kit_adherence_index, morning_pain_score)=C |
| comfort_bundle_offered, alarm_quieting_bundle_state | comfort_bundle_offered   alarm_quieting_bundle_state (no edge) | comfort_bundle_offered   alarm_quieting_bundle_state (no edge) | comfort_bundle_offered->alarm_quieting_bundle_state | comfort_bundle_offered->alarm_quieting_bundle_state | comfort_bundle_offered->alarm_quieting_bundle_state | no edge | (comfort_bundle_offered, alarm_quieting_bundle_state)=A |
| roommate_Lmax_spikes_count, nightly_alarm_count | roommate_Lmax_spikes_count   nightly_alarm_count (no edge) | roommate_Lmax_spikes_count   nightly_alarm_count (no edge) | roommate_Lmax_spikes_count->nightly_alarm_count | roommate_Lmax_spikes_count->nightly_alarm_count | roommate_Lmax_spikes_count->nightly_alarm_count | no edge | (roommate_Lmax_spikes_count, nightly_alarm_count)=A |
| roommate_Lmax_spikes_count, perceived_noise_dose | roommate_Lmax_spikes_count   perceived_noise_dose (no edge) | roommate_Lmax_spikes_count   perceived_noise_dose (no edge) | roommate_Lmax_spikes_count->perceived_noise_dose | roommate_Lmax_spikes_count->perceived_noise_dose | roommate_Lmax_spikes_count->perceived_noise_dose | no edge | (roommate_Lmax_spikes_count, perceived_noise_dose)=A |
| roommate_Lmax_spikes_count, sleep_fragmentation_index | roommate_Lmax_spikes_count   sleep_fragmentation_index (no edge) | roommate_Lmax_spikes_count   sleep_fragmentation_index (no edge) | roommate_Lmax_spikes_count->sleep_fragmentation_index | roommate_Lmax_spikes_count->sleep_fragmentation_index | roommate_Lmax_spikes_count->sleep_fragmentation_index | no edge | (roommate_Lmax_spikes_count, sleep_fragmentation_index)=A |
| roommate_Lmax_spikes_count, morning_pain_score | morning_pain_score->roommate_Lmax_spikes_count | morning_pain_score->roommate_Lmax_spikes_count | roommate_Lmax_spikes_count   morning_pain_score (no edge) | roommate_Lmax_spikes_count   morning_pain_score (no edge) | roommate_Lmax_spikes_count   morning_pain_score (no edge) | morning_pain_score -> roommate_Lmax_spikes_count | (roommate_Lmax_spikes_count, morning_pain_score)=C |
| roommate_Lmax_spikes_count, alarm_related_LAeq | alarm_related_LAeq o-> roommate_Lmax_spikes_count | alarm_related_LAeq o-> roommate_Lmax_spikes_count | roommate_Lmax_spikes_count->alarm_related_LAeq | roommate_Lmax_spikes_count->alarm_related_LAeq | roommate_Lmax_spikes_count->alarm_related_LAeq | alarm_related_LAeq -> roommate_Lmax_spikes_count | (roommate_Lmax_spikes_count, alarm_related_LAeq)=A |
| transfer_time_seconds, nightly_alarm_count | transfer_time_seconds o-> nightly_alarm_count | transfer_time_seconds   nightly_alarm_count (no edge) | transfer_time_seconds   nightly_alarm_count (no edge) | transfer_time_seconds   nightly_alarm_count (no edge) | transfer_time_seconds   nightly_alarm_count (no edge) | transfer_time_seconds -> nightly_alarm_count | (transfer_time_seconds, nightly_alarm_count)=C |
| transfer_time_seconds, morning_pain_score | transfer_time_seconds o-> morning_pain_score | transfer_time_seconds   morning_pain_score (no edge) | transfer_time_seconds   morning_pain_score (no edge) | transfer_time_seconds   morning_pain_score (no edge) | transfer_time_seconds   morning_pain_score (no edge) | no edge | (transfer_time_seconds, morning_pain_score)=C |
| planned_nursing_minutes, vital_sign_schedule_frequency | planned_nursing_minutes   vital_sign_schedule_frequency (no edge) | planned_nursing_minutes   vital_sign_schedule_frequency (no edge) | planned_nursing_minutes->vital_sign_schedule_frequency | planned_nursing_minutes->vital_sign_schedule_frequency | planned_nursing_minutes->vital_sign_schedule_frequency | no edge | (planned_nursing_minutes, vital_sign_schedule_frequency)=A |
| planned_nursing_minutes, baseline_evening_pain_score | planned_nursing_minutes   baseline_evening_pain_score (no edge) | planned_nursing_minutes   baseline_evening_pain_score (no edge) | planned_nursing_minutes->baseline_evening_pain_score | planned_nursing_minutes->baseline_evening_pain_score | planned_nursing_minutes->baseline_evening_pain_score | no edge | (planned_nursing_minutes, baseline_evening_pain_score)=A |
| planned_nursing_minutes, sleep_fragmentation_index | planned_nursing_minutes   sleep_fragmentation_index (no edge) | planned_nursing_minutes   sleep_fragmentation_index (no edge) | planned_nursing_minutes->sleep_fragmentation_index | planned_nursing_minutes->sleep_fragmentation_index | planned_nursing_minutes->sleep_fragmentation_index | no edge | (planned_nursing_minutes, sleep_fragmentation_index)=A |
| planned_nursing_minutes, alarm_quieting_bundle_state | planned_nursing_minutes <-> alarm_quieting_bundle_state | planned_nursing_minutes <-> alarm_quieting_bundle_state | planned_nursing_minutes   alarm_quieting_bundle_state (no edge) | planned_nursing_minutes   alarm_quieting_bundle_state (no edge) | planned_nursing_minutes   alarm_quieting_bundle_state (no edge) | alarm_quieting_bundle_state -> planned_nursing_minutes | (planned_nursing_minutes, alarm_quieting_bundle_state)=C |
| planned_nursing_minutes, morning_pain_score | planned_nursing_minutes   morning_pain_score (no edge) | planned_nursing_minutes   morning_pain_score (no edge) | planned_nursing_minutes->morning_pain_score | planned_nursing_minutes->morning_pain_score | planned_nursing_minutes->morning_pain_score | no edge | (planned_nursing_minutes, morning_pain_score)=A |
| cns_depressant_dose_index, sleep_fragmentation_index | cns_depressant_dose_index   sleep_fragmentation_index (no edge) | cns_depressant_dose_index   sleep_fragmentation_index (no edge) | cns_depressant_dose_index->sleep_fragmentation_index | cns_depressant_dose_index->sleep_fragmentation_index | cns_depressant_dose_index->sleep_fragmentation_index | no edge | (cns_depressant_dose_index, sleep_fragmentation_index)=A |
| room_acoustic_reverberation_gain, nightly_alarm_count | room_acoustic_reverberation_gain   nightly_alarm_count (no edge) | room_acoustic_reverberation_gain   nightly_alarm_count (no edge) | room_acoustic_reverberation_gain->nightly_alarm_count | room_acoustic_reverberation_gain->nightly_alarm_count | room_acoustic_reverberation_gain->nightly_alarm_count | no edge | (room_acoustic_reverberation_gain, nightly_alarm_count)=A |
| room_acoustic_reverberation_gain, sleep_fragmentation_index | room_acoustic_reverberation_gain   sleep_fragmentation_index (no edge) | room_acoustic_reverberation_gain   sleep_fragmentation_index (no edge) | room_acoustic_reverberation_gain->sleep_fragmentation_index | room_acoustic_reverberation_gain->sleep_fragmentation_index | room_acoustic_reverberation_gain->sleep_fragmentation_index | no edge | (room_acoustic_reverberation_gain, sleep_fragmentation_index)=A |
| room_acoustic_reverberation_gain, alarm_related_LAeq | room_acoustic_reverberation_gain   alarm_related_LAeq (no edge) | room_acoustic_reverberation_gain   alarm_related_LAeq (no edge) | room_acoustic_reverberation_gain->alarm_related_LAeq | room_acoustic_reverberation_gain->alarm_related_LAeq | room_acoustic_reverberation_gain->alarm_related_LAeq | no edge | (room_acoustic_reverberation_gain, alarm_related_LAeq)=A |
| vital_sign_schedule_frequency, sleep_fragmentation_index | vital_sign_schedule_frequency o-> sleep_fragmentation_index | vital_sign_schedule_frequency   sleep_fragmentation_index (no edge) | vital_sign_schedule_frequency   sleep_fragmentation_index (no edge) | vital_sign_schedule_frequency   sleep_fragmentation_index (no edge) | vital_sign_schedule_frequency   sleep_fragmentation_index (no edge) | vital_sign_schedule_frequency -> sleep_fragmentation_index | (vital_sign_schedule_frequency, sleep_fragmentation_index)=C |
| nightly_alarm_count, perceived_noise_dose | nightly_alarm_count   perceived_noise_dose (no edge) | nightly_alarm_count   perceived_noise_dose (no edge) | nightly_alarm_count->perceived_noise_dose | nightly_alarm_count->perceived_noise_dose | nightly_alarm_count->perceived_noise_dose | no edge | (nightly_alarm_count, perceived_noise_dose)=A |
| nightly_alarm_count, sleep_fragmentation_index | sleep_fragmentation_index->nightly_alarm_count | sleep_fragmentation_index->nightly_alarm_count | nightly_alarm_count->sleep_fragmentation_index | nightly_alarm_count->sleep_fragmentation_index | nightly_alarm_count->sleep_fragmentation_index | sleep_fragmentation_index -> nightly_alarm_count | (nightly_alarm_count, sleep_fragmentation_index)=A |
| nightly_alarm_count, alarm_related_LAeq | nightly_alarm_count   alarm_related_LAeq (no edge) | nightly_alarm_count   alarm_related_LAeq (no edge) | nightly_alarm_count->alarm_related_LAeq | nightly_alarm_count->alarm_related_LAeq | nightly_alarm_count->alarm_related_LAeq | no edge | (nightly_alarm_count, alarm_related_LAeq)=A |
| baseline_evening_pain_score, night_lux_summary | baseline_evening_pain_score <-> night_lux_summary | baseline_evening_pain_score <-> night_lux_summary | baseline_evening_pain_score   night_lux_summary (no edge) | baseline_evening_pain_score   night_lux_summary (no edge) | baseline_evening_pain_score   night_lux_summary (no edge) | night_lux_summary -> baseline_evening_pain_score | (baseline_evening_pain_score, night_lux_summary)=C |
| baseline_evening_pain_score, morning_pain_score | baseline_evening_pain_score   morning_pain_score (no edge) | baseline_evening_pain_score   morning_pain_score (no edge) | baseline_evening_pain_score->morning_pain_score | baseline_evening_pain_score->morning_pain_score | baseline_evening_pain_score->morning_pain_score | no edge | (baseline_evening_pain_score, morning_pain_score)=A |
| perceived_noise_dose, sleep_fragmentation_index | perceived_noise_dose   sleep_fragmentation_index (no edge) | perceived_noise_dose   sleep_fragmentation_index (no edge) | perceived_noise_dose->sleep_fragmentation_index | perceived_noise_dose->sleep_fragmentation_index | perceived_noise_dose->sleep_fragmentation_index | no edge | (perceived_noise_dose, sleep_fragmentation_index)=A |
| perceived_noise_dose, morning_pain_score | perceived_noise_dose   morning_pain_score (no edge) | perceived_noise_dose   morning_pain_score (no edge) | perceived_noise_dose->morning_pain_score | perceived_noise_dose->morning_pain_score | perceived_noise_dose->morning_pain_score | no edge | (perceived_noise_dose, morning_pain_score)=A |
| perceived_noise_dose, alarm_related_LAeq | perceived_noise_dose   alarm_related_LAeq (no edge) | perceived_noise_dose   alarm_related_LAeq (no edge) | perceived_noise_dose->alarm_related_LAeq | perceived_noise_dose->alarm_related_LAeq | perceived_noise_dose->alarm_related_LAeq | no edge | (perceived_noise_dose, alarm_related_LAeq)=A |
| night_lux_summary, sleep_fragmentation_index | night_lux_summary <-> sleep_fragmentation_index | night_lux_summary   sleep_fragmentation_index (no edge) | night_lux_summary->sleep_fragmentation_index | night_lux_summary->sleep_fragmentation_index | night_lux_summary->sleep_fragmentation_index | no edge | (night_lux_summary, sleep_fragmentation_index)=A |
| sleep_fragmentation_index, morning_pain_score | sleep_fragmentation_index   morning_pain_score (no edge) | sleep_fragmentation_index   morning_pain_score (no edge) | sleep_fragmentation_index->morning_pain_score | sleep_fragmentation_index->morning_pain_score | sleep_fragmentation_index->morning_pain_score | no edge | (sleep_fragmentation_index, morning_pain_score)=A |
| sleep_fragmentation_index, alarm_related_LAeq | sleep_fragmentation_index   alarm_related_LAeq (no edge) | sleep_fragmentation_index   alarm_related_LAeq (no edge) | sleep_fragmentation_index->alarm_related_LAeq | sleep_fragmentation_index->alarm_related_LAeq | sleep_fragmentation_index->alarm_related_LAeq | no edge | (sleep_fragmentation_index, alarm_related_LAeq)=A |
| alarm_quieting_bundle_state, morning_pain_score | alarm_quieting_bundle_state   morning_pain_score (no edge) | alarm_quieting_bundle_state   morning_pain_score (no edge) | alarm_quieting_bundle_state->morning_pain_score | alarm_quieting_bundle_state->morning_pain_score | alarm_quieting_bundle_state->morning_pain_score | no edge | (alarm_quieting_bundle_state, morning_pain_score)=A |
| alarm_quieting_bundle_state, alarm_related_LAeq | alarm_quieting_bundle_state   alarm_related_LAeq (no edge) | alarm_quieting_bundle_state   alarm_related_LAeq (no edge) | alarm_related_LAeq->alarm_quieting_bundle_state | alarm_quieting_bundle_state   alarm_related_LAeq (no edge) | alarm_quieting_bundle_state   alarm_related_LAeq (no edge) | alarm_quieting_bundle_state -> alarm_related_LAeq | (alarm_quieting_bundle_state, alarm_related_LAeq)=B |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
