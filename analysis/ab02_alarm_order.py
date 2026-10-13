"""AB-02 (AUD-34): column order vs causal order in the gCastle PCIC 2021 alarm datasets (second-scoreboard candidate).

  python analysis/ab02_alarm_order.py --data external/gcastle_alarm --out analysis/results/ab02/alarm_order.json

For each of 18V_55N_Wireless, 24V_439N_Microwave, 25V_474N_Microwave (raw.githubusercontent.com/gcastle-hub/dataset,
MIT; sha256 recorded): the share of true edges running from an earlier to a later alarm id (0.5 = no order signal), and
Kendall's tau between the alarm id and its depth in the true DAG (P3 needs tau > 0.3 on some release). No model calls.
Tickets: AUD-34, BEN-07
"""
import argparse, hashlib, json
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.stats import kendalltau

SETS = ("18V_55N_Wireless", "24V_439N_Microwave", "25V_474N_Microwave")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    res = {"tickets": ["AUD-34", "BEN-07"], "source": "https://raw.githubusercontent.com/gcastle-hub/dataset/master/alarm/<name>.tar.gz", "sets": {}}
    for n in SETS:
        tgz = Path(a.data) / ("%s.tar.gz" % n)
        D = np.load(Path(a.data) / n / n / "DAG.npy")
        E = [tuple(map(int, e)) for e in np.argwhere(D != 0)]
        G = nx.DiGraph()
        G.add_nodes_from(range(D.shape[0]))
        G.add_edges_from(E)
        depth = {v: 0 for v in G}
        for v in nx.topological_sort(G):
            for w in G.successors(v):
                depth[w] = max(depth[w], depth[v] + 1)
        tau = kendalltau(range(D.shape[0]), [depth[i] for i in range(D.shape[0])])
        res["sets"][n] = {"tar_sha256": hashlib.sha256(tgz.read_bytes()).hexdigest() if tgz.exists() else None, "variables": int(D.shape[0]),
                          "edges": len(E), "acyclic": nx.is_directed_acyclic_graph(G),
                          "share_edges_earlier_to_later_id": round(sum(a_ < b for a_, b in E) / len(E), 4),
                          "kendall_tau_id_vs_depth": round(float(tau.statistic), 4), "p_value": round(float(tau.pvalue), 4)}
    res["P3_this_release"] = "order correlated with causal order (tau > 0.3)" if any(v["kendall_tau_id_vs_depth"] > 0.3 for v in res["sets"].values()) else "no (all |tau| < 0.3)"
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
