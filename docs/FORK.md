# Working on Causal-Copilot: the fork

Tickets: INF-06, BLD-06

Until now Causal-Copilot has been an unpacked zip of upstream commit `a31aa7c`, checked byte for byte against
`manifests/baseline_a31aa7c.sha256` before every run. Changing it (the drop-in refinement stage, BLD-06; bug reports,
EXT-03) needs a fork with history, without ever losing the untouched baseline.

## Shape

- Upstream: `https://github.com/Lancelot39/Causal-Copilot`.
- Fork: `<you>/Causal-Copilot`, cloned as a sibling of `cc-research` (the harness expects `..\Causal-Copilot`).
- `main` in the fork = upstream `a31aa7c` exactly, tagged `baseline-a31aa7c`. Nothing is ever committed to `main`.
- One branch per change, named after its ticket: `bld-06-refinement-v2`, `ext-03-cycle-step-key`. Each branch changes only
  what its ticket names; the diff against `baseline-a31aa7c` is the change.
- `cc-research/upstream.lock` pins which commit a run used. Every run already records the tree's identity in `meta.json`.

## One-time setup (PowerShell, from `...\DSC 180A`)

    # 1. on github.com: fork Lancelot39/Causal-Copilot to your account
    # 2. move the unpacked copy aside (it holds .env, which must never be committed)
    Rename-Item Causal-Copilot Causal-Copilot-zip
    git clone -c core.autocrlf=false https://github.com/<you>/Causal-Copilot.git
    cd Causal-Copilot
    git remote add upstream https://github.com/Lancelot39/Causal-Copilot.git
    git fetch upstream
    git checkout -B main a31aa7c
    git tag baseline-a31aa7c
    git push -f origin main --tags
    # 3. bring the key file back without tracking it
    Copy-Item ..\Causal-Copilot-zip\.env .env
    git check-ignore .env          # must print .env; if it prints nothing, add .env to .git/info/exclude
    # 4. confirm the clone is the same tree the harness pinned
    cd ..\cc-research
    powershell -ExecutionPolicy Bypass -File .\cc.ps1 preflight

`preflight` compares every file with `manifests/baseline_a31aa7c.sha256`. The clone must keep the repository's own line
endings (`core.autocrlf=false`): with Windows' default conversion every text file changes its hash. If the clone differs from the zip (for
example in line endings or files the zip lacked), stop and compare before deleting `Causal-Copilot-zip`.

## Working on a change

    git switch -c bld-06-refinement-v2 baseline-a31aa7c
    # edit; commit with the ticket ID in the message
    git switch main                # back to the untouched baseline for unmodified runs

Runs of the unmodified agent always use `main`. Today the harness aborts on any tree that differs from
`manifests/baseline_a31aa7c.sha256`, so a branch cannot be run by accident. Running a branch needs a harness option that
records the branch, its commit and its diff against `baseline-a31aa7c` in `meta.json` and labels the results with the
ticket; that option is part of BLD-06.

## Status (20 Oct): done

- Fork: https://github.com/uzairgheewala/Causal-Copilot (made from the GitHub page, main branch only). Upstream's head is
  a31aa7c itself, so the fork's `main` is the untouched baseline with no force push.
- `..\Causal-Copilot` is now a clone of the fork *in place*: `git init`, fetch, `reset --mixed` to `origin/main`. The working
  files were already byte-identical to a31aa7c (the harness's manifest check), so nothing in the tree was rewritten and
  `.env` (ignored by upstream's .gitignore) was never opened, copied or moved. Tag `baseline-a31aa7c`; remotes `origin`
  (the fork) and `upstream`.
- One tracked upstream file has backslashes in its name (`externals/pyCausalFS/CBD/.\output\indicator.txt`); the zip
  unpacked it as `CBD\output\indicator.txt`, which is what the baseline manifest lists. It is marked skip-worktree, so
  `git status` is clean.
- Branch folders: `..\Causal-Copilot-branches\ext-03-cycle-step-key` (commit da55264) and
  `..\Causal-Copilot-branches\bld-06-refinement-v2` (commit 55a490a), each a clone at its branch, remotes `local` (the
  main clone), `origin` (the fork) and `upstream`. Both pass the harness's branch check (files equal
  `jobs/fork/<branch>.sha256`, HEAD on the branch); main passes the baseline check.
- Not yet on GitHub: the two branches and the tag (pushing needs your credentials). From the DSC 180A folder:

      git -C Causal-Copilot push origin bld-06-refinement-v2 ext-03-cycle-step-key baseline-a31aa7c

## Ticket branches

The harness runs a ticket branch when `$env:CC_BRANCH = "<branch>"` is set before any `cc.ps1` command. `cc.ps1` then
mounts `..\Causal-Copilot-branches\<branch>` as the repo (and the main clone's `.env`, read-only); the tree is checked
against `jobs/fork/<branch>.json` (the baseline manifest plus exactly that branch's patch), the checkout must be on that
branch, and every run's `meta.json` records `fork`: branch, ticket, commit, patch sha256. Without `CC_BRANCH` the harness
uses `..\Causal-Copilot` and checks it against the untouched baseline as before.

| Branch | Ticket | Patch | What it changes |
|---|---|---|---|
| `ext-03-cycle-step-key` | EXT-03 | `jobs/fork/ext-03-cycle-step-key.patch` | `postprocess/judge_functions.py`: the cycle-step prompt names its JSON key; the reply is read defensively; no usable answer removes the cycle's closing edge (logged) |
| `bld-06-refinement-v2` | BLD-06 | `jobs/fork/bld-06-refinement-v2.patch` | `postprocess/judge.py` + new `postprocess/refinement_v2_dropin.py`: refinement v2 replaces the bootstrap/LLM/KCI pruning and the cycle step; `CC_REFINEMENT=original` restores them, `CC_REFINEMENT=v2d` runs the data part only |

`jobs/fork/make_branches.ps1` rebuilds a missing branch folder. `tests/test_fork_patches.py` checks that the drop-in gives
the same graphs as `analysis/refinement_v2.py` and that the patch adds exactly that file. A new branch: write its patch in
`jobs/fork/`, describe it with `harness/fork_branch.py describe`, add it to `make_branches.ps1`.

Rule 3 of AGENTS.md: never change `main` of the fork or the unpacked copy; changes live only on ticket branches, made from
patch files in `jobs/fork/`.
