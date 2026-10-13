"""Column-order check over every released CausalArena sample file: share of true edges whose cause sits in an
earlier column than its effect, per family. No LLM. Writes column_order_check.json. Gate O1: every file was read."""
import argparse, glob, json, os
import numpy as np


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out, unread = {}, []
    for fam in ("semantic", "formula", "synthetic"):
        files = sorted(glob.glob(os.path.join(a.root, "scm", fam, "data", "**", "*rep000.npz"), recursive=True))
        files = [f for f in files if "obs_only" in f]
        fw = tot = full = 0
        for f in files:
            try:
                g = np.load(f, allow_pickle=False)["g"]
            except Exception:
                unread.append(f); continue
            ij = np.argwhere(g != 0)
            k = int((ij[:, 0] < ij[:, 1]).sum()); fw += k; tot += len(ij); full += int(k == len(ij))
        out[fam] = {"files": len(files), "files_fully_ordered": full, "true_edges": tot, "cause_in_earlier_column": fw,
                    "share": round(fw / tot, 6) if tot else None}
    out["unreadable_files"] = unread
    out["gate_O1_all_files_read"] = not unread
    os.makedirs(a.out, exist_ok=True)
    json.dump(out, open(os.path.join(a.out, "column_order_check.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(out))


if __name__ == "__main__":
    main()
