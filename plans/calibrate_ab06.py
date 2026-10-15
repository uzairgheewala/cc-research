"""AB-06 (AUD-38) plan calibration from the AB-05 LIVE probes: per-run cost, calls and wall time; new per-run caps.

  python plans/calibrate_ab06.py [--write]        (without --write: report only)

Why: the AB-06 plans were capped from stub runs (assumed completion lengths). The live probes of 13 Oct showed the
assumptions were low (analysis/results/ab05/live_calibration.json): MATMCD's domain-knowledge answers average 722 tokens
(stub 400) and its yes/no prompts carry them (prompt x1.61); Vashishtha et al.'s triplet answers hit the repository's
300-token limit in 2,105 of 2,300 calls, so 91% of votes are lost and 38% of pairs go to the gpt-4o tie-breaker (stub:
11%); PyWhy-LLM completions are x1.22; causaliq-knowledge x0.27. Both capped probes stopped on our caps, not on agent
failures.

Model per plan (stub calls of THAT plan: runs/ab06_stub/<agent>/<scenario>/<arm>/calls.jsonl, grouped by call kind):
  calls      stub count; Vashishtha tie-breakers = tie share x C(d, 2) (share 0.377 measured live; caps use 0.55)
  prompt     stub mean x live/stub prompt ratio of that kind
  completion live mean of that kind (absolute: stub completions were padding)
  seconds    live mean of that kind (sequential agent calls; the probe gate serialises a run's calls)
Caps (written with --write): max_usd = cent-ceiling of 1.25 x cap-basis cost + the largest single call's allowance;
max_calls = ceil(1.25 x cap-basis calls). A run that still hits its cap resumes for free (replayed answers) with
--retry-failed after the cap is raised, so caps stay tight.
Writes plans/ab06/BUDGET.json (v2, the old one kept as basis_v1 inside) and updates each plan's run caps and basis.

Amendment 1 (14 Oct, plans/ab06_prereg_amendment_1.json): the tie share is not a constant. With most triplet answers
untagged, a pair's vote count is about (d - 2) x (tagged share), so smaller scenarios tie more: the first two tier-A
Vashishtha runs (17 variables) tied on 85% and 93% of pairs and stopped on their caps. Now: a scenario/arm whose triplets
are complete in runs/ab06 uses its measured tie share (recomputed with the repository's merge rule); every other plan uses
an estimate of 0.85 and caps at 1.0 (every pair to the tie-breaker).
"""
import argparse, collections, json, math, statistics as st, sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KIT / "analysis"))
from ab05_live_calibration import kind, PRICES  # noqa: E402

TIE_EST, TIE_CAP = 0.85, 1.0          # amendment 1; v2 used 0.377 / 0.55 (the AB-05 probe scenario)


def measured_tie_share(out_dir, d):
    """Tie share recomputed from a live run whose C(d, 3) triplet answers are all recorded; None otherwise."""
    from ab05_live_calibration import vashishtha_votes, load
    calls = []
    for f in sorted(Path(out_dir).glob("calls*.jsonl")):
        calls += load(f)
    if not calls:
        return None
    v = vashishtha_votes(calls)
    return v["share_pairs_tied"] if v["triplets"] == d * (d - 1) * (d - 2) // 6 else None
CAP_FACTOR = 1.25


def price(model):
    m = (model or "").replace("stub:", "")
    return PRICES["gpt-4o-mini"] if m.startswith("gpt-4o-mini") else PRICES["gpt-4o"]


def load_calls(p):
    return [r for r in (json.loads(l) for l in open(p, encoding="utf-8") if l.strip()) if "request" in r]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--plans", default=str(KIT / "plans" / "ab06"))
    a = ap.parse_args()
    cal = json.loads((KIT / "analysis" / "results" / "ab05" / "live_calibration.json").read_text(encoding="utf-8"))["agents"]
    plans = sorted(p for p in Path(a.plans).glob("*__*__*.json"))
    rows = []
    for p in plans:
        pl = json.loads(p.read_text(encoding="utf-8"))
        agent = pl["agent"]
        stub_dir = KIT / pl["run"]["out_stub"].replace("/research/", "", 1)
        calls = load_calls(stub_dir / "calls.jsonl")
        d = json.loads((stub_dir / "summary.json").read_text(encoding="utf-8"))["variables"]
        C = cal[agent]
        by = collections.defaultdict(list)
        for r in calls:
            by[kind(agent, r["request"])].append(r)
        est = {"usd": 0.0, "calls": 0.0, "seconds": 0.0}
        capb = {"usd": 0.0, "calls": 0.0}
        biggest = 0.0
        for k, rs in by.items():
            L = C["live"].get(k)
            ratio = (C["ratios"].get(k) or {}).get("prompt_live_over_stub", 1.0)
            if L is None:
                raise SystemExit("no live calibration for %s/%s" % (agent, k))
            n = len(rs)
            n_cap = n
            if agent == "vashishtha" and k == "tiebreak":
                m = measured_tie_share(KIT / pl["run"]["out"].replace("/research/", "", 1), d)
                n, n_cap = (m if m is not None else TIE_EST) * d * (d - 1) / 2, TIE_CAP * d * (d - 1) / 2
            pt = st.mean((r.get("usage") or {}).get("prompt_tokens", 0) for r in rs) * ratio
            ct = L["completion_mean"]
            pi, po = price(rs[0].get("requested_model"))
            one = (pt * pi + ct * po) / 1e6
            allowance = (pt * pi + float(L["max_completion_tokens"][0] if L["max_completion_tokens"][0] not in ("None",) else 1000) * po) / 1e6
            biggest = max(biggest, allowance)
            est["usd"] += n * one
            est["calls"] += n
            est["seconds"] += n * L["seconds_mean"]
            capb["usd"] += n_cap * one
            capb["calls"] += n_cap
        max_usd = math.ceil(100 * (CAP_FACTOR * capb["usd"] + biggest)) / 100
        max_calls = math.ceil(CAP_FACTOR * capb["calls"])
        rows.append({"plan": p.name, "agent": agent, "arm": pl["arm"], "scenario": pl["scenario_id"], "d": d,
                     "est_usd": round(est["usd"], 4), "est_calls": round(est["calls"]), "est_hours": round(est["seconds"] / 3600, 3),
                     "max_usd": max_usd, "max_calls": max_calls, "old_max_usd": pl["run"]["max_usd"], "old_max_calls": pl["run"]["max_calls"]})
        if a.write:
            pl["run"]["max_usd"], pl["run"]["max_calls"] = max_usd, max_calls
            b = pl.setdefault("basis", {})
            b.update({"live_est_usd": round(est["usd"], 4), "live_est_calls": round(est["calls"]), "live_est_hours": round(est["seconds"] / 3600, 3),
                      "calibration": "plans/calibrate_ab06.py from analysis/results/ab05/live_calibration.json (AB-05 live probes, 13 Oct)"})
            p.write_text(json.dumps(pl, indent=1), encoding="utf-8")
    agg = collections.OrderedDict()
    for r in rows:
        g = agg.setdefault(r["agent"], {"runs": 0, "est_usd": 0.0, "cap_usd": 0.0, "est_hours": 0.0, "by_arm_usd": collections.Counter()})
        g["runs"] += 1
        g["est_usd"] += r["est_usd"]
        g["cap_usd"] += r["max_usd"]
        g["est_hours"] += r["est_hours"]
        g["by_arm_usd"][r["arm"]] += r["est_usd"]
    out = {"version": 2, "calibrated": "2026-10-14", "producer": "plans/calibrate_ab06.py",
           "basis": "AB-05 live probes (analysis/results/ab05/live_calibration.json); Vashishtha tie share measured where its triplets are complete, else est %.3f; caps %.2f (amendment 1)" % (TIE_EST, TIE_CAP),
           "per_agent": {k: {"runs": v["runs"], "est_usd": round(v["est_usd"], 2), "cap_usd": round(v["cap_usd"], 2),
                             "est_hours_sequential": round(v["est_hours"], 1), "est_usd_by_arm": {a_: round(x, 2) for a_, x in v["by_arm_usd"].items()}}
                         for k, v in agg.items()},
           "total": {"runs": len(rows), "est_usd": round(sum(r["est_usd"] for r in rows), 2), "cap_usd": round(sum(r["max_usd"] for r in rows), 2),
                     "est_hours_sequential": round(sum(r["est_hours"] for r in rows), 1)},
           "rows": rows}
    old = KIT / "plans" / "ab06" / "BUDGET.json"
    if old.exists():
        prev = json.loads(old.read_text(encoding="utf-8"))
        out["basis_v1"] = prev.get("basis_v1") or {k: prev[k] for k in ("per_agent", "total") if k in prev}
        out["models"], out["scenarios"] = prev.get("models"), prev.get("scenarios")
    if a.write:
        old.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("per_agent", "total")}, indent=1))


if __name__ == "__main__":
    main()
