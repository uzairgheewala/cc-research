# Edge lineage: 20261011T224148Z_s2_q081_r01_7d01ca

Dataset `/research/datasets/suite_q1s2/q081/q081.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 22 | 0.77 | 0.42 | 0.55 | 4 | 1 | 12 | 41 |
| S1 after bootstrap edits | 11 | 0.82 | 0.23 | 0.35 | 4 | 1 | 4 | 38 |
| S2 after LLM review | 41 | 0.54 | 0.55 | 0.54 | 14 | 7 | 1 | 47 |
| S3 after KCI pruning | 39 | 0.56 | 0.55 | 0.56 | 14 | 7 | 1 | 45 |
| S4 final (after cycle step) | 39 | 0.56 | 0.55 | 0.56 | 14 | 7 | 1 | 45 |

Scored against: reference graph s2_08_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 11. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 32, "B": 8, "C": 148, "D": 43}.
- LLM effect: added 32 (of which 21 where the resamples showed no edge at frequency >= 0.9), removed 2, re-oriented 5.
- KCI step removed 2. Cycle step changed 0.
- Final graph: 39 edges; set by {"llm": 35, "algorithm (unchanged)": 4}; 4 identical to the algorithm's output; 25 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| baseline_salt_rejection->osmotic_pressure_diff | llm | no | 1.00 |
| baseline_salt_rejection->true_permeate_salt | llm | no | 0.85 |
| baseline_salt_rejection->feed_salinity | llm | no | 1.00 |
| baseline_salt_rejection->observed_permeate_conductivity | llm | no | 0.70 |
| cip_removal_fraction->fouling_stock | llm | yes | 0.00 |
| fouling_stock->fouling_stock_prior | llm | yes | 0.00 |
| fouling_stock->deposition_rate | llm | no | 1.00 |
| membrane_age->intrinsic_permeability | llm | yes | 0.00 |
| membrane_age->required_tmp | llm | no | 0.95 |
| membrane_age->specific_energy_consumption | llm | no | 1.00 |
| membrane_age->achieved_permeate_flow_rate | llm | no | 1.00 |
| true_permeate_salt->osmotic_pressure_diff | algorithm (unchanged) | yes | 0.25 |
| feed_salinity->osmotic_pressure_diff | llm | yes | 0.00 |
| osmotic_pressure_diff->required_tmp | llm | no | 0.50 |
| concentration_polarization_index->feed_salinity | llm | no | 0.95 |
| feed_salinity->true_permeate_salt | llm | no | 0.95 |
| true_permeate_salt->observed_permeate_conductivity | llm | yes | 0.00 |
| feed_salinity->antiscalant_effectiveness | algorithm (unchanged) | yes | 0.40 |
| feed_salinity->required_tmp | llm | no | 1.00 |
| feed_salinity->specific_energy_consumption | llm | no | 0.85 |
| feed_salinity->observed_permeate_conductivity | llm | no | 1.00 |
| antiscalant_effectiveness->deposition_rate | llm | no | 1.00 |
| intrinsic_permeability->required_tmp | algorithm (unchanged) | yes | 0.55 |
| intrinsic_permeability->achieved_permeate_flow_rate | llm | no | 1.00 |
| recovery_ratio_target->achieved_recovery_ratio | llm | yes | 0.00 |
| required_tmp->achieved_recovery_ratio | llm | no | 1.00 |
| achieved_recovery_ratio->achieved_permeate_flow_rate | llm | no | 1.00 |
| assayed_sdi->pretreatment_fouling_potential | llm | yes | 0.00 |
| required_tmp->specific_energy_consumption | llm | yes | 0.00 |
| required_tmp->achieved_permeate_flow_rate | llm | no | 0.70 |
| specific_energy_consumption->achieved_permeate_flow_rate | llm | no | 0.75 |
| feed_temperature->observed_permeate_conductivity | llm | no | 1.00 |
| feed_temperature->achieved_permeate_flow_rate | llm | no | 1.00 |
| feed_temperature <-> pretreatment_fouling_potential | algorithm (unchanged) | yes | 0.00 |
| fouling_stock_prior->deposition_rate | llm | no | 1.00 |
| fouling_stock_prior->pretreatment_fouling_potential | llm | no | 1.00 |
| deposition_rate->achieved_permeate_flow_rate | llm | no | 0.90 |
| deposition_rate->pretreatment_fouling_potential | llm | yes | 0.60 |
| daily_production_demand->achieved_permeate_flow_rate | llm | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| baseline_salt_rejection, membrane_age | baseline_salt_rejection o-o membrane_age | baseline_salt_rejection   membrane_age (no edge) | baseline_salt_rejection   membrane_age (no edge) | baseline_salt_rejection   membrane_age (no edge) | baseline_salt_rejection   membrane_age (no edge) | membrane_age -> baseline_salt_rejection | (baseline_salt_rejection, membrane_age)=D |
| baseline_salt_rejection, osmotic_pressure_diff | baseline_salt_rejection   osmotic_pressure_diff (no edge) | baseline_salt_rejection   osmotic_pressure_diff (no edge) | baseline_salt_rejection->osmotic_pressure_diff | baseline_salt_rejection->osmotic_pressure_diff | baseline_salt_rejection->osmotic_pressure_diff | no edge | (baseline_salt_rejection, osmotic_pressure_diff)=A |
| baseline_salt_rejection, true_permeate_salt | baseline_salt_rejection   true_permeate_salt (no edge) | baseline_salt_rejection   true_permeate_salt (no edge) | baseline_salt_rejection->true_permeate_salt | baseline_salt_rejection->true_permeate_salt | baseline_salt_rejection->true_permeate_salt | baseline_salt_rejection -> true_permeate_salt | (baseline_salt_rejection, true_permeate_salt)=A |
| baseline_salt_rejection, feed_salinity | baseline_salt_rejection   feed_salinity (no edge) | baseline_salt_rejection   feed_salinity (no edge) | baseline_salt_rejection->feed_salinity | baseline_salt_rejection->feed_salinity | baseline_salt_rejection->feed_salinity | no edge | (baseline_salt_rejection, feed_salinity)=A |
| baseline_salt_rejection, observed_permeate_conductivity | baseline_salt_rejection   observed_permeate_conductivity (no edge) | baseline_salt_rejection   observed_permeate_conductivity (no edge) | baseline_salt_rejection->observed_permeate_conductivity | baseline_salt_rejection->observed_permeate_conductivity | baseline_salt_rejection->observed_permeate_conductivity | no edge | (baseline_salt_rejection, observed_permeate_conductivity)=A |
| fouling_stock, cip_removal_fraction | fouling_stock o-o cip_removal_fraction | fouling_stock o-o cip_removal_fraction | cip_removal_fraction->fouling_stock | cip_removal_fraction->fouling_stock | cip_removal_fraction->fouling_stock | cip_removal_fraction -> fouling_stock | (fouling_stock, cip_removal_fraction)=B |
| fouling_stock, antiscalant_effectiveness | fouling_stock   antiscalant_effectiveness (no edge) | fouling_stock   antiscalant_effectiveness (no edge) | antiscalant_effectiveness->fouling_stock | fouling_stock   antiscalant_effectiveness (no edge) | fouling_stock   antiscalant_effectiveness (no edge) | no edge | (fouling_stock, antiscalant_effectiveness)=B |
| fouling_stock, fouling_stock_prior | fouling_stock o-o fouling_stock_prior | fouling_stock   fouling_stock_prior (no edge) | fouling_stock->fouling_stock_prior | fouling_stock->fouling_stock_prior | fouling_stock->fouling_stock_prior | fouling_stock_prior -> fouling_stock | (fouling_stock, fouling_stock_prior)=A |
| fouling_stock, deposition_rate | fouling_stock   deposition_rate (no edge) | fouling_stock   deposition_rate (no edge) | fouling_stock->deposition_rate | fouling_stock->deposition_rate | fouling_stock->deposition_rate | deposition_rate -> fouling_stock | (fouling_stock, deposition_rate)=A |
| membrane_age, intrinsic_permeability | membrane_age o-o intrinsic_permeability | membrane_age   intrinsic_permeability (no edge) | membrane_age->intrinsic_permeability | membrane_age->intrinsic_permeability | membrane_age->intrinsic_permeability | membrane_age -> intrinsic_permeability | (membrane_age, intrinsic_permeability)=A |
| membrane_age, required_tmp | membrane_age   required_tmp (no edge) | membrane_age   required_tmp (no edge) | membrane_age->required_tmp | membrane_age->required_tmp | membrane_age->required_tmp | no edge | (membrane_age, required_tmp)=A |
| membrane_age, specific_energy_consumption | membrane_age   specific_energy_consumption (no edge) | membrane_age   specific_energy_consumption (no edge) | membrane_age->specific_energy_consumption | membrane_age->specific_energy_consumption | membrane_age->specific_energy_consumption | no edge | (membrane_age, specific_energy_consumption)=A |
| membrane_age, achieved_permeate_flow_rate | membrane_age   achieved_permeate_flow_rate (no edge) | membrane_age   achieved_permeate_flow_rate (no edge) | membrane_age->achieved_permeate_flow_rate | membrane_age->achieved_permeate_flow_rate | membrane_age->achieved_permeate_flow_rate | no edge | (membrane_age, achieved_permeate_flow_rate)=A |
| osmotic_pressure_diff, feed_salinity | osmotic_pressure_diff->feed_salinity | osmotic_pressure_diff->feed_salinity | feed_salinity->osmotic_pressure_diff | feed_salinity->osmotic_pressure_diff | feed_salinity->osmotic_pressure_diff | feed_salinity -> osmotic_pressure_diff | (osmotic_pressure_diff, feed_salinity)=B |
| osmotic_pressure_diff, recovery_ratio_target | osmotic_pressure_diff <-> recovery_ratio_target | osmotic_pressure_diff   recovery_ratio_target (no edge) | osmotic_pressure_diff   recovery_ratio_target (no edge) | osmotic_pressure_diff   recovery_ratio_target (no edge) | osmotic_pressure_diff   recovery_ratio_target (no edge) | no edge | (osmotic_pressure_diff, recovery_ratio_target)=C |
| osmotic_pressure_diff, required_tmp | osmotic_pressure_diff   required_tmp (no edge) | osmotic_pressure_diff   required_tmp (no edge) | osmotic_pressure_diff->required_tmp | osmotic_pressure_diff->required_tmp | osmotic_pressure_diff->required_tmp | osmotic_pressure_diff -> required_tmp | (osmotic_pressure_diff, required_tmp)=A |
| cip_removal_fraction, fouling_stock_prior | cip_removal_fraction o-o fouling_stock_prior | cip_removal_fraction   fouling_stock_prior (no edge) | cip_removal_fraction   fouling_stock_prior (no edge) | cip_removal_fraction   fouling_stock_prior (no edge) | cip_removal_fraction   fouling_stock_prior (no edge) | fouling_stock_prior -> cip_removal_fraction | (cip_removal_fraction, fouling_stock_prior)=C |
| concentration_polarization_index, feed_salinity | concentration_polarization_index   feed_salinity (no edge) | concentration_polarization_index   feed_salinity (no edge) | concentration_polarization_index->feed_salinity | concentration_polarization_index->feed_salinity | concentration_polarization_index->feed_salinity | no edge | (concentration_polarization_index, feed_salinity)=A |
| concentration_polarization_index, feed_temperature | concentration_polarization_index <-> feed_temperature | concentration_polarization_index   feed_temperature (no edge) | concentration_polarization_index   feed_temperature (no edge) | concentration_polarization_index   feed_temperature (no edge) | concentration_polarization_index   feed_temperature (no edge) | feed_temperature -> concentration_polarization_index | (concentration_polarization_index, feed_temperature)=C |
| concentration_polarization_index, daily_production_demand | daily_production_demand->concentration_polarization_index | daily_production_demand->concentration_polarization_index | concentration_polarization_index   daily_production_demand (no edge) | concentration_polarization_index   daily_production_demand (no edge) | concentration_polarization_index   daily_production_demand (no edge) | no edge | (concentration_polarization_index, daily_production_demand)=C |
| true_permeate_salt, feed_salinity | true_permeate_salt   feed_salinity (no edge) | true_permeate_salt   feed_salinity (no edge) | feed_salinity->true_permeate_salt | feed_salinity->true_permeate_salt | feed_salinity->true_permeate_salt | feed_salinity -> true_permeate_salt | (true_permeate_salt, feed_salinity)=B |
| true_permeate_salt, observed_permeate_conductivity | true_permeate_salt o-o observed_permeate_conductivity | true_permeate_salt o-o observed_permeate_conductivity | true_permeate_salt->observed_permeate_conductivity | true_permeate_salt->observed_permeate_conductivity | true_permeate_salt->observed_permeate_conductivity | true_permeate_salt -> observed_permeate_conductivity | (true_permeate_salt, observed_permeate_conductivity)=A |
| feed_salinity, required_tmp | feed_salinity   required_tmp (no edge) | feed_salinity   required_tmp (no edge) | feed_salinity->required_tmp | feed_salinity->required_tmp | feed_salinity->required_tmp | no edge | (feed_salinity, required_tmp)=A |
| feed_salinity, specific_energy_consumption | feed_salinity   specific_energy_consumption (no edge) | feed_salinity   specific_energy_consumption (no edge) | feed_salinity->specific_energy_consumption | feed_salinity->specific_energy_consumption | feed_salinity->specific_energy_consumption | no edge | (feed_salinity, specific_energy_consumption)=A |
| feed_salinity, observed_permeate_conductivity | feed_salinity   observed_permeate_conductivity (no edge) | feed_salinity   observed_permeate_conductivity (no edge) | feed_salinity->observed_permeate_conductivity | feed_salinity->observed_permeate_conductivity | feed_salinity->observed_permeate_conductivity | no edge | (feed_salinity, observed_permeate_conductivity)=A |
| antiscalant_effectiveness, assayed_sdi | assayed_sdi->antiscalant_effectiveness | assayed_sdi->antiscalant_effectiveness | antiscalant_effectiveness   assayed_sdi (no edge) | antiscalant_effectiveness   assayed_sdi (no edge) | antiscalant_effectiveness   assayed_sdi (no edge) | assayed_sdi -> antiscalant_effectiveness | (antiscalant_effectiveness, assayed_sdi)=C |
| antiscalant_effectiveness, deposition_rate | antiscalant_effectiveness   deposition_rate (no edge) | antiscalant_effectiveness   deposition_rate (no edge) | antiscalant_effectiveness->deposition_rate | antiscalant_effectiveness->deposition_rate | antiscalant_effectiveness->deposition_rate | antiscalant_effectiveness -> deposition_rate | (antiscalant_effectiveness, deposition_rate)=A |
| intrinsic_permeability, achieved_permeate_flow_rate | intrinsic_permeability   achieved_permeate_flow_rate (no edge) | intrinsic_permeability   achieved_permeate_flow_rate (no edge) | intrinsic_permeability->achieved_permeate_flow_rate | intrinsic_permeability->achieved_permeate_flow_rate | intrinsic_permeability->achieved_permeate_flow_rate | no edge | (intrinsic_permeability, achieved_permeate_flow_rate)=A |
| achieved_recovery_ratio, recovery_ratio_target | achieved_recovery_ratio o-> recovery_ratio_target | achieved_recovery_ratio   recovery_ratio_target (no edge) | recovery_ratio_target->achieved_recovery_ratio | recovery_ratio_target->achieved_recovery_ratio | recovery_ratio_target->achieved_recovery_ratio | recovery_ratio_target -> achieved_recovery_ratio | (achieved_recovery_ratio, recovery_ratio_target)=B |
| achieved_recovery_ratio, required_tmp | achieved_recovery_ratio   required_tmp (no edge) | achieved_recovery_ratio   required_tmp (no edge) | required_tmp->achieved_recovery_ratio | required_tmp->achieved_recovery_ratio | required_tmp->achieved_recovery_ratio | no edge | (achieved_recovery_ratio, required_tmp)=B |
| achieved_recovery_ratio, specific_energy_consumption | achieved_recovery_ratio   specific_energy_consumption (no edge) | achieved_recovery_ratio   specific_energy_consumption (no edge) | specific_energy_consumption->achieved_recovery_ratio | achieved_recovery_ratio   specific_energy_consumption (no edge) | achieved_recovery_ratio   specific_energy_consumption (no edge) | no edge | (achieved_recovery_ratio, specific_energy_consumption)=B |
| achieved_recovery_ratio, achieved_permeate_flow_rate | achieved_recovery_ratio   achieved_permeate_flow_rate (no edge) | achieved_recovery_ratio   achieved_permeate_flow_rate (no edge) | achieved_recovery_ratio->achieved_permeate_flow_rate | achieved_recovery_ratio->achieved_permeate_flow_rate | achieved_recovery_ratio->achieved_permeate_flow_rate | no edge | (achieved_recovery_ratio, achieved_permeate_flow_rate)=A |
| assayed_sdi, pretreatment_fouling_potential | pretreatment_fouling_potential->assayed_sdi | pretreatment_fouling_potential->assayed_sdi | assayed_sdi->pretreatment_fouling_potential | assayed_sdi->pretreatment_fouling_potential | assayed_sdi->pretreatment_fouling_potential | pretreatment_fouling_potential -> assayed_sdi | (assayed_sdi, pretreatment_fouling_potential)=A |
| recovery_ratio_target, required_tmp | recovery_ratio_target <-> required_tmp | recovery_ratio_target   required_tmp (no edge) | recovery_ratio_target   required_tmp (no edge) | recovery_ratio_target   required_tmp (no edge) | recovery_ratio_target   required_tmp (no edge) | no edge | (recovery_ratio_target, required_tmp)=C |
| required_tmp, specific_energy_consumption | specific_energy_consumption o-> required_tmp | required_tmp   specific_energy_consumption (no edge) | required_tmp->specific_energy_consumption | required_tmp->specific_energy_consumption | required_tmp->specific_energy_consumption | required_tmp -> specific_energy_consumption | (required_tmp, specific_energy_consumption)=A |
| required_tmp, daily_production_demand | daily_production_demand->required_tmp | required_tmp   daily_production_demand (no edge) | required_tmp   daily_production_demand (no edge) | required_tmp   daily_production_demand (no edge) | required_tmp   daily_production_demand (no edge) | no edge | (required_tmp, daily_production_demand)=C |
| required_tmp, achieved_permeate_flow_rate | required_tmp   achieved_permeate_flow_rate (no edge) | required_tmp   achieved_permeate_flow_rate (no edge) | required_tmp->achieved_permeate_flow_rate | required_tmp->achieved_permeate_flow_rate | required_tmp->achieved_permeate_flow_rate | achieved_permeate_flow_rate -> required_tmp | (required_tmp, achieved_permeate_flow_rate)=A |
| specific_energy_consumption, achieved_permeate_flow_rate | specific_energy_consumption   achieved_permeate_flow_rate (no edge) | specific_energy_consumption   achieved_permeate_flow_rate (no edge) | specific_energy_consumption->achieved_permeate_flow_rate | specific_energy_consumption->achieved_permeate_flow_rate | specific_energy_consumption->achieved_permeate_flow_rate | achieved_permeate_flow_rate -> specific_energy_consumption | (specific_energy_consumption, achieved_permeate_flow_rate)=A |
| feed_temperature, observed_permeate_conductivity | feed_temperature   observed_permeate_conductivity (no edge) | feed_temperature   observed_permeate_conductivity (no edge) | feed_temperature->observed_permeate_conductivity | feed_temperature->observed_permeate_conductivity | feed_temperature->observed_permeate_conductivity | feed_temperature -> observed_permeate_conductivity | (feed_temperature, observed_permeate_conductivity)=A |
| feed_temperature, achieved_permeate_flow_rate | feed_temperature   achieved_permeate_flow_rate (no edge) | feed_temperature   achieved_permeate_flow_rate (no edge) | feed_temperature->achieved_permeate_flow_rate | feed_temperature->achieved_permeate_flow_rate | feed_temperature->achieved_permeate_flow_rate | no edge | (feed_temperature, achieved_permeate_flow_rate)=A |
| fouling_stock_prior, deposition_rate | fouling_stock_prior   deposition_rate (no edge) | fouling_stock_prior   deposition_rate (no edge) | fouling_stock_prior->deposition_rate | fouling_stock_prior->deposition_rate | fouling_stock_prior->deposition_rate | no edge | (fouling_stock_prior, deposition_rate)=A |
| fouling_stock_prior, pretreatment_fouling_potential | fouling_stock_prior   pretreatment_fouling_potential (no edge) | fouling_stock_prior   pretreatment_fouling_potential (no edge) | fouling_stock_prior->pretreatment_fouling_potential | fouling_stock_prior->pretreatment_fouling_potential | fouling_stock_prior->pretreatment_fouling_potential | no edge | (fouling_stock_prior, pretreatment_fouling_potential)=A |
| deposition_rate, achieved_permeate_flow_rate | deposition_rate   achieved_permeate_flow_rate (no edge) | deposition_rate   achieved_permeate_flow_rate (no edge) | deposition_rate->achieved_permeate_flow_rate | deposition_rate->achieved_permeate_flow_rate | deposition_rate->achieved_permeate_flow_rate | achieved_permeate_flow_rate -> deposition_rate | (deposition_rate, achieved_permeate_flow_rate)=A |
| deposition_rate, pretreatment_fouling_potential | deposition_rate o-> pretreatment_fouling_potential | deposition_rate   pretreatment_fouling_potential (no edge) | deposition_rate->pretreatment_fouling_potential | deposition_rate->pretreatment_fouling_potential | deposition_rate->pretreatment_fouling_potential | pretreatment_fouling_potential -> deposition_rate | (deposition_rate, pretreatment_fouling_potential)=A |
| daily_production_demand, achieved_permeate_flow_rate | daily_production_demand o-o achieved_permeate_flow_rate | daily_production_demand o-o achieved_permeate_flow_rate | daily_production_demand->achieved_permeate_flow_rate | daily_production_demand->achieved_permeate_flow_rate | daily_production_demand->achieved_permeate_flow_rate | daily_production_demand -> achieved_permeate_flow_rate | (daily_production_demand, achieved_permeate_flow_rate)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
