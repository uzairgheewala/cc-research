"""K2 dev evaluation: decision weights and knowledge propagation, on the engine cache, with AB-07's recorded tier
replies replayed through the supplier contract (no model call). Dev split only.

  python -m kernel.k2_eval --family semantic formula     -> analysis/results/q2_v3/k2_dev.json

Per file and name arm (real, neutral, moved): B3's rule (no propagation) against K2's (Meek propagation from data and
knowledge directions); directed F1 (expectation rule), expected-credit F1, DV-1; the T3 bound with k = direct + propagated;
and the decision weights of the D ledger's open pairs with the oracle gain of each (orient it the true way).
"""
import argparse, json, multiprocessing as mp, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
ARMS = ("real", "neutral", "moved")


def one(args):
    path, family, answers_path, scen_path = args
    from score import bench, dv, graph
    from supplier import contract as C, tiers as TS
    from kernel import build as B, cache, views, weights, checker
    from kernel.knowledge import apply_tiers
    from kernel.run_b3 import expected_f1, t3_bound
    import verify02
    s = bench.load(path)
    X, name = s["values"], Path(path).name
    sc_all = json.load(open(scen_path))
    key = next(k for k, v in sc_all.items() if v["family"] == family and "_%s__" % v["scenario"] in name)
    scen = sc_all[key]
    answers = TS.load_answers(answers_path)
    I = bench.truth_info(family, name)
    T, seed = I["T"], graph.file_seed(name)
    row = {"file": name, "scenario": bench.scenario_of(name), "arms": {}}
    for arm in ARMS:
        names = list(scen["labels"][arm])
        eng = cache.engines(X, names, read_only=True)
        led_d, _ = B.build(X, names, rule="C3", eng=eng, created_utc="")
        if led_d is None:
            return {"file": name, "failure": "pc"}
        stmts = {}
        for ph in ("p0", "p1", "p2"):
            rec = answers.get((family, scen["scenario"], arm, ph))
            if rec is None:
                stmts[ph] = None
                continue
            out = C.call(TS.replay_transport(rec), {"id": rec["id"]}, TS.schema(names), max_tokens=1500)
            stmts[ph] = None if out.status in ("abstained", "stopped") else {"tiers": out.value, "supplier": {"type": "model", "phrasing_id": ph}}
        Dd, Ud = views.graph_sets(led_d)
        res = {"D": _sc(I, Dd, Ud, T, seed)}
        lk, ik = apply_tiers(led_d, stmts)
        lp, ip = weights.apply_tiers_propagating(led_d, stmts)
        for lab, led, inf in (("B3", lk, ik), ("K2", lp, ip)):
            Dk, Uk = views.graph_sets(led)
            pos = {v["name"]: v["position"] for v in led["variables"]}
            dec = [tuple(sorted((pos[a], pos[b]))) for a, b in inf["decided"]] + [tuple(sorted((pos[a], pos[b]))) for a, b, *_ in inf.get("propagated", [])]
            ef_d, nP, nT = expected_f1(Dd, Ud, T)
            ef_k, _, _ = expected_f1(Dk, Uk, T)
            r = _sc(I, Dk, Uk, T, seed)
            r.update({"decided": len(inf["decided"]), "propagated": len(inf.get("propagated", [])), "loss_expected": ef_d - ef_k,
                      "t3_bound": t3_bound(Dd, Ud, T, dec), "within_t3": (ef_d - ef_k) <= t3_bound(Dd, Ud, T, dec) + 1e-12,
                      "claims_identical_to_D": [(c["x"], c["y"], c["relation"]) for c in led["claims"]] == [(c["x"], c["y"], c["relation"]) for c in led_d["claims"]],
                      "verify_failures": sum(len(v) for v in verify02.verify(led).values()), "checker_ok": checker.check(led)["ok"]})
            res[lab] = r
        if arm == "real":
            W = weights.decision_weights(I["n"], Dd, Ud, I["targets"])
            gains = []
            for (a, b), w in W.items():
                truth = (a, b) if (a, b) in T else ((b, a) if (b, a) in T else None)
                g = 0.0
                if truth is not None:
                    from kernel import policy
                    adj = {frozenset(e) for e in Dd} | {frozenset(u) for u in Ud}
                    D2, _ = policy.meek_closure(I["n"], adj, Dd | {truth})
                    U2 = {u for u in Ud if (u[0], u[1]) not in D2 and (u[1], u[0]) not in D2}
                    g = expected_f1(D2, U2, T)[0] - expected_f1(Dd, Ud, T)[0]
                gains.append({"pair": [a, b], "weight": w["weight"], "settle": w["settle"], "answers": w["answers"], "true_edge": truth is not None, "oracle_gain": g})
            row["weights"] = gains
        row["arms"][arm] = res
    return row


def _sc(I, D, U, T, seed):
    from score import dv, graph
    ch = dv.check(dv.claims(I["n"], D, U, I["targets"]), I["desc"])
    return {"f1": graph.directed_f1(D, U, T, seed)["f1"], "dv_com": len(ch), "dv_ok": sum(ok for *_, ok in ch),
            "dv_yes": sum(1 for *_, v, ok in ch if v), "dv_yes_ok": sum(1 for *_, v, ok in ch if v and ok), "dv_pairs": dv.n_pairs(I["n"], I["targets"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", nargs="+", default=["semantic", "formula"])
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--answers", default=str(ROOT / "plans" / "results" / "a3_tiers_answers.jsonl"))
    ap.add_argument("--scenarios", default=str(ROOT / "plans" / "a3_scenarios.json"))
    a = ap.parse_args()
    from score import bench, paired
    out = {}
    for fam in a.family:
        fs = [str(p) for p in bench.files(fam, split="dev")]
        fs = fs[: a.limit] if a.limit else fs
        t0 = time.time()
        with mp.get_context("fork").Pool(a.workers) as pool:
            rows = [r for r in pool.map(one, [(f, fam, a.answers, a.scenarios) for f in fs]) if "failure" not in r]
        summ = {"files": len(rows), "wall_seconds": round(time.time() - t0, 1), "arms": {}}
        for arm in ARMS:
            summ["arms"][arm] = {}
            for lab in ("D", "B3", "K2"):
                S = lambda k: sum(r["arms"][arm][lab][k] for r in rows)  # noqa: E731
                d = {"f1": S("f1") / len(rows), "dv1_precision": S("dv_ok") / S("dv_com"), "dv1_coverage": S("dv_com") / S("dv_pairs"),
                     "dv1_yes_precision": S("dv_yes_ok") / max(1, S("dv_yes"))}
                if lab != "D":
                    by = {}
                    for r in rows:
                        by.setdefault(r["scenario"], []).append(r["arms"][arm][lab]["f1"] - r["arms"][arm]["D"]["f1"])
                    d.update({"gain": paired.cluster_bootstrap(by), "decided": S("decided"), "propagated": S("propagated"),
                              "within_t3": sum(r["arms"][arm][lab]["within_t3"] for r in rows),
                              "claims_identical_to_D": sum(r["arms"][arm][lab]["claims_identical_to_D"] for r in rows),
                              "ledgers_failing": sum((r["arms"][arm][lab]["verify_failures"] > 0) or (not r["arms"][arm][lab]["checker_ok"]) for r in rows)})
                summ["arms"][arm][lab] = d
        W = [w for r in rows for w in r.get("weights", [])]
        W.sort(key=lambda w: -w["weight"])
        tot = sum(w["oracle_gain"] for w in W)
        third = W[: max(1, len(W) // 3)]
        summ["weights"] = {"open_pairs": len(W), "oracle_gain_total_sum": tot, "top_third_share_of_oracle_gain": (sum(w["oracle_gain"] for w in third) / tot) if tot else None,
                           "weight_quartiles": [W[int(q * (len(W) - 1))]["weight"] for q in (0, 0.25, 0.5, 0.75, 1.0)] if W else None,
                           "true_edge_share_top_third": sum(w["true_edge"] for w in third) / len(third) if third else None,
                           "true_edge_share_all": sum(w["true_edge"] for w in W) / len(W) if W else None}
        out[fam] = dict(summ, rows=rows)
        print(fam, json.dumps({k: v for k, v in summ.items()}, default=float)[:3000])
    p = ROOT / "analysis" / "results" / "q2_v3" / "k2_dev.json"
    json.dump(out, open(p, "w"), indent=1)


if __name__ == "__main__":
    main()
