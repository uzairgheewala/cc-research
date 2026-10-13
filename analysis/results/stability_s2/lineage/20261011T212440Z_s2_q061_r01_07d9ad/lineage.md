# Edge lineage: 20261011T212440Z_s2_q061_r01_07d9ad

Dataset `/research/datasets/suite_q1s2/q061/q061.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 19 | 0.79 | 0.32 | 0.45 | 3 | 0 | 12 | 49 |
| S1 after bootstrap edits | 5 | 0.80 | 0.09 | 0.15 | 3 | 0 | 1 | 46 |
| S2 after LLM review | 19 | 0.47 | 0.19 | 0.27 | 5 | 3 | 1 | 52 |
| S3 after KCI pruning | 19 | 0.47 | 0.19 | 0.27 | 5 | 3 | 1 | 52 |
| S4 final (after cycle step) | 19 | 0.47 | 0.19 | 0.27 | 5 | 3 | 1 | 52 |

Scored against: reference graph s2_06_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 14. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 16, "C": 90, "D": 194}.
- LLM effect: added 15 (of which 11 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 19 edges; set by {"llm": 15, "algorithm (unchanged)": 4}; 4 identical to the algorithm's output; 11 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| incident_error_rate->failover_latency_seconds | llm | no | 1.00 |
| incident_error_rate->observed_incident_error_rate | llm | yes | 0.05 |
| incident_error_rate->primary_pop_outage | llm | yes | 0.90 |
| incident_error_rate->detection_delay_seconds | llm | no | 0.90 |
| incident_error_rate->observed_failover_latency_seconds | llm | no | 1.00 |
| nearest_backup_capacity_rps->failover_latency_seconds | llm | no | 1.00 |
| nearest_backup_capacity_rps->selected_backup_pop | llm | no | 1.00 |
| nearest_backup_capacity_rps->observed_failover_latency_seconds | llm | no | 1.00 |
| resolver_ttl_floor_seconds o-o resolver_class | algorithm (unchanged) | yes | 0.00 |
| resolver_ttl_floor_seconds o-> cohort_request_rate_qps | algorithm (unchanged) | yes | 0.60 |
| serve_stale_enabled->stale_hit_probability_at_outage | llm | no | 1.00 |
| resolver_class->cohort_request_rate_qps | algorithm (unchanged) | yes | 0.00 |
| time_to_95p_adoption_seconds->failover_latency_seconds | algorithm (unchanged) | yes | 0.50 |
| failover_latency_seconds->observed_failover_latency_seconds | llm | yes | 0.00 |
| selected_backup_pop->primary_pop_outage | llm | no | 1.00 |
| selected_backup_pop->observed_failover_latency_seconds | llm | no | 1.00 |
| observed_incident_error_rate->primary_pop_outage | llm | no | 0.50 |
| primary_pop_outage->observed_failover_latency_seconds | llm | no | 0.95 |
| detection_delay_seconds->health_check_interval_seconds | llm | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| incident_error_rate, failover_latency_seconds | incident_error_rate   failover_latency_seconds (no edge) | incident_error_rate   failover_latency_seconds (no edge) | incident_error_rate->failover_latency_seconds | incident_error_rate->failover_latency_seconds | incident_error_rate->failover_latency_seconds | no edge | (incident_error_rate, failover_latency_seconds)=A |
| incident_error_rate, observed_incident_error_rate | incident_error_rate ~~~ observed_incident_error_rate | incident_error_rate   observed_incident_error_rate (no edge) | incident_error_rate->observed_incident_error_rate | incident_error_rate->observed_incident_error_rate | incident_error_rate->observed_incident_error_rate | incident_error_rate -> observed_incident_error_rate | (incident_error_rate, observed_incident_error_rate)=A |
| incident_error_rate, primary_pop_outage | incident_error_rate ~~~ primary_pop_outage | incident_error_rate   primary_pop_outage (no edge) | incident_error_rate->primary_pop_outage | incident_error_rate->primary_pop_outage | incident_error_rate->primary_pop_outage | primary_pop_outage -> incident_error_rate | (incident_error_rate, primary_pop_outage)=A |
| incident_error_rate, detection_delay_seconds | incident_error_rate   detection_delay_seconds (no edge) | incident_error_rate   detection_delay_seconds (no edge) | incident_error_rate->detection_delay_seconds | incident_error_rate->detection_delay_seconds | incident_error_rate->detection_delay_seconds | detection_delay_seconds -> incident_error_rate | (incident_error_rate, detection_delay_seconds)=A |
| incident_error_rate, observed_failover_latency_seconds | incident_error_rate   observed_failover_latency_seconds (no edge) | incident_error_rate   observed_failover_latency_seconds (no edge) | incident_error_rate->observed_failover_latency_seconds | incident_error_rate->observed_failover_latency_seconds | incident_error_rate->observed_failover_latency_seconds | no edge | (incident_error_rate, observed_failover_latency_seconds)=A |
| nearest_backup_capacity_rps, failover_latency_seconds | nearest_backup_capacity_rps   failover_latency_seconds (no edge) | nearest_backup_capacity_rps   failover_latency_seconds (no edge) | nearest_backup_capacity_rps->failover_latency_seconds | nearest_backup_capacity_rps->failover_latency_seconds | nearest_backup_capacity_rps->failover_latency_seconds | no edge | (nearest_backup_capacity_rps, failover_latency_seconds)=A |
| nearest_backup_capacity_rps, selected_backup_pop | nearest_backup_capacity_rps   selected_backup_pop (no edge) | nearest_backup_capacity_rps   selected_backup_pop (no edge) | nearest_backup_capacity_rps->selected_backup_pop | nearest_backup_capacity_rps->selected_backup_pop | nearest_backup_capacity_rps->selected_backup_pop | nearest_backup_capacity_rps -> selected_backup_pop | (nearest_backup_capacity_rps, selected_backup_pop)=A |
| nearest_backup_capacity_rps, observed_failover_latency_seconds | nearest_backup_capacity_rps   observed_failover_latency_seconds (no edge) | nearest_backup_capacity_rps   observed_failover_latency_seconds (no edge) | nearest_backup_capacity_rps->observed_failover_latency_seconds | nearest_backup_capacity_rps->observed_failover_latency_seconds | nearest_backup_capacity_rps->observed_failover_latency_seconds | no edge | (nearest_backup_capacity_rps, observed_failover_latency_seconds)=A |
| nearest_backup_capacity_rps, client_region | nearest_backup_capacity_rps o-o client_region | nearest_backup_capacity_rps   client_region (no edge) | nearest_backup_capacity_rps   client_region (no edge) | nearest_backup_capacity_rps   client_region (no edge) | nearest_backup_capacity_rps   client_region (no edge) | client_region -> nearest_backup_capacity_rps | (nearest_backup_capacity_rps, client_region)=C |
| baseline_latency_ms, selected_backup_pop | baseline_latency_ms o-o selected_backup_pop | baseline_latency_ms   selected_backup_pop (no edge) | baseline_latency_ms   selected_backup_pop (no edge) | baseline_latency_ms   selected_backup_pop (no edge) | baseline_latency_ms   selected_backup_pop (no edge) | selected_backup_pop -> baseline_latency_ms | (baseline_latency_ms, selected_backup_pop)=C |
| serve_stale_enabled, resolver_class | resolver_class->serve_stale_enabled | resolver_class->serve_stale_enabled | serve_stale_enabled   resolver_class (no edge) | serve_stale_enabled   resolver_class (no edge) | serve_stale_enabled   resolver_class (no edge) | resolver_class -> serve_stale_enabled | (serve_stale_enabled, resolver_class)=C |
| serve_stale_enabled, stale_hit_probability_at_outage | serve_stale_enabled   stale_hit_probability_at_outage (no edge) | serve_stale_enabled   stale_hit_probability_at_outage (no edge) | serve_stale_enabled->stale_hit_probability_at_outage | serve_stale_enabled->stale_hit_probability_at_outage | serve_stale_enabled->stale_hit_probability_at_outage | no edge | (serve_stale_enabled, stale_hit_probability_at_outage)=A |
| serve_stale_enabled, time_to_95p_adoption_seconds | serve_stale_enabled <-> time_to_95p_adoption_seconds | serve_stale_enabled   time_to_95p_adoption_seconds (no edge) | serve_stale_enabled   time_to_95p_adoption_seconds (no edge) | serve_stale_enabled   time_to_95p_adoption_seconds (no edge) | serve_stale_enabled   time_to_95p_adoption_seconds (no edge) | serve_stale_enabled -> time_to_95p_adoption_seconds | (serve_stale_enabled, time_to_95p_adoption_seconds)=C |
| resolver_class, failure_caching_level | resolver_class o-o failure_caching_level | resolver_class   failure_caching_level (no edge) | resolver_class   failure_caching_level (no edge) | resolver_class   failure_caching_level (no edge) | resolver_class   failure_caching_level (no edge) | resolver_class -> failure_caching_level | (resolver_class, failure_caching_level)=D |
| resolver_class, resolver_prefetch_threshold | resolver_class o-o resolver_prefetch_threshold | resolver_class   resolver_prefetch_threshold (no edge) | resolver_class   resolver_prefetch_threshold (no edge) | resolver_class   resolver_prefetch_threshold (no edge) | resolver_class   resolver_prefetch_threshold (no edge) | resolver_class -> resolver_prefetch_threshold | (resolver_class, resolver_prefetch_threshold)=D |
| cohort_request_rate_qps, failover_latency_seconds | cohort_request_rate_qps <-> failover_latency_seconds | cohort_request_rate_qps   failover_latency_seconds (no edge) | cohort_request_rate_qps   failover_latency_seconds (no edge) | cohort_request_rate_qps   failover_latency_seconds (no edge) | cohort_request_rate_qps   failover_latency_seconds (no edge) | no edge | (cohort_request_rate_qps, failover_latency_seconds)=D |
| cohort_request_rate_qps, observed_failover_latency_seconds | cohort_request_rate_qps <-> observed_failover_latency_seconds | cohort_request_rate_qps   observed_failover_latency_seconds (no edge) | cohort_request_rate_qps   observed_failover_latency_seconds (no edge) | cohort_request_rate_qps   observed_failover_latency_seconds (no edge) | cohort_request_rate_qps   observed_failover_latency_seconds (no edge) | no edge | (cohort_request_rate_qps, observed_failover_latency_seconds)=D |
| consecutive_failure_threshold, detection_delay_seconds | consecutive_failure_threshold o-> detection_delay_seconds | consecutive_failure_threshold   detection_delay_seconds (no edge) | consecutive_failure_threshold   detection_delay_seconds (no edge) | consecutive_failure_threshold   detection_delay_seconds (no edge) | consecutive_failure_threshold   detection_delay_seconds (no edge) | consecutive_failure_threshold -> detection_delay_seconds | (consecutive_failure_threshold, detection_delay_seconds)=D |
| ttl_config_seconds, time_to_95p_adoption_seconds | ttl_config_seconds o-> time_to_95p_adoption_seconds | ttl_config_seconds   time_to_95p_adoption_seconds (no edge) | ttl_config_seconds   time_to_95p_adoption_seconds (no edge) | ttl_config_seconds   time_to_95p_adoption_seconds (no edge) | ttl_config_seconds   time_to_95p_adoption_seconds (no edge) | ttl_config_seconds -> time_to_95p_adoption_seconds | (ttl_config_seconds, time_to_95p_adoption_seconds)=C |
| failover_latency_seconds, observed_failover_latency_seconds | failover_latency_seconds ~~~ observed_failover_latency_seconds | failover_latency_seconds   observed_failover_latency_seconds (no edge) | failover_latency_seconds->observed_failover_latency_seconds | failover_latency_seconds->observed_failover_latency_seconds | failover_latency_seconds->observed_failover_latency_seconds | failover_latency_seconds -> observed_failover_latency_seconds | (failover_latency_seconds, observed_failover_latency_seconds)=A |
| selected_backup_pop, primary_pop_outage | selected_backup_pop   primary_pop_outage (no edge) | selected_backup_pop   primary_pop_outage (no edge) | selected_backup_pop->primary_pop_outage | selected_backup_pop->primary_pop_outage | selected_backup_pop->primary_pop_outage | no edge | (selected_backup_pop, primary_pop_outage)=A |
| selected_backup_pop, observed_failover_latency_seconds | selected_backup_pop   observed_failover_latency_seconds (no edge) | selected_backup_pop   observed_failover_latency_seconds (no edge) | selected_backup_pop->observed_failover_latency_seconds | selected_backup_pop->observed_failover_latency_seconds | selected_backup_pop->observed_failover_latency_seconds | no edge | (selected_backup_pop, observed_failover_latency_seconds)=A |
| observed_incident_error_rate, primary_pop_outage | observed_incident_error_rate   primary_pop_outage (no edge) | observed_incident_error_rate   primary_pop_outage (no edge) | observed_incident_error_rate->primary_pop_outage | observed_incident_error_rate->primary_pop_outage | observed_incident_error_rate->primary_pop_outage | no edge | (observed_incident_error_rate, primary_pop_outage)=A |
| time_to_95p_adoption_seconds, observed_failover_latency_seconds | time_to_95p_adoption_seconds->observed_failover_latency_seconds | time_to_95p_adoption_seconds   observed_failover_latency_seconds (no edge) | time_to_95p_adoption_seconds   observed_failover_latency_seconds (no edge) | time_to_95p_adoption_seconds   observed_failover_latency_seconds (no edge) | time_to_95p_adoption_seconds   observed_failover_latency_seconds (no edge) | no edge | (time_to_95p_adoption_seconds, observed_failover_latency_seconds)=D |
| primary_pop_outage, observed_failover_latency_seconds | primary_pop_outage   observed_failover_latency_seconds (no edge) | primary_pop_outage   observed_failover_latency_seconds (no edge) | primary_pop_outage->observed_failover_latency_seconds | primary_pop_outage->observed_failover_latency_seconds | primary_pop_outage->observed_failover_latency_seconds | no edge | (primary_pop_outage, observed_failover_latency_seconds)=A |
| detection_delay_seconds, health_check_interval_seconds | health_check_interval_seconds o-> detection_delay_seconds | detection_delay_seconds   health_check_interval_seconds (no edge) | detection_delay_seconds->health_check_interval_seconds | detection_delay_seconds->health_check_interval_seconds | detection_delay_seconds->health_check_interval_seconds | health_check_interval_seconds -> detection_delay_seconds | (detection_delay_seconds, health_check_interval_seconds)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
