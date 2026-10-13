# Relay: milestones, summaries and artifacts to Slack

Every message about the work is generated from the tracker files, names its tickets, and is logged with where it landed.
`relay.py` prepares messages and records them; it never talks to Slack itself. Posting is done by Claude (dev) or by
Uzair (prod) with the Slack tools.

## 1. Where things go

| | Dev: #cd-tracker (C0C7Q2CA2G7) | Prod: #causal-discovery (C0C8CQK1XME) |
|---|---|---|
| Audience | working record | classmates, TA, mentor |
| Scope | every dev ticket | only the rows of the CD Tracker list |
| Who posts | Claude posts directly | Claude creates a Slack draft in the channel; Uzair edits and sends it (or tells Claude to send that one message) |
| List | Dev CD Tracker: synced after every verification | CD Tracker: synced after every verification (`prod-rows`, update, `mirror --list prod`, `prod-publish`) |
| Artifacts | any file in cc-research except credentials and upstream code | only files that evidence a prod row, each upload confirmed by Uzair |

## 2. Message types

| Type | When | Content | Command |
|---|---|---|---|
| digest | dev: end of each working session and at least weekly; prod: weekly (Fridays) | summary points (each must name a ticket; in prod, a prod row), then what is newly done, reopened, started, blocked and new since the last digest in that channel, what is due in 14 days, and totals | `relay.py digest --channel dev\|prod --point "..."` |
| milestone | a ticket (dev) or a prod row (prod) turns ✅, or a ✅ is reopened | dev: closing criterion, checks, evidence paths and the group or deliverable it feeds; prod: the row, its evidence level and its tickets | `relay.py milestones --channel dev\|prod` |
| artifact | a report, table or figure worth reading | path, sha256, tickets, one-line summary; the file itself is uploaded in the same message or as a thread reply | `relay.py artifact PATH --tickets ... --summary ... --channel ...` |
| correction | R2 fired: something announced ✅ is no longer done | a reply in the thread of the original message, naming what changed | written by hand, recorded like any other |

The first digest in a channel sets the baseline: later digests and milestones report changes against the last one recorded.

## 3. Flow

1. `python tracker/verify.py` and `python tracker/trace.py check` (zero errors).
2. Sync both lists: `trace.py list-diff dev` and `list-diff prod` give only the cells that changed (new rows have no record ID
   yet and are added); push them, run `trace.py list-synced <list>`, then `prod-publish`. `mirror` against a fresh export
   whenever someone may have edited a list by hand.
3. Prepare: `relay.py milestones` and/or `relay.py digest` per channel. The text is in `relay_out/<stamp>_<type>_<channel>.md`.
4. Dev: post it, then `relay.py record relay_out/<file>.json --ts <message ts>`.
   Prod: create it as a draft in #causal-discovery, `relay.py record <file> --draft`; once Uzair sends it, find the message and
   `relay.py record <file> --ts <message ts>`.
5. Recording appends to `relay_log.jsonl` and adds `TICKET published_at slack:<channel>/<ts>` for every ticket in the message,
   so `trace.py show ID` lists every message that mentioned it.

## 4. Checks (run by `trace.py check` and `relay.py check`)

| Code | Fires when |
|---|---|
| R1 | a relayed artifact changed or disappeared after it was posted: the Slack copy is stale |
| R2 | a ticket announced ✅ in a channel is no longer done: a correction is owed in that thread |
| R3 | a message was prepared (or drafted) two or more days ago and never sent and recorded |
| R5 | a channel's last digest is eight or more days old |

## 5. Rules

- Every number in a message comes from `status.json` or an evidence file; nothing is typed from memory.
- Summary points name the tickets they are about; prod points name prod rows.
- Never relay `.env`, keys, tokens, or files from `../Causal-Copilot` (`relay.py` refuses paths outside cc-research).
- A prod message is sent only by Uzair, or by Claude after Uzair says to send that message.
