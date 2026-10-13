# Goals tracker with evidence

Every goal of the project is a ticket with a stable ID (REP-01, AUD-05, ...). A ticket is "done" only when the evidence
that closed it can be checked again, by anyone, from the files in this folder. This file is the contract.

## Files

| File | Role | Who writes it |
|---|---|---|
| `catalogue.py` | the tickets: ID, category, title, status, kind, closing criterion, evidence, checks, reproduce command, reopen triggers, due date, blocker, note | edited by hand (or by Claude), reviewed like code |
| `verify.py` | checks every ticket's evidence, computes its evidence level, writes the outputs below | code |
| `pins.json` | the hash of every evidence file or folder when it was first verified | written by `verify.py`; changed deliberately with `--repin` |
| `evidence_log.jsonl` | append-only history: every verification (per ticket: status, level, evidence hashes, failed checks) and every recorded reproduction | appended by `verify.py`; never edited |
| `status.json`, `status.md` | the current verified state of every ticket | written by `verify.py` |
| Slack List "CD tracker" | a mirror of `status.json` for reading and quick status changes | written from `status.json`; it is not the source of truth |
| `LINKS.md`, `trace.py` | the correlation layer: typed links between tickets, the prod list (`prod.json`), evidence, runs, docs and Slack; IDs locked in `ids.lock`; prod reviews in `reviews.jsonl`; Slack record IDs in `mirrors.json`; report in `trace.md` / `trace.json` | `trace.py` (see LINKS.md) |
| `../AGENTS.md` (via `../CLAUDE.md`) | the rules every agent follows here, including how to reference and link tickets | Uzair |

## Status (the legend used in Slack)

| Emoji | Status | Meaning |
|---|---|---|
| ✅ | done | closing criterion met and evidence recorded |
| 👀 | in progress | started; or a done ticket reopened because its evidence changed, disappeared or a check now fails |
| ⏳ | to-do | committed, not started |
| 🔴 | blocked | cannot proceed until the named blocker is resolved |
| 🔵 | open | not committed: a question, a decision not yet taken, a stretch goal, a monitored risk |

## Evidence levels

| Level | Name | Meaning |
|---|---|---|
| V0 | claimed | nothing recorded |
| V1 | pointer | evidence named but not checkable from here (project doc, chat, Slack, URL), or files missing |
| V2 | pinned | every file of evidence exists and its hash matches the pin |
| V3 | asserted | V2, and every machine check on the evidence passes now (a number in a result file, a gate, a pattern in code) |
| V4 | reproduced | V3, and the producing command was re-run after the current pins and the result recorded (`--reproduced ID`) |

## Rules

1. A ticket may be marked done only with a written closing criterion and evidence. Required level: V2, or V3 when the ticket has checks. Numerical claims must have checks.
2. A done ticket whose evidence changes (hash drift), disappears, or whose check fails is reopened automatically (👀) until someone re-verifies it and repins on purpose (`verify.py --repin ID`), saying why in the commit message or log.
3. A done ticket below its required level keeps ✅ but is listed as "needs evidence" in every verification report.
4. Reopen triggers are written per ticket (for example: the Causal-Copilot tree stops matching the baseline manifest; the CausalArena files change; new runs added to an analysed label).
5. Pointers to places that cannot be checked from here (project docs, chat, Slack) never count above V1. To raise them, snapshot the content into `docs/project_snapshots/<date>/` and add a check.
6. IDs are never reused. A ticket that is abandoned is marked open with a note, not deleted.
7. The Slack List mirrors `status.json`. If a status is changed in Slack, the same change goes into `catalogue.py` before the next verification.

## Commands

    python tracker/verify.py                       # verify everything (about a minute; reads, never modifies evidence)
    python tracker/verify.py --repin AUD-05        # accept new evidence hashes for AUD-05 after a deliberate change
    python tracker/verify.py --reproduced BEN-03 --note "re-ran error_budget.py, identical JSON"
    python tracker/trace.py check                  # after verify.py: links, prod list, IDs, mirrors (LINKS.md section 6)
    python tracker/trace.py show BEN-03            # one ticket with everything linked to it

## What closed each done ticket

For any done ticket, `status.md` lists its evidence files, the checks and their current results, and its level;
`evidence_log.jsonl` shows when each of those was verified and with which hashes.
