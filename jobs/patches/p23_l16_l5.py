"""2026-10-19: L16 (applicability conditions for the link filters) and L5 (interventions as link evidence), pre-registered
and measured on dev (analysis/reports/q2_l16_dev.md, analysis/reports/q2_l5_dev.md). TGT-18 and TGT-19 get the reports,
results and manifest checks; BEN-13 (CausalBench shortcut audit, opened in the Dev list on 19 Oct) enters the catalogue;
CRS-01 moves to 29 Oct (Uzair, 19 Oct). Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p22" in c, "apply p22 first"
assert "# ---- overrides p23" not in c, "already applied"
old = 'item("CRS-01", "CRS", "TA check-in 1 (TA: Nate)", "todo", kind="deadline", due="2026-10-19"),'
assert old in c, "CRS-01 line changed; patch by hand"
c = c.replace(old, 'item("CRS-01", "CRS", "TA check-in 1 (TA: Nate)", "todo", kind="deadline", due="2026-10-29",\n'
                   '     note="Rescheduled: Thursday 29 Oct 2026, 10:45 am PT (Uzair, 19 Oct)."),')
c = c.rstrip("\n") + '''

# ---- overrides p23 (2026-10-19): L16 applicability conditions and L5 interventions as link evidence (dev); BEN-13
_L16 = ["plans/l16_prereg.json", "manifests/evidence/l16_prereg_2026-10-19.sha256", "analysis/q2_l16.py", "tests/test_q2_l16_l5.py",
        "analysis/results/q2_v3/l16_dev.json", "analysis/reports/q2_l16_dev.md", "docs/design/q2_lever_map.md"]
_L5 = ["plans/l5_prereg.json", "manifests/evidence/l5_prereg_2026-10-19.sha256", "analysis/q2_l5.py", "analysis/q2_l5_diag.py",
       "analysis/results/q2_v3/l5_dev.json", "analysis/results/q2_v3/l5_diag_dev.json", "analysis/reports/q2_l5_dev.md"]
for _i in ITEMS:
    if _i["id"] == "TGT-18":
        _i["evidence"] = list(_i["evidence"]) + [e for e in _L16 + _L5 if e not in _i["evidence"]]
        _i["checks"] = list(_i.get("checks") or []) + [
            {"t": "manifest", "path": "manifests/evidence/l16_prereg_2026-10-19.sha256"},
            {"t": "manifest", "path": "manifests/evidence/l5_prereg_2026-10-19.sha256"},
            J("analysis/results/q2_v3/l16_dev.json", ["verdicts", "P-A3"], "eq", "supported"),
            J("analysis/results/q2_v3/l16_dev.json", ["selected_gate", "transfer_guard", "passes"], "eq", False),
            J("analysis/results/q2_v3/l5_dev.json", ["licences"], "len_eq", 0)]
        _i["note"] = _i["note"] + (" 19 Oct (dev): L16, an observable gate (ledger density or triangle share) clears the pooled bar "
                                   "(0.803, 20% of false links) only by acting at a stricter cut-off on denser files; it fails the "
                                   "transfer guard (within-family rho <= 0.33) and its semantic cuts are right 0.735, so it is not acted "
                                   "on. A declared domain-structure statement licensing L8a costs -0.002 DV-1 precision when wrong "
                                   "(analysis/reports/q2_l16_dev.md). L5, interventions as link evidence: no licence; the shadow signal is "
                                   "real (48% vs 7%) but CausalArena's release reaches 20% / 13% of false links with about 40 rows per "
                                   "target (analysis/reports/q2_l5_dev.md).")
    if _i["id"] == "TGT-19":
        _i["evidence"] = list(_i["evidence"]) + [e for e in ["analysis/reports/q2_l5_dev.md", "analysis/results/q2_v3/l5_dev.json"] if e not in _i["evidence"]]
        _i["note"] = _i["note"] + (" 19 Oct: adding missed links from interventions (L5 rule A) is 9-14% precise on dev; no licence "
                                   "(analysis/reports/q2_l5_dev.md).")
ITEMS.append(item("BEN-13", "BEN", "CausalBench (GSK) shortcut audit: how much of each published score is metric echo, edge placement or name recall",
                  "todo", kind="task",
                  criterion=("Two published rows per cell line (K562, RPE1) reproduced within tolerance before any re-score claim; then per "
                             "published method: (a) edge-placement control on mean Wasserstein and FOR; (b) names-only baseline on the "
                             "biological and statistical evaluations under a gene-label permutation; the share of each published score each "
                             "channel accounts for, with intervals; predictions and thresholds hashed before the first re-score"),
                  evidence=["docs/project_snapshots/2026-10-19/benchmark-targets.md"],
                  note=("Opened 19 Oct from the CausalBench deep-dive (project:claude/benchmark-targets.md, update 2026-10-19). Data "
                        "download and long runs on Uzair's machine; the names-only arm needs a small approved model spend. First step "
                        "toward Rung 3 (evidence-typed, calibrated pairs) and the large real testbed for lever L5.")))
'''
p.write_text(c + "\n", encoding="utf-8")
print("p23 applied")
