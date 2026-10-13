# Edge lineage: 20261011T194923Z_s2_q031_r01_a1dacd

Dataset `/research/datasets/suite_q1s2/q031/q031.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 25 | 0.72 | 0.31 | 0.43 | 1 | 1 | 16 | 64 |
| S1 after bootstrap edits | 10 | 0.40 | 0.07 | 0.12 | 1 | 0 | 3 | 63 |
| S2 after LLM review | 22 | 0.36 | 0.14 | 0.20 | 2 | 5 | 1 | 70 |
| S3 after KCI pruning | 19 | 0.42 | 0.14 | 0.21 | 2 | 5 | 1 | 67 |
| S4 final (after cycle step) | 19 | 0.42 | 0.14 | 0.21 | 2 | 5 | 1 | 67 |

Scored against: reference graph s2_03_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 15. Of the deleted, 7 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 11, "B": 8, "C": 79, "D": 202}.
- LLM effect: added 15 (of which 13 where the resamples showed no edge at frequency >= 0.9), removed 3, re-oriented 2.
- KCI step removed 3. Cycle step changed 0.
- Final graph: 19 edges; set by {"algorithm (unchanged)": 5, "llm": 14}; 5 identical to the algorithm's output; 11 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| attention_share_siren <-> attention_share_sms | algorithm (unchanged) | yes | 0.00 |
| attention_share_siren->siren_audibility_index | llm | yes | 0.00 |
| attention_share_siren->attention_share_news | algorithm (unchanged) | yes | 0.20 |
| hazard_distance_at_t0->departure_time_observed | llm | no | 0.90 |
| readiness_time_since_t0->departure_time_observed | llm | no | 0.95 |
| hazard_distance_at_t0->congestion_index_at_decision | llm | no | 1.00 |
| hazard_distance_at_t0->departure_time_true | llm | yes | 0.15 |
| hazard_distance_at_t0->readiness_time_since_t0 | llm | no | 0.85 |
| hazard_distance_at_t0->local_cumulative_departure_fraction | llm | no | 1.00 |
| attention_share_sms->sms_alert_enabled | llm | no | 1.00 |
| attention_share_sms->handset_reachable | llm | no | 1.00 |
| attention_share_social->attention_share_sms | algorithm (unchanged) | yes | 0.10 |
| congestion_index_at_decision->local_cumulative_departure_fraction | llm | yes | 0.00 |
| attention_share_neighbors o-o attention_share_social | algorithm (unchanged) | yes | 0.20 |
| departure_time_true->readiness_time_since_t0 | llm | no | 0.95 |
| hazard_approach_rate->departure_time_true | llm | no | 0.90 |
| departure_time_true->vehicle_access | llm | no | 1.00 |
| pickup_eta_minutes->departure_time_true | llm | no | 1.00 |
| readiness_time_since_t0 <-> pickup_eta_minutes | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| prior_false_alarm_experience, attention_share_siren | prior_false_alarm_experience <-> attention_share_siren | prior_false_alarm_experience   attention_share_siren (no edge) | prior_false_alarm_experience   attention_share_siren (no edge) | prior_false_alarm_experience   attention_share_siren (no edge) | prior_false_alarm_experience   attention_share_siren (no edge) | prior_false_alarm_experience -> attention_share_siren | (prior_false_alarm_experience, attention_share_siren)=D |
| prior_false_alarm_experience, perceived_credibility_score | perceived_credibility_score o-> prior_false_alarm_experience | prior_false_alarm_experience   perceived_credibility_score (no edge) | prior_false_alarm_experience   perceived_credibility_score (no edge) | prior_false_alarm_experience   perceived_credibility_score (no edge) | prior_false_alarm_experience   perceived_credibility_score (no edge) | prior_false_alarm_experience -> perceived_credibility_score | (prior_false_alarm_experience, perceived_credibility_score)=D |
| assistance_request, readiness_time_since_t0 | readiness_time_since_t0->assistance_request | assistance_request   readiness_time_since_t0 (no edge) | assistance_request   readiness_time_since_t0 (no edge) | assistance_request   readiness_time_since_t0 (no edge) | assistance_request   readiness_time_since_t0 (no edge) | assistance_request -> readiness_time_since_t0 | (assistance_request, readiness_time_since_t0)=D |
| assistance_request, pickup_eta_minutes | assistance_request <-> pickup_eta_minutes | assistance_request   pickup_eta_minutes (no edge) | assistance_request   pickup_eta_minutes (no edge) | assistance_request   pickup_eta_minutes (no edge) | assistance_request   pickup_eta_minutes (no edge) | assistance_request -> pickup_eta_minutes | (assistance_request, pickup_eta_minutes)=D |
| attention_share_siren, siren_audibility_index | attention_share_siren <-> siren_audibility_index | attention_share_siren   siren_audibility_index (no edge) | attention_share_siren->siren_audibility_index | attention_share_siren->siren_audibility_index | attention_share_siren->siren_audibility_index | siren_audibility_index -> attention_share_siren | (attention_share_siren, siren_audibility_index)=A |
| attention_share_siren, attention_share_neighbors | attention_share_neighbors o-> attention_share_siren | attention_share_neighbors o-> attention_share_siren | attention_share_siren   attention_share_neighbors (no edge) | attention_share_siren   attention_share_neighbors (no edge) | attention_share_siren   attention_share_neighbors (no edge) | no edge | (attention_share_siren, attention_share_neighbors)=C |
| attention_share_siren, attention_share_social | attention_share_social o-> attention_share_siren | attention_share_social o-> attention_share_siren | attention_share_siren   attention_share_social (no edge) | attention_share_siren   attention_share_social (no edge) | attention_share_siren   attention_share_social (no edge) | no edge | (attention_share_siren, attention_share_social)=C |
| departure_time_observed, hazard_distance_at_t0 | departure_time_observed   hazard_distance_at_t0 (no edge) | departure_time_observed   hazard_distance_at_t0 (no edge) | hazard_distance_at_t0->departure_time_observed | hazard_distance_at_t0->departure_time_observed | hazard_distance_at_t0->departure_time_observed | no edge | (departure_time_observed, hazard_distance_at_t0)=B |
| departure_time_observed, congestion_index_at_decision | departure_time_observed   congestion_index_at_decision (no edge) | departure_time_observed   congestion_index_at_decision (no edge) | congestion_index_at_decision->departure_time_observed | departure_time_observed   congestion_index_at_decision (no edge) | departure_time_observed   congestion_index_at_decision (no edge) | no edge | (departure_time_observed, congestion_index_at_decision)=B |
| departure_time_observed, departure_time_true | departure_time_observed o-o departure_time_true | departure_time_observed   departure_time_true (no edge) | departure_time_observed   departure_time_true (no edge) | departure_time_observed   departure_time_true (no edge) | departure_time_observed   departure_time_true (no edge) | departure_time_true -> departure_time_observed | (departure_time_observed, departure_time_true)=D |
| departure_time_observed, readiness_time_since_t0 | departure_time_observed   readiness_time_since_t0 (no edge) | departure_time_observed   readiness_time_since_t0 (no edge) | readiness_time_since_t0->departure_time_observed | readiness_time_since_t0->departure_time_observed | readiness_time_since_t0->departure_time_observed | no edge | (departure_time_observed, readiness_time_since_t0)=B |
| departure_time_observed, hazard_approach_rate | departure_time_observed   hazard_approach_rate (no edge) | departure_time_observed   hazard_approach_rate (no edge) | hazard_approach_rate->departure_time_observed | departure_time_observed   hazard_approach_rate (no edge) | departure_time_observed   hazard_approach_rate (no edge) | no edge | (departure_time_observed, hazard_approach_rate)=B |
| departure_time_observed, vehicle_access | departure_time_observed   vehicle_access (no edge) | departure_time_observed   vehicle_access (no edge) | vehicle_access->departure_time_observed | departure_time_observed   vehicle_access (no edge) | departure_time_observed   vehicle_access (no edge) | no edge | (departure_time_observed, vehicle_access)=B |
| departure_time_observed, censor_indicator | departure_time_observed o-o censor_indicator | departure_time_observed   censor_indicator (no edge) | departure_time_observed   censor_indicator (no edge) | departure_time_observed   censor_indicator (no edge) | departure_time_observed   censor_indicator (no edge) | censor_indicator -> departure_time_observed | (departure_time_observed, censor_indicator)=D |
| hazard_distance_at_t0, congestion_index_at_decision | hazard_distance_at_t0   congestion_index_at_decision (no edge) | hazard_distance_at_t0   congestion_index_at_decision (no edge) | hazard_distance_at_t0->congestion_index_at_decision | hazard_distance_at_t0->congestion_index_at_decision | hazard_distance_at_t0->congestion_index_at_decision | no edge | (hazard_distance_at_t0, congestion_index_at_decision)=A |
| hazard_distance_at_t0, departure_time_true | hazard_distance_at_t0 o-o departure_time_true | hazard_distance_at_t0 o-o departure_time_true | hazard_distance_at_t0->departure_time_true | hazard_distance_at_t0->departure_time_true | hazard_distance_at_t0->departure_time_true | hazard_distance_at_t0 -> departure_time_true | (hazard_distance_at_t0, departure_time_true)=A |
| hazard_distance_at_t0, readiness_time_since_t0 | hazard_distance_at_t0   readiness_time_since_t0 (no edge) | hazard_distance_at_t0   readiness_time_since_t0 (no edge) | hazard_distance_at_t0->readiness_time_since_t0 | hazard_distance_at_t0->readiness_time_since_t0 | hazard_distance_at_t0->readiness_time_since_t0 | no edge | (hazard_distance_at_t0, readiness_time_since_t0)=A |
| hazard_distance_at_t0, local_cumulative_departure_fraction | hazard_distance_at_t0   local_cumulative_departure_fraction (no edge) | hazard_distance_at_t0   local_cumulative_departure_fraction (no edge) | hazard_distance_at_t0->local_cumulative_departure_fraction | hazard_distance_at_t0->local_cumulative_departure_fraction | hazard_distance_at_t0->local_cumulative_departure_fraction | no edge | (hazard_distance_at_t0, local_cumulative_departure_fraction)=A |
| message_specificity_level, local_cumulative_departure_fraction | message_specificity_level o-> local_cumulative_departure_fraction | message_specificity_level   local_cumulative_departure_fraction (no edge) | message_specificity_level   local_cumulative_departure_fraction (no edge) | message_specificity_level   local_cumulative_departure_fraction (no edge) | message_specificity_level   local_cumulative_departure_fraction (no edge) | message_specificity_level -> local_cumulative_departure_fraction | (message_specificity_level, local_cumulative_departure_fraction)=D |
| attention_share_sms, sms_alert_enabled | attention_share_sms   sms_alert_enabled (no edge) | attention_share_sms   sms_alert_enabled (no edge) | attention_share_sms->sms_alert_enabled | attention_share_sms->sms_alert_enabled | attention_share_sms->sms_alert_enabled | sms_alert_enabled -> attention_share_sms | (attention_share_sms, sms_alert_enabled)=A |
| attention_share_sms, handset_reachable | attention_share_sms   handset_reachable (no edge) | attention_share_sms   handset_reachable (no edge) | attention_share_sms->handset_reachable | attention_share_sms->handset_reachable | attention_share_sms->handset_reachable | handset_reachable -> attention_share_sms | (attention_share_sms, handset_reachable)=A |
| attention_share_sms, siren_audibility_index | siren_audibility_index o-> attention_share_sms | siren_audibility_index o-> attention_share_sms | attention_share_sms   siren_audibility_index (no edge) | attention_share_sms   siren_audibility_index (no edge) | attention_share_sms   siren_audibility_index (no edge) | siren_audibility_index -> attention_share_sms | (attention_share_sms, siren_audibility_index)=C |
| attention_share_sms, attention_share_news | attention_share_sms <-> attention_share_news | attention_share_sms   attention_share_news (no edge) | attention_share_sms   attention_share_news (no edge) | attention_share_sms   attention_share_news (no edge) | attention_share_sms   attention_share_news (no edge) | no edge | (attention_share_sms, attention_share_news)=C |
| congestion_index_at_decision, local_cumulative_departure_fraction | local_cumulative_departure_fraction->congestion_index_at_decision | local_cumulative_departure_fraction->congestion_index_at_decision | congestion_index_at_decision->local_cumulative_departure_fraction | congestion_index_at_decision->local_cumulative_departure_fraction | congestion_index_at_decision->local_cumulative_departure_fraction | local_cumulative_departure_fraction -> congestion_index_at_decision | (congestion_index_at_decision, local_cumulative_departure_fraction)=A |
| sms_alert_enabled, local_cumulative_departure_fraction | sms_alert_enabled o-> local_cumulative_departure_fraction | sms_alert_enabled   local_cumulative_departure_fraction (no edge) | sms_alert_enabled   local_cumulative_departure_fraction (no edge) | sms_alert_enabled   local_cumulative_departure_fraction (no edge) | sms_alert_enabled   local_cumulative_departure_fraction (no edge) | sms_alert_enabled -> local_cumulative_departure_fraction | (sms_alert_enabled, local_cumulative_departure_fraction)=C |
| mobility_needs_index, readiness_time_since_t0 | mobility_needs_index o-> readiness_time_since_t0 | mobility_needs_index   readiness_time_since_t0 (no edge) | mobility_needs_index   readiness_time_since_t0 (no edge) | mobility_needs_index   readiness_time_since_t0 (no edge) | mobility_needs_index   readiness_time_since_t0 (no edge) | mobility_needs_index -> readiness_time_since_t0 | (mobility_needs_index, readiness_time_since_t0)=D |
| siren_audibility_index, attention_share_news | siren_audibility_index <-> attention_share_news | siren_audibility_index   attention_share_news (no edge) | siren_audibility_index   attention_share_news (no edge) | siren_audibility_index   attention_share_news (no edge) | siren_audibility_index   attention_share_news (no edge) | siren_audibility_index -> attention_share_news | (siren_audibility_index, attention_share_news)=D |
| departure_time_true, readiness_time_since_t0 | departure_time_true   readiness_time_since_t0 (no edge) | departure_time_true   readiness_time_since_t0 (no edge) | departure_time_true->readiness_time_since_t0 | departure_time_true->readiness_time_since_t0 | departure_time_true->readiness_time_since_t0 | readiness_time_since_t0 -> departure_time_true | (departure_time_true, readiness_time_since_t0)=A |
| departure_time_true, hazard_approach_rate | departure_time_true   hazard_approach_rate (no edge) | departure_time_true   hazard_approach_rate (no edge) | hazard_approach_rate->departure_time_true | hazard_approach_rate->departure_time_true | hazard_approach_rate->departure_time_true | hazard_approach_rate -> departure_time_true | (departure_time_true, hazard_approach_rate)=B |
| departure_time_true, vehicle_access | departure_time_true   vehicle_access (no edge) | departure_time_true   vehicle_access (no edge) | departure_time_true->vehicle_access | departure_time_true->vehicle_access | departure_time_true->vehicle_access | no edge | (departure_time_true, vehicle_access)=A |
| departure_time_true, pickup_eta_minutes | departure_time_true   pickup_eta_minutes (no edge) | departure_time_true   pickup_eta_minutes (no edge) | pickup_eta_minutes->departure_time_true | pickup_eta_minutes->departure_time_true | pickup_eta_minutes->departure_time_true | no edge | (departure_time_true, pickup_eta_minutes)=B |
| departure_time_true, censor_indicator | departure_time_true o-o censor_indicator | departure_time_true   censor_indicator (no edge) | departure_time_true   censor_indicator (no edge) | departure_time_true   censor_indicator (no edge) | departure_time_true   censor_indicator (no edge) | departure_time_true -> censor_indicator | (departure_time_true, censor_indicator)=D |
| readiness_time_since_t0, vehicle_access | vehicle_access o-> readiness_time_since_t0 | readiness_time_since_t0   vehicle_access (no edge) | readiness_time_since_t0   vehicle_access (no edge) | readiness_time_since_t0   vehicle_access (no edge) | readiness_time_since_t0   vehicle_access (no edge) | vehicle_access -> readiness_time_since_t0 | (readiness_time_since_t0, vehicle_access)=D |
| hazard_approach_rate, local_cumulative_departure_fraction | hazard_approach_rate o-> local_cumulative_departure_fraction | hazard_approach_rate   local_cumulative_departure_fraction (no edge) | hazard_approach_rate   local_cumulative_departure_fraction (no edge) | hazard_approach_rate   local_cumulative_departure_fraction (no edge) | hazard_approach_rate   local_cumulative_departure_fraction (no edge) | hazard_approach_rate -> local_cumulative_departure_fraction | (hazard_approach_rate, local_cumulative_departure_fraction)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
