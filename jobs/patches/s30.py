"""s30 (Inside Causal-Copilot, TEAM-13): tracker entry for the code-explorer site. Refuses to run twice; needs s24.

Everything else of TEAM-13 is new files (site/copilot/*, tests/test_copilot_site.py, analysis/reports/copilot_code_notes.md)
and the two workflow steps; this patch only adds the ticket, because tracker/catalogue.py is in sheet A's code identity:
apply it when the wave chat next refreshes that identity (or after sheet A's final run)."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides s24" in c, "apply s24 first"
assert "# ---- overrides s30" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides s30 (2026-10-20): Inside Causal-Copilot, the code-explorer site (TEAM-13)
ITEMS.append(item("TEAM-13", "TEAM", "Inside Causal-Copilot: a site explaining how every part of Causal-Copilot works",
                  "in_progress", kind="task",
                  criterion=("A typed model of the first-party code at a31aa7c extracted from the AST and checked against the baseline "
                             "manifest; nine step pages written by reading the code and bound to the hashes of the functions they "
                             "describe; reference pages (state, model calls, algorithms, prompts, every module and function); a "
                             "findings layer with evidence labels; one recorded scenario replayed under three name arms; the build "
                             "fails on any function, excerpt, prompt or source that does not match; unit tests"),
                  evidence=["site/copilot/extract.py", "site/copilot/model.json", "site/copilot/snip.py", "site/copilot/excerpts.json",
                            "site/copilot/build.py", "site/copilot/bindings.json", "site/copilot/replay.json",
                            "site/copilot/export_replay.py", "site/copilot/algorithms.json", "tests/test_copilot_site.py",
                            "analysis/reports/copilot_code_notes.md"],
                  note=("Uzair, 20 Oct: wants to understand Causal-Copilot's code, with a full site on its architecture "
                        "(project:claude/copilot-explorer-design-2026-10-20.md). Built 20 Oct; done once he has read it on the deployed site.")))
'''
p.write_text(c, encoding="utf-8", newline="\n")
print("s30 applied")
