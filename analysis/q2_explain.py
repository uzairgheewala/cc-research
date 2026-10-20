"""Explanation round (wave A; TGT-18, TGT-19): why the ledger misses links, adds links and reverses directions.

Tickets: TGT-18, TGT-19

    python analysis/q2_explain.py x123 --family semantic [--workers 2]   free, from the engine cache (minutes)
    python analysis/q2_explain.py x4   --family semantic [--part 1/4]     KCI tests (heavy: Uzair's machine)
    python analysis/q2_explain.py ledger                                   merge into explain_dev.json + the D1 / D2 rule

Pre-registration: plans/q2_explain_prereg.json (hashed in manifests/evidence/ before any number here existed).
Dev split only; reads analysis/results/q2_v3/floor_dev_<family>.json (which missed link is in which class) and the
engine cache (read-only). No test split, no model calls.

X1 score oracle. GES's own score (ges 1.1.0 GaussObsL0Pen, lambda = log(n)/2, on column z-scores, as engines/core.py):
   missed links    gain = local(C, other true parents + P) - local(C, other true parents). gain > 0: the score prefers
                   the link given the true parents, so a search that reached the true parents would add it (a search
                   miss); gain <= 0: the score itself does not want it at 1,000 rows (a score / sample-size miss).
   false links     gain of adding the link to the true graph, the better of the two directions. gain > 0 on a pair the
                   truth leaves unconnected: the linear score is misspecified for this mechanism (it patches a nonlinear
                   or discrete dependence with an extra parent).
   global          BIC of the true DAG against BIC of GES's output: true higher = the greedy search stopped short of a
                   better-scoring graph; GES higher = the score prefers a wrong graph.
X2 orientation oracle. The same orientation rules (causal-learn 0.1.4.8 maxP priority 3, then Meek; Fisher z) applied
   on the true skeleton and on the ledger's skeleton, same data. A ledger reversal that the true skeleton orients
   correctly is skeleton-caused; one that stays reversed is rule-caused (the collider tests themselves).
X3 discrete-aware test on the floor class: nested OLS F-test of adding P to C's regression on its other true parents,
   discrete columns as indicators, continuous ones as cubic polynomials; both directions, Bonferroni. Null calibration
   on true-null pairs (local Markov: A independent of B given B's parents, A a non-descendant non-parent of B).
X4 kernel test (KCI, causal-learn) on the nonlinear-only class and on the same null pairs.
"""
import argparse, json, multiprocessing as mp, os, sys, zlib
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
RES = ROOT / "analysis" / "results" / "q2_v3"
PREREG = ROOT / "plans" / "q2_explain_prereg.json"
NULLS_PER_FILE = 2
V3_OPEN = ("meek_r1", "meek_r3")        # analysis/q2_anatomy.py CONFIGS["v3_D"]


# ------------------------------------------------------------------------------------------------ shared helpers
def _load(path):
    import numpy as np
    from score import bench
    from kernel import build as B, cache
    s = bench.load(path)
    X, names, name = s["values"], list(s["node_ids"]), Path(path).name
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
    return np.asarray(X, float), names, name, eng, led


def null_pairs(name, n, T, desc, k=NULLS_PER_FILE):
    """True-null (A, B, parents of B): A not a descendant of B, not a parent of B, A != B. Seeded by the file name."""
    import numpy as np
    pa = {b: sorted(a for a, c in T if c == b) for b in range(n)}
    cand = [(a, b) for b in range(n) for a in range(n) if a != b and a not in pa[b] and a not in desc[b]]
    rng = np.random.default_rng(zlib.crc32(name.encode()))
    pick = rng.choice(len(cand), size=min(k, len(cand)), replace=False) if cand else []
    return [(int(cand[i][0]), int(cand[i][1]), pa[cand[i][1]]) for i in sorted(pick)]


def nested_f(X, p_, c, others):
    """Discrete-aware nested regression test of P -> C given others, both directions, Bonferroni."""
    import numpy as np
    from scipy import stats
    from kernel import recover
    disc = [recover.is_discrete(X[:, j]) for j in range(X.shape[1])]

    def terms(v):
        x = X[:, v]
        if disc[v]:
            lv = np.unique(x)
            return [(x == l).astype(float) for l in lv[1:]]
        z = (x - x.mean()) / (x.std() or 1.0)
        return [z, z ** 2, z ** 3]

    def one(y_col, add_col):
        y = X[:, y_col].astype(float)
        B0 = recover._basis(X, others, disc)
        B1 = np.column_stack([B0] + terms(add_col))
        r0 = y - B0 @ np.linalg.lstsq(B0, y, rcond=None)[0]
        r1 = y - B1 @ np.linalg.lstsq(B1, y, rcond=None)[0]
        q = np.linalg.matrix_rank(B1) - np.linalg.matrix_rank(B0)
        dfr = len(y) - np.linalg.matrix_rank(B1)
        rss0, rss1 = float(r0 @ r0), float(r1 @ r1)
        if q <= 0 or dfr <= 0 or rss1 <= 0:
            return 1.0
        F = ((rss0 - rss1) / q) / (rss1 / dfr)
        return float(stats.f.sf(F, q, dfr))

    pa, pb = one(c, p_), one(p_, c)
    return {"p": min(1.0, 2 * min(pa, pb)), "p_c_given_p": pa, "p_p_given_c": pb,
            "discrete": bool(disc[p_] or disc[c])}


def orient(X, skeleton_pairs, n):
    """maxP (priority 3) + Meek on a given skeleton (causal-learn 0.1.4.8, Fisher z). -> set of directed (i, j)."""
    from causallearn.graph.GraphClass import CausalGraph
    from causallearn.utils.cit import CIT
    from causallearn.utils.PCUtils import UCSepset, Meek
    cg = CausalGraph(n, ["X%d" % i for i in range(n)])
    cg.set_ind_test(CIT(X, "fisherz"))
    keep = {frozenset(e) for e in skeleton_pairs}
    for i in range(n):
        for j in range(i + 1, n):
            if frozenset((i, j)) not in keep:
                cg.G.remove_edge(cg.G.get_edge(cg.G.nodes[i], cg.G.nodes[j]))
    cg = Meek.meek(UCSepset.maxp(cg, 3))
    G = cg.G.graph
    return {(i, j) for i in range(n) for j in range(n) if G[j, i] == 1 and G[i, j] == -1}


def _gain(S, c, base, add):
    """Score gain of adding `add` to c's parents `base`; None on a singular design (collinear columns)."""
    import numpy as np
    try:
        return float(S.local_score(c, set(base) | {add}) - S.local_score(c, set(base)))
    except np.linalg.LinAlgError:
        return None


# ------------------------------------------------------------------------------------------------ X1-X3, one file
def one_x123(args):
    path, family, floor_missed = args
    import numpy as np
    from ges.scores.gauss_obs_l0_pen import GaussObsL0Pen
    from ges import utils as gu
    from score import bench
    from kernel import experiment
    X, names, name, eng, led = _load(path)
    if led is None:
        return {"file": name, "failure": "pc"}
    I = bench.truth_info(family, name)
    n, T, desc = I["n"], set(map(tuple, I["T"])), I["desc"]
    D, U = experiment.configure(led, V3_OPEN)        # v3's direction view (Meek R1 / R3 left open)
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    anc = {v: {a for a in range(n) if v in desc[a]} for v in range(n)}
    pa = {b: sorted(a for a, c in T if c == b) for b in range(n)}
    # score the table GES saw: the engine's canonical-order data (jittered when the raw table was singular), mapped back
    Xg = np.empty_like(X)
    for k_, j_ in enumerate(eng["order"]):
        Xg[:, j_] = np.asarray(eng["Xc"])[:, k_]
    Z = (Xg - Xg.mean(0)) / np.where(Xg.std(0) > 0, Xg.std(0), 1.0)
    S = GaussObsL0Pen(Z)
    out = {"file": name, "scenario": bench.scenario_of(name), "missed": [], "false": [], "global": {}, "x2": {}, "x3": [],
           "engine_jittered": bool(eng.get("jittered"))}
    # X1 missed links (classes from the floor file)
    for m in floor_missed:
        p_, c = m["edge"]
        others = [x for x in pa[c] if x != p_]
        gain = _gain(S, c, others, p_)
        out["missed"].append({"edge": [p_, c], "class": m["class"], "discrete": m["discrete"], "gain": gain})
    # X1 false links
    tadj = {frozenset(e) for e in T}
    for e in sorted(tuple(sorted(x)) for x in adj - tadj):
        a, b = e
        cls = "shadow" if (b in desc[a] or a in desc[b]) else "common_cause" if anc[a] & anc[b] else "unrelated"
        gs = [g for g in (_gain(S, b, pa[b], a), _gain(S, a, pa[a], b)) if g is not None]
        out["false"].append({"pair": [a, b], "class": cls, "gain": max(gs) if gs else None})
    # X1 global: BIC of the true DAG vs GES's output (both in the original column order)
    A_true = np.zeros((n, n), int)
    for a, b in T:
        A_true[a, b] = 1
    g = eng["ges"]
    if g.ok:
        order = list(eng["order"])
        Mc = np.asarray(g.marks)
        C = np.zeros((n, n), int)
        for i in range(n):
            for j in range(n):
                if Mc[i, j] == -1 and Mc[j, i] == 1:
                    C[order[i], order[j]] = 1
                elif Mc[i, j] == -1 and Mc[j, i] == -1:
                    C[order[i], order[j]] = 1
        try:
            A_ges = gu.pdag_to_dag(C)
            out["global"] = {"bic_true": float(S.full_score(A_true)), "bic_ges": float(S.full_score(A_ges)),
                             "ges_reported": float(g.score)}
        except Exception as e:     # an inconsistent PDAG extension or a singular design is recorded, not fatal
            out["global"] = {"error": "%s: %s" % (type(e).__name__, str(e)[:120])}
    # X2 orientation oracle
    true_skel = [tuple(e) for e in T]
    led_skel = [tuple(sorted(x)) for x in adj]
    jit = False
    try:
        Dt, Dl = orient(X, true_skel, n), orient(X, led_skel, n)
    except Exception:
        # Fisher z on a singular correlation matrix: the kernel's own rule (engines/MANIFEST.json, singular_data):
        # retry once with seeded Gaussian jitter sd 1e-6, and record it
        jit = True
        Xj = X + np.random.default_rng(zlib.crc32(name.encode())).normal(0.0, 1e-6, X.shape)
        try:
            Dt, Dl = orient(Xj, true_skel, n), orient(Xj, led_skel, n)
        except Exception as e:
            Dt = Dl = None
            out["x2"] = {"error": "%s: %s" % (type(e).__name__, str(e)[:120])}
    led_dir = set(map(tuple, D))
    found = [e for e in T if frozenset(e) in adj]
    rev_ledger = [e for e in found if (e[1], e[0]) in led_dir]
    out["x2"] = out["x2"] if Dt is None else {
        "jittered": jit,
        "found_true": len(found),
        "ledger_reversed": len(rev_ledger),
        "ledger_reversed_fixed_by_true_skeleton": sum(1 for e in rev_ledger if tuple(e) in Dt),
        "ledger_reversed_still_reversed_true_skeleton": sum(1 for e in rev_ledger if (e[1], e[0]) in Dt),
        "ledger_reversed_open_true_skeleton": sum(1 for e in rev_ledger if tuple(e) not in Dt and (e[1], e[0]) not in Dt),
        "rules_on_ledger_skeleton": {"right": sum(1 for e in found if tuple(e) in Dl), "reversed": sum(1 for e in found if (e[1], e[0]) in Dl)},
        "rules_on_true_skeleton": {"right": sum(1 for e in T if tuple(e) in Dt), "reversed": sum(1 for e in T if (e[1], e[0]) in Dt),
                                   "true_links": len(T)},
        "agreement_rules_vs_ledger_on_found": sum(1 for e in found if (tuple(e) in Dl) == (tuple(e) in led_dir)
                                                  and ((e[1], e[0]) in Dl) == ((e[1], e[0]) in led_dir))}
    # X3 discrete-aware test on the floor class, plus nulls
    for m in floor_missed:
        if m["class"] != "floor":
            continue
        p_, c = m["edge"]
        r = nested_f(X, p_, c, [x for x in pa[c] if x != p_])
        out["x3"].append(dict(r, edge=[p_, c], kind="floor"))
    for a, b, pb in null_pairs(name, n, T, desc):
        r = nested_f(X, a, b, pb)
        out["x3"].append(dict(r, edge=[a, b], kind="null"))
    return out


# ------------------------------------------------------------------------------------------------ X4, one file
def one_x4(args):
    path, family, nl_missed = args
    import numpy as np
    from causallearn.utils.cit import CIT
    from score import bench
    s = bench.load(path)
    X, name = np.asarray(s["values"], float), Path(path).name
    I = bench.truth_info(family, name)
    n, T, desc = I["n"], set(map(tuple, I["T"])), I["desc"]
    pa = {b: sorted(a for a, c in T if c == b) for b in range(n)}
    Xs = (X - X.mean(0)) / np.where(X.std(0) > 0, X.std(0), 1.0)
    kci = CIT(Xs, "kci")
    rows = []
    for m in nl_missed:
        p_, c = m["edge"]
        rows.append({"edge": [p_, c], "kind": "nonlinear_only", "p": float(kci(p_, c, [x for x in pa[c] if x != p_]))})
    for a, b, pb in null_pairs(name, n, T, desc):
        rows.append({"edge": [a, b], "kind": "null", "p": float(kci(a, b, pb))})
    return {"file": name, "x4": rows}


# ------------------------------------------------------------------------------------------------ commands
def floor_rows(family):
    d = json.loads((RES / ("floor_dev_%s.json" % family)).read_text())
    return {r["file"]: r["missed"] for r in d["rows"]}


def cmd_x123(a):
    from score import bench
    fr = floor_rows(a.family)
    fs = [str(p) for p in bench.files(a.family, split="dev") if Path(p).name in fr]
    fs = fs[: a.limit] if a.limit else fs
    with mp.get_context("fork").Pool(a.workers) as pool:
        rows = pool.map(one_x123, [(f, a.family, fr[Path(f).name]) for f in fs], chunksize=1)
    out = {"tickets": ["TGT-18", "TGT-19"], "family": a.family, "split": "dev", "files": len(rows),
           "prereg_sha256": _sha(PREREG), "rows": rows}
    p = RES / ("explain_x123_dev_%s.json" % a.family)
    p.write_text(json.dumps(out, indent=1))
    print(json.dumps(summarise_x123(rows), indent=1))
    return 0


def cmd_x4(a):
    from score import bench
    fr = floor_rows(a.family)
    k, n = (int(x) for x in a.part.split("/"))
    fs = [str(p) for p in bench.files(a.family, split="dev") if Path(p).name in fr]
    fs = [f for i, f in enumerate(fs) if i % n == k - 1]
    fs = fs[: a.limit] if a.limit else fs
    p = RES / "x4" / ("explain_x4_dev_%s_part%dof%d.jsonl" % (a.family, k, n))
    p.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if p.exists():
        done = {json.loads(l)["file"] for l in p.read_text().splitlines() if l.strip()}
    todo = [f for f in fs if Path(f).name not in done]
    print("[x4] %s part %d/%d: %d files, %d to do" % (a.family, k, n, len(fs), len(todo)), flush=True)
    with open(p, "a") as fh, mp.get_context("fork").Pool(a.workers) as pool:
        args = [(f, a.family, [m for m in fr[Path(f).name] if m["class"] == "method_nonlinear"]) for f in todo]
        for r in pool.imap(one_x4, args):
            fh.write(json.dumps(r) + "\n")
            fh.flush()
    (p.parent / (p.stem + ".done")).write_text("JOB-COMPLETE %d files\n" % len(fs))
    return 0


def _sha(p):
    import hashlib
    return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).exists() else None


def _share(xs):
    return (sum(xs) / len(xs)) if xs else None


def summarise_x123(rows):
    rows = [r for r in rows if "failure" not in r]
    miss = [m for r in rows for m in r["missed"]]
    s = {"files": len(rows), "missed": {}, "false": {}, "global": {}, "x2": {}, "x3": {}}
    for cls in ("method_linear", "method_nonlinear", "sample_size", "floor"):
        g = [m["gain"] for m in miss if m["class"] == cls and m["gain"] is not None]
        s["missed"][cls] = {"n": len(g), "singular": sum(1 for m in miss if m["class"] == cls and m["gain"] is None), "share_gain_positive": _share([x > 0 for x in g]),
                            "median_gain": sorted(g)[len(g) // 2] if g else None}
    fl = [f for r in rows for f in r["false"]]
    for cls in ("shadow", "common_cause", "unrelated"):
        g = [f["gain"] for f in fl if f["class"] == cls and f["gain"] is not None]
        s["false"][cls] = {"n": len(g), "singular": sum(1 for f in fl if f["class"] == cls and f["gain"] is None), "share_gain_positive": _share([x > 0 for x in g])}
    gl_all = [r["global"] for r in rows if "bic_true" in r.get("global", {})]
    gl = [x for x in gl_all if abs(x["bic_ges"] - x["ges_reported"]) < 1.0]   # our rescoring reproduces GES's own score (its running total drifts by < 0.1)
    s["global"] = {"files": len(gl), "excluded_score_check_failed": len(gl_all) - len(gl),
                   "share_true_dag_scores_higher": _share([x["bic_true"] > x["bic_ges"] for x in gl]),
                   "median_bic_ges_minus_true": sorted(x["bic_ges"] - x["bic_true"] for x in gl)[len(gl) // 2] if gl else None,
                   "errors": sum(1 for r in rows if "error" in r.get("global", {}))}
    keys = ["found_true", "ledger_reversed", "ledger_reversed_fixed_by_true_skeleton",
            "ledger_reversed_still_reversed_true_skeleton", "ledger_reversed_open_true_skeleton", "agreement_rules_vs_ledger_on_found"]
    r2 = [r for r in rows if "error" not in r["x2"]]
    x2 = {k: sum(r["x2"][k] for r in r2) for k in keys}
    x2["files"], x2["errors"] = len(r2), len(rows) - len(r2)
    x2["jittered_files"] = sum(1 for r in r2 if r["x2"].get("jittered"))
    x2["skeleton_caused_share"] = x2["ledger_reversed_fixed_by_true_skeleton"] / max(1, x2["ledger_reversed"])
    x2["rule_caused_share"] = x2["ledger_reversed_still_reversed_true_skeleton"] / max(1, x2["ledger_reversed"])
    for which in ("rules_on_ledger_skeleton", "rules_on_true_skeleton"):
        x2[which] = {k: sum(r["x2"][which][k] for r in r2) for k in r2[0]["x2"][which]} if r2 else {}
    s["x2"] = x2
    t3 = [t for r in rows for t in r["x3"]]
    fl3, nu3 = [t for t in t3 if t["kind"] == "floor"], [t for t in t3 if t["kind"] == "null"]
    s["x3"] = {"floor_n": len(fl3), "floor_detected": _share([t["p"] <= 0.05 for t in fl3]),
               "floor_discrete_detected": _share([t["p"] <= 0.05 for t in fl3 if t["discrete"]]),
               "null_n": len(nu3), "null_rejection": _share([t["p"] <= 0.05 for t in nu3])}
    if s["x3"]["floor_detected"] is not None and s["x3"]["null_rejection"] is not None:
        s["x3"]["floor_detected_beyond_null"] = s["x3"]["floor_detected"] - s["x3"]["null_rejection"]
    return s


def summarise_x4(family):
    rows = []
    for p in sorted((RES / "x4").glob("explain_x4_dev_%s_part*.jsonl" % family)):
        rows += [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    t = [x for r in rows for x in r["x4"]]
    nl, nu = [x for x in t if x["kind"] == "nonlinear_only"], [x for x in t if x["kind"] == "null"]
    if not t:
        return {"status": "not_run"}
    s = {"files": len(rows), "nonlinear_n": len(nl), "nonlinear_detected": _share([x["p"] <= 0.05 for x in nl]),
         "null_n": len(nu), "null_rejection": _share([x["p"] <= 0.05 for x in nu])}
    if s["nonlinear_detected"] is not None and s["null_rejection"] is not None:
        s["nonlinear_detected_beyond_null"] = s["nonlinear_detected"] - s["null_rejection"]
    return s


def decide(sem, pre):
    """The pre-registered D1 / D2 rule on the semantic family (plans/q2_explain_prereg.json, rules)."""
    r = pre["rules"]
    s_search = sem["missed"]["method_linear"]["share_gain_positive"]
    m_unrel = sem["false"]["unrelated"]["share_gain_positive"]
    if s_search is None:
        return {"direction": "not_decided", "why": "X1 not run"}
    if s_search >= r["d2_search_share_at_least"]:
        d = "D2-search"
    elif m_unrel is not None and m_unrel >= r["d2_score_misspecification_at_least"]:
        d = "D2-score"
    elif s_search <= r["d1_search_share_at_most"]:
        d = "D1"
    else:
        d = "D1-with-search-follow-up"
    return {"direction": d, "search_share": s_search, "unrelated_misspecification_share": m_unrel}


def cmd_ledger(a):
    pre = json.loads(PREREG.read_text())
    out = {"tickets": ["TGT-18", "TGT-19"], "prereg_sha256": _sha(PREREG), "families": {}}
    for fam in ("semantic", "formula"):
        p = RES / ("explain_x123_dev_%s.json" % fam)
        f = {"x123": summarise_x123(json.loads(p.read_text())["rows"]) if p.exists() else {"status": "not_run"},
             "x4": summarise_x4(fam)}
        floor = json.loads((RES / ("floor_dev_%s.json" % fam)).read_text())
        f["missed_classes"] = {k: v["share_of_true_links"] for k, v in floor["classes"].items()}
        f["missed_share"] = floor["missed_share"]
        out["families"][fam] = f
    sem = out["families"]["semantic"]["x123"]
    out["decision"] = decide(sem, pre) if "missed" in sem else {"direction": "not_decided"}
    p = RES / "explain_dev.json"
    p.write_text(json.dumps(out, indent=1))
    print(json.dumps(out["decision"]))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("x123", "x4", "ledger"))
    ap.add_argument("--family", default="semantic", choices=("semantic", "formula"))
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--part", default="1/1")
    a = ap.parse_args()
    return {"x123": cmd_x123, "x4": cmd_x4, "ledger": cmd_ledger}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
