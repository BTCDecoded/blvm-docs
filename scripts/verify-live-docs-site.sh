#!/usr/bin/env bash
# Smoke-test the public docs URL after deploy-pages (catches 404 regressions).
set -euo pipefail

ORIGIN="${DOCS_SITE_URL:-https://docs.btcdecoded.org}"
TRIES="${DOCS_SITE_VERIFY_TRIES:-6}"
SLEEP="${DOCS_SITE_VERIFY_SLEEP:-10}"

check() {
  local url="$1"
  local i
  for i in $(seq 1 "$TRIES"); do
    if curl -sf --retry 2 --retry-delay 3 -o /dev/null "$url"; then
      echo "OK: ${url} returned 200"
      return 0
    fi
    echo "Waiting for ${url} (${i}/${TRIES})..."
    sleep "$SLEEP"
  done
  echo "::error::Live docs site ${url} did not return 200 after deploy" >&2
  return 1
}

check "${ORIGIN}/"
check "${ORIGIN}/blvm/"
check "${ORIGIN}/intelligence/"
