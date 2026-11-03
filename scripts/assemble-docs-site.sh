#!/usr/bin/env bash
# Lay the GitHub Pages artifact out as the docs host:
#   /                hub
#   /intelligence/   Intelligence guide
#   /blvm/           mdBook (already built in ./book)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ ! -f book/index.html ]; then
  echo "::error::book/index.html missing — run mdbook build first" >&2
  exit 1
fi

PUBLISH="${ROOT}/publish"
mkdir -p "$PUBLISH/blvm" "$PUBLISH/intelligence"

# Hub files. A CNAME inside the book tree would claim the wrong host root.
cp -a hub/. "$PUBLISH/"
cp -a book/. "$PUBLISH/blvm/"
rm -f "$PUBLISH/blvm/CNAME"

printf '%s\n' 'docs.btcdecoded.org' > "$PUBLISH/CNAME"
touch "$PUBLISH/.nojekyll"

echo "OK: ${PUBLISH} hub + /blvm + /intelligence"
