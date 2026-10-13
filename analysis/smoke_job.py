"""Smoke job for the compute runner (INF-04 gates J1, J2). Deterministic work over 24 items, slow enough to need chunks.

  python analysis/smoke_job.py --out jobs/smoke/out/smoke.json [--budget-s 5] [--sleep 0.5]
"""
import argparse, hashlib, os, re, socket, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jobkit  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--budget-s", type=float, default=0)
ap.add_argument("--sleep", type=float, default=0.5)
a = ap.parse_args()

# J2: what this process can see. A compute job must not see a key and, in the container, must have no network.
secret_vars = sorted(k for k, v in os.environ.items() if re.search(r"KEY|TOKEN|SECRET|PASSWORD", k, re.I) and v)
try:
    socket.create_connection(("1.1.1.1", 443), timeout=2).close(); net = True
except OSError:
    net = False
dotenv = "/app/.env"
dotenv_size = os.path.getsize(dotenv) if os.path.exists(dotenv) else None   # size only; the file is never opened
print("J2 env secret-like variables: %s; network reachable: %s; /app/.env size: %s" % (secret_vars or "none", net, dotenv_size))

parts = jobkit.Parts(a.out)
budget = jobkit.Budget(a.budget_s)
items = list(range(24))
for i in items:
    k = "item%02d" % i
    if parts.has(k):
        continue
    if not budget.ok(a.sleep + 0.2):
        break
    time.sleep(a.sleep)
    parts.add(k, {"value": hashlib.sha256(str(i).encode()).hexdigest()[:16]})
jobkit.finish(parts, {"job": "smoke", "items": len(items)}, len(items))
