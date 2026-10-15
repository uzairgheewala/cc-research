"""Data-only combination rules over the two data-pattern engines (D1.3; design doc section 4).

Input, in canonical index space: PC's derived graph with its labels, and GES's CPDAG (or None when GES failed).
Output: {pair (a, b), a < b: Decision}. Every rule keeps both engines' records; the rule only decides what is claimed.

  pc   PC maxP alone (the floor's comparator, re-derived acyclic; see kernel.derive)
  ges  GES (BIC) alone
  C1   agreement: adjacent where both engines are; a direction where both commit the same one; else open
  C2   union with source: adjacent where either engine is; a direction where both agree, or where one commits and the
       other is silent (not adjacent or undirected); opposite commitments leave the pair open
  C3   GES-led, PC-audited: GES's adjacencies; a GES direction that PC's committed direction contradicts is opened, and
       so is any GES direction that can no longer be derived (v-structures touching an opened pair are dropped, then
       Meek R1-R3 re-run over GES's skeleton with the opened pairs blocked; a direction survives only if it is both
       re-derived and committed by GES)
A file on which GES failed falls back to `pc` under every rule, and the run report says so (policy_fallback).
"""
from dataclasses import dataclass, field


@dataclass
class Decision:
    relation: str                 # "a->b", "b->a", "a-b", "none"  (a < b in canonical index space)
    engines: str                  # "pc", "ges", "both", "none"
    licensed_by: str
    conflict: bool = False
    premises: list = field(default_factory=list)   # pairs an orientation rule relied on


RULES = ("pc", "ges", "C1", "C2", "C3")


def _rel(D, U, a, b):
    if (a, b) in D:
        return "a->b"
    if (b, a) in D:
        return "b->a"
    if (a, b) in U or (b, a) in U:
        return "a-b"
    return "none"


def _committed(rel):
    return rel in ("a->b", "b->a")


def vstructures(D, adj):
    """Unshielded colliders x -> c <- y (x < y, x and y not adjacent) in a partially directed graph."""
    parents = {}
    for x, c in D:
        parents.setdefault(c, set()).add(x)
    out = []
    for c, ps in parents.items():
        ps = sorted(ps)
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                if frozenset((ps[i], ps[j])) not in adj:
                    out.append((ps[i], c, ps[j]))
    return sorted(out)


def meek_closure(n, adj, D0, blocked=frozenset()):
    """Meek R1-R3 from the directed set D0 over the skeleton `adj` (set of frozensets); pairs in `blocked` are never
    oriented; an orientation that would close a directed cycle is skipped. Deterministic (pairs in sorted order).
    Returns (directed set, {edge: (rule, [premise edges])})."""
    D = set(D0)
    why = {}

    def und(u, v):
        return frozenset((u, v)) in adj and (u, v) not in D and (v, u) not in D

    def reach(src, dst):
        stack, seen = [src], {src}
        while stack:
            u = stack.pop()
            for (a, b) in D:
                if a == u and b not in seen:
                    if b == dst:
                        return True
                    seen.add(b)
                    stack.append(b)
        return False
    changed = True
    while changed:
        changed = False
        for pr in sorted(tuple(sorted(p)) for p in adj):
            x, y = pr
            if not und(x, y) or frozenset(pr) in blocked:
                continue
            for (u, v) in ((x, y), (y, x)):
                others = [w for w in range(n) if w not in (u, v)]
                prem = None
                rule = None
                for w in others:
                    if (w, u) in D and frozenset((w, v)) not in adj:
                        rule, prem = "meek_r1", [(w, u)]
                        break
                if rule is None:
                    for w in others:
                        if (u, w) in D and (w, v) in D:
                            rule, prem = "meek_r2", [(u, w), (w, v)]
                            break
                if rule is None:
                    for i_ in range(len(others)):
                        for j_ in range(i_ + 1, len(others)):
                            p_, q_ = others[i_], others[j_]
                            if und(u, p_) and und(u, q_) and (p_, v) in D and (q_, v) in D and frozenset((p_, q_)) not in adj:
                                rule, prem = "meek_r3", [(p_, v), (q_, v)]
                                break
                        if rule:
                            break
                if rule and not reach(v, u):
                    D.add((u, v))
                    why[(u, v)] = (rule, prem)
                    changed = True
                    break
    return D, why


def label_cpdag(n, D, U):
    """Labels for a CPDAG's directed edges: v_structure, meek_rN (re-derived), else score_search."""
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    vs = vstructures(D, adj)
    D0 = {(x, c) for x, c, y in vs} | {(y, c) for x, c, y in vs}
    Dm, why = meek_closure(n, adj, D0)
    labels = {}
    for e in D:
        if e in D0:
            labels[e] = ("v_structure", [])
        elif e in why and e in Dm:
            labels[e] = why[e]
        else:
            labels[e] = ("score_search", [])
    return labels


def decide(rule, n, pc, ges):
    """pc: {"D", "U", "labels": {edge: (licence, premises)}}; ges: same or None. -> ({pair: Decision}, fallback flag)."""
    fallback = False
    if rule != "pc" and ges is None:
        rule, fallback = "pc", True
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    out = {}
    if rule in ("pc", "ges"):
        g = pc if rule == "pc" else ges
        for a, b in pairs:
            r = _rel(g["D"], g["U"], a, b)
            e = (a, b) if r == "a->b" else (b, a)
            lic, prem = g["labels"].get(e, ("adjacency_test" if rule == "pc" else "score_search", [])) if _committed(r) else \
                ("adjacency_test" if rule == "pc" else "score_search", [])
            out[(a, b)] = Decision(r, rule if r != "none" else "none", lic, False, prem)
        return out, fallback
    if rule == "C3":
        adj = {frozenset(e) for e in ges["D"]} | {frozenset(u) for u in ges["U"]}
        conflicts = set()
        for a, b in pairs:
            rp, rg = _rel(pc["D"], pc["U"], a, b), _rel(ges["D"], ges["U"], a, b)
            if _committed(rp) and _committed(rg) and rp != rg:
                conflicts.add(frozenset((a, b)))
        vs = [t for t in vstructures(ges["D"], adj) if frozenset((t[0], t[1])) not in conflicts and frozenset((t[2], t[1])) not in conflicts]
        D0 = {(x, c) for x, c, y in vs} | {(y, c) for x, c, y in vs}
        Dm, why = meek_closure(n, adj, D0, blocked=frozenset(conflicts))
        Dfinal = Dm & set(ges["D"])
        for a, b in pairs:
            if frozenset((a, b)) not in adj:
                rp = _rel(pc["D"], pc["U"], a, b)
                out[(a, b)] = Decision("none", "none", "score_search", rp != "none", [])
                continue
            rp = _rel(pc["D"], pc["U"], a, b)
            eng = "both" if rp != "none" else "ges"
            if (a, b) in Dfinal or (b, a) in Dfinal:
                e = (a, b) if (a, b) in Dfinal else (b, a)
                lic, prem = ("v_structure", []) if e in D0 else why.get(e, ("score_search", []))
                out[(a, b)] = Decision("a->b" if e == (a, b) else "b->a", eng, lic, False, prem)
            else:
                out[(a, b)] = Decision("a-b", eng, "score_search", frozenset((a, b)) in conflicts, [])
        return out, fallback
    for a, b in pairs:
        rp, rg = _rel(pc["D"], pc["U"], a, b), _rel(ges["D"], ges["U"], a, b)
        inp, ing = rp != "none", rg != "none"
        adjacent = (inp and ing) if rule == "C1" else (inp or ing)
        if not adjacent:
            out[(a, b)] = Decision("none", "none", "adjacency_test" if not inp else "score_search", inp != ing, [])
            continue
        eng = "both" if (inp and ing) else ("pc" if inp else "ges")
        conflict = _committed(rp) and _committed(rg) and rp != rg
        if _committed(rp) and _committed(rg) and rp == rg:
            r, src = rp, pc
        elif rule == "C2" and _committed(rp) and not _committed(rg):
            r, src = rp, pc
        elif rule == "C2" and _committed(rg) and not _committed(rp):
            r, src = rg, ges
        else:
            r, src = "a-b", None
        if _committed(r):
            e = (a, b) if r == "a->b" else (b, a)
            lic, prem = src["labels"].get(e, ("score_search", []))
        else:
            lic, prem = ("adjacency_test" if inp else "score_search"), []
        out[(a, b)] = Decision(r, eng, lic, conflict, prem)
    return out, fallback


def cyclic_edges(D):
    """Directed edges that lie on a directed cycle (both ends in one strongly connected component of size > 1)."""
    nodes = sorted({v for e in D for v in e})
    succ = {v: [] for v in nodes}
    for a, b in D:
        succ[a].append(b)
    index, low, on, stack, comp, counter = {}, {}, set(), [], {}, [0]

    def strong(v):                                   # Tarjan, iterative enough for these sizes
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in succ[v]:
            if w not in index:
                strong(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            members = []
            while True:
                w = stack.pop()
                on.discard(w)
                members.append(w)
                if w == v:
                    break
            for w in members:
                comp[w] = (v, len(members))
    import sys as _s
    _s.setrecursionlimit(max(_s.getrecursionlimit(), 10000))
    for v in nodes:
        if v not in index:
            strong(v)
    return {(a, b) for a, b in D if comp[a][0] == comp[b][0] and comp[a][1] > 1}


def open_cycles(D, U):
    """Every orientation on a directed cycle is withdrawn (the pair stays adjacent, direction open): the data patterns that
    licensed them contradict each other. -> (D, U, opened pairs)."""
    cyc = cyclic_edges(D)
    if not cyc:
        return set(D), set(U), []
    D2 = set(D) - cyc
    U2 = set(U) | {tuple(sorted(e)) for e in cyc}
    return D2, U2, sorted(tuple(sorted(e)) for e in cyc)


def guard(decisions, n):
    """Final acyclicity guard on a rule's decisions (any rule, e.g. C2's union of two engines' directions):
    decisions on a directed cycle become open, marked as a conflict. -> (decisions, opened pairs)."""
    D = set()
    for (a, b), d in decisions.items():
        if d.relation == "a->b":
            D.add((a, b))
        elif d.relation == "b->a":
            D.add((b, a))
    cyc = cyclic_edges(D)
    opened = []
    for e in sorted(cyc):
        k = tuple(sorted(e))
        d = decisions[k]
        decisions[k] = Decision("a-b", d.engines, "adjacency_test" if d.engines in ("pc", "both") else "score_search", True, [])
        opened.append(k)
    return decisions, opened
