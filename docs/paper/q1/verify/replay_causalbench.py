"""Read-only CausalBench score replay for selected Q1 checkpoint rows (DLV-07)."""
import hashlib
import json
import math
import sys
from importlib.metadata import version

from statistics import mean
from analysis.ben13 import evaluate, methods
from analysis.ben13.run import DATA, PREREG, OUT
from causalscbench.data_access.utils.splitting import DatasetSplitter
from causalscbench.evaluation.statistical_evaluation import Evaluator

EXPECTED_ARRAYS = {
    "k562": "513d763a466efcbeb9cdd30f219c6162e857035d3af1e7f574dbb7103764c57a",
    "rpe1": "a1f728261be13972e6739345dc70db6dde10e6248aef04fa3b2261ffec18d9ba",
}
CELLS = ("md_k1000", "md_k5000", "oracle_k1000") + tuple(
    f"random_k{k}" + (f"_s{seed}" if seed else "")
    for k in (1000, 5000) for seed in range(20)
)
FIELDS = ("tp", "fp", "edges", "wasserstein", "for", "negative_wasserstein")


def replay():
    if version("causalbench") != "1.1.2":
        raise RuntimeError("Replay requires causalbench==1.1.2")
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    protocol = prereg["protocol"]
    published = prereg["published"]
    tolerance = prereg["tolerance"]
    rows = []
    for name, expected_sha in EXPECTED_ARRAYS.items():
        with (DATA / f"dataset_{name}_filtered.npz").open("rb") as source:
            sha = hashlib.file_digest(source, "sha256").hexdigest()
        if sha != expected_sha:
            raise ValueError(f"Unexpected filtered-array bytes for {name}: {sha}")
        print(f"Verified {name} arrays", file=sys.stderr, flush=True)
        sp = DatasetSplitter(str(DATA / f"dataset_{name}_filtered.npz"), 1.0)
        train, train_iv, genes = sp.get_interventional()
        test, test_iv, _ = sp.get_test_data()
        genes = list(map(str, genes))
        ev = Evaluator(test, list(test_iv), genes)
        by_train = methods.mean_difference_scores(train, list(train_iv), genes)
        by_test = methods.mean_difference_scores(test, list(test_iv), genes)
        for cell in CELLS:
            print(f"Scoring {name} {cell}", file=sys.stderr, flush=True)
            expected = json.loads((OUT / name / f"{cell}.json").read_text(encoding="utf-8"))
            kind, budget, *tail = cell.split("_")
            k = int(budget[1:])
            if kind == "random":
                net = methods.random_network(genes, k, int(tail[0][1:]) if tail else 0)
            else:
                net = methods.top_k(by_train if kind == "md" else by_test, k)
            network_bytes = "\n".join(f"{a}\t{b}" for a, b in sorted(set(net))).encode()
            actual = {
                "network_sha256": hashlib.sha256(network_bytes).hexdigest(),
                "statistical": evaluate.statistical(
                    ev, net, protocol["max_path_length"], protocol["omission_estimation_size"]
                ),
            }
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
    summary = {}
    for name in EXPECTED_ARRAYS:
        line = {r["cell"]: {key: v["actual"] for key, v in r["scores"].items()}
                for r in rows if r["line"] == name}
        checks = {}
        for k in (1000, 5000):
            row = f"md_k{k}"
            available = [metrics["for"] for cell, metrics in line.items()
                         if (cell == f"random_k{k}" or cell.startswith(f"random_k{k}_"))
                         and metrics["for"] is not None]
            random_for = mean(available) if available else None
            md_for = line[row]["for"]
            checks[row] = {
                "published_within_tolerance": all(abs(line[row][m] - published[name][row][m]) <= tolerance[m]
                                                  for m in ("wasserstein", "for")),
                "random_for_defined": len(available),
                "random_for_mean": random_for,
                "md_for": md_for,
                "within_random_for_margin": None if random_for is None or md_for is None
                                            else abs(md_for - random_for) <= tolerance["for"],
            }
        summary[name] = {"echo_ratio_k1000": line["md_k1000"]["wasserstein"] / line["oracle_k1000"]["wasserstein"],
                         "comparisons": checks}
    return {"ticket": "DLV-07", "python": sys.version.split()[0], "paper_summary": summary,
            "packages": {name: version(name) for name in ("causalbench", "numpy", "scipy", "scikit-learn")},
            "rows": rows, "pass": all(all(row["checks"].values()) for row in rows)}


if __name__ == "__main__":
    receipt = replay()
    print(json.dumps(receipt, indent=2, allow_nan=False))
    raise SystemExit(0 if receipt["pass"] else 1)
