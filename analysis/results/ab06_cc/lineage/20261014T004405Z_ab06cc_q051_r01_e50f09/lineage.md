# Edge lineage: 20261014T004405Z_ab06cc_q051_r01_e50f09

Dataset `/research/datasets/suite_q1s2/q051/q051.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 20 variables, 190 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 17 | 0.76 | 0.34 | 0.47 | 5 | 0 | 8 | 37 |
| S1 after bootstrap edits | 5 | 0.80 | 0.11 | 0.19 | 3 | 0 | 1 | 36 |
| S2 after LLM review | 46 | 0.50 | 0.61 | 0.55 | 9 | 14 | 0 | 54 |
| S3 after KCI pruning | 46 | 0.50 | 0.61 | 0.55 | 9 | 14 | 0 | 54 |
| S4 final (after cycle step) | 46 | 0.50 | 0.61 | 0.55 | 9 | 14 | 0 | 54 |

Scored against: reference graph s2_05_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 12. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 20 calls, 190 distinct pairs answered out of 190, plus 20 self-pairs. Letters: {"A": 46, "C": 140, "D": 4}.
- LLM effect: added 42 (of which 29 where the resamples showed no edge at frequency >= 0.9), removed 1, re-oriented 3.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 46 edges; set by {"llm": 45, "algorithm (unchanged)": 1}; 1 identical to the algorithm's output; 34 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| retail_list_price_dollars->cycle_gross_margin_dollars | llm | yes | 0.00 |
| retail_list_price_dollars->demand_forecast_units_per_day | llm | no | 1.00 |
| retail_list_price_dollars->markdown_policy_schedule | llm | no | 1.00 |
| retail_list_price_dollars->tentative_order_quantity_units | llm | no | 1.00 |
| cycle_gross_margin_dollars->demand_forecast_units_per_day | llm | no | 1.00 |
| cycle_gross_margin_dollars->markdown_policy_schedule | llm | no | 1.00 |
| cycle_gross_margin_dollars->tentative_order_quantity_units | llm | yes | 0.05 |
| cycle_gross_margin_dollars->unit_wholesale_price | llm | no | 1.00 |
| lead_time_days->stockout_days_count | llm | no | 0.60 |
| lead_time_days->reorder_point_units | llm | no | 1.00 |
| waste_units_disposed->stockout_days_count | llm | yes | 0.90 |
| waste_units_disposed->demand_forecast_units_per_day | llm | no | 1.00 |
| waste_units_disposed->shelf_capacity_units | llm | no | 1.00 |
| waste_units_disposed->markdown_policy_schedule | llm | yes | 0.00 |
| waste_units_disposed->reorder_point_units | llm | no | 0.90 |
| waste_units_disposed->tentative_order_quantity_units | llm | yes | 0.40 |
| waste_units_disposed->on_hand_units_at_open | llm | no | 0.70 |
| stockout_days_count->demand_forecast_units_per_day | llm | no | 1.00 |
| stockout_days_count->reorder_point_units | llm | no | 1.00 |
| stockout_days_count->tentative_order_quantity_units | llm | no | 0.70 |
| stockout_days_count->on_hand_units_at_open | llm | yes | 0.25 |
| demand_forecast_units_per_day->reorder_point_units | llm | yes | 0.00 |
| demand_forecast_units_per_day->tentative_order_quantity_units | algorithm (unchanged) | yes | 0.00 |
| shelf_capacity_units->reorder_point_units | llm | no | 0.95 |
| shelf_capacity_units->tentative_order_quantity_units | llm | no | 1.00 |
| shelf_capacity_units->on_hand_units_at_open | llm | no | 0.90 |
| markdown_policy_schedule->chosen_service_level | llm | no | 0.95 |
| markdown_policy_schedule->tentative_order_quantity_units | llm | no | 1.00 |
| credit_draw_amount_dollars->interest_expense_dollars | llm | no | 0.35 |
| credit_draw_amount_dollars->available_credit_dollars | llm | yes | 0.40 |
| credit_draw_amount_dollars->cash_on_hand_dollars | llm | yes | 0.00 |
| credit_line_offer_flag->early_payment_choice | llm | no | 1.00 |
| credit_line_offer_flag->available_credit_dollars | llm | yes | 0.00 |
| interest_expense_dollars->interest_rate_apr | llm | no | 1.00 |
| interest_expense_dollars->available_credit_dollars | llm | no | 0.95 |
| interest_expense_dollars->cash_on_hand_dollars | llm | no | 0.90 |
| reorder_point_units->chosen_service_level | llm | no | 1.00 |
| reorder_point_units->tentative_order_quantity_units | llm | no | 0.50 |
| reorder_point_units->on_hand_units_at_open | llm | no | 1.00 |
| interest_rate_apr->available_credit_dollars | llm | no | 0.95 |
| interest_rate_apr->cash_on_hand_dollars | llm | no | 1.00 |
| chosen_service_level->tentative_order_quantity_units | llm | no | 1.00 |
| tentative_order_quantity_units->on_hand_units_at_open | llm | yes | 0.00 |
| early_payment_choice->available_credit_dollars | llm | no | 1.00 |
| early_payment_choice->cash_on_hand_dollars | llm | no | 0.80 |
| available_credit_dollars->cash_on_hand_dollars | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| retail_list_price_dollars, cycle_gross_margin_dollars | retail_list_price_dollars <-> cycle_gross_margin_dollars | retail_list_price_dollars   cycle_gross_margin_dollars (no edge) | retail_list_price_dollars->cycle_gross_margin_dollars | retail_list_price_dollars->cycle_gross_margin_dollars | retail_list_price_dollars->cycle_gross_margin_dollars | retail_list_price_dollars -> cycle_gross_margin_dollars | (retail_list_price_dollars, cycle_gross_margin_dollars)=A |
| retail_list_price_dollars, lead_time_days | retail_list_price_dollars <-> lead_time_days | retail_list_price_dollars   lead_time_days (no edge) | retail_list_price_dollars   lead_time_days (no edge) | retail_list_price_dollars   lead_time_days (no edge) | retail_list_price_dollars   lead_time_days (no edge) | no edge | (retail_list_price_dollars, lead_time_days)=C |
| retail_list_price_dollars, demand_forecast_units_per_day | retail_list_price_dollars   demand_forecast_units_per_day (no edge) | retail_list_price_dollars   demand_forecast_units_per_day (no edge) | retail_list_price_dollars->demand_forecast_units_per_day | retail_list_price_dollars->demand_forecast_units_per_day | retail_list_price_dollars->demand_forecast_units_per_day | no edge | (retail_list_price_dollars, demand_forecast_units_per_day)=A |
| retail_list_price_dollars, markdown_policy_schedule | retail_list_price_dollars   markdown_policy_schedule (no edge) | retail_list_price_dollars   markdown_policy_schedule (no edge) | retail_list_price_dollars->markdown_policy_schedule | retail_list_price_dollars->markdown_policy_schedule | retail_list_price_dollars->markdown_policy_schedule | no edge | (retail_list_price_dollars, markdown_policy_schedule)=A |
| retail_list_price_dollars, tentative_order_quantity_units | retail_list_price_dollars   tentative_order_quantity_units (no edge) | retail_list_price_dollars   tentative_order_quantity_units (no edge) | retail_list_price_dollars->tentative_order_quantity_units | retail_list_price_dollars->tentative_order_quantity_units | retail_list_price_dollars->tentative_order_quantity_units | no edge | (retail_list_price_dollars, tentative_order_quantity_units)=A |
| cycle_gross_margin_dollars, demand_forecast_units_per_day | cycle_gross_margin_dollars   demand_forecast_units_per_day (no edge) | cycle_gross_margin_dollars   demand_forecast_units_per_day (no edge) | cycle_gross_margin_dollars->demand_forecast_units_per_day | cycle_gross_margin_dollars->demand_forecast_units_per_day | cycle_gross_margin_dollars->demand_forecast_units_per_day | demand_forecast_units_per_day -> cycle_gross_margin_dollars | (cycle_gross_margin_dollars, demand_forecast_units_per_day)=A |
| cycle_gross_margin_dollars, markdown_policy_schedule | cycle_gross_margin_dollars   markdown_policy_schedule (no edge) | cycle_gross_margin_dollars   markdown_policy_schedule (no edge) | cycle_gross_margin_dollars->markdown_policy_schedule | cycle_gross_margin_dollars->markdown_policy_schedule | cycle_gross_margin_dollars->markdown_policy_schedule | markdown_policy_schedule -> cycle_gross_margin_dollars | (cycle_gross_margin_dollars, markdown_policy_schedule)=A |
| cycle_gross_margin_dollars, tentative_order_quantity_units | tentative_order_quantity_units->cycle_gross_margin_dollars | tentative_order_quantity_units->cycle_gross_margin_dollars | cycle_gross_margin_dollars->tentative_order_quantity_units | cycle_gross_margin_dollars->tentative_order_quantity_units | cycle_gross_margin_dollars->tentative_order_quantity_units | tentative_order_quantity_units -> cycle_gross_margin_dollars | (cycle_gross_margin_dollars, tentative_order_quantity_units)=A |
| cycle_gross_margin_dollars, unit_wholesale_price | cycle_gross_margin_dollars   unit_wholesale_price (no edge) | cycle_gross_margin_dollars   unit_wholesale_price (no edge) | cycle_gross_margin_dollars->unit_wholesale_price | cycle_gross_margin_dollars->unit_wholesale_price | cycle_gross_margin_dollars->unit_wholesale_price | unit_wholesale_price -> cycle_gross_margin_dollars | (cycle_gross_margin_dollars, unit_wholesale_price)=A |
| lead_time_days, stockout_days_count | lead_time_days   stockout_days_count (no edge) | lead_time_days   stockout_days_count (no edge) | lead_time_days->stockout_days_count | lead_time_days->stockout_days_count | lead_time_days->stockout_days_count | lead_time_days -> stockout_days_count | (lead_time_days, stockout_days_count)=A |
| lead_time_days, reorder_point_units | lead_time_days   reorder_point_units (no edge) | lead_time_days   reorder_point_units (no edge) | lead_time_days->reorder_point_units | lead_time_days->reorder_point_units | lead_time_days->reorder_point_units | no edge | (lead_time_days, reorder_point_units)=A |
| lead_time_days, chosen_service_level | chosen_service_level o-> lead_time_days | lead_time_days   chosen_service_level (no edge) | lead_time_days   chosen_service_level (no edge) | lead_time_days   chosen_service_level (no edge) | lead_time_days   chosen_service_level (no edge) | chosen_service_level -> lead_time_days | (lead_time_days, chosen_service_level)=C |
| waste_units_disposed, stockout_days_count | stockout_days_count->waste_units_disposed | waste_units_disposed   stockout_days_count (no edge) | waste_units_disposed->stockout_days_count | waste_units_disposed->stockout_days_count | waste_units_disposed->stockout_days_count | no edge | (waste_units_disposed, stockout_days_count)=A |
| waste_units_disposed, demand_forecast_units_per_day | waste_units_disposed   demand_forecast_units_per_day (no edge) | waste_units_disposed   demand_forecast_units_per_day (no edge) | waste_units_disposed->demand_forecast_units_per_day | waste_units_disposed->demand_forecast_units_per_day | waste_units_disposed->demand_forecast_units_per_day | demand_forecast_units_per_day -> waste_units_disposed | (waste_units_disposed, demand_forecast_units_per_day)=A |
| waste_units_disposed, shelf_capacity_units | waste_units_disposed   shelf_capacity_units (no edge) | waste_units_disposed   shelf_capacity_units (no edge) | waste_units_disposed->shelf_capacity_units | waste_units_disposed->shelf_capacity_units | waste_units_disposed->shelf_capacity_units | no edge | (waste_units_disposed, shelf_capacity_units)=A |
| waste_units_disposed, markdown_policy_schedule | markdown_policy_schedule->waste_units_disposed | waste_units_disposed   markdown_policy_schedule (no edge) | waste_units_disposed->markdown_policy_schedule | waste_units_disposed->markdown_policy_schedule | waste_units_disposed->markdown_policy_schedule | markdown_policy_schedule -> waste_units_disposed | (waste_units_disposed, markdown_policy_schedule)=A |
| waste_units_disposed, reorder_point_units | waste_units_disposed   reorder_point_units (no edge) | waste_units_disposed   reorder_point_units (no edge) | waste_units_disposed->reorder_point_units | waste_units_disposed->reorder_point_units | waste_units_disposed->reorder_point_units | no edge | (waste_units_disposed, reorder_point_units)=A |
| waste_units_disposed, tentative_order_quantity_units | tentative_order_quantity_units->waste_units_disposed | waste_units_disposed   tentative_order_quantity_units (no edge) | waste_units_disposed->tentative_order_quantity_units | waste_units_disposed->tentative_order_quantity_units | waste_units_disposed->tentative_order_quantity_units | tentative_order_quantity_units -> waste_units_disposed | (waste_units_disposed, tentative_order_quantity_units)=A |
| waste_units_disposed, on_hand_units_at_open | waste_units_disposed   on_hand_units_at_open (no edge) | waste_units_disposed   on_hand_units_at_open (no edge) | waste_units_disposed->on_hand_units_at_open | waste_units_disposed->on_hand_units_at_open | waste_units_disposed->on_hand_units_at_open | no edge | (waste_units_disposed, on_hand_units_at_open)=A |
| stockout_days_count, demand_forecast_units_per_day | stockout_days_count   demand_forecast_units_per_day (no edge) | stockout_days_count   demand_forecast_units_per_day (no edge) | stockout_days_count->demand_forecast_units_per_day | stockout_days_count->demand_forecast_units_per_day | stockout_days_count->demand_forecast_units_per_day | demand_forecast_units_per_day -> stockout_days_count | (stockout_days_count, demand_forecast_units_per_day)=A |
| stockout_days_count, reorder_point_units | stockout_days_count   reorder_point_units (no edge) | stockout_days_count   reorder_point_units (no edge) | stockout_days_count->reorder_point_units | stockout_days_count->reorder_point_units | stockout_days_count->reorder_point_units | no edge | (stockout_days_count, reorder_point_units)=A |
| stockout_days_count, tentative_order_quantity_units | stockout_days_count   tentative_order_quantity_units (no edge) | stockout_days_count   tentative_order_quantity_units (no edge) | stockout_days_count->tentative_order_quantity_units | stockout_days_count->tentative_order_quantity_units | stockout_days_count->tentative_order_quantity_units | no edge | (stockout_days_count, tentative_order_quantity_units)=A |
| stockout_days_count, on_hand_units_at_open | stockout_days_count o-o on_hand_units_at_open | stockout_days_count   on_hand_units_at_open (no edge) | stockout_days_count->on_hand_units_at_open | stockout_days_count->on_hand_units_at_open | stockout_days_count->on_hand_units_at_open | on_hand_units_at_open -> stockout_days_count | (stockout_days_count, on_hand_units_at_open)=A |
| demand_forecast_units_per_day, reorder_point_units | demand_forecast_units_per_day o-o reorder_point_units | demand_forecast_units_per_day   reorder_point_units (no edge) | demand_forecast_units_per_day->reorder_point_units | demand_forecast_units_per_day->reorder_point_units | demand_forecast_units_per_day->reorder_point_units | demand_forecast_units_per_day -> reorder_point_units | (demand_forecast_units_per_day, reorder_point_units)=A |
| shelf_capacity_units, reorder_point_units | shelf_capacity_units   reorder_point_units (no edge) | shelf_capacity_units   reorder_point_units (no edge) | shelf_capacity_units->reorder_point_units | shelf_capacity_units->reorder_point_units | shelf_capacity_units->reorder_point_units | no edge | (shelf_capacity_units, reorder_point_units)=A |
| shelf_capacity_units, tentative_order_quantity_units | shelf_capacity_units   tentative_order_quantity_units (no edge) | shelf_capacity_units   tentative_order_quantity_units (no edge) | shelf_capacity_units->tentative_order_quantity_units | shelf_capacity_units->tentative_order_quantity_units | shelf_capacity_units->tentative_order_quantity_units | shelf_capacity_units -> tentative_order_quantity_units | (shelf_capacity_units, tentative_order_quantity_units)=A |
| shelf_capacity_units, on_hand_units_at_open | shelf_capacity_units   on_hand_units_at_open (no edge) | shelf_capacity_units   on_hand_units_at_open (no edge) | shelf_capacity_units->on_hand_units_at_open | shelf_capacity_units->on_hand_units_at_open | shelf_capacity_units->on_hand_units_at_open | no edge | (shelf_capacity_units, on_hand_units_at_open)=A |
| markdown_policy_schedule, chosen_service_level | markdown_policy_schedule   chosen_service_level (no edge) | markdown_policy_schedule   chosen_service_level (no edge) | markdown_policy_schedule->chosen_service_level | markdown_policy_schedule->chosen_service_level | markdown_policy_schedule->chosen_service_level | no edge | (markdown_policy_schedule, chosen_service_level)=A |
| markdown_policy_schedule, tentative_order_quantity_units | markdown_policy_schedule   tentative_order_quantity_units (no edge) | markdown_policy_schedule   tentative_order_quantity_units (no edge) | markdown_policy_schedule->tentative_order_quantity_units | markdown_policy_schedule->tentative_order_quantity_units | markdown_policy_schedule->tentative_order_quantity_units | no edge | (markdown_policy_schedule, tentative_order_quantity_units)=A |
| markdown_policy_schedule, unit_wholesale_price | markdown_policy_schedule o-o unit_wholesale_price | markdown_policy_schedule   unit_wholesale_price (no edge) | markdown_policy_schedule   unit_wholesale_price (no edge) | markdown_policy_schedule   unit_wholesale_price (no edge) | markdown_policy_schedule   unit_wholesale_price (no edge) | no edge | (markdown_policy_schedule, unit_wholesale_price)=C |
| credit_draw_amount_dollars, credit_line_offer_flag | credit_line_offer_flag o-> credit_draw_amount_dollars | credit_line_offer_flag o-> credit_draw_amount_dollars | credit_draw_amount_dollars   credit_line_offer_flag (no edge) | credit_draw_amount_dollars   credit_line_offer_flag (no edge) | credit_draw_amount_dollars   credit_line_offer_flag (no edge) | no edge | (credit_draw_amount_dollars, credit_line_offer_flag)=C |
| credit_draw_amount_dollars, interest_expense_dollars | credit_draw_amount_dollars   interest_expense_dollars (no edge) | credit_draw_amount_dollars   interest_expense_dollars (no edge) | credit_draw_amount_dollars->interest_expense_dollars | credit_draw_amount_dollars->interest_expense_dollars | credit_draw_amount_dollars->interest_expense_dollars | credit_draw_amount_dollars -> interest_expense_dollars | (credit_draw_amount_dollars, interest_expense_dollars)=A |
| credit_draw_amount_dollars, available_credit_dollars | available_credit_dollars o-> credit_draw_amount_dollars | credit_draw_amount_dollars   available_credit_dollars (no edge) | credit_draw_amount_dollars->available_credit_dollars | credit_draw_amount_dollars->available_credit_dollars | credit_draw_amount_dollars->available_credit_dollars | available_credit_dollars -> credit_draw_amount_dollars | (credit_draw_amount_dollars, available_credit_dollars)=A |
| credit_draw_amount_dollars, cash_on_hand_dollars | cash_on_hand_dollars o-> credit_draw_amount_dollars | credit_draw_amount_dollars   cash_on_hand_dollars (no edge) | credit_draw_amount_dollars->cash_on_hand_dollars | credit_draw_amount_dollars->cash_on_hand_dollars | credit_draw_amount_dollars->cash_on_hand_dollars | cash_on_hand_dollars -> credit_draw_amount_dollars | (credit_draw_amount_dollars, cash_on_hand_dollars)=A |
| credit_line_offer_flag, early_payment_choice | credit_line_offer_flag   early_payment_choice (no edge) | credit_line_offer_flag   early_payment_choice (no edge) | credit_line_offer_flag->early_payment_choice | credit_line_offer_flag->early_payment_choice | credit_line_offer_flag->early_payment_choice | no edge | (credit_line_offer_flag, early_payment_choice)=A |
| credit_line_offer_flag, available_credit_dollars | credit_line_offer_flag ~~~ available_credit_dollars | credit_line_offer_flag ~~~ available_credit_dollars | credit_line_offer_flag->available_credit_dollars | credit_line_offer_flag->available_credit_dollars | credit_line_offer_flag->available_credit_dollars | credit_line_offer_flag -> available_credit_dollars | (credit_line_offer_flag, available_credit_dollars)=A |
| interest_expense_dollars, interest_rate_apr | interest_expense_dollars   interest_rate_apr (no edge) | interest_expense_dollars   interest_rate_apr (no edge) | interest_expense_dollars->interest_rate_apr | interest_expense_dollars->interest_rate_apr | interest_expense_dollars->interest_rate_apr | interest_rate_apr -> interest_expense_dollars | (interest_expense_dollars, interest_rate_apr)=A |
| interest_expense_dollars, early_payment_choice | interest_expense_dollars o-o early_payment_choice | interest_expense_dollars   early_payment_choice (no edge) | interest_expense_dollars   early_payment_choice (no edge) | interest_expense_dollars   early_payment_choice (no edge) | interest_expense_dollars   early_payment_choice (no edge) | early_payment_choice -> interest_expense_dollars | (interest_expense_dollars, early_payment_choice)=C |
| interest_expense_dollars, available_credit_dollars | interest_expense_dollars   available_credit_dollars (no edge) | interest_expense_dollars   available_credit_dollars (no edge) | interest_expense_dollars->available_credit_dollars | interest_expense_dollars->available_credit_dollars | interest_expense_dollars->available_credit_dollars | no edge | (interest_expense_dollars, available_credit_dollars)=A |
| interest_expense_dollars, cash_on_hand_dollars | interest_expense_dollars   cash_on_hand_dollars (no edge) | interest_expense_dollars   cash_on_hand_dollars (no edge) | interest_expense_dollars->cash_on_hand_dollars | interest_expense_dollars->cash_on_hand_dollars | interest_expense_dollars->cash_on_hand_dollars | no edge | (interest_expense_dollars, cash_on_hand_dollars)=A |
| reorder_point_units, chosen_service_level | reorder_point_units   chosen_service_level (no edge) | reorder_point_units   chosen_service_level (no edge) | reorder_point_units->chosen_service_level | reorder_point_units->chosen_service_level | reorder_point_units->chosen_service_level | reorder_point_units -> chosen_service_level | (reorder_point_units, chosen_service_level)=A |
| reorder_point_units, tentative_order_quantity_units | reorder_point_units   tentative_order_quantity_units (no edge) | reorder_point_units   tentative_order_quantity_units (no edge) | reorder_point_units->tentative_order_quantity_units | reorder_point_units->tentative_order_quantity_units | reorder_point_units->tentative_order_quantity_units | reorder_point_units -> tentative_order_quantity_units | (reorder_point_units, tentative_order_quantity_units)=A |
| reorder_point_units, on_hand_units_at_open | reorder_point_units   on_hand_units_at_open (no edge) | reorder_point_units   on_hand_units_at_open (no edge) | reorder_point_units->on_hand_units_at_open | reorder_point_units->on_hand_units_at_open | reorder_point_units->on_hand_units_at_open | no edge | (reorder_point_units, on_hand_units_at_open)=A |
| interest_rate_apr, available_credit_dollars | interest_rate_apr   available_credit_dollars (no edge) | interest_rate_apr   available_credit_dollars (no edge) | interest_rate_apr->available_credit_dollars | interest_rate_apr->available_credit_dollars | interest_rate_apr->available_credit_dollars | no edge | (interest_rate_apr, available_credit_dollars)=A |
| interest_rate_apr, cash_on_hand_dollars | interest_rate_apr   cash_on_hand_dollars (no edge) | interest_rate_apr   cash_on_hand_dollars (no edge) | interest_rate_apr->cash_on_hand_dollars | interest_rate_apr->cash_on_hand_dollars | interest_rate_apr->cash_on_hand_dollars | no edge | (interest_rate_apr, cash_on_hand_dollars)=A |
| chosen_service_level, tentative_order_quantity_units | chosen_service_level   tentative_order_quantity_units (no edge) | chosen_service_level   tentative_order_quantity_units (no edge) | chosen_service_level->tentative_order_quantity_units | chosen_service_level->tentative_order_quantity_units | chosen_service_level->tentative_order_quantity_units | no edge | (chosen_service_level, tentative_order_quantity_units)=A |
| tentative_order_quantity_units, on_hand_units_at_open | on_hand_units_at_open->tentative_order_quantity_units | on_hand_units_at_open->tentative_order_quantity_units | tentative_order_quantity_units->on_hand_units_at_open | tentative_order_quantity_units->on_hand_units_at_open | tentative_order_quantity_units->on_hand_units_at_open | on_hand_units_at_open -> tentative_order_quantity_units | (tentative_order_quantity_units, on_hand_units_at_open)=A |
| early_payment_choice, available_credit_dollars | early_payment_choice   available_credit_dollars (no edge) | early_payment_choice   available_credit_dollars (no edge) | early_payment_choice->available_credit_dollars | early_payment_choice->available_credit_dollars | early_payment_choice->available_credit_dollars | no edge | (early_payment_choice, available_credit_dollars)=A |
| early_payment_choice, cash_on_hand_dollars | early_payment_choice   cash_on_hand_dollars (no edge) | early_payment_choice   cash_on_hand_dollars (no edge) | early_payment_choice->cash_on_hand_dollars | early_payment_choice->cash_on_hand_dollars | early_payment_choice->cash_on_hand_dollars | cash_on_hand_dollars -> early_payment_choice | (early_payment_choice, cash_on_hand_dollars)=A |
| available_credit_dollars, cash_on_hand_dollars | available_credit_dollars   cash_on_hand_dollars (no edge) | available_credit_dollars   cash_on_hand_dollars (no edge) | available_credit_dollars->cash_on_hand_dollars | available_credit_dollars->cash_on_hand_dollars | available_credit_dollars->cash_on_hand_dollars | no edge | (available_credit_dollars, cash_on_hand_dollars)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
