Param(
    [switch]$NoStrict,        # skip strict provenance checks if set
    [switch]$SkipManifest,     # skip regenerating file_manifest if set
    [string]$ZipName           # optional custom zip name or path
)

# Resolve repo root (this script lives in .\code\)
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo
Write-Host "Repo root: $repo" -ForegroundColor Cyan

# 0) Rebuild the file manifest (CSV + pretty MD) unless skipped
if (-not $SkipManifest) {
    Write-Host "Rebuilding file manifest..." -ForegroundColor Yellow
    $LASTEXITCODE = 0
    & python .\code\build_manifest.py
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Manifest build failed. Aborting."
        exit 1
    }
}

# 1) Validate (strict by default)
$validateCmd = "python .\code\run_all.py --validate"
if (-not $NoStrict) { $validateCmd += " --strict" }
Write-Host "Running: $validateCmd" -ForegroundColor Yellow
$LASTEXITCODE = 0
& cmd /c $validateCmd
if ($LASTEXITCODE -ne 0) {
    Write-Error "Validation failed. Aborting."
    exit 1
}

# 2) Refresh checksums (ASCII file for cross-platform stability)
Write-Host "Refreshing checksums/SHA256SUMS..." -ForegroundColor Yellow
Get-FileHash -Algorithm SHA256 -Path `
  .\data\*.csv, `
  .\dictionaries\*.csv, `
  .\code\run_all.py, `
  .\code\build_manifest.py, `
  .\code\environment.yml, `
  .\code\requirements.txt, `
  .\metadata\zenodo.json, `
  .\metadata\file_manifest.csv, `
  .\docs\readme_*.md, `
  .\docs\FILE_MANIFEST.md, `
  .\provenance\* `
| ForEach-Object { "{0}  {1}" -f $_.Hash, (Resolve-Path $_.Path -Relative) } `
| Out-File -Encoding ascii .\checksums\SHA256SUMS

# 3) Build zip (one level up, or use custom name if provided)
if ([string]::IsNullOrWhiteSpace($ZipName)) {
    $zipName = "$(Split-Path $repo -Leaf).zip"
    $zipPath = Join-Path (Split-Path $repo -Parent) $zipName
} else {
    if ([System.IO.Path]::IsPathRooted($ZipName)) {
        $zipPath = $ZipName
    } else {
        # relative path -> place one level up
        $zipPath = Join-Path (Split-Path $repo -Parent) $ZipName
    }
}
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Write-Host "Creating zip: $zipPath" -ForegroundColor Yellow
Compress-Archive -Path * -DestinationPath $zipPath -Force

Write-Host ""
Write-Host "SUCCESS ✅  Created $zipPath" -ForegroundColor Green
Write-Host "Hints:" -ForegroundColor DarkGray
Write-Host "  - Add -NoStrict to skip provenance strict checks" -ForegroundColor DarkGray
Write-Host "  - Add -SkipManifest to skip rebuilding the file manifest" -ForegroundColor DarkGray
Write-Host "  - Use -ZipName MyBundle.zip to override the output name" -ForegroundColor DarkGray
