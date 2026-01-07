# Stack-Scout

**Stack-Scout** is an automated codebase analysis tool that detects programming languages, frameworks, build systems, and DevOps tooling used in a project. It scans repositories, dependency files, and configuration artifacts to produce clear, auditable reports for developers, teams, and CI pipelines.

## 🌟 Features

- **Multi-Language Support**: Detects Python, JavaScript, TypeScript, Java, Go, Ruby, PHP, Rust, C/C++, and more
- **Framework Detection**: Identifies popular frameworks like React, Django, Spring Boot, Express, and many others
- **Package Manager Recognition**: Detects npm, pip, Maven, Gradle, Cargo, Bundler, Composer, and more
- **Build Tool Identification**: Recognizes webpack, Vite, Make, CMake, Gradle, and other build systems
- **DevOps Tooling**: Identifies Docker, Kubernetes, GitHub Actions, Jenkins, and other CI/CD tools
- **Multiple Output Formats**: Colorized CLI output and structured JSON reports
- **GitHub Actions Integration**: Easy to integrate into CI/CD pipelines
- **Zero Dependencies**: Uses only Python standard library

## 📦 Installation

### From Source

```bash
git clone https://github.com/lukebancroft4-max/stact_scout.git
cd stact_scout
pip install -e .
```

### Using pip (after publishing)

```bash
pip install stack-scout
```

## 🚀 Usage

### Command Line

```bash
# Scan current directory
stack-scout .

# Scan specific directory
stack-scout /path/to/project

# Generate JSON report
stack-scout . --json report.json

# Disable colored output
stack-scout . --no-color
```

### Examples

**Scan a Python project:**
```bash
stack-scout ~/my-python-project
```

**Scan and save JSON report:**
```bash
stack-scout ~/my-project --json tech-stack.json
```

## 📊 Output

### Console Output

Stack-Scout provides a colorized, human-readable summary:

```
================================================================================
Stack-Scout Analysis Report
Project: /path/to/project
================================================================================

📊 Summary:
  📝 Languages: 3 detected
  🔧 Frameworks: 5 detected
  📦 Package Managers: 2 detected
  🔨 Build Tools: 3 detected
  🚀 DevOps: 2 detected

📝 Languages
------------
  • Python (>=3.8)
    Source: requirements.txt, setup.py
  • JavaScript/TypeScript
    Source: package.json
  • Shell
    Source: scripts/deploy.sh

🔧 Frameworks
-------------
  • Django (>=4.0)
    Source: requirements.txt
    Package: django
  • React (^18.0.0)
    Source: package.json
    Package: react

... (more details)

================================================================================
Total technologies detected: 15
================================================================================
```

### JSON Output

```json
{
  "project_path": "/path/to/project",
  "scan_timestamp": "2024-01-07T10:00:00Z",
  "summary": {
    "total_technologies": 15,
    "by_category": {
      "language": 3,
      "framework": 5,
      "package_manager": 2,
      "build_tool": 3,
      "devops": 2
    }
  },
  "technologies": {
    "language": [
      {
        "category": "language",
        "name": "Python",
        "version": ">=3.8",
        "confidence": "high",
        "source_files": ["requirements.txt", "setup.py"],
        "metadata": {"file_count": 45}
      }
    ],
    "framework": [...],
    ...
  }
}
```

## 🔧 Architecture

Stack-Scout uses a **modular, rules-based design**:

```
stack_scout/
├── detectors/           # Technology detection modules
│   ├── base.py          # Base detector class
│   ├── language_detector.py
│   ├── framework_detector.py
│   ├── package_manager_detector.py
│   ├── build_tool_detector.py
│   └── devops_detector.py
├── scanners/            # File scanning modules
│   └── file_scanner.py
├── formatters/          # Output formatting
│   ├── console_formatter.py
│   └── json_formatter.py
├── scanner.py           # Main scanner coordinator
└── cli.py               # CLI entry point
```

### How It Works

1. **File Scanning**: Recursively scans the project directory for relevant files
2. **Detection**: Applies rules-based detectors to identify technologies
3. **Aggregation**: Collects and deduplicates detection results
4. **Formatting**: Outputs results in human-readable or JSON format

### Adding New Detectors

To add support for new technologies:

1. Create a new detector class extending `Detector`
2. Implement the `detect()` method with your detection logic
3. Add the detector to `StackScanner` in `scanner.py`

Example:
```python
from .base import Detector, DetectionResult

class MyDetector(Detector):
    def detect(self, file_paths, file_contents):
        results = []
        # Your detection logic here
        return results
```

## 🎯 Detection Capabilities

### Languages
Python, JavaScript, TypeScript, Java, Go, Ruby, PHP, C, C++, C#, Rust, Swift, Kotlin, Scala, Shell, R, Dart, Lua, Perl, Elixir, Clojure, Haskell, Erlang, SQL, HTML, CSS, SCSS

### Frameworks
- **Python**: Django, Flask, FastAPI, Pyramid, Streamlit
- **JavaScript/TypeScript**: React, Angular, Vue.js, Svelte, Next.js, Express, NestJS
- **Java**: Spring Boot, Spring, Hibernate, JUnit
- **Go**: Gin, Gorilla, Echo, Fiber
- **Ruby**: Rails, Sinatra

### Package Managers
npm, yarn, pnpm, pip, pipenv, poetry, bundler, composer, maven, gradle, cargo, go modules, swift package manager, pub, mix, sbt, cocoapods

### Build Tools
Make, CMake, webpack, Vite, Rollup, Gradle, Maven, Gulp, Grunt, TypeScript Compiler, Babel, esbuild

### DevOps Tools
Docker, Docker Compose, Kubernetes, Helm, GitHub Actions, Jenkins, Travis CI, CircleCI, GitLab CI, Azure Pipelines, Terraform, Ansible, Vagrant

## 🤖 GitHub Actions Integration

Use Stack-Scout in your CI/CD pipeline:

```yaml
name: Technology Stack Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install Stack-Scout
        run: |
          pip install stack-scout
      
      - name: Run Stack-Scout
        run: |
          stack-scout . --json stack-report.json
          cat stack-report.json
      
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: stack-report
          path: stack-report.json
```

## 🧪 Testing

Run tests (if available):

```bash
pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Limitations

- GitHub repository scanning (remote) is not yet implemented
- Version detection is best-effort and may not be accurate for all tools
- Binary files and very large files are skipped
- Symbolic links are not followed

## 🗺️ Roadmap

- [ ] GitHub API integration for remote repository scanning
- [ ] Database detection (PostgreSQL, MySQL, MongoDB, etc.)
- [ ] Cloud provider detection (AWS, GCP, Azure)
- [ ] License detection
- [ ] Security vulnerability scanning integration
- [ ] Web UI for results visualization
- [ ] Plugin system for custom detectors

## 📧 Support

For issues, questions, or contributions, please open an issue on GitHub.
