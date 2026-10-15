"""B1 numbers: dev selection (rung R4) and the held-out read (gates B1.1-B1.3, landmark ER-F, route A of ER-4a).

  python -m kernel.report_b1 select           -> analysis/results/q2_b1/dev_selection.json
  python -m kernel.report_b1 heldout          -> analysis/results/q2_b1/heldout.json

Comparators are the audit chapter's stored per-file rows on shuffled columns (analysis/results/methods):
plain causal-learn PC maxP (pc_upstream_maxp_<family>_obs_shuf) and GES (gesbic_<family>_obs_shuf), paired by file;
files on which a comparator failed are excluded from that comparison (AB-01's rule). Intervals: scenario-cluster bootstrap
(score.paired), B = 2000.
"""
import json, statistics as st, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
RES = ROOT / "analysis" / "results" / "q2_b1"
RULE_ORDER = ("pc", "C3", "C2", "C1", "ges")
BASE = {"pc_maxp": "pc_upstream_maxp_%s_obs_shuf", "ges": {"semantic": "gesbic_semantic_obs_shuf", "formula": "gesbic_formula_obs_shuf"}}


def load(split, fam):
    return [json.loads(l) for l in open(RES / ("%s_%s.jsonl" % (split, fam))) if l.strip()]


def baseline_rows(fam, which):
    from score import bench, dv, graph
    name = BASE["pc_maxp"] % fam if which == "pc_maxp" else BASE["ges"][fam]
    out = {}
    for f, r in bench.method_rows(name).items():
        if r.get("failed"):
            continue
        I = bench.truth_info(fam, f)
        D, U = bench.row_graph(r)
        checked = dv.check(dv.claims(I["n"], D, U, I["targets"]), I["desc"])
        out[f] = {"f1": graph.directed_f1(D, U, I["T"], graph.file_seed(f))["f1"],
                  "dv1": {"committed": len(checked), "correct": sum(ok for *_, ok in checked), "pairs": dv.n_pairs(I["n"], I["targets"])}}
    return out


def summarize(rows, rule, files=None):
    rs = [r for r in rows if "rules" in r and rule in r["rules"] and (files is None or r["file"] in files)]
    f1 = [r["rules"][rule]["f1"] for r in rs]
    com = sum(r["rules"][rule]["dv1"]["yes"] + r["rules"][rule]["dv1"]["no"] for r in rs)
    cor = sum(r["rules"][rule]["dv1"]["yes_ok"] + r["rules"][rule]["dv1"]["no_ok"] for r in rs)
    pairs = sum(r["rules"][rule]["dv1"]["pairs"] for r in rs)
    return {"files": len(rs), "f1": st.mean(f1) if f1 else None, "dv1_precision": cor / com if com else None,
            "dv1_coverage": com / pairs if pairs else None}


def base_summary(base, files):
    xs = [base[f] for f in files if f in base]
    com = sum(x["dv1"]["committed"] for x in xs)
    return {"files": len(xs), "f1": st.mean(x["f1"] for x in xs) if xs else None,
            "dv1_precision": sum(x["dv1"]["correct"] for x in xs) / com if com else None,
            "dv1_coverage": com / sum(x["dv1"]["pairs"] for x in xs) if xs else None}


def checks(rows):
    out = {"files": len(rows), "pc_failed": sum(1 for r in rows if not r.get("pc_ok")), "jittered": sum(1 for r in rows if r.get("jittered")),
           "ges_failed": sum(1 for r in rows if not r.get("ges_ok")), "r1_equal": sum(1 for r in rows if r.get("r1_equal_reference") is True),
           "r1_not_equal": sum(1 for r in rows if r.get("r1_equal_reference") is False),
           "files_with_set_aside_pairs": sum(1 for r in rows if r.get("r1_exact_without_defect_fix") is False),
           "pairs_set_aside": sum(r.get("r1_pairs_set_aside", 0) for r in rows),
           "pc_defect_types": {t: sum(r.get("pc_defects", {}).get(t, 0) for r in rows) for t in ("engine_meek_divergence", "pc_directed_cycle")},
           "rule_cycles": {rule: sum(1 for r in rows if r.get("rules", {}).get(rule, {}).get("rule_cycles")) for rule in RULE_ORDER}}
    bad = [(r["file"], k) for r in rows for k, v in r.get("rules", {}).items() if v["verify_failures"] or not v["checker_ok"]]
    out["ledgers_failing_verify_or_checker"] = len(bad)
    out["examples"] = bad[:5]
    out["ledgers"] = sum(len(r.get("rules", {})) for r in rows)
    return out


def select():
    out = {"tickets": ["BLD-02", "TGT-19"], "rule_text": json.load(open(ROOT / "plans" / "b1_prereg.json"))["selection_rule"], "families": {}}
    for fam in ("semantic", "formula"):
        rows = load("dev", fam)
        files = {r["file"] for r in rows if "rules" in r}
        pcb = baseline_rows(fam, "pc_maxp")
        gesb = baseline_rows(fam, "ges")
        paired = sorted(files & set(pcb))
        fam_out = {"checks": checks(rows), "rules_all_files": {}, "rules_paired_with_pc_maxp": {}}
        for rule in RULE_ORDER:
            fam_out["rules_all_files"][rule] = summarize(rows, rule)
            fam_out["rules_paired_with_pc_maxp"][rule] = summarize(rows, rule, set(paired))
        fam_out["pc_maxp_baseline_paired"] = base_summary(pcb, paired)
        pg = sorted(files & set(gesb))
        fam_out["ges_baseline_paired"] = base_summary(gesb, pg)
        fam_out["rules_paired_with_ges"] = {rule: summarize(rows, rule, set(pg)) for rule in RULE_ORDER}
        out["families"][fam] = fam_out
    # the selection rule
    best = {fam: max(out["families"][fam]["rules_all_files"][r]["f1"] for r in RULE_ORDER) for fam in out["families"]}
    elig = []
    for rule in RULE_ORDER:
        ok = True
        for fam, v in out["families"].items():
            a, p, b = v["rules_all_files"][rule], v["rules_paired_with_pc_maxp"][rule], v["pc_maxp_baseline_paired"]
            ok &= a["f1"] >= best[fam] - 0.01
            ok &= p["f1"] >= b["f1"] - 0.01 and p["dv1_precision"] >= b["dv1_precision"] - 0.01
        if ok:
            elig.append(rule)
    score = {r: st.mean(out["families"][f]["rules_all_files"][r]["dv1_precision"] for f in out["families"]) for r in elig}
    chosen = max(elig, key=lambda r: (score[r], -RULE_ORDER.index(r))) if elig else "pc"
    out["best_f1"] = best
    out["eligible"] = elig
    out["eligible_dv1_mean"] = score
    out["chosen"] = chosen
    out["Q-B1b"] = {f: {"C2_minus_ges": out["families"][f]["rules_paired_with_ges"]["C2"]["f1"] - out["families"][f]["ges_baseline_paired"]["f1"],
                        "C3_minus_ges": out["families"][f]["rules_paired_with_ges"]["C3"]["f1"] - out["families"][f]["ges_baseline_paired"]["f1"]}
                    for f in out["families"]}
    out["Q-B1b"]["verdict"] = "supported" if max(out["Q-B1b"]["semantic"].values()) >= 0.01 else "refuted"
    json.dump(out, open(RES / "dev_selection.json", "w"), indent=1)
    for fam, v in out["families"].items():
        print(fam, v["checks"])
        print("  baseline PC maxP (paired)", {k: round(x, 4) if isinstance(x, float) else x for k, x in v["pc_maxp_baseline_paired"].items()})
        print("  baseline GES (paired)    ", {k: round(x, 4) if isinstance(x, float) else x for k, x in v["ges_baseline_paired"].items()})
        for rule in RULE_ORDER:
            print("  %-4s all %s | paired-pc %s" % (rule, {k: round(x, 4) if isinstance(x, float) else x for k, x in v["rules_all_files"][rule].items()},
                                                   {k: round(x, 4) if isinstance(x, float) else x for k, x in v["rules_paired_with_pc_maxp"][rule].items()}))
    print("eligible", elig, "chosen", chosen, "Q-B1b", out["Q-B1b"]["verdict"])


def heldout():
    from score import bench, paired
    fz = json.load(open(ROOT / "plans" / "b1_freeze.json"))
    rule = fz["rule"]
    out = {"tickets": ["BLD-02", "CAP-05", "CAP-09", "CAP-11", "TGT-10", "TGT-19"], "rule": rule, "freeze": fz["id"], "families": {}}
    for fam in ("semantic", "formula"):
        rows = load("test", fam)
        byfile = {r["file"]: r for r in rows if "rules" in r}
        fo = {"checks": checks(rows)}
        for which in ("pc_maxp", "ges"):
            base = baseline_rows(fam, which)
            common = sorted(set(byfile) & set(base))
            f1_k = {f: byfile[f]["rules"][rule]["f1"] for f in common}
            f1_b = {f: base[f]["f1"] for f in common}
            d_f1 = paired.paired_diff(f1_k, f1_b, bench.scenario_of)
            per_s = {}
            for f in common:
                k, b = byfile[f]["rules"][rule]["dv1"], base[f]["dv1"]
                per_s.setdefault(bench.scenario_of(f), []).append((k["yes_ok"] + k["no_ok"], k["yes"] + k["no"], b["correct"], b["committed"]))

            def stat(gs):
                ck = sum(x[0] for g in gs for x in g)
                nk = sum(x[1] for g in gs for x in g)
                cb = sum(x[2] for g in gs for x in g)
                nb = sum(x[3] for g in gs for x in g)
                return (ck / nk if nk else 0) - (cb / nb if nb else 0)
            d_dv = paired.cluster_bootstrap(per_s, stat=stat)
            mean_file_dv = st.mean([(byfile[f]["rules"][rule]["dv1"]["yes_ok"] + byfile[f]["rules"][rule]["dv1"]["no_ok"]) /
                                    max(1, byfile[f]["rules"][rule]["dv1"]["yes"] + byfile[f]["rules"][rule]["dv1"]["no"]) -
                                    base[f]["dv1"]["correct"] / max(1, base[f]["dv1"]["committed"]) for f in common])
            fo["vs_" + which] = {"files": len(common), "kernel": summarize(rows, rule, set(common)), "baseline": base_summary(base, common),
                                 "f1_diff": d_f1, "dv1_pooled_diff": d_dv, "dv1_mean_per_file_diff": mean_file_dv}
        fo["kernel_all_files"] = summarize(rows, rule)
        fo["pc_rule_all_files"] = summarize(rows, "pc")
        v = fo["vs_pc_maxp"]
        fo["B1.2"] = {"f1_mean_diff": v["f1_diff"]["point"], "dv1_pooled_diff": v["dv1_pooled_diff"]["point"],
                      "pass": v["f1_diff"]["point"] >= -0.01 and v["dv1_pooled_diff"]["point"] >= -0.01,
                      "refuted": v["f1_diff"]["point"] <= -0.05 or v["dv1_pooled_diff"]["point"] <= -0.05}
        fo["ER-F"] = {"f1_lower": v["f1_diff"]["lo"], "dv1_lower": v["dv1_pooled_diff"]["lo"],
                      "met": v["f1_diff"]["lo"] >= -0.01 and v["dv1_pooled_diff"]["lo"] >= -0.01}
        g = fo["vs_ges"]
        fo["ER-4a_route_A"] = {"f1_minus_ges": g["f1_diff"]["point"], "lower": g["f1_diff"]["lo"], "met": g["f1_diff"]["lo"] > 0}
        out["families"][fam] = fo
    out["B1.2_pass"] = all(v["B1.2"]["pass"] for v in out["families"].values())
    out["ER-F_met"] = all(v["ER-F"]["met"] for v in out["families"].values())
    out["ER-4a_route_A_met"] = any(v["ER-4a_route_A"]["met"] for v in out["families"].values())
    json.dump(out, open(RES / "heldout.json", "w"), indent=1)
    for fam, v in out["families"].items():
        print(fam, v["checks"])
        print("  vs PC maxP: F1 %+.4f [%+.4f, %+.4f]  DV-1 %+.4f [%+.4f, %+.4f]  files %d" % (
            v["vs_pc_maxp"]["f1_diff"]["point"], v["vs_pc_maxp"]["f1_diff"]["lo"], v["vs_pc_maxp"]["f1_diff"]["hi"],
            v["vs_pc_maxp"]["dv1_pooled_diff"]["point"], v["vs_pc_maxp"]["dv1_pooled_diff"]["lo"], v["vs_pc_maxp"]["dv1_pooled_diff"]["hi"], v["vs_pc_maxp"]["files"]))
        print("  vs GES:     F1 %+.4f [%+.4f, %+.4f]  DV-1 %+.4f [%+.4f, %+.4f]  files %d" % (
            v["vs_ges"]["f1_diff"]["point"], v["vs_ges"]["f1_diff"]["lo"], v["vs_ges"]["f1_diff"]["hi"],
            v["vs_ges"]["dv1_pooled_diff"]["point"], v["vs_ges"]["dv1_pooled_diff"]["lo"], v["vs_ges"]["dv1_pooled_diff"]["hi"], v["vs_ges"]["files"]))
        print("  kernel all files", v["kernel_all_files"])
    print("B1.2 pass", out["B1.2_pass"], "ER-F met", out["ER-F_met"], "ER-4a route A met", out["ER-4a_route_A_met"])


if __name__ == "__main__":
    {"select": select, "heldout": heldout}[sys.argv[1]]()
