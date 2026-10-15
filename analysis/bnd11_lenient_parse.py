"""BND-11 exploratory (written 2026-10-14, AFTER the pre-registered apply; never replaces R4-R6): how much of the names
part's abstention comes from the strict reply format.

The frozen runner (harness/names_runner.py) accepts only a reply that is exactly the JSON asked for. Live gpt-4o wrapped
most first replies in a Markdown code fence (```json ... ```), so 785 of 786 questions needed the retry and 251 ended as
abstentions. This script re-reads the SAME recorded replies (no model calls) with one change: a reply whose content is
valid after stripping a surrounding code fence is accepted. It writes a lenient copy of the answers and runs the frozen
apply step on it with a separate output file.

  python analysis/bnd11_lenient_parse.py
Outputs: analysis/results/refinement_v2/exploratory_lenient_answers.jsonl and names_s2_exploratory_lenient.json
"""
import json, re, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "plans" / "results" / "bnd11_names_requests.answers.jsonl"
OUTD = ROOT / "analysis" / "results" / "refinement_v2"
VALID = {"A->B", "B->A", "unknown"}
FENCE = re.compile(r"^\s*```(?:json)?\s*(.*?)\s*```\s*$", re.S)


def lenient(text):
    if text is None:
        return None
    m = FENCE.match(text)
    body = m.group(1) if m else text
    try:
        d = json.loads(body)
    except ValueError:
        return None
    if isinstance(d, dict) and set(d) == {"direction"} and d["direction"] in VALID:
        return d["direction"]
    return None


def main():
    rows = [json.loads(l) for l in open(SRC, encoding="utf-8") if l.strip()]
    out, changed = [], Counter()
    for r in rows:
        r2 = dict(r)
        for t in r.get("attempts") or []:
            d = lenient(t.get("reply"))
            if d is not None:
                if r.get("abstained") or r.get("direction") != d:
                    changed["abstention -> answer" if r.get("abstained") else "answer changed"] += 1
                r2["direction"], r2["abstained"] = d, False
                r2["lenient_from_attempt"] = t.get("attempt")
                break
        out.append(r2)
    p = OUTD / "exploratory_lenient_answers.jsonl"
    p.write_text("".join(json.dumps(x) + "\n" for x in out), encoding="utf-8")
    print("strict:", Counter("abstained" if r["abstained"] else r["direction"] for r in rows))
    print("lenient:", Counter("abstained" if r["abstained"] else r["direction"] for r in out), dict(changed))
    subprocess.run([sys.executable, str(ROOT / "analysis" / "refinement_v2.py"), "apply", "--answers", str(p),
                    "--out", str(OUTD / "names_s2_exploratory_lenient.json")], check=True, stdout=subprocess.DEVNULL)
    d = json.loads((OUTD / "names_s2_exploratory_lenient.json").read_text(encoding="utf-8"))
    d["exploratory"] = ("lenient re-parse of the recorded replies (code fence stripped), written after the pre-registered apply; "
                        "reported beside R4-R6, never instead of them")
    (OUTD / "names_s2_exploratory_lenient.json").write_text(json.dumps(d, indent=1, default=float) + "\n", encoding="utf-8")
    for k in ("R4", "R5", "R6"):
        print(k, {kk: v for kk, v in d[k].items() if not isinstance(v, (dict, list))})


if __name__ == "__main__":
    main()
