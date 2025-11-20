# Multisig Configuration

Bitcoin Commons uses multisig thresholds for all governance decisions, with different thresholds based on the layer and tier of the change.

## Layer-Based Thresholds

### Constitutional Layers (Layer 1-2)
- **Orange Paper** (Layer 1): 6-of-7 maintainers, 180 days (365 for consensus changes)
- **bllvm-consensus** (Layer 2): 6-of-7 maintainers, 180 days (365 for consensus changes)

### Implementation Layer (Layer 3)
- **bllvm-protocol**: 4-of-5 maintainers, 90 days

### Application Layer (Layer 4)
- **bllvm-node**: 3-of-5 maintainers, 60 days

### Extension Layer (Layer 5)
- **bllvm-sdk**: 2-of-3 maintainers, 14 days
- **governance**: 2-of-3 maintainers, 14 days
- **bllvm-commons**: 2-of-3 maintainers, 14 days

## Tier-Based Thresholds

### Tier 1: Routine Maintenance
- **Signatures**: 3-of-5 maintainers
- **Review Period**: 7 days
- **Scope**: Bug fixes, documentation, performance optimizations

### Tier 2: Feature Changes
- **Signatures**: 4-of-5 maintainers
- **Review Period**: 30 days
- **Scope**: New RPC methods, P2P changes, wallet features

### Tier 3: Consensus-Adjacent
- **Signatures**: 5-of-5 maintainers
- **Review Period**: 90 days
- **Economic Node Veto**: 30%+ hashpower or 40%+ economic activity
- **Scope**: Changes affecting consensus validation code

### Tier 4: Emergency Actions
- **Signatures**: 4-of-5 maintainers
- **Review Period**: 0 days (immediate)
- **Scope**: Critical security patches, network-threatening bugs

### Tier 5: Governance Changes
- **Signatures**: 5-of-5 maintainers (special process)
- **Review Period**: 180 days
- **Economic Node Signaling**: 50%+ hashpower, 60%+ economic activity
- **Scope**: Changes to governance rules themselves

## Combined Model

When both layer and tier apply, the system uses **"most restrictive wins"** rule. See [LAYER_TIER_MODEL.md](../../modules/governance/LAYER_TIER_MODEL.md) for the complete decision matrix.

## Multisig Threshold Sensitivity

![Multisig Threshold Sensitivity](../images/multisig-threshold-sensitivity.png)
*Figure: Multisig threshold sensitivity analysis showing how different threshold configurations affect security and decision-making speed.*

## Governance Signature Thresholds

![Governance Signature Thresholds](../images/governance-signature-thresholds.png)
*Figure: Signature thresholds by layer showing the graduated security model.*

For configuration details, see the [governance configuration files](../../modules/governance/config/).

