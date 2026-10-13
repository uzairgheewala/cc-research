"""How much of each baseline's directed F1 comes from the scoreboard authors' rule for undecided pairs
(orient from the lower to the higher column index) on released vs shuffled column order. No model calls.
Reads the existing BND-04/BND-06 method results; writes analysis/results/authors_rule/check.json.
Tickets: BEN-07, REP-07, AUD-16
"""
import json, statistics as st
from pathlib import Path

R = Path(__file__).resolve().parent / "results"
PAIRS = {"PC": ("methods/pc_semantic_obs_rel.json", "methods/pc_semantic_obs_shuf.json"),
         "GES": ("methods/gesbic_semantic_obs.json", "methods/gesbic_semantic_obs_shuf.json"),
         "FCI": ("methods/fci_semantic_obs.json", "methods/fci_semantic_obs_shuf.json")}


def summ(path):
    d = json.load(open(R / path))
    rows = d["rows"] if isinstance(d, dict) and "rows" in d else d
    ok = [r for r in rows if r.get("scores") and not r.get("error") and not r.get("failed")]
    lo = st.mean(r["scores"]["lower"]["f1"] for r in ok)
    ra = st.mean(r["scores"]["random"]["f1"] for r in ok)
    return {"files": len(ok), "f1_authors_rule": round(lo, 4), "f1_random_rule": round(ra, 4), "layout_gain": round(lo - ra, 4)}


out = {"family": "semantic (public 50 scenarios x 5 files)", "tickets": ["BEN-07", "REP-07"],
       "rule": "undecided pairs oriented lower column index -> higher (authors' rule) vs at random (expected)",
       "methods": {m: {"released_order": summ(a), "shuffled_order": summ(b)} for m, (a, b) in PAIRS.items()}}
json.dump(out, open(R / "authors_rule" / "check.json", "w"), indent=1)
json.dump({"producer": "analysis/authors_rule_layout_check.py", "score_bearing": False, "tickets": out["tickets"]},
          open(R / "authors_rule" / "CONTRACT.json", "w"), indent=1)
for m, v in out["methods"].items():
    print(m, "released gain %+.3f, shuffled gain %+.3f" % (v["released_order"]["layout_gain"], v["shuffled_order"]["layout_gain"]))
