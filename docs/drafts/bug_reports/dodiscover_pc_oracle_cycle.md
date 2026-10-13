# DRAFT (not sent): PC returns a cyclic graph with a perfect (oracle) CI test

Repository: py-why/dodiscover. Version: git main 6e64456198a5b66e515f250a8f4b143ebc31c9a6 (pywhy-graphs 0.1.0, networkx 3.6.1).

**What happens.** With `dodiscover.ci.Oracle` on the DAG 0->1, 4->1, 1->2, 4->2 (plus an isolated node 3), `PC.learn_graph`
returns the directed edges 0->1, 4->1, 1->2, 2->4, which contain the cycle 4->1->2->4. The expected output is the true
CPDAG, fully directed: 0->1, 4->1 (v-structure), 1->2 (Meek R1), 4->2 (Meek R2).

**Reproduce.**
```python
import networkx as nx, numpy as np, pandas as pd
from dodiscover import PC, make_context
from dodiscover.ci import Oracle
if not hasattr(nx, "d_separated"): nx.d_separated = nx.is_d_separator   # networkx >= 3.5
names = ["v0", "v1", "v2", "v3", "v4"]
G = nx.DiGraph(); G.add_nodes_from(names)
G.add_edges_from([("v4", "v1"), ("v4", "v2"), ("v0", "v1"), ("v1", "v2")])
df = pd.DataFrame(np.zeros((5, 5)), columns=names)
m = PC(ci_estimator=Oracle(G)); m.learn_graph(df, make_context().variables(data=df).build())
print(sorted(m.graph_.directed_edges), sorted(m.graph_.undirected_edges))
```

**Scale.** On 120 random DAGs (6-12 nodes) x 6 column orders: 597 of 717 completed runs return the true CPDAG, 88 of 120
DAGs give the same output in every column order; 122 arrows reversed, 89 committed where the class is undirected.
3 of 720 runs raised `NetworkXError: The edge v3-v2 not in graph` once and not on a rerun.
Separately, `dodiscover.ci.Oracle` calls `nx.d_separated`, removed in networkx 3.5.
