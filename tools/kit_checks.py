"""The once-per-kit checks of AGENTS.md, as one command a wave sheet can run on Uzair's machine (INF-10).

Tickets: INF-10

    python tools/kit_checks.py --out jobs/waves/A/out/checks.json

Runs, in order: tracker/verify.py, tracker/trace.py check, tracker/snapshot.py, tools/secret_scan.py, tools/ci_check.py,
site/build.py. Each step's exit code and the last lines of its output are recorded; the trace check's error count is parsed
from its summary line. Runs on the machine that holds runs/ and external/, which the agent's sandbox does not.
"""
import argparse, json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STEPS = [("verify", ["tracker/verify.py"]), ("trace", ["tracker/trace.py", "check"]), ("snapshot", ["tracker/snapshot.py"]),
         ("secret_scan", ["tools/secret_scan.py"]), ("ci_check", ["tools/ci_check.py"]), ("site", ["site/build.py"])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = {"tickets": ["INF-10"], "steps": {}}
    for name, args in STEPS:
        t0 = time.time()
        p = subprocess.run([sys.executable] + args, cwd=str(ROOT), capture_output=True, text=True)
        txt = (p.stdout + p.stderr).strip().splitlines()
        rec = {"exit": p.returncode, "seconds": round(time.time() - t0, 1), "tail": txt[-12:]}
        if name == "trace":
            m = re.search(r"(\d+) errors, (\d+) warnings", "\n".join(txt))
            rec["errors"], rec["warnings"] = (int(m.group(1)), int(m.group(2))) if m else (None, None)
        if name == "site":
            m = re.search(r"(\d+) errors, (\d+) warnings, (\d+) pages to re-read", "\n".join(txt))
            rec["errors"], rec["reread"] = (int(m.group(1)), int(m.group(3))) if m else (None, None)
        out["steps"][name] = rec
        print("[checks] %-11s exit %s" % (name, p.returncode), flush=True)
    out["trace_errors"] = out["steps"]["trace"].get("errors")
    out["site_errors"] = out["steps"]["site"].get("errors")
    Path(args and a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
