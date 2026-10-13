"""Record the 13 Oct live results and the follow-up work in the catalogue: AB-07 (A3) scored, RQ-10..14 answered,
CAP-04 / BLD-04 / TGT-07 unblocked, AB-05 partial, AB-06 plans ready, AB-02 Bayesys, and date-free bundle notes.
Applied as a block of overrides at the end of tracker/catalogue.py (by item id). Idempotent: refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
s = p.read_text(encoding="utf-8")
assert "# ---- overrides p04" not in s, "already applied"
block = r'''
# ---- overrides p04 (2026-10-13): live results and follow-ups; applied by id after the items above are built
_P04 = {
    "AUD-48": dict(status="done", blocked_by=None,
                   evidence=["analysis/a3_make_requests.py", "harness/tiers_runner.py", "analysis/a3_score.py", "plans/a3_prereg.json",
                             "plans/a3_tiers_requests.jsonl", "plans/a3_scenarios.json", "analysis/results/a3/a3.json",
                             "analysis/results/a3/selftest.json", "analysis/a3_orient_only.py", "analysis/results/a3/a3_orient_only.json",
                             "analysis/reports/ab07_knowledge_elicitation.md", "tests/test_tiers_runner.py"],
                   checks=[J("plans/a3_prereg.json", ["requests"], "eq", 900), J("analysis/results/a3/a3.json", ["requests_answered"], "eq", 900),
                           J("analysis/results/a3/a3.json", ["verdicts", "O4", "verdict"], "eq", "refuted"),
                           G("analysis/reports/ab07_knowledge_elicitation.md", r"Pre-registered verdicts")],
                   note="Live 13 Oct (gpt-4o-2024-08-06, 914 calls, about $2.08). O1 inconclusive (69.4% correct, 12.1% contradicted), "
                        "O2 supported, O3 supported by data, O4 refuted (0.448), O5 refuted (0.384). Orient-only use of the tiers "
                        "(exploratory): GES 0.528 -> 0.546 semantic."),
    "RQ-10": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json", "analysis/reports/ab07_knowledge_elicitation.md"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O1", "verdict"], "eq", "inconclusive")],
                  note="Answered 13 Oct: no, narrowly: 69.4% of true edges ordered correctly, 12.1% contradicted (semantic, consensus tiers)."),
    "RQ-11": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O2", "verdict"], "eq", "supported")],
                  note="Answered 13 Oct: yes. With neutral names the model puts every variable in one tier."),
    "RQ-12": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O3", "by_data", "verdict"], "eq", "supported")],
                  note="Answered 13 Oct: yes. Moved names: ordering follows the labels (72% correct by label) and is worse than chance by data."),
    "RQ-13": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O4", "verdict"], "eq", "refuted")],
                  note="Answered 13 Oct: no. Regression on the model's tiers 0.448 (oracle depth 0.714)."),
    "RQ-14": dict(status="done", blocked_by=None, evidence=["analysis/results/a3/a3.json"],
                  checks=[J("analysis/results/a3/a3.json", ["verdicts", "O5", "verdict"], "eq", "refuted")],
                  note="Answered 13 Oct: no. 0.384 on formula (oracle depth 0.615)."),
    "CAP-04": dict(status="todo", blocked_by=None, note="Unblocked 13 Oct by AUD-48: orient-only tiers lift GES 0.528 -> 0.546 (exploratory); wrong tiers cost 0.19, bounded."),
    "BLD-04": dict(status="todo", blocked_by=None, note="Unblocked 13 Oct by AUD-48 (model tiers measured)."),
    "TGT-07": dict(status="todo", blocked_by=None, note="Unblocked 13 Oct by AUD-48."),
    "AUD-37": dict(note="Live 13 Oct: causaliq ok (1 call, $0.004, F1 0.231); Causal-Copilot on gpt-4o-mini crashed at judge_functions.py:562 "
                        "(the upstream key bug that also killed 15 of 114 gpt-4o runs). Remaining: PyWhy-LLM, MATMCD, Vashishtha.",
                   evidence=["harness/agent_probe.py", "harness/probe_llm.py", "harness/probe_io.py", "harness/agents/registry.json",
                             "docker/Dockerfile.probes", "plans/ab05_probe_causaliq.json", "plans/ab05_probe_pywhyllm.json",
                             "plans/ab05_probe_matmcd.json", "plans/ab05_probe_vashishtha.json", "plans/ab05_cc_gpt4omini.json",
                             "analysis/reports/ab05_probe_prep.md", "analysis/reports/ab05_probe_results.md", "tests/test_agent_probe.py"],
                   blocked_by="Uzair: three remaining live probes"),
    "AUD-38": dict(status="blocked", blocked_by="Uzair: live batch (plans/ab06, estimate about $58) and the Causal-Copilot arm (about $1)",
                   evidence=["plans/make_ab06_plans.py", "plans/ab06/BUDGET.json", "harness/agent_batch.py", "analysis/ab06_score.py",
                             "plans/ab06_cc_gpt4omini_s2.json"],
                   checks=[J("plans/ab06/BUDGET.json", ["total", "runs"], "eq", 120)],
                   note="Plans, batch runner (resumable, total cap) and scorer ready; the full grid ran end to end with the stub model."),
    "DEC-05": dict(note="Bundle AB-16: decide once the evidence is in (no date pressure)."),
    "AUD-47": dict(note="Bundle AB-17: after AB-16."),
}
for _i in ITEMS:
    if _i["id"] in _P04:
        _i.update(_P04[_i["id"]])
BUNDLE_STATUS.update({"AB-07": "done", "AB-06": "blocked"})
BUNDLE_NOTE.update({"AB-07": "Model orders 69% of true edges from names (12% contradicted); follows moved labels; tiers alone 0.448.",
                    "AB-05": "causaliq live ok; Causal-Copilot gpt-4o-mini hit the upstream key crash; 3 probes to run.",
                    "AB-06": "120-run agent grid and the Causal-Copilot arm are ready; waits on your live runs.",
                    "AB-16": "Decide once the evidence is in.", "AB-17": "After AB-16."})
'''
p.write_text(s.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p04 applied")
