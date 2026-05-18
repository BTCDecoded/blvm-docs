#!/usr/bin/env bash
# Fail if wired chapters contain raw N-of-M policy literals (should use [[gov:…]]).
set -euo pipefail

ROOT="${1:-.}"
cd "$ROOT"

shopt -s globstar nullglob
PATTERN='[0-9]+-of-[0-9]+'

# Chapters that must use [[gov:KEY]] for policy thresholds (see contributing-docs.md).
mapfile -t FILES < <(
  find src/development/pr-process.md \
    src/development/contributing.md \
    src/governance/layer-tier-model.md \
    src/governance/multisig-configuration.md \
    src/governance/keyholder-procedures.md \
    src/governance/governance-fork.md \
    src/governance/governance-model.md \
    src/architecture/component-relationships.md \
    src/architecture/module-system.md \
    src/appendices/faq.md \
    src/reference/glossary.md \
    src/sdk/overview.md \
    src/sdk/getting-started.md \
    src/sdk/examples.md \
    src/sdk/api-reference.md \
    src/getting-started/quick-start.md \
    src/security/security-controls.md \
    src/governance/configuration-system.md \
    -type f 2>/dev/null
)

violations=0
for f in "${FILES[@]}"; do
  [[ -f "$f" ]] || continue
  while IFS= read -r line; do
  [[ -z "$line" ]] && continue
  if [[ "$line" =~ $PATTERN ]] && [[ "$line" != *'[[gov:'* ]]; then
    # Tier 5 special process is documented in GOVERNANCE.md, not action-tiers.yml.
    if [[ "$f" == *pr-process.md ]] && [[ "$line" == *'2-of-3 emergency'* ]]; then
      continue
    fi
    echo "::error file=$f::raw policy literal (use [[gov:KEY]]): $line"
    violations=$((violations + 1))
  fi
  done < <(grep -E "$PATTERN" "$f" || true)
done

if [[ "$violations" -gt 0 ]]; then
  echo "check-governance-literals: $violations violation(s)"
  exit 1
fi

echo "check-governance-literals: OK"
