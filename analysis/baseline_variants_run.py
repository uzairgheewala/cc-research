"""Run baseline variants the scoreboard runner (causalarena_methods.py, unchanged) does not cover, writing rows in the
same format so rescore_controls / decision_value read them unchanged (AB-01, AUD-33).

Variants
  pc        PC from a causal-learn copy given by --causal-learn (upstream PyPI wheel), stable, Fisher-z, alpha 0.05, with
            the collider rule set by --uc-rule / --uc-priority (0/2 = causal-learn default; 1/3 = maxP; 2/3 = definite maxP)
  gies      GIES with the released intervention targets (regime D+I): Gamella's `gies` 0.0.3 (pip install gies), Gaussian
            l0-penalised likelihood (BIC), phases forward/backward/turning. One environment per distinct intervened-cell
            pattern in the obs_int file (the observational rows are the environment with no targets). The released values
            are already standardised (causalarena_io). Gaussian jitter of sd --jitter (default 1e-6, seeded by crc32 of
            the file name, added before any column permutation) is added because formula files contain exact
            deterministic relations: a zero residual variance makes the score log(0) and GIES stops on a near-empty graph
            (checked 2026-10-12 on 5 + 5 files: jitter changes no semantic file and repairs the degenerate formula files).
            Output: an I-essential graph.
Same shuffle as the runner: seed + crc32(file name), the method sees permuted columns, the graph is mapped back.
Scores per file under the rules "random" (per-file seed crc32(file name)), "drop", "both", and "lower" in the index space
the method saw (earlier column -> later column; on released order this reads the answer).
Resumable (jobkit): finished files are skipped; --budget-s stops cleanly; --shard k/n splits work across processes.

  python analysis/baseline_variants_run.py --variant pc --causal-learn PATH --uc-rule 1 --uc-priority 3 --family semantic \
      --out analysis/results/methods/pc_upstream_maxp_semantic_obs_rel.json [--shuffle-seed 20261010]
  python analysis/baseline_variants_run.py --variant gies --family semantic --files-every 2 \
      --out analysis/results/methods/gies_semantic_obsint_rel.json [--shuffle-seed 20261010]
No model calls. Tickets: AUD-33, BEN-07, REP-07
"""
import argparse, contextlib, glob, io, json, os, signal, sys, time, zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402
from causalarena_load import load_any  # noqa: E402
import jobkit  # noqa: E402
import score_record as SR  # noqa: E402


def marks_from_cpdag(C):
    """C[i, j] = 1 and C[j, i] = 0: i -> j; both 1: undirected -> causal-learn endpoint marks M[i, j] (mark at i)."""
    d = C.shape[0]
    M = np.zeros((d, d), dtype=int)
    for i in range(d):
        for j in range(d):
            if C[i, j] and not C[j, i]:
                M[i, j], M[j, i] = -1, 1
            elif C[i, j] and C[j, i]:
                M[i, j] = M[j, i] = -1
    return M


def to_graph(M):
    """causal-learn marks -> committed arrows (i, j) and undecided pairs {(i, j): (mark_i, mark_j)} with i < j."""
    d = M.shape[0]
    directed, undecided = set(), {}
    for i in range(d):
        for j in range(i + 1, d):
            a, b = int(M[i, j]), int(M[j, i])
            if a == 0 and b == 0:
                continue
            if a == -1 and b == 1:
                directed.add((i, j))
            elif a == 1 and b == -1:
                directed.add((j, i))
            else:
                undecided[(i, j)] = (a, b)
    return directed, undecided


def environments(s, X):
    """Split rows by intervened-cell pattern: list of (targets, row indices); observational rows first."""
    I = s["intervened"]
    pats = {}
    for r in range(I.shape[0]):
        pats.setdefault(tuple(int(k) for k in np.where(I[r])[0]), []).append(r)
    keys = sorted(pats, key=lambda k: (len(k) > 0, k))
    return [(list(k), pats[k]) for k in keys]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", required=True, choices=("pc", "gies"))
    ap.add_argument("--causal-learn", default=None)
    ap.add_argument("--uc-rule", type=int, default=0)
    ap.add_argument("--uc-priority", type=int, default=2)
    ap.add_argument("--family", default="semantic")
    ap.add_argument("--root", default=str(HERE.parent / "external" / "causalarena"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--files-every", type=int, default=1)
    ap.add_argument("--shuffle-seed", type=int, default=None)
    ap.add_argument("--shard", default="0/1")
    ap.add_argument("--budget-s", type=float, default=0)
    ap.add_argument("--file-timeout-s", type=int, default=0,
                    help="per-file wall-clock limit; a file over it is a failed file (row kept, flagged, excluded from paired comparisons)")
    ap.add_argument("--jitter", type=float, default=1e-6, help="gies only: sd of seeded Gaussian jitter (0 = none)")
    a = ap.parse_args()
    regime_dir = "obs_int" if a.variant == "gies" else "obs_only"
    if a.variant == "pc":
        if not a.causal_learn:
            raise SystemExit("--causal-learn PATH is required for --variant pc")
        sys.path.insert(0, str(Path(a.causal_learn).resolve()))
        from causallearn.search.ConstraintBased.PC import pc
        import causallearn
        engine = "causal-learn at %s (%s)" % (Path(causallearn.__file__).parent.parent.name, getattr(causallearn, "__version__", "?"))
        method = "pc_upstream_uc%d_p%d" % (a.uc_rule, a.uc_priority)
    else:
        import gies
        engine = "gies %s (Gamella, PyPI)" % getattr(gies, "__version__", "0.0.3")
        method = "gies_targets"
    splits = json.load(open(HERE.parent / "plans" / "splits.json", encoding="utf-8"))["families"].get(a.family, {})
    files = sorted(glob.glob(os.path.join(a.root, "scm", a.family, "data", "%s_%s" % (a.family, regime_dir), "*.npz")))[::a.files_every]
    k, n = (int(x) for x in a.shard.split("/"))
    files = files[k::n]
    parts = jobkit.Parts(a.out)
    budget = jobkit.Budget(a.budget_s)
    for f in files:
        key = os.path.basename(f)
        if parts.has(key):
            continue
        if not budget.ok(90):
            break
        s = load_any(f)
        X, d = s["values"], len(s["node_ids"])
        if a.variant == "gies" and a.jitter:
            X = X + a.jitter * np.random.default_rng(zlib.crc32(key.encode())).standard_normal(X.shape)
        perm = list(range(d))
        if a.shuffle_seed is not None:
            perm = list(np.random.default_rng(a.shuffle_seed + zlib.crc32(key.encode())).permutation(d))
        pos = {int(v): i for i, v in enumerate(perm)}          # original variable -> column the method saw
        Xp = X[:, perm]
        t0, failed, n_env = time.time(), None, None

        def _alarm(signum, frame):
            raise TimeoutError("file exceeded --file-timeout-s %d" % a.file_timeout_s)
        if a.file_timeout_s:
            signal.signal(signal.SIGALRM, _alarm)
            signal.alarm(a.file_timeout_s)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                if a.variant == "pc":
                    M = pc(Xp, 0.05, "fisherz", stable=True, uc_rule=a.uc_rule, uc_priority=a.uc_priority, show_progress=False).G.graph
                else:
                    envs = environments(s, X)
                    n_env = len(envs)
                    data = [Xp[rows] for _, rows in envs]
                    targets = [[pos[t] for t in tg] for tg, _ in envs]
                    C, _ = gies.fit_bic(data, targets)
                    M = marks_from_cpdag((np.asarray(C) != 0).astype(int))
        except ImportError:
            raise
        except Exception as e:  # noqa: BLE001 - a failed file is data, scored as an empty graph (authors' runners do the same)
            M, failed = np.zeros((d, d), dtype=int), "%s: %s" % (type(e).__name__, e)
        finally:
            signal.alarm(0)
        secs = time.time() - t0
        directed, undecided = to_graph(np.asarray(M))
        back = lambda i: int(perm[i])
        directed = {(back(i), back(j)) for i, j in directed}
        undecided = {tuple(sorted((back(i), back(j)))): (m if back(i) < back(j) else m[::-1]) for (i, j), m in undecided.items()}
        truth = CA.true_edges(s["g"])
        und = {frozenset(p) for p in undecided}
        scores = {rule: CA.directed_scores(directed, und, truth, d, rule, seed=zlib.crc32(key.encode())) for rule in ("random", "drop", "both")}
        P = lambda e: (pos[e[0]], pos[e[1]])
        scores["lower"] = CA.directed_scores({P(e) for e in directed}, {frozenset(pos[i] for i in p) for p in und},
                                             {P(e) for e in truth}, d, "lower")
        scen = s["meta"].get("scenario_id")
        slug = next((sl for sl in splits.get("dev", []) + splits.get("test", []) if sl in key), None)
        split = "dev" if slug in splits.get("dev", []) else ("test" if slug in splits.get("test", []) else "all-public (measurement, no tuning)")
        r = SR.row(ticket="AUD-33", family=a.family, scenario=scen, file=key, method=method, regime="D+I" if a.variant == "gies" else "D",
                   columns_shuffled=a.shuffle_seed is not None, names="not applicable", supplier="causalarena", split=split,
                   metrics={"directed_f1": scores["random"]["f1"], "directed_precision": scores["random"]["precision"],
                            "directed_recall": scores["random"]["recall"], "shd": scores["random"]["shd"], "seconds": round(secs, 2)},
                   domain=s["meta"].get("domain_id"), d=d, failed=failed, true_edges=len(truth), shuffle_seed=a.shuffle_seed,
                   environments=n_env, directed_edges=sorted([list(e) for e in directed]),
                   undecided_pairs=sorted([[i, j, m[0], m[1]] for (i, j), m in undecided.items()]), scores=scores)
        parts.add(key, r)
    header = {"shard": a.shard, "method": method, "variant": a.variant, "uc_rule": a.uc_rule, "uc_priority": a.uc_priority,
              "family": a.family, "regime": "D+I" if a.variant == "gies" else "D", "files": len(files), "files_every": a.files_every,
              "shuffle_seed": a.shuffle_seed, "jitter": a.jitter if a.variant == "gies" else None, "file_timeout_s": a.file_timeout_s, "engine": engine, "env": jobkit.environment(), "ticket": "AUD-33"}
    jobkit.finish(parts, header, len(files))


if __name__ == "__main__":
    main()
