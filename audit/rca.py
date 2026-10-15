"""Root-cause ranking through the ledger (D5.2; ER-4b; AB-12's PetShop protocol).

  python -m audit.rca --data /path/to/petshop/dataset --rule C3 --out analysis/results/q2_b5/rca_ledger.json [--split train|test]

For each PetShop scenario and target metric (latency, availability):
  ledger   kernel D (frozen B1 rule) on the normal period (the metric's Average series; columns with >= 10 values and
           non-zero spread, gaps filled with the column mean, as AB-12's learn_pc), plus the declared topology (the call
           graph reversed, AB-12's declared causal graph) as required-edge knowledge statements supplied by the operators.
           Knowledge never connects (I5): a declared edge on a pair the data left unconnected is recorded as an override
           with that reason; on an open data pair it orients the pair; against a data direction the data direction stands.
  view     the RCA graph is read from the ledger alone: every declared edge from the knowledge records, except a
           withheld share (gap experiment, seeded); with 'fill', every directed claim of the ledger on a pair no remaining
           declared edge covers is added.
  ranking  AB-12's traversal and abstention (analysis/ab12_rca_probe.py: MAD>5 anomalies, roots without anomalous
           parents, path-sum score, margin rule with tau tuned on the train split; tau = 0.0 for declared traversal).
Rows: declared (full) through the ledger, which must reproduce AB-12's declared traversal with abstention; withheld 10% and
25% of declared edges (5 seeds each), without and with fill; ledger data claims only (learned).
No model calls. Tickets: BLD-15 (proposed), TGT-20 (proposed), CAP-09
"""
import argparse, json, sys, zlib
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "analysis"))
sys.path.insert(0, str(ROOT / "ledger"))


def declared_edges(call_graph):
    return sorted((str(b), str(a)) for a, b in call_graph.edges())      # call graph reversed: callee -> caller


def rca_ledger(normal, metric, call_graph, rule):
    import ab12_rca_probe as A
    from kernel import build as B
    from kernel.ledger_hash import canonical_hash
    R = A.reduce_df(normal, metric, "Average")
    keep = []
    for c in R.columns:
        x = R[c].to_numpy(dtype=float)
        x = x[~np.isnan(x)]
        if x.shape[0] >= 10 and np.std(x) > 0:
            keep.append(c)
    X = R[keep].copy()
    X = X.fillna(X.mean())
    names = [str(c) for c in keep]
    led, info = B.build(X.to_numpy(dtype=float), names, rule=rule, created_utc="",
                        question={"text": "which service caused the anomaly on the target", "context_of_use": "root-cause analysis (AB-12 protocol)",
                                  "estimand": "the root-cause node of each issue", "cost_ratio": None},
                        file_meta={"source": "AWS PetShop (Hardt et al.), normal period", "file": "noissue/metrics.csv %s Average" % metric})
    if led is None:
        return None, {"failure": info.get("failure"), "names": names}
    led["report"]["regime"] = "D+K"
    byp = {frozenset((c["x"], c["y"])): c for c in led["claims"]}
    knowledge, overrides, ev_new = [], [], []
    for (a, b) in declared_edges(call_graph):
        kid = "kd:%s>%s" % (a, b)
        knowledge.append({"id": kid, "kind": "required_edge", "content": {"from": a, "to": b},
                          "supplier": {"type": "person", "shown": ["declared service topology (graph.csv), reversed call graph"]}})
        c = byp.get(frozenset((a, b)))
        if c is None or c["data_only_relation"] == "none":
            overrides.append({"knowledge": kid, "by": "data", "reason": "declared edge on a pair the data left unconnected (or a node without usable data): used by the RCA view as declared topology, not as a causal claim"})
        elif c["relation"] == "x-y":
            eid = "kd-ev:%s>%s" % (a, b)
            ev_new.append({"id": eid, "type": "knowledge_statement", "variables": [a, b], "conditioning": [], "supports": "x->y", "knowledge": [kid]})
            c.update({"x": a, "y": b, "relation": "x->y", "direction_source": "knowledge", "licensed_by": "declared",
                      "evidence": sorted(set(c["evidence"]) | {eid}), "knowledge": [kid]})
        elif c["relation"] == "x->y" and (c["x"], c["y"]) != (a, b):
            overrides.append({"knowledge": kid, "by": "data", "reason": "the data commit the opposite direction (%s->%s)" % (c["x"], c["y"])})
        else:
            c["knowledge"] = sorted(set(c.get("knowledge", [])) | {kid})
    led["knowledge"] = knowledge
    led["overrides"] = overrides
    led["evidence"] += ev_new
    led["report"]["ledger_sha256"] = canonical_hash(led)
    return led, {"names": names}


FILL_RULES = ("all", "disconnected", "both_engines")


def view_graph(led, nodes, withheld=frozenset(), fill=False, declared=True, fill_rule="all"):
    """fill_rule: 'all' adds every data-sourced directed claim on a pair no remaining declared edge covers;
    'disconnected' only those joining two nodes the remaining declared graph does not connect (in either direction);
    'both_engines' only those both data engines found (claim engines == 'both')."""
    import networkx as nx
    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    cover = set()
    if declared:
        for k in led["knowledge"]:
            if k["kind"] == "required_edge":
                e = (k["content"]["from"], k["content"]["to"])
                if e not in withheld:
                    G.add_edge(*e)
                    cover.add(frozenset(e))
    if fill or not declared:
        comp = {n: i for i, cc in enumerate(nx.weakly_connected_components(G)) for n in cc} if (declared and fill_rule == "disconnected") else None
        for c in led["claims"]:
            if c["relation"] != "x->y" or frozenset((c["x"], c["y"])) in cover or c["direction_source"] == "knowledge":
                continue
            if declared and fill_rule == "disconnected" and comp.get(c["x"]) == comp.get(c["y"]):
                continue
            if declared and fill_rule == "both_engines" and c.get("engines") != "both":
                continue
            G.add_edge(c["x"], c["y"])
    return G


def run(data, rule, seeds=5, shares=(0.10, 0.25), fill_rules=("all",)):
    import ab12_rca_probe as A
    import verify02
    rows, ledgers = [], {}
    for sc in A.SCENARIOS:
        call_graph, normal, issues, _ = A.load_scenario(Path(data), sc, shuffle=False)
        nodes = sorted(set(map(str, call_graph.nodes())) | {str(c[0]) for c in normal.columns})
        dec = declared_edges(call_graph)
        for metric in ("latency", "availability"):
            led, info = rca_ledger(normal, metric, call_graph, rule)
            key = "%s|%s" % (sc, metric)
            ledgers[key] = {"ok": led is not None, "variables": len(info["names"]),
                            "verify_failures": ({k: len(v) for k, v in verify02.verify(led).items() if v} if led else None),
                            "claims_directed": sum(1 for c in led["claims"] if c["relation"] == "x->y") if led else None,
                            "declared_edges": len(dec), "declared_overridden": len(led["overrides"]) if led else None,
                            "ledger_sha256": led["report"]["ledger_sha256"] if led else None}
            variants = {"declared": dict(withheld=frozenset(), fill=False, declared=True)}
            if led is not None:
                variants["learned_ledger_only"] = dict(withheld=frozenset(), fill=False, declared=False)
                for sh in shares:
                    for s in range(seeds):
                        rng = np.random.default_rng([20261015, zlib.crc32(key.encode()), int(sh * 100), s])
                        k = max(1, int(round(sh * len(dec))))
                        w = frozenset(tuple(dec[i]) for i in rng.choice(len(dec), k, replace=False))
                        variants["withheld_%d_s%d" % (int(sh * 100), s)] = dict(withheld=w, fill=False, declared=True)
                        for fr in fill_rules:
                            variants["withheld_%d_s%d_fill-%s" % (int(sh * 100), s, fr)] = dict(withheld=w, fill=True, declared=True, fill_rule=fr)
            graphs = {v: view_graph(led or {"knowledge": [{"kind": "required_edge", "content": {"from": a, "to": b}} for a, b in dec], "claims": []},
                                    nodes, **kw) for v, kw in variants.items()}
            for it in issues:
                t = it["target"]
                tn, tm = t["target"]["node"], t["target"]["metric"]
                if tm != metric:
                    continue
                truth = t["root_cause"]["node"]
                anomalous, row = A.detect(normal, it["metrics"], tn, tm, t["target"]["agg"])
                for v, G in graphs.items():
                    if anomalous is None:
                        cands, info2 = [], {}
                    else:
                        cands, roots, info2 = A.traversal(G, anomalous, tn, check_acyclic=False)
                    hits, _, rlo, rhi = A.tie_hits(cands, truth)
                    rows.append({"scenario": sc, "split": it["split"], "issue": it["issue"], "metric": metric, "variant": v,
                                 "truth": truth, "n_candidates": len(cands), "hits": hits, "margin34": A.margin34(cands),
                                 "abstains": A.abstains(cands, 0.0), "cyclic": bool(info2.get("cyclic_anomalous_subgraph"))})
    return rows, ledgers


def summarize(rows, split):
    out = {}
    for v in sorted({r["variant"] for r in rows}):
        R = [r for r in rows if r["variant"] == v and r["split"] == split]
        ans = [r for r in R if not r["abstains"]]
        out[v] = {"n": len(R), "coverage": len(ans) / len(R) if R else None,
                  "AC@3_answered": float(np.mean([r["hits"][3] for r in ans])) if ans else None,
                  "AC@3_strict": float(np.sum([r["hits"][3] for r in ans]) / len(R)) if R else None,
                  "AC@1_answered": float(np.mean([r["hits"][1] for r in ans])) if ans else None, "cyclic": sum(r["cyclic"] for r in R)}
    import re
    agg = {}
    for v, s in out.items():
        base = "_".join(t for t in v.split("_") if not re.fullmatch(r"s\d+", t))
        agg.setdefault(base, []).append(s)
    return out, {b: {k: float(np.mean([x[k] for x in xs if x[k] is not None])) if any(x[k] is not None for x in xs) else None
                     for k in ("coverage", "AC@3_answered", "AC@3_strict")} | {"draws": len(xs)} for b, xs in agg.items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="/home/claude/work/ext2/petshop/dataset")
    ap.add_argument("--rule", required=True)
    ap.add_argument("--split", default="train", choices=("train", "test"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--fill-rules", nargs="+", default=list(FILL_RULES))
    ap.add_argument("--held-out-read", default=None)
    a = ap.parse_args()
    if a.split == "test":
        import datetime
        from kernel import freeze
        fz_path = ROOT / "plans" / "b5_freeze.json"
        if not a.held_out_read or not fz_path.exists():
            raise SystemExit("the PetShop test split is read through the ledger only with --held-out-read FREEZE_ID and plans/b5_freeze.json")
        fz = json.load(open(fz_path))
        h, _ = freeze.code_sha256()
        if fz["id"] != a.held_out_read or fz["code_sha256"] != h or fz.get("rule") != a.rule:
            raise SystemExit("code, rule or freeze id does not match plans/b5_freeze.json")
        log = ROOT / "analysis" / "results" / "q2_b5" / "access_log.jsonl"
        log.parent.mkdir(parents=True, exist_ok=True)
        with open(log, "a") as fh:
            fh.write(json.dumps({"utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "split": "test",
                                 "freeze": a.held_out_read, "rule": a.rule}) + "\n")
    rows, ledgers = run(a.data, a.rule, fill_rules=tuple(a.fill_rules))
    per, agg = summarize(rows, a.split)
    res = {"tickets": ["BLD-15", "TGT-20", "CAP-09"], "rule": a.rule, "split": a.split, "ledgers": ledgers, "variants": per, "summary": agg,
           "rows": [r for r in rows if r["split"] == a.split]}
    d = [r for r in rows if r["split"] == a.split and r["variant"] == "declared" and not r["abstains"]]
    if d:
        rng = np.random.default_rng(20261015)
        hits = np.array([r["hits"][3] for r in d])
        boots = [float(np.mean(hits[rng.integers(0, len(hits), len(hits))])) for _ in range(2000)]
        lo, hi = np.percentile(boots, [2.5, 97.5])
        cov = per["declared"]["coverage"]
        res["ER-4b"] = {"AC@3_answered": float(hits.mean()), "coverage": cov, "lo": float(lo), "hi": float(hi), "answered": len(d),
                        "met": bool(lo >= 0.90 and cov >= 0.5), "rule": "lower end of the 95% bootstrap interval over answered issues (2,000 resamples, seed 20261015) >= 0.90 at coverage >= 0.5"}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1, default=str)
    for b, s in agg.items():
        print("%-28s %s" % (b, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in s.items()}))


if __name__ == "__main__":
    main()
