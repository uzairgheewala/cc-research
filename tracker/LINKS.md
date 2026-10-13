# Correlation layer: how dev tickets, prod rows, evidence, runs, docs and Slack are linked

`README.md` (this folder) defines one ticket and its evidence. This file defines how things relate to each other.
`RELAY.md` defines how milestones, summaries and artifacts reach the Slack channels. All three are plain files, so any
agent or person can read, check and diff them.

## 1. Two lists, one ID space

| | Dev | Prod |
|---|---|---|
| Slack List | "Dev CD Tracker" (F0C869P25NE), private | "CD Tracker" (F0C8ADF3DNG), in #causal-discovery |
| Channel | #cd-tracker (C0C7Q2CA2G7) | #causal-discovery (C0C8CQK1XME) |
| Rows | every ticket in `catalogue.py` | the rows Uzair chose, in `prod.json` (his instruction: `prod_spec.json`) |
| Who decides what is in it | anyone working (Claude, Uzair) | Uzair |
| Status | `verify.py` (evidence) | derived from the dev tickets behind each row, never set by hand |

Both lists use the same encoding (`REP-01`, `AUD-05`, ...). A prod row is one of two types:

- **pass-through**: the row is a dev ticket, with the same ID. Its prod title may differ (the research questions are
  phrased as questions in prod). Its status and evidence are the dev ticket's.
- **group**: a new ID in the same encoding (the next free number of its prefix, e.g. `REP-14`) that rolls up several dev
  tickets through `curates` links. The ID is locked in `ids.lock` as a prod ID, so no dev ticket can take it later
  (`trace.py next-id REP` gives the next number free in both lists).

Dev tickets named in no prod row stay dev-only. `trace.md` lists them on every check.

## 2. Node IDs (namespaced, immutable)

| Kind | Form | Example | Resolves when |
|---|---|---|---|
| dev | `<PREFIX>-NN`, prefix from `catalogue.CATS` | `AUD-05` | defined in `catalogue.py` |
| prod group | same form, issued to a group | `AUD-16` | defined in `prod.json` as a group |
| file | `file:<path from cc-research>` (globs allowed) | `file:analysis/reports/program_v2.md` | exists on disk |
| repo | `repo:<path from Causal-Copilot>` | `repo:postprocess/judge_functions.py` | exists on disk |
| run | `run:<run_id>` | | `runs/<id>/meta.json` exists |
| slack | `slack:<channel>[/<ts>]` | `slack:C0C8CQK1XME/1791580546.004809` | format only |
| slacklist | `slacklist:<list>[/<record>]` | `slacklist:F0C869P25NE/Rec0C88CY66NM` | format only |
| project, url, chat | `project:claude/<doc>.md`, `url:https://...`, `chat:<where>` | | format only |

An ID is bound the first time `trace.py check` (or `prod-apply`) sees it, and is never reused. A ticket may leave only
through `trace.py retire ID --note WHY`. Titles may change; IDs may not.

## 3. Relations

| Relation | From -> to | Inverse | Acyclic | Meaning and effect |
|---|---|---|---|---|
| curates | prod group -> dev | curated_into | | the group rolls up these tickets; its status is derived from theirs (section 4) |
| blocks | ticket -> ticket | blocked_by | yes | SRC must finish before DST can; `blocked_by` text in the catalogue that names an ID creates this link |
| parent_of | dev -> dev | child_of | yes | a deliverable or epic and its parts; at most one parent; a parent cannot be done before its children |
| supersedes | ticket -> ticket | superseded_by | yes | DST is replaced by SRC; prod must not curate DST |
| duplicates | dev -> dev | duplicated_by | yes | SRC repeats DST |
| answers | dev -> dev | answered_by | | SRC (a result) answers DST (a question) |
| implements | dev -> dev | implemented_by | | SRC realises DST (for example DLV-06 implements the course item CRS-04) |
| evidences | artifact or pointer -> dev | evidenced_by | | derived from each ticket's `evidence` list |
| produced_by | file -> file, run | produced | yes | a result file and the script or run that made it |
| published_at | ticket -> slack, url, project | publishes | | a Slack message about the ticket (written by `relay.py record`) |
| mirrors | slacklist record -> ticket | mirrored_by | | from `mirrors.json`, written when a Slack List is read |
| relates | anything -> anything | relates | | weak; a note saying why is required |
| mentions | doc -> ticket | mentioned_in | | computed by scanning reports, plans and READMEs for IDs |

## 4. Status of a prod row

Pass-through: the dev ticket's effective status. Group: from the effective statuses of the tickets it curates.

| Curated tickets | Group derives |
|---|---|
| any reopened | reopened |
| all done at their required evidence level | done |
| all done, some below the required level | done_needs_evidence |
| all open | open |
| some done or in progress (and not all done) | in progress |
| none started; every one that is not open is blocked | blocked |
| none started otherwise | to-do |

What prod may show (`PUBLISH`): ✅ only for done. A row that is done below its evidence bar, or reopened, shows 👀.
Evidence level of a group = the lowest level among its tickets. The "Checks" cell counts its tickets by status.

## 5. Binding times

| What | Bound when | By |
|---|---|---|
| dev ID | first `check` after it appears in `catalogue.py` | `ids.lock` |
| group ID | `prod-apply` / `prod-add`, with the next free number of its prefix | `ids.lock`, `prod.json` |
| which rows are in prod | Uzair's instruction, recorded in `prod_spec.json` and applied with `prod-apply` | `prod.json` |
| a link | `link`, `prod-apply`, `relay.py record`, or a catalogue edit followed by `check` | `links.txt`, `catalogue.py` |
| evidence hashes | first `verify.py` that sees the file; changed only by `--repin` | `pins.json` |
| effective status and level | every `verify.py` | `status.json` |
| what prod shows | `prod-publish`, after the Slack list was updated from `prod_rows.json` | `prod.json` history, `reviews.jsonl` |
| Slack record IDs | every `mirror` of a list export | `mirrors.json` |

## 6. Checks (`trace.py check`; exit code 1 on any error)

| Code | Severity | Fires when |
|---|---|---|
| T1 | error | a link names a node that does not resolve (missing catalogue evidence is a warning; `verify.py` handles it) |
| T2 | error | unknown relation, a relation between kinds it does not allow, or an unparseable line |
| T3 | error | a cycle in blocks, parent_of, supersedes, duplicates or produced_by |
| T4 | error | an issued ID vanished without `retire`; a retired ID is back; a dev ticket took an ID issued to a group |
| T5 | error | a group curates nothing |
| T6 | error | a prod row shows ✅ while its dev side is not done (prod over-claims) |
| T7 | error | malformed or duplicated ID; a group ID that is also a dev ticket; a pass-through row that is not a dev ticket |
| T8 | error | a ticket with more than one parent |
| T10 | error | `status.json` disagrees with `catalogue.py` (run `verify.py` first) |
| W1 | warning | a published prod row is suspect: a ticket behind it changed since it was last published or reviewed |
| W2 | warning | the prod list is out of date: it shows a different status from the one the dev side now gives |
| W3 | warning | in progress or done while a blocker is unfinished; or blocked when every blocker is done |
| W4 | warning | a parent is done while a child is not |
| W5 | warning | a doc mentions an ID that does not exist |
| W6 | warning | a prod row curates a superseded or duplicate ticket |
| W7 | warning | `relates` without a note |
| W9 | warning | a prod row is missing from the Slack list CD Tracker (once that list has been mirrored) |
| W10 | warning | the same link written twice |
| R1-R5 | warning | relay problems: see `RELAY.md` |

`selftest_trace.py` injects one failure of each kind into a throwaway copy and confirms the code above fires (40 cases).

## 7. Failure modes this design closes

| Failure | Closed by |
|---|---|
| Prod shows ✅ while the dev work behind it regressed | statuses are derived, never typed; T6 on every check; `prod-set` refuses ✅ unless dev is done |
| Dev evidence changes after a prod row was published | the ticket reopens (README rule 2); the prod row turns suspect (W1) and out of date (W2) until the list is re-synced |
| A group ID collides with a later dev ticket | group IDs are locked as prod IDs (T4); `next-id` counts both lists |
| A ticket is renamed, renumbered or deleted and links break | IDs are immutable (`ids.lock`, T4); titles are free to change |
| A link points at nothing | `link` refuses it; T1 at check time |
| Slack shows something the files do not | `mirror` compares each list's export with the files |
| A Slack message claims more than the files | `relay.py` writes messages from the files; R2 when an announced ✅ reopens |
| An artifact in Slack is older than the file | its hash is logged at posting; R1 when the file changes |
| A summary point that cites nothing | `relay.py` refuses points that name no ticket (and, in prod, no prod row) |
| Status computed from an old verification | T10 |

## 8. Commands

    python tracker/verify.py                                   # evidence first, always
    python tracker/trace.py check                              # every rule above; writes trace.md, trace.json, ids.lock
    python tracker/trace.py show AUD-16                        # one row or ticket with everything linked to it
    python tracker/trace.py next-id REP                        # next number free in both lists
    python tracker/trace.py link DLV-04 parent_of CAP-06       # typed link, validated before it is written
    python tracker/trace.py prod-apply tracker/prod_spec.json  # Uzair's curation, idempotent
    python tracker/trace.py list-diff dev|prod                 # cells that changed since the last sync -> list_updates_<list>.json
    python tracker/trace.py list-synced dev|prod               # after pushing those updates to Slack
    python tracker/trace.py mirror export.csv --list prod      # Slack export against the files; records record IDs
    python tracker/trace.py prod-publish --note "synced"       # the list now shows the derived statuses
    python tracker/trace.py slack-links                        # Links cells for the Dev CD Tracker list
    python tracker/selftest_trace.py                           # the checks themselves still work

Slack List columns added through the API get an internal key made from their display name. A key that collides with a
reserved field (`id` did) breaks the list in the Slack app. Add such a column under a distinct name, then rename it.
