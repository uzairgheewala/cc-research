"""Gates J1 and J2 for the compute runner (INF-04). Writes jobs/gates.json.

J1  a job run in many chunks ends with the same output hash as the same job run in one chunk (smoke vs smoke_oneshot), and
    the container run (smoke_container) matches too once it exists.
J2  inside the container: no secret-like environment variable, no network, and the repo's .env replaced by an empty file.
"""
import json, re
from pathlib import Path

R = Path(__file__).resolve().parent.parent / "jobs"
done = {k: json.load(open(R / k / "done.json")) if (R / k / "done.json").exists() else None for k in ("smoke", "smoke_oneshot", "smoke_container")}
h = {k: (list(v["outputs"].values())[0] if v else None) for k, v in done.items()}
g = {"hashes": h, "chunks": {k: (v or {}).get("chunks") for k, v in done.items()}}
g["J1_shell"] = bool(h["smoke"] and h["smoke"] == h["smoke_oneshot"] and done["smoke"]["chunks"] > 1)
g["J1_container"] = bool(h["smoke_container"] and h["smoke_container"] == h["smoke_oneshot"] and done["smoke_container"]["chunks"] > 1)
j2 = None
log = R / "smoke_container" / "log.jsonl"
if log.exists():
    lines = [json.loads(l) for l in open(log) if l.strip()]
    outs = " ".join(l["stdout_tail"] for l in lines)
    m = re.search(r"J2 env secret-like variables: (.*?); network reachable: (\w+); /app/.env size: (\w+)", outs)
    if m:
        j2 = {"secret_vars": m.group(1), "network": m.group(2), "dotenv_size": m.group(3),
              "host": sorted({l["host"] for l in lines})}
g["J2_observed"] = j2
g["J2"] = bool(j2 and j2["secret_vars"] == "none" and j2["network"] == "False" and j2["dotenv_size"] == "0" and j2["host"] == ["container"])
json.dump(g, open(R / "gates.json", "w"), indent=1, sort_keys=True)
print(json.dumps(g, indent=1))
