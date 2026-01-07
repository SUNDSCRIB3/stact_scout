"""Tests for scanner."""

import pytest
from pathlib import Path
from stack_scout.scanner import Scanner


def test_scanner():
    """Test scanner on sample project."""
    scanner = Scanner()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    report = scanner.scan(str(project_path))
    
    # Check report structure
    assert report.project_path
    assert report.scan_timestamp
    assert len(report.detections) > 0
    assert len(report.summary) > 0
    
    # Check categories are present
    assert 'language' in report.summary
    assert 'framework' in report.summary
    assert 'build_tool' in report.summary
    assert 'devops' in report.summary
    
    # Check some expected detections
    all_names = [d.name for d in report.detections]
    assert 'Python' in all_names
    assert 'TypeScript' in all_names
    assert 'React' in all_names
    assert 'FastAPI' in all_names
    assert 'Docker' in all_names


def test_scanner_to_dict():
    """Test report serialization."""
    scanner = Scanner()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    report = scanner.scan(str(project_path))
    report_dict = report.to_dict()
    
    # Check dict structure
    assert 'project_path' in report_dict
    assert 'scan_timestamp' in report_dict
    assert 'detections' in report_dict
    assert 'summary' in report_dict
    
    # Check detections structure
    assert len(report_dict['detections']) > 0
    first_detection = report_dict['detections'][0]
    assert 'name' in first_detection
    assert 'category' in first_detection
    assert 'confidence' in first_detection
    assert 'evidence' in first_detection
    assert 'metadata' in first_detection


def test_scanner_nonexistent_path():
    """Test scanner with non-existent path."""
    scanner = Scanner()
    
    with pytest.raises(FileNotFoundError):
        scanner.scan('/nonexistent/path')
