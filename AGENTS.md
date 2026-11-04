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
4. Local commits in cc-research and the standalone audit repository are authorized. Follow the milestone workflow below.
   Do not push, publish, merge, rewrite history, or alter other repositories without authorization for that action.
5. Never start anything that spends API credit (`cc.ps1 golden`, `cc.ps1 plan ...`, the queue runner). Write the plan; Uzair runs it.
6. Research analysis/results go in `analysis/`; plans in `plans/`. The reusable auditor belongs in its own sibling
   repository. Migration backups/checks and the local Python environment may live in `_repo_migration/` and `.tooling/`
   beside this repository. Preserve recorded evidence paths during extraction.
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
   Text written through Slack rich-text parsing must escape literal `&`, `<` and `>`
   as `&amp;`, `&lt;` and `&gt;`, then be read back. A successful update response is not
   proof of preserved scientific notation: the unescaped AUD-12 note lost part of
   `<-> and o->` during the 3 Nov parity repair; the escaped write read back correctly.
   A zero `list-diff` compares with the last local synced copy, not live Slack.
   Claim parity only after a fresh readback. Keep expected date lag separate:
   Verified dates are sent only with another changed field, not as mass date-only updates.
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

This folder is a git repository (layout and reasons: `docs/REPO.md`). Uzair authorized automatic local milestone commits
on 3 Nov 2026. Read `tools/skills/milestone-commit/SKILL.md` at the start of development work and follow it after every
small coherent, validated milestone, including documentation and design milestones. Check again before ending the turn.
Stage explicit owned paths or hunks, preserve other workstreams' changes, and report each commit hash. Prepared commit
messages in `docs/commit_msgs/` remain useful inputs; writing a message is not a substitute for committing.

**Crucis separation (3 Nov 2026):** the reusable auditor is in the sibling `../crucis` repository.
The separation receipt records the installed-wheel, recorded-data and certificate checks. The user-required
migration hold is lifted by that verified cutover; make automatic local milestone commits from then on.
Research evidence, the paper, and the historical B5 modules remain here. Current instructions supersede
older no-git/Uzair-commits and pre-extraction paths in historical handoffs. No remote publication is implied.

Crucis is now public at https://github.com/crucis-lab/crucis. Its approved
distribution/command is `crucis-causal`; Python imports use `crucis_causal`.
Read `../crucis/README.md` and `../crucis/provenance/publication.json` before
resuming subsystem work; current design notes are under `../crucis/crucis_causal/docs/`.
The original four extraction milestones were backed up and cleaned before their
first push. Never reintroduce archived funding/correspondence files or old history.

Before committing evidence or ticket changes:

    python tracker/verify.py && python tracker/trace.py check
    python tracker/snapshot.py          # site/snapshot.json: every ticket, bundle, list state and site number
    python tools/secret_scan.py && python tools/ci_check.py
    python site/build.py

`tracker/snapshot.py` copies `tracker/status.json`, so it runs after the last `verify.py` (including `--repin`) and the
last catalogue patch, and `site/snapshot.json` goes in the same commit as the change that moved the status. A repin or
patch after the snapshot leaves it stale: CI fails (20 Oct, commit 1a2c631, after p30). The pre-commit hook runs
`tools/commit_gate.py`, which exports the exact staged tree into an isolated directory and runs the checks in the staged
`.commit-policy.json`. It catches a refreshed snapshot left unstaged and refuses the commit if the index or HEAD changes
during validation. Run external-data checks separately when needed; a skipped test is not a completed reproduction.

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
