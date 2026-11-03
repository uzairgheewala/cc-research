# Publication lifecycle and research-site reconciliation

Tickets: INF-06, BLD-11, TEAM-08, TEAM-09, TEAM-11, DLV-05, DLV-07.

Uzair approved Apache-2.0, qualified distribution/import/command names, a backed-up
cleanup of eight unpublished Crucis planning files, and publication on 3 Nov.
Crucis is public at https://github.com/crucis-lab/crucis. The distribution/command
is crucis-causal; Python imports use crucis_causal. Original extraction targets
and hashes remain historical; Crucis provenance/publication.json records the
path translation and cleaned-history mapping.

The first remote package run passed on Linux/Python 3.10 and 3.12 and Windows/3.12:
https://github.com/crucis-lab/crucis/actions/runs/41740797633 . The initial
documentation workflow is gated on those same-commit checks. No package-index
release, newly completed scientific campaign or protocol adoption is implied.

The research landing page now identifies the independent auditor, its validation
and the proposed multi-system study, with the earlier ledger landmarks explicitly
historical and the refinement reproduction labeled as a companion study. Existing
numerical registry entries and frozen paper sources remain unchanged. The
checkpoint prose/citation/PDF corrections and mentor review remain outstanding.

Research Pages now downloads the artifact from a successful full ci run on main,
checks its repository identity and records that run's exact source commit. It no
longer starts an independent weaker build in parallel with full CI. Remote CI
also runs the frozen checkpoint/number-source checks and manuscript lint using
only the two hash-pinned public metadata fixtures.

The October production digest was already sent at Slack timestamp
1793412937.228969. Its local draft was reconciled using the connector-observed
delivered text, with the original prepared JSON preserved byte-for-byte under
slack-prepared-originals/. The capture basis is explicit: rendered connector text
is not a native Slack API byte export. The existing record command appended its
delivery receipt and typed ticket links; no message was reposted. The dev digest
was already correctly recorded at 1793412474.583979.

The deliberate TEAM-08/09 repins accept the companion page-label change in
site/pages.py; their page routing and drift-detection behavior are preserved.
The TEAM-11 repin accepts the reviewed current research framing in pg_today.py.
These changes do not close TEAM-11 or any Q1 deliverable. Verification retains
151 done, zero reopened/problem items; trace reports zero errors/warnings. The
snapshot was regenerated after the final verification. Remaining historical
page re-read flags are visible rather than silently marked reviewed.

Local milestone commits remain automatic and independent of GitHub or Slack
availability. Publication and delivery retain separate commit/run/URL receipts.
New production Slack updates remain draft-first; no new announcement was sent by
this reconciliation. The private mentor brief and funding records stay outside
the public framework repository.
