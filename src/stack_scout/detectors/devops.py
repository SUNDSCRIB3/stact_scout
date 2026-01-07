"""DevOps tools detection module."""

from pathlib import Path
from typing import List
from .base import BaseDetector
from .patterns import DEVOPS_PATTERNS
from ..models import Detection, Evidence
from ..utils import (
    find_files_by_name,
    find_files_by_pattern,
    find_directories,
    read_file_safe,
    get_relative_path,
)


class DevOpsDetector(BaseDetector):
    """Detects DevOps tools and configurations."""
    
    def detect(self, project_path: Path) -> List[Detection]:
        """Detect DevOps tools based on configuration files and directories."""
        detections = []
        
        for tool, patterns in DEVOPS_PATTERNS.items():
            evidence = []
            
            for pattern in patterns:
                # Check if it's a directory pattern
                if pattern.endswith('/'):
                    dir_path = pattern.rstrip('/')
                    # Handle nested paths like .github/workflows/
                    if '/' in dir_path:
                        # Look for the nested directory
                        full_path = project_path / dir_path
                        if full_path.exists() and full_path.is_dir():
                            rel_path = get_relative_path(full_path, project_path)
                            evidence.append(Evidence(
                                file_path=rel_path + '/',
                                reason=f'{tool} directory'
                            ))
                    else:
                        # Single directory name
                        found_dirs = find_directories(project_path, [dir_path])
                        for found_dir in found_dirs[:3]:
                            rel_path = get_relative_path(found_dir, project_path)
                            evidence.append(Evidence(
                                file_path=rel_path + '/',
                                reason=f'{tool} directory'
                            ))
                # Check if pattern contains wildcards
                elif '*' in pattern:
                    found_files = find_files_by_pattern(project_path, pattern)
                    for found_file in found_files[:3]:
                        rel_path = get_relative_path(found_file, project_path)
                        evidence.append(Evidence(
                            file_path=rel_path,
                            reason=f'{tool} configuration file'
                        ))
                else:
                    found_files = find_files_by_name(project_path, [pattern])
                    for found_file in found_files[:3]:
                        rel_path = get_relative_path(found_file, project_path)
                        evidence.append(Evidence(
                            file_path=rel_path,
                            reason=f'{tool} configuration file'
                        ))
            
            # Special case for Kubernetes: also check YAML files for k8s resources
            if tool == 'Kubernetes' and not evidence:
                yaml_files = find_files_by_pattern(project_path, '*.yaml')
                yaml_files.extend(find_files_by_pattern(project_path, '*.yml'))
                
                for yaml_file in yaml_files[:10]:  # Check up to 10 YAML files
                    content = read_file_safe(yaml_file)
                    if content:
                        # Look for k8s API resources
                        k8s_keywords = ['kind: Deployment', 'kind: Service', 'kind: Pod', 
                                       'kind: ConfigMap', 'kind: Ingress', 'apiVersion: apps/v1']
                        for keyword in k8s_keywords:
                            if keyword in content:
                                rel_path = get_relative_path(yaml_file, project_path)
                                evidence.append(Evidence(
                                    file_path=rel_path,
                                    reason='Kubernetes manifest file'
                                ))
                                break
                    
                    # Stop if we found enough evidence
                    if len(evidence) >= 3:
                        break
            
            # Create detection if evidence was found
            if evidence:
                confidence = self.calculate_confidence(evidence)
                detections.append(Detection(
                    name=tool,
                    category='devops',
                    confidence=confidence,
                    evidence=evidence,
                    metadata={}
                ))
        
        return detections
