# Edge lineage: 20261006T145848Z_p4b_d03_r04_a54ced

Dataset `/research/datasets/d03/d03.csv`, algorithm **FCI** {"alpha": 0.05, "indep_test": "rcit", "depth": 4}. 11 variables, 55 pairs. 20 bootstrap resamples.

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
| S1 after bootstrap edits | 0 | n/a | 0.00 | 0.00 | 0 | 0 | 0 | 19 |
| S2 after LLM review | 8 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 27 |
| S3 after KCI pruning | 7 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 26 |
| S4 final (after cycle step) | 7 | 0.00 | 0.00 | 0.00 | 0 | 0 | 0 | 26 |

Scored against: reference graph reference_by_data.npy (not loaded by the pipeline).

## What each step did

- Bootstrap step: added 0, deleted 10. Of the deleted, 8 were existing edges whose most frequent status across resamples was a non-directed edge (frequency >= 0.5).
- LLM review: 11 calls, 55 distinct pairs answered out of 55, plus 11 self-pairs. Letters: {"A": 6, "B": 2, "C": 30, "D": 17}.
- LLM effect: added 8 (of which 7 where the resamples showed no edge at frequency >= 0.9), removed 0, re-oriented 0.
- KCI step removed 1. Cycle step changed 0.
- Final graph: 7 edges; set by {"llm": 7}; 0 identical to the algorithm's output; 7 between pairs the algorithm did not connect.

## Final edges

| Edge | Set by | Adjacent in algorithm output | Resample frequency of 'no edge' |
|---|---|---|---|
| Raf->Mek | llm | no | 0.95 |
| Mek->Erk | llm | no | 1.00 |
| Plcg->PIP2 | llm | no | 1.00 |
| PIP2->PKC | llm | no | 1.00 |
| Raf->Erk | llm | no | 0.90 |
| P38->Jnk | llm | no | 1.00 |
| PIP3->Akt | llm | no | 1.00 |

## Pairs that changed

| Pair | S0 | S1 | S2 | S3 | S4 | Truth/reference | LLM answers |
|---|---|---|---|---|---|---|---|
| Mek, Plcg | Mek o-o Plcg | Mek   Plcg (no edge) | Mek   Plcg (no edge) | Mek   Plcg (no edge) | Mek   Plcg (no edge) | Mek -> Plcg | (Mek, Plcg)=C |
| Mek, Raf | Mek   Raf (no edge) | Mek   Raf (no edge) | Raf->Mek | Raf->Mek | Raf->Mek | no edge | (Mek, Raf)=B |
| Mek, Erk | Mek   Erk (no edge) | Mek   Erk (no edge) | Mek->Erk | Mek->Erk | Mek->Erk | no edge | (Mek, Erk)=A |
| Plcg, PIP2 | Plcg   PIP2 (no edge) | Plcg   PIP2 (no edge) | Plcg->PIP2 | Plcg->PIP2 | Plcg->PIP2 | no edge | (Plcg, PIP2)=A |
| PIP2, Raf | PIP2 o-o Raf | PIP2   Raf (no edge) | PIP2   Raf (no edge) | PIP2   Raf (no edge) | PIP2   Raf (no edge) | PIP2 -> Raf | (PIP2, Raf)=D |
| PIP2, PKA | PIP2 o-o PKA | PIP2   PKA (no edge) | PIP2   PKA (no edge) | PIP2   PKA (no edge) | PIP2   PKA (no edge) | PKA -> PIP2 | (PIP2, PKA)=D |
| PIP2, PIP3 | PIP2   PIP3 (no edge) | PIP2   PIP3 (no edge) | PIP3->PIP2 | PIP2   PIP3 (no edge) | PIP2   PIP3 (no edge) | no edge | (PIP2, PIP3)=B |
| PIP2, PKC | PIP2   PKC (no edge) | PIP2   PKC (no edge) | PIP2->PKC | PIP2->PKC | PIP2->PKC | no edge | (PIP2, PKC)=A |
| Raf, PKA | Raf o-o PKA | Raf   PKA (no edge) | Raf   PKA (no edge) | Raf   PKA (no edge) | Raf   PKA (no edge) | PKA -> Raf | (Raf, PKA)=C |
| Raf, Erk | Raf   Erk (no edge) | Raf   Erk (no edge) | Raf->Erk | Raf->Erk | Raf->Erk | no edge | (Raf, Erk)=A |
| P38, PIP3 | P38 ~~~ PIP3 | P38   PIP3 (no edge) | P38   PIP3 (no edge) | P38   PIP3 (no edge) | P38   PIP3 (no edge) | P38 -> PIP3 | (P38, PIP3)=C |
| P38, Erk | P38 o-o Erk | P38   Erk (no edge) | P38   Erk (no edge) | P38   Erk (no edge) | P38   Erk (no edge) | Erk -> P38 | (P38, Erk)=C |
| P38, Jnk | P38   Jnk (no edge) | P38   Jnk (no edge) | P38->Jnk | P38->Jnk | P38->Jnk | no edge | (P38, Jnk)=A |
| PIP3, Erk | PIP3 o-o Erk | PIP3   Erk (no edge) | PIP3   Erk (no edge) | PIP3   Erk (no edge) | PIP3   Erk (no edge) | Erk -> PIP3 | (PIP3, Erk)=C |
| PIP3, Akt | PIP3   Akt (no edge) | PIP3   Akt (no edge) | PIP3->Akt | PIP3->Akt | PIP3->Akt | no edge | (PIP3, Akt)=A |
| Akt, Jnk | Akt o-o Jnk | Akt   Jnk (no edge) | Akt   Jnk (no edge) | Akt   Jnk (no edge) | Akt   Jnk (no edge) | Akt -> Jnk | (Akt, Jnk)=C |
| Akt, PKC | Akt o-o PKC | Akt   PKC (no edge) | Akt   PKC (no edge) | Akt   PKC (no edge) | Akt   PKC (no edge) | Akt -> PKC | (Akt, PKC)=C |
| Jnk, PKC | Jnk o-o PKC | Jnk   PKC (no edge) | Jnk   PKC (no edge) | Jnk   PKC (no edge) | Jnk   PKC (no edge) | no edge | (Jnk, PKC)=D |

Full per-pair evidence (resample frequencies by edge type, LLM explanations, KCI p-values) is in `lineage.json`.
