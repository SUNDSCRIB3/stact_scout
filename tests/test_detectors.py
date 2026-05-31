"""Tests for Stack-Scout detectors."""

import pytest
from stack_scout.detectors.base import DetectionResult, Detector
from stack_scout.detectors.language_detector import LanguageDetector
from stack_scout.detectors.framework_detector import FrameworkDetector
from stack_scout.detectors.package_manager_detector import PackageManagerDetector
from stack_scout.detectors.build_tool_detector import BuildToolDetector
from stack_scout.detectors.devops_detector import DevOpsDetector


class TestDetectionResult:
    def test_to_dict(self):
        result = DetectionResult(
            category="language",
            name="Python",
            version=">=3.8",
            source_files=["setup.py", "requirements.txt"],
            metadata={"file_count": 42},
        )
        d = result.to_dict()
        assert d["category"] == "language"
        assert d["name"] == "Python"
        assert d["version"] == ">=3.8"
        assert d["source_files"] == ["setup.py", "requirements.txt"]
        assert d["metadata"]["file_count"] == 42


class TestLanguageDetector:
    def test_python_detection(self):
        detector = LanguageDetector()
        paths = ["app.py", "utils/helpers.py", "requirements.txt"]
        contents = {"requirements.txt": "flask==2.0.0\ndjango>=3.2"}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Python" in names

    def test_javascript_detection(self):
        detector = LanguageDetector()
        paths = ["index.js", "app.ts", "components/Button.jsx"]
        contents = {}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert names >= {"JavaScript", "TypeScript"}

    def test_rust_detection(self):
        detector = LanguageDetector()
        paths = ["src/main.rs", "Cargo.toml"]
        contents = {"Cargo.toml": '[package]\nname = "test"'}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Rust" in names

    def test_go_detection(self):
        detector = LanguageDetector()
        paths = ["main.go", "go.mod", "pkg/handler.go"]
        contents = {"go.mod": "module example.com/pkg"}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Go" in names


class TestFrameworkDetector:
    def test_django_detection(self):
        detector = FrameworkDetector()
        paths = ["manage.py", "requirements.txt"]
        contents = {"requirements.txt": "django>=3.2"}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Django" in names

    def test_react_detection(self):
        detector = FrameworkDetector()
        paths = ["package.json", "src/App.jsx"]
        contents = {"package.json": '{"dependencies": {"react": "^18.0.0"}}'}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "React" in names

    def test_express_detection(self):
        detector = FrameworkDetector()
        paths = ["package.json"]
        contents = {"package.json": '{"dependencies": {"express": "^4.18.0"}}'}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Express" in names


class TestPackageManagerDetector:
    def test_npm_detection(self):
        detector = PackageManagerDetector()
        paths = ["package.json", "package-lock.json"]
        contents = {}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Node Package Manager" in names

    def test_pip_detection(self):
        detector = PackageManagerDetector()
        paths = ["requirements.txt"]
        contents = {}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "pip" in names

    def test_cargo_detection(self):
        detector = PackageManagerDetector()
        paths = ["Cargo.toml", "Cargo.lock"]
        contents = {}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Cargo" in names


class TestBuildToolDetector:
    def test_make_detection(self):
        detector = BuildToolDetector()
        paths = ["Makefile", "src/main.c"]
        contents = {}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Make" in names

    def test_cmake_detection(self):
        detector = BuildToolDetector()
        paths = ["CMakeLists.txt"]
        contents = {}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "CMake" in names


class TestDevOpsDetector:
    def test_docker_detection(self):
        detector = DevOpsDetector()
        paths = ["Dockerfile", "docker-compose.yml"]
        contents = {}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Docker" in names

    def test_kubernetes_detection(self):
        detector = DevOpsDetector()
        paths = ["k8s/deployment.yaml", "helm/Chart.yaml"]
        contents = {"k8s/deployment.yaml": "apiVersion: apps/v1\nkind: Deployment"}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "Kubernetes" in names

    def test_github_actions_detection(self):
        detector = DevOpsDetector()
        paths = [".github/workflows/ci.yml"]
        contents = {".github/workflows/ci.yml": "on: [push]"}
        results = detector.detect(paths, contents)
        names = {r.name for r in results}
        assert "GitHub Actions" in names
