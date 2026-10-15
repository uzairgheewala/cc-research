"""B0.2 evidence: run the supplier contract's fault-injection suite and write the outcome table.

  python -m supplier.fault_suite --out analysis/results/q2_b0/fault_suite.json

The 7 cases and the data-only check are the ones in tests/test_q2_supplier.py (imported, not copied). Pass: every case
completes with its expected outcome and failure class counted; with every phrasing failed the D+K ledger's claims equal
the data-only claims and the ledger verifies.
"""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT), str(ROOT / "tests"), str(ROOT / "ledger")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "analysis" / "results" / "q2_b0" / "fault_suite.json"))
    a = ap.parse_args()
    import test_q2_supplier as T
    from supplier import contract as C, tiers as TS
    from kernel import knowledge as K
    import verify02
    rows, counts = [], C.Counts()
    for name, replies in T.CASES.items():
        out = C.call(T.scripted(*replies), {"q": name}, TS.schema(T.NAMES), max_tokens=100)
        counts.add(out)
        rows.append({"case": name, "outcome": out.status, "expected": T.EXPECT[name], "failures": [x["failure"] for x in out.attempts],
                     "normalisations": out.normalisations, "attempts": len(out.attempts),
                     "ok": out.status == T.EXPECT[name] and (name not in T.FAILURE or T.FAILURE[name] in [x["failure"] for x in out.attempts])})
    led_d = T.data_only_ledger()
    same = []
    for name, replies in T.CASES.items():
        if T.EXPECT[name] == "accepted_normalised":
            continue
        stmts = {}
        for ph in ("p0", "p1", "p2"):
            o = C.call(T.scripted(*replies), {}, TS.schema([v["name"] for v in led_d["variables"]]), 100)
            stmts[ph] = None if o.status in ("abstained", "stopped") else {"tiers": o.value}
        led_k, info = K.apply_tiers(led_d, stmts)
        same.append({"case": name, "claims_equal_data_only": [(c["x"], c["y"], c["relation"]) for c in led_k["claims"]] ==
                     [(c["x"], c["y"], c["relation"]) for c in led_d["claims"]],
                     "verify_failures": {k: len(v) for k, v in verify02.verify(led_k).items() if v}})
    res = {"tickets": ["CAP-10", "TGT-13", "BLD-04"], "gate": "B0.2", "cases": rows, "counts": counts.as_dict(), "data_only_when_failed": same,
           "pass": all(r["ok"] for r in rows) and all(s["claims_equal_data_only"] and not s["verify_failures"] for s in same)}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    for r in rows:
        print("%-18s %-20s %s" % (r["case"], r["outcome"], "ok" if r["ok"] else "FAIL"))
    print("data-only when failed:", all(s["claims_equal_data_only"] for s in same), "; B0.2", "PASS" if res["pass"] else "FAIL")
    sys.exit(0 if res["pass"] else 1)


if __name__ == "__main__":
    main()
