"""AB-09 theory pack (AUD-40): numerical checks of statements T1-T5 on every public CausalArena file we hold.

Prediction P12: every statement holds on all public CausalArena files to numerical precision; any counterexample refutes
it and forces a restatement. This script is the check. One command:

  nice python analysis/theory_checks.py

Defaults point at the cc-research tree (graph helpers, released files, learned graphs) and at causal-learn 0.1.4.8.
Writes analysis/results/theory/theory_checks.json and CONTRACT.json (score_bearing false). No model calls.

Statements (proofs and status in analysis/reports/ab09_theory_pack.md):
  T1  expected directed F1 under the random rule = S x a, when each predicted adjacency yields exactly one arrow;
      the general form for rules that yield 0 or 2 arrows per undecided pair.
  T2  1 - F1 = identifiability + skeleton + orientation, exact per file.
  T3  orientation-only knowledge (I5) changes directed F1 by at most the credit of the pairs it decides.
  T4  causal-learn's collider-conflict rules (uc_priority 2 / 0) resolve conflicts by column index; a 4-variable example.
  T5  the true CPDAG's committed reachability claims are always right; coverage vs constant-over-the-class answers.
Tickets: AUD-40, RQ-04, RQ-06
"""
import argparse, collections, itertools, json, math, os, statistics as st, sys, time, zlib
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # shared CPUs: one BLAS thread
    os.environ.setdefault(_v, "1")
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
DEF_CC = Path("/home/claude/work/run_pc/cc-research/analysis")
DEF_CL = Path("/home/claude/work/engines/cl_0.1.4.8")
TOL = 1e-12
SHUFFLE_SEED = 20261010           # same per-file shuffle as pc_upstream_run.py / pc_orientation_order.py


def _import_cc(cc):
    if str(cc) not in sys.path:
        sys.path.insert(0, str(cc))


# ----------------------------------------------------------------------------------------------------------------- T1
def norm_graph(directed, undecided):
    """directed: iterable of (cause, effect); undecided: iterable of pairs (or [i, j, mark_i, mark_j])."""
    D = {(int(e[0]), int(e[1])) for e in directed}
    U = {frozenset((int(u[0]), int(u[1]))) for u in undecided}
    return D, U


def scorer_f1(tp, npred, ntrue):
    """Exactly the scoreboard's arithmetic (causalarena_io.directed_scores)."""
    prec = tp / npred if npred else 0.0
    rec = tp / ntrue if ntrue else 0.0
    return 2 * prec * rec / (prec + rec) if prec + rec else 0.0


def f1_distribution(D, U, T):
    """Exact distribution of directed F1 when every undecided pair is oriented by an independent fair coin.
    Returns {(tp, npred): probability}. Undecided pairs contribute independently because distinct pairs give distinct
    arrows; an arrow already committed in D adds nothing (set union), which covers overlapping inputs."""
    states = {(len(D & T), len(D)): 1.0}
    for a, b in sorted(tuple(sorted(u)) for u in U):
        opts = []
        for arrow in ((a, b), (b, a)):
            new = arrow not in D
            opts.append((1 if (new and arrow in T) else 0, 1 if new else 0))
        nxt = collections.defaultdict(float)
        for (tp, npred), p in states.items():
            for dtp, dn in opts:
                nxt[(tp + dtp, npred + dn)] += 0.5 * p
        states = nxt
    return states


def expected_f1(D, U, T):
    dist = f1_distribution(D, U, T)
    vals = [(p, scorer_f1(tp, n, len(T))) for (tp, n), p in dist.items()]
    m = sum(p * v for p, v in vals)
    var = sum(p * (v - m) ** 2 for p, v in vals)
    return m, var, sorted({round(v, 15) for _, v in vals})


def coords(D, U, T):
    """S, c, q, a and the counts behind them (definitions as in rescore_controls.py)."""
    tadj = {frozenset(e) for e in T}
    padj = {frozenset(e) for e in D} | U
    tp_adj = len(tadj & padj)
    nP, nT = len(padj), len(tadj)
    right = sum(1 for e in D if e in T)
    wrong = sum(1 for e in D if (e[1], e[0]) in T)
    und_tp = len(U & tadj)
    P = tp_adj / nP if nP else 0.0
    R = tp_adj / nT if nT else 0.0
    S = 2 * P * R / (P + R) if P + R else 0.0
    c = (right + wrong) / tp_adj if tp_adj else 0.0
    q = right / (right + wrong) if right + wrong else None
    a = (right + 0.5 * und_tp) / tp_adj if tp_adj else 0.0
    a_cq = (c * q if q is not None else 0.0) + (1 - c) / 2 if tp_adj else 0.0
    one_arrow = (len(D) + len(U) == nP) and not any((e[1], e[0]) in D for e in D)
    return {"S": S, "c": c, "q": q, "a": a, "a_cq": a_cq, "tp_adj": tp_adj, "nP": nP, "nT": nT, "right": right,
            "wrong": wrong, "und_tp": und_tp, "n_und": len(U), "n_dir": len(D), "one_arrow_per_pair": one_arrow}


def rule_f1_closed_form(rule, D, U, T, pos=None):
    """pos: column position each variable had when the method ran (the "lower" rule reads it; default identity).
    Corrected identity F1_rule = S * a_rule * (nP + nT) / (m_rule + nT), with a_rule = TP_dir / TP_adj and m_rule the
    number of predicted arrows. Valid when D and U do not overlap and D has no 2-cycles (checked by the caller)."""
    k = coords(D, U, T)
    if rule == "lower":
        pos = pos or {}
        tp_dir = k["right"] + sum(1 for u in U if tuple(sorted(u, key=lambda v: pos.get(v, v))) in T)
        m = k["nP"]
    elif rule == "both":
        tp_dir = k["right"] + k["und_tp"]
        m = k["nP"] + k["n_und"]
    elif rule == "drop":
        tp_dir = k["right"]
        m = k["nP"] - k["n_und"]
    else:
        raise ValueError(rule)
    if k["tp_adj"] == 0 or m + k["nT"] == 0:
        return 0.0
    a_rule = tp_dir / k["tp_adj"]
    return k["S"] * a_rule * (k["nP"] + k["nT"]) / (m + k["nT"])


# ----------------------------------------------------------------------------------------------------------------- T2
def cpdag_parts(T, n, G):
    """Compelled arrows and undecided pairs of the true CPDAG (cc_graph.cpdag_of)."""
    C = G.cpdag_of(T, n)
    cd, cu = set(), set()
    for x in range(n):
        for y in range(x + 1, n):
            tp = G.pair_type(C, x, y)
            if tp == "a->b":
                cd.add((x, y))
            elif tp == "b->a":
                cd.add((y, x))
            elif tp == "undirected":
                cu.add(frozenset((x, y)))
            elif tp != "none":
                raise ValueError("unexpected CPDAG mark %s" % tp)
    return cd, cu


def budget(D, U, T, cd, cu):
    """1 - E[F1] = I + K + O (exact). v_C(e) = 1 compelled, 1/2 CPDAG-undecided; v(e) = 1 right, 0 wrong, 1/2 undecided.
    I = 1 - a_C;  K = a_C - 2 sum_TP v_C / N;  O = 2 sum_TP (v_C - v) / N  with N = nP + nT."""
    k = coords(D, U, T)
    tadj = {frozenset(e) for e in T}
    nT, N = k["nT"], k["nP"] + k["nT"]
    vC = {frozenset(e): (1.0 if e in cd else 0.5) for e in T}
    aC = sum(vC.values()) / nT
    padj = {frozenset(e) for e in D} | U
    sum_vC_tp, o_wrong, o_abst, o_beyond, sum_v = 0.0, 0.0, 0.0, 0.0, 0.0
    for e in tadj & padj:
        x, y = tuple(e)
        true_arrow = (x, y) if (x, y) in T else (y, x)
        if true_arrow in D:
            v = 1.0
        elif (true_arrow[1], true_arrow[0]) in D:
            v = 0.0
        else:
            v = 0.5
        sum_vC_tp += vC[e]
        sum_v += v
        if vC[e] == 1.0:
            if v == 0.0:
                o_wrong += 1.0
            elif v == 0.5:
                o_abst += 0.5
        else:
            o_beyond += 0.5 - v          # +1/2 wrong commit, -1/2 right commit, 0 undecided
    I = 1 - aC
    K = aC - 2 * sum_vC_tp / N
    s = 2 / N
    O = s * (o_wrong + o_abst + o_beyond)
    return {"I": I, "K": K, "O": O, "O_wrong_compelled": s * o_wrong, "O_abstain_compelled": s * o_abst,
            "O_beyond_class": s * o_beyond, "F1_identity": s * sum_v, "a_C": aC, "S": k["S"],
            "skeleton_old_style": aC - k["S"], "orientation_old_style": k["S"] - s * sum_v}


# ----------------------------------------------------------------------------------------------------------------- T3
def credit(D, U, T, pair):
    """Expected directed-F1 credit (in TP units) of one predicted adjacency: 1 right, 0 wrong or not a true edge, 1/2
    undecided true edge."""
    x, y = tuple(pair)
    if (x, y) in T:
        ta = (x, y)
    elif (y, x) in T:
        ta = (y, x)
    else:
        return 0.0
    if ta in D:
        return 1.0
    if (ta[1], ta[0]) in D:
        return 0.0
    return 0.5


def apply_orientations(D, U, decide):
    """I5 procedure: decide maps a predicted adjacency (frozenset) to an arrow on it; adjacencies are never added or
    removed. Returns the new graph and the set of decided pairs."""
    padj = {frozenset(e) for e in D} | U
    D2, U2, decided = set(), set(), set()
    for e in D:
        if frozenset(e) not in decide:
            D2.add(e)
    for u in U:
        if u not in decide:
            U2.add(u)
    for pair, arrow in decide.items():
        if pair not in padj or frozenset(arrow) != pair:
            raise ValueError("knowledge may only orient an existing adjacency")
        D2.add(tuple(arrow))
        decided.add(pair)
    return D2, U2, decided


def tier_decisions(D, U, tier):
    """Tier knowledge: each predicted adjacency across tiers is drawn from the earlier tier to the later one."""
    out = {}
    for pair in {frozenset(e) for e in D} | U:
        x, y = tuple(pair)
        if tier[x] < tier[y]:
            out[pair] = (x, y)
        elif tier[y] < tier[x]:
            out[pair] = (y, x)
    return out


def harm_bounds(D, U, T, decided):
    k = coords(D, U, T)
    N = k["nP"] + k["nT"]
    tadj = {frozenset(e) for e in T}
    c0 = sum(credit(D, U, T, p) for p in decided)
    tp_dec = sum(1 for p in decided if p in tadj)
    return {"bound_exact": 2 * c0 / N if N else 0.0,
            "gain_bound_exact": 2 * (tp_dec - c0) / N if N else 0.0,
            "bound_k": 2 * min(len(decided), k["tp_adj"]) / N if N else 0.0,
            "k": len(decided), "k_tp": tp_dec, "N": N}


def depth_of(T, n):
    import networkx as nx
    g = nx.DiGraph()
    g.add_nodes_from(range(n))
    g.add_edges_from(T)
    d = {v: 0 for v in range(n)}
    for v in nx.topological_sort(g):
        for w in g.successors(v):
            d[w] = max(d[w], d[v] + 1)
    return d


# ----------------------------------------------------------------------------------------------------------------- T4
TOY_TRUE = [("a", "b"), ("b", "c"), ("d", "c")]
TOY_ERRORS = {("a", "c", frozenset()): 0.08, ("a", "c", frozenset({"d"})): 0.07}   # finite-sample false independences


def toy_pc(order, uc_rule, uc_priority, cl_path=DEF_CL):
    """Run causal-learn PC on the 4-variable example with a hand-coded CI-test table (no data is read)."""
    if str(cl_path) not in sys.path:
        sys.path.insert(0, str(cl_path))
    import networkx as nx
    from causallearn.search.ConstraintBased.PC import pc
    from causallearn.utils import cit as C

    if "ab09_table" not in C._custom_ci_tests:
        class TableCIT(C.CIT_Base):
            """p = table value for the two scripted errors; otherwise d-separation in the true DAG, graded so that
            maxP's comparisons are not ties (0.5 + 0.01 |S| if separated, 0.001 if connected)."""
            def __init__(self, data, names=None, **kw):
                super().__init__(data, **kw)
                self.check_cache_method_consistent("ab09_table", "toy-v1")
                self.names = names
                self.g = nx.DiGraph(TOY_TRUE)

            def __call__(self, X, Y, condition_set=None):
                cs = () if condition_set is None else tuple(condition_set)
                x, y = self.names[X], self.names[Y]
                S = frozenset(self.names[i] for i in cs)
                key = (min(x, y), max(x, y), S)
                if key in TOY_ERRORS:
                    return TOY_ERRORS[key]
                return 0.5 + 0.01 * len(S) if nx.is_d_separator(self.g, {x}, {y}, set(S)) else 0.001
        C.register_ci_test("ab09_table", TableCIT)
    data = np.zeros((10, len(order)))      # placeholder; the table test never reads it
    cg = pc(data, 0.05, "ab09_table", stable=True, uc_rule=uc_rule, uc_priority=uc_priority, show_progress=False,
            names=list(order))
    g = cg.G.graph
    out = []
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            a, b = g[i, j], g[j, i]
            if a == 0 and b == 0:
                continue
            if a == -1 and b == 1:
                out.append("%s->%s" % (order[i], order[j]))
            elif a == 1 and b == -1:
                out.append("%s->%s" % (order[j], order[i]))
            elif a == -1 and b == -1:
                out.append("%s-%s" % tuple(sorted((order[i], order[j]))))
            else:
                out.append("%s<->%s" % tuple(sorted((order[i], order[j]))))
    return sorted(out)


def uc_model(UT, claims, priority):
    """Model of causal-learn 0.1.4.8 uc_sepset's collider phase, used to test the T4 proposition: claims are applied in
    the order of UT; priority 0 always overwrites; priority 2 applies (x, y, z) only if neither y->x nor y->z is
    already directed. Returns {frozenset pair: arrow}."""
    arrows = {}
    for t in UT:
        if t not in claims:
            continue
        x, y, z = t
        if priority == 2 and (arrows.get(frozenset((x, y))) == (y, x) or arrows.get(frozenset((y, z))) == (y, z)):
            continue
        arrows[frozenset((x, y))] = (x, y)
        arrows[frozenset((z, y))] = (z, y)
    return arrows


def cl_arrows(g):
    out = {}
    d = g.shape[0]
    for i in range(d):
        for j in range(i + 1, d):
            a, b = g[i, j], g[j, i]
            if a == -1 and b == 1:
                out[frozenset((i, j))] = (i, j)
            elif a == 1 and b == -1:
                out[frozenset((i, j))] = (j, i)
            elif a == 1 and b == 1:
                out[frozenset((i, j))] = "bidirected"
    return out


# ----------------------------------------------------------------------------------------------------------------- T5
def reach_matrix(n, arcs):
    R = np.zeros((n, n), dtype=bool)
    for a, b in arcs:
        R[a, b] = True
    for k in range(n):                                     # Warshall transitive closure
        R |= np.outer(R[:, k], R[k, :])
    return R


def chain_component_orientations(n, cu, adj):
    """All orientations of each undirected chain component that are acyclic and create no v-structure (Andersson et
    al. 1997: the members of the class are exactly the combinations of such orientations)."""
    import networkx as nx
    ug = nx.Graph()
    ug.add_edges_from(tuple(e) for e in cu)
    comps = []
    for comp in nx.connected_components(ug):
        edges = [tuple(sorted(e)) for e in ug.subgraph(comp).edges()]
        good = []
        for bits in itertools.product((0, 1), repeat=len(edges)):
            arcs = [(a, b) if s == 0 else (b, a) for (a, b), s in zip(edges, bits)]
            dg = nx.DiGraph(arcs)
            if not nx.is_directed_acyclic_graph(dg):
                continue
            ok = True
            for v in dg.nodes:
                ps = list(dg.predecessors(v))
                for p1, p2 in itertools.combinations(ps, 2):
                    if frozenset((p1, p2)) not in adj:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                good.append(arcs)
        comps.append(good)
    return comps


def cpdag_claims(n, cd, cu, targets):
    definite = reach_matrix(n, cd)
    possible = reach_matrix(n, list(cd) + [tuple(e) for e in cu] + [tuple(e)[::-1] for e in cu])
    out = {}
    for t in targets:
        for y in range(n):
            if y == t:
                continue
            out[(t, y)] = "yes" if definite[t, y] else ("no" if not possible[t, y] else "abstain")
    return out


def targets_of(intfile, CA):
    s = CA.load(intfile)
    I = s["intervened"]
    single = I.sum(1) == 1
    return [t for t in range(I.shape[1]) if int((I[:, t] & single).sum()) >= 5]


# ----------------------------------------------------------------------------------------------------------------- run
METHOD_FILES = {  # label -> {family: {arm: file stem}}
    "PC (Causal-Copilot copy)": {"semantic": {"released": "pc_semantic_obs_rel", "shuffled": "pc_semantic_obs_shuf"},
                                 "formula": {"released": "pc_formula_obs_rel", "shuffled": "pc_formula_obs_shuf"},
                                 "synthetic": {"released": "pc_synthetic100_rel", "shuffled": "pc_synthetic100_shuf"}},
    "PC (upstream causal-learn)": {"semantic": {"released": "pc_upstream_semantic_obs_rel", "shuffled": "pc_upstream_semantic_obs_shuf"},
                                   "formula": {"released": "pc_upstream_formula_obs_rel", "shuffled": "pc_upstream_formula_obs_shuf"}},
    "PC maxP (upstream)": {"semantic": {"released": "pc_upstream_maxp_semantic_obs_rel", "shuffled": "pc_upstream_maxp_semantic_obs_shuf"},
                           "formula": {"released": "pc_upstream_maxp_formula_obs_rel", "shuffled": "pc_upstream_maxp_formula_obs_shuf"}},
    "GES (BIC)": {"semantic": {"released": "gesbic_semantic_obs", "shuffled": "gesbic_semantic_obs_shuf"},
                  "formula": {"released": "gesbic_formula_obs_rel", "shuffled": "gesbic_formula_obs_shuf"},
                  "synthetic": {"released": "gesbic_synthetic100_rel", "shuffled": "gesbic_synthetic100_shuf"}},
    "FCI": {"semantic": {"released": "fci_semantic_obs", "shuffled": "fci_semantic_obs_shuf"},
            "formula": {"released": "fci_formula_obs_rel", "shuffled": "fci_formula_obs_shuf"},
            "synthetic": {"released": "fci_synthetic100_rel", "shuffled": "fci_synthetic100_shuf"}},
    "DirectLiNGAM": {"semantic": {"released": "lingam_semantic_obs_rel", "shuffled": "lingam_semantic_obs_shuf"},
                     "formula": {"released": "lingam_formula_obs_rel", "shuffled": "lingam_formula_obs_shuf"},
                     "synthetic": {"released": "lingam_synthetic100_rel", "shuffled": "lingam_synthetic100_shuf"}},
    "NOTEARS": {"semantic": {"released": "notears_semantic_obs_rel", "shuffled": "notears_semantic_obs_shuf"},
                "formula": {"released": "notears_formula_obs_rel", "shuffled": "notears_formula_obs_shuf"},
                "synthetic": {"released": "notears_synthetic100_rel", "shuffled": "notears_synthetic100_shuf"}},
}


class Data:
    def __init__(self, root, cc):
        _import_cc(cc)
        import causalarena_io as CA
        import causalarena_load as L
        import cc_graph as G
        self.CA, self.L, self.G = CA, L, G
        self.root = Path(root)
        self._cache = {}

    def folder(self, fam):
        return self.root / "scm" / fam / "data" / ("synthetic_obs_only" if fam == "synthetic" else "%s_obs_only" % fam)

    def files(self, fam):
        return sorted(os.listdir(self.folder(fam)))

    def truth(self, fam, file):
        key = (fam, file)
        if key not in self._cache:
            s = self.L.load_any(self.folder(fam) / file)
            T = self.CA.true_edges(s["g"])
            n = len(s["node_ids"])
            cd, cu = cpdag_parts(T, n, self.G)
            self._cache[key] = {"T": T, "n": n, "cd": cd, "cu": cu}
        return self._cache[key]

    def sample(self, fam, file):
        return self.L.load_any(self.folder(fam) / file)


def load_rows(methods_dir, stem):
    p = Path(methods_dir) / (stem + ".json")
    if not p.exists():
        return None
    return [r for r in json.load(open(p))["rows"] if not r.get("failed")]


def mx(xs):
    xs = [abs(x) for x in xs]
    return max(xs) if xs else 0.0


def check_truth(data, families):
    """Preconditions: every true graph is a DAG with no 2-cycles; columns are in a topological order; cc_graph.cpdag_of
    equals causal-learn's dag2cpdag on every file."""
    sys.path.insert(0, str(DEF_CL))
    from causallearn.graph.Dag import Dag
    from causallearn.graph.GraphNode import GraphNode
    from causallearn.utils.DAG2CPDAG import dag2cpdag
    import networkx as nx
    out = {}
    for fam in families:
        n_files = dag = topo = agree = 0
        for f in data.files(fam):
            t = data.truth(fam, f)
            T, n = t["T"], t["n"]
            n_files += 1
            g = nx.DiGraph()
            g.add_nodes_from(range(n))
            g.add_edges_from(T)
            dag += nx.is_directed_acyclic_graph(g) and not any((b, a) in T for a, b in T)
            topo += all(a < b for a, b in T)
            nodes = [GraphNode("X%d" % i) for i in range(n)]
            dg = Dag(nodes)
            for a, b in T:
                dg.add_directed_edge(nodes[a], nodes[b])
            C = dag2cpdag(dg).graph
            cd2, cu2 = set(), set()
            for x in range(n):
                for y in range(x + 1, n):
                    if C[x, y] == -1 and C[y, x] == 1:
                        cd2.add((x, y))
                    elif C[x, y] == 1 and C[y, x] == -1:
                        cd2.add((y, x))
                    elif C[x, y] == -1 and C[y, x] == -1:
                        cu2.add(frozenset((x, y)))
            agree += (cd2 == t["cd"] and cu2 == t["cu"])
        out[fam] = {"files": n_files, "dag_no_2cycles": dag, "columns_topological": topo, "cpdag_matches_causal_learn": agree}
    out["pass"] = all(v["files"] == v["dag_no_2cycles"] == v["cpdag_matches_causal_learn"] for k, v in out.items() if k != "pass")
    return out


def run_t1_t2(data, methods_dir):
    t1, t2 = {"per_method": {}}, {"per_method": {}}
    all_err, all_cq, all_lower, all_both, all_drop, all_support, all_bud, all_cp = [], [], [], [], [], [], [], []
    rows_checked = 0
    one_arrow_viol = 0
    z_fail = []
    for label, fams in METHOD_FILES.items():
        for fam, arms in fams.items():
            for arm, stem in arms.items():
                rows = load_rows(methods_dir, stem)
                if rows is None:
                    continue
                err, cq, lo, bo, dr, sup, diffs, vars_ = [], [], [], [], [], [], [], []
                F, Ss, As, budg, cp = [], [], [], [], []
                for r in rows:
                    t = data.truth(fam, r["file"])
                    T = t["T"]
                    D, U = norm_graph(r["directed_edges"], r["undecided_pairs"])
                    k = coords(D, U, T)
                    one_arrow_viol += not k["one_arrow_per_pair"]
                    m, var, support = expected_f1(D, U, T)
                    err.append(m - k["S"] * k["a"])
                    cq.append(k["a"] - k["a_cq"])
                    pos = None
                    if r.get("shuffle_seed") is not None:
                        perm = np.random.default_rng(int(r["shuffle_seed"]) + zlib.crc32(r["key"].encode())).permutation(t["n"])
                        pos = {int(o): i for i, o in enumerate(perm)}
                    lo.append(r["scores"]["lower"]["f1"] - rule_f1_closed_form("lower", D, U, T, pos))
                    bo.append(r["scores"]["both"]["f1"] - rule_f1_closed_form("both", D, U, T))
                    dr.append(r["scores"]["drop"]["f1"] - rule_f1_closed_form("drop", D, U, T))
                    sampled = r["scores"]["random"]["f1"]
                    sup.append(min(abs(sampled - v) for v in support))
                    diffs.append(sampled - m)
                    vars_.append(var)
                    F.append(m)
                    Ss.append(k["S"])
                    As.append(k["a"])
                    b = budget(D, U, T, t["cd"], t["cu"])
                    b["resid"] = (b["I"] + b["K"] + b["O"]) - (1 - m)
                    budg.append(b)
                    # identifiability term = 1 - F1 of the true CPDAG under the random rule (exact)
                    cpm, _, _ = expected_f1(set(t["cd"]), set(t["cu"]), T)
                    cp.append((1 - cpm) - b["I"])
                    rows_checked += 1
                n = len(rows)
                se = math.sqrt(sum(vars_)) / n if n else 0.0
                z = (st.mean(diffs) / se) if se > 0 else 0.0
                rec = {"rows": n, "max_abs_err_F1_vs_S_times_a": mx(err), "max_abs_err_a_vs_cq_formula": mx(cq),
                       "max_abs_err_lower_rule_closed_form": mx(lo), "max_abs_err_both_rule_closed_form": mx(bo),
                       "max_abs_err_drop_rule_closed_form": mx(dr),
                       "max_dist_sampled_to_support": mx(sup),
                       "mean_sampled_minus_expected": st.mean(diffs) if n else None, "se_of_mean": se, "z": z,
                       "mean_F1_expected": st.mean(F) if n else None,
                       "mean_S_times_mean_a": (st.mean(Ss) * st.mean(As)) if n else None,
                       "mean_of_S_times_a": st.mean([s * a for s, a in zip(Ss, As)]) if n else None}
                t1["per_method"].setdefault(label, {}).setdefault(fam, {})[arm] = rec
                t2["per_method"].setdefault(label, {}).setdefault(fam, {})[arm] = {
                    "rows": n, "max_abs_residual": mx([b["resid"] for b in budg]),
                    "max_abs_I_vs_true_cpdag_F1": mx(cp),
                    **{"mean_" + key: st.mean([b[key] for b in budg]) for key in (
                        "I", "K", "O", "O_wrong_compelled", "O_abstain_compelled", "O_beyond_class",
                        "skeleton_old_style", "orientation_old_style")},
                    "mean_one_minus_F1": st.mean([1 - f for f in F]),
                    "files_K_negative": sum(b["K"] < -TOL for b in budg),
                    "files_O_negative": sum(b["O"] < -TOL for b in budg),
                    "files_beyond_class_negative": sum(b["O_beyond_class"] < -TOL for b in budg)}
                all_err += err; all_cq += cq; all_lower += lo; all_both += bo; all_drop += dr; all_support += sup
                all_bud += [b["resid"] for b in budg]; all_cp += cp
                if abs(z) > 4:
                    z_fail.append((label, fam, arm, z))
                print("T1 %-28s %-9s %-8s n=%3d  max|E F1 - S a| %.1e  lower %.1e both %.1e drop %.1e  support %.1e  z %+.2f"
                      % (label, fam, arm, n, mx(err), mx(lo), mx(bo), mx(dr), mx(sup), z))
    t1["summary"] = {"rows_checked": rows_checked, "rows_violating_one_arrow_condition": one_arrow_viol,
                     "max_abs_err_F1_vs_S_times_a": mx(all_err), "max_abs_err_a_vs_cq": mx(all_cq),
                     "max_abs_err_lower": mx(all_lower), "max_abs_err_both": mx(all_both), "max_abs_err_drop": mx(all_drop),
                     "max_dist_sampled_to_support": mx(all_support), "groups_with_abs_z_over_4": z_fail}
    t1["pass"] = (mx(all_err) <= TOL and mx(all_cq) <= TOL and mx(all_lower) <= TOL and mx(all_both) <= TOL
                  and mx(all_drop) <= TOL and mx(all_support) <= 1e-9 and not z_fail)
    t2["summary"] = {"rows_checked": rows_checked, "max_abs_residual": mx(all_bud), "max_abs_I_vs_true_cpdag_F1": mx(all_cp)}
    t2["pass"] = mx(all_bud) <= TOL and mx(all_cp) <= TOL
    return t1, t2


def run_t3(data, methods_dir, n_random=20, seed=20261012):
    res = {"schemes": {}, "edge_adding_contrast": {}}
    viol = 0
    checks = 0
    max_id_err = 0.0
    max_adv_err = 0.0
    max_k_slack_neg = 0.0
    rows_used = 0
    for fam in ("semantic", "formula"):
        for arm in ("released", "shuffled"):
            rows = load_rows(methods_dir, METHOD_FILES["PC (upstream causal-learn)"][fam][arm])
            for r in rows:
                rows_used += 1
                t = data.truth(fam, r["file"])
                T, n = t["T"], t["n"]
                D, U = norm_graph(r["directed_edges"], r["undecided_pairs"])
                f0, _, _ = expected_f1(D, U, T)
                dep = depth_of(T, n)
                maxd = max(dep.values())
                rng = np.random.default_rng(seed + zlib.crc32(r["file"].encode()) + (0 if arm == "released" else 7))
                schemes = {"true_depth": dep, "reversed_depth": {v: maxd - d for v, d in dep.items()},
                           "reversed_depth_3bins": {v: 2 - min(2, (3 * d) // (maxd + 1)) for v, d in dep.items()}}
                for i in range(n_random):
                    perm = rng.permutation(maxd + 1)
                    schemes["random_depth_order_%02d" % i] = {v: int(perm[d]) for v, d in dep.items()}
                    perm3 = rng.permutation(3)
                    schemes["random_depth_3bins_%02d" % i] = {v: int(perm3[min(2, (3 * d) // (maxd + 1))]) for v, d in dep.items()}
                    schemes["random_variable_tiers_%02d" % i] = {v: int(x) for v, x in enumerate(rng.integers(0, 3, n))}
                adversarial = {}
                for pair in {frozenset(e) for e in D} | U:
                    x, y = tuple(pair)
                    if (x, y) in T:
                        adversarial[pair] = (y, x)
                    elif (y, x) in T:
                        adversarial[pair] = (x, y)
                for name, tier in list(schemes.items()) + [("adversarial_all_pairs", None)]:
                    dec = adversarial if tier is None else tier_decisions(D, U, tier)
                    D2, U2, decided = apply_orientations(D, U, dec)
                    f1, _, _ = expected_f1(D2, U2, T)
                    hb = harm_bounds(D, U, T, decided)
                    k = coords(D, U, T)
                    N = k["nP"] + k["nT"]
                    ident = 2 * sum(credit(D2, U2, T, p) - credit(D, U, T, p) for p in decided) / N
                    delta = f1 - f0
                    max_id_err = max(max_id_err, abs(delta - ident))
                    bad = (delta < -hb["bound_exact"] - TOL) or (hb["bound_exact"] > hb["bound_k"] + TOL) or (delta > hb["gain_bound_exact"] + TOL)
                    viol += bad
                    checks += 1
                    if name in ("reversed_depth", "adversarial_all_pairs"):
                        max_adv_err = max(max_adv_err, abs(delta + hb["bound_exact"]))
                    key = name.rsplit("_", 1)[0] if name[-2:].isdigit() else name
                    agg = res["schemes"].setdefault(key, {"checks": 0, "violations": 0, "delta": [], "bound_exact": [],
                                                          "bound_k": [], "share_of_bound_used": []})
                    agg["checks"] += 1
                    agg["violations"] += bad
                    agg["delta"].append(delta)
                    agg["bound_exact"].append(hb["bound_exact"])
                    agg["bound_k"].append(hb["bound_k"])
                    if delta < 0 and hb["bound_exact"] > 0:
                        agg["share_of_bound_used"].append(-delta / hb["bound_exact"])
                # contrast: knowledge that adds m wrong connections (pairs neither predicted nor true)
                padj = {frozenset(e) for e in D} | U
                tadj = {frozenset(e) for e in T}
                free = [(x, y) for x in range(n) for y in range(x + 1, n) if frozenset((x, y)) not in padj | tadj]
                for m in (1, 5, 25):
                    if len(free) < m:
                        continue
                    pick = [free[i] for i in rng.choice(len(free), m, replace=False)]
                    D3 = D | set(pick)
                    f3, _, _ = expected_f1(D3, U, T)
                    k = coords(D, U, T)
                    N = k["nP"] + k["nT"]
                    formula = f0 * m / (N + m)
                    c = res["edge_adding_contrast"].setdefault(str(m), {"rows": 0, "max_abs_err_formula": 0.0,
                                                                        "rows_harm_exceeds_touched_credit": 0, "harm": []})
                    c["rows"] += 1
                    c["max_abs_err_formula"] = max(c["max_abs_err_formula"], abs((f0 - f3) - formula))
                    c["rows_harm_exceeds_touched_credit"] += (f0 - f3) > TOL      # touched pairs had credit 0
                    c["harm"].append(f0 - f3)
    for key, agg in res["schemes"].items():
        for fld in ("delta", "bound_exact", "bound_k"):
            xs = agg.pop(fld)
            agg["mean_" + fld] = st.mean(xs)
            agg["min_" + fld] = min(xs)
            agg["max_" + fld] = max(xs)
        sh = agg.pop("share_of_bound_used")
        agg["mean_share_of_bound_used_when_harmful"] = st.mean(sh) if sh else None
    for m, c in res["edge_adding_contrast"].items():
        h = c.pop("harm")
        c["mean_harm"] = st.mean(h)
        c["max_harm"] = max(h)
    res["summary"] = {"pc_rows": rows_used, "checks": checks, "violations": viol, "max_abs_err_delta_identity": max_id_err,
                      "max_abs_err_adversarial_attains_bound": max_adv_err}
    res["pass"] = viol == 0 and max_id_err <= TOL and max_adv_err <= TOL
    print("T3 rows %d checks %d violations %d  identity err %.1e  adversarial attains bound err %.1e"
          % (rows_used, checks, viol, max_id_err, max_adv_err))
    return res


def run_t4(data, cl_path, families=("semantic", "formula"), files_every=1):
    out = {"toy": {}, "data": {}}
    expect = {  # prediction written before running causal-learn (worked example in the report)
        ("causal", 0, 2): ["a->b", "c->b", "c-d"],
        ("causal", 0, 0): ["a->b", "b->c", "d->c"],
        ("causal", 1, 3): ["a-b", "b->c", "d->c"],
        ("reversed", 0, 2): ["a-b", "b->c", "d->c"],
        ("reversed", 0, 0): ["a->b", "c->b", "d->c"],
        ("reversed", 1, 3): ["a-b", "b->c", "d->c"],
    }
    toy_ok = True
    for (name, rule, prio), want in expect.items():
        order = ["a", "b", "c", "d"] if name == "causal" else ["d", "c", "b", "a"]
        got = toy_pc(order, rule, prio, cl_path)
        ok = got == want
        toy_ok &= ok
        out["toy"]["%s order, uc_rule=%d, uc_priority=%d" % (name, rule, prio)] = {"got": got, "expected": want, "ok": ok}
        print("T4 toy %-8s rule %d prio %d -> %s %s" % (name, rule, prio, got, "ok" if ok else "MISMATCH"))
    out["toy"]["true_cpdag"] = ["a-b", "b->c", "d->c"]
    if str(cl_path) not in sys.path:
        sys.path.insert(0, str(cl_path))
    from causallearn.utils.cit import CIT
    from causallearn.utils.PCUtils import SkeletonDiscovery, UCSepset, Meek
    tot = collections.Counter()
    for fam in families:
        for arm in ("released", "shuffled"):
            c = collections.Counter()
            for f in data.files(fam)[::files_every]:
                s = data.sample(fam, f)
                X = s["values"][: s["n_obs"]]
                d = X.shape[1]
                perm = list(range(d)) if arm == "released" else \
                    [int(p) for p in np.random.default_rng(SHUFFLE_SEED + zlib.crc32(f.encode())).permutation(d)]
                Xp = X[:, perm]
                try:
                    cg = SkeletonDiscovery.skeleton_discovery(Xp, 0.05, CIT(Xp, "fisherz"), stable=True,
                                                              show_progress=False)
                except ValueError:
                    c["skipped_singular"] += 1
                    continue
                c["files"] += 1
                UT = [(i, j, k) for (i, j, k) in cg.find_unshielded_triples() if i < k]
                mids = [t[1] for t in UT]
                c["files_triples_sorted_by_middle"] += all(a <= b for a, b in zip(mids, mids[1:]))
                claims = {t for t in UT if all(t[1] not in S for S in cg.sepset[t[0], t[2]])}
                T = {(perm.index(a), perm.index(b)) for a, b in data.truth(fam, f)["T"]}   # truth in permuted indices
                claim_at = collections.defaultdict(set)              # pair -> endpoints that carry a collider claim
                for x, y, z in claims:
                    claim_at[frozenset((x, y))].add(y)
                    claim_at[frozenset((z, y))].add(y)
                conflicted = {p for p, ends in claim_at.items() if len(ends) == 2}
                for prio in (2, 0):
                    cg_uc = UCSepset.uc_sepset(cg, prio)
                    cl = cl_arrows(cg_uc.G.graph)
                    model = uc_model(UT, claims, prio)
                    c["files_model_equals_causal_learn_p%d" % prio] += (cl == model)
                    final = cl_arrows(Meek.meek(cg_uc).G.graph)
                    c["files_meek_keeps_uc_arrows_p%d" % prio] += all(final.get(p) == a for p, a in cl.items())
                    for p in conflicted:
                        lo, hi = min(p), max(p)
                        arrow = cl.get(p)
                        c["conflicted_edges_p%d" % prio] += 1
                        c["conflicted_into_lower_p%d" % prio] += arrow == (hi, lo)
                        c["conflicted_into_higher_p%d" % prio] += arrow == (lo, hi)
                        true_arrow = (lo, hi) if (lo, hi) in T else ((hi, lo) if (hi, lo) in T else None)
                        if true_arrow is not None:
                            c["conflicted_true_edges_p%d" % prio] += 1
                            c["conflicted_true_edges_wrong_p%d" % prio] += arrow == (true_arrow[1], true_arrow[0])
                    for p, arrow in cl.items():
                        lo, hi = min(p), max(p)
                        true_arrow = (lo, hi) if (lo, hi) in T else ((hi, lo) if (hi, lo) in T else None)
                        if true_arrow is None or arrow == "bidirected":
                            continue
                        c["uc_true_edges_p%d" % prio] += 1
                        c["uc_true_edges_wrong_p%d" % prio] += arrow != true_arrow
                # claim correctness by endpoint position (true edges only)
                for p, ends in claim_at.items():
                    lo, hi = min(p), max(p)
                    if (lo, hi) in T or (hi, lo) in T:
                        upstream_is_lower = (lo, hi) in T
                        for e in ends:
                            c["claims_on_true_edges"] += 1
                            c["claims_at_lower_endpoint"] += e == lo
                            c["claims_wrong"] += (e == lo) == upstream_is_lower    # a claim at the cause's end is wrong
            out["data"]["%s/%s" % (fam, arm)] = dict(c)
            tot.update({k: v for k, v in c.items()})
            print("T4 data %s/%s %s" % (fam, arm, dict(c)))
    files = tot["files"]
    out["data_summary"] = dict(tot)
    out["pass_toy"] = toy_ok
    out["pass_model"] = all(tot["files_model_equals_causal_learn_p%d" % p] == files for p in (2, 0)) \
        and tot["files_triples_sorted_by_middle"] == files
    out["pass_p0_conflicts_into_higher"] = tot["conflicted_into_higher_p0"] == tot["conflicted_edges_p0"]
    out["pass_meek_keeps_uc_arrows"] = all(tot["files_meek_keeps_uc_arrows_p%d" % p] == files for p in (2, 0))
    out["pass"] = out["pass_toy"] and out["pass_model"] and out["pass_p0_conflicts_into_higher"]
    return out


def run_t5(data, dv_json, max_members=200000):
    import networkx as nx
    out = {"families": {}}
    ok_prec = True
    ok_cov = True
    orig_ok = True
    restated_ok = True
    max_members_seen = 0
    for fam in ("semantic", "formula"):
        c = collections.Counter()
        base = data.root / "scm" / fam / "data"
        for f in data.files(fam):
            intfile = base / ("%s_obs_int" % fam) / f.replace("_obs_only__", "_obs_int__")
            if not intfile.exists():
                c["files_without_int"] += 1
                continue
            targets = targets_of(intfile, data.CA)
            if not targets:
                c["files_without_targets"] += 1
                continue
            t = data.truth(fam, f)
            T, n, cd, cu = t["T"], t["n"], t["cd"], t["cu"]
            c["files"] += 1
            claims = cpdag_claims(n, cd, cu, targets)
            desc = reach_matrix(n, T)
            # every member of the class: compelled arrows + one admissible orientation per chain component
            adj = {frozenset(e) for e in T}
            comps = chain_component_orientations(n, cu, adj)
            size = math.prod(len(cpt) for cpt in comps) if comps else 1
            max_members_seen = max(max_members_seen, size)
            if size > max_members:
                c["files_class_too_large"] += 1
                continue
            yes_all = {k: True for k in claims}
            no_all = {k: True for k in claims}
            members = 0
            for combo in itertools.product(*comps) if comps else [()]:
                arcs = list(cd) + [a for part in combo for a in part]
                R = reach_matrix(n, arcs)
                members += 1
                # each member must reproduce the true CPDAG (same skeleton and v-structures)
                if members <= 64:
                    cd2, cu2 = cpdag_parts(set(arcs), n, data.G)
                    c["members_cpdag_mismatch"] += (cd2 != cd or cu2 != cu)
                for (tt, y) in claims:
                    if R[tt, y]:
                        no_all[(tt, y)] = False
                    else:
                        yes_all[(tt, y)] = False
            c["members"] += members
            for (tt, y), cl in claims.items():
                c["pairs"] += 1
                truth = bool(desc[tt, y])
                const = yes_all[(tt, y)] or no_all[(tt, y)]
                c["constant_over_class"] += const
                if cl == "yes":
                    c["yes"] += 1
                    c["yes_true"] += truth
                    c["yes_true_in_every_member"] += yes_all[(tt, y)]
                elif cl == "no":
                    c["no"] += 1
                    c["no_true"] += not truth
                    c["no_true_in_every_member"] += no_all[(tt, y)]
                else:
                    c["abstain"] += 1
                    c["abstain_but_constant_yes"] += yes_all[(tt, y)]   # implicit definite causes (Fang et al. 2022)
                    c["abstain_but_constant_no"] += no_all[(tt, y)]     # would contradict Zhang/Perkovic completeness
        committed = c["yes"] + c["no"]
        cov = committed / c["pairs"]
        dv = json.load(open(dv_json))["families"][fam]["ceiling: true CPDAG"]["reference"]
        rec = dict(c)
        rec.update({"coverage": cov, "coverage_published_decision_value_json": dv["coverage"],
                    "pairs_published": dv["pairs"],
                    "precision_committed": (c["yes_true"] + c["no_true"]) / committed if committed else None,
                    "constant_share": c["constant_over_class"] / c["pairs"],
                    "implicit_share": c["abstain_but_constant_yes"] / c["pairs"]})
        prec_ok = (c["yes_true"] == c["yes"] == c["yes_true_in_every_member"]
                   and c["no_true"] == c["no"] == c["no_true_in_every_member"])
        cov_ok = abs(cov - dv["coverage"]) <= 5e-5 and c["pairs"] == dv["pairs"]
        rec["pass_precision_one_in_every_member"] = prec_ok
        rec["pass_coverage_matches_measured"] = cov_ok
        rec["original_statement_coverage_equals_constant_share"] = abs(cov - rec["constant_share"]) <= TOL
        rec["restated_coverage_equals_constant_minus_implicit"] = (
            abs(cov - (rec["constant_share"] - rec["implicit_share"])) <= TOL and c["abstain_but_constant_no"] == 0)
        ok_prec &= prec_ok and c["members_cpdag_mismatch"] == 0 and c["files_class_too_large"] == 0
        ok_cov &= cov_ok
        orig_ok &= rec["original_statement_coverage_equals_constant_share"]
        restated_ok &= rec["restated_coverage_equals_constant_minus_implicit"]
        out["families"][fam] = rec
        print("T5 %s files %d pairs %d coverage %.6f (json %.4f) precision %s constant %.6f implicit %.6f members %d"
              % (fam, c["files"], c["pairs"], cov, dv["coverage"], rec["precision_committed"], rec["constant_share"],
                 rec["implicit_share"], c["members"]))
    out["max_class_size"] = max_members_seen
    out["pass_precision"] = ok_prec
    out["pass_coverage_matches_measured"] = ok_cov
    out["pass_original_coverage_statement_on_data"] = orig_ok
    out["pass_restated_coverage_statement"] = restated_ok
    out["pass"] = ok_prec and ok_cov and restated_ok
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cc-analysis", default=str(DEF_CC))
    ap.add_argument("--root", default=None, help="CausalArena release (default: <cc-analysis>/../external/causalarena)")
    ap.add_argument("--methods", default=None, help="learned graphs (default: <cc-analysis>/results/methods)")
    ap.add_argument("--causal-learn", default=str(DEF_CL))
    ap.add_argument("--dv-json", default=str(HERE / "results" / "decision_value" / "decision_value.json"))
    ap.add_argument("--out", default=str(HERE / "results" / "theory"))
    ap.add_argument("--only", nargs="*", default=["T1", "T2", "T3", "T4", "T5"])
    a = ap.parse_args()
    cc = Path(a.cc_analysis)
    root = a.root or str(cc.parent / "external" / "causalarena")
    methods = a.methods or str(cc / "results" / "methods")
    data = Data(root, cc)
    t0 = time.time()
    report = {"bundle": "AB-09", "tickets": ["AUD-40", "RQ-04", "RQ-06"], "prediction": "P12", "tolerance": TOL,
              "inputs": {"root": root, "methods": methods, "causal_learn": a.causal_learn, "dv_json": a.dv_json},
              "statements": {}}
    report["preconditions"] = check_truth(data, ("semantic", "formula", "synthetic"))
    print("preconditions", report["preconditions"])
    if "T1" in a.only or "T2" in a.only:
        t1, t2 = run_t1_t2(data, methods)
        report["statements"]["T1"] = t1
        report["statements"]["T2"] = t2
    if "T3" in a.only:
        report["statements"]["T3"] = run_t3(data, methods)
    if "T4" in a.only:
        report["statements"]["T4"] = run_t4(data, a.causal_learn)
    if "T5" in a.only:
        report["statements"]["T5"] = run_t5(data, a.dv_json)
    report["pass"] = {k: v["pass"] for k, v in report["statements"].items()}
    refuted = []
    if "T5" in report["statements"] and not report["statements"]["T5"]["pass_original_coverage_statement_on_data"]:
        refuted.append({"statement": "T5 (as briefed): coverage of the true CPDAG's directed-path rule equals the share "
                                     "of pairs whose answer is constant over the equivalence class",
                        "counterexample": {f: {"pairs_constant_yes_but_abstained": v["abstain_but_constant_yes"],
                                               "pairs": v["pairs"], "coverage": v["coverage"],
                                               "constant_share": v["constant_share"]}
                                           for f, v in report["statements"]["T5"]["families"].items()},
                        "restated": "coverage = constant share - share of definite causes with no directed path in the "
                                    "CPDAG; 'pass' for T5 refers to the restated form"})
    report["refuted_as_originally_stated"] = refuted
    report["P12_holds_as_restated"] = all(report["pass"].values()) and report["preconditions"]["pass"]
    report["seconds"] = round(time.time() - t0, 1)
    os.makedirs(a.out, exist_ok=True)
    json.dump(report, open(os.path.join(a.out, "theory_checks.json"), "w"), indent=1, default=str)
    json.dump({"producer": "analysis/theory_checks.py", "score_bearing": False, "tickets": ["AUD-40", "RQ-04", "RQ-06"],
               "split": "all-public (verification of identities and bounds; no tuning, no new scores)",
               "outputs": ["theory_checks.json"], "report": "analysis/reports/ab09_theory_pack.md"},
              open(os.path.join(a.out, "CONTRACT.json"), "w"), indent=1)
    print("pass", report["pass"], "P12 (as restated)", report["P12_holds_as_restated"], "seconds", report["seconds"])


if __name__ == "__main__":
    main()
