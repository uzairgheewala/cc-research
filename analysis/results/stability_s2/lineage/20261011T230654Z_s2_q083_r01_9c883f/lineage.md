# Edge lineage: 20261011T230654Z_s2_q083_r01_9c883f

Dataset `/research/datasets/suite_q1s2/q083/q083.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 22 variables, 231 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 23 | 0.87 | 0.50 | 0.63 | 6 | 0 | 14 | 37 |
| S1 after bootstrap edits | 10 | 1.00 | 0.25 | 0.40 | 6 | 0 | 4 | 34 |
| S2 after LLM review | 49 | 0.20 | 0.25 | 0.22 | 4 | 3 | 3 | 75 |
| S3 after KCI pruning | 42 | 0.24 | 0.25 | 0.24 | 4 | 3 | 3 | 68 |
| S4 final (after cycle step) | 42 | 0.24 | 0.25 | 0.24 | 4 | 3 | 3 | 68 |

Scored against: reference graph s2_08_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 13. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 22 calls, 231 distinct pairs answered out of 231, plus 22 self-pairs. Letters: {"A": 34, "B": 11, "C": 101, "D": 85}.
- LLM effect: added 42 (of which 39 where the resamples showed no edge at frequency >= 0.9), removed 3, re-oriented 1.
- KCI step removed 7. Cycle step changed 0.
- Final graph: 42 edges; set by {"llm": 36, "algorithm (unchanged)": 6}; 6 identical to the algorithm's output; 35 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| fouling_stock->cip_removal_fraction | llm | no | 1.00 |
| antiscalant_effectiveness->fouling_stock | llm | no | 0.85 |
| baseline_salt_rejection->achieved_recovery_ratio | llm | no | 1.00 |
| baseline_salt_rejection->true_permeate_salt | llm | no | 1.00 |
| baseline_salt_rejection->required_tmp | llm | no | 1.00 |
| baseline_salt_rejection->observed_permeate_conductivity | llm | no | 1.00 |
| baseline_salt_rejection->specific_energy_consumption | llm | no | 1.00 |
| baseline_salt_rejection->achieved_permeate_flow_rate | llm | no | 1.00 |
| osmotic_pressure_diff->feed_salinity | llm | no | 1.00 |
| osmotic_pressure_diff->feed_temperature | llm | no | 1.00 |
| membrane_age->intrinsic_permeability | llm | no | 1.00 |
| membrane_age->recovery_ratio_target | algorithm (unchanged) | yes | 0.35 |
| concentration_polarization_index->feed_salinity | llm | no | 1.00 |
| concentration_polarization_index->antiscalant_effectiveness | llm | no | 1.00 |
| concentration_polarization_index->feed_temperature | llm | no | 1.00 |
| cip_removal_fraction->deposition_rate | llm | no | 1.00 |
| cip_removal_fraction->achieved_permeate_flow_rate | llm | no | 1.00 |
| feed_salinity->achieved_recovery_ratio | llm | no | 0.95 |
| feed_salinity->true_permeate_salt | llm | no | 1.00 |
| feed_salinity->required_tmp | llm | no | 1.00 |
| feed_salinity->observed_permeate_conductivity | llm | no | 1.00 |
| feed_salinity->specific_energy_consumption | llm | no | 1.00 |
| feed_salinity->achieved_permeate_flow_rate | llm | no | 1.00 |
| achieved_recovery_ratio->true_permeate_salt | algorithm (unchanged) | yes | 0.30 |
| achieved_recovery_ratio->required_tmp | algorithm (unchanged) | yes | 0.05 |
| achieved_recovery_ratio->achieved_permeate_flow_rate | llm | no | 1.00 |
| true_permeate_salt->intrinsic_permeability | llm | yes | 0.00 |
| observed_permeate_conductivity->true_permeate_salt | llm | no | 0.95 |
| antiscalant_effectiveness->deposition_rate | llm | no | 1.00 |
| antiscalant_effectiveness->achieved_permeate_flow_rate | llm | no | 1.00 |
| assayed_sdi <-> required_tmp | algorithm (unchanged) | yes | 0.00 |
| feed_temperature->required_tmp | llm | no | 1.00 |
| required_tmp->specific_energy_consumption | llm | no | 0.55 |
| achieved_permeate_flow_rate->required_tmp | llm | no | 1.00 |
| recovery_ratio_target->achieved_permeate_flow_rate | llm | no | 1.00 |
| feed_temperature->specific_energy_consumption | llm | no | 0.75 |
| feed_temperature->achieved_permeate_flow_rate | llm | no | 1.00 |
| observed_permeate_conductivity <-> achieved_permeate_flow_rate | algorithm (unchanged) | yes | 0.05 |
| deposition_rate->specific_energy_consumption | llm | no | 1.00 |
| daily_production_demand->specific_energy_consumption | llm | no | 1.00 |
| daily_production_demand->achieved_permeate_flow_rate | llm | no | 0.95 |
| pretreatment_fouling_potential o-o specific_energy_consumption | algorithm (unchanged) | yes | 0.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| fouling_stock, osmotic_pressure_diff | fouling_stock o-o osmotic_pressure_diff | fouling_stock o-o osmotic_pressure_diff | fouling_stock   osmotic_pressure_diff (no edge) | fouling_stock   osmotic_pressure_diff (no edge) | fouling_stock   osmotic_pressure_diff (no edge) | osmotic_pressure_diff -> fouling_stock | (fouling_stock, osmotic_pressure_diff)=C |
| fouling_stock, cip_removal_fraction | fouling_stock   cip_removal_fraction (no edge) | fouling_stock   cip_removal_fraction (no edge) | fouling_stock->cip_removal_fraction | fouling_stock->cip_removal_fraction | fouling_stock->cip_removal_fraction | no edge | (fouling_stock, cip_removal_fraction)=A |
| fouling_stock, antiscalant_effectiveness | fouling_stock   antiscalant_effectiveness (no edge) | fouling_stock   antiscalant_effectiveness (no edge) | antiscalant_effectiveness->fouling_stock | antiscalant_effectiveness->fouling_stock | antiscalant_effectiveness->fouling_stock | no edge | (fouling_stock, antiscalant_effectiveness)=B |
| fouling_stock, deposition_rate | fouling_stock   deposition_rate (no edge) | fouling_stock   deposition_rate (no edge) | deposition_rate->fouling_stock | fouling_stock   deposition_rate (no edge) | fouling_stock   deposition_rate (no edge) | no edge | (fouling_stock, deposition_rate)=B |
| fouling_stock, fouling_stock_prior | fouling_stock   fouling_stock_prior (no edge) | fouling_stock   fouling_stock_prior (no edge) | fouling_stock_prior->fouling_stock | fouling_stock   fouling_stock_prior (no edge) | fouling_stock   fouling_stock_prior (no edge) | no edge | (fouling_stock, fouling_stock_prior)=B |
| fouling_stock, pretreatment_fouling_potential | fouling_stock   pretreatment_fouling_potential (no edge) | fouling_stock   pretreatment_fouling_potential (no edge) | pretreatment_fouling_potential->fouling_stock | fouling_stock   pretreatment_fouling_potential (no edge) | fouling_stock   pretreatment_fouling_potential (no edge) | no edge | (fouling_stock, pretreatment_fouling_potential)=B |
| baseline_salt_rejection, concentration_polarization_index | baseline_salt_rejection o-o concentration_polarization_index | baseline_salt_rejection   concentration_polarization_index (no edge) | baseline_salt_rejection   concentration_polarization_index (no edge) | baseline_salt_rejection   concentration_polarization_index (no edge) | baseline_salt_rejection   concentration_polarization_index (no edge) | concentration_polarization_index -> baseline_salt_rejection | (baseline_salt_rejection, concentration_polarization_index)=C |
| baseline_salt_rejection, achieved_recovery_ratio | baseline_salt_rejection   achieved_recovery_ratio (no edge) | baseline_salt_rejection   achieved_recovery_ratio (no edge) | baseline_salt_rejection->achieved_recovery_ratio | baseline_salt_rejection->achieved_recovery_ratio | baseline_salt_rejection->achieved_recovery_ratio | no edge | (baseline_salt_rejection, achieved_recovery_ratio)=A |
| baseline_salt_rejection, true_permeate_salt | baseline_salt_rejection   true_permeate_salt (no edge) | baseline_salt_rejection   true_permeate_salt (no edge) | baseline_salt_rejection->true_permeate_salt | baseline_salt_rejection->true_permeate_salt | baseline_salt_rejection->true_permeate_salt | no edge | (baseline_salt_rejection, true_permeate_salt)=A |
| baseline_salt_rejection, required_tmp | baseline_salt_rejection   required_tmp (no edge) | baseline_salt_rejection   required_tmp (no edge) | baseline_salt_rejection->required_tmp | baseline_salt_rejection->required_tmp | baseline_salt_rejection->required_tmp | no edge | (baseline_salt_rejection, required_tmp)=A |
| baseline_salt_rejection, observed_permeate_conductivity | baseline_salt_rejection   observed_permeate_conductivity (no edge) | baseline_salt_rejection   observed_permeate_conductivity (no edge) | baseline_salt_rejection->observed_permeate_conductivity | baseline_salt_rejection->observed_permeate_conductivity | baseline_salt_rejection->observed_permeate_conductivity | no edge | (baseline_salt_rejection, observed_permeate_conductivity)=A |
| baseline_salt_rejection, deposition_rate | baseline_salt_rejection o-o deposition_rate | baseline_salt_rejection   deposition_rate (no edge) | baseline_salt_rejection   deposition_rate (no edge) | baseline_salt_rejection   deposition_rate (no edge) | baseline_salt_rejection   deposition_rate (no edge) | deposition_rate -> baseline_salt_rejection | (baseline_salt_rejection, deposition_rate)=C |
| baseline_salt_rejection, specific_energy_consumption | baseline_salt_rejection   specific_energy_consumption (no edge) | baseline_salt_rejection   specific_energy_consumption (no edge) | baseline_salt_rejection->specific_energy_consumption | baseline_salt_rejection->specific_energy_consumption | baseline_salt_rejection->specific_energy_consumption | no edge | (baseline_salt_rejection, specific_energy_consumption)=A |
| baseline_salt_rejection, achieved_permeate_flow_rate | baseline_salt_rejection   achieved_permeate_flow_rate (no edge) | baseline_salt_rejection   achieved_permeate_flow_rate (no edge) | baseline_salt_rejection->achieved_permeate_flow_rate | baseline_salt_rejection->achieved_permeate_flow_rate | baseline_salt_rejection->achieved_permeate_flow_rate | no edge | (baseline_salt_rejection, achieved_permeate_flow_rate)=A |
| osmotic_pressure_diff, feed_salinity | osmotic_pressure_diff   feed_salinity (no edge) | osmotic_pressure_diff   feed_salinity (no edge) | osmotic_pressure_diff->feed_salinity | osmotic_pressure_diff->feed_salinity | osmotic_pressure_diff->feed_salinity | no edge | (osmotic_pressure_diff, feed_salinity)=A |
| osmotic_pressure_diff, antiscalant_effectiveness | osmotic_pressure_diff o-o antiscalant_effectiveness | osmotic_pressure_diff   antiscalant_effectiveness (no edge) | osmotic_pressure_diff   antiscalant_effectiveness (no edge) | osmotic_pressure_diff   antiscalant_effectiveness (no edge) | osmotic_pressure_diff   antiscalant_effectiveness (no edge) | osmotic_pressure_diff -> antiscalant_effectiveness | (osmotic_pressure_diff, antiscalant_effectiveness)=D |
| osmotic_pressure_diff, feed_temperature | osmotic_pressure_diff   feed_temperature (no edge) | osmotic_pressure_diff   feed_temperature (no edge) | osmotic_pressure_diff->feed_temperature | osmotic_pressure_diff->feed_temperature | osmotic_pressure_diff->feed_temperature | no edge | (osmotic_pressure_diff, feed_temperature)=A |
| membrane_age, achieved_recovery_ratio | membrane_age o-o achieved_recovery_ratio | membrane_age   achieved_recovery_ratio (no edge) | membrane_age   achieved_recovery_ratio (no edge) | membrane_age   achieved_recovery_ratio (no edge) | membrane_age   achieved_recovery_ratio (no edge) | achieved_recovery_ratio -> membrane_age | (membrane_age, achieved_recovery_ratio)=D |
| membrane_age, intrinsic_permeability | membrane_age   intrinsic_permeability (no edge) | membrane_age   intrinsic_permeability (no edge) | membrane_age->intrinsic_permeability | membrane_age->intrinsic_permeability | membrane_age->intrinsic_permeability | no edge | (membrane_age, intrinsic_permeability)=A |
| concentration_polarization_index, feed_salinity | concentration_polarization_index   feed_salinity (no edge) | concentration_polarization_index   feed_salinity (no edge) | concentration_polarization_index->feed_salinity | concentration_polarization_index->feed_salinity | concentration_polarization_index->feed_salinity | no edge | (concentration_polarization_index, feed_salinity)=A |
| concentration_polarization_index, antiscalant_effectiveness | concentration_polarization_index   antiscalant_effectiveness (no edge) | concentration_polarization_index   antiscalant_effectiveness (no edge) | concentration_polarization_index->antiscalant_effectiveness | concentration_polarization_index->antiscalant_effectiveness | concentration_polarization_index->antiscalant_effectiveness | no edge | (concentration_polarization_index, antiscalant_effectiveness)=A |
| concentration_polarization_index, feed_temperature | concentration_polarization_index   feed_temperature (no edge) | concentration_polarization_index   feed_temperature (no edge) | concentration_polarization_index->feed_temperature | concentration_polarization_index->feed_temperature | concentration_polarization_index->feed_temperature | no edge | (concentration_polarization_index, feed_temperature)=A |
| concentration_polarization_index, deposition_rate | concentration_polarization_index o-o deposition_rate | concentration_polarization_index   deposition_rate (no edge) | concentration_polarization_index   deposition_rate (no edge) | concentration_polarization_index   deposition_rate (no edge) | concentration_polarization_index   deposition_rate (no edge) | deposition_rate -> concentration_polarization_index | (concentration_polarization_index, deposition_rate)=C |
| cip_removal_fraction, assayed_sdi | cip_removal_fraction <-> assayed_sdi | cip_removal_fraction   assayed_sdi (no edge) | cip_removal_fraction   assayed_sdi (no edge) | cip_removal_fraction   assayed_sdi (no edge) | cip_removal_fraction   assayed_sdi (no edge) | assayed_sdi -> cip_removal_fraction | (cip_removal_fraction, assayed_sdi)=D |
| cip_removal_fraction, feed_temperature | cip_removal_fraction <-> feed_temperature | cip_removal_fraction   feed_temperature (no edge) | cip_removal_fraction   feed_temperature (no edge) | cip_removal_fraction   feed_temperature (no edge) | cip_removal_fraction   feed_temperature (no edge) | no edge | (cip_removal_fraction, feed_temperature)=D |
| cip_removal_fraction, observed_permeate_conductivity | cip_removal_fraction <-> observed_permeate_conductivity | cip_removal_fraction   observed_permeate_conductivity (no edge) | cip_removal_fraction   observed_permeate_conductivity (no edge) | cip_removal_fraction   observed_permeate_conductivity (no edge) | cip_removal_fraction   observed_permeate_conductivity (no edge) | observed_permeate_conductivity -> cip_removal_fraction | (cip_removal_fraction, observed_permeate_conductivity)=D |
| cip_removal_fraction, deposition_rate | cip_removal_fraction   deposition_rate (no edge) | cip_removal_fraction   deposition_rate (no edge) | cip_removal_fraction->deposition_rate | cip_removal_fraction->deposition_rate | cip_removal_fraction->deposition_rate | no edge | (cip_removal_fraction, deposition_rate)=A |
| cip_removal_fraction, achieved_permeate_flow_rate | cip_removal_fraction   achieved_permeate_flow_rate (no edge) | cip_removal_fraction   achieved_permeate_flow_rate (no edge) | cip_removal_fraction->achieved_permeate_flow_rate | cip_removal_fraction->achieved_permeate_flow_rate | cip_removal_fraction->achieved_permeate_flow_rate | no edge | (cip_removal_fraction, achieved_permeate_flow_rate)=A |
| feed_salinity, achieved_recovery_ratio | feed_salinity   achieved_recovery_ratio (no edge) | feed_salinity   achieved_recovery_ratio (no edge) | feed_salinity->achieved_recovery_ratio | feed_salinity->achieved_recovery_ratio | feed_salinity->achieved_recovery_ratio | achieved_recovery_ratio -> feed_salinity | (feed_salinity, achieved_recovery_ratio)=A |
| feed_salinity, true_permeate_salt | feed_salinity   true_permeate_salt (no edge) | feed_salinity   true_permeate_salt (no edge) | feed_salinity->true_permeate_salt | feed_salinity->true_permeate_salt | feed_salinity->true_permeate_salt | no edge | (feed_salinity, true_permeate_salt)=A |
| feed_salinity, required_tmp | feed_salinity   required_tmp (no edge) | feed_salinity   required_tmp (no edge) | feed_salinity->required_tmp | feed_salinity->required_tmp | feed_salinity->required_tmp | no edge | (feed_salinity, required_tmp)=A |
| feed_salinity, observed_permeate_conductivity | feed_salinity   observed_permeate_conductivity (no edge) | feed_salinity   observed_permeate_conductivity (no edge) | feed_salinity->observed_permeate_conductivity | feed_salinity->observed_permeate_conductivity | feed_salinity->observed_permeate_conductivity | no edge | (feed_salinity, observed_permeate_conductivity)=A |
| feed_salinity, daily_production_demand | feed_salinity o-o daily_production_demand | feed_salinity   daily_production_demand (no edge) | feed_salinity   daily_production_demand (no edge) | feed_salinity   daily_production_demand (no edge) | feed_salinity   daily_production_demand (no edge) | feed_salinity -> daily_production_demand | (feed_salinity, daily_production_demand)=C |
| feed_salinity, specific_energy_consumption | feed_salinity   specific_energy_consumption (no edge) | feed_salinity   specific_energy_consumption (no edge) | feed_salinity->specific_energy_consumption | feed_salinity->specific_energy_consumption | feed_salinity->specific_energy_consumption | no edge | (feed_salinity, specific_energy_consumption)=A |
| feed_salinity, achieved_permeate_flow_rate | feed_salinity   achieved_permeate_flow_rate (no edge) | feed_salinity   achieved_permeate_flow_rate (no edge) | feed_salinity->achieved_permeate_flow_rate | feed_salinity->achieved_permeate_flow_rate | feed_salinity->achieved_permeate_flow_rate | no edge | (feed_salinity, achieved_permeate_flow_rate)=A |
| achieved_recovery_ratio, achieved_permeate_flow_rate | achieved_recovery_ratio   achieved_permeate_flow_rate (no edge) | achieved_recovery_ratio   achieved_permeate_flow_rate (no edge) | achieved_recovery_ratio->achieved_permeate_flow_rate | achieved_recovery_ratio->achieved_permeate_flow_rate | achieved_recovery_ratio->achieved_permeate_flow_rate | achieved_recovery_ratio -> achieved_permeate_flow_rate | (achieved_recovery_ratio, achieved_permeate_flow_rate)=A |
| true_permeate_salt, intrinsic_permeability | intrinsic_permeability->true_permeate_salt | intrinsic_permeability->true_permeate_salt | true_permeate_salt->intrinsic_permeability | true_permeate_salt->intrinsic_permeability | true_permeate_salt->intrinsic_permeability | intrinsic_permeability -> true_permeate_salt | (true_permeate_salt, intrinsic_permeability)=A |
| true_permeate_salt, observed_permeate_conductivity | true_permeate_salt   observed_permeate_conductivity (no edge) | true_permeate_salt   observed_permeate_conductivity (no edge) | observed_permeate_conductivity->true_permeate_salt | observed_permeate_conductivity->true_permeate_salt | observed_permeate_conductivity->true_permeate_salt | no edge | (true_permeate_salt, observed_permeate_conductivity)=B |
| antiscalant_effectiveness, recovery_ratio_target | antiscalant_effectiveness->recovery_ratio_target | antiscalant_effectiveness->recovery_ratio_target | antiscalant_effectiveness   recovery_ratio_target (no edge) | antiscalant_effectiveness   recovery_ratio_target (no edge) | antiscalant_effectiveness   recovery_ratio_target (no edge) | antiscalant_effectiveness -> recovery_ratio_target | (antiscalant_effectiveness, recovery_ratio_target)=C |
| antiscalant_effectiveness, deposition_rate | antiscalant_effectiveness   deposition_rate (no edge) | antiscalant_effectiveness   deposition_rate (no edge) | antiscalant_effectiveness->deposition_rate | antiscalant_effectiveness->deposition_rate | antiscalant_effectiveness->deposition_rate | no edge | (antiscalant_effectiveness, deposition_rate)=A |
| antiscalant_effectiveness, achieved_permeate_flow_rate | antiscalant_effectiveness   achieved_permeate_flow_rate (no edge) | antiscalant_effectiveness   achieved_permeate_flow_rate (no edge) | antiscalant_effectiveness->achieved_permeate_flow_rate | antiscalant_effectiveness->achieved_permeate_flow_rate | antiscalant_effectiveness->achieved_permeate_flow_rate | no edge | (antiscalant_effectiveness, achieved_permeate_flow_rate)=A |
| intrinsic_permeability, achieved_permeate_flow_rate | achieved_permeate_flow_rate->intrinsic_permeability | achieved_permeate_flow_rate->intrinsic_permeability | intrinsic_permeability   achieved_permeate_flow_rate (no edge) | intrinsic_permeability   achieved_permeate_flow_rate (no edge) | intrinsic_permeability   achieved_permeate_flow_rate (no edge) | achieved_permeate_flow_rate -> intrinsic_permeability | (intrinsic_permeability, achieved_permeate_flow_rate)=C |
| required_tmp, recovery_ratio_target | required_tmp <-> recovery_ratio_target | required_tmp   recovery_ratio_target (no edge) | required_tmp   recovery_ratio_target (no edge) | required_tmp   recovery_ratio_target (no edge) | required_tmp   recovery_ratio_target (no edge) | no edge | (required_tmp, recovery_ratio_target)=C |
| required_tmp, feed_temperature | required_tmp   feed_temperature (no edge) | required_tmp   feed_temperature (no edge) | feed_temperature->required_tmp | feed_temperature->required_tmp | feed_temperature->required_tmp | no edge | (required_tmp, feed_temperature)=B |
| required_tmp, specific_energy_consumption | required_tmp   specific_energy_consumption (no edge) | required_tmp   specific_energy_consumption (no edge) | required_tmp->specific_energy_consumption | required_tmp->specific_energy_consumption | required_tmp->specific_energy_consumption | no edge | (required_tmp, specific_energy_consumption)=A |
| required_tmp, achieved_permeate_flow_rate | required_tmp   achieved_permeate_flow_rate (no edge) | required_tmp   achieved_permeate_flow_rate (no edge) | achieved_permeate_flow_rate->required_tmp | achieved_permeate_flow_rate->required_tmp | achieved_permeate_flow_rate->required_tmp | no edge | (required_tmp, achieved_permeate_flow_rate)=B |
| recovery_ratio_target, feed_temperature | recovery_ratio_target <-> feed_temperature | recovery_ratio_target   feed_temperature (no edge) | recovery_ratio_target   feed_temperature (no edge) | recovery_ratio_target   feed_temperature (no edge) | recovery_ratio_target   feed_temperature (no edge) | recovery_ratio_target -> feed_temperature | (recovery_ratio_target, feed_temperature)=D |
| recovery_ratio_target, pretreatment_fouling_potential | pretreatment_fouling_potential->recovery_ratio_target | recovery_ratio_target   pretreatment_fouling_potential (no edge) | recovery_ratio_target   pretreatment_fouling_potential (no edge) | recovery_ratio_target   pretreatment_fouling_potential (no edge) | recovery_ratio_target   pretreatment_fouling_potential (no edge) | no edge | (recovery_ratio_target, pretreatment_fouling_potential)=D |
| recovery_ratio_target, achieved_permeate_flow_rate | recovery_ratio_target   achieved_permeate_flow_rate (no edge) | recovery_ratio_target   achieved_permeate_flow_rate (no edge) | recovery_ratio_target->achieved_permeate_flow_rate | recovery_ratio_target->achieved_permeate_flow_rate | recovery_ratio_target->achieved_permeate_flow_rate | no edge | (recovery_ratio_target, achieved_permeate_flow_rate)=A |
| feed_temperature, specific_energy_consumption | feed_temperature   specific_energy_consumption (no edge) | feed_temperature   specific_energy_consumption (no edge) | feed_temperature->specific_energy_consumption | feed_temperature->specific_energy_consumption | feed_temperature->specific_energy_consumption | specific_energy_consumption -> feed_temperature | (feed_temperature, specific_energy_consumption)=A |
| feed_temperature, achieved_permeate_flow_rate | feed_temperature   achieved_permeate_flow_rate (no edge) | feed_temperature   achieved_permeate_flow_rate (no edge) | feed_temperature->achieved_permeate_flow_rate | feed_temperature->achieved_permeate_flow_rate | feed_temperature->achieved_permeate_flow_rate | no edge | (feed_temperature, achieved_permeate_flow_rate)=A |
| deposition_rate, fouling_stock_prior | deposition_rate   fouling_stock_prior (no edge) | deposition_rate   fouling_stock_prior (no edge) | fouling_stock_prior->deposition_rate | deposition_rate   fouling_stock_prior (no edge) | deposition_rate   fouling_stock_prior (no edge) | no edge | (deposition_rate, fouling_stock_prior)=B |
| deposition_rate, pretreatment_fouling_potential | deposition_rate   pretreatment_fouling_potential (no edge) | deposition_rate   pretreatment_fouling_potential (no edge) | pretreatment_fouling_potential->deposition_rate | deposition_rate   pretreatment_fouling_potential (no edge) | deposition_rate   pretreatment_fouling_potential (no edge) | no edge | (deposition_rate, pretreatment_fouling_potential)=B |
| deposition_rate, specific_energy_consumption | deposition_rate   specific_energy_consumption (no edge) | deposition_rate   specific_energy_consumption (no edge) | deposition_rate->specific_energy_consumption | deposition_rate->specific_energy_consumption | deposition_rate->specific_energy_consumption | no edge | (deposition_rate, specific_energy_consumption)=A |
| deposition_rate, achieved_permeate_flow_rate | deposition_rate   achieved_permeate_flow_rate (no edge) | deposition_rate   achieved_permeate_flow_rate (no edge) | achieved_permeate_flow_rate->deposition_rate | deposition_rate   achieved_permeate_flow_rate (no edge) | deposition_rate   achieved_permeate_flow_rate (no edge) | no edge | (deposition_rate, achieved_permeate_flow_rate)=B |
| fouling_stock_prior, achieved_permeate_flow_rate | fouling_stock_prior o-> achieved_permeate_flow_rate | fouling_stock_prior   achieved_permeate_flow_rate (no edge) | fouling_stock_prior   achieved_permeate_flow_rate (no edge) | fouling_stock_prior   achieved_permeate_flow_rate (no edge) | fouling_stock_prior   achieved_permeate_flow_rate (no edge) | achieved_permeate_flow_rate -> fouling_stock_prior | (fouling_stock_prior, achieved_permeate_flow_rate)=C |
| daily_production_demand, specific_energy_consumption | daily_production_demand   specific_energy_consumption (no edge) | daily_production_demand   specific_energy_consumption (no edge) | daily_production_demand->specific_energy_consumption | daily_production_demand->specific_energy_consumption | daily_production_demand->specific_energy_consumption | no edge | (daily_production_demand, specific_energy_consumption)=A |
| daily_production_demand, achieved_permeate_flow_rate | daily_production_demand   achieved_permeate_flow_rate (no edge) | daily_production_demand   achieved_permeate_flow_rate (no edge) | daily_production_demand->achieved_permeate_flow_rate | daily_production_demand->achieved_permeate_flow_rate | daily_production_demand->achieved_permeate_flow_rate | no edge | (daily_production_demand, achieved_permeate_flow_rate)=A |
| specific_energy_consumption, achieved_permeate_flow_rate | specific_energy_consumption   achieved_permeate_flow_rate (no edge) | specific_energy_consumption   achieved_permeate_flow_rate (no edge) | achieved_permeate_flow_rate->specific_energy_consumption | specific_energy_consumption   achieved_permeate_flow_rate (no edge) | specific_energy_consumption   achieved_permeate_flow_rate (no edge) | no edge | (specific_energy_consumption, achieved_permeate_flow_rate)=B |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
