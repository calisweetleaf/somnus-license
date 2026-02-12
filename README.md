# Somnus Sovereign License & Defense Tools

[![License](https://img.shields.io/badge/License-Sovereign_Leviathan_v4.0-7000FF.svg)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Active_Enforcement-FF0000.svg)](./LICENSE)
[![Tool-Suite](https://img.shields.io/badge/Tools-Defense_Grade-007ACC.svg)](./hash-index.ps1)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18617098.svg)](https://doi.org/10.5281/zenodo.18617098)

> **"Open Functionality for the Individual. A Closed Fortress for the Algorithmic Leviathans."**

This repository hosts the **Sovereign Anti-Exploitation Software License (SAESL)**—a weaponized legal instrument designed to protect independent developers from extraction by surveillance capitalists and corporate monopolies—and the **Defense-Grade Tool Suite** required to maintain cryptographic integrity in a hostile digital environment.

---

## The Sovereign License (v4.0 "Leviathan")

**[Read the breakdown and explanation here.](./license-docs/output/Sovereign_License_Reference.md)**

The `LICENSE` file in this repository is **Version 4.0 (Leviathan Enforcement Edition)**. It is not an MIT or Apache license. It is a **Unilateral Contract of Adherence** that fundamentally alters the "Open Source" deal.

### The Core Doctrine

1. **Anti-Capture (Art. II)**: Explicit, identity-based exclusions for the "ClosedAI Cartel" (OpenAI, Anthropic, Google, Meta, Microsoft, Apple, NVIDIA) and their VC backers (a16z, Sequoia, YC).
2. **Strict Liability (Art. X)**: No "innocent infringement." If money flows to a Prohibited Party, the license is breached.
3. **Means-Tested Access**:
    * **Tier 1 (Sovereign Individual)**: Free for individuals making <$50k/year (CPI-adjusted).
    * **Tier 2 (Academic)**: Free for non-profit research (must publish results).
    * **Tier 3 (Commercial)**: **Negotiated Paid License** for ANY revenue generation or "Service Deployment."
4. **The "SaaS Ban"**: You cannot wrap this software in an API and sell it.
5. **The "AI Ban"**: You cannot use this software to train, benchmark, or generate data for third-party AI models.

### Documentation Hierarchy

* **[The Sovereign Code](./license-docs/output/Sovereign_License_Reference.md)**: The definitive "nitty gritty" explanation of every clause.
* **[Citation File](./CITATION.cff)**: Professional citation metadata for academic use.
* **[Visual Logic](./license-docs/src/visuals/)**: Mermaid flowcharts demonstrating liability flows.

---

## Tool 1: The Hash Index (`hash-index.ps1`)

**Status: Production (v2.0) | Size: 62KB | Integrity: Critical**

The `hash-index.ps1` is not just a hashing script; it is a **Cryptographic Provenance Engine**. It creates a verifiable, immutable history of your project's state, preventing supply chain attacks, silent corruption, and modification.

### Capabilities (Usage Guide)

#### 1. Basic Operations

Run a standard integrity check using SHA-256 (default).

```powershell
.\hash-index.ps1 -Path "."
```

#### 2. "Turbo Mode" (Defense-Grade Verification)

Engage **ALL** integrity sensors. This runs every hash algorithm (SHA256, SHA512, BLAKE2b), extracts metadata, generates an SBOM, and creates an HTML report.

```powershell
.\hash-index.ps1 -All -DeepArchives -Verbose
```

#### 3. Signal Intelligence (Experimental)

For research datasets or media archives, use signal processing to detect "drift" even if hashes change.

```powershell
# Compute Entropy, Zero-Crossing Rates, and Spectral Centroids
.\hash-index.ps1 -Path "./data" -FrequencySignature -EntropyAnalysis -PerceptualHash
```

#### 4. Supply Chain Defense (SBOM)

Generate a **Software Bill of Materials (SPDX 2.3)** to document exactly what is in your deployment.

```powershell
.\hash-index.ps1 -GenerateSBOM -ExportJSON
# Output: .sbom/sbom.spdx.json
```

### Technical Parameters

| Switch | Function | Impact |
| :--- | :--- | :--- |
| `-All` | **Protocol Override**. Runs ALL algorithms and features. | Maximum visibility, slower speed. |
| `-Algorithm` | Select `SHA256` (Default), `SHA512`, `BLAKE2B`, etc. | Targeting specific compliance needs. |
| `-Verify` | Checks current files against the existing index. | Audit mode. |
| `-UseGitIgnore` | Respects `.gitignore` and `.hashignore`. | Prevents hashing trash/artifacts. |
| `-EnableHistory` | Activates SQLite DB to track file evolution. | Enables time-travel analysis. |
| `-SignWithGPG` | Signs the index with your local GPG key. | **Non-Repudiation**. |
| `-TimestampProof` | Uses OTS to anchor hash in Bitcoin blockchain. | **Absolute Timeline Proof**. |

> **Dependency Note**: Advanced features (BLAKE2b, SQLite History) require a local Python environment. The script automatically detects the active venv.

---

## Tool 2: Python Production Doctor (`python_production_doctor.py`)

**Status: Active | Focus: Code Health**

A static analysis tool that acts as a "Field Medic" for your codebase. It scans for "lazy" coding practices that lead to technical debt.

### Core Scans

* **Stub Detection**: Finds `pass`, `...`, and `NotImplementedError`.
* **Documentation Gaps**: Flags missing docstrings in complex functions.
* **Type Hinting**: Enforces modern Python typing standards.
* **Todo/Fixme**: Aggregates all technical debt markers.

### Usage

```bash
# Full health scan
python python_production_doctor.py ./src

# Strict mode for CI/CD (fail on errors)
python python_production_doctor.py ./src --strict --json-report report.json
```

---

## Repository Structure

```
somnus-license/
├── LICENSE                      # The Sovereign License (Legal Instrument)
├── license-docs/                # DETAILED DOCUMENTATION (The Codex)
│   ├── output/                  # Final Reference Docs
│   └── src/                     # Source sections & diagrams
├── hash-index.ps1               # Cryptographic Provenance Tool (62KB)
├── python_production_doctor.py  # Code Health Scanner 
└── README.md                    # This file
```

---


---

## Citation

```mla
Rowell, C. T. L. Somnus-license. v2.0.0, Zenodo, 12 Feb. 2026, https://doi.org/10.5281/zenodo.18615826.
```


---

## Legal Notice

The **LICENSE** file in this repository is the Sovereign Anti-Exploitation Software License itself. The development tools (`hash-index.ps1` and `python_production_doctor.py`) are also covered under this license.

**COPYRIGHT © 2026 CHRISTIAN TREY LEVI ROWELL. ALL RIGHTS RESERVED.**

---

## Used and Cited By

[NGSST](https://github.com/calisweetleaf/NGSST)

[RLHF](https://github.com/calisweetleaf/Reinforcement-Learning-Full-Pipeline)

[SOTA-Runtime-Tools](https://github.com/calisweetleaf/SOTA-Runtime-Core)
