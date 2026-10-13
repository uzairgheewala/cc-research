"""Freeze the development / held-out split by scenario (EVL-05). Run once; the output is pinned by the tracker.

Rule (fixed before any tuning): within each family, scenarios are ordered by sha256("cc-research-split-v1:<family>:<domain>:<slug>")
and, within every domain, the first ceil(k/2) in that order go to dev and the rest to test, alternating the rounding by domain
index so each family splits 25 / 25. Everything recorded before the split (bundle 1, pass 4b, offline cells) is dev.
The 10 S2 scenarios for the Quarter 1 suite are the first 10 test scenarios in the same hash order, at most one per domain.

  python analysis/make_splits.py --root external/causalarena --out plans/splits.json
"""
import argparse, hashlib, json, math
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--root", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()

out = {"rule": __doc__.split("\n\n")[1].strip(), "salt": "cc-research-split-v1", "families": {},
       "always_dev": ["datasets/suite_b1 (bundle 1)", "datasets/d01..d03 and sachs (pass 4b)", "analysis/results/offline (offline cells)"]}
for fam in ("semantic", "formula"):
    m = json.load(open(Path(a.root) / "scm" / fam / "release_split_manifest.json", encoding="utf-8"))
    dev, test = [], []
    for di, (dom, scen) in enumerate(sorted(m["domains"].items())):
        h = lambda s: hashlib.sha256(("cc-research-split-v1:%s:%s:%s" % (fam, dom, s["data_slug"])).encode()).hexdigest()
        ordered = sorted(scen, key=h)
        k = len(ordered)
        n_dev = math.ceil(k / 2) if di % 2 == 0 else math.floor(k / 2)
        for i, s in enumerate(ordered):
            rec = {"domain": dom, "slug": s["data_slug"], "scenario_dir": s["scenario_dir"], "key": h(s)}
            (dev if i < n_dev else test).append(rec)
    by_key = lambda r: r["key"]
    s2, seen = [], set()
    if fam == "semantic":
        for r in sorted(test, key=by_key):
            if r["domain"] not in seen:
                s2.append(r["slug"]); seen.add(r["domain"])
            if len(s2) == 10:
                break
    out["families"][fam] = {"dev": sorted(r["slug"] for r in dev), "test": sorted(r["slug"] for r in test),
                            "dev_by_domain": {}, "s2_test_scenarios": s2}
    for r in dev:
        out["families"][fam]["dev_by_domain"].setdefault(r["domain"], []).append(r["slug"])
    assert not set(out["families"][fam]["dev"]) & set(out["families"][fam]["test"])
json.dump(out, open(a.out, "w", encoding="utf-8"), indent=1, sort_keys=True)
for fam, v in out["families"].items():
    print(fam, "dev", len(v["dev"]), "test", len(v["test"]), "S2", v["s2_test_scenarios"])
