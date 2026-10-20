"""2026-10-20, wave A: the tracker side of the wave's build. Refuses to run twice; apply p24 first.

INF-10 wave runner built (in progress until the demo sheet runs on Uzair's machine); BEN-13 S0-S2 built and
pre-registered (in progress); TGT-18 / TGT-19 gain the explanation round X1-X3 and the family-2 amendment; INF-06 gains
the fork branches (patches, branch identity in the harness); REP-07 / BEN-07 gain the X5 pre-registration; TEAM-09 records
site bundle S23 (the drift detector).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "tracker" / "catalogue.py"
c = p.read_text(encoding="utf-8")
assert "# ---- overrides p24" in c, "apply p24 first"
assert "# ---- overrides p25" not in c, "already applied"
c = c.rstrip("\n") + '''

# ---- overrides p25 (2026-10-20): wave A build
_W = {
    "INF-10": ["harness/wave.py", "tests/test_wave_runner.py", "docker/Dockerfile.kernel", "docker/requirements_kernel.txt",
               "analysis/wave_canary.py", "jobs/waves/A/plan.md", "jobs/waves/A/sheet.json", "jobs/waves/A/canary_expected.json",
               "harness/live_capped.py"],
    "BEN-13": ["plans/ben13_prereg.json", "manifests/evidence/explain_ben13_prereg_2026-10-20.sha256",
               "analysis/ben13/stream_preprocess.py", "analysis/ben13/run.py", "analysis/ben13/methods.py",
               "analysis/ben13/evaluate.py", "analysis/ben13/literature.py", "analysis/ben13/fetch.py", "analysis/ben13/synth.py",
               "tests/test_ben13_stream.py", "docker/Dockerfile.bench", "docker/requirements_bench.txt"],
    "TGT-18": ["plans/q2_explain_prereg.json", "analysis/q2_explain.py", "analysis/reports/q2_explain_dev.md",
               "analysis/results/q2_v3/explain_dev.json", "manifests/evidence/explain_x123_results_2026-10-20.sha256",
               "plans/v3_prereg_amendment_1_family2.json", "manifests/evidence/family2_prereg_2026-10-20.sha256",
               "analysis/q2_family2.py"],
    "TGT-19": ["analysis/reports/q2_explain_dev.md", "analysis/results/q2_v3/explain_dev.json"],
    "INF-06": ["docs/FORK.md", "harness/fork_branch.py", "jobs/fork/bld-06-refinement-v2.json", "jobs/fork/ext-03-cycle-step-key.json",
               "jobs/fork/bld-06-refinement-v2.patch", "jobs/fork/ext-03-cycle-step-key.patch", "jobs/fork/make_branches.ps1",
               "tests/test_fork_patches.py", "analysis/fork_check.py"],
    "REP-07": ["plans/x5_prereg.json", "manifests/evidence/x5_prereg_2026-10-20.sha256", "analysis/x5_pretrained.py",
               "docker/Dockerfile.x5", "docker/requirements_x5.txt"],
    "BEN-07": ["plans/x5_prereg.json"],
    "EXT-03": ["jobs/fork/ext-03-cycle-step-key.patch"],
}
_N = {
    "INF-10": (" 20 Oct (wave A): harness/wave.py built (preflight with code identity, disk, Docker memory and the CPU's BLAS "
               "family; canaries; when-gates over must-shows; resume; parts and memory packing; verdict.json and a small return "
               "zip); tests/test_wave_runner.py passes. Must-show still open: the demo sheet on Uzair's machine (wave A sheet, run "
               "A0)."),
    "BEN-13": (" 20 Oct (wave A): S0-S2 built and pre-registered (plans/ben13_prereg.json). CausalBench's preprocessing is "
               "streamed in row chunks (peak about 0.5 GB instead of about 30 GB) and equals causalbench 1.1.2's arrays bit for bit "
               "on synthetic files; evaluation through causalbench's own classes (all-path tests skipped, checked equal by a canary "
               "cell). Names-only LLM arm not run (decision D-3 = no): the names channel is measured with literature networks and "
               "gene-label permutations."),
    "TGT-18": (" 20 Oct (wave A, dev): explanation round X1-X3 (analysis/reports/q2_explain_dev.md). Both semantic gaps come "
               "from a linear-Gaussian score on nonlinear / discrete mechanisms: given the true graph the score still wants 78% of "
               "shadow links and 76% of the missed search-gap links, while GES's graph outscores the true graph on 117 of 120 "
               "files. Pre-registered rule: D2-search; read with the global check, the lever is the score (post-hoc reading, "
               "labelled). Floor confirmed real (X3). Second held-out family pre-registered (plans/v3_prereg_amendment_1_family2.json)."),
    "TGT-19": (" 20 Oct (wave A, dev): X2, semantic reversals are 49% skeleton-caused, 38% rule-caused, 13% left open on the "
               "true skeleton (formula 62 / 29 / 9) (analysis/reports/q2_explain_dev.md)."),
    "INF-06": (" 20 Oct (wave A): ticket branches of the fork as patch files (jobs/fork/), applied by Uzair with "
               "jobs/fork/make_branches.ps1; the harness checks a branch run (CC_BRANCH) against jobs/fork/<branch>.json and records "
               "branch, commit and patch in meta.json. The fork itself is a manual step (docs/FORK.md)."),
    "REP-07": (" 20 Oct (wave A): X5 pre-registered (plans/x5_prereg.json): AVICI scm-v0 on CausalArena dev, columns shuffled, "
               "beside GES and v3. FoundCause / CDFM weights not located."),
    "BEN-07": " 20 Oct: X5 tests AVICI's column-order sensitivity (original vs shuffled) on dev (plans/x5_prereg.json).",
    "EXT-03": (" 20 Oct: fix written as branch ext-03-cycle-step-key (jobs/fork/ext-03-cycle-step-key.patch); stub run on "
               "the wave A sheet."),
}
for _i in ITEMS:
    if _i["id"] in _W:
        _i["evidence"] = list(_i["evidence"]) + [e for e in _W[_i["id"]] if e not in _i["evidence"]]
    if _i["id"] in _N:
        _i["note"] = (_i.get("note") or "") + _N[_i["id"]]
    if _i["id"] in ("INF-10", "BEN-13", "INF-06") and _i["status"] == "todo":
        _i["status"] = "in_progress"
for _i in ITEMS:   # the harness gained branch identity (INF-06): tool manifest re-taken; the 10-14 manifest stays as history
    if _i["id"] == "BLD-01":
        _i["evidence"] = ["manifests/evidence/BLD-01_tools_2026-10-20.sha256" if e == "manifests/evidence/BLD-01_tools_2026-10-14.sha256" else e
                          for e in _i["evidence"]]
        _i["checks"] = [dict(ck, path="manifests/evidence/BLD-01_tools_2026-10-20.sha256")
                        if ck.get("t") == "manifest" and ck.get("path") == "manifests/evidence/BLD-01_tools_2026-10-14.sha256" else ck
                        for ck in _i["checks"]]
        _i["note"] = (_i.get("note") or "") + " Tool manifest re-taken 2026-10-20: cc_common.py and run_traced.py learned ticket-branch runs (CC_BRANCH, INF-06)."
ITEMS.append(item("TEAM-09", "TEAM", "Site drift detector (S23): Q2 bindings, evidence-aware re-read, superseded reads, guarded literals",
                  "done", kind="task",
                  criterion=("Pages bind Q2 tickets; the re-read fingerprint is status + evidence count + note hash; a registry number "
                             "from a superseded read prints only when marked historic; hand-written status sentences carry a guard that "
                             "fails the build once their ticket moves on; unit tests"),
                  evidence=["site/build.py", "site/pages.py", "site/registry.py", "site/literals.json", "site/levels/bundles.py",
                            "site/levels/theses.py", "tests/test_site_s23.py", "tracker/snapshot.py"],
                  note=("From the 19 Oct drift audit (project:claude/site-drift-audit-2026-10-19.md, bundle S23). The first build "
                        "after it lists home, status and theses as pages to re-read: the drift the audit found.")))
'''
p.write_text(c + "\n", encoding="utf-8")
print("p25 applied")
