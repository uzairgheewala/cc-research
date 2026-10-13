"""Atlas v2 design (analysis/reports/site_flow_design.md): add TEAM-08 (the build, S1-S5) and DEC-06 (Uzair approves the
page sequence). Readability pass of 13 Oct recorded on TEAM-08. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p06" in c, "apply p06 first"
assert "# ---- additions p07" not in c, "already applied"
block = r'''
# ---- additions p07 (2026-10-13): Atlas v2, a guided sequence of pages (design awaiting approval)
ITEMS.append(item("TEAM-08", "TEAM", "Atlas v2: the site as a guided sequence of pages (four acts, thirteen pages)", "blocked", kind="task",
    criterion="Must show (per bundle S1-S5 in the design): pages build; 0 missing numbers; 0 broken links; 0 term-order violations; "
              "no horizontal scroll at 390 px; 'pages to re-read' list works; recentering path Home -> changes -> status",
    evidence=["analysis/reports/site_flow_design.md", "site/build.py", "site/levels/bundles.py", "site/levels/theses.py"],
    checks=[G("analysis/reports/site_flow_design.md", r"Failure modes named in advance"), G("site/build.py", r"max-width: 640px")],
    blocked_by="DEC-06",
    note="Design written 13 Oct. Readability pass done the same day on the current site: dates out of headings, stale DEC-02/A3 text "
         "fixed, audit board follows DAG v2, clipped notes fixed, no phone overflow. Build waits on DEC-06."))
ITEMS.append(item("DEC-06", "DEC", "Approve the Atlas v2 page sequence (and whether the market page is public)", "open", kind="decision",
    criterion="Uzair's decision recorded with what it approves",
    evidence=["analysis/reports/site_flow_design.md"],
    note="Three choices in the design: the 4-act / 13-page sequence; market page public or repo-only; Home leads with research."))
'''
p.write_text(c.rstrip("\n") + "\n" + block, encoding="utf-8")
print("p07 applied")
