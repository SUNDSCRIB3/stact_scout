"""Base detector abstract class."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from ..models import Detection, Evidence


class BaseDetector(ABC):
    """Abstract base class for all detectors"""
    
    @abstractmethod
    def detect(self, project_path: Path) -> List[Detection]:
        """Return list of detections with evidence"""
        pass
    
    def calculate_confidence(self, evidence: List[Evidence]) -> str:
        """
        Calculate confidence level based on evidence strength
        Returns: 'high', 'medium', or 'low'
        """
        if not evidence:
            return 'low'
        
        # High: 3+ pieces of evidence
        if len(evidence) >= 3:
            return 'high'
        # Medium: 2 pieces of evidence
        elif len(evidence) == 2:
            return 'medium'
        # Low: 1 piece of evidence
        else:
            return 'low'
