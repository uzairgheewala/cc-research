"""L5 diagnosis (post hoc, NOT pre-registered; labelled as such in the report). Tickets: TGT-18, CAP-03

  python analysis/q2_l5_diag.py   -> analysis/results/q2_v3/l5_diag_dev.json

Why rules S, N and A found almost nothing to act on: for every testable link (an effective target t at one end), whether
do(t) moves y at all, whether t is an ancestor of y in the truth (so it should), whether a candidate mediator existed,
and what the conditional test then said; plus one exploratory rule the pre-registration did not contain (X: no shift
under do(t) while the ledger claims t -> y). Dev only.
"""
import gzip, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
RES = ROOT / "analysis" / "results" / "q2_v3"


def main():
    from score import bench
    rows = [json.loads(l) for l in gzip.open(RES / "l5_links_dev.jsonl.gz", "rt")]
    out = {"post_hoc": True, "tickets": ["TGT-18", "CAP-03"], "families": {}}
    for fam in ("semantic", "formula"):
        C = Counter()
        X = Counter()
        tests_by_kind = {}
        for f in (r for r in rows if r["family"] == fam):
            I = bench.truth_info(fam, f["file"])
            desc = I["desc"]
            D = {tuple(e) for e in f["D"]}
            for l in f["links"]:
                k = l["label"]
                for x in l["tests"]:
                    t, y = x["t"], x["y"]
                    anc = y in desc[t]                       # t is an ancestor of y in the truth: do(t) should move y
                    moved = x["pM"] < 0.01
                    C[(k, "tests")] += 1
                    C[(k, "t_ancestor_of_y")] += anc
                    C[(k, "moved")] += moved
                    C[(k, "moved_given_ancestor")] += moved and anc
                    C[(k, "moved_not_ancestor")] += moved and not anc
                    C[(k, "mediator_found")] += x["nZ"] > 0
                    if moved and x["nZ"] > 0:
                        C[(k, "moved_with_mediator")] += 1
                        C[(k, "moved_with_mediator_pC_ge_0.05")] += x["pC"] >= 0.05
                    tests_by_kind.setdefault(k, []).append(x["pM"])
                    # exploratory rule X: the ledger claims t -> y, yet do(t) leaves y unmoved
                    if (t, y) in D and x["pM"] >= 0.2:
                        X["fired"] += 1
                        X[k] += 1
                        X["reversed_true"] += (k == "true" and (y, t) in I["T"])
        kinds = ("true", "shadow", "common_cause", "unrelated")
        F = {k: {m: C[(k, m)] for m in ("tests", "t_ancestor_of_y", "moved", "moved_given_ancestor", "moved_not_ancestor",
                                        "mediator_found", "moved_with_mediator", "moved_with_mediator_pC_ge_0.05")} for k in kinds}
        for k in kinds:
            a = F[k]
            a["power_moved_when_ancestor"] = round(a["moved_given_ancestor"] / a["t_ancestor_of_y"], 3) if a["t_ancestor_of_y"] else None
            a["false_moves_when_not_ancestor"] = round(a["moved_not_ancestor"] / (a["tests"] - a["t_ancestor_of_y"]), 3) if a["tests"] - a["t_ancestor_of_y"] else None
        fired = X["fired"]
        F["rule_X_exploratory"] = {"fired": fired, "false_share": round(sum(X[k] for k in kinds[1:]) / fired, 3) if fired else None,
                                   "true_but_reversed_in_ledger": X["reversed_true"], "by_kind": {k: X[k] for k in kinds}}
        out["families"][fam] = F
        print("==", fam)
        for k in kinds:
            print("  %-13s %s" % (k, json.dumps(F[k])))
        print("  rule X (exploratory):", F["rule_X_exploratory"])
    json.dump(out, open(RES / "l5_diag_dev.json", "w"), indent=1)


if __name__ == "__main__":
    main()
