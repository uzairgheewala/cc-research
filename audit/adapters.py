"""Audit adapters (D5.1): another system's output -> typed claims -> violations by class.

Input per run (AB-06 harness, harness/agent_probe.py): result.json with
  directed   [{"from_idx", "to_idx", "from", "to", "source"}]  final arrows over ORIGINAL column indices, with the
             source the agent itself exposes ("data", "llm", "llm_order"; absent = not exposed)
  undecided  [[a, b], ...]
  variants   the agent's own intermediate graphs; a data-only one when the agent has it:
             MATMCD "pc_only_initial" (its first PC run, no LLM), Vashishtha et al. "pc_only" (PC before the LLM order)
Rules (fixed in plans/b5_prereg.json; nothing is guessed):
  source      the agent's label mapped to the ledger's vocabulary: data -> data_pattern; llm, llm_order -> knowledge;
              anything else or absent -> unknown (counted, never guessed)
  data floor  the agent's data-only variant when it exposes one; otherwise the I5/I3 checks are 'not checkable' for that
              agent and say so
Violation classes (each row names the pair, the claim's relation and source, and the evidence the class rests on):
  knowledge_created_connection   final adjacency the agent's own data-only graph does not have          (I5)
  knowledge_deleted_connection   data-only adjacency missing from the final graph                       (I5)
  knowledge_reversed_data        data-only committed direction reversed in the final graph              (I3/G3)
  unsourced_direction            final arrow whose source the agent does not expose                     (G4)
  direction_follows_names        across the AB-06 name arms on the same data: an arrow present with real names and reversed
                                 or absent with swapped names, where the agent attributes the arrow to knowledge (G5)
Pass (gate B5.1): every flagged violation traced to a claim and a source; 0 'unknown' sources for agents that record
provenance (MATMCD, Vashishtha et al. label every arrow).
"""
import json
from pathlib import Path

SOURCE_MAP = {"data": "data_pattern", "llm": "knowledge", "llm_order": "knowledge"}
DATA_ONLY_VARIANT = {"matmcd": "pc_only_initial", "vashishtha": "pc_only"}
RECORDS_PROVENANCE = {"matmcd", "vashishtha", "causaliq", "pywhyllm"}


def _pairs(directed, undecided):
    D = {(int(e[0]), int(e[1])) for e in directed}
    U = {tuple(sorted((int(u[0]), int(u[1])))) for u in undecided}
    return D, U


def final_graph(res):
    D, src = set(), {}
    for e in res.get("directed") or []:
        a, b = int(e["from_idx"]), int(e["to_idx"])
        D.add((a, b))
        src[(a, b)] = SOURCE_MAP.get(e.get("source"), "unknown")
    U = set()
    for u in (res.get("undecided") or []):
        a, b = (u["a_idx"], u["b_idx"]) if isinstance(u, dict) else (u[0], u[1])
        U.add(tuple(sorted((int(a), int(b)))))
    return D, U, src


def data_only(agent, res):
    v = (res.get("variants") or {}).get(DATA_ONLY_VARIANT.get(agent, ""), None)
    if not isinstance(v, dict) or "directed" not in v:
        return None
    return _pairs(v.get("directed") or [], v.get("undecided") or [])


def audit_run(agent, res, names=None):
    """-> {"claims": [...], "violations": [...], "counts": {...}, "checkable": {...}}"""
    D, U, src = final_graph(res)
    do = data_only(agent, res)
    nm = (lambda i: names[i]) if names else (lambda i: str(i))
    claims, viol = [], []
    adj = {frozenset(e) for e in D} | {frozenset(u) for u in U}
    for (a, b) in sorted(D):
        claims.append({"x": nm(a), "y": nm(b), "relation": "x->y", "direction_source": src[(a, b)]})
    for (a, b) in sorted(U):
        claims.append({"x": nm(a), "y": nm(b), "relation": "x-y", "direction_source": "none"})
    if do is not None:
        Dd, Ud = do
        dadj = {frozenset(e) for e in Dd} | {frozenset(u) for u in Ud}
        for p in sorted(tuple(sorted(x)) for x in adj - dadj):
            a, b = p
            e = (a, b) if (a, b) in D else (b, a) if (b, a) in D else None
            viol.append({"class": "knowledge_created_connection", "pair": [nm(a), nm(b)],
                         "claim": ("%s->%s" % (nm(e[0]), nm(e[1]))) if e else "%s-%s" % (nm(a), nm(b)),
                         "source": src.get(e, "none") if e else "none", "evidence": "absent from the agent's data-only graph (%s)" % DATA_ONLY_VARIANT[agent]})
        for p in sorted(tuple(sorted(x)) for x in dadj - adj):
            viol.append({"class": "knowledge_deleted_connection", "pair": [nm(p[0]), nm(p[1])], "claim": "none",
                         "source": "knowledge" if agent in RECORDS_PROVENANCE else "unknown",
                         "evidence": "present in the agent's data-only graph (%s), absent from its final graph" % DATA_ONLY_VARIANT[agent]})
        for (a, b) in sorted(Dd):
            if (b, a) in D:
                viol.append({"class": "knowledge_reversed_data", "pair": [nm(a), nm(b)], "claim": "%s->%s" % (nm(b), nm(a)),
                             "source": src[(b, a)], "evidence": "data-only graph commits %s->%s" % (nm(a), nm(b))})
    for (a, b) in sorted(D):
        if src[(a, b)] == "unknown":
            viol.append({"class": "unsourced_direction", "pair": [nm(a), nm(b)], "claim": "%s->%s" % (nm(a), nm(b)),
                         "source": "unknown", "evidence": "the agent exposes no source for this arrow"})
    counts = {}
    for v in viol:
        counts[v["class"]] = counts.get(v["class"], 0) + 1
    return {"claims": claims, "violations": viol, "counts": counts,
            "checkable": {"I5_I3": do is not None, "provenance": any(s != "unknown" for s in src.values()) or not src},
            "unknown_sources": sum(1 for s in src.values() if s == "unknown"), "arrows": len(D), "open_pairs": len(U)}


def names_flip(agent, real, swapped):
    """Arrows attributed to knowledge in the real arm that are reversed or absent in the swapped arm (same data, same
    column permutation; only the names differ)."""
    Dr, _, sr = final_graph(real)
    Ds, Us, _ = final_graph(swapped)
    out = []
    for (a, b) in sorted(Dr):
        if sr[(a, b)] != "knowledge":
            continue
        if (b, a) in Ds or ((a, b) not in Ds and tuple(sorted((a, b))) not in Us):
            out.append({"class": "direction_follows_names", "pair": [a, b], "claim": "%d->%d (real arm)" % (a, b), "source": "knowledge",
                        "evidence": "swapped arm: %s" % ("reversed" if (b, a) in Ds else "absent")})
    return out


# ---------------------------------------------------------------- Causal-Copilot (stage graphs, provenance reconstructed)
def _sets_by_name(stage):
    D = {(a, b) for a, b in stage["directed"]}
    U = {tuple(sorted((u[0], u[1]))) for u in stage["undirected"]}
    return D, U


def audit_cc_run(row, floor="S1"):
    """Causal-Copilot does not record provenance; the stages S0-S3 (audit/export_cc_stages.py) let us reconstruct it.
    Final = S3 (the graph after refinement, before the cycle step); data floor = S1 (the algorithm's graph after the
    bootstrap filter, no names read yet) or S0. An S3 arrow already in the floor is 'data_pattern (reconstructed)'; an
    arrow the LLM step set or reversed is 'knowledge (reconstructed)'."""
    st = row["stages"]
    Df, Uf = _sets_by_name(st["S3"])
    Dd, Ud = _sets_by_name(st[floor])
    D2, _ = _sets_by_name(st["S2"])
    D1, U1 = _sets_by_name(st["S1"])
    src = {}
    for e in Df:
        src[e] = "data_pattern" if e in D1 else "knowledge"
    adj = {frozenset(e) for e in Df} | {frozenset(u) for u in Uf}
    dadj = {frozenset(e) for e in Dd} | {frozenset(u) for u in Ud}
    viol = []
    for p in sorted(tuple(sorted(x)) for x in adj - dadj):
        e = p if p in Df else (p[1], p[0]) if (p[1], p[0]) in Df else None
        viol.append({"class": "knowledge_created_connection", "pair": list(p), "claim": "%s->%s" % e if e else "%s-%s" % p,
                     "source": src.get(e, "knowledge") + " (reconstructed)", "evidence": "absent from %s" % floor})
    for p in sorted(tuple(sorted(x)) for x in dadj - adj):
        viol.append({"class": "knowledge_deleted_connection", "pair": list(p), "claim": "none",
                     "source": "reconstructed: removed at %s" % ("S1->S2 (LLM)" if frozenset(p) in ({frozenset(e) for e in D1} | {frozenset(u) for u in U1})
                                                                 and frozenset(p) not in {frozenset(e) for e in D2} else "S2->S3 (KCI) or earlier"),
                     "evidence": "present in %s, absent from S3" % floor})
    for (a, b) in sorted(Dd):
        if (b, a) in Df:
            viol.append({"class": "knowledge_reversed_data", "pair": [a, b], "claim": "%s->%s" % (b, a), "source": src[(b, a)] + " (reconstructed)",
                         "evidence": "%s commits %s->%s" % (floor, a, b)})
    counts = {}
    for v in viol:
        counts[v["class"]] = counts.get(v["class"], 0) + 1
    return {"violations": viol, "counts": counts, "arrows": len(Df), "sources": {s: sum(1 for x in src.values() if x == s) for s in set(src.values())},
            "unknown_sources": 0, "provenance": "reconstructed from stage graphs (Causal-Copilot records none)"}
