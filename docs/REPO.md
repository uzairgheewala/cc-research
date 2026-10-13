# The cc-research repository

Tickets: INF-06, INF-07, BLD-10, BLD-11

What goes in git, what stays out, how CI keeps the evidence honest, and how the site is published.

## Layout

| Path | In git | What |
|---|---|---|
| `analysis/` | yes | analysis code, `results/` (JSON, CSV, small NPZ), `reports/`, `literature/` |
| `tracker/` | yes | tickets (`catalogue.py`), evidence pins, status, Slack list rows, relay, `snapshot.py` |
| `site/` | yes | the Causal Atlas: `registry.py` (every number and its file), `pillars.py`, `levels/`, `build.py`, `snapshot.json` |
| `plans/`, `jobs/` (minus `jobs/transfer/`), `harness/`, `docker/`, `datasets/`, `tests/`, `manifests/`, `docs/`, `preflight/` | yes | as described in `AGENTS.md` |
| `tools/` | yes | `secret_scan.py`, `ci_check.py`, `data_manifest.py`, `hooks/pre-commit` |
| `.github/workflows/` | yes | `ci.yml` (every push), `pages.yml` (publish the site from `main`) |
| `external/` | **no** | downloaded benchmarks (CausalArena about 1.6 GB, Causal Chambers about 0.8 GB). Listed with sha256 in `manifests/excluded/external.sha256` |
| `runs/` | **no** | recorded Causal-Copilot runs. Listed in `manifests/excluded/runs.sha256`; archived as release assets (below) |
| `jobs/transfer/` | **no** | scratch tarballs used to move files between machines |
| `queue/`, caches, `directory_structure.txt` | **no** | runtime state and generated listings |

Credentials are never in this folder. `.gitignore` also blocks `.env*`, `*.pem`, `*.key`, `*secret*` and `*.zip`
(the methodology zip with a Jupyter token lives outside this folder and must stay out).

## Why `* -text` in `.gitattributes`

Every evidence file is pinned by the sha256 of its bytes (`tracker/pins.json`, `manifests/**/*.sha256`). Git for Windows
converts line endings by default, which would change those bytes on checkout and break every pin. `* -text` turns all
conversion off: the bytes in git are the bytes on disk, on Windows and in CI.

## What CI checks (`.github/workflows/ci.yml`)

1. `tools/secret_scan.py`: no key, token or private-key block in any tracked file; no file over 50 MB.
2. `tracker/snapshot.py --check`: the committed `site/snapshot.json` equals what the committed files produce.
3. `tools/ci_check.py`: every evidence file the tracker pins and that lives in git still has its pinned hash; evidence
   outside git must appear in `manifests/excluded/`.
4. `tests/run_tests.py`: unit tests (the one test that needs `external/` is skipped in CI).
5. `tracker/trace.py check`: tickets, links and prod rows are consistent (zero errors).
6. `site/build.py`: the site builds, every printed number resolves in the snapshot, no canvas link is left.

Steps 2 and 3 run before 4 and 5 because those write files (`tests/last_run.json`, `tracker/trace.*`).

The checkout folder must be called `cc-research` (pins of file sets include it); the workflows set `path: cc-research`.

## Before every commit

    python tracker/verify.py              # if any evidence or ticket changed
    python tracker/trace.py check
    python tracker/snapshot.py            # refresh site/snapshot.json
    python site/build.py                  # optional: look at site/_build/index.html locally

The pre-commit hook (`git config core.hooksPath tools/hooks`, once per clone) runs the secret scan on staged files.

## The site

`site/build.py` writes one page, `site/_build/index.html`, with five zoom levels (Space, Bounds, Theses, Bundles, Stages).
It may print a number only through `site/registry.py`, where each entry names its file and JSON pointer (or a literal that
must appear in the cited report). `tracker/snapshot.py` evaluates the registry, records the value, the source path and the
source's sha256, and fails on any number it cannot read. On GitHub, each dotted number links to its file at the commit
the page was built from.

`pages.yml` publishes on every push to `main`. One-time setting: repository Settings → Pages → Source: GitHub Actions.
A GitHub Pages site is public even when the repository is private, and a private repository needs a paid or education
plan for Pages. Until the repository goes public, the page is the only public part; nothing in it is secret, but it
names the agent under audit and our unpublished numbers.

## Data outside git

`python tools/data_manifest.py --budget 150` hashes `external/`, `runs/` and `jobs/transfer/` in resumable chunks
(state in `manifests/excluded/.state.json`, not committed). `--check` re-hashes and reports changes.
`runs/` is the evidence for every live claim; archive it per label as a GitHub release asset
(`runs_<label>.tar.gz`) and record the asset's sha256 next to the manifest when the repository is created.

## Creating the repository (once; Uzair runs these, PowerShell in `...\DSC 180A\cc-research`)

    git init -b main
    git config core.hooksPath tools/hooks
    git config core.autocrlf false
    python tools/secret_scan.py                 # must print 0 findings before anything is added
    git add -A
    git status --short | Select-String -Pattern "^A  (external|runs|jobs/transfer)/"   # must print nothing
    git commit -F docs/commit_msgs/repo_init_cc-research.txt
    # on github.com: create an empty private repository named cc-research (no README, no licence)
    git remote add origin https://github.com/<you>/cc-research.git
    git push -u origin main
    # Settings -> Pages -> Source: GitHub Actions; the pages workflow then publishes the Atlas

The first push runs both workflows. If `ci` fails on `Evidence pins`, a pinned file differs between this machine and the
commit (usually a line-ending conversion): check `git config core.autocrlf` is `false` and that `.gitattributes` is committed.
