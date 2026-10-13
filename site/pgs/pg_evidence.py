"""Reference: every number the narrative pages printed, with its source file and that file's sha256 (from the snapshot)."""
from pagekit import *  # noqa: F401,F403
import common
import pagekit

SNAP = common.SNAP
rows = []
for key in sorted(getattr(pagekit, "PRINTED", set())):
    mm = SNAP["metrics"].get(key)
    if not mm:
        continue
    src = mm["src"]
    rows.append([f'<code>{esc(key)}</code>', esc(common.fmt(mm["value"])),
                 f'<a href="{common.EVBASE[0]}{src}">{esc(src)}</a>', f'<code>{SNAP["sources"].get(src, "")[:12]}</code>'])

BODY = "\n".join([
    question("Where does each number on this site come from?"),
    P(f"{len(rows)} numbers printed on the pages above, read by <code>tracker/snapshot.py</code> from {len(SNAP['sources'])} files. A number that is "
      f"quoted from a report is checked to appear verbatim in that report; every other number is read from a result file. The "
      f"hash fixes the file's exact contents at the time of the snapshot."),
    table(["Key", "Value", "Source file", "sha256 (first 12)"], rows, mono_cols=(1,)),
])
