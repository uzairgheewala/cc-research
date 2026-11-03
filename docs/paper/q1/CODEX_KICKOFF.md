# Kickoff prompt: W1 (the Q1 paper) in Codex

Tickets: DLV-05, DLV-06
Paste everything between the two lines into a new Codex session opened on
`C:\Users\uzair\Documents\UCSD\Fall 2026\DSC 180A\cc-research`.

**3 Nov stage-2 update:** the verified Crucis extraction is complete. The current
root AGENTS.md and `docs/migrations/crucis-separation.json` lift the original
commit hold mentioned below; make automatic local milestone commits. Framework
development is now in `../crucis`, namespace `crucis`. Paper inputs stay here.

---

You are continuing **W1, the Q1 paper workstream** of my UCSD DSC 180A capstone. It was carried in a Claude chat until
3 Nov 2026; you pick it up exactly where it stopped.

**Read first, in this order, and do nothing else until you have:**
1. `AGENTS.md` (repo root) — the rules of this repository. Note the 3 Nov commit policy and the **temporary migration hold:
   no commits until the audit package is separated into its own repository** (`_repo_migration/2026-11-03/PROGRESS.md`).
2. `docs/paper/q1/HANDOFF.md` — W1's single resume point: role and owned files (§1), verified state (§2), rules (§3), the
   paper's machinery (§4), what other workstreams found that the paper must take in (§5), the ordered work queue with
   must-show lists (§6), my submission steps (§7), where inputs are (§8), and the session log (§9).
3. `docs/paper/q1/DESIGN.md`, then `docs/paper/q1/report.tex` and `docs/paper/q1/numbers.json`.
4. `docs/research/heuresis-scope-and-auditor-positioning-2026-11-03.md`.
5. `docs/paper/q1/CHECKPOINT_CONTRACT.md` and `checkpoint_contract.json`: the adopted 3 Nov scope/evidence freeze.
   Crucis is the chosen name. Keep the checkpoint's existing numerical sources while the package evolves separately.

**Then verify the state before changing anything** (use `tools/python.ps1` or the `.tooling` venv; always `-B`):
- `python -B docs/paper/q1/check_checkpoint_contract.py` → 78 keys, 13 number sources, 19 frozen files; OK;
- `python -B docs/paper/q1/build_numbers.py --check` → expect "78 entries match the lock";
- `python -B docs/paper/q1/lint_report.py` → expect 0 errors, 0 warnings;
- `git --no-optional-locks status --porcelain -- docs/paper docs/q1` and `git log -1` → HEAD `cf536c1`, W1's files
  uncommitted.
If anything differs from HANDOFF §2, stop and report the difference before editing.

HEAD may advance legitimately after the package separation. The immutable evidence baseline remains `cf536c1`;
do not treat a new HEAD alone as evidence drift. The checkpoint checker deliberately permits that change while
checking exact sources, registry bytes and values. Changes to registry keys/sources/selectors/formats require an
explicit contract revision; there is no automatic re-freeze. Manuscript/citation corrections remain permitted.

**The job now is P0 in HANDOFF §6 — the checkpoint due Fri 6 Nov:**
- P0.1 apply W2's corrections (HANDOFF §5 items 1–4): Causal-Copilot's loss is in its bootstrap step, not the model's
  review; say what Causal-Copilot's name-reliance number measures and that its verdict is exploratory; MATMCD "below on the
  point estimate" (or its interval via a key); 81 of 101 as BND-08's pre-registered test.
- P0.2 the Heuresis check (HANDOFF §5 item 5): narrow the `\ours` novelty sentences if they overclaim, and add a checked
  citation (claim, location, short quote, verdict in `lit_claims.json`; BibTeX from the primary page).
- P0.3 build (`python -B docs/paper/q1/build_paper.py`; if XeLaTeX or the fonts are missing, `--no-pdf --overleaf`).

**Non-negotiables** (HANDOFF §3): every number through `\nm{key}` from a file + pointer in `numbers.json` (the lint
enforces it); no literature claim without a citation checked against its paper; edit only `docs/paper/q1/**` and
`docs/q1/**` (pinned files through a `jobs/patches/w1_NN_*.py` patch with a hash guard, then verify / trace / snapshot
last); ticket or contract changes are requests in `docs/paper/q1/w5_requests.md`; never open `../Causal-Copilot/.env`;
no API spend; no push; no commits while the migration hold stands.

**How to work and report:** full design first for anything non-trivial, then bundles, each with a must-show list. Open
every reply with "where we are now" and close with "where we're going"; plain language; derive any metric step by step.

**Before you end the session (every time):** append a dated entry to HANDOFF §9 (what changed, which sentences, which
keys were added, check results, anything left open), update HANDOFF §2 to the new verified state, and update
`docs/commit_msgs/q1_checkpoint_cc-research.txt` to cover the new changes. That is how I carry the work back to the Claude
chat, which resumes from HANDOFF.md.

---

## Coming back to the Claude chat
Paste: "Resume W1 from `docs/paper/q1/HANDOFF.md` (read §2 and the newest §9 entry first) and verify the state before
continuing."
