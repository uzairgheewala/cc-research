# Site v3 patches s24-s28: how to apply (TEAM-10, TEAM-11, TEAM-12)

Tickets: TEAM-10, TEAM-11, TEAM-12. Built 20 Oct in the site chat (wave B, parallel part). Design: project docs
claude/site-v3-design-2026-10-20.md and claude/site-v3-wave-b-plan-2026-10-20.md; results claude/site-v3-build-2026-10-20.md.

## When
After sheet A's `return_A.zip` is packed (the patches edit files in `jobs/waves/A/identity.sha256`). They need p25 and the
S23 site patch (both in the wave A kit, already on disk). Order between them and p26-p29 does not matter: each appends its
own block or edits its own anchor, and refuses with a clear message if an anchor moved.

## Apply (PowerShell, in cc-research)
    py -3 jobs\patches\s24.py
    py -3 jobs\patches\s25.py
    py -3 jobs\patches\s26.py
    py -3 jobs\patches\s27.py
    py -3 jobs\patches\s28.py
Each prints "sNN applied"; a second run refuses ("already applied"). s25-s27 refuse without s24; s28 stands alone.
Rehearsed in the sandbox on a copy matching identity.sha256, in three orders, and after simulated p26-style appends.

## Then (the usual pre-commit sequence, plus two repins)
    py -3 tracker\verify.py                      # TEAM-10..12 enter status.json
    py -3 tracker\verify.py --repin TEAM-08 TEAM-09   # reason: s24-s28 changed site/build.py, pages.py, registry.py,
                                                      # pg_changes.py and tracker/snapshot.py, which these tickets pin
    py -3 tracker\trace.py check
    py -3 tracker\snapshot.py
    py -3 -m unittest tests.test_site_v3 tests.test_site_s23
    py -3 site\build.py

## Must show
1. snapshot: 0 metric errors.
2. build: 0 errors, 0 warnings; pages to re-read: index, theses, gaps, status, explore (theses and status were already on
   the list from S23). An INFO line names BEN-14 until B4 adds it.
3. tests: test_site_v3 (19 tests) and test_site_s23 pass.
4. site/_build/explore.json exists and its sha256 starts with the 12 characters printed on the explore page.
5. Today (index.html): 600 words or fewer; 2 of 5 landmarks met for the paper and for the product; 3 of 4 open landmarks
   short only on test cases; next deliverable 29 Oct.
6. changes.html shows prod digests only (newest 15 Oct while the drafts stay unsent) and the count of dev updates since.

## If the explanation ledger (B1) is in place
`analysis/results/q2_v3/explain_ledger_dev.json` is registered automatically. Its rows must use a board name in
gaps_spec.json's lists (semantic / causalarena-semantic / causalarena_semantic, and the formula equivalents) and a gap name
in missed / missed_links, false / false_links, reversed / reversals; anything else fails the build with the unmapped rows
listed (fix by adding the alias to site/gaps_spec.json, a data file). Each gap's segments must sum to the anatomy total.
S29 sets `rules.explain_ledger.required` to true once it is in.

## After reading the pages
    py -3 site\build.py --mark-reviewed index gaps explore
(theses and status are reviewed in S29, the prose sync.)
