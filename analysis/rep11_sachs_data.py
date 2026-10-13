"""REP-11 (BND-12), data-only part: reproduce the BNSL-ensemble F1 that Kitson & Constantinou report for Sachs.

  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<dir with pgmpy 1.1.2> python analysis/rep11_sachs_data.py [--quick]
      [--causaliq-path DIR]   # optional: dir holding the authors' causaliq_core 0.7.0 / causaliq_analysis 0.4.0
                              # (PyPI wheels, unpacked); if given, the PDG merge, ToDAGGreedy and F1 ports below are
                              # re-run with the authors' own code and the results must be identical

Paper: arXiv 2608.27472v1, "LLM-Augmented Causal Discovery: Probabilistic Fusion of Edge Existence and Orientation".
No LLM or API calls: only the BNSL ("data-only") numbers are in scope.

Protocol as read (Sections 2.1, 2.3, 2.4; Tables 5 and 9):
  network   Sachs from bnlearn (11 nodes, 17 arcs), discrete; synthetic observational rows sampled from the BN, 10,000 rows
  BNSL      PC-Stable (bnlearn), Tabu-Stable (Kitson & Constantinou 2025), FGES (Tetrad)
  ensemble  "three different sets of five datasets for each BNSL algorithm"; each set of five learnt graphs -> one PDG
            (Algorithm 1, MERGEGRAPHS, equal weights); "in turn merge these individual PDGs" into one BNSL PDG;
            DAG by ToDAGGREEDY (Algorithm 2), tau = 0.3
  metric    F1 of the output DAG against the reference DAG, "semantics ... used in bnlearn"
  reported  Sachs: Mean Indiv. 0.293, Ensemble 0.606 (Table 9); BNSL 0.606 (Table 5)

Substitutions (no R, no Java here):
  PC-Stable (bnlearn pc.stable, default test "mi")  -> causal-learn pc(stable=True, indep_test="gsq", alpha=0.05,
                                                       uc_rule=0, uc_priority=2) from Causal-Copilot/externals/causal-learn
  Tabu-Stable (authors' Python, causal-iq/discovery) -> this file's tabu_stable(): BIC, tabu list 10 DAGs, noinc 10
                                                       (bnlearn tabu defaults; the Tabu-Stable paper gives no values),
                                                       stable order per arXiv 2504.01740 Algorithm 2 as read
  FGES (Tetrad, BDeu)                                -> causal-learn ges() with a BDeu local score written here
                                                       (ESS 1, Tetrad-style structure prior 1/(p-1)); causal-learn's
                                                       own local_score_BDeu uses n-1 rows in the structure prior and
                                                       is pandas-slow, so it is swapped in-memory (no file edited)
Data: 15 datasets x 10,000 rows, pgmpy DiscreteBayesianNetwork.simulate(seed=SEED0 + k), k = 0..14;
      set s = k // 5 (sets 0, 1, 2 of five datasets each); every algorithm runs on all 15 datasets.

Ensemble readings (fixed here before any run; the paper's text admits all three):
  B (PRIMARY)  per (algorithm, set): MERGEGRAPHS(5 graphs) -> 9 PDGs; MERGEGRAPHS(9 PDGs, equal weights) -> one PDG;
               ToDAGGREEDY(tau 0.3) -> one DAG -> F1.  ("in turn merge these individual PDGs to create one final ...")
  A            per set s: MERGEGRAPHS of the 3 per-algorithm PDGs of set s -> DAG -> F1; report the mean over the
               3 sets ("The 'Ensemble' column shows the mean F1 ...").
  C            algorithm i uses only set i (FGES set 0, Tabu set 1, PC set 2): 3 PDGs -> one PDG -> DAG -> F1
               ("three different sets of five datasets", one set per algorithm).
Mean Indiv.: mean F1 over all 45 individual learnt graphs (3 algorithms x 15 datasets), each scored as learnt
             (CPDAG/PDAG/DAG) with the same F1 ("averaging across all the individual BNSL runs").

F1 ("bnlearn semantics"): ported from the authors' causaliq_analysis 0.4.0 metrics.pdag_compare (the evaluate action
calls it on the learnt graph vs the reference): TP = arcs matched with the same orientation + undirected edges matched
as undirected; a reversed arc, or an arc/edge type mismatch, counts once as FP and once as FN; extra -> FP; missing -> FN.
This is the bnlearn compare() rule (direction matters; an undirected edge does not match a directed arc).
Skeleton F1 (edge type ignored) is reported alongside, not used for the verdict.

Verdict rule (fixed before running): |ours - reported| <= 0.05 -> "reproduced"; otherwise "not reproduced", with the
substitutions listed as the likely reason. Applied to Mean Indiv. (0.293) and to the PRIMARY ensemble reading (0.606).
Writes analysis/results/rep11/rep11_sachs_data.json.
"""
import argparse, collections, gzip, hashlib, importlib.util, io, json, math, os, platform, sys, time, warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CL_PATH = ROOT.parent / "Causal-Copilot" / "externals" / "causal-learn"
OUT = HERE / "results" / "rep11" / "rep11_sachs_data.json"

N_ROWS = 10000
N_SETS, PER_SET = 3, 5
SEED0 = 11000                      # dataset k uses seed SEED0 + k
ALPHA = 0.05
TAU = 0.3
TABU_LEN, NOINC = 10, 10
BDEU_ESS, BDEU_STRUCT_PRIOR = 1.0, 1.0
ALGS = ("FGES", "Tabu", "PC")      # order of Table 9's sentence "(FGES, Tabu, PC)"
REPORTED = {"mean_indiv_f1": 0.293, "ensemble_f1": 0.606, "where": "Table 9 (Sachs row); Table 5 BNSL column = 0.606"}
VERDICT_TOL = 0.05
EXPECTED_SHA_PREFIX = "ed1830fb"

warnings.filterwarnings("ignore")


# ----------------------------------------------------------------------------- data
def load_sachs():
    import pgmpy
    from pgmpy.readwrite import BIFReader
    path = Path(pgmpy.__file__).parent / "utils" / "example_models" / "sachs.bif.gz"
    raw = path.read_bytes()
    model = BIFReader(string=gzip.decompress(raw).decode("utf-8")).get_model()
    src = {"source": "pgmpy %s bundled file pgmpy/utils/example_models/sachs.bif.gz (the bnlearn repository BIF; "
                     "bnlearn.com was blocked by the proxy, HTTP 403)" % pgmpy.__version__,
           "sha256_gz": hashlib.sha256(raw).hexdigest(),
           "sha256_bif_text": hashlib.sha256(gzip.decompress(raw)).hexdigest()}
    src["sha256_prefix_matches_ed1830fb"] = src["sha256_gz"].startswith(EXPECTED_SHA_PREFIX)
    return model, src


def sample(model, nodes, k):
    df = model.simulate(n_samples=N_ROWS, seed=SEED0 + k, show_progress=False)
    X = np.empty((N_ROWS, len(nodes)), dtype=np.int64)
    for j, v in enumerate(nodes):
        states = list(model.states[v])
        X[:, j] = df[v].astype(str).map({s: i for i, s in enumerate(states)}).to_numpy()
    return X


# ----------------------------------------------------------------------------- graphs
# A graph is {"nodes": [...], "edges": {(a, b): "->" or "--"}}; "--" stored with a < b (canonical, as causaliq does).
def mk(nodes, arcs=(), und=()):
    e = {(a, b): "->" for a, b in arcs}
    for a, b in und:
        e[tuple(sorted((a, b)))] = "--"
    return {"nodes": sorted(nodes), "edges": e}


def from_cl_matrix(G, names):
    """causal-learn GeneralGraph matrix: G[j,i]==1 and G[i,j]==-1 -> i->j; both -1 -> i--j; both 1 -> i<->j."""
    arcs, und, bidir = [], [], 0
    p = len(names)
    for i in range(p):
        for j in range(i + 1, p):
            a, b = G[i, j], G[j, i]
            if a == 0 and b == 0:
                continue
            if a == -1 and b == 1:
                arcs.append((names[i], names[j]))
            elif a == 1 and b == -1:
                arcs.append((names[j], names[i]))
            elif a == -1 and b == -1:
                und.append((names[i], names[j]))
            else:                       # bidirected / other marks: causaliq merge treats "other types" as undirected
                und.append((names[i], names[j]))
                bidir += 1
    return mk(names, arcs, und), bidir


def pdag_compare(g, ref):
    """Port of causaliq_analysis 0.4.0 metrics.pdag_compare (bnlearn semantics)."""
    def metric(rt, t, rev=False):
        if rt == "->" and t == "->":
            return "arc_matched" if not rev else "arc_reversed"
        if rt == "->" and t == "--":
            return "edge_not_arc"
        if rt == "--" and t == "->":
            return "arc_not_edge"
        if rt == "->" and t is None:
            return "arc_missing"
        if rt == "--" and t is None:
            return "edge_missing"
        return "edge_matched"
    m = dict.fromkeys(["arc_matched", "arc_reversed", "edge_not_arc", "arc_not_edge", "edge_matched", "arc_extra",
                       "edge_extra", "arc_missing", "edge_missing"], 0)
    E, R = g["edges"], ref["edges"]
    for e, t in E.items():
        if e in R:
            m[metric(R[e], t)] += 1
        elif (e[1], e[0]) in R:
            m[metric(R[(e[1], e[0])], t, rev=True)] += 1
        else:
            m["arc_extra" if t == "->" else "edge_extra"] += 1
    for e, t in R.items():
        if e not in E and (e[1], e[0]) not in E:
            m[metric(t, None)] += 1
    tp = m["arc_matched"] + m["edge_matched"]
    mis = m["arc_not_edge"] + m["edge_not_arc"] + m["arc_reversed"]
    fp = m["arc_extra"] + m["edge_extra"] + mis
    fn = m["arc_missing"] + m["edge_missing"] + mis
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f1 = 0.0 if p is None or r is None or (p == 0 and r == 0) else 2 * p * r / (p + r)
    shd = m["arc_extra"] + m["edge_extra"] + m["arc_missing"] + m["edge_missing"] + mis
    return dict(m, tp=tp, fp=fp, fn=fn, precision=p, recall=r, f1=f1, shd=shd)


def skeleton_f1(g, ref):
    s = {frozenset(e) for e in g["edges"]}
    t = {frozenset(e) for e in ref["edges"]}
    tp = len(s & t)
    p = tp / len(s) if s else 0.0
    r = tp / len(t) if t else 0.0
    return {"precision": p, "recall": r, "f1": 2 * p * r / (p + r) if p + r else 0.0}


# ----------------------------------------------------------------------------- Algorithms 1 and 2 (ports)
STATES = ("forward", "backward", "undirected", "none")


def merge_graphs(graphs, weights=None):
    """Algorithm 1 MERGEGRAPHS, ported from causaliq_analysis 0.4.0 merge.merge_graphs (strategy "average").
    A PDG here is {"nodes": [...], "pdg": {(a, b): {forward, backward, undirected, none}}} with a < b."""
    n = len(graphs)
    weights = weights or [1.0 / n] * n
    nodes = sorted(graphs[0]["nodes"])
    acc = {}
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            acc[(a, b)] = dict.fromkeys(STATES, 0.0)
    for g, w in zip(graphs, weights):
        for (a, b), pr in acc.items():
            if "pdg" in g:
                q = g["pdg"].get((a, b), {"forward": 0.0, "backward": 0.0, "undirected": 0.0, "none": 1.0})
                for s in STATES:
                    pr[s] += w * q[s]
            else:
                ab, ba = g["edges"].get((a, b)), g["edges"].get((b, a))
                if ab == "->":
                    pr["forward"] += w
                elif ba == "->":
                    pr["backward"] += w
                elif ab is not None or ba is not None:
                    pr["undirected"] += w
                else:
                    pr["none"] += w
    return {"nodes": nodes, "pdg": {k: v for k, v in acc.items() if v["none"] < 1.0 - 1e-9}}


def to_dag_greedy(pdg, tau):
    """Algorithm 2 ToDAGGREEDY, ported from causaliq_core 0.7.0 graph.pdg.PDG.to_dag_greedy.
    Keeps a pair when p_exist >= tau (pseudocode: skip if p_fwd + p_bwd + p_und < tau); direction by
    p_fwd + p_und/2 vs p_bwd + p_und/2, ties -> canonical (alphabetical) forward; stable sort by score, descending;
    an arc that closes a cycle is skipped."""
    cands, skipped_tau, at_tau = [], 0, 0
    for (a, b), pr in pdg["pdg"].items():
        pe = pr["forward"] + pr["backward"] + pr["undirected"]
        if abs(pe - tau) < 1e-9:
            at_tau += 1
        if pe < tau:
            skipped_tau += 1
            continue
        ef, eb = pr["forward"] + pr["undirected"] / 2, pr["backward"] + pr["undirected"] / 2
        if ef > eb:
            cands.append((ef, a, b, "f", False))
        elif eb > ef:
            cands.append((eb, a, b, "b", False))
        else:
            cands.append((ef, a, b, "f", True))
    cands.sort(key=lambda x: -x[0])
    anc = {v: set() for v in pdg["nodes"]}
    arcs, skipped_cycle, ties = [], 0, 0
    for _, a, b, d, tie in cands:
        x, y = (a, b) if d == "f" else (b, a)
        if y in anc[x]:
            skipped_cycle += 1
            continue
        arcs.append((x, y))
        ties += tie
        new = anc[x] | {x}
        anc[y] |= new
        stack, seen = [y], set()
        while stack:
            c = stack.pop()
            if c in seen:
                continue
            seen.add(c)
            for (u, v) in arcs:
                if u == c:
                    anc[v] |= new
                    stack.append(v)
    stats = {"candidates": len(cands), "included": len(arcs), "skipped_cycle": skipped_cycle,
             "skipped_threshold": skipped_tau, "pairs_with_p_exist_equal_tau": at_tau, "tie_breaks": ties}
    return mk(pdg["nodes"], arcs), stats


# ----------------------------------------------------------------------------- scores
class Scorer:
    """Decomposable discrete scores with a cache. bic: log-lik - log(n)/2 * (r-1) * q (bnlearn "bic").
    bdeu: log BDeu marginal likelihood with ESS, plus the Tetrad BDeuScore structure prior
    k*log(sp/(p-1)) + (p-1-k)*log(1 - sp/(p-1)). Higher is better for both."""

    def __init__(self, X, kind):
        self.X, self.kind = X, kind
        self.n, self.p = X.shape
        self.card = [int(X[:, j].max()) + 1 for j in range(self.p)]
        self.cache = {}

    def local(self, i, parents):
        key = (i, frozenset(parents))
        if key in self.cache:
            return self.cache[key]
        pa = sorted(parents)
        r = self.card[i]
        q = 1
        idx = np.zeros(self.n, dtype=np.int64)
        for j in pa:
            idx = idx * self.card[j] + self.X[:, j]
            q *= self.card[j]
        cnt = np.bincount(idx * r + self.X[:, i], minlength=q * r).reshape(q, r).astype(float)
        nij = cnt.sum(1)
        if self.kind == "bic":
            nz = cnt > 0
            ll = float((cnt[nz] * np.log((cnt / np.where(nij[:, None] > 0, nij[:, None], 1))[nz])).sum())
            s = ll - 0.5 * math.log(self.n) * (r - 1) * q
        else:
            from scipy.special import gammaln
            a_ij, a_ijk = BDEU_ESS / q, BDEU_ESS / (q * r)
            s = float((gammaln(a_ij) - gammaln(nij + a_ij)).sum() + (gammaln(cnt + a_ijk) - gammaln(a_ijk)).sum())
            k, m = len(pa), self.p - 1
            sp = BDEU_STRUCT_PRIOR / m
            s += k * math.log(sp) + (m - k) * math.log(1 - sp)
        self.cache[key] = s
        return s


# ----------------------------------------------------------------------------- Tabu-Stable stand-in
def _has_path(par, src, dst):
    """True if a directed path src ~> dst exists (par[v] = parents of v)."""
    children = collections.defaultdict(set)
    for v, ps in par.items():
        for u in ps:
            children[u].add(v)
    stack, seen = [src], set()
    while stack:
        c = stack.pop()
        if c == dst:
            return True
        if c in seen:
            continue
        seen.add(c)
        stack.extend(children[c])
    return False


def _search(sc, order, tabu):
    """Greedy search over add/delete/reverse from the empty DAG. `order` is the stable tie-break order: moves are
    scanned in that order and an addition whose opposite orientation has the same delta is taken in the orientation
    whose parent comes first in `order` (arXiv 2504.01740 Alg. 1 'equivalent change'). tabu=False -> plain HC."""
    p = sc.p
    rank = {v: i for i, v in enumerate(order)}
    par = {i: set() for i in range(p)}
    cur = sum(sc.local(i, ()) for i in range(p))
    best, best_par = cur, {i: set() for i in range(p)}
    tl = collections.deque([frozenset()], maxlen=TABU_LEN)
    noinc, iters = 0, 0
    while True:
        iters += 1
        bm, bd = None, -math.inf
        arcset = frozenset((u, v) for v in par for u in par[v])
        for x in order:
            for y in order:
                if x == y:
                    continue
                if x in par[y]:
                    d_del = sc.local(y, par[y] - {x}) - sc.local(y, par[y])
                    moves = [("del", x, y, d_del, arcset - {(x, y)})]
                    par[y].discard(x)
                    if not _has_path(par, x, y):
                        d_rev = d_del + sc.local(x, par[x] | {y}) - sc.local(x, par[x])
                        moves.append(("rev", x, y, d_rev, (arcset - {(x, y)}) | {(y, x)}))
                    par[y].add(x)
                elif y not in par[x]:
                    if _has_path(par, y, x):
                        continue
                    moves = [("add", x, y, sc.local(y, par[y] | {x}) - sc.local(y, par[y]), arcset | {(x, y)})]
                else:
                    continue
                for kind, a, b, d, res in moves:
                    if tabu and res in tl:
                        continue
                    if bm is None or d > bd + 1e-9 * max(1.0, abs(bd)):
                        bm, bd = (kind, a, b, res), d
        if bm is None or (not tabu and bd <= 1e-9):
            break
        kind, a, b, res = bm
        if kind == "add":     # equivalent change: same arc, opposite orientation, same delta
            if not _has_path(par, a, b):
                d2 = sc.local(a, par[a] | {b}) - sc.local(a, par[a])
                res2 = arcset | {(b, a)}
                if abs(d2 - bd) <= 1e-9 * max(1.0, abs(bd)) and rank[b] < rank[a] and not (tabu and res2 in tl):
                    bm, a, b, res = ("add", b, a, res2), b, a, res2
        if kind == "add":
            par[b].add(a)
        elif kind == "del":
            par[b].discard(a)
        else:
            par[b].discard(a)
            par[a].add(b)
        cur += bd
        tl.append(res)
        if cur > best + 1e-9 * abs(best):
            best, best_par, noinc = cur, {v: set(s) for v, s in par.items()}, 0
        else:
            noinc += 1
            if tabu and noinc >= NOINC:
                break
        if not tabu:
            best, best_par = cur, {v: set(s) for v, s in par.items()}
    return best_par, best, iters


def _topo(par, order):
    rank = {v: i for i, v in enumerate(order)}
    indeg = {v: len(par[v]) for v in par}
    out, ready = [], sorted([v for v in par if indeg[v] == 0], key=rank.get)
    while ready:
        v = ready.pop(0)
        out.append(v)
        for w in par:
            if v in par[w]:
                indeg[w] -= 1
                if indeg[w] == 0:
                    ready.append(w)
        ready.sort(key=rank.get)
    return out


def stable_order(sc):
    """arXiv 2504.01740 Alg. 2 as read: key = (score with no parents, mean single-parent score, value-count text);
    dec order = key descending; inc = reverse; HC with each; keep the order whose DAG scores higher; return that
    DAG's topological order (ties by the chosen order)."""
    p = sc.p
    keys = []
    for i in range(p):
        s0 = sc.local(i, ())
        s1 = sum(sc.local(i, (j,)) for j in range(p) if j != i) / (p - 1)
        counts = sorted(np.bincount(sc.X[:, i]).tolist())
        keys.append((s0, s1, str(counts), i))
    dec = [k[3] for k in sorted(keys, key=lambda k: (k[0], k[1], k[2]), reverse=True)]
    inc = dec[::-1]
    res = []
    for o in (dec, inc):
        par, s, _ = _search(sc, o, tabu=False)
        res.append((s, o, par))
    s, o, par = max(res, key=lambda t: t[0])
    return _topo(par, o), {"dec_hc_score": res[0][0], "inc_hc_score": res[1][0],
                          "chosen": "dec" if o is dec else "inc"}


def tabu_stable(X, names):
    sc = Scorer(X, "bic")
    order, info = stable_order(sc)
    par, score, iters = _search(sc, order, tabu=True)
    arcs = [(names[u], names[v]) for v in par for u in par[v]]
    return mk(names, arcs), {"bic": score, "iterations": iters, "stable_order": [names[i] for i in order], **info}


# ----------------------------------------------------------------------------- PC and GES via causal-learn
def _causallearn():
    if str(CL_PATH) not in sys.path:
        sys.path.insert(0, str(CL_PATH))
    from causallearn.search.ConstraintBased.PC import pc
    import causallearn.search.ScoreBased.GES as GESmod
    return pc, GESmod


def run_pc(X, names):
    pc, _ = _causallearn()
    with open(os.devnull, "w") as dn:
        old = sys.stdout
        sys.stdout = dn
        try:
            cg = pc(X.astype(float), alpha=ALPHA, indep_test="gsq", stable=True, uc_rule=0, uc_priority=2,
                    show_progress=False, node_names=names)
        finally:
            sys.stdout = old
    g, bidir = from_cl_matrix(cg.G.graph, names)
    return g, {"bidirected_as_undirected": bidir}


def run_ges(X, names, kind="bdeu"):
    _, GESmod = _causallearn()
    sc = Scorer(X, kind)
    orig = GESmod.local_score_BDeu
    GESmod.local_score_BDeu = lambda Data, i, PAi, parameters=None: -sc.local(i, tuple(PAi))  # causal-learn minimises
    try:
        rec = GESmod.ges(X, score_func="local_score_BDeu", maxP=None, parameters=None, node_names=names)
    finally:
        GESmod.local_score_BDeu = orig
    g, bidir = from_cl_matrix(rec["G"].graph, names)
    return g, {"score_kind": kind, "bidirected_as_undirected": bidir}


# ----------------------------------------------------------------------------- truth helpers
def truth_cpdag(model, names):
    _causallearn()
    from causallearn.graph.Dag import Dag
    from causallearn.graph.GraphNode import GraphNode
    from causallearn.utils.DAG2CPDAG import dag2cpdag
    nd = [GraphNode(v) for v in names]
    d = Dag(nd)
    for a, b in model.edges():
        d.add_directed_edge(nd[names.index(a)], nd[names.index(b)])
    g, _ = from_cl_matrix(dag2cpdag(d).graph, names)
    return g


def verdict(ours, reported):
    diff = ours - reported
    return {"ours": round(ours, 4), "reported": reported, "diff": round(diff, 4),
            "verdict": "reproduced" if abs(diff) <= VERDICT_TOL else "not reproduced"}


# ----------------------------------------------------------------------------- authors'-code cross-check
def crosscheck(path, individual, pdgs_inputs, ref, tau):
    """Re-run merge / to_dag_greedy / pdag_compare with causaliq_core 0.7.0 + causaliq_analysis 0.4.0."""
    sys.path.insert(0, str(Path(path) / "x_causaliq_core"))
    from causaliq_core.graph import DAG, PDAG
    def load(modname, file):
        spec = importlib.util.spec_from_file_location(modname, file)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    an = Path(path) / "x_causaliq_analysis" / "causaliq_analysis"
    M = load("cq_merge", an / "merge.py")
    Mt = load("cq_metrics", an / "metrics.py")

    def conv(g):
        edges = [(a, "->" if t == "->" else "-", b) for (a, b), t in g["edges"].items()]
        return DAG(g["nodes"], edges) if all(t == "->" for t in g["edges"].values()) else PDAG(g["nodes"], edges)
    ref_c = conv(ref)
    out = {"individual_f1_identical": True, "ensemble": {}}
    for key, g in individual.items():
        f_theirs = Mt.pdag_compare(conv(g), ref_c)["f1"]
        if abs(f_theirs - pdag_compare(g, ref)["f1"]) > 1e-12:
            out["individual_f1_identical"] = False
    for name, groups in pdgs_inputs.items():
        level1 = [M.merge_graphs([conv(g) for g in grp]) for grp in groups]
        final = M.merge_graphs(level1)
        dag = final.to_dag_greedy(threshold=tau).dag
        out["ensemble"][name] = {"arcs": sorted("%s->%s" % (a, b) for (a, b), t in dag.edges.items()),
                                 "f1": Mt.pdag_compare(dag, ref_c)["f1"]}
    return out


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="2 datasets per set, for a smoke test (not written)")
    ap.add_argument("--causaliq-path", default=None)
    a = ap.parse_args()
    t0 = time.time()
    model, src = load_sachs()
    names = sorted(model.nodes())
    ref = mk(names, list(model.edges()))
    assert len(names) == 11 and len(ref["edges"]) == 17
    ref_cpdag = truth_cpdag(model, names)
    per_set = 2 if a.quick else PER_SET

    datasets, graphs, info = [], {}, {}
    for s in range(N_SETS):
        for j in range(per_set):
            k = s * PER_SET + j
            X = sample(model, names, k)
            datasets.append({"k": k, "set": s, "seed": SEED0 + k, "rows": int(X.shape[0]),
                             "sha256_int_codes": hashlib.sha256(X.tobytes()).hexdigest()})
            for alg in ALGS:
                t = time.time()
                if alg == "PC":
                    g, extra = run_pc(X, names)
                elif alg == "Tabu":
                    g, extra = tabu_stable(X, names)
                else:
                    g, extra = run_ges(X, names, "bdeu")
                graphs[(alg, k)] = g
                info[(alg, k)] = dict(extra, seconds=round(time.time() - t, 2))
            # sensitivity: FGES stand-in with BIC instead of BDeu
            g, extra = run_ges(X, names, "bic")
            graphs[("FGES_bic", k)] = g
            info[("FGES_bic", k)] = extra
            print("dataset %d done (%.0fs)" % (k, time.time() - t0), flush=True)
    ks = sorted({k for (_, k) in graphs})
    sets = {s: [k for k in ks if k // PER_SET == s] for s in range(N_SETS)}

    # individual runs
    indiv = []
    for (alg, k), g in sorted(graphs.items()):
        c = pdag_compare(g, ref)
        indiv.append({"alg": alg, "k": k, "set": k // PER_SET, "f1": c["f1"], "precision": c["precision"],
                      "recall": c["recall"], "shd": c["shd"], "counts": {x: c[x] for x in (
                          "arc_matched", "arc_reversed", "edge_not_arc", "arc_extra", "edge_extra", "arc_missing")},
                      "n_arcs": sum(t == "->" for t in g["edges"].values()),
                      "n_undirected": sum(t == "--" for t in g["edges"].values()),
                      "skeleton_f1": skeleton_f1(g, ref)["f1"], "info": info[(alg, k)],
                      "edges": sorted("%s%s%s" % (e[0], t, e[1]) for e, t in g["edges"].items())})
    main_rows = [r for r in indiv if r["alg"] in ALGS]
    per_alg = {alg: {"mean_f1": float(np.mean([r["f1"] for r in indiv if r["alg"] == alg])),
                     "sd_f1": float(np.std([r["f1"] for r in indiv if r["alg"] == alg], ddof=1)),
                     "mean_skeleton_f1": float(np.mean([r["skeleton_f1"] for r in indiv if r["alg"] == alg]))}
               for alg in ALGS + ("FGES_bic",)}
    mean_indiv = float(np.mean([r["f1"] for r in main_rows]))
    mean_indiv_skel = float(np.mean([r["skeleton_f1"] for r in main_rows]))

    # individual graphs turned into DAGs by ToDAGGreedy (alternative reading of "individual run" F1)
    mean_indiv_dag = float(np.mean([pdag_compare(to_dag_greedy(merge_graphs([graphs[(r["alg"], r["k"])]]), TAU)[0],
                                                 ref)["f1"] for r in main_rows]))

    def ensemble(groups, label):
        lvl1 = [merge_graphs([graphs[x] for x in grp]) for grp in groups]
        final = merge_graphs(lvl1)
        dag, st = to_dag_greedy(final, TAU)
        c = pdag_compare(dag, ref)
        return {"label": label, "n_level1_pdgs": len(lvl1), "f1": c["f1"], "precision": c["precision"],
                "recall": c["recall"], "shd": c["shd"], "skeleton_f1": skeleton_f1(dag, ref)["f1"],
                "counts": {x: c[x] for x in ("arc_matched", "arc_reversed", "arc_extra", "arc_missing")},
                "to_dag_greedy": st, "arcs": sorted("%s->%s" % e for e in dag["edges"]),
                "pdg": {"%s|%s" % kk: {s: round(v, 4) for s, v in pr.items()} for kk, pr in final["pdg"].items()}}

    def readings(algs):
        B = ensemble([[(alg, k) for k in sets[s]] for alg in algs for s in range(N_SETS)],
                     "B: 9 per-(algorithm,set) PDGs merged into one PDG")
        A_sets = [ensemble([[(alg, k) for k in sets[s]] for alg in algs], "A: set %d" % s) for s in range(N_SETS)]
        A = {"label": "A: per-set ensemble (3 per-algorithm PDGs), mean over 3 sets",
             "f1": float(np.mean([x["f1"] for x in A_sets])), "per_set_f1": [x["f1"] for x in A_sets],
             "skeleton_f1": float(np.mean([x["skeleton_f1"] for x in A_sets])), "per_set": A_sets}
        C = ensemble([[(alg, k) for k in sets[i]] for i, alg in enumerate(algs)],
                     "C: algorithm i on set i only, 3 PDGs merged")
        return {"B_primary": B, "A_mean_over_sets": A, "C_one_set_per_algorithm": C}

    ens = readings(ALGS)
    ens_bic = readings(("FGES_bic", "Tabu", "PC"))
    per_alg_ensemble = {alg: ensemble([[(alg, k) for k in sets[s]] for s in range(N_SETS)],
                                      "single-algorithm ensemble (3 set PDGs)")["f1"] for alg in ALGS}

    out = {
        "ticket": "REP-11", "bundle": "BND-12", "scope": "data-only (no LLM, no API calls)",
        "paper": {"arxiv": "2608.27472v1", "url": "https://arxiv.org/html/2608.27472v1",
                  "title": "LLM-Augmented Causal Discovery: Probabilistic Fusion of Edge Existence and Orientation",
                  "reported_sachs": REPORTED},
        "network": dict(src, nodes=names, n_arcs=len(ref["edges"]),
                        true_arcs=sorted("%s->%s" % e for e in ref["edges"]),
                        true_cpdag={"directed": sum(t == "->" for t in ref_cpdag["edges"].values()),
                                    "undirected": sum(t == "--" for t in ref_cpdag["edges"].values()),
                                    "cpdag_vs_dag_f1": pdag_compare(ref_cpdag, ref)["f1"]}),
        "protocol": {"rows": N_ROWS, "sets": N_SETS, "datasets_per_set": per_set, "seed_rule": "seed = %d + k" % SEED0,
                     "alpha": ALPHA, "tau": TAU, "tabu_list": TABU_LEN, "noinc": NOINC,
                     "bdeu": {"ess": BDEU_ESS, "structure_prior": BDEU_STRUCT_PRIOR},
                     "verdict_rule": "|ours - reported| <= %.2f -> reproduced, else not reproduced" % VERDICT_TOL,
                     "primary_reading": "B", "quick": a.quick},
        "datasets": datasets,
        "results": {
            "per_algorithm": per_alg,
            "mean_indiv_f1": mean_indiv, "mean_indiv_skeleton_f1": mean_indiv_skel,
            "mean_indiv_f1_after_todaggreedy": mean_indiv_dag,
            "ensemble": ens, "ensemble_sensitivity_fges_bic": {k: v["f1"] for k, v in ens_bic.items()},
            "single_algorithm_ensembles_f1": per_alg_ensemble,
        },
        "verdicts": {"mean_indiv_f1": verdict(mean_indiv, REPORTED["mean_indiv_f1"]),
                     "ensemble_f1_primary_B": verdict(ens["B_primary"]["f1"], REPORTED["ensemble_f1"]),
                     "ensemble_f1_A_sensitivity": verdict(ens["A_mean_over_sets"]["f1"], REPORTED["ensemble_f1"]),
                     "ensemble_f1_C_sensitivity": verdict(ens["C_one_set_per_algorithm"]["f1"], REPORTED["ensemble_f1"])},
        "individual_runs": indiv,
        "versions": {"python": platform.python_version()},
        "seconds": None,
    }
    import pgmpy, scipy, pandas
    out["versions"].update(pgmpy=pgmpy.__version__, numpy=np.__version__, scipy=scipy.__version__,
                           pandas=pandas.__version__, causal_learn="vendored at Causal-Copilot/externals/causal-learn")
    if a.causaliq_path:
        groups = {"B_primary": [[graphs[(alg, k)] for k in sets[s]] for alg in ALGS for s in range(N_SETS)],
                  "C_one_set_per_algorithm": [[graphs[(alg, k)] for k in sets[i]] for i, alg in enumerate(ALGS)]}
        cc = crosscheck(a.causaliq_path, {(r["alg"], r["k"]): graphs[(r["alg"], r["k"])] for r in main_rows},
                        groups, ref, TAU)
        cc["ensemble_f1_identical"] = all(abs(cc["ensemble"][n]["f1"] - ens[n]["f1"]) < 1e-12 and
                                          cc["ensemble"][n]["arcs"] == ens[n]["arcs"] for n in cc["ensemble"])
        cc["code"] = "causaliq-core 0.7.0, causaliq-analysis 0.4.0 (PyPI wheels; merge.merge_graphs, " \
                     "PDG.to_dag_greedy, metrics.pdag_compare)"
        out["authors_code_crosscheck"] = cc
    out["seconds"] = round(time.time() - t0, 1)
    v = out["verdicts"]
    print(json.dumps({"per_algorithm": per_alg, "mean_indiv": mean_indiv, "ensemble": {k: x["f1"] for k, x in ens.items()},
                      "verdicts": v, "crosscheck": out.get("authors_code_crosscheck", {}).get("ensemble_f1_identical")},
                     indent=1))
    if not a.quick:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
        print("wrote", OUT)


if __name__ == "__main__":
    main()
