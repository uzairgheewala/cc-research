"""2026-10-19: adopt batched waves (docs/WAVES.md, WAVE_STATE.md). AGENTS.md gains a 'How work is batched' section;
INF-10 (the wave runner and kit builder, built in wave A) enters the catalogue. Refuses to run twice."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
a = ROOT / "AGENTS.md"
t = a.read_text(encoding="utf-8")
assert "## How work is batched (waves)" not in t, "already applied"
anchor = "## Where things are"
assert anchor in t
t = t.replace(anchor, """## How work is batched (waves)

Read `WAVE_STATE.md` first, then `docs/WAVES.md`. One "go" from Uzair is one wave: read the last run sheet's
`RETURN.json`, build all the logic for every unblocked bundle (design, hashed pre-registration, code, tests, a free smoke
run of every heavy or live job), pack every heavy (H) and live (L) job into one run sheet, list manual steps and
decisions (with defaults) once, hand over in one message, and stop. Never wait on or poll Uzair's runs; never rebuild in
the sandbox what a previous wave computed (the engine cache ships with the kit); run tests and checks once per kit.

""" + anchor, 1)
a.write_text(t, encoding="utf-8")
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p23" in c, "apply p23 first"
assert "# ---- overrides p24" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p24 (2026-10-19): batched waves adopted; INF-10
ITEMS.append(item("INF-10", "INF", "Wave runner and kit builder: one run sheet per wave (preflight, canaries, gates, caps, resume, RETURN.json)",
                  "todo", kind="task",
                  criterion=("cc.ps1 wave <id> runs a sheet on Uzair's machine: preflight checks code identity, disk, RAM and files; one "
                             "canary per job runs first; gated jobs are skipped when their gate fails; a failing job stops only itself; "
                             "RETURN.json is written incrementally with status, exit, code identity, output hashes, cost and wall time; "
                             "the kit builder ships code, the engine cache and needed data to the agent's sandbox; unit tests"),
                  evidence=["docs/WAVES.md", "WAVE_STATE.md"],
                  note="Adopted 19 Oct (docs/WAVES.md). Built in wave A; must show: a 3-job demo sheet with one gated skip and one failing canary."))
'''
p.write_text(c + "\n", encoding="utf-8")
print("p24 applied")
