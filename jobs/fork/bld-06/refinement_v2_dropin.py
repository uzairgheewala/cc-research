"""Refinement v2 (cc-research BLD-06 / BND-11) as a drop-in for Judge.quality_judge. Self-contained: numpy only.

The data part never deletes an adjacency the algorithm found; an absent pair is added only when the bootstrap connects it
in at least 90% of resamples; the type of every kept or added pair is the commonest typed bootstrap outcome (ties to the
algorithm's own type, then to non-directed types). The names part asks the model only about pairs the data leave
adjacent but undirected, three paraphrases each, and uses a direction only when all three agree, it does not contradict a
mark the data set, and it creates no directed cycle. Every edge gets a source.

Identical in logic to cc-research analysis/refinement_v2.py (v2d, apply_names) and analysis/refinement_v1.py (typed_freqs,
put, ORDER); cc-research tests/test_fork_patches.py checks the two give the same graphs.
Matrix convention as the repo: M[i, j] = 1 means j -> i; codes 2-6 for non-directed marks.
"""
import itertools
import json

import numpy as np

ADD = 0.9
ORDER = ["undirected", "o-o", "bidirected", "a o-> b", "b o-> a", "a o- b", "b o- a", "a->b", "b->a"]
ASKABLE = {"undirected", "o-o", "a o-> b", "b o-> a", "a o- b", "b o- a"}
COMPATIBLE = {"undirected": {"a->b", "b->a"}, "o-o": {"a->b", "b->a"}, "a o-> b": {"a->b"}, "b o-> a": {"b->a"},
              "a o- b": {"b->a"}, "b o- a": {"a->b"}}
PARAPHRASES = [
    "Consider two variables in a dataset: A = \"{a}\" and B = \"{b}\". Based only on what the names mean, which causes which? "
    "Reply with JSON only: {{\"direction\": \"A->B\"}}, {{\"direction\": \"B->A\"}} or {{\"direction\": \"unknown\"}}.",
    "Variable A is \"{a}\". Variable B is \"{b}\". If one of them is a direct cause of the other, which direction is it? "
    "If the names do not tell you, say unknown. Answer as JSON only: {{\"direction\": \"A->B\" | \"B->A\" | \"unknown\"}}.",
    "From domain knowledge about the names alone: does \"{a}\" (A) influence \"{b}\" (B), or does B influence A? "
    "Return JSON only, one of {{\"direction\": \"A->B\"}}, {{\"direction\": \"B->A\"}}, {{\"direction\": \"unknown\"}}.",
]
VALID = {"A->B", "B->A", "unknown"}


def pairs(p):
    return list(itertools.combinations(range(p), 2))


def is_adjacent(M, a, b):
    return bool(M[a, b] != 0 or M[b, a] != 0)


def pair_type(M, a, b):
    x, y = int(M[a, b]), int(M[b, a])
    if x == 0 and y == 0:
        return "none"
    if x == 1 and y == 1:
        return "conflict(both directions)"
    if x == 1 and y == 0:
        return "b->a"
    if y == 1 and x == 0:
        return "a->b"
    codes = {c for c in (x, y) if c != 0}
    if codes == {2}:
        return "undirected"
    if codes == {3}:
        return "bidirected"
    if codes == {6}:
        return "o-o"
    if codes == {7}:
        return "associated"
    if x == 4 and y == 0:
        return "b o-> a"
    if y == 4 and x == 0:
        return "a o-> b"
    if x == 5 and y == 0:
        return "b o- a"
    if y == 5 and x == 0:
        return "a o- b"
    return "mixed(%d,%d)" % (x, y)


def typed_freqs(boot, a, b):
    T = {k: np.asarray(v, dtype=float) for k, v in boot.items()}
    return {"a->b": T["certain_edges"][b, a], "b->a": T["certain_edges"][a, b], "undirected": T["uncertain_edges"][a, b],
            "bidirected": T["bi_edges"][a, b], "a o-> b": T["half_certain_edges"][b, a], "b o-> a": T["half_certain_edges"][a, b],
            "a o- b": T["half_uncertain_edges"][b, a], "b o- a": T["half_uncertain_edges"][a, b], "o-o": T["none_edges"][a, b]}


def put(M, a, b, t):
    if t == "a->b":
        M[b, a] = 1
    elif t == "b->a":
        M[a, b] = 1
    elif t == "undirected":
        M[a, b] = 2
    elif t == "bidirected":
        M[a, b] = 3
    elif t == "a o-> b":
        M[b, a] = 4
    elif t == "b o-> a":
        M[a, b] = 4
    elif t == "a o- b":
        M[b, a] = 5
    elif t == "b o- a":
        M[a, b] = 5
    elif t == "o-o":
        M[a, b] = 6
    else:
        raise ValueError(t)


def v2d(S0, boot):
    S0 = np.asarray(S0)
    p = S0.shape[0]
    M = np.zeros((p, p), dtype=int)
    sources = []
    none = np.asarray(boot["none_existence"], dtype=float)
    for a, b in pairs(p):
        conn = 1.0 - float(none[a, b])
        adj0 = is_adjacent(S0, a, b)
        if not (adj0 or conn >= ADD):
            continue
        t0 = pair_type(S0, a, b) if adj0 else None
        fr = typed_freqs(boot, a, b)
        top = max(fr.values())
        if top <= 0 or (adj0 and t0 not in ORDER):
            if adj0 and t0 not in ORDER:
                M[a, b], M[b, a] = S0[a, b], S0[b, a]
                sources.append({"pair": [a, b], "type": t0, "source": "algorithm", "connected": round(conn, 4)})
                continue
            t = t0 if t0 in ORDER else "undirected"
        else:
            tied = [k for k in ORDER if abs(fr[k] - top) < 1e-12]
            t = t0 if t0 in tied else tied[0]
        put(M, a, b, t)
        src = "bootstrap: added" if not adj0 else ("algorithm" if t == t0 else "algorithm; type from bootstrap")
        sources.append({"pair": [a, b], "type": t, "source": src, "connected": round(conn, 4)})
    return M, sources


def parse_reply(reply):
    """The direction in a reply (a JSON string or an already-parsed dict), or None if it is not exactly what was asked."""
    d = reply
    if isinstance(reply, str):
        try:
            d = json.loads(reply)
        except ValueError:
            return None
    if not isinstance(d, dict) or set(d) != {"direction"} or d["direction"] not in VALID:
        return None
    return d["direction"]


def committed(M):
    out = set()
    for a, b in pairs(M.shape[0]):
        t = pair_type(M, a, b)
        if t == "a->b":
            out.add((a, b))
        elif t == "b->a":
            out.add((b, a))
    return out


def creates_cycle(edges, new):
    a, b = new
    ch = {}
    for x, y in edges:
        ch.setdefault(x, []).append(y)
    seen, stack = set(), [b]
    while stack:
        v = stack.pop()
        if v == a:
            return True
        for c in ch.get(v, ()):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return False


def askable_pairs(M):
    return [(a, b) for a, b in pairs(M.shape[0]) if pair_type(M, a, b) in ASKABLE]


def apply_names(M, answers_for_pair):
    V = np.array(M, dtype=int)
    edges = committed(V)
    recs = []
    for (a, b) in sorted(answers_for_pair):
        t = pair_type(V, a, b)
        ans = answers_for_pair[(a, b)]
        rec = {"pair": [a, b], "type_by_data": t, "answers": ans, "used": False}
        if t not in ASKABLE:
            rec["why"] = "pair not askable in the v2d graph"
        elif any(x is None for x in ans):
            rec["why"] = "abstained (invalid reply after one retry)"
        elif len(set(ans)) != 1 or ans[0] == "unknown":
            rec["why"] = "paraphrases disagree or unknown"
        else:
            d = "a->b" if ans[0] == "A->B" else "b->a"
            new = (a, b) if d == "a->b" else (b, a)
            if d not in COMPATIBLE[t]:
                rec["why"] = "contradicts the mark set by the data"
            elif creates_cycle(edges, new):
                rec["why"] = "would create a directed cycle"
            else:
                V[a, b], V[b, a] = 0, 0
                put(V, a, b, d)
                edges.add(new)
                rec.update({"used": True, "direction": d, "source": "names"})
        recs.append(rec)
    return V, recs


def ask_names(ask, names, M):
    """ask(prompt) -> reply (dict or str). Three paraphrases per askable pair, one retry on an invalid reply."""
    answers = {}
    for a, b in askable_pairs(M):
        got = []
        for tpl in PARAPHRASES:
            prompt = tpl.format(a=names[a], b=names[b])
            r = None
            for _ in range(2):
                try:
                    r = parse_reply(ask(prompt))
                except Exception:          # a failed call counts as an invalid reply (no crash path)
                    r = None
                if r is not None:
                    break
            got.append(r)
        answers[(a, b)] = got
    return answers


def refine(S0, boot, names, ask=None):
    """-> (graph, record). ask=None runs the data part only."""
    M, sources = v2d(S0, boot)
    if ask is None:
        return M, {"refinement": "v2d", "sources": sources, "names": []}
    V, recs = apply_names(M, ask_names(ask, names, M))
    return V, {"refinement": "v2", "sources": sources, "names": recs}
