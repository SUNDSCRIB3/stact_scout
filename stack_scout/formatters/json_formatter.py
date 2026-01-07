"""JSON formatter for structured output."""

import json
from typing import List, Dict, Any
from datetime import datetime
from ..detectors.base import DetectionResult


class JSONFormatter:
    """Formats detection results as JSON."""
    
    def format(self, results: List[DetectionResult], project_path: str) -> str:
        """
        Format detection results as JSON.
        
        Args:
            results: List of detection results
            project_path: Path to the scanned project
            
        Returns:
            JSON string
        """
        # Group by category
        grouped = self._group_by_category(results)
        
        output = {
            "project_path": project_path,
            "scan_timestamp": datetime.utcnow().isoformat() + "Z",
            "summary": {
                "total_technologies": len(results),
                "by_category": {
                    category: len(items)
                    for category, items in grouped.items()
                }
            },
            "technologies": {
                category: [result.to_dict() for result in items]
                for category, items in grouped.items()
            }
        }
        
        return json.dumps(output, indent=2)
    
    def _group_by_category(self, results: List[DetectionResult]) -> Dict[str, List[DetectionResult]]:
        """Group results by category."""
        grouped = {}
        for result in results:
            if result.category not in grouped:
                grouped[result.category] = []
            grouped[result.category].append(result)
        return grouped
