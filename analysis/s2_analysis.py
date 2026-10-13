"""BND-08 verdicts M2-M4 for the S2 live runs. Thresholds are fixed here, in code, before the live plan runs (2026-10-10).

  python analysis/stability.py --runs-dir runs --label s2 --mapping datasets/suite_q1s2/MAPPING.json --out analysis/results/stability_s2
  python analysis/partial_stages.py ... --label s2 --out analysis/results/stability_s2
  python analysis/s2_analysis.py --stability analysis/results/stability_s2/stability.json \
      --partial analysis/results/stability_s2/partial_stages.json --out analysis/results/stability_s2/s2_verdicts.json

  M2  Names carry the agent's score: per S2 family, S3 directed-edge F1 (all runs that reached S3) with real names exceeds the
      neutral arm by at least 0.10.            SUPPORTED if in >= 8 of 10 families; REFUTED if in <= 5 of 10.
  M3  In swapped arms, LLM-set S3 edges follow the labels: of distinct (family, edge) adjacent in exactly one reading of the
      reference, the share adjacent by label (stability.py's N1 count).
                                               SUPPORTED if share >= 0.80 with n >= 30 AND the data-only count is not above the
                                               95th percentile of Binomial(n, 0.5) (edges picked without regard to labels or data
                                               fall on either reading with probability 1/2, since both readings have the same
                                               number of edges and only pairs in exactly one reading are counted);
                                               REFUTED if share <= 0.50 (n >= 30); otherwise INCONCLUSIVE.
  M4  Without names the agent is below its own toolbox: neutral-arm S3 directed-edge F1 below plain PC on the same file
      (analysis/results/s2_baselines/s2_baselines.json, method pc, rule "drop": committed arrows only, the same metric).
                                               SUPPORTED if in >= 8 of 10 families; REFUTED if in <= 5 of 10.
  A family enters M2 and M4 only if both arms have at least one run that reached S3; with fewer than 10 such families the
  verdict is computed on the counts that exist and can only be SUPPORTED or REFUTED if the threshold is already decided.
  M2 sensitivity (added 2026-10-11, before the live run; reported next to M2, never replaces it): CausalArena's released
  names are numbered in causal order in s2_02 (34 of 38 true edges low -> high; analysis/results/name_prefix/name_prefix.json),
  an order hint the other families' names lack. M2 is recomputed without every family whose real names are numbered, with
  the same 0.10 gap and the same proportions: SUPPORTED if hits >= ceil(0.8 n), REFUTED if hits <= floor(0.5 n), n = 10
  minus the excluded families (for n = 10 this is the 8 / 5 rule above).
"""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M2_GAP, M2_SUP, M2_REF = 0.10, 8, 5
M3_SUP, M3_REF, M3_MIN_N = 0.80, 0.50, 30
M4_SUP, M4_REF = 8, 5
N_FAMILIES = 10


def binom_q95(n, p=0.5):
    acc = 0.0
    for k in range(n + 1):
        acc += math.comb(n, k) * p ** k * (1 - p) ** (n - k)
        if acc >= 0.95:
            return k
    return n


def count_verdict(hits, total, sup, ref):
    missing = N_FAMILIES - total
    if hits >= sup:
        return "SUPPORTED"
    if hits + missing <= ref:
        return "REFUTED"
    return "INCONCLUSIVE" if missing else ("REFUTED" if hits <= ref else "INCONCLUSIVE")


def numbered_families(path):
    p = Path(path)
    if not p.exists():
        raise SystemExit("missing %s: run analysis/name_prefix_check.py first" % p)
    return sorted({r["family"] for r in json.loads(p.read_text(encoding="utf-8"))["s2"] if r["numbered"]})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stability", required=True)
    ap.add_argument("--partial", required=True)
    ap.add_argument("--baselines", default=str(ROOT / "analysis" / "results" / "s2_baselines" / "s2_baselines.json"))
    ap.add_argument("--name-prefix", default=str(ROOT / "analysis" / "results" / "name_prefix" / "name_prefix.json"))
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    stab = json.loads(Path(a.stability).read_text(encoding="utf-8"))
    part = json.loads(Path(a.partial).read_text(encoding="utf-8"))
    base = json.loads(Path(a.baselines).read_text(encoding="utf-8"))
    pc = {r["family"]: r["dir_f1"]["drop"] for r in base["rows"] if r["method"] == "pc"}
    s3 = {}
    for r in part["by_arm"]:
        if r.get("with_S3"):
            s3[(r["family"], r["role"])] = r["S3_dir_all"]
    fams = sorted({f for f, _ in s3})
    m2 = {f: round(s3[(f, "real")] - s3[(f, "neutral")], 4) for f in fams if (f, "real") in s3 and (f, "neutral") in s3}
    m4 = {f: {"neutral_S3_dir": s3[(f, "neutral")], "pc_dir_drop": pc[f], "below": s3[(f, "neutral")] < pc[f]}
          for f in fams if (f, "neutral") in s3 and f in pc}
    n1 = stab["predictions"].get("N1", {})
    lo, do = n1.get("labels_only", 0), n1.get("data_only", 0)
    n = lo + do
    share = lo / n if n else None
    q95 = binom_q95(n) if n else None
    if n >= M3_MIN_N and share >= M3_SUP and do <= q95:
        m3v = "SUPPORTED"
    elif n >= M3_MIN_N and share <= M3_REF:
        m3v = "REFUTED"
    else:
        m3v = "INCONCLUSIVE"
    out = {"thresholds": {"M2": [M2_GAP, M2_SUP, M2_REF], "M3": [M3_SUP, M3_REF, M3_MIN_N], "M4": [M4_SUP, M4_REF]},
           "M2": {"per_family_real_minus_neutral": m2, "hits": sum(v >= M2_GAP for v in m2.values()), "families": len(m2),
                  "verdict": count_verdict(sum(v >= M2_GAP for v in m2.values()), len(m2), M2_SUP, M2_REF)},
           "M3": {"labels_only": lo, "data_only": do, "neither": n1.get("neither"), "n": n, "share": share,
                  "binomial_q95_data_only": q95, "verdict": m3v},
           "M4": {"per_family": m4, "hits": sum(v["below"] for v in m4.values()), "families": len(m4),
                  "verdict": count_verdict(sum(v["below"] for v in m4.values()), len(m4), M4_SUP, M4_REF)}}
    excl = numbered_families(a.name_prefix)
    n_s = N_FAMILIES - len(excl)
    m2s = {f: v for f, v in m2.items() if f not in excl}
    hits_s = sum(v >= M2_GAP for v in m2s.values())
    sup_s, ref_s = math.ceil(0.8 * n_s), math.floor(0.5 * n_s)
    missing_s = n_s - len(m2s)
    v_s = ("SUPPORTED" if hits_s >= sup_s else "REFUTED" if hits_s + missing_s <= ref_s
           else "INCONCLUSIVE" if missing_s else ("REFUTED" if hits_s <= ref_s else "INCONCLUSIVE"))
    out["M2_sensitivity_unnumbered_names"] = {"excluded_families": excl, "families_possible": n_s, "families": len(m2s),
                                              "hits": hits_s, "thresholds": [M2_GAP, sup_s, ref_s], "verdict": v_s,
                                              "role": "sensitivity; the M2 verdict above is the pre-registered one"}
    Path(a.out).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k]["verdict"] for k in ("M2", "M3", "M4")}))


if __name__ == "__main__":
    main()
