"""Tests for detectors."""

import pytest
from pathlib import Path
from stack_scout.detectors import (
    LanguageDetector,
    FrameworkDetector,
    BuildToolsDetector,
    DevOpsDetector,
)


def test_language_detector():
    """Test language detector on sample project."""
    detector = LanguageDetector()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    detections = detector.detect(project_path)
    
    # Should detect Python and TypeScript
    detected_names = [d.name for d in detections]
    assert 'Python' in detected_names
    assert 'TypeScript' in detected_names
    
    # Check that detections have evidence
    for detection in detections:
        assert len(detection.evidence) > 0
        assert detection.confidence in ['high', 'medium', 'low']


def test_framework_detector():
    """Test framework detector on sample project."""
    detector = FrameworkDetector()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    detections = detector.detect(project_path)
    
    # Should detect React and FastAPI
    detected_names = [d.name for d in detections]
    assert 'React' in detected_names
    assert 'FastAPI' in detected_names


def test_framework_detector_python_requirement_without_version(tmp_path: Path):
    """Unversioned requirements (e.g. 'fastapi') should be detected."""
    (tmp_path / "requirements.txt").write_text("fastapi  # no pin\n", encoding="utf-8")

    detector = FrameworkDetector()
    detections = detector.detect(tmp_path)
    detected_names = [d.name for d in detections]

    assert "FastAPI" in detected_names


def test_build_tools_detector():
    """Test build tools detector on sample project."""
    detector = BuildToolsDetector()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    detections = detector.detect(project_path)
    
    # Should detect various build tools
    detected_names = [d.name for d in detections]
    assert 'TypeScript' in detected_names
    assert 'ESLint' in detected_names
    assert 'Prettier' in detected_names
    assert 'pip' in detected_names


def test_devops_detector():
    """Test DevOps detector on sample project."""
    detector = DevOpsDetector()
    project_path = Path(__file__).parent.parent / 'examples' / 'sample-project'
    
    detections = detector.detect(project_path)
    
    # Should detect Docker, GitHub Actions, etc.
    detected_names = [d.name for d in detections]
    assert 'Docker' in detected_names
    assert 'GitHub Actions' in detected_names
    assert 'Terraform' in detected_names
    assert 'Make' in detected_names


def test_devops_detector_circleci_nested_config(tmp_path: Path):
    """CircleCI should be detected via nested .circleci/config.yml."""
    (tmp_path / '.circleci').mkdir()
    (tmp_path / '.circleci' / 'config.yml').write_text("version: 2.1\n", encoding="utf-8")

    detector = DevOpsDetector()
    detections = detector.detect(tmp_path)
    detected_names = [d.name for d in detections]

    assert 'CircleCI' in detected_names


def test_confidence_calculation():
    """Test confidence calculation."""
    from stack_scout.detectors.base import BaseDetector
    from stack_scout.models import Evidence
    
    class TestDetector(BaseDetector):
        def detect(self, project_path):
            return []
    
    detector = TestDetector()
    
    # No evidence = low
    assert detector.calculate_confidence([]) == 'low'
    
    # 1 evidence = low
    ev1 = [Evidence('.', 'test')]
    assert detector.calculate_confidence(ev1) == 'low'
    
    # 2 evidence = medium
    ev2 = [Evidence('.', 'test'), Evidence('.', 'test2')]
    assert detector.calculate_confidence(ev2) == 'medium'
    
    # 3+ evidence = high
    ev3 = [Evidence('.', 'test'), Evidence('.', 'test2'), Evidence('.', 'test3')]
    assert detector.calculate_confidence(ev3) == 'high'
