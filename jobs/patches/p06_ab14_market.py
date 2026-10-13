"""AB-14 done without waiting on interviews (Uzair, 2026-10-13; docs/decisions/2026-10-13_interviews_not_gating.md).
1. plans/make_audit_dag.py -> version 2: AB-14 depends on AB-11 + AB-13 (not AB-10), with a wider scope; AB-16 no longer
   depends on AB-10; C1 wording. Then run `python plans/make_audit_dag.py` to rewrite plans/audit_dag.json.
2. tracker/catalogue.py overrides: AUD-45 done; AUD-41 and DEC-05 notes; AB-14 bundle done.
Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ---- 1. the DAG generator
g = ROOT / "plans" / "make_audit_dag.py"
s = g.read_text(encoding="utf-8")
assert '"version": 2' not in s, "already applied"
reps = [
    ('''bundle("AB-14", "Market and go-to-market hypotheses", "commercial", ["AB-10", "AB-13"], ("2026-10-27", "2026-11-12"), "Claude (desk)", NONE,
       ["bottom-up estimates for two verticals (IT incident analysis, marketing measurement) from public pricing; buyer, budget line, "
        "channel; every figure labelled estimate with its inputs"],
       ["none"], ["no number without its inputs"], ["two one-page vertical briefs"],
       ["analysis/reports/ab14_market.md"], ["C3"], advances=["STR-06"], proposed_tickets=["AUD-45 market hypotheses"])''',
     '''bundle("AB-14", "Market and go-to-market hypotheses", "commercial", ["AB-11", "AB-13"], ("2026-10-27", "2026-11-12"), "Claude (desk)", NONE,
       ["market map of causal AI: segments, vendors, funding, M&A, market-size estimates and their conflicts, platform churn",
        "bottom-up estimates for three verticals (IT incident RCA, marketing measurement, pharma RWE) from public pricing and filings; "
        "buyer, budget line, channel; every figure labelled estimate with its inputs",
        "public demand evidence on H1-H3, labelled indirect (stands in for AB-10 until interviews exist; cannot decide P13)"],
       ["none"], ["no number without its inputs"], ["market map", "three one-page vertical briefs", "H1-H3 public evidence, labelled indirect"],
       ["analysis/reports/ab14_market.md", "analysis/audits/ab14_notes/"], ["C1", "C3"], advances=["STR-06"],
       proposed_tickets=["AUD-45 market hypotheses"])'''),
    ('''bundle("AB-16", "Wedge decision (gate)", "wedge", ["AB-01", "AB-02", "AB-03", "AB-04", "AB-05", "AB-09", "AB-10", "AB-11", "AB-15"],''',
     '''bundle("AB-16", "Wedge decision (gate)", "wedge", ["AB-01", "AB-02", "AB-03", "AB-04", "AB-05", "AB-09", "AB-11", "AB-14", "AB-15"],'''),
    ('''        "if AB-06 has not finished, decide on its interim results"],''',
     '''        "if AB-06 has not finished, decide on its interim results",
        "C1 from AB-14's public demand evidence (indirect) plus AB-10 interviews if any exist; the memo states which"],'''),
    ('''    "C1": "Demand evidence: practitioners name decisions where provenance and abstention matter (interviews, teardown).",''',
     '''    "C1": "Demand evidence: practitioners name decisions where provenance and abstention matter (interviews if any, teardown, "
          "public demand evidence labelled indirect).",'''),
    ('''"version": 1, "drafted": "2026-10-12",''',
     '''"version": 2, "drafted": "2026-10-12",
       "amendments": [{"date": "2026-10-13", "record": "docs/decisions/2026-10-13_interviews_not_gating.md", "note": "AB-14 finished on 13 Oct, ahead of its plan window",
                       "change": "AB-14 and AB-16 no longer wait on AB-10 interviews; AB-14 widened to a market map and three verticals"}],'''),
]
for a, b in reps:
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
g.write_text(s, encoding="utf-8")

# ---- 2. the catalogue
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p05" in c, "apply p05 first"
assert "# ---- overrides p06" not in c
block = r'''
# ---- overrides p06 (2026-10-13): AB-14 market research done without waiting on interviews (Uzair's decision)
_P06 = {
    "AUD-45": dict(status="done", blocked_by=None,
                   criterion="Must show: market map; three one-page vertical briefs; H1-H3 public evidence, labelled indirect. Gate: no number without its inputs",
                   evidence=["analysis/reports/ab14_market.md", "analysis/audits/ab14_notes/market_map.md",
                             "analysis/audits/ab14_notes/it_incident_rca.md", "analysis/audits/ab14_notes/marketing_measurement.md",
                             "analysis/audits/ab14_notes/pharma_rwe.md", "analysis/audits/ab14_notes/demand_signals.md",
                             "docs/decisions/2026-10-13_interviews_not_gating.md"],
                   checks=[G("analysis/reports/ab14_market.md", r"Brief 1: IT incident RCA"), G("analysis/reports/ab14_market.md", r"Brief 2: marketing"),
                           G("analysis/reports/ab14_market.md", r"Brief 3: pharma RWE"), G("analysis/reports/ab14_market.md", r"The public evidence on H1-H3 is indirect"),
                           J("plans/audit_dag.json", ["version"], "eq", 2)],
                   note="Done 13 Oct without interviews (Uzair's decision). Start in IT incident RCA as a vendor-neutral audit of AI SRE agents' "
                        "root-cause claims; marketing a close second; pharma third. Obtainable (estimates): RCA $1.8-9M ARR in ~3 yrs; marketing "
                        "$3-67.5M at maturity; pharma core $2.8-11M/yr. 'Causal AI' sizings span $28.9M-$59.2B. H2 best supported; H1 for "
                        "provenance, not abstention; H3 by analogy only."),
    "AUD-41": dict(note="Interview kit ready; interviews run whenever a chance arises. No longer gates AB-14 or AB-16 (decision 2026-10-13); "
                        "P13 can only be decided by interviews."),
    "DEC-05": dict(note="Bundle AB-16: decide once the evidence is in. C1 from AB-14's public evidence (indirect) plus interviews if any."),
    "STR-06": dict(note="AB-14 (13 Oct): sell a vendor-neutral audit of other agents' causal claims, not a causal-AI platform; start in IT incident RCA.",
                   evidence=["analysis/reports/ab14_market.md"]),
}
for _i in ITEMS:
    if _i["id"] in _P06:
        _i.update(_P06[_i["id"]])
BUNDLE_STATUS.update({"AB-14": "done"})
BUNDLE_NOTE.update({"AB-14": "Market map + 3 briefs: start in IT incident RCA (audit AI SRE agents' claims); marketing second; pharma third.",
                    "AB-10": "Kit ready; interviews whenever a chance arises; no longer gates AB-14 or AB-16."})
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")

# ---- 3. the old scaffold points at the result
r = ROOT / "docs" / "market" / "README.md"
t = r.read_text(encoding="utf-8")
if "Superseded" not in t:
    r.write_text("> **Superseded 2026-10-13.** The briefs are built: `analysis/reports/ab14_market.md` (market map, three verticals, "
                 "public demand evidence). They did not wait on AB-10 (docs/decisions/2026-10-13_interviews_not_gating.md).\n\n" + t,
                 encoding="utf-8")
print("p06 applied: run python plans/make_audit_dag.py next")
