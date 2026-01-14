# Hash Index Tool - Command Reference

## Quick Start Commands

### Basic Operations

```powershell
# Generate SHA256 checksums for current directory
.\hash-index.ps1

# Generate checksums for specific directory
.\hash-index.ps1 -Path "C:\project"

# Use different algorithm
.\hash-index.ps1 -Algorithm BLAKE2B

# Verify existing checksums
.\hash-index.ps1 -Verify
```

### Production Workflows

```powershell
# Complete integrity check with all features
.\hash-index.ps1 -All

# Generate SBOM and sign with GPG
.\hash-index.ps1 -GenerateSBOM -SignWithGPG

# Research-grade analysis
.\hash-index.ps1 -FrequencySignature -EntropyAnalysis -PerceptualHash
```

## Parameter Reference

### Core Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `-Path` | String | "." | Root directory to scan |
| `-Algorithm` | String | "SHA256" | Hash algorithm (SHA256, SHA1, SHA384, SHA512, BLAKE2B) |
| `-IndexFile` | String | Auto-generated | Output filename for checksums |
| `-SkipExisting` | Switch | False | Skip files with existing sidecar hashes |
| `-UseSidecar` | Switch | False | Read/write hash files next to source files |

### Verification Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-Verify` | Switch | Verify files against existing checksums |
| `-ParallelVerify` | Switch | Use parallel processing for verification |
| `-DiffMode` | Switch | Compare current state with baseline |
| `-DiffWith` | String | Baseline file for comparison |

### Security Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-SignWithGPG` | Switch | Create GPG signature for checksum file |
| `-TimestampProof` | Switch | Create OpenTimestamps proof |

### Metadata Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-ExtractMetadata` | Switch | Extract file metadata |
| `-InjectMetadata` | Switch | Inject metadata into files |
| `-MetadataToInject` | Hashtable | Metadata to inject |

### Experimental Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-FrequencySignature` | Switch | Generate frequency-based signatures |
| `-EntropyAnalysis` | Switch | Calculate entropy metrics |
| `-PerceptualHash` | Switch | Generate perceptual hashes |
| `-DeepArchives` | Switch | Process archive contents |

### History Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-EnableHistory` | Switch | Store results in SQLite database |
| `-ShowHistory` | Switch | Display file history |

### Output Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-GenerateSBOM` | Switch | Generate Software Bill of Materials |
| `-GenerateReport` | Switch | Create HTML report |
| `-ReportFormat` | String | Report format (HTML, JSON) |
| `-ExportJSON` | Switch | Export results to JSON |
| `-ExportCSV` | Switch | Export results to CSV |

### Filtering Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `-Exclude` | String[] | @('.git', '.venv', 'node_modules') | Patterns to exclude |
| `-UseHashIgnore` | Switch | False | Use .hashignore file |
| `-UseGitIgnore` | Switch | False | Use .gitignore file |
| `-MinFileSize` | Int | 0 | Minimum file size in bytes |
| `-MaxFileSize` | Int | 0 | Maximum file size in bytes |

### Advanced Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-All` | Switch | Run all algorithms with all features |
| `-ImportFrom` | String | Import from existing index file |
| `-ManifestVersion` | String | SBOM manifest version |
| `-ReleaseVersion` | String | Release version for metadata |
| `-ReleaseTitle` | String | Release title for metadata |
| `-Verbose` | Switch | Enable verbose logging |

## Algorithm-Specific Outputs

### SHA256 (Default)

- Output: `SHA256SUMS.txt`
- Use case: Standard verification, Git compatibility

### SHA1

- Output: `SHA1SUMS.txt`
- Use case: Legacy system compatibility

### SHA384

- Output: `SHA384SUMS.txt`
- Use case: High-security environments

### SHA512

- Output: `SHA512SUMS.txt`
- Use case: Maximum security requirements

### BLAKE2B

- Output: `BLAKE2BSUMS.txt`
- Use case: Performance-optimized, modern applications

## Feature Combination Examples

### Development Workflow

```powershell
# Quick check during development
.\hash-index.ps1 -Path ".\src" -Algorithm SHA256 -Exclude "*.tmp", "*.log"
```

### Release Process

```powershell
# Complete release verification
.\hash-index.ps1 -Path "." -All -SignWithGPG -TimestampProof -GenerateSBOM -ReleaseVersion "v1.0.0"
```

### Research Analysis

```powershell
# Experimental analysis
.\hash-index.ps1 -Path ".\dataset" -FrequencySignature -EntropyAnalysis -PerceptualHash -ExportJSON
```

### Continuous Integration

```powershell
# CI/CD pipeline
.\hash-index.ps1 -Path "." -Verify -ParallelVerify
if ($LASTEXITCODE -ne 0) { exit 1 }
```

## Output File Structure

### Standard Outputs

```
project/
├── SHA256SUMS.txt          # Checksums
├── SHA256SUMS.txt.asc      # GPG signature
├── SHA256SUMS.txt.ots      # Timestamp proof
├── .hash-index.db          # SQLite database
├── .metadata/              # Extracted metadata
│   └── *.metadata.json
├── .reports/               # Generated reports
│   └── report-*.html
└── .sbom/                  # SBOM files
    └── sbom.spdx.json
```

### Experimental Outputs

```
project/
├── SHA256SUMS.json         # JSON export
├── SHA256SUMS.csv          # CSV export
└── .hash-index.db          # Frequency signatures
```

## Performance Considerations

### Parallel Processing

- Automatically enabled for >10 files
- Configurable via `-ParallelVerify`
- Falls back to sequential if jobs unavailable

### Memory Usage

- Streaming processing for large files
- Configurable sample sizes for analysis
- Efficient metadata caching

### Speed Optimization

- BLAKE2B for fastest hashing
- Skip existing hashes with `-SkipExisting`
- Use sidecar files for incremental updates

## Error Handling

### Common Issues

```powershell
# Python not found (BLAKE2B requires Python)
.\hash-index.ps1 -Algorithm SHA256  # Use native algorithm

# Permission errors
# Run PowerShell as Administrator

# Large file handling
.\hash-index.ps1 -MaxFileSize 1GB  # Limit file size
```

### Debug Mode

```powershell
# Enable verbose logging
.\hash-index.ps1 -Path "." -Verbose

# Check specific file
.\hash-index.ps1 -Path ".\problematic-file.exe" -Verbose
```

## Integration Examples

### PowerShell Script

```powershell
# Automated verification
$result = .\hash-index.ps1 -Path "." -Verify
if ($result -match "FAILED") {
    Write-Error "Integrity check failed"
    exit 1
}
```

### Batch Processing

```powershell
# Process multiple directories
@("project1", "project2", "project3") | ForEach-Object {
    .\hash-index.ps1 -Path $_ -Algorithm BLAKE2B
}
```

### Scheduled Tasks

```powershell
# Daily integrity check
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\tools\hash-index.ps1 -Path C:\important-data -Verify"
$trigger = New-ScheduledTaskTrigger -Daily -At 2AM
Register-ScheduledTask -TaskName "DailyIntegrityCheck" -Action $action -Trigger $trigger

---

## Exit Codes & Return Values ✅

- The script uses standard PowerShell exit conventions:
  - `0` — Success
  - non-zero — Failure (details will be logged to `.hash-index.log`)
- When run in CI, check `$LASTEXITCODE` and parse exported JSON for structured status fields.

## Example Outputs (Short)

- JSON export sample (trimmed):

```json
{
  "Generated": "2026-01-14T12:00:00Z",
  "Algorithm": "SHA256",
  "Files": [
    { "RelativePath": "src/main.ps1", "Hash": "...", "Size": 1234 }
  ]
}
```

- CSV export columns: `RelativePath,Hash,Size,Modified`

## Common FAQs ❓

Q: How do I run only a subset of files?
A: Use `-MinFileSize`/`-MaxFileSize` or combine with `-Exclude` patterns; for fine-grained control, pre-generate a file list and feed it via a script loop.

Q: Can I store multiple algorithm indices side-by-side?
A: Yes — use `-IndexFile` to name outputs per algorithm or use `-All` to produce algorithm-specific index files.

Q: Is the BLAKE2B implementation secure?
A: BLAKE2b is a modern and secure hash; the helper relies on Python's hashlib and streams the file for safety.

---

## Appendix: Troubleshooting Commands

- Inspect log tails:

```powershell
Get-Content .hash-index.log -Tail 200
```

- Re-run a previously failing file only:

```powershell
.\hash-index.ps1 -Path "C:\repo\specific" -Algorithm SHA256 -IgnorePatterns "*.tmp"
```

```
