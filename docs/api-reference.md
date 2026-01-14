# Hash Index Tool - API Reference

**License:** [Sovereign Anti-Exploitation Software License](../LICENSE) 🦈

This document catalogs each function in `hash-index.ps1` with a concise description of purpose, parameters, return values, and usage notes.

---

## Logging

### Write-Log

Signature: `function Write-Log { param([string]$Message, [string]$Level = 'INFO') }`

- Purpose: Centralized logging to file (`.hash-index.log`) and to console when appropriate.
- Params: `$Message` (string), `$Level` (DEBUG|INFO|WARN|ERROR|SUCCESS)
- Returns: None. Appends log lines and prints messages to host (colorized).
- Notes: Honors global `$Verbose` flag and writes to configured log file in `$script:Config.LogFile`.

### Write-Info / Write-Success / Write-Warn / Write-Err / Write-Debug

- Short wrappers around `Write-Log` setting appropriate log level.
- Usage: `Write-Info "Scanning files..."`.

---

## Database Layer

### Get-PythonExecutable

Signature: `function Get-PythonExecutable { }`

- Purpose: Locate a Python executable (prefers venv at `$env:VIRTUAL_ENV`, repo `.venv`, then PATH).
- Returns: Path to Python executable as string, or `$null` if not found.
- Notes: Used by functions that call Python (BLAKE2B helper, sqlite helper).

### Invoke-PythonSqlite

Signature: `function Invoke-PythonSqlite { param([string]$DbPath, [string]$Mode, [string]$Sql = '', [hashtable]$Data = @{}) }`

- Purpose: Small helper that runs an embedded Python program to operate on the SQLite DB.
- Modes: `executescript`, `execute_json`, `query_json`.
- Returns: For `query_json` returns JSON string of query results; otherwise, `null`.
- Notes: Uses temporary files & Start-Process to avoid known PS encoding issues.

### Initialize-Database

Signature: `function Initialize-Database { param([string]$dbPath) }`

- Purpose: Create necessary tables and indices for history, sessions, metadata, and frequency signatures.
- Returns: `$true` on success, `$false` on failure.
- Notes: Requires Python (via `Get-PythonExecutable`) to run the helper.

### Add-HistoryRecord

Signature: `function Add-HistoryRecord { param($dbPath, $filePath, $hash, $algorithm, $fileSize, $modifiedTime, $gitCommit, $gitTag, $metadata) }`

- Purpose: Insert a file history row into the `file_history` table.
- Returns: None.
- Notes: Converts metadata to compressed JSON; logs failures as warnings.

### Get-FileHistory

Signature: `function Get-FileHistory { param($dbPath, $filePath) }`

- Purpose: Retrieve file's history rows as JSON-parsed objects.
- Returns: Array of rows or `@()` if none / on failure.

### Add-ScanSession

Signature: `function Add-ScanSession { param($dbPath, $rootPath, $algorithm, $fileCount, $totalSize, $duration, $gitCommit, $gitTag, $releaseVersion) }`

- Purpose: Record a scan session with stats in the `scan_sessions` table.
- Returns: None.

---

## Metadata Extraction

### Get-FileMetadata

Signature: `function Get-FileMetadata { param([string]$filePath) }`

- Purpose: Extract file-level metadata and dispatch to format-specific extractors.
- Returns: Hashtable with fields like Path, Size, Extension, ContentType, Created, Modified and additional fields from type-specific extractors.
- Notes: Calls `Get-MagicBytes` and `Get-ContentType` to determine MIME type.

### Get-MagicBytes

Signature: `function Get-MagicBytes { param([string]$path) }`

- Purpose: Read up to first 16 bytes of a file to help content detection.
- Returns: Byte array or empty array on error.

### Get-ContentType

Signature: `function Get-ContentType { param([byte[]]$magic, [string]$ext) }`

- Purpose: Map magic bytes (or extension) to MIME type.
- Returns: String MIME type (e.g., `application/pdf`, `image/png`, `application/octet-stream`).
- Notes: Uses common magic signatures and a fallback extension map.

### Get-PDFMetadata, Get-ImageMetadata, Get-AudioMetadata, Get-VideoMetadata, Get-OfficeMetadata, Get-PEMetadata, Get-ArchiveMetadata

- Purpose: Type-specific metadata extraction helpers.
- Returns: Hashtables with fields relevant to each type (Title, Author, Width/Height, Dimensions, FileVersion, EntryCount, etc.).
- Notes: Image extraction uses `System.Drawing` where available; Office files are read as zip and core properties parsed.

### Export-MetadataToFile

Signature: `function Export-MetadataToFile { param($filePath, $metadata, $metadataDir) }`

- Purpose: Save a file's metadata as a JSON sidecar under `$metadataDir`.
- Returns: None; creates directory as needed.

---

## Experimental Frequency-Based Signatures

### Get-FrequencySignature

Signature: `function Get-FrequencySignature { param([string]$filePath) }`

- Purpose: Compute an experimental frequency-based signature for a file using a sampled byte signal.
- Returns: Hashtable with Entropy, ZeroCrossingRate, SpectralCentroid, DCTCoefficients (CSV), SignatureTime.
- Notes: Samples up to first 64KB, subsamples for DCT (~512 samples) and extracts first 32 coefficients.

### Get-Entropy

Signature: `function Get-Entropy { param([double[]]$signal) }`

- Purpose: Quantize signal to 256 bins and compute Shannon entropy.
- Returns: Floating-point entropy value.

### Get-ZeroCrossingRate

Signature: `function Get-ZeroCrossingRate { param([double[]]$signal) }`

- Purpose: Compute zero-crossing rate relative to signal mean; indicates noisiness/oscillation.
- Returns: Rate (0..1).

### Get-SpectralCentroid

Signature: `function Get-SpectralCentroid { param([double[]]$signal) }`

- Purpose: Compute spectral centroid (weighted mean frequency normalized by signal length).
- Returns: Floating-point centroid.

### Get-SimplifiedDCT

Signature: `function Get-SimplifiedDCT { param([double[]]$signal, [int]$numCoeffs) }`

- Purpose: Compute a simplified DCT and return first `numCoeffs` coefficients.
- Returns: Array of coefficients.
- Notes: O(N * K) naive implementation; considered stable for small `numCoeffs`.

### Get-PerceptualHash

Signature: `function Get-PerceptualHash { param([string]$filePath) }`

- Purpose: Produce an 8x8 perceptual-style hash for non-image files by sampling bytes and generating a binary grid.
- Returns: Hex string representing 64-bit-ish perceptual hash.
- Notes: Useful for similarity heuristics, not cryptographic hashing.

---

## SBOM & Export

### New-SBOM

Signature: `function New-SBOM { param([string]$rootPath, [array]$files, [string]$format = 'SPDX') }`

- Purpose: Build an SPDX-like SBOM structure from file list and checksums.
- Returns: Hashtable representing SBOM data.

### Export-SBOM

Signature: `function Export-SBOM { param([hashtable]$sbomData, [string]$outputPath, [string]$format = 'JSON') }`

- Purpose: Save SBOM data to JSON or YAML (simple converter).
- Returns: None; writes file and logs success.

### ConvertTo-SimpleYAML

Signature: `function ConvertTo-SimpleYAML { param([hashtable]$data, [int]$indent = 0) }`

- Purpose: Minimal YAML serializer for simple nested hashtables/arrays.
- Returns: YAML string.
- Notes: Not a full YAML implementation—intended for readable exports.

---

## Ignore Patterns

### Get-HashIgnorePatterns

Signature: `function Get-HashIgnorePatterns { param([string]$rootPath) }`

- Purpose: Parse `.hashignore` and return an array of patterns (skips comments and blank lines).
- Returns: Array of patterns.

### Get-GitIgnorePatterns

Signature: `function Get-GitIgnorePatterns { param([string]$rootPath) }`

- Purpose: Parse `.gitignore` similarly.
- Returns: Array of patterns.

### Test-ShouldIgnore

Signature: `function Test-ShouldIgnore { param([string]$path, [string[]]$patterns) }`

- Purpose: Simple wildcard-based pattern matcher used to filter files.
- Returns: Boolean: `$true` if path matches any pattern.
- Notes: Pattern matching is simple (`-like '*pattern*'`); supports trailing `/` directory marker.

---

## Report Generation

### New-HTMLReport

Signature: `function New-HTMLReport { param([array]$files, [string]$outputPath, [hashtable]$stats) }`

- Purpose: Create a styled HTML report summarizing hashes, sizes, and stats.
- Returns: Writes the HTML file and logs success.

### Format-FileSize

Signature: `function Format-FileSize { param([long]$bytes) }`

- Purpose: Human-readable formatting of bytes (B/KB/MB/GB).
- Returns: String.

---

## Core Hashing Utilities

### Get-ExpectedDigestLength

Signature: `function Get-ExpectedDigestLength([string]$alg) { }`

- Purpose: Return expected hex digest length for a supported algorithm.
- Returns: Integer length or throws on unsupported algorithm.

### Get-Blake2bHash

Signature: `function Get-Blake2bHash { param([string]$FilePath, [int]$DigestSize = 64) }`

- Purpose: Use Python's hashlib.blake2b for BLAKE2b hashing (PowerShell lacks it natively).
- Returns: Hex string or `$null` on failure.
- Notes: Requires Python; streams file in chunks; validates digest length.

### Get-UnifiedFileHash

Signature: `function Get-UnifiedFileHash { param([string]$FilePath, [string]$Algorithm) }`

- Purpose: Single API that routes to native `Get-FileHash` for standard algorithms or `Get-Blake2bHash` for BLAKE2b.
- Returns: Hex string; throws on failure for BLAKE2b.

### Get-SidecarHash

Signature: `function Get-SidecarHash([string]$filePath, [string]$alg) { }`

- Purpose: Read sidecar files (e.g., `file.txt.sha256`) to extract stored hashes.
- Returns: Hash string or `$null`.

### Get-FileHashParallel

Signature: `function Get-FileHashParallel { param([array]$files, [string]$algorithm) }`

- Purpose: Compute file hashes using background jobs when safe, with fallbacks to sequential processing. Handles BLAKE2B in sequential mode.
- Returns: Collection of objects with Path, Hash, Success and optional Error fields.
- Notes: Probes job support, collects progress and handles errors gracefully.

### Get-RelativePath

Signature: `function Get-RelativePath([string]$root, [string]$full) { }`

- Purpose: Normalize root and compute file path relative to root.
- Returns: Relative path string.

---

## Git Integration

### Get-GitCommit

Signature: `function Get-GitCommit { }`

- Purpose: Try to get current git commit via `git rev-parse HEAD`. Returns `N/A` on failure.

### Get-GitTag

Signature: `function Get-GitTag { }`

- Purpose: Try to get current tag via `git describe --tags --exact-match`. Returns `N/A` on failure.

---

## Utilities

### Test-Command

Signature: `function Test-Command { param([string]$command) }`

- Purpose: Check presence of a CLI program (Get-Command) and return boolean.
- Returns: `$true` if command exists, else `$false`.

---

## Main Execution Behavior (Notes)

- The script's main block (`# Main Execution`) handles CLI parsing via `param()` and implements high-level workflows: single algorithm runs, `-All` multi-algorithm runs, index filename auto-selection, database initialization, file enumeration, ignore handling, hashing (parallel vs sequential), metadata extraction, frequency/perceptual signature generation, SBOM creation, report generation, exporting JSON/CSV, GPG signing, timestamp proofs, and final logging.
- Many features are opt-in via switches (e.g., `-FrequencySignature`, `-EnableHistory`, `-GenerateReport`, `-SignWithGPG`).
- Experimental features (frequency, perceptual hash) are intended for research and should not be used as cryptographic guarantees.

---

If you'd like, I can:

- Expand each function entry with example invocations and expected outputs (small JSON examples) ✅
- Add cross-links from `README.md` to specific API sections ✅
- Generate a single-file printable reference (PDF) from these docs ✅

Which next step should I take?
