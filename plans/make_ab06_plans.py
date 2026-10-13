"""Write the AB-06 field-audit plans (AUD-38): 4 agents x 10 semantic dev scenarios x 3 name arms = 120 runs.

    python plans/make_ab06_plans.py [--pywhyllm-model gpt-4o|gpt-4o-mini]

Scenarios: the first 10 semantic dev scenarios of plans/splits.json (rep000 file), the same set the AB-05 stub runs used.
Arms (names shown to the agent; columns always shuffled with seed 20261010, as in AB-05):
  real     the scenario's own names
  neutral  V01..Vd, numbered by a random shown position (plans/a3_scenarios.json, the A3 labels: no order leak)
  swapped  the real names moved among the variables (the A3 "moved" derangement: variable i shows the name of sigma(i))
Every arm gets the same domain context text (the runner's default, the scenario's domain). Jitter 1e-6 for every run
(matmcd and vashishtha fail at PC on one scenario without it; applied to all agents so arms and agents stay comparable).
Per-run caps: max_calls = ceil(1.5 x calls of that agent's AB-05 stub run on that scenario) (the largest stub run of the
agent where the stub failed); max_usd = 1.5 x that stub's estimated cost, rounded up to the cent, floor $0.05.
Writes plans/ab06/<agent>__<scenario>__<arm>.json, plans/ab06/names/<scenario>__<arm>.json and plans/ab06/BUDGET.json.
"""
import argparse, glob, json, math, os
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
CA = "/research/external/causalarena/scm/semantic/data/semantic_obs_only/"
AGENTS = {"causaliq": ("gpt-4o", {}), "pywhyllm": ("gpt-4o", {}), "matmcd": ("gpt-4o-mini", {}),
          "vashishtha": ("gpt-4o", {"subgraph_model": "gpt-4o-mini"})}
MINI_RATIO = 0.15 / 2.50


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pywhyllm-model", default="gpt-4o")
    a = ap.parse_args()
    if a.pywhyllm_model != "gpt-4o":
        AGENTS["pywhyllm"] = (a.pywhyllm_model, {})
    S = json.load(open(KIT / "plans" / "a3_scenarios.json", encoding="utf-8"))
    splits = json.load(open(KIT / "plans" / "splits.json", encoding="utf-8"))["families"]["semantic"]["dev"][:10]
    scen = {}
    for k, v in S.items():
        if v["family"] == "semantic" and any(sl in v["file_rep000"] for sl in splits):
            scen[v["scenario"]] = v
    assert len(scen) == 10, len(scen)
    out = KIT / "plans" / "ab06"
    (out / "names").mkdir(parents=True, exist_ok=True)
    budget, n = {}, 0
    for sname, v in sorted(scen.items()):
        real = v["labels"]["real"]
        for arm, lab in (("neutral", v["labels"]["neutral"]), ("swapped", v["labels"]["moved"])):
            json.dump({real[i]: lab[i] for i in range(v["d"])}, open(out / "names" / ("%s__%s.json" % (sname, arm)), "w"), indent=1)
        for agent, (model, opts) in AGENTS.items():
            stub = glob.glob(str(KIT / "runs" / "ab05" / "stub_dev" / agent / ("%s" % sname) / "summary.json"))
            st = json.load(open(stub[0])) if stub else None
            if not st or st["status"] != "ok":
                allst = [json.load(open(f)) for f in glob.glob(str(KIT / "runs" / "ab05" / "stub_dev" / agent / "*" / "summary.json"))]
                st = max((x for x in allst if x["status"] == "ok"), key=lambda x: x["calls"])
            est = st["est_usd_at_served_prices"] * (MINI_RATIO if (agent == "pywhyllm" and model == "gpt-4o-mini") else 1.0)
            for arm in ("real", "neutral", "swapped"):
                plan = {"ticket": "AUD-38", "bundle": "AB-06", "agent": agent, "arm": arm, "scenario_id": sname,
                        "run": {"scenario": CA + v["file_rep000"], "shuffle_seed": 20261010, "model": model, "agent_opts": opts,
                                "jitter": 1e-6, "names_map": None if arm == "real" else "/research/plans/ab06/names/%s__%s.json" % (sname, arm),
                                "max_calls": math.ceil(1.5 * st["calls"]), "max_usd": max(0.05, math.ceil(150 * est) / 100),
                                "out": "/research/runs/ab06/%s/%s/%s/" % (agent, sname, arm),
                                "out_stub": "/research/runs/ab06_stub/%s/%s/%s/" % (agent, sname, arm)},
                        "basis": {"stub_calls": st["calls"], "stub_est_usd": round(est, 4), "note": "ESTIMATE from the AB-05 stub run"}}
                json.dump(plan, open(out / ("%s__%s__%s.json" % (agent, sname, arm)), "w"), indent=1)
                budget.setdefault(agent, {"runs": 0, "est_usd": 0.0, "cap_usd": 0.0})
                budget[agent]["runs"] += 1
                budget[agent]["est_usd"] += est
                budget[agent]["cap_usd"] += plan["run"]["max_usd"]
                n += 1
    tot = {"runs": n, "est_usd": round(sum(b["est_usd"] for b in budget.values()), 2), "cap_usd": round(sum(b["cap_usd"] for b in budget.values()), 2)}
    json.dump({"per_agent": {k: {kk: round(vv, 2) if isinstance(vv, float) else vv for kk, vv in b.items()} for k, b in budget.items()},
               "total": tot, "models": {k: v[0] for k, v in AGENTS.items()}, "scenarios": sorted(scen)},
              open(out / "BUDGET.json", "w"), indent=1)
    print(json.dumps(tot), {k: round(b["est_usd"], 2) for k, b in budget.items()})


if __name__ == "__main__":
    main()
