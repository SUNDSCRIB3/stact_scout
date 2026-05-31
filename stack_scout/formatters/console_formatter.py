"""Console formatter for colorized CLI output."""

from typing import List, Dict
from ..detectors.base import DetectionResult


class ConsoleFormatter:
    """Formats detection results for console output."""
    
    # ANSI color codes
    COLORS = {
        "header": "\033[95m",
        "blue": "\033[94m",
        "cyan": "\033[96m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "red": "\033[91m",
        "bold": "\033[1m",
        "underline": "\033[4m",
        "end": "\033[0m",
    }
    
    CATEGORY_ICONS = {
        "language": "📝",
        "framework": "🔧",
        "package_manager": "📦",
        "build_tool": "🔨",
        "devops": "🚀",
        "database": "🗄️",
        "cloud": "☁️",
        "license": "📜",
    }
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize formatter.
        
        Args:
            use_colors: Whether to use ANSI colors
        """
        self.use_colors = use_colors
    
    def format(self, results: List[DetectionResult], project_path: str) -> str:
        """
        Format detection results for console output.
        
        Args:
            results: List of detection results
            project_path: Path to the scanned project
            
        Returns:
            Formatted string for console output
        """
        if not results:
            return self._format_no_results(project_path)
        
        # Group by category
        grouped = self._group_by_category(results)
        
        output = []
        output.append(self._colorize("=" * 80, "bold"))
        output.append(self._colorize(f"Stack-Scout Analysis Report", "bold"))
        output.append(self._colorize(f"Project: {project_path}", "cyan"))
        output.append(self._colorize("=" * 80, "bold"))
        output.append("")
        
        # Summary
        output.append(self._colorize("📊 Summary:", "bold"))
        for category, items in grouped.items():
            icon = self.CATEGORY_ICONS.get(category, "•")
            output.append(f"  {icon} {category.replace('_', ' ').title()}: {len(items)} detected")
        output.append("")
        
        # Details by category
        for category in ["language", "framework", "package_manager", "build_tool", "devops", "database", "cloud", "license"]:
            if category in grouped:
                output.append(self._format_category(category, grouped[category]))
                output.append("")
        
        output.append(self._colorize("=" * 80, "bold"))
        output.append(f"Total technologies detected: {self._colorize(str(len(results)), 'green')}")
        output.append(self._colorize("=" * 80, "bold"))
        
        return "\n".join(output)
    
    def _format_category(self, category: str, results: List[DetectionResult]) -> str:
        """Format a category section."""
        icon = self.CATEGORY_ICONS.get(category, "•")
        lines = []
        
        title = f"{icon} {category.replace('_', ' ').title()}"
        lines.append(self._colorize(title, "bold"))
        lines.append(self._colorize("-" * len(title), "blue"))
        
        for result in results:
            # Name and version
            name_line = f"  • {result.name}"
            if result.version:
                name_line += f" ({self._colorize(result.version, 'yellow')})"
            lines.append(name_line)
            
            # Source files
            if result.source_files:
                files_str = ", ".join(result.source_files[:3])
                if len(result.source_files) > 3:
                    files_str += f" (and {len(result.source_files) - 3} more)"
                lines.append(f"    {self._colorize('Source:', 'cyan')} {files_str}")
            
            # Metadata
            if result.metadata:
                for key, value in result.metadata.items():
                    if key != "file_count":
                        lines.append(f"    {self._colorize(key.title() + ':', 'cyan')} {value}")
        
        return "\n".join(lines)
    
    def _format_no_results(self, project_path: str) -> str:
        """Format message when no results found."""
        output = []
        output.append(self._colorize("=" * 80, "bold"))
        output.append(self._colorize(f"Stack-Scout Analysis Report", "bold"))
        output.append(self._colorize(f"Project: {project_path}", "cyan"))
        output.append(self._colorize("=" * 80, "bold"))
        output.append("")
        output.append(self._colorize("⚠️  No technologies detected", "yellow"))
        output.append("")
        output.append("This could mean:")
        output.append("  • The project doesn't contain recognizable config files")
        output.append("  • The directory is empty or contains only source code")
        output.append("")
        output.append(self._colorize("=" * 80, "bold"))
        return "\n".join(output)
    
    def _group_by_category(self, results: List[DetectionResult]) -> Dict[str, List[DetectionResult]]:
        """Group results by category."""
        grouped = {}
        for result in results:
            if result.category not in grouped:
                grouped[result.category] = []
            grouped[result.category].append(result)
        return grouped
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled."""
        if not self.use_colors or color not in self.COLORS:
            return text
        return f"{self.COLORS[color]}{text}{self.COLORS['end']}"
