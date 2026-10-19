"""L5: interventions as link evidence (dev; plans/l5_prereg.json). Tickets: TGT-18, TGT-19, CAP-03

  python analysis/q2_l5.py collect    -> analysis/results/q2_v3/l5_links_dev.jsonl.gz (125 dev obs_int files per family)
  python analysis/q2_l5.py evaluate   -> analysis/results/q2_v3/l5_dev.json

Ledger: v3 (rule C3, Meek R1/R3 open) on the 800 observational rows of each obs_int file, from the engine cache.
For every effective released target t (own values shifted in its single-target rows, Welch p < 0.01):
  M      y in do(t) rows vs observational rows (Welch; B2's statistic)
  C      residual of y after least squares on Z (fitted on observational rows), do(t) rows vs observational rows;
         Z = ledger neighbours of y that are also ledger neighbours of t (found links), or for an add candidate the
         ledger neighbours of y shifted by do(t)
Rules S (cut shadow), N (cut, neither of two targets moves the other), A (add a missed link t -> y), confirm; thresholds
cross-fitted by scenario. Truth labels are used only to score. Nothing here changes the kernel. Dev split only.
"""
import gzip, json, multiprocessing as mp, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(ROOT / "analysis"))
RES = ROOT / "analysis" / "results" / "q2_v3"
LINKS = RES / "l5_links_dev.jsonl.gz"
OUT = RES / "l5_dev.json"
TAU = [0.05, 0.1, 0.2, 0.3, 0.5]
ALPHA_ADD = [0.001, 0.01, 0.05]
SHIFT, BAR, MIN_RECALL, MIN_N = 0.01, 0.80, 0.10, 30


def _resid_shift(obs, rows, y, Z):
    import numpy as np
    from kernel import interventions as IV
    if Z:
        A = np.column_stack([np.ones(obs.shape[0]), obs[:, Z]])
        beta, *_ = np.linalg.lstsq(A, obs[:, y], rcond=None)
        r_obs = obs[:, y] - A @ beta
        r_int = rows[:, y] - np.column_stack([np.ones(rows.shape[0]), rows[:, Z]]) @ beta
    else:
        r_obs, r_int = obs[:, y], rows[:, y]
    return IV.welch(r_int, r_obs)[1]


def _one(args):
    path, family = args
    import numpy as np
    from kernel import interventions as IV
    from score import bench
    import q2_linkfilt as LF
    name = Path(path).name
    s = bench.load(path)
    X, M, n_obs = np.asarray(s["values"], dtype=float), s["intervened"], int(s["n_obs"])
    names = list(s["node_ids"])
    obs = X[:n_obs]
    g = LF._ledger(obs, names)
    if g is None:
        return None
    D, U = g
    I = bench.truth_info(family, name)
    n = I["n"]
    anc_of = {v: {a for a in range(n) if v in I["desc"][a]} for v in range(n)}
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    nb = {v: set() for v in range(n)}
    for e in adj:
        a, b = tuple(e)
        nb[a].add(b)
        nb[b].add(a)
    single = M.sum(1) == 1
    by_t, eff = {}, {}
    for t in I["targets"]:
        r = np.where(M[:, t] & single)[0]
        if len(r) < 5:
            continue
        by_t[t] = X[r]
        eff[t] = IV.welch(X[r, t], obs[:, t])[1]
    effective = sorted(t for t, p in eff.items() if p < SHIFT)
    pM = {(t, y): IV.welch(by_t[t][:, y], obs[:, y])[1] for t in effective for y in range(n) if y != t}
    links = []
    for e in sorted(adj, key=sorted):
        a, b = sorted(e)
        tests = []
        for t, y in ((a, b), (b, a)):
            if t not in effective:
                continue
            Z = sorted((nb[y] & nb[t]) - {t, y})
            tests.append({"t": t, "y": y, "pM": pM[(t, y)], "pC": _resid_shift(obs, by_t[t], y, Z) if Z else None, "nZ": len(Z)})
        links.append({"a": a, "b": b, "label": LF._label(e, I, anc_of), "tests": tests})
    tadj = {frozenset(x) for x in I["T"]}
    adds = []
    for t in effective:
        for y in range(n):
            if y == t or frozenset((t, y)) in adj or pM[(t, y)] >= SHIFT:
                continue
            Z = sorted(z for z in nb[y] if z != t and pM.get((t, z), 1.0) < SHIFT)
            adds.append({"t": t, "y": y, "pM": pM[(t, y)], "pC": _resid_shift(obs, by_t[t], y, Z), "nZ": len(Z),
                         "true_link": frozenset((t, y)) in tadj, "true_dir": (t, y) in I["T"]})
    missed_reach = sum(1 for e in tadj - adj if set(e) & set(effective))
    return {"file": name, "scenario": bench.scenario_of(name), "family": family, "targets": sorted(by_t), "effective": effective,
            "target_rows": {str(t): int(v.shape[0]) for t, v in by_t.items()}, "D": sorted(map(list, D)), "U": sorted(map(list, U)),
            "links": links, "adds": adds, "missed_true_links": len(tadj - adj), "missed_true_links_with_effective_end": missed_reach}


def collect(workers):
    from score import bench
    t0 = time.time()
    with gzip.open(LINKS, "wt") as fh:
        for fam in ("semantic", "formula"):
            fs = [str(p) for p in bench.files(fam, regime="obs_int", split="dev")]
            with mp.get_context("fork").Pool(workers) as pool:
                k = 0
                for r in pool.imap(_one, [(f, fam) for f in fs]):
                    if r:
                        fh.write(json.dumps(r) + "\n")
                        k += 1
            print(fam, k, "files", "%.0fs" % (time.time() - t0), flush=True)


# ------------------------------------------------------------------------------------------------------------ evaluate
def rule_S(l, tau):
    return any(x["pM"] < SHIFT and x["nZ"] > 0 and x["pC"] is not None and x["pC"] >= tau for x in l["tests"])


def rule_N(l, tau):
    return len(l["tests"]) == 2 and all(x["pM"] >= tau for x in l["tests"])


def confirmed(l):
    return any((x["nZ"] > 0 and x["pC"] is not None and x["pC"] < SHIFT) or (x["nZ"] == 0 and x["pM"] < SHIFT) for x in l["tests"])


def rule_A(a, alpha):
    return a["pC"] < alpha


def _folds(files):
    sc = sorted({f["scenario"] for f in files})
    return {s: k % 5 for k, s in enumerate(sc)}


def _cut_stats(links, pred, p):
    cut = [l for l in links if pred(l, p)]
    cf = sum(1 for l in cut if l["label"] != "true")
    return len(cut), cf


def crossfit_cut(files, pred, grid):
    fd = _folds(files)
    picks, cut_all, cuts_by_file = [], [], {}
    for k in range(5):
        tr = [l for f in files if fd[f["scenario"]] != k for l in f["links"]]
        best = None
        for p in grid:                          # tau ascending; a smaller tau cuts more (S and N): the first that passes
            n, cf = _cut_stats(tr, pred, p)     # is the most permissive
            if n >= MIN_N and cf / n >= BAR:
                best = p
                break
        picks.append(best)
        for f in files:
            if fd[f["scenario"]] != k or best is None:
                continue
            cs = [l for l in f["links"] if pred(l, best)]
            cut_all += cs
            cuts_by_file[f["file"]] = {frozenset((l["a"], l["b"])) for l in cs}
    testable_false = sum(1 for f in files for l in f["links"] if l["tests"] and l["label"] != "true")
    all_false = sum(1 for f in files for l in f["links"] if l["label"] != "true")
    true_all = sum(1 for f in files for l in f["links"] if l["label"] == "true")
    cf = sum(1 for l in cut_all if l["label"] != "true")
    prec = cf / len(cut_all) if cut_all else None
    rec = cf / testable_false if testable_false else 0.0
    return {"picks": picks, "cuts": len(cut_all), "cut_precision": None if prec is None else round(prec, 3),
            "cut_recall_testable": round(rec, 3), "cut_recall_all_false": round(cf / all_false, 3) if all_false else None,
            "true_lost": round((len(cut_all) - cf) / true_all, 4) if true_all else None,
            "cut_by_kind": {k: sum(1 for l in cut_all if l["label"] == k) for k in ("shadow", "common_cause", "unrelated", "true")},
            "licence": bool(prec is not None and prec >= BAR and rec >= MIN_RECALL)}, cuts_by_file


def crossfit_add(files):
    fd = _folds(files)
    picks, added, adds_by_file = [], [], {}
    for k in range(5):
        tr = [a for f in files if fd[f["scenario"]] != k for a in f["adds"]]
        best = None
        for al in ALPHA_ADD:
            s = [a for a in tr if rule_A(a, al)]
            if len(s) >= MIN_N and sum(a["true_link"] for a in s) / len(s) >= BAR:
                best = al
        picks.append(best)
        for f in files:
            if fd[f["scenario"]] != k or best is None:
                continue
            s = [a for a in f["adds"] if rule_A(a, best)]
            added += s
            adds_by_file[f["file"]] = [(a["t"], a["y"]) for a in s]
    reach = sum(f["missed_true_links_with_effective_end"] for f in files)
    tp = sum(a["true_link"] for a in added)
    prec = tp / len(added) if added else None
    return {"picks": picks, "adds": len(added), "add_precision": None if prec is None else round(prec, 3),
            "add_direction_right": round(sum(a["true_dir"] for a in added) / max(1, tp), 3) if tp else None,
            "recall_of_reachable_missed": round(tp / reach, 3) if reach else None,
            "recall_of_all_missed": round(tp / max(1, sum(f["missed_true_links"] for f in files)), 4),
            "licence": bool(prec is not None and prec >= BAR and len(added) >= MIN_N)}, adds_by_file


def answers(files, cuts_by_file, adds_by_file, family):
    from score import bench, dv, graph
    agg = {"base": [0, 0, 0, 0.0], "new": [0, 0, 0, 0.0]}
    for f in files:
        I = bench.truth_info(family, f["file"])
        D = {tuple(e) for e in f["D"]}
        U = {tuple(e) for e in f["U"]}
        cuts = cuts_by_file.get(f["file"], set())
        D2 = {e for e in D if frozenset(e) not in cuts} | set(adds_by_file.get(f["file"], []))
        U2 = {e for e in U if frozenset(e) not in cuts}
        pairs = dv.n_pairs(I["n"], I["targets"])
        seed = graph.file_seed(f["file"])
        for key, (d, u) in (("base", (D, U)), ("new", (D2, U2))):
            ch = dv.check(dv.claims(I["n"], d, u, I["targets"]), I["desc"])
            agg[key][0] += len(ch)
            agg[key][1] += sum(ok for *_, ok in ch)
            agg[key][2] += pairs
            agg[key][3] += graph.directed_f1(d, u, I["T"], seed)["f1"]
    out = {k: {"dv1_precision": round(ok / com, 4) if com else None, "coverage": round(com / pairs, 4), "f1": round(f1 / len(files), 4)}
           for k, (com, ok, pairs, f1) in agg.items()}
    out["change"] = {k: round(out["new"][k] - out["base"][k], 4) for k in ("dv1_precision", "coverage", "f1")}
    return out


def evaluate():
    with gzip.open(LINKS, "rt") as fh:
        rows = [json.loads(l) for l in fh]
    out = {"prereg": "plans/l5_prereg.json", "tickets": ["TGT-18", "TGT-19", "CAP-03"], "families": {}}
    for fam in ("semantic", "formula"):
        files = [r for r in rows if r["family"] == fam]
        links = [l for f in files for l in f["links"]]
        false = [l for l in links if l["label"] != "true"]
        testable = [l for l in links if l["tests"]]
        F = {"files": len(files),
             "targets_per_file": round(sum(len(f["targets"]) for f in files) / len(files), 2),
             "effective_per_file": round(sum(len(f["effective"]) for f in files) / len(files), 2),
             "links": len(links), "false_links": len(false),
             "testable_links": len(testable), "testable_false": sum(1 for l in testable if l["label"] != "true"),
             "reach_false": round(sum(1 for l in testable if l["label"] != "true") / len(false), 3) if false else None,
             "testable_kinds": {k: sum(1 for l in testable if l["label"] == k) for k in ("true", "shadow", "common_cause", "unrelated")},
             "two_test_links": sum(1 for l in links if len(l["tests"]) == 2),
             "testable_with_mediator": sum(1 for l in testable if any(x["nZ"] > 0 for x in l["tests"]))}
        F["grid_S"] = {str(t): dict(zip(("cuts", "false_cut"), _cut_stats(links, rule_S, t))) for t in TAU}
        F["grid_N"] = {str(t): dict(zip(("cuts", "false_cut"), _cut_stats(links, rule_N, t))) for t in TAU}
        F["S"], cS = crossfit_cut(files, rule_S, TAU)
        F["N"], cN = crossfit_cut(files, rule_N, TAU)
        F["A"], aA = crossfit_add(files)
        F["grid_A"] = {str(al): {"adds": sum(1 for f in files for a in f["adds"] if rule_A(a, al)),
                                 "true": sum(1 for f in files for a in f["adds"] if rule_A(a, al) and a["true_link"])} for al in ALPHA_ADD}
        F["add_candidates"] = sum(len(f["adds"]) for f in files)
        F["add_candidates_true"] = sum(a["true_link"] for f in files for a in f["adds"])
        F["missed_true_links"] = sum(f["missed_true_links"] for f in files)
        F["missed_reachable"] = sum(f["missed_true_links_with_effective_end"] for f in files)
        conf = [l for l in testable if confirmed(l)]
        F["confirm"] = {"confirmed": len(conf), "true_share": round(sum(l["label"] == "true" for l in conf) / len(conf), 3) if conf else None,
                        "base_rate_testable": round(sum(l["label"] == "true" for l in testable) / len(testable), 3) if testable else None}
        lic_cuts = {}
        for r, c in (("S", cS), ("N", cN)):
            if F[r]["licence"]:
                for k, v in c.items():
                    lic_cuts.setdefault(k, set()).update(v)
        lic_adds = aA if F["A"]["licence"] else {}
        F["answers_licensed"] = answers(files, lic_cuts, lic_adds, fam) if (lic_cuts or lic_adds) else None
        # descriptive: what each rule would do at its cross-fitted picks whether licensed or not
        F["answers_S_unlicensed"] = answers(files, cS, {}, fam) if cS and not F["S"]["licence"] else None
        out["families"][fam] = F
        print("==", fam, json.dumps({k: F[k] for k in ("files", "targets_per_file", "effective_per_file", "links", "false_links", "testable_links",
                                                        "testable_false", "reach_false", "testable_kinds", "two_test_links", "testable_with_mediator")}))
        print("  S", json.dumps(F["S"]), "\n  N", json.dumps(F["N"]), "\n  A", json.dumps(F["A"]), "\n  confirm", F["confirm"])
        print("  grid S", F["grid_S"], "\n  grid A", F["grid_A"], "| candidates", F["add_candidates"], "true", F["add_candidates_true"], "missed reachable", F["missed_reachable"])
        print("  answers licensed", F["answers_licensed"], "\n  answers S (unlicensed)", F["answers_S_unlicensed"])
    S, Fm = out["families"]["semantic"], out["families"]["formula"]
    lic = [(fam, r) for fam in ("semantic", "formula") for r in ("S", "N", "A") if out["families"][fam][r]["licence"]]
    v = {}
    v["P-L5-0"] = "refuted" if (S["reach_false"] < 0.10 or Fm["reach_false"] > 0.20) else ("supported" if S["reach_false"] >= 0.20 and Fm["reach_false"] <= 0.10 else "partly")
    v["P-L5-1"] = "supported" if S["S"]["licence"] else "refuted" if (S["S"]["cut_precision"] is None or S["S"]["cut_precision"] < BAR) else "partly (precision met, recall short)"
    # judged on the rule's own behaviour at every tau of the grid (not only on cross-fitted picks, which can be empty)
    nbad = [(fam, t) for fam in ("semantic", "formula") for t, g in out["families"][fam]["grid_N"].items()
            if g["cuts"] >= MIN_N and g["false_cut"] / g["cuts"] < BAR]
    nbig = [(fam, t) for fam in ("semantic", "formula") for t, g in out["families"][fam]["grid_N"].items() if g["cuts"] >= MIN_N]
    v["P-L5-2"] = "refuted" if nbad else ("supported" if not nbig else "partly")
    v["P-L5-2_detail"] = {"tau_with_30_or_more_cuts_below_bar": nbad}
    v["P-L5-3"] = "refuted" if (S["A"]["licence"] or Fm["A"]["licence"]) else "supported"
    v["P-L5-4"] = (None if S["confirm"]["true_share"] is None else "supported" if S["confirm"]["true_share"] >= 0.90 else
                   "refuted" if S["confirm"]["true_share"] < 0.80 else "partly")
    if not lic:
        v["P-L5-5"] = "not tested (no licence)"
    else:
        bad = [fam for fam in {f for f, _ in lic} if out["families"][fam]["answers_licensed"]["change"]["dv1_precision"] < 0
               or out["families"][fam]["answers_licensed"]["change"]["f1"] < 0]
        good = all(out["families"][fam]["answers_licensed"]["change"]["dv1_precision"] >= 0.005 for fam in {f for f, _ in lic})
        v["P-L5-5"] = "refuted" if bad else ("supported" if good else "partly")
    out["licences"] = ["%s/%s" % x for x in lic]
    out["verdicts"] = v
    json.dump(out, open(OUT, "w"), indent=1, default=float)
    print(json.dumps({"licences": out["licences"], "verdicts": v}, indent=1))


if __name__ == "__main__":
    if sys.argv[1] == "collect":
        collect(int(os.environ.get("WORKERS", "2")))
    else:
        evaluate()
