#!/usr/bin/env bash
# Verify mdBook include sources and governance policy inputs (CI + local).
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

required=(
  modules/governance/README.md
  modules/governance/GOVERNANCE.md
  modules/governance/config/action-tiers.yml
  modules/governance/config/repository-layers.yml
  modules/governance/config/emergency-tiers.yml
  modules/governance/docs/ACTION_TIERS.md
)

for f in "${required[@]}"; do
  if [[ ! -f "$f" ]]; then
    echo "::error::missing required file: $f"
    exit 1
  fi
  echo "OK $f"
done

if grep -R -l '\[\[gov:' modules/governance/README.md modules/governance/GOVERNANCE.md 2>/dev/null; then
  echo "::error::Governance narrative includes must not contain [[gov: placeholders (use blvm-docs src/ only)"
  exit 1
fi

if [[ -x ./scripts/check-governance-literals.sh ]]; then
  ./scripts/check-governance-literals.sh
else
  echo "::warning::check-governance-literals.sh missing or not executable; skipping"
fi

echo "verify-book-inputs: OK"
