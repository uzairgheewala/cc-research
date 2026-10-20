# Causal-Copilot research harness launcher (Windows PowerShell + Docker Desktop).
# Usage:  powershell -ExecutionPolicy Bypass -File .\cc.ps1 <command>
# Commands: build | preflight [nollm] | dryrun | golden | plan <file> [model] | names <file> [stub] | tiers <file> [stub] | probebuild | probe <plan> [stub] | ensureimage | probebatch <dir> [stub|live] [agent|all] [workers=N tier=A arm=a+b scenario=s cap=X retry] | compute <job> | kernelbuild | benchbuild | x5build | wave <id> [workers] [memGB] | wavepack <id> | fetch | queue | stop | shell | help
param(
    [Parameter(Position = 0)] [string] $Command = "help",
    [Parameter(Position = 1)] [string] $Arg1 = "",
    [Parameter(Position = 2)] [string] $Arg2 = "",
    [Parameter(Position = 3)] [string] $Arg3 = "",
    [Parameter(ValueFromRemainingArguments = $true)] [string[]] $Rest = @()
)

$Research  = $PSScriptRoot
$Root      = Split-Path -Parent $Research
$Repo      = Join-Path $Root "Causal-Copilot"
$MainRepo  = $Repo
# INF-06: a ticket-branch run uses that branch's own clone (one checkout per branch, so main stays the untouched baseline
# while a branch runs); its .env is the main clone's, mounted read-only, never copied.
if ($env:CC_BRANCH -and $env:CC_BRANCH -ne "main") {
    $Repo = Join-Path $Root ("Causal-Copilot-branches\" + $env:CC_BRANCH)
}
$BaseImage = "causal-copilot-cpu:a31aa7c"
$Image     = "cc-research:a31aa7c-1"

function Fail([string] $Message) {
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

function Invoke-InContainer {
    param([string[]] $Cmd, [string[]] $Extra = @())
    # INF-06: a ticket branch run (set $env:CC_BRANCH = "bld-06-refinement-v2"); the harness checks the tree against
    # jobs\fork\<branch>.json and records branch, commit and patch in meta.json
    if ($env:CC_BRANCH -and $env:CC_BRANCH -ne "main") {
        $Extra += @("-e", "CC_BRANCH=$($env:CC_BRANCH)")
        $mainEnv = Join-Path $MainRepo ".env"
        if (Test-Path $mainEnv) { $Extra += @("-v", "${mainEnv}:/app/.env:ro") }
    }
    $dockerArgs = @("run", "--rm", "-i", "--init") + $Extra + @(
        "-v", "${Repo}:/app",
        "-v", "${Research}:/research",
        "-w", "/app",
        "-e", "CC_REPO=/app",
        "-e", "PYTHONDONTWRITEBYTECODE=1",
        "-e", "PYTHONUNBUFFERED=1",
        $Image) + $Cmd
    & docker @dockerArgs
    $code = $LASTEXITCODE
    Write-Host ""
    Write-Host "[cc] container exit code: $code"
    exit $code
}

if (-not (Test-Path (Join-Path $Repo "main.py"))) {
    Fail "Causal-Copilot was not found next to cc-research (looked in: $Repo)"
}

switch ($Command.ToLower()) {

    "build" {
        # The build context holds only requirements_cpu.txt, so the repo's .env (your API key)
        # can never be copied into an image layer. Dockerfile.cpu itself is used unmodified.
        $ctx = Join-Path $env:TEMP "cc-build-context"
        if (Test-Path $ctx) { Remove-Item -Recurse -Force $ctx }
        New-Item -ItemType Directory -Path $ctx | Out-Null
        Copy-Item (Join-Path $Repo "requirements_cpu.txt") $ctx
        Write-Host "[cc] building $BaseImage from the repo's own Dockerfile.cpu (large download; the first build can take 20-40 minutes)"
        & docker build -f (Join-Path $Repo "Dockerfile.cpu") -t $BaseImage $ctx
        if ($LASTEXITCODE -ne 0) { Fail "base image build failed" }
        Write-Host "[cc] building $Image (thin runtime layer)"
        & docker build --build-arg "BASE=$BaseImage" -f (Join-Path $Research "docker\Dockerfile.overlay") -t $Image (Join-Path $Research "docker")
        if ($LASTEXITCODE -ne 0) { Fail "runtime layer build failed" }
        $baseId = & docker image inspect $BaseImage --format "{{.Id}}"
        $runId  = & docker image inspect $Image --format "{{.Id}}"
        $info = @{ base_image = $BaseImage; base_id = "$baseId"; runtime_image = $Image; runtime_id = "$runId"; built_utc = (Get-Date).ToUniversalTime().ToString("o") }
        $info | ConvertTo-Json | Out-File -Encoding ascii (Join-Path $Research "manifests\image_ids.json")
        Write-Host "[cc] build complete. Next: powershell -ExecutionPolicy Bypass -File .\cc.ps1 preflight"
    }

    "preflight" {
        if ($Arg1 -eq "nollm" -or $Arg1 -eq "--no-llm") {
            Invoke-InContainer -Cmd @("python", "/research/harness/preflight.py", "--no-llm")
        }
        else {
            Invoke-InContainer -Cmd @("python", "/research/harness/preflight.py")
        }
    }

    "dryrun" {
        Invoke-InContainer -Cmd @("python", "/research/harness/run_traced.py", "--dataset", "data/dataset/Linear_Gaussian", "--data-mode", "simulated", "--label", "dryrun", "--stub-llm")
    }

    "golden" {
        Invoke-InContainer -Cmd @("python", "/research/harness/run_plan.py", "--plan", "/research/plans/golden.json")
    }

    "plan" {
        if (-not $Arg1) { Fail "usage: cc.ps1 plan <file name inside cc-research\plans>" }
        $leaf = Split-Path -Leaf $Arg1
        if (-not (Test-Path (Join-Path $Research "plans\$leaf"))) { Fail "plan file not found: cc-research\plans\$leaf" }
        $extra = @()
        if ($Arg2) {
            # Second model (AB-05/AB-06): passed as an environment variable; real environment variables win over the repo's
            # .env (python-dotenv, override=False), so the .env file is neither read here nor changed.
            if ($Arg2 -notmatch '^[A-Za-z0-9._:-]{1,60}$') { Fail "model name has unexpected characters: $Arg2" }
            $extra = @("-e", "LLM_MODEL=$Arg2")
            Write-Host "[cc] LLM_MODEL=$Arg2 for this plan (run_traced records it in each run's meta)"
        }
        Invoke-InContainer -Cmd @("python", "/research/harness/run_plan.py", "--plan", "/research/plans/$leaf") -Extra $extra
    }

    "tiers" {
        # AB-07 / A3 (DEC-02): tier requests from cc-research\plans. LIVE (uses the key in Causal-Copilot\.env) unless the
        # second argument is "stub". The runner refuses a live run whose request file differs from plans\a3_prereg.json.
        if (-not $Arg1) { Fail "usage: cc.ps1 tiers <request file inside cc-research\plans> [stub]" }
        $leaf = Split-Path -Leaf $Arg1
        if (-not (Test-Path (Join-Path $Research "plans\$leaf"))) { Fail "request file not found: cc-research\plans\$leaf" }
        $cmd = @("python", "/research/harness/tiers_runner.py", "--requests", "/research/plans/$leaf", "--prereg", "/research/plans/a3_prereg.json")
        if ($Arg2 -eq "stub") { $cmd += @("--stub", "--out", "/research/plans/results/a3_tiers_answers.STUB.jsonl") }
        else { $cmd += @("--out", "/research/plans/results/a3_tiers_answers.jsonl") }
        Invoke-InContainer -Cmd $cmd
    }

    "probebuild" {
        # AB-05: separate image with the four external agents (docker\Dockerfile.probes). Build context = the four
        # requirement files only. Never push this image (it contains code without a licence, used for evaluation only).
        $ctx = Join-Path $env:TEMP "cc-probes-context"
        if (Test-Path $ctx) { Remove-Item -Recurse -Force $ctx }
        New-Item -ItemType Directory -Path $ctx | Out-Null
        Copy-Item (Join-Path $Research "harness\agents\requirements_*.txt") $ctx
        & docker build --build-arg "BASE=$Image" -f (Join-Path $Research "docker\Dockerfile.probes") -t "cc-probes:ab05-1" $ctx
        if ($LASTEXITCODE -ne 0) { Fail "probe image build failed" }
        & docker image inspect "cc-probes:ab05-1" --format "{{.Id}}"
    }

    "probe" {
        # AB-05: one agent probe from a plan file in cc-research\plans. "stub" runs offline (no network, no key, no cost);
        # otherwise LIVE: only the .env file is mounted, read-only. Caps (calls, USD) come from the plan file.
        if (-not $Arg1) { Fail "usage: cc.ps1 probe <plan file inside cc-research\plans> [stub]" }
        $leaf = Split-Path -Leaf $Arg1
        if (-not (Test-Path (Join-Path $Research "plans\$leaf"))) { Fail "plan file not found: cc-research\plans\$leaf" }
        $base = @("run", "--rm", "-i", "--init")
        $common = @("-v", "${Research}:/research", "-w", "/research", "-e", "PYTHONPATH=", "-e", "PYTHONDONTWRITEBYTECODE=1", "-e", "PYTHONUNBUFFERED=1")
        if ($Arg2 -eq "stub") {
            $dockerArgs = $base + @("--network", "none") + $common + @("cc-probes:ab05-1", "python", "/research/harness/agent_probe.py", "--plan", "/research/plans/$leaf", "--stub")
        }
        else {
            $envFile = Join-Path $Repo ".env"
            $dockerArgs = $base + @("-v", "${envFile}:/app/.env:ro") + $common + @("cc-probes:ab05-1", "python", "/research/harness/agent_probe.py", "--plan", "/research/plans/$leaf")
        }
        & docker @dockerArgs
        $code = $LASTEXITCODE
        Write-Host ""
        Write-Host "[cc] probe exit code: $code (0 ok, 3 cap reached, 4 agent failed, 2 setup error)"
        exit $code
    }

    "probebatch" {
        # AB-06: every plan in a folder of cc-research\plans (e.g. ab06), one agent run per process, resumable, with a total
        # USD cap (default 60; plans\ab06\BUDGET.json has the estimate). "stub" = offline (no network, no key, no cost).
        # Optional third argument: one agent (causaliq, pywhyllm, matmcd, vashishtha) to run only that agent's plans.
        if (-not $Arg1) { Fail "usage: cc.ps1 probebatch <plan folder inside cc-research\plans> [stub|live] [agent]" }
        $leaf = Split-Path -Leaf $Arg1
        if (-not (Test-Path (Join-Path $Research "plans\$leaf"))) { Fail "plan folder not found: cc-research\plans\$leaf" }
        $base = @("run", "--rm", "-i", "--init")
        $common = @("-v", "${Research}:/research", "-w", "/research", "-e", "PYTHONPATH=", "-e", "PYTHONDONTWRITEBYTECODE=1", "-e", "PYTHONUNBUFFERED=1")
        $cmd = @("python", "/research/harness/agent_batch.py", "--plans", "/research/plans/$leaf")
        if ($Arg3 -and $Arg3 -ne "all") { $cmd += @("--agent", $Arg3) }
        # Further options as key=value words (no leading dashes, so PowerShell never reads them as its own parameters):
        #   workers=4  arm=real+swapped  scenario=name1+name2  cap=60  retry   ("+" separates values; "," also works with -File)
        foreach ($t in $Rest) {
            if ($t -match '^workers=([0-9]+)$') { $cmd += @("--workers", $Matches[1]) }
            elseif ($t -match '^cap=([0-9.]+)$') { $cmd += @("--max-usd-total", $Matches[1]) }
            elseif ($t -match '^arm=([a-z,+]+)$') { $cmd += @("--arm") + ($Matches[1] -split "[,+]") }
            elseif ($t -match '^scenario=([A-Za-z0-9_,+]+)$') { $cmd += @("--scenario") + ($Matches[1] -split "[,+]") }
            elseif ($t -match '^tier=([A-Za-z0-9]+)$') { $cmd += @("--tier", $Matches[1]) }
            elseif ($t -eq "retry") { $cmd += "--retry-failed" }
            else { Fail "unknown probebatch option: $t (use workers=N, tier=A, arm=a+b, scenario=s1+s2, cap=X, retry)" }
        }
        if ($Arg2 -eq "stub") {
            $dockerArgs = $base + @("--network", "none") + $common + @("cc-probes:ab05-1") + $cmd + @("--stub")
        }
        else {
            $envFile = Join-Path $Repo ".env"
            $dockerArgs = $base + @("-v", "${envFile}:/app/.env:ro") + $common + @("cc-probes:ab05-1") + $cmd
        }
        & docker @dockerArgs
        $code = $LASTEXITCODE
        Write-Host ""
        Write-Host "[cc] probebatch exit code: $code"
        exit $code
    }

    "compute" {
        # No-cost compute job (INF-04): no network at all, the repo mounted read-only, and an empty file mounted over the
        # repo's .env, so nothing in the container can see or use the API key. Only scripts in cc-research\analysis that use
        # jobkit are accepted by the runner.
        if (-not $Arg1) { Fail "usage: cc.ps1 compute <job file name inside cc-research\jobs>" }
        $leaf = Split-Path -Leaf $Arg1
        if (-not (Test-Path (Join-Path $Research "jobs\$leaf"))) { Fail "job file not found: cc-research\jobs\$leaf" }
        $empty = Join-Path $Research "jobs\empty.env"
        if (-not (Test-Path $empty)) { New-Item -ItemType File -Path $empty | Out-Null }
        $dockerArgs = @("run", "--rm", "-i", "--init", "--network", "none",
            "-v", "${Repo}:/app:ro",
            "-v", "${empty}:/app/.env:ro",
            "-v", "${Research}:/research",
            "-w", "/research",
            "-e", "PYTHONDONTWRITEBYTECODE=1", "-e", "PYTHONUNBUFFERED=1",
            $Image, "python", "/research/harness/compute_job.py", "--job", "/research/jobs/$leaf")
        & docker @dockerArgs
        $code = $LASTEXITCODE
        Write-Host ""
        Write-Host "[cc] compute job exit code: $code"
        exit $code
    }

    "names" {
        # BND-11 names part: short direction questions from a request file in cc-research\plans. LIVE (uses the key in
        # Causal-Copilot\.env) unless the second argument is "stub" (offline, no key, no cost). Answers go to plans\results.
        if (-not $Arg1) { Fail "usage: cc.ps1 names <request file inside cc-research\plans> [stub]" }
        $leaf = Split-Path -Leaf $Arg1
        if (-not (Test-Path (Join-Path $Research "plans\$leaf"))) { Fail "request file not found: cc-research\plans\$leaf" }
        $stem = [System.IO.Path]::GetFileNameWithoutExtension($leaf)
        $cmd = @("python", "/research/harness/names_runner.py", "--requests", "/research/plans/$leaf")
        if ($Arg2 -eq "stub") { $cmd += @("--stub", "--out", "/research/plans/results/$stem.STUB.answers.jsonl") }
        else { $cmd += @("--out", "/research/plans/results/$stem.answers.jsonl") }
        Invoke-InContainer -Cmd $cmd
    }

    "fetch" {
        Invoke-InContainer -Cmd @("python", "/research/harness/fetch_external.py")
    }

    "queue" {
        Invoke-InContainer -Cmd @("python", "/research/harness/run_plan.py", "--queue") -Extra @("--name", "cc-queue")
    }

    "stop" {
        $q = Join-Path $Research "queue"
        New-Item -ItemType Directory -Force -Path $q | Out-Null
        New-Item -ItemType File -Force -Path (Join-Path $q "STOP") | Out-Null
        Write-Host "[cc] STOP requested. The queue runner exits after the run in progress. For an immediate stop: docker stop cc-queue"
    }

    "ensureimage" {
        # INF-06 / INF-10 (wave A, 20 Oct): plan runs need $Image, which was missing on this machine. Build only what is
        # missing: the thin overlay when the base image exists (minutes), else first the base from the repo's own
        # Dockerfile.cpu (20-40 minutes, large download). A rebuilt base downloads its packages again, so it may differ
        # from the base BND-08's runs used: jobs\waves\images\cc.json records whether the ids equal the recorded ones.
        $imgDir = Join-Path $Research "jobs\waves\images"
        New-Item -ItemType Directory -Force -Path $imgDir | Out-Null
        $recPath = Join-Path $Research "manifests\image_ids.json"
        $prev = $null
        if (Test-Path $recPath) { $prev = Get-Content -Raw $recPath | ConvertFrom-Json }
        $built = @()
        $haveRun = (& docker image ls -q $Image | Out-String).Trim()
        if (-not $haveRun) {
            $haveBase = (& docker image ls -q $BaseImage | Out-String).Trim()
            if (-not $haveBase) {
                $ctx = Join-Path $env:TEMP "cc-build-context"
                if (Test-Path $ctx) { Remove-Item -Recurse -Force $ctx }
                New-Item -ItemType Directory -Path $ctx | Out-Null
                Copy-Item (Join-Path $Repo "requirements_cpu.txt") $ctx
                Write-Host "[cc] $BaseImage is missing: building it from the repo's own Dockerfile.cpu (20-40 minutes)"
                & docker build -f (Join-Path $Repo "Dockerfile.cpu") -t $BaseImage $ctx
                if ($LASTEXITCODE -ne 0) { Fail "base image build failed" }
                $built += "base"
            }
            Write-Host "[cc] $Image is missing: building the thin runtime layer"
            & docker build --build-arg "BASE=$BaseImage" -f (Join-Path $Research "docker\Dockerfile.overlay") -t $Image (Join-Path $Research "docker")
            if ($LASTEXITCODE -ne 0) { Fail "runtime layer build failed" }
            $built += "overlay"
        }
        $baseId = (& docker image inspect $BaseImage --format "{{.Id}}" | Out-String).Trim()
        $runId  = (& docker image inspect $Image --format "{{.Id}}" | Out-String).Trim()
        $recBase = ""
        $recRun = ""
        if ($prev) { $recBase = "$($prev.base_id)"; $recRun = "$($prev.runtime_id)" }
        $nowUtc = (Get-Date).ToUniversalTime().ToString("o")
        $info = [ordered]@{ base_image = $BaseImage; base_id = $baseId; runtime_image = $Image; runtime_id = $runId;
                            built = ($built -join "+"); base_same = ($baseId -eq $recBase); runtime_same = ($runId -eq $recRun);
                            recorded_base_id = $recBase; recorded_runtime_id = $recRun; checked_utc = $nowUtc }
        if (($built.Count -gt 0) -and $prev) {
            # the runs recorded so far keep their record; new runs (run_traced.py meta) read the new ids
            $keep = Join-Path $Research ("manifests\image_ids_before_" + (Get-Date).ToUniversalTime().ToString("yyyyMMddTHHmmssZ") + ".json")
            Copy-Item $recPath $keep
            $new = [ordered]@{ base_image = $BaseImage; base_id = $baseId; runtime_image = $Image; runtime_id = $runId; built_utc = $nowUtc;
                               rebuilt = ($built -join "+"); previous_record = (Split-Path -Leaf $keep) }
            $new | ConvertTo-Json | Out-File -Encoding ascii $recPath
        }
        $info | ConvertTo-Json | Out-File -Encoding ascii (Join-Path $imgDir "cc.json")
        $runId | Out-File -Encoding ascii (Join-Path $imgDir "cc.id")
        Get-Content (Join-Path $imgDir "cc.json")
    }

    "kernelbuild" {
        # INF-10: the pinned kernel image for wave sheets (docker\Dockerfile.kernel; context = cc-research\docker).
        & docker build -f (Join-Path $Research "docker\Dockerfile.kernel") -t "cc-kernel:wave-a" (Join-Path $Research "docker")
        if ($LASTEXITCODE -ne 0) { Fail "kernel image build failed" }
        $imgDir = Join-Path $Research "jobs\waves\images"
        New-Item -ItemType Directory -Force -Path $imgDir | Out-Null
        & docker image inspect "cc-kernel:wave-a" --format "{{.Id}}" | Out-File -Encoding ascii (Join-Path $imgDir "kernel.id")
        Get-Content (Join-Path $imgDir "kernel.id")
    }

    "benchbuild" {
        # BEN-13: causalbench evaluation image (docker\Dockerfile.bench).
        & docker build -f (Join-Path $Research "docker\Dockerfile.bench") -t "cc-bench:wave-a" (Join-Path $Research "docker")
        if ($LASTEXITCODE -ne 0) { Fail "bench image build failed" }
        $imgDir = Join-Path $Research "jobs\waves\images"
        New-Item -ItemType Directory -Force -Path $imgDir | Out-Null
        & docker image inspect "cc-bench:wave-a" --format "{{.Id}}" | Out-File -Encoding ascii (Join-Path $imgDir "bench.id")
        Get-Content (Join-Path $imgDir "bench.id")
    }

    "x5build" {
        # X5 (REP-07): AVICI inference image (docker\Dockerfile.x5).
        & docker build -f (Join-Path $Research "docker\Dockerfile.x5") -t "cc-x5:wave-a" (Join-Path $Research "docker")
        if ($LASTEXITCODE -ne 0) { Fail "x5 image build failed" }
        $imgDir = Join-Path $Research "jobs\waves\images"
        New-Item -ItemType Directory -Force -Path $imgDir | Out-Null
        & docker image inspect "cc-x5:wave-a" --format "{{.Id}}" | Out-File -Encoding ascii (Join-Path $imgDir "x5.id")
        Get-Content (Join-Path $imgDir "x5.id")
    }

    "wave" {
        # INF-10: run one wave's sheet (harness\wave.py, standard-library Python on this machine; it starts the containers).
        # usage: cc.ps1 wave A [workers] [memGB]    -> jobs\waves\A\sheet.json; run it again to resume
        if (-not $Arg1) { Fail "usage: cc.ps1 wave <wave id> [workers] [memGB]" }
        $sheet = Join-Path $Research "jobs\waves\$Arg1\sheet.json"
        if (-not (Test-Path $sheet)) { Fail "sheet not found: $sheet" }
        $py = Get-Command py -ErrorAction SilentlyContinue
        $pyArgs = @()
        if ($py) { $pyExe = "py"; $pyArgs = @("-3") } else {
            $py = Get-Command python -ErrorAction SilentlyContinue
            if (-not $py) { Fail "Python 3.8+ is needed on this machine for the wave runner (winget install Python.Python.3.12)" }
            $pyExe = "python" }
        $workers = if ($Arg2) { $Arg2 } else { "2" }
        $runArgs = $pyArgs + @((Join-Path $Research "harness\wave.py"), "run", "--sheet", $sheet, "--workers", $workers)
        if ($Arg3) { $runArgs += @("--mem", $Arg3) }
        & $pyExe @runArgs
        $code = $LASTEXITCODE
        & $pyExe @($pyArgs + @((Join-Path $Research "harness\wave.py"), "pack", "--sheet", $sheet))
        Write-Host ""
        Write-Host "[cc] wave $Arg1 exit code: $code. Send back: cc-research\jobs\waves\$Arg1\return_$Arg1.zip"
        exit $code
    }

    "wavepack" {
        if (-not $Arg1) { Fail "usage: cc.ps1 wavepack <wave id>" }
        $py = Get-Command py -ErrorAction SilentlyContinue
        if ($py) { & py -3 (Join-Path $Research "harness\wave.py") pack --sheet (Join-Path $Research "jobs\waves\$Arg1\sheet.json") }
        else { & python (Join-Path $Research "harness\wave.py") pack --sheet (Join-Path $Research "jobs\waves\$Arg1\sheet.json") }
    }

    "shell" {
        & docker run --rm -it --init -v "${Repo}:/app" -v "${Research}:/research" -w /app -e CC_REPO=/app -e PYTHONDONTWRITEBYTECODE=1 $Image bash
    }

    default {
        Write-Host "Causal-Copilot research harness"
        Write-Host "  build              build the Docker images (once)"
        Write-Host "  ensureimage        build only the missing Causal-Copilot images; jobs\waves\images\cc.json says if they changed"
        Write-Host "  preflight          check code identity, environment, imports, tools and one tiny LLM round trip"
        Write-Host "  preflight nollm    same, without the LLM calls"
        Write-Host "  dryrun             full pipeline on Linear_Gaussian with an offline stub instead of the LLM (no cost)"
        Write-Host "  golden             live golden runs: Linear_Gaussian, then sachs"
        Write-Host "  plan <file>        run a plan file from cc-research\plans"
        Write-Host "  plan <file> <model> same, with LLM_MODEL set for this run only (e.g. gpt-4o-mini)"
        Write-Host "  tiers <file> [stub] AB-07 tier questions (live; 'stub' = offline, no cost)"
        Write-Host "  probebuild         build the AB-05 agent-probe image (once)"
        Write-Host "  probe <plan> [stub] AB-05 agent probe (live; 'stub' = offline, no cost)"
        Write-Host "  probebatch <dir> [stub|live] [agent|all] [options]  AB-06 folder of probe plans, resumable, total cap"
        Write-Host "                     options: workers=N  tier=A  arm=real+swapped  scenario=s1+s2  cap=X  retry"
        Write-Host "  names <file> [stub] BND-11 direction questions from cc-research\plans (live; 'stub' = offline, no cost)"
        Write-Host "  compute <job>      run a no-cost compute job from cc-research\jobs (no network, no key)"
        Write-Host "  fetch              download public benchmark data into cc-research\external (no LLM, no cost)"
        Write-Host "  queue              keep running plans that appear in cc-research\queue\inbox"
        Write-Host "  stop               ask the queue runner to exit after the current run"
        Write-Host "  shell              interactive shell inside the container"
    }
}
