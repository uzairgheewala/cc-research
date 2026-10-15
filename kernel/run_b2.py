"""B2 runner: interventions as order evidence on CausalArena obs+int files and on Causal Chambers (D2.3, D2.4).

  python -m kernel.run_b2 arena --family semantic --split dev --rule C3 --out analysis/results/q2_b2/dev_semantic.jsonl
  python -m kernel.run_b2 chambers --rule C3 --out analysis/results/q2_b2/chambers.json

CausalArena (obs_int files: 800 observational rows, then rows with one or more intervened cells): D is the frozen B1
kernel on the observational rows; D+I adds the shift evidence of every released target from the rows that intervene on
it alone (kernel.interventions). B2.2 compares D+I with D on the same file (paired). DV-1 truth and targets as AB-04.
Causal Chambers (light tunnel, the BEN-10 sample: 1,000 observational rows, 100 rows for each single-target regime;
variables constant in the observational rows dropped, as AB-04): each regime's rows are split in half by a fixed seed;
the first half is shift evidence for D+I, the second half is the agreement check (Welch, alpha 0.01), so D+I is never
checked on the rows it used. Rows reported for the true DAG, the true CPDAG, the empty graph, D, D+I, and the
baselines PC maxP and GES on the same observational rows.
The test split is read only with --held-out-read matching plans/b2_freeze.json. No model calls. Tickets: BLD-03, CAP-03, TGT-06
"""
import argparse, datetime, hashlib, json, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))


def _dv(n, D, U, targets, desc):
    from score import dv
    checked = dv.check(dv.claims(n, D, U, targets), desc)
    return {"pairs": dv.n_pairs(n, targets), "committed": len(checked), "correct": sum(ok for *_, ok in checked),
            "yes": sum(1 for _, _, v, _ in checked if v), "yes_correct": sum(1 for _, _, v, ok in checked if v and ok)}


def arena_one(args):
    path, family, rule, prereg = args
    import numpy as np
    from kernel import build as B, checker, interventions as IV, views
    from score import bench, graph
    import verify02
    s = bench.load(path)
    name = Path(path).name
    X, M, n_obs = s["values"], s["intervened"], s["n_obs"]
    names = list(s["node_ids"])
    obs = X[:n_obs]
    single = M.sum(1) == 1
    by_t = {}
    for t in range(X.shape[1]):
        rows = np.where(M[:, t] & single)[0]
        if len(rows):
            by_t[t] = X[rows]
    t0 = time.time()
    led_d, info = B.build(obs, names, rule=rule, prereg=prereg, created_utc="", file_meta={"source": "CausalArena obs_int (observational rows)", "file": name})
    row = {"file": name, "family": family, "split": bench.split_of(family, name), "scenario": bench.scenario_of(name), "n_obs": int(n_obs),
           "targets_with_rows": {names[t]: int(v.shape[0]) for t, v in by_t.items()}}
    if led_d is None:
        row["failure"] = info.get("failure")
        return row
    ev = IV.shift_evidence(obs, by_t, names)
    led_i, iinfo = IV.apply_interventions(led_d, ev)
    I = bench.truth_info(family, name)
    T, seed = I["T"], graph.file_seed(name)
    for lab, led in (("D", led_d), ("DI", led_i)):
        D, U = views.graph_sets(led)
        row[lab] = {"f1": graph.directed_f1(D, U, T, seed)["f1"], **{k: graph.coords(D, U, T)[k] for k in ("S", "c", "q", "a")},
                    "dv1": _dv(I["n"], D, U, I["targets"], I["desc"]),
                    "verify_failures": {k: len(v) for k, v in verify02.verify(led).items() if v}, "checker_ok": checker.check(led)["ok"],
                    "ledger_sha256": led["report"]["ledger_sha256"]}
    right = sum(1 for a, b in iinfo["oriented"] + iinfo["propagated"] if (names.index(a), names.index(b)) in T)
    row["intervention"] = {"oriented": len(iinfo["oriented"]), "propagated": len(iinfo["propagated"]), "conflicts": len(iinfo["conflicts"]),
                           "oriented_right": right, "jittered": led_d["report"]["engine_outputs"]["jittered"],
                           "fallback": led_d["report"]["engine_outputs"]["policy_fallback"]}
    row["seconds"] = round(time.time() - t0, 1)
    return row


def chambers(rule, prereg, sample):
    import numpy as np
    from engines import core
    from kernel import build as B, checker, interventions as IV, views
    from score import dv, graph
    import verify02
    z = np.load(sample, allow_pickle=True)
    X, reg, var, tg, A = z["X"].astype(float), z["regime"], [str(v) for v in z["variables"]], [str(t) for t in z["targets"]], z["true_adjacency"]
    obs_all = X[reg == 0]
    keep = [j for j in range(X.shape[1]) if obs_all[:, j].std() > 1e-9]
    names = [var[j] for j in keep]
    obs = obs_all[:, keep]
    full_desc = graph.reach(len(var), {(int(i), int(j)) for i, j in zip(*np.where(A != 0))})
    kidx = {j: k for k, j in enumerate(keep)}
    desc = {k: {kidx[d] for d in full_desc[j] if d in kidx} for k, j in enumerate(keep)}
    true_sub = {(kidx[i], kidx[j]) for i, j in zip(*np.where(A != 0)) if i in kidx and j in kidx}
    ev_rows, chk_rows = {}, {}
    for r in sorted(set(reg.tolist()) - {0}):
        t = tg[r] if r < len(tg) else ""
        if not t or var.index(t) not in kidx:
            continue
        k = kidx[var.index(t)]
        e, c = IV.split_rows(X[reg == r][:, keep], seed=20261015 + r)
        ev_rows[k] = np.vstack([ev_rows[k], e]) if k in ev_rows else e
        chk_rows[k] = np.vstack([chk_rows[k], c]) if k in chk_rows else c
    targets = sorted(ev_rows)
    moves = {}
    for t in targets:
        for y in range(len(keep)):
            if y != t and IV.welch(chk_rows[t][:, y], obs[:, y])[1] < 0.01:
                moves.setdefault(t, set()).add(y)
    led_d, info = B.build(obs, names, rule=rule, prereg=prereg, created_utc="", file_meta={"source": "Causal Chambers lt standard (BEN-10 sample)", "file": str(sample)})
    led_i, iinfo = IV.apply_interventions(led_d, IV.shift_evidence(obs, ev_rows, names))
    out = {"tickets": ["BLD-03", "CAP-03", "TGT-06"], "rule": rule, "variables": len(keep), "targets": [names[t] for t in targets],
           "true_edges_kept": len(true_sub), "rows_observational": int(obs.shape[0]),
           "evidence_rows_per_target": {names[t]: int(v.shape[0]) for t, v in ev_rows.items()},
           "check_rows_per_target": {names[t]: int(v.shape[0]) for t, v in chk_rows.items()}, "rows": {}}
    ges = core.run_ges_bic(obs)                         # baselines: plain calls on the given column order (as AB-04)
    pcm = core.run_pc_reference(obs)
    cd, cu = graph.cpdag(true_sub, len(keep))
    graphs = {"true DAG": (true_sub, set()), "true CPDAG": (cd, cu), "empty graph": (set(), set()),
              "kernel D (%s)" % rule: views.graph_sets(led_d), "kernel D+I (%s)" % rule: views.graph_sets(led_i),
              "PC maxP (plain call)": core.marks_to_sets(pcm.marks) if pcm.ok else None,
              "GES (BIC)": core.marks_to_sets(ges.marks) if ges.ok else None}
    for lab, g in graphs.items():
        if g is None:
            out["rows"][lab] = {"failure": True}
            continue
        D, U = g
        cl = dv.claims(len(keep), D, U, targets)
        checked = dv.check(cl, desc)
        agree = [(y in moves.get(t, set())) == v for (t, y), v in cl.items()]
        out["rows"][lab] = {"coverage": len(checked) / dv.n_pairs(len(keep), targets), "precision": sum(ok for *_, ok in checked) / len(checked) if checked else None,
                            "agreement_with_check_rows": sum(agree) / len(agree) if agree else None, "committed": len(checked)}
    for lab, led in (("D", led_d), ("DI", led_i)):
        out["ledger_" + lab] = {"verify_failures": {k: len(v) for k, v in verify02.verify(led).items() if v}, "checker_ok": checker.check(led)["ok"],
                                "ledger_sha256": led["report"]["ledger_sha256"], "deviations": led["report"]["deviations"]}
    out["intervention"] = {k: (len(v) if isinstance(v, list) else v) for k, v in iinfo.items()}
    g = out["rows"].get("GES (BIC)", {}).get("precision")
    for lab in ("kernel D (%s)" % rule, "kernel D+I (%s)" % rule):
        p = out["rows"][lab]["precision"]
        out["rows"][lab]["minus_ges"] = None if (p is None or g is None) else p - g
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("what", choices=("arena", "chambers"))
    ap.add_argument("--family", choices=("semantic", "formula"))
    ap.add_argument("--split", choices=("dev", "test"))
    ap.add_argument("--rule", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--sample", default=str(ROOT / "analysis" / "results" / "chambers" / "sample" / "obs_int_sample.npz"))
    ap.add_argument("--prereg", default=str(ROOT / "plans" / "b2_prereg.json"))
    ap.add_argument("--held-out-read", default=None)
    a = ap.parse_args()
    from score import bench
    prereg = None
    if Path(a.prereg).exists():
        prereg = {"prereg": os.path.relpath(a.prereg, ROOT), "prereg_sha256": hashlib.sha256(Path(a.prereg).read_bytes()).hexdigest(),
                  "fixed_utc": json.load(open(a.prereg)).get("written_utc", "")}
    held = a.what == "chambers" or a.split == "test"
    if held:
        from kernel import freeze
        fz_path = ROOT / "plans" / "b2_freeze.json"
        if not a.held_out_read or prereg is None or not fz_path.exists():
            raise SystemExit("held-out data (test split, Chambers) are read only with --held-out-read FREEZE_ID, plans/b2_prereg.json and plans/b2_freeze.json")
        fz = json.load(open(fz_path))
        h, _ = freeze.code_sha256()
        if fz["id"] != a.held_out_read or fz["code_sha256"] != h or fz.get("rule") != a.rule:
            raise SystemExit("kernel code, rule or freeze id does not match plans/b2_freeze.json: refusing the held-out read")
        log = ROOT / "analysis" / "results" / "q2_b2" / "access_log.jsonl"
        log.parent.mkdir(parents=True, exist_ok=True)
        with open(log, "a") as fh:
            fh.write(json.dumps({"utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "what": a.what,
                                 "family": a.family, "split": a.split, "freeze": a.held_out_read, "rule": a.rule,
                                 "prereg_sha256": prereg["prereg_sha256"]}) + "\n")
    if a.what == "chambers":
        res = chambers(a.rule, prereg, a.sample)
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        json.dump(res, open(a.out, "w"), indent=1)
        for lab, r in res["rows"].items():
            print("%-28s %s" % (lab, r))
        return
    files = [str(f) for f in bench.files(a.family, "obs_int", a.split)]
    if a.limit:
        files = files[:a.limit]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["file"] for l in open(out)} if out.exists() else set()
    jobs = [(f, a.family, a.rule, prereg) for f in files if Path(f).name not in done]
    print("%d files, %d to do" % (len(files), len(jobs)), flush=True)
    import multiprocessing as mp
    with mp.get_context("fork").Pool(a.workers, maxtasksperchild=10) as pool:
        for row in pool.imap_unordered(arena_one, jobs):
            with open(out, "a") as fh:
                fh.write(json.dumps(row) + "\n")
            print(row["file"][:70], row.get("seconds"), flush=True)


if __name__ == "__main__":
    main()
