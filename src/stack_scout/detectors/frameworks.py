"""Framework detection module."""

import re
from pathlib import Path
from typing import List, Set
from .base import BaseDetector
from .patterns import FRAMEWORK_PATTERNS
from ..models import Detection, Evidence
from ..utils import (
    find_files_by_name,
    find_files_by_pattern,
    parse_json_file,
    read_file_safe,
    get_relative_path,
)


class FrameworkDetector(BaseDetector):
    """Detects frameworks used in the project."""
    
    def detect(self, project_path: Path) -> List[Detection]:
        """Detect frameworks based on dependency files and patterns."""
        detections = []
        
        for framework, patterns in FRAMEWORK_PATTERNS.items():
            evidence = []
            
            # Check package.json for JavaScript/TypeScript frameworks
            if 'package_json' in patterns:
                package_files = find_files_by_name(project_path, ['package.json'])
                for package_file in package_files:
                    data = parse_json_file(package_file)
                    if data:
                        deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}
                        for dep in patterns['package_json']:
                            if dep in deps:
                                rel_path = get_relative_path(package_file, project_path)
                                evidence.append(Evidence(
                                    file_path=rel_path,
                                    reason=f'Found {dep} in dependencies'
                                ))
                                break
            
            # Check requirements.txt for Python frameworks
            if 'python_deps' in patterns:
                req_files = find_files_by_name(project_path, ['requirements.txt'])
                for req_file in req_files:
                    content = read_file_safe(req_file)
                    if content:
                        for dep in patterns['python_deps']:
                            # Match a requirement name at the start of a line.
                            # Support both versioned ("fastapi==1.0") and unversioned ("fastapi")
                            # requirements, plus common suffixes like extras ("fastapi[all]"),
                            # direct references ("fastapi @ ..."), env markers ("fastapi ; ..."),
                            # whitespace, end-of-line, or comments.
                            dep_escaped = re.escape(dep)
                            if re.search(
                                rf'^\s*{dep_escaped}(?=($|\s|#|[=<>~!\[;@]))',
                                content,
                                re.MULTILINE | re.IGNORECASE,
                            ):
                                rel_path = get_relative_path(req_file, project_path)
                                evidence.append(Evidence(
                                    file_path=rel_path,
                                    reason=f'Found {dep} in requirements'
                                ))
                                break
                
                # Also check pyproject.toml
                pyproject_files = find_files_by_name(project_path, ['pyproject.toml'])
                for pyproject_file in pyproject_files:
                    content = read_file_safe(pyproject_file)
                    if content:
                        for dep in patterns['python_deps']:
                            if dep.lower() in content.lower():
                                rel_path = get_relative_path(pyproject_file, project_path)
                                evidence.append(Evidence(
                                    file_path=rel_path,
                                    reason=f'Found {dep} in pyproject.toml'
                                ))
                                break
            
            # Check for framework-specific files
            if 'files' in patterns:
                for file_pattern in patterns['files']:
                    if '*' in file_pattern:
                        found_files = find_files_by_pattern(project_path, file_pattern)
                        if found_files:
                            # Take up to 3 sample files
                            for found_file in found_files[:3]:
                                rel_path = get_relative_path(found_file, project_path)
                                evidence.append(Evidence(
                                    file_path=rel_path,
                                    reason=f'{framework} file'
                                ))
                    else:
                        found_files = find_files_by_name(project_path, [file_pattern])
                        for found_file in found_files[:3]:
                            rel_path = get_relative_path(found_file, project_path)
                            evidence.append(Evidence(
                                file_path=rel_path,
                                reason=f'{framework} configuration file'
                            ))
            
            # Check pom.xml for Maven (Java/Spring)
            if 'maven' in patterns:
                pom_files = find_files_by_name(project_path, ['pom.xml'])
                for pom_file in pom_files:
                    content = read_file_safe(pom_file)
                    if content:
                        for dep in patterns['maven']:
                            if dep in content:
                                rel_path = get_relative_path(pom_file, project_path)
                                evidence.append(Evidence(
                                    file_path=rel_path,
                                    reason=f'Found {dep} in pom.xml'
                                ))
                                break
            
            # Check build.gradle for Gradle (Java/Spring)
            if 'gradle' in patterns:
                gradle_files = find_files_by_pattern(project_path, 'build.gradle*')
                for gradle_file in gradle_files:
                    content = read_file_safe(gradle_file)
                    if content:
                        for dep in patterns['gradle']:
                            if dep in content:
                                rel_path = get_relative_path(gradle_file, project_path)
                                evidence.append(Evidence(
                                    file_path=rel_path,
                                    reason=f'Found {dep} in Gradle build file'
                                ))
                                break
            
            # Check Gemfile for Ruby frameworks
            if 'gemfile' in patterns:
                gemfiles = find_files_by_name(project_path, ['Gemfile'])
                for gemfile in gemfiles:
                    content = read_file_safe(gemfile)
                    if content:
                        for dep in patterns['gemfile']:
                            if f"'{dep}'" in content or f'"{dep}"' in content:
                                rel_path = get_relative_path(gemfile, project_path)
                                evidence.append(Evidence(
                                    file_path=rel_path,
                                    reason=f'Found {dep} in Gemfile'
                                ))
                                break
            
            # Check composer.json for PHP frameworks
            if 'composer' in patterns:
                composer_files = find_files_by_name(project_path, ['composer.json'])
                for composer_file in composer_files:
                    data = parse_json_file(composer_file)
                    if data:
                        deps = {**data.get('require', {}), **data.get('require-dev', {})}
                        for dep in patterns['composer']:
                            if dep in deps:
                                rel_path = get_relative_path(composer_file, project_path)
                                evidence.append(Evidence(
                                    file_path=rel_path,
                                    reason=f'Found {dep} in composer.json'
                                ))
                                break
            
            # If we found evidence, create a detection
            if evidence:
                confidence = self.calculate_confidence(evidence)
                detections.append(Detection(
                    name=framework,
                    category='framework',
                    confidence=confidence,
                    evidence=evidence,
                    metadata={}
                ))
        
        return detections
