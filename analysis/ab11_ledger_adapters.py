"""AB-11 (AUD-42, CAP-09): map each tool's raw discovery output to a claim ledger (ledger/DESIGN.md), as faithfully as the
tool allows and never more. Used by analysis/ab11_teardown_run.py; tested by tests/test_ab11_adapters.py.

Input: one run of a tool, normalised by the runner to ORIGINAL column indices:
  output = {"directed": [[a, b]], "undirected": [[a, b]], "other": [[a, b, mark]],
            "sepsets":   [[a, b, [cond], p or None, field]],     separating sets the tool exposes (non-adjacent pairs)
            "adj_tests": [[a, b, p, statistic, field]],          per-pair test results the tool exposes
            "edge_meta": [[a, b, {..}]],                        per-edge attributes (weight, origin, ...)
            "rule_records": [[a, b, c, rule, field]]}           an orientation rule the tool itself reports for a->b
                                                                (only Tetrad's verbose 'Collider oriented: a -> b <- c')
Rules (no evidence is ever invented):
  * An evidence record exists only for an item the tool exposed in `sepsets` or `adj_tests`, one record per item, type
    "ci_test", with `source_field` naming the tool's field. Weights, orders and origins are not evidence; they are copied
    onto the claim as `tool_edge_meta`.
  * Every unordered pair gets one claim. `evidence` lists the records on that pair (possibly none: then V1 fails, which is
    the finding). `licensed_by` is "adjacency_test" when a CI record exists for the pair, else "none".
  * `direction_source` is "none" unless the tool itself states why the arrow is there. Two cases do:
    - a rule record (Tetrad verbose 'Collider oriented: a -> b <- c') for an arrow that is still a->b in the output, AND an
      exposed CI record that separates a and c without b: source "data_pattern", licensed by "v_structure", citing that
      record. Without such a record the claim stays "none" (nothing to cite).
    - an edge the tool's output labels as knowledge-made (CausalNex `origin == "expert"`): source "knowledge", licensed by
      "declared", citing the knowledge statement it came from.
  * A claim cites a knowledge statement only when the tool's output says it used it (the CausalNex case). Otherwise the
    statement is listed but uncited and no override is written, because no tool reports either; V5 then fails.
  * Marks without a ledger equivalent are kept verbatim in `tool_mark`: an orientation conflict (Tigramite 'x-x', causal-learn
    G[i,j] = G[j,i] = 1) or a circle endpoint becomes relation "x-y" (connected, direction open), never "x<->y" (which the
    ledger reserves for latent confounding in a PAG).
  * Schema gap: RELATIONS has no "y->x", so when the data-only run had the opposite arrow the claim records
    data_only_relation "x-y" (lossy) plus `data_only_relation_exact` "y->x".
"""
import copy, datetime, hashlib, json, subprocess, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
KIT = HERE.parent
sys.path.insert(0, str(KIT / "ledger"))
import schema as S  # noqa: E402
import verify as V  # noqa: E402

FORMAT = "cc-claim-ledger/0.1"
UNVERIFIABLE = ["statistics are recomputed only from the data: not done here (adapter copies what the tool exposed)",
                "supplier saw only what is recorded: the knowledge was chosen by the teardown author from the true graph and the tool's data-only output",
                "calibration outside its calibration set: no tool gives a calibrated confidence",
                "this ledger was written by analysis/ab11_ledger_adapters.py from the tool's output; the tool writes no ledger"]
EVIDENCE_TYPES_ALLOWED = ("ci_test", "score_delta")


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def data_sha(X):
    return _sha(np.ascontiguousarray(np.asarray(X, dtype="<f8")).tobytes())


def var_id(col, name):
    return _sha(np.ascontiguousarray(np.asarray(col, dtype="<f8")).tobytes() + name.encode("utf-8"))


def _rel(o, a, b):
    """Relation of the ordered pair (a, b) in output o: 'x->y', 'y->x', 'x-y', 'none', plus the tool's mark."""
    if [a, b] in o["directed"]:
        return "x->y", "-->"
    if [b, a] in o["directed"]:
        return "y->x", "<--"
    if sorted([a, b]) in o["undirected"]:
        return "x-y", "---"
    for x in o.get("other", []):
        if sorted([a, b]) == sorted(x[:2]):
            return "x-y", str(x[2])
    return "none", ""


def evidence_records(output, names, engine, data_sha256):
    """One ci_test record per exposed item; returns (records, {frozenset(pair): [ids]}). Never adds anything else."""
    recs, by_pair = [], {}
    for k, (a, b, cond, p, field) in enumerate(output.get("sepsets", [])):
        r = {"id": "ev:sepset:%d" % k, "type": "ci_test", "variables": [names[a], names[b]], "conditioning": [names[c] for c in cond],
             "supports": "nonadjacent", "data_sha256": data_sha256, "engine": engine, "seed": None, "source_field": field}
        if p is not None:
            r["p_value"] = float(p)
        recs.append(r)
        by_pair.setdefault(frozenset((a, b)), []).append(r["id"])
    for k, (a, b, p, stat, field) in enumerate(output.get("adj_tests", [])):
        r = {"id": "ev:adjtest:%d" % k, "type": "ci_test", "variables": [names[a], names[b]], "supports": "adjacent",
             "data_sha256": data_sha256, "engine": engine, "seed": None, "source_field": field,
             "note": "conditioning set of this test is not exposed"}
        if p is not None:
            r["p_value"] = float(p)
        if stat is not None:
            r["statistic"] = float(stat)
        recs.append(r)
        by_pair.setdefault(frozenset((a, b)), []).append(r["id"])
    return recs, by_pair


def knowledge_records(K):
    out = []
    if not K:
        return out
    sup = {"type": "person", "shown": ["true graph of the public file (test fixture)", "the tool's data-only output"]}
    for a, b in K.get("required", []):
        out.append({"id": "k%d" % (len(out) + 1), "kind": "required_edge", "content": {"from": a, "to": b}, "supplier": sup})
    for a, b in K.get("forbidden", []):
        out.append({"id": "k%d" % (len(out) + 1), "kind": "forbidden_edge", "content": {"from": a, "to": b}, "supplier": sup})
    if K.get("tiers"):
        out.append({"id": "k%d" % (len(out) + 1), "kind": "tier", "content": {"tiers": K["tiers"]}, "supplier": sup})
    return out


def build_ledger(tool, run, data_only_output, X, names, regime, engine, permutations, identical, run_id):
    o = run["output"]
    d = len(names)
    dsha = data_sha(X)
    evid, by_pair = evidence_records(o, names, engine, dsha)
    know = knowledge_records(run.get("knowledge_by_name"))
    req_k = {(k["content"]["from"], k["content"]["to"]): k["id"] for k in know if k["kind"] == "required_edge"}
    meta = {(a, b): m for a, b, m in o.get("edge_meta", [])}
    perm = run.get("perm") or list(range(d))
    pos = {orig: shown for shown, orig in enumerate(perm)}
    sep_ids = {}
    for e, (a, b, cond, _, _) in zip([r for r in evid if r["id"].startswith("ev:sepset")], o.get("sepsets", [])):
        sep_ids.setdefault(frozenset((a, b)), []).append((e["id"], set(cond)))
    rules = {}
    for a, b, c, rule, field in o.get("rule_records", []):
        ok = [eid for eid, cond in sep_ids.get(frozenset((a, c)), []) if b not in cond]
        if ok:
            rules.setdefault((a, b), []).append((rule, ok, field))
    claims = []
    for i in range(d):
        for j in range(i + 1, d):
            rel, mark = _rel(o, i, j)
            x, y = (j, i) if rel == "y->x" else (i, j)
            rel = "x->y" if rel == "y->x" else rel
            drel, dmark = _rel(data_only_output, x, y)
            c = {"id": "c:%s|%s" % (names[x], names[y]), "x": names[x], "y": names[y], "relation": rel,
                 "direction_source": "none", "licensed_by": "adjacency_test" if by_pair.get(frozenset((i, j))) else "none",
                 "evidence": list(by_pair.get(frozenset((i, j)), [])), "data_only_relation": "x-y" if drel == "y->x" else drel,
                 "knowledge": []}
            if drel == "y->x":
                c["data_only_relation_exact"] = "y->x"
            if mark not in ("", "-->", "---"):
                c["tool_mark"] = mark
            if rel == "x->y" and (x, y) in rules:
                rule, ids, field = rules[(x, y)][0]
                c.update(direction_source="data_pattern", licensed_by=rule,
                         evidence=sorted(set(c["evidence"]) | {e for _, ok, _ in rules[(x, y)] for e in ok}), tool_rule_source=field)
            m = meta.get((x, y)) or meta.get((y, x))
            if m:
                c["tool_edge_meta"] = m
                if rel == "x->y" and m.get("origin") == "expert" and (names[x], names[y]) in req_k:
                    c.update(direction_source="knowledge", licensed_by="declared", knowledge=[req_k[(names[x], names[y])]])
            claims.append(c)
    led = {"format": FORMAT,
           "variables": [{"var_id": var_id(X[:, k], names[k]), "name": names[k], "position": pos.get(k, k)} for k in range(d)],
           "evidence": evid, "knowledge": know, "claims": claims, "overrides": [],
           "report": {"run_id": run_id, "created_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "regime": regime, "data_sha256": dsha, "engines": [engine],
                      "seeds": {"shuffle_seed": run.get("shuffle_seed"), "perm": perm},
                      "invariants": {}, "permutation_check": {"permutations": int(permutations), "identical": bool(identical)},
                      "ledger_sha256": "0" * 64, "unverifiable": list(UNVERIFIABLE),
                      "commentary": "Adapter output for %s. direction_source is 'none' wherever the tool gives no reason for a direction; "
                                    "evidence lists only records the tool exposed." % tool}}
    led["report"]["ledger_sha256"] = V.canonical_hash(led)
    return led


def engine_of(tool, w):
    v = w.get("versions") or {}
    main = {"dowhy+causal-learn": "causal-learn", "pgmpy-pc": "pgmpy", "pgmpy-hillclimb": "pgmpy", "causalnex": "causalnex",
            "dodiscover": "dodiscover", "tigramite": "tigramite", "gcastle": "gcastle", "lingam": "lingam", "py-tetrad": "py-tetrad",
            "pywhy-llm": "pywhy-llm"}[tool]
    ver = v.get(main)
    if tool == "py-tetrad":
        ver = "%s (tetrad %s)" % (ver, ((w["runs"].get("D_seed20261010") or {}).get("info") or {}).get("tetrad_version"))
    if tool == "pywhy-llm":
        ver = "%s (git %s; stub LLM)" % (ver, (v.get("pywhy-llm_git_head") or "")[:12])
    return {"name": main, "version": str(ver)}


def build_all(tool, w, X, names, permutation_identical, main_seed=20261010):
    R = w["runs"]
    D = R["D_seed%d" % main_seed]
    eng = engine_of(tool, w)
    if tool == "pywhy-llm":   # names only: no data-only run exists, so the data supported no connection
        empty = {"directed": [], "undirected": [], "other": []}
        return {"K": build_ledger(tool, D, empty, X, names, "D+K", eng, 3, permutation_identical, "ab11-%s-K" % tool)}
    out = {"D": build_ledger(tool, D, D["output"], X, names, "D", eng, 3, permutation_identical, "ab11-%s-D" % tool)}
    for lab in ("K_required", "K_forbidden", "K_tiers", "K_required_enforce", "K_forbidden_enforce", "K_required_digraph", "K_forbidden_digraph"):
        r = R.get(lab)
        if r and r.get("output"):
            out["D+K_" + lab[2:]] = build_ledger(tool, r, D["output"], X, names, "D+K", eng, 1, True, "ab11-%s-%s" % (tool, lab))
    return out


# ------------------------------------------------------------------------------------------------------------ verifying
def _short(k):
    return k.split()[0] if k.startswith("V") else "limits"


def verify_relaxed(led):
    """Diagnostic only: V2-V8 with the evidence minItems of V1 lifted; V2 counts a claim citing no evidence as a failure."""
    spec = S.CLAIM["properties"]["evidence"]
    old = spec.get("minItems")
    spec["minItems"] = 0
    try:
        res = V.verify(copy.deepcopy(led))
    finally:
        spec["minItems"] = old
    k2 = [k for k in res if k.startswith("V2")]
    if k2:
        res[k2[0]] = res[k2[0]] + ["claim %s cites no evidence" % c["id"] for c in led["claims"] if not c["evidence"]]
    return {_short(k): v for k, v in res.items()}


def run_verifier(path):
    """Run ledger/verify.py unchanged (subprocess, --json) and the relaxed diagnostic in process."""
    p = subprocess.run([sys.executable, str(KIT / "ledger" / "verify.py"), str(path), "--json"], capture_output=True, text=True)
    try:
        off = json.loads(p.stdout)["checks"]
    except (ValueError, KeyError):
        off = {"V1 schema": ["verify.py produced no JSON: %s" % p.stderr[-300:]]}
    led = json.loads(Path(path).read_text())
    rel = verify_relaxed(led)
    return {"exit_code": p.returncode, "official": {_short(k): v[:8] for k, v in off.items()},
            "official_counts": {_short(k): len(v) for k, v in off.items()},
            "relaxed": {k: v[:5] for k, v in rel.items()}, "relaxed_counts": {k: len(v) for k, v in rel.items()},
            "claims": len(led["claims"]), "claims_without_evidence": sum(1 for c in led["claims"] if not c["evidence"]),
            "direction_sources": {s: sum(1 for c in led["claims"] if c["direction_source"] == s and c["relation"] == "x->y")
                                  for s in S.SOURCES}}


SCOPE = {"V1": "all", "V2": "all", "V6": "all", "V3": "K", "V5": "K", "V7": "D", "V8": "D", "V4": "none"}


def _agg(checks, which):
    out = {}
    for v, scope in SCOPE.items():
        if scope == "none":
            vals = [c[which].get(v) for c in checks.values() if c[which].get(v)]
            out[v] = "fail" if vals else "na"
            continue
        rel = [lab for lab in checks if scope == "all" or (scope == "K" and lab != "D") or (scope == "D" and lab in ("D", "K"))]
        st = []
        for lab in rel:
            r = checks[lab][which]
            if v not in r:
                continue          # verify.py stopped after V1
            if scope == "K" and lab == "K" and v == "V5" and not r[v]:
                st.append("pass")
                continue
            st.append("fail" if r[v] else "pass")
        out[v] = "fail" if "fail" in st else ("pass" if st else "na")
    for v in ("V8",):
        if any(lab == "K" for lab in checks) and "D" not in checks:
            out[v] = "na"
    return dict(sorted(out.items()))


def aggregate(checks):
    """Per check: fail if any ledger in its scope fails, pass if at least one passes and none fails, na if untested."""
    return _agg(checks, "official"), _agg(checks, "relaxed")
