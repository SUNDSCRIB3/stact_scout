# Stack Scout 🔍

A powerful CLI tool and GitHub Action that automatically analyzes your project's technology stack and generates comprehensive reports. Stack Scout detects programming languages, frameworks, build tools, and DevOps configurations to give you instant insights into any codebase.

## Features

- 🔍 **Automatic Detection**: Scans your project directory to identify technologies
- 📊 **Comprehensive Analysis**: Detects 15+ languages, 15+ frameworks, 15+ build tools, and 12+ DevOps tools
- 📝 **Multiple Output Formats**: JSON, Markdown, or simple text reports
- 🎯 **Smart Detection**: Uses file patterns, content analysis, and dependency files
- 🚀 **GitHub Action**: Integrate stack analysis into your CI/CD pipeline
- 💻 **Cross-Platform**: Works on Linux, macOS, and Windows
- 🔧 **Extensible**: Easy to add support for new technologies

## Installation

### From PyPI (Recommended)

```bash
pip install stack-scout
```

### From Source

```bash
git clone https://github.com/lukebancroft4-max/stact_scout.git
cd stact_scout
pip install -e .
```

### Requirements

- Python 3.7 or higher
- No external dependencies required for core functionality

## Usage

### Basic Usage

Analyze the current directory:

```bash
stack-scout
```

Analyze a specific directory:

```bash
stack-scout /path/to/project
```

### Output Formats

Generate a JSON report:

```bash
stack-scout --format json --output report.json
```

Generate a Markdown report:

```bash
stack-scout --format markdown --output STACK_REPORT.md
```

Generate a text report:

```bash
stack-scout --format text --output stack.txt
```

### Command Line Options

```
usage: stack-scout [-h] [-f {json,markdown,text}] [-o OUTPUT] [path]

Analyze project technology stack

positional arguments:
  path                  Path to the project directory (default: current directory)

optional arguments:
  -h, --help            show this help message and exit
  -f {json,markdown,text}, --format {json,markdown,text}
                        Output format (default: text)
  -o OUTPUT, --output OUTPUT
                        Output file path (default: stdout)
```

## Supported Technologies

### Programming Languages (15+)

- Python
- JavaScript/TypeScript
- Java
- C/C++
- C#
- Go
- Rust
- Ruby
- PHP
- Swift
- Kotlin
- Scala
- R
- Shell/Bash
- PowerShell

### Frameworks (15+)

- **Python**: Django, Flask, FastAPI, Pytest
- **JavaScript**: React, Vue.js, Angular, Next.js, Express, Svelte
- **Java**: Spring Boot, Micronaut
- **Ruby**: Rails
- **.NET**: ASP.NET Core
- **Go**: Gin

### Build Tools & Package Managers (15+)

- npm
- Yarn
- pnpm
- pip
- Poetry
- Maven
- Gradle
- Cargo
- Go Modules
- Composer
- Bundler
- NuGet
- Make
- CMake
- Webpack

### DevOps & Infrastructure (12+)

- Docker
- Kubernetes
- Terraform
- Ansible
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Travis CI
- Azure Pipelines
- Vagrant
- Helm

## GitHub Action

Integrate Stack Scout into your CI/CD pipeline to automatically analyze and document your project's technology stack.

### Basic Usage

```yaml
name: Stack Analysis

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Analyze Stack
        uses: lukebancroft4-max/stact_scout@v1
        with:
          format: 'markdown'
          output: 'STACK_REPORT.md'
```

### Action Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `path` | Path to analyze | No | `.` |
| `format` | Output format (json/markdown/text) | No | `text` |
| `output` | Output file path | No | stdout |

### Action Outputs

| Output | Description |
|--------|-------------|
| `report` | The generated stack analysis report |
| `technologies-count` | Total number of technologies detected |

### Advanced Usage

Upload the report as an artifact:

```yaml
- name: Analyze Stack
  uses: lukebancroft4-max/stact_scout@v1
  with:
    format: 'markdown'
    output: 'STACK_REPORT.md'

- name: Upload Report
  uses: actions/upload-artifact@v3
  with:
    name: stack-report
    path: STACK_REPORT.md
```

Comment on PR with the analysis:

```yaml
- name: Analyze Stack
  id: analyze
  uses: lukebancroft4-max/stact_scout@v1
  with:
    format: 'markdown'
    output: 'STACK_REPORT.md'

- name: Comment PR
  uses: actions/github-script@v6
  with:
    script: |
      const fs = require('fs');
      const report = fs.readFileSync('STACK_REPORT.md', 'utf8');
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: report
      });
```

## Architecture

Stack Scout uses a modular detection system:

1. **File System Scanner**: Traverses the project directory
2. **Pattern Matchers**: Identifies files by name and extension
3. **Content Analyzers**: Examines file contents for specific patterns
4. **Dependency Parsers**: Reads package.json, requirements.txt, pom.xml, etc.
5. **Report Generators**: Formats output in JSON, Markdown, or text

### Detection Logic

- **Languages**: Detected by file extensions and shebang lines
- **Frameworks**: Identified through dependency files and configuration files
- **Build Tools**: Found via lock files, config files, and build scripts
- **DevOps**: Detected through CI/CD config files and infrastructure-as-code files

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/lukebancroft4-max/stact_scout.git
cd stact_scout

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest black flake8 mypy
```

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
# Format code
black stack_scout/

# Check linting
flake8 stack_scout/

# Type checking
mypy stack_scout/
```

### Project Structure

```
stact_scout/
├── stack_scout/
│   ├── __init__.py
│   ├── __main__.py
│   ├── scanner.py       # Core scanning logic
│   ├── detectors.py     # Technology detection
│   ├── reporters.py     # Output formatting
│   └── cli.py          # Command-line interface
├── tests/
│   ├── test_scanner.py
│   ├── test_detectors.py
│   └── test_reporters.py
├── action.yml          # GitHub Action definition
├── setup.py           # Package configuration
├── README.md
└── LICENSE
```

## Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-detector`
3. **Make your changes**
4. **Add tests** for new functionality
5. **Run tests**: `pytest tests/`
6. **Format code**: `black stack_scout/`
7. **Commit changes**: `git commit -m "feat: add support for Elixir"`
8. **Push to branch**: `git push origin feature/new-detector`
9. **Open a Pull Request**

### Adding New Technology Detectors

To add support for a new technology, update the relevant detector in `stack_scout/detectors.py`:

```python
def detect_languages(self, files):
    patterns = {
        'Elixir': r'\.exs?$',
        # ... existing patterns
    }
    # ... detection logic
```

### Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions or changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Roadmap

- [ ] Add support for more languages (Dart, Haskell, Clojure)
- [ ] Detect database technologies
- [ ] Cloud platform detection (AWS, Azure, GCP)
- [ ] Generate dependency graphs
- [ ] Security vulnerability scanning
- [ ] License compliance checking
- [ ] Web dashboard for visualization
- [ ] IDE extensions (VS Code, IntelliJ)
- [ ] API for programmatic access
- [ ] Machine learning for better detection accuracy

## Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/lukebancroft4-max/stact_scout/issues)
- 💡 **Feature Requests**: [Start a discussion](https://github.com/lukebancroft4-max/stact_scout/discussions)
- 📖 **Documentation**: [Wiki](https://github.com/lukebancroft4-max/stact_scout/wiki)

## Acknowledgments

- Inspired by GitHub's linguist and Stack Overflow's technology trends
- Built with ❤️ by the open-source community

---

**Stack Scout** - Know your stack, instantly. 🔍✨
