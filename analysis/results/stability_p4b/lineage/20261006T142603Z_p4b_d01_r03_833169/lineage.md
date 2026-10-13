# Edge lineage: 20261006T142603Z_p4b_d01_r03_833169

Dataset `/research/datasets/d01/d01.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 11 variables, 55 pairs. 20 bootstrap resamples.

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
| S0 algorithm output | 10 | 0.90 | 0.47 | 0.62 | 0 | 0 | 9 | 20 |
| S1 after bootstrap edits | 2 | 1.00 | 0.11 | 0.19 | 0 | 0 | 2 | 19 |
| S2 after LLM review | 6 | 0.83 | 0.26 | 0.40 | 4 | 1 | 0 | 17 |
| S3 after KCI pruning | 6 | 0.83 | 0.26 | 0.40 | 4 | 1 | 0 | 17 |
| S4 final (after cycle step) | 6 | 0.83 | 0.26 | 0.40 | 4 | 1 | 0 | 17 |

Scored against: reference graph reference_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 8. Of the deleted, 6 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 11 calls, 55 distinct pairs answered out of 55, plus 11 self-pairs. Letters: {"A": 6, "C": 44, "D": 5}.
- LLM effect: added 6 (of which 3 where the resamples showed no edge at frequency >= 0.9), removed 2, re-oriented 0.
- KCI step removed 0. Cycle step changed 0.
- Final graph: 6 edges; set by {"llm": 6}; 0 identical to the algorithm's output; 3 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Raf->Mek | llm | yes | 0.00 |
| Mek->Erk | llm | no | 0.95 |
| Plcg->PIP2 | llm | yes | 0.10 |
| PIP2->PIP3 | llm | yes | 0.00 |
| PIP3->Akt | llm | no | 1.00 |
| Erk->P38 | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Raf, Mek | Raf o-o Mek | Raf   Mek (no edge) | Raf->Mek | Raf->Mek | Raf->Mek | Raf -> Mek | (Raf, Mek)=A |
| Mek, Erk | Mek   Erk (no edge) | Mek   Erk (no edge) | Mek->Erk | Mek->Erk | Mek->Erk | Mek -> Erk | (Mek, Erk)=A |
| Plcg, PIP2 | Plcg o-o PIP2 | Plcg   PIP2 (no edge) | Plcg->PIP2 | Plcg->PIP2 | Plcg->PIP2 | Plcg -> PIP2 | (Plcg, PIP2)=A |
| Plcg, PIP3 | Plcg o-o PIP3 | Plcg   PIP3 (no edge) | Plcg   PIP3 (no edge) | Plcg   PIP3 (no edge) | Plcg   PIP3 (no edge) | PIP3 -> Plcg | (Plcg, PIP3)=C |
| PIP2, PIP3 | PIP2 o-o PIP3 | PIP2   PIP3 (no edge) | PIP2->PIP3 | PIP2->PIP3 | PIP2->PIP3 | PIP3 -> PIP2 | (PIP2, PIP3)=A |
| PIP3, Akt | PIP3   Akt (no edge) | PIP3   Akt (no edge) | PIP3->Akt | PIP3->Akt | PIP3->Akt | PIP3 -> Akt | (PIP3, Akt)=A |
| Erk, Akt | Erk ~~~ Akt | Erk ~~~ Akt | Erk   Akt (no edge) | Erk   Akt (no edge) | Erk   Akt (no edge) | Erk -> Akt | (Erk, Akt)=C |
| Erk, PKA | Erk o-o PKA | Erk o-o PKA | Erk   PKA (no edge) | Erk   PKA (no edge) | Erk   PKA (no edge) | PKA -> Erk | (Erk, PKA)=C |
| Erk, P38 | Erk   P38 (no edge) | Erk   P38 (no edge) | Erk->P38 | Erk->P38 | Erk->P38 | no edge | (Erk, P38)=A |
| Akt, PKA | Akt o-o PKA | Akt   PKA (no edge) | Akt   PKA (no edge) | Akt   PKA (no edge) | Akt   PKA (no edge) | PKA -> Akt | (Akt, PKA)=C |
| PKC, P38 | PKC o-o P38 | PKC   P38 (no edge) | PKC   P38 (no edge) | PKC   P38 (no edge) | PKC   P38 (no edge) | PKC -> P38 | (PKC, P38)=C |
| PKC, Jnk | PKC o-o Jnk | PKC   Jnk (no edge) | PKC   Jnk (no edge) | PKC   Jnk (no edge) | PKC   Jnk (no edge) | PKC -> Jnk | (PKC, Jnk)=C |
| P38, Jnk | P38 o-o Jnk | P38   Jnk (no edge) | P38   Jnk (no edge) | P38   Jnk (no edge) | P38   Jnk (no edge) | no edge | (P38, Jnk)=C |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
