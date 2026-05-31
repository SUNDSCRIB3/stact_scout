"""License detection module."""

from typing import List, Dict
from .base import Detector, DetectionResult

import re


class LicenseDetector(Detector):
    """Detects project license from LICENSE file and package metadata."""

    LICENSE_PATTERNS = {
        "MIT": [
            r"\bMIT\b",
            r"Permission is hereby granted, free of charge",
        ],
        "Apache-2.0": [
            r"\bApache\b.{0,20}\b(2\.0|2)\b",
            r"Licensed under the Apache License",
        ],
        "GPL-3.0": [
            r"\bGNU GENERAL PUBLIC LICENSE\b",
            r"\bGPL.{0,10}version 3\b",
        ],
        "GPL-2.0": [
            r"\bGNU GENERAL PUBLIC LICENSE\b.{0,50}Version 2",
            r"\bGPL.{0,10}version 2\b",
        ],
        "BSD-3-Clause": [
            r"\bBSD\b.{0,20}3.{0,20}Clause\b",
            r"Redistribution and use in source and binary forms",
        ],
        "BSD-2-Clause": [
            r"\bBSD\b.{0,20}2.{0,20}Clause\b",
        ],
        "LGPL": [
            r"\bGNU LESSER GENERAL PUBLIC LICENSE\b",
            r"\bLGPL\b",
        ],
        "AGPL": [
            r"\bGNU AFFERO GENERAL PUBLIC LICENSE\b",
            r"\bAGPL\b",
        ],
        "MPL-2.0": [
            r"\bMozilla Public License\b",
            r"\bMPL\b.{0,10}2\.0",
        ],
        "Unlicense": [
            r"\bunlicense\b",
            r"This is free and unencumbered software",
        ],
        "ISC": [
            r"\bISC License\b",
            r"Permission to use, copy, modify, and/or distribute",
        ],
    }

    def detect(self, file_paths: List[str], file_contents: Dict[str, str]) -> List[DetectionResult]:
        results = []

        # Check LICENSE file
        license_content = ""
        for path, content in file_contents.items():
            if path.lower().startswith("license") or path.lower().startswith("copying"):
                license_content += content + "\n"
            if path == "pyproject.toml" or path == "setup.py":
                license_content += content + "\n"
            if path == "package.json":
                license_content += content + "\n"

        if not license_content:
            return results

        license_lower = license_content.lower()
        for license_name, patterns in self.LICENSE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, license_content, re.IGNORECASE | re.DOTALL):
                    results.append(DetectionResult(
                        category="license",
                        name=license_name,
                        confidence="high",
                        source_files=[p for p in file_contents if p.lower().startswith(("license", "copying"))],
                    ))
                    break  # One match per license is enough

        return results
