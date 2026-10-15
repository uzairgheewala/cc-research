"""Dev-only ceiling of B3's orient-only rule: the directed-F1 gain if every pair the data-only ledger (frozen kernel, rule
C3) leaves open were oriented by a perfect tier oracle (true edges in their true direction; open non-edges stay open).
Also the share of the ledger's adjacencies that are open. Reads the dev split only.

  CC_CAUSAL_LEARN=... python analysis/q2_b3_ceiling_dev.py --workers 2  -> analysis/results/q2_b3/ceiling_dev.json
"""
import argparse, json, multiprocessing as mp, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))


def one(args):
    path, family = args
    from kernel import build as B, views
    from score import bench, graph
    s = bench.load(path)
    name = Path(path).name
    names = list(s["node_ids"])
    led, info = B.build(s["values"], names, rule="C3", created_utc="", file_meta={"source": "ceiling", "file": name})
    if led is None:
        return {"file": name, "failure": info.get("failure")}
    I = bench.truth_info(family, name)
    T, seed = I["T"], graph.file_seed(name)
    D, U = views.graph_sets(led)
    D, U = set(D), set(map(tuple, U))
    Do, Uo = set(D), set()
    for a, b in U:
        if (a, b) in T:
            Do.add((a, b))
        elif (b, a) in T:
            Do.add((b, a))
        else:
            Uo.add((a, b))
    f_d = graph.directed_f1(D, U, T, seed)["f1"]
    f_o = graph.directed_f1(Do, Uo, T, seed)["f1"]
    return {"file": name, "scenario": bench.scenario_of(name), "f1_D": f_d, "f1_oracle_open": f_o, "gain": f_o - f_d,
            "directed": len(D), "open": len(U), "open_true_edges": sum(1 for a, b in U if (a, b) in T or (b, a) in T)}


def _by(rows):
    g = {}
    for r in rows:
        g.setdefault(r["scenario"], []).append(r["gain"])
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    from score import bench, paired
    out = {"split": "dev", "rule": "C3", "what": __doc__.strip().splitlines()[0], "families": {}}
    for fam in ("semantic", "formula"):
        files = [str(p) for p in bench.files(fam, split="dev")]
        with mp.get_context("fork").Pool(a.workers, maxtasksperchild=10) as pool:
            rows = [r for r in pool.map(one, [(f, fam) for f in files]) if "failure" not in r]
        adj = sum(r["directed"] + r["open"] for r in rows)
        out["families"][fam] = {
            "files": len(rows), "f1_D": sum(r["f1_D"] for r in rows) / len(rows),
            "f1_oracle_open": sum(r["f1_oracle_open"] for r in rows) / len(rows),
            "gain": paired.cluster_bootstrap(_by(rows)),
            "open_share_of_adjacencies": sum(r["open"] for r in rows) / adj,
            "open_true_edge_share_of_open": sum(r["open_true_edges"] for r in rows) / max(1, sum(r["open"] for r in rows)),
            "rows": rows}
        print(fam, {k: v for k, v in out["families"][fam].items() if k != "rows"})
    json.dump(out, open(ROOT / "analysis" / "results" / "q2_b3" / "ceiling_dev.json", "w"), indent=1)


if __name__ == "__main__":
    main()
