# Trace check (2026-10-13T19:53:50Z)

status.json verified 2026-10-13T19:50:06Z. Dev tickets 220; prod rows 67 (7 groups, 60 pass-through). IDs newly locked: 0.

## Links

| relation | source | count |
|---|---|---|
| blocks | catalogue | 2 |
| blocks | links.txt | 1 |
| blocks | plan | 25 |
| curates | links.txt | 66 |
| evidences | catalogue | 507 |
| implements | links.txt | 2 |
| implements | plan | 52 |
| mentions | scan | 400 |
| mirrors | mirrors.json | 287 |
| parent_of | links.txt | 23 |
| published_at | links.txt | 149 |
| relates | links.txt | 1 |

## Findings: 0 errors, 4 warnings

- **WARN W1** DLV-02 is suspect: ['DLV-02'] changed since it was last published or reviewed (2026-10-12T10:12)
- **WARN W1** EVL-01 is suspect: ['EVL-01'] changed since it was last published or reviewed (2026-10-12T10:12)
- **WARN W1** EVL-02 is suspect: ['EVL-02'] changed since it was last published or reviewed (2026-10-12T10:12)
- **WARN W1** EVL-03 is suspect: ['EVL-03'] changed since it was last published or reviewed (2026-10-12T10:12)

## Prod rows

| ID | type | published | derived | min level | suspect | curates |
|---|---|---|---|---|---|---|
| DLV-01 | passthrough | done | done | V3 | - | DLV-01 |
| DLV-02 | passthrough | in_progress | in_progress | V3 | DLV-02 | DLV-02 |
| DLV-03 | passthrough | in_progress | in_progress | V2 | - | DLV-03 |
| DLV-04 | passthrough | todo | todo | V0 | - | DLV-04 |
| DLV-05 | passthrough | todo | todo | V0 | - | DLV-05 |
| DLV-06 | passthrough | todo | todo | V0 | - | DLV-06 |
| REP-09 | passthrough | done | done | V3 | - | REP-09 |
| REP-14 | group | in_progress | in_progress | V2 | - | REP-01, REP-02, REP-03, REP-04, REP-11, REP-12, REP-13 |
| REP-15 | group | in_progress | in_progress | V3 | - | REP-05, REP-06, REP-07, REP-08 |
| DOM-13 | group | in_progress | in_progress | V2 | - | DOM-02, DOM-03, DOM-04, DOM-05, DOM-06, DOM-07 |
| DOM-14 | group | done | done | V3 | - | DOM-01, DOM-08, DOM-09, DOM-10, DOM-11, DOM-12 |
| AUD-16 | group | done | done | V3 | - | AUD-01, AUD-02, AUD-03, AUD-04, AUD-05, AUD-06, AUD-07, AUD-08, AUD-09 |
| AUD-17 | group | in_progress | in_progress | V0 | - | AUD-10, AUD-11, AUD-12, AUD-13, AUD-14, AUD-15, BEN-01, BEN-02, BEN-03, BEN-04, BEN-05, BEN-06, BEN-07, BEN-08, BEN-09, BEN-10, BEN-11, BEN-12 |
| TGT-17 | group | in_progress | in_progress | V0 | - | TGT-01, TGT-02, TGT-03, TGT-04, TGT-05, TGT-06, TGT-07, TGT-08, TGT-09, TGT-10, TGT-11, TGT-12, TGT-13, TGT-14, TGT-15, TGT-16 |
| CAP-01 | passthrough | todo | todo | V0 | - | CAP-01 |
| CAP-02 | passthrough | todo | todo | V0 | - | CAP-02 |
| CAP-03 | passthrough | todo | todo | V0 | - | CAP-03 |
| CAP-04 | passthrough | todo | todo | V0 | - | CAP-04 |
| CAP-05 | passthrough | todo | todo | V0 | - | CAP-05 |
| CAP-06 | passthrough | done | done | V3 | - | CAP-06 |
| CAP-07 | passthrough | todo | todo | V0 | - | CAP-07 |
| CAP-08 | passthrough | todo | todo | V0 | - | CAP-08 |
| CAP-09 | passthrough | todo | todo | V0 | - | CAP-09 |
| CAP-10 | passthrough | in_progress | in_progress | V3 | - | CAP-10 |
| CAP-11 | passthrough | todo | todo | V0 | - | CAP-11 |
| CAP-12 | passthrough | todo | todo | V0 | - | CAP-12 |
| CAP-13 | passthrough | todo | todo | V0 | - | CAP-13 |
| CAP-14 | passthrough | todo | todo | V0 | - | CAP-14 |
| CAP-15 | passthrough | todo | todo | V0 | - | CAP-15 |
| CAP-16 | passthrough | todo | todo | V0 | - | CAP-16 |
| CAP-17 | passthrough | done | done | V3 | - | CAP-17 |
| CAP-18 | passthrough | todo | todo | V0 | - | CAP-18 |
| RQ-01 | passthrough | done | done | V3 | - | RQ-01 |
| RQ-02 | passthrough | done | done | V3 | - | RQ-02 |
| RQ-03 | passthrough | done | done | V3 | - | RQ-03 |
| RQ-04 | passthrough | open | open | V2 | - | RQ-04 |
| RQ-05 | passthrough | open | open | V2 | - | RQ-05 |
| RQ-06 | passthrough | open | open | V2 | - | RQ-06 |
| RQ-07 | passthrough | open | open | V2 | - | RQ-07 |
| RQ-08 | passthrough | open | open | V2 | - | RQ-08 |
| RQ-09 | passthrough | open | open | V2 | - | RQ-09 |
| RQ-10 | passthrough | done | done | V3 | - | RQ-10 |
| RQ-11 | passthrough | done | done | V3 | - | RQ-11 |
| RQ-12 | passthrough | done | done | V3 | - | RQ-12 |
| RQ-13 | passthrough | done | done | V3 | - | RQ-13 |
| RQ-14 | passthrough | done | done | V3 | - | RQ-14 |
| RQ-15 | passthrough | open | open | V0 | - | RQ-15 |
| RQ-16 | passthrough | done | done | V3 | - | RQ-16 |
| RQ-17 | passthrough | open | open | V0 | - | RQ-17 |
| BLD-01 | passthrough | done | done | V3 | - | BLD-01 |
| BLD-02 | passthrough | todo | todo | V0 | - | BLD-02 |
| BLD-03 | passthrough | todo | todo | V0 | - | BLD-03 |
| BLD-04 | passthrough | todo | todo | V0 | - | BLD-04 |
| BLD-05 | passthrough | todo | todo | V0 | - | BLD-05 |
| BLD-06 | passthrough | in_progress | in_progress | V3 | - | BLD-06 |
| BLD-07 | passthrough | todo | todo | V0 | - | BLD-07 |
| BLD-08 | passthrough | todo | todo | V0 | - | BLD-08 |
| BLD-09 | passthrough | todo | todo | V0 | - | BLD-09 |
| BLD-10 | passthrough | done | done | V3 | - | BLD-10 |
| BLD-11 | passthrough | done | done | V3 | - | BLD-11 |
| EVL-01 | passthrough | done | done | V3 | EVL-01 | EVL-01 |
| EVL-02 | passthrough | done | done | V3 | EVL-02 | EVL-02 |
| EVL-03 | passthrough | done | done | V3 | EVL-03 | EVL-03 |
| EVL-04 | passthrough | done | done | V3 | - | EVL-04 |
| EVL-05 | passthrough | done | done | V3 | - | EVL-05 |
| EVL-06 | passthrough | done | done | V3 | - | EVL-06 |
| EVL-07 | passthrough | done | done | V3 | - | EVL-07 |

## Dev tickets in no prod row (94)

AUD-18, AUD-19, AUD-20, AUD-21, AUD-22, AUD-23, AUD-24, AUD-25, AUD-26, AUD-27, AUD-28, AUD-29, AUD-30, AUD-31, AUD-32, AUD-33, AUD-34, AUD-35, AUD-36, AUD-37, AUD-38, AUD-39, AUD-40, AUD-41, AUD-42, AUD-43, AUD-44, AUD-45, AUD-46, AUD-47, AUD-48, BLD-12, BLD-13, BLD-14, BND-01, BND-02, BND-03, BND-04, BND-05, BND-06, BND-07, BND-08, BND-09, BND-10, BND-11, BND-12, BND-13, BND-14, CRS-01, CRS-02, CRS-03, CRS-04, CRS-05, CRS-06, CRS-07, DEC-01, DEC-02, DEC-03, DEC-04, DEC-05, EXT-01, EXT-02, EXT-03, EXT-04, EXT-05, INF-01, INF-02, INF-03, INF-04, INF-05, INF-06, INF-07, REP-10, RSK-01, RSK-02, RSK-03, RSK-04, RSK-05, RSK-06, RSK-07, RSK-08, STR-01, STR-02, STR-03, STR-04, STR-05, STR-06, TEAM-01, TEAM-02, TEAM-03, TEAM-04, TEAM-05, TEAM-06, TEAM-07
