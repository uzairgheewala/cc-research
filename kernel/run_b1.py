"""B1 runner: build data-only ledgers on CausalArena files and score every combination rule (D1.7).

  python -m kernel.run_b1 --family semantic --split dev --out analysis/results/q2_b1/dev_semantic.jsonl [--workers 2]
      [--rules pc ges C1 C2 C3] [--save-ledgers runs/q2_b1] [--limit N]

Per file (one engine run, every rule built from it):
  ledger per rule, verify02 (V1-V13), K7 checker, ledger hash;
  rung R1: the 'pc' rule's graph equals causal-learn's plain pc(...maxP) call on the same canonical columns, except
           the pairs a recorded directed-cycle defect left open;
  scores per rule: directed F1 (expectation rule, per-file seed), S, c, q, a; DV-1 committed claims against the
           released targets (counts, so the pooled numbers can be recomputed).
Resumable: files already in --out are skipped. The test split is refused unless --held-out-read is given together with
a frozen kernel (plans/b1_freeze.json, kernel/freeze.py), and each held-out read is appended to the access log.
No model calls. Tickets: BLD-02, BLD-14, CAP-05, CAP-09, CAP-11, TGT-10
"""
import argparse, datetime, gzip, json, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))

RULES = ("pc", "ges", "C1", "C2", "C3")


def one_file(args):
    path, family, rules, save_dir, prereg = args
    import numpy as np
    from engines import core
    from kernel import build as B, checker, views
    from score import bench, dv, graph
    import verify02
    s = bench.load(path)
    X, names = s["values"], list(s["node_ids"])
    name = Path(path).name
    t0 = time.time()
    eng = B.run_engines(X, names, with_ges=True)
    row = {"file": name, "family": family, "split": bench.split_of(family, name), "scenario": bench.scenario_of(name),
           "n": len(names), "rows": int(X.shape[0]), "pc_ok": eng["pc"].ok, "jittered": eng["jittered"] is not False,
           "ges_ok": bool(eng["ges"] is not None and eng["ges"].ok),
           "ges_failure": (eng["ges"].failure if eng["ges"] is not None and not eng["ges"].ok else None),
           "pc_seconds": round(eng["pc"].seconds, 2), "ges_seconds": round(eng["ges"].seconds, 2) if eng["ges"] is not None else None,
           "rules": {}}
    if not eng["pc"].ok:
        row["failure"] = eng["pc"].failure
        return row
    ref = core.run_pc_reference(eng["Xc"])
    I = bench.truth_info(family, name)
    seed = graph.file_seed(name)
    for rule in rules:
        led, info = B.build(X, names, rule=rule, eng=eng, prereg=prereg, file_meta={"source": "CausalArena", "file": name},
                            created_utc="")
        vres = verify02.verify(led)
        kres = checker.check(led)
        D, U = views.graph_sets(led)
        T = I["T"]
        f1 = graph.directed_f1(D, U, T, seed)
        co = graph.coords(D, U, T)
        checked = dv.check(dv.claims(I["n"], D, U, I["targets"]), I["desc"])
        yes = [ok for _, _, v, ok in checked if v]
        no = [ok for _, _, v, ok in checked if not v]
        r = {"f1": f1["f1"], "precision": f1["precision"], "recall": f1["recall"], **{k: co[k] for k in ("S", "c", "q", "a")},
             "dv1": {"pairs": dv.n_pairs(I["n"], I["targets"]), "yes": len(yes), "yes_ok": sum(yes), "no": len(no), "no_ok": sum(no)},
             "verify_failures": {k: len(v) for k, v in vres.items() if v}, "checker_ok": kres["ok"], "checker_errors": kres["errors"][:3],
             "ledger_sha256": led["report"]["ledger_sha256"], "fallback": led["report"]["engine_outputs"]["policy_fallback"],
             "defects": len(led["report"]["engine_outputs"]["pc"]["defects"]),
             "rule_cycles": sum(len(d.get("pairs_left_open", [])) for d in led["report"]["engine_outputs"]["pc"]["defects"] if d["type"] == "rule_directed_cycle"),
             "conflicts": sum(1 for c in led["claims"] if c["conflict"]),
             "licences": {}}
        for c in led["claims"]:
            if c["relation"] == "x->y":
                r["licences"][c["licensed_by"]] = r["licences"].get(c["licensed_by"], 0) + 1
        if rule == "pc":
            Dr, Ur = core.map_back(*core.marks_to_sets(ref.marks), eng["order"]) if ref.ok else (None, None)
            pos = {v["name"]: v["position"] for v in led["variables"]}
            left, types = set(), {}
            for d in led["report"]["engine_outputs"]["pc"]["defects"]:
                types[d["type"]] = types.get(d["type"], 0) + 1
                for a_, b_ in d.get("pairs_left_open", []) + d.get("pairs", []):
                    left.add(tuple(sorted((pos[a_], pos[b_]))))
            row["pc_defects"] = types
            if ref.ok:
                keep = lambda S: {e for e in S if tuple(sorted(e)) not in left}  # noqa: E731
                row["r1_equal_reference"] = (keep(D), keep(U)) == (keep(Dr), keep(Ur))
                row["r1_exact_without_defect_fix"] = (D, U) == (Dr, Ur)
                row["r1_pairs_set_aside"] = len(left)
            else:
                row["r1_equal_reference"] = None
        if save_dir:
            out = Path(save_dir) / family / rule
            out.mkdir(parents=True, exist_ok=True)
            with gzip.open(out / (name + ".ledger.json.gz"), "wt", encoding="utf-8") as fh:
                json.dump(led, fh)
        row["rules"][rule] = r
    row["seconds"] = round(time.time() - t0, 2)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=("semantic", "formula"))
    ap.add_argument("--split", required=True, choices=("dev", "test"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--rules", nargs="+", default=list(RULES))
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--save-ledgers", default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--held-out-read", default=None, help="kernel freeze id from plans/b1_freeze.json (required for --split test)")
    ap.add_argument("--prereg", default=str(ROOT / "plans" / "b1_prereg.json"))
    a = ap.parse_args()
    sys.path.insert(0, str(ROOT))
    from score import bench
    import hashlib
    prereg = None
    if Path(a.prereg).exists():
        prereg = {"prereg": os.path.relpath(a.prereg, ROOT), "prereg_sha256": hashlib.sha256(Path(a.prereg).read_bytes()).hexdigest(),
                  "fixed_utc": json.load(open(a.prereg)).get("written_utc", "")}
    if a.split == "test":
        from kernel import freeze
        fz_path = ROOT / "plans" / "b1_freeze.json"
        if not a.held_out_read or prereg is None or not fz_path.exists():
            raise SystemExit("the test split is read only with --held-out-read FREEZE_ID, plans/b1_prereg.json and plans/b1_freeze.json")
        fz = json.load(open(fz_path))
        h, _ = freeze.code_sha256()
        if fz["id"] != a.held_out_read or fz["code_sha256"] != h:
            raise SystemExit("kernel code or freeze id does not match plans/b1_freeze.json: refusing the held-out read")
        if fz.get("rule") and set(a.rules) != {fz["rule"]} | {"pc"}:
            raise SystemExit("a held-out read scores the frozen rule (and the pc floor regime) only: --rules pc %s" % fz["rule"])
        log = ROOT / "analysis" / "results" / "q2_b1" / "access_log.jsonl"
        log.parent.mkdir(parents=True, exist_ok=True)
        with open(log, "a") as fh:
            fh.write(json.dumps({"utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                                 "family": a.family, "split": "test", "freeze": a.held_out_read, "rules": a.rules,
                                 "prereg_sha256": prereg["prereg_sha256"]}) + "\n")
    files = [str(f) for f in bench.files(a.family, "obs_only", a.split)]
    if a.limit:
        files = files[:a.limit]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for ln in open(out):
            if ln.strip():
                done.add(json.loads(ln)["file"])
    todo = [f for f in files if Path(f).name not in done]
    print("%d files, %d done, %d to do" % (len(files), len(done), len(todo)), flush=True)
    jobs = [(f, a.family, tuple(a.rules), a.save_ledgers, prereg) for f in todo]
    if a.workers > 1:
        import multiprocessing as mp
        ctx = mp.get_context("fork")
        with ctx.Pool(a.workers, maxtasksperchild=20) as pool:
            for row in pool.imap_unordered(one_file, jobs):
                with open(out, "a") as fh:
                    fh.write(json.dumps(row) + "\n")
                print(row["file"][:70], row.get("seconds"), flush=True)
    else:
        for j in jobs:
            row = one_file(j)
            with open(out, "a") as fh:
                fh.write(json.dumps(row) + "\n")
            print(row["file"][:70], row.get("seconds"), flush=True)


if __name__ == "__main__":
    main()
