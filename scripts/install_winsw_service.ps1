<#
Install the Streamlit app as a Windows Service using WinSW (Windows Service Wrapper).

This script will:
- Download winsw-x64.exe into `scripts\winsw\<ServiceName>.exe` (from GitHub releases)
- Create a `<ServiceName>.xml` alongside the exe with a runnable wrapper that executes
    the existing `scripts\start_e10_app.bat` via `cmd.exe /c`.
- Optionally install the service and start it.

Usage (elevated PowerShell):
  .\scripts\install_winsw_service.ps1 -ServiceName E10AppService -DisplayName "E10 App Service" -Install

Important:
- This script does not embed passwords in plain text by default. If you need the
  service to run as a specific user, provide `-ServiceUser` and `-ServicePassword`.
- Review the generated XML before installing.
#>

param(
    [Parameter(Mandatory=$false)][string]$ServiceName = "E10AppService",
    [Parameter(Mandatory=$false)][string]$DisplayName = "E10 App Service",
    [Parameter(Mandatory=$false)][string]$Description = "E10 App Service wrapper",
    [Parameter(Mandatory=$false)][string]$ExecBatch = "scripts\start_e10_app.bat",
    [Parameter(Mandatory=$false)][switch]$Install,
    [Parameter(Mandatory=$false)][string]$ServiceUser = "",
    [Parameter(Mandatory=$false)][string]$ServicePassword = ""
)

. "$PSScriptRoot\common.ps1" 2>$null
if (-not (Test-Path (Join-Path $PSScriptRoot 'common.ps1'))) {
    Write-Warning "common.ps1 not found in $PSScriptRoot; using local fallbacks for Ensure-Strict and Assert-Admin."
    function Ensure-Strict { return }
    function Assert-Admin {
        $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        if (-not $isAdmin) { Write-Warning "Not running as Administrator; some operations may fail." }
    }
}
Ensure-Strict
Assert-Admin

$repoRoot = Split-Path -Parent $PSScriptRoot
$execPath = (Resolve-Path -Path (Join-Path $repoRoot $ExecBatch)).ProviderPath

$winswDir = Join-Path $PSScriptRoot "winsw"
if (-not (Test-Path $winswDir)) { New-Item -Path $winswDir -ItemType Directory | Out-Null }

# Normalize legacy/canonical service names to avoid creating duplicate wrappers
if ($ServiceName -in @('E10App','E10 App Win')) {
    Write-Warning "Legacy service name '$ServiceName' detected. Using canonical 'E10AppService' instead."
    $ServiceName = 'E10AppService'
}

# Cleanup legacy winsw artifacts (if present) to prevent duplicate/conflicting wrappers
$legacyExe = Join-Path $winswDir 'E10App.exe'
$legacyXml = Join-Path $winswDir 'E10App.xml'
if (Test-Path $legacyExe) {
    try {
        Remove-Item $legacyExe -Force -ErrorAction Stop
        Write-Host "Removed legacy winsw binary: $legacyExe"
    } catch {
        Write-Warning ("Unable to remove legacy winsw binary {0}: {1}" -f $legacyExe, $_)
    }
}
if (Test-Path $legacyXml) {
    try {
        Remove-Item $legacyXml -Force -ErrorAction Stop
        Write-Host "Removed legacy winsw xml: $legacyXml"
    } catch {
        Write-Warning ("Unable to remove legacy winsw xml {0}: {1}" -f $legacyXml, $_)
    }
}

$exeName = "$ServiceName.exe"
$exePath = Join-Path $winswDir $exeName
$xmlPath = [IO.Path]::ChangeExtension($exePath, '.xml')

Write-Host "Preparing WinSW wrapper in: $winswDir"

# Download WinSW if missing
if (-not (Test-Path $exePath)) {
    Write-Host "Downloading WinSW (latest x64) to $exePath"
    $latestUrl = 'https://github.com/winsw/winsw/releases/latest/download/winsw-x64.exe'
    try {
        Invoke-WebRequest -Uri $latestUrl -OutFile $exePath -UseBasicParsing -ErrorAction Stop
    } catch {
        throw "Failed to download WinSW from $latestUrl : $_"
    }
}

Write-Host "Generating service XML: $xmlPath"

$accountXml = ''
if ($ServiceUser -and $ServicePassword) {
    $escapedUser = [System.Security.SecurityElement]::Escape($ServiceUser)
    $escapedPass = [System.Security.SecurityElement]::Escape($ServicePassword)
    $accountXml = "<serviceaccount><user>$escapedUser</user><password>$escapedPass</password></serviceaccount>"
}

$xml = @"
<service>
  <id>$ServiceName</id>
  <name>$DisplayName</name>
  <description>$Description</description>
  <executable>cmd.exe</executable>
  <arguments>/c `"$execPath`"</arguments>
  <logpath>..\logs\$ServiceName</logpath>
  <log mode="roll">true</log>
  $accountXml
  <onfailure action="restart" delay="5000" />
</service>
"@

[IO.File]::WriteAllText($xmlPath, $xml)

Write-Host "Created $xmlPath"

if ($Install.IsPresent) {
    Write-Host "Installing service via WinSW: $exePath install"
    Push-Location $winswDir
    try {
        & "$exePath" install
        if ($LASTEXITCODE -ne 0) { throw "WinSW install returned exit $LASTEXITCODE" }
        & "$exePath" start
    } finally {
        Pop-Location
    }
    Write-Host "Service installed and started. Use 'Get-Service -Name $ServiceName' to check status."
} else {
    Write-Host "Sketched wrapper created. To install run (elevated):"
    Write-Host "  Push-Location '$winswDir' ; .\\$exeName install ; .\\$exeName start"
}
