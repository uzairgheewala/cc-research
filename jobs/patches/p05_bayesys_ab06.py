"""Record AB-02's Bayesys re-score (AUD-34: P3 supported, P4 mixed, reproduction gate open) and AB-06's batch and test
additions (AUD-38). Applied as a block of overrides at the end of tracker/catalogue.py, after p04. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
s = p.read_text(encoding="utf-8")
assert "# ---- overrides p04" in s, "apply p04 first"
assert "# ---- overrides p05" not in s, "already applied"
block = r'''
# ---- overrides p05 (2026-10-13): AB-02 Bayesys measured; AB-06 batch safety and tests
_P05 = {
    "AUD-34": dict(status="blocked", blocked_by="Uzair: results_noisyPaper.xlsx into external/bayesys (reproduction gate)",
                   evidence=["analysis/reports/ab02_second_scoreboard.md", "analysis/ab02_alarm_order.py", "analysis/results/ab02/alarm_order.json",
                             "analysis/audits/AB02_AB12_data_scouting.md", "analysis/ab02_bayesys.py", "analysis/results/ab02/bayesys.json",
                             "analysis/results/ab02/bayesys_runs.jsonl"],
                   checks=[J("analysis/results/ab02/bayesys.json", ["P3", "verdict"], "eq", "supported"),
                           G("analysis/reports/ab02_second_scoreboard.md", r"reproduction gate")],
                   note="Bayesys measured 13 Oct (6 networks, released vs 5 shuffled orders, PC/maxP/FCI/GES): ASIA, SPORTS, PATHFINDER "
                        "are released in topological order (P3 supported); an index tie-break gains +0.04 to +0.30 there and about 0 on "
                        "ALARM/PROPERTY. P4 inconclusive (conflict-rule gap on 2 of 3 ordered networks). No claim on the published "
                        "numbers until two cells are reproduced. Sortability not computed (discrete data)."),
    "AUD-38": dict(evidence=["plans/make_ab06_plans.py", "plans/ab06/BUDGET.json", "harness/agent_batch.py", "analysis/ab06_score.py",
                             "plans/ab06_cc_gpt4omini_s2.json", "analysis/reports/ab06_prep.md", "tests/test_ab06_batch.py"],
                   note="Plans, batch runner and scorer ready and stub-tested end to end. The batch never pays twice for a crashed run "
                        "(--retry-failed to override), counts every logged attempt, and stops at the total cap before a run (exit 3)."),
}
for _i in ITEMS:
    if _i["id"] in _P05:
        _i.update(_P05[_i["id"]])
BUNDLE_NOTE.update({"AB-02": "Bayesys: 3 of 6 networks in topological column order (P3 supported); index tie-break worth up to +0.30 there. "
                             "P4 mixed. Reproduction waits on the published xlsx."})
'''
p.write_text(s.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p05 applied")
