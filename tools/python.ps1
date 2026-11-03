# Run Python from the local project/workspace environment without requiring py.exe.
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PythonArgs)
$repoRoot = Split-Path -Parent $PSScriptRoot
$workspaceRoot = Split-Path -Parent $repoRoot
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$scratchRoot = Join-Path $workspaceRoot '.tooling\tmp'
New-Item -ItemType Directory -Path $scratchRoot -Force | Out-Null
$env:MILESTONE_TEMP_DIR = $scratchRoot
$env:TMP = $scratchRoot
$env:TEMP = $scratchRoot
$candidates = @(
    (Join-Path $repoRoot '.venv\Scripts\python.exe'),
    (Join-Path $workspaceRoot '.tooling\venv\Scripts\python.exe')
)
foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) {
        & $candidate @PythonArgs
        exit $LASTEXITCODE
    }
}
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 @PythonArgs
    exit $LASTEXITCODE
}
foreach ($name in @('python3', 'python')) {
    $command = Get-Command $name -ErrorAction SilentlyContinue
    if ($command) {
        & $command.Source -c 'import sys' 2>$null
        if ($LASTEXITCODE -eq 0) {
            & $command.Source @PythonArgs
            exit $LASTEXITCODE
        }
    }
}
Write-Error 'No working Python. Create the project environment before running checks.'
exit 1
