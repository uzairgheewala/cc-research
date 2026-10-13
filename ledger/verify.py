"""Verify a claim ledger from its records alone (ledger/DESIGN.md section 3). Read-only; needs no data and no network.

  python ledger/verify.py LEDGER.json [--json]

Checks V1-V8; exit 1 if any fails. Prints what it cannot check (the report's `unverifiable` list must name it).
"""
import argparse, hashlib, json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import schema as S  # noqa: E402

MUST_DECLARE = ("statistics are recomputed only from the data", "supplier saw only what is recorded",
                "calibration outside its calibration set")


def canonical_hash(led):
    body = {k: led[k] for k in ("variables", "evidence", "knowledge", "claims", "overrides")}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def _type_ok(v, spec):
    t = spec.get("type")
    if "enum" in spec and v not in spec["enum"]:
        return False
    if "const" in spec and v != spec["const"]:
        return False
    if t is None:
        return True
    types = t if isinstance(t, list) else [t]
    py = {"string": str, "number": (int, float), "integer": int, "object": dict, "array": list, "boolean": bool, "null": type(None)}
    if not any(isinstance(v, py[x]) and not (x in ("number", "integer") and isinstance(v, bool)) for x in types):
        return False
    if isinstance(v, str) and "pattern" in spec:
        import re
        return re.match(spec["pattern"], v) is not None
    return True


def validate(v, spec, path, errs):
    if not _type_ok(v, spec):
        errs.append("%s: %r does not match %s" % (path, v if not isinstance(v, (dict, list)) else type(v).__name__,
                                                  {k: spec[k] for k in ("type", "enum", "const", "pattern") if k in spec}))
        return
    if isinstance(v, dict):
        for r in spec.get("required", ()):
            if r not in v:
                errs.append("%s: missing %s" % (path, r))
        for k, sub in spec.get("properties", {}).items():
            if k in v:
                validate(v[k], sub, "%s.%s" % (path, k), errs)
    if isinstance(v, list):
        if len(v) < spec.get("minItems", 0):
            errs.append("%s: needs at least %d item(s)" % (path, spec["minItems"]))
        for i, x in enumerate(v):
            validate(x, spec.get("items", {}), "%s[%d]" % (path, i), errs)


def skeleton(claims, field):
    return {frozenset((c["x"], c["y"])) for c in claims if c[field] != "none"}


def verify(led):
    res = {}
    errs = []
    validate(led, S.LEDGER, "ledger", errs)
    res["V1 schema"] = errs
    if errs:
        return res
    ev = {e["id"]: e for e in led["evidence"]}
    kn = {k["id"]: k for k in led["knowledge"]}
    claims, rep = led["claims"], led["report"]

    res["V2 evidence closure (I4)"] = ["claim %s cites unknown evidence %s" % (c["id"], e) for c in claims for e in c["evidence"] if e not in ev] + \
        ["claim %s cites unknown knowledge %s" % (c["id"], k) for c in claims for k in c.get("knowledge", []) if k not in kn]

    v3 = []
    final, data_only = skeleton(claims, "relation"), skeleton(claims, "data_only_relation")
    if final != data_only:
        added = sorted(tuple(sorted(p)) for p in final - data_only)
        removed = sorted(tuple(sorted(p)) for p in data_only - final)
        v3.append("final skeleton differs from the data-only skeleton: added %s, removed %s" % (added[:5], removed[:5]))
    v3 += ["claim %s takes its direction from knowledge on a pair the data left unconnected" % c["id"]
           for c in claims if c["direction_source"] == "knowledge" and c["data_only_relation"] == "none"]
    res["V3 knowledge never connects (I5)"] = v3

    v4 = []
    over = {(o["knowledge"], o["by"]) for o in led["overrides"]}
    for c in claims:
        ints = [ev[e] for e in c["evidence"] if e in ev and ev[e]["type"] == "intervention_shift" and ev[e]["supports"] in ("x->y", "y->x")]
        kns = [ev[e] for e in c["evidence"] if e in ev and ev[e]["type"] == "knowledge_statement" and ev[e]["supports"] in ("x->y", "y->x")]
        for i in ints:
            for k in kns:
                if i["supports"] != k["supports"]:
                    follows_int = (c["relation"] == "x->y") == (i["supports"] == "x->y")
                    if not follows_int:
                        v4.append("claim %s follows knowledge %s against intervention %s" % (c["id"], k["id"], i["id"]))
                    elif not any(by == i["id"] for _, by in over):
                        v4.append("claim %s: knowledge overridden by intervention %s without an override record" % (c["id"], i["id"]))
    res["V4 interventions outrank knowledge (I6)"] = v4

    used = {k for c in claims for k in c.get("knowledge", [])}
    overridden = {o["knowledge"] for o in led["overrides"]}
    res["V5 knowledge honoured"] = ["knowledge %s is neither used by a claim nor recorded as overridden" % k for k in kn
                                    if k not in used and k not in overridden]

    h = canonical_hash(led)
    res["V6 hash (I2)"] = [] if h == rep["ledger_sha256"] else ["ledger_sha256 %s.. but records hash to %s.." % (rep["ledger_sha256"][:12], h[:12])]

    pc = rep["permutation_check"]
    res["V7 order invariance (I1)"] = [] if pc["permutations"] >= 2 and pc["identical"] else \
        ["permutation check: %d permutation(s), identical=%s" % (pc["permutations"], pc["identical"])]

    v8 = []
    if "K" not in rep["regime"]:
        v8 += ["claim %s: regime %s admits no knowledge but relation %s differs from data-only %s" % (
            c["id"], rep["regime"], c["relation"], c["data_only_relation"]) for c in claims
            if c["relation"] != c["data_only_relation"] and c["direction_source"] != "intervention"]
        v8 += ["claim %s uses knowledge in regime %s" % (c["id"], rep["regime"]) for c in claims if c["direction_source"] == "knowledge"]
    res["V8 floor (I3)"] = v8

    missing = [m for m in MUST_DECLARE if not any(m.split()[0] in u for u in rep.get("unverifiable", []))]
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
            print("%-40s %s" % (k, "ok" if not v else "FAIL"))
            for x in v[:10]:
                print("    " + x)
        print("not checkable from the records: " + "; ".join(MUST_DECLARE))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
