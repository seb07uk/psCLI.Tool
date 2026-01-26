param()
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$DestDir = Join-Path $env:USERPROFILE "Downloads\_psCLI"
$X64Url = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
$X86Url = "https://aka.ms/vs/17/release/vc_redist.x86.exe"
$X64Path = Join-Path $DestDir "vc_redist.x64.exe"
$X86Path = Join-Path $DestDir "vc_redist.x86.exe"

function Flash {
    param($bg="DarkGreen",$fg="White",$sec=2)
    $pbg = [Console]::BackgroundColor
    $pfg = [Console]::ForegroundColor
    try {
        [Console]::BackgroundColor = $bg
        [Console]::ForegroundColor = $fg
        Clear-Host
        Start-Sleep -Seconds $sec
    } finally {
        [Console]::BackgroundColor = $pbg
        [Console]::ForegroundColor = $pfg
        Clear-Host
    }
}

function Get-VCState($arch) {
    $key = "HKLM:\SOFTWARE\Microsoft\VisualStudio\VC\Runtimes\{0}" -f $arch
    $installed = 0
    $version = $null
    try {
        $props = Get-ItemProperty -Path $key -ErrorAction Stop
        $installed = [int]($props.Installed)
        $version = $props.Version
    } catch {}
    [PSCustomObject]@{Installed=$installed;Version=$version}
}

function Compare-Version($a,$b) {
    if(-not $a){return -1}
    if(-not $b){return 1}
    $pa = ($a -split '\.')
    $pb = ($b -split '\.')
    for($i=0;$i -lt [Math]::Max($pa.Length,$pb.Length);$i++){
        $va = if($i -lt $pa.Length){[int]$pa[$i]}else{0}
        $vb = if($i -lt $pb.Length){[int]$pb[$i]}else{0}
        if($va -gt $vb){return 1}
        if($va -lt $vb){return -1}
    }
    return 0
}

$os64 = [Environment]::Is64BitOperatingSystem
$stateX64 = Get-VCState "X64"
$stateX86 = Get-VCState "X86"

function Get-LatestVersionWinget($pkgId) {
    try {
        $out = winget show --id $pkgId -e | Out-String
        $m = [regex]::Match($out, "(?m)^\s*Version:\s*([0-9\.]+)")
        if($m.Success){ return $m.Groups[1].Value.Trim() }
    } catch {}
    return $null
}

function Get-FileVersion($path) {
    try { return (Get-Item $path).VersionInfo.FileVersion } catch { return $null }
}

New-Item -ItemType Directory -Force -Path $DestDir | Out-Null

function Try-Download($url,$out){
    for($i=1;$i -le 3;$i++){
        try{
            Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing -TimeoutSec 60
            if(Test-Path $out){ return $true }
        }catch{}
        Start-Sleep -Seconds 1
    }
    return $false
}

# Ustal najnowsze wersje dostępne (preferuj winget; fallback: pobierz i odczytaj wersję z pliku)
$winget = Get-Command winget -ErrorAction SilentlyContinue
$latestX64 = $null
$latestX86 = $null
if($null -ne $winget){
    if($os64){ $latestX64 = Get-LatestVersionWinget "Microsoft.VCRedist.2015+.x64" }
    $latestX86 = Get-LatestVersionWinget "Microsoft.VCRedist.2015+.x86"
}

if(-not $latestX64 -and $os64){
    Remove-Item -Force $X64Path -ErrorAction SilentlyContinue
    if(Try-Download $X64Url $X64Path){ $latestX64 = Get-FileVersion $X64Path }
}
if(-not $latestX86){
    Remove-Item -Force $X86Path -ErrorAction SilentlyContinue
    if(Try-Download $X86Url $X86Path){ $latestX86 = Get-FileVersion $X86Path }
}

# Jeżeli nie udało się ustalić wersji, uprzejmie przerwij
if(($os64 -and -not $latestX64) -or (-not $latestX86)){
    Write-Host "ERROR: Nie można ustalić najnowszej wersji Visual C++ Redistributable."
    exit 1
}

# Oceń potrzebę aktualizacji
$needX64 = $false
$needX86 = $false
if($os64){
    $needX64 = (Compare-Version $stateX64.Version $latestX64) -lt 0
}
$needX86 = (Compare-Version $stateX86.Version $latestX86) -lt 0

# Informacja gdy brak potrzeby
if(($os64 -and -not $needX64) -and (-not $needX86)){
    Write-Host "Brak potrzeby aktualizacji: zainstalowane wersje >= najnowszych."
    Write-Host ("Zainstalowane: x64={0}, x86={1}" -f ($stateX64.Version), ($stateX86.Version))
    Write-Host ("Najnowsze:    x64={0}, x86={1}" -f ($latestX64), ($latestX86))
    exit 0
}
$os64 = [Environment]::Is64BitOperatingSystem
# Pobierz instalatory tylko dla potrzebnych architektur (jeśli nie pobrano wcześniej)
if($needX64){
    if(-not (Test-Path $X64Path)){
        Remove-Item -Force $X64Path -ErrorAction SilentlyContinue
        if(-not (Try-Download $X64Url $X64Path)){ Write-Host "ERROR: Pobieranie x64 nie powiodło się."; exit 1 }
    }
}
if($needX86){
    if(-not (Test-Path $X86Path)){
        Remove-Item -Force $X86Path -ErrorAction SilentlyContinue
        if(-not (Try-Download $X86Url $X86Path)){ Write-Host "ERROR: Pobieranie x86 nie powiodło się."; exit 1 }
    }
}
$exit = 0
$attempted = $needX64 -or $needX86
if($needX64){
    $p = Start-Process -FilePath $X64Path -ArgumentList "/install /quiet /norestart" -Wait -PassThru
    if($p.ExitCode -ne 0){ $exit = $p.ExitCode }
}
if($needX86){
    $p = Start-Process -FilePath $X86Path -ArgumentList "/install /quiet /norestart" -Wait -PassThru
    if($p.ExitCode -ne 0){ $exit = $p.ExitCode }
}
$stateX64 = Get-VCState "X64"
$stateX86 = Get-VCState "X86"
$finalOkX64 = -not $needX64 -or ((Compare-Version $stateX64.Version $latestX64) -ge 0)
$finalOkX86 = -not $needX86 -or ((Compare-Version $stateX86.Version $latestX86) -ge 0)
# Jeżeli instalacja była wykonywana i zakończyła się powodzeniem (exit==0), przyjmij sukces
if($attempted -and $exit -eq 0){
    Flash "DarkGreen" "White" 2
    Write-Host "OK: Microsoft Visual C++ 2015-2022 zainstalowano/zaktualizowano."
    exit 0
}
if(($os64 -and $finalOkX64) -and $finalOkX86){
    Flash "DarkGreen" "White" 2
    Write-Host "OK: Microsoft Visual C++ 2015-2022 zainstalowano/zaktualizowano."
    exit 0
} else {
    Flash "DarkYellow" "Black" 2
    Write-Host "WARN: Instalacja niepełna."
    exit $exit
}
