"""Tier supplier (D3.1): ask for a causal tiering of shown variable names, validated by the supplier contract.

  schema(names)            -> schema function for supplier.contract.call: the reply must be exactly
                              {"tiers": [[name, ...], ...]} holding every shown name exactly once (surrounding
                              whitespace in a name is ignored; nothing else is repaired)
  replay_transport(rec)    -> a transport that returns the replies recorded in an AB-07 answer row, attempt by attempt
                              (finish_reason is not recorded there and is taken as "stop"; a reply-less attempt is empty)
  consensus(answers, names)-> {(a, b): (earlier, later)} for pairs every answering phrasing orders the same way (at least
                              two phrasings must have answered); per-phrasing tier positions are returned for the ledger
The prompts are AB-07's three phrasings (plans/a3_prereg.json, hashed there); B3 adds no prompt of its own.
"""
import json

from .contract import Reply


def schema(names):
    want = set(names)

    def fn(d):
        if not isinstance(d, dict) or set(d) != {"tiers"} or not isinstance(d["tiers"], list) or not d["tiers"]:
            return None, "the object must have exactly one key, tiers, holding a non-empty list"
        seen, tiers = [], []
        for t in d["tiers"]:
            if not isinstance(t, list) or not all(isinstance(x, str) for x in t):
                return None, "every tier must be a list of names"
            tiers.append([x.strip() for x in t if x.strip()])
            seen += tiers[-1]
        missing, extra = want - set(seen), set(seen) - want
        if missing or extra or len(seen) != len(set(seen)):
            return None, "missing %d, unknown %d, duplicated %s" % (len(missing), len(extra), len(seen) != len(set(seen)))
        return [t for t in tiers if t], None
    return fn


def replay_transport(row):
    """row: one line of plans/results/a3_tiers_answers.jsonl (attempts carry the raw replies)."""
    attempts = list(row.get("attempts") or [])
    state = {"k": 0}

    def transport(request, max_tokens, problem):
        k = state["k"]
        state["k"] += 1
        if k >= len(attempts):
            return Reply(text=None, status=0, error="no further recorded reply")
        a = attempts[k]
        return Reply(text=a.get("reply"), finish_reason=a.get("finish_reason") or "stop", status=a.get("status", 200) or 200,
                     model=a.get("served_model") or row.get("model_requested"))
    return transport


def positions(tiers):
    return {n: i for i, t in enumerate(tiers) for n in t}


def consensus(answers, names, min_answering=2):
    """answers: {phrasing_id: tiers or None}. -> (orders {(a, b): (earlier, later)}, info)."""
    pos = {p: positions(t) for p, t in answers.items() if t is not None}
    info = {"answering": sorted(pos), "abstained": sorted(p for p, t in answers.items() if t is None)}
    if len(pos) < min_answering:
        info["used"] = False
        return {}, info
    info["used"] = True
    out, disagree = {}, 0
    ns = sorted(names)
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            a, b = ns[i], ns[j]
            sides = set()
            for p in pos.values():
                sides.add("ab" if p[a] < p[b] else "ba" if p[b] < p[a] else "tie")
            if sides == {"ab"}:
                out[(a, b)] = (a, b)
            elif sides == {"ba"}:
                out[(a, b)] = (b, a)
            if {"ab", "ba"} <= sides:
                disagree += 1
    info["pairs_ordered"] = len(out)
    info["pairs_opposed"] = disagree
    return out, info


def load_answers(path):
    out = {}
    for ln in open(path, encoding="utf-8"):
        if ln.strip():
            r = json.loads(ln)
            out[(r["family"], r["scenario"], r["arm"], r["phrasing"])] = r
    return out
