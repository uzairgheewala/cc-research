"""BND-06 extension: order sensitivity (Q4c statistic) and published-row comparison on the formula family (250 public obs-only
files) and the 100-file synthetic sample (plans/synth_sample_100.txt). Writes analysis/results/methods/bnd06_families.json.

  python analysis/bnd06_summary_families.py --dir analysis/results/methods --out analysis/results/methods/bnd06_families.json

Inputs: <method>_formula_obs_{rel,shuf}.json and <method>_synthetic100_{rel,shuf}.json (causalarena_methods.py outputs).
Reuses bnd06_summary.summarise (same family mean, same published parsing, same 3-SE finite-population-corrected tolerance)
and adds, per method x family:
  |difference| under the random rule (order-free) and under the authors' rule "lower" (reads the order the method saw)
  failed files split into timeouts (TimeoutError from --file-timeout-s) and other failures, with the distinct failure messages
  the published comparison under both rules (bnd06_summary reports the authors' rule only; the random rule is the rule the
  C1 gate used for PC)
Q4c was pre-registered on the semantic family only (plans/bnd06_prereg.json). Here the same thresholds are applied
descriptively and every verdict is labelled "not pre-registered; same thresholds applied descriptively".
Synthetic caveat: the published synthetic obs-only cell averages 1000 scenarios x 5 replicates; the public sample has one
replicate (rep000) of 100 scenarios, so a per-scenario value here carries replicate noise that the published scm_std does not.
"""
import argparse
import collections
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bnd06_summary as B  # noqa: E402

FAMILIES = {"formula": {"family": "formula", "tag": "formula_obs", "files": 250},
            "synthetic100": {"family": "synthetic", "tag": "synthetic100", "files": 100}}
LABEL = "not pre-registered; same thresholds applied descriptively"


def failures(rows):
    out = {"timeout": 0, "other": 0, "messages": collections.Counter()}
    for r in rows:
        f = r.get("failed")
        if not f:
            continue
        out["timeout" if f.startswith("TimeoutError") else "other"] += 1
        out["messages"][re.sub(r"\d+", "#", f)[:120]] += 1
    out["messages"] = dict(out["messages"].most_common())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = Path(a.dir)
    pre = json.loads((B.ROOT / "plans" / "bnd06_prereg.json").read_text(encoding="utf-8"))
    sup, ref = [float(x) for x in re.findall(r"(?:<=|>)\s*([\d.]+)", pre["Q4c"]["text"])[:2]]
    res = {"prereg": "plans/bnd06_prereg.json", "Q4c_text": pre["Q4c"]["text"], "label": LABEL,
           "shuffle": pre["shuffle"], "families": {}}
    for key, F in FAMILIES.items():
        base = B.summarise(d, pre, F["family"], F["tag"])
        fam = {"family": F["family"], "files_expected": F["files"], "published_column": B.FAMILY_COLUMN[F["family"]],
               "published_population_scenarios": B.FAMILY_N_PUB[F["family"]], "methods": {}}
        for m, e in base["methods"].items():
            if "missing" in e:
                fam["methods"][m] = e
                continue
            rel = json.loads((d / ("%s_%s_rel.json" % (m, F["tag"]))).read_text(encoding="utf-8"))
            shuf = json.loads((d / ("%s_%s_shuf.json" % (m, F["tag"]))).read_text(encoding="utf-8"))
            ent = {"files": e["files"], "failed_files": e["failed_files"],
                   "failures_released": failures(rel["rows"]), "failures_shuffled": failures(shuf["rows"]),
                   "file_timeout_s": [rel["header"].get("file_timeout_s"), shuf["header"].get("file_timeout_s")],
                   "sum_file_seconds": [round(sum(r["metrics"]["seconds"] for r in rel["rows"]), 1),
                                        round(sum(r["metrics"]["seconds"] for r in shuf["rows"]), 1)],
                   "env": rel["header"].get("env")}
            for rule in ("random", "lower"):
                ent[rule] = dict(e[rule], abs_difference=round(abs(e[rule]["difference"]), 4))
            pub = B.published(m, B.FAMILY_COLUMN[F["family"]])
            if pub:
                n_pub, n = B.FAMILY_N_PUB[F["family"]], e["random"]["scenarios"]
                fpc = math.sqrt((n_pub - n) / (n_pub - 1))
                tol = {k: 3 * pub[k][1] / math.sqrt(n) * fpc for k in pub}
                vp = {"published_name": B.PUBLISHED_NAME[m], "published": pub, "scenarios_ours": n, "scenarios_published": n_pub,
                      "tolerance_3se": {k: round(v, 4) for k, v in tol.items()}}
                for rule in ("lower", "random"):
                    f1, _, _ = B.fam_mean(rel["rows"], rule)
                    shd, _, _ = B.fam_mean(rel["rows"], rule, "shd")
                    vp[rule] = {"f1": round(f1, 4), "f1_gap": round(f1 - pub["f1"][0], 4), "f1_within": abs(f1 - pub["f1"][0]) <= tol["f1"],
                                "shd": round(shd, 3), "shd_gap": round(shd - pub["shd"][0], 3), "shd_within": abs(shd - pub["shd"][0]) <= tol["shd"]}
                ent["vs_published"] = vp
            else:
                ent["vs_published"] = None
            fam["methods"][m] = ent
        judged = {m: v["random"]["abs_difference"] for m, v in fam["methods"].items() if "random" in v}
        if len(judged) == len(pre["methods"]):
            verdict = ("SUPPORTED" if all(v <= sup for v in judged.values())
                       else "REFUTED" if any(v > ref for v in judged.values()) else "INCONCLUSIVE")
        else:
            verdict = "INCOMPLETE"
        fam["Q4c_extension"] = {"label": LABEL, "abs_difference_random_rule": judged,
                                "methods_over_0.05": sorted(m for m, v in judged.items() if v > ref),
                                "methods_within_0.02": sorted(m for m, v in judged.items() if v <= sup), "verdict": verdict}
        res["families"][key] = fam
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    for key, fam in res["families"].items():
        print(key, json.dumps(fam["Q4c_extension"]))
        for m, e in fam["methods"].items():
            if "random" not in e:
                print("  %-8s missing %s" % (m, e.get("missing")))
                continue
            vp = e["vs_published"]
            print("  %-8s rand %.3f/%.3f d=%+.3f  lower %.3f/%.3f d=%+.3f  failed %s  pub %s" % (
                m, e["random"]["f1_released"], e["random"]["f1_shuffled"], e["random"]["difference"],
                e["lower"]["f1_released"], e["lower"]["f1_shuffled"], e["lower"]["difference"], e["failed_files"],
                None if not vp else (vp["published"]["f1"][0], vp["lower"]["f1"], vp["lower"]["f1_within"], vp["random"]["f1"], vp["random"]["f1_within"])))


if __name__ == "__main__":
    main()
