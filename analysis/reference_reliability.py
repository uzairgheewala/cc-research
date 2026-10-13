"""How far each Quarter 1 reference graph can be trusted (BEN-12). No network, no model calls.

  python analysis/reference_reliability.py      # writes analysis/results/reference_reliability/reliability.json

Tiers:
  exact        the graph the data were simulated from (S2; verified against the generator's graph.json by gate D8)
  contested    a curated real-data graph for which published versions disagree (Sachs: compared edge by edge where
               a second version is available here)
  provenance   a curated real-data graph with a named source but no second version to compare against
  mismatched   the dataset differs from the version a public benchmark uses, so scores are not comparable to that benchmark

Inputs: datasets/MAPPING.json (pass 4b), datasets/suite_b1/MAPPING.json, datasets/suite_q1s2/MAPPING.json,
external/bnlearn_sachs/sachs.bif.gz (bnlearn's Sachs network as shipped in the pgmpy 0.1.26 wheel from PyPI),
external/causalarena/real_data_index/real_dataset_index.csv, analysis/results/causalarena_calibration/dataset_match_check.json.
"""
import csv
import gzip
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent / "Causal-Copilot"
OUT = ROOT / "analysis" / "results" / "reference_reliability" / "reliability.json"
BIF = ROOT / "external" / "bnlearn_sachs" / "sachs.bif.gz"
BIF_SHA = "ed1830fbde101ed50cce3c7a3c8cbf1d2f5225531cf35ff09fb3cec0af101bce"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def bif_edges(path):
    edges = set()
    for line in gzip.open(path, "rt", encoding="utf-8"):
        m = re.match(r"probability \( (\w+)(?: \| ([\w, ]+))? \)", line)
        if m and m.group(2):
            for par in m.group(2).split(","):
                edges.add((par.strip(), m.group(1)))
    return edges


def compare(a, b):
    adj_a, adj_b = {frozenset(e) for e in a}, {frozenset(e) for e in b}
    shared = adj_a & adj_b
    same = {e for e in a if e in b}
    rev = {e for e in a if (e[1], e[0]) in b}
    return {"edges_a": len(a), "edges_b": len(b), "shared_adjacencies": len(shared),
            "same_direction": len(same), "reversed": len(rev),
            "only_in_a": sorted("%s->%s" % e for e in a if frozenset(e) not in adj_b),
            "only_in_b": sorted("%s->%s" % e for e in b if frozenset(e) not in adj_a),
            "reversed_pairs_as_in_a": sorted("%s->%s" % e for e in rev),
            "adjacency_jaccard": round(len(shared) / len(adj_a | adj_b), 3)}


def parse_edges(lst):
    return {tuple(s.split("->")) for s in lst}


def shape(edges):
    nodes = {n for e in edges for n in e}
    deg = {n: sum(1 for e in edges if n in e) for n in nodes}
    hub = max(deg, key=deg.get)
    return {"nodes_with_edges": len(nodes), "max_degree_node": hub, "max_degree": deg[hub],
            "share_of_edges_touching_hub": round(deg[hub] / len(edges), 3)}


def main():
    assert sha(BIF) == BIF_SHA, "bnlearn sachs file changed"
    p4b = json.loads((ROOT / "datasets" / "MAPPING.json").read_text(encoding="utf-8"))
    b1 = json.loads((ROOT / "datasets" / "suite_b1" / "MAPPING.json").read_text(encoding="utf-8"))
    s2 = json.loads((ROOT / "datasets" / "suite_q1s2" / "MAPPING.json").read_text(encoding="utf-8"))
    dmc = json.loads((ROOT / "analysis" / "results" / "causalarena_calibration" / "dataset_match_check.json").read_text(encoding="utf-8"))
    idx = list(csv.DictReader(open(ROOT / "external" / "causalarena" / "real_data_index" / "real_dataset_index.csv", encoding="utf-8")))
    ca_sachs = [r for r in idx if r["graph_family"] == "real_cmu_sachs"]
    repo_sachs = parse_edges(p4b["source"]["reference_edges"])
    bn = bif_edges(BIF)
    full = REPO / "data" / "dataset" / "sachs" / "sachs_full.csv"
    full_rows = sum(1 for _ in open(full, encoding="utf-8")) - 1 if full.exists() else None
    out = {"inputs": {"bnlearn_sachs_bif_gz_sha256": BIF_SHA, "bnlearn_source": "pgmpy 0.1.26 wheel (PyPI), pgmpy/utils/example_models/sachs.bif.gz",
                      "causalarena_index_sha256": sha(ROOT / "external" / "causalarena" / "real_data_index" / "real_dataset_index.csv")},
           "families": {}}
    out["families"]["sachs"] = {
        "suite": "S1", "tier": "contested",
        "reference_used": "Causal-Copilot repo data/dataset/sachs/base_graph.npy (%d edges)" % len(repo_sachs),
        "repo_vs_bnlearn": compare(repo_sachs, bn),
        "causalarena_version": {"edges": int(ca_sachs[0]["edges"]) if ca_sachs else None,
                                "graph_source": ca_sachs[0]["graph_source"] if ca_sachs else None,
                                "edge_list_available_here": False,
                                "rows": {r["dataset_id"]: int(r["n"]) for r in ca_sachs}},
        "rows": {"repo_sachs_csv": p4b["source"]["rows"], "repo_sachs_full_csv": full_rows},
        "consequence": ("Scores on the Sachs arms are agreement with the repo's 19-edge graph. At least three versions exist (19, 17 and 20 "
                       "edges); the repo's and bnlearn's share %d adjacencies and differ in %d direction(s); CausalArena's 20-edge list is "
                       "not available here. Scores are not accuracy and are not comparable to CausalArena's Sachs row."
                       % (len({frozenset(e) for e in repo_sachs} & {frozenset(e) for e in bn}), sum(1 for e in repo_sachs if (e[1], e[0]) in bn)))}
    for fam, f in b1["families"].items():
        m = dmc.get(fam, {})
        E = parse_edges(f["reference_edges"])
        out["families"][fam] = {
            "suite": "S1", "tier": "provenance" if m.get("match") else "mismatched",
            "reference_used": "Causal-Copilot repo %s" % f["reference"],
            "repo_vars_edges_rows": m.get("repo_vars_edges_rows"),
            "causalarena_vars_edges_rows": m.get("causalarena_vars_edges_rows"),
            "matches_causalarena_index": m.get("match"),
            "causalarena_graph_source": next((r["graph_source"] for r in idx if r["dataset_id"].endswith(
                {"abalone": "abalone", "autompg": "auto_mpg", "concrete": "concrete_ccs", "dwd": "dwd"}[fam])), None),
            "shape": shape(E),
            "consequence": ("Counts match CausalArena's indexed version; the tables are not republished there, so identity is not "
                            "confirmed. The graph is an expert graph with no second version here to compare against."
                            if m.get("match") else
                            "Does not match CausalArena's version (variables, edges, rows differ); scores are agreement with the "
                            "repo's graph only and must not be set beside CausalArena's Auto MPG row.")}
    for fam, f in s2["families"].items():
        out["families"][fam] = {
            "suite": "S2", "tier": "exact" if f["gates"]["D8_reference_matches_release_and_graph_json"] else "unverified",
            "scenario_id": f["scenario_id"], "reference_used": "release g, checked against %s" % f["graph_json"],
            "edges": f["edges"], "variables": f["variables"],
            "consequence": "The reference is the graph the data were simulated from; scores are accuracy against the generating "
                           "graph. The scenario and its names were written by CausalArena's generator, so a model may recognise "
                           "the domain story but cannot have seen this graph unless it saw the release."}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    c = out["families"]["sachs"]["repo_vs_bnlearn"]
    print("sachs repo vs bnlearn: %d vs %d edges, %d shared adjacencies (%d same direction, %d reversed), jaccard %.3f"
          % (c["edges_a"], c["edges_b"], c["shared_adjacencies"], c["same_direction"], c["reversed"], c["adjacency_jaccard"]))
    for k, v in out["families"].items():
        print("%-9s %-5s %s" % (k, v["suite"], v["tier"]))


if __name__ == "__main__":
    main()
