"""File scanner for reading project files."""

import os
from typing import List, Dict, Set, Tuple, Optional
from pathlib import Path


class FileScanner:
    """Scans a directory for files and reads their contents."""
    
    # Files we care about for detection
    INTERESTING_FILES = {
        # JavaScript/TypeScript
        "package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
        "tsconfig.json", "webpack.config.js", "webpack.config.ts",
        "vite.config.js", "vite.config.ts", "rollup.config.js",
        "babel.config.js", ".babelrc", "next.config.js", "nuxt.config.js",
        
        # Python
        "requirements.txt", "setup.py", "pyproject.toml", "Pipfile", "Pipfile.lock",
        "poetry.lock", "setup.cfg", "tox.ini", "pytest.ini",
        
        # Java
        "pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle",
        "build.xml", "build.sbt",
        
        # Go
        "go.mod", "go.sum",
        
        # Ruby
        "Gemfile", "Gemfile.lock", "Rakefile",
        
        # PHP
        "composer.json", "composer.lock",
        
        # Rust
        "Cargo.toml", "Cargo.lock",
        
        # Swift
        "Package.swift", "Podfile",
        
        # Dart
        "pubspec.yaml",
        
        # Elixir
        "mix.exs",
        
        # Clojure
        "project.clj",
        
        # Build tools
        "Makefile", "makefile", "CMakeLists.txt", "gulpfile.js", "Gruntfile.js",
        
        # DevOps
        "Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".dockerignore",
        "Jenkinsfile", ".travis.yml", ".gitlab-ci.yml", "azure-pipelines.yml",
        "bitbucket-pipelines.yml", ".drone.yml", "appveyor.yml",
        "Vagrantfile", "Chart.yaml", "skaffold.yaml",
    }
    
    # Directories to skip
    SKIP_DIRS = {
        ".git", ".svn", ".hg", ".bzr",
        "node_modules", "venv", "env", ".env", "virtualenv", ".venv",
        "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
        "dist", "build", "target", "out", "bin", "obj",
        ".idea", ".vscode", ".vs",
        "vendor", "Pods",
        ".terraform",
    }
    
    # File extensions to track
    CODE_EXTENSIONS = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb", ".php",
        ".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".cs", ".rs", ".swift",
        ".kt", ".kts", ".scala", ".sh", ".bash", ".r", ".R", ".dart", ".lua",
        ".pl", ".ex", ".exs", ".clj", ".cljs", ".hs", ".erl", ".sql",
        ".html", ".css", ".scss", ".sass", ".less",
    }
    
    # Max file size to read (1MB)
    MAX_FILE_SIZE = 1024 * 1024
    
    def __init__(self, root_path: str, max_depth: int = 10):
        """
        Initialize the file scanner.
        
        Args:
            root_path: Root directory to scan
            max_depth: Maximum directory depth to scan
        """
        self.root_path = os.path.abspath(root_path)
        self.max_depth = max_depth
    
    def scan(self) -> Tuple[List[str], Dict[str, str]]:
        """
        Scan the directory for files.
        
        Returns:
            Tuple of (file_paths, file_contents)
            - file_paths: List of all relevant file paths
            - file_contents: Dict mapping file paths to their contents
        """
        file_paths = []
        file_contents = {}
        
        for root, dirs, files in os.walk(self.root_path):
            # Calculate depth
            depth = root[len(self.root_path):].count(os.sep)
            if depth > self.max_depth:
                continue
            
            # Filter out skip directories
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.root_path)
                
                # Track all code files
                _, ext = os.path.splitext(file)
                if ext in self.CODE_EXTENSIONS:
                    file_paths.append(relative_path)
                
                # Track interesting config files
                if file in self.INTERESTING_FILES:
                    file_paths.append(relative_path)
                    # Read content for interesting files
                    content = self._read_file(file_path)
                    if content is not None:
                        file_contents[relative_path] = content
                
                # Check for GitHub Actions workflows
                if ".github/workflows" in root and file.endswith((".yml", ".yaml")):
                    file_paths.append(relative_path)
                    content = self._read_file(file_path)
                    if content is not None:
                        file_contents[relative_path] = content
                
                # Check for Kubernetes/Terraform files
                if any(keyword in root for keyword in ["k8s", "kubernetes", "terraform", "ansible"]):
                    if file.endswith((".yml", ".yaml", ".tf")):
                        file_paths.append(relative_path)
        
        return file_paths, file_contents
    
    def _read_file(self, file_path: str) -> Optional[str]:
        """
        Read file content safely.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File content or None if unreadable
        """
        try:
            # Check file size
            if os.path.getsize(file_path) > self.MAX_FILE_SIZE:
                return None
            
            # Try to read as text
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            # If we can't read it, skip it
            return None
