"""BND-06 side check: on which public files does upstream causal-learn's PC (Fisher-z) raise, where the Causal-Copilot vendored
build does not? The vendored skeleton step catches ValueError from the CI test and falls back to KCI
(externals/causal-learn/causallearn/utils/PCUtils/SkeletonDiscovery.py, _process_node_pair: `except ValueError` ->
backup_indep_test, built as CIT(data, method='kci')); upstream raises "Data correlation matrix is singular" instead, and the
authors' runner scores a raising method as an empty graph (TabCausal run_pc.py: except -> zeros).

  PYTHONPATH=<upstream causal-learn> python analysis/pc_upstream_failure_check.py --family formula \
      --rows analysis/results/methods/pc_formula_obs_rel.json --out analysis/results/methods/pc_upstream_failures_formula.json

For every file: does upstream PC (stable, Fisher-z, alpha 0.05, released order) raise? Then the family mean F1 of our vendored
PC rows (--rows) is recomputed with the files that raise upstream set to an empty graph, under the random and lower rules:
what our row would be if PC had failed where upstream fails. No LLM.
"""
import argparse
import contextlib
import io
import json
import signal
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import bnd06_summary as B  # noqa: E402
import causalarena_io as CA  # noqa: E402
from causalarena_load import load_any  # noqa: E402

DIRS = {"semantic": "semantic/data/semantic_obs_only", "formula": "formula/data/formula_obs_only",
        "synthetic": "synthetic/data/synthetic_obs_only"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=sorted(DIRS))
    ap.add_argument("--rows", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout-s", type=int, default=300)
    a = ap.parse_args()
    import causallearn
    from causallearn.search.ConstraintBased.PC import pc
    data = json.loads(Path(a.rows).read_text(encoding="utf-8"))
    root = HERE.parent / "external" / "causalarena" / "scm" / DIRS[a.family]

    def _alarm(signum, frame):
        raise TimeoutError("over %d s" % a.timeout_s)
    signal.signal(signal.SIGALRM, _alarm)
    per_file, rows_if = {}, []
    for r in data["rows"]:
        s = load_any(root / r["file"])
        t0 = time.time()
        err = None
        try:
            signal.alarm(a.timeout_s)
            with contextlib.redirect_stdout(io.StringIO()):
                pc(s["values"], alpha=0.05, indep_test="fisherz", stable=True, show_progress=False)
        except Exception as e:  # noqa: BLE001
            err = "%s: %s" % (type(e).__name__, str(e)[:100])
        finally:
            signal.alarm(0)
        per_file[r["file"]] = {"upstream_error": err, "seconds": round(time.time() - t0, 2)}
        rr = dict(r)
        if err:
            d = r["d"]
            truth = CA.true_edges(s["g"])
            rr["scores"] = {rule: CA.directed_scores(set(), set(), truth, d, rule, seed=0) for rule in ("random", "lower")}
        rows_if.append(rr)
    raised = sorted(f for f, v in per_file.items() if v["upstream_error"])
    out = {"family": a.family, "rows_file": a.rows, "upstream_causallearn": causallearn.__file__,
           "files": len(per_file), "files_upstream_raises": len(raised),
           "scenarios_with_any_raise": len({r["scenario"] for r in data["rows"] if r["file"] in raised}),
           "error_messages": sorted({v["upstream_error"].split(":")[0] + ": " + v["upstream_error"].split(":")[1][:60] for v in per_file.values() if v["upstream_error"]}),
           "vendored_rows_family_mean_f1": {rule: round(B.fam_mean(data["rows"], rule)[0], 4) for rule in ("random", "lower")},
           "vendored_rows_with_upstream_failures_as_empty_f1": {rule: round(B.fam_mean(rows_if, rule)[0], 4) for rule in ("random", "lower")},
           "vendored_rows_with_upstream_failures_as_empty_shd": {rule: round(B.fam_mean(rows_if, rule, "shd")[0], 3) for rule in ("random", "lower")},
           "per_file": per_file}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "per_file"}, indent=1))


if __name__ == "__main__":
    main()
