"""X5 (wave A; REP-07, BEN-07, TGT-18): a pretrained causal-discovery engine on CausalArena dev files, under controls.

Tickets: REP-07, BEN-07, TGT-18

    python analysis/x5_pretrained.py fetch                                     network on: AVICI scm-v0 from huggingface.co
    python analysis/x5_pretrained.py run --family semantic --order shuffled [--part 1/4]   network off (x5 image)
    python analysis/x5_pretrained.py score                                     kernel image: F1 beside GES on the same files

Question (plans/x5_prereg.json): does an engine trained on simulated nonlinear mechanisms beat the linear-Gaussian GES
that leads kernel v3, on the files where X1 found the linear score misspecified, once column order cannot help?
AVICI (Lorch et al. 2022; pip avici 1.0.7, checkpoint "scm-v0") reads the data matrix only (no names), and is built to be
invariant to column order; the "original" vs "shuffled" pair checks that, because CausalArena's released column order
leaks the causal order (every true edge runs from an earlier to a later column). Dev split only; the test split is not
read. FoundCause and CDFM weights were not located on 20 Oct: they are not run (recorded as not run, not as a result).

Edges: AVICI's edge probability p(i -> j) > 0.5; when both directions pass, the larger is kept. Directed F1 per file
(score/graph.directed_f1, no undecided pairs), averaged over files, beside GES (the engine cache) and kernel v3's
directed view (Meek R1 / R3 open; undecided pairs oriented by the per-file seed rule) on the same files.
"""
import argparse, hashlib, json, os, sys, time, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
sys.path.insert(0, str(ROOT / "analysis"))
OUT = ROOT / "analysis" / "results" / "x5"
CKPT = ROOT / "external" / "x5" / "avici_cache"
MODEL = "scm-v0"


def dev_files(family):
    from score import bench
    return [str(p) for p in bench.files(family, split="dev")]


def load_model():
    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    import avici
    return avici.load_pretrained(download=MODEL, cache_path=str(CKPT))


def predict(model, X, order, name):
    """-> d x d matrix p[i, j] = P(i -> j) in the file's own column indexing."""
    import numpy as np
    d = X.shape[1]
    perm = np.arange(d) if order == "original" else np.random.default_rng(zlib.crc32(name.encode())).permutation(d)
    P = np.asarray(model(np.asarray(X[:, perm], dtype=np.float64)))
    Q = np.zeros((d, d))
    Q[np.ix_(perm, perm)] = P                       # column c of the input is variable perm[c]
    return Q


def edges_from(P, thr=0.5):
    d = P.shape[0]
    out = set()
    for i in range(d):
        for j in range(d):
            if i != j and P[i, j] > thr and (P[i, j] > P[j, i] or (P[i, j] == P[j, i] and i < j)):
                out.add((i, j))
    return sorted(out)


def cmd_fetch(a):
    os.environ.pop("HF_HUB_OFFLINE", None)
    import avici
    CKPT.mkdir(parents=True, exist_ok=True)
    avici.load_pretrained(download=MODEL, cache_path=str(CKPT))
    files = sorted(str(p.relative_to(ROOT)) for p in CKPT.rglob("*") if p.is_file())
    rec = {"model": MODEL, "files": {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in files}}
    (CKPT / "FETCHED.json").write_text(json.dumps(rec, indent=1))
    print("fetched %d files" % len(files))
    return 0


def run(family, order, part, model=None, limit=0):
    from score import bench
    k, n = (int(x) for x in part.split("/"))
    fs = [f for i, f in enumerate(dev_files(family)) if i % n == k - 1]
    fs = fs[:limit] if limit else fs
    out = OUT / ("%s_%s_part%dof%d.jsonl" % (family, order, k, n))
    out.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["file"] for l in out.read_text().splitlines() if l.strip()} if out.exists() else set()
    model = model or load_model()
    with open(out, "a") as fh:
        for f in fs:
            name = Path(f).name
            if name in done:
                continue
            s = bench.load(f)
            t0 = time.time()
            P = predict(model, s["values"], order, name)
            fh.write(json.dumps({"file": name, "order": order, "edges": edges_from(P), "seconds": round(time.time() - t0, 2),
                                 "p": [[round(float(x), 4) for x in row] for row in P]}) + "\n")
            fh.flush()
    (out.parent / (out.stem + ".done")).write_text("JOB-COMPLETE %d files\n" % len(fs))
    return out


def cmd_run(a):
    run(a.family, a.order, a.part, limit=a.limit)
    return 0


def ges_and_v3(path, family):
    from score import bench, graph
    from kernel import build as B, cache, experiment
    for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[_k] = "1"
    os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
    s = bench.load(path)
    name = Path(path).name
    T = bench.truth_info(family, name)["T"]
    eng = cache.engines(s["values"], list(s["node_ids"]))      # computed (and cached) on a miss, e.g. another BLAS kernel
    out = {}
    g = eng["ges"]
    if g.ok:
        order, M = list(eng["order"]), g.marks
        Dg, Ug = set(), set()
        for i in range(len(order)):
            for j in range(len(order)):
                if M[i, j] == -1 and M[j, i] == 1:
                    Dg.add((order[i], order[j]))
                elif M[i, j] == -1 and M[j, i] == -1 and i < j:
                    Ug.add((order[i], order[j]))
        out["ges"] = graph.directed_f1(Dg, Ug, T, graph.file_seed(name))["f1"]
    led, _ = B.build(s["values"], list(s["node_ids"]), rule="C3", eng=eng, created_utc="")
    if led is not None:
        D, U = experiment.configure(led, ("meek_r1", "meek_r3"))
        out["v3"] = graph.directed_f1(D, U, T, graph.file_seed(name))["f1"]
    return out


def cmd_score(a):
    import numpy as np
    from score import bench, graph
    res = {"tickets": ["REP-07", "BEN-07", "TGT-18"], "model": MODEL, "split": "dev", "families": {}}
    for fam in ("semantic", "formula"):
        rows = {}
        for order in ("original", "shuffled"):
            for p in sorted(OUT.glob("%s_%s_part*.jsonl" % (fam, order))):
                for l in p.read_text().splitlines():
                    if l.strip():
                        r = json.loads(l)
                        rows.setdefault(r["file"], {})[order] = r["edges"]
        if not rows:
            res["families"][fam] = {"status": "not_run"}
            continue
        per = []
        for f in dev_files(fam):
            name = Path(f).name
            if name not in rows:
                continue
            T = bench.truth_info(fam, name)["T"]
            rec = {"file": name}
            for order, e in rows[name].items():
                rec["avici_" + order] = graph.directed_f1(set(map(tuple, e)), set(), T, 0)["f1"]
            rec.update(ges_and_v3(f, fam))
            per.append(rec)
        keys = sorted({k for r in per for k in r if k != "file"})
        summ = {k: float(np.mean([r[k] for r in per if k in r])) for k in keys}
        n = {k: sum(1 for r in per if k in r) for k in keys}
        diffs = {}
        for base in ("ges", "v3"):
            d = [r["avici_shuffled"] - r[base] for r in per if "avici_shuffled" in r and base in r]
            if d:
                rng = np.random.default_rng(20261020)
                scen = sorted({bench.scenario_of(r["file"]) for r in per})
                by = {s_: [r["avici_shuffled"] - r[base] for r in per if bench.scenario_of(r["file"]) == s_ and "avici_shuffled" in r and base in r] for s_ in scen}
                boots = [np.mean([x for s_ in rng.choice(scen, len(scen)) for x in by[s_]]) for _ in range(2000)]
                diffs["avici_shuffled_minus_" + base] = {"mean": float(np.mean(d)), "lo": float(np.percentile(boots, 2.5)),
                                                         "hi": float(np.percentile(boots, 97.5))}
        res["families"][fam] = {"files": len(per), "mean_f1": summ, "n": n, "paired": diffs,
                                "order_effect": (summ.get("avici_original", np.nan) - summ.get("avici_shuffled", np.nan))}
    (OUT / "x5_dev.json").write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps({f: v.get("mean_f1", v) for f, v in res["families"].items()}, indent=1))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=("fetch", "run", "score"))
    ap.add_argument("--family", default="semantic", choices=("semantic", "formula"))
    ap.add_argument("--order", default="shuffled", choices=("original", "shuffled"))
    ap.add_argument("--part", default="1/1")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    return {"fetch": cmd_fetch, "run": cmd_run, "score": cmd_score}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
