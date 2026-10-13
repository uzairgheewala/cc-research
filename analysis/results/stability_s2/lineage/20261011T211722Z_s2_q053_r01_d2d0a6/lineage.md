# Edge lineage: 20261011T211722Z_s2_q053_r01_d2d0a6

Dataset `/research/datasets/suite_q1s2/q053/q053.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 20 variables, 190 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 14 | 0.86 | 0.32 | 0.46 | 3 | 0 | 9 | 37 |
| S1 after bootstrap edits | 5 | 0.80 | 0.11 | 0.19 | 2 | 0 | 2 | 37 |
| S2 after LLM review | 28 | 0.11 | 0.08 | 0.09 | 1 | 2 | 0 | 62 |
| S3 after KCI pruning | 20 | 0.15 | 0.08 | 0.10 | 1 | 2 | 0 | 54 |
| S4 final (after cycle step) | 20 | 0.15 | 0.08 | 0.10 | 1 | 2 | 0 | 54 |

Scored against: reference graph s2_05_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 9. Of the deleted, 5 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 20 calls, 190 distinct pairs answered out of 190, plus 20 self-pairs. Letters: {"A": 17, "B": 11, "C": 159, "D": 3}.
- LLM effect: added 27 (of which 23 where the resamples showed no edge at frequency >= 0.9), removed 4, re-oriented 0.
- KCI step removed 8. Cycle step changed 0.
- Final graph: 20 edges; set by {"llm": 19, "algorithm (unchanged)": 1}; 1 identical to the algorithm's output; 18 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| cycle_gross_margin_dollars->retail_list_price_dollars | llm | yes | 0.55 |
| lead_time_days->stockout_days_count | llm | no | 1.00 |
| lead_time_days->reorder_point_units | llm | no | 1.00 |
| demand_forecast_units_per_day->retail_list_price_dollars | llm | no | 0.65 |
| retail_list_price_dollars->markdown_policy_schedule | llm | no | 1.00 |
| demand_forecast_units_per_day->reorder_point_units | llm | no | 1.00 |
| demand_forecast_units_per_day->tentative_order_quantity_units | llm | no | 1.00 |
| demand_forecast_units_per_day->chosen_service_level | llm | no | 1.00 |
| stockout_days_count->on_hand_units_at_open | llm | no | 0.95 |
| credit_draw_amount_dollars->interest_expense_dollars | llm | no | 1.00 |
| available_credit_dollars->credit_draw_amount_dollars | llm | no | 0.55 |
| interest_expense_dollars->interest_rate_apr | llm | no | 1.00 |
| credit_line_offer_flag->available_credit_dollars | llm | no | 1.00 |
| interest_rate_apr->cash_on_hand_dollars | llm | no | 1.00 |
| reorder_point_units->tentative_order_quantity_units | llm | no | 1.00 |
| reorder_point_units->chosen_service_level | llm | no | 0.90 |
| tentative_order_quantity_units->chosen_service_level | llm | no | 0.80 |
| tentative_order_quantity_units->on_hand_units_at_open | llm | no | 1.00 |
| early_payment_choice->unit_wholesale_price | algorithm (unchanged) | yes | 0.00 |
| cash_on_hand_dollars->early_payment_choice | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| cycle_gross_margin_dollars, lead_time_days | lead_time_days o-> cycle_gross_margin_dollars | cycle_gross_margin_dollars   lead_time_days (no edge) | cycle_gross_margin_dollars   lead_time_days (no edge) | cycle_gross_margin_dollars   lead_time_days (no edge) | cycle_gross_margin_dollars   lead_time_days (no edge) | cycle_gross_margin_dollars -> lead_time_days | (cycle_gross_margin_dollars, lead_time_days)=C |
| cycle_gross_margin_dollars, retail_list_price_dollars | cycle_gross_margin_dollars <-> retail_list_price_dollars | cycle_gross_margin_dollars   retail_list_price_dollars (no edge) | cycle_gross_margin_dollars->retail_list_price_dollars | cycle_gross_margin_dollars->retail_list_price_dollars | cycle_gross_margin_dollars->retail_list_price_dollars | no edge | (cycle_gross_margin_dollars, retail_list_price_dollars)=A |
| cycle_gross_margin_dollars, unit_wholesale_price | cycle_gross_margin_dollars   unit_wholesale_price (no edge) | cycle_gross_margin_dollars   unit_wholesale_price (no edge) | unit_wholesale_price->cycle_gross_margin_dollars | cycle_gross_margin_dollars   unit_wholesale_price (no edge) | cycle_gross_margin_dollars   unit_wholesale_price (no edge) | no edge | (cycle_gross_margin_dollars, unit_wholesale_price)=B |
| lead_time_days, stockout_days_count | lead_time_days   stockout_days_count (no edge) | lead_time_days   stockout_days_count (no edge) | lead_time_days->stockout_days_count | lead_time_days->stockout_days_count | lead_time_days->stockout_days_count | no edge | (lead_time_days, stockout_days_count)=A |
| lead_time_days, reorder_point_units | lead_time_days   reorder_point_units (no edge) | lead_time_days   reorder_point_units (no edge) | lead_time_days->reorder_point_units | lead_time_days->reorder_point_units | lead_time_days->reorder_point_units | no edge | (lead_time_days, reorder_point_units)=A |
| retail_list_price_dollars, demand_forecast_units_per_day | retail_list_price_dollars   demand_forecast_units_per_day (no edge) | retail_list_price_dollars   demand_forecast_units_per_day (no edge) | demand_forecast_units_per_day->retail_list_price_dollars | demand_forecast_units_per_day->retail_list_price_dollars | demand_forecast_units_per_day->retail_list_price_dollars | retail_list_price_dollars -> demand_forecast_units_per_day | (retail_list_price_dollars, demand_forecast_units_per_day)=B |
| retail_list_price_dollars, markdown_policy_schedule | retail_list_price_dollars   markdown_policy_schedule (no edge) | retail_list_price_dollars   markdown_policy_schedule (no edge) | retail_list_price_dollars->markdown_policy_schedule | retail_list_price_dollars->markdown_policy_schedule | retail_list_price_dollars->markdown_policy_schedule | no edge | (retail_list_price_dollars, markdown_policy_schedule)=A |
| retail_list_price_dollars, tentative_order_quantity_units | tentative_order_quantity_units o-> retail_list_price_dollars | tentative_order_quantity_units o-> retail_list_price_dollars | retail_list_price_dollars   tentative_order_quantity_units (no edge) | retail_list_price_dollars   tentative_order_quantity_units (no edge) | retail_list_price_dollars   tentative_order_quantity_units (no edge) | tentative_order_quantity_units -> retail_list_price_dollars | (retail_list_price_dollars, tentative_order_quantity_units)=C |
| retail_list_price_dollars, unit_wholesale_price | retail_list_price_dollars   unit_wholesale_price (no edge) | retail_list_price_dollars   unit_wholesale_price (no edge) | unit_wholesale_price->retail_list_price_dollars | retail_list_price_dollars   unit_wholesale_price (no edge) | retail_list_price_dollars   unit_wholesale_price (no edge) | no edge | (retail_list_price_dollars, unit_wholesale_price)=B |
| demand_forecast_units_per_day, stockout_days_count | demand_forecast_units_per_day   stockout_days_count (no edge) | demand_forecast_units_per_day   stockout_days_count (no edge) | stockout_days_count->demand_forecast_units_per_day | demand_forecast_units_per_day   stockout_days_count (no edge) | demand_forecast_units_per_day   stockout_days_count (no edge) | no edge | (demand_forecast_units_per_day, stockout_days_count)=B |
| demand_forecast_units_per_day, credit_draw_amount_dollars | credit_draw_amount_dollars o-> demand_forecast_units_per_day | demand_forecast_units_per_day   credit_draw_amount_dollars (no edge) | demand_forecast_units_per_day   credit_draw_amount_dollars (no edge) | demand_forecast_units_per_day   credit_draw_amount_dollars (no edge) | demand_forecast_units_per_day   credit_draw_amount_dollars (no edge) | credit_draw_amount_dollars -> demand_forecast_units_per_day | (demand_forecast_units_per_day, credit_draw_amount_dollars)=C |
| demand_forecast_units_per_day, reorder_point_units | demand_forecast_units_per_day   reorder_point_units (no edge) | demand_forecast_units_per_day   reorder_point_units (no edge) | demand_forecast_units_per_day->reorder_point_units | demand_forecast_units_per_day->reorder_point_units | demand_forecast_units_per_day->reorder_point_units | no edge | (demand_forecast_units_per_day, reorder_point_units)=A |
| demand_forecast_units_per_day, tentative_order_quantity_units | demand_forecast_units_per_day   tentative_order_quantity_units (no edge) | demand_forecast_units_per_day   tentative_order_quantity_units (no edge) | demand_forecast_units_per_day->tentative_order_quantity_units | demand_forecast_units_per_day->tentative_order_quantity_units | demand_forecast_units_per_day->tentative_order_quantity_units | no edge | (demand_forecast_units_per_day, tentative_order_quantity_units)=A |
| demand_forecast_units_per_day, unit_wholesale_price | unit_wholesale_price->demand_forecast_units_per_day | demand_forecast_units_per_day   unit_wholesale_price (no edge) | demand_forecast_units_per_day   unit_wholesale_price (no edge) | demand_forecast_units_per_day   unit_wholesale_price (no edge) | demand_forecast_units_per_day   unit_wholesale_price (no edge) | unit_wholesale_price -> demand_forecast_units_per_day | (demand_forecast_units_per_day, unit_wholesale_price)=C |
| demand_forecast_units_per_day, chosen_service_level | demand_forecast_units_per_day   chosen_service_level (no edge) | demand_forecast_units_per_day   chosen_service_level (no edge) | demand_forecast_units_per_day->chosen_service_level | demand_forecast_units_per_day->chosen_service_level | demand_forecast_units_per_day->chosen_service_level | no edge | (demand_forecast_units_per_day, chosen_service_level)=A |
| demand_forecast_units_per_day, on_hand_units_at_open | demand_forecast_units_per_day   on_hand_units_at_open (no edge) | demand_forecast_units_per_day   on_hand_units_at_open (no edge) | on_hand_units_at_open->demand_forecast_units_per_day | demand_forecast_units_per_day   on_hand_units_at_open (no edge) | demand_forecast_units_per_day   on_hand_units_at_open (no edge) | no edge | (demand_forecast_units_per_day, on_hand_units_at_open)=B |
| waste_units_disposed, early_payment_choice | waste_units_disposed o-o early_payment_choice | waste_units_disposed   early_payment_choice (no edge) | waste_units_disposed   early_payment_choice (no edge) | waste_units_disposed   early_payment_choice (no edge) | waste_units_disposed   early_payment_choice (no edge) | early_payment_choice -> waste_units_disposed | (waste_units_disposed, early_payment_choice)=C |
| shelf_capacity_units, interest_rate_apr | shelf_capacity_units o-o interest_rate_apr | shelf_capacity_units   interest_rate_apr (no edge) | shelf_capacity_units   interest_rate_apr (no edge) | shelf_capacity_units   interest_rate_apr (no edge) | shelf_capacity_units   interest_rate_apr (no edge) | shelf_capacity_units -> interest_rate_apr | (shelf_capacity_units, interest_rate_apr)=C |
| shelf_capacity_units, unit_wholesale_price | shelf_capacity_units->unit_wholesale_price | shelf_capacity_units->unit_wholesale_price | shelf_capacity_units   unit_wholesale_price (no edge) | shelf_capacity_units   unit_wholesale_price (no edge) | shelf_capacity_units   unit_wholesale_price (no edge) | shelf_capacity_units -> unit_wholesale_price | (shelf_capacity_units, unit_wholesale_price)=C |
| stockout_days_count, reorder_point_units | stockout_days_count   reorder_point_units (no edge) | stockout_days_count   reorder_point_units (no edge) | reorder_point_units->stockout_days_count | stockout_days_count   reorder_point_units (no edge) | stockout_days_count   reorder_point_units (no edge) | no edge | (stockout_days_count, reorder_point_units)=B |
| stockout_days_count, tentative_order_quantity_units | stockout_days_count   tentative_order_quantity_units (no edge) | stockout_days_count   tentative_order_quantity_units (no edge) | tentative_order_quantity_units->stockout_days_count | stockout_days_count   tentative_order_quantity_units (no edge) | stockout_days_count   tentative_order_quantity_units (no edge) | no edge | (stockout_days_count, tentative_order_quantity_units)=B |
| stockout_days_count, chosen_service_level | stockout_days_count   chosen_service_level (no edge) | stockout_days_count   chosen_service_level (no edge) | chosen_service_level->stockout_days_count | stockout_days_count   chosen_service_level (no edge) | stockout_days_count   chosen_service_level (no edge) | no edge | (stockout_days_count, chosen_service_level)=B |
| stockout_days_count, on_hand_units_at_open | stockout_days_count   on_hand_units_at_open (no edge) | stockout_days_count   on_hand_units_at_open (no edge) | stockout_days_count->on_hand_units_at_open | stockout_days_count->on_hand_units_at_open | stockout_days_count->on_hand_units_at_open | no edge | (stockout_days_count, on_hand_units_at_open)=A |
| credit_draw_amount_dollars, interest_expense_dollars | credit_draw_amount_dollars   interest_expense_dollars (no edge) | credit_draw_amount_dollars   interest_expense_dollars (no edge) | credit_draw_amount_dollars->interest_expense_dollars | credit_draw_amount_dollars->interest_expense_dollars | credit_draw_amount_dollars->interest_expense_dollars | no edge | (credit_draw_amount_dollars, interest_expense_dollars)=A |
| credit_draw_amount_dollars, credit_line_offer_flag | credit_draw_amount_dollars   credit_line_offer_flag (no edge) | credit_draw_amount_dollars   credit_line_offer_flag (no edge) | credit_line_offer_flag->credit_draw_amount_dollars | credit_draw_amount_dollars   credit_line_offer_flag (no edge) | credit_draw_amount_dollars   credit_line_offer_flag (no edge) | no edge | (credit_draw_amount_dollars, credit_line_offer_flag)=B |
| credit_draw_amount_dollars, available_credit_dollars | credit_draw_amount_dollars   available_credit_dollars (no edge) | credit_draw_amount_dollars   available_credit_dollars (no edge) | available_credit_dollars->credit_draw_amount_dollars | available_credit_dollars->credit_draw_amount_dollars | available_credit_dollars->credit_draw_amount_dollars | no edge | (credit_draw_amount_dollars, available_credit_dollars)=B |
| markdown_policy_schedule, interest_expense_dollars | interest_expense_dollars o-> markdown_policy_schedule | interest_expense_dollars o-> markdown_policy_schedule | markdown_policy_schedule   interest_expense_dollars (no edge) | markdown_policy_schedule   interest_expense_dollars (no edge) | markdown_policy_schedule   interest_expense_dollars (no edge) | no edge | (markdown_policy_schedule, interest_expense_dollars)=C |
| markdown_policy_schedule, chosen_service_level | chosen_service_level o-> markdown_policy_schedule | markdown_policy_schedule   chosen_service_level (no edge) | markdown_policy_schedule   chosen_service_level (no edge) | markdown_policy_schedule   chosen_service_level (no edge) | markdown_policy_schedule   chosen_service_level (no edge) | chosen_service_level -> markdown_policy_schedule | (markdown_policy_schedule, chosen_service_level)=C |
| markdown_policy_schedule, on_hand_units_at_open | on_hand_units_at_open o-> markdown_policy_schedule | markdown_policy_schedule   on_hand_units_at_open (no edge) | markdown_policy_schedule   on_hand_units_at_open (no edge) | markdown_policy_schedule   on_hand_units_at_open (no edge) | markdown_policy_schedule   on_hand_units_at_open (no edge) | on_hand_units_at_open -> markdown_policy_schedule | (markdown_policy_schedule, on_hand_units_at_open)=C |
| interest_expense_dollars, interest_rate_apr | interest_expense_dollars   interest_rate_apr (no edge) | interest_expense_dollars   interest_rate_apr (no edge) | interest_expense_dollars->interest_rate_apr | interest_expense_dollars->interest_rate_apr | interest_expense_dollars->interest_rate_apr | no edge | (interest_expense_dollars, interest_rate_apr)=A |
| interest_expense_dollars, chosen_service_level | interest_expense_dollars ~~~ chosen_service_level | interest_expense_dollars ~~~ chosen_service_level | interest_expense_dollars   chosen_service_level (no edge) | interest_expense_dollars   chosen_service_level (no edge) | interest_expense_dollars   chosen_service_level (no edge) | interest_expense_dollars -> chosen_service_level | (interest_expense_dollars, chosen_service_level)=C |
| credit_line_offer_flag, available_credit_dollars | credit_line_offer_flag   available_credit_dollars (no edge) | credit_line_offer_flag   available_credit_dollars (no edge) | credit_line_offer_flag->available_credit_dollars | credit_line_offer_flag->available_credit_dollars | credit_line_offer_flag->available_credit_dollars | no edge | (credit_line_offer_flag, available_credit_dollars)=A |
| credit_line_offer_flag, cash_on_hand_dollars | credit_line_offer_flag o-o cash_on_hand_dollars | credit_line_offer_flag   cash_on_hand_dollars (no edge) | credit_line_offer_flag   cash_on_hand_dollars (no edge) | credit_line_offer_flag   cash_on_hand_dollars (no edge) | credit_line_offer_flag   cash_on_hand_dollars (no edge) | cash_on_hand_dollars -> credit_line_offer_flag | (credit_line_offer_flag, cash_on_hand_dollars)=C |
| interest_rate_apr, cash_on_hand_dollars | interest_rate_apr   cash_on_hand_dollars (no edge) | interest_rate_apr   cash_on_hand_dollars (no edge) | interest_rate_apr->cash_on_hand_dollars | interest_rate_apr->cash_on_hand_dollars | interest_rate_apr->cash_on_hand_dollars | no edge | (interest_rate_apr, cash_on_hand_dollars)=A |
| reorder_point_units, tentative_order_quantity_units | reorder_point_units   tentative_order_quantity_units (no edge) | reorder_point_units   tentative_order_quantity_units (no edge) | reorder_point_units->tentative_order_quantity_units | reorder_point_units->tentative_order_quantity_units | reorder_point_units->tentative_order_quantity_units | no edge | (reorder_point_units, tentative_order_quantity_units)=A |
| reorder_point_units, chosen_service_level | reorder_point_units   chosen_service_level (no edge) | reorder_point_units   chosen_service_level (no edge) | reorder_point_units->chosen_service_level | reorder_point_units->chosen_service_level | reorder_point_units->chosen_service_level | no edge | (reorder_point_units, chosen_service_level)=A |
| tentative_order_quantity_units, chosen_service_level | tentative_order_quantity_units   chosen_service_level (no edge) | tentative_order_quantity_units   chosen_service_level (no edge) | tentative_order_quantity_units->chosen_service_level | tentative_order_quantity_units->chosen_service_level | tentative_order_quantity_units->chosen_service_level | chosen_service_level -> tentative_order_quantity_units | (tentative_order_quantity_units, chosen_service_level)=A |
| tentative_order_quantity_units, on_hand_units_at_open | tentative_order_quantity_units   on_hand_units_at_open (no edge) | tentative_order_quantity_units   on_hand_units_at_open (no edge) | tentative_order_quantity_units->on_hand_units_at_open | tentative_order_quantity_units->on_hand_units_at_open | tentative_order_quantity_units->on_hand_units_at_open | no edge | (tentative_order_quantity_units, on_hand_units_at_open)=A |
| cash_on_hand_dollars, early_payment_choice | cash_on_hand_dollars   early_payment_choice (no edge) | cash_on_hand_dollars   early_payment_choice (no edge) | cash_on_hand_dollars->early_payment_choice | cash_on_hand_dollars->early_payment_choice | cash_on_hand_dollars->early_payment_choice | no edge | (cash_on_hand_dollars, early_payment_choice)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
