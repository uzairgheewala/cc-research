"""AB-06 (AUD-38) name-reliance figure: mean directed F1 per system and name arm, with each hybrid's own data-only graph.

  python analysis/ab06_figure.py      -> analysis/results/ab06/name_reliance.png and .svg (reads analysis/results/ab06/ab06.json)
Colours: the dataviz reference palette's first three categorical slots (blue real, orange swapped, aqua neutral); the
data-only floor is a dark tick. Causal-Copilot rows use BND-08's metric (S3 directed F1 on the S2 test families) and are
labelled as such. No model calls.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / "analysis" / "results" / "ab06" / "ab06.json").read_text(encoding="utf-8"))
C = {"real": "#2a78d6", "swapped": "#eb6834", "neutral": "#1baf7a"}
rows = []
for key, label in (("causal_copilot_gpt4o", "Causal-Copilot, gpt-4o*"), ("causal_copilot_gpt4omini", "Causal-Copilot, gpt-4o-mini*")):
    c = R["causal_copilot"].get(key)
    if c:
        rows.append((label, {a: c[a]["f1_mean"] for a in ("real", "neutral", "swapped")}, None,
                     c["name_reliance_real_minus_swapped"]))
for ag, label in (("causaliq", "causaliq-knowledge"), ("pywhyllm", "PyWhy-LLM"), ("matmcd", "MATMCD"), ("vashishtha", "Vashishtha et al.")):
    A = R["agents"][ag]
    floor = (A.get("data_only_floor_real_arm") or {}).get("f1_data_only")
    rows.append((label, {a: A[a]["f1_mean"] for a in ("real", "neutral", "swapped")}, floor, A["name_reliance_real_minus_swapped"]))

fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=150)
fig.patch.set_facecolor("#fcfcfb")
ax.set_facecolor("#fcfcfb")
ys = list(range(len(rows)))[::-1]
for y, (label, v, floor, nr) in zip(ys, rows):
    if v.get("real") is not None and v.get("swapped") is not None:
        ax.plot([v["swapped"], v["real"]], [y, y], color="#c3c2b7", lw=2, zorder=1, solid_capstyle="round")
    for arm in ("swapped", "real"):
        if v.get(arm) is not None:
            ax.scatter(v[arm], y, s=64, color=C[arm], edgecolor="#fcfcfb", linewidth=2, zorder=3)
    if v.get("neutral") is not None:          # a ring drawn on top, so it stays visible where it sits on a filled dot
        ax.scatter(v["neutral"], y, s=120, facecolor="none", edgecolor=C["neutral"], linewidth=2, zorder=4)
    if floor is not None:
        ax.plot([floor, floor], [y - 0.28, y + 0.28], color="#0b0b0b", lw=2, zorder=2)
    gap = "" if nr["mean"] is None else "  real − swapped %+.3f (n=%d)" % (nr["mean"], nr["paired_scenarios"])
    ax.text(0.585, y, gap, va="center", ha="left", fontsize=8.5, color="#52514e")
ax.set_yticks(ys)
ax.set_yticklabels([r[0] for r in rows], fontsize=9.5, color="#0b0b0b")
ax.set_xlim(0, 0.585)
ax.set_xlabel("Mean directed F1 (columns shuffled)", fontsize=9.5, color="#52514e")
ax.grid(axis="x", color="#e6e5e0", lw=0.8)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#c3c2b7")
ax.tick_params(colors="#52514e", length=0)
from matplotlib.lines import Line2D
handles = [Line2D([], [], marker="o", ls="", color=C["real"], markersize=7, label="real names"),
           Line2D([], [], marker="o", ls="", markerfacecolor="none", markeredgecolor=C["neutral"], markeredgewidth=2,
                  markersize=8, label="neutral names"),
           Line2D([], [], marker="o", ls="", color=C["swapped"], markersize=7, label="swapped names")]
handles.append(Line2D([], [], color="#0b0b0b", lw=2, label="agent's own data-only graph"))
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.42, 1.14), ncol=4, frameon=False, fontsize=8.5)
fig.text(0.01, 0.01, "* BND-08 metric: S3 directed F1 on the 10 S2 test families. Agents: 10 semantic dev scenarios (PyWhy-LLM and "
                     "Vashishtha: first five, real and swapped only).", fontsize=7, color="#52514e")
fig.tight_layout(rect=(0, 0.03, 0.82, 1))
out = ROOT / "analysis" / "results" / "ab06"
fig.savefig(out / "name_reliance.png", facecolor=fig.get_facecolor())
fig.savefig(out / "name_reliance.svg", facecolor=fig.get_facecolor())
print("wrote", out / "name_reliance.png")
