# Edge lineage: 20261011T223000Z_s2_q073_r01_1de2c9

Dataset `/research/datasets/suite_q1s2/q073/q073.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 27 | 0.78 | 0.60 | 0.68 | 8 | 0 | 13 | 34 |
| S1 after bootstrap edits | 8 | 1.00 | 0.23 | 0.37 | 6 | 0 | 2 | 30 |
| S2 after LLM review | 20 | 0.25 | 0.14 | 0.18 | 3 | 0 | 2 | 47 |
| S3 after KCI pruning | 17 | 0.29 | 0.14 | 0.19 | 3 | 0 | 2 | 44 |
| S4 final (after cycle step) | 17 | 0.29 | 0.14 | 0.19 | 3 | 0 | 2 | 44 |

Scored against: reference graph s2_07_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 19. Of the deleted, 7 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 14, "B": 4, "C": 78, "D": 135}.
- LLM effect: added 15 (of which 14 where the resamples showed no edge at frequency >= 0.9), removed 3, re-oriented 0.
- KCI step removed 3. Cycle step changed 0.
- Final graph: 17 edges; set by {"algorithm (unchanged)": 5, "llm": 12}; 5 identical to the algorithm's output; 11 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| attempted_trips_count->adjusted_heat_dose_index | algorithm (unchanged) | yes | 0.00 |
| observed_heat_calls->attempted_trips_count | algorithm (unchanged) | yes | 0.00 |
| tree_canopy_pct->neighborhood_heat_index | llm | no | 1.00 |
| effective_cooled_hours o-> tree_canopy_pct | algorithm (unchanged) | yes | 0.80 |
| language_mismatch_rate->turnaways_count | llm | no | 0.95 |
| language_mismatch_rate->social_isolation_rate | llm | no | 1.00 |
| language_mismatch_rate->alerts_delivered_rate | llm | no | 0.90 |
| language_mismatch_rate->effective_awareness_rate | llm | no | 1.00 |
| neighborhood_heat_index->regional_heat_index_base | llm | no | 1.00 |
| neighborhood_heat_index->adjusted_heat_dose_index | llm | no | 0.95 |
| neighborhood_heat_index->observed_heat_calls | llm | no | 0.95 |
| social_isolation_rate->observed_heat_calls | llm | no | 1.00 |
| alerts_delivered_rate->effective_awareness_rate | llm | yes | 0.85 |
| outdoor_work_share->adjusted_heat_dose_index | llm | no | 1.00 |
| outdoor_work_share->observed_heat_calls | algorithm (unchanged) | yes | 0.00 |
| admitted_visits_count <-> ac_ownership_rate | algorithm (unchanged) | yes | 0.05 |
| power_outage_rate->observed_heat_calls | llm | no | 0.95 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| true_ems_heat_incidents, tree_canopy_pct | true_ems_heat_incidents->tree_canopy_pct | true_ems_heat_incidents   tree_canopy_pct (no edge) | true_ems_heat_incidents   tree_canopy_pct (no edge) | true_ems_heat_incidents   tree_canopy_pct (no edge) | true_ems_heat_incidents   tree_canopy_pct (no edge) | true_ems_heat_incidents -> tree_canopy_pct | (true_ems_heat_incidents, tree_canopy_pct)=D |
| true_ems_heat_incidents, alerts_delivered_rate | true_ems_heat_incidents ~~~ alerts_delivered_rate | true_ems_heat_incidents   alerts_delivered_rate (no edge) | true_ems_heat_incidents   alerts_delivered_rate (no edge) | true_ems_heat_incidents   alerts_delivered_rate (no edge) | true_ems_heat_incidents   alerts_delivered_rate (no edge) | true_ems_heat_incidents -> alerts_delivered_rate | (true_ems_heat_incidents, alerts_delivered_rate)=D |
| true_ems_heat_incidents, distance_to_center_km | true_ems_heat_incidents <-> distance_to_center_km | true_ems_heat_incidents   distance_to_center_km (no edge) | true_ems_heat_incidents   distance_to_center_km (no edge) | true_ems_heat_incidents   distance_to_center_km (no edge) | true_ems_heat_incidents   distance_to_center_km (no edge) | distance_to_center_km -> true_ems_heat_incidents | (true_ems_heat_incidents, distance_to_center_km)=D |
| true_ems_heat_incidents, functional_capacity_day | functional_capacity_day o-> true_ems_heat_incidents | true_ems_heat_incidents   functional_capacity_day (no edge) | true_ems_heat_incidents   functional_capacity_day (no edge) | true_ems_heat_incidents   functional_capacity_day (no edge) | true_ems_heat_incidents   functional_capacity_day (no edge) | no edge | (true_ems_heat_incidents, functional_capacity_day)=D |
| true_ems_heat_incidents, effective_awareness_rate | effective_awareness_rate o-> true_ems_heat_incidents | true_ems_heat_incidents   effective_awareness_rate (no edge) | true_ems_heat_incidents   effective_awareness_rate (no edge) | true_ems_heat_incidents   effective_awareness_rate (no edge) | true_ems_heat_incidents   effective_awareness_rate (no edge) | effective_awareness_rate -> true_ems_heat_incidents | (true_ems_heat_incidents, effective_awareness_rate)=D |
| tree_canopy_pct, neighborhood_heat_index | tree_canopy_pct   neighborhood_heat_index (no edge) | tree_canopy_pct   neighborhood_heat_index (no edge) | tree_canopy_pct->neighborhood_heat_index | tree_canopy_pct->neighborhood_heat_index | tree_canopy_pct->neighborhood_heat_index | no edge | (tree_canopy_pct, neighborhood_heat_index)=A |
| tree_canopy_pct, alerts_delivered_rate | alerts_delivered_rate->tree_canopy_pct | tree_canopy_pct   alerts_delivered_rate (no edge) | tree_canopy_pct   alerts_delivered_rate (no edge) | tree_canopy_pct   alerts_delivered_rate (no edge) | tree_canopy_pct   alerts_delivered_rate (no edge) | alerts_delivered_rate -> tree_canopy_pct | (tree_canopy_pct, alerts_delivered_rate)=D |
| tree_canopy_pct, regional_heat_index_base | regional_heat_index_base o-> tree_canopy_pct | tree_canopy_pct   regional_heat_index_base (no edge) | tree_canopy_pct   regional_heat_index_base (no edge) | tree_canopy_pct   regional_heat_index_base (no edge) | tree_canopy_pct   regional_heat_index_base (no edge) | no edge | (tree_canopy_pct, regional_heat_index_base)=D |
| language_mismatch_rate, turnaways_count | language_mismatch_rate   turnaways_count (no edge) | language_mismatch_rate   turnaways_count (no edge) | language_mismatch_rate->turnaways_count | language_mismatch_rate->turnaways_count | language_mismatch_rate->turnaways_count | no edge | (language_mismatch_rate, turnaways_count)=A |
| language_mismatch_rate, social_isolation_rate | language_mismatch_rate   social_isolation_rate (no edge) | language_mismatch_rate   social_isolation_rate (no edge) | language_mismatch_rate->social_isolation_rate | language_mismatch_rate->social_isolation_rate | language_mismatch_rate->social_isolation_rate | no edge | (language_mismatch_rate, social_isolation_rate)=A |
| language_mismatch_rate, alerts_delivered_rate | language_mismatch_rate   alerts_delivered_rate (no edge) | language_mismatch_rate   alerts_delivered_rate (no edge) | language_mismatch_rate->alerts_delivered_rate | language_mismatch_rate->alerts_delivered_rate | language_mismatch_rate->alerts_delivered_rate | no edge | (language_mismatch_rate, alerts_delivered_rate)=A |
| language_mismatch_rate, distance_to_center_km | language_mismatch_rate o-> distance_to_center_km | language_mismatch_rate   distance_to_center_km (no edge) | language_mismatch_rate   distance_to_center_km (no edge) | language_mismatch_rate   distance_to_center_km (no edge) | language_mismatch_rate   distance_to_center_km (no edge) | language_mismatch_rate -> distance_to_center_km | (language_mismatch_rate, distance_to_center_km)=C |
| language_mismatch_rate, effective_awareness_rate | language_mismatch_rate   effective_awareness_rate (no edge) | language_mismatch_rate   effective_awareness_rate (no edge) | language_mismatch_rate->effective_awareness_rate | language_mismatch_rate->effective_awareness_rate | language_mismatch_rate->effective_awareness_rate | no edge | (language_mismatch_rate, effective_awareness_rate)=A |
| turnaways_count, ac_ownership_rate | turnaways_count o-> ac_ownership_rate | turnaways_count   ac_ownership_rate (no edge) | turnaways_count   ac_ownership_rate (no edge) | turnaways_count   ac_ownership_rate (no edge) | turnaways_count   ac_ownership_rate (no edge) | no edge | (turnaways_count, ac_ownership_rate)=D |
| indoor_time_above_safe_prop, effective_cooled_hours | indoor_time_above_safe_prop   effective_cooled_hours (no edge) | indoor_time_above_safe_prop   effective_cooled_hours (no edge) | effective_cooled_hours->indoor_time_above_safe_prop | indoor_time_above_safe_prop   effective_cooled_hours (no edge) | indoor_time_above_safe_prop   effective_cooled_hours (no edge) | no edge | (indoor_time_above_safe_prop, effective_cooled_hours)=B |
| indoor_time_above_safe_prop, power_outage_rate | indoor_time_above_safe_prop   power_outage_rate (no edge) | indoor_time_above_safe_prop   power_outage_rate (no edge) | power_outage_rate->indoor_time_above_safe_prop | indoor_time_above_safe_prop   power_outage_rate (no edge) | indoor_time_above_safe_prop   power_outage_rate (no edge) | no edge | (indoor_time_above_safe_prop, power_outage_rate)=B |
| indoor_time_above_safe_prop, ac_ownership_rate | indoor_time_above_safe_prop   ac_ownership_rate (no edge) | indoor_time_above_safe_prop   ac_ownership_rate (no edge) | ac_ownership_rate->indoor_time_above_safe_prop | indoor_time_above_safe_prop   ac_ownership_rate (no edge) | indoor_time_above_safe_prop   ac_ownership_rate (no edge) | no edge | (indoor_time_above_safe_prop, ac_ownership_rate)=B |
| neighborhood_heat_index, regional_heat_index_base | neighborhood_heat_index   regional_heat_index_base (no edge) | neighborhood_heat_index   regional_heat_index_base (no edge) | neighborhood_heat_index->regional_heat_index_base | neighborhood_heat_index->regional_heat_index_base | neighborhood_heat_index->regional_heat_index_base | no edge | (neighborhood_heat_index, regional_heat_index_base)=A |
| neighborhood_heat_index, adjusted_heat_dose_index | neighborhood_heat_index   adjusted_heat_dose_index (no edge) | neighborhood_heat_index   adjusted_heat_dose_index (no edge) | neighborhood_heat_index->adjusted_heat_dose_index | neighborhood_heat_index->adjusted_heat_dose_index | neighborhood_heat_index->adjusted_heat_dose_index | no edge | (neighborhood_heat_index, adjusted_heat_dose_index)=A |
| neighborhood_heat_index, observed_heat_calls | neighborhood_heat_index   observed_heat_calls (no edge) | neighborhood_heat_index   observed_heat_calls (no edge) | neighborhood_heat_index->observed_heat_calls | neighborhood_heat_index->observed_heat_calls | neighborhood_heat_index->observed_heat_calls | no edge | (neighborhood_heat_index, observed_heat_calls)=A |
| transit_vouchers_per_1000, outdoor_work_share | transit_vouchers_per_1000->outdoor_work_share | transit_vouchers_per_1000->outdoor_work_share | transit_vouchers_per_1000   outdoor_work_share (no edge) | transit_vouchers_per_1000   outdoor_work_share (no edge) | transit_vouchers_per_1000   outdoor_work_share (no edge) | transit_vouchers_per_1000 -> outdoor_work_share | (transit_vouchers_per_1000, outdoor_work_share)=C |
| transit_vouchers_per_1000, hours_open | transit_vouchers_per_1000 o-o hours_open | transit_vouchers_per_1000   hours_open (no edge) | transit_vouchers_per_1000   hours_open (no edge) | transit_vouchers_per_1000   hours_open (no edge) | transit_vouchers_per_1000   hours_open (no edge) | hours_open -> transit_vouchers_per_1000 | (transit_vouchers_per_1000, hours_open)=D |
| social_isolation_rate, admitted_visits_count | social_isolation_rate <-> admitted_visits_count | social_isolation_rate   admitted_visits_count (no edge) | social_isolation_rate   admitted_visits_count (no edge) | social_isolation_rate   admitted_visits_count (no edge) | social_isolation_rate   admitted_visits_count (no edge) | social_isolation_rate -> admitted_visits_count | (social_isolation_rate, admitted_visits_count)=D |
| social_isolation_rate, distance_to_center_km | social_isolation_rate <-> distance_to_center_km | social_isolation_rate   distance_to_center_km (no edge) | social_isolation_rate   distance_to_center_km (no edge) | social_isolation_rate   distance_to_center_km (no edge) | social_isolation_rate   distance_to_center_km (no edge) | social_isolation_rate -> distance_to_center_km | (social_isolation_rate, distance_to_center_km)=C |
| social_isolation_rate, adjusted_heat_dose_index | social_isolation_rate <-> adjusted_heat_dose_index | social_isolation_rate   adjusted_heat_dose_index (no edge) | social_isolation_rate   adjusted_heat_dose_index (no edge) | social_isolation_rate   adjusted_heat_dose_index (no edge) | social_isolation_rate   adjusted_heat_dose_index (no edge) | no edge | (social_isolation_rate, adjusted_heat_dose_index)=D |
| social_isolation_rate, observed_heat_calls | social_isolation_rate   observed_heat_calls (no edge) | social_isolation_rate   observed_heat_calls (no edge) | social_isolation_rate->observed_heat_calls | social_isolation_rate->observed_heat_calls | social_isolation_rate->observed_heat_calls | no edge | (social_isolation_rate, observed_heat_calls)=A |
| alerts_delivered_rate, distance_to_center_km | alerts_delivered_rate <-> distance_to_center_km | alerts_delivered_rate   distance_to_center_km (no edge) | alerts_delivered_rate   distance_to_center_km (no edge) | alerts_delivered_rate   distance_to_center_km (no edge) | alerts_delivered_rate   distance_to_center_km (no edge) | no edge | (alerts_delivered_rate, distance_to_center_km)=C |
| alerts_delivered_rate, functional_capacity_day | functional_capacity_day o-> alerts_delivered_rate | alerts_delivered_rate   functional_capacity_day (no edge) | alerts_delivered_rate   functional_capacity_day (no edge) | alerts_delivered_rate   functional_capacity_day (no edge) | alerts_delivered_rate   functional_capacity_day (no edge) | alerts_delivered_rate -> functional_capacity_day | (alerts_delivered_rate, functional_capacity_day)=C |
| alerts_delivered_rate, effective_awareness_rate | effective_awareness_rate o-> alerts_delivered_rate | alerts_delivered_rate   effective_awareness_rate (no edge) | alerts_delivered_rate->effective_awareness_rate | alerts_delivered_rate->effective_awareness_rate | alerts_delivered_rate->effective_awareness_rate | no edge | (alerts_delivered_rate, effective_awareness_rate)=A |
| outdoor_work_share, power_outage_rate | power_outage_rate o-> outdoor_work_share | outdoor_work_share   power_outage_rate (no edge) | outdoor_work_share   power_outage_rate (no edge) | outdoor_work_share   power_outage_rate (no edge) | outdoor_work_share   power_outage_rate (no edge) | power_outage_rate -> outdoor_work_share | (outdoor_work_share, power_outage_rate)=C |
| outdoor_work_share, adjusted_heat_dose_index | outdoor_work_share   adjusted_heat_dose_index (no edge) | outdoor_work_share   adjusted_heat_dose_index (no edge) | outdoor_work_share->adjusted_heat_dose_index | outdoor_work_share->adjusted_heat_dose_index | outdoor_work_share->adjusted_heat_dose_index | no edge | (outdoor_work_share, adjusted_heat_dose_index)=A |
| outdoor_work_share, ac_ownership_rate | outdoor_work_share <-> ac_ownership_rate | outdoor_work_share   ac_ownership_rate (no edge) | outdoor_work_share   ac_ownership_rate (no edge) | outdoor_work_share   ac_ownership_rate (no edge) | outdoor_work_share   ac_ownership_rate (no edge) | ac_ownership_rate -> outdoor_work_share | (outdoor_work_share, ac_ownership_rate)=C |
| admitted_visits_count, distance_to_center_km | admitted_visits_count->distance_to_center_km | admitted_visits_count->distance_to_center_km | admitted_visits_count   distance_to_center_km (no edge) | admitted_visits_count   distance_to_center_km (no edge) | admitted_visits_count   distance_to_center_km (no edge) | admitted_visits_count -> distance_to_center_km | (admitted_visits_count, distance_to_center_km)=C |
| effective_cooled_hours, regional_heat_index_base | effective_cooled_hours ~~~ regional_heat_index_base | effective_cooled_hours   regional_heat_index_base (no edge) | effective_cooled_hours   regional_heat_index_base (no edge) | effective_cooled_hours   regional_heat_index_base (no edge) | effective_cooled_hours   regional_heat_index_base (no edge) | regional_heat_index_base -> effective_cooled_hours | (effective_cooled_hours, regional_heat_index_base)=C |
| hours_open, ac_ownership_rate | hours_open->ac_ownership_rate | hours_open->ac_ownership_rate | hours_open   ac_ownership_rate (no edge) | hours_open   ac_ownership_rate (no edge) | hours_open   ac_ownership_rate (no edge) | hours_open -> ac_ownership_rate | (hours_open, ac_ownership_rate)=C |
| power_outage_rate, observed_heat_calls | power_outage_rate   observed_heat_calls (no edge) | power_outage_rate   observed_heat_calls (no edge) | power_outage_rate->observed_heat_calls | power_outage_rate->observed_heat_calls | power_outage_rate->observed_heat_calls | no edge | (power_outage_rate, observed_heat_calls)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
