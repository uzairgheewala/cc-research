"""BEN-10 (BND-07): build a small observational + interventional sample from lt_interventions_standard_v1.

  PYTHONDONTWRITEBYTECODE=1 python analysis/chambers_sample.py

Sampling rule (deterministic; fixed seed; documented again in analysis/results/chambers/sample/README.md)
  source      external/causal_chambers/lt_interventions_standard_v1.zip, read only after its sha256 matches
              external/FETCH_REPORT.json
  columns     the 38 variables of causalchamber.ground_truth.main.variables('lt', 'standard'), in that order
  regime 0    experiment uniform_reference (observational reference): N_OBS = 1000 rows drawn without replacement
  regimes 1+  every other experiment in the zip whose README row names a single target (all 58 listed in the README),
              taken in sorted name order: up to K = 100 rows each, drawn without replacement
  draws       one numpy.random.default_rng(SEED = 20261012) used in that order (reference first, then sorted
              experiments); kept rows stay in their original file order
  targets     from analysis/results/chambers/mapping.json (README experiment table); osr_1 / osr_2 in experiment names
              are the columns osr_angle_1 / osr_angle_2
  flag        in_authors_a2 marks the 20 interventional experiments the authors used for task a2 (UT-IGSP) in
              causal_discovery_iid.ipynb, cell 18
Outputs (analysis/results/chambers/sample/)
  obs_int_sample.csv     experiment, regime, target, then the 38 variables
  obs_int_sample.npz     X (rows x 38 float), regime (int), variables, experiments, targets (per regime, '' = none),
                         true_adjacency (38 x 38, [i, j] = 1 for i -> j)
  regimes.csv            regime, experiment, target, rows kept, rows in file, in_authors_a2
  true_graph_lt_standard.csv   adjacency from causalchamber.ground_truth.main.graph('lt', 'standard') (written even
                         when the data are missing)
  sample_status.json     what was built, or why not
"""
import json, sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chambers_io as C  # noqa: E402

D = "lt_interventions_standard_v1"
SEED, N_OBS, K = 20261012, 1000, 100
AUTHORS_A2 = ["uniform_red_strong", "uniform_green_strong", "uniform_blue_strong", "uniform_v_c_strong",
              "uniform_t_ir_1_strong", "uniform_t_ir_2_strong", "uniform_t_ir_3_strong", "uniform_t_vis_1_strong",
              "uniform_t_vis_2_strong", "uniform_t_vis_3_strong", "uniform_pol_1_strong", "uniform_pol_2_strong",
              "uniform_v_angle_1_strong", "uniform_v_angle_2_strong", "uniform_l_11_mid", "uniform_l_12_mid",
              "uniform_l_21_mid", "uniform_l_22_mid", "uniform_l_31_mid", "uniform_l_32_mid"]
OUTD = C.OUT / "sample"


def main():
    OUTD.mkdir(parents=True, exist_ok=True)
    GT = C.ground_truth()
    V = GT.variables("lt", "standard")
    A = GT.graph("lt", "standard").loc[V, V]
    A.to_csv(OUTD / "true_graph_lt_standard.csv")
    rule = {"seed": SEED, "n_obs": N_OBS, "k_per_intervention": K, "columns": V,
            "order": "uniform_reference first, then the other experiments sorted by name; one rng for all draws"}
    st = C.data_status(D)
    if st not in C.READABLE:
        json.dump({"built": False, "reason": "%s.zip is %s in external/causal_chambers (S3 host refused by the egress "
                   "proxy; see ../fetch_status.json)" % (D, st), "rule": rule,
                   "written": ["true_graph_lt_standard.csv"]}, open(OUTD / "sample_status.json", "w"), indent=1)
        print("not built: %s.zip is %s" % (D, st))
        return
    mapping = json.load(open(C.OUT / "mapping.json", encoding="utf-8"))
    rec = [r for r in mapping["datasets"] if r["dataset"] == D][0]
    target_of = {e["experiment"]: (e["targets"][0] if e["targets"] else "") for e in rec["experiments"]}
    found = C.experiments(D)
    rng = np.random.default_rng(SEED)
    names = ["uniform_reference"] + sorted(n for n in found if n != "uniform_reference" and n in target_of)
    frames, regimes = [], []
    for r, n in enumerate(names):
        df = C.load_experiment(D, n)
        k = N_OBS if r == 0 else K
        idx = np.sort(rng.choice(len(df), size=min(k, len(df)), replace=False))
        sub = df.iloc[idx][V].copy()
        sub.insert(0, "target", target_of[n])
        sub.insert(0, "regime", r)
        sub.insert(0, "experiment", n)
        frames.append(sub)
        regimes.append({"regime": r, "experiment": n, "target": target_of[n], "rows_kept": int(len(sub)),
                        "rows_in_file": int(len(df)), "in_authors_a2": n in AUTHORS_A2})
    S = pd.concat(frames, ignore_index=True)
    S.to_csv(OUTD / "obs_int_sample.csv", index=False)
    pd.DataFrame(regimes).to_csv(OUTD / "regimes.csv", index=False)
    np.savez_compressed(OUTD / "obs_int_sample.npz", X=S[V].values.astype(float), regime=S.regime.values,
                        variables=np.array(V), experiments=np.array(names),
                        targets=np.array([g["target"] for g in regimes]), true_adjacency=A.values)
    unlisted = sorted(set(found) - set(names))
    json.dump({"built": True, "rule": rule, "rows": int(len(S)), "regimes": len(regimes),
               "experiments_in_zip_not_used": unlisted, "source_sha256": C.expected_sha(D)},
              open(OUTD / "sample_status.json", "w"), indent=1)
    print("built %d rows, %d regimes" % (len(S), len(regimes)))


if __name__ == "__main__":
    main()
