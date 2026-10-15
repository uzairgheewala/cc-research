"""Interventions as order evidence (bundle B2; D2.1; guarantee G6, invariant I6).

  ev = shift_evidence(obs, int_rows_by_target, names, alpha=0.01)
  led_i, info = apply_interventions(led_d, ev)

Evidence: for every target T with at least 5 rows that intervene on T alone, and every other variable Y, a Welch
two-sample statistic comparing Y in those rows with Y in the observational rows (two-sided normal approximation, the
AB-04 rule, analysis/decision_value.targets_and_shifts). "T moves Y" when p < alpha: Y is a descendant of T.
Orientation (rules fixed in plans/b2_prereg.json):
  1. an adjacent pair (T, Y) with "T moves Y" is oriented T -> Y (licence i_essential): in a DAG, an adjacent descendant
     is a child. If the data-only ledger directed it Y -> T, the intervention wins and the claim records conflict=True.
  2. both members targets and each moving the other (impossible in a DAG; noise): the pair stays as the data left it and
     the conflict is recorded.
  3. no shift is not used to orient (absence of a shift can be lack of power); it is recorded as evidence only.
  4. Meek R1-R3 over the claimed skeleton from all directed claims; an orientation it adds is source 'intervention'
     (licence meek_rN, derived_from its premises), and a cycle-closing orientation is skipped.
Connections are never added or removed (the skeleton is the data's).
"""
import copy, math

import numpy as np

from . import policy
from .ledger_hash import canonical_hash


def welch(a, b):
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    if va + vb <= 0:
        return 0.0, 1.0
    t = abs(a.mean() - b.mean()) / math.sqrt(va + vb)
    return float(t), float(math.erfc(t / math.sqrt(2)))


def shift_evidence(obs, int_rows_by_target, names, alpha=0.01, min_rows=5):
    """obs: (n_obs, d); int_rows_by_target: {target column: (rows, d) array}. -> list of evidence records."""
    out = []
    for t in sorted(int_rows_by_target):
        rows = int_rows_by_target[t]
        if rows.shape[0] < min_rows:
            continue
        for y in range(obs.shape[1]):
            if y == t:
                continue
            stat, p = welch(rows[:, y], obs[:, y])
            out.append({"id": "i:%s>%s" % (names[t], names[y]), "type": "intervention_shift", "variables": [names[t], names[y]],
                        "conditioning": [], "statistic": stat, "p_value": p, "alpha": alpha, "rows": int(rows.shape[0]),
                        "supports": "x->y" if p < alpha else "none",
                        "rule": "Welch statistic, intervened rows on %s vs observational rows; 'x->y' means %s is a descendant of %s" % (names[t], names[y], names[t])})
    return out


def apply_interventions(led_d, evidence):
    led = copy.deepcopy(led_d)
    rep = led["report"]
    rep["regime"] = {"D": "D+I", "D+K": "D+I+K"}.get(rep["regime"], rep["regime"])
    names = [v["name"] for v in led["variables"]]
    idx = {n: i for i, n in enumerate(names)}
    moves = {}
    for e in evidence:
        if e["supports"] == "x->y":
            moves[(e["variables"][0], e["variables"][1])] = e["id"]
    led["evidence"] = led["evidence"] + evidence
    byid = {frozenset((c["x"], c["y"])): c for c in led["claims"]}
    conflicts, oriented = [], []
    for key, c in sorted(byid.items(), key=lambda kv: kv[1]["id"]):
        if c["relation"] == "none":
            continue
        a, b = sorted(key)
        ab, ba = moves.get((a, b)), moves.get((b, a))
        if ab and ba:
            conflicts.append({"pair": [a, b], "type": "each moves the other", "evidence": [ab, ba]})
            c["conflict"] = True
            c["evidence"] = sorted(set(c["evidence"]) | {ab, ba})
            continue
        if not (ab or ba):
            continue
        cause, effect, eid = (a, b, ab) if ab else (b, a, ba)
        was = (c["x"], c["y"]) if c["relation"] == "x->y" else None
        if was is not None and was != (cause, effect):
            conflicts.append({"pair": [cause, effect], "type": "intervention reverses the data direction", "evidence": [eid],
                              "data_relation": "%s->%s" % was})
            c["conflict"] = True
        c.update({"x": cause, "y": effect, "relation": "x->y", "direction_source": "intervention", "licensed_by": "i_essential",
                  "evidence": sorted(set(c["evidence"]) | {eid})})
        oriented.append([cause, effect])
    # Meek closure, counting only what the intervention orientations add: closure(data + interventions) minus
    # closure(data alone); pairs the data ledger left open as conflicts stay blocked (the rule's own decision)
    n = len(names)
    adj = {frozenset((idx[c["x"]], idx[c["y"]])) for c in led["claims"] if c["relation"] != "none"}
    D_data = {(idx[c["x"]], idx[c["y"]]) for c in led_d["claims"] if c["relation"] == "x->y"}
    D_int = {(idx[a], idx[b]) for a, b in oriented}
    D0 = {(idx[c["x"]], idx[c["y"]]) for c in led["claims"] if c["relation"] == "x->y"}
    blocked = frozenset(frozenset((idx[c["x"]], idx[c["y"]])) for c in led_d["claims"] if c["relation"] == "x-y" and c.get("conflict"))
    Dm_base, _ = policy.meek_closure(n, adj, D_data, blocked=blocked)
    Dm, why = policy.meek_closure(n, adj, D0, blocked=blocked)
    added = Dm - D0 - Dm_base
    cid = {frozenset((idx[c["x"]], idx[c["y"]])): c["id"] for c in led["claims"]}
    propagated = []
    for e in sorted(added):
        c = byid[frozenset((names[e[0]], names[e[1]]))]
        rule, prem = why[e]
        c.update({"x": names[e[0]], "y": names[e[1]], "relation": "x->y", "direction_source": "intervention", "licensed_by": rule,
                  "derived_from": sorted(cid[frozenset(p)] for p in prem)})
        propagated.append([names[e[0]], names[e[1]]])
    # acyclicity guard: orientations on a directed cycle contradict each other and are withdrawn
    Dn = {(idx[c["x"]], idx[c["y"]]) for c in led["claims"] if c["relation"] == "x->y"}
    for e in sorted(policy.cyclic_edges(Dn)):
        c = byid[frozenset((names[e[0]], names[e[1]]))]
        conflicts.append({"pair": [names[e[0]], names[e[1]]], "type": "directed cycle after interventions; orientation withdrawn"})
        c.update({"relation": "x-y", "direction_source": "intervention", "licensed_by": "none", "conflict": True, "derived_from": []})
    rep["intervention_application"] = {"rule": "adjacent descendant -> child (i_essential), intervention over data; Meek closure; no shift not used",
                                       "targets": sorted({e["variables"][0] for e in evidence}), "shift_tests": len(evidence),
                                       "shifts": len(moves), "oriented": oriented, "propagated": propagated, "conflicts": conflicts}
    rep["ledger_sha256"] = canonical_hash(led)
    return led, {"oriented": oriented, "propagated": propagated, "conflicts": conflicts}


def split_rows(rows, seed, share=0.5):
    """Deterministic split of one regime's rows into an evidence half and a check half (Chambers agreement check)."""
    rng = np.random.default_rng(seed)
    idx = rng.permutation(rows.shape[0])
    k = int(round(share * rows.shape[0]))
    return rows[np.sort(idx[:k])], rows[np.sort(idx[k:])]
