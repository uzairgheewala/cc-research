"""Page 11: what changed recently, generated from the posted team digests (snapshot "changes")."""
from pagekit import *  # noqa: F401,F403
import re

SNAP = __import__("common").SNAP
TICKET = re.compile(r"\b((?:AUD|RQ|CAP|BLD|TGT|DEC|REP|DOM|BEN|EVL|INF|DLV|CRS|TEAM|EXT|STR|RSK|BND)-\d+)\b")


def digest(d):
    pts = "".join(f'<li style="margin: 0 0 8px">{esc(p)}</li>' for p in d["points"])
    done = (f'<p style="margin: 6px 0 0; font-size: 14px; color: #4E5751"><b>Finished:</b> {esc("; ".join(d["done"][:8]))}'
            f'{" …" if len(d["done"]) > 8 else ""}</p>') if d["done"] else ""
    when = (d.get("posted_utc") or "")[:16].replace("T", " ") + " UTC"
    return box(f'<span style="font-size: 12px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; color: #1D5C99">'
               f'{when}</span><ul class="prose" style="margin: 0; padding-left: 20px; font-size: 15px; line-height: 23px">{pts}</ul>{done}')


ch = SNAP.get("changes") or []
BODY = "\n".join([
    question("What moved since I last looked?", before="nothing: generated from the team's posted digests, newest first."),
    P("Each block is one digest the team posted in its public channel, with its summary points and what it finished. Ticket "
      "IDs (AUD-45, RQ-10 …) match the Slack lists and the status page. Working notes stay in the team's own channel; "
      + ("%d of them have been posted since the newest block below." % (SNAP.get("changes_lag") or {}).get("dev_since_last_prod", 0)
         if (SNAP.get("changes_lag") or {}).get("dev_since_last_prod") else "none are newer than the newest block below.")),
    *[digest(d) for d in ch],
    P("No digests recorded yet.") if not ch else "",
    answer("The newest block says what moved most recently; the status page shows where that leaves the plan.",
           "Back to the plan: what is done and what is waiting?"),
])
