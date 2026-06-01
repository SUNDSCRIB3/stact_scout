     1|# Stack-Scout
     2|
     3|**Stack-Scout** is an automated codebase analysis tool that detects programming languages, frameworks, build systems, and DevOps tooling used in a project. It scans repositories, dependency files, and configuration artifacts to produce clear, auditable reports for developers, teams, and CI pipelines.
     4|
     5|## 🌟 Features
     6|
     7|- **Multi-Language Support**: Detects Python, JavaScript, TypeScript, Java, Go, Ruby, PHP, Rust, C/C++, and more
     8|- **Framework Detection**: Identifies popular frameworks like React, Django, Spring Boot, Express, and many others
     9|- **Package Manager Recognition**: Detects npm, pip, Maven, Gradle, Cargo, Bundler, Composer, and more
    10|- **Build Tool Identification**: Recognizes webpack, Vite, Make, CMake, Gradle, and other build systems
    11|- **DevOps Tooling**: Identifies Docker, Kubernetes, GitHub Actions, Jenkins, and other CI/CD tools
    12|- **Multiple Output Formats**: Colorized CLI output and structured JSON reports
    13|- **GitHub Actions Integration**: Easy to integrate into CI/CD pipelines
    14|- **Zero Dependencies**: Uses only Python standard library
    15|
    16|## 📦 Installation
    17|
    18|### From Source
    19|
    20|```bash
    21|git clone https://github.com/lukebancroft4-max/stack_scout.git
    22|cd stack_scout
    23|pip install -e .
    24|```
    25|
    26|### Using pip (after publishing)
    27|
    28|```bash
    29|pip install stack-scout
    30|```
    31|
    32|## 🚀 Usage
    33|
    34|### Command Line
    35|
    36|```bash
    37|# Scan current directory
    38|stack-scout .
    39|
    40|# Scan specific directory
    41|stack-scout /path/to/project
    42|
    43|# Generate JSON report
    44|stack-scout . --json report.json
    45|
    46|# Disable colored output
    47|stack-scout . --no-color
    48|```
    49|
    50|### Examples
    51|
    52|**Scan a Python project:**
    53|```bash
    54|stack-scout ~/my-python-project
    55|```
    56|
    57|**Scan and save JSON report:**
    58|```bash
    59|stack-scout ~/my-project --json tech-stack.json
    60|```
    61|
    62|## 📊 Output
    63|
    64|### Console Output
    65|
    66|Stack-Scout provides a colorized, human-readable summary:
    67|
    68|```
    69|================================================================================
    70|Stack-Scout Analysis Report
    71|Project: /path/to/project
    72|================================================================================
    73|
    74|📊 Summary:
    75|  📝 Languages: 3 detected
    76|  🔧 Frameworks: 5 detected
    77|  📦 Package Managers: 2 detected
    78|  🔨 Build Tools: 3 detected
    79|  🚀 DevOps: 2 detected
    80|
    81|📝 Languages
    82|------------
    83|  • Python (>=3.8)
    84|    Source: requirements.txt, setup.py
    85|  • JavaScript/TypeScript
    86|    Source: package.json
    87|  • Shell
    88|    Source: scripts/deploy.sh
    89|
    90|🔧 Frameworks
    91|-------------
    92|  • Django (>=4.0)
    93|    Source: requirements.txt
    94|    Package: django
    95|  • React (^18.0.0)
    96|    Source: package.json
    97|    Package: react
    98|
    99|... (more details)
   100|
   101|================================================================================
   102|Total technologies detected: 15
   103|================================================================================
   104|```
   105|
   106|### JSON Output
   107|
   108|```json
   109|{
   110|  "project_path": "/path/to/project",
   111|  "scan_timestamp": "2024-01-07T10:00:00Z",
   112|  "summary": {
   113|    "total_technologies": 15,
   114|    "by_category": {
   115|      "language": 3,
   116|      "framework": 5,
   117|      "package_manager": 2,
   118|      "build_tool": 3,
   119|      "devops": 2
   120|    }
   121|  },
   122|  "technologies": {
   123|    "language": [
   124|      {
   125|        "category": "language",
   126|        "name": "Python",
   127|        "version": ">=3.8",
   128|        "confidence": "high",
   129|        "source_files": ["requirements.txt", "setup.py"],
   130|        "metadata": {"file_count": 45}
   131|      }
   132|    ],
   133|    "framework": [...],
   134|    ...
   135|  }
   136|}
   137|```
   138|
   139|## 🔧 Architecture
   140|
   141|Stack-Scout uses a **modular, rules-based design**:
   142|
   143|```
   144|stack_scout/
   145|├── detectors/           # Technology detection modules
   146|│   ├── base.py          # Base detector class
   147|│   ├── language_detector.py
   148|│   ├── framework_detector.py
   149|│   ├── package_manager_detector.py
   150|│   ├── build_tool_detector.py
   151|│   └── devops_detector.py
   152|├── scanners/            # File scanning modules
   153|│   └── file_scanner.py
   154|├── formatters/          # Output formatting
   155|│   ├── console_formatter.py
   156|│   └── json_formatter.py
   157|├── scanner.py           # Main scanner coordinator
   158|└── cli.py               # CLI entry point
   159|```
   160|
   161|### How It Works
   162|
   163|1. **File Scanning**: Recursively scans the project directory for relevant files
   164|2. **Detection**: Applies rules-based detectors to identify technologies
   165|3. **Aggregation**: Collects and deduplicates detection results
   166|4. **Formatting**: Outputs results in human-readable or JSON format
   167|
   168|### Adding New Detectors
   169|
   170|To add support for new technologies:
   171|
   172|1. Create a new detector class extending `Detector`
   173|2. Implement the `detect()` method with your detection logic
   174|3. Add the detector to `StackScanner` in `scanner.py`
   175|
   176|Example:
   177|```python
   178|from .base import Detector, DetectionResult
   179|
   180|class MyDetector(Detector):
   181|    def detect(self, file_paths, file_contents):
   182|        results = []
   183|        # Your detection logic here
   184|        return results
   185|```
   186|
   187|## 🎯 Detection Capabilities
   188|
   189|### Languages
   190|Python, JavaScript, TypeScript, Java, Go, Ruby, PHP, C, C++, C#, Rust, Swift, Kotlin, Scala, Shell, R, Dart, Lua, Perl, Elixir, Clojure, Haskell, Erlang, SQL, HTML, CSS, SCSS
   191|
   192|### Frameworks
   193|- **Python**: Django, Flask, FastAPI, Pyramid, Streamlit
   194|- **JavaScript/TypeScript**: React, Angular, Vue.js, Svelte, Next.js, Express, NestJS
   195|- **Java**: Spring Boot, Spring, Hibernate, JUnit
   196|- **Go**: Gin, Gorilla, Echo, Fiber
   197|- **Ruby**: Rails, Sinatra
   198|
   199|### Package Managers
   200|npm, yarn, pnpm, pip, pipenv, poetry, bundler, composer, maven, gradle, cargo, go modules, swift package manager, pub, mix, sbt, cocoapods
   201|
   202|### Build Tools
   203|Make, CMake, webpack, Vite, Rollup, Gradle, Maven, Gulp, Grunt, TypeScript Compiler, Babel, esbuild
   204|
   205|### DevOps Tools
   206|Docker, Docker Compose, Kubernetes, Helm, GitHub Actions, Jenkins, Travis CI, CircleCI, GitLab CI, Azure Pipelines, Terraform, Ansible, Vagrant
   207|
   208|## 🤖 GitHub Actions Integration
   209|
   210|Use Stack-Scout in your CI/CD pipeline:
   211|
   212|```yaml
   213|name: Technology Stack Analysis
   214|
   215|on: [push, pull_request]
   216|
   217|jobs:
   218|  analyze:
   219|    runs-on: ubuntu-latest
   220|    steps:
   221|      - uses: actions/checkout@v4
   222|      
   223|      - name: Set up Python
   224|        uses: actions/setup-python@v5
   225|        with:
   226|          python-version: '3.11'
   227|      
   228|      - name: Install Stack-Scout
   229|        run: |
   230|          pip install stack-scout
   231|      
   232|      - name: Run Stack-Scout
   233|        run: |
   234|          stack-scout . --json stack-report.json
   235|          cat stack-report.json
   236|      
   237|      - name: Upload Report
   238|        uses: actions/upload-artifact@v4
   239|        with:
   240|          name: stack-report
   241|          path: stack-report.json
   242|```
   243|
   244|## 🧪 Testing
   245|
   246|Run tests (if available):
   247|
   248|```bash
   249|pytest tests/
   250|```
   251|
   252|## 📝 License
   253|
   254|This project is licensed under the MIT License - see the LICENSE file for details.
   255|
   256|## 🤝 Contributing
   257|
   258|Contributions are welcome! Please feel free to submit a Pull Request.
   259|
   260|1. Fork the repository
   261|2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
   262|3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
   263|4. Push to the branch (`git push origin feature/AmazingFeature`)
   264|5. Open a Pull Request
   265|
   266|## 🐛 Known Limitations
   267|
   268|- GitHub repository scanning (remote) is not yet implemented
   269|- Version detection is best-effort and may not be accurate for all tools
   270|- Binary files and very large files are skipped
   271|- Symbolic links are not followed
   272|
   273|## 🗺️ Roadmap
   274|
   275|- [ ] GitHub API integration for remote repository scanning
   276|- [ ] Database detection (PostgreSQL, MySQL, MongoDB, etc.)
   277|- [ ] Cloud provider detection (AWS, GCP, Azure)
   278|- [ ] License detection
   279|- [ ] Security vulnerability scanning integration
   280|- [ ] Web UI for results visualization
   281|- [ ] Plugin system for custom detectors
   282|
   283|## 📧 Support
   284|
   285|For issues, questions, or contributions, please open an issue on GitHub.
   286|