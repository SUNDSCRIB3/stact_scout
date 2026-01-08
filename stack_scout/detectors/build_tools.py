"""Build tools detection module."""

from pathlib import Path
from typing import List
from .base import BaseDetector
from .patterns import BUILD_TOOL_PATTERNS
from ..models import Detection, Evidence
from ..utils import (
    find_files_by_name,
    find_files_by_pattern,
    read_file_safe,
    get_relative_path,
)


class BuildToolsDetector(BaseDetector):
    """Detects build tools and package managers."""
    
    def detect(self, project_path: Path) -> List[Detection]:
        """Detect build tools based on configuration files."""
        detections = []
        
        for tool, file_patterns in BUILD_TOOL_PATTERNS.items():
            evidence = []
            
            for pattern in file_patterns:
                # Check if pattern contains wildcards
                if '*' in pattern:
                    found_files = find_files_by_pattern(project_path, pattern)
                else:
                    found_files = find_files_by_name(project_path, [pattern])
                
                # Add evidence for found files
                for found_file in found_files[:3]:  # Limit to 3 files
                    rel_path = get_relative_path(found_file, project_path)
                    evidence.append(Evidence(
                        file_path=rel_path,
                        reason=f'{tool} configuration file'
                    ))
            
            # Special case for Poetry: check if [tool.poetry] section exists
            if tool == 'Poetry' and evidence:
                # Verify it's actually poetry by checking content
                verified = False
                for ev in evidence:
                    file_path = project_path / ev.file_path
                    if file_path.exists():
                        content = read_file_safe(file_path)
                        if content and '[tool.poetry]' in content:
                            verified = True
                            break
                
                if not verified:
                    evidence = []  # Clear evidence if not poetry
            
            # Create detection if evidence was found
            if evidence:
                confidence = self.calculate_confidence(evidence)
                detections.append(Detection(
                    name=tool,
                    category='build_tool',
                    confidence=confidence,
                    evidence=evidence,
                    metadata={}
                ))
        
        return detections
