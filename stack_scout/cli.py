#!/usr/bin/env python3
"""Stack-Scout CLI - Technology stack detection tool."""

import argparse
import sys
import os
from pathlib import Path

from .scanner import StackScanner
from .formatters import ConsoleFormatter, JSONFormatter


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Stack-Scout - Detect technology stacks in projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan current directory
  stack-scout .
  
  # Scan specific directory
  stack-scout /path/to/project
  
  # Generate JSON report
  stack-scout . --json output.json
  
  # Scan without colors
  stack-scout . --no-color
        """
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the project directory (default: current directory)"
    )
    
    parser.add_argument(
        "--json",
        metavar="FILE",
        help="Output results to JSON file"
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Stack-Scout 0.1.0"
    )
    
    args = parser.parse_args()
    
    # Validate path
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist", file=sys.stderr)
        return 1
    
    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a directory", file=sys.stderr)
        return 1
    
    try:
        # Run scan
        scanner = StackScanner()
        results = scanner.scan_directory(args.path)
        
        # Format and output results
        console_formatter = ConsoleFormatter(use_colors=not args.no_color)
        console_output = console_formatter.format(results, os.path.abspath(args.path))
        print(console_output)
        
        # Save JSON if requested
        if args.json:
            json_formatter = JSONFormatter()
            json_output = json_formatter.format(results, os.path.abspath(args.path))
            
            with open(args.json, 'w') as f:
                f.write(json_output)
            
            print(f"\n✅ JSON report saved to: {args.json}")
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user", file=sys.stderr)
        return 130
    
    except Exception as e:
        print(f"Error during scan: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
