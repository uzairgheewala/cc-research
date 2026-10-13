"""AUD-11 / BND-08: estimate the live cost and time of a plan from its stub runs, calibrated on recorded live runs.

  python analysis/stub_cost.py --stub-label s2stub --live-label-prefix b1_ --out analysis/results/stub_cost/bnd08_estimate.json

Inputs: runs/*/llm_calls.jsonl. A stub run records every prompt the pipeline would send (the stub answers instead of the API);
a live run records the API's usage block. Per caller function (file:function of the first stack frame):
  live calibration   prompt tokens per prompt character, mean completion tokens, mean API seconds per call
  stub measurement   calls and prompt characters per run
Estimate per stub run = sum over its callers of (prompt chars x tokens/char) and (calls x mean completion tokens); callers
never seen live use the pooled live ratio and the pooled mean completion.
Two cycle-step cases, because the stub's well-formed answers keep the cycle loop going while live answers crashed it on the
first call in 9 of 9 entries (bundle 1, crash C1): "crash" keeps only the first LLM_remove_cycles call; "loop" keeps all.
"""
import argparse
import glob
import json
import os
import statistics as st
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CYCLE = "postprocess/judge_functions.py:LLM_remove_cycles"


def caller(rec):
    c = rec["caller"][0].split(":")
    return c[0] + ":" + c[-1]


def prompt_chars(rec):
    n = 0
    for a in rec.get("api") or []:
        for m in (a.get("request") or {}).get("messages", []):
            c = m.get("content")
            n += len(c) if isinstance(c, str) else len(json.dumps(c))
    return n


def runs(pred):
    out = []
    for mf in sorted(glob.glob(str(ROOT / "runs" / "*" / "meta.json"))):
        meta = json.load(open(mf, encoding="utf-8"))
        if pred(meta):
            out.append((Path(mf).parent, meta))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stub-label", required=True)
    ap.add_argument("--live-label-prefix", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cal = defaultdict(lambda: {"chars": 0, "ptok": 0, "ctok": [], "sec": []})
    live = runs(lambda m: not m.get("stub_llm") and (m.get("label") or "").startswith(a.live_label_prefix))
    for rd, _ in live:
        for line in open(rd / "llm_calls.jsonl", encoding="utf-8"):
            r = json.loads(line)
            for api in r.get("api") or []:
                u = ((api.get("response") or {}).get("usage") or {})
                if not u:
                    continue
                k = caller(r)
                cal[k]["chars"] += sum(len(m.get("content") or "") for m in api["request"]["messages"] if isinstance(m.get("content"), str))
                cal[k]["ptok"] += u.get("prompt_tokens", 0)
                cal[k]["ctok"].append(u.get("completion_tokens", 0))
                cal[k]["sec"].append(float(api.get("duration_s") or 0))
    pooled_ratio = sum(v["ptok"] for v in cal.values()) / max(1, sum(v["chars"] for v in cal.values()))
    allc = [x for v in cal.values() for x in v["ctok"]]
    alls = [x for v in cal.values() for x in v["sec"]]
    pooled_ctok, pooled_sec = st.mean(allc), st.mean(alls)
    calib = {k: {"calls": len(v["ctok"]), "tokens_per_char": v["ptok"] / v["chars"] if v["chars"] else None,
                 "mean_completion": st.mean(v["ctok"]), "mean_api_s": st.mean(v["sec"])} for k, v in cal.items()}
    res = {"tickets": ["AUD-11", "BND-08"], "live_runs_used": len(live), "pooled": {"tokens_per_char": pooled_ratio,
           "mean_completion": pooled_ctok, "mean_api_s": pooled_sec}, "calibration": calib, "stub_runs": []}
    for rd, meta in runs(lambda m: m.get("stub_llm") and m.get("label") == a.stub_label):
        per = defaultdict(lambda: {"calls": 0, "chars": 0})
        recs = [json.loads(l) for l in open(rd / "llm_calls.jsonl", encoding="utf-8")]
        for r in recs:
            per[caller(r)]["calls"] += 1
            per[caller(r)]["chars"] += prompt_chars(r)
        summ = json.load(open(rd / "summary.json", encoding="utf-8")) if (rd / "summary.json").exists() else {}
        est = {}
        for case in ("crash", "loop"):
            pt = ct = sec = 0.0
            calls = 0
            for k, v in per.items():
                n, ch = v["calls"], v["chars"]
                if case == "crash" and k == CYCLE and n:
                    ch, n = ch / n, 1
                c = calib.get(k, {})
                pt += ch * (c.get("tokens_per_char") or pooled_ratio)
                ct += n * c.get("mean_completion", pooled_ctok)
                sec += n * c.get("mean_api_s", pooled_sec)
                calls += n
            est[case] = {"calls": calls, "prompt_tokens": round(pt), "completion_tokens": round(ct), "api_seconds": round(sec)}
        res["stub_runs"].append({"run": rd.name, "dataset": meta.get("dataset"), "status": summ.get("status"),
                                 "wall_s": summ.get("pipeline_wall_time_s"),
                                 "per_caller": {k: dict(v) for k, v in sorted(per.items())}, "estimate": est})
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    for r in res["stub_runs"]:
        print(r["run"], r["wall_s"], r["estimate"])
    print("pooled", res["pooled"], "live runs", len(live))


if __name__ == "__main__":
    main()
