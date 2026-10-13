"""Decision value of a learned graph: does it say correctly what an intervention will move? (DV-1, plus AID)

For every scenario, the graph a method learned from an observational file is asked, for each released intervention
target T (from the matching obs+int file) and every other variable Y: "will setting T move Y?"
  - definite yes : Y is reachable from T by committed arrows                       (a claim)
  - no           : Y is not reachable from T even treating undecided pairs as two-way (a claim)
  - possible     : reachable only through undecided pairs                           (abstain, or forced "yes")
Claims are checked against the true graph (descendant of T) and, separately, against the held-out interventional rows
(Welch t-test of Y on rows where only T was set vs the observational rows of the same file, alpha 0.01; noisy:
BEN-09 found many released interventions move nothing detectable).
Reported: precision and coverage of committed claims (abstaining on "possible"), the forced view (possible = yes), and
the adjustment identification distances of Henckel et al. (gadjid: ancestor, O-set, parent AID; normalised, lower is
better) between the true DAG and the learned graph (committed arrows = 1, undecided pairs = undirected).
Ceilings: the true CPDAG (what observational data can identify) and the true DAG.

  python analysis/decision_value.py --root external/causalarena --families semantic formula --out analysis/results/decision_value
Needs gadjid (pip install gadjid; MIT/Apache) for AID; without it AID is skipped. No model calls.
Tickets: AUD-30, AUD-24, EVL-03, TGT-15
"""
import argparse, json, os, statistics as st, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
import cc_graph as G  # noqa: E402

M = HERE / "results" / "methods"
METHODS = {  # label: {family: {arm: result file}}
    "PC (upstream causal-learn)": ("pc_upstream_{f}_obs_rel", "pc_upstream_{f}_obs_shuf"),
    "PC (Causal-Copilot copy)": ("pc_{f}_obs_rel", "pc_{f}_obs_shuf"),
    "GES (BIC)": ({"semantic": "gesbic_semantic_obs"}, "gesbic_{f}_obs_shuf"),
    "FCI (PAG; undecided marks as undirected)": ({"semantic": "fci_semantic_obs"}, "fci_{f}_obs_shuf"),
    "DirectLiNGAM": ("lingam_{f}_obs_rel", "lingam_{f}_obs_shuf"),
    "NOTEARS": ("notears_{f}_obs_rel", "notears_{f}_obs_shuf"),
}


def name_for(spec, fam, default_suffix="_obs_rel"):
    if isinstance(spec, dict):
        return spec.get(fam, "%s%s" % (list(spec.values())[0].split("_")[0] + "_" + fam, default_suffix))
    return spec.format(f=fam)


def reach(n, directed, undirected=()):
    out = {i: set() for i in range(n)}
    nxt = {i: set() for i in range(n)}
    for a, b in directed:
        nxt[a].add(b)
    for a, b in undirected:
        nxt[a].add(b)
        nxt[b].add(a)
    for s in range(n):
        stack, seen = [s], set()
        while stack:
            u = stack.pop()
            for v in nxt[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        out[s] = seen - {s}
    return out


def targets_and_shifts(path, alpha=0.01):
    s = CA.load(path)
    X, I, n_obs = s["values"], s["intervened"], s["n_obs"]
    obs = X[:n_obs]
    res = {}
    for t in range(X.shape[1]):
        rows = np.where(I[:, t] & (I.sum(1) == 1))[0]
        if len(rows) < 5:
            continue
        shifts = set()
        for y in range(X.shape[1]):
            if y == t:
                continue
            a, b = X[rows, y], obs[:, y]
            va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
            if va + vb <= 0:
                continue
            tstat = abs(a.mean() - b.mean()) / np.sqrt(va + vb)
            # two-sided normal approximation (rows >= 5 per target; Welch df is large for the observational side)
            from math import erfc, sqrt
            if erfc(tstat / sqrt(2)) < alpha:
                shifts.add(y)
        res[t] = shifts
    return res


def claim_scores(n, est_dir, est_und, true_desc, data_shift):
    definite = reach(n, est_dir)
    possible = reach(n, est_dir, est_und)
    c = {"pairs": 0, "yes": 0, "yes_true": 0, "no": 0, "no_true": 0, "abstain": 0, "abstain_true_yes": 0,
         "yes_data": 0, "no_data": 0}
    for t, dshift in data_shift.items():
        for y in range(n):
            if y == t:
                continue
            c["pairs"] += 1
            truth = y in true_desc[t]
            if y in definite[t]:
                c["yes"] += 1
                c["yes_true"] += truth
                c["yes_data"] += y in dshift
            elif y not in possible[t]:
                c["no"] += 1
                c["no_true"] += not truth
                c["no_data"] += y not in dshift
            else:
                c["abstain"] += 1
                c["abstain_true_yes"] += truth
    return c


def to_matrix(n, directed, undirected):
    A = np.zeros((n, n), dtype=np.int8)
    for a, b in directed:
        A[a, b] = 1
    for a, b in undirected:
        A[a, b] = A[b, a] = 2
    return A


def aid(Tm, Gm):
    try:
        import gadjid
    except ImportError:
        return None
    kw = {"edge_direction": "from row to column"}
    try:
        return {"ancestor_aid": gadjid.ancestor_aid(Tm, Gm, **kw)[0], "oset_aid": gadjid.oset_aid(Tm, Gm, **kw)[0],
                "parent_aid": gadjid.parent_aid(Tm, Gm, **kw)[0]}
    except BaseException:  # gadjid refuses graphs with directed cycles or invalid mixed edges (panics surface as BaseException)
        return {"invalid": True}


def summarise(cs, aids):
    tot = {k: sum(c[k] for c in cs) for k in cs[0]}
    committed = tot["yes"] + tot["no"]
    out = {"pairs": tot["pairs"], "coverage": round(committed / tot["pairs"], 4) if tot["pairs"] else None,
           "precision_committed": round((tot["yes_true"] + tot["no_true"]) / committed, 4) if committed else None,
           "precision_yes": round(tot["yes_true"] / tot["yes"], 4) if tot["yes"] else None,
           "precision_no": round(tot["no_true"] / tot["no"], 4) if tot["no"] else None,
           "forced_precision": round((tot["yes_true"] + tot["no_true"] + tot["abstain_true_yes"]) / tot["pairs"], 4) if tot["pairs"] else None,
           "abstain_share_truly_moved": round(tot["abstain_true_yes"] / tot["abstain"], 4) if tot["abstain"] else None,
           "share_of_pairs_truly_moved": round(sum(c["yes_true"] + (c["no"] - c["no_true"]) + c["abstain_true_yes"] for c in cs) / tot["pairs"], 4) if tot["pairs"] else None,
           "agreement_with_data_committed": round((tot["yes_data"] + tot["no_data"]) / committed, 4) if committed else None}
    for k in ("ancestor_aid", "oset_aid", "parent_aid"):
        vals = [x[k] for x in aids if x and not x.get("invalid")]
        out[k] = round(st.mean(vals), 4) if vals else None
    out["aid_graphs_refused"] = sum(1 for x in aids if x and x.get("invalid"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent / "external" / "causalarena"))
    ap.add_argument("--families", nargs="+", default=["semantic", "formula"])
    ap.add_argument("--out", default=str(HERE / "results" / "decision_value"))
    a = ap.parse_args()
    report = {"tickets": ["AUD-30", "AUD-24", "EVL-03", "TGT-15"], "families": {}}
    for fam in a.families:
        base = Path(a.root) / "scm" / fam / "data"
        cache = {}

        def info(file):
            if file not in cache:
                s = CA.load(base / ("%s_obs_only" % fam) / file)
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
                intfile = base / ("%s_obs_int" % fam) / file.replace("_obs_only__", "_obs_int__")
                cache[file] = {"n": n, "T": T, "cd": cd, "cu": cu, "desc": reach(n, T),
                               "shift": targets_and_shifts(intfile) if intfile.exists() else {}}
            return cache[file]

        fam_out = {}
        files_any = None
        for label, (rel, shuf) in METHODS.items():
            for arm, spec in (("released", rel), ("shuffled", shuf)):
                p = M / (name_for(spec, fam) + ".json")
                if not p.exists():
                    continue
                rows = [r for r in json.load(open(p))["rows"] if not r.get("failed")]
                cs, aids = [], []
                for r in rows:
                    I = info(r["file"])
                    if not I["shift"]:
                        continue
                    dirs = {tuple(e) for e in r["directed_edges"]}
                    und = {tuple(u[:2]) for u in r["undecided_pairs"]}
                    cs.append(claim_scores(I["n"], dirs, und, I["desc"], I["shift"]))
                    aids.append(aid(to_matrix(I["n"], I["T"], ()), to_matrix(I["n"], dirs, und)))
                if cs:
                    fam_out.setdefault(label, {})[arm] = {"files": len(cs), **summarise(cs, aids)}
                    files_any = files_any or [r["file"] for r in rows]
        # ceilings over every file that has interventions
        allfiles = sorted(os.listdir(base / ("%s_obs_only" % fam)))
        for label, use in (("ceiling: true CPDAG", "cpdag"), ("ceiling: true DAG", "dag"), ("baseline: empty graph (nothing moves)", "empty")):
            cs, aids = [], []
            for f in allfiles:
                I = info(f)
                if not I["shift"]:
                    continue
                d, u = {"cpdag": (I["cd"], I["cu"]), "dag": (I["T"], set()), "empty": (set(), set())}[use]
                cs.append(claim_scores(I["n"], d, u, I["desc"], I["shift"]))
                aids.append(aid(to_matrix(I["n"], I["T"], ()), to_matrix(I["n"], d, u)))
            fam_out[label] = {"reference": {"files": len(cs), **summarise(cs, aids)}}
        report["families"][fam] = fam_out
        for label, arms in fam_out.items():
            for arm, v in arms.items():
                print("%-8s %-44s %-9s cov %s prec %s (yes %s, no %s) forced %s data-agree %s ancAID %s osetAID %s" % (
                    fam, label, arm, v["coverage"], v["precision_committed"], v["precision_yes"], v["precision_no"],
                    v["forced_precision"], v["agreement_with_data_committed"], v["ancestor_aid"], v["oset_aid"]))
    os.makedirs(a.out, exist_ok=True)
    json.dump(report, open(os.path.join(a.out, "decision_value.json"), "w"), indent=1)
    json.dump({"producer": "analysis/decision_value.py", "score_bearing": True, "tickets": report["tickets"], "regime": "D",
               "split": "all-public (measurement, no tuning)", "split_detail": "public half", "controls": {"columns_shuffled": "both arms", "names": "not applicable", "supplier": "causalarena"},
               "orientation_rule": "no orientation rule: undecided pairs are abstentions (or 'yes' in the forced view)",
               "metric_defs": {"coverage": "share of (target, variable) pairs given a committed claim",
                               "precision_committed": "share of committed claims that match the true graph",
                               "forced_precision": "accuracy when undecided reachability counts as yes",
                               "share_of_pairs_truly_moved": round(sum(c["yes_true"] + (c["no"] - c["no_true"]) + c["abstain_true_yes"] for c in cs) / tot["pairs"], 4) if tot["pairs"] else None,
           "agreement_with_data_committed": "share of committed claims matching a Welch test on held-out interventional rows (alpha 0.01)",
                               "ancestor_aid": "Henckel et al. ancestor adjustment identification distance, normalised (gadjid)",
                               "oset_aid": "O-set AID, normalised", "parent_aid": "parent AID, normalised"}},
              open(os.path.join(a.out, "CONTRACT.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
