"""2026-10-14: the audit chapter closes. AB-06 tier A scored (P9, P10 supported; amendment 3), DEC-05 taken (B, with A as the
floor), DEC-01 adopted as amended (E1 done, scoped), AB-17 skeleton and Q2 build pre-registration hashed, DLV-02 closed under its
restated criterion (docs/decisions/2026-10-14_audit_closeout.md), AUD-13 done. Refuses to run twice."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p15" in c, "apply p15 first"
assert "# ---- overrides p16" not in c, "already applied"
block = r'''
# ---- overrides p16 (2026-10-14): the audit chapter closes
_WD = "docs/decisions/2026-10-14_wedge_decision.md"
_CO = "docs/decisions/2026-10-14_audit_closeout.md"
_AB06 = "analysis/results/ab06/ab06.json"
_P16 = {
    "AUD-38": dict(status="done", blocked_by=None,
                   evidence=None,  # extended below
                   checks=[{"t": "manifest", "path": "manifests/evidence/ab06_prereg_amendment3_2026-10-14.sha256"},
                           J(_AB06, ["P9", "verdict"], "eq", "supported"),
                           J(_AB06, ["P10", "verdict"], "eq", "supported"),
                           J("plans/ab06/TIERS.json", ["cost", "A", "runs"], "eq", 80),
                           J("analysis/results/ab06_cc/s2_verdicts.json", ["M4", "verdict"], "eq", "SUPPORTED")],
                   note="Tier A scored 14 Oct (80 runs, 79 ok; $32.11 for the grid, $48.23 with the earlier quota-stopped attempt). "
                        "P9 SUPPORTED: Causal-Copilot (gpt-4o), causaliq and MATMCD lose >= 0.10 directed F1 when names are swapped "
                        "(PyWhy-LLM not entered: 4 paired scenarios < 5). P10 SUPPORTED: MATMCD scores below its own data-only graph "
                        "with neutral or swapped names. Vashishtha is the exception (name reliance 0.020): 89 of 100 directions come "
                        "from data. One PyWhy-LLM run crashed inside the guidance library (negative time-to-first-token); counted as "
                        "an agent failure, not retried (amendment 3). Tier B not run (DEC-05)."),
    "DEC-05": dict(status="done", blocked_by=None,
                   evidence=["analysis/reports/ab16_wedge_decision.md", "analysis/reports/approach_v1.md", _WD,
                             "analysis/reports/ab06_field_audit.md"],
                   checks=[G(_WD, r"B: measurement \+ a reliability-first claim ledger"),
                           G("analysis/reports/ab16_wedge_decision.md", r"## Decision \(14 Oct\)"),
                           G("analysis/reports/approach_v1.md", r"## 3\. Binding times")],
                   note="Decided 14 Oct (Uzair delegated it with AB-06's results in hand): B, measurement plus a reliability-first "
                        "claim ledger, with A (measurement only) as the floor. Venue class: methods with a benchmark contribution. "
                        "B0 and B1 start now; AB-06 tier B not run."),
    "DEC-01": dict(status="done", blocked_by=None, criterion="Program v2 adopted, redirected or enlarged; E1-E5 scoped",
                   evidence=[_WD, "analysis/reports/audit_closeout.md"],
                   checks=[G(_WD, r"DEC-01")],
                   note="Adopted as amended 14 Oct: E1 done in a scoped form (STR-01); E2-E5 deferred behind the Q2 build gates."),
    "AUD-47": dict(status="done", blocked_by=None,
                   evidence=["docs/paper/skeleton.md", "plans/q2_build_prereg.json", "manifests/evidence/paper_prereg_2026-10-14.sha256"],
                   checks=[{"t": "manifest", "path": "manifests/evidence/paper_prereg_2026-10-14.sha256"},
                           G("docs/paper/skeleton.md", r"## Held-out discipline"),
                           G("plans/q2_build_prereg.json", r"AUD-47 \(AB-17\)")],
                   note="Skeleton (claims C1-C10, sections, figures, venue) and the Q2 build pre-registration (gates B0.1-B5.2 with "
                        "thresholds, splits, controls, order) hashed 14 Oct, before any held-out run of the build."),
    "STR-01": dict(status="done", blocked_by=None, criterion="E1 in scoped form: AB-05 probes and AB-06 tier A under name and layout controls",
                   evidence=["analysis/reports/ab06_field_audit.md", _AB06, "analysis/reports/ab06_cc_second_model.md"],
                   checks=[J(_AB06, ["P9", "verdict"], "eq", "supported")],
                   note="Done in scoped form: five systems (four agents and Causal-Copilot on two models), tier A only. Tier B and "
                        "further systems are not part of the audit chapter."),
    "RQ-05": dict(status="done", blocked_by=None, criterion="P9 verdict from AB-06 tier A",
                  evidence=["analysis/reports/ab06_field_audit.md", _AB06, "analysis/results/ab06/name_reliance.png"],
                  checks=[J(_AB06, ["P9", "verdict"], "eq", "supported")],
                  note="Answered: three of the four systems entered lose >= 0.10 directed F1 when names are swapped (Causal-Copilot "
                       "gpt-4o, causaliq, MATMCD). Vashishtha does not (0.020); it takes 89% of directions from data."),
    "DLV-02": dict(status="done", blocked_by=None,
                   criterion="Every dataset in the frozen suite has a recorded live run in each name arm (real, neutral, moved) that "
                             "reached S3; crashes are counted as crashes; every run recorded and the code tree verified before and after "
                             "(restated 14 Oct, docs/decisions/2026-10-14_audit_closeout.md)",
                   evidence=["runs/*/meta.json", "plans/results/", "analysis/results/stability_s2/bnd08_summary.json", _CO],
                   checks=[{"t": "runs", "live": True, "tree_ok": True},
                           J("analysis/results/stability_s2/bnd08_summary.json", ["all_code_identity_ok"], "true"),
                           G(_CO, r"DLV-02")],
                   note="Closed 14 Oct under the restated criterion: 84 live runs on S1 and 30 on S2; every arm reached S3. The 6 S2 "
                        "arms whose only gpt-4o run crashed at the cycle step are not rerun: the crash is the system's own (18 of 19 "
                        "live entries) and is reported as a finding."),
    "AUD-13": dict(status="done", blocked_by=None, criterion="Bundle-1 arms repeated with one other model (S2, 10 families x 3 arms)",
                   evidence=["analysis/reports/ab06_cc_second_model.md", "analysis/results/ab06_cc/s2_verdicts.json"],
                   checks=[J("analysis/results/ab06_cc/s2_verdicts.json", ["M4", "verdict"], "eq", "SUPPORTED")],
                   note="Causal-Copilot on gpt-4o-mini, 30 runs: M4 supported 9/10, M2 refuted on both models; name reliance 0.094 "
                        "vs 0.167 on gpt-4o (RQ-17)."),
    "EXT-06": dict(note="Draft ready (docs/drafts/bug_reports/); AB-06 adds the PyWhy guidance clock crash and MATMCD notes in "
                        "docs/drafts/bug_reports/agents_output_contracts_ab06.md. Uzair decides whether to send."),
    "AUD-41": dict(note="Carried forward past the audit chapter (docs/decisions/2026-10-14_audit_closeout.md): interviews still decide "
                        "P13 and C1; they run whenever a chance arises and gate nothing."),
    "AUD-32": dict(evidence=None,  # extended below
                   note="Approved 12 Oct. The chapter closed 14 Oct: 17 bundles done or closed by decision; see "
                        "analysis/reports/audit_closeout.md."),
}
for _i in ITEMS:
    if _i["id"] in _P16:
        _u = {k: v for k, v in _P16[_i["id"]].items() if v is not None or k == "blocked_by"}
        _i.update(_u)
        if _i["id"] == "AUD-38":
            _i["evidence"] = list(_i["evidence"]) + ["plans/ab06_prereg_amendment_3.json",
                "manifests/evidence/ab06_prereg_amendment3_2026-10-14.sha256", _AB06, "analysis/results/ab06/CONTRACT.json",
                "analysis/ab06_figure.py", "analysis/results/ab06/name_reliance.png", "analysis/results/ab06/name_reliance.svg",
                "analysis/reports/ab06_field_audit.md"]
        if _i["id"] == "AUD-32":
            _i["evidence"] = list(_i["evidence"]) + ["analysis/reports/audit_closeout.md", _CO]
        if _i["id"] == "EXT-06":
            _i["evidence"] = list(_i["evidence"]) + ["docs/drafts/bug_reports/agents_output_contracts_ab06.md"]

_B16 = {"BND-08": "done", "BND-10": "done", "BND-11": "done",
        "AB-06": "done", "AB-16": "done", "AB-17": "done"}
BUNDLE_STATUS.update(_B16)
BUNDLE_NOTE.update({
    "BND-08": "Closed 14 Oct with DLV-02 under its restated criterion: 30 runs, 24 completed, 6 crashed at the cycle step, all "
              "reached S3. M1, M3, M4 SUPPORTED; M2 REFUTED (5/10); M5 not run. Crashes are reported as a finding, not rerun.",
    "BND-10": "Done 14 Oct (BND-08 closed, rule W3). Pooled held-out (55 tables): R1 INCONCLUSIVE 40/55, R2 INCONCLUSIVE 47/55, "
              "R3 SUPPORTED -0.003. TGT-09 met by v2 in BND-11.",
    "BND-11": "Done 14 Oct: v2 R1-R3 SUPPORTED 22/22 held-out formula files; names R4, R5 SUPPORTED, R6 REFUTED (1/10); 0 crashes.",
    "BND-12": "Audit parts done (AUD-13, RQ-17; REP-11 data part reproduced). Remaining live parts (CARE moved-names control, "
              "LLM and fused Sachs numbers, CausalSteward) moved to the Q2 build (B3) on 14 Oct.",
    "AB-06": "Tier A scored 14 Oct: P9 SUPPORTED (3 of 4 systems lose >= 0.10 with names swapped), P10 SUPPORTED (MATMCD below "
             "its own data-only graph). $32.11. Tier B not run (DEC-05).",
    "AB-16": "Decided 14 Oct: B (measurement + reliability-first claim ledger), A as the floor; methods + benchmark venue.",
    "AB-17": "Skeleton and Q2 build pre-registration hashed 14 Oct (manifests/evidence/paper_prereg_2026-10-14.sha256).",
})
for _i in ITEMS:
    if _i["id"] in _B16 and _i.get("kind") == "bundle":
        _i["status"] = _B16[_i["id"]]
        _tail = ("Runner:" + _i["note"].split("Runner:", 1)[1]) if "Runner:" in _i["note"] else ""
        _i["note"] = (BUNDLE_NOTE[_i["id"]] + " " + _tail).strip()
    if _i["id"] == "BND-12":
        _tail = ("Runner:" + _i["note"].split("Runner:", 1)[1]) if "Runner:" in _i["note"] else ""
        _i["note"] = (BUNDLE_NOTE["BND-12"] + " " + _tail).strip()
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p16 applied")
