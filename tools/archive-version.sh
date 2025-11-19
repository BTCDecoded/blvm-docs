#!/bin/bash
# Archive current documentation version
# Usage: ./tools/archive-version.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
VERSION_FILE="$DOCS_DIR/VERSION"
ARCHIVE_DIR="$DOCS_DIR/archive/versions"

if [ ! -f "$VERSION_FILE" ]; then
    echo "❌ VERSION file not found"
    exit 1
fi

VERSION=$(cat "$VERSION_FILE" | tr -d '\n')
MAJOR_VERSION=$(echo "$VERSION" | cut -d. -f1-2)
ARCHIVE_PATH="$ARCHIVE_DIR/v$MAJOR_VERSION"

if [ -d "$ARCHIVE_PATH" ]; then
    echo "⚠️  Archive for v$MAJOR_VERSION already exists"
    exit 1
fi

echo "📦 Archiving version $VERSION (v$MAJOR_VERSION)..."

# Create archive directory
mkdir -p "$ARCHIVE_PATH"

# Files/directories to exclude
EXCLUDE=(
    ".git"
    ".github"
    "archive"
    "tools"
    "VERSION"
    ".nojekyll"
    "node_modules"
    ".DS_Store"
)

# Copy markdown files and documentation directories
COPIED=0
for item in "$DOCS_DIR"/*; do
    if [ ! -e "$item" ]; then
        continue
    fi
    
    ITEM_NAME=$(basename "$item")
    
    # Skip excluded items
    SKIP=0
    for excl in "${EXCLUDE[@]}"; do
        if [ "$ITEM_NAME" = "$excl" ]; then
            SKIP=1
            break
        fi
    done
    
    if [ $SKIP -eq 1 ]; then
        continue
    fi
    
    # Copy markdown files
    if [ -f "$item" ] && [[ "$item" == *.md ]]; then
        cp "$item" "$ARCHIVE_PATH/"
        COPIED=$((COPIED + 1))
    fi
    
    # Copy documentation directories (if any)
    if [ -d "$item" ] && [[ "$ITEM_NAME" =~ ^[A-Z] ]] || [ "$ITEM_NAME" = "docs" ]; then
        cp -r "$item" "$ARCHIVE_PATH/"
        COPIED=$((COPIED + 1))
    fi
done

echo "✅ Archived v$MAJOR_VERSION to $ARCHIVE_PATH ($COPIED items)"
echo ""
echo "To view archived version:"
echo "  cd archive/versions/v$MAJOR_VERSION"

