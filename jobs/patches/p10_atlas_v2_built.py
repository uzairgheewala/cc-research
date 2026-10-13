"""Atlas v2 built on 2026-10-13 (TEAM-08 done; analysis/reports/site_flow_design.md, "Built"). Refuses to run twice."""
from pathlib import Path

p = Path(__file__).resolve().parents[2] / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p09" in c, "apply p09 first"
assert "# ---- overrides p10" not in c, "already applied"
block = r'''
# ---- overrides p10 (2026-10-13): Atlas v2 built
_P10 = {
    "TEAM-08": dict(status="done", blocked_by=None,
                    evidence=["analysis/reports/site_flow_design.md", "site/build.py", "site/pages.py", "site/terms.py", "site/pagekit.py",
                              "site/registry.py", "site/pgs/pg_home.py", "site/pgs/pg_primer.py", "site/pgs/pg_scoring.py",
                              "site/pgs/pg_space.py", "site/pgs/pg_scoreboard.py", "site/pgs/pg_decisions.py", "site/pgs/pg_names.py",
                              "site/pgs/pg_rca.py", "site/pgs/pg_theses.py", "site/pgs/pg_market.py", "site/pgs/pg_status.py",
                              "site/pgs/pg_changes.py", "site/pgs/pg_glossary.py", "site/pgs/pg_evidence.py", "site/pgs/pg_about.py",
                              "tracker/snapshot.py"],
                    checks=[G("site/pages.py", r"SEQUENCE = "), G("site/build.py", r"is taught later, on"),
                            G("analysis/reports/site_flow_design.md", r"## Built \(2026-10-13\)")],
                    reproduce="python tracker/snapshot.py && python site/build.py",
                    note="Built 13 Oct on the existing Pages site: Home + 11 pages in four acts + glossary, evidence index, about. The build "
                         "fails on missing numbers, term-order violations, early results, broken links and unlabelled market $ figures. "
                         "Phone overflow (390 px, 15 pages) checked by hand with Playwright; not yet in CI."),
}
for _i in ITEMS:
    if _i["id"] in _P10:
        _i.update(_P10[_i["id"]])
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p10 applied")
