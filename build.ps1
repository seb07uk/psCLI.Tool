param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if ($Clean) {
    Remove-Item -Recurse -Force "$PSScriptRoot\build" -ErrorAction SilentlyContinue
    Remove-Item -Recurse -Force "$PSScriptRoot\dist" -ErrorAction SilentlyContinue
    Get-ChildItem "$PSScriptRoot" -Filter "*.spec" | Remove-Item -Force -ErrorAction SilentlyContinue
}

python -c "import PyInstaller" 2>$null
if ($LASTEXITCODE -ne 0) {
    python -m pip install --upgrade pip
    python -m pip install pyinstaller
}

$datas = @(
    "plugins;plugins",
    "games;games",
    "metadata;metadata",
    "ascii;ascii",
    "health;health",
    "tools;tools",
    "install;install"
)

$pyArgs = @("--noconfirm","--clean","--onefile","--name","psCLI")
foreach ($d in $datas) {
    $pyArgs += @("--add-data", $d)
}
$iconPath = Join-Path $PSScriptRoot "icon.ico"
if (Test-Path $iconPath) {
    $pyArgs += @("--icon", $iconPath)
}
$pyArgs += "cli.py"

& pyinstaller @pyArgs
