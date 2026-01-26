param()
$RequiredVersion = "1.8.0_481"
$DestDir = Join-Path $env:USERPROFILE "Downloads\_psCLI"
$InstallerName = "jre-8u481-windows-x64-online.exe"
$InstallerPath = Join-Path $DestDir $InstallerName
$PrimaryUrl = "https://javadl.oracle.com/webapps/download/AutoDL?BundleId=250878_3d5a2bb8f8d4428bbe94aed7ec7ae784"
$FallbackUrl = "https://archive.org/download/jre-8u481-windows-x64/jre-8u481-windows-x64-online.exe"
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
function Get-JavaVersion {
    try {
        $line = (& java -XshowSettings:properties -version 2>&1 | Select-String -Pattern "java.version") | Select-Object -First 1
        if ($line) {
            $ver = ($line.ToString() -split "=")[1].Trim()
            return $ver
        }
    } catch {}
    return $null
}
function Get-Update($ver) {
    if (-not $ver) { return 0 }
    $parts = $ver -split "_"
    if ($parts.Length -ge 2) { return [int]$parts[1] } else { return 0 }
}
$cur = Get-JavaVersion
$reqUpdate = Get-Update $RequiredVersion
$curUpdate = Get-Update $cur
if ($cur -and $curUpdate -ge $reqUpdate) {
    Flash "DarkGreen" "White" 2
    Write-Host "Java is already up to date ($cur >= $RequiredVersion)."
    exit 0
}
New-Item -ItemType Directory -Force -Path $DestDir | Out-Null
Remove-Item -Force $InstallerPath -ErrorAction SilentlyContinue
$downloaded = $false
for ($i=1; $i -le 3 -and -not $downloaded; $i++) {
    try {
        Invoke-WebRequest -Uri $PrimaryUrl -OutFile $InstallerPath -UseBasicParsing -TimeoutSec 30
        if (Test-Path $InstallerPath) { $downloaded = $true; break }
    } catch {}
    try {
        Invoke-WebRequest -Uri $FallbackUrl -OutFile $InstallerPath -UseBasicParsing -TimeoutSec 30
        if (Test-Path $InstallerPath) { $downloaded = $true; break }
    } catch {}
}
if (-not $downloaded) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($null -ne $winget) {
        $proc = Start-Process -FilePath "winget" -ArgumentList "install --id EclipseAdoptium.Temurin.8.JRE -e --silent --accept-source-agreements --accept-package-agreements" -Wait -PassThru
    } else {
        Flash "DarkRed" "White" 2
        Write-Host "ERROR: Failed to download Java installer and winget not available."
        exit 1
    }
} else {
    $proc = Start-Process -FilePath $InstallerPath -ArgumentList "/s REBOOT=0" -Wait -PassThru
    if ($proc.ExitCode -ne 0) { exit $proc.ExitCode }
}
$after = Get-JavaVersion
$afterUpdate = Get-Update $after
if ($after -and $afterUpdate -ge $reqUpdate) {
    Flash "DarkGreen" "White" 2
    Write-Host "OK: Java installed/updated to $after."
    exit 0
} else {
    Flash "DarkYellow" "Black" 2
    Write-Host "WARN: Java version ($after) is below required ($RequiredVersion)."
    exit 1
}
