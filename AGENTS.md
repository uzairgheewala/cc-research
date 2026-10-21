# AGENTS.md: rules for any agent working in cc-research

Read this before doing anything here. Claude reads it through `CLAUDE.md`; other agents read it directly.

## What this is

Out-of-repo research tooling and evidence for a study of Causal-Copilot (upstream commit `a31aa7c`, arXiv 2504.13263),
UCSD DSC 180A. Everything we claim must be checkable from the files in this folder.

## Hard rules

1. Never open, print, copy or summarise `../Causal-Copilot/.env`; never ask anyone to paste an API key.
2. Never write credentials or tokens anywhere (this includes the Jupyter token inside `../DSC180A-Methodology-1-main.zip`).
3. Never modify, refactor or overwrite anything in `../Causal-Copilot` yourself. `main` of the fork stays the untouched
   baseline (checked against `manifests/baseline_a31aa7c.sha256` before every run). Changes live only on ticket branches,
   written by the agent as patch files in `jobs/fork/` and applied by Uzair (`jobs/fork/make_branches.ps1`, docs/FORK.md);
   a branch run sets `CC_BRANCH` and is checked against `jobs/fork/<branch>.json`.
4. Never run git write operations on Uzair's repositories.
5. Never start anything that spends API credit (`cc.ps1 golden`, `cc.ps1 plan ...`, the queue runner). Write the plan; Uzair runs it.
6. Analysis code and results go in `analysis/`; plans in `plans/`; nothing outside `cc-research/`.
7. Slack has two lists and two channels (tracker/LINKS.md section 1, tracker/RELAY.md).
   Dev: #cd-tracker (C0C7Q2CA2G7) and the list "Dev CD Tracker" (F0C869P25NE): write freely.
   Prod: #causal-discovery (C0C8CQK1XME) and the list "CD Tracker" (F0C8ADF3DNG). Which rows are in prod is Uzair's call
   (`tracker/prod_spec.json`); never add or remove prod rows on your own. Keep the CD Tracker list in sync with
   `prod_rows.json`. Never send a message in #causal-discovery: prepare it with `relay.py`, create it as a draft, and
   let Uzair send it (or send that one message when he says so).
   Slack List columns added through the API get an internal key made from their name. Never add a column whose key would be
   a reserved word (`id`, `name`, `type`, `created`, ...): a column keyed `id` broke the CD Tracker list in the Slack app
   (10 Oct). Add it under a distinct name (e.g. "Ticket ID") and then rename it.
   A select column's options are stored as slug values ("0 Quarter 1 deliverables" is stored as `0_quarter_1_deliverables`).
   When adding an option, resend every existing option with its slug value and its label; sending label text as the value
   detaches every existing row from its option (seen 10 Oct on the Dev list's Category; fixed by resending the slugs).
8. Do not rely on answers from Prof. Huang's group.

## Tickets and links (the tracker)

Every piece of work belongs to a ticket. The contract is `tracker/README.md` (one ticket and its evidence) and
`tracker/LINKS.md` (how tickets, prod items, evidence, runs, docs and Slack are linked).

Before starting work:

    python tracker/trace.py show <ID>        # what the ticket needs, what blocks it, what it feeds, where it is shown

If no ticket fits, add one to `tracker/catalogue.py` with the ID from `python tracker/trace.py next-id <PREFIX>` (never reuse one).

While working:

- Name the ticket ID in everything you produce: the first lines of a report (`Tickets: BEN-03, TGT-02`), plan files,
  result JSON (`"tickets": [...]`), Slack messages in #cd-tracker. `trace.py` scans docs for IDs and warns on unknown ones.
- Record relations as typed links, never as prose only:
  `python tracker/trace.py link BLD-04 implements CAP-04` (relations: LINKS.md section 3).
- Put a blocker that is a ticket in `blocked_by` by its ID (it becomes a `blocks` link).

To close a ticket:

1. Write the closing criterion, the evidence files and, for any number, a check, in `catalogue.py`.
2. `python tracker/verify.py`: the ticket must reach V2, or V3 if it has checks. Never edit `pins.json` or `evidence_log.jsonl` by hand.
   Repin only after a deliberate change: `verify.py --repin ID`, and say why.
3. `python tracker/trace.py check`: zero errors. Read the warnings that name your ticket.
4. Sync both Slack lists and relay what changed (tracker/RELAY.md section 3): milestones and digests, prepared by
   `tracker/relay.py` and recorded after posting.

Never set a prod status by hand, never claim "done" in a summary for something `status.json` does not show as done, and say
"needs evidence" when it shows `done_needs_evidence`.

## Repository, CI and the site

This folder is a git repository (layout and reasons: `docs/REPO.md`). Uzair makes every commit and push; agents write the
commit message to `docs/commit_msgs/<execution>_cc-research.txt`. Before handing over a commit:

    python tracker/verify.py && python tracker/trace.py check
    python tracker/snapshot.py          # site/snapshot.json: every ticket, bundle, list state and site number
    python tools/secret_scan.py && python tools/ci_check.py
    python site/build.py

`tracker/snapshot.py` copies `tracker/status.json`, so it runs after the last `verify.py` (including `--repin`) and the
last catalogue patch, and `site/snapshot.json` goes in the same commit as the change that moved the status. A repin or
patch after the snapshot leaves it stale: CI fails (20 Oct, commit 1a2c631, after p30). The pre-commit hook runs
`tracker/snapshot.py --check` and stops a stale snapshot on disk; it cannot see a regenerated snapshot that was not staged.

The site (`site/`) may print a number only through `site/registry.py` (file + JSON pointer, or a literal checked in the
cited report). Never type a result into a level's text. New data kept outside git (`external/`, `runs/`) must be hashed
into `manifests/excluded/` with `python tools/data_manifest.py`.

## The plan

Work is done in bundles (`plans/q1_dag.json`, explained in `analysis/reports/q1_execution_plan.md`), each a ticket with a
must-show list. `python tracker/plan_check.py` must pass before a bundle starts. Never start a LIVE bundle: prepare it, and
Uzair approves and runs it.

## How work is batched (waves)

Read `WAVE_STATE.md` first, then `docs/WAVES.md`. One "go" from Uzair is one wave: read the last run sheet's
`verdict.json` (inside `return_<wave>.zip`), build all the logic for every unblocked bundle (design, hashed pre-registration, code, tests, a free smoke
run of every heavy or live job), pack every heavy (H) and live (L) job into one run sheet, list manual steps and
decisions (with defaults) once, hand over in one message, and stop. Never wait on or poll Uzair's runs; never rebuild in
the sandbox what a previous wave computed (the engine cache ships with the kit); run tests and checks once per kit.

## Where things are

| Path | What |
|---|---|
| `README.md` | harness setup and commands (`cc.ps1`) |
| `harness/` | recorder, plan runner, stub LLM, fetcher |
| `plans/` | run plans; `plans/results/` their outputs |
| `runs/<run_id>/` | one recorded run: `meta.json`, `llm_calls.jsonl`, artifacts, state snapshots |
| `analysis/` | analysis scripts, `results/`, `reports/`, `literature/` |
| `external/` | downloaded benchmarks (CausalArena, Causal Chambers) |
| `docs/project_snapshots/` | dated copies of claude.ai project docs, so tickets can check them |
| `tracker/` | tickets, evidence, links, prod list, checks |

## Style for anything written here

Plain, specific sentences; numbers with their source file; no claim beyond what the evidence shows.
