"""Amend plans/q2_dag.json after the Q2 build pass (2026-10-15): approval recorded, output paths set to where things were
built, proposed tickets issued and moved into the closing bundles, B3 no longer LIVE (recorded AB-07 replies replayed).
Changes no gate (gates are those of plans/q2_build_prereg.json and plans/b<k>_prereg.json). Refuses to run twice."""
import json
from pathlib import Path

p = Path(__file__).resolve().parent / "q2_dag.json"
d = json.load(open(p, encoding="utf-8"))
assert not d["amendments"], "already amended"
d["version"] = 2
d["status"] = "approved by Uzair 2026-10-15 (docs/decisions/2026-10-15_q2_dag_approved.md); B0-B5 built and read held-out 2026-10-15"
d["amendments"] = [{
    "date": "2026-10-15",
    "what": ["outputs: paths where each bundle was built (engines/, score/, supplier/, kernel/, ledger/schema02.py, ledger/verify02.py, "
             "calibration/, audit/, analysis/results/q2_b<k>/, analysis/reports/q2_b<k>_*.md)",
             "proposed tickets issued: TGT-18 (B4), TGT-19 (B3; route A measured in B1), TGT-20 and BLD-15 (B5); EXT-07 (causal-learn note) "
             "issued as an outside decision for Uzair",
             "B3: knowledge from AB-07's recorded gpt-4o replies replayed through the supplier contract (plans/b3_prereg.json); no live "
             "run was needed. A live rerun stays optional: it would add finish_reason (truncation) and a second date"],
    "why": "record what was built; no gate, threshold or split changed"}]
OUT = {"B0": ["engines/", "score/", "supplier/", "tests/test_q2_*.py", "analysis/results/q2_b0/", "analysis/reports/q2_b0_engines_guards.md"],
       "B1": ["kernel/", "ledger/schema02.py", "ledger/verify02.py", "plans/b1_prereg.json", "plans/b1_prereg_amendment_1.json",
              "plans/b1_freeze.json", "analysis/results/q2_b1/", "analysis/reports/q2_b1_data_only_ledger.md"],
       "B2": ["kernel/interventions.py", "kernel/run_b2.py", "plans/b2_prereg.json", "plans/b2_freeze.json", "analysis/results/q2_b2/",
              "analysis/reports/q2_b2_interventions.md"],
       "B3": ["kernel/knowledge.py", "kernel/run_b3.py", "supplier/tiers.py", "plans/b3_prereg.json", "plans/b3_freeze.json",
              "analysis/results/q2_b3/", "analysis/reports/q2_b3_knowledge_tiers.md"],
       "B4": ["kernel/confidence.py", "kernel/run_b4.py", "calibration/", "plans/b4_prereg.json", "plans/b4_freeze.json",
              "analysis/results/q2_b4/", "analysis/reports/q2_b4_confidence.md"],
       "B5": ["audit/", "plans/b5_prereg.json", "plans/b5_freeze.json", "analysis/results/q2_b5/", "analysis/reports/q2_b5_audit_adapter_rca.md"]}
ADD = {"B3": ["TGT-19"], "B4": ["TGT-18"], "B5": ["BLD-15", "TGT-20"]}
for b in d["bundles"]:
    b["outputs"] = OUT[b["id"]]
    b["closes"] = b["closes"] + ADD.get(b["id"], [])
    b["proposed_tickets"] = []
    if b["id"] == "B0":
        b["uzair_actions"] = []
    if b["id"] == "B3":
        b["title"] = "Knowledge as tiers"
        b["llm_cost"] = "none"
        b["approval_needed"] = False
        b["runner"] = "claude"
        b["uzair_actions"] = []
d["issued_tickets"] = {"TGT-18": "B4", "TGT-19": "B3", "TGT-20": "B5", "BLD-15": "B5", "EXT-07": "outside (decision for Uzair)"}
d["proposed_tickets"] = []
d["scope"]["build"] = sorted(set(d["scope"]["build"]) | {"TGT-18", "TGT-19", "TGT-20", "BLD-15"})
d["scope"]["outside_bundles"] = sorted(set(d["scope"]["outside_bundles"]) | {"EXT-07"})
json.dump(d, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("q2_dag.json amended (version 2)")
