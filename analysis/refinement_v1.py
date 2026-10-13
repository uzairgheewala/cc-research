"""Refinement v1 (BND-09 / BND-10): a bootstrap stage that keeps what the data found. No model call; built outside the repo.

Input: what the pipeline already records for one run - the algorithm output S0 (repo matrix convention, M[i, j] = 1 means
j -> i; codes 2-6 for non-directed marks) and the seven resample-frequency tables of postprocess/judge_functions.bootstrap
(M[i, j] = frequency of the type on j -> i; symmetric types are computed with OR over both cells, so T[a, b] is the pair's
frequency). Output: a graph in the same convention, and a source for every adjacent pair.

The rule (thresholds fixed in the design note before any replay, bundle2_onward_design.md section 6; not tuned):
  connected(a, b) = 1 - none_existence[a, b]
  an adjacency of S0 is kept iff connected >= KEEP (0.5); an absent pair is added iff connected >= ADD (0.9)
  the type of a kept or added pair is the commonest of the nine typed outcomes among resamples
    (a->b, b->a, undirected, bidirected, a o-> b, b o-> a, a o- b, b o- a, o-o);
  a direction is committed only when a directed outcome is strictly the commonest; on a tie the algorithm's own type wins if it
  is among the tied, otherwise the first of the tied in the order undirected, o-o, bidirected, a o-> b, b o-> a, a o- b,
  b o- a, a->b, b->a (non-directed first: no direction is committed on a tie);
  if no typed outcome was ever observed (only conflicting codes), a kept pair keeps the algorithm's type, an added pair is undirected.
Sources: "algorithm" (kept, same type), "algorithm; type from bootstrap" (kept, retyped), "bootstrap: added".

Modes
  python analysis/refinement_v1.py dev  --out analysis/results/refinement_v1/dev.json     # recorded live runs + dev replay files
  python analysis/refinement_v1.py freeze                                                  # writes RULE.json (sha256 of this file)
  python analysis/refinement_v1.py test --replay jobs/bootstrap_replay_ca_test/out/replay_test.json   (BND-10; refuses unless
        RULE.json matches this file; appends to the access log)
Predictions (from the design note; verdicts on dev are labelled dev):
  R1  v1 adjacency F1 >= algorithm output - 0.02      SUPPORTED if in >= 90% of files; REFUTED if < 70%
  R2  v1 adjacency F1 > the pipeline's S1             SUPPORTED if in >= 90% of files; REFUTED if < 70%
  R3  v1 directed-edge F1 (random orientation of undecided pairs, per-file seed) minus the algorithm's:
                                                       SUPPORTED if mean >= -0.01; REFUTED if mean <= -0.05
"""
import argparse
import datetime
import glob
import hashlib
import json
import os
import pickle
import sys
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import cc_graph as G  # noqa: E402
import causalarena_io as CA  # noqa: E402
from lineage import step_bootstrap  # noqa: E402

KEEP, ADD = 0.5, 0.9
ORDER = ["undirected", "o-o", "bidirected", "a o-> b", "b o-> a", "a o- b", "b o- a", "a->b", "b->a"]
RULE = HERE / "results" / "refinement_v1" / "RULE.json"
ACCESS = HERE / "results" / "refinement_v1" / "access_log.jsonl"


def typed_freqs(boot, a, b):
    T = {k: np.asarray(v, dtype=float) for k, v in boot.items()}
    return {"a->b": T["certain_edges"][b, a], "b->a": T["certain_edges"][a, b], "undirected": T["uncertain_edges"][a, b],
            "bidirected": T["bi_edges"][a, b], "a o-> b": T["half_certain_edges"][b, a], "b o-> a": T["half_certain_edges"][a, b],
            "a o- b": T["half_uncertain_edges"][b, a], "b o- a": T["half_uncertain_edges"][a, b], "o-o": T["none_edges"][a, b]}


def put(M, a, b, t):
    if t == "a->b":
        M[b, a] = 1
    elif t == "b->a":
        M[a, b] = 1
    elif t == "undirected":
        M[a, b] = 2
    elif t == "bidirected":
        M[a, b] = 3
    elif t == "a o-> b":
        M[b, a] = 4
    elif t == "b o-> a":
        M[a, b] = 4
    elif t == "a o- b":
        M[b, a] = 5
    elif t == "b o- a":
        M[a, b] = 5
    elif t == "o-o":
        M[a, b] = 6
    else:
        raise ValueError(t)


def v1(S0, boot):
    S0 = np.asarray(S0)
    p = S0.shape[0]
    M = np.zeros((p, p), dtype=int)
    sources = []
    none = np.asarray(boot["none_existence"], dtype=float)
    for a, b in G.pairs(p):
        conn = 1.0 - float(none[a, b])
        adj0 = G.is_adjacent(S0, a, b)
        if not ((adj0 and conn >= KEEP) or (not adj0 and conn >= ADD)):
            continue
        t0 = G.pair_type(S0, a, b) if adj0 else None
        fr = typed_freqs(boot, a, b)
        top = max(fr.values())
        if top <= 0:
            t = t0 if (t0 in ORDER) else "undirected"
            if adj0 and t0 not in ORDER:          # conflicting / mixed codes in S0: copy the two cells unchanged
                M[a, b], M[b, a] = S0[a, b], S0[b, a]
                sources.append({"pair": [a, b], "type": t0, "source": "algorithm", "connected": round(conn, 4)})
                continue
        else:
            tied = [k for k in ORDER if abs(fr[k] - top) < 1e-12]
            t = t0 if t0 in tied else tied[0]
        put(M, a, b, t)
        src = "bootstrap: added" if not adj0 else ("algorithm" if t == t0 else "algorithm; type from bootstrap")
        sources.append({"pair": [a, b], "type": t, "source": src, "connected": round(conn, 4), "type_frequency": round(float(fr.get(t, 0.0)), 4)})
    return M, sources


def to_sets(M):
    p = M.shape[0]
    directed, und = set(), set()
    for a, b in G.pairs(p):
        t = G.pair_type(M, a, b)
        if t == "a->b":
            directed.add((a, b))
        elif t == "b->a":
            directed.add((b, a))
        elif t != "none":
            und.add(frozenset((a, b)))
    return directed, und


def scores(M, E, p, seed):
    s = G.score(M, E, p)
    d, u = to_sets(np.asarray(M))
    r = CA.directed_scores(d, u, set(E), p, "random", seed=seed)
    return {"adj_f1": s["adj_f1"] or 0.0, "dir_f1_committed": s["dir_f1"] or 0.0, "dir_f1_random": r["f1"]}


def evaluate(items):
    rows = []
    for it in items:
        S0, boot, buckets, E, p = it["S0"], it["boot"], it["buckets"], it["E"], it["p"]
        S1, _, _ = step_bootstrap(np.asarray(S0), buckets) if buckets is not None else (np.asarray(it["S1"]), None, None)
        V, src = v1(S0, boot)
        seed = zlib.crc32(it["key"].encode())
        sc = {"S0": scores(S0, E, p, seed), "S1": scores(S1, E, p, seed), "v1": scores(V, E, p, seed)}
        S0a = np.asarray(S0)
        nd = [(a, b) for a, b in G.pairs(p) if G.is_adjacent(S0a, a, b) and G.pair_type(S0a, a, b) not in ("a->b", "b->a")]
        surv = {"nondirected_in_S0": len(nd), "survive_S1": sum(G.is_adjacent(np.asarray(S1), a, b) for a, b in nd),
                "survive_v1": sum(G.is_adjacent(V, a, b) for a, b in nd)}
        rows.append({"key": it["key"], "group": it["group"], "p": p, "scores": sc, "nondirected_survival": surv,
                     "sources": {k: sum(1 for s in src if s["source"] == k) for k in ("algorithm", "algorithm; type from bootstrap", "bootstrap: added")},
                     "every_edge_has_source": len(src) == int(sum(G.is_adjacent(V, a, b) for a, b in G.pairs(p)))})
    n = len(rows)
    r1 = sum(r["scores"]["v1"]["adj_f1"] >= r["scores"]["S0"]["adj_f1"] - 0.02 for r in rows)
    r2 = sum(r["scores"]["v1"]["adj_f1"] > r["scores"]["S1"]["adj_f1"] for r in rows)
    r3 = float(np.mean([r["scores"]["v1"]["dir_f1_random"] - r["scores"]["S0"]["dir_f1_random"] for r in rows])) if rows else None
    v = lambda share: "SUPPORTED" if share >= 0.9 else ("REFUTED" if share < 0.7 else "INCONCLUSIVE")
    return rows, {"files": n, "R1": {"hits": r1, "share": r1 / n if n else None, "verdict": v(r1 / n) if n else None},
                  "R2": {"hits": r2, "share": r2 / n if n else None, "verdict": v(r2 / n) if n else None},
                  "R3": {"mean_difference": r3, "verdict": None if r3 is None else ("SUPPORTED" if r3 >= -0.01 else "REFUTED" if r3 <= -0.05 else "INCONCLUSIVE")},
                  "all_edges_sourced": all(r["every_edge_has_source"] for r in rows),
                  "nondirected_survival": {k: sum(r["nondirected_survival"][k] for r in rows) for k in ("nondirected_in_S0", "survive_S1", "survive_v1")}}


def mapping_index():
    idx = {}
    for mp in [ROOT / "datasets" / "MAPPING.json"] + sorted((ROOT / "datasets").glob("suite_*/MAPPING.json")):
        m = json.loads(mp.read_text(encoding="utf-8"))
        for code, arm in m["arms"].items():
            if arm.get("reference_by_data"):
                idx[arm["dataset_arg"]] = (mp.parent / arm["reference_by_data"], m.get("suite", "pass4b"))
    return idx


def live_items():
    idx = mapping_index()
    items, seen = [], set()
    for meta_f in sorted(glob.glob(str(ROOT / "runs" / "*" / "meta.json"))):
        meta = json.load(open(meta_f, encoding="utf-8"))
        if meta.get("stub_llm"):
            continue
        ds = meta.get("dataset") or meta.get("dataset_arg") or ""
        if ds.startswith("/research/"):                # recorded as the container path; MAPPINGs use the plan's form
            ds = "research:" + ds[len("/research/"):]
        if ds not in idx:
            continue
        if "suite_q1s2" in str(idx[ds][0]):          # S2 runs are test data (F3): never in the dev set
            continue
        rd = Path(meta_f).parent
        bf = sorted(rd.glob("artifacts/*_bootstrap.pkl"))
        rf = sorted(rd.glob("artifacts/*_bootstrap_recommend.pkl"))
        if not bf or not rf:
            continue
        a = pickle.load(open(bf[0], "rb"))
        if a.get("error"):
            continue
        S0 = np.asarray(a["args_before"]["kwargs"]["full_graph"])
        boot = a["ret"][1]
        buckets = pickle.load(open(rf[0], "rb"))["ret"]
        sig = hashlib.sha256(S0.tobytes() + b"".join(np.asarray(boot[k]).tobytes() for k in sorted(boot)) + ds.encode()).hexdigest()
        if sig in seen:                                # identical (data, algorithm output, bootstrap tables): count once
            continue
        seen.add(sig)
        ref = np.load(idx[ds][0])
        items.append({"key": rd.name, "group": "live:" + idx[ds][1], "S0": S0, "boot": boot, "buckets": buckets,
                      "E": G.truth_edges(ref), "p": S0.shape[0]})
    return items


def replay_items(path, group):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    out = []
    for r in d["rows"]:
        if r.get("status") != "ok":
            continue
        s = CA.load(ROOT / "external" / "causalarena" / "scm" / "semantic" / "data" / "semantic_obs_only" / r["file"])
        out.append({"key": r["file"], "group": group, "S0": np.asarray(r["S0"]), "boot": r["boot"], "buckets": None,
                    "S1": r["S1"], "E": G.truth_edges(CA.to_repo_matrix(s["g"])), "p": len(r["S0"])})
    return out


def file_sha():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("dev", "freeze", "test"))
    ap.add_argument("--out", default=None)
    ap.add_argument("--replay", default=None)
    a = ap.parse_args()
    sys.path[:0] = [str(ROOT.parent / "Causal-Copilot"), str(ROOT.parent / "Causal-Copilot" / "externals" / "causal-learn")]
    if a.mode == "freeze":
        if RULE.exists():
            sys.exit("already frozen: %s" % json.loads(RULE.read_text())["sha256"])
        RULE.write_text(json.dumps({"file": "analysis/refinement_v1.py", "sha256": file_sha(), "KEEP": KEEP, "ADD": ADD,
                                    "frozen_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"}, indent=1) + "\n")
        print("frozen", file_sha())
        return
    if a.mode == "test":
        if not RULE.exists() or json.loads(RULE.read_text())["sha256"] != file_sha():
            sys.exit("refused: the rule is not frozen, or this file differs from the frozen rule")
        with open(ACCESS, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z", "mode": "test",
                                 "replay": a.replay, "rule_sha256": file_sha()}) + "\n")
        items = replay_items(a.replay, "replay:test")
    else:
        items = live_items()
        dev_replay = ROOT / "jobs" / "bootstrap_replay_ca_dev" / "out" / "replay_dev.json"
        if dev_replay.exists():
            items += replay_items(dev_replay, "replay:dev")
    rows, summary = evaluate(items)
    by_group = {}
    for g in sorted({r["group"] for r in rows}):
        _, by_group[g] = evaluate([it for it in items if it["group"] == g])
    out = {"mode": a.mode, "rule_sha256": file_sha(), "KEEP": KEEP, "ADD": ADD, "summary": summary, "by_group": by_group, "rows": rows}
    dest = Path(a.out or (HERE / "results" / "refinement_v1" / ("%s.json" % a.mode)))
    dest.write_text(json.dumps(out, indent=1, default=float) + "\n", encoding="utf-8")
    print(json.dumps({"summary": summary, "by_group": {g: {k: v.get("verdict") if isinstance(v, dict) else v for k, v in s.items()} for g, s in by_group.items()}}, indent=1))


if __name__ == "__main__":
    main()
