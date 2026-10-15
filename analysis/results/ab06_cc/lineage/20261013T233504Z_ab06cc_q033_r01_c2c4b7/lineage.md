# Edge lineage: 20261013T233504Z_ab06cc_q033_r01_c2c4b7

Dataset `/research/datasets/suite_q1s2/q033/q033.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 2}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 30 | 0.70 | 0.36 | 0.48 | 1 | 1 | 19 | 66 |
| S1 after bootstrap edits | 8 | 0.50 | 0.07 | 0.12 | 1 | 1 | 2 | 61 |
| S2 after LLM review | 41 | 0.20 | 0.14 | 0.16 | 5 | 2 | 1 | 86 |
| S3 after KCI pruning | 41 | 0.20 | 0.14 | 0.16 | 5 | 2 | 1 | 86 |
| S4 final (after cycle step) | 41 | 0.20 | 0.14 | 0.16 | 5 | 2 | 1 | 86 |

Scored against: reference graph s2_03_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 22. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 39, "C": 237, "D": 24}.
- LLM effect: added 35 (of which 31 where the resamples showed no edge at frequency >= 0.9), removed 2, re-oriented 2.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 41 edges; set by {"llm": 37, "algorithm (unchanged)": 4}; 4 identical to the algorithm's output; 33 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| assistance_request->prior_false_alarm_experience | llm | no | 1.00 |
| assistance_request->attention_share_siren | llm | no | 1.00 |
| assistance_request->baseline_risk_tolerance | llm | no | 1.00 |
| assistance_request->hazard_distance_at_t0 | llm | yes | 0.70 |
| assistance_request->perceived_credibility_score | llm | no | 1.00 |
| assistance_request->attention_share_sms | llm | no | 1.00 |
| assistance_request->congestion_index_at_decision | llm | no | 0.95 |
| assistance_request->message_specificity_level | llm | no | 1.00 |
| assistance_request->mobility_needs_index | llm | no | 1.00 |
| assistance_request->attention_share_neighbors | llm | no | 1.00 |
| assistance_request->sms_alert_enabled | llm | no | 1.00 |
| assistance_request->attention_share_social | llm | no | 0.95 |
| assistance_request->local_cumulative_departure_fraction | llm | no | 0.80 |
| assistance_request->hazard_approach_rate | llm | no | 1.00 |
| assistance_request->attention_share_news | llm | no | 0.75 |
| assistance_request->handset_reachable | llm | no | 1.00 |
| assistance_request->siren_audibility_index | llm | no | 1.00 |
| assistance_request->vehicle_access | llm | no | 1.00 |
| departure_time_observed->congestion_index_at_decision | llm | yes | 0.00 |
| departure_time_observed->departure_time_true | llm | no | 1.00 |
| departure_time_observed->censor_indicator | algorithm (unchanged) | yes | 0.20 |
| attention_share_siren->siren_audibility_index | llm | no | 1.00 |
| baseline_risk_tolerance->mobility_needs_index | llm | no | 0.90 |
| assistance_fleet_vehicles->vehicle_access | llm | no | 0.90 |
| perceived_credibility_score->message_specificity_level | llm | no | 1.00 |
| hazard_approach_rate->perceived_credibility_score | algorithm (unchanged) | yes | 0.15 |
| perceived_credibility_score->attention_share_news | llm | no | 1.00 |
| attention_share_sms->sms_alert_enabled | llm | no | 1.00 |
| congestion_index_at_decision <-> attention_share_social | algorithm (unchanged) | yes | 0.00 |
| congestion_index_at_decision->local_cumulative_departure_fraction | algorithm (unchanged) | yes | 0.35 |
| congestion_index_at_decision->departure_time_true | llm | no | 1.00 |
| congestion_index_at_decision->pickup_eta_minutes | llm | no | 1.00 |
| message_specificity_level->attention_share_news | llm | no | 1.00 |
| mobility_needs_index->vehicle_access | llm | no | 1.00 |
| attention_share_neighbors->attention_share_social | llm | no | 1.00 |
| attention_share_social->attention_share_news | llm | yes | 0.10 |
| local_cumulative_departure_fraction->departure_time_true | llm | no | 1.00 |
| hazard_approach_rate->attention_share_news | llm | no | 1.00 |
| handset_reachable->vehicle_access | llm | yes | 0.10 |
| departure_time_true->pickup_eta_minutes | llm | no | 1.00 |
| departure_time_true->censor_indicator | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| assistance_request, prior_false_alarm_experience | assistance_request   prior_false_alarm_experience (no edge) | assistance_request   prior_false_alarm_experience (no edge) | assistance_request->prior_false_alarm_experience | assistance_request->prior_false_alarm_experience | assistance_request->prior_false_alarm_experience | no edge | (assistance_request, prior_false_alarm_experience)=A |
| assistance_request, departure_time_observed | assistance_request o-> departure_time_observed | assistance_request   departure_time_observed (no edge) | assistance_request   departure_time_observed (no edge) | assistance_request   departure_time_observed (no edge) | assistance_request   departure_time_observed (no edge) | assistance_request -> departure_time_observed | (assistance_request, departure_time_observed)=C |
| assistance_request, attention_share_siren | assistance_request   attention_share_siren (no edge) | assistance_request   attention_share_siren (no edge) | assistance_request->attention_share_siren | assistance_request->attention_share_siren | assistance_request->attention_share_siren | no edge | (assistance_request, attention_share_siren)=A |
| assistance_request, baseline_risk_tolerance | assistance_request   baseline_risk_tolerance (no edge) | assistance_request   baseline_risk_tolerance (no edge) | assistance_request->baseline_risk_tolerance | assistance_request->baseline_risk_tolerance | assistance_request->baseline_risk_tolerance | no edge | (assistance_request, baseline_risk_tolerance)=A |
| assistance_request, hazard_distance_at_t0 | assistance_request o-> hazard_distance_at_t0 | assistance_request   hazard_distance_at_t0 (no edge) | assistance_request->hazard_distance_at_t0 | assistance_request->hazard_distance_at_t0 | assistance_request->hazard_distance_at_t0 | assistance_request -> hazard_distance_at_t0 | (assistance_request, hazard_distance_at_t0)=A |
| assistance_request, perceived_credibility_score | assistance_request   perceived_credibility_score (no edge) | assistance_request   perceived_credibility_score (no edge) | assistance_request->perceived_credibility_score | assistance_request->perceived_credibility_score | assistance_request->perceived_credibility_score | no edge | (assistance_request, perceived_credibility_score)=A |
| assistance_request, attention_share_sms | assistance_request   attention_share_sms (no edge) | assistance_request   attention_share_sms (no edge) | assistance_request->attention_share_sms | assistance_request->attention_share_sms | assistance_request->attention_share_sms | no edge | (assistance_request, attention_share_sms)=A |
| assistance_request, congestion_index_at_decision | assistance_request   congestion_index_at_decision (no edge) | assistance_request   congestion_index_at_decision (no edge) | assistance_request->congestion_index_at_decision | assistance_request->congestion_index_at_decision | assistance_request->congestion_index_at_decision | assistance_request -> congestion_index_at_decision | (assistance_request, congestion_index_at_decision)=A |
| assistance_request, message_specificity_level | assistance_request   message_specificity_level (no edge) | assistance_request   message_specificity_level (no edge) | assistance_request->message_specificity_level | assistance_request->message_specificity_level | assistance_request->message_specificity_level | no edge | (assistance_request, message_specificity_level)=A |
| assistance_request, mobility_needs_index | assistance_request   mobility_needs_index (no edge) | assistance_request   mobility_needs_index (no edge) | assistance_request->mobility_needs_index | assistance_request->mobility_needs_index | assistance_request->mobility_needs_index | no edge | (assistance_request, mobility_needs_index)=A |
| assistance_request, attention_share_neighbors | assistance_request   attention_share_neighbors (no edge) | assistance_request   attention_share_neighbors (no edge) | assistance_request->attention_share_neighbors | assistance_request->attention_share_neighbors | assistance_request->attention_share_neighbors | no edge | (assistance_request, attention_share_neighbors)=A |
| assistance_request, sms_alert_enabled | assistance_request   sms_alert_enabled (no edge) | assistance_request   sms_alert_enabled (no edge) | assistance_request->sms_alert_enabled | assistance_request->sms_alert_enabled | assistance_request->sms_alert_enabled | no edge | (assistance_request, sms_alert_enabled)=A |
| assistance_request, attention_share_social | assistance_request   attention_share_social (no edge) | assistance_request   attention_share_social (no edge) | assistance_request->attention_share_social | assistance_request->attention_share_social | assistance_request->attention_share_social | no edge | (assistance_request, attention_share_social)=A |
| assistance_request, local_cumulative_departure_fraction | assistance_request   local_cumulative_departure_fraction (no edge) | assistance_request   local_cumulative_departure_fraction (no edge) | assistance_request->local_cumulative_departure_fraction | assistance_request->local_cumulative_departure_fraction | assistance_request->local_cumulative_departure_fraction | assistance_request -> local_cumulative_departure_fraction | (assistance_request, local_cumulative_departure_fraction)=A |
| assistance_request, hazard_approach_rate | assistance_request   hazard_approach_rate (no edge) | assistance_request   hazard_approach_rate (no edge) | assistance_request->hazard_approach_rate | assistance_request->hazard_approach_rate | assistance_request->hazard_approach_rate | no edge | (assistance_request, hazard_approach_rate)=A |
| assistance_request, attention_share_news | assistance_request   attention_share_news (no edge) | assistance_request   attention_share_news (no edge) | assistance_request->attention_share_news | assistance_request->attention_share_news | assistance_request->attention_share_news | assistance_request -> attention_share_news | (assistance_request, attention_share_news)=A |
| assistance_request, handset_reachable | assistance_request   handset_reachable (no edge) | assistance_request   handset_reachable (no edge) | assistance_request->handset_reachable | assistance_request->handset_reachable | assistance_request->handset_reachable | no edge | (assistance_request, handset_reachable)=A |
| assistance_request, siren_audibility_index | assistance_request   siren_audibility_index (no edge) | assistance_request   siren_audibility_index (no edge) | assistance_request->siren_audibility_index | assistance_request->siren_audibility_index | assistance_request->siren_audibility_index | no edge | (assistance_request, siren_audibility_index)=A |
| assistance_request, vehicle_access | assistance_request   vehicle_access (no edge) | assistance_request   vehicle_access (no edge) | assistance_request->vehicle_access | assistance_request->vehicle_access | assistance_request->vehicle_access | no edge | (assistance_request, vehicle_access)=A |
| prior_false_alarm_experience, perceived_credibility_score | prior_false_alarm_experience o-> perceived_credibility_score | prior_false_alarm_experience   perceived_credibility_score (no edge) | prior_false_alarm_experience   perceived_credibility_score (no edge) | prior_false_alarm_experience   perceived_credibility_score (no edge) | prior_false_alarm_experience   perceived_credibility_score (no edge) | perceived_credibility_score -> prior_false_alarm_experience | (prior_false_alarm_experience, perceived_credibility_score)=C |
| prior_false_alarm_experience, vehicle_access | prior_false_alarm_experience o-> vehicle_access | prior_false_alarm_experience   vehicle_access (no edge) | prior_false_alarm_experience   vehicle_access (no edge) | prior_false_alarm_experience   vehicle_access (no edge) | prior_false_alarm_experience   vehicle_access (no edge) | prior_false_alarm_experience -> vehicle_access | (prior_false_alarm_experience, vehicle_access)=C |
| departure_time_observed, congestion_index_at_decision | congestion_index_at_decision->departure_time_observed | congestion_index_at_decision->departure_time_observed | departure_time_observed->congestion_index_at_decision | departure_time_observed->congestion_index_at_decision | departure_time_observed->congestion_index_at_decision | no edge | (departure_time_observed, congestion_index_at_decision)=A |
| departure_time_observed, attention_share_social | departure_time_observed <-> attention_share_social | departure_time_observed   attention_share_social (no edge) | departure_time_observed   attention_share_social (no edge) | departure_time_observed   attention_share_social (no edge) | departure_time_observed   attention_share_social (no edge) | attention_share_social -> departure_time_observed | (departure_time_observed, attention_share_social)=C |
| departure_time_observed, local_cumulative_departure_fraction | departure_time_observed->local_cumulative_departure_fraction | departure_time_observed   local_cumulative_departure_fraction (no edge) | departure_time_observed   local_cumulative_departure_fraction (no edge) | departure_time_observed   local_cumulative_departure_fraction (no edge) | departure_time_observed   local_cumulative_departure_fraction (no edge) | no edge | (departure_time_observed, local_cumulative_departure_fraction)=C |
| departure_time_observed, attention_share_news | departure_time_observed->attention_share_news | departure_time_observed   attention_share_news (no edge) | departure_time_observed   attention_share_news (no edge) | departure_time_observed   attention_share_news (no edge) | departure_time_observed   attention_share_news (no edge) | no edge | (departure_time_observed, attention_share_news)=C |
| departure_time_observed, departure_time_true | departure_time_observed   departure_time_true (no edge) | departure_time_observed   departure_time_true (no edge) | departure_time_observed->departure_time_true | departure_time_observed->departure_time_true | departure_time_observed->departure_time_true | no edge | (departure_time_observed, departure_time_true)=A |
| attention_share_siren, hazard_approach_rate | attention_share_siren o-o hazard_approach_rate | attention_share_siren   hazard_approach_rate (no edge) | attention_share_siren   hazard_approach_rate (no edge) | attention_share_siren   hazard_approach_rate (no edge) | attention_share_siren   hazard_approach_rate (no edge) | hazard_approach_rate -> attention_share_siren | (attention_share_siren, hazard_approach_rate)=C |
| attention_share_siren, siren_audibility_index | attention_share_siren   siren_audibility_index (no edge) | attention_share_siren   siren_audibility_index (no edge) | attention_share_siren->siren_audibility_index | attention_share_siren->siren_audibility_index | attention_share_siren->siren_audibility_index | no edge | (attention_share_siren, siren_audibility_index)=A |
| attention_share_siren, readiness_time_since_t0 | attention_share_siren o-o readiness_time_since_t0 | attention_share_siren   readiness_time_since_t0 (no edge) | attention_share_siren   readiness_time_since_t0 (no edge) | attention_share_siren   readiness_time_since_t0 (no edge) | attention_share_siren   readiness_time_since_t0 (no edge) | readiness_time_since_t0 -> attention_share_siren | (attention_share_siren, readiness_time_since_t0)=C |
| baseline_risk_tolerance, mobility_needs_index | baseline_risk_tolerance   mobility_needs_index (no edge) | baseline_risk_tolerance   mobility_needs_index (no edge) | baseline_risk_tolerance->mobility_needs_index | baseline_risk_tolerance->mobility_needs_index | baseline_risk_tolerance->mobility_needs_index | no edge | (baseline_risk_tolerance, mobility_needs_index)=A |
| assistance_fleet_vehicles, vehicle_access | assistance_fleet_vehicles   vehicle_access (no edge) | assistance_fleet_vehicles   vehicle_access (no edge) | assistance_fleet_vehicles->vehicle_access | assistance_fleet_vehicles->vehicle_access | assistance_fleet_vehicles->vehicle_access | no edge | (assistance_fleet_vehicles, vehicle_access)=A |
| hazard_distance_at_t0, attention_share_sms | attention_share_sms o-> hazard_distance_at_t0 | hazard_distance_at_t0   attention_share_sms (no edge) | hazard_distance_at_t0   attention_share_sms (no edge) | hazard_distance_at_t0   attention_share_sms (no edge) | hazard_distance_at_t0   attention_share_sms (no edge) | attention_share_sms -> hazard_distance_at_t0 | (hazard_distance_at_t0, attention_share_sms)=C |
| hazard_distance_at_t0, congestion_index_at_decision | hazard_distance_at_t0 <-> congestion_index_at_decision | hazard_distance_at_t0   congestion_index_at_decision (no edge) | hazard_distance_at_t0   congestion_index_at_decision (no edge) | hazard_distance_at_t0   congestion_index_at_decision (no edge) | hazard_distance_at_t0   congestion_index_at_decision (no edge) | congestion_index_at_decision -> hazard_distance_at_t0 | (hazard_distance_at_t0, congestion_index_at_decision)=C |
| perceived_credibility_score, message_specificity_level | perceived_credibility_score   message_specificity_level (no edge) | perceived_credibility_score   message_specificity_level (no edge) | perceived_credibility_score->message_specificity_level | perceived_credibility_score->message_specificity_level | perceived_credibility_score->message_specificity_level | no edge | (perceived_credibility_score, message_specificity_level)=A |
| perceived_credibility_score, attention_share_news | perceived_credibility_score   attention_share_news (no edge) | perceived_credibility_score   attention_share_news (no edge) | perceived_credibility_score->attention_share_news | perceived_credibility_score->attention_share_news | perceived_credibility_score->attention_share_news | no edge | (perceived_credibility_score, attention_share_news)=A |
| attention_share_sms, sms_alert_enabled | attention_share_sms   sms_alert_enabled (no edge) | attention_share_sms   sms_alert_enabled (no edge) | attention_share_sms->sms_alert_enabled | attention_share_sms->sms_alert_enabled | attention_share_sms->sms_alert_enabled | no edge | (attention_share_sms, sms_alert_enabled)=A |
| attention_share_sms, pickup_eta_minutes | attention_share_sms o-> pickup_eta_minutes | attention_share_sms o-> pickup_eta_minutes | attention_share_sms   pickup_eta_minutes (no edge) | attention_share_sms   pickup_eta_minutes (no edge) | attention_share_sms   pickup_eta_minutes (no edge) | attention_share_sms -> pickup_eta_minutes | (attention_share_sms, pickup_eta_minutes)=C |
| congestion_index_at_decision, attention_share_news | congestion_index_at_decision <-> attention_share_news | congestion_index_at_decision   attention_share_news (no edge) | congestion_index_at_decision   attention_share_news (no edge) | congestion_index_at_decision   attention_share_news (no edge) | congestion_index_at_decision   attention_share_news (no edge) | no edge | (congestion_index_at_decision, attention_share_news)=D |
| congestion_index_at_decision, departure_time_true | congestion_index_at_decision   departure_time_true (no edge) | congestion_index_at_decision   departure_time_true (no edge) | congestion_index_at_decision->departure_time_true | congestion_index_at_decision->departure_time_true | congestion_index_at_decision->departure_time_true | no edge | (congestion_index_at_decision, departure_time_true)=A |
| congestion_index_at_decision, pickup_eta_minutes | congestion_index_at_decision   pickup_eta_minutes (no edge) | congestion_index_at_decision   pickup_eta_minutes (no edge) | congestion_index_at_decision->pickup_eta_minutes | congestion_index_at_decision->pickup_eta_minutes | congestion_index_at_decision->pickup_eta_minutes | no edge | (congestion_index_at_decision, pickup_eta_minutes)=A |
| congestion_index_at_decision, censor_indicator | congestion_index_at_decision->censor_indicator | congestion_index_at_decision->censor_indicator | congestion_index_at_decision   censor_indicator (no edge) | congestion_index_at_decision   censor_indicator (no edge) | congestion_index_at_decision   censor_indicator (no edge) | no edge | (congestion_index_at_decision, censor_indicator)=C |
| message_specificity_level, attention_share_news | message_specificity_level   attention_share_news (no edge) | message_specificity_level   attention_share_news (no edge) | message_specificity_level->attention_share_news | message_specificity_level->attention_share_news | message_specificity_level->attention_share_news | no edge | (message_specificity_level, attention_share_news)=A |
| message_specificity_level, pickup_eta_minutes | message_specificity_level o-> pickup_eta_minutes | message_specificity_level   pickup_eta_minutes (no edge) | message_specificity_level   pickup_eta_minutes (no edge) | message_specificity_level   pickup_eta_minutes (no edge) | message_specificity_level   pickup_eta_minutes (no edge) | pickup_eta_minutes -> message_specificity_level | (message_specificity_level, pickup_eta_minutes)=C |
| mobility_needs_index, pickup_eta_minutes | mobility_needs_index o-> pickup_eta_minutes | mobility_needs_index   pickup_eta_minutes (no edge) | mobility_needs_index   pickup_eta_minutes (no edge) | mobility_needs_index   pickup_eta_minutes (no edge) | mobility_needs_index   pickup_eta_minutes (no edge) | mobility_needs_index -> pickup_eta_minutes | (mobility_needs_index, pickup_eta_minutes)=C |
| mobility_needs_index, vehicle_access | mobility_needs_index   vehicle_access (no edge) | mobility_needs_index   vehicle_access (no edge) | mobility_needs_index->vehicle_access | mobility_needs_index->vehicle_access | mobility_needs_index->vehicle_access | no edge | (mobility_needs_index, vehicle_access)=A |
| attention_share_neighbors, attention_share_social | attention_share_neighbors   attention_share_social (no edge) | attention_share_neighbors   attention_share_social (no edge) | attention_share_neighbors->attention_share_social | attention_share_neighbors->attention_share_social | attention_share_neighbors->attention_share_social | no edge | (attention_share_neighbors, attention_share_social)=A |
| sms_alert_enabled, handset_reachable | sms_alert_enabled o-> handset_reachable | sms_alert_enabled   handset_reachable (no edge) | sms_alert_enabled   handset_reachable (no edge) | sms_alert_enabled   handset_reachable (no edge) | sms_alert_enabled   handset_reachable (no edge) | sms_alert_enabled -> handset_reachable | (sms_alert_enabled, handset_reachable)=C |
| attention_share_social, local_cumulative_departure_fraction | attention_share_social <-> local_cumulative_departure_fraction | attention_share_social   local_cumulative_departure_fraction (no edge) | attention_share_social   local_cumulative_departure_fraction (no edge) | attention_share_social   local_cumulative_departure_fraction (no edge) | attention_share_social   local_cumulative_departure_fraction (no edge) | attention_share_social -> local_cumulative_departure_fraction | (attention_share_social, local_cumulative_departure_fraction)=C |
| attention_share_social, attention_share_news | attention_share_social <-> attention_share_news | attention_share_social   attention_share_news (no edge) | attention_share_social->attention_share_news | attention_share_social->attention_share_news | attention_share_social->attention_share_news | attention_share_social -> attention_share_news | (attention_share_social, attention_share_news)=A |
| local_cumulative_departure_fraction, attention_share_news | local_cumulative_departure_fraction <-> attention_share_news | local_cumulative_departure_fraction   attention_share_news (no edge) | local_cumulative_departure_fraction   attention_share_news (no edge) | local_cumulative_departure_fraction   attention_share_news (no edge) | local_cumulative_departure_fraction   attention_share_news (no edge) | no edge | (local_cumulative_departure_fraction, attention_share_news)=C |
| local_cumulative_departure_fraction, departure_time_true | local_cumulative_departure_fraction   departure_time_true (no edge) | local_cumulative_departure_fraction   departure_time_true (no edge) | local_cumulative_departure_fraction->departure_time_true | local_cumulative_departure_fraction->departure_time_true | local_cumulative_departure_fraction->departure_time_true | no edge | (local_cumulative_departure_fraction, departure_time_true)=A |
| local_cumulative_departure_fraction, censor_indicator | censor_indicator o-> local_cumulative_departure_fraction | local_cumulative_departure_fraction   censor_indicator (no edge) | local_cumulative_departure_fraction   censor_indicator (no edge) | local_cumulative_departure_fraction   censor_indicator (no edge) | local_cumulative_departure_fraction   censor_indicator (no edge) | no edge | (local_cumulative_departure_fraction, censor_indicator)=C |
| hazard_approach_rate, attention_share_news | hazard_approach_rate   attention_share_news (no edge) | hazard_approach_rate   attention_share_news (no edge) | hazard_approach_rate->attention_share_news | hazard_approach_rate->attention_share_news | hazard_approach_rate->attention_share_news | no edge | (hazard_approach_rate, attention_share_news)=A |
| handset_reachable, departure_time_true | departure_time_true o-> handset_reachable | handset_reachable   departure_time_true (no edge) | handset_reachable   departure_time_true (no edge) | handset_reachable   departure_time_true (no edge) | handset_reachable   departure_time_true (no edge) | departure_time_true -> handset_reachable | (handset_reachable, departure_time_true)=C |
| handset_reachable, vehicle_access | vehicle_access->handset_reachable | vehicle_access->handset_reachable | handset_reachable->vehicle_access | handset_reachable->vehicle_access | handset_reachable->vehicle_access | vehicle_access -> handset_reachable | (handset_reachable, vehicle_access)=A |
| siren_audibility_index, pickup_eta_minutes | siren_audibility_index o-> pickup_eta_minutes | siren_audibility_index   pickup_eta_minutes (no edge) | siren_audibility_index   pickup_eta_minutes (no edge) | siren_audibility_index   pickup_eta_minutes (no edge) | siren_audibility_index   pickup_eta_minutes (no edge) | siren_audibility_index -> pickup_eta_minutes | (siren_audibility_index, pickup_eta_minutes)=C |
| departure_time_true, pickup_eta_minutes | departure_time_true   pickup_eta_minutes (no edge) | departure_time_true   pickup_eta_minutes (no edge) | departure_time_true->pickup_eta_minutes | departure_time_true->pickup_eta_minutes | departure_time_true->pickup_eta_minutes | no edge | (departure_time_true, pickup_eta_minutes)=A |
| departure_time_true, censor_indicator | departure_time_true   censor_indicator (no edge) | departure_time_true   censor_indicator (no edge) | departure_time_true->censor_indicator | departure_time_true->censor_indicator | departure_time_true->censor_indicator | no edge | (departure_time_true, censor_indicator)=A |
| pickup_eta_minutes, vehicle_access | pickup_eta_minutes <-> vehicle_access | pickup_eta_minutes   vehicle_access (no edge) | pickup_eta_minutes   vehicle_access (no edge) | pickup_eta_minutes   vehicle_access (no edge) | pickup_eta_minutes   vehicle_access (no edge) | pickup_eta_minutes -> vehicle_access | (pickup_eta_minutes, vehicle_access)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
