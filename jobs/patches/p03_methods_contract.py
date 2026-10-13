"""Declare the AB-01 variant row files in analysis/results/methods/CONTRACT.json: GIES with targets is regime D+I (per_file),
and the producer list names baseline_variants_run.py. Idempotent."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "analysis" / "results" / "methods" / "CONTRACT.json"
c = json.load(open(p, encoding="utf-8"))
if "baseline_variants_run.py" not in c["producer"]:
    c["producer"] += "; analysis/baseline_variants_run.py (AB-01: pc_upstream_{maxp,dmaxp,}_<family>_obs_{rel,shuf}.json, gies_targets_<family>_obsint_{rel,shuf}.json)"
pf = c.setdefault("per_file", {})
for fam in ("semantic", "formula"):
    for arm in ("rel", "shuf"):
        pf["gies_targets_%s_obsint_%s.json" % (fam, arm)] = {"regime": "D+I", "note": "GIES with the released intervention targets (gies 0.0.3, jitter 1e-6)"}
c["tickets"] = sorted(set(c["tickets"]) | {"AUD-33"})
json.dump(c, open(p, "w", encoding="utf-8"), indent=1, sort_keys=True)
print("methods contract: %d per-file entries" % len(pf))
