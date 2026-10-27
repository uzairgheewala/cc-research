"""s34 (27 Oct): the public Q1 repository (DLV-07, new) and the course's corrected checkpoint (DLV-05, CRS-02).

The course page (dsc-capstone.org/2026-27/assignments/projects/q1, read 27 Oct) sets the checkpoint on Fri 6 Nov. It holds the
title, abstract and introduction (intro paragraph, prior work, data) in the course's LaTeX template, plus a link to a public
GitHub repository with the code so far. The 2 Nov date in DLV-05 / CRS-02 came from older notes.
Run once from cc-research: py -3 jobs\\patches\\s34_q1_repo.py   (refuses twice)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides s34" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides s34 (2026-10-27): public Q1 repository (DLV-07); checkpoint date and content per the course page
ITEMS.append(item("DLV-07", "DLV", "Public Q1 code repository: a curated, reproducible export of cc-research", "in_progress",
                  kind="deadline", due="2026-11-06",
                  criterion=("A public GitHub repository, linked from the checkpoint, produced by tools/export_q1.py from an allowlist: "
                             "README with data, dependencies and commands; the comparison script run verbatim on reduced run states "
                             "checked against a manifest of the full files; python run.py reproduce recomputes "
                             "analysis/results/fork/bld06_live_compare.json exactly with no API key; CI runs it on every push"),
                  evidence=["tools/export_q1.py", "docs/q1_repo/README.md", "docs/q1_repo/run.py", "docs/q1_repo/tests/test_reproduce.py",
                            "docs/q1_repo/docs/method.md", "docs/q1_repo/docs/code_tour.md", "analysis/trace_q011.py",
                            "analysis/results/run_trace/q011_gas_void.json", "analysis/reports/run_trace/q011_gas_void.md"],
                  checks=[{"t": "json", "path": "analysis/results/run_trace/q011_gas_void.json",
                           "ptr": ["arms", "branch (refinement v2)", "delivered_graph"], "op": "eq", "v": "void -> gas", "tol": None},
                          {"t": "json", "path": "analysis/results/run_trace/q011_gas_void.json",
                           "ptr": ["arms", "main (unmodified)", "delivered_graph"], "op": "eq", "v": "no link", "tol": None}],
                  note=("Uzair, 27 Oct: route (b) of claude/reorg-2026-10-27.md, a curated public Q1 repo (cc-research is public too). "
                        "Export checked on the device 27 Oct: 165 files, 9.1 MB, reproduction exact, 4 tests pass. Done when the "
                        "repository is public, CI is green and the checkpoint links it.")))
for _i in ITEMS:
    if _i["id"] in ("DLV-05", "CRS-02"):
        _i["due"] = "2026-11-06"
        _i["title"] = _i["title"].replace("(Mon 2 Nov)", "(Fri 6 Nov)")
        _i["note"] = ((_i.get("note") or "") + " 27 Oct: the course page sets Fri 6 Nov; the checkpoint is the title, abstract and "
                      "introduction (intro paragraph, prior work, data) in the course LaTeX template, plus the public code link (DLV-07).").strip()
    if _i["id"] == "DLV-05":
        _i["criterion"] = ("Title, abstract and introduction (intro paragraph, prior work, data description) submitted in the course "
                           "LaTeX template, with a link to the public Q1 repository (DLV-07)")
'''
p.write_text(c, encoding="utf-8", newline="\n")
print("s34 applied")
