"""Extract CausalArena's published leaderboard (directed-edge F1, mean over each family's 100 scenarios) into a small
JSON that lives in git, with the sha256 of the source table (which stays in external/, outside git).

  python analysis/published_extract.py
Writes analysis/results/published/leaderboard.json. No network.
"""
import csv, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "external/causalarena/results/tables/main/main_leaderboard_f1_wide_with_std.csv"
OUT = ROOT / "analysis/results/published/leaderboard.json"
COLS = {"Synthetic obs+int": ("synthetic", "D+I"), "Synthetic obs-only": ("synthetic", "D"),
        "Semantic obs+int": ("semantic", "D+I"), "Semantic obs-only": ("semantic", "D"),
        "Formula obs+int": ("formula", "D+I"), "Formula obs-only": ("formula", "D")}


def main():
    raw = SRC.read_bytes()
    rows = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    table = {}
    for r in rows:
        for col, (fam, reg) in COLS.items():
            m = re.match(r"\s*([0-9.]+)\s*\(([0-9.]+)\)", r.get(col) or "")
            if m:
                table.setdefault(fam, {}).setdefault(reg, {})[r.get("Method") or r.get("method")] = {"f1": float(m.group(1)), "sd": float(m.group(2))}
    best = {fam: {reg: max(v.items(), key=lambda kv: kv[1]["f1"]) for reg, v in regs.items()} for fam, regs in table.items()}
    out = {"source": SRC.relative_to(ROOT).as_posix(), "source_sha256": hashlib.sha256(raw).hexdigest(),
           "metric": "directed-edge F1, mean (sd) over the family's scenarios, as published",
           "table": table,
           "best": {fam: {reg: {"method": m, "f1": v["f1"]} for reg, (m, v) in regs.items()} for fam, regs in best.items()}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, sort_keys=True)
    print("published: %d methods; best semantic D %s" % (len(rows), out["best"]["semantic"]["D"]))


if __name__ == "__main__":
    main()
