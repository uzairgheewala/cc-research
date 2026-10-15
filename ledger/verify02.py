"""Verify a v0.2 claim ledger from its records alone (BLD-14, D1.4). Read-only; no data, no network, NumPy not needed.

  python ledger/verify02.py LEDGER.json [--json]

V1-V8 are v0.1's checks (ledger/verify.py, unchanged and still used for v0.1 ledgers) restated for v0.2; unlike v0.1,
every check runs even when V1 fails (AB-11 finding), each inside its own guard, and a check that cannot run says why.
New in v0.2:
  V9  plan, deviations, assumptions, lineage and question are present and well-formed (AB-13's five gaps)
  V10 exactly one claim per unordered pair of variables, and every claim names two declared variables
  V11 the orientation convention is declared (AB-11)
  V12 a required-edge knowledge statement on a pair the data left unconnected is recorded as an override (AB-11)
  V13 a directed claim's evidence includes at least one record on the claim's own pair, or the claim names the claims
      its orientation rule relied on (derived_from)
Convention (v0.2): an evidence record's 'supports' value ("x->y", "y->x") is relative to that record's own variables
list; V4 compares arrows, not strings (v0.1 compared the strings, which is ambiguous once a claim is re-oriented).
"""
import argparse, json, sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import schema02 as S  # noqa: E402
import verify as V01  # noqa: E402

MUST_DECLARE = V01.MUST_DECLARE
canonical_hash = V01.canonical_hash


def _skeleton(claims, field):
    return {frozenset((c["x"], c["y"])) for c in claims if c[field] != "none"}


def _v1(led):
    errs = []
    V01.validate(led, S.LEDGER, "ledger", errs)
    return errs


def _v2(led):
    ev = {e["id"] for e in led["evidence"]}
    kn = {k["id"] for k in led["knowledge"]}
    out = []
    for c in led["claims"]:
        if not c.get("evidence"):
            out.append("claim %s cites no evidence" % c["id"])
        out += ["claim %s cites unknown evidence %s" % (c["id"], e) for e in c.get("evidence", []) if e not in ev]
        out += ["claim %s cites unknown knowledge %s" % (c["id"], k) for k in c.get("knowledge", []) if k not in kn]
    return out


def _v3(led):
    claims = led["claims"]
    out = []
    final, data_only = _skeleton(claims, "relation"), _skeleton(claims, "data_only_relation")
    if final != data_only:
        out.append("final skeleton differs from the data-only skeleton: added %s, removed %s" % (
            sorted(tuple(sorted(p)) for p in final - data_only)[:5], sorted(tuple(sorted(p)) for p in data_only - final)[:5]))
    out += ["claim %s takes its direction from knowledge on a pair the data left unconnected" % c["id"]
            for c in claims if c["direction_source"] == "knowledge" and c["data_only_relation"] == "none"]
    return out


def _dir(e):
    """The arrow an evidence record supports, from its own variables list (v0.2: 'supports' is relative to the record's
    variables[0], variables[1], never to the claim that cites it)."""
    a, b = e["variables"][0], e["variables"][1]
    return (a, b) if e["supports"] == "x->y" else (b, a) if e["supports"] == "y->x" else None


def _v4(led):
    ev = {e["id"]: e for e in led["evidence"]}
    over = {o["by"] for o in led["overrides"]}
    out = []
    for c in led["claims"]:
        recs = [ev[e] for e in c["evidence"] if e in ev]
        ints = [e for e in recs if e["type"] == "intervention_shift" and _dir(e)]
        kns = [e for e in recs if e["type"] == "knowledge_statement" and _dir(e)]
        claimed = (c["x"], c["y"]) if c["relation"] == "x->y" else None
        for i in ints:
            for k in kns:
                if _dir(i) != _dir(k):
                    if claimed != _dir(i):
                        out.append("claim %s follows knowledge %s against intervention %s" % (c["id"], k["id"], i["id"]))
                    elif i["id"] not in over:
                        out.append("claim %s: knowledge overridden by intervention %s without an override record" % (c["id"], i["id"]))
    return out


def _v5(led):
    used = {k for c in led["claims"] for k in c.get("knowledge", [])}
    overridden = {o["knowledge"] for o in led["overrides"]}
    return ["knowledge %s is neither used by a claim nor recorded as overridden" % k["id"] for k in led["knowledge"]
            if k["id"] not in used and k["id"] not in overridden]


def _v6(led):
    h = canonical_hash(led)
    want = led["report"]["ledger_sha256"]
    return [] if h == want else ["ledger_sha256 %s.. but records hash to %s.." % (want[:12], h[:12])]


def _v7(led):
    pc = led["report"]["permutation_check"]
    return [] if pc["permutations"] >= 2 and pc["identical"] else ["permutation check: %d permutation(s), identical=%s" % (pc["permutations"], pc["identical"])]


def _v8(led):
    rep = led["report"]
    if "K" in rep["regime"]:
        return []
    out = ["claim %s: regime %s admits no knowledge but relation %s differs from data-only %s" % (c["id"], rep["regime"], c["relation"], c["data_only_relation"])
           for c in led["claims"] if c["relation"] != c["data_only_relation"] and c["direction_source"] != "intervention"]
    out += ["claim %s uses knowledge in regime %s" % (c["id"], rep["regime"]) for c in led["claims"] if c["direction_source"] == "knowledge"]
    return out


def _v9(led):
    rep = led["report"]
    out = []
    for k in ("plan", "deviations", "assumptions", "lineage", "question"):
        if k not in rep:
            out.append("report.%s missing" % k)
    if not rep.get("assumptions"):
        out.append("report.assumptions is empty: identifying assumptions must be stated")
    for a in rep.get("assumptions", []):
        if not a.get("sensitivity"):
            out.append("assumption %s states no sensitivity" % a.get("id"))
    plan = rep.get("plan") or {}
    if not plan.get("prereg_sha256"):
        out.append("report.plan has no prereg_sha256: the plan must be fixed before the data")
    return out


def _v10(led):
    names = [v["name"] for v in led["variables"]]
    out = []
    if len(set(names)) != len(names):
        out.append("variable names are not unique")
    known = set(names)
    seen = {}
    for c in led["claims"]:
        if c["x"] not in known or c["y"] not in known or c["x"] == c["y"]:
            out.append("claim %s names an unknown or repeated variable (%s, %s)" % (c["id"], c["x"], c["y"]))
            continue
        key = frozenset((c["x"], c["y"]))
        if key in seen:
            out.append("pair %s has two claims (%s, %s)" % (sorted(key), seen[key], c["id"]))
        seen[key] = c["id"]
    missing = [p for p in combinations(sorted(known), 2) if frozenset(p) not in seen]
    if missing:
        out.append("%d unordered pair(s) have no claim, e.g. %s" % (len(missing), missing[:3]))
    return out


def _v11(led):
    return [] if led["report"].get("orientation_convention") == S.CONVENTION else ["orientation convention not declared"]


def _v12(led):
    data_none = {frozenset((c["x"], c["y"])) for c in led["claims"] if c["data_only_relation"] == "none"}
    overridden = {o["knowledge"] for o in led["overrides"]}
    out = []
    for k in led["knowledge"]:
        if k["kind"] == "required_edge":
            pair = frozenset((k["content"].get("from"), k["content"].get("to")))
            if pair in data_none and k["id"] not in overridden:
                out.append("required edge %s on a pair the data left unconnected is not recorded as an override" % k["id"])
    return out


def _v13(led):
    ev = {e["id"]: e for e in led["evidence"]}
    out = []
    for c in led["claims"]:
        if c["relation"] != "x->y":
            continue
        own = any(set(ev[e]["variables"][:2]) == {c["x"], c["y"]} for e in c["evidence"] if e in ev)
        if not own and not c.get("derived_from"):
            out.append("directed claim %s cites no record on its own pair and names no premises" % c["id"])
    return out


CHECKS = [("V1 schema", _v1), ("V2 evidence closure (I4)", _v2), ("V3 knowledge never connects (I5)", _v3),
          ("V4 interventions outrank knowledge (I6)", _v4), ("V5 knowledge honoured", _v5), ("V6 hash (I2)", _v6),
          ("V7 order invariance (I1)", _v7), ("V8 floor (I3)", _v8), ("V9 plan, assumptions, lineage, question", _v9),
          ("V10 one claim per pair", _v10), ("V11 orientation convention", _v11), ("V12 required edges on unconnected pairs", _v12),
          ("V13 directed claims cite their pair or premises", _v13)]


def verify(led):
    res = {}
    for name, fn in CHECKS:
        try:
            res[name] = fn(led)
        except Exception as e:  # noqa: BLE001 - a check that cannot run is reported, never skipped silently
            res[name] = ["could not run: %s: %s" % (type(e).__name__, e)]
    missing = [m for m in MUST_DECLARE if not any(m.split()[0] in u for u in led.get("report", {}).get("unverifiable", []))]
    res["declared limits"] = ["report.unverifiable does not mention: %s" % m for m in missing]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ledger")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = verify(json.load(open(a.ledger, encoding="utf-8")))
    bad = sum(len(v) for v in res.values())
    if a.json:
        print(json.dumps({"ok": bad == 0, "checks": res}, indent=1))
    else:
        for k, v in res.items():
            print("%-48s %s" % (k, "ok" if not v else "FAIL"))
            for x in v[:10]:
                print("    " + x)
        print("not checkable from the records: " + "; ".join(MUST_DECLARE))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
