"""Read-only CausalBench score replay for selected Q1 checkpoint rows (DLV-07)."""
import hashlib
import json
import math
import sys
from importlib.metadata import version

from analysis.ben13.run import DATA, PREREG, Line, OUT

EXPECTED_ARRAYS = {
    "k562": "513d763a466efcbeb9cdd30f219c6162e857035d3af1e7f574dbb7103764c57a",
    "rpe1": "a1f728261be13972e6739345dc70db6dde10e6248aef04fa3b2261ffec18d9ba",
}
CELLS = ("md_k1000", "md_k5000", "random_k1000", "random_k5000")
FIELDS = ("tp", "fp", "edges", "wasserstein", "for", "negative_wasserstein")


def replay():
    if version("causalbench") != "1.1.2":
        raise RuntimeError("Replay requires causalbench==1.1.2")
    protocol = json.loads(PREREG.read_text(encoding="utf-8"))["protocol"]
    rows = []
    for name, expected_sha in EXPECTED_ARRAYS.items():
        with (DATA / f"dataset_{name}_filtered.npz").open("rb") as source:
            sha = hashlib.file_digest(source, "sha256").hexdigest()
        if sha != expected_sha:
            raise ValueError(f"Unexpected filtered-array bytes for {name}: {sha}")
        line = Line(name)
        for cell in CELLS:
            expected = json.loads((OUT / name / f"{cell}.json").read_text(encoding="utf-8"))
            actual = line.score(cell, protocol)
            comparisons = {"network_sha256": actual["network_sha256"] == expected["network_sha256"]}
            scores = {}
            for field in FIELDS:
                got, want = (r["statistical"].get(field) for r in (actual, expected))
                scores[field] = {"expected": want, "actual": got}
                comparisons[field] = (
                    math.isclose(got, want, rel_tol=0, abs_tol=1e-10)
                    if field in ("wasserstein", "negative_wasserstein") and got is not None and want is not None
                    else got == want
                )
            rows.append({"line": name, "cell": cell, "array_sha256": sha,
                         "network_sha256": actual["network_sha256"], "scores": scores,
                         "checks": comparisons})
    return {"ticket": "DLV-07", "python": sys.version.split()[0],
            "packages": {name: version(name) for name in ("causalbench", "numpy", "scipy", "scikit-learn")},
            "rows": rows, "pass": all(all(row["checks"].values()) for row in rows)}


if __name__ == "__main__":
    receipt = replay()
    print(json.dumps(receipt, indent=2, allow_nan=False))
    raise SystemExit(0 if receipt["pass"] else 1)
