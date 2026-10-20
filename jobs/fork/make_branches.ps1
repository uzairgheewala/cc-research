# INF-06: recreate the ticket-branch folders of the Causal-Copilot fork, if one is missing. On 20 Oct the agent created
# both (Causal-Copilot-branches\<branch>, each a clone checked out at its branch, commits made from jobs\fork\*.patch);
# run this only to rebuild a deleted one. From cc-research:
#     powershell -ExecutionPolicy Bypass -File .\jobs\fork\make_branches.ps1
# Layout: ..\Causal-Copilot = the fork's main (= a31aa7c, tag baseline-a31aa7c), never checked out elsewhere;
#         ..\Causal-Copilot-branches\<branch> = one clone per ticket branch (cc.ps1 uses it when $env:CC_BRANCH is set).
# One tracked upstream file has backslashes in its name (externals/pyCausalFS/CBD/.\output\indicator.txt), which Windows
# cannot create; it is marked skip-worktree, and the unpacked copy's externals\pyCausalFS\CBD\output\indicator.txt (the
# file the baseline manifest lists) is copied in.
$ErrorActionPreference = "Stop"
$Research = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Root = Split-Path -Parent $Research
$Main = Join-Path $Root "Causal-Copilot"
$Dir = Join-Path $Root "Causal-Copilot-branches"
$odd = 'externals/pyCausalFS/CBD/.\output\indicator.txt'
$branches = @(
    @{ name = "ext-03-cycle-step-key"; msg = "EXT-03: cycle step names its JSON key and reads the reply defensively"; files = @("postprocess/judge_functions.py") },
    @{ name = "bld-06-refinement-v2"; msg = "BLD-06: refinement v2 (cc-research) replaces the pruning stages; CC_REFINEMENT=original restores them"; files = @("postprocess/judge.py", "postprocess/refinement_v2_dropin.py") }
)
New-Item -ItemType Directory -Force -Path $Dir | Out-Null
foreach ($b in $branches) {
    $d = Join-Path $Dir $b.name
    if (Test-Path (Join-Path $d ".git")) { Write-Host "[fork] $($b.name) exists"; continue }
    git clone --no-checkout -c core.autocrlf=false $Main $d
    git -C $d sparse-checkout set --no-cone '/*' '!/externals/pyCausalFS/CBD/.*indicator.txt'
    $has = git -C $Main branch --list $b.name
    if ($has) { git -C $d checkout $b.name } else {
        git -C $d checkout -b $b.name baseline-a31aa7c
        git -C $d apply (Join-Path $Research ("jobs\fork\" + $b.name + ".patch"))
        git -C $d add $b.files
        git -C $d commit -m $b.msg
        git -C $d push local "$($b.name):$($b.name)"
    }
    Copy-Item (Join-Path $Main "externals\pyCausalFS\CBD\output\indicator.txt") (Join-Path $d "externals\pyCausalFS\CBD\output\indicator.txt") -Force
    git -C $d remote rename origin local
    git -C $d remote add origin (git -C $Main remote get-url origin)
    $env:CC_BRANCH = $b.name
    powershell -ExecutionPolicy Bypass -File (Join-Path $Research "cc.ps1") preflight nollm
    Remove-Item Env:\CC_BRANCH
}
