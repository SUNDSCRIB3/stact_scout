"""Main scanning orchestrator."""

from datetime import datetime, timezone
from pathlib import Path
from typing import List
from .models import Report, Detection
from .detectors import (
    LanguageDetector,
    FrameworkDetector,
    BuildToolsDetector,
    DevOpsDetector,
)


class Scanner:
    """Main scanner that orchestrates all detectors."""
    
    def __init__(self):
        """Initialize all detectors."""
        self.detectors = [
            LanguageDetector(),
            FrameworkDetector(),
            BuildToolsDetector(),
            DevOpsDetector(),
        ]
    
    def scan(self, project_path: str) -> Report:
        """
        Scan a project directory and return a report.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            Report object with all detections
        """
        path = Path(project_path).resolve()
        
        if not path.exists():
            raise FileNotFoundError(f"Project path does not exist: {project_path}")
        
        if not path.is_dir():
            raise NotADirectoryError(f"Project path is not a directory: {project_path}")
        
        # Run all detectors
        all_detections: List[Detection] = []
        for detector in self.detectors:
            detections = detector.detect(path)
            all_detections.extend(detections)
        
        # Sort detections by category and confidence
        confidence_order = {'high': 0, 'medium': 1, 'low': 2}
        category_order = {'language': 0, 'framework': 1, 'build_tool': 2, 'devops': 3}
        
        all_detections.sort(
            key=lambda d: (category_order.get(d.category, 999), 
                          confidence_order.get(d.confidence, 999),
                          d.name)
        )
        
        # Generate summary
        summary = {}
        for detection in all_detections:
            category = detection.category
            if category not in summary:
                summary[category] = []
            summary[category].append(detection.name)
        
        # Create report
        report = Report(
            project_path=str(path),
            scan_timestamp=datetime.now(timezone.utc).isoformat(),
            detections=all_detections,
            summary=summary
        )
        
        return report
