# Stack Scout 🔍

**Automated technology stack detection for software projects**

Stack Scout is a powerful CLI tool that automatically detects programming languages, frameworks, build tools, and DevOps configurations in your codebase. Perfect for developers, teams, and CI/CD pipelines.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

## ✨ Features

- 🔎 **Automatic Detection** - Scans your codebase and identifies technologies
- 📊 **Evidence-Based** - Shows exactly where each technology was found
- 🎯 **Confidence Scoring** - Rates detection confidence (high/medium/low)
- 🎨 **Beautiful Output** - Rich terminal formatting with colors and trees
- 📄 **JSON Export** - Machine-readable output for CI/CD integration
- ⚡ **Fast Scanning** - Efficient directory traversal with smart exclusions
- 🔧 **GitHub Action** - Easy integration into your workflows

## 🚀 Quick Start

### Installation

```bash
# From PyPI (coming soon)
pip install stack-scout

# From source
git clone https://github.com/lukebancroft4-max/stact_scout.git
cd stact_scout
pip install -e .
```

### Basic Usage

```bash
# Scan current directory
stack-scout scan .

# Scan specific path
stack-scout scan /path/to/project

# Output JSON
stack-scout scan . --format json

# Save to file
stack-scout scan . --output report.json

# Show detailed evidence
stack-scout scan . --verbose
```

## 📖 Example Output

### Text Output

```
🔍 Stack Scout Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Project: /home/user/my-project
🕐 Scanned: 2026-01-07T10:23:28.248609+00:00

💻 Languages (2)
├── Python HIGH
│   └── 45 files
└── TypeScript HIGH
    └── 23 files

🚀 Frameworks (2)
├── React HIGH
│   └── Found react in dependencies
└── FastAPI HIGH
    └── Found fastapi in requirements

🔧 Build Tools (5)
├── Vite HIGH
│   └── Vite configuration file
├── TypeScript HIGH
│   └── TypeScript configuration file
├── ESLint HIGH
│   └── ESLint configuration file
├── Prettier MEDIUM
│   └── Prettier configuration file
└── pip HIGH
    └── pip configuration file

⚙️ DevOps (3)
├── Docker HIGH
│   └── Docker configuration file
├── GitHub Actions HIGH
│   └── GitHub Actions directory
└── Terraform MEDIUM
    └── Terraform configuration file
```

### JSON Output

```json
{
  "project_path": "/home/user/my-project",
  "scan_timestamp": "2026-01-07T10:23:28.248609+00:00",
  "summary": {
    "language": ["Python", "TypeScript"],
    "framework": ["React", "FastAPI"],
    "build_tool": ["Vite", "TypeScript", "ESLint", "Prettier", "pip"],
    "devops": ["Docker", "GitHub Actions", "Terraform"]
  },
  "detections": [...]
}
```

## 🎯 Supported Technologies

### Languages (15+)
Python, TypeScript, JavaScript, Go, Java, Rust, Ruby, PHP, C++, C, C#, Swift, Kotlin, Scala, Shell

### Frameworks (15+)
React, Vue, Angular, Next.js, Svelte, Express, Django, Flask, FastAPI, Streamlit, Spring Boot, Rails, Laravel

### Build Tools (15+)
npm, Yarn, pnpm, Vite, Webpack, Rollup, ESLint, Prettier, TypeScript, pip, Poetry, Pipenv, Maven, Gradle, Go Modules, Cargo, Bundler, Composer

### DevOps Tools (12+)
Docker, Kubernetes, GitHub Actions, GitLab CI, Jenkins, CircleCI, Travis CI, Terraform, Ansible, CloudFormation, Pre-commit, Make

## 🔧 GitHub Action

Use Stack Scout in your GitHub workflows:

```yaml
name: Stack Analysis
on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: lukebancroft4-max/stact_scout@v1
        with:
          path: '.'
          output-format: 'text'
          upload-artifact: 'true'
```

### Action Inputs

| Input | Description | Default |
|-------|-------------|---------|
| `path` | Path to scan | `.` |
| `output-format` | Output format (`text` or `json`) | `text` |
| `upload-artifact` | Upload report as artifact | `true` |

### Action Outputs

| Output | Description |
|--------|-------------|
| `report-json` | JSON report of detected technologies |

## 🏗️ Architecture

Stack Scout uses a modular detector architecture:

```
src/stack_scout/
├── cli.py              # CLI interface (Click + Rich)
├── scanner.py          # Orchestrates all detectors
├── models.py           # Data models (Detection, Evidence, Report)
├── utils.py            # File system utilities
└── detectors/
    ├── base.py         # Base detector class
    ├── patterns.py     # Technology patterns
    ├── languages.py    # Language detection
    ├── frameworks.py   # Framework detection
    ├── build_tools.py  # Build tools detection
    └── devops.py       # DevOps tools detection
```

Each detector:
1. Scans the project directory
2. Looks for evidence (files, configs, dependencies)
3. Calculates confidence based on evidence strength
4. Returns detections with full evidence trail

## 🧪 Development

### Setup

```bash
# Clone repository
git clone https://github.com/lukebancroft4-max/stact_scout.git
cd stact_scout

# Install in development mode
pip install -e .

# Install dev dependencies
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=stack_scout --cov-report=html

# Run specific test
pytest tests/test_scanner.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/
```

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Add support for new technologies
- ✅ Write tests

### Adding New Technology Detections

1. Add pattern to `src/stack_scout/detectors/patterns.py`
2. Update corresponding detector if needed
3. Add test in `tests/test_detectors.py`
4. Update README with new technology

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🗺️ Roadmap

- [ ] PyPI publication
- [ ] More language support (Elixir, Haskell, OCaml, etc.)
- [ ] Database detection (PostgreSQL, MongoDB, Redis, etc.)
- [ ] Cloud provider detection (AWS, Azure, GCP)
- [ ] Dependency version tracking
- [ ] Security scanning integration
- [ ] Visual reports (HTML/PDF)
- [ ] VS Code extension
- [ ] CI/CD templates generation

## 📧 Contact

- GitHub: [@lukebancroft4-max](https://github.com/lukebancroft4-max)
- Issues: [GitHub Issues](https://github.com/lukebancroft4-max/stact_scout/issues)

---

Made with ❤️ by the Stack Scout team
