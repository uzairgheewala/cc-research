"""BEN-10 (BND-07): map each of the 8 Causal Chambers datasets to its ground-truth graph and source.

  PYTHONDONTWRITEBYTECODE=1 python analysis/chambers_map.py

Writes analysis/results/chambers/mapping.json and analysis/results/chambers/mapping_table.csv.

Sources per field (each is recorded in the output with the file it came from):
  chamber, configuration   the dataset README's "Dataset Description" table (external/causal_chambers_docs/<d>__README.md)
  ground-truth graph       causalchamber 0.2.8, causalchamber.ground_truth.main.graph(chamber, configuration)
                           (edges() / variables() in the same module); the README names the configuration
  dataset columns          the dataset's variables.csv (external/causal_chambers_docs/<d>__variables.csv)
  experiments, targets     the README experiment table (names split on <br>), plus the validation config tables
                           (lt_validation_configs.csv, wt_standard_validation_configs.csv) for validate_* experiments
  row counts               "stated": the N given in the README / config table; "observed": counted in the verified zip
                           (only when external/causal_chambers/<d>.zip exists with the sha256 of FETCH_REPORT.json);
                           "authors_notebook": sample sizes printed in the authors' causal_discovery_iid.ipynb output
Nothing is inferred about column semantics beyond what these files say.
"""
import csv, json, re, sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chambers_io as C  # noqa: E402

D = C.DOCS
GT = C.ground_truth()

# --- README parsing --------------------------------------------------------------------------------------------------


def readme(d):
    return (D / ("%s__README.md" % d)).read_text(encoding="utf-8")


def chamber_config(d):
    txt = readme(d)
    m = re.search(r"\|\s*(Light tunnel|Wind tunnel)\s*\|\s*([\w\-]+)\s*\|", txt)
    return {"Light tunnel": "lt", "Wind tunnel": "wt"}[m.group(1)], m.group(2), m.group(0)


def readme_experiments(d):
    """Experiment names (or name patterns with *) from the README's experiment table, first column, split on <br>."""
    txt = readme(d)
    sec = txt.split("## Dataset Description", 1)[1].split("## Changelog", 1)[0]
    names = []
    in_table = False
    for line in sec.splitlines():
        if re.match(r"\|\s*Experiment\s*\|", line):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                if names:
                    break
                continue
            if re.match(r"\|\s*:?-", line):
                continue
            cell = line.split("|")[1]
            for n in re.split(r"<br>", cell):
                n = n.replace("\\_", "_").strip()
                if n:
                    names.append(n)
    return names


def readme_md5(d):
    m = re.search(r"\((https://causalchamber[^)]*\.zip)\)\s*\|\s*([0-9a-f]{32})", readme(d))
    return {"url": m.group(1), "md5": m.group(2)} if m else None


# --- per-dataset experiment semantics (from the README text; quoted fragments kept short) ----------------------------

LT_NAME_FIX = {"osr_1": "osr_angle_1", "osr_2": "osr_angle_2"}   # README names O_1/O_2 experiments osr_1/osr_2;
# O_1, O_2 are latex_name('osr_angle_1'), latex_name('osr_angle_2') in causalchamber.ground_truth.main


def lt_interventions(names):
    out = []
    for n in names:
        if n == "uniform_reference":
            out.append(dict(experiment=n, kind="observational (reference)", targets=[], rows_stated=10000,
                            note="all actuators sampled independently and uniformly; sensor parameters fixed"))
            continue
        core = n[len("uniform_"):]
        strength = core.rsplit("_", 1)[1]
        t = core.rsplit("_", 1)[0]
        t = LT_NAME_FIX.get(t, t)
        note = "single-target shift of the target's distribution relative to uniform_reference (%s)" % strength
        if t.startswith(("t_ir", "t_vis", "osr")):
            note += ("; README sentence for this row lists several symbols (e.g. 'We set O_1, O_2, O_C = 2'); "
                     "the experiment name names one target, taken as the target here; unverified against the files")
        out.append(dict(experiment=n, kind="interventional (single target)", targets=[t], rows_stated=1000, note=note))
    return out


def validation(d):
    if d == "lt_validate_v1":
        cfg = pd.read_csv(D / "lt_validate_v1_lt_validation_configs.csv")
        rows = [(r.target, None, r) for r in cfg.itertuples()]
        src = "lt_validate_v1_lt_validation_configs.csv"
    else:
        cfg = pd.read_csv(D / "wt_validate_v1_wt_standard_validation_configs.csv")
        rows = [(r._1, (r.to if isinstance(r.to, str) else None), r) for r in cfg.itertuples()]
        src = "wt_validate_v1_wt_standard_validation_configs.csv"
    out = []
    for target, to, r in rows:
        name = "validate_%s_%s" % (target, to) if to else "validate_%s" % target
        out.append(dict(experiment=name, kind="interventional (two-level randomized, single target)", targets=[target],
                        rows_stated=int(r.N), xA=float(r.xA), xB=float(r.xB), T_ms=int(r.T), effect_named=to,
                        note="flag=0 rows: target at xA, flag=1 rows: target at xB, chosen at random per measurement "
                             "(generators/binary_interventions.py); all other manipulable variables fixed (%s)" % src))
    return out


def lt_malus(names):
    return [dict(experiment=n, kind="interventional (two targets randomized, others fixed)", targets=["pol_1", "pol_2"],
                 rows_stated=1000, note="pol_1, pol_2 ~ Unif{-90,...,90}; light-source colour fixed as named")
            for n in names]


def wt_intake(names):
    return [dict(experiment=n, kind="interventional time series (impulse on load_in)", targets=["load_in", "hatch"],
                 rows_stated=None, note="50 measurements per impulse; load_in 0.01 -> 1 -> 0.01; hatch random per impulse; "
                 "README: 'We collect a total of 5000 impulses' (per experiment or in total is not stated "
                 "unambiguously); load_out and osr_downwind fixed as named")
            for n in names]


def wt_bernoulli(names):
    spec = {"fans_off": (["load_in", "load_out"], 5000, "both loads set to 0"),
            "random_loads_both": (["load_in", "load_out"], 200000, "L_in = L_out ~ Unif([0,1]), 2000 settings x 100 measurements"),
            "random_loads_intake": (["load_in"], 200000, "as random_loads_both with L_out fixed at 0.1 ('Same as the previous')")}
    return [dict(experiment=n, kind="interventional (loads set or randomized)", targets=spec[n][0], rows_stated=spec[n][1],
                 note=spec[n][2]) for n in names]


def wt_changepoints(names):
    return [dict(experiment=n, kind="interventional time series (load_in changed at random intervals)", targets=["load_in"],
                 rows_stated=None, note="10 random seeds; row count not stated in the README") for n in names]


def wt_walks(names):
    import ast
    tree = ast.parse((D / "wt_walks_v1_regimes_targets.py").read_text(encoding="utf-8"))
    lists = {t.targets[0].id: ast.literal_eval(t.value) for t in tree.body if isinstance(t, ast.Assign)}
    out = []
    for n in names:
        if n.startswith("actuators_random_walk"):
            out.append(dict(experiment=n, kind="time series, actuators on random walks (no reference regime)",
                            targets=["load_in", "load_out", "hatch", "pot_1", "pot_2"], rows_stated=10000,
                            note="10 seeds; sensor parameters fixed"))
        elif n.startswith("loads_hatch_mix"):
            out.append(dict(experiment=n, kind="time series, loads sinusoid / hatch square wave", targets=["load_in", "load_out", "hatch"],
                            rows_stated=10000, note="'a total of 5 runs'"))
        else:
            key = "targets_single" if n.endswith("single") else "targets_multi"
            regs = lists.get(key, [])
            tg = sorted({t for r in regs for t in r})
            out.append(dict(experiment=n, kind="time series, regime 0 reference + interventional regimes", targets=tg,
                            rows_stated=320000, n_regimes=len(regs), regimes_without_intervention=sum(1 for r in regs if not r),
                            regime_targets=regs, note="regimes identified by the flag column; load_in, load_out, pot_1, pot_2 "
                            "on random walks throughout; targets from regimes_targets.py (%s)" % key))
    return out


SEMANTICS = {"lt_interventions_standard_v1": lt_interventions, "lt_malus_v1": lt_malus,
             "wt_intake_impulse_v1": wt_intake, "wt_bernoulli_v1": wt_bernoulli, "wt_changepoints_v1": wt_changepoints,
             "wt_walks_v1": wt_walks}


def authors_sizes():
    nb = json.load(open(D / "paper__case_studies_causal_discovery_iid.ipynb", encoding="utf-8"))
    for c in nb["cells"]:
        for o in c.get("outputs", []):
            t = "".join(o.get("text", ""))
            if t.startswith("Sample sizes:"):
                return {ln.split()[1]: int(ln.split()[0]) for ln in t.splitlines()[1:] if ln.strip()}
    return {}


def authors_validation_experiments():
    """Experiment lists printed by dataset.available_experiments() in the authors' causal_validation.ipynb."""
    nb = json.load(open(D / "paper__causal_validation.ipynb", encoding="utf-8"))
    found = {}
    for c in nb["cells"]:
        src = "".join(c["source"])
        m = re.search(r'Dataset\(name="(\w+)"', src)
        if not m:
            continue
        for o in c.get("outputs", []):
            t = "".join(o.get("data", {}).get("text/plain", ""))
            if t.startswith("["):
                found[m.group(1)] = sorted(re.findall(r"'([^']+)'", t))
    return found


def main():
    C.OUT.mkdir(parents=True, exist_ok=True)
    nb_sizes = authors_sizes()
    nb_val = authors_validation_experiments()
    out = {"ticket": "BEN-10", "bundle": "BND-07", "package": "causalchamber 0.2.8 (external/causalchamber_pkg)",
           "graph_function": "causalchamber.ground_truth.main.graph(chamber, configuration)", "datasets": []}
    table = []
    for d in C.DATASETS:
        ch, cfgname, cfg_line = chamber_config(d)
        nodes = GT.variables(ch, cfgname)
        edges = GT.edges(ch, cfgname)
        cols = list(pd.read_csv(D / ("%s__variables.csv" % d)).column_name)
        names = readme_experiments(d)
        exps = validation(d) if d.endswith("validate_v1") else SEMANTICS[d](names)
        if d.endswith("validate_v1"):
            readme_names = set(names)
            for e in exps:
                e["listed_in_readme"] = e["experiment"] in readme_names
        if d in nb_val:
            mine = sorted(e["experiment"] for e in exps)
            check = {"authors_notebook_experiments": len(nb_val[d]), "same_names_as_config_table": mine == nb_val[d],
                     "source": "paper__causal_validation.ipynb output of dataset.available_experiments()"}
        else:
            check = None
        status = C.data_status(d)
        if status in C.READABLE:
            found = C.experiments(d)
            for e in exps:
                if e["experiment"] in found:
                    e["rows_observed"] = int(len(C.load_experiment(d, e["experiment"])))
            out_names = sorted(set(found) - {e["experiment"] for e in exps})
        else:
            out_names = None
        for e in exps:
            if e["experiment"] in nb_sizes and d == "lt_interventions_standard_v1":
                e["rows_authors_notebook"] = nb_sizes[e["experiment"]]
            bad = [t for t in e["targets"] if t not in nodes]
            if bad:
                e["targets_not_in_graph"] = bad
        n_obs = sum(1 for e in exps if e["kind"].startswith("observational"))
        rec = {
            "dataset": d, "chamber": ch, "configuration": cfgname,
            "configuration_source": "%s__README.md, 'Dataset Description' table: %s" % (d, cfg_line.strip()),
            "graph": "causalchamber.ground_truth.main.graph('%s', '%s')" % (ch, cfgname),
            "graph_variables": len(nodes), "graph_edges": len(edges),
            "graph_longest_path": C.longest_path(edges, nodes),
            "graph_parents": sorted({a for a, _ in edges}), "graph_children": sorted({b for _, b in edges}),
            "dataset_columns": len(cols),
            "columns_in_graph": [c for c in cols if c in nodes],
            "columns_not_in_graph": [c for c in cols if c not in nodes],
            "graph_variables_missing_from_columns": [v for v in nodes if v not in cols],
            "columns_source": "%s__variables.csv" % d,
            "zip": {"url": "https://causalchamber.s3.eu-central-1.amazonaws.com/downloadables/%s.zip" % d,
                    "sha256_expected": C.expected_sha(d), "status": status, "readme_md5": readme_md5(d)},
            "experiments_source": "%s__README.md experiment table" % d,
            "experiments": exps, "n_experiments_listed": len(exps),
            "n_observational_experiments": n_obs, "n_interventional_experiments": len(exps) - n_obs,
            "experiments_in_zip_not_listed": out_names,
            "experiment_names_vs_authors_notebook": check,
            "rows_stated_total": (sum(e["rows_stated"] for e in exps) if all(e.get("rows_stated") for e in exps)
                                  and "*" not in "".join(e["experiment"] for e in exps) else None),
        }
        out["datasets"].append(rec)
        table.append({"dataset": d, "chamber": ch, "configuration": cfgname, "graph": rec["graph"],
                      "graph_variables": len(nodes), "graph_edges": len(edges),
                      "columns_in_graph": len(rec["columns_in_graph"]),
                      "columns_not_in_graph": " ".join(rec["columns_not_in_graph"]),
                      "experiments": len(exps), "observational": n_obs, "interventional": len(exps) - n_obs,
                      "targets": " ".join(sorted({t for e in exps for t in e["targets"]})),
                      "rows_stated_total": rec["rows_stated_total"], "zip_status": status})
    out["note"] = ("All 8 READMEs name the 'standard' configuration, so every dataset maps to the standard graph of its "
                   "chamber. Rows marked rows_stated come from README/config text; rows_observed exist only for verified zips.")
    json.dump(out, open(C.OUT / "mapping.json", "w", encoding="utf-8"), indent=1)
    with open(C.OUT / "mapping_table.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]))
        w.writeheader()
        w.writerows(table)
    for r in table:
        print(r)


if __name__ == "__main__":
    main()
