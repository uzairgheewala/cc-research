"""Leak scan of the neutral-name arms: did any real column name or dataset word reach a prompt before the final graph?

Searches every LLM request (prompt, system prompt, messages) of every live run whose arm has role "neutral" in the
mapping, for every real column label of the family and for the dataset words. Matches are classified as
  template: the matched context also occurs in a non-neutral arm's prompts of the same stage (fixed template text), or
  leak:     anything else before the report stage (stages numbered 08 and later run after the final graph).
No LLM. python neutral_leak_scan.py --runs-dir runs --label b1 --mapping datasets/suite_b1/MAPPING.json --out analysis/results/stability_b1
Gate L1: zero leaks before the final graph.
"""
import argparse, json, os, re, sys
from pathlib import Path

WORDS = ["abalone", "auto mpg", "auto_mpg", "autompg", "concrete", "dwd", "wetterdienst"]
AFTER_FINAL = ("08", "09")


def requests(run_dir):
    f = Path(run_dir) / "llm_calls.jsonl"
    if not f.exists():
        return
    for line in open(f, encoding="utf-8"):
        d = json.loads(line)
        if d.get("level") != "client":
            continue
        a = d.get("args") or {}
        txt = " \n ".join(str(a.get(k) or "") for k in ("prompt", "system_prompt")) + " \n " + json.dumps(a.get("messages") or "")
        yield d.get("stage") or "", txt


def variants(labels):
    """Each real label as written, with spaces for underscores, and without a numbering prefix ("V12_", "v_"): a leak
    need not reuse the exact spelling (added 2026-10-12 for the S2 suite, whose released names carry such prefixes)."""
    out = []
    for l in labels:
        bare = re.sub(r"^[Vv]\d*_", "", l)
        for v in (l, l.replace("_", " "), bare, bare.replace("_", " ")):
            if len(v) >= 4 and v not in out:
                out.append(v)
    return out


def family_words(info):
    """Dataset-level words of a family from its MAPPING entry (scenario id, scenario name, domain), as phrases."""
    out = []
    for k in ("scenario_id", "scenario_name", "domain_id"):
        v = info.get(k)
        if isinstance(v, str):
            for w in (v, v.replace("_", " ")):
                if len(w) >= 6 and w not in out:
                    out.append(w)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs-dir", required=True); ap.add_argument("--label", required=True)
    ap.add_argument("--mapping", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    m = json.load(open(a.mapping, encoding="utf-8"))
    real = {s["family"]: s["column_labels"] for s in m["arms"].values() if s["role"] == "real"}
    real = {f: variants(labels) for f, labels in real.items()}
    fam_words = {f: family_words(info) for f, info in (m.get("families") or {}).items() if isinstance(info, dict)}
    neutral_arms = {k: s for k, s in m["arms"].items() if s["role"] == "neutral"}
    named_ctx = {}          # (family, stage) -> concatenated prompt text of named arms, for the template test
    runs = []
    for mf in sorted(Path(a.runs_dir).glob("*/meta.json")):
        meta = json.load(open(mf, encoding="utf-8"))
        if meta.get("label") != a.label or meta.get("stub_llm"):
            continue
        arm = os.path.basename(str(meta.get("dataset", ""))).replace(".csv", "")
        if arm not in m["arms"]:
            continue
        runs.append((mf.parent, arm))
        if m["arms"][arm]["role"] != "neutral":
            fam = m["arms"][arm]["family"]
            for st, txt in requests(mf.parent):
                named_ctx[(fam, st)] = named_ctx.get((fam, st), "") + "\n" + txt.lower()
    n_req, hits = 0, []
    for rd, arm in runs:
        if arm not in neutral_arms:
            continue
        fam = neutral_arms[arm]["family"]
        for st, txt in requests(rd):
            n_req += 1
            for name in real[fam] + WORDS + fam_words.get(fam, []):
                for mm in re.finditer(r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z])", txt, flags=re.I):
                    ctx = txt[max(0, mm.start() - 40): mm.end() + 40].lower()
                    template = ctx in named_ctx.get((fam, st), "")
                    after = st.startswith(AFTER_FINAL)
                    hits.append({"run": rd.name, "arm": arm, "stage": st, "name": name, "context": ctx,
                                 "class": "after_final_graph" if after else ("template" if template else "leak")})
    leaks = [h for h in hits if h["class"] == "leak"]
    out = {"label": a.label, "neutral_runs": sum(1 for _, arm in runs if arm in neutral_arms), "requests_scanned": n_req,
           "matches": len(hits), "by_class": {c: sum(1 for h in hits if h["class"] == c) for c in ("template", "after_final_graph", "leak")},
           "leaks": leaks[:50], "gate_L1_no_leak_before_final_graph": not leaks}
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "neutral_leak_scan.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "leaks"}))
    sys.exit(0 if not leaks else 1)


if __name__ == "__main__":
    main()
