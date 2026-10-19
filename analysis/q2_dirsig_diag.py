"""Why the direction signals sit near a coin flip: their accuracy on true found links by property of the child (dev, D).

Joins analysis/results/q2_v3/dirsig_links_dev.jsonl.gz with, per true link cause -> child:
  indeg      the child's number of true parents (1, 2, 3, 4+): other parents act as noise for a pairwise signal
  family     the child's executable mechanism family from the scenario's mechanism_execution_plan.json
  masspoint  share of the child's rows on its single most frequent value (clamps, floors, zero inflation)
  noise      the child has a noise model in the plan (anything but none / deterministic)

  python analysis/q2_dirsig_diag.py -> analysis/results/q2_v3/dirsig_diag_dev.json
"""
import gzip, json, sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "ledger"))
RES = ROOT / "analysis" / "results" / "q2_v3"
ART = ROOT / "external" / "causalarena" / "scm"


def mechanism_map(family, scen_name):
    """{node_id: executable mechanism family} for one scenario, or {} if its plan has no per-node families."""
    rest = scen_name[len(family) + 1:].split("__")[0]
    for dom in sorted((ART / family / "artifacts").iterdir(), key=lambda p: -len(p.name)):
        if rest.startswith(dom.name + "_"):
            sid = rest[len(dom.name) + 1:]
            for d in dom.iterdir():
                if d.name.split("_", 1)[1].startswith(sid + "_") or d.name.split("_", 1)[1] == sid:
                    p = d / "mechanism_execution_plan.json"
                    if not p.exists():
                        return {}
                    j = json.load(open(p))
                    out = {}
                    for n in j.get("node_execution_plan") or []:
                        out[n["node_id"]] = n.get("executable_mechanism_family") or "unknown"
                    for n in j.get("node_execution_table") or []:
                        op = (n.get("operation") or {}).get("op")
                        out[n["node_id"]] = "table:" + str(op)
                    return out
    return {}


def main():
    from score import bench
    rows = []
    with gzip.open(RES / "dirsig_links_dev.jsonl.gz", "rt") as fh:
        for line in fh:
            r = json.loads(line)
            if r["regime"] == "D" and r["truth"] != 0:
                rows.append(r)
    byfile = defaultdict(list)
    for r in rows:
        byfile[(r["family"], r["file"])].append(r)
    mech_cache = {}
    for (fam, f), rs in byfile.items():
        I = bench.truth_info(fam, f)
        X = np.asarray(bench.load(str(next(p for p in bench.files(fam, split="dev") if p.name == f)))["values"], dtype=float)
        names = I["names"]
        indeg = defaultdict(int)
        for a, b in I["T"]:
            indeg[b] += 1
        sc = bench.scenario_of(f)
        if sc not in mech_cache:
            mech_cache[sc] = mechanism_map(fam, sc)
        mm = mech_cache[sc]
        for r in rs:
            child = r["b"] if r["truth"] > 0 else r["a"]
            col = X[:, child]
            _, cnt = np.unique(col, return_counts=True)
            r["indeg"] = min(indeg[child], 4)
            r["mech"] = mm.get(names[child], "unmapped")
            r["masspoint"] = float(cnt.max() / len(col))
    sigs = list(rows[0]["s"])

    def acc(rs, sig):
        v = [(r["s"][sig], r["truth"]) for r in rs if r["s"][sig] not in (None, 0)]
        return {"n": len(v), "acc": round(sum((s > 0) == (t > 0) for s, t in v) / len(v), 3) if len(v) >= 25 else None}

    out = {}
    for fam in ("semantic", "formula"):
        R = [r for r in rows if r["family"] == fam]
        d = {"links": len(R), "mapped_share": round(sum(r["mech"] != "unmapped" for r in R) / len(R), 3)}
        d["indeg"] = {str(k): {"n": sum(r["indeg"] == k for r in R), **{s: acc([r for r in R if r["indeg"] == k], s)["acc"] for s in sigs}} for k in (1, 2, 3, 4)}
        mp_bins = [(0, 0.01, "none"), (0.01, 0.05, "1-5%"), (0.05, 0.2, "5-20%"), (0.2, 1.01, "20%+")]
        d["masspoint"] = {lab: {"n": sum(lo <= r["masspoint"] < hi for r in R), **{s: acc([r for r in R if lo <= r["masspoint"] < hi], s)["acc"] for s in sigs}}
                          for lo, hi, lab in mp_bins}
        fams = defaultdict(list)
        for r in R:
            fams[r["mech"]].append(r)
        d["mechanism"] = {m: {"n": len(rs), **{s: acc(rs, s)["acc"] for s in sigs}} for m, rs in sorted(fams.items(), key=lambda kv: -len(kv[1])) if len(rs) >= 40}
        clean = [r for r in R if r["indeg"] == 1 and r["masspoint"] < 0.01]
        d["clean_single_parent_no_masspoint"] = {"n": len(clean), **{s: acc(clean, s)["acc"] for s in sigs}}
        out[fam] = d
        print("==", fam, "links", len(R), "mechanism mapped", d["mapped_share"])
        hdr = "%-34s %5s " % ("", "n") + " ".join("%7s" % s.split("_")[0] for s in sigs)
        print(hdr)
        for grp in ("indeg", "masspoint", "mechanism"):
            for k, v in d[grp].items():
                print("%-34s %5d " % (grp + ":" + k, v["n"]) + " ".join("%7s" % (v[s] if v[s] is not None else "-") for s in sigs))
        v = d["clean_single_parent_no_masspoint"]
        print("%-34s %5d " % ("clean (1 parent, no mass point)", v["n"]) + " ".join("%7s" % (v[s] if v[s] is not None else "-") for s in sigs))
    json.dump(out, open(RES / "dirsig_diag_dev.json", "w"), indent=1)


if __name__ == "__main__":
    main()
