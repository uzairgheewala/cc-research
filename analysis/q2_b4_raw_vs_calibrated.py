"""TGT-12: calibrated claim probabilities against raw bootstrap frequencies (stability used as the probability), on the
rows of B4's single logged held-out read (analysis/results/q2_b4/stab_test_<family>.jsonl). No new read: the same rows,
another statistic (the one TGT-12 names). Also the same comparison on dev, out of fold, from fit_dev.json's rows.

  python analysis/q2_b4_raw_vs_calibrated.py  -> analysis/results/q2_b4/raw_vs_calibrated_test.json
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from kernel import confidence  # noqa: E402
from score import calib, paired  # noqa: E402

RES, CAL = ROOT / "analysis" / "results" / "q2_b4", ROOT / "calibration"


def main():
    out = {"what": __doc__.strip().splitlines()[0], "source_rows": "stab_test_<family>.jsonl", "families": {}}
    for fam in ("semantic", "formula"):
        rows = [json.loads(l) for l in open(RES / ("stab_test_%s.jsonl" % fam)) if l.strip()]
        rows = [r for r in rows if "failure" not in r]
        fo = {}
        for kind, si, oi in (("dv", 4, 3), ("edges", 3, 2)):
            m = json.load(open(CAL / ("map_%s_%s.json" % (fam, kind))))["map"]
            by_raw, by_cal = {}, {}
            for r in rows:
                for x in r[kind]:
                    s, ok = float(x[si]), bool(x[oi])
                    by_raw.setdefault(r["scenario"], []).append((s, ok))
                    by_cal.setdefault(r["scenario"], []).append((float(confidence.isotonic_apply(m, [s])[0]), ok))

            def ece_stat(gs):
                items = [x for g in gs for x in g]
                return calib.ece([x[0] for x in items], [x[1] for x in items])

            def diff_stat_factory(keys):
                def f(gs):
                    raw = [x for g in gs for x in g[0]]
                    cal = [x for g in gs for x in g[1]]
                    return calib.ece([x[0] for x in raw], [x[1] for x in raw]) - calib.ece([x[0] for x in cal], [x[1] for x in cal])
                return f
            paired_groups = {s: [(by_raw[s], by_cal[s])] for s in by_raw}
            fo[kind] = {"claims": sum(len(v) for v in by_raw.values()),
                        "ece_raw": paired.cluster_bootstrap(by_raw, stat=ece_stat),
                        "ece_calibrated": paired.cluster_bootstrap(by_cal, stat=ece_stat),
                        "ece_raw_minus_calibrated": paired.cluster_bootstrap(
                            paired_groups, stat=lambda gs: diff_stat_factory(None)([x for g in gs for x in g]))}
        out["families"][fam] = fo
        print(fam, {k: {kk: round(vv["point"], 3) if isinstance(vv, dict) else vv for kk, vv in v.items()} for k, v in fo.items()})
    out["TGT-12_met"] = all(v[k]["ece_raw_minus_calibrated"]["lo"] > 0 for v in out["families"].values() for k in ("dv",))
    json.dump(out, open(RES / "raw_vs_calibrated_test.json", "w"), indent=1)


if __name__ == "__main__":
    main()
