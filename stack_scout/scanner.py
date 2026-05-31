"""Main scanner engine that coordinates detection."""

from typing import List
from .scanners import FileScanner
from .detectors import (
    DetectionResult,
    LanguageDetector,
    FrameworkDetector,
    PackageManagerDetector,
    BuildToolDetector,
    DevOpsDetector,
    DatabaseDetector,
    CloudDetector,
    LicenseDetector,
)


class StackScanner:
    """Main scanner that coordinates all detectors."""
    
    def __init__(self):
        """Initialize the scanner with all detectors."""
        self.detectors = [
            LanguageDetector(),
            FrameworkDetector(),
            PackageManagerDetector(),
            BuildToolDetector(),
            DevOpsDetector(),
            DatabaseDetector(),
            CloudDetector(),
            LicenseDetector(),
        ]
    
    def scan_directory(self, path: str) -> List[DetectionResult]:
        """
        Scan a local directory for technologies.
        
        Args:
            path: Path to the directory to scan
            
        Returns:
            List of detection results
        """
        # Scan files
        scanner = FileScanner(path)
        file_paths, file_contents = scanner.scan()
        
        # Run all detectors
        results = []
        for detector in self.detectors:
            results.extend(detector.detect(file_paths, file_contents))
        
        return results
