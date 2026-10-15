"""B3 runner: declared knowledge as tiers on the data-only ledger, in three name arms (D3.3-D3.5).

  python -m kernel.run_b3 --family semantic --split dev --rule C3 --out analysis/results/q2_b3/dev_semantic.jsonl

Knowledge: AB-07's recorded gpt-4o tier replies (plans/results/a3_tiers_answers.jsonl; prompts and requests hashed in
plans/a3_prereg.json; 3 phrasings x 3 arms x 100 scenarios, collected 2026-10-12), replayed through the supplier
contract (supplier.contract.call with supplier.tiers.replay_transport): no new model call. Names per arm come from
plans/a3_scenarios.json (labels[arm][i] is the name shown for released column i; all 5 replicate files share them).
Per file and arm: the data-only ledger D (frozen B1 rule, variables named as in the arm) and D+K (kernel.knowledge).
Scores per arm: directed F1 (expectation rule, per-file seed), expected-credit F1 (open pairs earn 1/2; the quantity
theory pack T3 bounds), the exact T3 bound with the truth, DV-1 counts, the neutral-arm identity check, and supplier
counts. The test split is read only with --held-out-read FREEZE_ID matching plans/b3_freeze.json.
No model calls. Tickets: BLD-04, CAP-04, TGT-11, TGT-19 (proposed)
"""
import argparse, datetime, hashlib, json, os, sys, time
from pathlib import Path

for _k in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_k, "1")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
ARMS = ("real", "neutral", "moved")


def expected_f1(D, U, T):
    """2 x expected true positives / (claimed adjacencies + true edges), open true edges earning 1/2."""
    T = set(T)
    nP = len(D) + len(U)
    tp = sum(1.0 for e in D if e in T) + sum(0.5 for a, b in U if (a, b) in T or (b, a) in T)
    N = nP + len(T)
    return 2 * tp / N if N else 0.0, nP, len(T)


def t3_bound(D, U, T, decided_pairs):
    """Exact T3 harm bound: 2 x (credit of the decided pairs in D) / (nP + nT). Decided pairs were open in D: credit 1/2
    when the pair is a true edge, 0 otherwise."""
    T = set(T)
    c0 = sum(0.5 for a, b in decided_pairs if (a, b) in T or (b, a) in T)
    N = len(D) + len(U) + len(T)
    return 2 * c0 / N if N else 0.0


def one(args):
    path, family, rule, answers_path, scen_path, prereg = args
    from kernel import build as B, checker, knowledge as K, views
    from score import bench, dv, graph
    from supplier import contract as C, tiers as TS
    import verify02
    s = bench.load(path)
    X = s["values"]
    name = Path(path).name
    sc_all = json.load(open(scen_path))
    key = next(k for k, v in sc_all.items() if v["family"] == family and "_%s__" % v["scenario"] in name)
    scen = sc_all[key]
    answers = TS.load_answers(answers_path)
    I = bench.truth_info(family, name)
    T = I["T"]
    seed = graph.file_seed(name)
    row = {"file": name, "family": family, "split": bench.split_of(family, name), "scenario": bench.scenario_of(name), "arms": {}}
    eng_cache = {}
    t0 = time.time()
    for arm in ARMS:
        names = list(scen["labels"][arm])
        _, order = B.variables(X, names)
        ck = tuple(order)
        if ck not in eng_cache:
            eng_cache[ck] = B.run_engines(X, names, with_ges=(rule != "pc"))
        led_d, _ = B.build(X, names, rule=rule, eng=eng_cache[ck], prereg=prereg, created_utc="",
                           file_meta={"source": "CausalArena", "file": name})
        if led_d is None:
            row["arms"][arm] = {"failure": "pc"}
            continue
        counts = C.Counts()
        stmts = {}
        for ph in ("p0", "p1", "p2"):
            rec = answers.get((family, scen["scenario"], arm, ph))
            if rec is None:
                stmts[ph] = None
                continue
            out = C.call(TS.replay_transport(rec), {"id": rec["id"]}, TS.schema(names), max_tokens=1500)
            counts.add(out)
            stmts[ph] = None if out.status in ("abstained", "stopped") else {
                "tiers": out.value, "supplier": {"type": "model", "model_id": (out.attempts[-1].get("model") or "gpt-4o"),
                                                 "prompt_sha256": hashlib.sha256(rec.get("id", "").encode()).hexdigest(),
                                                 "phrasing_id": ph, "shown": ["variable names (arm %s), random order" % arm]}}
        led_k, kinfo = K.apply_tiers(led_d, stmts, counts.as_dict())
        vk = {k: len(v) for k, v in verify02.verify(led_k).items() if v}
        ck_ok = checker.check(led_k)
        Dd, Ud = views.graph_sets(led_d)
        Dk, Uk = views.graph_sets(led_k)
        pos = {v["name"]: v["position"] for v in led_d["variables"]}
        decided = [tuple(sorted((pos[a], pos[b]))) for a, b in kinfo["decided"]]
        ef_d, nP, nT = expected_f1(Dd, Ud, T)
        ef_k, _, _ = expected_f1(Dk, Uk, T)
        res = {}
        for lab, (D, U) in (("D", (Dd, Ud)), ("DK", (Dk, Uk))):
            checked = dv.check(dv.claims(I["n"], D, U, I["targets"]), I["desc"])
            res[lab] = {"f1": graph.directed_f1(D, U, T, seed)["f1"],
                        "dv1": {"pairs": dv.n_pairs(I["n"], I["targets"]), "committed": len(checked), "correct": sum(ok for *_, ok in checked)}}
        right = sum(1 for a, b in kinfo["decided"] if (pos[a], pos[b]) in T)
        wrong = sum(1 for a, b in kinfo["decided"] if (pos[b], pos[a]) in T)
        row["arms"][arm] = {"D": res["D"], "DK": res["DK"], "expected_f1_D": ef_d, "expected_f1_DK": ef_k, "nP": nP, "nT": nT,
                            "decided": len(decided), "decided_true_right": right, "decided_true_wrong": wrong,
                            "t3_bound": t3_bound(Dd, Ud, T, decided), "t3_bound_truth_free": led_k["report"]["knowledge_application"]["t3_bound_truth_free"],
                            "loss_expected": ef_d - ef_k, "within_t3": (ef_d - ef_k) <= t3_bound(Dd, Ud, T, decided) + 1e-12,
                            "skeleton_identical": {frozenset(e) for e in Dd} | {frozenset(u) for u in Ud} == {frozenset(e) for e in Dk} | {frozenset(u) for u in Uk},
                            "claims_identical_to_D": [(c["x"], c["y"], c["relation"]) for c in led_k["claims"]] == [(c["x"], c["y"], c["relation"]) for c in led_d["claims"]],
                            "consensus": kinfo["consensus"], "skipped_cycle": len(kinfo["skipped"]), "supplier": counts.as_dict(),
                            "verify_failures": vk, "checker_ok": ck_ok["ok"], "checker_errors": ck_ok["errors"][:2],
                            "ledger_sha256_D": led_d["report"]["ledger_sha256"], "ledger_sha256_DK": led_k["report"]["ledger_sha256"]}
    row["seconds"] = round(time.time() - t0, 1)
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=("semantic", "formula"))
    ap.add_argument("--split", required=True, choices=("dev", "test"))
    ap.add_argument("--rule", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--answers", default=str(ROOT / "plans" / "results" / "a3_tiers_answers.jsonl"))
    ap.add_argument("--scenarios", default=str(ROOT / "plans" / "a3_scenarios.json"))
    ap.add_argument("--prereg", default=str(ROOT / "plans" / "b3_prereg.json"))
    ap.add_argument("--held-out-read", default=None)
    a = ap.parse_args()
    from score import bench
    prereg = None
    if Path(a.prereg).exists():
        prereg = {"prereg": os.path.relpath(a.prereg, ROOT), "prereg_sha256": hashlib.sha256(Path(a.prereg).read_bytes()).hexdigest(),
                  "fixed_utc": json.load(open(a.prereg)).get("written_utc", "")}
    if a.split == "test":
        from kernel import freeze
        fz_path = ROOT / "plans" / "b3_freeze.json"
        if not a.held_out_read or prereg is None or not fz_path.exists():
            raise SystemExit("the test split is read only with --held-out-read FREEZE_ID, plans/b3_prereg.json and plans/b3_freeze.json")
        fz = json.load(open(fz_path))
        h, _ = freeze.code_sha256()
        if fz["id"] != a.held_out_read or fz["code_sha256"] != h or fz.get("rule") != a.rule:
            raise SystemExit("kernel code, rule or freeze id does not match plans/b3_freeze.json: refusing the held-out read")
        log = ROOT / "analysis" / "results" / "q2_b3" / "access_log.jsonl"
        log.parent.mkdir(parents=True, exist_ok=True)
        with open(log, "a") as fh:
            fh.write(json.dumps({"utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "family": a.family,
                                 "split": "test", "freeze": a.held_out_read, "rule": a.rule, "prereg_sha256": prereg["prereg_sha256"]}) + "\n")
    files = [str(f) for f in bench.files(a.family, "obs_only", a.split)]
    if a.limit:
        files = files[:a.limit]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["file"] for l in open(out)} if out.exists() else set()
    jobs = [(f, a.family, a.rule, a.answers, a.scenarios, prereg) for f in files if Path(f).name not in done]
    print("%d files, %d to do" % (len(files), len(jobs)), flush=True)
    import multiprocessing as mp
    with mp.get_context("fork").Pool(a.workers, maxtasksperchild=10) as pool:
        for row in pool.imap_unordered(one, jobs):
            with open(out, "a") as fh:
                fh.write(json.dumps(row) + "\n")
            print(row["file"][:70], row.get("seconds"), flush=True)


if __name__ == "__main__":
    main()
