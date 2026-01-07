"""Tests for CLI."""

import json
from pathlib import Path
from click.testing import CliRunner
from stack_scout.cli import cli


def test_cli_scan_text():
    """Test CLI scan command with text output."""
    runner = CliRunner()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    result = runner.invoke(cli, ['scan', str(project_path)])
    
    assert result.exit_code == 0
    assert 'Stack Scout Report' in result.output
    assert 'Languages' in result.output
    assert 'Frameworks' in result.output


def test_cli_scan_json():
    """Test CLI scan command with JSON output."""
    runner = CliRunner()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    result = runner.invoke(cli, ['scan', str(project_path), '--format', 'json'])
    
    assert result.exit_code == 0
    
    # Parse JSON output
    data = json.loads(result.output)
    assert 'project_path' in data
    assert 'detections' in data
    assert len(data['detections']) > 0


def test_cli_scan_output_file():
    """Test CLI scan command with output file."""
    runner = CliRunner()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ['scan', str(project_path), '--output', 'report.txt'])
        
        assert result.exit_code == 0
        assert Path('report.txt').exists()


def test_cli_scan_verbose():
    """Test CLI scan command with verbose flag."""
    runner = CliRunner()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    result = runner.invoke(cli, ['scan', str(project_path), '--verbose'])
    
    assert result.exit_code == 0
    assert 'Stack Scout Report' in result.output
