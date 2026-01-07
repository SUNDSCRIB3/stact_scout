"""Framework detector for identifying frameworks and libraries."""

import json
import os
from typing import List, Dict
from .base import Detector, DetectionResult


class FrameworkDetector(Detector):
    """Detects frameworks and libraries used in a project."""
    
    # Patterns to look for in package.json dependencies
    NPM_FRAMEWORKS = {
        "react": "React",
        "react-dom": "React",
        "@angular/core": "Angular",
        "vue": "Vue.js",
        "svelte": "Svelte",
        "next": "Next.js",
        "nuxt": "Nuxt.js",
        "express": "Express",
        "nestjs": "NestJS",
        "koa": "Koa",
        "fastify": "Fastify",
        "gatsby": "Gatsby",
        "electron": "Electron",
        "react-native": "React Native",
    }
    
    # Patterns in Python requirements/setup
    PYTHON_FRAMEWORKS = {
        "django": "Django",
        "flask": "Flask",
        "fastapi": "FastAPI",
        "pyramid": "Pyramid",
        "tornado": "Tornado",
        "bottle": "Bottle",
        "sanic": "Sanic",
        "aiohttp": "aiohttp",
        "streamlit": "Streamlit",
        "pytest": "pytest",
        "numpy": "NumPy",
        "pandas": "Pandas",
        "tensorflow": "TensorFlow",
        "torch": "PyTorch",
        "keras": "Keras",
        "scikit-learn": "scikit-learn",
        "scrapy": "Scrapy",
        "celery": "Celery",
    }
    
    # Java frameworks (pom.xml, build.gradle)
    JAVA_FRAMEWORKS = {
        "spring-boot": "Spring Boot",
        "spring-framework": "Spring",
        "junit": "JUnit",
        "hibernate": "Hibernate",
        "struts": "Struts",
        "play": "Play Framework",
        "vertx": "Vert.x",
    }
    
    # Go frameworks (go.mod)
    GO_FRAMEWORKS = {
        "gin-gonic/gin": "Gin",
        "gorilla/mux": "Gorilla Mux",
        "echo": "Echo",
        "fiber": "Fiber",
        "beego": "Beego",
    }
    
    # Ruby frameworks (Gemfile)
    RUBY_FRAMEWORKS = {
        "rails": "Ruby on Rails",
        "sinatra": "Sinatra",
        "rspec": "RSpec",
    }
    
    def detect(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect frameworks and libraries."""
        results = []
        
        # Check package.json for JavaScript frameworks
        results.extend(self._detect_npm_frameworks(file_paths, file_contents))
        
        # Check Python dependencies
        results.extend(self._detect_python_frameworks(file_paths, file_contents))
        
        # Check Java dependencies
        results.extend(self._detect_java_frameworks(file_paths, file_contents))
        
        # Check Go dependencies
        results.extend(self._detect_go_frameworks(file_paths, file_contents))
        
        # Check Ruby dependencies
        results.extend(self._detect_ruby_frameworks(file_paths, file_contents))
        
        return results
    
    def _detect_npm_frameworks(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect JavaScript/TypeScript frameworks from package.json."""
        results = []
        
        for file_path in file_paths:
            if "package.json" in file_path and file_path in file_contents:
                try:
                    package_data = json.loads(file_contents[file_path])
                    dependencies = {**package_data.get("dependencies", {}), 
                                  **package_data.get("devDependencies", {})}
                    
                    for dep, version in dependencies.items():
                        for pattern, framework in self.NPM_FRAMEWORKS.items():
                            if pattern in dep:
                                results.append(DetectionResult(
                                    category="framework",
                                    name=framework,
                                    version=version,
                                    confidence="high",
                                    source_files=[file_path],
                                    metadata={"package": dep}
                                ))
                except:
                    pass
        
        return results
    
    def _detect_python_frameworks(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect Python frameworks from requirements.txt, setup.py, etc."""
        results = []
        detected = set()
        
        for file_path in file_paths:
            basename = os.path.basename(file_path)
            if basename in ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"] and file_path in file_contents:
                content = file_contents[file_path].lower()
                
                for pattern, framework in self.PYTHON_FRAMEWORKS.items():
                    if pattern in content and framework not in detected:
                        detected.add(framework)
                        # Try to extract version
                        version = self._extract_python_version(file_contents[file_path], pattern)
                        results.append(DetectionResult(
                            category="framework",
                            name=framework,
                            version=version,
                            confidence="high",
                            source_files=[file_path],
                            metadata={"package": pattern}
                        ))
        
        return results
    
    def _detect_java_frameworks(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect Java frameworks from pom.xml, build.gradle."""
        results = []
        detected = set()
        
        for file_path in file_paths:
            basename = os.path.basename(file_path)
            if basename in ["pom.xml", "build.gradle", "build.gradle.kts"] and file_path in file_contents:
                content = file_contents[file_path].lower()
                
                for pattern, framework in self.JAVA_FRAMEWORKS.items():
                    if pattern in content and framework not in detected:
                        detected.add(framework)
                        results.append(DetectionResult(
                            category="framework",
                            name=framework,
                            confidence="high",
                            source_files=[file_path],
                        ))
        
        return results
    
    def _detect_go_frameworks(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect Go frameworks from go.mod."""
        results = []
        detected = set()
        
        for file_path in file_paths:
            if "go.mod" in file_path and file_path in file_contents:
                content = file_contents[file_path]
                
                for pattern, framework in self.GO_FRAMEWORKS.items():
                    if pattern in content and framework not in detected:
                        detected.add(framework)
                        results.append(DetectionResult(
                            category="framework",
                            name=framework,
                            confidence="high",
                            source_files=[file_path],
                        ))
        
        return results
    
    def _detect_ruby_frameworks(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """Detect Ruby frameworks from Gemfile."""
        results = []
        detected = set()
        
        for file_path in file_paths:
            if "Gemfile" in os.path.basename(file_path) and file_path in file_contents:
                content = file_contents[file_path].lower()
                
                for pattern, framework in self.RUBY_FRAMEWORKS.items():
                    if pattern in content and framework not in detected:
                        detected.add(framework)
                        results.append(DetectionResult(
                            category="framework",
                            name=framework,
                            confidence="high",
                            source_files=[file_path],
                        ))
        
        return results
    
    def _extract_python_version(self, content: str, package: str) -> str:
        """Extract version from Python dependency files."""
        for line in content.split("\n"):
            if package in line.lower():
                if "==" in line:
                    return line.split("==")[1].strip().split()[0]
                elif ">=" in line:
                    return ">=" + line.split(">=")[1].strip().split()[0]
        return ""
