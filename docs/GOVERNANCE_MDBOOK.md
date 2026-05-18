# ADR: Governance YAML → mdBook placeholders

**Status:** Accepted (implemented in blvm-docs)  
**Date:** 2026-05-18

## Context

Policy numbers (review periods, signature thresholds) lived in three places: `governance/config/*.yml`, narrative docs in `blvm-docs`, and hardcoded `blvm-commons/src/validation/threshold.rs`. Hand-edited prose drifted from YAML.

## Decision

1. **Published book** resolves `[[gov:KEY]]` at `mdbook build` via **`mdbook-governance-vars`** (Rust mdBook preprocessor).
2. **YAML roots:** `modules/governance/config/action-tiers.yml`, `repository-layers.yml`, `emergency-tiers.yml` (cloned in CI).
3. **Emergency** tables use **`emergency-tiers.yml` only**; duplicate `emergency_tiers` removed from `action-tiers.yml`.
4. **PR action tiers** narrative: `governance/docs/ACTION_TIERS.md` — separate from emergency classes.
5. **Tier 5 special process** (5-of-7 + 2-of-3) stays in **`GOVERNANCE.md`**, not `action-tiers.yml`.
6. **Layer × tier matrix** uses max(layer, tier) in the preprocessor, matching `threshold.rs` today.
7. **Drift test:** `cargo test` in `mdbook-governance-vars` compares YAML-derived combine output to `threshold_ref` (mirror of commons).
8. **Literal guard:** `scripts/check-governance-literals.sh` (also run from `verify-book-inputs.sh`) fails CI if wired chapters contain raw `N-of-M` strings without `[[gov:…]]` (Tier 5 special-process line exempt).

**Allowlist extras:** `tier_N_sig_required` / `tier_N_sig_total`, `layer_N_sig_required` / `layer_N_sig_total` (parsed from `*-of-*` fields), `security_critical_signatures` / `security_critical_review_days`.

## Consequences

- Doc changes to policy numbers require **governance YAML** + allowlisted keys in `mdbook-governance-vars`.
- **Merge enforcement** still uses `threshold.rs` until commons loads YAML; drift test fails when YAML and code disagree.
- mdBook pinned to **0.4.43**; preprocessor installed with `cargo install --locked --path mdbook-governance-vars`.
- **Fork registry tables** in `configuration-system.md` (`tier_1_signatures_required`, etc.) remain hand-maintained DB keys—not `[[gov:]]`—until a separate schema mapping exists.

## References

- `GOVERNANCE_YAML_MDBOOK_PLAN.md` (implementation checklist)
- `mdbook-governance-vars/README.md` (allowlist)
