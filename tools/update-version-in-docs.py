#!/usr/bin/env python3
"""
Update version number in documentation files.
Run from bllvm-docs directory: python3 tools/update-version-in-docs.py
"""
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
VERSION_FILE = DOCS_DIR / "VERSION"

def get_version():
    """Read version from VERSION file."""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return None

def update_version_in_file(file_path, version):
    """Update version in a markdown file."""
    if not file_path.exists():
        return False
    
    content = file_path.read_text()
    original = content
    
    # Pattern 1: **Version:** X.Y.Z
    content = re.sub(
        r'\*\*Version:\*\*\s*[0-9.]+',
        f'**Version:** {version}',
        content
    )
    
    # Pattern 2: **Current Version:** X.Y.Z
    content = re.sub(
        r'\*\*Current Version:\*\*\s*[0-9.]+',
        f'**Current Version:** {version}',
        content
    )
    
    # Pattern 3: This documentation corresponds to BLLVM version X.Y.Z
    content = re.sub(
        r'This documentation corresponds to BLLVM version\s+[0-9.]+',
        f'This documentation corresponds to BLLVM version {version}',
        content
    )
    
    if content != original:
        file_path.write_text(content)
        return True
    return False

def main():
    version = get_version()
    if not version:
        print("❌ No version found in VERSION file")
        return
    
    files_updated = []
    
    # Update INDEX.md
    if update_version_in_file(DOCS_DIR / "INDEX.md", version):
        files_updated.append("INDEX.md")
    
    # Update README.md
    if update_version_in_file(DOCS_DIR / "README.md", version):
        files_updated.append("README.md")
    
    if files_updated:
        print(f"✅ Updated version to {version} in: {', '.join(files_updated)}")
    else:
        print(f"ℹ️  Version {version} already up to date in documentation")

if __name__ == '__main__':
    main()

