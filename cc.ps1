# Causal-Copilot research harness launcher (Windows PowerShell + Docker Desktop).
# Usage:  powershell -ExecutionPolicy Bypass -File .\cc.ps1 <command>
# Commands: build | preflight [nollm] | dryrun | golden | plan <file> | names <file> [stub] | compute <job> | fetch | queue | stop | shell | help
param(
    [Parameter(Position = 0)] [string] $Command = "help",
    [Parameter(Position = 1)] [string] $Arg1 = "",
    [Parameter(Position = 2)] [string] $Arg2 = ""
)

$Research  = $PSScriptRoot
$Root      = Split-Path -Parent $Research
$Repo      = Join-Path $Root "Causal-Copilot"
$BaseImage = "causal-copilot-cpu:a31aa7c"
$Image     = "cc-research:a31aa7c-1"

function Fail([string] $Message) {
    Write-Host "ERROR: $Message" -ForegroundColor Red
    exit 1
}

function Invoke-InContainer {
    param([string[]] $Cmd, [string[]] $Extra = @())
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
        Invoke-InContainer -Cmd @("python", "/research/harness/run_plan.py", "--plan", "/research/plans/$leaf")
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

    "shell" {
        & docker run --rm -it --init -v "${Repo}:/app" -v "${Research}:/research" -w /app -e CC_REPO=/app -e PYTHONDONTWRITEBYTECODE=1 $Image bash
    }

    default {
        Write-Host "Causal-Copilot research harness"
        Write-Host "  build              build the Docker images (once)"
        Write-Host "  preflight          check code identity, environment, imports, tools and one tiny LLM round trip"
        Write-Host "  preflight nollm    same, without the LLM calls"
        Write-Host "  dryrun             full pipeline on Linear_Gaussian with an offline stub instead of the LLM (no cost)"
        Write-Host "  golden             live golden runs: Linear_Gaussian, then sachs"
        Write-Host "  plan <file>        run a plan file from cc-research\plans"
        Write-Host "  names <file> [stub] BND-11 direction questions from cc-research\plans (live; 'stub' = offline, no cost)"
        Write-Host "  compute <job>      run a no-cost compute job from cc-research\jobs (no network, no key)"
        Write-Host "  fetch              download public benchmark data into cc-research\external (no LLM, no cost)"
        Write-Host "  queue              keep running plans that appear in cc-research\queue\inbox"
        Write-Host "  stop               ask the queue runner to exit after the current run"
        Write-Host "  shell              interactive shell inside the container"
    }
}
