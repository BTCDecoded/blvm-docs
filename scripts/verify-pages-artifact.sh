#!/usr/bin/env bash
# Sanity-check the docs host artifact before upload-pages-artifact.
set -euo pipefail

SITE="${1:-publish}"

for f in index.html CNAME .nojekyll blvm/index.html intelligence/index.html hub.css; do
  if [ ! -f "${SITE}/${f}" ]; then
    echo "::error::Missing ${SITE}/${f} — artifact is not the docs host layout" >&2
    exit 1
  fi
done

if [ -f "${SITE}/blvm/CNAME" ]; then
  echo "::error::${SITE}/blvm/CNAME would publish a second custom domain" >&2
  exit 1
fi

if ! grep -qx 'docs.btcdecoded.org' "${SITE}/CNAME"; then
  echo "::error::${SITE}/CNAME must be docs.btcdecoded.org" >&2
  exit 1
fi

if ! grep -q 'mdbook' "${SITE}/blvm/index.html"; then
  echo "::warning::${SITE}/blvm/index.html does not mention mdbook (unexpected layout?)"
fi

echo "OK: ${SITE} has the hub, /blvm, /intelligence, CNAME, .nojekyll"
