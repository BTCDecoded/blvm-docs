#!/usr/bin/env bash
# Build mdBook output and post-process Mermaid diagrams (matches CI deploy).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# additional-css resolves under src/; root custom.css is canonical (CI copies it to book/)
cp custom.css src/custom.css
mdbook build
cp custom.css book/custom.css
cp llms.txt book/llms.txt
cp llm.txt book/llm.txt
python3 "$ROOT/scripts/postprocess-mermaid.py" "$ROOT/book"
