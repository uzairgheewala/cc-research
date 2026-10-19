"""Where the wrong answers come from, stage by stage (dev, from the engine cache; seconds per family).

For one kernel configuration (v2 = rule C3; v3 = C3 with Meek R1/R3 directions not acted on) in regime D (1,000 rows)
or DxR (five replicates pooled), per family, pooled over the 125 dev files:

  stage 1, links      true links, found, missed; claimed links, false; false split into shadow (an ancestor path joins
                      the pair in the true graph), common cause (shared ancestor, no path), unrelated
  stage 2, directions found true links: committed or left open; committed right or reversed; by licence; and how many
                      committed links the truth itself leaves open (outside the equivalence class: right only by luck)
  stage 3, answers    DV-1 pairs: answered / abstained; yes right / wrong; no right / wrong; the "nothing moves" floor;
                      wrong yes by first wrong edge (reversed true link, backward shadow, common-cause link, unrelated
                      link); wrong no by first blocked true edge (missed link, reversed link)

  python analysis/q2_anatomy.py [--family semantic formula] [--workers 2]  -> analysis/results/q2_v3/anatomy_dev.json
"""
import argparse, json, multiprocessing as mp, os, sys, time
from collections import Counter, deque
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))

CONFIGS = {"v2_D": ((), "obs"), "v3_D": (("meek_r1", "meek_r3"), "obs"), "v2_DxR": ((), "pooled"), "v3_DxR": (("meek_r1", "meek_r3"), "pooled")}


def _path(n, edges, s, t):
    """One directed path s -> t over `edges` (set of (a, b)), as a list of edges, or None."""
    out = {}
    for a, b in edges:
        out.setdefault(a, []).append(b)
    prev = {s: None}
    q = deque([s])
    while q:
        u = q.popleft()
        if u == t:
            break
        for v in out.get(u, ()):
            if v not in prev:
                prev[v] = u
                q.append(v)
    if t not in prev:
        return None
    p, v = [], t
    while prev[v] is not None:
        p.append((prev[v], v))
        v = prev[v]
    return p[::-1]


def _one(args):
    path, family, open_lic, source = args
    from score import bench, dv, graph
    from kernel import build as B, cache, harness, experiment
    name = Path(path).name
    if source == "pooled":
        X, names = harness.pooled_table(path)
    else:
        s = bench.load(path)
        X, names = s["values"], list(s["node_ids"])
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
    if led is None:
        return None
    D, U = experiment.configure(led, open_lic)
    I = bench.truth_info(family, name)
    n, T, desc = I["n"], set(I["T"]), I["desc"]
    anc = {v: {a for a in range(n) if v in desc[a]} for v in range(n)}
    pos = {v["name"]: v["position"] for v in led["variables"]}
    lic = {(pos[c["x"]], pos[c["y"]]): c["licensed_by"] for c in led["claims"] if c["relation"] == "x->y"}
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    tadj = {frozenset(e) for e in T}
    c = Counter()
    # stage 1
    c["true_links"] = len(tadj)
    c["found"] = len(adj & tadj)
    c["claimed_links"] = len(adj)
    for e in adj - tadj:
        a, b = tuple(e)
        if b in desc[a] or a in desc[b]:
            c["false_shadow"] += 1
        elif anc[a] & anc[b]:
            c["false_common_cause"] += 1
        else:
            c["false_unrelated"] += 1
    # stage 2
    mec_open = {frozenset(e) for e in I["cpdag_undirected"]}
    for a, b in T:
        if frozenset((a, b)) not in adj:
            continue
        if (a, b) in D:
            c["dir_committed"] += 1
            c["dir_right"] += 1
            c["lic_%s_right" % lic.get((a, b), "?")] += 1
            c["lic_%s_n" % lic.get((a, b), "?")] += 1
            if frozenset((a, b)) in mec_open:
                c["dir_committed_mec_open"] += 1
                c["dir_committed_mec_open_right"] += 1
        elif (b, a) in D:
            c["dir_committed"] += 1
            c["dir_reversed"] += 1
            c["lic_%s_n" % lic.get((b, a), "?")] += 1
            if frozenset((a, b)) in mec_open:
                c["dir_committed_mec_open"] += 1
        else:
            c["dir_open"] += 1
            c["dir_open_truth_open" if frozenset((a, b)) in mec_open else "dir_open_truth_oriented"] += 1
    c["true_links_truth_open"] = sum(1 for e in tadj if e in mec_open)
    # stage 3
    cl = dv.claims(n, D, U, I["targets"])
    c["pairs"] = dv.n_pairs(n, I["targets"])
    c["answered"] = len(cl)
    for t in I["targets"]:
        for y in range(n):
            if y != t and y not in desc[t]:
                c["floor_no_right"] += 1
    for (t, y), v in cl.items():
        truth = y in desc[t]
        if v:
            if truth:
                c["yes_right"] += 1
                continue
            c["yes_wrong"] += 1
            p = _path(n, D, t, y)
            cul = "unknown"
            for a, b in p or ():
                if b not in desc[t]:
                    if (b, a) in T:
                        cul = "reversed_true_link"
                    elif a in desc[b]:
                        cul = "backward_shadow"
                    elif anc[a] & anc[b]:
                        cul = "common_cause_link"
                    else:
                        cul = "unrelated_link"
                    break
            c["yes_wrong_" + cul] += 1
        else:
            if not truth:
                c["no_right"] += 1
                continue
            c["no_wrong"] += 1
            p = _path(n, T, t, y)
            cul = "unknown"
            for a, b in p or ():
                if frozenset((a, b)) not in adj:
                    cul = "missed_link"
                    break
                if (b, a) in D:
                    cul = "reversed_link"
                    break
            c["no_wrong_" + cul] += 1
    return dict(c)


def derive(c):
    r = lambda a, b: round(a / b, 3) if b else None  # noqa: E731
    out = {"links": {
        "true": c["true_links"], "found": c["found"], "missed": c["true_links"] - c["found"],
        "missed_share": r(c["true_links"] - c["found"], c["true_links"]),
        "claimed": c["claimed_links"], "false": c["claimed_links"] - c["found"],
        "link_precision": r(c["found"], c["claimed_links"]),
        "false_shadow": c.get("false_shadow", 0), "false_common_cause": c.get("false_common_cause", 0), "false_unrelated": c.get("false_unrelated", 0)},
        "directions": {
            "found_true_links": c["found"], "committed": c.get("dir_committed", 0), "left_open": c.get("dir_open", 0),
            "committed_share": r(c.get("dir_committed", 0), c["found"]),
            "right": c.get("dir_right", 0), "reversed": c.get("dir_reversed", 0),
            "right_share": r(c.get("dir_right", 0), c.get("dir_committed", 0)),
            "left_open_and_truth_leaves_open": c.get("dir_open_truth_open", 0), "left_open_but_truth_orients": c.get("dir_open_truth_oriented", 0),
            "true_links_truth_leaves_open": c.get("true_links_truth_open", 0),
            "committed_but_truth_leaves_open": c.get("dir_committed_mec_open", 0),
            "of_those_right": c.get("dir_committed_mec_open_right", 0),
            "by_licence": {k[4:-2]: {"n": c[k], "right": c.get(k[:-2] + "_right", 0), "right_share": r(c.get(k[:-2] + "_right", 0), c[k])}
                           for k in sorted(c) if k.startswith("lic_") and k.endswith("_n")}},
        "answers": {
            "pairs": c["pairs"], "answered": c["answered"], "coverage": r(c["answered"], c["pairs"]),
            "precision": r(c.get("yes_right", 0) + c.get("no_right", 0), c["answered"]),
            "nothing_moves_floor": r(c["floor_no_right"], c["pairs"]),
            "yes": c.get("yes_right", 0) + c.get("yes_wrong", 0), "yes_right": c.get("yes_right", 0), "yes_wrong": c.get("yes_wrong", 0),
            "yes_precision": r(c.get("yes_right", 0), c.get("yes_right", 0) + c.get("yes_wrong", 0)),
            "no": c.get("no_right", 0) + c.get("no_wrong", 0), "no_right": c.get("no_right", 0), "no_wrong": c.get("no_wrong", 0),
            "no_precision": r(c.get("no_right", 0), c.get("no_right", 0) + c.get("no_wrong", 0)),
            "yes_wrong_by_cause": {k[10:]: c[k] for k in sorted(c) if k.startswith("yes_wrong_")},
            "no_wrong_by_cause": {k[9:]: c[k] for k in sorted(c) if k.startswith("no_wrong_")}}}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", nargs="+", default=["semantic", "formula"])
    ap.add_argument("--configs", nargs="+", default=list(CONFIGS))
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    from score import bench
    res = {}
    for fam in a.family:
        res[fam] = {}
        for cfg in a.configs:
            open_lic, source = CONFIGS[cfg]
            fs = [str(p) for p in bench.files(fam, split="dev")]
            if source == "pooled":
                fs = [f for f in fs if f.endswith("__rep000.npz")]
            t0 = time.time()
            with mp.get_context("fork").Pool(a.workers) as pool:
                rows = [r for r in pool.map(_one, [(f, fam, open_lic, source) for f in fs]) if r]
            tot = Counter()
            for r in rows:
                tot.update(r)
            d = derive(tot)
            d["files"] = len(rows)
            d["wall_seconds"] = round(time.time() - t0, 1)
            res[fam][cfg] = d
            print(fam, cfg, "files", len(rows), "%.0fs" % d["wall_seconds"], "| missed %.3f linkP %.3f | dir committed %.2f right %.2f | DV-1 P %.3f cov %.3f yesP %.3f noP %.3f" % (
                d["links"]["missed_share"], d["links"]["link_precision"], d["directions"]["committed_share"], d["directions"]["right_share"],
                d["answers"]["precision"], d["answers"]["coverage"], d["answers"]["yes_precision"], d["answers"]["no_precision"]))
    out = ROOT / "analysis" / "results" / "q2_v3" / "anatomy_dev.json"
    json.dump({"split": "dev", "rule": "C3", "configs": {k: {"open": v[0], "source": v[1]} for k, v in CONFIGS.items()}, "families": res},
              open(out, "w"), indent=1)
    print("->", out)


if __name__ == "__main__":
    main()
