# BLD-22: create the ticket branch bld-22-direction-sufficiency of the Causal-Copilot fork, stacked on bld-06-refinement-v2
# (55a490a), as Causal-Copilot-branches\bld-22-direction-sufficiency. Uzair runs this (it makes a commit and a local push).
# From cc-research:
#     powershell -ExecutionPolicy Bypass -File .\jobs\fork\make_bld22.ps1
# Same layout and steps as make_branches.ps1; the only difference is the base: bld-06-refinement-v2, not baseline-a31aa7c,
# because BLD-22 changes refinement v2's drop-in (one branch per ticket, stacked).
# After it: push the branch to GitHub yourself (git -C ..\Causal-Copilot-branches\bld-22-direction-sufficiency push origin bld-22-direction-sufficiency).
$ErrorActionPreference = "Stop"
$Research = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Root = Split-Path -Parent $Research
$Main = Join-Path $Root "Causal-Copilot"
$Dir = Join-Path $Root "Causal-Copilot-branches"
$name = "bld-22-direction-sufficiency"
$base = "bld-06-refinement-v2"
$baseCommit = "55a490a16776bbae1d81694bfe54525f11658be3"
$msg = "BLD-22: commit an arrow only when at least 15 of 20 resamples give it (95% Wilson bound above 1/2); otherwise leave the direction open. CC_DIRECTION=plurality restores bld-06"
$patch = Join-Path $Research "jobs\fork\bld-22-direction-sufficiency.patch"
$d = Join-Path $Dir $name
if (Test-Path (Join-Path $d ".git")) { Write-Host "[fork] $name exists"; exit 0 }
$expect = (Get-Content (Join-Path $Research "jobs\fork\bld-22-direction-sufficiency.json") -Raw | ConvertFrom-Json).patch_sha256
$got = (Get-FileHash -Algorithm SHA256 $patch).Hash.ToLower()
if ($got -ne $expect) { throw "patch sha256 $got differs from the branch spec ($expect)" }
git clone --no-checkout -c core.autocrlf=false $Main $d
git -C $d sparse-checkout set --no-cone '/*' '!/externals/pyCausalFS/CBD/.*indicator.txt'
git -C $d checkout -b $name "origin/$base"
$head = (git -C $d rev-parse HEAD).Trim()
if ($head -ne $baseCommit) { throw "origin/$base is at $head, expected $baseCommit" }
git -C $d apply $patch
git -C $d add postprocess/judge.py postprocess/refinement_v2_dropin.py
git -C $d commit -m $msg -m "Patch: cc-research/jobs/fork/bld-22-direction-sufficiency.patch" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`nClaude-Session: https://claude.ai/code/session_01P6WxGPn7FW9pxha7bcmgxt"
git -C $d push origin "${name}:${name}"
Copy-Item (Join-Path $Main "externals\pyCausalFS\CBD\output\indicator.txt") (Join-Path $d "externals\pyCausalFS\CBD\output\indicator.txt") -Force
git -C $d remote rename origin local
git -C $d remote add origin (git -C $Main remote get-url origin)
$env:CC_BRANCH = $name
powershell -ExecutionPolicy Bypass -File (Join-Path $Research "cc.ps1") preflight nollm
Remove-Item Env:\CC_BRANCH
