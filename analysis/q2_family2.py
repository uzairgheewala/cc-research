"""Second held-out family (wave A; TGT-18, CAP-07): frozen kernel v3 read once on our labelled generator's files.

Tickets: TGT-18, CAP-07

    python analysis/q2_family2.py list                                   files, scenarios, tracks (no data read)
    python analysis/q2_family2.py fill [--part 1/8] [--workers 2]        engine cache for the b2 files (heavy; no scoring)
    python analysis/q2_family2.py read --held-out-read FREEZE_ID         the one logged read -> results/q2_v3/family2_read.json

Pre-registration: plans/v3_prereg_amendment_1_family2.json (hashed before any b2 file was scored by v3).
Files: external/b2_namereliance/<track>/<rho>/b2_*.npz (analysis/b2_generator.py; 1,000 rows, columns shuffled, data from
G_D with standardised linear or nonlinear mechanisms). The kernel is data-only, so the names (and rho's name/data
disagreement) never reach it; rho only changes the true graph G_D. Scored exactly as kernel/v3.py evaluate (regime D):
the frozen semantic D confidence model (calibration/v3_semantic_D.pkl, sha256 in plans/v3_freeze.json), DV-1 claims over
every variable as a target (no interventional files exist here), scenario-cluster bootstrap intervals (B = 2000) with
the source scenario (slug) as the cluster. ER-2 and ER-3 as in plans/v3_prereg.json.
The read refuses unless the code and the confidence models match the v3 freeze, and refuses a second read.
"""
import argparse, hashlib, json, multiprocessing as mp, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(ROOT / "analysis"))
B2 = ROOT / "external" / "b2_namereliance"
RES = ROOT / "analysis" / "results" / "q2_v3"
PREREG = ROOT / "plans" / "v3_prereg_amendment_1_family2.json"
ACCESS = RES / "access_log.jsonl"


def b2_files():
    return sorted(str(p) for p in B2.glob("*/*/b2_*__rep000.npz"))     # replicate 0 of every (scenario, track, rho)


def meta_of(path):
    import numpy as np
    with np.load(path, allow_pickle=False) as z:
        return json.loads(str(z["metadata_json"]))


def load(path):
    import causalarena_load as L
    return L.load_any(path)


def truth(s):
    from score import graph
    import causalarena_io as CA
    T = CA.true_edges(s["g"])
    n = len(s["node_ids"])
    return {"n": n, "T": frozenset(T), "desc": graph.reach(n, T), "targets": list(range(n))}


def fill_one(path):
    from kernel import cache
    s = load(path)
    t0 = time.time()
    hit = cache.has(s["values"], list(s["node_ids"]))
    if not hit:
        cache.engines(s["values"], list(s["node_ids"]))
    return {"file": Path(path).name, "hit": hit, "seconds": round(time.time() - t0, 1)}


def claim_rows(path):
    """kernel/v3.py claim_rows, regime D, with the b2 file's own truth (every variable a target)."""
    from score import dv
    from kernel import build as B, cache, claim_features as CF, experiment, k4_eval
    from kernel.v3 import OPEN
    s = load(path)
    X, names, name = s["values"], list(s["node_ids"]), Path(path).name
    eng = cache.engines(X, names, read_only=True)
    led, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
    if led is None:
        return {"file": name, "failure": "pc"}
    I = truth(s)
    D, U = experiment.configure(led, OPEN)
    cl = dv.claims(I["n"], D, U, I["targets"])
    F = CF.features(k4_eval._relabel(led, D, U), I["targets"], cl)
    rows = [{"t": int(t), "y": int(y), "f": F[(t, y)], "yes": bool(v), "ok": (y in I["desc"][t]) == v} for (t, y), v in sorted(cl.items())]
    m = meta_of(path)
    return {"file": name, "scenario": m["slug"], "track": m["track"], "rho": m["rho"], "source_split": m["split"],
            "pairs": dv.n_pairs(I["n"], I["targets"]), "rows": rows, "ledger_sha256": led["report"]["ledger_sha256"]}


def cmd_list(a):
    fs = b2_files()
    ms = [meta_of(f) for f in fs]
    out = {"files": len(fs), "scenarios": len({m["slug"] for m in ms}), "tracks": sorted({m["track"] for m in ms}),
           "rhos": sorted({m["rho"] for m in ms}), "by_source_split": {s: sum(1 for m in ms if m["split"] == s) for s in ("dev", "test")}}
    print(json.dumps(out, indent=1))
    return 0


def cmd_fill(a):
    k, n = (int(x) for x in a.part.split("/"))
    fs = [f for i, f in enumerate(b2_files()) if i % n == k - 1]
    print("[family2] fill part %d/%d: %d files" % (k, n, len(fs)), flush=True)
    with mp.get_context("fork").Pool(a.workers) as pool:
        rows = list(pool.imap(fill_one, fs))
    done = RES / "family2_fill" / ("part%dof%d.json" % (k, n))
    done.parent.mkdir(parents=True, exist_ok=True)
    done.write_text(json.dumps({"files": len(rows), "misses_filled": sum(1 for r in rows if not r["hit"]), "rows": rows}, indent=1))
    print("JOB-COMPLETE %d files" % len(rows))
    return 0


def _guard(read_id):
    from kernel import freeze
    fz = ROOT / "plans" / "v3_freeze.json"
    rec = json.loads(fz.read_text())
    h, _ = freeze.code_sha256()
    if rec["id"] != read_id or rec["code_sha256"] != h:
        raise SystemExit("code or freeze id does not match plans/v3_freeze.json")
    models = json.loads((ROOT / "calibration" / "v3_models.json").read_text())
    for k, v in models.items():
        if hashlib.sha256((ROOT / v["path"]).read_bytes()).hexdigest() != rec["models"][k]:
            raise SystemExit("confidence model %s differs from the frozen one" % k)
    if ACCESS.exists() and any(json.loads(l).get("what") == "v3 family2 read" for l in ACCESS.read_text().splitlines() if l.strip()):
        raise SystemExit("the family-2 files were already read once (access log); a second read needs a new amendment")
    ev = ROOT / "manifests" / "evidence" / "family2_prereg_2026-10-20.sha256"
    if not ev.exists() or hashlib.sha256(PREREG.read_bytes()).hexdigest() not in ev.read_text():
        raise SystemExit("the pre-registration is not hashed in %s, or changed since" % ev.relative_to(ROOT))
    return rec


def cmd_read(a):
    import pickle
    from kernel import v3
    rec = _guard(a.held_out_read)
    RES.mkdir(parents=True, exist_ok=True)
    with open(ACCESS, "a") as fh:
        fh.write(json.dumps({"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "what": "v3 family2 read",
                             "family": "b2_namereliance", "regime": "D", "freeze": rec["id"],
                             "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest()}) + "\n")
    fs = b2_files()
    with mp.get_context("fork").Pool(a.workers) as pool:
        rows = list(pool.imap(claim_rows, fs, chunksize=4))
    failed = [r["file"] for r in rows if "failure" in r]
    files = [r for r in rows if "failure" not in r]
    model = pickle.loads(v3.model_path("semantic", "D").read_bytes())
    probs = {f["file"]: v3.apply_model(model, f["rows"]) for f in files}
    out = {"tickets": ["TGT-18", "CAP-07"], "freeze": rec["id"], "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest(),
           "files_read": len(rows), "failed": failed, "subsets": {}}
    subsets = {"all": files,
               "linear": [f for f in files if f["track"] == "linear"],
               "nonlinear": [f for f in files if f["track"] == "nonlinear"],
               "source_test_scenarios": [f for f in files if f["source_split"] == "test"]}
    for k, fl in subsets.items():
        if fl:
            out["subsets"][k] = v3.scored(fl, probs)
            r = out["subsets"][k]
            print("%-22s tables %4d scen %2d | P@half %.3f [%.3f, %.3f] cov %.3f | ECE %.3f [%.3f, %.3f] | ER-2 %s ER-3 %s" % (
                k, r["tables"], r["scenarios"], r["precision_half"], r["er2_interval"]["lo"], r["er2_interval"]["hi"],
                r["coverage_half"], r["ece"], r["ece_interval"]["lo"], r["ece_interval"]["hi"], r["ER-2_met"], r["ER-3_met"]), flush=True)
    (RES / "family2_read.json").write_text(json.dumps(out, indent=1, default=float))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("list", "fill", "read"))
    ap.add_argument("--part", default="1/1")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--held-out-read", default="")
    a = ap.parse_args()
    return {"list": cmd_list, "fill": cmd_fill, "read": cmd_read}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
