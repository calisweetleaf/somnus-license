<#
.SYNOPSIS
    Test script to verify Python Production Doctor setup

.DESCRIPTION
    Runs the production doctor on itself to generate a test report
#>

param(
    [string]$ConfigFile = "DOCTOR_CONFIG.json",
    [string]$OutputFile = "test_report.md"
)

$ErrorActionPreference = 'Stop'

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Python Production Doctor - Test Run" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "❌ Python not found in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python found: $($python.Source)" -ForegroundColor Green

# Check if main script exists
$scriptPath = Join-Path $PSScriptRoot "python_production_doctor.py"
if (-not (Test-Path $scriptPath)) {
    Write-Host "❌ python_production_doctor.py not found" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Main script found" -ForegroundColor Green

# Check if config exists
$configPath = Join-Path $PSScriptRoot $ConfigFile
if (-not (Test-Path $configPath)) {
    Write-Host "❌ Config file $ConfigFile not found" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Config file found: $ConfigFile" -ForegroundColor Green

# Run the doctor
Write-Host ""
Write-Host "Running analysis..." -ForegroundColor Yellow
Write-Host ""

try {
    # Use UTF-8 encoding to avoid Unicode issues
    $env:PYTHONUTF8 = 1
    
    & python $scriptPath $PSScriptRoot `
        -c $configPath `
        -o $OutputFile `
        -j 2
    
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Cyan
    
    if (Test-Path $OutputFile) {
        $reportSize = (Get-Item $OutputFile).Length
        Write-Host "✓ Report generated: $OutputFile ($($reportSize) bytes)" -ForegroundColor Green
        
        # Show summary from the report
        Write-Host ""
        Write-Host "Report Preview:" -ForegroundColor Cyan
        Write-Host "----------------------------------------" -ForegroundColor Gray
        $first20Lines = Get-Content $OutputFile -TotalCount 20
        $first20Lines | ForEach-Object { Write-Host $_ }
        Write-Host "..." -ForegroundColor Gray
        Write-Host "----------------------------------------" -ForegroundColor Gray
    }
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Host "✓ Analysis completed successfully (Exit code: $exitCode)" -ForegroundColor Green
        Write-Host "  No critical issues found!" -ForegroundColor Green
    } else {
        Write-Host "⚠ Analysis completed with issues (Exit code: $exitCode)" -ForegroundColor Yellow
        Write-Host "  Critical issues were found - check the report" -ForegroundColor Yellow
    }
    
    Write-Host "==========================================" -ForegroundColor Cyan
    
    exit $exitCode
    
} catch {
    Write-Host ""
    Write-Host "❌ Error running analysis: $_" -ForegroundColor Red
    exit 1
}
