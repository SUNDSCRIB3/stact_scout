"""Tests for Stack-Scout CLI."""

import tempfile
import os
from stack_scout.cli import main


class TestCLI:
    def test_version_flag(self, capsys, monkeypatch):
        import sys
        testargs = ["stack-scout", "--version"]
        monkeypatch.setattr(sys, "argv", testargs)
        try:
            main()
        except SystemExit:
            pass
        # Version flag causes system exit; just verifying it doesn't crash

    def test_invalid_path(self, capsys, monkeypatch):
        import sys
        testargs = ["stack-scout", "/nonexistent/path"]
        monkeypatch.setattr(sys, "argv", testargs)
        result = main()
        assert result == 1

    def test_scan_temp_dir(self, capsys, monkeypatch):
        import sys
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "app.py"), "w") as f:
                f.write("print('hello')")
            
            testargs = ["stack-scout", tmpdir, "--no-color"]
            monkeypatch.setattr(sys, "argv", testargs)
            result = main()
            assert result == 0
            captured = capsys.readouterr()
            assert "Stack-Scout Analysis Report" in captured.out

    def test_json_output(self, capsys, monkeypatch):
        import sys
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, "app.py"), "w") as f:
                f.write("print('hello')")
            
            json_path = os.path.join(tmpdir, "report.json")
            testargs = ["stack-scout", tmpdir, "--json", json_path, "--no-color"]
            monkeypatch.setattr(sys, "argv", testargs)
            result = main()
            assert result == 0
            assert os.path.exists(json_path)
