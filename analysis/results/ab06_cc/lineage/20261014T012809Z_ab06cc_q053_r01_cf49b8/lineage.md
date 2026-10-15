# Edge lineage: 20261014T012809Z_ab06cc_q053_r01_cf49b8

Dataset `/research/datasets/suite_q1s2/q053/q053.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 2}. 20 variables, 190 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 18 | 0.83 | 0.39 | 0.54 | 2 | 0 | 13 | 39 |
| S1 after bootstrap edits | 4 | 1.00 | 0.11 | 0.19 | 2 | 0 | 2 | 36 |
| S2 after LLM review | 38 | 0.13 | 0.13 | 0.13 | 3 | 2 | 0 | 68 |
| S3 after KCI pruning | 38 | 0.13 | 0.13 | 0.13 | 3 | 2 | 0 | 68 |
| S4 final (after cycle step) | 38 | 0.13 | 0.13 | 0.13 | 3 | 2 | 0 | 68 |

Scored against: reference graph s2_05_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 14. Of the deleted, 7 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 20 calls, 190 distinct pairs answered out of 190, plus 20 self-pairs. Letters: {"A": 37, "C": 147, "D": 6}.
- LLM effect: added 36 (of which 30 where the resamples showed no edge at frequency >= 0.9), removed 2, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 38 edges; set by {"llm": 36, "algorithm (unchanged)": 2}; 2 identical to the algorithm's output; 33 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| cycle_gross_margin_dollars->retail_list_price_dollars | llm | yes | 0.60 |
| cycle_gross_margin_dollars->demand_forecast_units_per_day | llm | no | 1.00 |
| cycle_gross_margin_dollars->markdown_policy_schedule | llm | no | 1.00 |
| lead_time_days->stockout_days_count | llm | no | 1.00 |
| lead_time_days->reorder_point_units | llm | no | 1.00 |
| lead_time_days->on_hand_units_at_open | llm | no | 1.00 |
| retail_list_price_dollars->demand_forecast_units_per_day | llm | no | 0.65 |
| retail_list_price_dollars->markdown_policy_schedule | llm | no | 1.00 |
| retail_list_price_dollars->tentative_order_quantity_units | llm | yes | 0.00 |
| retail_list_price_dollars->on_hand_units_at_open | llm | no | 0.95 |
| demand_forecast_units_per_day->stockout_days_count | llm | no | 1.00 |
| demand_forecast_units_per_day->reorder_point_units | llm | no | 1.00 |
| demand_forecast_units_per_day->tentative_order_quantity_units | llm | no | 1.00 |
| demand_forecast_units_per_day->on_hand_units_at_open | llm | no | 1.00 |
| shelf_capacity_units->reorder_point_units | llm | no | 1.00 |
| shelf_capacity_units->tentative_order_quantity_units | llm | no | 1.00 |
| shelf_capacity_units->unit_wholesale_price | algorithm (unchanged) | yes | 0.10 |
| shelf_capacity_units->on_hand_units_at_open | llm | no | 1.00 |
| stockout_days_count->reorder_point_units | llm | no | 1.00 |
| stockout_days_count->tentative_order_quantity_units | llm | no | 1.00 |
| stockout_days_count->on_hand_units_at_open | llm | no | 0.90 |
| credit_draw_amount_dollars->interest_expense_dollars | llm | no | 1.00 |
| credit_draw_amount_dollars->credit_line_offer_flag | llm | no | 0.95 |
| credit_draw_amount_dollars->available_credit_dollars | llm | no | 0.60 |
| credit_draw_amount_dollars->cash_on_hand_dollars | llm | no | 0.70 |
| markdown_policy_schedule->credit_line_offer_flag | algorithm (unchanged) | yes | 0.55 |
| interest_expense_dollars->credit_line_offer_flag | llm | no | 0.90 |
| interest_expense_dollars->interest_rate_apr | llm | no | 1.00 |
| interest_expense_dollars->available_credit_dollars | llm | no | 1.00 |
| interest_expense_dollars->cash_on_hand_dollars | llm | no | 1.00 |
| credit_line_offer_flag->available_credit_dollars | llm | no | 1.00 |
| credit_line_offer_flag->cash_on_hand_dollars | llm | yes | 0.05 |
| interest_rate_apr->available_credit_dollars | llm | no | 1.00 |
| interest_rate_apr->cash_on_hand_dollars | llm | no | 1.00 |
| reorder_point_units->tentative_order_quantity_units | llm | no | 0.95 |
| reorder_point_units->on_hand_units_at_open | llm | no | 1.00 |
| tentative_order_quantity_units->on_hand_units_at_open | llm | no | 0.95 |
| available_credit_dollars->cash_on_hand_dollars | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| cycle_gross_margin_dollars, lead_time_days | cycle_gross_margin_dollars <-> lead_time_days | cycle_gross_margin_dollars   lead_time_days (no edge) | cycle_gross_margin_dollars   lead_time_days (no edge) | cycle_gross_margin_dollars   lead_time_days (no edge) | cycle_gross_margin_dollars   lead_time_days (no edge) | cycle_gross_margin_dollars -> lead_time_days | (cycle_gross_margin_dollars, lead_time_days)=C |
| cycle_gross_margin_dollars, retail_list_price_dollars | cycle_gross_margin_dollars <-> retail_list_price_dollars | cycle_gross_margin_dollars   retail_list_price_dollars (no edge) | cycle_gross_margin_dollars->retail_list_price_dollars | cycle_gross_margin_dollars->retail_list_price_dollars | cycle_gross_margin_dollars->retail_list_price_dollars | no edge | (cycle_gross_margin_dollars, retail_list_price_dollars)=A |
| cycle_gross_margin_dollars, demand_forecast_units_per_day | cycle_gross_margin_dollars   demand_forecast_units_per_day (no edge) | cycle_gross_margin_dollars   demand_forecast_units_per_day (no edge) | cycle_gross_margin_dollars->demand_forecast_units_per_day | cycle_gross_margin_dollars->demand_forecast_units_per_day | cycle_gross_margin_dollars->demand_forecast_units_per_day | no edge | (cycle_gross_margin_dollars, demand_forecast_units_per_day)=A |
| cycle_gross_margin_dollars, markdown_policy_schedule | cycle_gross_margin_dollars   markdown_policy_schedule (no edge) | cycle_gross_margin_dollars   markdown_policy_schedule (no edge) | cycle_gross_margin_dollars->markdown_policy_schedule | cycle_gross_margin_dollars->markdown_policy_schedule | cycle_gross_margin_dollars->markdown_policy_schedule | no edge | (cycle_gross_margin_dollars, markdown_policy_schedule)=A |
| lead_time_days, stockout_days_count | lead_time_days   stockout_days_count (no edge) | lead_time_days   stockout_days_count (no edge) | lead_time_days->stockout_days_count | lead_time_days->stockout_days_count | lead_time_days->stockout_days_count | no edge | (lead_time_days, stockout_days_count)=A |
| lead_time_days, reorder_point_units | lead_time_days   reorder_point_units (no edge) | lead_time_days   reorder_point_units (no edge) | lead_time_days->reorder_point_units | lead_time_days->reorder_point_units | lead_time_days->reorder_point_units | no edge | (lead_time_days, reorder_point_units)=A |
| lead_time_days, unit_wholesale_price | lead_time_days <-> unit_wholesale_price | lead_time_days <-> unit_wholesale_price | lead_time_days   unit_wholesale_price (no edge) | lead_time_days   unit_wholesale_price (no edge) | lead_time_days   unit_wholesale_price (no edge) | unit_wholesale_price -> lead_time_days | (lead_time_days, unit_wholesale_price)=C |
| lead_time_days, on_hand_units_at_open | lead_time_days   on_hand_units_at_open (no edge) | lead_time_days   on_hand_units_at_open (no edge) | lead_time_days->on_hand_units_at_open | lead_time_days->on_hand_units_at_open | lead_time_days->on_hand_units_at_open | no edge | (lead_time_days, on_hand_units_at_open)=A |
| retail_list_price_dollars, demand_forecast_units_per_day | retail_list_price_dollars   demand_forecast_units_per_day (no edge) | retail_list_price_dollars   demand_forecast_units_per_day (no edge) | retail_list_price_dollars->demand_forecast_units_per_day | retail_list_price_dollars->demand_forecast_units_per_day | retail_list_price_dollars->demand_forecast_units_per_day | retail_list_price_dollars -> demand_forecast_units_per_day | (retail_list_price_dollars, demand_forecast_units_per_day)=A |
| retail_list_price_dollars, waste_units_disposed | retail_list_price_dollars <-> waste_units_disposed | retail_list_price_dollars   waste_units_disposed (no edge) | retail_list_price_dollars   waste_units_disposed (no edge) | retail_list_price_dollars   waste_units_disposed (no edge) | retail_list_price_dollars   waste_units_disposed (no edge) | retail_list_price_dollars -> waste_units_disposed | (retail_list_price_dollars, waste_units_disposed)=C |
| retail_list_price_dollars, markdown_policy_schedule | retail_list_price_dollars   markdown_policy_schedule (no edge) | retail_list_price_dollars   markdown_policy_schedule (no edge) | retail_list_price_dollars->markdown_policy_schedule | retail_list_price_dollars->markdown_policy_schedule | retail_list_price_dollars->markdown_policy_schedule | no edge | (retail_list_price_dollars, markdown_policy_schedule)=A |
| retail_list_price_dollars, tentative_order_quantity_units | tentative_order_quantity_units o-> retail_list_price_dollars | retail_list_price_dollars   tentative_order_quantity_units (no edge) | retail_list_price_dollars->tentative_order_quantity_units | retail_list_price_dollars->tentative_order_quantity_units | retail_list_price_dollars->tentative_order_quantity_units | tentative_order_quantity_units -> retail_list_price_dollars | (retail_list_price_dollars, tentative_order_quantity_units)=A |
| retail_list_price_dollars, on_hand_units_at_open | retail_list_price_dollars   on_hand_units_at_open (no edge) | retail_list_price_dollars   on_hand_units_at_open (no edge) | retail_list_price_dollars->on_hand_units_at_open | retail_list_price_dollars->on_hand_units_at_open | retail_list_price_dollars->on_hand_units_at_open | no edge | (retail_list_price_dollars, on_hand_units_at_open)=A |
| demand_forecast_units_per_day, stockout_days_count | demand_forecast_units_per_day   stockout_days_count (no edge) | demand_forecast_units_per_day   stockout_days_count (no edge) | demand_forecast_units_per_day->stockout_days_count | demand_forecast_units_per_day->stockout_days_count | demand_forecast_units_per_day->stockout_days_count | no edge | (demand_forecast_units_per_day, stockout_days_count)=A |
| demand_forecast_units_per_day, credit_draw_amount_dollars | credit_draw_amount_dollars o-> demand_forecast_units_per_day | demand_forecast_units_per_day   credit_draw_amount_dollars (no edge) | demand_forecast_units_per_day   credit_draw_amount_dollars (no edge) | demand_forecast_units_per_day   credit_draw_amount_dollars (no edge) | demand_forecast_units_per_day   credit_draw_amount_dollars (no edge) | credit_draw_amount_dollars -> demand_forecast_units_per_day | (demand_forecast_units_per_day, credit_draw_amount_dollars)=C |
| demand_forecast_units_per_day, reorder_point_units | demand_forecast_units_per_day   reorder_point_units (no edge) | demand_forecast_units_per_day   reorder_point_units (no edge) | demand_forecast_units_per_day->reorder_point_units | demand_forecast_units_per_day->reorder_point_units | demand_forecast_units_per_day->reorder_point_units | no edge | (demand_forecast_units_per_day, reorder_point_units)=A |
| demand_forecast_units_per_day, tentative_order_quantity_units | demand_forecast_units_per_day   tentative_order_quantity_units (no edge) | demand_forecast_units_per_day   tentative_order_quantity_units (no edge) | demand_forecast_units_per_day->tentative_order_quantity_units | demand_forecast_units_per_day->tentative_order_quantity_units | demand_forecast_units_per_day->tentative_order_quantity_units | no edge | (demand_forecast_units_per_day, tentative_order_quantity_units)=A |
| demand_forecast_units_per_day, unit_wholesale_price | demand_forecast_units_per_day <-> unit_wholesale_price | demand_forecast_units_per_day   unit_wholesale_price (no edge) | demand_forecast_units_per_day   unit_wholesale_price (no edge) | demand_forecast_units_per_day   unit_wholesale_price (no edge) | demand_forecast_units_per_day   unit_wholesale_price (no edge) | unit_wholesale_price -> demand_forecast_units_per_day | (demand_forecast_units_per_day, unit_wholesale_price)=D |
| demand_forecast_units_per_day, on_hand_units_at_open | demand_forecast_units_per_day   on_hand_units_at_open (no edge) | demand_forecast_units_per_day   on_hand_units_at_open (no edge) | demand_forecast_units_per_day->on_hand_units_at_open | demand_forecast_units_per_day->on_hand_units_at_open | demand_forecast_units_per_day->on_hand_units_at_open | no edge | (demand_forecast_units_per_day, on_hand_units_at_open)=A |
| demand_forecast_units_per_day, early_payment_choice | early_payment_choice o-> demand_forecast_units_per_day | demand_forecast_units_per_day   early_payment_choice (no edge) | demand_forecast_units_per_day   early_payment_choice (no edge) | demand_forecast_units_per_day   early_payment_choice (no edge) | demand_forecast_units_per_day   early_payment_choice (no edge) | no edge | (demand_forecast_units_per_day, early_payment_choice)=C |
| waste_units_disposed, early_payment_choice | early_payment_choice o-> waste_units_disposed | early_payment_choice o-> waste_units_disposed | waste_units_disposed   early_payment_choice (no edge) | waste_units_disposed   early_payment_choice (no edge) | waste_units_disposed   early_payment_choice (no edge) | early_payment_choice -> waste_units_disposed | (waste_units_disposed, early_payment_choice)=C |
| shelf_capacity_units, interest_rate_apr | shelf_capacity_units o-o interest_rate_apr | shelf_capacity_units   interest_rate_apr (no edge) | shelf_capacity_units   interest_rate_apr (no edge) | shelf_capacity_units   interest_rate_apr (no edge) | shelf_capacity_units   interest_rate_apr (no edge) | shelf_capacity_units -> interest_rate_apr | (shelf_capacity_units, interest_rate_apr)=C |
| shelf_capacity_units, reorder_point_units | shelf_capacity_units   reorder_point_units (no edge) | shelf_capacity_units   reorder_point_units (no edge) | shelf_capacity_units->reorder_point_units | shelf_capacity_units->reorder_point_units | shelf_capacity_units->reorder_point_units | no edge | (shelf_capacity_units, reorder_point_units)=A |
| shelf_capacity_units, tentative_order_quantity_units | shelf_capacity_units   tentative_order_quantity_units (no edge) | shelf_capacity_units   tentative_order_quantity_units (no edge) | shelf_capacity_units->tentative_order_quantity_units | shelf_capacity_units->tentative_order_quantity_units | shelf_capacity_units->tentative_order_quantity_units | no edge | (shelf_capacity_units, tentative_order_quantity_units)=A |
| shelf_capacity_units, on_hand_units_at_open | shelf_capacity_units   on_hand_units_at_open (no edge) | shelf_capacity_units   on_hand_units_at_open (no edge) | shelf_capacity_units->on_hand_units_at_open | shelf_capacity_units->on_hand_units_at_open | shelf_capacity_units->on_hand_units_at_open | no edge | (shelf_capacity_units, on_hand_units_at_open)=A |
| stockout_days_count, reorder_point_units | stockout_days_count   reorder_point_units (no edge) | stockout_days_count   reorder_point_units (no edge) | stockout_days_count->reorder_point_units | stockout_days_count->reorder_point_units | stockout_days_count->reorder_point_units | no edge | (stockout_days_count, reorder_point_units)=A |
| stockout_days_count, tentative_order_quantity_units | stockout_days_count   tentative_order_quantity_units (no edge) | stockout_days_count   tentative_order_quantity_units (no edge) | stockout_days_count->tentative_order_quantity_units | stockout_days_count->tentative_order_quantity_units | stockout_days_count->tentative_order_quantity_units | no edge | (stockout_days_count, tentative_order_quantity_units)=A |
| stockout_days_count, on_hand_units_at_open | stockout_days_count   on_hand_units_at_open (no edge) | stockout_days_count   on_hand_units_at_open (no edge) | stockout_days_count->on_hand_units_at_open | stockout_days_count->on_hand_units_at_open | stockout_days_count->on_hand_units_at_open | no edge | (stockout_days_count, on_hand_units_at_open)=A |
| credit_draw_amount_dollars, interest_expense_dollars | credit_draw_amount_dollars   interest_expense_dollars (no edge) | credit_draw_amount_dollars   interest_expense_dollars (no edge) | credit_draw_amount_dollars->interest_expense_dollars | credit_draw_amount_dollars->interest_expense_dollars | credit_draw_amount_dollars->interest_expense_dollars | no edge | (credit_draw_amount_dollars, interest_expense_dollars)=A |
| credit_draw_amount_dollars, credit_line_offer_flag | credit_draw_amount_dollars   credit_line_offer_flag (no edge) | credit_draw_amount_dollars   credit_line_offer_flag (no edge) | credit_draw_amount_dollars->credit_line_offer_flag | credit_draw_amount_dollars->credit_line_offer_flag | credit_draw_amount_dollars->credit_line_offer_flag | no edge | (credit_draw_amount_dollars, credit_line_offer_flag)=A |
| credit_draw_amount_dollars, available_credit_dollars | credit_draw_amount_dollars   available_credit_dollars (no edge) | credit_draw_amount_dollars   available_credit_dollars (no edge) | credit_draw_amount_dollars->available_credit_dollars | credit_draw_amount_dollars->available_credit_dollars | credit_draw_amount_dollars->available_credit_dollars | no edge | (credit_draw_amount_dollars, available_credit_dollars)=A |
| credit_draw_amount_dollars, cash_on_hand_dollars | credit_draw_amount_dollars   cash_on_hand_dollars (no edge) | credit_draw_amount_dollars   cash_on_hand_dollars (no edge) | credit_draw_amount_dollars->cash_on_hand_dollars | credit_draw_amount_dollars->cash_on_hand_dollars | credit_draw_amount_dollars->cash_on_hand_dollars | no edge | (credit_draw_amount_dollars, cash_on_hand_dollars)=A |
| markdown_policy_schedule, interest_expense_dollars | interest_expense_dollars o-> markdown_policy_schedule | markdown_policy_schedule   interest_expense_dollars (no edge) | markdown_policy_schedule   interest_expense_dollars (no edge) | markdown_policy_schedule   interest_expense_dollars (no edge) | markdown_policy_schedule   interest_expense_dollars (no edge) | no edge | (markdown_policy_schedule, interest_expense_dollars)=C |
| markdown_policy_schedule, chosen_service_level | chosen_service_level o-> markdown_policy_schedule | markdown_policy_schedule   chosen_service_level (no edge) | markdown_policy_schedule   chosen_service_level (no edge) | markdown_policy_schedule   chosen_service_level (no edge) | markdown_policy_schedule   chosen_service_level (no edge) | chosen_service_level -> markdown_policy_schedule | (markdown_policy_schedule, chosen_service_level)=C |
| markdown_policy_schedule, on_hand_units_at_open | on_hand_units_at_open o-> markdown_policy_schedule | markdown_policy_schedule   on_hand_units_at_open (no edge) | markdown_policy_schedule   on_hand_units_at_open (no edge) | markdown_policy_schedule   on_hand_units_at_open (no edge) | markdown_policy_schedule   on_hand_units_at_open (no edge) | on_hand_units_at_open -> markdown_policy_schedule | (markdown_policy_schedule, on_hand_units_at_open)=C |
| interest_expense_dollars, credit_line_offer_flag | interest_expense_dollars   credit_line_offer_flag (no edge) | interest_expense_dollars   credit_line_offer_flag (no edge) | interest_expense_dollars->credit_line_offer_flag | interest_expense_dollars->credit_line_offer_flag | interest_expense_dollars->credit_line_offer_flag | no edge | (interest_expense_dollars, credit_line_offer_flag)=A |
| interest_expense_dollars, interest_rate_apr | interest_expense_dollars   interest_rate_apr (no edge) | interest_expense_dollars   interest_rate_apr (no edge) | interest_expense_dollars->interest_rate_apr | interest_expense_dollars->interest_rate_apr | interest_expense_dollars->interest_rate_apr | no edge | (interest_expense_dollars, interest_rate_apr)=A |
| interest_expense_dollars, available_credit_dollars | interest_expense_dollars   available_credit_dollars (no edge) | interest_expense_dollars   available_credit_dollars (no edge) | interest_expense_dollars->available_credit_dollars | interest_expense_dollars->available_credit_dollars | interest_expense_dollars->available_credit_dollars | no edge | (interest_expense_dollars, available_credit_dollars)=A |
| interest_expense_dollars, cash_on_hand_dollars | interest_expense_dollars   cash_on_hand_dollars (no edge) | interest_expense_dollars   cash_on_hand_dollars (no edge) | interest_expense_dollars->cash_on_hand_dollars | interest_expense_dollars->cash_on_hand_dollars | interest_expense_dollars->cash_on_hand_dollars | no edge | (interest_expense_dollars, cash_on_hand_dollars)=A |
| interest_expense_dollars, chosen_service_level | interest_expense_dollars ~~~ chosen_service_level | interest_expense_dollars   chosen_service_level (no edge) | interest_expense_dollars   chosen_service_level (no edge) | interest_expense_dollars   chosen_service_level (no edge) | interest_expense_dollars   chosen_service_level (no edge) | interest_expense_dollars -> chosen_service_level | (interest_expense_dollars, chosen_service_level)=C |
| credit_line_offer_flag, available_credit_dollars | credit_line_offer_flag   available_credit_dollars (no edge) | credit_line_offer_flag   available_credit_dollars (no edge) | credit_line_offer_flag->available_credit_dollars | credit_line_offer_flag->available_credit_dollars | credit_line_offer_flag->available_credit_dollars | no edge | (credit_line_offer_flag, available_credit_dollars)=A |
| credit_line_offer_flag, cash_on_hand_dollars | cash_on_hand_dollars o-> credit_line_offer_flag | credit_line_offer_flag   cash_on_hand_dollars (no edge) | credit_line_offer_flag->cash_on_hand_dollars | credit_line_offer_flag->cash_on_hand_dollars | credit_line_offer_flag->cash_on_hand_dollars | cash_on_hand_dollars -> credit_line_offer_flag | (credit_line_offer_flag, cash_on_hand_dollars)=A |
| interest_rate_apr, available_credit_dollars | interest_rate_apr   available_credit_dollars (no edge) | interest_rate_apr   available_credit_dollars (no edge) | interest_rate_apr->available_credit_dollars | interest_rate_apr->available_credit_dollars | interest_rate_apr->available_credit_dollars | no edge | (interest_rate_apr, available_credit_dollars)=A |
| interest_rate_apr, cash_on_hand_dollars | interest_rate_apr   cash_on_hand_dollars (no edge) | interest_rate_apr   cash_on_hand_dollars (no edge) | interest_rate_apr->cash_on_hand_dollars | interest_rate_apr->cash_on_hand_dollars | interest_rate_apr->cash_on_hand_dollars | no edge | (interest_rate_apr, cash_on_hand_dollars)=A |
| reorder_point_units, tentative_order_quantity_units | reorder_point_units   tentative_order_quantity_units (no edge) | reorder_point_units   tentative_order_quantity_units (no edge) | reorder_point_units->tentative_order_quantity_units | reorder_point_units->tentative_order_quantity_units | reorder_point_units->tentative_order_quantity_units | no edge | (reorder_point_units, tentative_order_quantity_units)=A |
| reorder_point_units, on_hand_units_at_open | reorder_point_units   on_hand_units_at_open (no edge) | reorder_point_units   on_hand_units_at_open (no edge) | reorder_point_units->on_hand_units_at_open | reorder_point_units->on_hand_units_at_open | reorder_point_units->on_hand_units_at_open | no edge | (reorder_point_units, on_hand_units_at_open)=A |
| tentative_order_quantity_units, on_hand_units_at_open | tentative_order_quantity_units   on_hand_units_at_open (no edge) | tentative_order_quantity_units   on_hand_units_at_open (no edge) | tentative_order_quantity_units->on_hand_units_at_open | tentative_order_quantity_units->on_hand_units_at_open | tentative_order_quantity_units->on_hand_units_at_open | no edge | (tentative_order_quantity_units, on_hand_units_at_open)=A |
| unit_wholesale_price, early_payment_choice | early_payment_choice o-> unit_wholesale_price | unit_wholesale_price   early_payment_choice (no edge) | unit_wholesale_price   early_payment_choice (no edge) | unit_wholesale_price   early_payment_choice (no edge) | unit_wholesale_price   early_payment_choice (no edge) | early_payment_choice -> unit_wholesale_price | (unit_wholesale_price, early_payment_choice)=C |
| available_credit_dollars, cash_on_hand_dollars | available_credit_dollars   cash_on_hand_dollars (no edge) | available_credit_dollars   cash_on_hand_dollars (no edge) | available_credit_dollars->cash_on_hand_dollars | available_credit_dollars->cash_on_hand_dollars | available_credit_dollars->cash_on_hand_dollars | no edge | (available_credit_dollars, cash_on_hand_dollars)=A |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
