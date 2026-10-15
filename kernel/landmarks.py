"""The Q2 landmark table: every external requirement of docs/design/q2_requirements_and_ladders.md with its held-out
value, interval, threshold and verdict, read from the bundles' result files (missing ones reported as pending).

  python -m kernel.landmarks      -> analysis/results/q2_landmarks.json

Rule (docs/decisions/2026-10-14_q2_landmarks.md): held-out only; a landmark is met when the conservative end of the 95%
interval clears its threshold (the lower end for 'at least', the upper end for 'at most').
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "analysis" / "results"


def _load(p):
    p = R / p
    return json.load(open(p)) if p.exists() else None


def main():
    out = {"tickets": ["BLD-02", "BLD-03", "BLD-04", "BLD-05", "BLD-15", "TGT-18", "TGT-19", "TGT-20"], "landmarks": {}}
    L = out["landmarks"]
    b1 = _load("q2_b1/heldout.json")
    if b1:
        L["ER-F"] = {"threshold": "F1 and DV-1 vs plain PC maxP: lower end >= -0.01, both families", "met": b1["ER-F_met"], "evidence": "analysis/results/q2_b1/heldout.json",
                     "values": {f: {"f1": v["vs_pc_maxp"]["f1_diff"], "dv1": v["vs_pc_maxp"]["dv1_pooled_diff"]} for f, v in b1["families"].items()}}
        L["ER-4a_route_A"] = {"threshold": "data-only F1 above GES on one family: lower end > 0", "met": b1["ER-4a_route_A_met"], "evidence": "analysis/results/q2_b1/heldout.json",
                              "values": {f: v["vs_ges"]["f1_diff"] for f, v in b1["families"].items()}}
    b3 = _load("q2_b3/summary_test.json")
    if b3 and b3.get("families"):
        fams = b3["families"]
        L["ER-4a_route_B"] = {"threshold": "real-arm tier gain over B1 > 0.03 on one family: lower end > 0.03", "met": any(v["ER-4a_route_B"]["met"] for v in fams.values()),
                              "evidence": "analysis/results/q2_b3/summary_test.json", "values": {f: v["arms"]["real"]["gain"] for f, v in fams.items()}}
        L["ER-1"] = {"threshold": "neutral arm == D; skeleton identical in every arm; moved-arm loss within T3 in 100% of files; every ledger verifies",
                     "met": all(v["B3.1"] and v["B3.2"] and all(a["ledgers_failing"] == 0 for a in v["arms"].values()) for v in fams.values()),
                     "evidence": "analysis/results/q2_b3/summary_test.json",
                     "values": {f: {"neutral_identical": "%d/%d" % (v["arms"]["neutral"]["claims_identical_to_D"], v["arms"]["neutral"]["files"]),
                                    "moved_within_t3": "%d/%d" % (v["arms"]["moved"]["within_t3"], v["arms"]["moved"]["files"])} for f, v in fams.items()}}
    if "ER-4a_route_A" in L and "ER-4a_route_B" in L:
        L["ER-4a"] = {"met": L["ER-4a_route_A"]["met"] or L["ER-4a_route_B"]["met"], "threshold": "route A or route B"}
    b4 = _load("q2_b4/evaluate_test.json")
    if b4:
        fams = b4["families"]
        L["ER-2"] = {"threshold": "DV-1 precision > 0.80 at coverage >= 0.50, both families: lower end > 0.80",
                     "met": all(v["dv"]["er2_interval"]["lo"] > 0.80 and v["dv"]["selective_at_half_coverage"]["coverage"] >= 0.5 for v in fams.values()),
                     "evidence": "analysis/results/q2_b4/evaluate_test.json",
                     "values": {f: {"precision": v["dv"]["selective_at_half_coverage"], "interval": v["dv"]["er2_interval"]} for f, v in fams.items()}}
        L["ER-3"] = {"threshold": "ECE <= 0.05 (upper end); realised >= claimed - 0.03 at c/g = 1, 2, 4 (lower end)",
                     "met": all(v["dv"]["ece_interval"]["hi"] <= 0.05 and all(g["lo"] >= -0.03 for g in v["dv"]["realised_minus_claimed_intervals"].values())
                                for v in fams.values()),
                     "evidence": "analysis/results/q2_b4/evaluate_test.json",
                     "values": {f: {"ece": v["dv"]["ece_interval"], "realised_minus_claimed": v["dv"]["realised_minus_claimed_intervals"]} for f, v in fams.items()}}
    b5 = _load("q2_b5/rca_test.json")
    if b5 and "ER-4b" in b5:
        L["ER-4b"] = {"threshold": "AC@3 on answered PetShop test issues >= 0.90 at coverage >= 0.5: lower end", "met": b5["ER-4b"]["met"],
                      "evidence": "analysis/results/q2_b5/rca_test.json", "values": b5["ER-4b"]}
    b2 = _load("q2_b2/summary_test.json")
    if b2 and "chambers" in b2:
        c = b2["chambers"]
        L["ER-C"] = {"threshold": "report: kernel DV-1 precision on Causal Chambers within 0.03 of GES", "met": all(c["ER-C"]["within_0.03"]),
                     "report_only": True, "evidence": "analysis/results/q2_b2/summary_test.json", "values": c["ER-C"]}
    for k in ("ER-F", "ER-1", "ER-2", "ER-3", "ER-4a", "ER-4b", "ER-C"):
        L.setdefault(k, {"met": None, "status": "pending"})
    req_paper = ("ER-F", "ER-1", "ER-2", "ER-3", "ER-4a")
    req_wedge = ("ER-F", "ER-1", "ER-2", "ER-3", "ER-4b")
    out["paper_constraints_met"] = [k for k in req_paper if L[k]["met"]]
    out["wedge_constraints_met"] = [k for k in req_wedge if L[k]["met"]]
    out["paper_all_met"] = all(L[k]["met"] for k in req_paper)
    out["wedge_all_met"] = all(L[k]["met"] for k in req_wedge)
    json.dump(out, open(R / "q2_landmarks.json", "w"), indent=1)
    for k, v in L.items():
        print("%-14s %s" % (k, {True: "MET", False: "not met", None: "pending"}[v["met"]]))
    print("paper:", out["paper_constraints_met"], "wedge:", out["wedge_constraints_met"])


if __name__ == "__main__":
    main()
