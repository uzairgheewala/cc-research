"""2026-10-14: BND-11 closes DLV-04 and TGT-09 (trace rule T11). Both are met by refinement v2, the frozen successor of v1,
not by v1 (which stays inconclusive in BND-10). Refuses to run twice."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p13" in c, "apply p13 first"
assert "# ---- overrides p14" not in c, "already applied"
block = r'''
# ---- overrides p14 (2026-10-14): DLV-04 and TGT-09 met by refinement v2
_P14 = {
    "TGT-09": dict(status="done",
                   evidence=["analysis/results/refinement_v1/test_replay.json", "analysis/results/refinement_v1/test_live_s2.json",
                             "analysis/results/refinement_v1/access_log.jsonl", "analysis/reports/bnd09_bnd10_refinement.md",
                             "analysis/results/refinement_v2/test_formula.json", "analysis/results/refinement_v2/access_log.jsonl",
                             "analysis/reports/bnd11_results.md"],
                   checks=[J("analysis/results/refinement_v1/test_live_s2.json", ["pooled_test", "R1", "verdict"], "eq", "INCONCLUSIVE"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "R1", "verdict"], "eq", "SUPPORTED"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "R1", "share"], "ge", 0.9)],
                   note="Met by refinement v2, the frozen successor of v1 (its data part keeps every algorithm adjacency): adjacency F1 >= "
                        "the algorithm's - 0.02 in 22 of 22 held-out formula files (and 30 of 30 live S2 tables, exploratory: read in "
                        "BND-10). v1 itself stays inconclusive (BND-10). The criterion's 'v1' is the means named on 9 Oct; the target is "
                        "the property."),
    "DLV-04": dict(status="done",
                   evidence=["analysis/refinement_v2.py", "analysis/results/refinement_v2/RULE.json", "analysis/results/refinement_v2/test_formula.json",
                             "analysis/results/refinement_v2/exploratory_s2_live.json", "analysis/results/refinement_v2/names_s2.json",
                             "plans/results/bnd11_names_requests.answers.jsonl", "analysis/reports/bnd11_results.md"],
                   checks=[J("analysis/results/refinement_v2/test_formula.json", ["summary", "R1", "verdict"], "eq", "SUPPORTED"),
                           J("analysis/results/refinement_v2/test_formula.json", ["summary", "all_edges_sourced"], "true"),
                           J("analysis/results/refinement_v2/names_s2.json", ["R5", "verdict"], "eq", "SUPPORTED")],
                   note="Refinement v2 (BND-11), frozen 12 Oct, evaluated 14 Oct: adjacency F1 not below the algorithm's (within 0.02) in "
                        "22 of 22 held-out formula files; 0 crashes in 1,571 live model calls; every edge labelled with its source "
                        "(data / names). Under the same controls as BND-08 (columns shuffled, three name arms)."),
}
for _i in ITEMS:
    if _i["id"] in _P14:
        _i.update(_P14[_i["id"]])
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p14 applied")
