#!/bin/bash
# Build documentation for GitHub Pages
# Converts markdown to HTML with styling

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$DOCS_DIR/docs"

echo "📦 Building documentation..."

# Create build directory structure
mkdir -p "$BUILD_DIR/assets/css"
mkdir -p "$BUILD_DIR/assets/js"

# Copy CSS
cp "$DOCS_DIR/docs/assets/css/style.css" "$BUILD_DIR/assets/css/" 2>/dev/null || true

# Copy VERSION file
cp "$DOCS_DIR/VERSION" "$BUILD_DIR/" 2>/dev/null || true

# Copy index.html
cp "$DOCS_DIR/docs/index.html" "$BUILD_DIR/" 2>/dev/null || true

# Copy all markdown files
for md in "$DOCS_DIR"/*.md; do
    if [ -f "$md" ]; then
        cp "$md" "$BUILD_DIR/"
    fi
done

echo "✅ Documentation built in $BUILD_DIR"

