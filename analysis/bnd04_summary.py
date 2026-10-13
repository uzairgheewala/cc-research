"""BND-04: combine the per-method budgets into the Q4a / Q4b verdicts (RQ-16) and the published-row comparison.

  python analysis/bnd04_summary.py      # writes analysis/results/methods/bnd04_verdicts.json

Q4a (plan text, fixed before the runs): committed-direction accuracy <= 0.65 for both GES and FCI -> supported;
>= 0.75 for either -> refuted. Q4b: direction errors cost each method >= 0.15 F1 -> supported; <= 0.05 for any -> refuted.
PC's budget (error_budget.json, pc_semantic_n1000) is shown alongside for reference.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "analysis" / "results" / "methods"


def main():
    ges = json.loads((M / "error_budget_gesbic.json").read_text(encoding="utf-8"))
    fci = json.loads((M / "error_budget_fci.json").read_text(encoding="utf-8"))
    gx = json.loads((M / "error_budget_gesbic_excl_failed.json").read_text(encoding="utf-8"))
    pc = json.loads((ROOT / "analysis" / "results" / "error_budget" / "error_budget.json").read_text(encoding="utf-8"))["pc_semantic_n1000"]
    acc = {"gesbic": ges["accuracy_of_committed_directions"], "fci": fci["accuracy_of_committed_directions"]}
    cost = {"gesbic": ges["cost_of_direction_errors_f1"], "fci": fci["cost_of_direction_errors_f1"]}
    q4a = "SUPPORTED" if all(v <= 0.65 for v in acc.values()) else "REFUTED" if any(v >= 0.75 for v in acc.values()) else "INCONCLUSIVE"
    q4b = "SUPPORTED" if all(v >= 0.15 for v in cost.values()) else "REFUTED" if any(v <= 0.05 for v in cost.values()) else "INCONCLUSIVE"
    out = {"Q4a": {"text": ges["predictions"]["Q4a"]["text"], "accuracy_of_committed_directions": acc, "verdict": q4a},
           "Q4b": {"text": ges["predictions"]["Q4b"]["text"], "cost_of_direction_errors_f1": cost, "verdict": q4b},
           "pc_reference": {"accuracy_of_committed_directions": pc["accuracy_of_committed_directions"],
                            "cost_of_direction_errors_f1": round(pc["pc_skeleton_with_perfect_orientation_f1"] - pc["pc_as_scored_f1"], 4)},
           "ges_vs_published_GIES": {"all_50": ges["vs_published"], "excluding_failed_scenarios_post_hoc": gx["vs_published"],
                                      "failed_files": ges["failed_files"], "scenarios_with_failures": ges["scenarios_with_failures"],
                                      "tolerance_3se_all_50": ges["tolerance_3se"], "tolerance_3se_45": gx["tolerance_3se"]},
           "order_leak_under_authors_rule": {m: {"f1_random": b["family_means"]["f1_random"], "f1_lower": b["family_means"]["f1_lower"],
                                                 "share_of_found_true_adjacencies_left_undecided": b["of_true_adjacencies_found"]["undec"]}
                                             for m, b in (("gesbic", ges), ("fci", fci))},
           "gates": {"C1": ges["gates"]["C1_pc_scorer_reproduces_published_F1"] and fci["gates"]["C1_pc_scorer_reproduces_published_F1"],
                     "split_labelled": ges["gates"]["split_labelled"] and fci["gates"]["split_labelled"],
                     "files_250_each": ges["files"] == 250 and fci["files"] == 250}}
    (M / "bnd04_verdicts.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
