"""Recompute the checkpoint MATMCD precision comparison from public counters (DLV-07)."""
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[4]


def main():
    counters = json.loads((ROOT / "analysis/results/ab06/ab06.json").read_text(encoding="utf-8"))
    report = ROOT / "docs/paper/q1/checkpoint_evidence/matmcd-report-2026-11-03.json"
    effect = next(row["effect"] for row in json.loads(report.read_text(encoding="utf-8"))["findings"]
                  if row["id"] == "K07")
    eligible = sorted(
        (row for row in counters["rows"] if row["agent"] == "matmcd" and row["arm"] == "real"
         and row["status"] == "ok" and "dv_com_data_only" in row),
        key=lambda row: row["scenario"],
    )
    if len(eligible) != effect["units"] or len({row["scenario"] for row in eligible}) != effect["clusters"]:
        raise ValueError("MATMCD counter scope differs from the retained effect")
    counts = np.array([[row[key] for key in ("dv_ok", "dv_com", "dv_ok_data_only", "dv_com_data_only")]
                       for row in eligible])
    a, b, c, d = counts.sum(axis=0)
    rng = np.random.default_rng(effect["seed"])
    pooled = counts[rng.integers(len(counts), size=(effect["B"], len(counts)))].sum(axis=1)
    lo, hi = np.percentile(pooled[:, 0] / pooled[:, 1] - pooled[:, 2] / pooled[:, 3], [2.5, 97.5])
    actual = dict(dv1_precision_final=a / b, dv1_precision_data_only=c / d,
                  point=a / b - c / d, lo=float(lo), hi=float(hi))
    for key, value in actual.items():
        if not np.isclose(value, effect[key], rtol=0, atol=1e-12):
            raise ValueError(f"MATMCD {key} differs from the retained effect")
    print(json.dumps({"units": len(counts), "pooled_counts": counts.sum(axis=0).tolist(), **actual}, indent=2))


if __name__ == "__main__":
    main()
