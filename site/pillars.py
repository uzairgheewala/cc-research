"""Which pillar each tracker item belongs to. Explicit, so the counts on the site can be re-derived by hand.

P1 Measurement : where each system's direction comes from and how far it is from the limit (audits, replication,
                 benchmarks, evaluation protocol, comparison targets, the runs of the unmodified agent).
P2 Claim ledger: our system for rungs 1-2 in the knowledge columns (capabilities, build, system targets, the
                 knowledge-elicitation predictions, the refinement deliverable).
P3 Decisions   : effects and experiments (rungs 3-4).
spine          : course, team, infrastructure, risks, decisions, bundles, delivery packages. Not a pillar.
"""
P1_PREFIX = ("REP", "AUD", "BEN", "EVL", "DOM")
P2 = {"CAP-%02d" % i for i in range(1, 15)} | {"CAP-18", "BLD-02", "BLD-03", "BLD-04", "BLD-05", "BLD-06", "BLD-09",
                                                "TGT-07", "TGT-09", "TGT-10", "TGT-11", "TGT-12", "TGT-13", "TGT-14",
                                                "RQ-06", "RQ-07", "RQ-10", "RQ-11", "RQ-12", "RQ-13", "RQ-14",
                                                "DLV-04", "DOM-08", "STR-04"}
P3 = {"CAP-15", "CAP-16", "BLD-07", "BLD-08", "TGT-15", "TGT-16", "RQ-08", "RQ-09", "DOM-09", "DOM-10", "STR-03"}
P1_EXTRA = {"RQ-01", "RQ-02", "RQ-03", "RQ-04", "RQ-05", "RQ-15", "RQ-16", "RQ-17",
            "TGT-01", "TGT-02", "TGT-03", "TGT-04", "TGT-05", "TGT-06", "TGT-08",
            "DLV-01", "DLV-02", "DLV-03", "EXT-01", "EXT-03", "STR-01", "CAP-17"}


def pillar(item_id):
    if item_id in P2:
        return "P2"
    if item_id in P3:
        return "P3"
    if item_id in P1_EXTRA or item_id.split("-")[0] in P1_PREFIX:
        return "P1"
    return "spine"
