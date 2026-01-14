# Hash Index Tool - Configuration Guide

## Configuration Files

### .hashignore File

Create a `.hashignore` file in your project root to exclude specific patterns:

```
# Build artifacts
bin/
obj/
*.exe
*.dll

# Temporary files
*.tmp
*.temp
.cache/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
logs/

# Dependencies
node_modules/
vendor/
packages/

# OS files
.DS_Store
Thumbs.db
```

### .gitignore Integration

The tool automatically respects `.gitignore` files when `-UseGitIgnore` is specified:

```powershell
.\hash-index.ps1 -Path "." -UseGitIgnore
```

## Environment Variables

### Python Configuration

```powershell
# Set Python executable path
$env:PYTHON_PATH = "C:\Python39\python.exe"

# Use virtual environment
$env:VIRTUAL_ENV = "C:\project\.venv"
```

### Performance Tuning

```powershell
# Maximum parallel jobs (default: min(8, CPU cores))
$env:HASH_INDEX_MAX_JOBS = "16"

# Database timeout in seconds
$env:HASH_INDEX_DB_TIMEOUT = "30"
```

## Database Configuration

### SQLite Database Schema

The tool creates a comprehensive database structure:

```sql
-- File history tracking
CREATE TABLE file_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT NOT NULL,
    hash_value TEXT NOT NULL,
    algorithm TEXT NOT NULL,
    file_size INTEGER,
    modified_time TEXT,
    scan_time TEXT NOT NULL,
    git_commit TEXT,
    git_tag TEXT,
    metadata TEXT
);

-- Scan session tracking
CREATE TABLE scan_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scan_time TEXT NOT NULL,
    root_path TEXT NOT NULL,
    algorithm TEXT NOT NULL,
    file_count INTEGER,
    total_size INTEGER,
    duration_seconds REAL,
    git_commit TEXT,
    git_tag TEXT,
    release_version TEXT
);

-- Metadata storage
CREATE TABLE metadata_store (
    file_path TEXT PRIMARY KEY,
    content_type TEXT,
    encoding TEXT,
    dimensions TEXT,
    duration REAL,
    author TEXT,
    title TEXT,
    subject TEXT,
    keywords TEXT,
    created_date TEXT,
    modified_date TEXT,
    extra_metadata TEXT
);

-- Frequency signatures (experimental)
CREATE TABLE frequency_signatures (
    file_path TEXT PRIMARY KEY,
    dct_coefficients TEXT,
    fft_peaks TEXT,
    spectral_centroid REAL,
    spectral_rolloff REAL,
    zero_crossing_rate REAL,
    entropy REAL,
    signature_time TEXT
);
```

### Database Performance

Optimize database performance for large datasets:

```powershell
# Vacuum database periodically
sqlite3 .hash-index.db "VACUUM;"

# Analyze query performance
sqlite3 .hash-index.db "ANALYZE;"

# Backup database
copy-item .hash-index.db .hash-index.db.backup
```

## Algorithm Selection

### Security Levels

Choose algorithms based on your security requirements:

```powershell
# Standard security (recommended)
.\hash-index.ps1 -Algorithm SHA256

# High security
.\hash-index.ps1 -Algorithm SHA512

# Performance optimized
.\hash-index.ps1 -Algorithm BLAKE2B

# Legacy compatibility
.\hash-index.ps1 -Algorithm SHA1
```

### Multi-Algorithm Verification

Use multiple algorithms for comprehensive verification:

```powershell
# Run all algorithms sequentially
.\hash-index.ps1 -All

# Manual multi-algorithm approach
@("SHA256", "BLAKE2B") | ForEach-Object {
    .\hash-index.ps1 -Path "." -Algorithm $_
}
```

## Performance Configuration

### Parallel Processing

Configure parallel processing for optimal performance:

```powershell
# Enable parallel verification
.\hash-index.ps1 -Path "." -ParallelVerify

# Process large datasets
.\hash-index.ps1 -Path "." -ParallelVerify -MinFileSize 1024

# Memory-conscious processing
.\hash-index.ps1 -Path "." -MaxFileSize 100MB
```

### Memory Management

Optimize memory usage for large files:

```powershell
# Skip large files
.\hash-index.ps1 -Path "." -MaxFileSize 1GB

# Process only significant files
.\hash-index.ps1 -Path "." -MinFileSize 1KB

# Sequential processing for memory constraints
.\hash-index.ps1 -Path "." -Algorithm SHA256  # Avoids parallel jobs
```

## Output Configuration

### Report Customization

Configure report generation:

```powershell
# HTML report with custom format
.\hash-index.ps1 -Path "." -GenerateReport -ReportFormat HTML

# JSON export for automation
.\hash-index.ps1 -Path "." -ExportJSON

# CSV for spreadsheet analysis
.\hash-index.ps1 -Path "." -ExportCSV
```

### SBOM Configuration

Configure Software Bill of Materials generation:

```powershell
# Standard SBOM
.\hash-index.ps1 -Path "." -GenerateSBOM

# Release-specific SBOM
.\hash-index.ps1 -Path "." -GenerateSBOM -ReleaseVersion "v2.1.0" -ReleaseTitle "Production Release"

# Custom manifest version
.\hash-index.ps1 -Path "." -GenerateSBOM -ManifestVersion "2.2"
```

## Security Configuration

### GPG Signing

Configure GPG signing for integrity proofs:

```powershell
# Basic signing
.\hash-index.ps1 -Path "." -SignWithGPG

# Verify signatures
gpg --verify SHA256SUMS.txt.asc SHA256SUMS.txt
```

### Timestamp Proofs

Configure OpenTimestamps for time-based proofs:

```powershell
# Create timestamp proof
.\hash-index.ps1 -Path "." -TimestampProof

# Verify timestamp
ots verify SHA256SUMS.txt.ots
```

## Experimental Features

### Frequency Analysis Configuration

Configure experimental frequency analysis:

```powershell
# Basic frequency signatures
.\hash-index.ps1 -Path "." -FrequencySignature

# Comprehensive analysis
.\hash-index.ps1 -Path "." -FrequencySignature -EntropyAnalysis -PerceptualHash

# Research-grade analysis
.\hash-index.ps1 -Path "." -All -EnableHistory
```

### Advanced Signal Processing

Tune signal processing parameters:

```powershell
# Note: Advanced parameters require code modification
# Sample size: 64KB default (modify in Get-FrequencySignature function)
# DCT coefficients: 32 default (modify in Get-SimplifiedDCT function)
# Grid size: 8x8 default (modify in Get-PerceptualHash function)
```

## Integration Configuration

### CI/CD Integration

Configure for continuous integration:

```yaml
# GitHub Actions example
- name: Verify Integrity
  run: |
    .\hash-index.ps1 -Path "." -Verify
    if ($LASTEXITCODE -ne 0) { exit 1 }

- name: Generate Provenance
  run: |
    .\hash-index.ps1 -Path "." -GenerateSBOM -SignWithGPG -ReleaseVersion "${{ github.ref_name }}"
```

### Scheduled Tasks

Configure automated integrity checks:

```powershell
# Daily verification
$trigger = New-ScheduledTaskTrigger -Daily -At 2AM
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\tools\hash-index.ps1 -Path C:\data -Verify"
Register-ScheduledTask -TaskName "DailyIntegrity" -Trigger $trigger -Action $action

# Weekly comprehensive scan
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 3AM
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\tools\hash-index.ps1 -Path C:\data -All"
Register-ScheduledTask -TaskName "WeeklyComprehensive" -Trigger $trigger -Action $action
```

## Troubleshooting Configuration

### Debug Configuration

Enable comprehensive logging:

```powershell
# Verbose logging
.\hash-index.ps1 -Path "." -Verbose

# Log file analysis
Get-Content .hash-index.log | Select-String "ERROR|WARN"

# Performance profiling
Measure-Command { .\hash-index.ps1 -Path "." }
```

### Common Configuration Issues

```powershell
# Python not found
$env:PYTHON_PATH = "C:\Python39\python.exe"
.\hash-index.ps1 -Path "." -Algorithm BLAKE2B

# Database locked
Remove-Item .hash-index.db -Force
.\hash-index.ps1 -Path "." -EnableHistory

# Permission denied
# Run PowerShell as Administrator
# or adjust file permissions
```

## Best Practices

### Project Configuration

1. Create `.hashignore` file for project-specific exclusions
2. Use `.gitignore` integration for consistency
3. Configure appropriate algorithm for security requirements
4. Set up automated verification in CI/CD

### Performance Optimization

1. Use parallel processing for large datasets
2. Configure appropriate file size limits
3. Exclude unnecessary files and directories
4. Use incremental updates with sidecar files

### Security Hardening

1. Use multiple algorithms for critical data
2. Enable GPG signing for release artifacts
3. Implement timestamp proofs for long-term verification
4. Regular database backups and integrity checks

---

## Operational Maintenance 🛠️

### Database Maintenance

- **Vacuum & Analyze** periodically to keep SQLite performant:

```powershell
sqlite3 .hash-index.db "VACUUM;"
sqlite3 .hash-index.db "ANALYZE;"
```

- **Backup** your database before schema or tool upgrades:

```powershell
Copy-Item -LiteralPath .hash-index.db -Destination .hash-index.db.bak -Force
```

### Python & Virtualenv Best Practices

- Create a project `.venv` and ensure PowerShell sees it using `VIRTUAL_ENV`.
- Pin Python and library versions with a `requirements.txt` for reproducibility.

```powershell
python -m venv .venv
.\.venv\Scripts\pip install --upgrade pip
pip install -r requirements.txt
```

### Logging & Retention

- Rotate or archive `.hash-index.log` periodically. Example rotation script:

```powershell
if ((Get-Item .hash-index.log).Length -gt 10MB) { Move-Item .hash-index.log ".logs\hash-index-$(Get-Date -Format yyyyMMdd-HHmmss).log" }
```

### Monitoring

- Configure a scheduled task or monitoring job to run a verification and alert on failures via your team's alerting system (email, webhook, etc.).

---

## Security Notes

- Restrict access to the database and metadata directories using filesystem ACLs.
- Keep signing keys in secure HSMs or protected keyrings; avoid checking secrets into source control.

---

## Troubleshooting Checklist

1. Check `.hash-index.log` for ERROR/WARN
2. Ensure Python is available for BLAKE2B and DB operations
3. Check file permissions
4. Re-run with `-Verbose` and inspect the HTML/JSON exports for insights
