"""The explanation ledger (wave B, B-1): every dev gap of kernel v3 split into typed segments with their state.

Tickets: TGT-18, TGT-19

    python analysis/explanation_ledger.py [--out analysis/results/q2_v3/explanation_ledger.json]

One record per segment, the shared shape of claude/wave-b-parallel-2026-10-20.md rule 7:
  {board, gap, segment, size, unit, state, ticket, report, evidence}
state is one of: unattributed, attributed, mechanism_known, walled, lever_disputed, lever_chosen, acted_on.
The sizes of a gap's segments sum to the gap's total in analysis/results/q2_v3/anatomy_dev.json (checked; the script
refuses to write otherwise). Inputs: anatomy_dev.json (v3_D), explain_dev.json (X1-X4, sheet A). Dev split only.
Segment states follow the evidence, not hopes: 'lever_chosen' means a lever is built and pre-registered (BLD-18, v4
score), 'acted_on' would mean a kernel version that changed the segment was read on held-out data (none yet).
"""
import argparse, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "analysis" / "results" / "q2_v3"
STATES = ("unattributed", "attributed", "mechanism_known", "walled", "lever_disputed", "lever_chosen", "acted_on")
REPORT = "analysis/reports/q2_explain_dev.md"


def records(board, an, ex):
    L, x = an["links"], ex["x123"]
    m, f, d = x["missed"], x["false"], x["x2"]
    R = []

    def add(gap, seg, size, unit, state, ticket, why, evidence):
        assert state in STATES, state
        R.append({"board": board, "gap": gap, "segment": seg, "size": int(size), "unit": unit, "state": state,
                  "ticket": ticket, "report": REPORT, "why": why, "evidence": evidence})
    U = "true links (dev, regime D)"
    add("missed_links", "floor", m["floor"]["n"], U, "walled", "TGT-18",
        "a discrete-aware nested test detects them no more often than it rejects true nulls (X3)", "explain_dev.json x123.x3")
    add("missed_links", "sample_size", m["sample_size"]["n"], U, "mechanism_known", "TGT-18",
        "signal too weak for 1,000 rows; the score never wants them (X1); the DxR regime (5,000 rows) is the reported remedy",
        "explain_dev.json x123.missed.sample_size")
    add("missed_links", "nonlinear_only", m["method_nonlinear"]["n"], U, "lever_chosen", "BLD-18",
        "invisible to the linear score (X1) but a kernel test detects them %.0f points above its null (X4); lever: the v4 score"
        % (100 * ex["x4"]["nonlinear_detected_beyond_null"]), "explain_dev.json x4; plans/v4_prereg.json")
    add("missed_links", "search_gap", m["method_linear"]["n"], U, "lever_chosen", "BLD-18",
        "the score wants %.0f %% of them given the true parents but GES's graph, which the score prefers to the true one, "
        "holds stand-in links instead (X1); lever: a score that fits the mechanisms (v4)" % (100 * m["method_linear"]["share_gain_positive"]),
        "explain_dev.json x123.missed.method_linear, x123.global")
    U = "claimed links that are false (dev, regime D)"
    add("false_links", "shadow", f["shadow"]["n"], U, "lever_chosen", "BLD-18",
        "the linear score wants %.0f %% of them even added to the true graph (X1)" % (100 * f["shadow"]["share_gain_positive"]),
        "explain_dev.json x123.false.shadow")
    add("false_links", "common_cause", f["common_cause"]["n"], U, "lever_chosen", "BLD-18",
        "the linear score wants %.0f %% of them given the true graph (X1)" % (100 * f["common_cause"]["share_gain_positive"]),
        "explain_dev.json x123.false.common_cause")
    n_u = f["unrelated"]["n"]
    n_um = round(n_u * f["unrelated"]["share_gain_positive"])
    add("false_links", "unrelated_wanted_by_score", n_um, U, "mechanism_known", "BLD-18",
        "wanted by the linear score given the true graph (X1)", "explain_dev.json x123.false.unrelated")
    add("false_links", "unrelated_neighbourhood", n_u - n_um, U, "attributed", "TGT-18",
        "not wanted given the true graph: added because of the wrong neighbourhood GES built (follows the segments above)",
        "explain_dev.json x123.false.unrelated")
    U = "found true links whose committed direction is wrong (dev, regime D)"
    add("reversed_directions", "skeleton_caused", d["ledger_reversed_fixed_by_true_skeleton"], U, "mechanism_known", "TGT-19",
        "the same orientation rules get them right on the true skeleton (X2)", "explain_dev.json x123.x2")
    add("reversed_directions", "rule_caused", d["ledger_reversed_still_reversed_true_skeleton"], U, "mechanism_known", "TGT-19",
        "still reversed on the true skeleton: Fisher-z collider tests on nonlinear data (X2)", "explain_dev.json x123.x2")
    add("reversed_directions", "open_on_true_skeleton", d["ledger_reversed_open_true_skeleton"], U, "attributed", "TGT-19",
        "left open by the rules on the true skeleton (X2)", "explain_dev.json x123.x2")
    totals = {"missed_links": L["missed"], "false_links": L["false"], "reversed_directions": an["directions"]["reversed"]}
    return R, totals


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(RES / "explanation_ledger.json"))
    a = ap.parse_args(argv)
    an = json.loads((RES / "anatomy_dev.json").read_text())
    ex = json.loads((RES / "explain_dev.json").read_text())
    out = {"tickets": ["TGT-18", "TGT-19"], "split": "dev", "regime": "D", "kernel": "v3", "states": list(STATES),
           "records": [], "totals": {}, "checks": {}}
    for board in ("semantic", "formula"):
        R, T = records(board, an["families"][board]["v3_D"], ex["families"][board])
        out["records"] += R
        out["totals"][board] = T
        for gap, tot in T.items():
            s = sum(r["size"] for r in R if r["gap"] == gap)
            out["checks"]["%s/%s" % (board, gap)] = {"segments": s, "total": tot, "equal": s == tot}
    bad = [k for k, v in out["checks"].items() if not v["equal"]]
    if bad:
        raise SystemExit("segment sizes do not sum to the gap totals: %s" % {k: out["checks"][k] for k in bad})
    Path(a.out).write_text(json.dumps(out, indent=1))
    print("wrote %s: %d records; sums equal" % (a.out, len(out["records"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
