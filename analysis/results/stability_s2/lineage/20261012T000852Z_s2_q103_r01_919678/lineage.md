# Edge lineage: 20261012T000852Z_s2_q103_r01_919678

Dataset `/research/datasets/suite_q1s2/q103/q103.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 22 | 0.86 | 0.42 | 0.57 | 6 | 3 | 10 | 44 |
| S1 after bootstrap edits | 12 | 0.92 | 0.24 | 0.39 | 5 | 1 | 5 | 43 |
| S2 after LLM review | 46 | 0.24 | 0.24 | 0.24 | 6 | 2 | 3 | 76 |
| S3 after KCI pruning | 41 | 0.27 | 0.24 | 0.26 | 6 | 2 | 3 | 71 |
| S4 final (after cycle step) | 41 | 0.27 | 0.24 | 0.26 | 6 | 2 | 3 | 71 |

Scored against: reference graph s2_10_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 10. Of the deleted, 1 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 28, "B": 11, "C": 110, "D": 151}.
- LLM effect: added 37 (of which 34 where the resamples showed no edge at frequency >= 0.9), removed 3, re-oriented 1.
- KCI step removed 5. Cycle step changed 0.
- Final graph: 41 edges; set by {"llm": 33, "algorithm (unchanged)": 8}; 8 identical to the algorithm's output; 31 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| v_review_staff->v_permits_posted_obs | llm | no | 0.95 |
| v_review_staff->v_permit_apps_true | llm | no | 1.00 |
| v_review_staff->v_permit_backlog | llm | no | 1.00 |
| v_review_staff->v_permit_approvals_true | llm | no | 0.95 |
| v_zoning_far->v_rent_true | llm | no | 1.00 |
| v_measured_noise_dba->v_zoning_far | algorithm (unchanged) | yes | 0.40 |
| v_zoning_far->v_asking_rent_obs | llm | no | 1.00 |
| v_zoning_far->v_school_quality_score | algorithm (unchanged) | yes | 0.05 |
| v_station_open->v_rent_true | llm | no | 0.95 |
| v_station_open->v_job_access_45m | llm | no | 0.65 |
| v_station_open->v_walk_time_min | llm | no | 1.00 |
| v_station_open->v_vacancy_rate | llm | no | 1.00 |
| v_station_open->v_spatial_spillover_idx | llm | no | 1.00 |
| v_station_open->v_asking_rent_obs | llm | no | 0.95 |
| v_station_open->v_service_freq_tph | llm | no | 0.95 |
| v_true_noise_dba->v_noise_complaints | llm | no | 1.00 |
| v_noise_complaints o-o v_permit_backlog | algorithm (unchanged) | yes | 0.00 |
| v_platform_adoption->v_true_noise_dba | algorithm (unchanged) | yes | 0.00 |
| v_vacancy_rate->v_rent_true | llm | no | 1.00 |
| v_asking_rent_obs->v_rent_true | llm | no | 1.00 |
| v_school_quality_score->v_rent_true | llm | no | 1.00 |
| v_interest_rate_ann o-> v_permits_posted_obs | algorithm (unchanged) | yes | 0.00 |
| v_permits_posted_obs->v_permit_backlog | llm | yes | 0.05 |
| v_permit_approvals_true->v_permits_posted_obs | llm | no | 1.00 |
| v_job_access_45m->v_walk_time_min | llm | no | 0.95 |
| v_job_access_45m->v_vacancy_rate | llm | no | 1.00 |
| v_job_access_45m->v_asking_rent_obs | llm | no | 0.90 |
| v_job_access_45m->v_service_freq_tph | llm | no | 1.00 |
| v_permit_apps_true->v_permit_backlog | llm | no | 1.00 |
| v_permit_apps_true->v_permit_approvals_true | llm | no | 0.95 |
| v_noise_barrier->v_measured_noise_dba | llm | no | 1.00 |
| v_noise_barrier->v_true_noise_dba | llm | no | 1.00 |
| v_measured_noise_dba->v_listing_coverage | algorithm (unchanged) | yes | 0.35 |
| v_measured_noise_dba->v_true_noise_dba | llm | no | 0.95 |
| v_interest_rate_ann->v_vacancy_rate | llm | no | 0.80 |
| v_interest_rate_ann->v_asking_rent_obs | llm | yes | 0.70 |
| v_vacancy_rate->v_asking_rent_obs | llm | no | 1.00 |
| v_asking_rent_obs->v_school_quality_score | llm | no | 1.00 |
| v_permit_approvals_true->v_permit_backlog | llm | no | 0.95 |
| v_permit_approvals_true o-o v_season_regime | algorithm (unchanged) | yes | 0.60 |
| v_permit_approvals_true o-> v_school_quality_score | algorithm (unchanged) | yes | 0.25 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| v_review_staff, v_permits_posted_obs | v_review_staff   v_permits_posted_obs (no edge) | v_review_staff   v_permits_posted_obs (no edge) | v_review_staff->v_permits_posted_obs | v_review_staff->v_permits_posted_obs | v_review_staff->v_permits_posted_obs | no edge | (v_review_staff, v_permits_posted_obs)=A |
| v_review_staff, v_permit_apps_true | v_review_staff   v_permit_apps_true (no edge) | v_review_staff   v_permit_apps_true (no edge) | v_review_staff->v_permit_apps_true | v_review_staff->v_permit_apps_true | v_review_staff->v_permit_apps_true | no edge | (v_review_staff, v_permit_apps_true)=A |
| v_review_staff, v_permit_backlog | v_review_staff   v_permit_backlog (no edge) | v_review_staff   v_permit_backlog (no edge) | v_review_staff->v_permit_backlog | v_review_staff->v_permit_backlog | v_review_staff->v_permit_backlog | no edge | (v_review_staff, v_permit_backlog)=A |
| v_review_staff, v_permit_approvals_true | v_review_staff   v_permit_approvals_true (no edge) | v_review_staff   v_permit_approvals_true (no edge) | v_review_staff->v_permit_approvals_true | v_review_staff->v_permit_approvals_true | v_review_staff->v_permit_approvals_true | no edge | (v_review_staff, v_permit_approvals_true)=A |
| v_zoning_far, v_rent_true | v_zoning_far   v_rent_true (no edge) | v_zoning_far   v_rent_true (no edge) | v_zoning_far->v_rent_true | v_zoning_far->v_rent_true | v_zoning_far->v_rent_true | no edge | (v_zoning_far, v_rent_true)=A |
| v_zoning_far, v_asking_rent_obs | v_zoning_far   v_asking_rent_obs (no edge) | v_zoning_far   v_asking_rent_obs (no edge) | v_zoning_far->v_asking_rent_obs | v_zoning_far->v_asking_rent_obs | v_zoning_far->v_asking_rent_obs | no edge | (v_zoning_far, v_asking_rent_obs)=A |
| v_station_open, v_rent_true | v_station_open   v_rent_true (no edge) | v_station_open   v_rent_true (no edge) | v_station_open->v_rent_true | v_station_open->v_rent_true | v_station_open->v_rent_true | no edge | (v_station_open, v_rent_true)=A |
| v_station_open, v_job_access_45m | v_station_open   v_job_access_45m (no edge) | v_station_open   v_job_access_45m (no edge) | v_station_open->v_job_access_45m | v_station_open->v_job_access_45m | v_station_open->v_job_access_45m | no edge | (v_station_open, v_job_access_45m)=A |
| v_station_open, v_walk_time_min | v_station_open   v_walk_time_min (no edge) | v_station_open   v_walk_time_min (no edge) | v_station_open->v_walk_time_min | v_station_open->v_walk_time_min | v_station_open->v_walk_time_min | no edge | (v_station_open, v_walk_time_min)=A |
| v_station_open, v_vacancy_rate | v_station_open   v_vacancy_rate (no edge) | v_station_open   v_vacancy_rate (no edge) | v_station_open->v_vacancy_rate | v_station_open->v_vacancy_rate | v_station_open->v_vacancy_rate | v_vacancy_rate -> v_station_open | (v_station_open, v_vacancy_rate)=A |
| v_station_open, v_spatial_spillover_idx | v_station_open   v_spatial_spillover_idx (no edge) | v_station_open   v_spatial_spillover_idx (no edge) | v_station_open->v_spatial_spillover_idx | v_station_open->v_spatial_spillover_idx | v_station_open->v_spatial_spillover_idx | no edge | (v_station_open, v_spatial_spillover_idx)=A |
| v_station_open, v_asking_rent_obs | v_station_open   v_asking_rent_obs (no edge) | v_station_open   v_asking_rent_obs (no edge) | v_station_open->v_asking_rent_obs | v_station_open->v_asking_rent_obs | v_station_open->v_asking_rent_obs | no edge | (v_station_open, v_asking_rent_obs)=A |
| v_station_open, v_service_freq_tph | v_station_open   v_service_freq_tph (no edge) | v_station_open   v_service_freq_tph (no edge) | v_station_open->v_service_freq_tph | v_station_open->v_service_freq_tph | v_station_open->v_service_freq_tph | no edge | (v_station_open, v_service_freq_tph)=A |
| v_noise_complaints, v_permits_posted_obs | v_noise_complaints o-> v_permits_posted_obs | v_noise_complaints   v_permits_posted_obs (no edge) | v_noise_complaints   v_permits_posted_obs (no edge) | v_noise_complaints   v_permits_posted_obs (no edge) | v_noise_complaints   v_permits_posted_obs (no edge) | v_noise_complaints -> v_permits_posted_obs | (v_noise_complaints, v_permits_posted_obs)=D |
| v_noise_complaints, v_noise_barrier | v_noise_complaints   v_noise_barrier (no edge) | v_noise_complaints   v_noise_barrier (no edge) | v_noise_barrier->v_noise_complaints | v_noise_complaints   v_noise_barrier (no edge) | v_noise_complaints   v_noise_barrier (no edge) | no edge | (v_noise_complaints, v_noise_barrier)=B |
| v_noise_complaints, v_measured_noise_dba | v_noise_complaints   v_measured_noise_dba (no edge) | v_noise_complaints   v_measured_noise_dba (no edge) | v_measured_noise_dba->v_noise_complaints | v_noise_complaints   v_measured_noise_dba (no edge) | v_noise_complaints   v_measured_noise_dba (no edge) | no edge | (v_noise_complaints, v_measured_noise_dba)=B |
| v_noise_complaints, v_true_noise_dba | v_noise_complaints   v_true_noise_dba (no edge) | v_noise_complaints   v_true_noise_dba (no edge) | v_true_noise_dba->v_noise_complaints | v_true_noise_dba->v_noise_complaints | v_true_noise_dba->v_noise_complaints | no edge | (v_noise_complaints, v_true_noise_dba)=B |
| v_platform_adoption, v_vacancy_rate | v_vacancy_rate->v_platform_adoption | v_platform_adoption   v_vacancy_rate (no edge) | v_platform_adoption   v_vacancy_rate (no edge) | v_platform_adoption   v_vacancy_rate (no edge) | v_platform_adoption   v_vacancy_rate (no edge) | v_vacancy_rate -> v_platform_adoption | (v_platform_adoption, v_vacancy_rate)=D |
| v_platform_adoption, v_asking_rent_obs | v_platform_adoption <-> v_asking_rent_obs | v_platform_adoption   v_asking_rent_obs (no edge) | v_platform_adoption   v_asking_rent_obs (no edge) | v_platform_adoption   v_asking_rent_obs (no edge) | v_platform_adoption   v_asking_rent_obs (no edge) | v_asking_rent_obs -> v_platform_adoption | (v_platform_adoption, v_asking_rent_obs)=D |
| v_rent_true, v_job_access_45m | v_rent_true   v_job_access_45m (no edge) | v_rent_true   v_job_access_45m (no edge) | v_job_access_45m->v_rent_true | v_rent_true   v_job_access_45m (no edge) | v_rent_true   v_job_access_45m (no edge) | no edge | (v_rent_true, v_job_access_45m)=B |
| v_rent_true, v_construction_cost_idx | v_rent_true o-> v_construction_cost_idx | v_rent_true   v_construction_cost_idx (no edge) | v_rent_true   v_construction_cost_idx (no edge) | v_rent_true   v_construction_cost_idx (no edge) | v_rent_true   v_construction_cost_idx (no edge) | v_rent_true -> v_construction_cost_idx | (v_rent_true, v_construction_cost_idx)=C |
| v_rent_true, v_measured_noise_dba | v_rent_true->v_measured_noise_dba | v_rent_true   v_measured_noise_dba (no edge) | v_rent_true   v_measured_noise_dba (no edge) | v_rent_true   v_measured_noise_dba (no edge) | v_rent_true   v_measured_noise_dba (no edge) | v_measured_noise_dba -> v_rent_true | (v_rent_true, v_measured_noise_dba)=C |
| v_rent_true, v_interest_rate_ann | v_rent_true   v_interest_rate_ann (no edge) | v_rent_true   v_interest_rate_ann (no edge) | v_interest_rate_ann->v_rent_true | v_rent_true   v_interest_rate_ann (no edge) | v_rent_true   v_interest_rate_ann (no edge) | no edge | (v_rent_true, v_interest_rate_ann)=B |
| v_rent_true, v_vacancy_rate | v_rent_true   v_vacancy_rate (no edge) | v_rent_true   v_vacancy_rate (no edge) | v_vacancy_rate->v_rent_true | v_vacancy_rate->v_rent_true | v_vacancy_rate->v_rent_true | no edge | (v_rent_true, v_vacancy_rate)=B |
| v_rent_true, v_asking_rent_obs | v_rent_true   v_asking_rent_obs (no edge) | v_rent_true   v_asking_rent_obs (no edge) | v_asking_rent_obs->v_rent_true | v_asking_rent_obs->v_rent_true | v_asking_rent_obs->v_rent_true | no edge | (v_rent_true, v_asking_rent_obs)=B |
| v_rent_true, v_school_quality_score | v_rent_true   v_school_quality_score (no edge) | v_rent_true   v_school_quality_score (no edge) | v_school_quality_score->v_rent_true | v_school_quality_score->v_rent_true | v_school_quality_score->v_rent_true | no edge | (v_rent_true, v_school_quality_score)=B |
| v_permits_posted_obs, v_permit_apps_true | v_permits_posted_obs   v_permit_apps_true (no edge) | v_permits_posted_obs   v_permit_apps_true (no edge) | v_permit_apps_true->v_permits_posted_obs | v_permits_posted_obs   v_permit_apps_true (no edge) | v_permits_posted_obs   v_permit_apps_true (no edge) | no edge | (v_permits_posted_obs, v_permit_apps_true)=B |
| v_permits_posted_obs, v_permit_backlog | v_permit_backlog o-> v_permits_posted_obs | v_permit_backlog o-> v_permits_posted_obs | v_permits_posted_obs->v_permit_backlog | v_permits_posted_obs->v_permit_backlog | v_permits_posted_obs->v_permit_backlog | v_permit_backlog -> v_permits_posted_obs | (v_permits_posted_obs, v_permit_backlog)=A |
| v_permits_posted_obs, v_permit_approvals_true | v_permits_posted_obs   v_permit_approvals_true (no edge) | v_permits_posted_obs   v_permit_approvals_true (no edge) | v_permit_approvals_true->v_permits_posted_obs | v_permit_approvals_true->v_permits_posted_obs | v_permit_approvals_true->v_permits_posted_obs | no edge | (v_permits_posted_obs, v_permit_approvals_true)=B |
| v_job_access_45m, v_walk_time_min | v_job_access_45m   v_walk_time_min (no edge) | v_job_access_45m   v_walk_time_min (no edge) | v_job_access_45m->v_walk_time_min | v_job_access_45m->v_walk_time_min | v_job_access_45m->v_walk_time_min | no edge | (v_job_access_45m, v_walk_time_min)=A |
| v_job_access_45m, v_vacancy_rate | v_job_access_45m   v_vacancy_rate (no edge) | v_job_access_45m   v_vacancy_rate (no edge) | v_job_access_45m->v_vacancy_rate | v_job_access_45m->v_vacancy_rate | v_job_access_45m->v_vacancy_rate | no edge | (v_job_access_45m, v_vacancy_rate)=A |
| v_job_access_45m, v_asking_rent_obs | v_job_access_45m   v_asking_rent_obs (no edge) | v_job_access_45m   v_asking_rent_obs (no edge) | v_job_access_45m->v_asking_rent_obs | v_job_access_45m->v_asking_rent_obs | v_job_access_45m->v_asking_rent_obs | no edge | (v_job_access_45m, v_asking_rent_obs)=A |
| v_job_access_45m, v_service_freq_tph | v_job_access_45m   v_service_freq_tph (no edge) | v_job_access_45m   v_service_freq_tph (no edge) | v_job_access_45m->v_service_freq_tph | v_job_access_45m->v_service_freq_tph | v_job_access_45m->v_service_freq_tph | no edge | (v_job_access_45m, v_service_freq_tph)=A |
| v_permit_apps_true, v_permit_backlog | v_permit_apps_true   v_permit_backlog (no edge) | v_permit_apps_true   v_permit_backlog (no edge) | v_permit_apps_true->v_permit_backlog | v_permit_apps_true->v_permit_backlog | v_permit_apps_true->v_permit_backlog | no edge | (v_permit_apps_true, v_permit_backlog)=A |
| v_permit_apps_true, v_service_freq_tph | v_permit_apps_true o-> v_service_freq_tph | v_permit_apps_true   v_service_freq_tph (no edge) | v_permit_apps_true   v_service_freq_tph (no edge) | v_permit_apps_true   v_service_freq_tph (no edge) | v_permit_apps_true   v_service_freq_tph (no edge) | no edge | (v_permit_apps_true, v_service_freq_tph)=D |
| v_permit_apps_true, v_permit_approvals_true | v_permit_apps_true   v_permit_approvals_true (no edge) | v_permit_apps_true   v_permit_approvals_true (no edge) | v_permit_apps_true->v_permit_approvals_true | v_permit_apps_true->v_permit_approvals_true | v_permit_apps_true->v_permit_approvals_true | no edge | (v_permit_apps_true, v_permit_approvals_true)=A |
| v_noise_barrier, v_measured_noise_dba | v_noise_barrier   v_measured_noise_dba (no edge) | v_noise_barrier   v_measured_noise_dba (no edge) | v_noise_barrier->v_measured_noise_dba | v_noise_barrier->v_measured_noise_dba | v_noise_barrier->v_measured_noise_dba | no edge | (v_noise_barrier, v_measured_noise_dba)=A |
| v_noise_barrier, v_true_noise_dba | v_noise_barrier   v_true_noise_dba (no edge) | v_noise_barrier   v_true_noise_dba (no edge) | v_noise_barrier->v_true_noise_dba | v_noise_barrier->v_true_noise_dba | v_noise_barrier->v_true_noise_dba | no edge | (v_noise_barrier, v_true_noise_dba)=A |
| v_noise_barrier, v_season_regime | v_noise_barrier o-o v_season_regime | v_noise_barrier o-o v_season_regime | v_noise_barrier   v_season_regime (no edge) | v_noise_barrier   v_season_regime (no edge) | v_noise_barrier   v_season_regime (no edge) | v_noise_barrier -> v_season_regime | (v_noise_barrier, v_season_regime)=C |
| v_construction_cost_idx, v_measured_noise_dba | v_construction_cost_idx->v_measured_noise_dba | v_construction_cost_idx->v_measured_noise_dba | v_construction_cost_idx   v_measured_noise_dba (no edge) | v_construction_cost_idx   v_measured_noise_dba (no edge) | v_construction_cost_idx   v_measured_noise_dba (no edge) | v_measured_noise_dba -> v_construction_cost_idx | (v_construction_cost_idx, v_measured_noise_dba)=C |
| v_construction_cost_idx, v_spatial_spillover_idx | v_spatial_spillover_idx o-> v_construction_cost_idx | v_construction_cost_idx   v_spatial_spillover_idx (no edge) | v_construction_cost_idx   v_spatial_spillover_idx (no edge) | v_construction_cost_idx   v_spatial_spillover_idx (no edge) | v_construction_cost_idx   v_spatial_spillover_idx (no edge) | v_spatial_spillover_idx -> v_construction_cost_idx | (v_construction_cost_idx, v_spatial_spillover_idx)=D |
| v_measured_noise_dba, v_true_noise_dba | v_measured_noise_dba   v_true_noise_dba (no edge) | v_measured_noise_dba   v_true_noise_dba (no edge) | v_measured_noise_dba->v_true_noise_dba | v_measured_noise_dba->v_true_noise_dba | v_measured_noise_dba->v_true_noise_dba | no edge | (v_measured_noise_dba, v_true_noise_dba)=A |
| v_interest_rate_ann, v_vacancy_rate | v_interest_rate_ann   v_vacancy_rate (no edge) | v_interest_rate_ann   v_vacancy_rate (no edge) | v_interest_rate_ann->v_vacancy_rate | v_interest_rate_ann->v_vacancy_rate | v_interest_rate_ann->v_vacancy_rate | v_interest_rate_ann -> v_vacancy_rate | (v_interest_rate_ann, v_vacancy_rate)=A |
| v_interest_rate_ann, v_asking_rent_obs | v_interest_rate_ann o-> v_asking_rent_obs | v_interest_rate_ann   v_asking_rent_obs (no edge) | v_interest_rate_ann->v_asking_rent_obs | v_interest_rate_ann->v_asking_rent_obs | v_interest_rate_ann->v_asking_rent_obs | v_interest_rate_ann -> v_asking_rent_obs | (v_interest_rate_ann, v_asking_rent_obs)=A |
| v_vacancy_rate, v_asking_rent_obs | v_vacancy_rate   v_asking_rent_obs (no edge) | v_vacancy_rate   v_asking_rent_obs (no edge) | v_vacancy_rate->v_asking_rent_obs | v_vacancy_rate->v_asking_rent_obs | v_vacancy_rate->v_asking_rent_obs | no edge | (v_vacancy_rate, v_asking_rent_obs)=A |
| v_vacancy_rate, v_service_freq_tph | v_service_freq_tph->v_vacancy_rate | v_vacancy_rate   v_service_freq_tph (no edge) | v_vacancy_rate   v_service_freq_tph (no edge) | v_vacancy_rate   v_service_freq_tph (no edge) | v_vacancy_rate   v_service_freq_tph (no edge) | v_vacancy_rate -> v_service_freq_tph | (v_vacancy_rate, v_service_freq_tph)=D |
| v_asking_rent_obs, v_school_quality_score | v_asking_rent_obs   v_school_quality_score (no edge) | v_asking_rent_obs   v_school_quality_score (no edge) | v_asking_rent_obs->v_school_quality_score | v_asking_rent_obs->v_school_quality_score | v_asking_rent_obs->v_school_quality_score | no edge | (v_asking_rent_obs, v_school_quality_score)=A |
| v_permit_backlog, v_service_freq_tph | v_permit_backlog->v_service_freq_tph | v_permit_backlog   v_service_freq_tph (no edge) | v_permit_backlog   v_service_freq_tph (no edge) | v_permit_backlog   v_service_freq_tph (no edge) | v_permit_backlog   v_service_freq_tph (no edge) | no edge | (v_permit_backlog, v_service_freq_tph)=C |
| v_permit_backlog, v_permit_approvals_true | v_permit_backlog   v_permit_approvals_true (no edge) | v_permit_backlog   v_permit_approvals_true (no edge) | v_permit_approvals_true->v_permit_backlog | v_permit_approvals_true->v_permit_backlog | v_permit_approvals_true->v_permit_backlog | no edge | (v_permit_backlog, v_permit_approvals_true)=B |
| v_season_regime, v_school_quality_score | v_season_regime->v_school_quality_score | v_season_regime->v_school_quality_score | v_season_regime   v_school_quality_score (no edge) | v_season_regime   v_school_quality_score (no edge) | v_season_regime   v_school_quality_score (no edge) | v_season_regime -> v_school_quality_score | (v_season_regime, v_school_quality_score)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
