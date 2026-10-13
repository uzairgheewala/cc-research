"""AUD-15: does any upstream branch fix the two crash points? Read-only; works on a separate clone, never on Uzair's repo.

  git clone --filter=blob:none --no-checkout https://github.com/Lancelot39/Causal-Copilot $HOME/scratch/cc_up
  python analysis/upstream_check.py --clone $HOME/scratch/cc_up

Crash points at a31aa7c (seen live, pass 4b and bundle 1):
  C1 postprocess/judge_functions.py:562   `return response['nodes']` in LLM_remove_cycles: the reply is requested as free JSON
     (json_response=True, the VarList schema defined above it is never passed), and the model answered with other keys
     (edge_to_remove 5 times, nodes_to_remove 4 times) -> KeyError.
  C2 global_setting/Initialize_state.py:178   `info_extracted["linearity"]`: an empty {} reply -> KeyError.
For each remote branch: does the file exist, is it identical to a31aa7c, does the crash line still occur, and is there a guard.
Output: analysis/results/upstream/upstream_check.json
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent / "Causal-Copilot"
BASE = "a31aa7cab277d7e19478bc326dbec154525969cc"
POINTS = {
    "C1": {"file": "postprocess/judge_functions.py", "line": 562, "crash": r"return\s+response\[['\"]nodes['\"]\]",
           "function": "LLM_remove_cycles", "pickaxe": "return response['nodes']",
           "guard": r"response_format\s*=\s*VarList|response\.get\(['\"]nodes|['\"]nodes['\"]\s+in\s+response|except\s+KeyError"},
    "C2": {"file": "global_setting/Initialize_state.py", "line": 178, "crash": r"info_extracted\[['\"]linearity['\"]\]",
           "function": "global_state_initialization", "pickaxe": 'info_extracted["linearity"]',
           "guard": r"info_extracted\.get\(['\"]linearity|['\"]linearity['\"]\s+in\s+info_extracted|except\s+KeyError"},
}


def function_body(txt, name):
    """Text of `def name(...)` up to the next top-level def/class (guards are judged inside the function only)."""
    m = re.search(r"^def %s\(.*?(?=^(?:def |class )|\Z)" % re.escape(name), txt, re.S | re.M)
    return m.group(0) if m else None


def git(clone, *args):
    return subprocess.run(["git", "-C", str(clone)] + list(args), capture_output=True, text=True, timeout=120)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", required=True)
    a = ap.parse_args()
    clone = Path(a.clone)
    git(clone, "fetch", "--quiet", "origin")
    refs = [l.split() for l in git(clone, "for-each-ref", "--format=%(refname:short) %(objectname) %(committerdate:iso8601-strict)",
                                   "refs/remotes").stdout.splitlines() if "HEAD" not in l.split()[0]]
    out = {"upstream": "https://github.com/Lancelot39/Causal-Copilot", "base": BASE, "points": {}, "branches": []}
    for k, p in POINTS.items():
        local = (REPO / p["file"]).read_text(encoding="utf-8").splitlines()
        out["points"][k] = {**p, "local_line_text": local[p["line"] - 1].strip(),
                            "local_line_matches_crash": bool(re.search(p["crash"], local[p["line"] - 1])),
                            "local_sha256": hashlib.sha256((REPO / p["file"]).read_bytes()).hexdigest()}
    for ref, sha, date in sorted(refs, key=lambda r: r[2]):
        row = {"branch": ref, "commit": sha, "date": date, "is_base": sha == BASE,
               "base_is_ancestor": git(clone, "merge-base", "--is-ancestor", BASE, sha).returncode == 0}
        for k, p in POINTS.items():
            r = git(clone, "show", "%s:%s" % (sha, p["file"]))
            if r.returncode != 0:
                row[k] = {"exists": False}
                continue
            txt = function_body(r.stdout, p["function"])
            if txt is None:
                row[k] = {"exists": True, "function_present": False}
                continue
            base_txt = function_body(git(clone, "show", "%s:%s" % (BASE, p["file"])).stdout, p["function"])
            row[k] = {"exists": True, "function_present": True, "function_identical_to_base": txt == base_txt,
                      "crash_line_present": bool(re.search(p["crash"], txt)),
                      "crash_line_numbers": [i + 1 for i, l in enumerate(txt.splitlines()) if re.search(p["crash"], l)],
                      "guard_present": bool(re.search(p["guard"], txt))}
        out["branches"].append(row)
    for k, p in POINTS.items():
        r = git(clone, "log", "origin/main", "--format=%H %cI %s", "-S", p["pickaxe"], "--", p["file"])
        out["points"][k]["commits_touching_crash_text_on_main"] = r.stdout.splitlines()
    fixed = {k: [b["branch"] for b in out["branches"] if b[k].get("function_present") and not b[k]["crash_line_present"]] for k in POINTS}
    absent = {k: [b["branch"] for b in out["branches"] if not b[k].get("function_present")] for k in POINTS}
    out["summary"] = {"branches": len(out["branches"]),
                      "main_is_base": any(b["branch"] == "origin/main" and b["is_base"] for b in out["branches"]),
                      "newer_than_base": [b["branch"] for b in out["branches"] if b["date"] > "2026-05-15T07:43:14-07:00"],
                      "branches_without_crash_line": fixed, "branches_without_the_function": absent}
    dest = ROOT / "analysis" / "results" / "upstream" / "upstream_check.json"
    dest.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(out["summary"], indent=1))
    for b in out["branches"]:
        print("%-38s %s  C1 %s  C2 %s" % (b["branch"], b["date"][:10],
              {x: b["C1"].get(x) for x in ("function_present", "function_identical_to_base", "crash_line_present", "guard_present")},
              {x: b["C2"].get(x) for x in ("function_present", "function_identical_to_base", "crash_line_present", "guard_present")}))


if __name__ == "__main__":
    main()
