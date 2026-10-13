"""AB-07 / A3 knowledge elicitation (DEC-02, approved 2026-10-12): build the tier requests and the pre-registration.

  python analysis/a3_make_requests.py --root external/causalarena --out plans/a3_tiers_requests.jsonl --prereg plans/a3_prereg.json

One request per scenario x name arm x phrasing: 50 public semantic + 50 public formula scenarios (rep000 file gives the
names and the graph; all 5 replicate files share them), arms real / neutral / moved, three phrasings = 900 requests.
The model is asked ONLY for tiers (an ordered partition of the shown names, earliest first), never for edges.

  real     the scenario's own variable names
  neutral  V01..Vd, numbered by the position shown (the shown order is random, so numbers carry no order)
  moved    the real names permuted among the variables (a derangement; seeded): the name shown for variable i is the
           real name of variable sigma(i). Scored "by label" (does the model follow the names?) and "by data"
Shown order: a permutation seeded by crc32(scenario id) + SALT, the same in all arms and phrasings of a scenario.
Nothing else is shown: no scenario title, no data, no graph.

The pre-registration file records, before any live call: sha256 of the request file, of each prompt template, of the
scorer (analysis/a3_score.py) and of this script; thresholds O1-O5 exactly as in program v2; the model and call caps.
harness/tiers_runner.py refuses a live run whose request file does not match the pre-registration.
No model calls. Tickets: AUD-48, DEC-02, RQ-10..RQ-14
"""
import argparse, hashlib, json, os, sys, zlib
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import causalarena_io as CA  # noqa: E402

SALT = 20261012
TEMPLATES = [
    ("p0", "Below are the variables measured in one system, listed in random order:\n{names}\n\n"
           "Sort them into tiers by causal order: tier 1 holds variables that nothing else in the list causes (inputs, settings, "
           "background conditions); each later tier may be caused only by variables in earlier tiers; the last tier holds the "
           "most downstream outcomes. Use as many tiers as you need. Put every variable in exactly one tier, spelled exactly as "
           "given. If the names give you no basis to order some variables, put them together in one tier.\n"
           "Reply with JSON only: {{\"tiers\": [[\"name\", ...], [\"name\", ...], ...]}} with the earliest tier first."),
    ("p1", "Variables (random order):\n{names}\n\n"
           "Using only what these names mean, group them into an ordered list of tiers so that a variable can only be "
           "influenced by variables in earlier tiers. First tier = root causes / inputs; last tier = final outcomes. "
           "Every variable must appear exactly once, spelled exactly as listed. Variables you cannot order go in the same tier.\n"
           "Answer with JSON only, earliest tier first: {{\"tiers\": [[...], [...]]}}"),
    ("p2", "A dataset has these columns (shown in random order):\n{names}\n\n"
           "Which come first causally? Partition the columns into tiers ordered from upstream to downstream: nothing in a tier "
           "causes anything in an earlier tier. Include each column exactly once with its exact spelling; if you cannot tell "
           "the order of some columns, keep them in a single tier rather than guessing.\n"
           "Return only this JSON: {{\"tiers\": [[\"col\", ...], ...]}} (upstream tier first)."),
]
THRESHOLDS = {
    "O1": {"claim": "with real names the model's tiers order true edges correctly (semantic)",
           "support": "correct >= 0.70 and contradicted <= 0.10", "refute": "correct < 0.50 or contradicted > 0.25"},
    "O2": {"claim": "with neutral names it supplies nothing", "support": "correct - contradicted <= 0.05", "refute": "correct - contradicted > 0.15"},
    "O3": {"claim": "with moved names its tiers follow the labels",
           "support": "by label: as O1; by data: correct - contradicted <= 0.05", "refute": "by data: correct - contradicted > 0.15"},
    "O4": {"claim": "regression on the model's tiers (real names, shuffled columns) reaches the best published semantic number",
           "support": "mean directed F1 >= 0.634 on public semantic", "refute": "<= 0.50"},
    "O5": {"claim": "the same on formula against 0.524", "support": ">= 0.524", "refute": "<= 0.40"},
}
SCORING_RULES = {
    "edge_order": "a true edge u->v is 'correct' if tier(u) < tier(v), 'contradicted' if tier(u) > tier(v), 'tied' otherwise; "
                  "shares are over all true edges of the scenario; a variable missing from a reply makes the request an abstention",
    "aggregation": "per arm and family: mean over scenarios of the per-scenario shares, for each phrasing and for the consensus "
                   "tiers (median tier position across the three phrasings after normalising each to [0, 1]); verdicts use consensus",
    "abstention": "an abstained request (invalid twice) counts as no information: correct = contradicted = 0 for that scenario/phrasing; reported separately",
    "O4_O5": "analysis/order_value.tier_regression (alpha 0.01) on all 5 replicate obs_only files of each scenario, consensus tiers; "
             "directed F1 against the true graph; columns order is irrelevant to the regression and recorded as shuffled",
    "splits": "verdicts on all 50 + 50 public scenarios; dev and test halves (plans/splits.json) reported separately",
}


def sha(b):
    return hashlib.sha256(b if isinstance(b, bytes) else b.encode()).hexdigest()


def derangement(d, rng):
    while True:
        p = rng.permutation(d)
        if all(p[i] != i for i in range(d)):
            return [int(x) for x in p]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(HERE.parent / "external" / "causalarena"))
    ap.add_argument("--out", default=str(HERE.parent / "plans" / "a3_tiers_requests.jsonl"))
    ap.add_argument("--prereg", default=str(HERE.parent / "plans" / "a3_prereg.json"))
    ap.add_argument("--model", default="gpt-4o")
    a = ap.parse_args()
    splits = json.load(open(HERE.parent / "plans" / "splits.json", encoding="utf-8"))["families"]
    lines, scen_index = [], {}
    for fam in ("semantic", "formula"):
        folder = Path(a.root) / "scm" / fam / "data" / ("%s_obs_only" % fam)
        reps = sorted(f for f in os.listdir(folder) if f.endswith("rep000.npz"))
        for f in reps:
            s = CA.load(folder / f)
            scen = s["meta"]["scenario_id"]
            d = len(s["node_ids"])
            rng = np.random.default_rng(SALT + zlib.crc32(scen.encode()))
            shown = [int(x) for x in rng.permutation(d)]           # shown position k -> variable shown[k]
            sigma = derangement(d, rng)                             # moved arm: variable i shown with real name of sigma[i]
            real = s["node_ids"]
            labels = {"real": [real[i] for i in range(d)], "neutral": [None] * d, "moved": [real[sigma[i]] for i in range(d)]}
            for k, v in enumerate(shown):
                labels["neutral"][v] = "V%02d" % (k + 1)
            slug = next((sl for sl in splits[fam]["dev"] + splits[fam]["test"] if sl in f), None)
            split = "dev" if slug in splits[fam]["dev"] else ("test" if slug in splits[fam]["test"] else "unassigned")
            scen_index["%s/%s" % (fam, scen)] = {"family": fam, "scenario": scen, "file_rep000": f, "d": d, "shown_order": shown,
                                                  "sigma_moved": sigma, "labels": labels, "split": split,
                                                  "true_edges": sorted([list(e) for e in CA.true_edges(s["g"])])}
            for arm in ("real", "neutral", "moved"):
                names_block = "\n".join("- %s" % labels[arm][v] for v in shown)
                for pid, tpl in TEMPLATES:
                    lines.append({"id": "%s|%s|%s|%s" % (fam, scen, arm, pid), "family": fam, "scenario": scen, "arm": arm,
                                  "phrasing": pid, "split": split, "names_shown": [labels[arm][v] for v in shown],
                                  "prompt": tpl.format(names=names_block)})
    body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in lines)
    Path(a.out).write_text(body, encoding="utf-8")
    idx_path = Path(a.out).with_name("a3_scenarios.json")
    json.dump(scen_index, open(idx_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    est_prompt = sum(len(r["prompt"]) for r in lines) / 4
    est_completion = sum(12 * len(r["names_shown"]) + 20 for r in lines)
    usd = est_prompt / 1e6 * 2.5 + est_completion / 1e6 * 10.0
    prereg = {"ticket": "AUD-48", "decision": "DEC-02 approved 2026-10-12 (docs/decisions/2026-10-12_audit_dag.md)",
              "requests_file": os.path.relpath(a.out, HERE.parent), "requests": len(lines),
              "requests_sha256": sha(body.encode("utf-8")), "scenarios_file_sha256": sha(idx_path.read_bytes()),
              "templates": {pid: {"sha256": sha(t), "text": t} for pid, t in TEMPLATES},
              "generator_sha256": sha(Path(__file__).read_bytes()),
              "scorer": "analysis/a3_score.py", "scorer_sha256": sha((HERE / "a3_score.py").read_bytes()) if (HERE / "a3_score.py").exists() else None,
              "thresholds": THRESHOLDS, "scoring_rules": SCORING_RULES,
              "model": a.model, "temperature": 0, "max_tokens": 1500, "retries": 1,
              "call_cap": 2 * len(lines), "estimate": {"prompt_tokens": int(est_prompt), "completion_tokens": int(est_completion),
                                                       "usd_at_gpt4o_list": round(usd, 2), "method": "chars/4 for prompts; 12 tokens per name + 20 for replies"},
              "written_before_any_live_call": True}
    json.dump(prereg, open(a.prereg, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote %d requests (%s), pre-registration %s; estimate %s" % (len(lines), prereg["requests_sha256"][:12], a.prereg, prereg["estimate"]))


if __name__ == "__main__":
    main()
