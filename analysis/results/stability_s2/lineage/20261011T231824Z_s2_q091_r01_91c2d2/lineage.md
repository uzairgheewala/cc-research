# Edge lineage: 20261011T231824Z_s2_q091_r01_91c2d2

Dataset `/research/datasets/suite_q1s2/q091/q091.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 22 | 0.91 | 0.57 | 0.70 | 9 | 0 | 11 | 28 |
| S1 after bootstrap edits | 10 | 0.90 | 0.26 | 0.40 | 8 | 0 | 1 | 28 |
| S2 after LLM review | 36 | 0.58 | 0.60 | 0.59 | 18 | 2 | 1 | 32 |
| S3 after KCI pruning | 35 | 0.60 | 0.60 | 0.60 | 18 | 2 | 1 | 31 |
| S4 final (after cycle step) | 35 | 0.60 | 0.60 | 0.60 | 18 | 2 | 1 | 31 |

Scored against: reference graph s2_09_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 12. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 27, "B": 5, "C": 67, "D": 132}.
- LLM effect: added 27 (of which 16 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 1.
- KCI step removed 1. Cycle step changed 0.
- Final graph: 35 edges; set by {"algorithm (unchanged)": 8, "llm": 27}; 8 identical to the algorithm's output; 20 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| patient_acuity_score->cns_depressant_dose_index | algorithm (unchanged) | yes | 0.00 |
| patient_acuity_score->planned_nursing_minutes | llm | no | 0.40 |
| patient_acuity_score->nightly_alarm_count | algorithm (unchanged) | yes | 0.00 |
| morning_HRV_rMSSD->cns_depressant_dose_index | llm | no | 0.95 |
| morning_HRV_rMSSD->sleep_fragmentation_index | llm | yes | 0.30 |
| nurse_staffing_ratio->planned_nursing_minutes | llm | yes | 0.00 |
| nurse_staffing_ratio->vital_sign_schedule_frequency | llm | no | 1.00 |
| nurse_staffing_ratio->nightly_alarm_count | llm | no | 1.00 |
| comfort_kit_adherence_index->perceived_noise_dose | algorithm (unchanged) | yes | 0.00 |
| arousal_threshold_index->perceived_noise_dose | llm | no | 0.95 |
| arousal_threshold_index->sleep_fragmentation_index | llm | yes | 0.00 |
| perceived_lux_dose->night_lux_summary | llm | no | 0.55 |
| perceived_lux_dose->sleep_fragmentation_index | llm | no | 0.95 |
| sleep_fragmentation_index->transfer_time_seconds | algorithm (unchanged) | yes | 0.00 |
| morning_pain_score o-> transfer_time_seconds | algorithm (unchanged) | yes | 0.00 |
| roommate_Lmax_spikes_count->perceived_noise_dose | llm | yes | 0.15 |
| roommate_Lmax_spikes_count->alarm_related_LAeq | llm | no | 0.95 |
| roommate_Lmax_spikes_count->sleep_fragmentation_index | llm | no | 0.85 |
| cns_depressant_dose_index->sleep_fragmentation_index | llm | no | 1.00 |
| cns_depressant_dose_index->morning_pain_score | llm | no | 1.00 |
| vital_sign_schedule_frequency->night_lux_summary | algorithm (unchanged) | yes | 0.00 |
| room_acoustic_reverberation_gain->perceived_noise_dose | llm | no | 0.75 |
| room_acoustic_reverberation_gain->alarm_related_LAeq | llm | yes | 0.00 |
| nightly_alarm_count->perceived_noise_dose | llm | no | 0.95 |
| alarm_quieting_bundle_state->perceived_noise_dose | llm | no | 1.00 |
| alarm_related_LAeq->perceived_noise_dose | algorithm (unchanged) | yes | 0.00 |
| perceived_noise_dose->sleep_fragmentation_index | llm | no | 0.70 |
| alarm_quieting_bundle_state->nightly_alarm_count | llm | yes | 0.00 |
| nightly_alarm_count->alarm_related_LAeq | algorithm (unchanged) | yes | 0.10 |
| nightly_alarm_count->sleep_fragmentation_index | llm | no | 1.00 |
| night_lux_summary->sleep_fragmentation_index | llm | no | 1.00 |
| alarm_quieting_bundle_state->alarm_related_LAeq | llm | yes | 0.40 |
| alarm_quieting_bundle_state->sleep_fragmentation_index | llm | no | 1.00 |
| alarm_related_LAeq->sleep_fragmentation_index | llm | no | 1.00 |
| baseline_evening_pain_score->morning_pain_score | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| patient_acuity_score, nurse_staffing_ratio | patient_acuity_score   nurse_staffing_ratio (no edge) | patient_acuity_score   nurse_staffing_ratio (no edge) | nurse_staffing_ratio->patient_acuity_score | patient_acuity_score   nurse_staffing_ratio (no edge) | patient_acuity_score   nurse_staffing_ratio (no edge) | no edge | (patient_acuity_score, nurse_staffing_ratio)=B |
| patient_acuity_score, planned_nursing_minutes | patient_acuity_score   planned_nursing_minutes (no edge) | patient_acuity_score   planned_nursing_minutes (no edge) | patient_acuity_score->planned_nursing_minutes | patient_acuity_score->planned_nursing_minutes | patient_acuity_score->planned_nursing_minutes | patient_acuity_score -> planned_nursing_minutes | (patient_acuity_score, planned_nursing_minutes)=A |
| patient_acuity_score, vital_sign_schedule_frequency | patient_acuity_score o-o vital_sign_schedule_frequency | patient_acuity_score   vital_sign_schedule_frequency (no edge) | patient_acuity_score   vital_sign_schedule_frequency (no edge) | patient_acuity_score   vital_sign_schedule_frequency (no edge) | patient_acuity_score   vital_sign_schedule_frequency (no edge) | patient_acuity_score -> vital_sign_schedule_frequency | (patient_acuity_score, vital_sign_schedule_frequency)=D |
| morning_HRV_rMSSD, cns_depressant_dose_index | morning_HRV_rMSSD   cns_depressant_dose_index (no edge) | morning_HRV_rMSSD   cns_depressant_dose_index (no edge) | morning_HRV_rMSSD->cns_depressant_dose_index | morning_HRV_rMSSD->cns_depressant_dose_index | morning_HRV_rMSSD->cns_depressant_dose_index | no edge | (morning_HRV_rMSSD, cns_depressant_dose_index)=A |
| morning_HRV_rMSSD, sleep_fragmentation_index | sleep_fragmentation_index->morning_HRV_rMSSD | sleep_fragmentation_index->morning_HRV_rMSSD | morning_HRV_rMSSD->sleep_fragmentation_index | morning_HRV_rMSSD->sleep_fragmentation_index | morning_HRV_rMSSD->sleep_fragmentation_index | sleep_fragmentation_index -> morning_HRV_rMSSD | (morning_HRV_rMSSD, sleep_fragmentation_index)=A |
| morning_HRV_rMSSD, morning_pain_score | morning_pain_score o-> morning_HRV_rMSSD | morning_HRV_rMSSD   morning_pain_score (no edge) | morning_HRV_rMSSD   morning_pain_score (no edge) | morning_HRV_rMSSD   morning_pain_score (no edge) | morning_HRV_rMSSD   morning_pain_score (no edge) | morning_pain_score -> morning_HRV_rMSSD | (morning_HRV_rMSSD, morning_pain_score)=D |
| nurse_staffing_ratio, planned_nursing_minutes | nurse_staffing_ratio o-o planned_nursing_minutes | nurse_staffing_ratio   planned_nursing_minutes (no edge) | nurse_staffing_ratio->planned_nursing_minutes | nurse_staffing_ratio->planned_nursing_minutes | nurse_staffing_ratio->planned_nursing_minutes | nurse_staffing_ratio -> planned_nursing_minutes | (nurse_staffing_ratio, planned_nursing_minutes)=A |
| nurse_staffing_ratio, vital_sign_schedule_frequency | nurse_staffing_ratio   vital_sign_schedule_frequency (no edge) | nurse_staffing_ratio   vital_sign_schedule_frequency (no edge) | nurse_staffing_ratio->vital_sign_schedule_frequency | nurse_staffing_ratio->vital_sign_schedule_frequency | nurse_staffing_ratio->vital_sign_schedule_frequency | no edge | (nurse_staffing_ratio, vital_sign_schedule_frequency)=A |
| nurse_staffing_ratio, nightly_alarm_count | nurse_staffing_ratio   nightly_alarm_count (no edge) | nurse_staffing_ratio   nightly_alarm_count (no edge) | nurse_staffing_ratio->nightly_alarm_count | nurse_staffing_ratio->nightly_alarm_count | nurse_staffing_ratio->nightly_alarm_count | no edge | (nurse_staffing_ratio, nightly_alarm_count)=A |
| nurse_staffing_ratio, night_lux_summary | nurse_staffing_ratio->night_lux_summary | nurse_staffing_ratio->night_lux_summary | nurse_staffing_ratio   night_lux_summary (no edge) | nurse_staffing_ratio   night_lux_summary (no edge) | nurse_staffing_ratio   night_lux_summary (no edge) | no edge | (nurse_staffing_ratio, night_lux_summary)=C |
| comfort_kit_adherence_index, comfort_bundle_offered | comfort_kit_adherence_index o-o comfort_bundle_offered | comfort_kit_adherence_index   comfort_bundle_offered (no edge) | comfort_kit_adherence_index   comfort_bundle_offered (no edge) | comfort_kit_adherence_index   comfort_bundle_offered (no edge) | comfort_kit_adherence_index   comfort_bundle_offered (no edge) | comfort_bundle_offered -> comfort_kit_adherence_index | (comfort_kit_adherence_index, comfort_bundle_offered)=C |
| arousal_threshold_index, perceived_noise_dose | arousal_threshold_index   perceived_noise_dose (no edge) | arousal_threshold_index   perceived_noise_dose (no edge) | arousal_threshold_index->perceived_noise_dose | arousal_threshold_index->perceived_noise_dose | arousal_threshold_index->perceived_noise_dose | no edge | (arousal_threshold_index, perceived_noise_dose)=A |
| arousal_threshold_index, baseline_evening_pain_score | arousal_threshold_index o-o baseline_evening_pain_score | arousal_threshold_index   baseline_evening_pain_score (no edge) | arousal_threshold_index   baseline_evening_pain_score (no edge) | arousal_threshold_index   baseline_evening_pain_score (no edge) | arousal_threshold_index   baseline_evening_pain_score (no edge) | baseline_evening_pain_score -> arousal_threshold_index | (arousal_threshold_index, baseline_evening_pain_score)=D |
| arousal_threshold_index, sleep_fragmentation_index | arousal_threshold_index o-o sleep_fragmentation_index | arousal_threshold_index   sleep_fragmentation_index (no edge) | arousal_threshold_index->sleep_fragmentation_index | arousal_threshold_index->sleep_fragmentation_index | arousal_threshold_index->sleep_fragmentation_index | arousal_threshold_index -> sleep_fragmentation_index | (arousal_threshold_index, sleep_fragmentation_index)=A |
| perceived_lux_dose, night_lux_summary | perceived_lux_dose   night_lux_summary (no edge) | perceived_lux_dose   night_lux_summary (no edge) | perceived_lux_dose->night_lux_summary | perceived_lux_dose->night_lux_summary | perceived_lux_dose->night_lux_summary | night_lux_summary -> perceived_lux_dose | (perceived_lux_dose, night_lux_summary)=A |
| perceived_lux_dose, sleep_fragmentation_index | perceived_lux_dose   sleep_fragmentation_index (no edge) | perceived_lux_dose   sleep_fragmentation_index (no edge) | perceived_lux_dose->sleep_fragmentation_index | perceived_lux_dose->sleep_fragmentation_index | perceived_lux_dose->sleep_fragmentation_index | perceived_lux_dose -> sleep_fragmentation_index | (perceived_lux_dose, sleep_fragmentation_index)=A |
| roommate_Lmax_spikes_count, perceived_noise_dose | roommate_Lmax_spikes_count o-> perceived_noise_dose | roommate_Lmax_spikes_count   perceived_noise_dose (no edge) | roommate_Lmax_spikes_count->perceived_noise_dose | roommate_Lmax_spikes_count->perceived_noise_dose | roommate_Lmax_spikes_count->perceived_noise_dose | roommate_Lmax_spikes_count -> perceived_noise_dose | (roommate_Lmax_spikes_count, perceived_noise_dose)=A |
| roommate_Lmax_spikes_count, alarm_related_LAeq | roommate_Lmax_spikes_count   alarm_related_LAeq (no edge) | roommate_Lmax_spikes_count   alarm_related_LAeq (no edge) | roommate_Lmax_spikes_count->alarm_related_LAeq | roommate_Lmax_spikes_count->alarm_related_LAeq | roommate_Lmax_spikes_count->alarm_related_LAeq | no edge | (roommate_Lmax_spikes_count, alarm_related_LAeq)=A |
| roommate_Lmax_spikes_count, sleep_fragmentation_index | roommate_Lmax_spikes_count   sleep_fragmentation_index (no edge) | roommate_Lmax_spikes_count   sleep_fragmentation_index (no edge) | roommate_Lmax_spikes_count->sleep_fragmentation_index | roommate_Lmax_spikes_count->sleep_fragmentation_index | roommate_Lmax_spikes_count->sleep_fragmentation_index | no edge | (roommate_Lmax_spikes_count, sleep_fragmentation_index)=A |
| cns_depressant_dose_index, baseline_evening_pain_score | baseline_evening_pain_score->cns_depressant_dose_index | cns_depressant_dose_index   baseline_evening_pain_score (no edge) | cns_depressant_dose_index   baseline_evening_pain_score (no edge) | cns_depressant_dose_index   baseline_evening_pain_score (no edge) | cns_depressant_dose_index   baseline_evening_pain_score (no edge) | baseline_evening_pain_score -> cns_depressant_dose_index | (cns_depressant_dose_index, baseline_evening_pain_score)=D |
| cns_depressant_dose_index, sleep_fragmentation_index | cns_depressant_dose_index   sleep_fragmentation_index (no edge) | cns_depressant_dose_index   sleep_fragmentation_index (no edge) | cns_depressant_dose_index->sleep_fragmentation_index | cns_depressant_dose_index->sleep_fragmentation_index | cns_depressant_dose_index->sleep_fragmentation_index | no edge | (cns_depressant_dose_index, sleep_fragmentation_index)=A |
| cns_depressant_dose_index, morning_pain_score | cns_depressant_dose_index   morning_pain_score (no edge) | cns_depressant_dose_index   morning_pain_score (no edge) | cns_depressant_dose_index->morning_pain_score | cns_depressant_dose_index->morning_pain_score | cns_depressant_dose_index->morning_pain_score | cns_depressant_dose_index -> morning_pain_score | (cns_depressant_dose_index, morning_pain_score)=A |
| room_acoustic_reverberation_gain, perceived_noise_dose | room_acoustic_reverberation_gain   perceived_noise_dose (no edge) | room_acoustic_reverberation_gain   perceived_noise_dose (no edge) | room_acoustic_reverberation_gain->perceived_noise_dose | room_acoustic_reverberation_gain->perceived_noise_dose | room_acoustic_reverberation_gain->perceived_noise_dose | no edge | (room_acoustic_reverberation_gain, perceived_noise_dose)=A |
| room_acoustic_reverberation_gain, alarm_related_LAeq | room_acoustic_reverberation_gain o-> alarm_related_LAeq | room_acoustic_reverberation_gain   alarm_related_LAeq (no edge) | room_acoustic_reverberation_gain->alarm_related_LAeq | room_acoustic_reverberation_gain->alarm_related_LAeq | room_acoustic_reverberation_gain->alarm_related_LAeq | room_acoustic_reverberation_gain -> alarm_related_LAeq | (room_acoustic_reverberation_gain, alarm_related_LAeq)=A |
| perceived_noise_dose, nightly_alarm_count | perceived_noise_dose   nightly_alarm_count (no edge) | perceived_noise_dose   nightly_alarm_count (no edge) | nightly_alarm_count->perceived_noise_dose | nightly_alarm_count->perceived_noise_dose | nightly_alarm_count->perceived_noise_dose | nightly_alarm_count -> perceived_noise_dose | (perceived_noise_dose, nightly_alarm_count)=B |
| perceived_noise_dose, alarm_quieting_bundle_state | perceived_noise_dose   alarm_quieting_bundle_state (no edge) | perceived_noise_dose   alarm_quieting_bundle_state (no edge) | alarm_quieting_bundle_state->perceived_noise_dose | alarm_quieting_bundle_state->perceived_noise_dose | alarm_quieting_bundle_state->perceived_noise_dose | no edge | (perceived_noise_dose, alarm_quieting_bundle_state)=B |
| perceived_noise_dose, sleep_fragmentation_index | perceived_noise_dose   sleep_fragmentation_index (no edge) | perceived_noise_dose   sleep_fragmentation_index (no edge) | perceived_noise_dose->sleep_fragmentation_index | perceived_noise_dose->sleep_fragmentation_index | perceived_noise_dose->sleep_fragmentation_index | perceived_noise_dose -> sleep_fragmentation_index | (perceived_noise_dose, sleep_fragmentation_index)=A |
| nightly_alarm_count, night_lux_summary | nightly_alarm_count <-> night_lux_summary | nightly_alarm_count   night_lux_summary (no edge) | nightly_alarm_count   night_lux_summary (no edge) | nightly_alarm_count   night_lux_summary (no edge) | nightly_alarm_count   night_lux_summary (no edge) | nightly_alarm_count -> night_lux_summary | (nightly_alarm_count, night_lux_summary)=C |
| nightly_alarm_count, alarm_quieting_bundle_state | nightly_alarm_count <-> alarm_quieting_bundle_state | nightly_alarm_count   alarm_quieting_bundle_state (no edge) | alarm_quieting_bundle_state->nightly_alarm_count | alarm_quieting_bundle_state->nightly_alarm_count | alarm_quieting_bundle_state->nightly_alarm_count | alarm_quieting_bundle_state -> nightly_alarm_count | (nightly_alarm_count, alarm_quieting_bundle_state)=B |
| nightly_alarm_count, sleep_fragmentation_index | nightly_alarm_count   sleep_fragmentation_index (no edge) | nightly_alarm_count   sleep_fragmentation_index (no edge) | nightly_alarm_count->sleep_fragmentation_index | nightly_alarm_count->sleep_fragmentation_index | nightly_alarm_count->sleep_fragmentation_index | no edge | (nightly_alarm_count, sleep_fragmentation_index)=A |
| night_lux_summary, sleep_fragmentation_index | night_lux_summary   sleep_fragmentation_index (no edge) | night_lux_summary   sleep_fragmentation_index (no edge) | night_lux_summary->sleep_fragmentation_index | night_lux_summary->sleep_fragmentation_index | night_lux_summary->sleep_fragmentation_index | no edge | (night_lux_summary, sleep_fragmentation_index)=A |
| alarm_quieting_bundle_state, alarm_related_LAeq | alarm_quieting_bundle_state <-> alarm_related_LAeq | alarm_quieting_bundle_state   alarm_related_LAeq (no edge) | alarm_quieting_bundle_state->alarm_related_LAeq | alarm_quieting_bundle_state->alarm_related_LAeq | alarm_quieting_bundle_state->alarm_related_LAeq | no edge | (alarm_quieting_bundle_state, alarm_related_LAeq)=A |
| alarm_quieting_bundle_state, sleep_fragmentation_index | alarm_quieting_bundle_state   sleep_fragmentation_index (no edge) | alarm_quieting_bundle_state   sleep_fragmentation_index (no edge) | alarm_quieting_bundle_state->sleep_fragmentation_index | alarm_quieting_bundle_state->sleep_fragmentation_index | alarm_quieting_bundle_state->sleep_fragmentation_index | no edge | (alarm_quieting_bundle_state, sleep_fragmentation_index)=A |
| alarm_related_LAeq, sleep_fragmentation_index | alarm_related_LAeq   sleep_fragmentation_index (no edge) | alarm_related_LAeq   sleep_fragmentation_index (no edge) | alarm_related_LAeq->sleep_fragmentation_index | alarm_related_LAeq->sleep_fragmentation_index | alarm_related_LAeq->sleep_fragmentation_index | no edge | (alarm_related_LAeq, sleep_fragmentation_index)=A |
| baseline_evening_pain_score, morning_pain_score | baseline_evening_pain_score   morning_pain_score (no edge) | baseline_evening_pain_score   morning_pain_score (no edge) | baseline_evening_pain_score->morning_pain_score | baseline_evening_pain_score->morning_pain_score | baseline_evening_pain_score->morning_pain_score | baseline_evening_pain_score -> morning_pain_score | (baseline_evening_pain_score, morning_pain_score)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
