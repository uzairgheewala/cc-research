"""Read-only stage and BND-08 endpoint replay for the Q1 checkpoint (DLV-07)."""
from dataclasses import replace
import json

from crucis_causal.controls.effects import binom_q95
from crucis_causal.docs.checks.rebase_facts import stages
from crucis_causal.findings import k11_counts
from crucis_causal.rerun.existing import Cache, NAME_ARMS


def endpoints():
    _, battery, records, _ = Cache().get("causal_copilot", "q1s2", NAME_ARMS, source="bnd08")
    pre_cycle = ["S1", "S2", "S3"]
    # Project eligible swapped records onto S3 so a later crash does not remove
    # a usable graph from the pre-cycle diagnostic. Original statuses stay intact.
    reached = [
        replace(record, status="ok", graph=record.variants["S3"])
        for record in records
        if record.arm == "swapped" and all(stage in record.variants for stage in pre_cycle)
    ]
    stage_sets = {
        "pre_cycle_all": (pre_cycle, reached),
        "pre_cycle_completed": (
            pre_cycle, [record for record in records if record.status == "ok" and "S4" in record.variants],
        ),
        "final_completed": ([*pre_cycle, "S4"], records),
    }
    out = {}
    for label, (stage_names, group) in stage_sets.items():
        counts = k11_counts(group, battery, stage_names, 1)
        counts["q95_data_only"] = binom_q95(counts["n"])
        counts["swapped_runs"] = sum(
            record.arm == "swapped" and record.status == "ok"
            and all(stage in record.variants for stage in stage_names)
            for record in group
        )
        out[label] = counts
    return out


if __name__ == "__main__":
    print(json.dumps({"stages": stages(), "bnd08_endpoints": endpoints()}, indent=2))
