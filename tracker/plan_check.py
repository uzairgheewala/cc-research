"""Check a bundle DAG (plans/q1_dag.json): IDs, dependencies, acyclicity, ticket references, coverage of the declared scope,
dates (a bundle cannot end before what it depends on; a milestone cannot come before the bundles it requires; a bundle cannot
end after the due date of a ticket it closes), and approval flags on bundles that spend API credit.

  python tracker/plan_check.py [plans/q1_dag.json] [--mermaid]
"""
import datetime, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import catalogue as C  # noqa: E402

path = Path(next((a for a in sys.argv[1:] if not a.startswith("--")), HERE.parent / "plans" / "q1_dag.json"))
P = json.load(open(path, encoding="utf-8"))
dev = {i["id"]: i for i in C.ITEMS}
prod = {r["id"] for r in json.load(open(HERE / "prod.json", encoding="utf-8"))}
B = {b["id"]: b for b in P["bundles"]}
d = lambda s: datetime.date.fromisoformat(s)
errs, warns = [], []
if len(B) != len(P["bundles"]):
    errs.append("duplicate bundle IDs")
for b in B.values():
    for dep in b["depends_on"]:
        if dep not in B:
            errs.append("%s depends on unknown %s" % (b["id"], dep))
        elif d(b["window"][1]) < d(B[dep]["window"][1]):
            errs.append("%s ends %s before its dependency %s ends %s" % (b["id"], b["window"][1], dep, B[dep]["window"][1]))
    for t in b["closes"] + b["advances"]:
        if t not in dev and t not in B and t not in prod:
            errs.append("%s names unknown ticket %s" % (b["id"], t))
    for t in b["closes"]:
        due = dev.get(t, {}).get("due")
        if due and d(b["window"][1]) > d(due):
            errs.append("%s closes %s after its due date %s" % (b["id"], t, due))
    spends = b["llm_cost"] != "none"
    if spends and not b["approval_needed"]:
        errs.append("%s spends API credit but has no approval flag" % b["id"])
    if spends and "Uzair" not in b["runner"]:
        errs.append("%s spends API credit but is not run by Uzair" % b["id"])
    if not b["must_show"]:
        errs.append("%s has no must-show list" % b["id"])
# acyclic
state = {}
def visit(u, stack):
    state[u] = 1
    for v in B[u]["depends_on"]:
        if v in B and state.get(v) == 1:
            errs.append("cycle: %s" % " -> ".join(stack + [v]))
        elif v in B and v not in state:
            visit(v, stack + [v])
    state[u] = 2
for u in B:
    if u not in state:
        visit(u, [u])
# coverage: every scoped ticket closed by exactly one bundle (or listed as outside, or already done)
closers = {}
for b in B.values():
    for t in b["closes"]:
        closers.setdefault(t, []).append(b["id"])
scoped = sorted({t for k, v in P["scope"].items() if k != "outside_bundles" for t in v})
status = {r["id"]: r for r in json.load(open(HERE / "status.json", encoding="utf-8"))["items"]}
for t in scoped:
    n = len(closers.get(t, []))
    if t in P["scope"]["outside_bundles"]:
        continue
    if n == 0 and (status.get(t) or {}).get("effective_status") != "done":
        errs.append("%s is in scope but no bundle closes it" % t)
    if n > 1:
        errs.append("%s is closed by several bundles: %s" % (t, closers[t]))
for t, bs in closers.items():
    if t not in scoped:
        warns.append("%s closed by %s is outside the declared scope (supporting ticket)" % (t, bs[0]))
for m in P["milestones"]:
    for r in m["requires"]:
        if d(B[r]["window"][1]) > d(m["date"]):
            errs.append("milestone %s (%s) needs %s, which ends %s" % (m["id"], m["date"], r, B[r]["window"][1]))
# critical path by end dates
order, seen = [], set()
def topo(u):
    if u in seen: return
    seen.add(u)
    for v in B[u]["depends_on"]: topo(v)
    order.append(u)
for u in B: topo(u)
longest = {}
for u in order:
    prev = max((longest[v] for v in B[u]["depends_on"]), key=len, default=[])
    longest[u] = prev + [u]
crit = max(longest.values(), key=len)
print("bundles %d; scoped tickets %d; closed by bundles %d; live (API) bundles %s" % (
    len(B), len(scoped), len(closers), [b for b in B if B[b]["llm_cost"] != "none"]))
print("longest dependency chain: " + " -> ".join(crit))
for e in errs: print("  ERROR " + e)
for w in warns: print("  note  " + w)
if "--mermaid" in sys.argv:
    print("graph LR")
    for b in B.values():
        live = b["llm_cost"] != "none"
        print('  %s["%s<br/>%s"]%s' % (b["id"].replace("-", ""), b["id"], b["title"].split(":")[0][:38], ":::live" if live else ""))
        for dep in b["depends_on"]:
            print("  %s --> %s" % (dep.replace("-", ""), b["id"].replace("-", "")))
sys.exit(1 if errs else 0)
