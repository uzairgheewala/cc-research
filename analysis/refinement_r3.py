"""Refinement r3 (BLD-22, program v3 R3): commit a direction only on sufficient evidence; otherwise leave it open. No model call.

Tickets: BLD-22, BLD-06, ADV-01

The current rule (refinement v2's data part, v2d: analysis/refinement_v2.py, frozen, imported unchanged; the same logic as
postprocess/refinement_v2_dropin.py on fork branch bld-06-refinement-v2) gives each linked pair the commonest of the nine
typed bootstrap outcomes, so a direction is committed whenever an arrow is the plurality of the resamples (gas/void: 8 of 20).

The sufficiency rule (r3s), applied to v2d's graph and nothing else:
  for every pair v2d leaves fully directed d (a->b or b->a), let k = the number of the N resamples whose outcome for the pair is
  exactly d (N = 20, the pipeline's boot_num). Keep d iff k >= K_MIN, where K_MIN is the smallest k whose two-sided 95% Wilson
  lower bound of k/N is above 1/2: "a majority of resamples, with 95% confidence" (N = 20 gives K_MIN = 15).
  Otherwise the pair stays linked and its direction is open: mark o-o if any resample, or the algorithm, gave the pair a PAG
  mark (o-o, o->, o-, <->), else undirected. Source "data: direction open (k of N below K_MIN)".
  Links are never changed (the same pairs as v2d); semi-directed marks and conflicting codes pass through unchanged (typed gap:
  the rule gates full arrows only). Since K_MIN > N/2, every arrow r3s keeps is one v2d commits: r3s only removes arrows, so it
  creates no directed cycle that v2d did not have.
K_MIN is fixed by the confidence level, not fitted. The sweep over K in --sweep is sensitivity on the development battery only.

Outcome counts per graph, against the reference (cc_graph conventions; one unordered pair at a time):
  links      adj_tp (true link found), adj_fp (link not in the reference), adj_fn (true link missed)
  on true links found: right (arrow as in the reference), wrong (arrow reversed), open (no arrow committed), partial (a
             semi-directed mark: neither right nor wrong here, counted apart)
  arrows_on_false_links  arrows committed on a link the reference does not have
  right/wrong split by whether the true edge is compelled in the reference's CPDAG (identifiable from the pattern alone)
  direction precision = right / (right + wrong)
Groups and truth tiers: CausalArena replays have exact (simulated) references and form the development pool; live dev runs
(suite_b1: Causal-Copilot's bundled reference graphs; pass 4b: Sachs) have contested references and are reported as agreement
only, never pooled into the headline.

Modes
  python analysis/refinement_r3.py dev [--out F]        development battery -> analysis/results/refinement_r3/dev.json
  python analysis/refinement_r3.py freeze               RULE.json: sha256 of this file, its imports and plans/r3_prereg.json
  python analysis/refinement_r3.py heldout --battery H1|H2|H3 [--replay F ...]
                                                        refuses unless frozen; appends to access_log.jsonl; one read per battery
  python analysis/refinement_r3.py regress              the gas/void pair (q011, BLD-06 branch run): a regression check only
"""
import argparse
import datetime
import hashlib
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import cc_graph as G  # noqa: E402
import refinement_v1 as V1  # noqa: E402   (frozen; imported unchanged)
import refinement_v2 as V2  # noqa: E402   (frozen; imported unchanged)

N_RESAMPLES = 20
Z95 = 1.959963984540054
OUTD = HERE / "results" / "refinement_r3"
RULE = OUTD / "RULE.json"
ACCESS = OUTD / "access_log.jsonl"
PREREG = ROOT / "plans" / "r3_prereg.json"
DIRS = ("a->b", "b->a")
SEMI = ("a o-> b", "b o-> a", "a o- b", "b o- a")
PAG_MARKS = ("o-o", "bidirected") + SEMI
BOOT_SEED = 20261031
B = 2000


def wilson_lb(k, n, z=Z95):
    if n == 0:
        return 0.0
    ph = k / n
    den = 1 + z * z / n
    c = ph + z * z / (2 * n)
    r = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return (c - r) / den


def k_min(n=N_RESAMPLES, z=Z95):
    return next(k for k in range(n + 1) if wilson_lb(k, n, z) > 0.5)


K_MIN = k_min()


def r3s(S0, boot, n=N_RESAMPLES, kmin=None):
    """-> (graph, v2d sources, gate records). kmin=None uses K_MIN; another value is for the dev sensitivity sweep only."""
    kmin = K_MIN if kmin is None else kmin
    S0 = np.asarray(S0)
    M, sources = V2.v2d(S0, boot)
    R = np.array(M, dtype=int)
    gates = []
    for a, b in G.pairs(R.shape[0]):
        d = G.pair_type(M, a, b)
        if d not in DIRS:
            continue
        fr = {t: float(v) for t, v in V1.typed_freqs(boot, a, b).items()}
        k = int(round(fr[d] * n))
        rec = {"pair": [a, b], "v2d": d, "k": k, "n": n, "k_min": kmin, "integral": abs(fr[d] * n - k) < 1e-6}
        if k >= kmin:
            rec["r3s"] = d
        else:
            pag = any(fr[t] > 0 for t in PAG_MARKS) or G.pair_type(S0, a, b) in PAG_MARKS
            t = "o-o" if pag else "undirected"
            R[a, b], R[b, a] = 0, 0
            V1.put(R, a, b, t)
            rec.update({"r3s": t, "source": "data: direction open (%d of %d below %d)" % (k, n, kmin)})
        gates.append(rec)
    return R, sources, gates


def outcome(M, E, p):
    M = np.asarray(M)
    E = set(E)
    tadj = {frozenset(e) for e in E}
    C = G.cpdag_of(E, p)
    o = dict.fromkeys(("adj_tp", "adj_fp", "adj_fn", "right", "wrong", "open", "partial", "other", "arrows_on_false_links",
                       "right_compelled", "right_reversible", "wrong_compelled", "wrong_reversible"), 0)
    for a, b in G.pairs(p):
        est, tru = G.is_adjacent(M, a, b), frozenset((a, b)) in tadj
        t = G.pair_type(M, a, b)
        if est and tru:
            o["adj_tp"] += 1
            want = "a->b" if (a, b) in E else "b->a"
            comp = "compelled" if G.pair_type(C, a, b) in DIRS else "reversible"
            if t == want:
                o["right"] += 1
                o["right_" + comp] += 1
            elif t in DIRS:
                o["wrong"] += 1
                o["wrong_" + comp] += 1
            elif t in SEMI:
                o["partial"] += 1
            elif t.startswith("conflict") or t.startswith("mixed"):
                o["other"] += 1
            else:
                o["open"] += 1
        elif est:
            o["adj_fp"] += 1
            if t in DIRS:
                o["arrows_on_false_links"] += 1
        elif tru:
            o["adj_fn"] += 1
    s = G.score(M, E, p)
    o["dir_f1"] = s["dir_f1"] or 0.0
    o["adj_f1"] = s["adj_f1"] or 0.0
    return o


def tier(group):
    return "exact" if group.startswith("replay:") or group.startswith("live:s2") or group.startswith("live:f06") else "contested"


def cluster(key):
    m = re.search(r"_(b1_k\d|p4b_[a-z0-9]+)", key)
    return m.group(1)[:-1] if m and m.group(1).startswith("b1_k") else (m.group(1) if m else key)


def evaluate_item(it, sweep=()):
    S0 = np.asarray(it["S0"])
    S1 = np.asarray(it["S1"]) if it.get("S1") is not None else V1.step_bootstrap(S0, it["buckets"])[0]
    R, _, gates = r3s(S0, it["boot"])
    Vd, _ = V2.v2d(S0, it["boot"])
    row = {"key": it["key"], "group": it["group"], "tier": tier(it["group"]), "cluster": cluster(it["key"]), "p": it["p"],
           "arms": {"S0": outcome(S0, it["E"], it["p"]), "S1": outcome(S1, it["E"], it["p"]), "v2d": outcome(Vd, it["E"], it["p"]),
                    "r3s": outcome(R, it["E"], it["p"])},
           "links_identical": bool(all(G.is_adjacent(Vd, a, b) == G.is_adjacent(R, a, b) for a, b in G.pairs(it["p"]))),
           "opened": sum(1 for g in gates if g["r3s"] not in DIRS), "kept": sum(1 for g in gates if g["r3s"] in DIRS),
           "non_integral_k": sum(1 for g in gates if not g["integral"])}
    if sweep:
        row["sweep"] = {str(k): outcome(r3s(S0, it["boot"], kmin=k)[0], it["E"], it["p"]) for k in sweep}
    return row


KEYS = ("adj_tp", "adj_fp", "adj_fn", "right", "wrong", "open", "partial", "other", "arrows_on_false_links",
        "right_compelled", "right_reversible", "wrong_compelled", "wrong_reversible")


def totals(rows, arm, field="arms"):
    t = {k: int(sum(r[field][arm][k] for r in rows)) for k in KEYS}
    t["files"] = len(rows)
    t["direction_precision"] = round(t["right"] / (t["right"] + t["wrong"]), 4) if t["right"] + t["wrong"] else None
    t["mean_dir_f1"] = round(float(np.mean([r[field][arm]["dir_f1"] for r in rows])), 4) if rows else None
    t["mean_adj_f1"] = round(float(np.mean([r[field][arm]["adj_f1"] for r in rows])), 4) if rows else None
    return t


def paired_intervals(rows, a="r3s", b="v2d"):
    """Cluster bootstrap (resampling clusters of files) of r3s minus v2d: totals of wrong, right, open, arrows on false links,
    and the direction precision of each arm and their difference."""
    if not rows:
        return {}
    cl = sorted({r["cluster"] for r in rows})
    byc = {c: [r for r in rows if r["cluster"] == c] for c in cl}
    rng = np.random.default_rng(BOOT_SEED)

    def stat(rs):
        s = {}
        for k in ("wrong", "right", "open", "arrows_on_false_links"):
            s["d_" + k] = sum(r["arms"][a][k] - r["arms"][b][k] for r in rs)
        for arm in (a, b):
            rw = sum(r["arms"][arm]["right"] for r in rs), sum(r["arms"][arm]["wrong"] for r in rs)
            s["prec_" + arm] = rw[0] / (rw[0] + rw[1]) if sum(rw) else float("nan")
        s["d_prec"] = s["prec_" + a] - s["prec_" + b]
        s["d_mean_dir_f1"] = float(np.mean([r["arms"][a]["dir_f1"] - r["arms"][b]["dir_f1"] for r in rs]))
        return s

    point = stat(rows)
    draws = [stat([r for c in rng.choice(cl, size=len(cl), replace=True) for r in byc[c]]) for _ in range(B)]
    out = {}
    for k, v in point.items():
        xs = np.array([d[k] for d in draws], dtype=float)
        xs = xs[~np.isnan(xs)]
        if not len(xs) or v != v:
            out[k] = {"point": None, "lo": None, "hi": None}
            continue
        out[k] = {"point": round(float(v), 4), "lo": round(float(np.quantile(xs, 0.025)), 4), "hi": round(float(np.quantile(xs, 0.975)), 4)}
    out["clusters"] = len(cl)
    out["resamples"] = B
    return out


def summarise(rows, sweep=()):
    out = {"arms": {arm: totals(rows, arm) for arm in ("S0", "S1", "v2d", "r3s")},
           "links_identical_all": all(r["links_identical"] for r in rows), "opened": sum(r["opened"] for r in rows),
           "kept": sum(r["kept"] for r in rows), "non_integral_k": sum(r["non_integral_k"] for r in rows)}
    out["paired_r3s_minus_v2d"] = paired_intervals(rows)
    if sweep:
        out["sweep_sensitivity_dev_only"] = {k: totals(rows, k, "sweep") for k in map(str, sweep)}
    return out


def dev_items():
    items = V1.live_items()
    items += V2.replay_items_any(ROOT / "jobs" / "bootstrap_replay_ca_dev" / "out" / "replay_dev.json", "replay:semantic:dev")[0]
    items += V2.replay_items_any(ROOT / "jobs" / "bootstrap_replay_ca_formula_dev" / "out" / "replay_formula_dev.json", "replay:formula:dev")[0]
    for it in items:
        if it["group"] == "live:pass4b":
            it["group"] = "live:pass4b(sachs)"
    return items


def live_s2_items():
    """BLD-06's S2 runs (label f06, both arms, the new image of 21-22 Oct) and BND-08's (label s2, main, old image)."""
    import glob
    import pickle
    m = json.loads((ROOT / "datasets" / "suite_q1s2" / "MAPPING.json").read_text(encoding="utf-8"))
    by_arg = {arm["dataset_arg"]: (code, arm) for code, arm in m["arms"].items()}
    out = []
    for mf in sorted(glob.glob(str(ROOT / "runs" / "*" / "meta.json"))):
        meta = json.load(open(mf, encoding="utf-8"))
        if meta.get("stub_llm") or meta.get("label") not in ("s2", "f06"):
            continue
        ds = (meta.get("dataset") or "").replace("/research/", "research:", 1)
        if ds not in by_arg:
            continue
        code, arm = by_arg[ds]
        rd = Path(mf).parent
        bf = sorted(rd.glob("artifacts/*_bootstrap.pkl"))
        rf = sorted(rd.glob("artifacts/*_bootstrap_recommend.pkl"))
        if not bf:
            continue
        a = pickle.load(open(bf[0], "rb"))
        if a.get("error"):
            continue
        S0 = np.asarray(a["args_before"]["kwargs"]["full_graph"])
        branch = ((meta.get("fork") or {}).get("branch")) or "main"
        ref = np.load(ROOT / "datasets" / "suite_q1s2" / arm["reference_by_data"])
        out.append({"key": rd.name, "group": "live:%s:%s" % (meta["label"], branch), "S0": S0, "boot": a["ret"][1],
                    "buckets": pickle.load(open(rf[0], "rb"))["ret"] if rf else None, "S1": None if rf else S0,
                    "E": G.truth_edges(ref), "p": S0.shape[0], "code": code, "role": arm["role"], "family": arm["family"]})
    return out


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


FROZEN_FILES = ("analysis/refinement_r3.py", "analysis/refinement_v2.py", "analysis/refinement_v1.py", "analysis/cc_graph.py",
                "analysis/lineage.py", "analysis/causalarena_io.py", "plans/r3_prereg.json")


def composite():
    lines = ["%s  %s" % (sha(ROOT / f), f) for f in FROZEN_FILES]
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest(), lines


def frozen_ok():
    if not RULE.exists():
        return False
    r = json.loads(RULE.read_text(encoding="utf-8"))
    return r["composite_sha256"] == composite()[0]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def by_group(rows, sweep=()):
    return {g: summarise([r for r in rows if r["group"] == g], sweep) for g in sorted({r["group"] for r in rows})}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("dev", "freeze", "heldout", "regress"))
    ap.add_argument("--battery", choices=("H1", "H2", "H3"))
    ap.add_argument("--replay", nargs="*", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    sys.path[:0] = [str(ROOT.parent / "Causal-Copilot"), str(ROOT.parent / "Causal-Copilot" / "externals" / "causal-learn")]
    OUTD.mkdir(parents=True, exist_ok=True)
    if a.mode == "dev":
        sweep = tuple(range(8, N_RESAMPLES + 1))
        rows = [evaluate_item(it, sweep) for it in dev_items()]
        exact = [r for r in rows if r["tier"] == "exact"]
        out = {"tickets": ["BLD-22", "BLD-06"], "mode": "dev", "utc": now(), "rule_file_sha256": sha(__file__), "K_MIN": K_MIN,
               "N": N_RESAMPLES, "pooled_exact": summarise(exact, sweep), "by_group": by_group(rows, sweep),
               "note": "pooled_exact = CausalArena dev replays (exact references); live groups are agreement with contested references",
               "rows": rows}
        Path(a.out or OUTD / "dev.json").write_text(json.dumps(out, indent=1, default=float) + "\n", encoding="utf-8")
        pe = out["pooled_exact"]
        print(json.dumps({"K_MIN": K_MIN, "pooled_exact": {k: pe["arms"][k] for k in ("S0", "S1", "v2d", "r3s")},
                          "paired": pe["paired_r3s_minus_v2d"], "links_identical_all": pe["links_identical_all"]}, indent=1))
        return
    if a.mode == "freeze":
        if RULE.exists():
            sys.exit("already frozen: %s" % json.loads(RULE.read_text())["composite_sha256"])
        if not PREREG.exists():
            sys.exit("refused: write plans/r3_prereg.json first")
        c, lines = composite()
        RULE.write_text(json.dumps({"tickets": ["BLD-22"], "rule": "r3s", "K_MIN": K_MIN, "N": N_RESAMPLES,
                                    "rule_file_sha256": sha(__file__), "prereg_sha256": sha(PREREG), "files": lines,
                                    "composite_sha256": c, "frozen_utc": now()}, indent=1) + "\n", encoding="utf-8")
        print("frozen", c)
        return
    if not frozen_ok():
        sys.exit("refused: r3s is not frozen, or a frozen file differs (see RULE.json)")
    with open(ACCESS, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"utc": now(), "mode": a.mode, "battery": a.battery, "replay": a.replay,
                             "composite_sha256": composite()[0]}) + "\n")
    if a.mode == "regress":
        it = next(i for i in live_s2_items() if "_f06_q011_" in i["key"] and i["group"].endswith("bld-06-refinement-v2"))
        R, _, gates = r3s(it["S0"], it["boot"])
        Vd, _ = V2.v2d(it["S0"], it["boot"])
        pair = (14, 15)
        g = next(x for x in gates if tuple(x["pair"]) == pair)
        res = {"tickets": ["BLD-22", "BLD-06"], "run": it["key"], "pair": list(pair), "names": ["residual_entrained_gas_mg", "true_void_fraction"],
               "truth": "gas -> void", "v2d": G.pair_type(Vd, *pair), "r3s": G.pair_type(R, *pair), "gate": g,
               "check": "linked, and no arrow against the truth", "pass": bool(G.is_adjacent(R, *pair) and G.pair_type(R, *pair) != "b->a"),
               "role": "regression check only (program v3 section 4 rule 5): never a tuning target or a threshold"}
        Path(a.out or OUTD / "regress_q011.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(res, indent=1))
        return
    pre = json.loads(PREREG.read_text(encoding="utf-8"))
    if a.battery == "H1":
        items = []
        for f, g in ((ROOT / "jobs" / "bootstrap_replay_ca_test" / "out" / "replay_test.json", "replay:semantic:test"),
                     (ROOT / "jobs" / "bootstrap_replay_ca_formula_test" / "out" / "replay_formula_test.json", "replay:formula:test")):
            items += V2.replay_items_any(f, g)[0]
    elif a.battery == "H2":
        items = live_s2_items()
    else:
        items = []
        for f in a.replay or []:
            items += V2.replay_items_any(f, "replay:%s:test_rep1" % ("formula" if "formula" in f else "semantic"))[0]
    rows = [evaluate_item(it) for it in items]
    out = {"tickets": ["BLD-22"], "mode": "heldout", "battery": a.battery, "utc": now(), "composite_sha256": composite()[0],
           "prereg_sha256": sha(PREREG), "pooled": summarise(rows), "by_group": by_group(rows), "rows": rows}
    out["verdicts"] = verdicts(out["pooled"], pre)
    Path(a.out or OUTD / ("heldout_%s.json" % a.battery)).write_text(json.dumps(out, indent=1, default=float) + "\n", encoding="utf-8")
    print(json.dumps({"pooled": out["pooled"], "verdicts": out["verdicts"]}, indent=1, default=float))


def verdicts(s, pre):
    """The predictions in plans/r3_prereg.json, evaluated on one battery's pooled summary."""
    out = {}
    v, r, pi = s["arms"]["v2d"], s["arms"]["r3s"], s["paired_r3s_minus_v2d"]
    for p in pre["predictions"]:
        x = {"wrong_share_removed": 1 - r["wrong"] / v["wrong"] if v["wrong"] else None,
             "right_share_kept": r["right"] / v["right"] if v["right"] else None,
             "precision_r3s": r["direction_precision"],
             "d_prec_lo": pi.get("d_prec", {}).get("lo"),
             "links_identical": 1.0 if s["links_identical_all"] else 0.0,
             "false_link_arrow_share_removed": 1 - r["arrows_on_false_links"] / v["arrows_on_false_links"] if v["arrows_on_false_links"] else None}[p["metric"]]
        verdict = None if x is None else ("SUPPORTED" if x >= p["supported_if_at_least"] else
                                          ("REFUTED" if x <= p["refuted_if_at_most"] else "INCONCLUSIVE"))
        out[p["id"]] = {"metric": p["metric"], "value": None if x is None else round(float(x), 4), "verdict": verdict}
    return out


if __name__ == "__main__":
    main()
