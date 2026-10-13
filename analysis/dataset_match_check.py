"""Do the repo's named datasets match CausalArena's real-data index (variables, edges, rows)? No LLM.
Writes dataset_match_check.json."""
import csv, json, os, sys
import numpy as np

PAIRS = {"abalone": ("cd_csg_abalone", "data/dataset/Abalone"), "autompg": ("cd_csg_auto_mpg", "data/dataset/Auto_mpg"),
         "concrete": ("cd_csg_concrete_ccs", "data/dataset/CCS_Data"), "dwd": ("cd_csg_dwd", "data/dataset/DWD")}


def main():
    research, repo, out = sys.argv[1], sys.argv[2], sys.argv[3]
    idx = {r["dataset_id"]: r for r in csv.DictReader(open(os.path.join(research, "external/causalarena/real_data_index/real_dataset_index.csv")))}
    m = json.load(open(os.path.join(research, "datasets/suite_b1/MAPPING.json")))
    res = {}
    for fam, (cid, folder) in PAIRS.items():
        spec = next(s for s in m["arms"].values() if s["family"] == fam and s["role"] == "real")
        ref = np.load(os.path.join(research, "datasets/suite_b1", spec["reference_by_data"]))
        csvs = [f for f in os.listdir(os.path.join(repo, folder)) if f.endswith(".csv")]
        rows = sum(1 for _ in open(os.path.join(repo, folder, csvs[0]), encoding="utf-8")) - 1
        repo_t = (len(spec["column_labels"]), int((ref != 0).sum()), rows)
        ca = idx[cid]; ca_t = (int(ca["d"]), int(ca["edges"]), int(ca["n"]))
        res[fam] = {"repo_vars_edges_rows": repo_t, "causalarena_vars_edges_rows": ca_t, "match": repo_t == ca_t}
    os.makedirs(out, exist_ok=True)
    json.dump(res, open(os.path.join(out, "dataset_match_check.json"), "w"), indent=1)
    print(json.dumps(res))


if __name__ == "__main__":
    main()
