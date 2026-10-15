"""Export Causal-Copilot's stage graphs S0-S3 for every BND-08 S2 run (input to the B5 adapter for Causal-Copilot).

  python -m audit.export_cc_stages --runs-dir RUNS --mapping datasets/suite_q1s2/MAPPING.json --repo CAUSAL_COPILOT \
      --out analysis/results/q2_b5/cc_stages_s2.json

The stages are rebuilt exactly as analysis/partial_stages.py does (its Q1 gate showed the rebuilt S2 and S3 equal the
graphs the pipeline recorded): S0 the algorithm's graph handed to refinement; S1 after the bootstrap filter; S2 after
the LLM review (direct / forbid); S3 after KCI pruning. Causal-Copilot does not record where an arrow came from; these
stage differences are the provenance our lineage tool reconstructs, and the adapter labels them as reconstructed.
Graphs are written over the dataset's column labels, Causal-Copilot's convention decoded (cc_graph.pair_type).
"""
import argparse, glob, json, os, pickle, sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis"))


def decode(M, labels):
    import cc_graph as G
    D, U = [], []
    p = len(labels)
    for a in range(p):
        for b in range(a + 1, p):
            t = G.pair_type(M, a, b)
            if t == "a->b":
                D.append([labels[a], labels[b]])
            elif t == "b->a":
                D.append([labels[b], labels[a]])
            elif t != "none":
                U.append([labels[a], labels[b], t])
    return {"directed": D, "undirected": U}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", required=True)
    ap.add_argument("--mapping", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--analysis", default=str(ROOT / "analysis"), help="folder holding lineage.py / stability.py")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    sys.path[:0] = [a.analysis, a.repo, os.path.join(a.repo, "externals", "causal-learn")]
    from lineage import step_bootstrap, step_kci, step_llm
    from stability import arm_of, family_role
    mapping = json.load(open(a.mapping))
    rows = []
    for meta_f in sorted(Path(a.runs_dir).glob("*/meta.json")):
        meta = json.load(open(meta_f))
        if meta.get("label") != "s2" or meta.get("stub_llm"):
            continue
        arts = {}
        for f in sorted(glob.glob(str(meta_f.parent / "artifacts" / "*.pkl"))):
            with open(f, "rb") as fh:
                x = pickle.load(fh)
            arts.setdefault(x["name"], []).append(x)
        arm, spec = arm_of(meta, mapping)
        fam, role = family_role(arm, spec)
        labels = spec["column_labels"]
        need = ("quality_judge", "bootstrap_recommend", "llm_evaluation_new", "kci_pruning")
        row = {"run_id": meta["run_id"], "arm": arm, "family": fam, "role": role, "labels": labels,
               "completed": not meta.get("failure")}
        if not all(k in arts for k in need) or arts["kci_pruning"][0].get("ret") is None:
            row["stages"] = None
            rows.append(row)
            continue
        S0 = np.asarray(arts["quality_judge"][0]["args_before"]["kwargs"]["full_graph"]).copy()
        S1, added, deleted = step_bootstrap(S0, arts["bootstrap_recommend"][0]["ret"])
        direct, forbid = arts["llm_evaluation_new"][0]["ret"]
        S2 = step_llm(S1, direct, forbid)
        S3 = step_kci(S2, arts["kci_pruning"][0]["ret"])
        S2_rec = np.asarray(arts["kci_pruning"][0]["args_before"]["args"][1])
        row["rebuilt_S2_equals_recorded"] = bool(np.array_equal(S2, S2_rec))
        row["stages"] = {k: decode(M, labels) for k, M in (("S0", S0), ("S1", S1), ("S2", S2), ("S3", S3))}
        rows.append(row)
    out = {"tickets": ["BLD-15", "CAP-09"], "source": "BND-08 S2 runs (gpt-4o), artifacts rebuilt as analysis/partial_stages.py", "runs": rows}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    print("runs %d; with stages %d; S2 rebuilt equal %d" % (len(rows), sum(1 for r in rows if r["stages"]),
                                                           sum(1 for r in rows if r.get("rebuilt_S2_equals_recorded"))))


if __name__ == "__main__":
    main()
