"""Page 10: plan and status, generated from the snapshot (bundles, queue, gates). Day-to-day work lives in the Slack lists."""
from pagekit import *  # noqa: F401,F403
import bundles as L4
import theses as L3

SNAP = __import__("common").SNAP
items = SNAP["items"]
cnt = {}
for i in items:
    cnt[i["status"]] = cnt.get(i["status"], 0) + 1
ab = [b for b in SNAP["bundles"] if b.get("plan") == "audit"]
q1 = [b for b in SNAP["bundles"] if b.get("plan", "q1") == "q1"]


def tile(num, label_):
    return (f'<div style="padding: 14px 16px; background: #FFFFFF; border: 1px solid #C9CEC6; border-radius: 12px">'
            f'<div style="font-family: {COND}; font-size: 34px; line-height: 38px; font-weight: 700">{num}</div>'
            f'<div style="font-size: 14px; color: #4E5751">{label_}</div></div>')


tiles = grid([tile(cnt.get("done", 0), "tracker items done, of %d" % len(items)),
              tile(cnt.get("in_progress", 0), "in progress"),
              tile(cnt.get("blocked", 0), "blocked, each on a named person or run"),
              tile("%d / %d" % (sum(b["status"] == "done" for b in ab), len(ab)), "audit bundles done"),
              tile("%d / %d" % (sum(b["status"] == "done" for b in q1), len(q1)), "Q1 bundles done")], min_w=180)


def you(h):
    return h.replace("your live runs", "Uzair's live runs").replace("waits on you", "waits on Uzair").replace("waiting on you", "waiting on Uzair").replace("Waiting on you", "Waiting on Uzair").replace("WAITING ON YOU", "WAITING ON UZAIR")


BODY = "\n".join([
    question("What is done, what is next, and what is waiting on whom?",
             before="nothing: this page is generated from the tracker and can be read on its own."),
    P(f"The team works from two Slack lists, kept in sync with the tracker; this page is the same state, for recentering. Work "
      f"comes in {T('bundle', 'bundles')}: each closes a set of {T('ticket', 'tickets')} and has a must-show list. {T('live', 'LIVE')} "
      f"work spends model calls and is started only by Uzair. Decisions happen at {T('gate', 'gates')} with tests stated in advance."),
    tiles,
    you(L4.audit_intro), you(L4.audit_host),
    H2("Quarter 1 plan"),
    delevel(L4.legend), delevel(L4.host),
    f'<div style="display: flex; flex-wrap: wrap; gap: 20px; align-items: stretch">{you(delevel(L4.detail))}{you(delevel(L4.queue))}</div>',
    delevel(L3.gates),
    answer(f"{cnt.get('done', 0)} of {len(items)} tracked items are done. The audits that remain wait on live runs that are under way "
           f"and, when a chance arises, interviews. The next decision is the wedge (AB-16): which results carry the paper, and when "
           f"the ledger kernel starts.",
           "What changed since you last looked?"),
])
