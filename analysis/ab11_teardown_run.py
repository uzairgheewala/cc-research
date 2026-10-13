"""AB-11 hands-on teardown (AUD-42, CAP-09): run each open causal-discovery tool on one public CausalArena file, test its
knowledge interface empirically, check column-order invariance, map its output to a claim ledger and verify it.

  nice /home/claude/work/engines/venv/bin/python analysis/ab11_teardown_run.py            # everything (one command)
  ... analysis/ab11_teardown_run.py --tools tigramite lingam                              # a subset (merges into teardown.json)
  <tool venv>/bin/python analysis/ab11_teardown_run.py --worker TOOL --out DIR             # internal: one tool in its venv

Scenario: semantic_cybersecurity_and_it_operations_api_rate_limit_abuse_spillover, obs only, rep000 (25 variables, 1000 rows).
Truth g[i, j] == 1 means i -> j. Columns are always shown to a tool in a shuffled order:
  perm = numpy.random.default_rng(seed + zlib.crc32(file name)).permutation(d)     (same rule as baseline_variants_run.py
  and harness/agent_probe.py); the tool sees column k = original column perm[k]; results are mapped back by name.
Main order: seed 20261010. Order check (V7, empirical): seeds 20261010, 1, 2.

Knowledge tests, each a separate run on the seed-20261010 order through the tool's documented interface:
  (i)   required edge a->b on a pair the data-only run left unconnected (first true edge in (i, j) order that the run left
        unconnected; fallback: first unconnected pair). Question: is a connection added (a V3 failure)?
  (ii)  forbidden edge a->b on an adjacency the data-only run found (first committed arrow in (i, j) order; fallback: first
        undirected pair). Question: is a->b still asserted (committed, or left open) afterwards (V5)?
  (iii) tier ordering: tier 0 = original columns 0..11 (all exogenous in the truth), tier 1 = 12..24; no within-tier rule.
        Question: does any arrow point from tier 1 into tier 0, and are cross-tier adjacencies oriented?
CI-based tools use alpha 0.05 (one value for all, so differences are behaviour, not settings). No LLM calls anywhere:
PyWhy-LLM is run only through the AB-05 probe's --stub path (offline fake LLM, answers seeded by prompt hash).
Writes analysis/results/teardown/{teardown.json, CONTRACT.json, raw/<tool>/..., ledgers/<tool>__<regime>.json}.
"""
import argparse, hashlib, io, json, logging, os, pickle, subprocess, sys, time, traceback, warnings, zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
WORK = KIT.parent
CC_ANALYSIS = WORK / "run_pc" / "cc-research" / "analysis"
SCENARIO = WORK / "run_pc/cc-research/external/causalarena/scm/semantic/data/semantic_obs_only" / \
    "semantic_cybersecurity_and_it_operations_api_rate_limit_abuse_spillover__semantic_obs_only__rep000.npz"
OUT = HERE / "results" / "teardown"
MAIN_SEED, ORDER_SEEDS = 20261010, (20261010, 1, 2)
ALPHA = 0.05
TIER0 = list(range(12))  # original indices 0..11: no parents in the truth (checked at run time)

PY = {"venv": WORK / "engines/venv/bin/python", "venv2": WORK / "engines/venv2/bin/python",
      "teardown": WORK / "agents/venv_teardown/bin/python", "causalnex": WORK / "agents/venv_teardown_causalnex/bin/python",
      "probe": WORK / "agents/venv_probe/bin/python"}
TOOLS = {  # row label: (venv, documented interface used)
    "dowhy+causal-learn": ("teardown", "causallearn.search.ConstraintBased.PC.pc + BackgroundKnowledge; graph handed to dowhy.CausalModel"),
    "pgmpy-pc": ("venv2", "pgmpy.causal_discovery.PC(variant='stable') + ExpertKnowledge (enforce_expert_knowledge False and True)"),
    "pgmpy-hillclimb": ("venv2", "pgmpy.causal_discovery.HillClimbSearch(scoring_method='bic-g') + ExpertKnowledge"),
    "causalnex": ("causalnex", "causalnex.structure.notears.from_pandas(w_threshold=0.3, tabu_edges=...) + StructureModel.add_edge(origin=...)"),
    "dodiscover": ("venv2", "dodiscover.PC(FisherZCITest) + make_context().included_edges/excluded_edges"),
    "tigramite": ("venv2", "PCMCI.run_pcmciplus(tau_max=0, ParCorr, link_assumptions)"),
    "gcastle": ("venv", "castle.algorithms.PC(variant='parallel', p_cores=1) + PrioriKnowledge"),
    "lingam": ("teardown", "lingam.DirectLiNGAM(prior_knowledge=matrix)"),
    "py-tetrad": ("teardown", "edu.cmu.tetrad.search.Pc(IndTestFisherZ) + edu.cmu.tetrad.data.Knowledge via JPype (py-tetrad jar)"),
    "pywhy-llm": ("probe", "harness/agent_probe.py --agent pywhyllm --stub (ModelSuggester Pairwise)"),
}


# ----------------------------------------------------------------------------------------------------------------- data
def load_scenario():
    sys.path.insert(0, str(CC_ANALYSIS))
    import causalarena_io as CA
    s = CA.load(SCENARIO)
    X = s["values"][: s["n_obs"]]
    return X, s["node_ids"], s["g"]


def perm_for(seed, d):
    return [int(p) for p in np.random.default_rng(seed + zlib.crc32(SCENARIO.name.encode())).permutation(d)]


def sha_array(a):
    return hashlib.sha256(np.ascontiguousarray(np.asarray(a, dtype="<f8")).tobytes()).hexdigest()


def var_id(col, name):
    return hashlib.sha256(np.ascontiguousarray(np.asarray(col, dtype="<f8")).tobytes() + name.encode("utf-8")).hexdigest()


def version_of(dist):
    try:
        from importlib.metadata import version, distribution
        v = version(dist)
        try:
            du = json.loads(distribution(dist).read_text("direct_url.json") or "{}")
            if du.get("vcs_info"):
                v += " (git %s %s)" % (du["url"], du["vcs_info"].get("commit_id", "")[:12])
        except Exception:  # noqa: BLE001
            pass
        return v
    except Exception:  # noqa: BLE001
        return None


# ------------------------------------------------------------------------------------------------- tool implementations
# Each discover(df, K) takes the shown-order DataFrame and knowledge by NAME (None = data only) and returns a dict:
#   directed [(a, b)], undirected [(a, b)], other [(a, b, mark)], sepsets [(a, b, [cond], p or None, field)],
#   adj_tests [(a, b, p, stat, field)], edge_meta [(a, b, {..})], raw (object), info {..}

def _cl_graph(G, names):
    d = len(names)
    out = {"directed": [], "undirected": [], "other": []}
    for i in range(d):
        for j in range(i + 1, d):
            a, b = G[i, j], G[j, i]
            if a == 0 and b == 0:
                continue
            if a == -1 and b == 1:
                out["directed"].append((names[i], names[j]))
            elif a == 1 and b == -1:
                out["directed"].append((names[j], names[i]))
            elif a == -1 and b == -1:
                out["undirected"].append((names[i], names[j]))
            else:
                out["other"].append((names[i], names[j], "G[i,j]=%d,G[j,i]=%d" % (a, b)))
    return out


def tool_causallearn(df, K):
    sys.path.insert(0, str(WORK / "engines" / "cl_0.1.4.8"))
    from causallearn.search.ConstraintBased.PC import pc
    from causallearn.utils.PCUtils.BackgroundKnowledge import BackgroundKnowledge
    from causallearn.graph.GraphNode import GraphNode
    import causallearn
    names = list(df.columns)
    bk = None
    if K:
        bk = BackgroundKnowledge()
        for a, b in K.get("required", []):
            bk.add_required_by_node(GraphNode(a), GraphNode(b))
        for a, b in K.get("forbidden", []):
            bk.add_forbidden_by_node(GraphNode(a), GraphNode(b))
        for t, tier in enumerate(K.get("tiers", [])):
            for n in tier:
                bk.add_node_to_tier(GraphNode(n), t)
    cg = pc(df.values, alpha=ALPHA, indep_test="fisherz", stable=True, uc_rule=0, uc_priority=2, background_knowledge=bk,
            show_progress=False, node_names=names)
    res = _cl_graph(cg.G.graph, names)
    seps = []
    d = len(names)
    for i in range(d):
        for j in range(i + 1, d):
            s = cg.sepset[i, j]
            if s is not None and cg.G.graph[i, j] == 0 and cg.G.graph[j, i] == 0:
                for S in s:
                    seps.append((names[i], names[j], [names[k] for k in S], None, "cg.sepset"))
    res.update(sepsets=seps, adj_tests=[], edge_meta=[], raw=cg,
               info={"settings": "alpha=%s fisherz stable=True uc_rule=0 uc_priority=2" % ALPHA,
                     "causallearn_path": causallearn.__file__,
                     "pvalue_cache_entries_internal": len(getattr(cg.test, "pvalue_cache", {}) or {})})
    if K is None:
        res["info"]["dowhy"] = _dowhy_handoff(df, res)
    return res


def _dowhy_handoff(df, res):
    """Hand the causal-learn output to DoWhy the documented way (CausalModel(graph=...)) and record what DoWhy keeps."""
    out = {"version": version_of("dowhy")}
    try:
        import networkx as nx
        from dowhy import CausalModel
        G = nx.DiGraph()
        G.add_nodes_from(df.columns)
        G.add_edges_from(res["directed"])
        for a, b in res["undirected"]:
            G.add_edges_from([(a, b), (b, a)])
        t, o = res["directed"][0] if res["directed"] else (df.columns[0], df.columns[1])
        out["graph_given"] = "nx.DiGraph: committed arrows, undirected pairs as two opposite arrows"
        out["graph_is_dag"] = nx.is_directed_acyclic_graph(G)
        try:
            m = CausalModel(data=df, treatment=t, outcome=o, graph=G)
            out["causalmodel_accepted_cyclic_cpdag"] = True
            g2 = getattr(m, "_graph", None)
            out["what_dowhy_keeps"] = "graph only (%s); no sepset, p-value or orientation source survives" % type(g2).__name__
            try:
                m.identify_effect(proceed_when_unidentifiable=True)
                out["identify_effect_on_cpdag"] = "returned"
            except Exception as e:  # noqa: BLE001
                out["identify_effect_on_cpdag"] = "raised %s: %s" % (type(e).__name__, str(e)[:200])
        except Exception as e:  # noqa: BLE001
            out["causalmodel_accepted_cyclic_cpdag"] = False
            out["causalmodel_error"] = "%s: %s" % (type(e).__name__, str(e)[:300])
    except Exception as e:  # noqa: BLE001
        out["error"] = "%s: %s" % (type(e).__name__, str(e)[:300])
    return out


def _pgmpy_pdag(pdag):
    return {"directed": [tuple(e) for e in sorted(pdag.directed_edges)],
            "undirected": [tuple(e) for e in sorted(pdag.undirected_edges)], "other": []}


def _pgmpy_ek(K):
    from pgmpy.causal_discovery import ExpertKnowledge
    if not K:
        return None
    kw = {}
    if K.get("required"):
        kw["required_edges"] = [tuple(e) for e in K["required"]]
    if K.get("forbidden"):
        kw["forbidden_edges"] = [tuple(e) for e in K["forbidden"]]
    if K.get("tiers"):
        kw["temporal_order"] = [list(t) for t in K["tiers"]]
    return ExpertKnowledge(**kw)


def tool_pgmpy_pc(df, K):
    from pgmpy.causal_discovery import PC
    enforce = bool(K and K.get("enforce"))
    est = PC(variant="stable", ci_test=None, significance_level=ALPHA, expert_knowledge=_pgmpy_ek(K),
             enforce_expert_knowledge=enforce, n_jobs=1, show_progress=False)
    est.fit(df)
    res = _pgmpy_pdag(est.causal_graph_)
    seps = [(sorted(p)[0], sorted(p)[1], sorted(map(str, S)), None, "separating_sets_") for p, S in est.separating_sets_.items()
            if not est.skeleton_.has_edge(*sorted(p))]
    ci = getattr(est, "ci_test_", None)
    res.update(sepsets=seps, adj_tests=[], edge_meta=[], raw=est,
               info={"settings": "variant=stable ci_test=None(auto) significance_level=%s max_cond_vars=5 enforce_expert_knowledge=%s"
                                 % (ALPHA, enforce), "ci_test_chosen": getattr(ci, "__name__", type(ci).__name__)})
    return res


def tool_pgmpy_hc(df, K):
    from pgmpy.causal_discovery import HillClimbSearch
    est = HillClimbSearch(scoring_method="bic-g", expert_knowledge=_pgmpy_ek(K), show_progress=False)
    est.fit(df)
    res = _pgmpy_pdag(est.causal_graph_)
    res.update(sepsets=[], adj_tests=[], edge_meta=[], raw=est,
               info={"settings": "scoring_method=bic-g tabu_length=100 return_type=pdag (default) epsilon=1e-4"})
    return res


def tool_causalnex(df, K):
    from causalnex.structure.notears import from_pandas
    tabu = []
    if K:
        tabu += [tuple(e) for e in K.get("forbidden", [])]
        if K.get("tiers"):
            t0, t1 = K["tiers"]
            tabu += [(b, a) for a in t0 for b in t1]   # no interface for tiers: every later->earlier edge is tabu
    sm = from_pandas(df, w_threshold=0.3, tabu_edges=tabu or None)
    meta_before = {(u, v): dict(dd) for u, v, dd in sm.edges(data=True)}
    if K and K.get("required"):
        for a, b in K["required"]:
            sm.add_edge(a, b, origin="expert")       # the only documented way to require an edge: post-hoc
    res = {"directed": [], "undirected": [], "other": []}
    meta = []
    for u, v, dd in sm.edges(data=True):
        res["directed"].append((u, v))
        meta.append((u, v, {k: (float(x) if isinstance(x, (int, float, np.floating)) else str(x)) for k, x in dd.items()}))
    info = {"settings": "from_pandas max_iter=100 h_tol=1e-8 w_threshold=0.3 (Zheng et al. 2018 reference threshold; "
                        "the CausalNex tutorial uses remove_edges_below_threshold(0.8))",
            "tabu_edges": len(tabu), "edges_at_tutorial_threshold_0.8": sum(1 for x in meta_before.values() if abs(x.get("weight", 0)) >= 0.8),
            "origin_counts": {}}
    for _, _, m in meta:
        info["origin_counts"][m.get("origin")] = info["origin_counts"].get(m.get("origin"), 0) + 1
    if K and K.get("required"):  # the tutorial's form (no origin argument): what does the edge get?
        import copy
        sm2 = copy.deepcopy(sm)
        a, b = K["required"][0]
        sm2.remove_edge(a, b)
        sm2.add_edge(a, b)
        info["add_edge_without_origin_gets"] = sm2.edges[a, b].get("origin")
    res.update(sepsets=[], adj_tests=[], edge_meta=meta, raw=sm, info=info)
    return res


def tool_dodiscover(df, K):
    import networkx as nx
    from dodiscover import PC, make_context
    from dodiscover.ci import FisherZCITest
    b = make_context().variables(data=df)
    gtype = nx.DiGraph if (K and K.get("digraph")) else nx.Graph   # Context declares included/excluded_edges: nx.Graph
    if K and K.get("required"):
        g = gtype()
        g.add_edges_from(K["required"])
        b = b.included_edges(g)
    if K and K.get("forbidden"):
        g = gtype()
        g.add_edges_from(K["forbidden"])
        b = b.excluded_edges(g)
    ctx = b.build()
    pc = PC(ci_estimator=FisherZCITest(), alpha=ALPHA, n_jobs=1)
    pc.learn_graph(df, ctx)
    G = pc.graph_
    res = {"directed": sorted((str(u), str(v)) for u, v in G.sub_directed_graph().edges),
           "undirected": sorted(tuple(sorted((str(u), str(v)))) for u, v in G.sub_undirected_graph().edges), "other": []}
    adj = {frozenset(e) for e in res["directed"]} | {frozenset(e) for e in res["undirected"]}
    seps, seen = [], set()
    for x, inner in pc.separating_sets_.items():
        for y, sets in inner.items():
            key = frozenset((str(x), str(y)))
            if key in seen or key in adj or not sets:
                continue
            seen.add(key)
            a, c = sorted(key)
            for S in sets:
                seps.append((a, c, sorted(map(str, S)), None, "separating_sets_"))
    res.update(sepsets=seps, adj_tests=[], edge_meta=[], raw={"graph_": G, "separating_sets_": {str(k): {str(k2): [sorted(map(str, s)) for s in v2] for k2, v2 in v.items()} for k, v in pc.separating_sets_.items()}},
               info={"settings": "PC(FisherZCITest(), alpha=%s), default condsel NBRS" % ALPHA,
                     "tiers_interface": "none (Context has included/excluded edges, init_graph, state variables; no tiers)"})
    return res


def tool_tigramite(df, K):
    from tigramite.pcmci import PCMCI
    from tigramite.independence_tests.parcorr import ParCorr
    import tigramite.data_processing as pp
    names = list(df.columns)
    d = len(names)
    ix = {n: k for k, n in enumerate(names)}
    la = None
    if K:
        la = {j: {(i, 0): "o?o" for i in range(d) if i != j} for j in range(d)}
        for a, b in K.get("required", []):
            la[ix[b]][(ix[a], 0)] = "-->"
            la[ix[a]][(ix[b], 0)] = "<--"
        for a, b in K.get("forbidden", []):          # a->b forbidden: if the link exists it is b->a
            la[ix[b]][(ix[a], 0)] = "<?-"
            la[ix[a]][(ix[b], 0)] = "-?>"
        if K.get("tiers"):
            t0, t1 = K["tiers"]
            for a in t0:
                for b in t1:
                    la[ix[b]][(ix[a], 0)] = "-?>"
                    la[ix[a]][(ix[b], 0)] = "<?-"
    pcmci = PCMCI(dataframe=pp.DataFrame(df.values, var_names=names), cond_ind_test=ParCorr(significance="analytic"), verbosity=0)
    r = pcmci.run_pcmciplus(tau_min=0, tau_max=0, pc_alpha=ALPHA, link_assumptions=la)
    gr, P, V = r["graph"][:, :, 0], r["p_matrix"][:, :, 0], r["val_matrix"][:, :, 0]
    res = {"directed": [], "undirected": [], "other": []}
    adj_tests, seps = [], []
    for i in range(d):
        for j in range(i + 1, d):
            m = str(gr[i, j])
            if m == "-->":
                res["directed"].append((names[i], names[j]))
            elif m == "<--":
                res["directed"].append((names[j], names[i]))
            elif m == "o-o":
                res["undirected"].append((names[i], names[j]))
            elif m:
                res["other"].append((names[i], names[j], m))
            if m:
                adj_tests.append((names[i], names[j], float(P[i, j]), float(V[i, j]), "p_matrix,val_matrix"))
    for key, S in (r.get("sepsets") or {}).items():
        try:
            (i, tau), j = key
        except (TypeError, ValueError):
            continue
        if tau != 0 or str(gr[i, j]) or i == j:
            continue
        a, c = sorted((names[i], names[j]))
        if any(s[0] == a and s[1] == c for s in seps):
            continue
        seps.append((a, c, sorted(names[k] for k, _ in S), float(P[i, j]), "sepsets + p_matrix (max p over tests)"))
    res.update(sepsets=seps, adj_tests=adj_tests, edge_meta=[], raw=r,
               info={"settings": "run_pcmciplus tau_min=0 tau_max=0 pc_alpha=%s ParCorr(analytic) contemp_collider_rule=majority "
                                 "conflict_resolution=True (defaults; documented as order independent)" % ALPHA,
                     "ambiguous_triples": len(r.get("ambiguous_triples") or []), "result_keys": sorted(r.keys())})
    return res


def tool_gcastle(df, K):
    sys.path.insert(0, str(WORK / "engines" / "gc"))
    sys.path.insert(0, str(HERE))
    from engine_shims import torch_stub
    torch_stub()
    from castle.algorithms import PC
    from castle.common.priori_knowledge import PrioriKnowledge
    names = list(df.columns)
    d = len(names)
    ix = {n: k for k, n in enumerate(names)}
    pk = None
    info = {"settings": "PC(variant='parallel', alpha=%s, ci_test='fisherz'), learn(p_cores=1)" % ALPHA}
    if K:
        pk = PrioriKnowledge(d)
        if K.get("required"):
            pk.add_required_edges([(ix[a], ix[b]) for a, b in K["required"]])
        if K.get("forbidden"):
            pk.add_forbidden_edges([(ix[a], ix[b]) for a, b in K["forbidden"]])
        if K.get("tiers"):
            t0, t1 = K["tiers"]
            pk.add_forbidden_edges([(ix[b], ix[a]) for a in t0 for b in t1])
            info["tiers_interface"] = "none; tiers encoded as forbidden later->earlier edges (PrioriKnowledge)"
    pc = PC(variant="parallel", alpha=ALPHA, ci_test="fisherz", priori_knowledge=pk)
    pc.learn(df.values, columns=names, p_cores=1)
    M = np.asarray(pc.causal_matrix)
    res = {"directed": [], "undirected": [], "other": []}
    for i in range(d):
        for j in range(i + 1, d):
            if M[i, j] and M[j, i]:
                res["undirected"].append((names[i], names[j]))
            elif M[i, j]:
                res["directed"].append((names[i], names[j]))
            elif M[j, i]:
                res["directed"].append((names[j], names[i]))
    res.update(sepsets=[], adj_tests=[], edge_meta=[], raw={"causal_matrix": M, "columns": names}, info=info)
    return res


def tool_lingam(df, K):
    import lingam
    names = list(df.columns)
    d = len(names)
    ix = {n: k for k, n in enumerate(names)}
    pk = None
    if K:
        pk = -np.ones((d, d), dtype=int)
        np.fill_diagonal(pk, -1)
        for a, b in K.get("required", []):
            pk[ix[b], ix[a]] = 1        # "x_a has a directed path to x_b"
        for a, b in K.get("forbidden", []):
            pk[ix[b], ix[a]] = 0        # "x_a has no directed path to x_b" (paths, not edges)
        if K.get("tiers"):
            t0, t1 = K["tiers"]
            for a in t0:
                for b in t1:
                    pk[ix[a], ix[b]] = 0  # later tier has no path into earlier tier
    m = lingam.DirectLiNGAM(random_state=0, prior_knowledge=pk)
    m.fit(df.values)
    B = m.adjacency_matrix_
    res = {"directed": [], "undirected": [], "other": []}
    meta = []
    for i in range(d):
        for j in range(d):
            if i != j and B[i, j] != 0:
                res["directed"].append((names[j], names[i]))
                meta.append((names[j], names[i], {"weight": float(B[i, j])}))
    res.update(sepsets=[], adj_tests=[], edge_meta=meta, raw={"adjacency_matrix_": B, "causal_order_": [names[k] for k in m.causal_order_]},
               info={"settings": "DirectLiNGAM(random_state=0, measure='pwling', prune: adaptive lasso)",
                     "prior_knowledge_semantics": "matrix of directed PATHS (0 = no path, 1 = path), not edges"})
    return res


_JVM = {}


def tool_tetrad(df, K):
    import jpype, jpype.imports
    import importlib.resources as ir
    if not jpype.isJVMStarted():
        jar = str(ir.files("pytetrad").joinpath("resources", "tetrad-current.jar"))
        jpype.startJVM("-Xmx1g", classpath=[jar])
        _JVM["jar"] = jar
    import pytetrad.tools.translate as ptt
    import edu.cmu.tetrad.search as ts
    import edu.cmu.tetrad.data as td
    import java.io as jio
    from edu.cmu.tetrad.util import Version
    data = ptt.pandas_data_to_tetrad(df)
    test = ts.test.IndTestFisherZ(data, ALPHA)
    alg = ts.Pc(test)
    alg.setFasStable(True)
    if K:
        kn = td.Knowledge()
        for a, b in K.get("required", []):
            kn.setRequired(a, b)
        for a, b in K.get("forbidden", []):
            kn.setForbidden(a, b)
        for t, tier in enumerate(K.get("tiers", [])):
            for n in tier:
                kn.addToTier(t, n)
        alg.setKnowledge(kn)
    buf, out_buf = jio.ByteArrayOutputStream(), jio.ByteArrayOutputStream()
    import java.lang as jl
    old_out = jl.System.out
    alg.setVerbose(True)
    alg.setLogStream(jio.PrintStream(buf))
    jl.System.setOut(jio.PrintStream(out_buf))      # TetradLogger writes the verbose decisions to System.out
    try:
        g = alg.search()
    finally:
        jl.System.setOut(old_out)
    log = str(buf.toString()) + str(out_buf.toString())
    res = {"directed": [], "undirected": [], "other": []}
    for e in g.getEdges():
        a, b = str(e.getNode1().getName()), str(e.getNode2().getName())
        e1, e2 = str(e.getEndpoint1()), str(e.getEndpoint2())
        if e1 == "TAIL" and e2 == "ARROW":
            res["directed"].append((a, b))
        elif e1 == "ARROW" and e2 == "TAIL":
            res["directed"].append((b, a))
        elif e1 == "TAIL" and e2 == "TAIL":
            res["undirected"].append(tuple(sorted((a, b))))
        else:
            res["other"].append(tuple(sorted((a, b))) + ("%s-%s" % (e1, e2),))
    seps, sep_note = [], None
    try:
        fas = alg.getFas()
        ss = fas.getSepsets() if fas is not None else None
        if ss is not None:
            nodes = list(data.getVariables())
            adj = {frozenset(e[:2]) for e in res["directed"] + res["undirected"] + [x[:2] for x in res["other"]]}
            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    a, b = str(nodes[i].getName()), str(nodes[j].getName())
                    if frozenset((a, b)) in adj:
                        continue
                    S = ss.get(nodes[i], nodes[j])
                    if S is not None:
                        seps.append((min(a, b), max(a, b), sorted(str(n.getName()) for n in S), None, "getFas().getSepsets()"))
        else:
            sep_note = "getFas() or getSepsets() returned null"
    except Exception as ex:  # noqa: BLE001
        sep_note = "%s: %s" % (type(ex).__name__, str(ex)[:200])
    import re
    log_tests, rules = [], []
    for ln in log.splitlines():
        m = re.match(r"Independence accepted: (\S+) _\|\|_ (\S+)(?: \| (.*?))?\tp = (\S+)", ln)
        if m:
            a, b, c, pv = m.groups()
            try:
                pv = float(pv)
            except ValueError:
                pv = None
            log_tests.append((min(a, b), max(a, b), sorted(x.strip() for x in c.split(",")) if c else [], pv,
                              "verbose log (System.out): 'Independence accepted'"))
        m = re.match(r"Collider oriented: (\S+) -> (\S+) <- (\S+)", ln)
        if m:
            a, b, c = m.groups()
            rules += [(a, b, c, "v_structure", "verbose log (System.out): 'Collider oriented'"), (c, b, a, "v_structure", "verbose log (System.out): 'Collider oriented'")]
    res.update(sepsets=log_tests, adj_tests=[], edge_meta=[], rule_records=rules, raw={"graph_text": str(g.toString()), "verbose_log": log},
               info={"settings": "Pc(IndTestFisherZ alpha=%s), setFasStable(True), defaults otherwise" % ALPHA,
                     "tetrad_version": str(Version.currentViewableVersion()), "jar": _JVM.get("jar"),
                     "verbose_log_lines": len(log.splitlines()), "sepset_note": sep_note, "getSepsets_records": len(seps),
                     "evidence_source": "the verbose log's 'Independence accepted' lines (pair, conditioning set, p) are used as the CI records; "
                                        "getFas().getSepsets() gives the same pairs and sets without p-values",
                     "verbose_line_kinds": _line_kinds(log),
                     "verbose_log_head": log.splitlines()[:6]})
    return res


def _line_kinds(log):
    kinds = {}
    for ln in log.splitlines():
        k = " ".join(ln.split(":")[0].split()[:3]) if ":" in ln else " ".join(ln.split()[:2])
        kinds[k] = kinds.get(k, 0) + 1
    return dict(sorted(kinds.items(), key=lambda x: -x[1])[:12])


IMPLS = {"dowhy+causal-learn": tool_causallearn, "pgmpy-pc": tool_pgmpy_pc, "pgmpy-hillclimb": tool_pgmpy_hc,
         "causalnex": tool_causalnex, "dodiscover": tool_dodiscover, "tigramite": tool_tigramite, "gcastle": tool_gcastle,
         "lingam": tool_lingam, "py-tetrad": tool_tetrad}
DISTS = {"dowhy+causal-learn": ["dowhy", "causal-learn"], "pgmpy-pc": ["pgmpy"], "pgmpy-hillclimb": ["pgmpy"],
         "causalnex": ["causalnex", "torch"], "dodiscover": ["dodiscover", "pywhy-graphs"], "tigramite": ["tigramite"],
         "gcastle": ["gcastle"], "lingam": ["lingam"], "py-tetrad": ["py-tetrad", "JPype1"], "pywhy-llm": ["pywhy-llm", "guidance"]}


TIER_IF = {"dodiscover": None, "gcastle": "none; emulated with PrioriKnowledge forbidden later->earlier edges",
           "causalnex": "none; emulated with tabu_edges later->earlier", "lingam": "via prior_knowledge path matrix (no path later->earlier)"}


# -------------------------------------------------------------------------------------------------------------- worker
def pick_knowledge(D, g, names):
    """D: data-only output in ORIGINAL indices. Returns knowledge by original index, with the rule used."""
    d = len(names)
    adj = {frozenset(e) for e in D["directed"]} | {frozenset(e) for e in D["undirected"]} | {frozenset(e[:2]) for e in D["other"]}
    true = sorted((int(i), int(j)) for i, j in np.argwhere(np.asarray(g) != 0))
    req = next(((i, j) for i, j in true if frozenset((i, j)) not in adj), None)
    req_rule = "first true edge (i, j order) the data-only run left unconnected"
    if req is None:
        req = next(((i, j) for i in range(d) for j in range(i + 1, d) if frozenset((i, j)) not in adj), None)
        req_rule = "first unconnected pair (no true edge was unconnected)"
    if D["directed"]:
        forb, forb_rule = tuple(sorted(D["directed"])[0]), "first committed arrow (i, j order) of the data-only run"
    elif D["undirected"]:
        forb, forb_rule = tuple(sorted(D["undirected"])[0]), "first undirected pair (no committed arrow)"
    else:
        forb, forb_rule = None, "the data-only run found no adjacency"
    parents_of_tier0 = [(int(i), int(j)) for i, j in true if j in TIER0]
    tiers = [TIER0, [k for k in range(d) if k not in TIER0]]
    return {"required": req, "required_rule": req_rule, "forbidden": forb, "forbidden_rule": forb_rule, "tiers": tiers,
            "tiers_rule": "tier 0 = original columns 0..11, tier 1 = 12..24; true edges into tier 0: %d" % len(parents_of_tier0)}


def to_orig(res, ix):
    o = {"directed": sorted([ix[a], ix[b]] for a, b in res["directed"]),
         "undirected": sorted(sorted([ix[a], ix[b]]) for a, b in res["undirected"]),
         "other": sorted(sorted([ix[x[0]], ix[x[1]]]) + [x[2]] for x in res["other"]),
         "sepsets": [[ix[a], ix[b], sorted(ix[c] for c in S), p, f] for a, b, S, p, f in res["sepsets"]],
         "adj_tests": [[ix[a], ix[b], p, s, f] for a, b, p, s, f in res["adj_tests"]],
         "edge_meta": [[ix[a], ix[b], m] for a, b, m in res["edge_meta"]],
         "rule_records": [[ix[a], ix[b], ix[c], r, f] for a, b, c, r, f in res.get("rule_records", [])]}
    return o


def worker(tool, outdir):
    import pandas as pd
    outdir = Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    X, names, g = load_scenario()
    d = len(names)
    ix = {n: k for k, n in enumerate(names)}
    impl = IMPLS[tool]
    logrec = io.StringIO()
    h = logging.StreamHandler(logrec)
    h.setLevel(logging.WARNING)
    logging.getLogger().addHandler(h)

    def run(seed, K_orig, label, extra=None):
        perm = perm_for(seed, d)
        df = pd.DataFrame(X[:, perm], columns=[names[k] for k in perm])
        K = None
        if K_orig is not None:
            K = {}
            if K_orig.get("required"):
                K["required"] = [(names[K_orig["required"][0]], names[K_orig["required"][1]])]
            if K_orig.get("forbidden"):
                K["forbidden"] = [(names[K_orig["forbidden"][0]], names[K_orig["forbidden"][1]])]
            if K_orig.get("tiers"):
                K["tiers"] = [[names[k] for k in t] for t in K_orig["tiers"]]
            K.update(extra or {})
        t0 = time.process_time()
        w0 = time.time()
        logrec.truncate(0), logrec.seek(0)
        with warnings.catch_warnings(record=True) as wl:
            warnings.simplefilter("always")
            try:
                res = impl(df, K)
                err = None
            except Exception as e:  # noqa: BLE001
                res, err = None, "%s: %s\n%s" % (type(e).__name__, str(e)[:500], traceback.format_exc()[-1500:])
        rec = {"label": label, "shuffle_seed": seed, "perm": perm, "knowledge_by_name": K, "cpu_s": round(time.process_time() - t0, 2),
               "wall_s": round(time.time() - w0, 2), "error": err,
               "warnings": sorted({str(w.message)[:300] for w in wl if "deprecat" not in str(w.message).lower()})[:20],
               "log_warnings": [x[:300] for x in logrec.getvalue().splitlines() if x.strip()][:20]}
        if res is not None:
            raw = res.pop("raw")
            rec["info"] = res.pop("info")
            rec["output"] = to_orig(res, ix)
            rec["raw_type"] = type(raw).__name__
            rec["raw_fields"] = describe(raw)
            p = outdir / ("%s.pkl" % label)
            try:
                with open(p, "wb") as f:
                    pickle.dump(raw, f)
                rec["raw_file"] = str(p.relative_to(KIT))
            except Exception as e:  # noqa: BLE001
                p = outdir / ("%s.txt" % label)
                p.write_text(repr(raw)[:2_000_000] + ("\n\n" + raw.get("verbose_log", "") if isinstance(raw, dict) else ""))
                rec["raw_file"] = str(p.relative_to(KIT))
                rec["raw_pickle_error"] = "%s: %s" % (type(e).__name__, str(e)[:200])
        print("[%s] %-22s cpu %.1fs %s" % (tool, label, rec["cpu_s"], "ERROR " + err.splitlines()[0] if err else
                                           "%d directed, %d undirected, %d other" % (len(rec["output"]["directed"]), len(rec["output"]["undirected"]), len(rec["output"]["other"]))), flush=True)
        return rec

    runs = {}
    for s in ORDER_SEEDS:
        runs["D_seed%d" % s] = run(s, None, "D_seed%d" % s)
    D = runs["D_seed%d" % MAIN_SEED]
    kp = pick_knowledge(D["output"], g, names) if D.get("output") else None
    if kp:
        if kp["required"]:
            runs["K_required"] = run(MAIN_SEED, {"required": kp["required"]}, "K_required")
        if kp["forbidden"]:
            runs["K_forbidden"] = run(MAIN_SEED, {"forbidden": kp["forbidden"]}, "K_forbidden")
        if TIER_IF.get(tool, "native") is not None:
            runs["K_tiers"] = run(MAIN_SEED, {"tiers": kp["tiers"]}, "K_tiers")
        if tool == "dodiscover":   # the same statements passed as a DiGraph (type not enforced by the builder)
            if kp["required"]:
                runs["K_required_digraph"] = run(MAIN_SEED, {"required": kp["required"]}, "K_required_digraph", {"digraph": True})
            if kp["forbidden"]:
                runs["K_forbidden_digraph"] = run(MAIN_SEED, {"forbidden": kp["forbidden"]}, "K_forbidden_digraph", {"digraph": True})
        if tool == "pgmpy-pc":   # the other documented mode
            if kp["required"]:
                runs["K_required_enforce"] = run(MAIN_SEED, {"required": kp["required"]}, "K_required_enforce", {"enforce": True})
            if kp["forbidden"]:
                runs["K_forbidden_enforce"] = run(MAIN_SEED, {"forbidden": kp["forbidden"]}, "K_forbidden_enforce", {"enforce": True})
    out = {"tool": tool, "python": sys.version.split()[0], "executable": sys.executable,
           "versions": {k: version_of(k) for k in DISTS[tool]} | {"numpy": np.__version__}, "knowledge_pick": kp, "runs": runs,
           "names": names}
    (outdir / "worker.json").write_text(json.dumps(out, indent=1, default=str))
    return out


def describe(raw):
    if isinstance(raw, dict):
        return {str(k): type(v).__name__ for k, v in raw.items()}
    attrs = {}
    for k in sorted(dir(raw)):
        if k.startswith("__"):
            continue
        try:
            v = getattr(raw, k)
        except Exception:  # noqa: BLE001
            continue
        if callable(v) and not hasattr(v, "shape"):
            continue
        attrs[k] = type(v).__name__
    return attrs


# -------------------------------------------------------------------------------------------------------- orchestrator
def run_worker(tool, raw_dir):
    venv = TOOLS[tool][0]
    py = PY[venv]
    if not py.exists():
        return {"installed": False, "error": "interpreter %s missing" % py}
    cmd = ["nice", "-n", "10", str(py), "-W", "ignore::DeprecationWarning", str(Path(__file__).resolve()), "--worker", tool, "--out", str(raw_dir)]
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONHASHSEED="0")
    t = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(KIT))
    (raw_dir / "worker_stdout.log").write_text(p.stdout + "\n--- stderr ---\n" + p.stderr[-20000:])
    print(p.stdout.strip(), flush=True)
    if p.returncode != 0 or not (raw_dir / "worker.json").exists():
        return {"installed": True, "error": "worker exit %d: %s" % (p.returncode, p.stderr[-1500:])}
    w = json.loads((raw_dir / "worker.json").read_text())
    w["wall_total_s"] = round(time.time() - t, 1)
    return w


def run_pywhyllm(raw_dir):
    """Stub only. Three column orders; no knowledge interface (the tool is the knowledge supplier)."""
    runs = {}
    env = dict(os.environ, PROBES_ROOT=str(WORK / "agents/venv_probe/probes"), PROBES_SRC=str(WORK / "agents"),
               TIKTOKEN_CACHE_DIR=str(WORK / "agents/venv_probe/tiktoken_cache"), OMP_NUM_THREADS="1")
    _, names, _ = load_scenario()
    for s in ORDER_SEEDS:
        od = raw_dir / ("seed%d" % s)
        cmd = ["nice", "-n", "10", str(PY["probe"]), str(KIT / "harness/agent_probe.py"), "--agent", "pywhyllm", "--scenario", str(SCENARIO),
               "--shuffle-seed", str(s), "--out", str(od), "--stub"]
        t0 = time.time()
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(KIT))
        print(p.stdout.strip()[-300:], flush=True)
        rec = {"label": "D_seed%d" % s, "shuffle_seed": s, "wall_s": round(time.time() - t0, 1), "error": None if p.returncode == 0 else p.stderr[-1500:]}
        if (od / "result.json").exists():
            r = json.loads((od / "result.json").read_text())
            rec["perm"] = r.get("perm")
            rec["output"] = {"directed": sorted([e["from_idx"], e["to_idx"]] for e in r["directed"]),
                             "undirected": sorted(sorted(u[:2]) for u in r.get("undecided", [])), "other": [],
                             "sepsets": [], "adj_tests": [], "edge_meta": [[e["from_idx"], e["to_idx"], {"source": e.get("source")}] for e in r["directed"]]}
            rec["info"] = {"provenance_exposed": r.get("provenance_exposed"), "decision_rule": r.get("decision_rule"),
                           "agent_notes": r.get("agent_notes"), "stub": r.get("stub")}
            rec["raw_file"] = str((od / "result.json").relative_to(KIT))
            rec["raw_fields"] = {k: type(v).__name__ for k, v in r.items()}
            sm = json.loads((od / "summary.json").read_text())
            rec["calls"] = sm.get("calls")
        runs[rec["label"]] = rec
    vers = {}
    try:
        q = subprocess.run([str(PY["probe"]), "-c", "import sys;sys.path.insert(0,%r);from importlib.metadata import version as v;"
                            "print(v('pywhy-llm') if 1 else '')" % str(WORK / "agents/venv_probe/probes/pywhyllm")],
                           capture_output=True, text=True)
        vers["pywhy-llm"] = q.stdout.strip() or None
        q = subprocess.run([str(PY["probe"]), "-c", "import sys;sys.path.insert(0,%r);from importlib.metadata import version as v;"
                            "print(v('guidance'))" % str(WORK / "agents/venv_probe/probes/pywhyllm")], capture_output=True, text=True)
        vers["guidance"] = q.stdout.strip() or None
    except Exception:  # noqa: BLE001
        pass
    head = None
    try:
        hp = WORK / "agents/pywhy-llm/.git/HEAD"
        h = hp.read_text().strip()
        head = (WORK / "agents/pywhy-llm/.git" / h.split(" ", 1)[1]).read_text().strip() if h.startswith("ref:") else h
    except OSError:
        pass
    vers["pywhy-llm_git_head"] = head
    if not vers.get("pywhy-llm"):     # used from source (PROBES_SRC), not pip-installed: read the project's own version
        try:
            import re as _re
            m = _re.search(r'^version\s*=\s*"([^"]+)"', (WORK / "agents/pywhy-llm/pyproject.toml").read_text(), _re.M)
            vers["pywhy-llm"] = (m.group(1) + " (source tree agents/pywhy-llm)") if m else None
        except OSError:
            pass
    return {"tool": "pywhy-llm", "python": "3.10 (venv_probe)", "versions": vers, "knowledge_pick": None, "runs": runs, "names": names}


def graph_key(o):
    return (tuple(map(tuple, o["directed"])), tuple(map(tuple, o["undirected"])), tuple(map(tuple, o["other"])))


def skel(o):
    return {frozenset(e[:2]) for e in o["directed"]} | {frozenset(e[:2]) for e in o["undirected"]} | {frozenset(e[:2]) for e in o["other"]}


def asserts(o, a, b):
    """Does output o still admit a->b? committed arrow, undirected, or a non-arrowhead-at-a mark."""
    if [a, b] in o["directed"]:
        return "committed a->b"
    if sorted([a, b]) in o["undirected"]:
        return "left undirected"
    for x in o["other"]:
        if sorted([a, b]) == x[:2]:
            return "other mark %s" % x[2]
    if [b, a] in o["directed"]:
        return None
    return None


def knowledge_tests(w):
    R = w["runs"]
    D = R.get("D_seed%d" % MAIN_SEED, {}).get("output")
    kp = w.get("knowledge_pick")
    if not D or not kp:
        return {"required_edge_added_connection": "na", "forbidden_honoured": "na", "tiers_honoured": "na", "detail": "no knowledge interface tested"}
    out, det = {}, {}
    sD = skel(D)
    for lab in ("K_required", "K_forbidden", "K_tiers", "K_required_enforce", "K_forbidden_enforce", "K_required_digraph", "K_forbidden_digraph"):
        r = R.get(lab)
        if not r:
            continue
        if not r.get("output"):
            det[lab] = {"error": (r.get("error") or "")[:400]}
            continue
        o = r["output"]
        sK = skel(o)
        dd = {"skeleton_added_n": len(sK - sD), "skeleton_removed_n": len(sD - sK),
              "skeleton_added": sorted(sorted(p) for p in sK - sD), "skeleton_removed": sorted(sorted(p) for p in sD - sK),
              "warnings": (r.get("warnings") or []) + (r.get("log_warnings") or [])}
        if lab.startswith("K_required"):
            a, b = kp["required"]
            dd.update(edge=[a, b], connected_after=frozenset((a, b)) in sK, oriented_a_to_b=[a, b] in o["directed"])
        elif lab.startswith("K_forbidden"):
            a, b = kp["forbidden"]
            st = asserts(o, a, b)
            dd.update(edge=[a, b], data_only_mark=asserts(D, a, b), after=st or ("reversed to b->a" if [b, a] in o["directed"] else "adjacency removed"),
                      honoured=st is None)
        else:
            t0, t1 = set(kp["tiers"][0]), set(kp["tiers"][1])
            viol = [e for e in o["directed"] if e[0] in t1 and e[1] in t0]
            cross_open = [e for e in o["undirected"] + [x[:2] for x in o["other"]] if (e[0] in t0) != (e[1] in t0)]
            cross_D = [e for e in D["directed"] if e[0] in t1 and e[1] in t0]
            dd.update(arrows_into_tier0=len(viol), cross_tier_left_open=len(cross_open), data_only_arrows_into_tier0=len(cross_D),
                      honoured=not viol and not cross_open)
        det[lab] = dd
    g = lambda lab, k: det.get(lab, {}).get(k, "na") if lab in det and "error" not in det[lab] else "na"  # noqa: E731
    out["required_edge_added_connection"] = g("K_required", "connected_after")
    out["forbidden_honoured"] = g("K_forbidden", "honoured")
    out["tiers_honoured"] = g("K_tiers", "honoured") if TIER_IF.get(w["tool"], "native") is not None else "na"
    out["tiers_interface"] = TIER_IF.get(w["tool"], "native")
    if "K_required_enforce" in det:
        out["required_edge_added_connection_enforce_true"] = g("K_required_enforce", "connected_after")
        out["forbidden_honoured_enforce_true"] = g("K_forbidden_enforce", "honoured")
    if "K_required_digraph" in det:
        out["required_edge_added_connection_as_digraph"] = g("K_required_digraph", "connected_after")
        out["forbidden_honoured_as_digraph"] = g("K_forbidden_digraph", "honoured")
    out["detail"] = det
    out["knowledge_pick"] = kp
    return out


def order_check(w):
    keys = {s: graph_key(w["runs"][lab]["output"]) for s in ORDER_SEEDS for lab in ["D_seed%d" % s] if w["runs"].get(lab, {}).get("output")}
    if len(keys) < 3:
        return "na", {"orders_completed": len(keys)}
    base = keys[MAIN_SEED]
    diffs = {}
    for s, k in keys.items():
        if s == MAIN_SEED:
            continue
        a, b = base, k
        diffs["seed%d" % s] = {"directed_only_in_main": len(set(a[0]) - set(b[0])), "directed_only_here": len(set(b[0]) - set(a[0])),
                               "undirected_only_in_main": len(set(a[1]) - set(b[1])), "undirected_only_here": len(set(b[1]) - set(a[1])),
                               "skeleton_differs": skel({"directed": list(a[0]), "undirected": list(a[1]), "other": list(a[2])}) !=
                               skel({"directed": list(b[0]), "undirected": list(b[1]), "other": list(b[2])})}
    return all(k == base for k in keys.values()), diffs


def scores(o, g, names):
    sys.path.insert(0, str(HERE))
    sys.path.insert(1, str(CC_ANALYSIS))
    import causalarena_io as CA
    from decision_value_v2 import claims
    from decision_value import reach
    d = len(names)
    T = CA.true_edges(g)
    desc = reach(d, T)
    directed = {tuple(e) for e in o["directed"]}
    und = {tuple(sorted(e[:2])) for e in o["undirected"]} | {tuple(sorted(e[:2])) for e in o["other"]}
    cl = claims(d, directed, und, list(range(d)))
    pairs = d * (d - 1)
    yes = sum(1 for v in cl.values() if v)
    yes_t = sum(1 for (t, y), v in cl.items() if v and y in desc[t])
    no_t = sum(1 for (t, y), v in cl.items() if not v and y not in desc[t])
    com = len(cl)
    empty = claims(d, set(), set(), list(range(d)))
    empty_prec = sum(1 for (t, y), v in empty.items() if y not in desc[t]) / len(empty)
    dv = {"targets": "every variable", "pairs": pairs, "committed": com, "coverage": round(com / pairs, 4),
          "precision_committed": round((yes_t + no_t) / com, 4) if com else None,
          "precision_yes": round(yes_t / yes, 4) if yes else None, "precision_no": round(no_t / (com - yes), 4) if com - yes else None,
          "yes_rate": round(yes / pairs, 4), "empty_graph_precision": round(empty_prec, 4),
          "lift_over_empty_graph": round((yes_t + no_t) / com - empty_prec, 4) if com else None}
    undirected = {frozenset(e) for e in und}
    fr = CA.directed_scores(directed, undirected, T, d, "random", seed=zlib.crc32(SCENARIO.name.encode()))
    fd = CA.directed_scores(directed, undirected, T, d, "drop")
    f1 = {"f1": round(fr["f1"], 4), "rule": "random (CausalArena's stated rule; seed crc32(file name))", "precision": round(fr["precision"], 4),
          "recall": round(fr["recall"], 4), "shd": fr["shd"], "f1_drop_undecided": round(fd["f1"], 4), "true_edges": len(T),
          "predicted_arrows_committed": len(directed), "undecided_pairs": len(undirected)}
    return dv, f1


def output_fields(tool, w):
    """What the raw output contains, observed from the saved object plus what the worker could extract."""
    R = w["runs"].get("D_seed%d" % MAIN_SEED, {})
    o = R.get("output") or {}
    info = R.get("info") or {}
    marks = sorted({x[2] for x in o.get("other", [])})
    base = {"raw_type": R.get("raw_type"), "raw_fields_observed": R.get("raw_fields"), "raw_file": R.get("raw_file"),
            "edge_marks_observed": (["-->"] if o.get("directed") else []) + (["---"] if o.get("undirected") else []) + marks,
            "sepsets_retrievable": bool(o.get("sepsets")), "sepset_records": len(o.get("sepsets", [])),
            "adjacency_test_stats_retrievable": bool(o.get("adj_tests")), "per_edge_metadata": sorted({k for _, _, m in o.get("edge_meta", []) for k in m}),
            "settings": info.get("settings"), "seeds": {"shuffle_seeds": list(ORDER_SEEDS)}, "versions": w.get("versions")}
    curated = {
        "dowhy+causal-learn": {"graph_type": "CPDAG as GeneralGraph matrix cg.G.graph (-1 tail, 1 arrowhead)", "sepsets": "cg.sepset[i, j]: tuples of conditioning-set indices, no p-values",
                               "test_statistics": "not in the output; only in the CIT object's internal pvalue_cache (undocumented)",
                               "per_edge_source": "none", "seed": "none needed (deterministic)", "dowhy": "CausalModel keeps the graph only"},
        "pgmpy-pc": {"graph_type": "PDAG (directed_edges, undirected_edges)", "sepsets": "separating_sets_ {frozenset: tuple}, no p-values",
                     "test_statistics": "not stored", "per_edge_source": "none (knowledge-oriented edges unmarked)", "seed": "none (deterministic)"},
        "pgmpy-hillclimb": {"graph_type": "PDAG of the learned DAG (return_type='pdag' default)", "sepsets": "n/a", "test_statistics": "no score deltas stored",
                            "per_edge_source": "none", "seed": "none (deterministic)"},
        "causalnex": {"graph_type": "StructureModel (networkx DiGraph), directed edges only", "sepsets": "n/a",
                      "per_edge_metadata": "weight (float), origin in {unknown, learned, expert}", "test_statistics": "none",
                      "per_edge_source": "origin: 'learned' on every from_pandas edge; 'expert' only if add_edge is given origin='expert'"},
        "dodiscover": {"graph_type": "pywhy_graphs CPDAG (directed + undirected edge sets)", "sepsets": "separating_sets_[x][y]: list of sets, no p-values",
                       "test_statistics": "not stored", "per_edge_source": "none", "seed": "none (deterministic)"},
        "tigramite": {"graph_type": "string mark array graph[i, j, tau]: '-->', 'o-o', 'x-x' (conflict), '' ", "sepsets": "results['sepsets'] {((i, -tau), j): conditioning set}",
                      "test_statistics": "p_matrix and val_matrix for every pair (max p over tests; statistic of that test)",
                      "per_edge_source": "none; 'x-x' marks an orientation conflict, 'o-o' an undecided pair", "seed": "none (deterministic)"},
        "gcastle": {"graph_type": "causal_matrix (0/1; both 1 = undirected)", "sepsets": "computed internally (find_skeleton) but not kept on the object",
                    "test_statistics": "none", "per_edge_source": "none", "seed": "none (deterministic)"},
        "lingam": {"graph_type": "weighted DAG adjacency_matrix_ (B[i, j] != 0 means j -> i) + causal_order_", "sepsets": "n/a",
                   "test_statistics": "none in the fit; get_error_independence_p_values() is a separate model check, not per edge",
                   "per_edge_source": "none (weights only)", "seed": "random_state=0 (DirectLiNGAM is deterministic)"},
        "py-tetrad": {"graph_type": "Tetrad EdgeListGraph (endpoints TAIL/ARROW/CIRCLE)", "sepsets": "Pc.getFas().getSepsets() if exposed (see notes)",
                      "test_statistics": "free-text verbose log via setLogStream; not attached to edges", "per_edge_source": "none on edges",
                      "seed": "none (deterministic)"},
        "pywhy-llm": {"graph_type": "dict {(a, b): count} of LLM-suggested arrows", "sepsets": "n/a (no data interface)", "test_statistics": "none",
                      "per_edge_source": "none in the library output; all arrows come from the LLM by construction", "seed": "stub answers seeded by prompt sha256"},
    }
    base.update(curated.get(tool, {}))
    return base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--worker")
    ap.add_argument("--out")
    ap.add_argument("--tools", nargs="+", default=list(TOOLS))
    ap.add_argument("--reuse", action="store_true", help="rebuild ledgers and scores from saved worker.json files without rerunning tools")
    a = ap.parse_args()
    if a.worker:
        worker(a.worker, a.out)
        return
    sys.path.insert(0, str(HERE))
    import ab11_ledger_adapters as LA
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "ledgers").mkdir(exist_ok=True)
    X, names, g = load_scenario()
    tj = OUT / "teardown.json"
    report = json.loads(tj.read_text()) if tj.exists() else {}
    report.setdefault("tools", {})
    t_start = time.time()
    for tool in a.tools:
        raw_dir = OUT / "raw" / tool
        raw_dir.mkdir(parents=True, exist_ok=True)
        print("=== %s" % tool, flush=True)
        if a.reuse and (raw_dir / ("worker.json" if tool != "pywhy-llm" else "probe.json")).exists():
            w = json.loads((raw_dir / ("worker.json" if tool != "pywhy-llm" else "probe.json")).read_text())
        else:
            w = run_pywhyllm(raw_dir) if tool == "pywhy-llm" else run_worker(tool, raw_dir)
            if tool == "pywhy-llm":
                (raw_dir / "probe.json").write_text(json.dumps(w, indent=1, default=str))
        row = {"interface": TOOLS[tool][1], "venv": str(PY[TOOLS[tool][0]].parent.parent)}
        if "runs" not in w:
            row.update(installed=w.get("installed", False), version=None, notes=w.get("error"))
            report["tools"][tool] = row
            continue
        D = w["runs"].get("D_seed%d" % MAIN_SEED, {})
        row["installed"] = True
        row["version"] = w.get("versions")
        row["python"] = w.get("python")
        row["output_fields"] = output_fields(tool, w)
        row["knowledge_tests"] = knowledge_tests(w) if tool != "pywhy-llm" else {
            "required_edge_added_connection": "na", "forbidden_honoured": "na", "tiers_honoured": "na",
            "detail": "no knowledge-input interface: the library is itself the knowledge supplier (names only, no data)"}
        inv, diffs = order_check(w)
        row["order_invariant_over_3_orders"] = inv
        row["order_check_detail"] = diffs
        row["errors"] = {k: (r.get("error") or "")[:600] for k, r in w["runs"].items() if r.get("error")}
        row["cpu_s"] = round(sum(r.get("cpu_s", 0) or 0 for r in w["runs"].values()), 1)
        if D.get("output"):
            row["dv1"], row["f1"] = scores(D["output"], g, names)
            ledgers = LA.build_all(tool, w, X, names, permutation_identical=inv if inv != "na" else False, main_seed=MAIN_SEED)
            checks = {}
            for reg_label, led in ledgers.items():
                p = OUT / "ledgers" / ("%s__%s.json" % (tool, reg_label))
                p.write_text(json.dumps(led, indent=1))
                checks[reg_label] = LA.run_verifier(p)
            row["ledger_files"] = sorted(str((OUT / "ledgers" / ("%s__%s.json" % (tool, k))).relative_to(KIT)) for k in ledgers)
            row["ledger_checks"], row["ledger_checks_after_relaxing_V1"] = LA.aggregate(checks)
            row["ledger_checks_by_ledger"] = checks
        row["notes"] = notes_for(tool, w, row)
        report["tools"][tool] = row
        print("  -> invariant=%s K=%s V=%s" % (inv, {k: v for k, v in row["knowledge_tests"].items() if k not in ("detail", "knowledge_pick")},
                                                row.get("ledger_checks")), flush=True)
    report["not_run"] = {
        "cdt": "installed (cdt 0.6.0 in agents/venv_teardown) but its PC/GES/GIES/LiNGAM/CAM wrappers call R (pcalg, bnlearn) and no R "
               "is on this machine; the Python-only methods (CGNN, SAM) need torch training and an LLM-free run would not test knowledge. Not run.",
        "causal-cmd": "Tetrad's CLI; the same Tetrad 7.6.11 search was run through py-tetrad."}
    report.update(ticket=["AUD-42", "CAP-09"], bundle="AB-11 hands-on", created_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                  scenario=str(SCENARIO.relative_to(WORK)), scenario_data_sha256=sha_array(X), variables=len(names), rows=int(X.shape[0]),
                  true_edges=int(np.asarray(g).sum()), shuffle_rule="perm = default_rng(seed + crc32(file name)).permutation(d)",
                  main_seed=MAIN_SEED, order_seeds=list(ORDER_SEEDS), alpha_ci_tools=ALPHA, runner="analysis/ab11_teardown_run.py",
                  orchestrator_python=sys.version.split()[0], verifier="ledger/verify.py (unchanged)",
                  no_llm_calls="PyWhy-LLM run only with --stub (offline fake LLM); nothing else calls a model",
                  check_mapping={"V1, V2, V6": "every ledger of the tool", "V3, V5": "the D+K ledgers (one per knowledge test)",
                                 "V7, V8": "the D ledger (only the data-only run was permuted)", "V4": "na: no interventional data in this file",
                                 "aggregation": "fail if any ledger fails the check; na if no ledger tests it; V2-V8 are 'na' in ledger_checks when V1 fails, "
                                                "because verify.py stops after V1; ledger_checks_after_relaxing_V1 reruns them with evidence minItems=0 "
                                                "(diagnostic only) and counts V2 as failed if any claim cites no evidence (DESIGN.md wording)"},
                  orchestrator_wall_s_last_call=round(time.time() - t_start, 1))
    tj.write_text(json.dumps(report, indent=1, default=str))
    contract = {"producer": "analysis/ab11_teardown_run.py", "score_bearing": True, "tickets": ["AUD-42", "CAP-09"],
                "regime": "per-row", "regime_by_row": {t: ("D+K" if t == "pywhy-llm" else "D (scores, V7, V8) / D+K (knowledge tests, V3, V5)")
                                                       for t in report["tools"]},
                "regime_detail": "DV-1 and F1 are scored on the data-only (D) run at shuffle seed 20261010; knowledge runs are D+K and are not scored; "
                                 "PyWhy-LLM has no data interface, so its only regime is K (recorded as D+K, data-only relation 'none'), and it ran on the offline stub",
                "split": "all-public (measurement, no tuning)",
                "controls": {"columns_shuffled": "three orders", "names": "not applicable", "supplier": "causalarena"},
                "scenario": report["scenario"], "metric_defs": {
                    "dv1": "decision_value_v2.claims with every variable as a target: coverage = committed (target, variable) claims / d(d-1); "
                           "precision_committed = share of committed yes/no claims matching the true graph's reachability",
                    "f1": "directed-edge F1 (causalarena_io.directed_scores), undecided pairs oriented by the random rule seeded crc32(file name); "
                          "f1_drop_undecided also given",
                    "ledger_checks": "ledger/verify.py V1-V8 on ledgers written by analysis/ab11_ledger_adapters.py from what each tool exposes"}}
    (OUT / "CONTRACT.json").write_text(json.dumps(contract, indent=1))
    print("wrote", tj, OUT / "CONTRACT.json")


def notes_for(tool, w, row):
    n = []
    D = w["runs"].get("D_seed%d" % MAIN_SEED, {})
    info = D.get("info") or {}
    if tool == "dowhy+causal-learn":
        n.append("DoWhy has no discovery of its own; causal-learn PC found the graph and DoWhy received it: %s" % json.dumps(info.get("dowhy")))
        n.append("DoWhy 0.12 is what uv resolved next to numpy<2; CausalModel accepted the CPDAG given as a cyclic DiGraph without a check, and "
                 "identify_effect then failed on networkx 3.6 (nx.algorithms.d_separated removed). falsify_graph was not run (CPU budget).")
    if tool == "causalnex":
        n.append("Requires-Python <3.11 (causalnex 0.12.2 metadata), so it does not install on 3.11; run on CPython 3.10 with its declared "
                 "deps (numpy 1.23.5, pandas 1.5.3, pgmpy 0.1.19, CUDA torch pulled by pgmpy). EOL 2026-06. origin counts (D run): %s; "
                 "tiers have no interface and were sent as tabu_edges; a required edge can only be added after learning (add_edge)" % info.get("origin_counts"))
        k = w["runs"].get("K_required", {}).get("info") or {}
        if k:
            n.append("add_edge without origin (the tutorial's form) labels the edge %r" % k.get("add_edge_without_origin_gets"))
    if tool == "pywhy-llm":
        n.append("STUB ONLY: answers come from the probe's offline fake LLM (seeded by prompt sha256, 20/20/60 A/B/C), so graph, DV-1 and F1 "
                 "measure the stub, not PyWhy-LLM; order (in)variance reflects prompt wording changing with the order.")
    if tool == "gcastle":
        n.append("gCastle 1.0.4 imported with the torch stub (analysis/engine_shims.py); PC is numpy only. No tier interface: tiers sent as forbidden edges.")
    if tool == "py-tetrad":
        n.append("py-tetrad from git (cmu-phil/py-tetrad) installed in seconds; bundled jar %s. With setVerbose(true) Tetrad prints its decisions "
                 "to System.out (not to setLogStream): %s. The adapter parses 'Independence accepted: a _||_ b | S  p = ..' into ci_test "
                 "records and 'Collider oriented: a -> b <- c' into v_structure licences; Meek-rule orientations are not logged. "
                 "getFas().getSepsets() returns the same sets without p-values (%s records)."
                 % (info.get("tetrad_version"), json.dumps(info.get("verbose_line_kinds")), info.get("getSepsets_records")))
    if tool == "tigramite":
        n.append("p_matrix/val_matrix cover every pair and sepsets every removed pair, so every claim cites an exposed test: the D ledger passes "
                 "V1-V8 although every arrow has direction_source 'none' ('x-x' conflict marks become 'x-y' with tool_mark). "
                 "link_assumptions '-->' makes a link exist (V3).")
    if tool == "pgmpy-pc":
        n.append("With temporal_order, candidate separating sets of (u, v) are cut to variables in tiers <= min(tier u, tier v) "
                 "(pgmpy/causal_discovery/_base.py _get_potential_sepsets), so a later-tier mediator can never separate an earlier-tier cause "
                 "from a later-tier effect: correct tiers added 43 adjacencies here (13 true, 30 false). Default mode ignores conflicting "
                 "required/forbidden edges with a logged warning; enforce_expert_knowledge=True adds the required adjacency and deletes the forbidden one.")
    if tool == "dowhy+causal-learn":
        n.append("A required edge on a pair the skeleton removed is dropped silently (no warning, no record): V3 holds, V5 does not. "
                 "Orientation changes with column order although stable=True (skeleton is stable, orientations are not).")
    if tool == "dodiscover":
        n.append("included_edges/excluded_edges take a graph; there is no tier interface (tiers test: na)")
    if tool == "lingam":
        n.append("prior_knowledge is about directed PATHS: required a->b sent as 'path a to b', forbidden as 'no path a to b'")
    if row.get("errors"):
        n.append("errors: %s" % json.dumps({k: v[:200] for k, v in row["errors"].items()}))
    return n


if __name__ == "__main__":
    main()
