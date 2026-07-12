# Governance layers and tiers

## Overview

Bitcoin Commons implements dual-dimensional governance combining **Layers** (repository architecture) and **Tiers** (action classification). When both apply, the system uses the **most restrictive wins** rule, taking the highest signature requirement and longest review period.

PR **action tiers** (1-5) are defined in governance [action-tiers.yml](https://github.com/BTCDecoded/governance/blob/main/config/action-tiers.yml) with narrative in [action tiers](https://github.com/BTCDecoded/governance/blob/main/docs/ACTION_TIERS.md). **Emergency classes** use [emergency-tiers.yml](https://github.com/BTCDecoded/governance/blob/main/config/emergency-tiers.yml) only.

## Layer System

The layer system maps repository architecture to governance requirements:

| Layer | Repository | Purpose | Signatures | Review Period |
|-------|------------|---------|------------|---------------|
| 1 | blvm-spec | Constitutional | [[gov:layer_1_signatures]] | [[gov:layer_1_review_days]] days |
| 2 | blvm-consensus | Constitutional | [[gov:layer_2_signatures]] | [[gov:layer_2_review_days]] days |
| 3 | blvm-protocol | Implementation | [[gov:layer_3_signatures]] | [[gov:layer_3_review_days]] days |
| 4 | blvm-node / blvm | Application | [[gov:layer_4_signatures]] | [[gov:layer_4_review_days]] days |
| 5 | blvm-sdk | Extension | [[gov:layer_5_signatures]] | [[gov:layer_5_review_days]] days |

**Note:** For consensus rule changes, Layer 1-2 require [[gov:layer_1_consensus_review_days]] days review period.

## Tier System

The tier system classifies changes by action type:

| Tier | Type | Signatures | Review Period |
|------|------|------------|---------------|
| 1 | Routine Maintenance | [[gov:tier_1_signatures]] | [[gov:tier_1_review_days]] days |
| 2 | Feature Changes | [[gov:tier_2_signatures]] | [[gov:tier_2_review_days]] days |
| 3 | Consensus-Adjacent | [[gov:tier_3_signatures]] | [[gov:tier_3_review_days]] days |
| 4 | Emergency Actions | [[gov:tier_4_signatures]] | [[gov:tier_4_review_days]] days |
| 5 | Governance Changes | [[gov:tier_5_signatures]] | [[gov:tier_5_review_days]] days |

Tier 5 **special process** (wider maintainer pool and emergency keyholders) is documented in [governance policy](https://github.com/BTCDecoded/governance/blob/main/GOVERNANCE.md), not in `action-tiers.yml`.

## Combination Rules

When both Layer and Tier requirements apply, the system takes the **most restrictive** (highest) requirements:

[[gov:combination_matrix_table]]

## Examples

| Example | Layer | Tier | Result | Source |
|---------|-------|------|--------|--------|
| Bug fix in blvm-protocol | 3 ([[gov:layer_3_signatures]], [[gov:layer_3_review_days]]d) | 1 ([[gov:tier_1_signatures]], [[gov:tier_1_review_days]]d) | [[gov:matrix_3_1_signatures]], [[gov:matrix_3_1_review_days]]d | [[gov:matrix_3_1_source]] |
| New feature in blvm-sdk | 5 ([[gov:layer_5_signatures]], [[gov:layer_5_review_days]]d) | 2 ([[gov:tier_2_signatures]], [[gov:tier_2_review_days]]d) | [[gov:matrix_5_2_signatures]], [[gov:matrix_5_2_review_days]]d | [[gov:matrix_5_2_source]] |
| Consensus change in blvm-spec | 1 ([[gov:layer_1_signatures]], [[gov:layer_1_review_days]]d) | 3 ([[gov:tier_3_signatures]], [[gov:tier_3_review_days]]d) | [[gov:matrix_1_3_signatures]], [[gov:matrix_1_3_review_days]]d | [[gov:matrix_1_3_source]] |
| Emergency fix in blvm-node | 4 ([[gov:layer_4_signatures]], [[gov:layer_4_review_days]]d) | 4 ([[gov:tier_4_signatures]], [[gov:tier_4_review_days]]d) | [[gov:matrix_4_4_signatures]], [[gov:matrix_4_4_review_days]]d | [[gov:matrix_4_4_source]] |

## Implementation


```rust
pub fn get_combined_requirements(layer: i32, tier: u32) -> (usize, usize, i64) {
    let (layer_sigs_req, layer_sigs_total) = Self::get_threshold_for_layer(layer);
    let layer_review = Self::get_review_period_for_layer(layer, false);
    let (tier_sigs_req, tier_sigs_total) = Self::get_tier_threshold(tier);
    let tier_review = Self::get_tier_review_period(tier);
    // Take most restrictive
    (layer_sigs_req.max(tier_sigs_req), layer_sigs_total.max(tier_sigs_total), layer_review.max(tier_review))
}
```

**Test**: `cd blvm-commons && cargo test threshold`

Published tables above are derived from the same max-rule at book build time (`mdbook-governance-vars`). Merge enforcement in `blvm-commons` still uses hardcoded values in `threshold.rs` until that code loads YAML (see plan backlog).

## Configuration

- `config/repository-layers.yml` - Layer definitions
- `config/action-tiers.yml` - Tier definitions ([action tiers](https://github.com/BTCDecoded/governance/blob/main/docs/ACTION_TIERS.md))
- `config/emergency-tiers.yml` - Emergency classes (separate from action tiers)
- `config/tier-classification-rules.yml` - PR classification

## Source

- [threshold.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/threshold.rs)
## See Also

- [PR Process](../development/pr-process.md) - How governance tiers apply to pull requests
- [Governance Model](governance-model.md) - Governance system
- [Multisig Configuration](multisig-configuration.md) - Signature threshold configuration
- [Governance Overview](overview.md) - Governance system introduction
