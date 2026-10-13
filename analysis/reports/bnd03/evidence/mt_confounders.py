# Offline micro-test (no LLM, no network): runs Analysis._identify_confounders and
# convert_adj_mat verbatim from causal_inference/ on a hand-built revised graph.
import ast, sys, types, numpy as np, pandas as pd, networkx as nx
root = sys.argv[1]
def grab(path, name, cls=None):
    src = open(f"{root}/{path}").read(); tree = ast.parse(src)
    body = tree.body
    if cls:
        body = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls][0].body
    for n in body:
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return ast.get_source_segment(src, n)
ns = {"np": np, "nx": nx}
exec(grab("causal_inference/help_functions.py", "convert_adj_mat"), ns)
import textwrap
exec(textwrap.dedent(grab("causal_inference/inference.py", "_identify_confounders", cls="Analysis")), ns)
cols = ["T", "Y", "Z", "W"]
M = np.zeros((4, 4), dtype=int)       # repo convention: M[i,j]!=0 marks an edge between j and i, M[i,j]==1 means j->i
M[1, 0] = 1                            # T -> Y
M[0, 2] = 3                            # Z <-> T  (bidirected = latent common cause, stored in one cell)
M[1, 2] = 3                            # Z <-> Y
M[0, 3] = 1; M[1, 3] = 1               # W -> T, W -> Y (a real observed confounder)
self = types.SimpleNamespace()
self.data = pd.DataFrame(np.zeros((2, 4)), columns=cols)
self.global_state = types.SimpleNamespace(results=types.SimpleNamespace(revised_graph=M))
G = ns["convert_adj_mat"](M); self.graph = G
self.G = nx.relabel_nodes(nx.from_numpy_array(G, create_using=nx.DiGraph), dict(enumerate(cols)))
conf, pot = ns["_identify_confounders"](self, "T", "Y")
print("confounders:", conf, "potential:", pot)
print("inference DiGraph edges:", sorted(self.G.edges))
