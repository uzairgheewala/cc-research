"""Re-score every baseline we can run under the layout controls: released vs shuffled columns, the scoreboard authors'
orientation rule ("lower": earlier column -> later column) vs the expectation rule (undecided pairs at random), in the
coordinates S (skeleton F1), c (commit rate), q (commit accuracy), a = c q + (1 - c)/2, and directed F1.
Paired on the files both arms scored. No model calls; reads stored graphs only.

  python analysis/rescore_controls.py --root external/causalarena --out analysis/results/rescore

Reads analysis/results/methods/<method>_<family>_obs*_{rel,shuf}.json (and the BND-04 names without _rel) and
analysis/results/published/leaderboard.json. Writes rescore.json (+ CONTRACT.json).
Tickets: AUD-28, BEN-07, REP-07
"""
import argparse, json, os, statistics as st, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402

M = HERE / "results" / "methods"
PAIRS = {  # label: {family: (released file, shuffled file)}
    "PC (Causal-Copilot copy)": {"semantic": ("pc_semantic_obs_rel", "pc_semantic_obs_shuf"),
                                 "formula": ("pc_formula_obs_rel", "pc_formula_obs_shuf")},
    "PC (upstream causal-learn)": {"semantic": ("pc_upstream_semantic_obs_rel", "pc_upstream_semantic_obs_shuf"),
                                   "formula": ("pc_upstream_formula_obs_rel", "pc_upstream_formula_obs_shuf")},
    "GES (BIC)": {"semantic": ("gesbic_semantic_obs", "gesbic_semantic_obs_shuf"),
                  "formula": ("gesbic_formula_obs_rel", "gesbic_formula_obs_shuf")},
    "FCI": {"semantic": ("fci_semantic_obs", "fci_semantic_obs_shuf"), "formula": ("fci_formula_obs_rel", "fci_formula_obs_shuf")},
    "DirectLiNGAM": {"semantic": ("lingam_semantic_obs_rel", "lingam_semantic_obs_shuf"),
                     "formula": ("lingam_formula_obs_rel", "lingam_formula_obs_shuf")},
    "NOTEARS": {"semantic": ("notears_semantic_obs_rel", "notears_semantic_obs_shuf"),
                "formula": ("notears_formula_obs_rel", "notears_formula_obs_shuf")},
}
PUBLISHED_NAME = {"PC (Causal-Copilot copy)": "PC", "PC (upstream causal-learn)": "PC", "GES (BIC)": "GIES",
                  "DirectLiNGAM": "LiNGAM", "NOTEARS": "NOTEARS"}


def rows(name):
    p = M / (name + ".json")
    if not p.exists():
        return None
    d = json.load(open(p))
    return {r["file"]: r for r in d["rows"] if not r.get("failed")}


_truth = {}


def truth(root, fam, file):
    key = (fam, file)
    if key not in _truth:
        sub = "%s_obs_only" % fam
        _truth[key] = CA.true_edges(CA.load(Path(root) / "scm" / fam / "data" / sub / file)["g"])
    return _truth[key]


def coords(r, T):
    directed = {tuple(e) for e in r["directed_edges"]}
    und = {frozenset(u[:2]) for u in r["undecided_pairs"]}
    tadj = {frozenset(e) for e in T}
    padj = {frozenset(e) for e in directed} | und
    tp = len(tadj & padj)
    P = tp / len(padj) if padj else 0.0
    R = tp / len(tadj) if tadj else 0.0
    S = 2 * P * R / (P + R) if P + R else 0.0
    right = sum(1 for e in directed if e in T)
    wrong = sum(1 for e in directed if (e[1], e[0]) in T)
    c = (right + wrong) / tp if tp else 0.0
    q = right / (right + wrong) if right + wrong else None
    a = (right + 0.5 * (tp - right - wrong)) / tp if tp else 0.0
    return {"S": S, "c": c, "q": q, "a": a, "F1_random": r["scores"]["random"]["f1"], "F1_lower": r["scores"]["lower"]["f1"]}


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(st.mean(xs), 4) if xs else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent / "external" / "causalarena"))
    ap.add_argument("--out", default=str(HERE / "results" / "rescore"))
    a = ap.parse_args()
    pub = json.load(open(HERE / "results" / "published" / "leaderboard.json"))
    out = {"tickets": ["AUD-28", "BEN-07", "REP-07"], "rules": {
        "lower": "undecided pair -> earlier column to later column (the authors' baseline rule; reads column order)",
        "random": "undecided pair oriented at random with a per-file seed (expectation rule)"}, "methods": {}}
    for label, fams in PAIRS.items():
        for fam, (rel, shuf) in fams.items():
            R, S = rows(rel), rows(shuf)
            if R is None or S is None:
                continue
            common = sorted(set(R) & set(S))
            cr = [coords(R[f], truth(a.root, fam, f)) for f in common]
            cs = [coords(S[f], truth(a.root, fam, f)) for f in common]
            summ = {arm: {k: mean([x[k] for x in xs]) for k in ("S", "c", "q", "a", "F1_random", "F1_lower")}
                    for arm, xs in (("released", cr), ("shuffled", cs))}
            d_rand = [y["F1_random"] - x["F1_random"] for x, y in zip(cr, cs)]
            rec = {"files_paired": len(common), "files_released_ok": len(R), "files_shuffled_ok": len(S), **summ,
                   "layout_gain_authors_rule": round(summ["released"]["F1_lower"] - summ["shuffled"]["F1_random"], 4),
                   "order_effect_expectation_rule": round(st.mean(d_rand), 4),
                   "files_better_shuffled": sum(d > 0 for d in d_rand), "files_worse_shuffled": sum(d < 0 for d in d_rand),
                   "published": None}
            pn = PUBLISHED_NAME.get(label)
            if pn:
                rec["published"] = pub["table"].get(fam, {}).get("D", {}).get(pn, {}).get("f1")
            out["methods"].setdefault(label, {})[fam] = rec
            print("%-28s %-8s n=%3d  S %.3f/%.3f  q %s/%s  F1 rel(lower %.3f, random %.3f) shuf(random %.3f)  published %s" % (
                label, fam, len(common), summ["released"]["S"], summ["shuffled"]["S"], summ["released"]["q"], summ["shuffled"]["q"],
                summ["released"]["F1_lower"], summ["released"]["F1_random"], summ["shuffled"]["F1_random"], rec["published"]))
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "rescore.json"), "w"), indent=1)
    json.dump({"producer": "analysis/rescore_controls.py", "score_bearing": True, "tickets": out["tickets"],
               "regime": "D", "split": "all-public (measurement, no tuning)", "split_detail": "public half (50 scenarios x 5 files per family)",
               "controls": {"columns_shuffled": "both arms reported", "names": "not applicable", "supplier": "causalarena"},
               "orientation_rule": "both reported: lower (authors') and random (expectation)",
               "metric_defs": {"S": "skeleton F1", "c": "commit rate", "q": "commit accuracy", "a": "c q + (1 - c)/2",
                               "F1_random": "directed F1, undecided at random", "F1_lower": "directed F1, authors' rule"}},
              open(os.path.join(a.out, "CONTRACT.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
