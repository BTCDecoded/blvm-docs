#!/usr/bin/env bash
# Sanity-check mdbook output before upload-pages-artifact.
set -euo pipefail

BOOK_DIR="${1:-book}"

for f in index.html CNAME .nojekyll; do
  if [ ! -f "${BOOK_DIR}/${f}" ]; then
    echo "::error::Missing ${BOOK_DIR}/${f} — artifact is not a complete mdbook deploy"
    exit 1
  fi
done

if ! grep -q 'mdbook' "${BOOK_DIR}/index.html"; then
  echo "::warning::${BOOK_DIR}/index.html does not mention mdbook (unexpected layout?)"
fi

echo "OK: ${BOOK_DIR} has index.html, CNAME, .nojekyll"
