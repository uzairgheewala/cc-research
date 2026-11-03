# INF-11: record this machine for sizing wave sheets: CPU, cores, RAM, Docker memory, and what BLAS selects inside the
# kernel image. No network, no secrets, nothing outside cc-research is written.
#   powershell -ExecutionPolicy Bypass -File .\tools\host_probe.ps1 [-Name laptop2]   -> manifests\hosts\<Name>.json
param([string] $Name = "laptop2")
$ErrorActionPreference = "Continue"
$Research = Split-Path -Parent $PSScriptRoot
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$cs  = Get-CimInstance Win32_ComputerSystem
$os  = Get-CimInstance Win32_OperatingSystem
$r = [ordered]@{
    name = $Name; recorded_utc = (Get-Date).ToUniversalTime().ToString("o")
    cpu = $cpu.Name.Trim(); cores = $cpu.NumberOfCores; logical_processors = $cpu.NumberOfLogicalProcessors
    ram_gb = [math]::Round($cs.TotalPhysicalMemory / 1GB, 1); os = "$($os.Caption) $($os.Version)"
    disk_free_gb = [math]::Round((Get-PSDrive ((Split-Path -Qualifier $Research).TrimEnd(':'))).Free / 1GB, 1)
}
$wsl = Join-Path $env:USERPROFILE ".wslconfig"
if (Test-Path $wsl) { $r.wslconfig = ((Get-Content $wsl) | Where-Object { $_ -match '^\s*(memory|processors|swap)\s*=' }) -join "; " }
else { $r.wslconfig = "none (WSL2 default: half the RAM)" }
try {
    $r.docker_mem_gb = [math]::Round([double]((& docker info --format "{{.MemTotal}}" | Out-String).Trim()) / 1e9, 1)
    $r.docker_cpus = [int]((& docker info --format "{{.NCPU}}" | Out-String).Trim())
    $r.images = @(& docker image ls --format "{{.Repository}}:{{.Tag}} {{.ID}} {{.CreatedAt}}" | Where-Object { $_ -match '^(cc-|causal-copilot)' })
} catch { $r.docker_error = "$_" }
# What the CPU offers and what OpenBLAS picks when nothing is pinned (the wave runner pins HASWELL on CPUs without AVX-512).
$py = "import json, numpy; from numpy.core._multiarray_umath import __cpu_features__ as f; import threadpoolctl as t; " +
      "print(json.dumps({'numpy': numpy.__version__, 'avx2': f['AVX2'], 'avx512f': f['AVX512F'], " +
      "'blas': [(i.get('internal_api'), i.get('architecture')) for i in t.threadpool_info()]}))"
try {
    $out = (& docker run --rm --network none -e OPENBLAS_CORETYPE= cc-kernel:wave-a python -c $py | Out-String).Trim()
    $r.kernel_image = $out | ConvertFrom-Json
} catch { $r.kernel_image_error = "$_" }
$dst = Join-Path $Research ("manifests\hosts\" + $Name + ".json")
$r | ConvertTo-Json -Depth 5 | Out-File -Encoding ascii $dst
Get-Content $dst
