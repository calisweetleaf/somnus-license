# Project Structure Overview

## Repository Layout

```
license-and-tools/
├── .gitignore                      # Git ignore rules (1921 bytes)
├── .venv/                          # Python virtual environment (IGNORED)
├── __pycache__/                    # Python bytecode cache (IGNORED)
├── data/                           # Data storage directory (IGNORED)
│   ├── mcp_server.log             # MCP server logs (25KB)
│   ├── memory_store.json          # Memory storage (2 bytes)
│   ├── sessions/                  # Session data
│   └── web_cache/                 # Web cache data
├── python_production_doctor.py    # Main analysis tool (56KB)
├── hash-index.ps1                 # PowerShell hash/index tool (52KB)
├── LICENSE                        # Custom license file (82KB)
├── DOCTOR_CONFIG.json             # Example config (803 bytes)
├── openrouter_keys.txt.example    # API key template (177 bytes)
├── requirements.txt               # Dependencies (none!)
├── README.md                      # Full documentation (6.4KB)
├── QUICKSTART.md                  # Quick start guide (6KB)
├── RUN_TEST.ps1                   # Test script (3.2KB)
└── production_doctor.log          # Log file (86 bytes)
```

## Key Files Breakdown

### Core Tools
- **`python_production_doctor.py`** (56KB): Python code health analyzer
  - Zero dependencies
  - 10 types of code analysis
  - Parallel processing support
  - Markdown/JSON output

- **`hash-index.ps1`** (52KB): PowerShell provenance/hash tool
  - Multiple hash algorithms
  - Database tracking
  - SBOM generation
  - Metadata extraction

### Configuration & Setup
- **`.gitignore`** (1.9KB): Comprehensive ignore rules
  - Virtual environments
  - Python cache files
  - Log files and databases
  - IDE/editor files
  - OS generated files
  - Production Doctor specific files

- **`DOCTOR_CONFIG.json`**: Example configuration
  - Analysis thresholds
  - Ignore patterns
  - Severity levels

- **`openrouter_keys.txt.example`**: API key template
  - Optional AI features
  - Multi-key support

### Documentation
- **`README.md`** (6.4KB): Complete user guide
- **`QUICKSTART.md`** (6KB): Quick reference
- **`PROJECT_STRUCTURE.md`**: This file

### Testing & Logs
- **`RUN_TEST.ps1`** (3.2KB): PowerShell test script
- **`production_doctor.log`**: Analysis logs

## Git Ignore Strategy

The `.gitignore` file excludes:

### Environment & Cache
- `.venv/`, `venv/`, `env/` - Virtual environments
- `__pycache__/`, `*.pyc`, `*.pyo` - Python bytecode

### Logs & Databases
- `*.log`, `*.db`, `*.sqlite` - Logs and databases
- `production_doctor.log` - Specific tool log
- `.hash-index.db` - Hash index database

### Data Directory (data/)
- MCP server logs
- Memory storage
- Session data
- Web cache
- Temporary files

### IDE & OS Files
- `.vscode/`, `.idea/` - Editor configs
- `.DS_Store`, `Thumbs.db` - OS files
- `*.swp`, `*~` - Temporary files

### Build & Distribution
- `build/`, `dist/`, `*.egg-info/` - Build artifacts
- `__pypackages__/` - PEP 582 packages

### Reports & Secrets
- `production_report.*` - Generated reports
- `test_report.*` - Test reports
- `openrouter_keys.txt` - API keys (keep private!)

## Usage Patterns

### For Code Analysis
1. `python python_production_doctor.py /path/to/project`
2. Review `production_report.md`
3. Address critical issues first
4. Track improvements over time

### For File Provenance
1. `.\hash-index.ps1 -Path .\project\files`
2. Check `.hash-index.db` for history
3. Generate reports/SBOMs as needed

### For Repository Management
1. All tools committed to repo
2. Configs and examples included
3. Logs and data ignored
4. Keys kept private

## File Sizes Summary
- Total tracked: ~205KB
- Documentation: ~13KB
- Tools: ~108KB
- License: 82KB
- Configs: <1KB

## Key Points
- ✅ Zero dependencies for Python tool
- ✅ Comprehensive git ignore coverage
- ✅ Data directory properly excluded
- ✅ Example configs provided
- ✅ Full documentation included
- ✅ Test script available
