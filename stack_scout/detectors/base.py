"""Base detector class for technology detection."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class DetectionResult:
    """Result of a technology detection."""
    
    category: str  # e.g., "language", "framework", "package_manager"
    name: str  # e.g., "Python", "React", "npm"
    version: str = ""  # Optional version information
    confidence: str = "high"  # high, medium, low
    source_files: List[str] = field(default_factory=list)  # Files that led to detection
    metadata: Dict[str, Any] = field(default_factory=dict)  # Additional info
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "category": self.category,
            "name": self.name,
            "version": self.version,
            "confidence": self.confidence,
            "source_files": self.source_files,
            "metadata": self.metadata,
        }


class Detector(ABC):
    """Base class for all technology detectors."""
    
    @abstractmethod
    def detect(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        """
        Detect technologies based on file paths and contents.
        
        Args:
            file_paths: List of file paths in the project
            file_contents: Dictionary mapping file paths to their contents
            
        Returns:
            List of DetectionResult objects
        """
        pass
