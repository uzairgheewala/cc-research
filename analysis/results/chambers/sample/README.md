# Causal Chambers obs+int sample (BEN-10, BND-07)

Status: **not built yet.** `lt_interventions_standard_v1.zip` could not be downloaded into this workspace: the egress proxy refuses the host `causalchamber.s3.eu-central-1.amazonaws.com` (see `../fetch_status.json`). The folder holds only `true_graph_lt_standard.csv` and `sample_status.json`. Once the zip is in `external/causal_chambers/` with the sha256 from `external/FETCH_REPORT.json`, run:

```
PYTHONDONTWRITEBYTECODE=1 python analysis/chambers_map.py
PYTHONDONTWRITEBYTECODE=1 python analysis/chambers_sample.py
```

## Sampling rule (deterministic)

- Source: `lt_interventions_standard_v1` (light tunnel, standard configuration). The zip is read only after its sha256 matches `external/FETCH_REPORT.json`.
- Columns: the 38 variables of `causalchamber.ground_truth.main.variables('lt', 'standard')` (package 0.2.8), in that order, after `experiment`, `regime`, `target`.
- Regime 0: `uniform_reference`, the observational reference. All actuators are sampled independently and the sensor parameters are fixed (dataset README). 1,000 rows are drawn from its 10,000 rows without replacement.
- Regimes 1 and up: every other experiment in the zip that the README lists, in sorted name order. Each is a single-target intervention, and up to 100 rows are drawn from each without replacement. The README lists 58 such experiments of 1,000 rows each, so the expected total is 1,000 + 58 x 100 = 6,800 rows.
- Randomness: a single `numpy.random.default_rng(20261012)` makes all the draws, in the order above. Kept rows stay in their original file order.
- Targets: taken from the README experiment table (`../mapping.json`). In experiment names, `osr_1` and `osr_2` mean the columns `osr_angle_1` and `osr_angle_2`.
- `in_authors_a2` in `regimes.csv` marks the 20 interventional experiments that the authors used for task a2 (`causal_discovery_iid.ipynb`, cell 18).

## Files (after a build)

| File | Content |
|---|---|
| `obs_int_sample.csv` | experiment, regime, target, 38 variables |
| `obs_int_sample.npz` | `X`, `regime`, `variables`, `experiments`, `targets` (per regime; '' = none), `true_adjacency` |
| `regimes.csv` | regime, experiment, target, rows kept, rows in file, in_authors_a2 |
| `true_graph_lt_standard.csv` | 38 x 38 adjacency, row -> column (`graph('lt','standard')`); 57 edges |
| `sample_status.json` | the rule, row counts, and any experiments in the zip that were not used |

## Caveats

- Some README rows for sensor-parameter experiments list several symbols, for example "We set O_1, O_2, O_C = 2". The rule takes the single target named in the experiment name. This has not been checked against the files.
- Interventions on `v_c`, `osr_c`, `t_*`, `diode_*` and `osr_angle_*` target variables outside the authors' 20-variable subgraph. They are still interventions in the full 38-variable graph.
