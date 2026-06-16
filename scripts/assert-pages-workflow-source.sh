#!/usr/bin/env bash
# Fail if GitHub Pages is set to legacy branch deploy (serves repo root → 404 for mdbook).
set -euo pipefail

REPO="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY required}"
TOKEN="${GH_TOKEN:-${GITHUB_TOKEN:-}}"

if [ -z "$TOKEN" ]; then
  echo "::warning::No GH_TOKEN/GITHUB_TOKEN; skipping Pages source check"
  exit 0
fi

BUILD_TYPE="$(gh api "repos/${REPO}/pages" --jq .build_type 2>/dev/null || true)"
if [ -z "$BUILD_TYPE" ] || [ "$BUILD_TYPE" = "null" ]; then
  echo "::error::Could not read GitHub Pages config for ${REPO}"
  exit 1
fi

if [ "$BUILD_TYPE" != "workflow" ]; then
  echo "::error::GitHub Pages build_type is '${BUILD_TYPE}' (expected 'workflow')."
  echo "Legacy branch deploy publishes the repo root, which has no index.html — the site 404s even when mdbook CI passes."
  echo "Fix: Settings → Pages → Build and deployment → Source: GitHub Actions"
  echo "Or: gh api -X PUT repos/${REPO}/pages -f build_type=workflow"
  exit 1
fi

echo "OK: GitHub Pages build_type=workflow"
