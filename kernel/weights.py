"""K2 decisions as a resource (kernel v3).

A decision is one open pair: the ledger connects x and y and leaves the direction open. Deciding it settles more than
itself: Meek's rules may orient other open pairs, and "does y move if I set t?" answers (DV-1) may change from abstain
to a committed yes or no. The weight of a decision is that reach, computed from the ledger alone (no truth):

  settle(x -> y)  pairs Meek's closure orients after adding x -> y to the ledger's directed claims (itself excluded)
  answers(x -> y) DV-1 answers over the released targets that change (abstain -> committed, or committed -> other)
  weight(pair)    1 + mean over the two orientations of (settle + answers), and 0 for a pair whose either orientation
                  would close a directed cycle on its own (it is decided by the cycle check, not by evidence)

apply_tiers_propagating(led_d, statements): B3's rule (consensus, orient-only, cycle skip) followed by Meek closure of
data + knowledge directions over the open pairs. A propagated orientation is a claim with direction_source "knowledge",
licence "meek_from_tier", and the knowledge claims it rests on as premises. It changes T3's k: the bound uses every pair
knowledge decided directly or by propagation (theory pack T3), and the report records both counts.
"""
import copy

from . import policy
from .knowledge import apply_tiers
from .ledger_hash import canonical_hash


def _graph(led):
    pos = {v["name"]: v["position"] for v in led["variables"]}
    D, U = set(), set()
    for c in led["claims"]:
        a, b = pos[c["x"]], pos[c["y"]]
        if c["relation"] == "x->y":
            D.add((a, b))
        elif c["relation"] in ("x-y", "x<->y"):
            U.add(tuple(sorted((a, b))))
    return D, U, pos


def decision_weights(n, D, U, targets):
    """-> {pair: {"weight", "settle": [ab, ba], "answers": [ab, ba], "cycle": bool}} for every open pair."""
    from score import dv
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    base = dv.claims(n, D, U, targets)
    out = {}
    for a, b in sorted(U):
        st, an, cyc = [], [], False
        for x, y in ((a, b), (b, a)):
            if _reach(D, y, x):
                cyc = True
                st.append(0)
                an.append(0)
                continue
            D2, _ = policy.meek_closure(n, adj, D | {(x, y)})
            new = D2 - D - {(x, y)}
            U2 = {u for u in U if (u[0], u[1]) not in D2 and (u[1], u[0]) not in D2}
            cl = dv.claims(n, D2, U2, targets)
            changed = sum(1 for k in set(base) | set(cl) if base.get(k) != cl.get(k))
            st.append(len(new))
            an.append(changed)
        out[(a, b)] = {"weight": 0.0 if cyc else 1.0 + (sum(st) + sum(an)) / 2.0, "settle": st, "answers": an, "cycle": cyc}
    return out


def _reach(D, src, dst):
    nxt = {}
    for a, b in D:
        nxt.setdefault(a, set()).add(b)
    stack, seen = [src], {src}
    while stack:
        u = stack.pop()
        for v in nxt.get(u, ()):
            if v == dst:
                return True
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return False


def apply_tiers_propagating(led_d, statements, outcomes=None, min_answering=2):
    led, info = apply_tiers(led_d, statements, outcomes, min_answering)
    D, U, pos = _graph(led)
    names = {p: nm for nm, p in pos.items()}
    n = len(pos)
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    data_dirs = {(pos[c["x"]], pos[c["y"]]) for c in led_d["claims"] if c["relation"] == "x->y"}
    # only what knowledge adds counts: closure(data + knowledge) minus closure(data), so that with no knowledge the ledger
    # is unchanged (I3), the same class of fix as the B2 intervention closure (only the added closure counts)
    base, _ = policy.meek_closure(n, adj, data_dirs)
    D2, why = policy.meek_closure(n, adj, D)
    new = sorted(D2 - D - base)
    by_pair = {tuple(sorted((pos[c["x"]], pos[c["y"]]))): c for c in led["claims"]}
    cid = {k: c["id"] for k, c in by_pair.items()}
    propagated = []
    for a, b in new:
        c = by_pair[tuple(sorted((a, b)))]
        rule, prem = why.get((a, b), ("meek", []))
        prem_ids = sorted(cid[tuple(sorted(p))] for p in prem if tuple(sorted(p)) in cid)
        rests_on_knowledge = any(by_pair[tuple(sorted(p))]["direction_source"] == "knowledge" for p in prem if tuple(sorted(p)) in by_pair)
        c.update({"x": names[a], "y": names[b], "relation": "x->y", "direction_source": "knowledge" if rests_on_knowledge else "data_pattern",
                  "licensed_by": ("%s_from_tier" % rule) if rests_on_knowledge else rule, "derived_from": prem_ids})
        propagated.append([names[a], names[b], rule])
    ka = led["report"]["knowledge_application"]
    nP = ka["claimed_adjacencies"]
    k_total = len(info["decided"]) + len(propagated)
    ka.update({"rule": ka["rule"].replace("no propagation", "Meek propagation from data + knowledge directions (K2)"),
               "propagated": len(propagated), "propagated_pairs": propagated,
               "t3_bound_truth_free": (k_total / nP) if nP else 0.0})
    led["report"]["ledger_sha256"] = canonical_hash(led)
    info = dict(info, propagated=propagated, data_dirs=len(data_dirs))
    return led, info
