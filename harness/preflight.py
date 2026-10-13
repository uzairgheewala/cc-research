"""Preflight for Causal-Copilot runs. Checks code identity, environment, imports, external tools,
a deterministic no-LLM smoke test, and (unless --no-llm) one tiny LLM round trip in text and JSON mode.

Usage:  python /research/harness/preflight.py [--no-llm]
Never prints or stores the API key.
"""
import argparse
import datetime
import importlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cc_common import BASELINE_COMMIT, REPO, RESEARCH, Scrubber, dump_json, key_status, verify_tree  # noqa: E402

RESULTS = []          # (section, name, status, detail)   status in PASS / FAIL / WARN / INFO
IMPORTS = ["utils.suppress_logs", "utils.logger", "llm", "global_setting.state", "preprocess.dataset",
           "preprocess.stat_info_functions", "preprocess.eda_generation", "causal_discovery.wrappers",
           "causal_discovery.filter", "causal_discovery.rerank", "causal_discovery.hyperparameter_selector",
           "causal_discovery.program", "postprocess.judge_functions", "postprocess.judge",
           "postprocess.visualization", "report.report_generation", "global_setting.Initialize_state",
           "user.discuss", "main"]


def add(section, name, status, detail=""):
    RESULTS.append({"section": section, "name": name, "status": status, "detail": str(detail)[:1500]})
    print("  [%-4s] %-34s %s" % (status, name, str(detail)[:200]))


def guarded(section, name, fn, warn_only=False):
    t = time.time()
    try:
        detail = fn()
        add(section, name, "PASS", "%s (%.1fs)" % (detail if detail is not None else "", time.time() - t))
        return True
    except BaseException as e:   # noqa: BLE001
        tb = traceback.extract_tb(e.__traceback__)
        where = "%s:%d" % (tb[-1].filename, tb[-1].lineno) if tb else "?"
        add(section, name, "WARN" if warn_only else "FAIL", "%s: %s @ %s" % (type(e).__name__, str(e)[:500], where))
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-llm", action="store_true", help="skip the two tiny LLM calls")
    ap.add_argument("--stub-llm", action="store_true", help="self-test: answer the two calls with the offline stub")
    a = ap.parse_args()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    scrub = Scrubber()
    # Taken before any repo import: importing main.py runs load_dotenv(), which would make a key
    # that came from .env look as if it had been in the process environment all along.
    env_at_start = {k: (k in os.environ) for k in ("OPENAI_API_KEY", "LLM_PROVIDER", "LLM_MODEL")}
    print("=" * 78 + "\nCAUSAL-COPILOT PREFLIGHT  %s\n" % stamp + "=" * 78)

    print("\n[1] Code identity (baseline %s)" % BASELINE_COMMIT)
    if not (REPO / "main.py").is_file():
        add("identity", "repo present", "FAIL", "no main.py under %s (CC_REPO)" % REPO)
        return finish(stamp, scrub)
    ident = verify_tree()
    add("identity", "manifest file intact", "PASS" if ident["manifest_digest_ok"] else "FAIL", ident["manifest"])
    add("identity", "baseline files", "PASS" if not ident["missing"] and not ident["changed"] else "FAIL",
        "%d listed, %d missing, %d changed %s" % (ident["n_listed"], len(ident["missing"]), len(ident["changed"]),
                                                 (ident["missing"] + ident["changed"])[:5] or ""))
    add("identity", "unexpected new files", "PASS" if not ident["extra_unexpected"] else "WARN",
        "%d %s" % (len(ident["extra_unexpected"]), ident["extra_unexpected"][:5] or ""))

    print("\n[2] Runtime")
    add("runtime", "python", "PASS" if sys.version_info[:2] == (3, 10) else "WARN",
        "%s (repo pins 3.10)" % platform.python_version())
    add("runtime", "platform", "INFO", platform.platform())
    for tool, critical in (("dot", True), ("pdflatex", True), ("latexmk", True), ("bibtex", False), ("lacheck", False)):
        p = shutil.which(tool)
        add("runtime", "tool: " + tool, "PASS" if p else ("FAIL" if critical else "WARN"), p or "not on PATH")

    print("\n[3] Imports (repo modules on the CLI path)")
    os.chdir(REPO)
    sys.path.insert(0, str(REPO))
    all_ok = True
    for m in IMPORTS:
        all_ok &= guarded("imports", m, lambda m=m: (importlib.import_module(m), None)[1])
    for m in ("psutil", "dowhy", "dill"):
        guarded("imports", "lib: " + m, lambda m=m: getattr(importlib.import_module(m), "__version__", ""),
                warn_only=(m != "psutil"))

    def torch_info():
        import torch
        return "torch %s, cuda_available=%s" % (torch.__version__, torch.cuda.is_available())
    guarded("imports", "torch", torch_info)

    print("\n[4] Deterministic smoke test (no LLM)")
    if all_ok:
        def smoke_pc():
            import pandas as pd
            import causal_discovery.wrappers as w
            df = pd.read_csv(REPO / "data/dataset/Linear_Gaussian/Linear_Gaussian_data.csv")
            graph, _info, _raw = w.PC({}).fit(df)
            return "PC on Linear_Gaussian -> matrix %s, %d nonzero cells" % (graph.shape, int((graph != 0).sum()))

        def smoke_kci():
            import pandas as pd
            from causallearn.utils.cit import CIT
            df = pd.read_csv(REPO / "data/dataset/Linear_Gaussian/Linear_Gaussian_data.csv").iloc[:200]
            p = CIT(df.to_numpy(), "kci")(0, 1)
            return "KCI p-value(X1, X2 | {}) on 200 rows = %.4g" % p

        def smoke_pickle():
            import pickle
            from global_setting.state import GlobalState
            return "GlobalState pickle round trip, %d bytes" % len(pickle.dumps(pickle.loads(pickle.dumps(GlobalState()))))

        def smoke_latex():
            from plumbum.cmd import latexmk
            d = tempfile.mkdtemp(prefix="cc_latex_")
            tex = os.path.join(d, "t.tex")
            Path(tex).write_text("\\documentclass{article}\\begin{document}ok\\end{document}\n")
            latexmk["-pdf", "-interaction=nonstopmode", "-halt-on-error", "-output-directory=" + d, tex]()
            ok = os.path.isfile(os.path.join(d, "t.pdf"))
            shutil.rmtree(d, ignore_errors=True)
            if not ok:
                raise RuntimeError("latexmk ran but produced no PDF")
            return "latexmk compiled a one-line document"

        guarded("smoke", "PC wrapper fit", smoke_pc)
        guarded("smoke", "KCI test (needs psutil)", smoke_kci)
        guarded("smoke", "state pickle", smoke_pickle)
        guarded("smoke", "latexmk compile", smoke_latex)
    else:
        add("smoke", "skipped", "FAIL", "imports failed above")

    print("\n[5] LLM configuration")
    before = env_at_start
    try:
        from dotenv import load_dotenv
        load_dotenv(REPO / ".env")
    except Exception as e:
        add("llm", ".env load", "WARN", repr(e))
    scrub.refresh()
    provider = os.environ.get("LLM_PROVIDER", "openai (code default)")
    model = os.environ.get("LLM_MODEL", "gpt-4o-mini (code default)")
    add("llm", "provider", "INFO", provider)
    add("llm", "model", "INFO", model)
    ks = key_status()
    src = "process environment" if before["OPENAI_API_KEY"] else ".env file"
    add("llm", "OPENAI_API_KEY", "PASS" if ks == "set" else ("WARN" if (a.no_llm or a.stub_llm) else "FAIL"),
        "%s (source: %s)" % (ks, src) if ks == "set" else "%s -> edit the OPENAI_API_KEY line in Causal-Copilot/.env" % ks)

    if a.no_llm:
        add("llm", "round trip", "INFO", "skipped (--no-llm)")
    elif (ks != "set" and not a.stub_llm) or not all_ok:
        add("llm", "round trip", "FAIL", "not attempted (key or imports not ready)")
    else:
        print("\n[6] LLM round trip (2 tiny calls through the repo's own LLMClient)")
        seen = {}
        if a.stub_llm:
            import stub_llm
            stub_llm.install()
            if ks != "set":
                os.environ["OPENAI_API_KEY"] = "stub-key-not-real"
        try:
            from openai.resources.chat.completions import Completions
            orig = Completions.create

            def create(self_, *aa, **kk):
                r = orig(self_, *aa, **kk)
                seen["model"] = getattr(r, "model", None)
                seen["fingerprint"] = getattr(r, "system_fingerprint", None)
                u = getattr(r, "usage", None)
                seen["tokens"] = seen.get("tokens", 0) + (getattr(u, "total_tokens", 0) or 0)
                return r
            Completions.create = create
        except Exception as e:
            add("llm", "sdk hook", "WARN", repr(e))

        def ping_text():
            from llm import LLMClient
            out = LLMClient().chat_completion(prompt="Reply with the single word: pong")
            return "reply=%r" % str(out)[:40]

        def ping_json():
            from llm import LLMClient
            out = LLMClient().chat_completion(prompt='Return the JSON object {"ok": true}', json_response=True)
            if not isinstance(out, dict):
                raise RuntimeError("JSON mode did not return a dict: %r" % (out,))
            return "reply=%r" % (out,)

        guarded("llm", "text call", ping_text)
        guarded("llm", "JSON-mode call", ping_json)
        add("llm", "served model snapshot", "INFO", "%s (fingerprint %s, %s tokens total)" % (
            seen.get("model"), seen.get("fingerprint"), seen.get("tokens")))
    return finish(stamp, scrub)


def finish(stamp, scrub):
    fails = [r for r in RESULTS if r["status"] == "FAIL"]
    warns = [r for r in RESULTS if r["status"] == "WARN"]
    verdict = "PASS" if not fails else "FAIL"
    out_dir = RESEARCH / "preflight"
    out_dir.mkdir(exist_ok=True)
    path = out_dir / ("preflight_%s_%s.json" % (stamp, verdict))
    try:
        freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True,
                                timeout=120).stdout.splitlines()
    except Exception as e:
        freeze = ["unavailable: %r" % (e,)]
    dump_json(path, {"stamp": stamp, "verdict": verdict, "results": RESULTS, "pip_freeze": freeze}, scrub)
    print("\n" + "=" * 78)
    print("PREFLIGHT %s   (%d failed, %d warnings)   report: %s" % (verdict, len(fails), len(warns), path))
    for r in fails:
        print("  FAIL  %s / %s: %s" % (r["section"], r["name"], r["detail"][:300]))
    print("=" * 78)
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
