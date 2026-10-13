Tickets: REP-11, BND-12

# REP-11 (data-only part): Sachs BNSL-ensemble F1 from Kitson & Constantinou (arXiv 2608.27472v1)

Scope: only the statistical structure-learning (BNSL) numbers. No LLM or API calls were made. The LLM and fused numbers are out of scope.
Producer: `analysis/rep11_sachs_data.py`. Results: `analysis/results/rep11/rep11_sachs_data.json` and `CONTRACT.json`.
`check_scores.py` passes: all five results directories are "ok" and none is nonconforming.

## Verdict

| quantity (Sachs) | reported | ours | diff | rule: within 0.05 |
|---|---|---|---|---|
| Mean Indiv. F1 (Table 9) | 0.293 | 0.259 | -0.034 | **reproduced** |
| Ensemble F1, primary reading B (Table 9; Table 5 "BNSL") | 0.606 | 0.647 | +0.041 | **reproduced** |
| Ensemble F1, reading A (mean over 3 per-set ensembles) | 0.606 | 0.627 | +0.022 | reproduced (sensitivity) |
| Ensemble F1, reading C (one set per algorithm) | 0.606 | 0.647 | +0.041 | reproduced (sensitivity) |

The verdict rule was fixed in the script before any run: within 0.05 of the reported value counts as reproduced; otherwise not reproduced, with the substitutions as the likely reason.
Both numbers fall inside that band. **This is a conditional reproduction, for the reason below.**

**Caveat: what drives the number.** The Sachs DAG has no v-structures, so its CPDAG has 0 compelled arcs and 17 undirected edges.
Under bnlearn F1 semantics an undirected edge never matches a true arc. So any algorithm that returns a correct CPDAG scores directed F1 = 0.
Our FGES stand-in did exactly that on all 15 datasets: skeleton F1 1.0, directed F1 0.0.
In the merged PDG, FGES and most PC runs contribute only undirected mass, and that mass splits evenly between the two directions. So the ensemble DAG takes almost all of its orientations from Tabu-Stable, which is the only DAG learner.
- Our ensemble DAG has a perfect skeleton (17 of 17 adjacencies) and 11 of 17 orientations correct, which gives F1 = 0.647.
- The paper's 0.606 corresponds to about 10.3 correct orientations on a perfect skeleton.

As a result, the match depends mostly on how our Tabu-Stable stand-in orients edges inside the equivalence class. It is not an independent check of the fusion machinery.
The single-algorithm ensembles show the same thing: Tabu alone gives 0.647, PC alone 0.412 and FGES alone 0.118. The FGES-only 0.118 is 2 of 17 arcs, because alphabetical tie-breaking happens to orient only PKA->Raf and PKC->Raf correctly.

## Protocol as read (arXiv 2608.27472v1, HTML version)

- Data (Sec. 2.3, 2.4): synthetic observational samples drawn from the bnlearn reference BN. "We primarily use a sample size of 10,000 rows" (Sec. 2.3).
- Algorithms (Sec. 2.3):
  - PC-Stable, bnlearn implementation, which "learns a CPDAG".
  - Tabu-Stable (Kitson & Constantinou 2025), which "learns a DAG".
  - FGES, Tetrad implementation, "returning a CPDAG".
  - No hyperparameters (alpha, test, score, tabu length) are stated.
- Ensemble (Sec. 2.3): "three different sets of five datasets for each BNSL algorithm". The sets are then merged: "in turn merge these individual PDGs to create one final ensemble BNSL PDG".
- Algorithm 1, MERGEGRAPHS (Sec. 2.1): a weighted average of per-pair state indicators (forward, backward, undirected, none). Weights are equal (1/n) by default.
- Algorithm 2, ToDAGGREEDY (Sec. 2.1), with tau = 0.3:
  - Existence is p_fwd + p_bwd + p_und.
  - Direction is decided by comparing p_fwd + p_und/2 with p_bwd + p_und/2.
  - Arcs are added greedily by that score, skipping any arc that would close a cycle.
- F1 (Sec. 2.4): "we follow the semantics for computing F1 that is used in bnlearn". No formula is given.
- Table 9 defines "Mean Indiv." as "mean F1 achieved averaging across all the individual BNSL runs". It defines "Ensemble" as the F1 of the Algorithm 2 DAG built from the Algorithm 1 PDG.
- Reported Sachs values: Mean Indiv. 0.293, Ensemble 0.606, gain +0.313 (Table 9). BNSL 0.606 (Table 5).

### Ambiguities and the choices made (fixed before running)

1. **Ensemble construction.** All three readings were run. Reading B is primary because it is the most literal reading of "merge these individual PDGs to create one final ... PDG".
   - **B (primary).** For each (algorithm, set) pair, the 5 graphs are merged into one PDG, giving 9 PDGs. These are merged with equal weights into one PDG, and one DAG is extracted.
   - **A.** For each set, the 3 per-algorithm PDGs are merged and one DAG is extracted. The result is the mean F1 over the 3 sets. This reading follows Table 9's word "mean".
   - **C.** Algorithm i uses only set i, giving 3 PDGs in total.
   - All three readings fall within 0.05 of 0.606.
2. **Threshold test.** The text says existence must exceed tau, while the pseudocode says skip when existence is below tau. These differ only when existence equals tau exactly. No pair had existence equal to 0.3 (`pairs_with_p_exist_equal_tau = 0`), so this ambiguity has no effect here.
3. **Tie direction.** The text says lexicographic; the pseudocode says forward. These agree, because forward means the alphabetically first node of the canonical pair. Reading B needed 0 tie-breaks.
4. **F1 semantics.** We ported `pdag_compare` from the authors' own package, `causaliq-analysis` 0.4.0 on PyPI. Its evaluate action applies this function to the learnt graph against the reference. The rules are:
   - TP is a matched arc with the same orientation, or a matched undirected edge.
   - A reversed arc, or an arc/edge type mismatch, counts as 1 FP and 1 FN.
   - An extra edge counts as FP; a missing edge counts as FN.
   - This is the bnlearn `compare()` rule, under which direction matters.
   - The bnlearn manual page itself only says tp is "arcs in current also present in target" and does not spell out undirected edges.
   - Skeleton F1 is reported alongside but is not used for the verdict. Mean skeleton F1 of the individual runs is 0.999; the ensemble skeleton F1 is 1.0.
5. **Mean Indiv. scope.** The mean is over all 45 individual graphs (3 algorithms x 15 datasets), each scored as learnt.
   - Alternative: turning each single graph into a DAG with ToDAGGREEDY first gives 0.323. That is diff +0.030 and also inside the band. It is not used for the verdict.

**Authors'-code cross-check.** We ran the same merge, ToDAGGREEDY and F1 steps with the authors' own `causaliq-core` 0.7.0 and `causaliq-analysis` 0.4.0 PyPI wheels (`merge.merge_graphs`, `PDG.to_dag_greedy`, `metrics.pdag_compare`).
The results are identical: all 45 individual F1 values match, and the ensemble arcs and F1 match for readings B and C (`authors_code_crosscheck` in the JSON).
These packages do not contain the BNSL algorithms themselves.

## Substitutions (R and Java tools replaced by Python)

| paper | here | known differences |
|---|---|---|
| bnlearn Sachs BIF (bnlearn.com) | pgmpy 1.1.2 bundled `utils/example_models/sachs.bif.gz` | bnlearn.com is blocked by the proxy (HTTP 403). The sha256 of the .gz is `ed1830fbde101ed50cce3c7a3c8cbf1d2f5225531cf35ff09fb3cec0af101bce`, whose prefix matches the project's `ed1830fb`. It has 11 nodes and 17 arcs. |
| Sampling (the authors' code, unspecified) | pgmpy `DiscreteBayesianNetwork.simulate`, seeds 11000 to 11014, 10,000 rows each; set = k // 5 | Different random streams. The sha256 of each dataset's integer codes is in the JSON. |
| PC-Stable (bnlearn `pc.stable`, default test "mi") | vendored causal-learn `pc(stable=True, indep_test="gsq", alpha=0.05, uc_rule=0, uc_priority=2)` | G-test degrees of freedom and v-structure conflict handling differ from bnlearn. Because the truth has no v-structures, every PC orientation is spurious. Our PC returned a fully undirected CPDAG on 9 of 15 datasets and oriented 8 or 14 arcs on the other 6, for a mean F1 of 0.152. |
| Tabu-Stable (the authors' Python code, causal-iq/discovery) | `tabu_stable()` in the producer, implementing arXiv 2504.01740 Algorithms 1 and 2 as read | Our version is a re-implementation; see the details below this table. Mean F1 0.624 (sd 0.030), with a perfect skeleton every time and 10 or 11 of 17 orientations correct. |
| FGES (Tetrad) | vendored causal-learn `ges()`, with a BDeu local score written here and swapped in at runtime (no file edited) | Tetrad's FGES speed-ups and its `faithfulnessAssumed` default are not reproduced. The stock causal-learn `local_score_BDeu` has two problems: it uses n-1 rows in the structure prior, and it raises `KeyError` under pandas 3 for any non-empty parent set. Our port matches its data term exactly for the empty parent set. A BIC variant (sensitivity) returned the same CPDAGs and the same ensemble F1. |

**Tabu-Stable re-implementation details:**
- BIC score (bnlearn form), starting from the empty DAG, with add, delete and reverse moves.
- Tabu list of the last 10 DAGs; the search stops after 10 changes without improving the best score.
- These are bnlearn's tabu defaults, because the Tabu-Stable paper gives no values.
- The stable order uses the key (no-parent score, mean single-parent score, value-count text). A decreasing order and its reverse are each run through HC, and the order from the better HC result is kept, taking that result's topological order.
- When an arc addition ties with the same arc in the opposite orientation, the orientation consistent with the stable order is taken.

## Numbers

- Per-algorithm mean directed F1 over the 15 datasets:
  - FGES stand-in: 0.000 (skeleton 1.000)
  - Tabu-Stable stand-in: 0.624 (skeleton 1.000)
  - PC-Stable stand-in: 0.152 (skeleton 0.998)
- Mean Indiv.: 0.259 (reported 0.293).
- Ensemble B: F1 0.647. The DAG has 17 arcs: 11 matched, 6 reversed, 0 extra, 0 missing.
  - In ToDAGGREEDY, 17 candidates were included, 1 pair fell below tau (a PC extra edge), and 0 arcs were skipped for cycles.
- Ensemble A: per-set F1 0.647, 0.588 and 0.647, mean 0.627.
- Ensemble C: 0.647.
- Gain of ensemble over Mean Indiv.: +0.388 here, against +0.313 reported. This gain is not a separate claim; it follows from the two numbers above.
- The full PDG probabilities, the ensemble arcs and every individual graph are in the JSON.

## What could not be matched, and why

- **The exact tools.** No R or Java was available, so PC-Stable, Tabu-Stable and FGES are replaced by the stand-ins above. The Tabu-Stable code (github causal-iq/discovery) could not be fetched, because GitHub access is not enabled for this session.
- **Hyperparameters.** The paper states none, so the bnlearn and Tetrad defaults as we understand them were used: alpha 0.05, BIC for Tabu, BDeu with ESS 1 for FGES.
- **Random draws.** The paper's random draws, and how its five datasets per set were generated, are not given.
- **Fragility of the match.** Because the Sachs CPDAG is fully undirected, the reported ensemble F1 depends on the orientation behaviour of one algorithm (Tabu-Stable) and on alphabetical tie-breaks. The close match is therefore fragile to the Tabu stand-in. Getting 1 more or 1 fewer orientation right moves F1 by 0.059.

## Versions

Python 3.13.16; pgmpy 1.1.2, numpy 2.5.4, scipy 1.18.1 and pandas 3.0.6, installed in a scratch `--target` directory and put on PYTHONPATH.
causal-learn is the copy vendored at `../Causal-Copilot/externals/causal-learn` (read only; run with PYTHONDONTWRITEBYTECODE=1).
The cross-check used causaliq-core 0.7.0 and causaliq-analysis 0.4.0 (PyPI wheels).
Runtime is 78 s.
