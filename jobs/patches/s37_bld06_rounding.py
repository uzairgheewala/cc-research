"""s37 (30 Oct): two interval ends of the BLD-06 live comparison were rounded up in the notes; the result file says otherwise.

Tickets: BLD-06, INF-10
analysis/results/fork/bld06_live_compare.json, paired_branch_minus_main:
  L1 (delivered directed F1) hi = 0.11048 -> 0.110 (notes said 0.111);
  L2_dir (directed F1, 22 shared tables) hi = 0.03847 -> 0.038 (notes said 0.039; the reorg doc of 27 Oct already corrected it).
Edits: the BLD-06 note (catalogue override, so the p32 text stays as history) and WAVE_STATE.md's wave B section (repin INF-10).
Run once from cc-research: py -3 jobs\\patches\\s37_bld06_rounding.py   (refuses twice)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
d = json.load(open(ROOT / "analysis/results/fork/bld06_live_compare.json"))["paired_branch_minus_main"]
assert "%.3f" % d["L1"]["hi"] == "0.110" and "%.3f" % d["L2_dir"]["hi"] == "0.038", "result file is not the one this patch was written for"

p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides s37" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides s37 (2026-10-30): BLD-06 interval ends as the result file rounds them (0.11048 -> 0.110, 0.03847 -> 0.038)
for _i in ITEMS:
    if _i["id"] == "BLD-06":
        _i["note"] = _i["note"].replace("+0.071 [0.035, 0.111]", "+0.071 [0.035, 0.110]").replace("+0.014 [-0.017, 0.039]", "+0.014 [-0.017, 0.038]")
'''
p.write_text(c, encoding="utf-8", newline="\n")
w = ROOT / "WAVE_STATE.md"
s = w.read_text(encoding="utf-8")
assert s.count("+0.071 [0.035, 0.111]") == 1 and s.count("[-0.017, 0.039]") == 1
s = s.replace("+0.071 [0.035, 0.111]", "+0.071 [0.035, 0.110]").replace("[-0.017, 0.039]", "[-0.017, 0.038]")
w.write_text(s, encoding="utf-8", newline="\n")
print("s37 applied")
