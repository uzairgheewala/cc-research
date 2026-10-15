"""B5.1 runner: audit every AB-06 agent run with the adapters (audit/adapters.py).

  python -m audit.run_adapters --runs runs/ab06 --out analysis/results/q2_b5/adapters.json

Per agent: runs audited, arrows, sources (data / knowledge / unknown), violation counts by class with examples, and
the names check across arms (real vs swapped, same data and column permutation). Gate B5.1: every flagged violation
names a pair, a claim and a source; 0 'unknown' sources for agents that record provenance.
No model calls. Tickets: BLD-15 (proposed), CAP-09
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from audit import adapters as AD  # noqa: E402

ARMS = ("real", "neutral", "swapped")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default=str(ROOT / "runs" / "ab06"))
    ap.add_argument("--out", default=str(ROOT / "analysis" / "results" / "q2_b5" / "adapters.json"))
    a = ap.parse_args()
    out = {"tickets": ["BLD-15", "CAP-09"], "agents": {}}
    traced_ok = True
    for agent_dir in sorted(Path(a.runs).iterdir()):
        if not agent_dir.is_dir():
            continue
        agent = agent_dir.name
        runs, viol, src, arrows, unknown, uncheck = 0, Counter(), Counter(), 0, 0, 0
        examples = {}
        flips = []
        for scen in sorted(p for p in agent_dir.iterdir() if p.is_dir()):
            res = {}
            for arm in ARMS:
                f = scen / arm / "result.json"
                if not f.exists():
                    continue
                r = json.load(open(f))
                if r.get("status") not in (None, "ok", "completed") and not r.get("directed"):
                    continue
                res[arm] = r
                au = AD.audit_run(agent, r)
                runs += 1
                arrows += au["arrows"]
                unknown += au["unknown_sources"]
                uncheck += not au["checkable"]["I5_I3"]
                for c in au["claims"]:
                    if c["relation"] == "x->y":
                        src[c["direction_source"]] += 1
                for v in au["violations"]:
                    viol[v["class"]] += 1
                    if not (v.get("pair") and v.get("claim") is not None and v.get("source")):
                        traced_ok = False
                    examples.setdefault(v["class"], [])
                    if len(examples[v["class"]]) < 3:
                        examples[v["class"]].append(dict(v, scenario=scen.name, arm=arm))
            if "real" in res and "swapped" in res:
                fl = AD.names_flip(agent, res["real"], res["swapped"])
                for v in fl:
                    viol[v["class"]] += 1
                flips.append({"scenario": scen.name, "flips": len(fl), "knowledge_arrows_real": sum(1 for e in res["real"].get("directed") or []
                                                                                                    if AD.SOURCE_MAP.get(e.get("source")) == "knowledge")})
        out["agents"][agent] = {"runs": runs, "arrows": arrows, "sources": dict(src), "unknown_sources": unknown,
                                "records_provenance": agent in AD.RECORDS_PROVENANCE, "runs_without_data_floor": uncheck,
                                "violations": dict(viol), "examples": examples, "names_pairs": flips}
    cc_path = ROOT / "analysis" / "results" / "q2_b5" / "cc_stages_s2.json"
    if cc_path.exists():
        cc = json.load(open(cc_path))["runs"]
        viol, src, arrows, examples, runs = Counter(), Counter(), 0, {}, 0
        by_family = {}
        for r in cc:
            if not r.get("stages"):
                continue
            au = AD.audit_cc_run(r)
            runs += 1
            arrows += au["arrows"]
            src.update(au["sources"])
            for v in au["violations"]:
                viol[v["class"]] += 1
                if not (v.get("pair") and v.get("claim") is not None and v.get("source")):
                    traced_ok = False
                examples.setdefault(v["class"], [])
                if len(examples[v["class"]]) < 3:
                    examples[v["class"]].append(dict(v, run=r["run_id"], role=r["role"]))
            by_family.setdefault(r["family"], {})[r["role"]] = r
        flips = 0
        for fam, roles in by_family.items():
            if "real" in roles and "swapped" in roles:
                Dr, _ = AD._sets_by_name(roles["real"]["stages"]["S3"])
                D1r, _ = AD._sets_by_name(roles["real"]["stages"]["S1"])
                lab_r, lab_s = roles["real"]["labels"], roles["swapped"]["labels"]
                # same data, names moved: compare by column position
                pos_r = {n: i for i, n in enumerate(lab_r)}
                Ds, Us = AD._sets_by_name(roles["swapped"]["stages"]["S3"])
                pos_s = {n: i for i, n in enumerate(lab_s)}
                Dsp = {(pos_s[x], pos_s[y]) for x, y in Ds}
                Usp = {tuple(sorted((pos_s[u[0]], pos_s[u[1]]))) for u in Us}
                for x, y in Dr:
                    if (x, y) in D1r:
                        continue
                    i, j = pos_r[x], pos_r[y]
                    if (j, i) in Dsp or ((i, j) not in Dsp and tuple(sorted((i, j))) not in Usp):
                        flips += 1
        viol["direction_follows_names"] += flips
        out["agents"]["causal_copilot_gpt4o"] = {"runs": runs, "arrows": arrows, "sources": dict(src), "unknown_sources": 0,
                                                 "records_provenance": False, "provenance": "reconstructed from stage graphs (S0-S3)",
                                                 "runs_without_data_floor": 0, "violations": dict(viol), "examples": examples}
    out["B5.1"] = {"every_violation_traced": traced_ok,
                   "unknown_sources_where_provenance_recorded": sum(v["unknown_sources"] for v in out["agents"].values() if v["records_provenance"])}
    out["B5.1"]["pass"] = out["B5.1"]["every_violation_traced"] and out["B5.1"]["unknown_sources_where_provenance_recorded"] == 0
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=1)
    for ag, v in out["agents"].items():
        print("%-11s runs %3d arrows %4d sources %s unknown %d no-floor %d violations %s" % (ag, v["runs"], v["arrows"], v["sources"], v["unknown_sources"],
                                                                                          v["runs_without_data_floor"], v["violations"]))
    print("B5.1", out["B5.1"])


if __name__ == "__main__":
    main()
