"""BEN-10 (BND-07): the "one layer deep" check of the Causal Chambers ground-truth graphs.

  PYTHONDONTWRITEBYTECODE=1 python analysis/chambers_validate.py

What "one layer deep" means operationally here
  The standard graphs (causalchamber.ground_truth.main.edges('lt'|'wt', 'standard')) have longest directed path 1: every
  edge runs from a manipulable input (actuator or sensor parameter) to a measured output, and no output has children.
  So for every intervened variable X, children(X) = descendants(X). The authors' validation (appendix V; code in
  causal_validation.ipynb) randomizes ONE input X between two values xA / xB (column flag = 0 / 1, chosen at random per
  measurement, generators/binary_interventions.py), holds every other input fixed, and runs a two-sample
  Kolmogorov-Smirnov test of each response between the flag = 0 and flag = 1 rows. A graph edge X -> Y is supported
  when Y shifts. "One layer deep" = the check covers exactly the direct input -> output edges; there is no deeper layer.

Our check (part A, needs the verified zips lt_validate_v1.zip / wt_validate_v1.zip)
  For each validate_* experiment with target X and every graph variable Z != X: scipy.stats.ks_2samp(Z | flag=0,
  Z | flag=1). Holm correction over all tests of one dataset, family-wise level 1%. Each (X, Z) is classed as child,
  descendant-not-child (empty here, by the depth-1 structure) or non-descendant. Reported: children that shift, children
  that do not, non-descendants that shift (a shift of a non-descendant contradicts the graph or reveals an effect the
  graph omits). Edge -> experiment assignment follows the authors' notebook: wt edges with a dedicated experiment
  validate_<X>_<Y> (or validate_hatch_{pressures,rpms,mic}) are judged on that experiment.
  The reference rows are the flag = 0 arm of the same experiment: these datasets contain no observational experiment.

Authors' published p-values (part B, runs without the data)
  The p-values the authors printed for the appendix V tables (edges only) are parsed from the notebook output (LaTeX
  lines "$A\\to B$ & $p$"), mapped back to column names with causalchamber.ground_truth.main.latex_name (per chamber),
  and Holm-corrected over the printed edges at 1%. Non-edge p-values were shown only as a heatmap image, so the
  non-descendant part cannot be read from the published material.

Writes analysis/results/chambers/one_layer_deep.json.
"""
import json, re, sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chambers_io as C  # noqa: E402

GT = C.ground_truth()
ALPHA = 0.01
DEDICATED_WT = {("hatch", "pressure_upwind"): "validate_hatch_pressures", ("hatch", "pressure_downwind"): "validate_hatch_pressures",
                ("hatch", "pressure_intake"): "validate_hatch_pressures", ("hatch", "rpm_in"): "validate_hatch_rpms",
                ("hatch", "rpm_out"): "validate_hatch_rpms", ("hatch", "mic"): "validate_hatch_mic",
                ("load_in", "mic"): "validate_load_in_mic", ("load_in", "current_out"): "validate_load_in_current_out",
                ("load_out", "mic"): "validate_load_out_mic", ("load_out", "current_in"): "validate_load_out_current_in",
                ("load_out", "pressure_intake"): "validate_load_out_pressure_intake"}


def holm(pvals, alpha=ALPHA):
    p = np.asarray(pvals, dtype=float)
    order = np.argsort(p, kind="mergesort")
    m = len(p)
    rej = np.zeros(m, dtype=bool)
    for k, i in enumerate(order):
        if p[i] <= alpha / (m - k):
            rej[i] = True
        else:
            break
    return rej


def structure(ch):
    nodes = GT.variables(ch, "standard")
    edges = GT.edges(ch, "standard")
    parents = sorted({a for a, _ in edges})
    return {"variables": len(nodes), "edges": len(edges), "longest_path": C.longest_path(edges, nodes),
            "sources_of_edges": len(parents),
            "children_equal_descendants_for_every_source": all(
                C.descendants(edges, x) == {b for a, b in edges if a == x} for x in parents),
            "outputs_with_children": sorted({a for a, _ in edges} & {b for _, b in edges})}


# --- part B: authors' printed p-values ---------------------------------------------------------------------------------

def parse_float(s):
    s = s.strip()
    m = re.match(r"([\d.]+)\s*\\times\s*10\^\{(-?\d+)\}", s)
    return float(m.group(1)) * 10 ** int(m.group(2)) if m else float(s)


def authors_pvalues():
    nb = json.load(open(C.DOCS / "paper__causal_validation.ipynb", encoding="utf-8"))
    out = {}
    current = None
    for c in nb["cells"]:
        src = "".join(c["source"])
        m = re.search(r"edges_to_validate = .*?chamber='(\w+)', configuration='([\w-]+)'", src)
        if m:
            current = (m.group(1), m.group(2))
        if "print latex" in src.lower() or ("latex_float(p)" in src and current):
            for o in c.get("outputs", []):
                t = "".join(o.get("text", ""))
                pairs = re.findall(r"\$([^$]+?)\\to([^$]+?)\$ & \$([^$]+?)\\quad\$", t)
                if pairs and current:
                    out.setdefault(current, []).extend(pairs)
    return out


def inverse_latex(ch, cfg):
    inv = {}
    for v in GT.variables(ch, cfg):
        inv[GT.latex_name(v, enclose=False)] = v
    return inv


def part_b():
    res = {}
    raw = authors_pvalues()
    for (ch, cfg), pairs in raw.items():
        if cfg != "standard":
            continue
        inv = inverse_latex(ch, cfg)
        rows = [{"from": inv[a], "to": inv[b], "p": parse_float(p)} for a, b, p in pairs]
        truth = set(GT.edges(ch, cfg))
        rej = holm([r["p"] for r in rows])
        for r, x in zip(rows, rej):
            r["shift_holm_1pct"] = bool(x)
        printed = {(r["from"], r["to"]) for r in rows}
        res["%s_%s" % (ch, cfg)] = {
            "source": "external/causal_chambers_docs/paper__causal_validation.ipynb (printed LaTeX table rows)",
            "edges_printed": len(rows), "edges_in_graph": len(truth),
            "printed_equal_graph_edges": printed == truth,
            "children_shift": int(sum(rej)), "children_no_shift": [(r["from"], r["to"], r["p"]) for r in rows if not r["shift_holm_1pct"]],
            "max_p": max(r["p"] for r in rows), "rows": rows,
            "non_descendants_shift": "not available: non-edge p-values appear only in a heatmap image in the notebook",
        }
    return res


# --- part A: our KS check on the data ---------------------------------------------------------------------------------

def part_a(d):
    from scipy.stats import ks_2samp
    ch = C.chamber_of(d)
    nodes = GT.variables(ch, "standard")
    edges = GT.edges(ch, "standard")
    if not C.readable(d):
        return {"status": "not run: %s.zip is %s in external/causal_chambers (download blocked; see fetch_status.json)"
                % (d, C.data_status(d))}
    exps = C.experiments(d)
    tests = []
    for e in sorted(exps):
        df = C.load_experiment(d, e)
        target = None
        for v in sorted(nodes, key=len, reverse=True):
            if e == "validate_" + v or e.startswith("validate_" + v + "_"):
                target = v
                break
        a, b = df[df.flag == 0], df[df.flag == 1]
        desc = C.descendants(edges, target)
        children = {y for x, y in edges if x == target}
        for z in nodes:
            if z == target:
                continue
            p = float(ks_2samp(a[z], b[z]).pvalue)
            cls = "child" if z in children else ("descendant" if z in desc else "non-descendant")
            tests.append({"experiment": e, "target": target, "variable": z, "class": cls, "p": p,
                          "n0": int(len(a)), "n1": int(len(b))})
    rej = holm([t["p"] for t in tests])
    for t, x in zip(tests, rej):
        t["shift"] = bool(x)
    by = {(t["experiment"], t["variable"]): t for t in tests}
    edge_rows = []
    for x, y in edges:
        exp = DEDICATED_WT.get((x, y), "validate_" + x) if ch == "wt" else "validate_" + x
        t = by.get((exp, y))
        edge_rows.append({"from": x, "to": y, "experiment": exp, "p": t["p"] if t else None, "shift": t["shift"] if t else None})
    nd = [t for t in tests if t["class"] == "non-descendant" and t["shift"]]
    return {"status": "run", "tests": len(tests), "holm_family": "all tests of this dataset", "alpha": ALPHA,
            "edges": len(edges), "children_shift": sum(1 for r in edge_rows if r["shift"]),
            "children_no_shift": [r for r in edge_rows if r["shift"] is False],
            "edges_without_experiment": [r for r in edge_rows if r["shift"] is None],
            "non_descendant_tests": sum(1 for t in tests if t["class"] == "non-descendant"),
            "non_descendants_shift": len(nd),
            "non_descendants_shift_list": [(t["experiment"], t["variable"], t["p"]) for t in nd],
            "edge_rows": edge_rows}


def main():
    C.OUT.mkdir(parents=True, exist_ok=True)
    out = {"ticket": "BEN-10", "bundle": "BND-07",
           "definition": ("One layer deep: the standard graphs have longest path 1, so each intervened input's children "
                          "are all its descendants; validation = randomize one input between two values with all other "
                          "inputs fixed, KS-test every response between the two arms; edges = input -> output only."),
           "test": "scipy.stats.ks_2samp, flag=0 arm vs flag=1 arm of the same validate_* experiment; Holm at 1%",
           "structure": {"lt_standard": structure("lt"), "wt_standard": structure("wt")},
           "part_a_our_check": {d: part_a(d) for d in ("lt_validate_v1", "wt_validate_v1")},
           "part_b_authors_printed_pvalues": part_b(),
           "limitations": [
               "Each validate_* experiment fixes all other inputs at one setting (validation config tables), so an edge "
               "is checked at one operating point; an effect that vanishes there would be missed, and a missing edge "
               "that only appears elsewhere is not tested.",
               "Only inputs can be randomized; output -> output effects (e.g. sensor-sensor) are not tested by design; "
               "the graphs contain none.",
               "The KS test on flag arms compares two random halves taken over the same time span; slow drift affects "
               "both arms alike, but a shift of a non-descendant can still come from an effect the graph omits.",
               "Part B covers edges only (children); the authors did not print non-edge p-values as numbers.",
           ]}
    json.dump(out, open(C.OUT / "one_layer_deep.json", "w", encoding="utf-8"), indent=1)
    print(json.dumps(out["structure"], indent=1))
    for k, v in out["part_a_our_check"].items():
        print(k, v.get("status"))
    for k, v in out["part_b_authors_printed_pvalues"].items():
        print(k, {x: v[x] for x in ("edges_printed", "edges_in_graph", "printed_equal_graph_edges", "children_shift",
                                    "children_no_shift", "max_p")})


if __name__ == "__main__":
    main()
