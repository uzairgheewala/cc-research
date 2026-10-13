"""AB-05 (AUD-37) agent probes: run one external LLM causal-discovery agent end to end on one CausalArena scenario.

  python /research/harness/agent_probe.py --agent {vashishtha,pywhyllm,matmcd,causaliq} --scenario FILE.npz \
         --shuffle-seed 20261010 --out /research/runs/ab05/<agent>/ [--stub] [--model gpt-4o] [--max-calls N] [--max-usd X]
         [--context-text TEXT] [--names-map FILE.json] [--agent-opt key=value ...] [--jitter SD]
  python /research/harness/agent_probe.py --plan /research/plans/ab05_probe_<agent>.json [--stub]

What it does
  1. Loads the scenario (harness/probe_io.py, a copy of analysis/causalarena_io.py). Released files store columns in a
     causal order, so the columns are ALWAYS shuffled first: perm = default_rng(shuffle_seed + crc32(file name)), the
     agent sees names and data in shuffled order and never sees the true graph or the metadata beyond a coarse domain
     string (--context-text overrides it; "" gives none). --names-map {original: shown} renames variables (AB-06 arms).
  2. Calls the agent through harness/agents/<agent>.py. Every LLM request passes one counting gate
     (harness/probe_llm.py) that enforces --max-calls / --max-usd, answers offline in --stub mode, and records
     calls.jsonl. The agent process never sees the API key.
  3. Maps the result back to the original column indices and writes, in --out:
       result.json   committed arrows, undecided pairs, and where each direction came from (llm / data / ...)
       calls.jsonl   every LLM request and response: prompt sha256, served model, usage, seconds, cost
       summary.json  calls, tokens, estimated USD at gpt-4o list prices ($2.50 / $10 per 1M), wall time, failure point,
                     directed F1 (random rule, per-file seed crc32(file name)) against the true graph
       agent_stdout.log  everything the agent printed
Exit codes: 0 ok, 3 cap reached (state recorded; rerun with a higher cap resumes by replaying recorded answers),
4 agent failed (failure point recorded), 2 setup error (e.g. no key for a live run).

Live mode reads the key like names_runner.py: a real OPENAI_API_KEY environment variable wins, else python-dotenv's
reading of /app/.env. The key is never printed or written; the agent process gets a dummy key.
Agent packages are looked up in $PROBES_ROOT/<agent> (pip --target dirs; default /opt/probes) and agent sources in
$PROBES_SRC/<repo dir> (default $PROBES_ROOT/src); both are put first on sys.path before anything else is imported.
"""
import argparse
import contextlib
import hashlib
import importlib.util
import json
import os
import sys
import time
import traceback
from pathlib import Path

HARNESS = Path(__file__).resolve().parent
AGENTS = ("vashishtha", "pywhyllm", "matmcd", "causaliq")


def plan_argv(path, stub):
    """A plan file (plans/ab05_probe_<agent>.json) -> runner arguments. With --stub the plan's out_stub is used."""
    pl = json.loads(Path(path).read_text(encoding="utf-8"))
    r = pl["run"]
    argv = ["--agent", pl["agent"], "--scenario", r["scenario"], "--shuffle-seed", str(r["shuffle_seed"]),
            "--out", r["out_stub"] if stub else r["out"], "--model", r["model"],
            "--max-calls", str(r["max_calls"]), "--max-usd", str(r["max_usd"])]
    for k, v in (r.get("agent_opts") or {}).items():
        argv += ["--agent-opt", "%s=%s" % (k, v)]
    if r.get("jitter"):
        argv += ["--jitter", str(r["jitter"])]
    if r.get("context_text") is not None:
        argv += ["--context-text", r["context_text"]]
    if r.get("names_map"):
        argv += ["--names-map", r["names_map"]]
    return argv


def parse_args(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--plan" in argv:                       # --plan FILE [--stub]: everything else comes from the plan
        i = argv.index("--plan")
        plan = argv[i + 1]
        rest = argv[:i] + argv[i + 2:]
        argv = plan_argv(plan, "--stub" in rest) + rest
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--agent", required=True, choices=AGENTS)
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--shuffle-seed", type=int, required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stub", action="store_true", help="offline deterministic fake LLM: no key, no network, no cost")
    ap.add_argument("--model", default="gpt-4o")
    ap.add_argument("--max-calls", type=int, default=None)
    ap.add_argument("--max-usd", type=float, default=None)
    ap.add_argument("--context-text", default=None, help="domain text given to agents that take one (default: the "
                                                          "scenario's domain_id, humanised); '' for none")
    ap.add_argument("--names-map", default=None, help="JSON file {original name: name shown to the agent}")
    ap.add_argument("--agent-opt", action="append", default=[], help="adapter option key=value (see the adapter)")
    ap.add_argument("--jitter", type=float, default=0.0,
                    help="sd of seeded Gaussian jitter added to the data before the shuffle (kit convention from "
                         "analysis/baseline_variants_run.py: seed crc32(file name)); 0 = none. 1e-6 repairs formula files "
                         "whose exact deterministic relations make Fisher-z's correlation matrix singular")
    ap.add_argument("--dotenv", default="/app/.env")
    a = ap.parse_args(argv)
    if not a.stub and (a.max_calls is None or a.max_usd is None):
        ap.error("a live run needs both --max-calls and --max-usd")
    return a


def setup_paths(agent_mod_name, repo_dirname, src_subdir):
    root = Path(os.environ.get("PROBES_ROOT", "/opt/probes"))
    src = Path(os.environ.get("PROBES_SRC", str(root / "src")))
    target = root / agent_mod_name
    repo = src / repo_dirname
    added = []
    for p in (repo / src_subdir if src_subdir else repo, target):
        if p.is_dir():
            sys.path.insert(0, str(p))
            added.append(str(p))
    if str(HARNESS) not in sys.path:
        sys.path.insert(1, str(HARNESS))
    return target, repo, added


def load_adapter(agent):
    path = HARNESS / "agents" / (agent + ".py")
    spec = importlib.util.spec_from_file_location("ab05_adapter_" + agent, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def failure_point(exc, repo):
    tb = traceback.extract_tb(exc.__traceback__)
    inner = tb[-1] if tb else None
    in_repo = [f for f in tb if repo and str(repo) in f.filename]
    fmt = lambda f: "%s:%d (%s)" % (f.filename, f.lineno, f.name)  # noqa: E731
    return {"type": type(exc).__name__, "message": str(exc)[:500],
            "innermost_frame": fmt(inner) if inner else None,
            "innermost_agent_frame": fmt(in_repo[-1]) if in_repo else None,
            "traceback_tail": [fmt(f) for f in tb[-8:]]}


def git_head(repo):
    try:
        head = (Path(repo) / ".git" / "HEAD").read_text().strip()
        if head.startswith("ref:"):
            return (Path(repo) / ".git" / head.split(" ", 1)[1]).read_text().strip()
        return head
    except OSError:
        return None


def sha_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main(argv=None):
    a = parse_args(argv)
    t_start = time.time()
    # The adapter module is loaded only after sys.path is set, so its imports resolve to the agent's own pins.
    meta_spec = json.loads((HARNESS / "agents" / "registry.json").read_text())[a.agent]
    target, repo, added = setup_paths(a.agent, meta_spec["repo_dir"], meta_spec.get("src_subdir"))

    import numpy as np  # after sys.path: the agent's numpy
    import probe_io as PIO
    import probe_llm as PL

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    adapter = load_adapter(a.agent)

    s = PIO.load(a.scenario)
    names0, d = s["node_ids"], len(s["node_ids"])
    X = s["values"][: s["n_obs"]] if s["n_int"] else s["values"]
    if a.jitter:
        X = X + a.jitter * np.random.default_rng(PIO.score_seed(a.scenario)).standard_normal(X.shape)
    perm = PIO.shuffle_perm(a.scenario, d, a.shuffle_seed)
    shown = list(names0)
    if a.names_map:
        nm = json.loads(Path(a.names_map).read_text(encoding="utf-8"))
        shown = [str(nm.get(n, n)) for n in names0]
    if len(set(shown)) != d:
        sys.exit("ABORTED: variable names are not unique after --names-map")
    names = [shown[perm[k]] for k in range(d)]
    data = X[:, perm]
    context = PIO.domain_context(s["meta"]) if a.context_text is None else a.context_text
    truth = PIO.true_edges(s["g"])
    seed = PIO.score_seed(a.scenario)
    opts = dict(o.split("=", 1) for o in a.agent_opt)

    key = None
    if not a.stub:
        key = PL.resolve_live_key(a.dotenv)
        if not key:
            sys.exit("ABORTED: no OPENAI_API_KEY in the environment or %s" % a.dotenv)
    PL.isolate_environment()

    llm = PL.ProbeLLM(out, a.stub, a.model, a.max_calls, a.max_usd, stub_responder=adapter.stub_reply, api_key=key,
                      assumed_completion_tokens=int(opts.get("assumed_completion_tokens", 600)))
    del key

    class Ctx:
        pass
    ctx = Ctx()
    ctx.names, ctx.data, ctx.context, ctx.model, ctx.llm, ctx.out, ctx.repo, ctx.opts, ctx.stub = (
        names, data, context, a.model, llm, out, repo, opts, a.stub)
    ctx.scenario_key = PIO.file_key(a.scenario)
    ctx.dummy_key = PL.DUMMY_KEY

    print("[probe] %s on %s (%d variables, %d rows), shuffle seed %d, model %s%s, caps calls=%s usd=%s"
          % (a.agent, ctx.scenario_key, d, data.shape[0], a.shuffle_seed, a.model, " (STUB)" if a.stub else "",
             a.max_calls, a.max_usd), flush=True)
    status, fail, res = "ok", None, None
    t_agent = time.time()
    log_path = out / "agent_stdout.log"
    with open(log_path, "a", encoding="utf-8") as logfh:
        logfh.write("\n===== %s start %s\n" % (a.agent, time.strftime("%Y-%m-%dT%H:%M:%S")))
        try:
            with contextlib.redirect_stdout(logfh), contextlib.redirect_stderr(logfh):
                res = adapter.run(ctx)
        except PL.CapReached as e:
            status = "aborted_cap"
            fail = {"type": "CapReached", "message": e.reason, "state": e.state}
        except KeyboardInterrupt:
            status = "interrupted"
            fail = {"type": "KeyboardInterrupt"}
        except Exception as e:  # noqa: BLE001  recorded, never re-raised: the summary must always be written
            status = "failed"
            fail = failure_point(e, repo)
        finally:
            llm.close()
    agent_seconds = time.time() - t_agent

    # ---- map back to original indices: shown position k -> original column perm[k]
    def back(i):
        return perm[int(i)]

    result = {"agent": a.agent, "scenario": ctx.scenario_key, "status": status, "stub": a.stub,
              "shown_order": names, "perm": perm, "context_text": context,
              "convention": "edges are over ORIGINAL column indices of the file; from -> to means cause -> effect"}
    scores = None
    if res is not None:
        directed = [(back(i), back(j)) for i, j in res["directed"]]
        undecided = [(back(i), back(j)) for i, j in res["undirected"]]
        src = res.get("edge_source", {})
        result["directed"] = [{"from_idx": back(i), "to_idx": back(j), "from": names0[back(i)], "to": names0[back(j)],
                               "source": src.get((i, j), res.get("default_source", "llm"))} for i, j in res["directed"]]
        result["undecided"] = [{"a_idx": back(i), "b_idx": back(j), "a": names0[back(i)], "b": names0[back(j)],
                                "source": src.get((i, j), src.get((j, i), "undecided"))} for i, j in res["undirected"]]
        result["source_counts"] = {}
        for e in result["directed"]:
            result["source_counts"][e["source"]] = result["source_counts"].get(e["source"], 0) + 1
        result["provenance_exposed"] = res.get("provenance_exposed", "")
        result["decision_rule"] = res.get("decision_rule", "")
        extra = {}
        for k, v in (res.get("variants") or {}).items():      # e.g. the LLM-only graph before data
            vd = [(back(i), back(j)) for i, j in v["directed"]]
            vu = [(back(i), back(j)) for i, j in v.get("undirected", [])]
            extra[k] = {"directed": [[i, j] for i, j in vd], "undecided": [[i, j] for i, j in vu],
                        "note": v.get("note", ""), "scores": PIO.score_graph(vd, vu, truth, d, seed)}
        result["variants"] = extra
        result["agent_notes"] = res.get("notes", {})
        scores = PIO.score_graph(directed, undecided, truth, d, seed)
        result["scores"] = scores
    (out / "result.json").write_text(json.dumps(result, indent=1, default=str), encoding="utf-8")

    st = llm.state()
    summary = {
        "agent": a.agent, "ticket": "AUD-37 / AB-05", "scenario": ctx.scenario_key, "scenario_path": a.scenario,
        "variables": d, "rows": int(data.shape[0]), "true_edges": len(truth), "shuffle_seed": a.shuffle_seed,
        "jitter": a.jitter, "context_text": context, "names_map": a.names_map,
        "score_seed": seed, "mode": "stub" if a.stub else "live", "model": a.model, "agent_opts": opts,
        "status": status, "failure_point": fail,
        "calls": st["calls"], "new_api_calls": st["new_api_calls"], "replayed_calls": st["replayed_calls"],
        "error_calls": st["error_calls"], "prompt_tokens": st["prompt_tokens"],
        "completion_tokens": st["completion_tokens"],
        "est_usd_gpt4o_list": round(st["usd_at_gpt4o_list"], 6),
        "est_usd_at_served_prices": round(st["usd_at_served_prices"], 6),
        "price_basis": "gpt-4o list $2.50 / $10.00 per 1M input / output tokens; served-price column uses the per-model "
                       "table in probe_llm.PRICES (gpt-4o-mini $0.15 / $0.60)",
        "token_counter": st["token_counter"], "usage_sources": st["usage_sources"], "served_models": st["served_models"],
        "caps": {"max_calls": a.max_calls, "max_usd": a.max_usd},
        "wall_seconds": round(time.time() - t_start, 2), "agent_seconds": round(agent_seconds, 2),
        "directed_f1_random_rule": scores["random"]["f1"] if scores else None,
        "scores": scores,
        "estimates_note": ("STUB RUN: token counts are counted locally and completion lengths are ASSUMED (see "
                           "calls.jsonl assumed_completion_tokens); cost is an estimate of a live run. The graph and "
                           "its F1 carry no meaning (random stub answers)." if a.stub else
                           "LIVE RUN: usage from the API responses (usage_sources says where any count was local)."),
        "agent_repo": {"path": str(repo), "commit": git_head(repo), "pinned_commit": meta_spec["commit"],
                       "url": meta_spec["url"], "licence": meta_spec["licence"]},
        "sys_path_added": added,
        "harness_sha256": {p.name: sha_file(p) for p in [HARNESS / "agent_probe.py", HARNESS / "probe_llm.py",
                                                         HARNESS / "probe_io.py", HARNESS / "agents" / (a.agent + ".py")]},
        "python": sys.version.split()[0],
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=1, default=str), encoding="utf-8")
    print("[probe] %s: %d calls (%d new, %d replayed), tokens %d + %d, est. $%.4f at gpt-4o list, %.1fs%s"
          % (status, st["calls"], st["new_api_calls"], st["replayed_calls"], st["prompt_tokens"],
             st["completion_tokens"], st["usd_at_gpt4o_list"], summary["wall_seconds"],
             (", F1 %.3f" % scores["random"]["f1"]) if scores else ""), flush=True)
    if fail:
        print("[probe] failure point: %s" % json.dumps(fail, default=str)[:600], flush=True)
    return {"ok": 0, "aborted_cap": 3, "failed": 4, "interrupted": 4}[status]


if __name__ == "__main__":
    sys.exit(main())
