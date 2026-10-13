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
    git clone https://github.com/<you>/Causal-Copilot.git
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

`preflight` compares every file with `manifests/baseline_a31aa7c.sha256`. If the clone differs from the zip (for
example in line endings or files the zip lacked), stop and compare before deleting `Causal-Copilot-zip`.

## Working on a change

    git switch -c bld-06-refinement-v2 baseline-a31aa7c
    # edit; commit with the ticket ID in the message
    git switch main                # back to the untouched baseline for unmodified runs

Runs of the unmodified agent always use `main`. Today the harness aborts on any tree that differs from
`manifests/baseline_a31aa7c.sha256`, so a branch cannot be run by accident. Running a branch needs a harness option that
records the branch, its commit and its diff against `baseline-a31aa7c` in `meta.json` and labels the results with the
ticket; that option is part of BLD-06.
