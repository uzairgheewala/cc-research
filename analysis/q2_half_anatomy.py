"""What the confident half of v3's answers is made of (dev, out of fold by scenario, from the engine cache).

For each family and regime: the half-coverage view's yes / no mix, the precision of each, and the probability bands
the model assigns to right and wrong answers; plus, among the wrong answers kept, how many are "no" answers (which can
only be wrong because of a link the ledger never saw).

  python analysis/q2_half_anatomy.py -> analysis/results/q2_v3/half_anatomy_dev.json
"""
import json, os, sys
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_k] = "1"
os.environ.setdefault("OPENBLAS_CORETYPE", "SKYLAKEX")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
from kernel import v3  # noqa: E402


def main():
    out = {}
    for fam in ("semantic", "formula"):
        out[fam] = {}
        for reg in ("D", "DxR"):
            files = v3._collect(fam, "dev", reg, 4)
            scen = sorted({f["scenario"] for f in files})
            fold = {s: k % 5 for k, s in enumerate(scen)}
            items = []
            for k in range(5):
                m = v3.fit_model([f for f in files if fold[f["scenario"]] != k])
                for f in files:
                    if fold[f["scenario"]] == k:
                        for p, r in zip(v3.apply_model(m, f["rows"]), f["rows"]):
                            items.append((p, r["ok"], r["yes"]))
            tot = sum(f["pairs"] for f in files)
            items.sort(key=lambda t: -t[0])
            kept, k = [], 0
            while k < len(items):
                kept.append(items[k])
                if len(kept) >= 0.5 * tot and (k + 1 == len(items) or items[k + 1][0] < items[k][0]):
                    break
                k += 1
            dropped = items[len(kept):]
            r = lambda a, b: round(a / b, 3) if b else None  # noqa: E731
            S = lambda it, yes: [x for x in it if x[2] == yes]  # noqa: E731
            bands = {}
            for lo in (0.5, 0.6, 0.7, 0.8, 0.9):
                b = [x for x in items if lo <= x[0] < lo + 0.1 or (lo == 0.9 and x[0] >= 0.9)]
                bands["%.1f-%.1f" % (lo, lo + 0.1)] = {"n": len(b), "right_share": r(sum(x[1] for x in b), len(b)), "yes_share": r(len(S(b, True)), len(b))}
            d = {"pairs": tot, "answered": len(items), "kept": len(kept), "kept_coverage": r(len(kept), tot),
                 "kept_precision": r(sum(x[1] for x in kept), len(kept)), "kept_threshold": round(kept[-1][0], 3),
                 "kept_yes": len(S(kept, True)), "kept_yes_precision": r(sum(x[1] for x in S(kept, True)), len(S(kept, True))),
                 "kept_no": len(S(kept, False)), "kept_no_precision": r(sum(x[1] for x in S(kept, False)), len(S(kept, False))),
                 "kept_wrong": sum(1 for x in kept if not x[1]), "kept_wrong_no_share": r(sum(1 for x in S(kept, False) if not x[1]), max(1, sum(1 for x in kept if not x[1]))),
                 "dropped": len(dropped), "dropped_precision": r(sum(x[1] for x in dropped), len(dropped)),
                 "dropped_yes_share": r(len(S(dropped, True)), len(dropped)),
                 "all_yes_precision": r(sum(x[1] for x in S(items, True)), len(S(items, True))),
                 "all_no_precision": r(sum(x[1] for x in S(items, False)), len(S(items, False))),
                 "probability_bands": bands}
            out[fam][reg] = d
            print(fam, reg, json.dumps({k: v for k, v in d.items() if k != "probability_bands"}))
            print("   bands", json.dumps(bands))
    json.dump(out, open(ROOT / "analysis" / "results" / "q2_v3" / "half_anatomy_dev.json", "w"), indent=1)


if __name__ == "__main__":
    main()
