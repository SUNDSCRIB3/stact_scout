"""Language detector for identifying programming languages."""

import json
import os
from typing import List, Dict
from .base import Detector, DetectionResult


class LanguageDetector(Detector):
    """Detects programming languages used in a project."""
    
    # Map file extensions to languages
    EXTENSION_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".jsx": "JavaScript",
        ".tsx": "TypeScript",
        ".java": "Java",
        ".go": "Go",
        ".rb": "Ruby",
        ".php": "PHP",
        ".c": "C",
        ".cpp": "C++",
        ".cc": "C++",
        ".cxx": "C++",
        ".h": "C/C++",
        ".hpp": "C++",
        ".cs": "C#",
        ".rs": "Rust",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".kts": "Kotlin",
        ".scala": "Scala",
        ".sh": "Shell",
        ".bash": "Shell",
        ".r": "R",
        ".R": "R",
        ".dart": "Dart",
        ".lua": "Lua",
        ".pl": "Perl",
        ".ex": "Elixir",
        ".exs": "Elixir",
        ".clj": "Clojure",
        ".cljs": "ClojureScript",
        ".hs": "Haskell",
        ".erl": "Erlang",
        ".sql": "SQL",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".sass": "Sass",
        ".less": "Less",
    }
    
    # Config files that indicate languages
    CONFIG_FILES = {
        "requirements.txt": "Python",
        "setup.py": "Python",
        "pyproject.toml": "Python",
        "Pipfile": "Python",
        "package.json": "JavaScript/TypeScript",
        "pom.xml": "Java",
        "build.gradle": "Java",
        "build.gradle.kts": "Kotlin",
        "go.mod": "Go",
        "Gemfile": "Ruby",
        "composer.json": "PHP",
        "Cargo.toml": "Rust",
        "Package.swift": "Swift",
        "pubspec.yaml": "Dart",
        "mix.exs": "Elixir",
        "project.clj": "Clojure",
    }
    
    def detect(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect programming languages."""
        language_files = {}
        
        for file_path in file_paths:
            # Check by extension
            _, ext = os.path.splitext(file_path)
            if ext in self.EXTENSION_MAP:
                lang = self.EXTENSION_MAP[ext]
                if lang not in language_files:
                    language_files[lang] = []
                language_files[lang].append(file_path)
            
            # Check by config file
            basename = os.path.basename(file_path)
            if basename in self.CONFIG_FILES:
                lang = self.CONFIG_FILES[basename]
                if lang not in language_files:
                    language_files[lang] = []
                language_files[lang].append(file_path)
        
        results = []
        for lang, files in language_files.items():
            version = self._detect_version(lang, files, file_contents)
            results.append(DetectionResult(
                category="language",
                name=lang,
                version=version,
                confidence="high",
                source_files=files[:5],  # Limit to 5 example files
                metadata={"file_count": len(files)}
            ))
        
        return results
    
    def _detect_version(self, language: str, files: List[str], file_contents: Dict[str, str]) -> str:
        """Try to detect language version from config files."""
        if language == "Python":
            for file in files:
                if file in file_contents:
                    content = file_contents[file]
                    # Check pyproject.toml
                    if "pyproject.toml" in file and "requires-python" in content:
                        try:
                            for line in content.split("\n"):
                                if "requires-python" in line and "=" in line:
                                    # Split on first = only
                                    parts = line.split("=", 1)
                                    if len(parts) > 1:
                                        return parts[1].strip().strip('"\'')
                        except (ValueError, KeyError):
                            pass
                    # Check setup.py
                    if "setup.py" in file and "python_requires" in content:
                        try:
                            for line in content.split("\n"):
                                if "python_requires" in line:
                                    parts = line.split("=")
                                    if len(parts) > 1:
                                        return parts[1].strip().strip('",\'')
                        except (ValueError, KeyError, IndexError):
                            pass
        
        elif language in ["JavaScript/TypeScript", "JavaScript", "TypeScript"]:
            for file in files:
                if "package.json" in file and file in file_contents:
                    try:
                        package_data = json.loads(file_contents[file])
                        if "engines" in package_data and "node" in package_data["engines"]:
                            return package_data["engines"]["node"]
                    except (json.JSONDecodeError, KeyError):
                        pass
        
        elif language == "Go":
            for file in files:
                if "go.mod" in file and file in file_contents:
                    content = file_contents[file]
                    for line in content.split("\n"):
                        if line.strip().startswith("go "):
                            return line.split()[1]
        
        return ""
