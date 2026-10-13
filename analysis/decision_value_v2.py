"""AB-04 decision-value scoreboard (AUD-36): DV-1 paired by file, replicate-agreement risk-coverage, DV-2 target choice, and
the usefulness threshold. Extends analysis/decision_value.py (AUD-30, unchanged; its helpers are imported).

  python analysis/decision_value_v2.py --root external/causalarena --out analysis/results/decision_value_v2

DV-1 (as AUD-30): for each intervention target T and every other variable Y, the learned graph claims "T moves Y" (Y reachable
by committed arrows), "T does not move Y" (unreachable even through undecided pairs), or abstains. Checked against the
true graph. Targets: the released intervention targets (semantic, formula; same as AUD-30) and, for the synthetic family
(no interventional release), every variable.
New here:
  paired      every baseline (empty graph = "nothing moves", true CPDAG, true DAG) is computed on exactly the files the
              method finished; "lift" = method precision minus the empty graph's on those files (closes the AUD-30 caveat)
  confidence  a claim's replicate agreement: the share of the scenario's 5 replicate files whose learned graph makes the same
              claim (independent samples of the same system; a stability measure, not a calibrated probability)
  risk-coverage  claims sorted by agreement; precision of the most-agreed share of claims at coverage 10%, 20%, ..., 100%
  DV-2        for each outcome Y truly moved by at least one target: pick a target uniformly among those the graph claims
              definitely move Y; success = it truly moves Y. Reported: answer rate, success when answering, and the random
              baseline (a target picked uniformly among all targets)
  threshold   stylised usefulness: acting on a "yes" claim gains g when right and costs c when wrong; acting beats doing
              nothing (the empty graph never acts) iff precision_yes > c/(g+c). For c/g in {0.25, 0.5, 1, 2, 4}: whether each
              method clears it, and its value per pair relative to doing nothing, (p_yes g - (1 - p_yes) c) x yes-rate, g = 1
No model calls. Tickets: AUD-36, TGT-15, TGT-16, EVL-03, CAP-15
"""
import argparse, json, os, re, statistics as st, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
import cc_graph as G  # noqa: E402
from causalarena_load import load_any  # noqa: E402
from decision_value import reach, targets_and_shifts  # noqa: E402

M = HERE / "results" / "methods"
METHODS = {  # label: {family: (released, shuffled)}; names without the .json suffix
    "PC, Causal-Copilot copy": {"semantic": ("pc_semantic_obs_rel", "pc_semantic_obs_shuf"), "formula": ("pc_formula_obs_rel", "pc_formula_obs_shuf"),
                                "synthetic": ("pc_synthetic100_rel", "pc_synthetic100_shuf")},
    "PC, upstream (default rule)": {f: ("pc_upstream_%s_obs_rel" % f, "pc_upstream_%s_obs_shuf" % f) for f in ("semantic", "formula", "synthetic")},
    "PC, upstream maxP": {f: ("pc_upstream_maxp_%s_obs_rel" % f, "pc_upstream_maxp_%s_obs_shuf" % f) for f in ("semantic", "formula", "synthetic")},
    "PC, upstream definite maxP": {f: ("pc_upstream_dmaxp_%s_obs_rel" % f, "pc_upstream_dmaxp_%s_obs_shuf" % f) for f in ("semantic", "formula", "synthetic")},
    "GES (BIC)": {"semantic": ("gesbic_semantic_obs", "gesbic_semantic_obs_shuf"), "formula": ("gesbic_formula_obs_rel", "gesbic_formula_obs_shuf"),
                  "synthetic": ("gesbic_synthetic100_rel", "gesbic_synthetic100_shuf")},
    "GIES with targets (D+I)": {f: ("gies_targets_%s_obsint_rel" % f, "gies_targets_%s_obsint_shuf" % f) for f in ("semantic", "formula")},
    "FCI (PAG; undecided as undirected)": {"semantic": ("fci_semantic_obs", "fci_semantic_obs_shuf"), "formula": ("fci_formula_obs_rel", "fci_formula_obs_shuf"),
                                           "synthetic": ("fci_synthetic100_rel", "fci_synthetic100_shuf")},
    "DirectLiNGAM": {f: ("lingam_%s_obs_rel" % f, "lingam_%s_obs_shuf" % f) for f in ("semantic", "formula")} | {"synthetic": ("lingam_synthetic100_rel", "lingam_synthetic100_shuf")},
    "NOTEARS": {f: ("notears_%s_obs_rel" % f, "notears_%s_obs_shuf" % f) for f in ("semantic", "formula")} | {"synthetic": ("notears_synthetic100_rel", "notears_synthetic100_shuf")},
}
COST_RATIOS = (0.25, 0.5, 1.0, 2.0, 4.0)
COVERAGES = tuple(round(0.1 * k, 1) for k in range(1, 11))


def obs_name(file):
    return file.replace("_obs_int__", "_obs_only__")


def scenario_key(file):
    return re.sub(r"__rep\d+\.npz$", "", obs_name(file))


class Truth:
    def __init__(self, root, fam):
        self.base = Path(root) / "scm" / fam / "data"
        self.fam = fam
        self.cache = {}

    def get(self, file):
        f = obs_name(file)
        if f not in self.cache:
            s = load_any(self.base / ("%s_obs_only" % self.fam) / f)
            T = CA.true_edges(s["g"])
            n = len(s["node_ids"])
            Cm = G.cpdag_of(T, n)
            cd, cu = set(), set()
            for x in range(n):
                for y in range(x + 1, n):
                    tp = G.pair_type(Cm, x, y)
                    if tp == "a->b":
                        cd.add((x, y))
                    elif tp == "b->a":
                        cd.add((y, x))
                    elif tp != "none":
                        cu.add((x, y))
            intfile = self.base / ("%s_obs_int" % self.fam) / f.replace("_obs_only__", "_obs_int__")
            targets = sorted(targets_and_shifts(intfile)) if intfile.exists() else list(range(n))
            self.cache[f] = {"n": n, "T": T, "cd": cd, "cu": cu, "desc": reach(n, T), "targets": targets,
                             "released_targets": intfile.exists()}
        return self.cache[f]


def claims(n, directed, undirected, targets):
    """{(t, y): True (moves) | False (does not move)} for committed claims; abstentions are absent."""
    definite = reach(n, directed)
    possible = reach(n, directed, undirected)
    out = {}
    for t in targets:
        for y in range(n):
            if y == t:
                continue
            if y in definite[t]:
                out[(t, y)] = True
            elif y not in possible[t]:
                out[(t, y)] = False
    return out


def precision_stats(per_file, truth_of):
    pairs = yes = yes_t = no = no_t = 0
    for f, (cl, npairs) in per_file.items():
        desc = truth_of(f)
        pairs += npairs
        for (t, y), v in cl.items():
            tr = y in desc[t]
            if v:
                yes += 1
                yes_t += tr
            else:
                no += 1
                no_t += not tr
    com = yes + no
    return {"files": len(per_file), "pairs": pairs, "coverage": round(com / pairs, 4) if pairs else None,
            "precision_committed": round((yes_t + no_t) / com, 4) if com else None,
            "precision_yes": round(yes_t / yes, 4) if yes else None, "precision_no": round(no_t / no, 4) if no else None,
            "yes_rate": round(yes / pairs, 4) if pairs else None}


def dv2(per_file, tr):
    answered = success = outcomes = 0
    rand = []
    for f, (cl, _) in per_file.items():
        I = tr.get(f)
        for y in range(I["n"]):
            movers = [t for t in I["targets"] if t != y and y in I["desc"][t]]
            if not movers:
                continue
            outcomes += 1
            cand = [t for t in I["targets"] if t != y]
            rand.append(len(movers) / len(cand))
            claimed = [t for t in cand if cl.get((t, y)) is True]
            if claimed:
                answered += 1
                success += sum(1 for t in claimed if y in I["desc"][t]) / len(claimed)
    return {"outcomes": outcomes, "answer_rate": round(answered / outcomes, 4) if outcomes else None,
            "success_when_answering": round(success / answered, 4) if answered else None,
            "random_target_success": round(st.mean(rand), 4) if rand else None}


def threshold(stats):
    p, yr = stats.get("precision_yes"), stats.get("yes_rate") or 0.0
    out = {}
    for r in COST_RATIOS:
        pstar = r / (1 + r)
        out[str(r)] = {"p_star": round(pstar, 4), "clears": (p is not None and p > pstar),
                       "value_per_pair_vs_nothing": round(((p or 0) - (1 - (p or 0)) * r) * yr, 4)}
    return out


def risk_coverage(per_file, agree, truth_of):
    items = []
    for f, (cl, _) in per_file.items():
        desc = truth_of(f)
        for (t, y), v in cl.items():
            items.append((agree[f].get((t, y), 0.0), (y in desc[t]) == v))
    if not items:
        return None
    items.sort(key=lambda x: -x[0])
    out = {}
    for c in COVERAGES:
        k = max(1, int(round(c * len(items))))
        out[str(c)] = round(sum(ok for _, ok in items[:k]) / k, 4)
    # area under the precision-coverage curve over the 10 points (higher is better)
    out["mean_over_coverages"] = round(st.mean(out[str(c)] for c in COVERAGES), 4)
    out["claims"] = len(items)
    return out


def load_rows(name):
    p = M / (name + ".json")
    if not p.exists():
        return None
    return [r for r in json.load(open(p))["rows"] if not r.get("failed")]


def analyse(rows, tr):
    per_file = {}
    for r in rows:
        I = tr.get(r["file"])
        dirs = {tuple(e) for e in r["directed_edges"]}
        und = {tuple(u[:2]) for u in r["undecided_pairs"]}
        per_file[obs_name(r["file"])] = (claims(I["n"], dirs, und, I["targets"]), len(I["targets"]) * (I["n"] - 1))
    by_scen = {}
    for f, (cl, _) in per_file.items():
        by_scen.setdefault(scenario_key(f), []).append(cl)
    agree = {}
    for f, (cl, _) in per_file.items():
        reps = by_scen[scenario_key(f)]
        agree[f] = {k: sum(1 for c in reps if c.get(k) == v) / len(reps) for k, v in cl.items()}
    return per_file, agree


def reference(files, tr, use):
    per_file = {}
    for f in files:
        I = tr.get(f)
        d, u = {"cpdag": (I["cd"], I["cu"]), "dag": (I["T"], set()), "empty": (set(), set())}[use]
        per_file[f] = (claims(I["n"], d, u, I["targets"]), len(I["targets"]) * (I["n"] - 1))
    return per_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent / "external" / "causalarena"))
    ap.add_argument("--families", nargs="+", default=["semantic", "formula", "synthetic"])
    ap.add_argument("--out", default=str(HERE / "results" / "decision_value_v2"))
    a = ap.parse_args()
    report = {"tickets": ["AUD-36", "TGT-15", "TGT-16", "EVL-03", "CAP-15"], "cost_ratios": COST_RATIOS, "families": {}}
    for fam in a.families:
        tr = Truth(a.root, fam)
        F = report["families"][fam] = {}
        for label, fams in METHODS.items():
            if fam not in fams:
                continue
            for arm, name in zip(("released", "shuffled"), fams[fam]):
                rows = load_rows(name)
                if not rows:
                    continue
                per_file, agree = analyse(rows, tr)
                truth_of = lambda f: tr.get(f)["desc"]
                files = sorted(per_file)
                m = precision_stats(per_file, truth_of)
                e = precision_stats(reference(files, tr, "empty"), truth_of)
                c = precision_stats(reference(files, tr, "cpdag"), truth_of)
                rec = {"source": name, **m, "paired_empty_graph_precision": e["precision_committed"],
                       "lift_over_empty_graph": round(m["precision_committed"] - e["precision_committed"], 4) if m["precision_committed"] is not None else None,
                       "paired_cpdag_precision": c["precision_committed"], "paired_cpdag_coverage": c["coverage"],
                       "gap_to_cpdag_ceiling": round(c["precision_committed"] - m["precision_committed"], 4) if m["precision_committed"] is not None else None,
                       "dv2": dv2(per_file, tr), "dv2_cpdag": dv2(reference(files, tr, "cpdag"), tr),
                       "risk_coverage_replicate_agreement": risk_coverage(per_file, agree, truth_of),
                       "threshold": threshold(m), "targets": "released interventions" if tr.get(files[0])["released_targets"] else "every variable"}
                F.setdefault(label, {})[arm] = rec
                print("%-9s %-36s %-8s files %3d cov %.3f prec %.3f | empty %.3f lift %+.3f | cpdag %.3f | DV2 %s/%s rand %s | RC@0.5 %s" % (
                    fam, label, arm, m["files"], m["coverage"], m["precision_committed"], e["precision_committed"], rec["lift_over_empty_graph"],
                    c["precision_committed"], rec["dv2"]["answer_rate"], rec["dv2"]["success_when_answering"], rec["dv2"]["random_target_success"],
                    (rec["risk_coverage_replicate_agreement"] or {}).get("0.5")), flush=True)
        allfiles = sorted(os.listdir(tr.base / ("%s_obs_only" % fam)))
        truth_of = lambda f: tr.get(f)["desc"]
        for label, use in (("ceiling: true CPDAG", "cpdag"), ("ceiling: true DAG", "dag"), ("baseline: empty graph (nothing moves)", "empty")):
            pf = reference(allfiles, tr, use)
            F[label] = {"reference": {**precision_stats(pf, truth_of), "dv2": dv2(pf, tr), "threshold": threshold(precision_stats(pf, truth_of))}}
    # P6 / P7 verdicts per family (released arm; methods with a row)
    # P6 is worded over "reproduced methods": rows that reproduce a published scoreboard method (PC, GES/GIES, GIES with
    # targets, LiNGAM, NOTEARS). FCI (not on the board) and our PC variants (maxP, definite maxP) are reported alongside.
    REPRODUCED = {"PC, Causal-Copilot copy", "PC, upstream (default rule)", "GES (BIC)", "GIES with targets (D+I)", "DirectLiNGAM", "NOTEARS"}
    p6 = lambda k: "supported" if k <= 2 else ("refuted" if k >= 4 else "inconclusive")
    ver = {}
    for fam, F in report["families"].items():
        lifts = {lab: v["released"]["lift_over_empty_graph"] for lab, v in F.items() if "released" in v}
        gaps = {lab: v["released"]["gap_to_cpdag_ceiling"] for lab, v in F.items() if "released" in v}
        beat = [lab for lab, x in lifts.items() if x is not None and x > 0.05]
        beat_rep = [lab for lab in beat if lab in REPRODUCED]
        rep_gaps = [g for lab, g in gaps.items() if g is not None and lab in REPRODUCED]
        best_gap = min(rep_gaps, default=None)
        ver[fam] = {"reproduced_methods": sorted(l for l in lifts if l in REPRODUCED), "beat_empty_by_more_than_0.05": beat_rep,
                    "P6": p6(len(beat_rep)),
                    "all_methods_incl_variants_beating_empty": beat, "P6_if_variants_counted": p6(len(beat)),
                    "smallest_gap_to_cpdag_reproduced": best_gap,
                    "P7": None if best_gap is None else ("supported" if best_gap >= 0.15 else ("refuted" if best_gap < 0.05 else "inconclusive")),
                    "smallest_gap_to_cpdag_all": min((g for g in gaps.values() if g is not None), default=None)}
    report["verdicts"] = ver
    print(json.dumps(ver, indent=1))
    os.makedirs(a.out, exist_ok=True)
    json.dump(report, open(os.path.join(a.out, "decision_value_v2.json"), "w"), indent=1)
    json.dump({"producer": "analysis/decision_value_v2.py", "score_bearing": True, "tickets": report["tickets"],
               "regime": "per-row", "regime_detail": "D for observational methods; D+I for GIES with targets",
               "split": "all-public (measurement, no tuning)",
               "controls": {"columns_shuffled": "both arms", "names": "not applicable", "supplier": "causalarena"},
               "orientation_rule": "none: undecided reachability is an abstention",
               "metric_defs": {"coverage": "share of (target, variable) pairs given a committed claim",
                               "precision_committed": "share of committed claims that match the true graph",
                               "lift_over_empty_graph": "precision minus the empty graph's precision on the same files",
                               "risk_coverage_replicate_agreement": "precision of the claims with the highest replicate agreement, by coverage",
                               "dv2": "target choice for a named outcome: answer rate, success when answering, random baseline",
                               "threshold": "stylised act/do-nothing comparison at cost ratio c/g"}},
              open(os.path.join(a.out, "CONTRACT.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
