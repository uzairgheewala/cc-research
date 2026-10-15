"""B2 and B3 numbers from their runners' rows, with gates and scenario-cluster intervals.

  python -m kernel.report_b23 b2 --split dev|test      -> analysis/results/q2_b2/summary_<split>.json
  python -m kernel.report_b23 b3 --split dev|test      -> analysis/results/q2_b3/summary_<split>.json
"""
import json, statistics as st, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
FAMS = ("semantic", "formula")


def _rows(path):
    return [json.loads(l) for l in open(path) if l.strip()] if Path(path).exists() else []


def _prec(d):
    return d["correct"] / d["committed"] if d["committed"] else None


def b2(split):
    from score import paired
    out = {"tickets": ["BLD-03", "CAP-03", "TGT-06"], "split": split, "families": {}}
    for fam in FAMS:
        rows = [r for r in _rows(ROOT / "analysis" / "results" / "q2_b2" / ("%s_%s.jsonl" % (split, fam))) if "D" in r]
        if not rows:
            continue
        per_file = {r["file"]: (_prec(r["DI"]["dv1"]) or 0) - (_prec(r["D"]["dv1"]) or 0) for r in rows}
        f1d = {r["file"]: r["DI"]["f1"] - r["D"]["f1"] for r in rows}
        sc = lambda f: next(r["scenario"] for r in rows if r["file"] == f)  # noqa: E731
        by = {}
        for r in rows:
            by.setdefault(r["scenario"], []).append((r["DI"]["dv1"]["correct"], r["DI"]["dv1"]["committed"], r["D"]["dv1"]["correct"], r["D"]["dv1"]["committed"]))

        def pooled_diff(gs):
            a = sum(x[0] for g in gs for x in g) / max(1, sum(x[1] for g in gs for x in g))
            b = sum(x[2] for g in gs for x in g) / max(1, sum(x[3] for g in gs for x in g))
            return a - b
        com = lambda lab: sum(r[lab]["dv1"]["committed"] for r in rows)  # noqa: E731
        cor = lambda lab: sum(r[lab]["dv1"]["correct"] for r in rows)  # noqa: E731
        pairs = sum(r["D"]["dv1"]["pairs"] for r in rows)
        inter = [r["intervention"] for r in rows]
        fo = {"files": len(rows),
              "D": {"f1": st.mean(r["D"]["f1"] for r in rows), "dv1_precision": cor("D") / com("D"), "dv1_coverage": com("D") / pairs},
              "DI": {"f1": st.mean(r["DI"]["f1"] for r in rows), "dv1_precision": cor("DI") / com("DI"), "dv1_coverage": com("DI") / pairs},
              "dv1_mean_per_file_diff": st.mean(per_file.values()),
              "dv1_pooled_diff": paired.cluster_bootstrap(by, stat=pooled_diff),
              "f1_diff": paired.paired_diff({f: v for f, v in f1d.items()}, {f: 0.0 for f in f1d}, sc),
              "oriented": sum(i["oriented"] for i in inter), "oriented_right": sum(i["oriented_right"] for i in inter),
              "propagated": sum(i["propagated"] for i in inter), "conflicts": sum(i["conflicts"] for i in inter),
              "ledgers_failing": sum(1 for r in rows for lab in ("D", "DI") if r[lab]["verify_failures"] or not r[lab]["checker_ok"])}
        fo["B2.2_family"] = fo["dv1_mean_per_file_diff"] >= 0
        out["families"][fam] = fo
    chamb = ROOT / "analysis" / "results" / "q2_b2" / "chambers.json"
    if split == "test" and chamb.exists():
        c = json.load(open(chamb))
        rule = c["rule"]
        d, di = c["rows"]["kernel D (%s)" % rule], c["rows"]["kernel D+I (%s)" % rule]
        out["chambers"] = {"rows": c["rows"], "B2.2_chambers": (di["precision"] or 0) >= (d["precision"] or 0),
                           "ER-C": {"kernel_D_minus_GES": d.get("minus_ges"), "kernel_DI_minus_GES": di.get("minus_ges"),
                                    "within_0.03": [x is not None and x >= -0.03 for x in (d.get("minus_ges"), di.get("minus_ges"))]}}
    if out["families"]:
        out["B2.2_arena"] = all(v["B2.2_family"] for v in out["families"].values())
    dst = ROOT / "analysis" / "results" / "q2_b2" / ("summary_%s.json" % split)
    json.dump(out, open(dst, "w"), indent=1)
    for fam, v in out["families"].items():
        print(fam, {k: (round(x, 4) if isinstance(x, float) else x) for k, x in v.items() if k not in ("dv1_pooled_diff", "f1_diff", "D", "DI")})
        print("   D", {k: round(x, 4) for k, x in v["D"].items()}, "DI", {k: round(x, 4) for k, x in v["DI"].items()},
              "pooled diff %.4f [%.4f, %.4f]" % (v["dv1_pooled_diff"]["point"], v["dv1_pooled_diff"]["lo"], v["dv1_pooled_diff"]["hi"]))
    if "chambers" in out:
        print("chambers", json.dumps(out["chambers"]["ER-C"]), "B2.2", out["chambers"]["B2.2_chambers"])


def b3(split):
    from score import paired
    out = {"tickets": ["BLD-04", "CAP-04", "TGT-11", "TGT-19"], "split": split, "families": {}}
    for fam in FAMS:
        rows = [r for r in _rows(ROOT / "analysis" / "results" / "q2_b3" / ("%s_%s.jsonl" % (split, fam))) if r.get("arms")]
        if not rows:
            continue
        fo = {"files": len(rows), "arms": {}}
        for arm in ("real", "neutral", "moved"):
            A = [r for r in rows if arm in r["arms"] and "D" in r["arms"][arm]]
            gain = {r["file"]: r["arms"][arm]["DK"]["f1"] - r["arms"][arm]["D"]["f1"] for r in A}
            egain = {r["file"]: r["arms"][arm]["expected_f1_DK"] - r["arms"][arm]["expected_f1_D"] for r in A}
            sc = {r["file"]: r["scenario"] for r in A}
            sup = {}
            for r in A:
                for k, v in r["arms"][arm]["supplier"].items():
                    if isinstance(v, dict):
                        for kk, vv in v.items():
                            sup[k + "." + kk] = sup.get(k + "." + kk, 0) + vv
                    else:
                        sup[k] = sup.get(k, 0) + v
            fo["arms"][arm] = {"files": len(A), "f1_D": st.mean(r["arms"][arm]["D"]["f1"] for r in A), "f1_DK": st.mean(r["arms"][arm]["DK"]["f1"] for r in A),
                               "gain": paired.paired_diff(gain, {f: 0.0 for f in gain}, lambda f: sc[f]),
                               "expected_gain": paired.paired_diff(egain, {f: 0.0 for f in egain}, lambda f: sc[f]),
                               "decided": sum(r["arms"][arm]["decided"] for r in A), "decided_right": sum(r["arms"][arm]["decided_true_right"] for r in A),
                               "decided_wrong": sum(r["arms"][arm]["decided_true_wrong"] for r in A),
                               "within_t3": sum(1 for r in A if r["arms"][arm]["within_t3"]), "skeleton_identical": sum(1 for r in A if r["arms"][arm]["skeleton_identical"]),
                               "claims_identical_to_D": sum(1 for r in A if r["arms"][arm]["claims_identical_to_D"]),
                               "ledgers_failing": sum(1 for r in A if r["arms"][arm]["verify_failures"] or not r["arms"][arm]["checker_ok"]),
                               "skipped_cycle": sum(r["arms"][arm]["skipped_cycle"] for r in A), "supplier": sup}
        a = fo["arms"]
        fo["B3.1"] = a["neutral"]["claims_identical_to_D"] == a["neutral"]["files"] and all(v["skeleton_identical"] == v["files"] for v in a.values())
        fo["B3.2"] = a["moved"]["within_t3"] == a["moved"]["files"]
        fo["B3.3"] = (a["real"]["f1_DK"] - a["real"]["f1_D"]) >= -0.01
        fo["ER-4a_route_B"] = {"gain": a["real"]["gain"]["point"], "lower": a["real"]["gain"]["lo"], "met": a["real"]["gain"]["lo"] > 0.03}
        out["families"][fam] = fo
    dst = ROOT / "analysis" / "results" / "q2_b3" / ("summary_%s.json" % split)
    json.dump(out, open(dst, "w"), indent=1)
    for fam, v in out["families"].items():
        print(fam, "B3.1", v["B3.1"], "B3.2", v["B3.2"], "B3.3", v["B3.3"], "route B", v["ER-4a_route_B"])
        for arm, x in v["arms"].items():
            print("   %-7s files %d F1 D %.4f DK %.4f gain %+.4f [%+.4f, %+.4f] decided %d (right %d wrong %d) within T3 %d skeleton same %d claims same %d failing %d" % (
                arm, x["files"], x["f1_D"], x["f1_DK"], x["gain"]["point"], x["gain"]["lo"], x["gain"]["hi"], x["decided"], x["decided_right"], x["decided_wrong"],
                x["within_t3"], x["skeleton_identical"], x["claims_identical_to_D"], x["ledgers_failing"]))


if __name__ == "__main__":
    split = sys.argv[sys.argv.index("--split") + 1] if "--split" in sys.argv else "dev"
    {"b2": b2, "b3": b3}[sys.argv[1]](split)
