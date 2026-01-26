param(
    [switch]$NoVenv
)
$ErrorActionPreference = "Stop"
Write-Host "== psCLI.Tool setup ==" -ForegroundColor Cyan

function Ensure-Dir($path) {
    if (-not [string]::IsNullOrWhiteSpace($path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }
}
function Ensure-File($path, $content = "") {
    $dir = Split-Path $path -Parent
    Ensure-Dir $dir
    if (-not (Test-Path $path)) {
        Set-Content -Path $path -Value $content -Encoding UTF8
    }
}

# 1) Python and venv
function Ensure-Python() {
    try {
        $v = & python -V 2>&1
        Write-Host "Python detected: $v" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "Python not found. Please install Python 3.7+ and re-run." -ForegroundColor Red
        return $false
    }
}
function Ensure-Venv() {
    if ($NoVenv) { return }
    $venv = Join-Path $PSScriptRoot ".venv"
    if (-not (Test-Path $venv)) {
        Write-Host "Creating virtual environment at .venv ..." -ForegroundColor Yellow
        & python -m venv $venv
    }
    $pip = Join-Path $venv "Scripts\\pip.exe"
    if (Test-Path $pip) {
        & $pip install --upgrade pip
        & $pip install pyinstaller
    } else {
        Write-Host "pip not found in venv; installing pyinstaller globally" -ForegroundColor Yellow
        & python -m pip install --upgrade pip
        & python -m pip install pyinstaller
    }
}

# 2) Create user profile directories and files
$root = Join-Path $env:USERPROFILE ".polsoft"
$cliA = Join-Path $root "psCLI"
$cliB = Join-Path $root "psCli"  # case-insensitive on Windows, keep both for compatibility
Ensure-Dir $cliA
Ensure-Dir $cliB

$paths = @(
    (Join-Path $cliA "Notepad"),
    (Join-Path $cliA "ascii"),
    (Join-Path $cliA "FileList"),
    (Join-Path $cliA "metadata"),
    (Join-Path $cliA "Browser"),
    (Join-Path $cliA "Log"),
    (Join-Path $cliA "reports"),
    (Join-Path $cliB "settings"),
    (Join-Path $cliB "venv"),
    (Join-Path $cliB "network")
)
foreach ($p in $paths) { Ensure-Dir $p }

# Known files
Ensure-File (Join-Path $cliB "aliases.json") "{}"
Ensure-File (Join-Path $cliB "settings\\terminal.json") "{`"network`":{`"preferred_adapter`":null}}"
Ensure-File (Join-Path $cliB "settings\\protected.json") "{}"
Ensure-File (Join-Path $cliA "Calculator\\history.txt") ""
Ensure-File (Join-Path $cliA "Log\\List.log") ""

# 3) HTML assets (Pico.css + Highlight.js)
$assets = Join-Path (Join-Path $cliA "reports") "assets"
$cssDir = Join-Path $assets "css"
$jsDir = Join-Path $assets "js"
Ensure-Dir $cssDir
Ensure-Dir $jsDir
$urls = @{
    "css/pico.min.css"     = "https://unpkg.com/@picocss/pico@latest/css/pico.min.css";
    "css/highlight.min.css"= "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/default.min.css";
    "js/highlight.min.js"  = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js";
}
foreach ($rel in $urls.Keys) {
    $dest = Join-Path $assets ($rel -replace '/', [System.IO.Path]::DirectorySeparatorChar)
    Ensure-Dir (Split-Path $dest -Parent)
    try {
        Invoke-WebRequest -Uri $urls[$rel] -OutFile $dest -UseBasicParsing -TimeoutSec 60
    } catch {
        if ($rel.EndsWith(".css")) { Set-Content -Path $dest -Value "/* fallback */ body{font-family:Segoe UI,Consolas,Courier New,monospace}" -Encoding UTF8 }
        else { Set-Content -Path $dest -Value "/* fallback */" -Encoding UTF8 }
    }
}

# 4) Optional: ensure version.txt exists for build.ps1 (skip if already present)
$versionTxt = Join-Path $PSScriptRoot "version.txt"
if (-not (Test-Path $versionTxt)) {
    $ver = "3.1.0.0"
    $content = @"
VSVersionInfo(
  ffi=FixedFileInfo(filevers=(3,1,0,0), prodvers=(3,1,0,0), mask=0x3f, flags=0, OS=0x40004, fileType=0x1, subtype=0, date=(0,0)),
  kids=[StringFileInfo([StringTable('040904B0',[StringStruct('CompanyName','Polsoft ITS'),StringStruct('FileDescription','TERMINAL CLI'),StringStruct('FileVersion','$ver'),StringStruct('ProductName','TERMINAL CLI'),StringStruct('ProductVersion','$ver'),StringStruct('OriginalFilename','psCLI.exe'),StringStruct('InternalName','psCLI'),StringStruct('LegalCopyright','© 2026 Polsoft')])]),VarFileInfo([VarStruct('Translation',[1033,1200])])]
)
"@
    Set-Content -Path $versionTxt -Value $content -Encoding UTF8
}

# Execute
if (Ensure-Python) {
    Ensure-Venv
    Write-Host "Setup complete." -ForegroundColor Green
    Write-Host "Directories prepared under: $root"
    Write-Host "HTML assets stored in: $assets"
} else {
    exit 1
}
