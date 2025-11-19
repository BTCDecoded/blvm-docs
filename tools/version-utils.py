#!/usr/bin/env python3
"""
Version management utilities for bllvm-docs.
"""
from pathlib import Path
import shutil
import re

SCRIPT_DIR = Path(__file__).parent
DOCS_DIR = SCRIPT_DIR.parent
VERSION_FILE = DOCS_DIR / "VERSION"
ARCHIVE_DIR = DOCS_DIR / "archive" / "versions"

def get_version():
    """Get current version from VERSION file."""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return None

def get_major_version(version):
    """Extract major version (e.g., '1.0.0' -> '1.0')."""
    match = re.match(r'^(\d+\.\d+)', version)
    return match.group(1) if match else None

def archive_current_version():
    """Archive current version to archive/versions/vX.Y/."""
    version = get_version()
    if not version:
        print("❌ No version found in VERSION file")
        return False
    
    major = get_major_version(version)
    if not major:
        print(f"❌ Invalid version format: {version}")
        return False
    
    archive_path = ARCHIVE_DIR / f"v{major}"
    
    if archive_path.exists():
        print(f"⚠️  Archive for v{major} already exists")
        return False
    
    # Files to archive (exclude certain files)
    exclude = {
        '.git', '.github', 'archive', 'tools', 'VERSION',
        '.nojekyll', 'node_modules', '.DS_Store'
    }
    
    # Create archive directory
    archive_path.mkdir(parents=True, exist_ok=True)
    
    # Copy files
    copied = 0
    for item in DOCS_DIR.iterdir():
        if item.name in exclude:
            continue
        
        if item.is_file() and item.suffix in ['.md', '.txt', '.yml', '.yaml']:
            shutil.copy2(item, archive_path / item.name)
            copied += 1
        elif item.is_dir() and item.name not in exclude:
            # Only copy documentation directories
            if item.name in ['docs'] or item.name.startswith('_'):
                shutil.copytree(item, archive_path / item.name, dirs_exist_ok=True)
                copied += 1
    
    print(f"✅ Archived v{major} to {archive_path} ({copied} items)")
    return True

def create_version_index():
    """Create index page with version selector."""
    version = get_version()
    major = get_major_version(version) if version else None
    
    # Find all archived versions
    archived_versions = []
    if ARCHIVE_DIR.exists():
        for item in ARCHIVE_DIR.iterdir():
            if item.is_dir() and item.name.startswith('v'):
                ver = item.name[1:]  # Remove 'v' prefix
                archived_versions.append(ver)
    
    archived_versions.sort(reverse=True)
    
    return version, major, archived_versions

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'archive':
        archive_current_version()
    else:
        version = get_version()
        print(f"Current version: {version}")

