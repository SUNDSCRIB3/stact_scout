"""Tests for Stack-Scout scanner and formatters."""

import json
import tempfile
import os
from stack_scout.scanner import StackScanner
from stack_scout.formatters.console_formatter import ConsoleFormatter
from stack_scout.formatters.json_formatter import JSONFormatter


class TestStackScanner:
    def test_scan_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            scanner = StackScanner()
            results = scanner.scan_directory(tmpdir)
            assert isinstance(results, list)

    def test_scan_python_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mock Python project
            os.makedirs(os.path.join(tmpdir, "src"))
            with open(os.path.join(tmpdir, "requirements.txt"), "w") as f:
                f.write("flask>=2.0\ndjango>=3.2\n")
            with open(os.path.join(tmpdir, "src", "app.py"), "w") as f:
                f.write("print('hello')")
            
            scanner = StackScanner()
            results = scanner.scan_directory(tmpdir)
            names = {r.name for r in results}
            assert "Python" in names
            assert "pip" in names or "Flask" in names or "Django" in names

    def test_scan_node_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "package.json"), "w") as f:
                f.write('{"dependencies": {"react": "^18.0.0", "express": "^4.18.0"}}')
            with open(os.path.join(tmpdir, "index.js"), "w") as f:
                f.write("console.log('hello')")
            
            scanner = StackScanner()
            results = scanner.scan_directory(tmpdir)
            names = {r.name for r in results}
            assert "JavaScript" in names
            assert "React" in names or "Express" in names


class TestConsoleFormatter:
    def test_format_with_results(self):
        from stack_scout.detectors.base import DetectionResult
        
        results = [
            DetectionResult("language", "Python", ">=3.8", "high", ["setup.py"], {"file_count": 10}),
            DetectionResult("framework", "Flask", ">=2.0", "high", ["requirements.txt"], {}),
        ]
        formatter = ConsoleFormatter(use_colors=False)
        output = formatter.format(results, "/test/project")
        assert "Stack-Scout Analysis Report" in output
        assert "Python" in output
        assert "Flask" in output

    def test_format_empty(self):
        formatter = ConsoleFormatter(use_colors=False)
        output = formatter.format([], "/test/project")
        assert "No technologies detected" in output


class TestJSONFormatter:
    def test_format_json(self):
        from stack_scout.detectors.base import DetectionResult
        
        results = [
            DetectionResult("language", "Python", "", "high", ["app.py"], {}),
        ]
        formatter = JSONFormatter()
        output = formatter.format(results, "/test/project")
        data = json.loads(output)
        assert data["project_path"] == "/test/project"
        assert data["technologies"]["language"][0]["name"] == "Python"
        assert data["summary"]["total_technologies"] == 1
