# Edge lineage: 20261014T042200Z_ab06cc_q103_r01_3b125f

Dataset `/research/datasets/suite_q1s2/q103/q103.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 2}. 25 variables, 300 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 21 | 0.76 | 0.36 | 0.48 | 3 | 2 | 11 | 48 |
| S1 after bootstrap edits | 12 | 0.92 | 0.24 | 0.39 | 3 | 2 | 6 | 44 |
| S2 after LLM review | 56 | 0.18 | 0.22 | 0.20 | 8 | 2 | 0 | 84 |
| S3 after KCI pruning | 55 | 0.18 | 0.22 | 0.20 | 8 | 2 | 0 | 83 |
| S4 final (after cycle step) | 55 | 0.18 | 0.22 | 0.20 | 8 | 2 | 0 | 83 |

Scored against: reference graph s2_10_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 1, deleted 9. Of the deleted, 3 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 25 calls, 300 distinct pairs answered out of 300, plus 25 self-pairs. Letters: {"A": 54, "B": 1, "C": 231, "D": 14}.
- LLM effect: added 49 (of which 42 where the resamples showed no edge at frequency >= 0.9), removed 5, re-oriented 4.
- KCI step removed 1. Cycle step changed 0.
- Final graph: 55 edges; set by {"llm": 52, "algorithm (unchanged)": 3}; 3 identical to the algorithm's output; 47 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| v_review_staff->v_permits_posted_obs | llm | no | 0.90 |
| v_review_staff->v_permit_apps_true | llm | no | 1.00 |
| v_review_staff->v_permit_backlog | llm | no | 1.00 |
| v_review_staff->v_permit_approvals_true | llm | no | 1.00 |
| v_zoning_far->v_rent_true | llm | no | 1.00 |
| v_zoning_far->v_permits_posted_obs | llm | no | 1.00 |
| v_zoning_far->v_permit_apps_true | llm | no | 1.00 |
| v_zoning_far->v_construction_cost_idx | llm | no | 0.60 |
| v_zoning_far->v_listing_coverage | llm | no | 1.00 |
| v_zoning_far->v_vacancy_rate | llm | no | 1.00 |
| v_zoning_far->v_asking_rent_obs | llm | no | 1.00 |
| v_zoning_far->v_permit_backlog | llm | no | 1.00 |
| v_zoning_far->v_permit_approvals_true | llm | no | 1.00 |
| v_station_open->v_rent_true | llm | no | 0.95 |
| v_station_open->v_job_access_45m | llm | yes | 0.65 |
| v_station_open->v_asking_rent_obs | llm | no | 1.00 |
| v_station_open->v_service_freq_tph | llm | no | 0.90 |
| v_noise_complaints->v_noise_barrier | llm | no | 1.00 |
| v_noise_complaints->v_measured_noise_dba | llm | no | 1.00 |
| v_noise_complaints->v_true_noise_dba | llm | no | 1.00 |
| v_noise_complaints->v_permit_backlog | llm | yes | 0.00 |
| v_platform_adoption->v_job_access_45m | llm | no | 1.00 |
| v_platform_adoption->v_service_freq_tph | llm | no | 0.95 |
| v_rent_true->v_construction_cost_idx | llm | yes | 0.00 |
| v_measured_noise_dba->v_rent_true | algorithm (unchanged) | yes | 0.45 |
| v_rent_true->v_interest_rate_ann | llm | no | 1.00 |
| v_rent_true->v_vacancy_rate | llm | no | 1.00 |
| v_rent_true->v_asking_rent_obs | llm | no | 1.00 |
| v_permits_posted_obs->v_permit_apps_true | llm | no | 1.00 |
| v_permits_posted_obs->v_permit_backlog | llm | yes | 0.00 |
| v_permits_posted_obs->v_permit_approvals_true | llm | no | 1.00 |
| v_job_access_45m->v_vacancy_rate | llm | no | 1.00 |
| v_job_access_45m->v_asking_rent_obs | llm | no | 0.95 |
| v_job_access_45m->v_service_freq_tph | llm | no | 1.00 |
| v_permit_apps_true->v_permit_backlog | llm | no | 0.95 |
| v_permit_apps_true->v_permit_approvals_true | llm | no | 1.00 |
| v_noise_barrier->v_measured_noise_dba | llm | no | 1.00 |
| v_noise_barrier->v_true_noise_dba | llm | no | 1.00 |
| v_construction_cost_idx->v_vacancy_rate | llm | no | 1.00 |
| v_construction_cost_idx->v_asking_rent_obs | llm | no | 1.00 |
| v_construction_cost_idx->v_permit_backlog | llm | no | 1.00 |
| v_construction_cost_idx->v_permit_approvals_true | llm | no | 0.85 |
| v_listing_coverage->v_vacancy_rate | llm | no | 1.00 |
| v_listing_coverage->v_asking_rent_obs | llm | no | 1.00 |
| v_measured_noise_dba->v_vacancy_rate | llm | no | 1.00 |
| v_measured_noise_dba->v_asking_rent_obs | llm | no | 1.00 |
| v_measured_noise_dba->v_true_noise_dba | algorithm (unchanged) | yes | 0.75 |
| v_interest_rate_ann->v_vacancy_rate | llm | no | 0.75 |
| v_interest_rate_ann->v_asking_rent_obs | llm | no | 0.35 |
| v_vacancy_rate->v_asking_rent_obs | llm | no | 1.00 |
| v_vacancy_rate->v_permit_backlog | llm | yes | 0.30 |
| v_spatial_spillover_idx->v_asking_rent_obs | llm | no | 0.85 |
| v_asking_rent_obs->v_school_quality_score | llm | no | 1.00 |
| v_permit_backlog->v_permit_approvals_true | llm | no | 0.85 |
| v_season_regime->v_school_quality_score | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| v_review_staff, v_permits_posted_obs | v_review_staff   v_permits_posted_obs (no edge) | v_review_staff   v_permits_posted_obs (no edge) | v_review_staff->v_permits_posted_obs | v_review_staff->v_permits_posted_obs | v_review_staff->v_permits_posted_obs | no edge | (v_review_staff, v_permits_posted_obs)=A |
| v_review_staff, v_permit_apps_true | v_review_staff   v_permit_apps_true (no edge) | v_review_staff   v_permit_apps_true (no edge) | v_review_staff->v_permit_apps_true | v_review_staff->v_permit_apps_true | v_review_staff->v_permit_apps_true | no edge | (v_review_staff, v_permit_apps_true)=A |
| v_review_staff, v_permit_backlog | v_review_staff   v_permit_backlog (no edge) | v_review_staff   v_permit_backlog (no edge) | v_review_staff->v_permit_backlog | v_review_staff->v_permit_backlog | v_review_staff->v_permit_backlog | no edge | (v_review_staff, v_permit_backlog)=A |
| v_review_staff, v_permit_approvals_true | v_review_staff   v_permit_approvals_true (no edge) | v_review_staff   v_permit_approvals_true (no edge) | v_review_staff->v_permit_approvals_true | v_review_staff->v_permit_approvals_true | v_review_staff->v_permit_approvals_true | no edge | (v_review_staff, v_permit_approvals_true)=A |
| v_zoning_far, v_rent_true | v_zoning_far   v_rent_true (no edge) | v_zoning_far   v_rent_true (no edge) | v_zoning_far->v_rent_true | v_zoning_far->v_rent_true | v_zoning_far->v_rent_true | no edge | (v_zoning_far, v_rent_true)=A |
| v_zoning_far, v_permits_posted_obs | v_zoning_far   v_permits_posted_obs (no edge) | v_zoning_far   v_permits_posted_obs (no edge) | v_zoning_far->v_permits_posted_obs | v_zoning_far->v_permits_posted_obs | v_zoning_far->v_permits_posted_obs | no edge | (v_zoning_far, v_permits_posted_obs)=A |
| v_zoning_far, v_permit_apps_true | v_zoning_far   v_permit_apps_true (no edge) | v_zoning_far   v_permit_apps_true (no edge) | v_zoning_far->v_permit_apps_true | v_zoning_far->v_permit_apps_true | v_zoning_far->v_permit_apps_true | no edge | (v_zoning_far, v_permit_apps_true)=A |
| v_zoning_far, v_construction_cost_idx | v_zoning_far   v_construction_cost_idx (no edge) | v_zoning_far   v_construction_cost_idx (no edge) | v_zoning_far->v_construction_cost_idx | v_zoning_far->v_construction_cost_idx | v_zoning_far->v_construction_cost_idx | no edge | (v_zoning_far, v_construction_cost_idx)=A |
| v_zoning_far, v_listing_coverage | v_zoning_far   v_listing_coverage (no edge) | v_zoning_far   v_listing_coverage (no edge) | v_zoning_far->v_listing_coverage | v_zoning_far->v_listing_coverage | v_zoning_far->v_listing_coverage | no edge | (v_zoning_far, v_listing_coverage)=A |
| v_zoning_far, v_vacancy_rate | v_zoning_far   v_vacancy_rate (no edge) | v_zoning_far   v_vacancy_rate (no edge) | v_zoning_far->v_vacancy_rate | v_zoning_far->v_vacancy_rate | v_zoning_far->v_vacancy_rate | no edge | (v_zoning_far, v_vacancy_rate)=A |
| v_zoning_far, v_asking_rent_obs | v_zoning_far   v_asking_rent_obs (no edge) | v_zoning_far   v_asking_rent_obs (no edge) | v_zoning_far->v_asking_rent_obs | v_zoning_far->v_asking_rent_obs | v_zoning_far->v_asking_rent_obs | no edge | (v_zoning_far, v_asking_rent_obs)=A |
| v_zoning_far, v_permit_backlog | v_zoning_far   v_permit_backlog (no edge) | v_zoning_far   v_permit_backlog (no edge) | v_zoning_far->v_permit_backlog | v_zoning_far->v_permit_backlog | v_zoning_far->v_permit_backlog | no edge | (v_zoning_far, v_permit_backlog)=A |
| v_zoning_far, v_permit_approvals_true | v_zoning_far   v_permit_approvals_true (no edge) | v_zoning_far   v_permit_approvals_true (no edge) | v_zoning_far->v_permit_approvals_true | v_zoning_far->v_permit_approvals_true | v_zoning_far->v_permit_approvals_true | v_zoning_far -> v_permit_approvals_true | (v_zoning_far, v_permit_approvals_true)=A |
| v_zoning_far, v_school_quality_score | v_zoning_far o-> v_school_quality_score | v_zoning_far o-> v_school_quality_score | v_zoning_far   v_school_quality_score (no edge) | v_zoning_far   v_school_quality_score (no edge) | v_zoning_far   v_school_quality_score (no edge) | v_zoning_far -> v_school_quality_score | (v_zoning_far, v_school_quality_score)=C |
| v_station_open, v_rent_true | v_station_open   v_rent_true (no edge) | v_station_open   v_rent_true (no edge) | v_station_open->v_rent_true | v_station_open->v_rent_true | v_station_open->v_rent_true | no edge | (v_station_open, v_rent_true)=A |
| v_station_open, v_job_access_45m | v_station_open o-o v_job_access_45m | v_station_open   v_job_access_45m (no edge) | v_station_open->v_job_access_45m | v_station_open->v_job_access_45m | v_station_open->v_job_access_45m | no edge | (v_station_open, v_job_access_45m)=A |
| v_station_open, v_asking_rent_obs | v_station_open   v_asking_rent_obs (no edge) | v_station_open   v_asking_rent_obs (no edge) | v_station_open->v_asking_rent_obs | v_station_open->v_asking_rent_obs | v_station_open->v_asking_rent_obs | no edge | (v_station_open, v_asking_rent_obs)=A |
| v_station_open, v_service_freq_tph | v_station_open   v_service_freq_tph (no edge) | v_station_open   v_service_freq_tph (no edge) | v_station_open->v_service_freq_tph | v_station_open->v_service_freq_tph | v_station_open->v_service_freq_tph | no edge | (v_station_open, v_service_freq_tph)=A |
| v_noise_complaints, v_permits_posted_obs | v_noise_complaints <-> v_permits_posted_obs | v_noise_complaints   v_permits_posted_obs (no edge) | v_noise_complaints   v_permits_posted_obs (no edge) | v_noise_complaints   v_permits_posted_obs (no edge) | v_noise_complaints   v_permits_posted_obs (no edge) | v_noise_complaints -> v_permits_posted_obs | (v_noise_complaints, v_permits_posted_obs)=C |
| v_noise_complaints, v_noise_barrier | v_noise_complaints   v_noise_barrier (no edge) | v_noise_complaints   v_noise_barrier (no edge) | v_noise_complaints->v_noise_barrier | v_noise_complaints->v_noise_barrier | v_noise_complaints->v_noise_barrier | no edge | (v_noise_complaints, v_noise_barrier)=A |
| v_noise_complaints, v_measured_noise_dba | v_noise_complaints   v_measured_noise_dba (no edge) | v_noise_complaints   v_measured_noise_dba (no edge) | v_noise_complaints->v_measured_noise_dba | v_noise_complaints->v_measured_noise_dba | v_noise_complaints->v_measured_noise_dba | no edge | (v_noise_complaints, v_measured_noise_dba)=A |
| v_noise_complaints, v_true_noise_dba | v_noise_complaints   v_true_noise_dba (no edge) | v_noise_complaints   v_true_noise_dba (no edge) | v_noise_complaints->v_true_noise_dba | v_noise_complaints->v_true_noise_dba | v_noise_complaints->v_true_noise_dba | no edge | (v_noise_complaints, v_true_noise_dba)=A |
| v_noise_complaints, v_permit_backlog | v_permit_backlog->v_noise_complaints | v_permit_backlog->v_noise_complaints | v_noise_complaints->v_permit_backlog | v_noise_complaints->v_permit_backlog | v_noise_complaints->v_permit_backlog | v_noise_complaints -> v_permit_backlog | (v_noise_complaints, v_permit_backlog)=A |
| v_platform_adoption, v_job_access_45m | v_platform_adoption   v_job_access_45m (no edge) | v_platform_adoption   v_job_access_45m (no edge) | v_platform_adoption->v_job_access_45m | v_platform_adoption->v_job_access_45m | v_platform_adoption->v_job_access_45m | no edge | (v_platform_adoption, v_job_access_45m)=A |
| v_platform_adoption, v_permit_apps_true | v_permit_apps_true o-> v_platform_adoption | v_platform_adoption   v_permit_apps_true (no edge) | v_platform_adoption   v_permit_apps_true (no edge) | v_platform_adoption   v_permit_apps_true (no edge) | v_platform_adoption   v_permit_apps_true (no edge) | no edge | (v_platform_adoption, v_permit_apps_true)=C |
| v_platform_adoption, v_asking_rent_obs | v_asking_rent_obs o-> v_platform_adoption | v_platform_adoption   v_asking_rent_obs (no edge) | v_platform_adoption   v_asking_rent_obs (no edge) | v_platform_adoption   v_asking_rent_obs (no edge) | v_platform_adoption   v_asking_rent_obs (no edge) | v_asking_rent_obs -> v_platform_adoption | (v_platform_adoption, v_asking_rent_obs)=C |
| v_platform_adoption, v_true_noise_dba | v_platform_adoption <-> v_true_noise_dba | v_platform_adoption   v_true_noise_dba (no edge) | v_platform_adoption   v_true_noise_dba (no edge) | v_platform_adoption   v_true_noise_dba (no edge) | v_platform_adoption   v_true_noise_dba (no edge) | v_platform_adoption -> v_true_noise_dba | (v_platform_adoption, v_true_noise_dba)=C |
| v_platform_adoption, v_service_freq_tph | v_platform_adoption   v_service_freq_tph (no edge) | v_platform_adoption   v_service_freq_tph (no edge) | v_platform_adoption->v_service_freq_tph | v_platform_adoption->v_service_freq_tph | v_platform_adoption->v_service_freq_tph | no edge | (v_platform_adoption, v_service_freq_tph)=A |
| v_rent_true, v_construction_cost_idx | v_construction_cost_idx->v_rent_true | v_construction_cost_idx->v_rent_true | v_rent_true->v_construction_cost_idx | v_rent_true->v_construction_cost_idx | v_rent_true->v_construction_cost_idx | v_rent_true -> v_construction_cost_idx | (v_rent_true, v_construction_cost_idx)=A |
| v_rent_true, v_interest_rate_ann | v_rent_true   v_interest_rate_ann (no edge) | v_rent_true   v_interest_rate_ann (no edge) | v_rent_true->v_interest_rate_ann | v_rent_true->v_interest_rate_ann | v_rent_true->v_interest_rate_ann | no edge | (v_rent_true, v_interest_rate_ann)=A |
| v_rent_true, v_vacancy_rate | v_rent_true   v_vacancy_rate (no edge) | v_rent_true   v_vacancy_rate (no edge) | v_rent_true->v_vacancy_rate | v_rent_true->v_vacancy_rate | v_rent_true->v_vacancy_rate | no edge | (v_rent_true, v_vacancy_rate)=A |
| v_rent_true, v_asking_rent_obs | v_rent_true   v_asking_rent_obs (no edge) | v_rent_true   v_asking_rent_obs (no edge) | v_rent_true->v_asking_rent_obs | v_rent_true->v_asking_rent_obs | v_rent_true->v_asking_rent_obs | no edge | (v_rent_true, v_asking_rent_obs)=A |
| v_permits_posted_obs, v_permit_apps_true | v_permits_posted_obs   v_permit_apps_true (no edge) | v_permits_posted_obs   v_permit_apps_true (no edge) | v_permits_posted_obs->v_permit_apps_true | v_permits_posted_obs->v_permit_apps_true | v_permits_posted_obs->v_permit_apps_true | no edge | (v_permits_posted_obs, v_permit_apps_true)=A |
| v_permits_posted_obs, v_interest_rate_ann | v_interest_rate_ann o-> v_permits_posted_obs | v_interest_rate_ann o-> v_permits_posted_obs | v_permits_posted_obs   v_interest_rate_ann (no edge) | v_permits_posted_obs   v_interest_rate_ann (no edge) | v_permits_posted_obs   v_interest_rate_ann (no edge) | v_interest_rate_ann -> v_permits_posted_obs | (v_permits_posted_obs, v_interest_rate_ann)=C |
| v_permits_posted_obs, v_permit_backlog | v_permits_posted_obs <-> v_permit_backlog | v_permits_posted_obs <-> v_permit_backlog | v_permits_posted_obs->v_permit_backlog | v_permits_posted_obs->v_permit_backlog | v_permits_posted_obs->v_permit_backlog | v_permit_backlog -> v_permits_posted_obs | (v_permits_posted_obs, v_permit_backlog)=A |
| v_permits_posted_obs, v_permit_approvals_true | v_permits_posted_obs   v_permit_approvals_true (no edge) | v_permits_posted_obs   v_permit_approvals_true (no edge) | v_permits_posted_obs->v_permit_approvals_true | v_permits_posted_obs->v_permit_approvals_true | v_permits_posted_obs->v_permit_approvals_true | no edge | (v_permits_posted_obs, v_permit_approvals_true)=A |
| v_job_access_45m, v_walk_time_min | v_job_access_45m   v_walk_time_min (no edge) | v_job_access_45m   v_walk_time_min (no edge) | v_walk_time_min->v_job_access_45m | v_job_access_45m   v_walk_time_min (no edge) | v_job_access_45m   v_walk_time_min (no edge) | no edge | (v_job_access_45m, v_walk_time_min)=B |
| v_job_access_45m, v_vacancy_rate | v_job_access_45m   v_vacancy_rate (no edge) | v_job_access_45m   v_vacancy_rate (no edge) | v_job_access_45m->v_vacancy_rate | v_job_access_45m->v_vacancy_rate | v_job_access_45m->v_vacancy_rate | no edge | (v_job_access_45m, v_vacancy_rate)=A |
| v_job_access_45m, v_asking_rent_obs | v_job_access_45m   v_asking_rent_obs (no edge) | v_job_access_45m   v_asking_rent_obs (no edge) | v_job_access_45m->v_asking_rent_obs | v_job_access_45m->v_asking_rent_obs | v_job_access_45m->v_asking_rent_obs | no edge | (v_job_access_45m, v_asking_rent_obs)=A |
| v_job_access_45m, v_service_freq_tph | v_job_access_45m   v_service_freq_tph (no edge) | v_job_access_45m   v_service_freq_tph (no edge) | v_job_access_45m->v_service_freq_tph | v_job_access_45m->v_service_freq_tph | v_job_access_45m->v_service_freq_tph | no edge | (v_job_access_45m, v_service_freq_tph)=A |
| v_permit_apps_true, v_permit_backlog | v_permit_apps_true   v_permit_backlog (no edge) | v_permit_apps_true   v_permit_backlog (no edge) | v_permit_apps_true->v_permit_backlog | v_permit_apps_true->v_permit_backlog | v_permit_apps_true->v_permit_backlog | no edge | (v_permit_apps_true, v_permit_backlog)=A |
| v_permit_apps_true, v_permit_approvals_true | v_permit_apps_true   v_permit_approvals_true (no edge) | v_permit_apps_true   v_permit_approvals_true (no edge) | v_permit_apps_true->v_permit_approvals_true | v_permit_apps_true->v_permit_approvals_true | v_permit_apps_true->v_permit_approvals_true | no edge | (v_permit_apps_true, v_permit_approvals_true)=A |
| v_noise_barrier, v_measured_noise_dba | v_noise_barrier   v_measured_noise_dba (no edge) | v_noise_barrier   v_measured_noise_dba (no edge) | v_noise_barrier->v_measured_noise_dba | v_noise_barrier->v_measured_noise_dba | v_noise_barrier->v_measured_noise_dba | no edge | (v_noise_barrier, v_measured_noise_dba)=A |
| v_noise_barrier, v_true_noise_dba | v_noise_barrier   v_true_noise_dba (no edge) | v_noise_barrier   v_true_noise_dba (no edge) | v_noise_barrier->v_true_noise_dba | v_noise_barrier->v_true_noise_dba | v_noise_barrier->v_true_noise_dba | no edge | (v_noise_barrier, v_true_noise_dba)=A |
| v_noise_barrier, v_season_regime | v_noise_barrier o-o v_season_regime | v_noise_barrier   v_season_regime (no edge) | v_noise_barrier   v_season_regime (no edge) | v_noise_barrier   v_season_regime (no edge) | v_noise_barrier   v_season_regime (no edge) | v_noise_barrier -> v_season_regime | (v_noise_barrier, v_season_regime)=C |
| v_construction_cost_idx, v_measured_noise_dba | v_measured_noise_dba o-> v_construction_cost_idx | v_measured_noise_dba o-> v_construction_cost_idx | v_construction_cost_idx   v_measured_noise_dba (no edge) | v_construction_cost_idx   v_measured_noise_dba (no edge) | v_construction_cost_idx   v_measured_noise_dba (no edge) | v_measured_noise_dba -> v_construction_cost_idx | (v_construction_cost_idx, v_measured_noise_dba)=C |
| v_construction_cost_idx, v_vacancy_rate | v_construction_cost_idx   v_vacancy_rate (no edge) | v_construction_cost_idx   v_vacancy_rate (no edge) | v_construction_cost_idx->v_vacancy_rate | v_construction_cost_idx->v_vacancy_rate | v_construction_cost_idx->v_vacancy_rate | no edge | (v_construction_cost_idx, v_vacancy_rate)=A |
| v_construction_cost_idx, v_spatial_spillover_idx | v_spatial_spillover_idx o-> v_construction_cost_idx | v_construction_cost_idx   v_spatial_spillover_idx (no edge) | v_construction_cost_idx   v_spatial_spillover_idx (no edge) | v_construction_cost_idx   v_spatial_spillover_idx (no edge) | v_construction_cost_idx   v_spatial_spillover_idx (no edge) | v_spatial_spillover_idx -> v_construction_cost_idx | (v_construction_cost_idx, v_spatial_spillover_idx)=C |
| v_construction_cost_idx, v_asking_rent_obs | v_construction_cost_idx   v_asking_rent_obs (no edge) | v_construction_cost_idx   v_asking_rent_obs (no edge) | v_construction_cost_idx->v_asking_rent_obs | v_construction_cost_idx->v_asking_rent_obs | v_construction_cost_idx->v_asking_rent_obs | no edge | (v_construction_cost_idx, v_asking_rent_obs)=A |
| v_construction_cost_idx, v_permit_backlog | v_construction_cost_idx   v_permit_backlog (no edge) | v_construction_cost_idx   v_permit_backlog (no edge) | v_construction_cost_idx->v_permit_backlog | v_construction_cost_idx->v_permit_backlog | v_construction_cost_idx->v_permit_backlog | no edge | (v_construction_cost_idx, v_permit_backlog)=A |
| v_construction_cost_idx, v_permit_approvals_true | v_construction_cost_idx   v_permit_approvals_true (no edge) | v_construction_cost_idx   v_permit_approvals_true (no edge) | v_construction_cost_idx->v_permit_approvals_true | v_construction_cost_idx->v_permit_approvals_true | v_construction_cost_idx->v_permit_approvals_true | no edge | (v_construction_cost_idx, v_permit_approvals_true)=A |
| v_listing_coverage, v_vacancy_rate | v_listing_coverage   v_vacancy_rate (no edge) | v_listing_coverage   v_vacancy_rate (no edge) | v_listing_coverage->v_vacancy_rate | v_listing_coverage->v_vacancy_rate | v_listing_coverage->v_vacancy_rate | no edge | (v_listing_coverage, v_vacancy_rate)=A |
| v_listing_coverage, v_asking_rent_obs | v_listing_coverage   v_asking_rent_obs (no edge) | v_listing_coverage   v_asking_rent_obs (no edge) | v_listing_coverage->v_asking_rent_obs | v_listing_coverage->v_asking_rent_obs | v_listing_coverage->v_asking_rent_obs | no edge | (v_listing_coverage, v_asking_rent_obs)=A |
| v_measured_noise_dba, v_vacancy_rate | v_measured_noise_dba   v_vacancy_rate (no edge) | v_measured_noise_dba   v_vacancy_rate (no edge) | v_measured_noise_dba->v_vacancy_rate | v_measured_noise_dba->v_vacancy_rate | v_measured_noise_dba->v_vacancy_rate | v_measured_noise_dba -> v_vacancy_rate | (v_measured_noise_dba, v_vacancy_rate)=A |
| v_measured_noise_dba, v_asking_rent_obs | v_measured_noise_dba   v_asking_rent_obs (no edge) | v_measured_noise_dba   v_asking_rent_obs (no edge) | v_measured_noise_dba->v_asking_rent_obs | v_measured_noise_dba->v_asking_rent_obs | v_measured_noise_dba->v_asking_rent_obs | no edge | (v_measured_noise_dba, v_asking_rent_obs)=A |
| v_interest_rate_ann, v_vacancy_rate | v_interest_rate_ann   v_vacancy_rate (no edge) | v_interest_rate_ann   v_vacancy_rate (no edge) | v_interest_rate_ann->v_vacancy_rate | v_interest_rate_ann->v_vacancy_rate | v_interest_rate_ann->v_vacancy_rate | v_interest_rate_ann -> v_vacancy_rate | (v_interest_rate_ann, v_vacancy_rate)=A |
| v_interest_rate_ann, v_asking_rent_obs | v_interest_rate_ann   v_asking_rent_obs (no edge) | v_interest_rate_ann   v_asking_rent_obs (no edge) | v_interest_rate_ann->v_asking_rent_obs | v_interest_rate_ann->v_asking_rent_obs | v_interest_rate_ann->v_asking_rent_obs | v_interest_rate_ann -> v_asking_rent_obs | (v_interest_rate_ann, v_asking_rent_obs)=A |
| v_vacancy_rate, v_asking_rent_obs | v_vacancy_rate   v_asking_rent_obs (no edge) | v_vacancy_rate   v_asking_rent_obs (no edge) | v_vacancy_rate->v_asking_rent_obs | v_vacancy_rate->v_asking_rent_obs | v_vacancy_rate->v_asking_rent_obs | no edge | (v_vacancy_rate, v_asking_rent_obs)=A |
| v_vacancy_rate, v_permit_backlog | v_permit_backlog->v_vacancy_rate | v_permit_backlog->v_vacancy_rate | v_vacancy_rate->v_permit_backlog | v_vacancy_rate->v_permit_backlog | v_vacancy_rate->v_permit_backlog | v_permit_backlog -> v_vacancy_rate | (v_vacancy_rate, v_permit_backlog)=A |
| v_vacancy_rate, v_service_freq_tph | v_vacancy_rate <-> v_service_freq_tph | v_vacancy_rate <-> v_service_freq_tph | v_vacancy_rate   v_service_freq_tph (no edge) | v_vacancy_rate   v_service_freq_tph (no edge) | v_vacancy_rate   v_service_freq_tph (no edge) | v_vacancy_rate -> v_service_freq_tph | (v_vacancy_rate, v_service_freq_tph)=C |
| v_spatial_spillover_idx, v_asking_rent_obs | v_spatial_spillover_idx   v_asking_rent_obs (no edge) | v_spatial_spillover_idx   v_asking_rent_obs (no edge) | v_spatial_spillover_idx->v_asking_rent_obs | v_spatial_spillover_idx->v_asking_rent_obs | v_spatial_spillover_idx->v_asking_rent_obs | no edge | (v_spatial_spillover_idx, v_asking_rent_obs)=A |
| v_asking_rent_obs, v_school_quality_score | v_asking_rent_obs   v_school_quality_score (no edge) | v_asking_rent_obs   v_school_quality_score (no edge) | v_asking_rent_obs->v_school_quality_score | v_asking_rent_obs->v_school_quality_score | v_asking_rent_obs->v_school_quality_score | no edge | (v_asking_rent_obs, v_school_quality_score)=A |
| v_permit_backlog, v_service_freq_tph | v_permit_backlog <-> v_service_freq_tph | v_permit_backlog   v_service_freq_tph (no edge) | v_permit_backlog   v_service_freq_tph (no edge) | v_permit_backlog   v_service_freq_tph (no edge) | v_permit_backlog   v_service_freq_tph (no edge) | no edge | (v_permit_backlog, v_service_freq_tph)=C |
| v_permit_backlog, v_permit_approvals_true | v_permit_backlog   v_permit_approvals_true (no edge) | v_permit_backlog   v_permit_approvals_true (no edge) | v_permit_backlog->v_permit_approvals_true | v_permit_backlog->v_permit_approvals_true | v_permit_backlog->v_permit_approvals_true | no edge | (v_permit_backlog, v_permit_approvals_true)=A |
| v_permit_approvals_true, v_season_regime | v_permit_approvals_true o-o v_season_regime | v_permit_approvals_true o-o v_season_regime | v_permit_approvals_true   v_season_regime (no edge) | v_permit_approvals_true   v_season_regime (no edge) | v_permit_approvals_true   v_season_regime (no edge) | v_season_regime -> v_permit_approvals_true | (v_permit_approvals_true, v_season_regime)=C |
| v_permit_approvals_true, v_school_quality_score | v_permit_approvals_true o-> v_school_quality_score | v_permit_approvals_true   v_school_quality_score (no edge) | v_permit_approvals_true   v_school_quality_score (no edge) | v_permit_approvals_true   v_school_quality_score (no edge) | v_permit_approvals_true   v_school_quality_score (no edge) | no edge | (v_permit_approvals_true, v_school_quality_score)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
