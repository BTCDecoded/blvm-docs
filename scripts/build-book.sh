#!/usr/bin/env bash
# Build mdBook output and post-process Mermaid diagrams (matches CI deploy).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mdbook build
python3 "$ROOT/scripts/postprocess-mermaid.py" "$ROOT/book"
