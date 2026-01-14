# Hash Index Tool - Master Hash Integrity & Provenance System

**License:** [Sovereign Anti-Exploitation Software License](../LICENSE) 🦈

## Overview

The Hash Index Tool (`hash-index.ps1`) is a comprehensive file integrity and provenance system designed for production-grade cryptographic verification, metadata extraction, and experimental frequency-based signatures. This tool represents an advanced approach to file system integrity monitoring with research-oriented features.

## Core Philosophy

This tool implements a multi-layered approach to file integrity that goes beyond traditional hashing. It combines established cryptographic methods with experimental signal processing techniques to create a comprehensive fingerprinting system that can detect both intentional modifications and subtle corruptions.

## Architecture

### Primary Components

1. **Cryptographic Hashing Engine**
   - Multi-algorithm support (SHA256, SHA1, SHA384, SHA512, BLAKE2B)
   - Parallel processing capabilities
   - Sidecar hash file support
   - GPG signature integration

2. **Metadata Extraction System**
   - Content-type detection via magic bytes
   - Format-specific metadata extraction
   - Historical tracking database
   - Cross-reference capabilities

3. **Experimental Frequency Analysis**
   - Signal processing on binary data
   - Entropy calculation
   - Spectral analysis
   - Perceptual hashing

4. **Provenance Tracking**
   - SQLite-backed history
   - Git integration
   - Timestamp proofs
   - SBOM generation

## Installation & Requirements

### Prerequisites

- PowerShell 5.1 or later
- Python 3.x (for BLAKE2B support and SQLite operations)
- Optional: GPG for signing
- Optional: OpenTimestamps client for timestamp proofs

### Quick Setup

```powershell
# Basic integrity check
.\hash-index.ps1 -Path ".\my-project"

# Full feature enablement
.\hash-index.ps1 -Path ".\my-project" -All
```

## Usage Patterns

### Basic Integrity Verification

```powershell
# Generate SHA256 checksums
.\hash-index.ps1 -Path ".\project" -Algorithm SHA256

# Verify existing checksums
.\hash-index.ps1 -Path ".\project" -Verify
```

### Advanced Provenance

```powershell
# Complete provenance with metadata
.\hash-index.ps1 -Path ".\project" -ExtractMetadata -EnableHistory -GenerateSBOM

# Research-grade analysis
.\hash-index.ps1 -Path ".\project" -FrequencySignature -EntropyAnalysis -PerceptualHash
```

### Production Deployment

```powershell
# All algorithms with full provenance
.\hash-index.ps1 -Path ".\project" -All -SignWithGPG -TimestampProof -GenerateReport
```

## Feature Deep Dive

### Cryptographic Hashing

The tool supports multiple hash algorithms, each serving specific use cases:

- **SHA256**: Standard verification, Git compatibility
- **SHA1**: Legacy system compatibility
- **SHA384/SHA512**: High-security environments
- **BLAKE2B**: Performance-optimized, modern applications

### Metadata Extraction

Automatic detection and extraction of metadata from various file types:

- **Documents**: PDF, Office formats
- **Media**: Images, audio, video
- **Archives**: ZIP, TAR, compression formats
- **Executables**: PE metadata, version information

### Experimental Frequency Signatures

Advanced signal processing techniques applied to binary data:

- **Entropy Analysis**: Information density measurement
- **Spectral Features**: Frequency domain characteristics
- **Zero-Crossing Rate**: Signal oscillation patterns
- **DCT Coefficients**: Compressed domain features

These experimental methods provide additional dimensions for file identification and corruption detection beyond traditional hashing.

## Configuration

### Ignore Patterns

The tool respects multiple ignore mechanisms:

- `.hashignore`: Project-specific exclusions
- `.gitignore`: Git-based exclusions
- Command-line exclusions

### Database Configuration

SQLite database stores:
- File history and changes
- Scan sessions
- Metadata correlations
- Frequency signatures

## Output Formats

### Standard Outputs

- **Text Files**: Traditional checksum format
- **JSON**: Structured data for automation
- **CSV**: Spreadsheet-compatible format
- **HTML**: Visual reports with statistics

### Advanced Outputs

- **SBOM**: Software Bill of Materials (SPDX format)
- **GPG Signatures**: Cryptographic proof of integrity
- **Timestamps**: Blockchain-based time proofs
- **Metadata Files**: Extracted information storage

## Integration Examples

### CI/CD Pipeline

```powershell
# Pre-build integrity check
.\hash-index.ps1 -Path "." -Verify
if ($LASTEXITCODE -ne 0) { exit 1 }

# Post-build provenance
.\hash-index.ps1 -Path "." -GenerateSBOM -SignWithGPG
```

### Research Workflow

```powershell
# Baseline establishment
.\hash-index.ps1 -Path ".\dataset" -All -EnableHistory

# Change detection
.\hash-index.ps1 -Path ".\dataset" -DiffMode -DiffWith "baseline.json"
```

## Security Considerations

### Cryptographic Strength

- BLAKE2B recommended for new deployments
- SHA256 for compatibility requirements
- Avoid SHA1 for security-critical applications

### Provenance Verification

- GPG signatures provide non-repudiation
- Timestamp proofs prevent backdating
- Historical tracking enables audit trails

### Experimental Features

Frequency-based signatures are research-oriented and should not be relied upon for security-critical applications. They provide additional analytical dimensions rather than cryptographic guarantees.

## Performance Optimization

### Parallel Processing

- Automatic parallelization for large file sets
- Configurable worker limits
- Fallback to sequential for problematic environments

### Memory Management

- Streaming hash computation for large files
- Configurable sample sizes for frequency analysis
- Efficient metadata caching

## Troubleshooting

### Common Issues

1. **Python Not Found**: Install Python or use native algorithms only
2. **GPG Failures**: Ensure GPG is installed and configured
3. **Permission Errors**: Run with appropriate filesystem permissions
4. **Large File Handling**: Adjust sample sizes for memory constraints

### Debug Mode

Enable verbose logging for detailed operation tracking:

```powershell
.\hash-index.ps1 -Path ".\project" -Verbose
```

## Future Development

### Planned Enhancements

- Machine learning integration for anomaly detection
- Distributed hash verification
- Advanced perceptual hashing for media files
- Blockchain anchoring for immutable provenance

### Research Directions

- Quantum-resistant hash algorithms
- Advanced signal processing techniques
- Behavioral analysis patterns
- Cross-platform optimization

## Contributing

This tool represents ongoing research in file integrity and provenance. Experimental features are marked as such and should be used with appropriate caution in production environments.

## How-to Guides & Examples 🔧

### 1) Establishing a Baseline

1. Create a fresh export and db records for your repository:

```powershell
# Full provenance baseline
.\hash-index.ps1 -Path "." -All -EnableHistory -ExtractMetadata -GenerateSBOM -GenerateReport -ExportJSON
```

2. Commit the index files and SBOM to a secure branch and sign the index:

```powershell
git add SHA256SUMS.txt .sbom/sbom.spdx.json
git commit -S -m "Baseline integrity checksums"
```

3. Store the baseline JSON in a safe archival location for later comparison.

---

### 2) Verifying Changes (Daily Checks)

```powershell
# Verify current working tree against the index
.\hash-index.ps1 -Path "." -Verify -ParallelVerify -UseGitIgnore
if ($LASTEXITCODE -ne 0) { Write-Error "Integrity check failure" }
```

- Interpret failures by reviewing `.hash-index.log` and `.reports/*` (HTML) or JSON exports for per-file failure details.

---

### 3) Using History & Diff Mode

```powershell
# Record a scan (if history enabled you'll have DB entries)
.\hash-index.ps1 -Path "." -EnableHistory

# Show history for a file
powershell -c "(Get-Item .hash-index.db) | Out-Null; .\hash-index.ps1 -ShowHistory"

# Compare current index with baseline
.\hash-index.ps1 -Path "." -DiffMode -DiffWith "baseline.json"
```

---

### 4) Interpreting Experimental Signatures

- **Entropy** close to 8 indicates high randomness (e.g., encrypted or compressed files).
- **Low zero-crossing rate** tends to indicate structured or sparse content.
- **DCT coefficients** provide a compact spectral fingerprint; similar files will often have correlated coefficient vectors.

> Note: Experimental signatures are for analysis and research — do not treat them as cryptographic proof.

---

## Troubleshooting & Debugging

1. Re-run with `-Verbose` to get detailed diagnostic output.
2. Check `.hash-index.log` and the generated HTML report for errors and context.
3. If BLAKE2b hashing fails, ensure `python` is on PATH and `hashlib` is available.
4. If DB operations fail, ensure the SQLite capability is available via the embedded Python helper.

---

## Contributing & Tests

- Add unit-like tests by creating small sample repositories under `tests/` and verifying expected outputs (JSON and index files).
- Use the `-ExportJSON` output to assert canonical fields in CI.

---

## License

This tool is part of the Somnus Sovereign Systems and is covered under the Sovereign Anti-Exploitation Software License.