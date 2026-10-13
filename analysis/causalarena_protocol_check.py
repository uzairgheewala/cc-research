"""REP-06 / BEN-08: CausalArena's baseline scoring protocol, read from the authors' code, against our PC calibration.

  git clone --depth 1 https://github.com/LAMDA-Tabular/TabCausal $HOME/scratch/tabcausal     # separate clone, read-only
  python analysis/causalarena_protocol_check.py --clone $HOME/scratch/tabcausal

The TabCausal repository (same authors as CausalArena) holds the baseline runners and metrics its README describes as
the benchmark's evaluation conventions. This script records the exact lines (with commit and file sha256) for:
  P1 SHD formula (a reversed edge counts once)        baselines/paper_algorithms/metrics.py
  P2 orientation of undirected CPDAG edges for PC      baselines/paper_algorithms/run_pc.py ("liberal": lower index -> higher)
  P3 the README's statement of the convention          baselines/README.md
  P4 PC configuration (fisherz, alpha 0.05, stable)    baselines/paper_algorithms/run_pc.py
and compares the published PC row with our 250-file calibration under each orientation rule
(analysis/results/causalarena_calibration/pc_calibration.json; our SHD is pair-level, i.e. P1's definition).
Output: analysis/results/causalarena_calibration/protocol_check.json
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAL = ROOT / "analysis" / "results" / "causalarena_calibration"
PATTERNS = {
    "P1_shd_formula": ("baselines/paper_algorithms/metrics.py", [r"shd\s*=\s*np\.sum\(diff\)\s*-\s*0\.5\s*\*\s*np\.sum\(diff\s*\*\s*diff\.T\)"]),
    "P2_liberal_orientation": ("baselines/paper_algorithms/run_pc.py", [r'strategy\s*==\s*"liberal"', r"#\s*Orient by index", r"if i < j:"]),
    "P3_readme_convention": ("baselines/README.md", [r"uncertain edges were not randomized", r"`liberal` strategy orients them from the smaller node index"]),
    "P4_pc_configuration": ("baselines/paper_algorithms/run_pc.py", [r"stable=True", r'"--alpha", type=float, default=0\.05', r'"--indep_test", type=str, default="fisherz"']),
    "P5_no_column_shuffle": ("baselines/paper_algorithms/run_pc.py", [r"shuffle|permut"]),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", required=True)
    a = ap.parse_args()
    clone = Path(a.clone)
    commit = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out = {"source": "https://github.com/LAMDA-Tabular/TabCausal", "commit": commit, "facts": {}}
    for key, (rel, pats) in PATTERNS.items():
        txt = (clone / rel).read_text(encoding="utf-8").splitlines()
        hits = []
        for pat in pats:
            hits += [{"pattern": pat, "line": i + 1, "text": l.strip()[:160]} for i, l in enumerate(txt) if re.search(pat, l)]
        out["facts"][key] = {"file": rel, "sha256": hashlib.sha256((clone / rel).read_bytes()).hexdigest(), "hits": hits,
                             "found": (not hits) if key == "P5_no_column_shuffle" else all(any(h["pattern"] == p for h in hits) for p in pats)}
    cal = json.loads((CAL / "pc_calibration.json").read_text(encoding="utf-8"))
    pub, tol = cal["published_pc_semantic_obs_only"], cal["tolerance"]
    order = json.loads((CAL / "order_baseline.json").read_text(encoding="utf-8"))
    rows = {}
    for c in cal["configs"]:
        rows[c["undecided_pairs_rule"]] = {"f1": c["f1_mean"], "shd": c["shd_mean"],
                                           "f1_gap": round(c["f1_mean"] - pub["f1"], 3), "shd_gap": round(c["shd_mean"] - pub["shd"], 3),
                                           "f1_within": abs(c["f1_mean"] - pub["f1"]) <= tol["f1"], "shd_within": abs(c["shd_mean"] - pub["shd"]) <= tol["shd"]}
    out["published"] = pub
    out["tolerance"] = tol
    out["ours_public_50_by_rule"] = rows
    out["release_order_topological_share"] = order["families"]["semantic"]["share"]
    code_rule = "lower"
    out["verdict"] = {
        "code_rule": "liberal = lower index -> higher index (our rule 'lower')",
        "shd_reproduced_under_code_rule": rows[code_rule]["shd_within"],
        "f1_reproduced_under_code_rule": rows[code_rule]["f1_within"],
        "any_rule_reproduces_both": any(r["f1_within"] and r["shd_within"] for r in rows.values()),
        "reading": ("Under the rule the authors' code states, our SHD is within tolerance of the published value but F1 is not; "
                    "under random orientation F1 is within tolerance but SHD is not. No rule reproduces both on the 50 public "
                    "scenarios, and the published means also cover 50 unreleased scenarios, so the gap cannot be settled from "
                    "public data. Because the released column order is topological in every public file, the code's rule gives "
                    "every undecided pair its true direction when the pair is truly adjacent."),
    }
    (CAL / "protocol_check.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v["found"] for k, v in out["facts"].items()}), json.dumps(out["verdict"], indent=1)[:900])
    for k, r in rows.items():
        print(k, r)


if __name__ == "__main__":
    main()
