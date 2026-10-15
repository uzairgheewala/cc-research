"""Declared knowledge as tiers, orient-only (bundle B3; D3.2; guarantees G3, G5; invariants I3, I5).

  led_k, info = apply_tiers(led_d, statements, outcomes)

statements  {phrasing_id: {"tiers": [[name, ...], ...] or None, "supplier": {...}}}: one tiering per phrasing, None
            when the supplier contract ended in 'abstained' or 'stopped' for that phrasing
outcomes    supplier.contract.Counts.as_dict() for the table (written to the report)

Rules (fixed in plans/b3_prereg.json before any held-out read):
  1. consensus: a pair is ordered only when every answering phrasing puts one variable in a strictly earlier tier than
     the other, the same way, and at least two phrasings answered (supplier.tiers.consensus). Otherwise no knowledge
     enters for that pair; with fewer than two answering phrasings none enters for the table.
  2. orient-only: only pairs the data-only ledger left open ('x-y') are oriented; a connection is never added or removed
     and a data direction is never reversed (I5; the evidence priority data > knowledge of approach v1 section 2).
  3. no propagation: an orientation from knowledge is not fed back into Meek's rules, so the number of pairs knowledge
     decides, k, is exactly the number of 'tier' claims (theory pack T3 needs k to include propagated orientations;
     there are none).
  4. no cycle: a tier orientation that would close a directed cycle with the claims already directed is skipped and
     recorded (skipped_cycle).
T3 bound (analysis/reports/ab09_theory_pack.md): with expected-credit directed F1 (open pairs earn 1/2), knowledge that
orients k open pairs changes F1 by at least -k / (nP + nT) where nP is the number of claimed adjacencies and nT the
number of true edges; without the truth, -k / nP is a valid (weaker) bound. Both are written into the report.
"""
import copy, hashlib, json

from .ledger_hash import canonical_hash


def _sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def _has_path(adj_out, src, dst):
    stack, seen = [src], {src}
    while stack:
        u = stack.pop()
        for v in adj_out.get(u, ()):
            if v == dst:
                return True
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return False


def apply_tiers(led_d, statements, outcomes=None, min_answering=2):
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from supplier.tiers import consensus
    names = [v["name"] for v in led_d["variables"]]
    answers = {p: (s.get("tiers") if s else None) for p, s in statements.items()}
    orders, cinfo = consensus(answers, names, min_answering=min_answering)
    led = copy.deepcopy(led_d)
    rep = led["report"]
    rep["regime"] = "D+K" if rep["regime"] == "D" else (rep["regime"] + "+K" if "K" not in rep["regime"] else rep["regime"])
    knowledge, kid = [], {}
    for p in sorted(statements):
        s = statements[p]
        if s is None or s.get("tiers") is None:
            continue
        rec = {"id": "k:%s:%s" % (p, _sha(json.dumps(s["tiers"], sort_keys=True))[:12]), "kind": "tier",
               "content": {"tiers": s["tiers"], "phrasing": p}, "supplier": s.get("supplier") or {"type": "model"}}
        knowledge.append(rec)
        kid[p] = rec["id"]
    led["knowledge"] = knowledge
    adj_out = {}
    for c in led["claims"]:
        if c["relation"] == "x->y":
            adj_out.setdefault(c["x"], set()).add(c["y"])
    decided, skipped = [], []
    ev_new = []
    for c in sorted(led["claims"], key=lambda c: c["id"]):
        if c["relation"] != "x-y":
            continue
        key = tuple(sorted((c["x"], c["y"])))
        if key not in orders:
            continue
        cause, effect = orders[key]
        if _has_path(adj_out, effect, cause):
            skipped.append({"pair": [cause, effect], "reason": "would close a directed cycle"})
            continue
        eid = "k-ev:%s|%s" % (cause, effect)
        ev_new.append({"id": eid, "type": "knowledge_statement", "variables": [cause, effect], "conditioning": [],
                       "supports": "x->y", "rule": "consensus of %d answering phrasing(s): %s earlier tier than %s" % (len(cinfo["answering"]), cause, effect),
                       "knowledge": [kid[p] for p in cinfo["answering"] if p in kid]})
        c.update({"x": cause, "y": effect, "relation": "x->y", "direction_source": "knowledge", "licensed_by": "tier",
                  "evidence": sorted(set(c["evidence"]) | {eid}), "knowledge": [kid[p] for p in cinfo["answering"] if p in kid],
                  "engines": c["engines"]})
        adj_out.setdefault(cause, set()).add(effect)
        decided.append([cause, effect])
    # knowledge against an intervention (I6): the claim keeps the intervention's direction; the statement is recorded
    # on the claim and overridden by the intervention record
    overridden_by_int = []
    for c in led["claims"]:
        if c["relation"] != "x->y" or c["direction_source"] != "intervention":
            continue
        key = tuple(sorted((c["x"], c["y"])))
        if key in orders and orders[key] != (c["x"], c["y"]):
            cause, effect = orders[key]
            eid = "k-ev:%s|%s" % (cause, effect)
            ev_new.append({"id": eid, "type": "knowledge_statement", "variables": [c["x"], c["y"]], "conditioning": [],
                           "supports": "y->x", "rule": "consensus says %s before %s" % (cause, effect),
                           "knowledge": [kid[p] for p in cinfo["answering"] if p in kid]})
            by = next((e for e in c["evidence"] if e.startswith("i:")), None)
            c["evidence"] = sorted(set(c["evidence"]) | {eid})
            for kk in [kid[p] for p in cinfo["answering"] if p in kid]:
                overridden_by_int.append({"knowledge": kk, "by": by, "reason": "an intervention record orders %s -> %s" % (c["x"], c["y"])})
    led["evidence"] = led["evidence"] + ev_new
    used = {k for c in led["claims"] for k in c.get("knowledge", [])}
    led["overrides"] = overridden_by_int + [{"knowledge": k["id"], "by": "data", "reason": "orders no pair the data left open (or only pairs a cycle check skipped)"}
                                            for k in knowledge if k["id"] not in used and k["id"] not in {o["knowledge"] for o in overridden_by_int}]
    nP = sum(1 for c in led["claims"] if c["relation"] != "none")
    rep["knowledge_application"] = {"rule": "tiers, consensus of answering phrasings (>= %d), orient-only, no propagation" % min_answering,
                                    "consensus": cinfo, "decided": len(decided), "decided_pairs": decided, "skipped_cycle": skipped,
                                    "t3_bound_truth_free": (len(decided) / nP) if nP else 0.0, "claimed_adjacencies": nP,
                                    "supplier_counts": outcomes}
    rep["unverifiable"] = [u if not u.startswith("supplier") else "supplier saw only what is recorded (prompts are AB-07's, hashed in plans/a3_prereg.json)"
                           for u in rep["unverifiable"]]
    rep["ledger_sha256"] = canonical_hash(led)
    return led, {"orders": orders, "consensus": cinfo, "decided": decided, "skipped": skipped}
