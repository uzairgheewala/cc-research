"""K7: re-derive every claim of a data-only ledger from its records alone (D1.6). NumPy only; no engine, no data.

  python -m kernel.checker LEDGER.json [--json]

1. PC: the ci_test records (with their phases) re-derive the skeleton, the maxP colliders and the Meek closure
   (kernel.derive); the result must equal report.engine_outputs.pc, except for pairs the report lists as left open
   because of the engine's directed-cycle defect.
2. The combination rule named in the report is re-applied to the re-derived PC graph and GES's recorded graph
   (kernel.policy); every claim's relation and licence must match.
3. Each claim's data_only_relation must equal its relation (regime D).
A ledger with one evidence record removed fails here or in verify02 (B1.3's mutation test).
"""
import argparse, json, sys

from . import derive, policy


def _sets(names_idx, pairs, directed):
    out = set()
    for a, b in pairs:
        i, j = names_idx[a], names_idx[b]
        out.add((i, j) if directed else tuple(sorted((i, j))))
    return out


def check(led):
    errs = []
    rep = led["report"]
    eo = rep["engine_outputs"]
    n = len(led["variables"])
    idx = {v["name"]: v["canonical_index"] for v in led["variables"]}
    alpha = rep.get("alpha", 0.05)
    tests = []
    for e in led["evidence"]:
        if e["type"] != "ci_test":
            continue
        i, j = idx[e["variables"][0]], idx[e["variables"][1]]
        S = tuple(sorted(idx[s] for s in e["conditioning"]))
        for ph in e.get("phases", ["skeleton"]):
            tests.append((ph, min(i, j), max(i, j), S, e["p_value"]))
    der = derive.pc_maxp_from_tests(n, tests, alpha)
    if der["missing_tests"]:
        errs.append("maxP needs %d test(s) the ledger does not record, e.g. %s" % (len(der["missing_tests"]), der["missing_tests"][:2]))
    from engines.core import marks_to_sets
    Dd0, Ud0 = marks_to_sets(der["final"])
    De = _sets(idx, eo["pc"]["directed"], True)
    Ue = _sets(idx, eo["pc"]["undirected"], False)
    declared_div = set()
    for d in eo["pc"].get("defects", []):
        if d["type"] == "engine_meek_divergence":
            declared_div |= {tuple(sorted((idx[a], idx[b]))) for a, b in d["pairs"]}
    diff = {tuple(sorted(e)) for e in (De ^ Dd0)} | {tuple(sorted(u)) for u in (Ue ^ Ud0)}
    if diff != declared_div:
        errs.append("PC re-derived from the tests differs from the recorded engine output on %d pair(s) not declared as divergence "
                    "(declared %d)" % (len(diff - declared_div), len(declared_div)))
    Dd, Ud, opened = policy.open_cycles(Dd0, Ud0)
    if "kernel_directed" in eo["pc"]:
        Dk = _sets(idx, eo["pc"]["kernel_directed"], True)
        Uk = _sets(idx, eo["pc"]["kernel_undirected"], False)
        if (Dk, Uk) != (Dd, Ud):
            errs.append("the kernel's PC graph (cycles opened) differs from the re-derivation")
    vlab = {}
    for c in der["colliders"]:
        if c["applied"]:
            vlab[(c["x"], c["y"])] = vlab[(c["z"], c["y"])] = ("v_structure", [])
    pc_labels = {}
    for e in Dd:
        if e in vlab and der["after_maxp"][e[0], e[1]] == -1 and der["after_maxp"][e[1], e[0]] == 1:
            pc_labels[e] = vlab[e]
        elif e in der["meek_labels"]:
            pc_labels[e] = (der["meek_labels"][e], [])
        else:
            pc_labels[e] = ("none", [])
    pc = {"D": Dd, "U": Ud, "labels": pc_labels}
    ges = None
    if eo.get("ges") and eo["ges"].get("ok"):
        Dg = _sets(idx, eo["ges"]["directed"], True)
        Ug = _sets(idx, eo["ges"]["undirected"], False)
        ges = {"D": Dg, "U": Ug, "labels": policy.label_cpdag(n, Dg, Ug)}
    dec, fallback = policy.decide(rep["rule"], n, pc, ges)
    dec, _ = policy.guard(dec, n)
    if fallback != eo.get("policy_fallback", False):
        errs.append("policy fallback recorded %s, re-derived %s" % (eo.get("policy_fallback"), fallback))
    claims = {frozenset((idx[c["x"]], idx[c["y"]])): c for c in led["claims"]}
    with_k = "K" in rep["regime"]
    korders = {}
    if with_k:
        import sys as _sys
        from pathlib import Path as _P
        _sys.path.insert(0, str(_P(__file__).resolve().parent.parent))
        from supplier.tiers import consensus
        ka = rep.get("knowledge_application", {})
        answers = {k["content"]["phrasing"]: k["content"]["tiers"] for k in led["knowledge"] if k["kind"] == "tier"}
        answers.update({p: None for p in ka.get("consensus", {}).get("abstained", [])})
        korders, _ = consensus(answers, list(idx), min_answering=2)
    for (a, b), d in dec.items():
        c = claims.get(frozenset((a, b)))
        if c is None:
            errs.append("no claim for pair %s" % [a, b])
            continue
        if d.relation in ("a->b", "b->a"):
            cause, eff = (a, b) if d.relation == "a->b" else (b, a)
            want = ("x->y", cause, eff)
            have = (c["relation"], idx[c["x"]], idx[c["y"]])
        else:
            want = ({"a-b": "x-y", "none": "none"}[d.relation],)
            have = (c["relation"],)
        if c["direction_source"] == "intervention" and "I" in rep["regime"]:
            evmap = {e["id"]: e for e in led["evidence"]}
            if c["relation"] == "x-y":
                if not c.get("conflict"):
                    errs.append("claim %s: an intervention-opened pair without a recorded conflict" % c["id"])
            elif c["licensed_by"] == "i_essential":
                if not any(evmap[e]["type"] == "intervention_shift" and evmap[e]["supports"] == "x->y"
                           and evmap[e]["variables"][:2] == [c["x"], c["y"]] for e in c["evidence"] if e in evmap):
                    errs.append("claim %s: i_essential without a shift record %s -> %s" % (c["id"], c["x"], c["y"]))
            elif not c.get("derived_from"):
                errs.append("claim %s: propagated intervention orientation names no premises" % c["id"])
            if d.relation == "none":
                errs.append("claim %s: an intervention claim on a pair the data left unconnected" % c["id"])
            continue
        if with_k and c["direction_source"] == "knowledge":
            names = {v: k for k, v in idx.items()}
            key = tuple(sorted((names[a], names[b])))
            if d.relation != "a-b":
                errs.append("claim %s: knowledge oriented a pair the data did not leave open (%s)" % (c["id"], d.relation))
            elif korders.get(key) != (c["x"], c["y"]):
                errs.append("claim %s: knowledge orientation %s is not the consensus %s" % (c["id"], (c["x"], c["y"]), korders.get(key)))
            continue
        if want != have:
            errs.append("claim %s: recorded %s, re-derived %s" % (c["id"], have, want))
        if c["licensed_by"] != d.licensed_by:
            errs.append("claim %s: licence %s, re-derived %s" % (c["id"], c["licensed_by"], d.licensed_by))
        if c["data_only_relation"] != c["relation"]:
            errs.append("claim %s: data-only relation differs from the relation without a knowledge source (%s)" % (c["id"], rep["regime"]))
    return {"ok": not errs, "errors": errs, "claims_rederived": len(dec), "tests_used": len(tests)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ledger")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = check(json.load(open(a.ledger, encoding="utf-8")))
    print(json.dumps(res, indent=1) if a.json else ("K7 re-derivation: %s (%d claims)" % ("ok" if res["ok"] else "FAIL", res["claims_rederived"])))
    for e in res["errors"][:20]:
        print("   ", e)
    sys.exit(0 if res["ok"] else 1)


if __name__ == "__main__":
    main()
