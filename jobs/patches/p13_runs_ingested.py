"""2026-10-14, after Uzair's runs of 14 Oct (terminal logs lost to a restart; state read from the files): AB-05 probes resumed
and finished; the q042 Causal-Copilot rerun scored (M2 4/10, M4 9/10); BND-11 done (v2 data part held-out R1-R3 supported,
names R4/R5 supported, R6 refuted); AB-06 tier A partly run and amended (amendment 1). Refuses to run twice."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p12" in c, "apply p12 first"
assert "# ---- overrides p13" not in c, "already applied"
block = r'''
# ---- overrides p13 (2026-10-14): runs of 14 Oct ingested; AB-06 amendment 1
_P13 = {
    "AUD-37": dict(note="P8 supported, all five systems end to end: causaliq, PyWhy-LLM (F1 0.329), Causal-Copilot on gpt-4o-mini, and "
                        "MATMCD and Vashishtha after resuming on 14 Oct (replayed paid answers; +$0.009 and +$0.651). On the probe scenario "
                        "both hybrids end exactly at their own data-only PC graph (F1 0.407). Vashishtha loses 91% of triplet votes to its "
                        "300-token limit (EXT-06). Spent $3.79 of $5."),
    "AUD-38": dict(evidence=["plans/make_ab06_plans.py", "plans/calibrate_ab06.py", "plans/ab06/BUDGET.json", "plans/ab06/TIERS.json",
                             "plans/ab06_prereg.json", "manifests/evidence/ab06_prereg_2026-10-14.sha256", "plans/ab06_prereg_amendment_1.json",
                             "manifests/evidence/ab06_prereg_amendment1_2026-10-14.sha256", "harness/agent_batch.py", "analysis/ab06_score.py",
                             "plans/ab06_cc_gpt4omini_s2.json", "plans/ab06_cc_gpt4omini_s2_q042.json", "analysis/reports/ab06_prep.md",
                             "analysis/reports/ab06_cc_second_model.md", "analysis/results/ab06_cc/s2_verdicts.json",
                             "analysis/results/ab06_cc/partial_stages.json", "tests/test_ab06_batch.py", "tests/test_probe_gate.py"],
                   checks=[{"t": "manifest", "path": "manifests/evidence/ab06_prereg_amendment1_2026-10-14.sha256"},
                           J("plans/ab06/BUDGET.json", ["total", "runs"], "eq", 120),
                           J("plans/ab06/TIERS.json", ["cost", "A", "runs"], "eq", 80),
                           J("analysis/results/ab06_cc/s2_verdicts.json", ["M4", "verdict"], "eq", "SUPPORTED")],
                   blocked_by="Uzair: resume AB-06 tier A (80 runs, about $48 in all, $7.92 spent; workers=4)",
                   note="Causal-Copilot part complete (q042 rerun 14 Oct): gpt-4o-mini name reliance 0.094 (gpt-4o 0.167), M2 refuted 4/10, M3 "
                        "inconclusive, M4 supported 9/10. Tier A started 14 Oct; a machine restart stopped it after 14 attempts (12 ok, 2 "
                        "Vashishtha cap hits; 4 runs cut short). Amendment 1: Vashishtha ties 85-93% of pairs on 17 variables (each a gpt-4o "
                        "call), so its tier-A runs are cut to the first five scenarios (tier A 80 runs, $48); cap hits resume without a flag; "
                        "spend is read from the call logs. P9/P10 and the scorer unchanged."),
    "RQ-17": dict(status="done", note="Causal-Copilot on gpt-4o-mini (10 families x 3 arms): the structure holds (M4 supported 9/10, M2 refuted on "
                                      "both models, the same bootstrap loss); name reliance is smaller (0.094 vs 0.167), and the model review lowers "
                                      "directed F1 even with real names (0.233 -> 0.208)."),
    "BND-11": dict(status="done",
                   evidence=["analysis/refinement_v2.py", "analysis/results/refinement_v2/RULE.json", "analysis/results/refinement_v2/dev.json",
                             "analysis/results/refinement_v2/test_formula.json", "analysis/results/refinement_v2/names_s2.json",
                             "analysis/results/refinement_v2/access_log.jsonl", "plans/bnd11_names_requests.jsonl",
                             "plans/results/bnd11_names_requests.answers.jsonl", "harness/names_runner.py", "analysis/bnd11_lenient_parse.py",
                             "analysis/results/refinement_v2/names_s2_exploratory_lenient.json", "analysis/reports/bnd11_prep.md",
                             "analysis/reports/bnd11_results.md", "manifests/evidence/bnd11_prereg_2026-10-12.sha256"],
                   checks=[{"t": "manifest", "path": "manifests/evidence/bnd11_prereg_2026-10-12.sha256"},
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "R1", "verdict"], "eq", "SUPPORTED"),
                           J("analysis/results/refinement_v2/names_s2.json", ["R4", "verdict"], "eq", "SUPPORTED"),
                           J("analysis/results/refinement_v2/names_s2.json", ["R6", "verdict"], "eq", "REFUTED")],
                   note="14 Oct. Data part v2d on the held-out formula test replay: R1 22/22, R2 22/22, R3 +0.010, all supported. Names only "
                        "where the data are silent: R4 (neutral adds nothing) and R5 (swapped harmless) supported; R6 (real names help in "
                        ">= 8/10) refuted, 1/10. gpt-4o fenced 1,036 of 1,571 replies, so the strict contract abstained on 251 of 786 "
                        "questions; an exploratory lenient re-read gives R6 5/10, still refuted. $0.47."),
    "BLD-06": dict(status="done",
                   evidence=["analysis/refinement_v1.py", "analysis/refinement_v2.py", "analysis/results/refinement_v2/RULE.json",
                             "analysis/results/refinement_v2/dev.json", "analysis/results/refinement_v2/test_formula.json",
                             "analysis/results/refinement_v2/names_s2.json", "analysis/reports/bnd11_prep.md", "analysis/reports/bnd11_results.md"],
                   checks=[J("analysis/results/refinement_v2/dev.json", ["summary", "all_edges_sourced"], "true"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "all_edges_sourced"], "true"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "R2", "verdict"], "eq", "SUPPORTED")],
                   note="v2 is the drop-in replacement: it never falls below the algorithm on held-out data (formula test 22/22) and "
                        "sources every edge; names add little (R6 refuted) and wrong names cost nothing measurable (R5)."),
    "CAP-10": dict(status="done", evidence=["harness/names_runner.py", "analysis/refinement_v2.py", "tests/test_refinement_v2.py",
                                            "analysis/reports/bnd11_prep.md", "analysis/reports/bnd11_results.md",
                                            "plans/results/bnd11_names_requests.answers.jsonl"],
                   note="0 crashes in 1,571 live calls (BND-11): every malformed reply was retried once or abstained. Lesson for approach v1 "
                        "G7: the strict contract turned gpt-4o's code fences into 251 abstentions; a contract must declare its accepted "
                        "normalisations and count them."),
    "TGT-13": dict(status="done", evidence=["harness/names_runner.py", "tests/test_refinement_v2.py", "analysis/reports/bnd11_results.md",
                                            "plans/results/bnd11_names_requests.answers.jsonl"],
                   note="Zero crashes over the BND-11 live run (786 questions, 1,571 calls)."),
    "TGT-09": dict(note="v1 inconclusive (BND-10). v2's data part meets the rule on the held-out formula test replay: adjacency F1 >= the "
                        "algorithm's - 0.02 in 22 of 22 files (bnd11_results.md)."),
}
for _i in ITEMS:
    if _i["id"] in _P13:
        _i.update(_P13[_i["id"]])
BUNDLE_NOTE.update({"AB-05": "P8 supported: all five systems end to end (MATMCD and Vashishtha after resuming). Vashishtha loses 91% of its "
                             "votes to its own token limit.",
                    "AB-06": "Causal-Copilot arm complete (gpt-4o-mini 0.094 vs gpt-4o 0.167; M4 9/10). Tier A amended to 80 runs (~$48), "
                             "14 attempted before a restart; resumes from the call logs."})
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p13 applied")
