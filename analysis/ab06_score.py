"""AB-06 (AUD-38) scorer: LLM-using systems under real / neutral / swapped names, columns shuffled.

  python analysis/ab06_score.py --plans plans/ab06 --out analysis/results/ab06 [--stub]

Reads each plan's run folder (result.json, summary.json; /research mapped to this repository). Per agent and arm:
runs ok / failed, mean directed F1 under the expectation rule (the runner's score; undecided pairs at random), DV-1
committed-claim precision and coverage with the released intervention targets (decision_value_v2), and cost.
Name reliance = F1(real) - F1(swapped), paired by scenario; neutral as the no-information arm.
Data-only floor (P10): where the agent exposes its own data-only graph (result.json variants "pc_only*"), DV-1 of that
graph against the agent's final graph, real arm.
Predictions (plans/audit_dag.json): P9 at least three agents lose >= 0.10 directed F1 from real to swapped (refuted:
none does); P10 at least one agent scores below its own data-only output with real names on DV-1 (refuted: all at or
above). Causal-Copilot's own numbers come from BND-08 (gpt-4o) and are added as a fifth system when present.
No model calls.

v2 (14 Oct, before any live grid run; plans/ab06_prereg.json, hashed in manifests/evidence/ab06_prereg_2026-10-14.sha256):
  * Systems for P9: the four agents plus Causal-Copilot on gpt-4o (BND-08, S3 directed F1 by data, paired by S2 family,
    from analysis/results/stability_s2/partial_stages.json; already measured, declared as such). Causal-Copilot on
    gpt-4o-mini (analysis/results/ab06_cc/partial_stages.json) is reported as RQ-17 and not counted again in P9.
  * A system enters P9 only with at least 5 paired (real, swapped) scenarios; the verdict counts the systems that enter.
  * Vashishtha et al.: per run, the share of triplet answers without an <Answer> tag (the repository's 300-token limit),
    read from calls.jsonl, reported as a diagnostic.
  * P10 is unchanged (agents that expose a data-only graph: MATMCD pc_only_initial, Vashishtha pc_only).
"""
import argparse, json, os, re, statistics as st, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from decision_value_v2 import Truth, claims  # noqa: E402


RUNS_ROOT = [ROOT]
MIN_PAIRS_P9 = 5
CC_SYSTEMS = (("causal_copilot_gpt4o", "stability_s2", True), ("causal_copilot_gpt4omini", "ab06_cc", False))


def untagged_share(calls_path):
    """Vashishtha et al.: share of triplet answers without <Answer>...</Answer> (the repository then casts no vote)."""
    n = bad = 0
    if not Path(calls_path).exists():
        return None
    for line in open(calls_path, encoding="utf-8"):
        if "create a directed acyclic graph" not in line:
            continue
        r = json.loads(line)
        if "request" not in r:
            continue
        n += 1
        if not re.search(r"<Answer>(.*?)</Answer>", r.get("response_text") or ""):
            bad += 1
    return round(bad / n, 4) if n else None


def cc_system(path):
    """Causal-Copilot from partial_stages.json: S3 directed F1 (by data) per family and role; paired real - swapped."""
    if not Path(path).exists():
        return None
    P = json.loads(Path(path).read_text(encoding="utf-8"))
    fam = {}
    for r in P["rows"]:
        if r.get("S3_dir_f1_by_data") is None:
            continue
        fam.setdefault(r["family"], {}).setdefault(r["role"], []).append(r["S3_dir_f1_by_data"])
    m = {f: {k: st.mean(v) for k, v in d.items()} for f, d in fam.items()}
    dr = [v["real"] - v["swapped"] for v in m.values() if "real" in v and "swapped" in v]
    dn = [v["real"] - v["neutral"] for v in m.values() if "real" in v and "neutral" in v]
    out = {"source": str(path), "metric": "S3 directed F1 (graph handed to the cycle step), by data, per S2 family",
           "families": len(m)}
    for arm in ("real", "neutral", "swapped"):
        xs = [v[arm] for v in m.values() if arm in v]
        out[arm] = {"families": len(xs), "f1_mean": round(st.mean(xs), 4) if xs else None}
    out["name_reliance_real_minus_swapped"] = {"paired_scenarios": len(dr), "mean": round(st.mean(dr), 4) if dr else None}
    out["real_minus_neutral"] = {"paired_scenarios": len(dn), "mean": round(st.mean(dn), 4) if dn else None}
    return out


def local(p):
    return Path(str(p).replace("/research", str(RUNS_ROOT[0]), 1))


def edges(directed, undecided):
    """Runner format: directed [{from_idx, to_idx, source}, ...] or [[a, b], ...]; undecided [{a_idx, b_idx}, ...] or [[a, b, ...]]."""
    D = {(e["from_idx"], e["to_idx"]) if isinstance(e, dict) else (e[0], e[1]) for e in directed}
    U = {tuple(sorted((u["a_idx"], u["b_idx"]) if isinstance(u, dict) else (u[0], u[1]))) for u in undecided}
    return D, U


def dv(tr, file, directed, undecided):
    I = tr.get(file)
    D, U = edges(directed, undecided)
    cl = claims(I["n"], D, U, I["targets"])
    ok = sum(1 for (t, y), v in cl.items() if (y in I["desc"][t]) == v)
    return ok, len(cl), len(I["targets"]) * (I["n"] - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans", default=str(ROOT / "plans" / "ab06"))
    ap.add_argument("--root", default=str(ROOT / "external" / "causalarena"))
    ap.add_argument("--out", default=str(HERE / "results" / "ab06"))
    ap.add_argument("--stub", action="store_true")
    ap.add_argument("--runs-root", default=str(ROOT), help="what /research means for the run folders (default: this repository)")
    ap.add_argument("--cc-root", default=str(HERE / "results"), help="folder holding stability_s2/ and ab06_cc/ (Causal-Copilot partial_stages.json)")
    a = ap.parse_args()
    RUNS_ROOT[0] = Path(a.runs_root)
    tr = Truth(a.root, "semantic")
    rows = []
    for p in sorted(Path(a.plans).glob("*__*__*.json")):      # plan files only (TIERS.json, BUDGET.json are not plans; v2.1)
        pl = json.loads(p.read_text(encoding="utf-8"))
        out = local(pl["run"]["out_stub" if a.stub else "out"])
        s = json.loads((out / "summary.json").read_text()) if (out / "summary.json").exists() else None
        r = json.loads((out / "result.json").read_text()) if (out / "result.json").exists() else None
        rec = {"agent": pl["agent"], "arm": pl["arm"], "scenario": pl["scenario_id"], "status": (s or {}).get("status", "not run"),
               "usd": (s or {}).get("est_usd_at_served_prices"), "calls": (s or {}).get("calls")}
        if r and rec["status"] == "ok":
            f = r["scenario"]
            rec["f1"] = (s or {}).get("directed_f1_random_rule")
            ok, com, pairs = dv(tr, f, r["directed"], r.get("undecided", []))
            rec.update({"dv_ok": ok, "dv_com": com, "dv_pairs": pairs})
            src = {}
            for e in r["directed"]:
                if isinstance(e, dict):
                    src[e.get("source", "unrecorded")] = src.get(e.get("source", "unrecorded"), 0) + 1
            rec["direction_sources"] = src
            if pl["agent"] == "vashishtha":
                rec["untagged_triplet_share"] = untagged_share(out / "calls.jsonl")
            for k, v in (r.get("variants") or {}).items():
                if k.startswith("pc_only") and isinstance(v, dict):
                    ok2, com2, _ = dv(tr, f, v["directed"], v.get("undecided", []))
                    rec.update({"data_only_variant": k, "dv_ok_data_only": ok2, "dv_com_data_only": com2,
                                "f1_data_only": (v.get("scores") or {}).get("random", {}).get("f1")})
        rows.append(rec)
    res = {"tickets": ["AUD-38", "STR-01", "RQ-05", "RQ-17"], "stub": a.stub, "agents": {}}
    for agent in sorted({r["agent"] for r in rows}):
        A = res["agents"][agent] = {}
        for arm in ("real", "neutral", "swapped"):
            xs = [r for r in rows if r["agent"] == agent and r["arm"] == arm]
            ok = [r for r in xs if r["status"] == "ok"]
            com = sum(r.get("dv_com", 0) for r in ok)
            A[arm] = {"runs": len(xs), "ok": len(ok), "not_ok": {s: sum(1 for r in xs if r["status"] == s) for s in {r["status"] for r in xs if r["status"] != "ok"}},
                      "f1_mean": round(st.mean(r["f1"] for r in ok), 4) if ok else None,
                      "dv1_precision": round(sum(r.get("dv_ok", 0) for r in ok) / com, 4) if com else None,
                      "dv1_coverage": round(com / sum(r.get("dv_pairs", 1) for r in ok), 4) if ok else None,
                      "usd": round(sum(r["usd"] or 0 for r in xs), 3),
                      "direction_sources": {k: sum(r.get("direction_sources", {}).get(k, 0) for r in ok)
                                            for k in sorted({k for r in ok for k in r.get("direction_sources", {})})}}
        pair = {}
        for r in rows:
            if r["agent"] == agent and r["status"] == "ok":
                pair.setdefault(r["scenario"], {})[r["arm"]] = r["f1"]
        dr = [v["real"] - v["swapped"] for v in pair.values() if "real" in v and "swapped" in v]
        dn = [v["real"] - v["neutral"] for v in pair.values() if "real" in v and "neutral" in v]
        A["name_reliance_real_minus_swapped"] = {"paired_scenarios": len(dr), "mean": round(st.mean(dr), 4) if dr else None}
        A["real_minus_neutral"] = {"paired_scenarios": len(dn), "mean": round(st.mean(dn), 4) if dn else None}
        do = [r for r in rows if r["agent"] == agent and r["arm"] == "real" and "dv_com_data_only" in r]
        if do:
            A["data_only_floor_real_arm"] = {
                "variant": do[0]["data_only_variant"], "scenarios": len(do),
                "dv1_precision_final": round(sum(r["dv_ok"] for r in do) / max(1, sum(r["dv_com"] for r in do)), 4),
                "dv1_precision_data_only": round(sum(r["dv_ok_data_only"] for r in do) / max(1, sum(r["dv_com_data_only"] for r in do)), 4),
                "f1_final": round(st.mean(r["f1"] for r in do), 4),
                "f1_data_only": round(st.mean(r["f1_data_only"] for r in do if r["f1_data_only"] is not None), 4) if any(r["f1_data_only"] is not None for r in do) else None}
        un = [r["untagged_triplet_share"] for r in rows if r["agent"] == agent and r.get("untagged_triplet_share") is not None]
        if un:
            A["untagged_triplet_share_mean"] = round(st.mean(un), 4)
    res["causal_copilot"] = {}
    systems = {ag: A["name_reliance_real_minus_swapped"] for ag, A in res["agents"].items()}
    for name, folder, counts in CC_SYSTEMS:
        c = cc_system(Path(a.cc_root) / folder / "partial_stages.json")
        if c:
            c["counted_in_P9"] = counts
            res["causal_copilot"][name] = c
            if counts:
                systems[name] = c["name_reliance_real_minus_swapped"]
    entered = {k: v for k, v in systems.items() if v["paired_scenarios"] >= MIN_PAIRS_P9}
    losers = sorted(k for k, v in entered.items() if (v["mean"] or 0) >= 0.10)
    res["P9"] = {"systems_entered": sorted(entered), "systems_not_entered": sorted(set(systems) - set(entered)),
                 "losing_ge_0.10": losers, "min_paired_scenarios": MIN_PAIRS_P9,
                 "verdict": "supported" if len(losers) >= 3 else ("refuted" if not losers else "inconclusive")}
    below = [ag for ag, A in res["agents"].items() if "data_only_floor_real_arm" in A and
             A["data_only_floor_real_arm"]["dv1_precision_final"] < A["data_only_floor_real_arm"]["dv1_precision_data_only"]]
    have = [ag for ag, A in res["agents"].items() if "data_only_floor_real_arm" in A]
    res["P10"] = {"agents_with_data_only_mode": have, "below_own_data_only": below,
                  "verdict": None if not have else ("supported" if below else "refuted")}
    if a.stub:
        res["warning"] = "STUB answers: the graphs carry no meaning; this checks the pipeline only"
    os.makedirs(a.out, exist_ok=True)
    json.dump({**res, "rows": rows}, open(os.path.join(a.out, "ab06_STUB.json" if a.stub else "ab06.json"), "w"), indent=1)
    json.dump({"producer": "analysis/ab06_score.py", "score_bearing": not a.stub, "tickets": res["tickets"], "regime": "per-row",
               "regime_detail": "D+K: agents read names (real/neutral/swapped) and, where they take it, data",
               "split": "dev", "controls": {"columns_shuffled": "always (seed 20261010)", "names": "per-row", "supplier": "per-row",
                                            "knowledge_source": "each agent's LLM (models in plans/ab06/BUDGET.json)"},
               "orientation_rule": "undecided pairs at random (per-file seed), as the runner scores",
               "metric_defs": {"f1_mean": "mean directed F1 over ok runs", "dv1_precision": "DV-1 committed-claim precision (released targets)",
                               "name_reliance_real_minus_swapped": "paired mean F1(real) - F1(swapped)"}},
              open(os.path.join(a.out, "CONTRACT.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "agents"}, indent=1))
    for ag, A in res["agents"].items():
        print(ag, {arm: (A[arm]["ok"], A[arm]["f1_mean"], A[arm]["dv1_precision"]) for arm in ("real", "neutral", "swapped")},
              A["name_reliance_real_minus_swapped"], A.get("data_only_floor_real_arm"))


if __name__ == "__main__":
    main()
