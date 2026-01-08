"""Language detection module."""

from pathlib import Path
from typing import List, Dict
from .base import BaseDetector
from .patterns import LANGUAGE_PATTERNS
from ..models import Detection, Evidence
from ..utils import walk_directory, get_relative_path


class LanguageDetector(BaseDetector):
    """Detects programming languages used in the project."""
    
    def detect(self, project_path: Path) -> List[Detection]:
        """Detect languages based on file extensions."""
        detections = []
        
        # Count files by language
        language_counts: Dict[str, int] = {}
        language_files: Dict[str, List[Path]] = {}
        
        all_files = walk_directory(project_path)
        
        for file_path in all_files:
            for language, extensions in LANGUAGE_PATTERNS.items():
                if file_path.suffix in extensions:
                    language_counts[language] = language_counts.get(language, 0) + 1
                    if language not in language_files:
                        language_files[language] = []
                    language_files[language].append(file_path)
                    break
        
        # Create detections for languages with files
        for language, count in language_counts.items():
            if count == 0:
                continue
            
            evidence = []
            
            # Add evidence with file count
            extensions = ', '.join(LANGUAGE_PATTERNS[language])
            evidence.append(Evidence(
                file_path='.',
                reason=f'{count} {extensions} files found'
            ))
            
            # Add sample files as evidence (up to 3)
            for file_path in language_files[language][:3]:
                rel_path = get_relative_path(file_path, project_path)
                evidence.append(Evidence(
                    file_path=rel_path,
                    reason=f'{language} source file'
                ))
            
            confidence = self.calculate_confidence(evidence)
            
            detections.append(Detection(
                name=language,
                category='language',
                confidence=confidence,
                evidence=evidence,
                metadata={'file_count': count}
            ))
        
        return detections
