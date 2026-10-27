"""BLD-06 live on the fork: refinement v2 (branch) against unmodified main on the same image and the same 30 tables.

Tickets: BLD-06, EXT-03, INF-06

    python analysis/bld06_live_compare.py [--out analysis/results/fork/bld06_live_compare.json]

Pre-registration: plans/bld06_live_prereg.json (hashed before any graph was scored). Reads only JSON state snapshots
(runs/<id>/state/*.json), so it needs NumPy but not the pipeline's environment. BND-08's runs (old image) are scored the
same way and reported beside, never compared by a rule.
"""
import argparse, glob, hashlib, json, sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
sys.path.insert(0, str(ROOT))
PREREG = ROOT / "plans" / "bld06_live_prereg.json"
MAP = ROOT / "datasets" / "suite_q1s2" / "MAPPING.json"


def arr(x):
    if isinstance(x, dict) and x.get("__ndarray__"):
        return np.array(x["data"])
    return None if x is None else np.asarray(x)


def last_state(run_id):
    fs = sorted(glob.glob(str(ROOT / "runs" / run_id / "state" / "*.json")))
    fin = [f for f in fs if f.endswith("99_final.json")]
    return json.loads(Path(fin[-1] if fin else fs[-1]).read_text(encoding="utf-8")), bool(fin)


def score_run(run_id, arm, mapping):
    import cc_graph as G
    st, completed = last_state(run_id)
    spec = mapping["arms"][arm]
    E = G.truth_edges(np.load(MAP.parent / spec["reference_by_data"]))
    r = st.get("results") or {}
    S0, fin = arr(r.get("converted_graph")), arr(r.get("revised_graph")) if completed else None
    p = len(spec["column_labels"])
    out = {"run_id": run_id, "arm": arm, "family": spec["family"], "role": spec["role"], "completed": completed}
    if S0 is not None:
        s = G.score(S0, E, p)
        out["S0_adj_f1"], out["S0_dir_f1"] = s["adj_f1"], s["dir_f1"]
    if fin is not None:
        s = G.score(fin, E, p)
        out["final_adj_f1"], out["final_dir_f1"] = s["adj_f1"], s["dir_f1"]
    out["delivered_dir_f1"] = out.get("final_dir_f1") or 0.0
    return out


def series(capped, mapping):
    c = json.loads((ROOT / capped).read_text(encoding="utf-8"))
    rows = []
    for r in c["runs"].values():
        arm = Path(r["dataset"]).parent.name
        rows.append(dict(score_run(r["run_id"], arm, mapping), usd=r.get("usd")))
    return {x["arm"]: x for x in rows}


def paired(a, b, key, arms):
    from score import paired as P
    by = {}
    for arm in arms:
        if a[arm].get(key) is not None and b[arm].get(key) is not None:
            by.setdefault(a[arm]["family"], []).append(a[arm][key] - b[arm][key])
    out = P.cluster_bootstrap(by) if by else None
    if out:
        out["arms"] = sum(len(v) for v in by.values())
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "analysis" / "results" / "fork" / "bld06_live_compare.json"))
    a = ap.parse_args(argv)
    mapping = json.loads(MAP.read_text(encoding="utf-8"))
    br = series("plans/results/fork_bld06_live.capped.json", mapping)
    mn = series("plans/results/fork_bld06_live_main.capped.json", mapping)
    arms = sorted(set(br) & set(mn))
    both = [x for x in arms if br[x]["completed"] and mn[x]["completed"]]
    hist = {}
    b8 = ROOT / "analysis" / "results" / "stability_s2" / "bnd08_summary.json"
    if b8.exists():
        for r in json.loads(b8.read_text())["runs"]:
            try:
                hist[r["arm"]] = score_run(r["run_id"], r["arm"], mapping)
            except Exception as e:  # noqa: BLE001 - history only
                hist[r["arm"]] = {"error": str(e)[:200]}
    mean = lambda d, k, ks: float(np.mean([d[x][k] for x in ks if d[x].get(k) is not None])) if ks else None
    P = {"L1": paired(br, mn, "delivered_dir_f1", arms), "L2": paired(br, mn, "final_adj_f1", both),
         "L2_dir": paired(br, mn, "final_dir_f1", both), "L3": paired(br, mn, "S0_adj_f1", arms)}
    v = {"L1": P["L1"]["point"] >= 0.02, "L2": P["L2"]["point"] >= -0.02, "L3": abs(P["L3"]["point"]) <= 0.03}
    rule = "drop_in" if v["L2"] and v["L3"] else ("trade_off" if v["L3"] else "incomparable")
    out = {"tickets": ["BLD-06", "EXT-03", "INF-06"], "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest(),
           "arms": len(arms), "both_completed": len(both),
           "completed": {"branch": sum(br[x]["completed"] for x in arms), "main": sum(mn[x]["completed"] for x in arms),
                         "bnd08": sum(1 for x in hist.values() if x.get("completed"))},
           "usd": {"branch": round(sum(br[x]["usd"] or 0 for x in arms), 4), "main": round(sum(mn[x]["usd"] or 0 for x in arms), 4)},
           "means": {s: {k: mean(d, k, arms if k != "final_adj_f1" and k != "final_dir_f1" else both)
                         for k in ("S0_adj_f1", "S0_dir_f1", "final_adj_f1", "final_dir_f1", "delivered_dir_f1")}
                     for s, d in (("branch", br), ("main", mn))},
           "means_bnd08_history": {k: mean(hist, k, [x for x in hist if "error" not in hist[x]]) for k in ("S0_adj_f1", "final_adj_f1", "final_dir_f1", "delivered_dir_f1")},
           "paired_branch_minus_main": P, "verdicts": v, "rule": rule,
           "rows": {"branch": br, "main": mn, "bnd08": hist}}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps({k: out[k] for k in ("arms", "both_completed", "completed", "usd", "verdicts", "rule")}))
    print(json.dumps({k: (None if x is None else round(x["point"], 4)) for k, x in P.items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
