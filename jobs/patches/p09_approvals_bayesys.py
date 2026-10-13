"""2026-10-13: Uzair approved Atlas v2 (DEC-06; docs/decisions/2026-10-13_atlas_v2_approved.md) and stated reliability
before features for the wedge; the Bayesys reproduction gate passed (AUD-34 done). Refuses to run twice."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p08" in c, "apply p08 first"
assert "# ---- overrides p09" not in c, "already applied"
block = r'''
# ---- overrides p09 (2026-10-13): Atlas v2 approved; reliability first; Bayesys reproduced
_P09 = {
    "DEC-06": dict(status="done", evidence=["analysis/reports/site_flow_design.md", "docs/decisions/2026-10-13_atlas_v2_approved.md"],
                   checks=[G("docs/decisions/2026-10-13_atlas_v2_approved.md", r"I also approve of the site structure")],
                   note="Approved 13 Oct: 4 acts / 13 pages on the existing GitHub Pages site; Home leads with the research and links the "
                        "market/wedge; market page public."),
    "TEAM-08": dict(status="in_progress", blocked_by=None,
                    note="Approved 13 Oct (DEC-06). Built on the existing Pages site in bundles S1-S5."),
    "DEC-05": dict(note="Bundle AB-16: decide once the evidence is in. Uzair, 13 Oct: auditing is the more valuable product, but reliability "
                        "comes first (ledger invariants, never below data-only, bounded harm, held-out calibration) before any product "
                        "surface. C1 from AB-14 (indirect) plus interviews if any."),
    "AUD-34": dict(status="done", blocked_by=None,
                   evidence=["analysis/reports/ab02_second_scoreboard.md", "analysis/ab02_alarm_order.py", "analysis/results/ab02/alarm_order.json",
                             "analysis/audits/AB02_AB12_data_scouting.md", "analysis/ab02_bayesys.py", "analysis/results/ab02/bayesys.json",
                             "analysis/results/ab02/bayesys_runs.jsonl", "analysis/ab02_bayesys_repro.py",
                             "analysis/results/ab02/bayesys_repro.json", "analysis/results/ab02/bayesys_repro_runs.jsonl"],
                   checks=[J("analysis/results/ab02/bayesys.json", ["P3", "verdict"], "eq", "supported"),
                           J("analysis/results/ab02/bayesys_repro.json", ["gate_by_alpha", "0.05", "cells_reproduced"], "ge", 2),
                           G("analysis/reports/ab02_second_scoreboard.md", r"Gate: passed at alpha 0.05")],
                   note="Bayesys reproduced (16 of 31 PC-Stable/FCI cells at alpha 0.05; PC 10 of 15). P3 supported (3 of 6 networks in "
                        "topological order); P4 inconclusive. Bayesys's half-credit F1 moves at most 0.03 when columns are shuffled, so "
                        "the layout leak needs an index tie-break (CausalArena's forced choice) to pay. Engine channel: causal-learn GES "
                        "on PROPERTY -0.07 to -0.09 on the released order. gCastle not reproduced, no claim."),
    "EXT-01": dict(note="Backed by two benchmarks (AB-01, AB-02): shuffle released columns, or score with a tie-break-invariant rule."),
}
for _i in ITEMS:
    if _i["id"] in _P09:
        _i.update(_P09[_i["id"]])
BUNDLE_STATUS.update({"AB-02": "done"})
BUNDLE_NOTE.update({"AB-02": "Bayesys reproduced (PC 10/15 cells). Layout in 3 of 6 networks, but Bayesys's half-credit score moves <= 0.03 "
                             "when shuffled; CausalArena's forced choice is what rewards the leak."})
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p09 applied")
