# mdbook-governance-vars

mdBook preprocessor for **blvm-docs**. At build time it loads governance policy YAML from
`modules/governance/config/` and replaces allowlisted placeholders in chapter markdown:

```text
[[gov:tier_1_review_days]]
```

Unknown keys or any leftover `[[gov:…]]` after expansion fails the build.

## Sources (build-time)

| File | Used for |
|------|----------|
| `action-tiers.yml` | PR tiers 1-5 review days and maintainer signatures |
| `emergency-tiers.yml` | Emergency class thresholds (not the duplicate block in `action-tiers.yml`) |
| `repository-layers.yml` | Layer signatures/review days, consensus review (layers 1-2), combination matrix |

## Allowlist keys

### PR process (`pr-process.md`)

| Key | Source |
|-----|--------|
| `tier_N_review_days`, `tier_N_signatures` | `action-tiers.yml` → `tiers.tier_N_*` (N = 1..5) |
| `tier_N_sig_required`, `tier_N_sig_total` | Parsed from `tier_N_signatures` (e.g. `3-of-5` → 3, 5) |
| `lifecycle_tierN_days` | Same as `tier_N_review_days` (editor-friendly alias) |
| `security_critical_signatures`, `security_critical_review_days` | `action-tiers.yml` → `security_critical.*` |
| `emergency_{critical,urgent,elevated}_*` | `emergency-tiers.yml` → `tiers.tier_1_critical` / `tier_2_urgent` / `tier_3_elevated` |

Emergency suffixes: `_review_days`, `_signature`, `_activation`, `_max_days`.

**Not templated:** Tier 5 special process (see governance `GOVERNANCE.md` / `docs/ACTION_TIERS.md`).

### Layer-tier model (`layer-tier-model.md`, `multisig-configuration.md`)

| Key pattern | Meaning |
|-------------|---------|
| `layer_N_signatures`, `layer_N_review_days` | `repository-layers.yml` |
| `layer_N_sig_required`, `layer_N_sig_total` | Parsed from `layer_N_signatures` |
| `layer_1_consensus_review_days`, `layer_2_consensus_review_days` | 365-day consensus path (layers 1-2) |
| `combination_matrix_table` | Full 5×5 markdown table (max-rule, matches `threshold.rs`) |
| `matrix_L_T_signatures`, `matrix_L_T_review_days`, `matrix_L_T_source` | Single matrix cell (L,T = 1..5) |

## Install

```bash
cargo install --locked --path mdbook-governance-vars
```

## Disable (optional rollout)

```bash
MDBOOK_GOVERNANCE_VARS=0 mdbook build
```

## Tests

```bash
cargo test --locked --manifest-path mdbook-governance-vars/Cargo.toml
```

Includes **drift checks**: YAML-derived layer×tier combine must match `blvm-commons` `threshold.rs` (see `src/threshold_ref.rs`). When you change governance YAML, update commons or expect test failure.

CI also runs `scripts/check-governance-literals.sh` so wired chapters do not contain raw `N-of-M` policy strings (use `[[gov:…]]` instead).

## Drift vs merge enforcement

| Source | Role |
|--------|------|
| `governance/config/*.yml` | Book build (`[[gov:…]]`) |
| `threshold_ref.rs` | Test mirror of `blvm-commons` `validation/threshold.rs` |
| `drift_check.rs` | Fails tests if YAML max-rule ≠ hardcoded merge logic |

