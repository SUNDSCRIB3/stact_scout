"""File system utilities for Stack Scout."""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import yaml


def walk_directory(project_path: Path, max_depth: int = 10) -> List[Path]:
    """
    Walk directory tree and return all file paths.
    Excludes common directories like node_modules, .git, etc.
    """
    excluded_dirs = {
        'node_modules', '__pycache__', 'venv', 'env', '.venv',
        'dist', 'build', '.pytest_cache', '.mypy_cache', '.tox',
        'target', '.terraform', 'vendor', 'coverage', '.next',
    }
    
    files = []
    
    def _walk(path: Path, depth: int):
        if depth > max_depth:
            return
        
        try:
            for item in path.iterdir():
                # Skip excluded directories
                # Exclude .git but NOT .github
                if item.is_dir():
                    if item.name in excluded_dirs or item.name == '.git':
                        continue
                
                if item.is_file():
                    files.append(item)
                elif item.is_dir():
                    _walk(item, depth + 1)
        except (PermissionError, OSError):
            pass
    
    _walk(project_path, 0)
    return files


def find_files_by_name(project_path: Path, filenames: List[str]) -> List[Path]:
    """Find files by exact name match."""
    found = []
    all_files = walk_directory(project_path)
    
    for file_path in all_files:
        if file_path.name in filenames:
            found.append(file_path)
    
    return found


def find_files_by_pattern(project_path: Path, pattern: str) -> List[Path]:
    """Find files matching a glob pattern."""
    found = []
    all_files = walk_directory(project_path)
    
    # Convert pattern to regex
    # *.tf -> .*\.tf$
    # *.config.js -> .*\.config\.js$
    regex_pattern = pattern.replace('.', r'\.').replace('*', '.*')
    regex = re.compile(regex_pattern + '$')
    
    for file_path in all_files:
        if regex.match(file_path.name):
            found.append(file_path)
    
    return found


def find_directories(project_path: Path, dir_names: List[str]) -> List[Path]:
    """Find directories by name."""
    found = []
    excluded_dirs = {
        'node_modules', '__pycache__', 'venv', 'env', '.venv',
        'dist', 'build', '.pytest_cache', '.mypy_cache', '.tox',
        'target', '.terraform', 'vendor', 'coverage', '.next',
    }
    
    def _walk(path: Path):
        try:
            for item in path.iterdir():
                if item.is_dir():
                    if item.name in dir_names:
                        found.append(item)
                    # Exclude .git but NOT .github
                    if item.name not in excluded_dirs and item.name != '.git':
                        _walk(item)
        except (PermissionError, OSError):
            pass
    
    _walk(project_path)
    return found


def read_file_safe(file_path: Path, max_size: int = 1024 * 1024) -> Optional[str]:
    """
    Safely read file contents.
    Returns None if file is too large or can't be read.
    """
    try:
        if file_path.stat().st_size > max_size:
            return None
        return file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return None


def parse_json_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Parse JSON file and return dict."""
    try:
        content = read_file_safe(file_path)
        if content:
            return json.loads(content)
    except Exception:
        pass
    return None


def parse_yaml_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Parse YAML file and return dict."""
    try:
        content = read_file_safe(file_path)
        if content:
            return yaml.safe_load(content)
    except Exception:
        pass
    return None


def search_in_file(file_path: Path, patterns: List[str]) -> List[str]:
    """
    Search for patterns in a file.
    Returns list of matching patterns found.
    """
    content = read_file_safe(file_path)
    if not content:
        return []
    
    found = []
    content_lower = content.lower()
    
    for pattern in patterns:
        if pattern.lower() in content_lower:
            found.append(pattern)
    
    return found


def count_files_by_extension(project_path: Path, extensions: List[str]) -> int:
    """Count files with given extensions."""
    count = 0
    all_files = walk_directory(project_path)
    
    for file_path in all_files:
        if file_path.suffix in extensions:
            count += 1
    
    return count


def get_relative_path(file_path: Path, project_path: Path) -> str:
    """Get relative path from project root."""
    try:
        return str(file_path.relative_to(project_path))
    except ValueError:
        return str(file_path)
