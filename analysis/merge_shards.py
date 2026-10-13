"""Merge jobkit shard outputs of one job into a single output (rows sorted by key; header from shard 0 without 'shard')."""
import argparse, hashlib, json
ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("shards", nargs="+")
a = ap.parse_args()
rows, header = {}, None
for f in a.shards:
    d = json.load(open(f, encoding="utf-8"))
    h = dict(d["header"]); h.pop("shard", None); h["files"] = None
    header = header or h
    for r in d["rows"]:
        assert r["key"] not in rows
        rows[r["key"]] = r
header["files"] = len(rows); header["merged_from"] = len(a.shards)
txt = json.dumps({"header": header, "rows": [rows[k] for k in sorted(rows)]}, sort_keys=True, indent=1)
open(a.out, "w", encoding="utf-8").write(txt)
print("merged %d rows sha256=%s" % (len(rows), hashlib.sha256(txt.encode()).hexdigest()))
