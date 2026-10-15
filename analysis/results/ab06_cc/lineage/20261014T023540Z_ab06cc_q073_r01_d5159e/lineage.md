# Edge lineage: 20261014T023540Z_ab06cc_q073_r01_d5159e

Dataset `/research/datasets/suite_q1s2/q073/q073.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 2}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 27 | 0.81 | 0.63 | 0.71 | 9 | 0 | 13 | 32 |
| S1 after bootstrap edits | 13 | 0.92 | 0.34 | 0.50 | 9 | 0 | 3 | 28 |
| S2 after LLM review | 48 | 0.21 | 0.29 | 0.24 | 6 | 4 | 0 | 68 |
| S3 after KCI pruning | 48 | 0.21 | 0.29 | 0.24 | 6 | 4 | 0 | 68 |
| S4 final (after cycle step) | 48 | 0.21 | 0.29 | 0.24 | 6 | 4 | 0 | 68 |

Scored against: reference graph s2_07_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 14. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 48, "C": 176, "D": 7}.
- LLM effect: added 42 (of which 37 where the resamples showed no edge at frequency >= 0.9), removed 7, re-oriented 3.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 48 edges; set by {"llm": 45, "algorithm (unchanged)": 3}; 3 identical to the algorithm's output; 39 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| attempted_trips_count->transit_vouchers_per_1000 | llm | no | 1.00 |
| true_ems_heat_incidents->neighborhood_heat_index | llm | no | 1.00 |
| true_ems_heat_incidents->alerts_delivered_rate | llm | yes | 0.00 |
| true_ems_heat_incidents->admitted_visits_count | llm | no | 1.00 |
| true_ems_heat_incidents->effective_awareness_rate | llm | yes | 0.80 |
| true_ems_heat_incidents->regional_heat_index_base | llm | no | 0.85 |
| true_ems_heat_incidents->adjusted_heat_dose_index | llm | no | 1.00 |
| true_ems_heat_incidents->observed_heat_calls | llm | no | 1.00 |
| tree_canopy_pct->neighborhood_heat_index | llm | no | 1.00 |
| tree_canopy_pct->effective_cooled_hours | llm | yes | 0.70 |
| tree_canopy_pct->regional_heat_index_base | llm | yes | 0.55 |
| tree_canopy_pct->adjusted_heat_dose_index | llm | no | 1.00 |
| language_mismatch_rate->social_isolation_rate | llm | no | 1.00 |
| language_mismatch_rate->alerts_delivered_rate | llm | no | 1.00 |
| turnaways_count->functional_capacity_day | llm | no | 0.95 |
| turnaways_count->hours_open | llm | no | 1.00 |
| indoor_time_above_safe_prop->admitted_visits_count | llm | no | 1.00 |
| indoor_time_above_safe_prop->adjusted_heat_dose_index | llm | no | 0.80 |
| indoor_time_above_safe_prop->observed_heat_calls | llm | no | 0.90 |
| neighborhood_heat_index->alerts_delivered_rate | llm | no | 0.95 |
| neighborhood_heat_index->admitted_visits_count | llm | no | 1.00 |
| neighborhood_heat_index->regional_heat_index_base | llm | no | 1.00 |
| neighborhood_heat_index->adjusted_heat_dose_index | llm | no | 1.00 |
| neighborhood_heat_index->observed_heat_calls | llm | no | 1.00 |
| transit_vouchers_per_1000->outdoor_work_share | algorithm (unchanged) | yes | 0.00 |
| social_isolation_rate->alerts_delivered_rate | llm | no | 0.90 |
| social_isolation_rate->admitted_visits_count | llm | yes | 0.05 |
| social_isolation_rate->effective_awareness_rate | llm | no | 1.00 |
| social_isolation_rate->observed_heat_calls | llm | no | 1.00 |
| alerts_delivered_rate->admitted_visits_count | llm | no | 1.00 |
| alerts_delivered_rate->effective_awareness_rate | llm | yes | 0.90 |
| alerts_delivered_rate->adjusted_heat_dose_index | llm | no | 1.00 |
| alerts_delivered_rate->observed_heat_calls | llm | no | 1.00 |
| outdoor_work_share->admitted_visits_count | llm | no | 1.00 |
| outdoor_work_share->observed_heat_calls | algorithm (unchanged) | yes | 0.00 |
| admitted_visits_count->observed_heat_calls | llm | no | 1.00 |
| effective_cooled_hours->hours_open | llm | no | 1.00 |
| effective_cooled_hours->adjusted_heat_dose_index | llm | no | 1.00 |
| effective_cooled_hours->observed_heat_calls | llm | no | 1.00 |
| effective_cooled_hours->ac_ownership_rate | llm | no | 1.00 |
| functional_capacity_day->hours_open | llm | no | 0.95 |
| effective_awareness_rate->observed_heat_calls | llm | no | 0.85 |
| hours_open->ac_ownership_rate | algorithm (unchanged) | yes | 0.00 |
| power_outage_rate->observed_heat_calls | llm | no | 0.95 |
| power_outage_rate->ac_ownership_rate | llm | no | 1.00 |
| regional_heat_index_base->adjusted_heat_dose_index | llm | no | 1.00 |
| regional_heat_index_base->observed_heat_calls | llm | no | 1.00 |
| adjusted_heat_dose_index->observed_heat_calls | llm | no | 0.90 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| attempted_trips_count, language_mismatch_rate | attempted_trips_count <-> language_mismatch_rate | attempted_trips_count   language_mismatch_rate (no edge) | attempted_trips_count   language_mismatch_rate (no edge) | attempted_trips_count   language_mismatch_rate (no edge) | attempted_trips_count   language_mismatch_rate (no edge) | language_mismatch_rate -> attempted_trips_count | (attempted_trips_count, language_mismatch_rate)=C |
| attempted_trips_count, transit_vouchers_per_1000 | attempted_trips_count   transit_vouchers_per_1000 (no edge) | attempted_trips_count   transit_vouchers_per_1000 (no edge) | attempted_trips_count->transit_vouchers_per_1000 | attempted_trips_count->transit_vouchers_per_1000 | attempted_trips_count->transit_vouchers_per_1000 | no edge | (attempted_trips_count, transit_vouchers_per_1000)=A |
| attempted_trips_count, adjusted_heat_dose_index | attempted_trips_count->adjusted_heat_dose_index | attempted_trips_count->adjusted_heat_dose_index | attempted_trips_count   adjusted_heat_dose_index (no edge) | attempted_trips_count   adjusted_heat_dose_index (no edge) | attempted_trips_count   adjusted_heat_dose_index (no edge) | attempted_trips_count -> adjusted_heat_dose_index | (attempted_trips_count, adjusted_heat_dose_index)=C |
| attempted_trips_count, observed_heat_calls | observed_heat_calls->attempted_trips_count | observed_heat_calls->attempted_trips_count | attempted_trips_count   observed_heat_calls (no edge) | attempted_trips_count   observed_heat_calls (no edge) | attempted_trips_count   observed_heat_calls (no edge) | observed_heat_calls -> attempted_trips_count | (attempted_trips_count, observed_heat_calls)=C |
| true_ems_heat_incidents, tree_canopy_pct | true_ems_heat_incidents->tree_canopy_pct | true_ems_heat_incidents->tree_canopy_pct | true_ems_heat_incidents   tree_canopy_pct (no edge) | true_ems_heat_incidents   tree_canopy_pct (no edge) | true_ems_heat_incidents   tree_canopy_pct (no edge) | true_ems_heat_incidents -> tree_canopy_pct | (true_ems_heat_incidents, tree_canopy_pct)=C |
| true_ems_heat_incidents, neighborhood_heat_index | true_ems_heat_incidents   neighborhood_heat_index (no edge) | true_ems_heat_incidents   neighborhood_heat_index (no edge) | true_ems_heat_incidents->neighborhood_heat_index | true_ems_heat_incidents->neighborhood_heat_index | true_ems_heat_incidents->neighborhood_heat_index | neighborhood_heat_index -> true_ems_heat_incidents | (true_ems_heat_incidents, neighborhood_heat_index)=A |
| true_ems_heat_incidents, alerts_delivered_rate | true_ems_heat_incidents ~~~ alerts_delivered_rate | true_ems_heat_incidents ~~~ alerts_delivered_rate | true_ems_heat_incidents->alerts_delivered_rate | true_ems_heat_incidents->alerts_delivered_rate | true_ems_heat_incidents->alerts_delivered_rate | true_ems_heat_incidents -> alerts_delivered_rate | (true_ems_heat_incidents, alerts_delivered_rate)=A |
| true_ems_heat_incidents, admitted_visits_count | true_ems_heat_incidents   admitted_visits_count (no edge) | true_ems_heat_incidents   admitted_visits_count (no edge) | true_ems_heat_incidents->admitted_visits_count | true_ems_heat_incidents->admitted_visits_count | true_ems_heat_incidents->admitted_visits_count | no edge | (true_ems_heat_incidents, admitted_visits_count)=A |
| true_ems_heat_incidents, distance_to_center_km | true_ems_heat_incidents <-> distance_to_center_km | true_ems_heat_incidents   distance_to_center_km (no edge) | true_ems_heat_incidents   distance_to_center_km (no edge) | true_ems_heat_incidents   distance_to_center_km (no edge) | true_ems_heat_incidents   distance_to_center_km (no edge) | distance_to_center_km -> true_ems_heat_incidents | (true_ems_heat_incidents, distance_to_center_km)=C |
| true_ems_heat_incidents, functional_capacity_day | true_ems_heat_incidents <-> functional_capacity_day | true_ems_heat_incidents   functional_capacity_day (no edge) | true_ems_heat_incidents   functional_capacity_day (no edge) | true_ems_heat_incidents   functional_capacity_day (no edge) | true_ems_heat_incidents   functional_capacity_day (no edge) | no edge | (true_ems_heat_incidents, functional_capacity_day)=C |
| true_ems_heat_incidents, effective_awareness_rate | effective_awareness_rate o-> true_ems_heat_incidents | true_ems_heat_incidents   effective_awareness_rate (no edge) | true_ems_heat_incidents->effective_awareness_rate | true_ems_heat_incidents->effective_awareness_rate | true_ems_heat_incidents->effective_awareness_rate | effective_awareness_rate -> true_ems_heat_incidents | (true_ems_heat_incidents, effective_awareness_rate)=A |
| true_ems_heat_incidents, regional_heat_index_base | true_ems_heat_incidents   regional_heat_index_base (no edge) | true_ems_heat_incidents   regional_heat_index_base (no edge) | true_ems_heat_incidents->regional_heat_index_base | true_ems_heat_incidents->regional_heat_index_base | true_ems_heat_incidents->regional_heat_index_base | regional_heat_index_base -> true_ems_heat_incidents | (true_ems_heat_incidents, regional_heat_index_base)=A |
| true_ems_heat_incidents, adjusted_heat_dose_index | true_ems_heat_incidents   adjusted_heat_dose_index (no edge) | true_ems_heat_incidents   adjusted_heat_dose_index (no edge) | true_ems_heat_incidents->adjusted_heat_dose_index | true_ems_heat_incidents->adjusted_heat_dose_index | true_ems_heat_incidents->adjusted_heat_dose_index | no edge | (true_ems_heat_incidents, adjusted_heat_dose_index)=A |
| true_ems_heat_incidents, observed_heat_calls | true_ems_heat_incidents   observed_heat_calls (no edge) | true_ems_heat_incidents   observed_heat_calls (no edge) | true_ems_heat_incidents->observed_heat_calls | true_ems_heat_incidents->observed_heat_calls | true_ems_heat_incidents->observed_heat_calls | no edge | (true_ems_heat_incidents, observed_heat_calls)=A |
| tree_canopy_pct, neighborhood_heat_index | tree_canopy_pct   neighborhood_heat_index (no edge) | tree_canopy_pct   neighborhood_heat_index (no edge) | tree_canopy_pct->neighborhood_heat_index | tree_canopy_pct->neighborhood_heat_index | tree_canopy_pct->neighborhood_heat_index | no edge | (tree_canopy_pct, neighborhood_heat_index)=A |
| tree_canopy_pct, alerts_delivered_rate | alerts_delivered_rate->tree_canopy_pct | alerts_delivered_rate->tree_canopy_pct | tree_canopy_pct   alerts_delivered_rate (no edge) | tree_canopy_pct   alerts_delivered_rate (no edge) | tree_canopy_pct   alerts_delivered_rate (no edge) | alerts_delivered_rate -> tree_canopy_pct | (tree_canopy_pct, alerts_delivered_rate)=C |
| tree_canopy_pct, effective_cooled_hours | effective_cooled_hours o-> tree_canopy_pct | effective_cooled_hours o-> tree_canopy_pct | tree_canopy_pct->effective_cooled_hours | tree_canopy_pct->effective_cooled_hours | tree_canopy_pct->effective_cooled_hours | effective_cooled_hours -> tree_canopy_pct | (tree_canopy_pct, effective_cooled_hours)=A |
| tree_canopy_pct, regional_heat_index_base | regional_heat_index_base o-> tree_canopy_pct | regional_heat_index_base o-> tree_canopy_pct | tree_canopy_pct->regional_heat_index_base | tree_canopy_pct->regional_heat_index_base | tree_canopy_pct->regional_heat_index_base | no edge | (tree_canopy_pct, regional_heat_index_base)=A |
| tree_canopy_pct, adjusted_heat_dose_index | tree_canopy_pct   adjusted_heat_dose_index (no edge) | tree_canopy_pct   adjusted_heat_dose_index (no edge) | tree_canopy_pct->adjusted_heat_dose_index | tree_canopy_pct->adjusted_heat_dose_index | tree_canopy_pct->adjusted_heat_dose_index | no edge | (tree_canopy_pct, adjusted_heat_dose_index)=A |
| language_mismatch_rate, social_isolation_rate | language_mismatch_rate   social_isolation_rate (no edge) | language_mismatch_rate   social_isolation_rate (no edge) | language_mismatch_rate->social_isolation_rate | language_mismatch_rate->social_isolation_rate | language_mismatch_rate->social_isolation_rate | no edge | (language_mismatch_rate, social_isolation_rate)=A |
| language_mismatch_rate, alerts_delivered_rate | language_mismatch_rate   alerts_delivered_rate (no edge) | language_mismatch_rate   alerts_delivered_rate (no edge) | language_mismatch_rate->alerts_delivered_rate | language_mismatch_rate->alerts_delivered_rate | language_mismatch_rate->alerts_delivered_rate | no edge | (language_mismatch_rate, alerts_delivered_rate)=A |
| language_mismatch_rate, distance_to_center_km | language_mismatch_rate <-> distance_to_center_km | language_mismatch_rate   distance_to_center_km (no edge) | language_mismatch_rate   distance_to_center_km (no edge) | language_mismatch_rate   distance_to_center_km (no edge) | language_mismatch_rate   distance_to_center_km (no edge) | language_mismatch_rate -> distance_to_center_km | (language_mismatch_rate, distance_to_center_km)=C |
| turnaways_count, functional_capacity_day | turnaways_count   functional_capacity_day (no edge) | turnaways_count   functional_capacity_day (no edge) | turnaways_count->functional_capacity_day | turnaways_count->functional_capacity_day | turnaways_count->functional_capacity_day | no edge | (turnaways_count, functional_capacity_day)=A |
| turnaways_count, hours_open | turnaways_count   hours_open (no edge) | turnaways_count   hours_open (no edge) | turnaways_count->hours_open | turnaways_count->hours_open | turnaways_count->hours_open | no edge | (turnaways_count, hours_open)=A |
| indoor_time_above_safe_prop, admitted_visits_count | indoor_time_above_safe_prop   admitted_visits_count (no edge) | indoor_time_above_safe_prop   admitted_visits_count (no edge) | indoor_time_above_safe_prop->admitted_visits_count | indoor_time_above_safe_prop->admitted_visits_count | indoor_time_above_safe_prop->admitted_visits_count | no edge | (indoor_time_above_safe_prop, admitted_visits_count)=A |
| indoor_time_above_safe_prop, adjusted_heat_dose_index | indoor_time_above_safe_prop   adjusted_heat_dose_index (no edge) | indoor_time_above_safe_prop   adjusted_heat_dose_index (no edge) | indoor_time_above_safe_prop->adjusted_heat_dose_index | indoor_time_above_safe_prop->adjusted_heat_dose_index | indoor_time_above_safe_prop->adjusted_heat_dose_index | no edge | (indoor_time_above_safe_prop, adjusted_heat_dose_index)=A |
| indoor_time_above_safe_prop, observed_heat_calls | indoor_time_above_safe_prop   observed_heat_calls (no edge) | indoor_time_above_safe_prop   observed_heat_calls (no edge) | indoor_time_above_safe_prop->observed_heat_calls | indoor_time_above_safe_prop->observed_heat_calls | indoor_time_above_safe_prop->observed_heat_calls | indoor_time_above_safe_prop -> observed_heat_calls | (indoor_time_above_safe_prop, observed_heat_calls)=A |
| neighborhood_heat_index, alerts_delivered_rate | neighborhood_heat_index   alerts_delivered_rate (no edge) | neighborhood_heat_index   alerts_delivered_rate (no edge) | neighborhood_heat_index->alerts_delivered_rate | neighborhood_heat_index->alerts_delivered_rate | neighborhood_heat_index->alerts_delivered_rate | no edge | (neighborhood_heat_index, alerts_delivered_rate)=A |
| neighborhood_heat_index, admitted_visits_count | neighborhood_heat_index   admitted_visits_count (no edge) | neighborhood_heat_index   admitted_visits_count (no edge) | neighborhood_heat_index->admitted_visits_count | neighborhood_heat_index->admitted_visits_count | neighborhood_heat_index->admitted_visits_count | no edge | (neighborhood_heat_index, admitted_visits_count)=A |
| neighborhood_heat_index, functional_capacity_day | neighborhood_heat_index o-> functional_capacity_day | neighborhood_heat_index   functional_capacity_day (no edge) | neighborhood_heat_index   functional_capacity_day (no edge) | neighborhood_heat_index   functional_capacity_day (no edge) | neighborhood_heat_index   functional_capacity_day (no edge) | no edge | (neighborhood_heat_index, functional_capacity_day)=C |
| neighborhood_heat_index, regional_heat_index_base | neighborhood_heat_index   regional_heat_index_base (no edge) | neighborhood_heat_index   regional_heat_index_base (no edge) | neighborhood_heat_index->regional_heat_index_base | neighborhood_heat_index->regional_heat_index_base | neighborhood_heat_index->regional_heat_index_base | no edge | (neighborhood_heat_index, regional_heat_index_base)=A |
| neighborhood_heat_index, adjusted_heat_dose_index | neighborhood_heat_index   adjusted_heat_dose_index (no edge) | neighborhood_heat_index   adjusted_heat_dose_index (no edge) | neighborhood_heat_index->adjusted_heat_dose_index | neighborhood_heat_index->adjusted_heat_dose_index | neighborhood_heat_index->adjusted_heat_dose_index | no edge | (neighborhood_heat_index, adjusted_heat_dose_index)=A |
| neighborhood_heat_index, observed_heat_calls | neighborhood_heat_index   observed_heat_calls (no edge) | neighborhood_heat_index   observed_heat_calls (no edge) | neighborhood_heat_index->observed_heat_calls | neighborhood_heat_index->observed_heat_calls | neighborhood_heat_index->observed_heat_calls | no edge | (neighborhood_heat_index, observed_heat_calls)=A |
| transit_vouchers_per_1000, hours_open | transit_vouchers_per_1000 o-o hours_open | transit_vouchers_per_1000   hours_open (no edge) | transit_vouchers_per_1000   hours_open (no edge) | transit_vouchers_per_1000   hours_open (no edge) | transit_vouchers_per_1000   hours_open (no edge) | hours_open -> transit_vouchers_per_1000 | (transit_vouchers_per_1000, hours_open)=C |
| social_isolation_rate, alerts_delivered_rate | social_isolation_rate   alerts_delivered_rate (no edge) | social_isolation_rate   alerts_delivered_rate (no edge) | social_isolation_rate->alerts_delivered_rate | social_isolation_rate->alerts_delivered_rate | social_isolation_rate->alerts_delivered_rate | no edge | (social_isolation_rate, alerts_delivered_rate)=A |
| social_isolation_rate, admitted_visits_count | social_isolation_rate o-> admitted_visits_count | social_isolation_rate   admitted_visits_count (no edge) | social_isolation_rate->admitted_visits_count | social_isolation_rate->admitted_visits_count | social_isolation_rate->admitted_visits_count | social_isolation_rate -> admitted_visits_count | (social_isolation_rate, admitted_visits_count)=A |
| social_isolation_rate, distance_to_center_km | social_isolation_rate->distance_to_center_km | social_isolation_rate->distance_to_center_km | social_isolation_rate   distance_to_center_km (no edge) | social_isolation_rate   distance_to_center_km (no edge) | social_isolation_rate   distance_to_center_km (no edge) | social_isolation_rate -> distance_to_center_km | (social_isolation_rate, distance_to_center_km)=C |
| social_isolation_rate, effective_awareness_rate | social_isolation_rate   effective_awareness_rate (no edge) | social_isolation_rate   effective_awareness_rate (no edge) | social_isolation_rate->effective_awareness_rate | social_isolation_rate->effective_awareness_rate | social_isolation_rate->effective_awareness_rate | no edge | (social_isolation_rate, effective_awareness_rate)=A |
| social_isolation_rate, observed_heat_calls | social_isolation_rate   observed_heat_calls (no edge) | social_isolation_rate   observed_heat_calls (no edge) | social_isolation_rate->observed_heat_calls | social_isolation_rate->observed_heat_calls | social_isolation_rate->observed_heat_calls | no edge | (social_isolation_rate, observed_heat_calls)=A |
| alerts_delivered_rate, admitted_visits_count | alerts_delivered_rate   admitted_visits_count (no edge) | alerts_delivered_rate   admitted_visits_count (no edge) | alerts_delivered_rate->admitted_visits_count | alerts_delivered_rate->admitted_visits_count | alerts_delivered_rate->admitted_visits_count | no edge | (alerts_delivered_rate, admitted_visits_count)=A |
| alerts_delivered_rate, distance_to_center_km | alerts_delivered_rate <-> distance_to_center_km | alerts_delivered_rate   distance_to_center_km (no edge) | alerts_delivered_rate   distance_to_center_km (no edge) | alerts_delivered_rate   distance_to_center_km (no edge) | alerts_delivered_rate   distance_to_center_km (no edge) | no edge | (alerts_delivered_rate, distance_to_center_km)=C |
| alerts_delivered_rate, functional_capacity_day | alerts_delivered_rate <-> functional_capacity_day | alerts_delivered_rate   functional_capacity_day (no edge) | alerts_delivered_rate   functional_capacity_day (no edge) | alerts_delivered_rate   functional_capacity_day (no edge) | alerts_delivered_rate   functional_capacity_day (no edge) | alerts_delivered_rate -> functional_capacity_day | (alerts_delivered_rate, functional_capacity_day)=C |
| alerts_delivered_rate, effective_awareness_rate | effective_awareness_rate o-> alerts_delivered_rate | alerts_delivered_rate   effective_awareness_rate (no edge) | alerts_delivered_rate->effective_awareness_rate | alerts_delivered_rate->effective_awareness_rate | alerts_delivered_rate->effective_awareness_rate | no edge | (alerts_delivered_rate, effective_awareness_rate)=A |
| alerts_delivered_rate, adjusted_heat_dose_index | alerts_delivered_rate   adjusted_heat_dose_index (no edge) | alerts_delivered_rate   adjusted_heat_dose_index (no edge) | alerts_delivered_rate->adjusted_heat_dose_index | alerts_delivered_rate->adjusted_heat_dose_index | alerts_delivered_rate->adjusted_heat_dose_index | no edge | (alerts_delivered_rate, adjusted_heat_dose_index)=A |
| alerts_delivered_rate, observed_heat_calls | alerts_delivered_rate   observed_heat_calls (no edge) | alerts_delivered_rate   observed_heat_calls (no edge) | alerts_delivered_rate->observed_heat_calls | alerts_delivered_rate->observed_heat_calls | alerts_delivered_rate->observed_heat_calls | no edge | (alerts_delivered_rate, observed_heat_calls)=A |
| outdoor_work_share, admitted_visits_count | outdoor_work_share   admitted_visits_count (no edge) | outdoor_work_share   admitted_visits_count (no edge) | outdoor_work_share->admitted_visits_count | outdoor_work_share->admitted_visits_count | outdoor_work_share->admitted_visits_count | no edge | (outdoor_work_share, admitted_visits_count)=A |
| outdoor_work_share, power_outage_rate | power_outage_rate o-> outdoor_work_share | outdoor_work_share   power_outage_rate (no edge) | outdoor_work_share   power_outage_rate (no edge) | outdoor_work_share   power_outage_rate (no edge) | outdoor_work_share   power_outage_rate (no edge) | power_outage_rate -> outdoor_work_share | (outdoor_work_share, power_outage_rate)=C |
| outdoor_work_share, ac_ownership_rate | outdoor_work_share <-> ac_ownership_rate | outdoor_work_share   ac_ownership_rate (no edge) | outdoor_work_share   ac_ownership_rate (no edge) | outdoor_work_share   ac_ownership_rate (no edge) | outdoor_work_share   ac_ownership_rate (no edge) | ac_ownership_rate -> outdoor_work_share | (outdoor_work_share, ac_ownership_rate)=C |
| admitted_visits_count, distance_to_center_km | admitted_visits_count->distance_to_center_km | admitted_visits_count->distance_to_center_km | admitted_visits_count   distance_to_center_km (no edge) | admitted_visits_count   distance_to_center_km (no edge) | admitted_visits_count   distance_to_center_km (no edge) | admitted_visits_count -> distance_to_center_km | (admitted_visits_count, distance_to_center_km)=C |
| admitted_visits_count, observed_heat_calls | admitted_visits_count   observed_heat_calls (no edge) | admitted_visits_count   observed_heat_calls (no edge) | admitted_visits_count->observed_heat_calls | admitted_visits_count->observed_heat_calls | admitted_visits_count->observed_heat_calls | no edge | (admitted_visits_count, observed_heat_calls)=A |
| admitted_visits_count, ac_ownership_rate | admitted_visits_count <-> ac_ownership_rate | admitted_visits_count <-> ac_ownership_rate | admitted_visits_count   ac_ownership_rate (no edge) | admitted_visits_count   ac_ownership_rate (no edge) | admitted_visits_count   ac_ownership_rate (no edge) | ac_ownership_rate -> admitted_visits_count | (admitted_visits_count, ac_ownership_rate)=C |
| effective_cooled_hours, hours_open | effective_cooled_hours   hours_open (no edge) | effective_cooled_hours   hours_open (no edge) | effective_cooled_hours->hours_open | effective_cooled_hours->hours_open | effective_cooled_hours->hours_open | no edge | (effective_cooled_hours, hours_open)=A |
| effective_cooled_hours, regional_heat_index_base | effective_cooled_hours ~~~ regional_heat_index_base | effective_cooled_hours   regional_heat_index_base (no edge) | effective_cooled_hours   regional_heat_index_base (no edge) | effective_cooled_hours   regional_heat_index_base (no edge) | effective_cooled_hours   regional_heat_index_base (no edge) | regional_heat_index_base -> effective_cooled_hours | (effective_cooled_hours, regional_heat_index_base)=C |
| effective_cooled_hours, adjusted_heat_dose_index | effective_cooled_hours   adjusted_heat_dose_index (no edge) | effective_cooled_hours   adjusted_heat_dose_index (no edge) | effective_cooled_hours->adjusted_heat_dose_index | effective_cooled_hours->adjusted_heat_dose_index | effective_cooled_hours->adjusted_heat_dose_index | no edge | (effective_cooled_hours, adjusted_heat_dose_index)=A |
| effective_cooled_hours, observed_heat_calls | effective_cooled_hours   observed_heat_calls (no edge) | effective_cooled_hours   observed_heat_calls (no edge) | effective_cooled_hours->observed_heat_calls | effective_cooled_hours->observed_heat_calls | effective_cooled_hours->observed_heat_calls | no edge | (effective_cooled_hours, observed_heat_calls)=A |
| effective_cooled_hours, ac_ownership_rate | effective_cooled_hours   ac_ownership_rate (no edge) | effective_cooled_hours   ac_ownership_rate (no edge) | effective_cooled_hours->ac_ownership_rate | effective_cooled_hours->ac_ownership_rate | effective_cooled_hours->ac_ownership_rate | no edge | (effective_cooled_hours, ac_ownership_rate)=A |
| functional_capacity_day, hours_open | functional_capacity_day   hours_open (no edge) | functional_capacity_day   hours_open (no edge) | functional_capacity_day->hours_open | functional_capacity_day->hours_open | functional_capacity_day->hours_open | no edge | (functional_capacity_day, hours_open)=A |
| effective_awareness_rate, observed_heat_calls | effective_awareness_rate   observed_heat_calls (no edge) | effective_awareness_rate   observed_heat_calls (no edge) | effective_awareness_rate->observed_heat_calls | effective_awareness_rate->observed_heat_calls | effective_awareness_rate->observed_heat_calls | no edge | (effective_awareness_rate, observed_heat_calls)=A |
| power_outage_rate, observed_heat_calls | power_outage_rate   observed_heat_calls (no edge) | power_outage_rate   observed_heat_calls (no edge) | power_outage_rate->observed_heat_calls | power_outage_rate->observed_heat_calls | power_outage_rate->observed_heat_calls | no edge | (power_outage_rate, observed_heat_calls)=A |
| power_outage_rate, ac_ownership_rate | power_outage_rate   ac_ownership_rate (no edge) | power_outage_rate   ac_ownership_rate (no edge) | power_outage_rate->ac_ownership_rate | power_outage_rate->ac_ownership_rate | power_outage_rate->ac_ownership_rate | no edge | (power_outage_rate, ac_ownership_rate)=A |
| regional_heat_index_base, adjusted_heat_dose_index | regional_heat_index_base   adjusted_heat_dose_index (no edge) | regional_heat_index_base   adjusted_heat_dose_index (no edge) | regional_heat_index_base->adjusted_heat_dose_index | regional_heat_index_base->adjusted_heat_dose_index | regional_heat_index_base->adjusted_heat_dose_index | no edge | (regional_heat_index_base, adjusted_heat_dose_index)=A |
| regional_heat_index_base, observed_heat_calls | regional_heat_index_base   observed_heat_calls (no edge) | regional_heat_index_base   observed_heat_calls (no edge) | regional_heat_index_base->observed_heat_calls | regional_heat_index_base->observed_heat_calls | regional_heat_index_base->observed_heat_calls | no edge | (regional_heat_index_base, observed_heat_calls)=A |
| adjusted_heat_dose_index, observed_heat_calls | adjusted_heat_dose_index   observed_heat_calls (no edge) | adjusted_heat_dose_index   observed_heat_calls (no edge) | adjusted_heat_dose_index->observed_heat_calls | adjusted_heat_dose_index->observed_heat_calls | adjusted_heat_dose_index->observed_heat_calls | no edge | (adjusted_heat_dose_index, observed_heat_calls)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
