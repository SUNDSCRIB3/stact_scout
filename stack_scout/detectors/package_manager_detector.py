"""Package manager detector."""

import os
from typing import List, Dict
from .base import Detector, DetectionResult


class PackageManagerDetector(Detector):
    """Detects package managers used in a project."""
    
    # Map files to package managers
    PACKAGE_MANAGER_FILES = {
        "package.json": ("npm", "Node Package Manager"),
        "package-lock.json": ("npm", "Node Package Manager"),
        "yarn.lock": ("yarn", "Yarn"),
        "pnpm-lock.yaml": ("pnpm", "pnpm"),
        "requirements.txt": ("pip", "pip"),
        "Pipfile": ("pipenv", "Pipenv"),
        "Pipfile.lock": ("pipenv", "Pipenv"),
        "poetry.lock": ("poetry", "Poetry"),
        "pyproject.toml": ("pip/poetry", "pip/Poetry"),
        "setup.py": ("pip", "pip"),
        "Gemfile": ("bundler", "Bundler"),
        "Gemfile.lock": ("bundler", "Bundler"),
        "composer.json": ("composer", "Composer"),
        "composer.lock": ("composer", "Composer"),
        "pom.xml": ("maven", "Maven"),
        "build.gradle": ("gradle", "Gradle"),
        "build.gradle.kts": ("gradle", "Gradle"),
        "go.mod": ("go modules", "Go Modules"),
        "go.sum": ("go modules", "Go Modules"),
        "Cargo.toml": ("cargo", "Cargo"),
        "Cargo.lock": ("cargo", "Cargo"),
        "Package.swift": ("swift", "Swift Package Manager"),
        "pubspec.yaml": ("pub", "Pub"),
        "mix.exs": ("mix", "Mix"),
        "build.sbt": ("sbt", "sbt"),
        "Podfile": ("cocoapods", "CocoaPods"),
    }
    
    def detect(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect package managers."""
        detected = {}
        
        for file_path in file_paths:
            basename = os.path.basename(file_path)
            if basename in self.PACKAGE_MANAGER_FILES:
                pm_id, pm_name = self.PACKAGE_MANAGER_FILES[basename]
                if pm_id not in detected:
                    detected[pm_id] = {
                        "name": pm_name,
                        "files": []
                    }
                detected[pm_id]["files"].append(file_path)
        
        results = []
        for pm_id, data in detected.items():
            results.append(DetectionResult(
                category="package_manager",
                name=data["name"],
                confidence="high",
                source_files=data["files"][:3],  # Limit to 3 files
            ))
        
        return results
