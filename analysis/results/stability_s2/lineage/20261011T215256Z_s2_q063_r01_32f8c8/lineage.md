# Edge lineage: 20261011T215256Z_s2_q063_r01_32f8c8

Dataset `/research/datasets/suite_q1s2/q063/q063.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 21 | 0.67 | 0.30 | 0.41 | 4 | 0 | 10 | 51 |
| S1 after bootstrap edits | 3 | 1.00 | 0.06 | 0.12 | 3 | 0 | 0 | 45 |
| S2 after LLM review | 14 | 0.29 | 0.09 | 0.13 | 2 | 2 | 0 | 55 |
| S3 after KCI pruning | 12 | 0.33 | 0.09 | 0.14 | 2 | 2 | 0 | 53 |
| S4 final (after cycle step) | 12 | 0.33 | 0.09 | 0.14 | 2 | 2 | 0 | 53 |

Scored against: reference graph s2_06_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 18. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 11, "B": 2, "C": 151, "D": 136}.
- LLM effect: added 11 (of which 10 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 1.
- KCI step removed 2. Cycle step changed 0.
- Final graph: 12 edges; set by {"llm": 10, "algorithm (unchanged)": 2}; 2 identical to the algorithm's output; 9 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| routing_weight_nearest_backup->failover_latency_seconds | llm | no | 0.85 |
| nearest_backup_capacity_rps->failover_latency_seconds | llm | no | 1.00 |
| nearest_backup_capacity_rps->observed_failover_latency_seconds | llm | no | 0.95 |
| resolver_ttl_floor_seconds->ttl_config_seconds | llm | no | 1.00 |
| cohort_request_rate_qps->incident_error_rate | algorithm (unchanged) | yes | 0.00 |
| incident_error_rate->observed_incident_error_rate | llm | no | 1.00 |
| serve_stale_enabled->stale_hit_probability_at_outage | llm | no | 0.95 |
| baseline_latency_ms->cohort_request_rate_qps | llm | yes | 0.35 |
| cohort_request_rate_qps->failure_caching_level | algorithm (unchanged) | yes | 0.00 |
| failover_latency_seconds->observed_failover_latency_seconds | llm | no | 1.00 |
| stale_hit_probability_at_outage->primary_pop_outage | llm | no | 1.00 |
| observed_incident_error_rate->primary_pop_outage | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| routing_weight_nearest_backup, failover_latency_seconds | routing_weight_nearest_backup   failover_latency_seconds (no edge) | routing_weight_nearest_backup   failover_latency_seconds (no edge) | routing_weight_nearest_backup->failover_latency_seconds | routing_weight_nearest_backup->failover_latency_seconds | routing_weight_nearest_backup->failover_latency_seconds | no edge | (routing_weight_nearest_backup, failover_latency_seconds)=A |
| routing_weight_nearest_backup, selected_backup_pop | routing_weight_nearest_backup o-o selected_backup_pop | routing_weight_nearest_backup   selected_backup_pop (no edge) | routing_weight_nearest_backup   selected_backup_pop (no edge) | routing_weight_nearest_backup   selected_backup_pop (no edge) | routing_weight_nearest_backup   selected_backup_pop (no edge) | no edge | (routing_weight_nearest_backup, selected_backup_pop)=D |
| nearest_backup_capacity_rps, failover_latency_seconds | nearest_backup_capacity_rps   failover_latency_seconds (no edge) | nearest_backup_capacity_rps   failover_latency_seconds (no edge) | nearest_backup_capacity_rps->failover_latency_seconds | nearest_backup_capacity_rps->failover_latency_seconds | nearest_backup_capacity_rps->failover_latency_seconds | no edge | (nearest_backup_capacity_rps, failover_latency_seconds)=A |
| nearest_backup_capacity_rps, time_to_95p_adoption_seconds | nearest_backup_capacity_rps ~~~ time_to_95p_adoption_seconds | nearest_backup_capacity_rps   time_to_95p_adoption_seconds (no edge) | nearest_backup_capacity_rps   time_to_95p_adoption_seconds (no edge) | nearest_backup_capacity_rps   time_to_95p_adoption_seconds (no edge) | nearest_backup_capacity_rps   time_to_95p_adoption_seconds (no edge) | nearest_backup_capacity_rps -> time_to_95p_adoption_seconds | (nearest_backup_capacity_rps, time_to_95p_adoption_seconds)=C |
| nearest_backup_capacity_rps, observed_incident_error_rate | nearest_backup_capacity_rps ~~~ observed_incident_error_rate | nearest_backup_capacity_rps   observed_incident_error_rate (no edge) | nearest_backup_capacity_rps   observed_incident_error_rate (no edge) | nearest_backup_capacity_rps   observed_incident_error_rate (no edge) | nearest_backup_capacity_rps   observed_incident_error_rate (no edge) | observed_incident_error_rate -> nearest_backup_capacity_rps | (nearest_backup_capacity_rps, observed_incident_error_rate)=C |
| nearest_backup_capacity_rps, observed_failover_latency_seconds | nearest_backup_capacity_rps   observed_failover_latency_seconds (no edge) | nearest_backup_capacity_rps   observed_failover_latency_seconds (no edge) | nearest_backup_capacity_rps->observed_failover_latency_seconds | nearest_backup_capacity_rps->observed_failover_latency_seconds | nearest_backup_capacity_rps->observed_failover_latency_seconds | observed_failover_latency_seconds -> nearest_backup_capacity_rps | (nearest_backup_capacity_rps, observed_failover_latency_seconds)=A |
| resolver_ttl_floor_seconds, ttl_config_seconds | resolver_ttl_floor_seconds   ttl_config_seconds (no edge) | resolver_ttl_floor_seconds   ttl_config_seconds (no edge) | resolver_ttl_floor_seconds->ttl_config_seconds | resolver_ttl_floor_seconds->ttl_config_seconds | resolver_ttl_floor_seconds->ttl_config_seconds | no edge | (resolver_ttl_floor_seconds, ttl_config_seconds)=A |
| resolver_ttl_floor_seconds, failure_caching_level | resolver_ttl_floor_seconds->failure_caching_level | resolver_ttl_floor_seconds   failure_caching_level (no edge) | resolver_ttl_floor_seconds   failure_caching_level (no edge) | resolver_ttl_floor_seconds   failure_caching_level (no edge) | resolver_ttl_floor_seconds   failure_caching_level (no edge) | no edge | (resolver_ttl_floor_seconds, failure_caching_level)=C |
| resolver_ttl_floor_seconds, resolver_prefetch_threshold | resolver_ttl_floor_seconds o-o resolver_prefetch_threshold | resolver_ttl_floor_seconds   resolver_prefetch_threshold (no edge) | resolver_ttl_floor_seconds   resolver_prefetch_threshold (no edge) | resolver_ttl_floor_seconds   resolver_prefetch_threshold (no edge) | resolver_ttl_floor_seconds   resolver_prefetch_threshold (no edge) | resolver_prefetch_threshold -> resolver_ttl_floor_seconds | (resolver_ttl_floor_seconds, resolver_prefetch_threshold)=C |
| incident_error_rate, consecutive_failure_threshold | incident_error_rate <-> consecutive_failure_threshold | incident_error_rate   consecutive_failure_threshold (no edge) | incident_error_rate   consecutive_failure_threshold (no edge) | incident_error_rate   consecutive_failure_threshold (no edge) | incident_error_rate   consecutive_failure_threshold (no edge) | no edge | (incident_error_rate, consecutive_failure_threshold)=D |
| incident_error_rate, stale_hit_probability_at_outage | incident_error_rate <-> stale_hit_probability_at_outage | incident_error_rate   stale_hit_probability_at_outage (no edge) | incident_error_rate   stale_hit_probability_at_outage (no edge) | incident_error_rate   stale_hit_probability_at_outage (no edge) | incident_error_rate   stale_hit_probability_at_outage (no edge) | no edge | (incident_error_rate, stale_hit_probability_at_outage)=D |
| incident_error_rate, observed_incident_error_rate | incident_error_rate   observed_incident_error_rate (no edge) | incident_error_rate   observed_incident_error_rate (no edge) | incident_error_rate->observed_incident_error_rate | incident_error_rate->observed_incident_error_rate | incident_error_rate->observed_incident_error_rate | no edge | (incident_error_rate, observed_incident_error_rate)=A |
| incident_error_rate, detection_delay_seconds | incident_error_rate <-> detection_delay_seconds | incident_error_rate   detection_delay_seconds (no edge) | incident_error_rate   detection_delay_seconds (no edge) | incident_error_rate   detection_delay_seconds (no edge) | incident_error_rate   detection_delay_seconds (no edge) | no edge | (incident_error_rate, detection_delay_seconds)=D |
| serve_stale_enabled, stale_hit_probability_at_outage | serve_stale_enabled   stale_hit_probability_at_outage (no edge) | serve_stale_enabled   stale_hit_probability_at_outage (no edge) | serve_stale_enabled->stale_hit_probability_at_outage | serve_stale_enabled->stale_hit_probability_at_outage | serve_stale_enabled->stale_hit_probability_at_outage | no edge | (serve_stale_enabled, stale_hit_probability_at_outage)=A |
| serve_stale_enabled, probe_loss_jitter_rate | serve_stale_enabled o-o probe_loss_jitter_rate | serve_stale_enabled   probe_loss_jitter_rate (no edge) | serve_stale_enabled   probe_loss_jitter_rate (no edge) | serve_stale_enabled   probe_loss_jitter_rate (no edge) | serve_stale_enabled   probe_loss_jitter_rate (no edge) | probe_loss_jitter_rate -> serve_stale_enabled | (serve_stale_enabled, probe_loss_jitter_rate)=C |
| baseline_latency_ms, cohort_request_rate_qps | cohort_request_rate_qps->baseline_latency_ms | cohort_request_rate_qps->baseline_latency_ms | baseline_latency_ms->cohort_request_rate_qps | baseline_latency_ms->cohort_request_rate_qps | baseline_latency_ms->cohort_request_rate_qps | cohort_request_rate_qps -> baseline_latency_ms | (baseline_latency_ms, cohort_request_rate_qps)=A |
| baseline_latency_ms, health_check_interval_seconds | baseline_latency_ms <-> health_check_interval_seconds | baseline_latency_ms   health_check_interval_seconds (no edge) | baseline_latency_ms   health_check_interval_seconds (no edge) | baseline_latency_ms   health_check_interval_seconds (no edge) | baseline_latency_ms   health_check_interval_seconds (no edge) | baseline_latency_ms -> health_check_interval_seconds | (baseline_latency_ms, health_check_interval_seconds)=C |
| cohort_request_rate_qps, ecs_present | cohort_request_rate_qps o-o ecs_present | cohort_request_rate_qps   ecs_present (no edge) | cohort_request_rate_qps   ecs_present (no edge) | cohort_request_rate_qps   ecs_present (no edge) | cohort_request_rate_qps   ecs_present (no edge) | cohort_request_rate_qps -> ecs_present | (cohort_request_rate_qps, ecs_present)=D |
| consecutive_failure_threshold, ecs_present | ecs_present->consecutive_failure_threshold | consecutive_failure_threshold   ecs_present (no edge) | consecutive_failure_threshold   ecs_present (no edge) | consecutive_failure_threshold   ecs_present (no edge) | consecutive_failure_threshold   ecs_present (no edge) | no edge | (consecutive_failure_threshold, ecs_present)=C |
| resolver_class, observed_failover_latency_seconds | resolver_class o-> observed_failover_latency_seconds | resolver_class   observed_failover_latency_seconds (no edge) | resolver_class   observed_failover_latency_seconds (no edge) | resolver_class   observed_failover_latency_seconds (no edge) | resolver_class   observed_failover_latency_seconds (no edge) | resolver_class -> observed_failover_latency_seconds | (resolver_class, observed_failover_latency_seconds)=D |
| failover_latency_seconds, health_check_interval_seconds | failover_latency_seconds o-> health_check_interval_seconds | failover_latency_seconds   health_check_interval_seconds (no edge) | failover_latency_seconds   health_check_interval_seconds (no edge) | failover_latency_seconds   health_check_interval_seconds (no edge) | failover_latency_seconds   health_check_interval_seconds (no edge) | failover_latency_seconds -> health_check_interval_seconds | (failover_latency_seconds, health_check_interval_seconds)=D |
| failover_latency_seconds, observed_failover_latency_seconds | failover_latency_seconds   observed_failover_latency_seconds (no edge) | failover_latency_seconds   observed_failover_latency_seconds (no edge) | failover_latency_seconds->observed_failover_latency_seconds | failover_latency_seconds->observed_failover_latency_seconds | failover_latency_seconds->observed_failover_latency_seconds | no edge | (failover_latency_seconds, observed_failover_latency_seconds)=A |
| failover_latency_seconds, primary_pop_outage | failover_latency_seconds   primary_pop_outage (no edge) | failover_latency_seconds   primary_pop_outage (no edge) | primary_pop_outage->failover_latency_seconds | failover_latency_seconds   primary_pop_outage (no edge) | failover_latency_seconds   primary_pop_outage (no edge) | no edge | (failover_latency_seconds, primary_pop_outage)=B |
| stale_hit_probability_at_outage, health_check_interval_seconds | health_check_interval_seconds->stale_hit_probability_at_outage | stale_hit_probability_at_outage   health_check_interval_seconds (no edge) | stale_hit_probability_at_outage   health_check_interval_seconds (no edge) | stale_hit_probability_at_outage   health_check_interval_seconds (no edge) | stale_hit_probability_at_outage   health_check_interval_seconds (no edge) | health_check_interval_seconds -> stale_hit_probability_at_outage | (stale_hit_probability_at_outage, health_check_interval_seconds)=D |
| stale_hit_probability_at_outage, detection_delay_seconds | stale_hit_probability_at_outage ~~~ detection_delay_seconds | stale_hit_probability_at_outage   detection_delay_seconds (no edge) | stale_hit_probability_at_outage   detection_delay_seconds (no edge) | stale_hit_probability_at_outage   detection_delay_seconds (no edge) | stale_hit_probability_at_outage   detection_delay_seconds (no edge) | stale_hit_probability_at_outage -> detection_delay_seconds | (stale_hit_probability_at_outage, detection_delay_seconds)=D |
| stale_hit_probability_at_outage, primary_pop_outage | stale_hit_probability_at_outage   primary_pop_outage (no edge) | stale_hit_probability_at_outage   primary_pop_outage (no edge) | stale_hit_probability_at_outage->primary_pop_outage | stale_hit_probability_at_outage->primary_pop_outage | stale_hit_probability_at_outage->primary_pop_outage | no edge | (stale_hit_probability_at_outage, primary_pop_outage)=A |
| health_check_interval_seconds, detection_delay_seconds | health_check_interval_seconds->detection_delay_seconds | health_check_interval_seconds   detection_delay_seconds (no edge) | health_check_interval_seconds   detection_delay_seconds (no edge) | health_check_interval_seconds   detection_delay_seconds (no edge) | health_check_interval_seconds   detection_delay_seconds (no edge) | no edge | (health_check_interval_seconds, detection_delay_seconds)=C |
| observed_incident_error_rate, primary_pop_outage | observed_incident_error_rate   primary_pop_outage (no edge) | observed_incident_error_rate   primary_pop_outage (no edge) | observed_incident_error_rate->primary_pop_outage | observed_incident_error_rate->primary_pop_outage | observed_incident_error_rate->primary_pop_outage | no edge | (observed_incident_error_rate, primary_pop_outage)=A |
| observed_failover_latency_seconds, client_region | client_region o-> observed_failover_latency_seconds | observed_failover_latency_seconds   client_region (no edge) | observed_failover_latency_seconds   client_region (no edge) | observed_failover_latency_seconds   client_region (no edge) | observed_failover_latency_seconds   client_region (no edge) | client_region -> observed_failover_latency_seconds | (observed_failover_latency_seconds, client_region)=D |
| observed_failover_latency_seconds, primary_pop_outage | observed_failover_latency_seconds   primary_pop_outage (no edge) | observed_failover_latency_seconds   primary_pop_outage (no edge) | primary_pop_outage->observed_failover_latency_seconds | observed_failover_latency_seconds   primary_pop_outage (no edge) | observed_failover_latency_seconds   primary_pop_outage (no edge) | no edge | (observed_failover_latency_seconds, primary_pop_outage)=B |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
