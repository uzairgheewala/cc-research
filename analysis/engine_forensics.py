"""AB-03 engine forensics: extend the perfect-oracle check (AUD-27) to more engines, and test determinism.

  python analysis/engine_forensics.py --python2 PATH_TO_PY_WITH_pgmpy_dodiscover_tigramite --vendored PATH --out analysis/results/engine_forensics

Oracle part (same 120 random DAGs x 6 column orders and the same truth as engine_oracle_check.py; the CI test is
d-separation in the true DAG, so a correct implementation returns the true CPDAG, or for FCI the true skeleton, in every
order). Engines added here:
  pgmpy 1.1.2 PC          variants orig / stable / parallel, max_cond_vars unbounded and at the default 5
  dodiscover (git main)   PC and FCI with dodiscover.ci.Oracle (shim: nx.d_separated = nx.is_d_separator, removed in networkx 3.5)
  tigramite 5.2.10.1      PCMCI+ with tau_max = 0 (contemporaneous only: PC with tigramite's order-independent rules),
                          OracleCI; marks '-->' directed, 'o-o' undecided, 'x-x' conflict (counted as undecided)
Determinism part: the same input run three times. Causal-Copilot's vendored causal-learn FCI under joblib threads
(AUD-27 saw 533 vs 531 exact) and pgmpy PC with n_jobs=-1 (parallel).
A defect class is assigned from the error pattern: "extra adjacency" (a separating set never tested),
"missing adjacency", "orientation only" (skeleton right, marks wrong), "order dependent" (output changes with the order).
No data, no model calls. Tickets: AUD-35, AUD-23, CAP-05, CAP-11, EXT-03
"""
import argparse, json, os, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from engine_oracle_check import random_dags, perms, summarise, decode_cl  # noqa: E402


def dsep_fn(nx, G):
    f = getattr(nx, "is_d_separator", None) or nx.d_separated
    return lambda x, y, z: f(G, {x}, {y}, set(z))


def worker(kind, dags_file, out_file, nperm):
    import contextlib, io, warnings
    warnings.filterwarnings("ignore")
    import numpy as np
    import networkx as nx
    import pandas as pd
    dags = json.load(open(dags_file))
    res = []
    for di, d in enumerate(dags):
        p, edges = d["p"], [tuple(e) for e in d["edges"]]
        for pi, perm in enumerate(perms(p, nperm, 1000 + di)):
            inv = {orig: j for j, orig in enumerate(perm)}
            pedges = [(inv[a], inv[b]) for a, b in edges]
            names = ["v%d" % j for j in range(p)]
            Gp = nx.DiGraph()
            Gp.add_nodes_from(range(p))
            Gp.add_edges_from(pedges)
            rec = {"dag": di, "perm": pi}
            try:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    if kind == "pgmpy":
                        from pgmpy.estimators import PC
                        ds = dsep_fn(nx, Gp)
                        idx = {n: j for j, n in enumerate(names)}

                        def ci(X, Y, Z, data=None, boolean=True, **kw):
                            return ds(idx[X], idx[Y], [idx[z] for z in Z])
                        df = pd.DataFrame(np.zeros((5, p)), columns=names)
                        for variant in ("orig", "stable", "parallel"):
                            for mcv, tag in ((p, "unbounded"), (5, "default5")):
                                g = PC(data=df).estimate(variant=variant, ci_test=ci, return_type="cpdag", max_cond_vars=mcv,
                                                         n_jobs=1, show_progress=False)
                                rec["pgmpy_%s_%s" % (variant, tag)] = decode_named(g.directed_edges, g.undirected_edges, idx, perm)
                    elif kind == "dodiscover":
                        from dodiscover import PC, FCI, make_context
                        from dodiscover.ci import Oracle
                        if not hasattr(nx, "d_separated"):      # networkx >= 3.5 removed the alias dodiscover's Oracle calls
                            nx.d_separated = nx.is_d_separator
                        Gn = nx.relabel_nodes(Gp, {j: names[j] for j in range(p)})
                        df = pd.DataFrame(np.zeros((5, p)), columns=names)
                        ctx = make_context().variables(data=df).build()
                        idx = {n: j for j, n in enumerate(names)}
                        m = PC(ci_estimator=Oracle(Gn))
                        m.learn_graph(df, ctx)
                        g = m.graph_
                        rec["dodiscover_pc"] = decode_named(list(g.directed_edges), list(g.undirected_edges), idx, perm)
                        f = FCI(ci_estimator=Oracle(Gn))
                        f.learn_graph(df, make_context().variables(data=df).build())
                        pag = f.graph_
                        sk = set()
                        for et in pag.edge_types:
                            for u, v in pag.get_graphs(et).edges:
                                sk.add(tuple(sorted((perm[idx[u]], perm[idx[v]]))))
                        rec["dodiscover_fci_skeleton"] = sorted(sk)
                    elif kind == "tigramite":
                        from tigramite import data_processing as pp
                        from tigramite.pcmci import PCMCI
                        from tigramite.independence_tests.oracle_conditional_independence import OracleCI
                        links = {j: [] for j in range(p)}
                        for a, b in pedges:
                            links[b].append(((a, 0), 1.0, None))
                        oracle = OracleCI(links=links, observed_vars=list(range(p)), tau_max=0)
                        df = pp.DataFrame(np.random.default_rng(0).standard_normal((50, p)))
                        m = PCMCI(dataframe=df, cond_ind_test=oracle, verbosity=0)
                        out = m.run_pcmciplus(tau_min=0, tau_max=0, pc_alpha=0.01)
                        G = out["graph"][:, :, 0]
                        directed, und, conflict = [], [], 0
                        for i in range(p):
                            for j in range(i + 1, p):
                                s = G[i, j]
                                if s == "":
                                    continue
                                if s == "-->":
                                    directed.append((perm[i], perm[j]))
                                elif s == "<--":
                                    directed.append((perm[j], perm[i]))
                                else:
                                    und.append(tuple(sorted((perm[i], perm[j]))))
                                    conflict += s == "x-x"
                        rec["tigramite_pcmciplus"] = {"directed": sorted(directed), "undirected": sorted(und)}
                        rec["tigramite_conflicts"] = conflict
            except Exception as e:  # noqa: BLE001
                rec["error"] = "%s: %s" % (type(e).__name__, str(e)[:300])
            res.append(rec)
    json.dump(res, open(out_file, "w"))


def decode_named(directed, undirected, idx, perm):
    dd = sorted((perm[idx[u]], perm[idx[v]]) for u, v in directed)
    uu = sorted(tuple(sorted((perm[idx[u]], perm[idx[v]]))) for u, v in undirected)
    return {"directed": dd, "undirected": uu}


def determinism(vendored, dags, nperm_runs=3, n_dags=40):
    """Run the vendored causal-learn FCI (joblib threading, as Causal-Copilot runs it) three times on the same inputs."""
    code = r'''
import json, sys, contextlib, io
import numpy as np, networkx as nx, joblib
sys.path.insert(0, sys.argv[1])
from causallearn.utils import cit as _cit
if not hasattr(_cit, "nx"):
    _cit.nx = nx
from causallearn.search.ConstraintBased.FCI import fci
dags = json.load(open(sys.argv[2]))
out = []
for d in dags:
    p = d["p"]
    G = nx.DiGraph(); G.add_nodes_from(range(p)); G.add_edges_from(map(tuple, d["edges"]))
    data = np.zeros((10, p))
    with contextlib.redirect_stdout(io.StringIO()), joblib.parallel_backend("threading"):
        g, _ = fci(data, "d_separation", 0.05, true_dag=G, show_progress=False, verbose=False)
    out.append(sorted([i, j] for i in range(p) for j in range(i + 1, p) if g.graph[i, j] != 0))
print(json.dumps(out))
'''
    tmp = Path(tempfile.mkdtemp())
    json.dump(dags[:n_dags], open(tmp / "d.json", "w"))
    (tmp / "w.py").write_text(code)
    runs = []
    for _ in range(nperm_runs):
        p = subprocess.run([sys.executable, str(tmp / "w.py"), vendored, str(tmp / "d.json")], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=""))
        if p.returncode:
            return {"error": p.stderr[-400:]}
        runs.append(json.loads(p.stdout.strip().splitlines()[-1]))
    differing = sum(1 for k in range(len(runs[0])) if len({json.dumps(r[k]) for r in runs}) > 1)
    return {"engine": "Causal-Copilot vendored causal-learn FCI, joblib threading", "runs": nperm_runs, "dags": len(runs[0]),
            "dags_with_differing_output": differing}


def classify(s):
    if s.get("runs", 0) == 0:
        return "not run"
    if s["exact_equivalence_class"] == s["runs"]:
        return "correct"
    cls = []
    if s["skeleton_extra_adjacencies"]:
        cls.append("extra adjacency")
    if s["skeleton_missing_adjacencies"]:
        cls.append("missing adjacency")
    if not cls:
        cls.append("orientation only")
    if s["dags_order_invariant"] < s["dags"]:
        cls.append("order dependent")
    return ", ".join(cls)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--python2", required=True, help="python with pgmpy, dodiscover, tigramite")
    ap.add_argument("--vendored", default=None, help="Causal-Copilot externals/causal-learn, for the determinism check")
    ap.add_argument("--dags", type=int, default=120)
    ap.add_argument("--perms", type=int, default=6)
    ap.add_argument("--seed", type=int, default=20261013)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", nargs="*", default=["pgmpy", "dodiscover", "tigramite"])
    ap.add_argument("--_worker", nargs=3, help=argparse.SUPPRESS)
    a = ap.parse_args()
    if a._worker:
        worker(a._worker[0], a._worker[1], a._worker[2], a.perms)
        return
    dags = random_dags(a.dags, a.seed)
    tmp = Path(tempfile.mkdtemp())
    json.dump(dags, open(tmp / "dags.json", "w"))
    report = {"tickets": ["AUD-35", "AUD-23", "CAP-05", "CAP-11"], "dags": a.dags, "perms_per_dag": a.perms, "seed": a.seed,
              "same_dags_as": "analysis/results/engine_oracle/oracle.json (AUD-27)", "engines": {}, "errors": {}}
    keys = {"pgmpy": ["pgmpy_%s_%s" % (v, t) for v in ("orig", "stable", "parallel") for t in ("unbounded", "default5")],
            "dodiscover": ["dodiscover_pc", "dodiscover_fci_skeleton"], "tigramite": ["tigramite_pcmciplus"]}
    for kind in a.only:
        out = tmp / ("%s.json" % kind)
        subprocess.run([a.python2, __file__, "--python2", a.python2, "--perms", str(a.perms), "--out", str(tmp), "--_worker", kind,
                        str(tmp / "dags.json"), str(out)], check=True, env=dict(os.environ, PYTHONPATH=""))
        res = json.load(open(out))
        errs = [r["error"] for r in res if "error" in r]
        if errs:
            report["errors"][kind] = {"count": len(errs), "first": errs[0]}
        for k in keys[kind]:
            key = "fci_skeleton" if k.endswith("fci_skeleton") else k
            if key == "fci_skeleton":
                sub = [dict(r, fci_skeleton=r[k]) for r in res if k in r]
            else:
                sub = res
            s = summarise(dags, sub, key)
            s["defect_class"] = classify(s)
            if kind == "tigramite":
                s["runs_with_conflict_marks"] = sum(1 for r in res if r.get("tigramite_conflicts"))
            report["engines"][k] = s
            print("%-32s %s" % (k, s))
    if a.vendored:
        report["determinism"] = determinism(a.vendored, dags)
        print("determinism", report["determinism"])
    os.makedirs(a.out, exist_ok=True)
    json.dump(report, open(os.path.join(a.out, "forensics.json"), "w"), indent=1)
    json.dump({"producer": "analysis/engine_forensics.py", "score_bearing": False, "tickets": report["tickets"]},
              open(os.path.join(a.out, "CONTRACT.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
