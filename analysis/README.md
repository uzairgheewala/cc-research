# cc-research/analysis

Analysis code, results and reports for the Causal-Copilot study. Nothing here imports from or writes to the `Causal-Copilot` tree except to read it. Baseline: upstream commit `a31aa7c`.

## Reports (start here)

| File | Pass | Status |
|---|---|---|
| `reports/pass3_llm_dependency_map.md` | 3 | complete |
| `reports/pass4a_edge_lineage.md` | 4a | complete |
| `reports/pass4b_design.md` | 4b | design, arms, predictions and gates (written before the live runs) |
| `reports/pass4b_results.md` | 4b | complete: 25 of 28 live runs analysed, P1-P3 supported |
| `reports/bundle1_design.md` | bundle 1 | design, predictions and gates (written before the live runs). Correction: three, not four, of its datasets match a CausalArena real-data entry in size (Auto MPG differs) |
| `reports/bundle1_results.md` | bundle 1 | final: 45 of 54 live runs analysed (section 0): N2 supported; N1, N4, P3 inconclusive; all gates pass. Also: what the CausalArena snapshot contains, scorer calibration (F1 reproduces, SHD does not), and the column-order finding |
| `reports/bundle2_onward_design.md` | bundles 2-5 | earlier design; superseded as the organising plan by `program_v2.md`, parts still current |
| `reports/error_budget_and_order.md` | measurement | ceilings (0.957 / 0.971), error budget for PC, value of order knowledge, sortability; no LLM |
| `reports/program_v2.md` | plan | proposal: order provenance, the claim ledger, four tracks, predictions O1-O5, gates G1-G4; awaiting Uzair's decision |
| `reports/pass5_identifiability_vs_encoding.md` | 5 | complete for the wrappers that could be run |
| `reports/pass6_literature_map.md` | 6 | complete for the search that was possible; citing-works sweep unfinished |
| `reports/pass7_framing_test_and_candidates.md` | 7 | draft for the decision gate |

## Tools and their gates

| Script | Does | Gates |
|---|---|---|
| `cc_graph.py` | edge encoding, CPDAG of a DAG, scoring | CPDAG routine agrees with causal-learn's `dag2cpdag` on 300 random DAGs |
| `lineage.py RUN_DIR` | per-edge lineage of one recorded run | A-F (replay equals the run, every change has evidence) |
| `refinement_offline.py` | the refinement steps without the LLM, per dataset and algorithm | uses the bootstrap edit function validated by lineage gate B |
| `refinement_offline_report.py`, `refinement_offline_seeds.py` | tables from the offline cells | S1 (every compared combination complete for every seed) |
| `llm_inventory_scan.py`, `llm_inventory_build.py` | LLM call-site inventory | G1-G4 |
| `encoding_consumers.py` | micro-tests of how each step treats each edge code | executed against the repo's functions |
| `make_datasets.py` | derived datasets for pass 4b | D1-D5 |
| `stability.py` | run-to-run stability and the name-versus-data test, per arm and per dataset family | T1-T6, known-answer checks on stub runs, regression against the pass-4b verdicts |
| `make_suite.py` | bundle-1 dataset suite (real / neutral / swapped labels) | D1-D7 |
| `partial_stages.py` | scores through S3 for every run that reached refinement, including runs that crashed in the cycle step; cycle-step call log | Q1-Q3 |
| `causalarena_io.py` | reads CausalArena sample files; directed-edge scoring under a stated rule for undirected edges | graph convention checked against `graph.json` for all 50 public semantic scenarios |
| `causalarena_pc_calibration.py` | plain PC in the published configuration on the 250 public semantic files, against the published PC row | C1 (F1) passes, C2 (SHD) fails |
| `error_budget.py` | identifiable ceilings per scenario (observational and with the released targets) and the PC error budget | B1 (equivalence-class routine equals `cc_graph.cpdag_of` on 100 scenarios), B2 |
| `order_value.py` | score of PC re-oriented, and of regression on earlier tiers, under oracle tier knowledge of several granularities | none; deterministic |
| `causalarena_sortability.py` | R2-sortability and the R2-SortnRegress baseline | none; deterministic |
| `causalarena_order_baseline.py` | column-order check and the order-reading regression, as released and after a seeded column shuffle | none; deterministic, seed in file |

## Results

- `results/lineage/<run_id>/` lineage of each golden run.
- `results/offline/` offline experiment: two reports, summaries, and every cell as JSON.
- `results/llm_inventory/` inventory CSV (88 rows), summary, raw scan.
- `results/encoding/` micro-test tables.
- `results/stability_p4b/` stability report, JSON and per-run lineage for the 28 live repeats.
- `results/stability_b1/` bundle 1: stability report, JSON, per-run lineage for 40 runs, and `partial_stages.md/json` for all 48.
- `results/causalarena_calibration/` PC calibration rows and summary; order-baseline and sortability summaries.
- `results/error_budget/` ceilings per scenario, PC budget, value-of-order table.
- `literature/agent_reports/cluster6..9_*.md` four literature checks of 2026-10-07 (evidence fusion, active discovery, leakage and ceilings, query-level evaluation), unedited.
- `results/stability_selftest_stub/` stability tool self-test on stub runs (no meaning beyond showing the tool works).
- `literature/agent_reports/` the five search reports, unedited.

## Re-running

The scripts need the repo's Python environment (they call the repo's own functions). Inside the container started by `cc.ps1 shell`:

    python /research/analysis/lineage.py /research/runs/<run_id> --repo /app --out /research/analysis/results/lineage/<run_id>
    python /research/analysis/stability.py --runs-dir /research/runs --label p4b --mapping /research/datasets/MAPPING.json --repo /app --out /research/analysis/results/stability_p4b

Add `--reference /research/datasets/_reference/reference_by_data.npy` to `lineage.py` for sachs runs, which have no ground truth loaded by the pipeline.

## Known limits

- The cycle step of the pipeline has crashed every time it was entered (8 of 8), so for named arms the last graph that always exists is S3 (before the cycle step); `partial_stages.py` reports it.
- SHD against CausalArena's published tables is not calibrated (gate C2 fails); directed-edge F1 is (gate C1).

- Torch-based wrappers were not run in the offline experiment (the analysis sandbox has no PyTorch).
- The sachs reference is the repo's `base_graph.npy`; scores against it measure agreement with that reference.
- Literature quotes marked A in the pass 6 report are second-hand.
