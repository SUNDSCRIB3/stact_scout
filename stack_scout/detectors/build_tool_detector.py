"""Build tool detector."""

import os
from typing import List, Dict
from .base import Detector, DetectionResult


class BuildToolDetector(Detector):
    """Detects build tools used in a project."""
    
    # Map files to build tools
    BUILD_TOOL_FILES = {
        "Makefile": "Make",
        "makefile": "Make",
        "CMakeLists.txt": "CMake",
        "webpack.config.js": "webpack",
        "webpack.config.ts": "webpack",
        "rollup.config.js": "Rollup",
        "vite.config.js": "Vite",
        "vite.config.ts": "Vite",
        "gulpfile.js": "Gulp",
        "Gruntfile.js": "Grunt",
        "build.gradle": "Gradle",
        "build.gradle.kts": "Gradle",
        "pom.xml": "Maven",
        "build.xml": "Ant",
        "build.sbt": "sbt",
        "Rakefile": "Rake",
        "setup.py": "setuptools",
        "pyproject.toml": "build (PEP 517)",
        "tsconfig.json": "TypeScript Compiler",
        "babel.config.js": "Babel",
        ".babelrc": "Babel",
        "esbuild.config.js": "esbuild",
    }
    
    # Scripts in package.json that indicate build tools
    NPM_SCRIPT_PATTERNS = {
        "webpack": "webpack",
        "vite": "Vite",
        "rollup": "Rollup",
        "parcel": "Parcel",
        "esbuild": "esbuild",
        "tsc": "TypeScript Compiler",
        "babel": "Babel",
    }
    
    def detect(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect build tools."""
        results = []
        detected = set()
        
        # Check by config files
        for file_path in file_paths:
            basename = os.path.basename(file_path)
            if basename in self.BUILD_TOOL_FILES:
                tool = self.BUILD_TOOL_FILES[basename]
                if tool not in detected:
                    detected.add(tool)
                    results.append(DetectionResult(
                        category="build_tool",
                        name=tool,
                        confidence="high",
                        source_files=[file_path],
                    ))
        
        # Check package.json scripts
        for file_path in file_paths:
            if "package.json" in file_path and file_path in file_contents:
                try:
                    import json
                    package_data = json.loads(file_contents[file_path])
                    scripts = package_data.get("scripts", {})
                    
                    for script_name, script_content in scripts.items():
                        for pattern, tool in self.NPM_SCRIPT_PATTERNS.items():
                            if pattern in script_content and tool not in detected:
                                detected.add(tool)
                                results.append(DetectionResult(
                                    category="build_tool",
                                    name=tool,
                                    confidence="medium",
                                    source_files=[file_path],
                                    metadata={"script": script_name}
                                ))
                except:
                    pass
        
        return results
