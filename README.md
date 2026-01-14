# Somnus License & Dev Tools

[![License](https://img.shields.io/badge/License-Somnus%20Sovereign-purple.svg)](./LICENSE)

This repository hosts the **Sovereign Anti-Exploitation Software License (SAESL)** — a custom, legally-binding proprietary license designed to protect independent developers from exploitation by large corporations and high-net-worth individuals while permitting academic research and personal education.

## 🔒 The License

The [LICENSE](./LICENSE) file contains **Version 4.0 (Leviathan Enforcement Edition)** of the Sovereign Anti-Exploitation Software License. Note: this License contains explicit provenance and use restrictions — please read the License for details. 🦈

Key features include:

- **Anti-Capture Framework** — Explicit prohibitions on use by specified large tech companies and high-net-worth individuals
- **Commercial Use Restrictions** — Requires paid licensing for any commercial deployment
- **Service Deployment Ban** — Prohibits SaaS/API deployments without explicit authorization
- **AI Training Prohibition** — Prevents use for training AI models without consent
- **Tiered Licensing** — Automatic licenses for personal non-commercial use and academic research
- **Strong Enforcement** — Liquidated damages, statutory damages, and injunctive relief provisions

### Usage

To apply this license to your own projects:

1. Copy the [LICENSE](./LICENSE) file to your project root
2. Update the copyright year and verify the integrity hash
3. Link back to this repository for reference: `https://github.com/calisweetleaf/somnus-license`

**Author:** Christian Trey Levi Rowell  
**Contact:** <treyrowell1826@gmail.com>  
**GitHub:** [@calisweetleaf](https://github.com/calisweetleaf)

---

## 🛠️ Included Development Tools

This repository also includes two development utilities I use regularly across my projects:

### 1. Hash Index (`hash-index.ps1`)

A **PowerShell-based cryptographic integrity and provenance system** for file verification.

**Features:**

- Multi-algorithm hashing (SHA256, SHA1, SHA384, SHA512, BLAKE2B)
- SBOM (Software Bill of Materials) generation
- Metadata extraction for various file types (PDF, images, Office docs, archives)
- SQLite-backed historical tracking
- Experimental frequency-based signatures for advanced research
- `.gitignore` and `.hashignore` support
- Parallel verification for large projects
- HTML/JSON report generation
- GPG signing and timestamp proofs

**📚 Documentation:** See the [docs](./docs/) folder for comprehensive guides:
- [Complete Documentation](./docs/hash-index-documentation.md) - Full feature overview
- [Command Reference](./docs/command-reference.md) - All command-line options
- [Configuration Guide](./docs/configuration-guide.md) - Setup and configuration
- [Experimental Methods](./docs/experimental-methods-reference.md) - Advanced signal processing

**Quick Start:**
```powershell
# Basic integrity check
.\hash-index.ps1 -Path ".\my-project"

# Full featured analysis
.\hash-index.ps1 -Path ".\my-project" -All
```

**Quick Start:**

```powershell
# Basic hash generation
.\hash-index.ps1 -Path ".\my-project"

# Run all algorithms with gitignore support
.\hash-index.ps1 -Path ".\my-project" -All -UseGitIgnore

# Generate SBOM and reports
.\hash-index.ps1 -Path ".\my-project" -GenerateSBOM -GenerateReport
```

---

### 2. Python Production Doctor (`python_production_doctor.py`)

A **comprehensive Python code health assessment tool** that scans codebases to identify production readiness issues and technical debt.

**Detects:**

- Syntax errors
- TODO/FIXME/HACK markers
- Stub implementations (pass, ellipsis, NotImplementedError)
- Placeholder return values
- Incomplete method implementations
- Missing docstrings
- Suspiciously short functions
- Unimplemented abstract methods
- Type hint gaps
- Test coverage gaps

**Quick Start:**

```bash
# Scan a project
python python_production_doctor.py /path/to/your/project

# With custom config
python python_production_doctor.py /path/to/project -c my_config.json

# JSON output for CI/CD
python python_production_doctor.py /path/to/project -f json -o report.json
```

**Configuration:**
Create a JSON config file to customize analysis rules:

```json
{
  "min_function_lines": 5,
  "min_docstring_length": 15,
  "test_coverage_threshold": 0.7,
  "ignore_patterns": ["__pycache__/*", ".venv/*"],
  "severity_levels": {
    "syntax_errors": "critical",
    "stubs": "serious",
    "todos": "minor"
  }
}
```

---

## 📁 Repository Structure

```
somnus-license/
├── LICENSE                      # Sovereign Anti-Exploitation Software License v4.0
├── README.md                    # This file
├── hash-index.ps1               # PowerShell hash integrity tool
└── python_production_doctor.py  # Python code health scanner
```

---

## 📜 License Notice

The **LICENSE** file in this repository is the Sovereign Anti-Exploitation Software License itself. The development tools (`hash-index.ps1` and `python_production_doctor.py`) are also covered under this license.

**COPYRIGHT © 2026 CHRISTIAN TREY LEVI ROWELL. ALL RIGHTS RESERVED.**
