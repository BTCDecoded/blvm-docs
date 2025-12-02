# Layer-Tier Governance Model

## Overview

Bitcoin Commons implements dual-dimensional governance combining **Layers** (repository architecture) and **Tiers** (action classification). When both apply, the system uses the **most restrictive wins** rule, taking the highest signature requirement and longest review period.

## Layer System

The layer system maps repository architecture to governance requirements:

| Layer | Repository | Purpose | Signatures | Review Period |
|-------|------------|---------|------------|---------------|
| 1 | bllvm-spec | Constitutional | 6-of-7 | 180 days |
| 2 | bllvm-consensus | Constitutional | 6-of-7 | 180 days |
| 3 | bllvm-protocol | Implementation | 4-of-5 | 90 days |
| 4 | bllvm-node / bllvm | Application | 3-of-5 | 60 days |
| 5 | bllvm-sdk | Extension | 2-of-3 | 14 days |

**Note:** For consensus rule changes, Layer 1-2 require 365 days review period.

## Tier System

The tier system classifies changes by action type:

| Tier | Type | Signatures | Review Period | Economic Veto |
|------|------|------------|---------------|---------------|
| 1 | Routine Maintenance | 3-of-5 | 7 days | No |
| 2 | Feature Changes | 4-of-5 | 30 days | No |
| 3 | Consensus-Adjacent | 5-of-5 | 90 days | Yes |
| 4 | Emergency Actions | 4-of-5 | 0 days | No |
| 5 | Governance Changes | 5-of-5 | 180 days | Yes |

## Combination Rules

When both Layer and Tier requirements apply, the system takes the **most restrictive** (highest) requirements:

| Layer | Tier | Final Signatures | Final Review | Source |
|-------|------|------------------|--------------|---------|
| 1 | 1 | 6-of-7 | 180 days | Layer 1 |
| 1 | 2 | 6-of-7 | 180 days | Layer 1 |
| 1 | 3 | 6-of-7 | 180 days | Layer 1 |
| 1 | 4 | 6-of-7 | 180 days | Layer 1 |
| 1 | 5 | 6-of-7 | 180 days | Layer 1 |
| 2 | 1 | 6-of-7 | 180 days | Layer 2 |
| 2 | 2 | 6-of-7 | 180 days | Layer 2 |
| 2 | 3 | 6-of-7 | 180 days | Layer 2 |
| 2 | 4 | 6-of-7 | 180 days | Layer 2 |
| 2 | 5 | 6-of-7 | 180 days | Layer 2 |
| 3 | 1 | 4-of-5 | 90 days | Layer 3 |
| 3 | 2 | 4-of-5 | 90 days | Layer 3 |
| 3 | 3 | 5-of-5 | 90 days | Tier 3 |
| 3 | 4 | 4-of-5 | 90 days | Layer 3 |
| 3 | 5 | 5-of-5 | 180 days | Tier 5 |
| 4 | 1 | 3-of-5 | 60 days | Layer 4 |
| 4 | 2 | 4-of-5 | 60 days | Tier 2 |
| 4 | 3 | 5-of-5 | 90 days | Tier 3 |
| 4 | 4 | 4-of-5 | 60 days | Layer 4 |
| 4 | 5 | 5-of-5 | 180 days | Tier 5 |
| 5 | 1 | 2-of-3 | 14 days | Layer 5 |
| 5 | 2 | 4-of-5 | 30 days | Tier 2 |
| 5 | 3 | 5-of-5 | 90 days | Tier 3 |
| 5 | 4 | 4-of-5 | 14 days | Layer 5 |
| 5 | 5 | 5-of-5 | 180 days | Tier 5 |

## Examples

| Example | Layer | Tier | Result | Source |
|---------|-------|------|--------|--------|
| Bug fix in bllvm-protocol | 3 (4-of-5, 90d) | 1 (3-of-5, 7d) | 4-of-5, 90d | Layer 3 |
| New feature in bllvm-sdk | 5 (2-of-3, 14d) | 2 (4-of-5, 30d) | 4-of-5, 30d | Tier 2 |
| Consensus change in bllvm-spec | 1 (6-of-7, 180d) | 3 (5-of-5, 90d) | 6-of-7, 180d | Layer 1 |
| Emergency fix in bllvm-node | 4 (3-of-5, 60d) | 4 (4-of-5, 0d) | 4-of-5, 0d | Tier 4 |

## Economic Veto Requirements

Economic node vetoes required for **Tier 3+** (any layer). Thresholds: Tier 3 (30%+ hashpower AND 40%+ economic), Tier 4 (25%+ AND 35%+), Tier 5 (50%+ AND 60%+).

## Implementation

**Code**: ```63:125:bllvm-commons/src/validation/threshold.rs```

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

**Test**: `cd bllvm-commons && cargo test threshold`

## Configuration

- `config/repository-layers.yml` - Layer definitions
- `config/action-tiers.yml` - Tier definitions
- `config/tier-classification-rules.yml` - PR classification

## See Also

- [PR Process](../development/pr-process.md) - How governance tiers apply to pull requests
- [Governance Model](governance-model.md) - Governance system
- [Multisig Configuration](multisig-configuration.md) - Signature threshold configuration
- [Economic Nodes](economic-nodes.md) - Economic node veto system
- [Governance Overview](overview.md) - Governance system introduction
