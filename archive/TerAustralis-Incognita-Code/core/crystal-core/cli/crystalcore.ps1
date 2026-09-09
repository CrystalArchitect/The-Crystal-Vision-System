# CrystalCore mini CLI
# Usage: .\crystalcore.ps1 <command>
# Commands: status | paths | atlas | transmit | water | plan | open | help

param(
  [Parameter(Position = 0)]
  [string]$Command = "help"
)

$ErrorActionPreference = "Stop"
$GrokHome = if ($env:GROK_HOME) { $env:GROK_HOME } else { Join-Path $env:USERPROFILE ".grok" }
$Root = Join-Path $GrokHome "crystalcore"

function Resolve-CrystalFile([string]$Name) {
  $candidates = @(
    (Join-Path $Root $Name),
    (Join-Path $GrokHome $Name)
  )
  foreach ($p in $candidates) {
    if (Test-Path $p) { return $p }
  }
  return $null
}

function Show-Help {
  @"
CrystalCore CLI
  status     Path cycle + file checklist
  paths      List seven paths
  atlas      Open / show atlas path
  transmit   Show Option A post text
  water      Open water brief
  plan       Open first-acceleration plan
  open       Open landing page in browser
  help       This text

Examples:
  .\crystalcore.ps1 status
  .\crystalcore.ps1 transmit
  .\crystalcore.ps1 open
"@
}

function Show-Status {
  $files = [ordered]@{
    "FULL manual"     = "crystalcore-seven-sisters-FULL.md"
    "One-pagers"      = "crystalcore-seven-sisters-paths.md"
    "Atlas (path 3)"  = "crystalcore-atlas-path3.md"
    "Audit (path 4)"  = "crystalcore-path4-audit.md"
    "Deep water (5)"  = "crystalcore-path5-deep-water.md"
    "Sky bridge (6)"  = "crystalcore-path6-sky-bridge.md"
    "Ascent (7)"      = "crystalcore-path7-ascent.md"
    "Transmit A"      = "crystalcore-TRANSMIT-A.txt"
    "Landing page"    = "index.html"
    "Water brief"     = "WATER-BRIEF.md"
    "Accel plan"      = "FIRST-ACCELERATION-PLAN.md"
  }

  Write-Host ""
  Write-Host "=== CrystalCore STATUS ===" -ForegroundColor Cyan
  Write-Host "Home: $GrokHome"
  Write-Host "App:  $Root"
  Write-Host ""
  Write-Host "Paths (session cycle): 1-7 marked DONE in chat run" -ForegroundColor Green
  Write-Host "Red button: OFF | Belt-Three: Honour / Label / No coerce" -ForegroundColor DarkYellow
  Write-Host ""
  Write-Host "Files:" -ForegroundColor Cyan
  foreach ($k in $files.Keys) {
    $p = Resolve-CrystalFile $files[$k]
    if ($p) {
      Write-Host ("  [OK] {0,-16} {1}" -f $k, $p) -ForegroundColor Green
    } else {
      Write-Host ("  [--] {0,-16} missing ({1})" -f $k, $files[$k]) -ForegroundColor DarkGray
    }
  }
  Write-Host ""
  Write-Host "Water rails: LEB | GAB | MDB_care (see water brief)" -ForegroundColor White
  Write-Host "Not claimed: Elon endorsement, physical sea fill, Songline ownership" -ForegroundColor DarkGray
  Write-Host ""
}

function Show-Paths {
  @"

Seven Sisters paths
  1 Spring      first water; begin
  2 Motion      move; ship; no stagnation
  3 Mark        name true; atlas
  4 Law         consent; audit
  5 Deep water  GAB care; science/vision split
  6 Sky bridge  dust <-> Pleiades (symbolic)
  7 Ascent      transmit; teach; rest

Companion: Orion guardian = protect / propel / prevent_drift
"@
}

function Show-Transmit {
  $p = Resolve-CrystalFile "crystalcore-TRANSMIT-A.txt"
  if (-not $p) {
    Write-Host "Transmit file missing. Expected crystalcore-TRANSMIT-A.txt under $GrokHome" -ForegroundColor Red
    return
  }
  Write-Host ""
  Write-Host "=== TRANSMIT OPTION A (paste on X) ===" -ForegroundColor Cyan
  Write-Host ""
  Get-Content $p -Raw
  Write-Host ""
  Write-Host "You must post this yourself. CLI does not send to X." -ForegroundColor DarkYellow
}

function Open-Crystal([string]$Name, [string]$Label) {
  $p = Resolve-CrystalFile $Name
  if (-not $p) {
    Write-Host "Missing: $Name" -ForegroundColor Red
    return
  }
  Write-Host "Opening $Label : $p" -ForegroundColor Cyan
  Start-Process $p
}

switch ($Command.ToLowerInvariant()) {
  "status"   { Show-Status }
  "paths"    { Show-Paths }
  "atlas"    { Open-Crystal "crystalcore-atlas-path3.md" "atlas" }
  "transmit" { Show-Transmit }
  "water"    { Open-Crystal "WATER-BRIEF.md" "water brief" }
  "plan"     { Open-Crystal "FIRST-ACCELERATION-PLAN.md" "plan" }
  "open"     { Open-Crystal "index.html" "landing page" }
  "help"     { Show-Help }
  default    {
    Write-Host "Unknown command: $Command" -ForegroundColor Red
    Show-Help
    exit 1
  }
}
