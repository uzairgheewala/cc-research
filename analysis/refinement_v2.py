"""Refinement v2 (BND-11): the data part never deletes the algorithm's adjacencies; model answers only where the data are silent.

Why v2 differs from v1 in its data part (decided 2026-10-12, after the BND-10 test read; see bnd09_bnd10_refinement.md):
on the live S2 tables v1's KEEP rule removed 120 algorithm adjacencies with resample frequency < 0.5, of which 50 were true,
so v1 fell below the algorithm (R1). Because this change was made after seeing test data, the data part of v2 gets a fresh
held-out set: the formula family's test split (jobs/bootstrap_replay_ca_formula_test.json; never run before the freeze).

Data part (v2d), from what the pipeline records for one run (S0 and the seven bootstrap tables, repo matrix convention):
  every adjacency of S0 is kept; an absent pair is added iff connected = 1 - none_existence >= ADD (0.9);
  the type of a kept or added pair is chosen exactly as in v1 (refinement_v1.py, imported unchanged): the commonest of the nine
  typed outcomes, ties to the algorithm's type, then to the non-directed types; no typed outcome: the algorithm's type kept.
Names part (v2 = v2d + names), only for pairs v2d leaves adjacent and not directed, excluding bidirected (a latent cause by
the data) and conflicting/mixed codes:
  three paraphrased questions to the model, each answered as JSON {"direction": "A->B" | "B->A" | "unknown"}; a reply that
  is not exactly that is retried once, then counts as an abstention (no crash path, CAP-10);
  a direction is used only if all three answers give it, it is compatible with the marks the data set (an arrowhead or tail
  of a PAG mark is never contradicted: for "a o-> b" only a->b; for "a o- b" only b->a), and adding it to the committed
  arrows creates no directed cycle (pairs taken in a fixed order: sorted by index); every such edge has source "names".
  Separating sets are not recorded by the pipeline for the bootstrap step, so the check against them is reported as not done.

Predictions (written before any answer or any formula replay exists; thresholds as in BND-09/10 and plans/q1_dag.json):
  data part, held-out = formula test replay (and dev = BND-09's dev set):
  R1 v2d adjacency F1 >= S0 - 0.02 in >= 90% of files (refuted < 70%)
  R2 v2d adjacency F1 > S1 (the pipeline's bootstrap step) in >= 90% (refuted < 70%)
  R3 mean directed F1 (undecided random, per-file seed) v2d - S0 >= -0.01 (refuted <= -0.05)
  names part, on the 30 recorded S2 live tables (10 families x real / neutral / swapped), scored against the data's reference:
  R4 neutral names: v2 == v2d (0 name-sourced edges) in >= 9 of 10 families (refuted if more than 2 have any)
  R5 swapped names: v2 directed F1 within 0.05 of v2d in >= 8 of 10 (refuted <= 5)
  R6 real names: v2 directed F1 > v2d in >= 8 of 10 (refuted <= 5)
  (the plan file wrote R4-R6 against v1; v2d replaces v1 as the base, recorded here before any answer existed)

Modes
  python analysis/refinement_v2.py dev                         # data part on BND-09's dev set -> results/refinement_v2/dev.json
  python analysis/refinement_v2.py freeze                      # RULE.json: sha256 of this file and of refinement_v1.py
  python analysis/refinement_v2.py requests --label s2         # plans/bnd11_names_requests.jsonl (what the model will be asked)
  python analysis/refinement_v2.py apply --answers FILE        # names part -> results/refinement_v2/names_s2.json (R4-R6)
  python analysis/refinement_v2.py test --replay jobs/bootstrap_replay_ca_formula_test/out/replay_formula_test.json
                                                               # data part held-out (refuses unless frozen; access log)
"""
import argparse
import datetime
import hashlib
import json
import sys
import zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import cc_graph as G  # noqa: E402
import refinement_v1 as V1  # noqa: E402   (frozen; imported unchanged)

ADD = V1.ADD
OUTD = HERE / "results" / "refinement_v2"
RULE = OUTD / "RULE.json"
ACCESS = OUTD / "access_log.jsonl"
ASKABLE = {"undirected", "o-o", "a o-> b", "b o-> a", "a o- b", "b o- a"}
COMPATIBLE = {"undirected": {"a->b", "b->a"}, "o-o": {"a->b", "b->a"}, "a o-> b": {"a->b"}, "b o-> a": {"b->a"},
              "a o- b": {"b->a"}, "b o- a": {"a->b"}}
PARAPHRASES = [
    "Consider two variables in a dataset: A = \"{a}\" and B = \"{b}\". Based only on what the names mean, which causes which? "
    "Reply with JSON only: {{\"direction\": \"A->B\"}}, {{\"direction\": \"B->A\"}} or {{\"direction\": \"unknown\"}}.",
    "Variable A is \"{a}\". Variable B is \"{b}\". If one of them is a direct cause of the other, which direction is it? "
    "If the names do not tell you, say unknown. Answer as JSON only: {{\"direction\": \"A->B\" | \"B->A\" | \"unknown\"}}.",
    "From domain knowledge about the names alone: does \"{a}\" (A) influence \"{b}\" (B), or does B influence A? "
    "Return JSON only, one of {{\"direction\": \"A->B\"}}, {{\"direction\": \"B->A\"}}, {{\"direction\": \"unknown\"}}.",
]
VALID = {"A->B", "B->A", "unknown"}


def v2d(S0, boot):
    S0 = np.asarray(S0)
    p = S0.shape[0]
    M = np.zeros((p, p), dtype=int)
    sources = []
    none = np.asarray(boot["none_existence"], dtype=float)
    for a, b in G.pairs(p):
        conn = 1.0 - float(none[a, b])
        adj0 = G.is_adjacent(S0, a, b)
        if not (adj0 or conn >= ADD):
            continue
        t0 = G.pair_type(S0, a, b) if adj0 else None
        fr = V1.typed_freqs(boot, a, b)
        top = max(fr.values())
        if top <= 0 or (adj0 and t0 not in V1.ORDER):
            if adj0 and t0 not in V1.ORDER:
                M[a, b], M[b, a] = S0[a, b], S0[b, a]
                sources.append({"pair": [a, b], "type": t0, "source": "algorithm", "connected": round(conn, 4)})
                continue
            t = t0 if t0 in V1.ORDER else "undirected"
        else:
            tied = [k for k in V1.ORDER if abs(fr[k] - top) < 1e-12]
            t = t0 if t0 in tied else tied[0]
        V1.put(M, a, b, t)
        src = "bootstrap: added" if not adj0 else ("algorithm" if t == t0 else "algorithm; type from bootstrap")
        sources.append({"pair": [a, b], "type": t, "source": src, "connected": round(conn, 4)})
    return M, sources


def parse_reply(text):
    """The direction in a reply, or None if the reply is not exactly the JSON asked for."""
    try:
        d = json.loads(text)
    except (TypeError, ValueError):
        return None
    if not isinstance(d, dict) or set(d) != {"direction"} or d["direction"] not in VALID:
        return None
    return d["direction"]


def committed(M):
    p = M.shape[0]
    out = set()
    for a, b in G.pairs(p):
        t = G.pair_type(M, a, b)
        if t == "a->b":
            out.add((a, b))
        elif t == "b->a":
            out.add((b, a))
    return out


def creates_cycle(edges, new):
    a, b = new                          # adding a -> b closes a cycle iff b already reaches a
    ch = {}
    for x, y in edges:
        ch.setdefault(x, []).append(y)
    seen, stack = set(), [b]
    while stack:
        v = stack.pop()
        if v == a:
            return True
        for c in ch.get(v, ()):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return False


def apply_names(M, answers_for_pair):
    """answers_for_pair: {(a, b): [direction or None] * 3}. Returns the v2 graph and one record per asked pair."""
    V = np.array(M, dtype=int)
    edges = committed(V)
    recs = []
    for (a, b) in sorted(answers_for_pair):
        t = G.pair_type(V, a, b)
        ans = answers_for_pair[(a, b)]
        rec = {"pair": [a, b], "type_by_data": t, "answers": ans, "used": False}
        if t not in ASKABLE:
            rec["why"] = "pair not askable in the v2d graph"
        elif any(x is None for x in ans):
            rec["why"] = "abstained (invalid reply after one retry)"
        elif len(set(ans)) != 1 or ans[0] == "unknown":
            rec["why"] = "paraphrases disagree or unknown"
        else:
            d = "a->b" if ans[0] == "A->B" else "b->a"
            new = (a, b) if d == "a->b" else (b, a)
            if d not in COMPATIBLE[t]:
                rec["why"] = "contradicts the mark set by the data"
            elif creates_cycle(edges, new):
                rec["why"] = "would create a directed cycle"
            else:
                V[a, b], V[b, a] = 0, 0
                V1.put(V, a, b, d)
                edges.add(new)
                rec.update({"used": True, "direction": d, "source": "names"})
        recs.append(rec)
    return V, recs


def evaluate(items, base="v2d"):
    rows = []
    for it in items:
        S0 = np.asarray(it["S0"])
        if it.get("S1") is not None:
            S1 = np.asarray(it["S1"])
        else:
            S1, _, _ = V1.step_bootstrap(S0, it["buckets"])
        V, src = v2d(S0, it["boot"])
        seed = zlib.crc32(it["key"].encode())
        sc = {"S0": V1.scores(S0, it["E"], it["p"], seed), "S1": V1.scores(np.asarray(S1), it["E"], it["p"], seed),
              "v2d": V1.scores(V, it["E"], it["p"], seed)}
        rows.append({"key": it["key"], "group": it["group"], "p": it["p"], "scores": sc,
                     "sources": {k: sum(1 for s in src if s["source"] == k) for k in ("algorithm", "algorithm; type from bootstrap", "bootstrap: added")},
                     "every_edge_has_source": len(src) == int(sum(G.is_adjacent(V, a, b) for a, b in G.pairs(it["p"])))})
    n = len(rows)
    share = lambda k: k / n if n else None
    v = lambda s: None if s is None else ("SUPPORTED" if s >= 0.9 else ("REFUTED" if s < 0.7 else "INCONCLUSIVE"))
    r1 = sum(r["scores"]["v2d"]["adj_f1"] >= r["scores"]["S0"]["adj_f1"] - 0.02 for r in rows)
    r2 = sum(r["scores"]["v2d"]["adj_f1"] > r["scores"]["S1"]["adj_f1"] for r in rows)
    r3 = float(np.mean([r["scores"]["v2d"]["dir_f1_random"] - r["scores"]["S0"]["dir_f1_random"] for r in rows])) if rows else None
    means = {s: {k: round(float(np.mean([r["scores"][s][k] for r in rows])), 4) for k in ("adj_f1", "dir_f1_random", "dir_f1_committed")}
             for s in ("S0", "S1", "v2d")} if rows else {}
    return rows, {"files": n, "R1": {"hits": r1, "share": share(r1), "verdict": v(share(r1))},
                  "R2": {"hits": r2, "share": share(r2), "verdict": v(share(r2))},
                  "R3": {"mean_difference": r3, "verdict": None if r3 is None else ("SUPPORTED" if r3 >= -0.01 else "REFUTED" if r3 <= -0.05 else "INCONCLUSIVE")},
                  "means": means, "all_edges_sourced": all(r["every_edge_has_source"] for r in rows)}


def replay_items_any(path, group):
    """Replay rows from bootstrap_replay_ca.py for either family; uses the stored permuted reference when columns were shuffled."""
    import causalarena_io as CA
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    fam = d["header"].get("family", "semantic")
    out = []
    for r in d["rows"]:
        if r.get("status") != "ok":
            continue
        if "truth_repo" in r:
            T = np.asarray(r["truth_repo"])
        else:
            T = CA.to_repo_matrix(CA.load(ROOT / "external" / "causalarena" / "scm" / fam / "data" / ("%s_obs_only" % fam) / r["file"])["g"])
        out.append({"key": r["file"], "group": group, "S0": np.asarray(r["S0"]), "boot": r["boot"], "buckets": None, "S1": r["S1"],
                    "E": G.truth_edges(T), "p": len(r["S0"])})
    return out, d["header"]


def file_sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def frozen_ok():
    if not RULE.exists():
        return False
    r = json.loads(RULE.read_text())
    return r["sha256"] == file_sha(__file__) and r["refinement_v1_sha256"] == file_sha(HERE / "refinement_v1.py")


def s2_items(label="s2"):
    import refinement_v1_test_live as L
    return L.items(label)


def labels_for(key):
    meta = json.loads((ROOT / "runs" / key / "meta.json").read_text(encoding="utf-8"))
    ds = meta["dataset"].replace("/research/", "research:")
    m = json.loads((ROOT / "datasets" / "suite_q1s2" / "MAPPING.json").read_text(encoding="utf-8"))
    for code, arm in m["arms"].items():
        if arm["dataset_arg"] == ds:
            return code, arm
    raise KeyError(key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("dev", "freeze", "requests", "apply", "test"))
    ap.add_argument("--label", default="s2")
    ap.add_argument("--answers", default=None)
    ap.add_argument("--replay", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    OUTD.mkdir(parents=True, exist_ok=True)
    sys.path[:0] = [str(ROOT.parent / "Causal-Copilot"), str(ROOT.parent / "Causal-Copilot" / "externals" / "causal-learn")]
    now = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    if a.mode == "freeze":
        if RULE.exists():
            sys.exit("already frozen: %s" % json.loads(RULE.read_text())["sha256"])
        RULE.write_text(json.dumps({"file": "analysis/refinement_v2.py", "sha256": file_sha(__file__),
                                    "refinement_v1_sha256": file_sha(HERE / "refinement_v1.py"), "ADD": ADD, "frozen_utc": now}, indent=1) + "\n")
        print("frozen", file_sha(__file__))
        return
    if a.mode == "dev":
        items = V1.live_items()
        dev_replay = ROOT / "jobs" / "bootstrap_replay_ca_dev" / "out" / "replay_dev.json"
        items += replay_items_any(dev_replay, "replay:semantic:dev")[0]
        fdev = ROOT / "jobs" / "bootstrap_replay_ca_formula_dev" / "out" / "replay_formula_dev.json"
        if fdev.exists():
            items += replay_items_any(fdev, "replay:formula:dev")[0]
        rows, summary = evaluate(items)
        by = {g: evaluate([i for i in items if i["group"] == g])[1] for g in sorted({i["group"] for i in items})}
        out = {"mode": "dev", "rule_sha256": file_sha(__file__), "summary": summary, "by_group": by, "rows": rows}
        Path(a.out or OUTD / "dev.json").write_text(json.dumps(out, indent=1, default=float) + "\n", encoding="utf-8")
        print(json.dumps({"summary": {k: (x.get("verdict") if isinstance(x, dict) and "verdict" in x else x) for k, x in summary.items()},
                          "by_group": {g: {k: s[k]["verdict"] for k in ("R1", "R2", "R3")} for g, s in by.items()}}, indent=1, default=float))
        return
    if a.mode == "test":
        if not frozen_ok():
            sys.exit("refused: v2 is not frozen, or this file or refinement_v1.py differs from the frozen rule")
        with open(ACCESS, "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"utc": now, "mode": "test", "replay": a.replay, "rule_sha256": file_sha(__file__)}) + "\n")
        items, header = replay_items_any(a.replay, "replay:%s:test" % "formula")
        rows, summary = evaluate(items)
        out = {"mode": "test", "rule_sha256": file_sha(__file__), "replay_header": {k: v for k, v in header.items() if k != "env"},
               "summary": summary, "rows": rows}
        Path(a.out or OUTD / "test_formula.json").write_text(json.dumps(out, indent=1, default=float) + "\n", encoding="utf-8")
        print(json.dumps(summary, indent=1, default=float))
        return
    if a.mode == "requests":
        if not frozen_ok():
            sys.exit("refused: freeze v2 before writing the requests the model will see")
        reqs, per_run = [], {}
        for it in s2_items(a.label):
            if "missing" in it:
                continue
            code, arm = labels_for(it["key"])
            names = arm["column_labels"]
            V, _ = v2d(it["S0"], it["boot"])
            n = 0
            for x, y in G.pairs(V.shape[0]):
                if G.pair_type(V, x, y) in ASKABLE:
                    n += 1
                    for k, tpl in enumerate(PARAPHRASES):
                        reqs.append({"id": "%s|%d|%d|%d" % (it["key"], x, y, k), "run": it["key"], "arm": code, "role": arm["role"],
                                     "family": arm["family"], "a": int(x), "b": int(y), "paraphrase": k,
                                     "prompt": tpl.format(a=names[x], b=names[y])})
            per_run[it["key"]] = n
        dest = Path(a.out or ROOT / "plans" / "bnd11_names_requests.jsonl")
        dest.write_text("".join(json.dumps(r) + "\n" for r in reqs), encoding="utf-8")
        chars = sum(len(r["prompt"]) for r in reqs)
        summ = {"requests": len(reqs), "pairs": sum(per_run.values()), "runs": len(per_run), "prompt_chars": chars,
                "approx_prompt_tokens": round(chars * 0.24), "per_run_pairs": per_run, "rule_sha256": file_sha(__file__)}
        (OUTD / "requests_summary.json").write_text(json.dumps(summ, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in summ.items() if k != "per_run_pairs"}))
        return
    if a.mode == "apply":
        if not frozen_ok():
            sys.exit("refused: v2 is not frozen")
        ans = {}
        for line in open(a.answers, encoding="utf-8"):
            r = json.loads(line)
            ans.setdefault(r["run"], {}).setdefault((r["a"], r["b"]), [None, None, None])[r["paraphrase"]] = r.get("direction")
        rows, malformed = [], 0
        for line in open(a.answers, encoding="utf-8"):
            r = json.loads(line)
            malformed += int(r.get("invalid_replies", 0))
        for it in s2_items(a.label):
            if "missing" in it:
                continue
            code, arm = labels_for(it["key"])
            M, _ = v2d(it["S0"], it["boot"])
            V, recs = apply_names(M, ans.get(it["key"], {}))
            seed = zlib.crc32(it["key"].encode())
            rows.append({"key": it["key"], "code": code, "family": arm["family"], "role": arm["role"],
                         "scores": {"v2d": V1.scores(M, it["E"], it["p"], seed), "v2": V1.scores(V, it["E"], it["p"], seed)},
                         "names_edges": sum(1 for x in recs if x["used"]), "asked_pairs": len(recs),
                         "why_not_used": {w: sum(1 for x in recs if not x["used"] and x.get("why") == w) for w in sorted({x.get("why") for x in recs if not x["used"]})},
                         "records": recs})
        by = lambda role: {r["family"]: r for r in rows if r["role"] == role}
        neu, swp, real = by("neutral"), by("swapped"), by("real")
        r4 = sum(1 for r in neu.values() if r["names_edges"] == 0)
        r4_any = sum(1 for r in neu.values() if r["names_edges"] > 0)
        r5 = sum(1 for r in swp.values() if abs(r["scores"]["v2"]["dir_f1_random"] - r["scores"]["v2d"]["dir_f1_random"]) <= 0.05)
        r6 = sum(1 for r in real.values() if r["scores"]["v2"]["dir_f1_random"] > r["scores"]["v2d"]["dir_f1_random"])
        cnt = lambda hits, sup, ref: "SUPPORTED" if hits >= sup else ("REFUTED" if hits <= ref else "INCONCLUSIVE")
        out = {"mode": "apply", "rule_sha256": file_sha(__file__), "answers": a.answers, "invalid_replies_total": malformed,
               "R4": {"families_with_no_names_edge": r4, "families_with_any": r4_any, "families": len(neu),
                      "verdict": "SUPPORTED" if r4 >= 9 else ("REFUTED" if r4_any > 2 else "INCONCLUSIVE")},
               "R5": {"hits": r5, "families": len(swp), "verdict": cnt(r5, 8, 5)},
               "R6": {"hits": r6, "families": len(real), "verdict": cnt(r6, 8, 5)},
               "separating_set_check": "not done: the pipeline does not record separating sets for the bootstrap step",
               "rows": rows}
        Path(a.out or OUTD / "names_s2.json").write_text(json.dumps(out, indent=1, default=float) + "\n", encoding="utf-8")
        print(json.dumps({k: out[k] for k in ("R4", "R5", "R6", "invalid_replies_total")}, indent=1))


if __name__ == "__main__":
    main()
