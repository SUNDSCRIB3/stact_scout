"""Data models for Stack Scout."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Evidence:
    """Evidence for a detection"""
    file_path: str
    reason: str
    line_number: Optional[int] = None


@dataclass
class Detection:
    """A detected technology or tool"""
    name: str
    category: str  # language, framework, build_tool, devops
    confidence: str  # high, medium, low
    evidence: List[Evidence]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Report:
    """Complete scan report"""
    project_path: str
    scan_timestamp: str
    detections: List[Detection]
    summary: Dict[str, List[str]] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary for JSON serialization"""
        return {
            'project_path': self.project_path,
            'scan_timestamp': self.scan_timestamp,
            'summary': self.summary,
            'detections': [
                {
                    'name': d.name,
                    'category': d.category,
                    'confidence': d.confidence,
                    'evidence': [
                        {
                            'file_path': e.file_path,
                            'reason': e.reason,
                            'line_number': e.line_number
                        } for e in d.evidence
                    ],
                    'metadata': d.metadata
                } for d in self.detections
            ]
        }
