"""AB-07 follow-up (AUD-48), EXPLORATORY and post hoc (not pre-registered): use the model's tiers the way the claim ledger
would, as knowledge that may only ORIENT adjacencies a data-only method already found, never add or remove them (I5).

  python analysis/a3_orient_only.py --answers plans/results/a3_tiers_answers.jsonl --out analysis/results/a3

For each public semantic and formula file and each data-only method row (PC upstream default rule, PC upstream maxP, GES):
  data only        the method's own graph
  + model tiers    adjacencies kept; a pair whose consensus tier positions differ is oriented earlier tier -> later tier;
                   a tied pair keeps the method's decision (committed arrow or undecided)
  + oracle depth   the same with tiers from the true depth (upper bound for tier knowledge of this kind)
  + moved tiers    the same with the model's tiers from the moved-names arm, read by data (wrong knowledge: bounded harm)
Scores: directed F1 under the expectation rule (undecided at random, per-file seed) and DV-1 committed-claim precision
and coverage with the released intervention targets (decision_value_v2.claims), released column order.
Consensus tiers and the A3 scenario index are rebuilt exactly as analysis/a3_score.py does. No model calls.
"""
import argparse, json, os, statistics as st, sys, zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
from a3_score import positions, consensus  # noqa: E402
from decision_value_v2 import Truth, claims  # noqa: E402
from order_value import depth  # noqa: E402

METHODS = {"PC upstream, default rule": "pc_upstream_{f}_obs_rel", "PC upstream, maxP": "pc_upstream_maxp_{f}_obs_rel",
           "GES (BIC)": {"semantic": "gesbic_semantic_obs", "formula": "gesbic_formula_obs_rel"}}


def reorient(directed, undecided, pos):
    D, U = set(), set()
    for a, b in directed:
        if pos[a] != pos[b]:
            D.add((a, b) if pos[a] < pos[b] else (b, a))
        else:
            D.add((a, b))
    for a, b in undecided:
        if pos[a] != pos[b]:
            D.add((a, b) if pos[a] < pos[b] else (b, a))
        else:
            U.add((a, b))
    return D, U


def f1(D, U, T, d, key):
    return CA.directed_scores(D, {frozenset(u) for u in U}, T, d, "random", seed=zlib.crc32(key.encode()))["f1"]


def dv(D, U, tr, f):
    I = tr.get(f)
    cl = claims(I["n"], D, U, I["targets"])
    pairs = len(I["targets"]) * (I["n"] - 1)
    ok = sum(1 for (t, y), v in cl.items() if (y in I["desc"][t]) == v)
    return ok, len(cl), pairs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", default=str(HERE.parent / "plans" / "results" / "a3_tiers_answers.jsonl"))
    ap.add_argument("--scenarios", default=str(HERE.parent / "plans" / "a3_scenarios.json"))
    ap.add_argument("--root", default=str(HERE.parent / "external" / "causalarena"))
    ap.add_argument("--out", default=str(HERE / "results" / "a3"))
    a = ap.parse_args()
    S = json.load(open(a.scenarios, encoding="utf-8"))
    ans = {}
    for l in open(a.answers, encoding="utf-8"):
        r = json.loads(l)
        ans.setdefault((r["family"], r["scenario"], r["arm"]), {})[r["phrasing"]] = r.get("tiers")
    tiers = {}
    for key, sc in S.items():
        fam, scen, d = sc["family"], sc["scenario"], sc["d"]
        for arm in ("real", "moved"):
            lab2var = {sc["labels"][arm][i]: i for i in range(d)}
            ps = [positions(t, lab2var) if t else None for t in (ans.get((fam, scen, arm), {}).get(p) for p in ("p0", "p1", "p2"))]
            tiers[(fam, scen, arm)] = consensus(ps, d)
        dep = depth(d, [tuple(e) for e in sc["true_edges"]])
        tiers[(fam, scen, "oracle")] = {v: float(dep[v]) for v in range(d)}
    out = {"tickets": ["AUD-48", "BLD-04", "CAP-04"], "status": "exploratory, post hoc (not pre-registered)", "families": {}}
    for fam in ("semantic", "formula"):
        tr = Truth(a.root, fam)
        scen_of = {S[k]["file_rep000"].replace("rep000.npz", ""): S[k]["scenario"] for k in S if S[k]["family"] == fam}
        F = out["families"][fam] = {}
        for lab, spec in METHODS.items():
            name = spec[fam] if isinstance(spec, dict) else spec.format(f=fam)
            p = HERE / "results" / "methods" / (name + ".json")
            if not p.exists():
                continue
            rows = [r for r in json.load(open(p))["rows"] if not r.get("failed")]
            acc = {arm: {"f1": [], "ok": 0, "com": 0, "pairs": 0} for arm in ("data only", "+ model tiers", "+ oracle depth", "+ moved tiers")}
            for r in rows:
                f = r["file"]
                stem = f.split("__rep")[0] + "__"
                scen = scen_of.get(stem)
                if scen is None:
                    continue
                s = CA.load(Path(a.root) / "scm" / fam / "data" / ("%s_obs_only" % fam) / f)
                T, d = CA.true_edges(s["g"]), len(s["node_ids"])
                D0 = {tuple(e) for e in r["directed_edges"]}
                U0 = {tuple(u[:2]) for u in r["undecided_pairs"]}
                for arm, src in (("data only", None), ("+ model tiers", "real"), ("+ oracle depth", "oracle"), ("+ moved tiers", "moved")):
                    pos = tiers.get((fam, scen, src)) if src else None
                    if src and pos is None:
                        continue
                    D, U = (D0, U0) if pos is None else reorient(D0, U0, pos)
                    acc[arm]["f1"].append(f1(D, U, T, d, f))
                    if tr.get(f)["released_targets"]:
                        ok, com, pairs = dv(D, U, tr, f)
                        acc[arm]["ok"] += ok
                        acc[arm]["com"] += com
                        acc[arm]["pairs"] += pairs
            F[lab] = {arm: {"files": len(v["f1"]), "directed_f1": round(st.mean(v["f1"]), 4) if v["f1"] else None,
                            "dv1_precision": round(v["ok"] / v["com"], 4) if v["com"] else None,
                            "dv1_coverage": round(v["com"] / v["pairs"], 4) if v["pairs"] else None} for arm, v in acc.items()}
            print(fam, lab, json.dumps(F[lab]))
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "a3_orient_only.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
