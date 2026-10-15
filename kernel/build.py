"""K0-K6: build a data-only claim ledger (v0.2) from one data table (D1.1-D1.5).

  led, info = build(X, names, rule="C3", file_meta={...}, prereg={...})

Steps
  K0  variables: var_id = sha256(values as float64 LE + name) (v0.1 rule), data_id = sha256(values); canonical order =
      columns sorted by data_id. Engines only ever see canonical columns, so the column order a caller passes cannot
      reach them (I1). Names never reach the engines either.
  K1  engines on canonical columns: PC maxP with every CI test recorded; GES (BIC) with a timeout. A singular correlation
      matrix (deterministic relations) is retried once with seeded Gaussian jitter sd 1e-6 on both engines and recorded
      as a deviation; GES failing or timing out makes the rule fall back to PC for this table (policy_fallback).
  K2  PC re-derived from its own tests (kernel.derive); equality with the engine's skeleton and maxP stages is required;
      a final-stage difference is accepted only when it is the engine's directed-cycle defect (causal-learn Meek
      ancestor tracking), and the cycle-closing pairs stay open; anything else is a build error.
  K3  the combination rule (kernel.policy) decides every unordered pair.
  K4  evidence: one ci_test record per distinct test (phases listed); one score_delta record per pair that either engine
      found adjacent (Gaussian BIC change of the pair's edge in a DAG extension of GES's graph, lambda = log(n)/2);
      claims cite the records on their own pair and the premises of their orientation rule.
  K6  the report: plan, deviations, assumptions, lineage, question, engine outputs, invariants, hash.
Everything here is deterministic given the inputs; the ledger hash is v0.1's canonical hash.
"""
import datetime, hashlib, zlib
from itertools import combinations

import numpy as np

from engines import core
from . import derive, policy
from .ledger_hash import canonical_hash

FORMAT = "cc-claim-ledger/0.2"
CONVENTION = "relation 'x->y' means claim.x causes claim.y; 'x-y' adjacent, direction open; 'none' not adjacent"
ALPHA = 0.05
UNVERIFIABLE = ["statistics are recomputed only from the data (verify02 checks the records, not the numbers)",
                "supplier saw only what is recorded (no supplier in a data-only ledger)",
                "calibration outside its calibration set (no calibration in B1)"]
ASSUMPTIONS = [
    {"id": "A1", "statement": "causal sufficiency: no unmeasured common cause of two measured variables", "testable": False,
     "sensitivity": "a hidden common cause produces an adjacency or a direction that no DAG over the measured variables explains; "
                    "FCI on the same data would mark such pairs o-o or <->"},
    {"id": "A2", "statement": "faithfulness: every independence in the data comes from the graph", "testable": False,
     "sensitivity": "near-cancelling paths delete true adjacencies; the ci_test records with p near alpha show where"},
    {"id": "A3", "statement": "Gaussian linear tests (Fisher-z, BIC) detect the dependences present", "testable": True,
     "sensitivity": "nonlinear or non-Gaussian dependence lowers recall; the skeleton is then a subset of the truth"},
    {"id": "A4", "statement": "rows are independent draws from one distribution (no interventions mixed in)", "testable": True,
     "sensitivity": "mixed regimes create dependences between intervention targets and their non-descendants"},
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def variables(X, names):
    X = np.ascontiguousarray(np.asarray(X, dtype="<f8"))
    data_ids = core.column_ids(X)
    var_ids = [sha(np.ascontiguousarray(X[:, j]).tobytes() + nm.encode()) for j, nm in enumerate(names)]
    order = core.canonical_order(ids=data_ids, tiebreak=var_ids)
    canon_index = {orig: k for k, orig in enumerate(order)}
    out = []
    for j, nm in enumerate(names):
        out.append({"var_id": var_ids[j], "name": nm, "position": j, "data_id": data_ids[j], "canonical_index": canon_index[j]})
    return out, order


def _local_bic(Z, v, parents, lam):
    n = Z.shape[0]
    y = Z[:, v]
    if parents:
        A = np.column_stack([Z[:, sorted(parents)], np.ones(n)])
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        r = y - A @ coef
    else:
        r = y - y.mean()
    rss = max(float(r @ r), 1e-300)
    return -0.5 * n * np.log(rss / n) - lam * len(parents)


def dag_extension(n, D, U):
    """Dor-Tarsi consistent extension of a PDAG; returns parents {v: set}. Falls back to orienting a -> b (a < b)
    for any undirected pair it cannot place (the PDAG then has no extension; recorded by the caller)."""
    D = set(D)
    U = {tuple(sorted(u)) for u in U}
    alive = set(range(n))
    parents = {v: {a for a, b in D if b == v} for v in range(n)}
    und = {v: set() for v in range(n)}
    for a, b in U:
        und[a].add(b)
        und[b].add(a)
    out_dir = {v: {b for a, b in D if a == v} for v in range(n)}
    ok = True
    while alive:
        pick = None
        for x in sorted(alive):
            if out_dir[x] & alive:
                continue
            nb = (und[x] | parents[x]) & alive
            if all(all(frozenset((y, w)) in {frozenset(e) for e in D} | {frozenset(u) for u in U} for w in nb if w != y)
                   for y in und[x] & alive):
                pick = x
                break
        if pick is None:
            ok = False
            for a, b in sorted(U):
                if a in alive and b in alive and b in und[a]:
                    parents[b].add(a)
            break
        for y in und[pick] & alive:
            parents[pick].add(y)
        alive.discard(pick)
    return parents, ok


def run_engines(X, names, with_ges=True, ges_timeout_s=600, jitter_seed=None, created_utc=None):
    """K1 on canonical columns. -> dict(order, Xc, data_sha, pc, ges, jittered, deviations). Reusable across rules."""
    X = np.asarray(X, dtype=float)
    _, order = variables(X, [str(n) for n in names])
    Xc = X[:, order]
    data_sha = sha(np.ascontiguousarray(Xc, dtype="<f8").tobytes())
    deviations = []
    pc_res = core.run_pc_maxp(Xc, alpha=ALPHA)
    jittered = False
    if not pc_res.ok and pc_res.failure["type"] == "singular":
        seed = jitter_seed if jitter_seed is not None else zlib.crc32(data_sha.encode())
        Xc = Xc + 1e-6 * np.random.default_rng(seed).standard_normal(Xc.shape)
        jittered = seed
        deviations.append({"what": "Gaussian jitter sd 1e-6 (seed %d) added to the canonical columns" % seed,
                           "why": "singular correlation matrix (%s): the Fisher-z test is undefined on exactly collinear columns" % pc_res.failure["message"][:80],
                           "utc": created_utc or ""})
        pc_res = core.run_pc_maxp(Xc, alpha=ALPHA)
    ges_res = core.run_ges_bic(Xc, timeout_s=ges_timeout_s) if (with_ges and pc_res.ok) else None
    return {"order": order, "Xc": Xc, "data_sha": data_sha, "pc": pc_res, "ges": ges_res, "jittered": jittered, "deviations": deviations}


def build(X, names, rule="C3", file_meta=None, prereg=None, question=None, regime="D", ges_timeout_s=600,
          jitter_seed=None, run_id=None, created_utc=None, eng=None):
    """-> (ledger dict, info dict). info carries the engine results and the derivation for runners and the checker.
    eng: the output of run_engines() for these data, to build several rules from one engine run.
    A table on which PC cannot run even after the jitter retry returns (None, info) with info['failure']."""
    file_meta = file_meta or {}
    names = [str(n) for n in names]
    if len(set(names)) != len(names):
        raise ValueError("variable names must be unique")
    X = np.asarray(X, dtype=float)
    n_rows, n = X.shape
    vars_, order = variables(X, names)
    eng = eng or run_engines(X, names, with_ges=(rule != "pc"), ges_timeout_s=ges_timeout_s, jitter_seed=jitter_seed, created_utc=created_utc)
    assert list(eng["order"]) == list(order)
    Xc, data_sha, pc_res, jittered = eng["Xc"], eng["data_sha"], eng["pc"], eng["jittered"]
    cname = [names[j] for j in order]
    deviations, info = list(eng["deviations"]), {"order": order, "rule": rule, "eng": eng}
    info["pc"] = pc_res
    if not pc_res.ok:
        info["failure"] = {"engine": "pc_maxp", **pc_res.failure}
        return None, info
    der = derive.pc_maxp_from_tests(n, pc_res.tests, ALPHA)
    info["derive"] = der
    defects = []
    if der["missing_tests"]:
        raise RuntimeError("maxP needed tests the engine did not record: %s" % der["missing_tests"][:3])
    if not np.array_equal(der["skeleton"], pc_res.stages["skeleton"]) or not np.array_equal(der["after_maxp"], pc_res.stages["after_maxp"]):
        raise RuntimeError("re-derived PC skeleton or maxP stage differs from the engine's")
    De, Ue = core.marks_to_sets(pc_res.marks)
    Dd0, Ud0 = core.marks_to_sets(der["final"])
    if (De, Ue) != (Dd0, Ud0):
        diff = sorted({tuple(sorted(e)) for e in (De ^ Dd0)} | {tuple(sorted(u)) for u in (Ue ^ Ud0)})
        defects.append({"type": "engine_meek_divergence", "engine": "causal-learn 0.1.4.8 Meek.meek",
                        "engine_cyclic": _has_cycle(n, De), "rederived_cyclic": _has_cycle(n, Dd0),
                        "pairs": sorted([cname[a], cname[b]] for a, b in diff),
                        "note": "skeleton and maxP stages equal; the Meek step differs (the engine's ancestor test reads a stale path matrix). "
                                "The kernel uses the re-derivation"})
    Dd, Ud, opened = policy.open_cycles(Dd0, Ud0)
    if opened:
        defects.append({"type": "pc_directed_cycle", "pairs_left_open": sorted([cname[a], cname[b]] for a, b in opened),
                        "note": "maxP colliders and Meek orientations form a directed cycle; every orientation on it is withdrawn"})
    applied = [c for c in der["colliders"] if c["applied"]]
    vlab = {}
    for c in applied:
        vlab[(c["x"], c["y"])] = ("v_structure", [])
        vlab[(c["z"], c["y"])] = ("v_structure", [])
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
    ges_res = None
    if rule != "pc":
        ges_res = eng["ges"]
        info["ges"] = ges_res
        if ges_res is not None and ges_res.ok:
            Dg, Ug = core.marks_to_sets(ges_res.marks)
            ges = {"D": Dg, "U": Ug, "labels": policy.label_cpdag(n, Dg, Ug)}
    decisions, fallback = policy.decide(rule, n, pc, ges)
    decisions, opened_rule = policy.guard(decisions, n)
    if opened_rule:
        defects.append({"type": "rule_directed_cycle", "rule": rule, "pairs_left_open": sorted([cname[a], cname[b]] for a, b in opened_rule),
                        "note": "the rule's combined directions form a directed cycle; every orientation on it is withdrawn"})
    info["decisions"] = decisions
    if fallback:
        deviations.append({"what": "rule %s fell back to pc for this table" % rule,
                           "why": "GES failed: %s" % (ges_res.failure["message"][:120] if ges_res is not None and ges_res.failure else "not run"),
                           "utc": created_utc or ""})

    # ---- K4 evidence
    eng_pc = {"name": "causal-learn PC (stable, fisherz, maxP priority 3)", "version": "0.1.4.8"}
    eng_ges = {"name": "ges.fit_bic (GES, Gaussian BIC)", "version": "1.1.0"}
    tests = {}
    for ph, i, j, S, p in pc_res.tests:
        key = (i, j, S)
        if key not in tests:
            tests[key] = {"p": p, "phases": [ph]}
        elif ph not in tests[key]["phases"]:
            tests[key]["phases"].append(ph)
    evidence, by_pair = [], {}
    for (i, j, S), t in sorted(tests.items(), key=lambda kv: (kv[0][0], kv[0][1], len(kv[0][2]), kv[0][2])):
        eid = "t:" + sha(("%s|%s|%s" % (vars_[order[i]]["var_id"], vars_[order[j]]["var_id"],
                                       ",".join(vars_[order[s]]["var_id"] for s in S))).encode())[:16]
        evidence.append({"id": eid, "type": "ci_test", "variables": [cname[i], cname[j]], "conditioning": [cname[s] for s in S],
                         "p_value": t["p"], "phases": t["phases"], "data_sha256": data_sha, "engine": eng_pc, "seed": None,
                         "supports": "nonadjacent" if t["p"] > ALPHA else "adjacent"})
        by_pair.setdefault((i, j), []).append((eid, t["p"], "skeleton" in t["phases"]))
    score_ev = {}
    if ges is not None:
        Z = (Xc - Xc.mean(0)) / Xc.std(0)
        lam = 0.5 * np.log(n_rows)
        parents, ext_ok = dag_extension(n, ges["D"], ges["U"])
        union = {frozenset(e) for e in ges["D"]} | {frozenset(u) for u in ges["U"]} | {frozenset(e) for e in Dd} | {frozenset(u) for u in Ud}
        gadj = {frozenset(e) for e in ges["D"]} | {frozenset(u) for u in ges["U"]}
        for pr in sorted(tuple(sorted(p)) for p in union):
            a, b = pr
            if frozenset(pr) in gadj:
                child, par = (b, a) if a in parents[b] else (a, b)
                delta = _local_bic(Z, child, parents[child], lam) - _local_bic(Z, child, parents[child] - {par}, lam)
                sup = "adjacent"
            else:
                d1 = _local_bic(Z, b, parents[b] | {a}, lam) - _local_bic(Z, b, parents[b], lam)
                d2 = _local_bic(Z, a, parents[a] | {b}, lam) - _local_bic(Z, a, parents[a], lam)
                delta, sup = max(d1, d2), "nonadjacent"
            eid = "s:" + sha(("%s|%s" % (vars_[order[a]]["var_id"], vars_[order[b]]["var_id"])).encode())[:16]
            evidence.append({"id": eid, "type": "score_delta", "variables": [cname[a], cname[b]], "conditioning": [],
                             "score": float(delta), "data_sha256": data_sha, "engine": eng_ges, "seed": None, "supports": sup,
                             "rule": "Gaussian BIC change of this pair's edge in a DAG extension of GES's graph (lambda log(n)/2)"})
            score_ev[pr] = eid
        if not ext_ok:
            deviations.append({"what": "GES graph has no consistent DAG extension", "why": "score deltas use a forced extension", "utc": created_utc or ""})

    # ---- claims
    claims = []
    cid = {}
    for (a, b), d in sorted(decisions.items()):
        if d.relation == "b->a":
            x, y = b, a
        else:
            x, y = a, b
        rel = {"a->b": "x->y", "b->a": "x->y", "a-b": "x-y", "none": "none"}[d.relation]
        ev = []
        own = by_pair.get((a, b), [])
        if own:
            sk = [t for t in own if t[2]]
            pick = max(sk or own, key=lambda t: t[1])
            ev.append(pick[0])
        if (a, b) in score_ev:
            ev.append(score_ev[(a, b)])
        if d.licensed_by == "v_structure" and rel == "x->y":
            col = next((c for c in applied if c["y"] == y and x in (c["x"], c["z"])), None)
            if col is not None:
                u, w = col["x"], col["z"]
                rec = [t for t in by_pair.get((min(u, w), max(u, w)), [])]
                if rec:
                    ev.append(max(rec, key=lambda t: t[1])[0])
        c = {"id": "c:%s|%s" % (cname[a], cname[b]), "x": cname[x], "y": cname[y], "relation": rel,
             "direction_source": "data_pattern" if rel == "x->y" else "none", "licensed_by": d.licensed_by,
             "evidence": sorted(set(ev)), "data_only_relation": rel, "knowledge": [], "engines": d.engines, "conflict": bool(d.conflict),
             "derived_from": []}
        cid[(a, b)] = c["id"]
        claims.append(c)
    for c, ((a, b), d) in zip(claims, sorted(decisions.items())):
        c["derived_from"] = sorted(cid[tuple(sorted(p))] for p in d.premises if tuple(sorted(p)) in cid)
    led = {"format": FORMAT, "variables": vars_, "evidence": evidence, "knowledge": [], "claims": claims, "overrides": [],
           "reviews": [],
           "report": {
               "run_id": run_id or ("ledger-" + data_sha[:12]), "created_utc": created_utc or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "regime": regime, "data_sha256": data_sha, "engines": [eng_pc] + ([eng_ges] if rule != "pc" else []),
               "seeds": {"jitter": jittered if jittered is not False else None},
               "rule": rule, "alpha": ALPHA,
               "invariants": {},
               "permutation_check": _permutation_check(X, names),
               "ledger_sha256": "0" * 64,
               "unverifiable": UNVERIFIABLE,
               "plan": prereg or {"prereg": "none", "prereg_sha256": "0" * 64},
               "deviations": deviations,
               "assumptions": ASSUMPTIONS,
               "lineage": {"source": file_meta.get("source", "caller"), "file": file_meta.get("file", ""), "sha256": file_meta.get("sha256", data_sha),
                           "transformations": ["columns reordered to canonical order (sorted by data_id)"] + (["Gaussian jitter sd 1e-6"] if jittered is not False else [])},
               "question": question or {"text": "which variables cause which, from these data alone", "context_of_use": "benchmark evaluation",
                                        "estimand": "the causal graph's equivalence class", "cost_ratio": None},
               "orientation_convention": CONVENTION,
               "engine_outputs": {
                   "canonical_order": [names[j] for j in order],
                   "pc": {"ok": True, "directed": sorted([cname[a], cname[b]] for a, b in De), "undirected": sorted([cname[a], cname[b]] for a, b in Ue),
                          "kernel_directed": sorted([cname[a], cname[b]] for a, b in Dd), "kernel_undirected": sorted([cname[a], cname[b]] for a, b in Ud),
                          "tests": len(pc_res.tests), "distinct_tests": len(tests), "seconds": round(pc_res.seconds, 3), "defects": defects},
                   "ges": None if rule == "pc" else ({"ok": True, "directed": sorted([cname[a], cname[b]] for a, b in ges["D"]),
                                                      "undirected": sorted([cname[a], cname[b]] for a, b in ges["U"]),
                                                      "score": ges_res.score, "seconds": round(ges_res.seconds, 3)} if ges is not None else
                                                     {"ok": False, "failure": ges_res.failure if ges_res is not None else None}),
                   "policy_fallback": fallback, "jittered": jittered is not False}}}
    led["report"]["ledger_sha256"] = canonical_hash(led)
    return led, info


def _has_cycle(n, D):
    nxt = {i: [b for a, b in D if a == i] for i in range(n)}
    color = [0] * n

    def dfs(u):
        color[u] = 1
        for v in nxt[u]:
            if color[v] == 1 or (color[v] == 0 and dfs(v)):
                return True
        color[u] = 2
        return False
    return any(color[i] == 0 and dfs(i) for i in range(n))


def _permutation_check(X, names, k=6, seed=20261014):
    """The engines see only the canonical table, and names map to canonical indices by data and name alone, so every
    column order must give the same canonical table and the same name in every canonical column. Checked here on k
    orders (identity, reversed, seeded random); full engine reruns under permutation are B1.1's test."""
    X = np.asarray(X, dtype=float)
    d = X.shape[1]
    _, o = variables(X, names)
    base, base_names = X[:, o], [names[j] for j in o]
    rng = np.random.default_rng(seed)
    perms = [list(range(d)), list(range(d))[::-1]] + [list(rng.permutation(d)) for _ in range(k - 2)]
    same = True
    for p in perms:
        Xp, Np = X[:, p], [names[j] for j in p]
        _, op = variables(Xp, Np)
        same &= bool(np.array_equal(Xp[:, op], base)) and [Np[j] for j in op] == base_names
    return {"permutations": k, "identical": bool(same),
            "method": "canonical table and name-to-column assignment identical under %d column orders (engines see only the table)" % k}
