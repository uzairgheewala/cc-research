"""AB-04 must-show figures from the stored results (no recomputation):
  1. risk-coverage: precision of the claims with the highest replicate agreement vs coverage, per method, per family
  2. F1 vs decision value: controlled directed F1 (shuffled, expectation rule; rescore_v2) against DV-1 lift over the
     empty graph on the same files (decision_value_v2), released arm

  python analysis/ab04_figures.py --dv analysis/results/decision_value_v2/decision_value_v2.json \
      --rescore analysis/results/rescore_v2/rescore_v2.json --out analysis/results/decision_value_v2
Tickets: AUD-36
"""
import argparse, json, os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ALIAS = {"PC, Causal-Copilot copy": "PC (Causal-Copilot copy)", "PC, upstream (default rule)": "PC (upstream, default rule)",
         "PC, upstream maxP": "PC (upstream, maxP)", "PC, upstream definite maxP": "PC (upstream, definite maxP)",
         "GES (BIC)": "GES (BIC)", "GIES with targets (D+I)": "GIES with targets (D+I)", "FCI (PAG; undecided as undirected)": "FCI",
         "DirectLiNGAM": "DirectLiNGAM", "NOTEARS": "NOTEARS"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dv", required=True)
    ap.add_argument("--rescore", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    dv = json.load(open(a.dv))["families"]
    rs = json.load(open(a.rescore))["methods"]
    fams = [f for f in ("semantic", "formula", "synthetic") if f in dv]
    fig, axes = plt.subplots(1, len(fams), figsize=(5.2 * len(fams), 4.4), sharey=True)
    cmap = plt.get_cmap("tab10")
    colour = {lab: cmap(i % 10) for i, lab in enumerate(ALIAS)}
    for ax, fam in zip(axes, fams):
        for lab, arms in dv[fam].items():
            rc = arms.get("released", {}).get("risk_coverage_replicate_agreement")
            if not rc:
                continue
            xs = [float(k) for k in rc if k.replace(".", "").isdigit()]
            ax.plot(xs, [rc[str(x)] for x in xs], marker="o", ms=3, label=lab, color=colour.get(lab, "k"))
        e = dv[fam].get("baseline: empty graph (nothing moves)", {}).get("reference", {}).get("precision_committed")
        if e:
            ax.axhline(e, color="k", ls="--", lw=1, label="empty graph (all files)")
        ax.set_title(fam)
        ax.set_xlabel("coverage (most-agreed claims first)")
        ax.grid(alpha=.3)
    axes[0].set_ylabel("precision of committed claims")
    handles = {}
    for ax in axes:
        for h, l in zip(*ax.get_legend_handles_labels()):
            handles.setdefault(l, h)
    fig.legend(list(handles.values()), list(handles.keys()), fontsize=7, loc="lower center", ncol=5)
    fig.suptitle("Risk-coverage by replicate agreement (released columns)")
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    fig.savefig(os.path.join(a.out, "risk_coverage.png"), dpi=130)

    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    marks = {"semantic": "o", "formula": "s", "synthetic": "^"}
    pts = []
    for fam in fams:
        for lab, arms in dv[fam].items():
            r = arms.get("released")
            if not r or ALIAS.get(lab) not in rs or fam not in rs[ALIAS[lab]]:
                continue
            f1 = rs[ALIAS[lab]][fam]["shuffled"]["F1_random"]
            ax.scatter(f1, r["lift_over_empty_graph"], marker=marks[fam], s=40, color=colour.get(lab, "k"))
            ax.annotate(lab.split(" (")[0].replace("PC, ", "PC ")[:18], (f1, r["lift_over_empty_graph"]), fontsize=6, xytext=(3, 2), textcoords="offset points")
            pts.append((fam, lab, f1, r["lift_over_empty_graph"]))
    ax.axhline(0, color="k", lw=1)
    ax.axhline(0.05, color="k", ls=":", lw=1)
    ax.set_xlabel("directed F1, controlled (shuffled columns, expectation rule)")
    ax.set_ylabel("DV-1 precision lift over 'nothing moves' (same files)")
    ax.set_title("F1 vs decision value (o semantic, s formula, ^ synthetic)")
    ax.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(os.path.join(a.out, "f1_vs_dv.png"), dpi=130)
    json.dump({"points": pts}, open(os.path.join(a.out, "f1_vs_dv_points.json"), "w"), indent=1)
    print("wrote figures to", a.out)


if __name__ == "__main__":
    main()
