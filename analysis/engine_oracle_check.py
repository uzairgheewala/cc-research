"""Does each PC / FCI implementation recover the right equivalence class from a perfect independence oracle, whatever
the column order? No data, no model calls: the conditional-independence test is d-separation in the true DAG.

  python analysis/engine_oracle_check.py --engine vendored=PATH --engine pypi-0.1.3.8=PATH --engine pypi-0.1.4.8=PATH \
      --gcastle PATH --dags 120 --perms 6 --out analysis/results/engine_oracle

With an oracle, a correct PC returns exactly the true CPDAG and a correct FCI (no hidden variables) the true skeleton,
for every column order. Any difference is an implementation defect, not a statistical error. Each engine runs in its
own subprocess (only its path on sys.path). Random DAGs: p in {6, 8, 10, 12}, expected degree 2-3, fixed seeds.
Tickets: AUD-27, AUD-23, CAP-05, REP-07
"""
import argparse, itertools, json, os, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


# ---------------------------------------------------------------- shared: DAGs and truth
def random_dags(n, seed):
    import random
    rng = random.Random(seed)
    out = []
    for k in range(n):
        p = (6, 8, 10, 12)[k % 4]
        prob = rng.uniform(2.0, 3.0) / (p - 1)
        order = list(range(p))
        rng.shuffle(order)
        edges = sorted((order[i], order[j]) for i in range(p) for j in range(i + 1, p) if rng.random() < prob)
        out.append({"p": p, "edges": edges})
    return out


def perms(p, k, seed):
    import random
    rng = random.Random(seed)
    ps = [list(range(p)), list(range(p))[::-1]]
    while len(ps) < k:
        q = list(range(p))
        rng.shuffle(q)
        if q not in ps:
            ps.append(q)
    return ps[:k]


def truth(edges, p):
    sys.path.insert(0, str(HERE))
    import cc_graph as G
    C = G.cpdag_of(set(map(tuple, edges)), p)
    directed, undirected = set(), set()
    for a, b in itertools.combinations(range(p), 2):
        t = G.pair_type(C, a, b)
        if t == "a->b":
            directed.add((a, b))
        elif t == "b->a":
            directed.add((b, a))
        elif t != "none":
            undirected.add((a, b))
    return directed, undirected


# ---------------------------------------------------------------- worker: one engine, all DAGs
def worker(kind, path, dags_file, out_file, nperm):
    import numpy as np
    import networkx as nx
    sys.path.insert(0, path)
    dags = json.load(open(dags_file))
    res = []
    import contextlib, io
    for di, d in enumerate(dags):
        p, edges = d["p"], [tuple(e) for e in d["edges"]]
        for pi, perm in enumerate(perms(p, nperm, 1000 + di)):
            # column j of the permuted data is original variable perm[j]
            inv = {orig: j for j, orig in enumerate(perm)}
            pedges = [(inv[a], inv[b]) for a, b in edges]
            Gp = nx.DiGraph()
            Gp.add_nodes_from(range(p))
            Gp.add_edges_from(pedges)
            data = np.zeros((20, p))
            rec = {"dag": di, "perm": pi}
            try:
              with contextlib.redirect_stdout(io.StringIO()):
                if kind == "causallearn":
                    import causallearn.utils.cit as _cit
                    if not hasattr(_cit, "nx"):          # Causal-Copilot's copy calls nx in its d-separation test without importing it
                        _cit.nx = nx
                    from causallearn.search.ConstraintBased.PC import pc
                    from causallearn.search.ConstraintBased.FCI import fci
                    import joblib                         # threads, so the oracle's lazy networkx import is shared
                    with joblib.parallel_backend("threading"):
                        g = pc(data, 0.05, "d_separation", true_dag=Gp, show_progress=False, verbose=False).G.graph
                    rec["pc"] = decode_cl(g, perm)
                    with joblib.parallel_backend("threading"):
                        fg, _ = fci(data, "d_separation", 0.05, true_dag=Gp, show_progress=False, verbose=False)
                    rec["fci_skeleton"] = sorted(sorted((perm[i], perm[j])) for i in range(p) for j in range(i + 1, p) if fg.graph[i, j] != 0)
                else:
                    import types
                    if "torch" not in sys.modules:      # gCastle imports torch for other algorithms; PC never calls it
                        class _Any:
                            def __call__(self, *a, **k):
                                return a[0] if len(a) == 1 and callable(a[0]) else self

                            def __getattr__(self, name):
                                return self

                            def __mro_entries__(self, bases):
                                return (object,)

                        class _Stub(types.ModuleType):
                            def __getattr__(self, name):
                                return object if name in ("Module", "Dataset") else _Any()
                        import importlib.abc, importlib.machinery

                        class _TorchFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
                            def find_spec(self, name, path=None, target=None):
                                if name == "torch" or name.startswith("torch."):
                                    return importlib.machinery.ModuleSpec(name, self, is_package=True)
                                return None

                            def create_module(self, spec):
                                mod = _Stub(spec.name)
                                mod.__path__ = []
                                return mod

                            def exec_module(self, module):
                                pass
                        sys.meta_path.insert(0, _TorchFinder())
                    from castle.algorithms.pc.pc import PC
                    dsep = getattr(nx, "is_d_separator", None) or nx.d_separated

                    def oracle(_data, x, y, z):
                        return None, None, 1.0 if dsep(Gp, {x}, {y}, set(z)) else 0.0
                    for variant in ("original", "stable", "parallel"):
                        m = PC(variant=variant, alpha=0.05, ci_test=oracle)
                        m.learn(data)
                        rec["gcastle_" + variant] = decode_gc(np.asarray(m.causal_matrix), perm)
            except Exception as e:  # noqa: BLE001
                rec["error"] = "%s: %s" % (type(e).__name__, str(e)[:200])
            res.append(rec)
    json.dump(res, open(out_file, "w"))


def decode_cl(g, perm):
    """causal-learn: g[i,j] = -1, g[j,i] = 1 means i -> j; both -1 means i - j. Map back to original indices."""
    p = len(perm)
    directed, undirected = [], []
    for i in range(p):
        for j in range(i + 1, p):
            a, b = g[i, j], g[j, i]
            if a == 0 and b == 0:
                continue
            if a == -1 and b == 1:
                directed.append((perm[i], perm[j]))
            elif a == 1 and b == -1:
                directed.append((perm[j], perm[i]))
            else:
                undirected.append(tuple(sorted((perm[i], perm[j]))))
    return {"directed": sorted(directed), "undirected": sorted(undirected)}


def decode_gc(m, perm):
    """gCastle causal_matrix: m[i,j] = 1 and m[j,i] = 0 means i -> j; both 1 means undirected."""
    p = len(perm)
    directed, undirected = [], []
    for i in range(p):
        for j in range(i + 1, p):
            a, b = m[i, j], m[j, i]
            if a and b:
                undirected.append(tuple(sorted((perm[i], perm[j]))))
            elif a:
                directed.append((perm[i], perm[j]))
            elif b:
                directed.append((perm[j], perm[i]))
    return {"directed": sorted(directed), "undirected": sorted(undirected)}


# ---------------------------------------------------------------- driver
def summarise(dags, results, key):
    exact = skel = total = 0
    extra = missing = 0
    invariant = 0
    by_dag = {}
    errors = 0
    for r in results:
        if "error" in r:
            errors += 1
            continue
        if key not in r:
            continue
        d = dags[r["dag"]]
        td, tu = truth(d["edges"], d["p"])
        out = r[key]
        if key == "fci_skeleton":
            got = {tuple(x) for x in out}
            want = {tuple(sorted(e)) for e in td} | set(tu)
            ok_s = got == want
            ok_e = ok_s
            sig = json.dumps(sorted(got))
        else:
            gd, gu = {tuple(x) for x in out["directed"]}, {tuple(x) for x in out["undirected"]}
            ok_e = gd == td and gu == tu
            ok_s = ({tuple(sorted(e)) for e in gd} | gu) == ({tuple(sorted(e)) for e in td} | tu)
            sig = json.dumps([sorted(gd), sorted(gu)])
        got_s = got if key == "fci_skeleton" else ({tuple(sorted(e)) for e in gd} | gu)
        want_s = {tuple(sorted(e)) for e in td} | set(tu)
        extra += len(got_s - want_s)
        missing += len(want_s - got_s)
        total += 1
        exact += ok_e
        skel += ok_s
        by_dag.setdefault(r["dag"], set()).add(sig)
    invariant = sum(1 for s in by_dag.values() if len(s) == 1)
    return {"runs": total, "errors": errors, "exact_equivalence_class": exact, "exact_skeleton": skel,
            "dags": len(by_dag), "dags_order_invariant": invariant,
            "skeleton_extra_adjacencies": extra, "skeleton_missing_adjacencies": missing}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine", action="append", default=[], help="label=path (causal-learn copy)")
    ap.add_argument("--gcastle", default=None, help="path containing the castle package")
    ap.add_argument("--dags", type=int, default=120)
    ap.add_argument("--perms", type=int, default=6)
    ap.add_argument("--seed", type=int, default=20261013)
    ap.add_argument("--out", required=True)
    ap.add_argument("--_worker", nargs=4, help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a._worker:
        kind, path, dags_file, out_file = a._worker
        worker(kind, path, dags_file, out_file, a.perms)
        return
    dags = random_dags(a.dags, a.seed)
    tmp = Path(tempfile.mkdtemp())
    json.dump(dags, open(tmp / "dags.json", "w"))
    jobs = [(lab, "causallearn", path) for lab, path in (e.split("=", 1) for e in a.engine)]
    if a.gcastle:
        jobs.append(("gcastle-1.0.4", "gcastle", a.gcastle))
    report = {"tickets": ["AUD-27", "AUD-23", "CAP-05", "REP-07"], "dags": a.dags, "perms_per_dag": a.perms, "seed": a.seed,
              "sizes": sorted({d["p"] for d in dags}), "edges_total": sum(len(d["edges"]) for d in dags), "engines": {}}
    for lab, kind, path in jobs:
        out = tmp / ("%s.json" % lab)
        env = dict(os.environ, PYTHONPATH="")
        subprocess.run([sys.executable, __file__, "--perms", str(a.perms), "--out", str(tmp), "--_worker", kind, path,
                        str(tmp / "dags.json"), str(out)], check=True, env=env)
        res = json.load(open(out))
        keys = ["pc", "fci_skeleton"] if kind == "causallearn" else ["gcastle_original", "gcastle_stable", "gcastle_parallel"]
        for k in keys:
            report["engines"]["%s/%s" % (lab, k)] = {"path": path, **summarise(dags, res, k)}
            print("%-40s %s" % ("%s/%s" % (lab, k), report["engines"]["%s/%s" % (lab, k)]))
        first_err = next((r["error"] for r in res if "error" in r), None)
        if first_err:
            report["engines"]["%s/first_error" % lab] = first_err
    os.makedirs(a.out, exist_ok=True)
    json.dump(report, open(os.path.join(a.out, "oracle.json"), "w"), indent=1)
    json.dump({"producer": "analysis/engine_oracle_check.py", "score_bearing": False, "tickets": report["tickets"]},
              open(os.path.join(a.out, "CONTRACT.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
