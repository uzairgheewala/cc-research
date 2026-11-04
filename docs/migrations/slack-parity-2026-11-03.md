# Live Slack parity after repository publication

Tickets: BLD-11, INF-06, TEAM-08, TEAM-11, DLV-05, DLV-06.

All 259 dev and 67 production row identities and statuses were read and compared
against generated local rows on 3 Nov Pacific time. All shared production fields
match. No row was added/removed and no Slack status was manually changed.

The substantive AUD-12 note discrepancy was corrected in dev. The source records
that both bidirected and circle-to-arrow marks are treated as parents. An initial
unescaped rich-text write returned success but did not preserve the complete
notation; the escaped write read back with the intended text. The verified date
was updated alongside that meaningful field change. Literal &, < and > must be
escaped on Slack's rich-text wire surface; see the rule in AGENTS.md and
https://docs.slack.dev/messaging/formatting-message-text/#escaping-text .

Two presentation differences are intentionally accepted: BLD-05 spacing around
an inequality, and INF-03's readable '8 datasets extracted' check summary instead
of the local truncated JSON rendering. Neither changes a status or scientific
claim. Fresh verification dates use the tracker's UTC convention. Under the
existing trace.py policy, Verified is sent only alongside another changed field;
older Slack dates alone do not trigger mass writes. The live comparison records
that expected lag separately from content/status parity.

The production October digest is now recorded at its actual sent timestamp with
connector-observed text and preserved original draft bytes. The dev digest was
already correctly recorded. No digest was reposted. Uzair chose to keep the new
publication announcements as drafts. Both were saved in Slack's Drafts & Sent
for their respective channels and recorded locally with draft_only=true and no
delivery timestamp or published_at link. No channel announcement was sent by the agent. Uzair subsequently sent both
messages manually. Fresh readback confirms production at 1793751394.325679
and dev at 1793751438.010819. Production omits the final checkpoint/funding
bullet; dev retains it. The observed bodies, original draft bytes and actual
delivery receipts are recorded without reposting either announcement.

The mirror export now writes deterministic LF newlines on Windows as well as
Unix. This removes platform-only changes to the generated row JSON without
altering field meanings, row selection or status derivation. The BLD-11 repin
and explicit review accept this formatting change and the updated namespace/
readback instructions; no new scientific or course deliverable is closed.

The local migration receipts retain fresh CSV pages, the exact targeted write
and readback, comparison categories and original-history backups. The public
tracker remains the source of truth for claims/status; a successful API response
alone is never a delivery or content-preservation receipt.
