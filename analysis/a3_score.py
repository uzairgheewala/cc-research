"""AB-07 / A3 scorer: verdicts O1-O5 from the tier answers, exactly by the pre-registered rules (plans/a3_prereg.json).

  python analysis/a3_score.py --answers plans/results/a3_tiers_answers.jsonl --root external/causalarena \
      --out analysis/results/a3 [--files-per-scenario 5]

Edge order: a true edge u->v is correct if tier(u) < tier(v), contradicted if tier(u) > tier(v), tied otherwise.
Tiers are read through the label each variable was shown with (plans/a3_scenarios.json):
  real / neutral : the shown name of variable i is variable i
  moved          : "by data"  - the name shown for variable i stands for variable i (the column's data)
                   "by label" - the name shown for variable i is the real name of variable sigma(i); the model's tier for
                                that name is compared with the graph over the names' owners
Consensus tiers: each phrasing's tiers normalised to [0, 1] by position, median over the non-abstained phrasings.
O4/O5: tier_regression (alpha 0.01, analysis/order_value.py) on the scenario's obs_only replicate files with consensus
tiers from the real arm; directed F1 vs the true graph. Writes a3.json and CONTRACT.json. No model calls.
Tickets: AUD-48, RQ-10..RQ-14, DEC-02
"""
import argparse, json, os, statistics as st, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
from order_value import tier_regression  # noqa: E402


def positions(tiers, label_to_var):
    """tiers (list of lists of labels) -> {variable: normalised position in [0, 1]}."""
    k = len(tiers)
    return {label_to_var[n]: (i / (k - 1) if k > 1 else 0.0) for i, t in enumerate(tiers) for n in t}


def edge_shares(pos, edges):
    if pos is None or not edges:
        return {"correct": 0.0, "contradicted": 0.0, "tied": 1.0, "abstained": True}
    c = sum(1 for u, v in edges if pos[u] < pos[v])
    x = sum(1 for u, v in edges if pos[u] > pos[v])
    n = len(edges)
    return {"correct": c / n, "contradicted": x / n, "tied": (n - c - x) / n, "abstained": False}


def consensus(pos_list, d):
    pl = [p for p in pos_list if p is not None]
    if not pl:
        return None
    return {v: float(np.median([p[v] for p in pl])) for v in range(d)}


def verdict(name, x, y=None):
    """x = mean correct, y = mean contradicted (O1/O3-label); for O2/O3-data x = correct - contradicted; O4/O5 x = F1."""
    if name in ("O1", "O3_label"):
        if x >= 0.70 and y <= 0.10:
            return "supported"
        return "refuted" if (x < 0.50 or y > 0.25) else "inconclusive"
    if name in ("O2", "O3_data"):
        return "supported" if x <= 0.05 else ("refuted" if x > 0.15 else "inconclusive")
    if name == "O4":
        return "supported" if x >= 0.634 else ("refuted" if x <= 0.50 else "inconclusive")
    if name == "O5":
        return "supported" if x >= 0.524 else ("refuted" if x <= 0.40 else "inconclusive")
    raise ValueError(name)


def mean(xs):
    xs = list(xs)
    return round(st.mean(xs), 4) if xs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers", required=True)
    ap.add_argument("--scenarios", default=str(HERE.parent / "plans" / "a3_scenarios.json"))
    ap.add_argument("--root", default=str(HERE.parent / "external" / "causalarena"))
    ap.add_argument("--out", default=str(HERE / "results" / "a3"))
    ap.add_argument("--files-per-scenario", type=int, default=5)
    a = ap.parse_args()
    S = json.load(open(a.scenarios, encoding="utf-8"))
    ans = [json.loads(l) for l in open(a.answers, encoding="utf-8") if l.strip()]
    stub = any(r.get("stub") for r in ans)
    by = {}
    for r in ans:
        by.setdefault((r["family"], r["scenario"], r["arm"]), {})[r["phrasing"]] = r
    rows = []
    for key, sc in S.items():
        fam, scen, d = sc["family"], sc["scenario"], sc["d"]
        E = [tuple(e) for e in sc["true_edges"]]
        sigma = sc["sigma_moved"]
        owner = {sc["labels"]["real"][i]: i for i in range(d)}                 # real name -> its variable
        for arm in ("real", "neutral", "moved"):
            got = by.get((fam, scen, arm), {})
            lab2var = {sc["labels"][arm][i]: i for i in range(d)}
            per_p, pos_data, pos_label = {}, [], []
            for pid in ("p0", "p1", "p2"):
                r = got.get(pid)
                tiers = r["tiers"] if r else None
                pd_ = positions(tiers, lab2var) if tiers else None
                pos_data.append(pd_)
                pl = positions(tiers, owner) if (tiers and arm == "moved") else None
                pos_label.append(pl)
                per_p[pid] = {"by_data": edge_shares(pd_, E), "answered": r is not None}
                if arm == "moved":
                    per_p[pid]["by_label"] = edge_shares(pl, E)
            cons = consensus(pos_data, d)
            row = {"family": fam, "scenario": scen, "split": sc["split"], "arm": arm, "d": d, "edges": len(E),
                   "per_phrasing": per_p, "consensus_by_data": edge_shares(cons, E),
                   "abstained_phrasings": sum(1 for p in pos_data if p is None)}
            if arm == "moved":
                row["consensus_by_label"] = edge_shares(consensus(pos_label, d), E)
            if arm == "real" and cons is not None:
                tier = [cons[v] for v in range(d)]
                folder = Path(a.root) / "scm" / fam / "data" / ("%s_obs_only" % fam)
                stem = sc["file_rep000"].replace("rep000.npz", "")
                f1s = []
                for k in range(a.files_per_scenario):
                    p = folder / ("%srep%03d.npz" % (stem, k))
                    if not p.exists():
                        continue
                    s = CA.load(p)
                    pred = tier_regression(s["values"], tier)
                    f1s.append(CA.directed_scores(pred, set(), CA.true_edges(s["g"]), d, "drop")["f1"])
                row["tier_regression_f1"] = mean(f1s)
                row["tier_regression_files"] = len(f1s)
            rows.append(row)

    def agg(fam, arm, field, split=None):
        xs = [r for r in rows if r["family"] == fam and r["arm"] == arm and (split is None or r["split"] == split)]
        out = {"scenarios": len(xs)}
        if not xs:
            return out
        for k in ("correct", "contradicted", "tied"):
            out[k] = mean(r[field][k] for r in xs)
        out["correct_minus_contradicted"] = round(out["correct"] - out["contradicted"], 4)
        out["abstained_scenarios"] = sum(1 for r in xs if r[field]["abstained"])
        return out

    res = {"tickets": ["AUD-48", "RQ-10", "RQ-11", "RQ-12", "RQ-13", "RQ-14"], "answers_file": a.answers, "stub": stub,
           "requests_answered": len(ans), "abstained_requests": sum(1 for r in ans if r.get("abstained")), "families": {}, "verdicts": {}}
    for fam in ("semantic", "formula"):
        F = res["families"][fam] = {}
        for arm in ("real", "neutral", "moved"):
            F[arm] = {"consensus_by_data": agg(fam, arm, "consensus_by_data"),
                      "dev": agg(fam, arm, "consensus_by_data", "dev"), "test": agg(fam, arm, "consensus_by_data", "test")}
            if arm == "moved":
                F[arm]["consensus_by_label"] = agg(fam, arm, "consensus_by_label")
            for pid in ("p0", "p1", "p2"):
                xs = [r["per_phrasing"][pid]["by_data"] for r in rows if r["family"] == fam and r["arm"] == arm]
                F[arm]["phrasing_" + pid] = {k: mean(x[k] for x in xs) for k in ("correct", "contradicted")}
        reg = [r["tier_regression_f1"] for r in rows if r["family"] == fam and r["arm"] == "real" and r.get("tier_regression_f1") is not None]
        F["tier_regression_f1_mean"] = mean(reg)
        F["tier_regression_scenarios"] = len(reg)
    sem = res["families"]["semantic"]
    o1 = sem["real"]["consensus_by_data"]
    res["verdicts"]["O1"] = {"value": {"correct": o1.get("correct"), "contradicted": o1.get("contradicted")},
                             "verdict": verdict("O1", o1.get("correct", 0), o1.get("contradicted", 1))}
    o2 = sem["neutral"]["consensus_by_data"]["correct_minus_contradicted"]
    res["verdicts"]["O2"] = {"value": o2, "verdict": verdict("O2", o2)}
    o3l = sem["moved"]["consensus_by_label"]
    o3d = sem["moved"]["consensus_by_data"]["correct_minus_contradicted"]
    res["verdicts"]["O3"] = {"by_label": {"correct": o3l.get("correct"), "contradicted": o3l.get("contradicted"),
                                          "verdict": verdict("O3_label", o3l.get("correct", 0), o3l.get("contradicted", 1))},
                             "by_data": {"value": o3d, "verdict": verdict("O3_data", o3d)}}
    res["verdicts"]["O4"] = {"value": sem["tier_regression_f1_mean"], "verdict": verdict("O4", sem["tier_regression_f1_mean"] or 0)}
    fo = res["families"]["formula"]["tier_regression_f1_mean"]
    res["verdicts"]["O5"] = {"value": fo, "verdict": verdict("O5", fo or 0)}
    if stub:
        res["warning"] = "STUB answers: these verdicts test the pipeline only and are not results"
    os.makedirs(a.out, exist_ok=True)
    name = "a3_STUB.json" if stub else "a3.json"
    json.dump({**res, "rows": rows}, open(os.path.join(a.out, name), "w"), indent=1, ensure_ascii=False)
    json.dump({"producer": "analysis/a3_score.py", "score_bearing": True, "tickets": res["tickets"], "regime": "D+K",
               "split": "per-row", "controls": {"columns_shuffled": "names shown in random order; regression ignores column order",
                                                 "names": "real / neutral / moved (three arms)", "supplier": "model (pre-registered)",
                                                 "knowledge_source": "model tiers"}},
              open(os.path.join(a.out, "CONTRACT.json"), "w"), indent=1)
    for k, v in res["verdicts"].items():
        print(k, v)
    print("wrote", os.path.join(a.out, name))


if __name__ == "__main__":
    main()
