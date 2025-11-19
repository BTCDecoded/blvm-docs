#!/usr/bin/env python3
"""
Extract and display version information.
Updates documentation with current version.
Run from bllvm-docs directory: python3 tools/extract-version.py
"""
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
VERSION_FILE = DOCS_DIR / "VERSION"

def get_version():
    """Read version from VERSION file."""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "unknown"

def main():
    version = get_version()
    print(f"Current version: {version}")
    return version

if __name__ == '__main__':
    main()

