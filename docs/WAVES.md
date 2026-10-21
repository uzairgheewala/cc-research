# How work is batched here: waves (adopted 19 Oct 2026)

Tickets: INF-10

The generic method is the `batched-waves` skill (proposed 19 Oct). This file is how it maps onto cc-research. AGENTS.md
points here; every agent working in this folder follows it.

## Classes, as they exist in this folder

| Class | Where it runs here |
|---|---|
| F free | the agent's sandbox (cloud container or the device shell), from the wave kit; under about 10 minutes |
| H heavy | Uzair's machine: `cc.ps1 wave <id>` (harness/wave.py on the host's Python; jobs in the kernel, bench or X5 images, no network except download jobs) |
| L live | Uzair's machine, his OpenAI key, inside the same sheet, gated and capped (`cc.ps1 plan` jobs) |
| M manual | Uzair: GitHub (the fork), git commits and pushes, downloads from hosts the sandboxes cannot reach (figshare, huggingface.co), sending prod messages |
| D decision | Uzair, with defaults |

## Files

| Path | What |
|---|---|
| `WAVE_STATE.md` | the one file a new session reads first: current wave, frontier, outstanding sheet, pending decisions, defaults taken |
| `jobs/waves/<wave>/sheet.json` | the run sheet (format: `harness/wave.py`): runs with class, profile (host or a Docker image), command, `when` gate, `done` test (resume), parts and memory, cost cap; must-shows with bars; the decision table; the identity manifest hash |
| `jobs/waves/<wave>/verdict.json`, `state.json` | rewritten after every run: per run status, exit, wall time, cost; must-shows scored pass / fail / not run; decisions matched; host, preflight (disk, Docker memory, BLAS family) |
| `jobs/waves/<wave>/return_<wave>.zip` | what comes back (`cc.ps1 wave <id>` packs it at the end): verdict, state, the sheet's small result files, the last 4 KB of each log |
| `jobs/transfer/wave_<id>_kit.tgz` | the code and data the agent's sandbox needs for a wave, built by the device shell |
| `jobs/transfer/cache_engines_<date>.tgz` | the engine cache (500 entries are 15 MB): shipped every wave, never rebuilt in the sandbox |

## The loop here

1. Intake: `verdict.json` first, then result files by path only when a rule asks; identity check against the kit's manifest; score the pre-registered
   predictions the returns decide.
2. Frontier: `tracker/trace.py` blockers plus the wave plan below.
3. Build: design note, pre-registration hashed in `manifests/evidence/`, code, tests, smoke on a slice, the sheet.
4. Pack: one sheet; one kit applied on device by one patch script; tests, `verify.py`, `trace.py check`, `snapshot.py`,
   `secret_scan.py`, `ci_check.py`, `site/build.py` once, at the end; one commit message in `docs/commit_msgs/`.
   Any `verify.py --repin` or catalogue patch made after that (e.g. during intake) is followed by `snapshot.py` again, and
   the commit message lists `site/snapshot.json` (AGENTS.md, Repository).
5. Hand over: one message; Slack dev digest once per wave.
6. Stop.

## Lessons that produced this (19 Oct)

- The L16 / L5 round rebuilt the engine cache in a fresh sandbox (about 40 minutes of session time) although the cache
  is 15 MB. Now it ships with the kit.
- A test run on the device shell (Python 3.10, NumPy 2, no SciPy) overwrote `tests/last_run.json` with a failing record;
  tests run once per kit in the pinned environment (Python 3.11, `engines/MANIFEST.json` pins).
- Checks were run several times per round; now once per kit.

## Runner (built in wave A, 20 Oct)

    powershell -ExecutionPolicy Bypass -File .\cc.ps1 wave A 2          # 2 workers; memory budget 70% of Docker's
    powershell -ExecutionPolicy Bypass -File .\cc.ps1 wavepack A        # repack only (the wave command packs at the end)

`harness/wave.py` refuses a sheet whose code identity differs from the files on the machine, checks disk and Docker
memory, reads the CPU's BLAS family (no AVX-512: OpenBLAS runs as HASWELL and the canary says whether results still match
the agent's), starts static checks first, then cheap runs, then heavy and live ones, each only when its `when` condition
holds over earlier must-shows. Running it again resumes: a run whose done test passes is not started again.
The names in the batched-waves skill (`RETURN.json`) map to `verdict.json` here.
