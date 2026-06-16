#!/usr/bin/env bash
# Smoke-test the public docs URL after deploy-pages (catches 404 regressions).
set -euo pipefail

URL="${DOCS_SITE_URL:-https://docs.thebitcoincommons.org}"
TRIES="${DOCS_SITE_VERIFY_TRIES:-6}"
SLEEP="${DOCS_SITE_VERIFY_SLEEP:-10}"

for i in $(seq 1 "$TRIES"); do
  if curl -sf --retry 2 --retry-delay 3 -o /dev/null "$URL"; then
    echo "OK: ${URL} returned 200"
    exit 0
  fi
  echo "Waiting for ${URL} (${i}/${TRIES})..."
  sleep "$SLEEP"
done

echo "::error::Live docs site ${URL} did not return 200 after deploy"
exit 1
