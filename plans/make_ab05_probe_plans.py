"""Write plans/ab05_probe_<agent>.json (AB-05, AUD-37) from the stub-run summaries.

    python plans/make_ab05_probe_plans.py --stub-runs runs/ab05/stub

Rule (from the AB-05 brief): max_calls = ceil(1.5 x stub-measured calls); max_usd = 1.5 x stub-estimated cost at the
prices of the models the plan uses, rounded UP to the cent - and never below the stub cost plus the gate's worst-case
projection for one more call (the gate refuses a call whose prompt plus max_tokens could cross max_usd), so a plan that
would block its own last call is raised to the smallest cent that does not. Sum of the four max_usd must be <= $4.00.
Stub token counts are local counts and completion lengths are ASSUMED (see the report): all costs are ESTIMATES.
"""
import argparse
import json
import math
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
SCENARIO = "semantic_cybersecurity_and_it_operations_api_rate_limit_abuse_spillover__semantic_obs_only__rep000.npz"
CA = "/research/external/causalarena/scm/semantic/data/semantic_obs_only/"
SEED = 20261010
GPT4O = (2.50, 10.00)
MINI = (0.15, 0.60)

# per agent: stub-run folder (under --stub-runs), model, adapter options, worst single next call (USD) for the gate
CONFIG = {
    "causaliq": {"stub": "causaliq/semantic", "model": "gpt-4o", "agent_opts": {},
                 "worst_call": 470 / 1e6 * GPT4O[0] + 2000 / 1e6 * GPT4O[1],
                 "deviation": None},
    "pywhyllm": {"stub": "pywhyllm/semantic", "model": "gpt-4o", "agent_opts": {},
                 "worst_call": 400 / 1e6 * GPT4O[0] + 600 / 1e6 * GPT4O[1],
                 "deviation": None},
    "matmcd": {"stub": "matmcd_mini/semantic", "model": "gpt-4o-mini", "agent_opts": {},
               "worst_call": 1200 / 1e6 * MINI[0] + 600 / 1e6 * MINI[1],
               "deviation": "gpt-4o-mini, the repository's own configured model (config.py: MODEL = \"gpt-4o-mini\"), "
                            "not gpt-4o: 2 x d(d-1) = 1,200 calls at gpt-4o are estimated at $4.53 (x1.5 = $6.80), "
                            "above the whole $4 AB-05 budget on their own"},
    "vashishtha": {"stub": "vashishtha_mini/semantic", "model": "gpt-4o", "agent_opts": {"subgraph_model": "gpt-4o-mini"},
                   "worst_call": 5200 / 1e6 * GPT4O[0] + 400 / 1e6 * GPT4O[1],
                   "deviation": "the repository's documented two-model split (README: --subgraph-model gpt-4o-mini "
                                "--expert-model gpt-4o): the C(d,3) = 2,300 triplet calls use gpt-4o-mini and only the "
                                "tie-breaker calls use gpt-4o; all-gpt-4o is estimated at $7.35 (x1.5 = $11.03)"},
}


def ceil_cent(x):
    return math.ceil(round(x * 100, 6)) / 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stub-runs", default=str(KIT / "runs" / "ab05" / "stub"))
    a = ap.parse_args()
    total = 0.0
    plans = {}
    for agent, c in CONFIG.items():
        s = json.loads((Path(a.stub_runs) / c["stub"] / "summary.json").read_text())
        assert s["status"] == "ok" and s["mode"] == "stub" and s["scenario"] == SCENARIO, (agent, s["status"])
        est = s["est_usd_at_served_prices"]
        max_calls = math.ceil(1.5 * s["calls"])
        usd_rule = ceil_cent(1.5 * est)
        usd_floor = ceil_cent(est + c["worst_call"])
        max_usd = max(usd_rule, usd_floor)
        total += max_usd
        reg = json.loads((KIT / "harness" / "agents" / "registry.json").read_text())[agent]
        plan = {
            "ticket": "AUD-37", "bundle": "AB-05", "agent": agent, "status": "PROPOSED - not run; live spend needs Uzair's approval",
            "run": {"scenario": CA + SCENARIO, "shuffle_seed": SEED, "model": c["model"], "agent_opts": c["agent_opts"],
                    "max_calls": max_calls, "max_usd": max_usd,
                    "out": "/research/runs/ab05/%s/" % agent, "out_stub": "/research/runs/ab05/stub_plan/%s/" % agent},
            "basis": {"stub_summary": "runs/ab05/stub/%s/summary.json" % c["stub"], "stub_calls": s["calls"],
                      "stub_prompt_tokens": s["prompt_tokens"], "stub_completion_tokens": s["completion_tokens"],
                      "token_counter": s["token_counter"],
                      "est_usd_at_plan_prices": round(est, 4), "est_usd_if_all_gpt4o": round(s["est_usd_gpt4o_list"], 4),
                      "max_usd_by_1_5x_rule": usd_rule, "max_usd_floor_for_last_call": usd_floor,
                      "note": "ESTIMATE: prompt tokens counted locally (%s); completion lengths assumed (adapter "
                              "constants, recorded per call in calls.jsonl)" % s["token_counter"]},
            "deviation_from_brief_model": c["deviation"],
            "agent_repo": {"url": reg["url"], "commit": reg["commit"], "licence": reg["licence"]},
            "launch": "python /research/harness/agent_probe.py --plan /research/plans/ab05_probe_%s.json [--stub]" % agent,
        }
        plans[agent] = plan
    assert total <= 4.0 + 1e-9, total
    for agent, plan in plans.items():
        plan["budget_check"] = {"sum_max_usd_all_four": round(total, 2), "limit": 4.00}
        (KIT / "plans" / ("ab05_probe_%s.json" % agent)).write_text(json.dumps(plan, indent=1) + "\n", encoding="utf-8")
        print(agent, plan["run"]["model"], plan["run"]["max_calls"], plan["run"]["max_usd"])
    print("sum of max_usd: %.2f (limit 4.00)" % total)


if __name__ == "__main__":
    main()
