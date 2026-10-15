# Edge lineage: 20261014T020501Z_ab06cc_q063_r01_d4f951

Dataset `/research/datasets/suite_q1s2/q063/q063.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 2}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 20 | 0.75 | 0.32 | 0.45 | 4 | 0 | 11 | 50 |
| S1 after bootstrap edits | 4 | 0.75 | 0.06 | 0.12 | 3 | 0 | 0 | 47 |
| S2 after LLM review | 25 | 0.16 | 0.09 | 0.11 | 1 | 3 | 0 | 67 |
| S3 after KCI pruning | 25 | 0.16 | 0.09 | 0.11 | 1 | 3 | 0 | 67 |
| S4 final (after cycle step) | 25 | 0.16 | 0.09 | 0.11 | 1 | 3 | 0 | 67 |

Scored against: reference graph s2_06_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 16. Of the deleted, 7 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 25, "C": 266, "D": 9}.
- LLM effect: added 22 (of which 21 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 3.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 25 edges; set by {"llm": 25}; 1 identical to the algorithm's output; 20 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| resolver_ttl_floor_seconds->baseline_latency_ms | llm | no | 1.00 |
| resolver_ttl_floor_seconds->ttl_config_seconds | llm | no | 1.00 |
| incident_error_rate->baseline_latency_ms | llm | no | 1.00 |
| incident_error_rate->cohort_request_rate_qps | llm | yes | 0.00 |
| incident_error_rate->failover_latency_seconds | llm | no | 1.00 |
| incident_error_rate->stale_hit_probability_at_outage | llm | yes | 0.75 |
| incident_error_rate->observed_incident_error_rate | llm | no | 1.00 |
| incident_error_rate->observed_failover_latency_seconds | llm | no | 1.00 |
| incident_error_rate->detection_delay_seconds | llm | yes | 0.95 |
| incident_error_rate->primary_pop_outage | llm | no | 1.00 |
| serve_stale_enabled->stale_hit_probability_at_outage | llm | no | 0.95 |
| baseline_latency_ms->cohort_request_rate_qps | llm | yes | 0.20 |
| baseline_latency_ms->observed_incident_error_rate | llm | no | 1.00 |
| cohort_request_rate_qps->observed_incident_error_rate | llm | no | 1.00 |
| consecutive_failure_threshold->observed_incident_error_rate | llm | no | 1.00 |
| failover_latency_seconds->observed_failover_latency_seconds | llm | no | 1.00 |
| stale_hit_probability_at_outage->observed_incident_error_rate | llm | no | 0.85 |
| health_check_interval_seconds->detection_delay_seconds | llm | yes | 1.00 |
| observed_incident_error_rate->observed_failover_latency_seconds | llm | no | 0.95 |
| observed_incident_error_rate->detection_delay_seconds | llm | no | 0.90 |
| observed_incident_error_rate->primary_pop_outage | llm | no | 1.00 |
| observed_failover_latency_seconds->detection_delay_seconds | llm | no | 1.00 |
| observed_failover_latency_seconds->primary_pop_outage | llm | no | 1.00 |
| detection_delay_seconds->primary_pop_outage | llm | no | 1.00 |
| client_region->primary_pop_outage | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| rum_sampling_fraction, resolver_ttl_floor_seconds | rum_sampling_fraction o-o resolver_ttl_floor_seconds | rum_sampling_fraction   resolver_ttl_floor_seconds (no edge) | rum_sampling_fraction   resolver_ttl_floor_seconds (no edge) | rum_sampling_fraction   resolver_ttl_floor_seconds (no edge) | rum_sampling_fraction   resolver_ttl_floor_seconds (no edge) | no edge | (rum_sampling_fraction, resolver_ttl_floor_seconds)=C |
| nearest_backup_capacity_rps, time_to_95p_adoption_seconds | nearest_backup_capacity_rps ~~~ time_to_95p_adoption_seconds | nearest_backup_capacity_rps   time_to_95p_adoption_seconds (no edge) | nearest_backup_capacity_rps   time_to_95p_adoption_seconds (no edge) | nearest_backup_capacity_rps   time_to_95p_adoption_seconds (no edge) | nearest_backup_capacity_rps   time_to_95p_adoption_seconds (no edge) | nearest_backup_capacity_rps -> time_to_95p_adoption_seconds | (nearest_backup_capacity_rps, time_to_95p_adoption_seconds)=C |
| nearest_backup_capacity_rps, observed_incident_error_rate | nearest_backup_capacity_rps ~~~ observed_incident_error_rate | nearest_backup_capacity_rps   observed_incident_error_rate (no edge) | nearest_backup_capacity_rps   observed_incident_error_rate (no edge) | nearest_backup_capacity_rps   observed_incident_error_rate (no edge) | nearest_backup_capacity_rps   observed_incident_error_rate (no edge) | observed_incident_error_rate -> nearest_backup_capacity_rps | (nearest_backup_capacity_rps, observed_incident_error_rate)=C |
| resolver_ttl_floor_seconds, baseline_latency_ms | resolver_ttl_floor_seconds   baseline_latency_ms (no edge) | resolver_ttl_floor_seconds   baseline_latency_ms (no edge) | resolver_ttl_floor_seconds->baseline_latency_ms | resolver_ttl_floor_seconds->baseline_latency_ms | resolver_ttl_floor_seconds->baseline_latency_ms | no edge | (resolver_ttl_floor_seconds, baseline_latency_ms)=A |
| resolver_ttl_floor_seconds, ttl_config_seconds | resolver_ttl_floor_seconds   ttl_config_seconds (no edge) | resolver_ttl_floor_seconds   ttl_config_seconds (no edge) | resolver_ttl_floor_seconds->ttl_config_seconds | resolver_ttl_floor_seconds->ttl_config_seconds | resolver_ttl_floor_seconds->ttl_config_seconds | no edge | (resolver_ttl_floor_seconds, ttl_config_seconds)=A |
| resolver_ttl_floor_seconds, resolver_prefetch_threshold | resolver_ttl_floor_seconds o-o resolver_prefetch_threshold | resolver_ttl_floor_seconds   resolver_prefetch_threshold (no edge) | resolver_ttl_floor_seconds   resolver_prefetch_threshold (no edge) | resolver_ttl_floor_seconds   resolver_prefetch_threshold (no edge) | resolver_ttl_floor_seconds   resolver_prefetch_threshold (no edge) | resolver_prefetch_threshold -> resolver_ttl_floor_seconds | (resolver_ttl_floor_seconds, resolver_prefetch_threshold)=C |
| incident_error_rate, baseline_latency_ms | incident_error_rate   baseline_latency_ms (no edge) | incident_error_rate   baseline_latency_ms (no edge) | incident_error_rate->baseline_latency_ms | incident_error_rate->baseline_latency_ms | incident_error_rate->baseline_latency_ms | no edge | (incident_error_rate, baseline_latency_ms)=A |
| incident_error_rate, cohort_request_rate_qps | cohort_request_rate_qps->incident_error_rate | cohort_request_rate_qps->incident_error_rate | incident_error_rate->cohort_request_rate_qps | incident_error_rate->cohort_request_rate_qps | incident_error_rate->cohort_request_rate_qps | cohort_request_rate_qps -> incident_error_rate | (incident_error_rate, cohort_request_rate_qps)=A |
| incident_error_rate, failover_latency_seconds | incident_error_rate   failover_latency_seconds (no edge) | incident_error_rate   failover_latency_seconds (no edge) | incident_error_rate->failover_latency_seconds | incident_error_rate->failover_latency_seconds | incident_error_rate->failover_latency_seconds | no edge | (incident_error_rate, failover_latency_seconds)=A |
| incident_error_rate, stale_hit_probability_at_outage | stale_hit_probability_at_outage->incident_error_rate | stale_hit_probability_at_outage->incident_error_rate | incident_error_rate->stale_hit_probability_at_outage | incident_error_rate->stale_hit_probability_at_outage | incident_error_rate->stale_hit_probability_at_outage | no edge | (incident_error_rate, stale_hit_probability_at_outage)=A |
| incident_error_rate, observed_incident_error_rate | incident_error_rate   observed_incident_error_rate (no edge) | incident_error_rate   observed_incident_error_rate (no edge) | incident_error_rate->observed_incident_error_rate | incident_error_rate->observed_incident_error_rate | incident_error_rate->observed_incident_error_rate | no edge | (incident_error_rate, observed_incident_error_rate)=A |
| incident_error_rate, observed_failover_latency_seconds | incident_error_rate   observed_failover_latency_seconds (no edge) | incident_error_rate   observed_failover_latency_seconds (no edge) | incident_error_rate->observed_failover_latency_seconds | incident_error_rate->observed_failover_latency_seconds | incident_error_rate->observed_failover_latency_seconds | no edge | (incident_error_rate, observed_failover_latency_seconds)=A |
| incident_error_rate, detection_delay_seconds | detection_delay_seconds->incident_error_rate | incident_error_rate   detection_delay_seconds (no edge) | incident_error_rate->detection_delay_seconds | incident_error_rate->detection_delay_seconds | incident_error_rate->detection_delay_seconds | no edge | (incident_error_rate, detection_delay_seconds)=A |
| incident_error_rate, primary_pop_outage | incident_error_rate   primary_pop_outage (no edge) | incident_error_rate   primary_pop_outage (no edge) | incident_error_rate->primary_pop_outage | incident_error_rate->primary_pop_outage | incident_error_rate->primary_pop_outage | no edge | (incident_error_rate, primary_pop_outage)=A |
| serve_stale_enabled, stale_hit_probability_at_outage | serve_stale_enabled   stale_hit_probability_at_outage (no edge) | serve_stale_enabled   stale_hit_probability_at_outage (no edge) | serve_stale_enabled->stale_hit_probability_at_outage | serve_stale_enabled->stale_hit_probability_at_outage | serve_stale_enabled->stale_hit_probability_at_outage | no edge | (serve_stale_enabled, stale_hit_probability_at_outage)=A |
| serve_stale_enabled, probe_loss_jitter_rate | serve_stale_enabled o-o probe_loss_jitter_rate | serve_stale_enabled   probe_loss_jitter_rate (no edge) | serve_stale_enabled   probe_loss_jitter_rate (no edge) | serve_stale_enabled   probe_loss_jitter_rate (no edge) | serve_stale_enabled   probe_loss_jitter_rate (no edge) | probe_loss_jitter_rate -> serve_stale_enabled | (serve_stale_enabled, probe_loss_jitter_rate)=C |
| baseline_latency_ms, cohort_request_rate_qps | cohort_request_rate_qps->baseline_latency_ms | cohort_request_rate_qps->baseline_latency_ms | baseline_latency_ms->cohort_request_rate_qps | baseline_latency_ms->cohort_request_rate_qps | baseline_latency_ms->cohort_request_rate_qps | cohort_request_rate_qps -> baseline_latency_ms | (baseline_latency_ms, cohort_request_rate_qps)=A |
| baseline_latency_ms, health_check_interval_seconds | baseline_latency_ms <-> health_check_interval_seconds | baseline_latency_ms   health_check_interval_seconds (no edge) | baseline_latency_ms   health_check_interval_seconds (no edge) | baseline_latency_ms   health_check_interval_seconds (no edge) | baseline_latency_ms   health_check_interval_seconds (no edge) | baseline_latency_ms -> health_check_interval_seconds | (baseline_latency_ms, health_check_interval_seconds)=C |
| baseline_latency_ms, observed_incident_error_rate | baseline_latency_ms   observed_incident_error_rate (no edge) | baseline_latency_ms   observed_incident_error_rate (no edge) | baseline_latency_ms->observed_incident_error_rate | baseline_latency_ms->observed_incident_error_rate | baseline_latency_ms->observed_incident_error_rate | no edge | (baseline_latency_ms, observed_incident_error_rate)=A |
| cohort_request_rate_qps, consecutive_failure_threshold | cohort_request_rate_qps <-> consecutive_failure_threshold | cohort_request_rate_qps   consecutive_failure_threshold (no edge) | cohort_request_rate_qps   consecutive_failure_threshold (no edge) | cohort_request_rate_qps   consecutive_failure_threshold (no edge) | cohort_request_rate_qps   consecutive_failure_threshold (no edge) | cohort_request_rate_qps -> consecutive_failure_threshold | (cohort_request_rate_qps, consecutive_failure_threshold)=C |
| cohort_request_rate_qps, failure_caching_level | failure_caching_level o-> cohort_request_rate_qps | cohort_request_rate_qps   failure_caching_level (no edge) | cohort_request_rate_qps   failure_caching_level (no edge) | cohort_request_rate_qps   failure_caching_level (no edge) | cohort_request_rate_qps   failure_caching_level (no edge) | cohort_request_rate_qps -> failure_caching_level | (cohort_request_rate_qps, failure_caching_level)=C |
| cohort_request_rate_qps, observed_incident_error_rate | cohort_request_rate_qps   observed_incident_error_rate (no edge) | cohort_request_rate_qps   observed_incident_error_rate (no edge) | cohort_request_rate_qps->observed_incident_error_rate | cohort_request_rate_qps->observed_incident_error_rate | cohort_request_rate_qps->observed_incident_error_rate | no edge | (cohort_request_rate_qps, observed_incident_error_rate)=A |
| cohort_request_rate_qps, ecs_present | cohort_request_rate_qps->ecs_present | cohort_request_rate_qps->ecs_present | cohort_request_rate_qps   ecs_present (no edge) | cohort_request_rate_qps   ecs_present (no edge) | cohort_request_rate_qps   ecs_present (no edge) | cohort_request_rate_qps -> ecs_present | (cohort_request_rate_qps, ecs_present)=C |
| consecutive_failure_threshold, observed_incident_error_rate | consecutive_failure_threshold   observed_incident_error_rate (no edge) | consecutive_failure_threshold   observed_incident_error_rate (no edge) | consecutive_failure_threshold->observed_incident_error_rate | consecutive_failure_threshold->observed_incident_error_rate | consecutive_failure_threshold->observed_incident_error_rate | no edge | (consecutive_failure_threshold, observed_incident_error_rate)=A |
| consecutive_failure_threshold, primary_pop_outage | primary_pop_outage o-> consecutive_failure_threshold | consecutive_failure_threshold   primary_pop_outage (no edge) | consecutive_failure_threshold   primary_pop_outage (no edge) | consecutive_failure_threshold   primary_pop_outage (no edge) | consecutive_failure_threshold   primary_pop_outage (no edge) | no edge | (consecutive_failure_threshold, primary_pop_outage)=C |
| resolver_class, observed_failover_latency_seconds | resolver_class o-> observed_failover_latency_seconds | resolver_class   observed_failover_latency_seconds (no edge) | resolver_class   observed_failover_latency_seconds (no edge) | resolver_class   observed_failover_latency_seconds (no edge) | resolver_class   observed_failover_latency_seconds (no edge) | resolver_class -> observed_failover_latency_seconds | (resolver_class, observed_failover_latency_seconds)=C |
| failover_latency_seconds, health_check_interval_seconds | failover_latency_seconds o-> health_check_interval_seconds | failover_latency_seconds   health_check_interval_seconds (no edge) | failover_latency_seconds   health_check_interval_seconds (no edge) | failover_latency_seconds   health_check_interval_seconds (no edge) | failover_latency_seconds   health_check_interval_seconds (no edge) | failover_latency_seconds -> health_check_interval_seconds | (failover_latency_seconds, health_check_interval_seconds)=C |
| failover_latency_seconds, observed_failover_latency_seconds | failover_latency_seconds   observed_failover_latency_seconds (no edge) | failover_latency_seconds   observed_failover_latency_seconds (no edge) | failover_latency_seconds->observed_failover_latency_seconds | failover_latency_seconds->observed_failover_latency_seconds | failover_latency_seconds->observed_failover_latency_seconds | no edge | (failover_latency_seconds, observed_failover_latency_seconds)=A |
| stale_hit_probability_at_outage, health_check_interval_seconds | health_check_interval_seconds->stale_hit_probability_at_outage | stale_hit_probability_at_outage   health_check_interval_seconds (no edge) | stale_hit_probability_at_outage   health_check_interval_seconds (no edge) | stale_hit_probability_at_outage   health_check_interval_seconds (no edge) | stale_hit_probability_at_outage   health_check_interval_seconds (no edge) | health_check_interval_seconds -> stale_hit_probability_at_outage | (stale_hit_probability_at_outage, health_check_interval_seconds)=C |
| stale_hit_probability_at_outage, observed_incident_error_rate | stale_hit_probability_at_outage   observed_incident_error_rate (no edge) | stale_hit_probability_at_outage   observed_incident_error_rate (no edge) | stale_hit_probability_at_outage->observed_incident_error_rate | stale_hit_probability_at_outage->observed_incident_error_rate | stale_hit_probability_at_outage->observed_incident_error_rate | observed_incident_error_rate -> stale_hit_probability_at_outage | (stale_hit_probability_at_outage, observed_incident_error_rate)=A |
| stale_hit_probability_at_outage, detection_delay_seconds | stale_hit_probability_at_outage ~~~ detection_delay_seconds | stale_hit_probability_at_outage   detection_delay_seconds (no edge) | stale_hit_probability_at_outage   detection_delay_seconds (no edge) | stale_hit_probability_at_outage   detection_delay_seconds (no edge) | stale_hit_probability_at_outage   detection_delay_seconds (no edge) | stale_hit_probability_at_outage -> detection_delay_seconds | (stale_hit_probability_at_outage, detection_delay_seconds)=C |
| health_check_interval_seconds, detection_delay_seconds | health_check_interval_seconds->detection_delay_seconds | health_check_interval_seconds   detection_delay_seconds (no edge) | health_check_interval_seconds->detection_delay_seconds | health_check_interval_seconds->detection_delay_seconds | health_check_interval_seconds->detection_delay_seconds | no edge | (health_check_interval_seconds, detection_delay_seconds)=A |
| observed_incident_error_rate, observed_failover_latency_seconds | observed_incident_error_rate   observed_failover_latency_seconds (no edge) | observed_incident_error_rate   observed_failover_latency_seconds (no edge) | observed_incident_error_rate->observed_failover_latency_seconds | observed_incident_error_rate->observed_failover_latency_seconds | observed_incident_error_rate->observed_failover_latency_seconds | observed_incident_error_rate -> observed_failover_latency_seconds | (observed_incident_error_rate, observed_failover_latency_seconds)=A |
| observed_incident_error_rate, detection_delay_seconds | observed_incident_error_rate   detection_delay_seconds (no edge) | observed_incident_error_rate   detection_delay_seconds (no edge) | observed_incident_error_rate->detection_delay_seconds | observed_incident_error_rate->detection_delay_seconds | observed_incident_error_rate->detection_delay_seconds | no edge | (observed_incident_error_rate, detection_delay_seconds)=A |
| observed_incident_error_rate, primary_pop_outage | observed_incident_error_rate   primary_pop_outage (no edge) | observed_incident_error_rate   primary_pop_outage (no edge) | observed_incident_error_rate->primary_pop_outage | observed_incident_error_rate->primary_pop_outage | observed_incident_error_rate->primary_pop_outage | no edge | (observed_incident_error_rate, primary_pop_outage)=A |
| observed_failover_latency_seconds, detection_delay_seconds | observed_failover_latency_seconds   detection_delay_seconds (no edge) | observed_failover_latency_seconds   detection_delay_seconds (no edge) | observed_failover_latency_seconds->detection_delay_seconds | observed_failover_latency_seconds->detection_delay_seconds | observed_failover_latency_seconds->detection_delay_seconds | no edge | (observed_failover_latency_seconds, detection_delay_seconds)=A |
| observed_failover_latency_seconds, client_region | client_region o-> observed_failover_latency_seconds | observed_failover_latency_seconds   client_region (no edge) | observed_failover_latency_seconds   client_region (no edge) | observed_failover_latency_seconds   client_region (no edge) | observed_failover_latency_seconds   client_region (no edge) | client_region -> observed_failover_latency_seconds | (observed_failover_latency_seconds, client_region)=C |
| observed_failover_latency_seconds, primary_pop_outage | observed_failover_latency_seconds   primary_pop_outage (no edge) | observed_failover_latency_seconds   primary_pop_outage (no edge) | observed_failover_latency_seconds->primary_pop_outage | observed_failover_latency_seconds->primary_pop_outage | observed_failover_latency_seconds->primary_pop_outage | no edge | (observed_failover_latency_seconds, primary_pop_outage)=A |
| detection_delay_seconds, primary_pop_outage | detection_delay_seconds   primary_pop_outage (no edge) | detection_delay_seconds   primary_pop_outage (no edge) | detection_delay_seconds->primary_pop_outage | detection_delay_seconds->primary_pop_outage | detection_delay_seconds->primary_pop_outage | no edge | (detection_delay_seconds, primary_pop_outage)=A |
| client_region, primary_pop_outage | client_region   primary_pop_outage (no edge) | client_region   primary_pop_outage (no edge) | client_region->primary_pop_outage | client_region->primary_pop_outage | client_region->primary_pop_outage | no edge | (client_region, primary_pop_outage)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
