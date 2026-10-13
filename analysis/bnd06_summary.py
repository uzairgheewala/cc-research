"""BND-06: order sensitivity (Q4c, BEN-07) and published-row comparison (REP-07) for every runnable method.

  python analysis/bnd06_summary.py --dir analysis/results/methods --out analysis/results/methods/bnd06_verdicts.json

Inputs: <method>_semantic_obs_rel.json and <method>_semantic_obs_shuf.json (merged causalarena_methods.py outputs; for gesbic
the released-order file is gesbic_semantic_obs.json from BND-04). Pre-registration: plans/bnd06_prereg.json (Q4c text and
metric are read from it, thresholds parsed from its text).
Family mean = replicate-averaged per scenario, then averaged over scenarios. Failed files count as empty graphs.

--family / --tag (BND-06 extension; defaults semantic / none reproduce the pre-registered run unchanged): with
--family formula|synthetic the inputs are <method>_<tag>_rel.json and <method>_<tag>_shuf.json for every method (tag defaults
to "<family>_obs"), the published column is "Formula obs-only" / "Synthetic obs-only", the published population for the
finite-population correction is FAMILY_N_PUB[family] scenarios, and the Q4c verdict is labelled as not pre-registered
(same thresholds applied descriptively). summarise() is reused by bnd06_summary_families.py.
"""
import argparse
import csv
import json
import math
import re
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "external" / "causalarena" / "results" / "tables" / "main"
PUBLISHED_NAME = {"pc": "PC", "gesbic": "GIES", "lingam": "LiNGAM", "notears": "NOTEARS", "fci": None}
FAMILY_COLUMN = {"semantic": "Semantic obs-only", "formula": "Formula obs-only", "synthetic": "Synthetic obs-only"}
FAMILY_N_PUB = {"semantic": 100, "formula": 100, "synthetic": 1000}     # scenarios behind each published obs-only cell


def fam_mean(rows, rule, key="f1"):
    per = {}
    for r in rows:
        per.setdefault(r["scenario"], []).append(r["scores"][rule][key])
    vals = [st.mean(v) for v in per.values()]
    return st.mean(vals), st.pstdev(vals), len(vals)


def published(method, column="Semantic obs-only"):
    name = PUBLISHED_NAME.get(method)
    out = {}
    if not name:
        return out
    for metric, fn in (("f1", "main_leaderboard_f1_wide_with_std.csv"), ("shd", "main_leaderboard_shd_wide_with_std.csv")):
        for row in csv.DictReader(open(T / fn, encoding="utf-8-sig")):
            if (row.get("method") or row.get("Method")) == name:
                m = re.match(r"\s*([\d.]+)\s*\(([\d.]+)\)", row[column])
                if m:                                          # "--": no published value
                    out[metric] = (float(m.group(1)), float(m.group(2)))
    return out


def summarise(d, pre, family="semantic", tag=None, methods=None):
    """Q4c statistic and published comparison for one family. The default arguments are the pre-registered semantic run."""
    q4c_txt = pre["Q4c"]["text"]
    sup, ref = [float(x) for x in re.findall(r"(?:<=|>)\s*([\d.]+)", q4c_txt)[:2]]
    res = {"prereg": "plans/bnd06_prereg.json", "Q4c_text": q4c_txt, "methods": {}}
    deltas = {}
    methods = methods or pre["methods"]
    for m in methods:
        if family == "semantic" and tag is None:
            rel_f = d / (("%s_semantic_obs.json" % m) if m in ("gesbic", "fci") else "%s_semantic_obs_rel.json" % m)
            shuf_f = d / ("%s_semantic_obs_shuf.json" % m)
        else:
            t = tag or "%s_obs" % family
            rel_f, shuf_f = d / ("%s_%s_rel.json" % (m, t)), d / ("%s_%s_shuf.json" % (m, t))
        if not rel_f.exists() or not shuf_f.exists():
            res["methods"][m] = {"missing": [str(p.name) for p in (rel_f, shuf_f) if not p.exists()]}
            continue
        rel = json.loads(rel_f.read_text(encoding="utf-8"))["rows"]
        shuf = json.loads(shuf_f.read_text(encoding="utf-8"))["rows"]
        entry = {"files": [len(rel), len(shuf)],
                 "failed_files": [sum(1 for r in rel if r.get("failed")), sum(1 for r in shuf if r.get("failed"))]}
        for rule in ("random", "lower"):
            fr, _, n = fam_mean(rel, rule)
            fs, _, _ = fam_mean(shuf, rule)
            entry[rule] = {"f1_released": round(fr, 4), "f1_shuffled": round(fs, 4), "difference": round(fr - fs, 4), "scenarios": n}
        deltas[m] = abs(entry["random"]["difference"])
        pub = published(m, FAMILY_COLUMN[family])
        if pub:
            n_pub, n = FAMILY_N_PUB[family], entry["random"]["scenarios"]
            fpc = math.sqrt((n_pub - n) / (n_pub - 1))
            tol = {k: 3 * pub[k][1] / math.sqrt(n) * fpc for k in pub}
            f1l, _, _ = fam_mean(rel, "lower")
            shdl, _, _ = fam_mean(rel, "lower", "shd")
            entry["vs_published_authors_rule"] = {"published": pub, "tolerance_3se": {k: round(v, 4) for k, v in tol.items()},
                                                  "f1": round(f1l, 4), "f1_within": abs(f1l - pub["f1"][0]) <= tol["f1"],
                                                  "shd": round(shdl, 3), "shd_within": abs(shdl - pub["shd"][0]) <= tol["shd"]}
        res["methods"][m] = entry
    judged = {m: v for m, v in deltas.items()}
    if len(judged) == len(methods):
        verdict = "SUPPORTED" if all(v <= sup for v in judged.values()) else ("REFUTED" if any(v > ref for v in judged.values()) else "INCONCLUSIVE")
    else:
        verdict = "INCOMPLETE"
    res["Q4c"] = {"abs_difference_random_rule": judged, "verdict": verdict}
    if family != "semantic" or tag is not None:
        res["family"] = family
        res["Q4c"]["label"] = "not pre-registered; same thresholds applied descriptively"
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--family", default="semantic", choices=sorted(FAMILY_COLUMN))
    ap.add_argument("--tag", default=None, help="file stem between method and _rel/_shuf (default <family>_obs; semantic keeps its BND-04 names)")
    a = ap.parse_args()
    d = Path(a.dir)
    pre = json.loads((ROOT / "plans" / "bnd06_prereg.json").read_text(encoding="utf-8"))
    res = summarise(d, pre, a.family, a.tag)
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
