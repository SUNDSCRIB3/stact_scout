"""CLI for Stack Scout using Click and Rich."""

import json
import sys
from pathlib import Path
import click
from rich.console import Console
from rich.tree import Tree
from rich.panel import Panel
from rich.text import Text

from .scanner import Scanner


console = Console()


def format_confidence(confidence: str) -> str:
    """Format confidence with color."""
    colors = {
        'high': 'green',
        'medium': 'yellow',
        'low': 'red'
    }
    color = colors.get(confidence, 'white')
    return f"[{color}]{confidence.upper()}[/{color}]"


def display_report(report, verbose: bool = False):
    """Display report using Rich formatting."""
    console.print()
    console.print("🔍 [bold cyan]Stack Scout Report[/bold cyan]")
    console.print("━" * 50)
    console.print()
    console.print(f"📦 [bold]Project:[/bold] {report.project_path}")
    console.print(f"🕐 [bold]Scanned:[/bold] {report.scan_timestamp}")
    console.print()
    
    # Group by category
    categories = {
        'language': ('Languages', '💻'),
        'framework': ('Frameworks', '🚀'),
        'build_tool': ('Build Tools', '🔧'),
        'devops': ('DevOps', '⚙️'),
    }
    
    for category_key, (category_name, emoji) in categories.items():
        detections = [d for d in report.detections if d.category == category_key]
        
        if not detections:
            continue
        
        console.print(f"\n{emoji} [bold]{category_name}[/bold] ({len(detections)})")
        
        tree = Tree("", guide_style="dim")
        
        for detection in detections:
            confidence_text = format_confidence(detection.confidence)
            node_text = f"{detection.name} {confidence_text}"
            branch = tree.add(node_text)
            
            if verbose:
                # Show all evidence
                for evidence in detection.evidence:
                    if evidence.line_number:
                        branch.add(f"[dim]{evidence.file_path}:{evidence.line_number}[/dim] - {evidence.reason}")
                    else:
                        branch.add(f"[dim]{evidence.file_path}[/dim] - {evidence.reason}")
            else:
                # Show summary
                if detection.metadata.get('file_count'):
                    branch.add(f"{detection.metadata['file_count']} files")
                elif detection.evidence:
                    # Show first evidence reason
                    branch.add(detection.evidence[0].reason)
        
        console.print(tree)
    
    console.print()


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """Stack Scout - Detect technologies, frameworks, and tools in your codebase."""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--format', 'output_format', type=click.Choice(['text', 'json']), 
              default='text', help='Output format')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed evidence')
def scan(path: str, output_format: str, output: str, verbose: bool):
    """Scan a project directory for technologies and tools."""
    try:
        scanner = Scanner()
        
        with console.status("[bold green]Scanning project..."):
            report = scanner.scan(path)
        
        if output_format == 'json':
            json_output = json.dumps(report.to_dict(), indent=2)
            
            if output:
                Path(output).write_text(json_output)
                console.print(f"✅ Report saved to {output}")
            else:
                print(json_output)
        else:
            # Text format
            if output:
                # Redirect console output to file
                old_console = globals()['console']
                try:
                    with open(output, 'w', encoding='utf-8') as f:
                        file_console = Console(file=f)
                        globals()['console'] = file_console
                        display_report(report, verbose)
                finally:
                    # Always restore the global console, even if rendering fails.
                    globals()['console'] = old_console

                console.print(f"✅ Report saved to {output}")
            else:
                display_report(report, verbose)
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        sys.exit(1)


def main():
    """Main entry point."""
    cli()


if __name__ == '__main__':
    main()
