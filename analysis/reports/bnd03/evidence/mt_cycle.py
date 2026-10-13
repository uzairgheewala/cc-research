import ast, sys, numpy as np, networkx as nx, pandas as pd
root = sys.argv[1]
def grab(path, name):
    src = open(f"{root}/{path}").read()
    tree = ast.parse(src)
    for n in tree.body:
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return ast.get_source_segment(src, n)
class L:
    def __getattr__(self, k): return lambda *a, **kw: None
calls = []
def LLM_remove_cycles(args, prompt):
    calls.append(prompt); raise RuntimeError("LLM would be called: " + prompt)
ns = {"np": np, "nx": nx, "logger": L(), "LLM_remove_cycles": LLM_remove_cycles}
exec(grab("causal_inference/help_functions.py", "convert_adj_mat"), ns)
exec(grab("postprocess/judge_functions.py", "check_cycle"), ns)
cols = pd.Index(["A","B","C"])
data = pd.DataFrame(np.zeros((3,3)), columns=cols)
# Case 1: revised graph with one undirected edge A--B stored as code 2 in one cell (repo convention), plus directed C->B (M[B,C]=1)
M = np.zeros((3,3)); M[0,1] = 2; M[1,2] = 1
G = ns["convert_adj_mat"](M)
print("case1 convert_adj_mat output (G[i,j]=1 means i->j):\n", G)
Gd = nx.from_numpy_array(G, create_using=nx.DiGraph)
print("case1 DiGraph edges:", list(Gd.edges))
# Case 2: undirected stored symmetrically as 1/1 (e.g. after LLM or wrapper storing both cells)
M2 = np.zeros((3,3)); M2[0,1] = 1; M2[1,0] = 1
G2 = ns["convert_adj_mat"](M2)
D2 = nx.from_numpy_array(G2, create_using=nx.DiGraph)
mat = nx.to_numpy_array(D2)
try:
    res = ns["check_cycle"](None, data, mat.copy())
    print("case2 check_cycle returned:\n", res)
    print("case2 is DAG after check_cycle:", nx.is_directed_acyclic_graph(nx.from_numpy_array(res, create_using=nx.DiGraph)))
except Exception as e:
    print("case2 exception:", type(e).__name__, e)
print("LLM calls attempted:", len(calls))
