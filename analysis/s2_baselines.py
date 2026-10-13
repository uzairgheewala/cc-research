"""BND-08 part 2b: plain data-only baselines on the S2 files exactly as the agent sees them (shuffled columns), for M4.

  python analysis/s2_baselines.py --out analysis/results/s2_baselines/s2_baselines.json

Per S2 family, on the neutral arm's CSV (numbers byte-identical in all three arms):
  pc      causal-learn (vendored 0.1.3.8) stable PC, Fisher-z, alpha 0.05
  gesbic  GES, Gaussian BIC (lambda = log(n)/2), forward/backward/turning (`ges` 1.1.0), on z-scored columns
Scores against the reference read by data (datasets/suite_q1s2/_reference/<family>_by_data.npy, repo convention
M[e, c] == 1 means c -> e): adjacency F1, and directed-edge F1 under "drop" (committed arrows only: the same metric as the
agent's stage scores, cc_graph.score dir_f1), "random" (per-family seed) and "lower" (earlier CSV column -> later; on S2 the
CSV order is shuffled, so this no longer reads the answer). M4 compares the agent's neutral-arm S3 directed F1 with "pc"
under "drop".
"""
import argparse, json, os, sys, time, zlib, contextlib, io
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
REPO = Path(os.environ.get("CC_REPO", ROOT.parent / "Causal-Copilot"))
sys.path[:0] = [str(REPO / "externals" / "causal-learn")]
from causalarena_methods import run, marks_to_graph  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    m = json.loads((ROOT / "datasets" / "suite_q1s2" / "MAPPING.json").read_text(encoding="utf-8"))
    rows = []
    for fam, f in sorted(m["families"].items()):
        code = f["arms"]["neutral"]
        X = pd.read_csv(ROOT / "datasets" / "suite_q1s2" / code / ("%s.csv" % code)).values.astype(float)
        R = np.load(ROOT / "datasets" / "suite_q1s2" / "_reference" / ("%s_by_data.npy" % fam))
        d = R.shape[0]
        truth = {(int(c), int(e)) for e, c in np.argwhere(R == 1)}
        tadj = {frozenset(e) for e in truth}
        for method in ("pc", "gesbic"):
            t = time.time()
            failed = None
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    A = run(method, X)
            except np.linalg.LinAlgError as e:          # scored as an empty graph, as the authors' runners do
                A, failed = np.zeros((d, d), dtype=int), "%s: %s" % (type(e).__name__, e)
            directed, undecided = marks_to_graph(A)
            und = {frozenset(p) for p in undecided}
            padj = {frozenset(e) for e in directed} | und
            tp = len(padj & tadj)
            P, Rc = (tp / len(padj) if padj else 0.0), tp / len(tadj)
            sc = {rule: CA.directed_scores(directed, und, truth, d, rule, seed=zlib.crc32(fam.encode())) for rule in ("drop", "random", "lower")}
            rows.append({"family": fam, "scenario_id": f["scenario_id"], "arm_csv": code, "method": method, "d": d, "true_edges": len(truth),
                         "seconds": round(time.time() - t, 1), "adj_f1": 2 * P * Rc / (P + Rc) if P + Rc else 0.0,
                         "dir_f1": {k: v["f1"] for k, v in sc.items()}, "shd": {k: v["shd"] for k, v in sc.items()},
                         "directed": len(directed), "undecided": len(und), "failed": failed})
            print(fam, method, round(rows[-1]["adj_f1"], 3), {k: round(v, 3) for k, v in rows[-1]["dir_f1"].items()}, flush=True)
    out = {"mapping_sha256": __import__("hashlib").sha256((ROOT / "datasets" / "suite_q1s2" / "MAPPING.json").read_bytes()).hexdigest(),
           "rows": rows}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
