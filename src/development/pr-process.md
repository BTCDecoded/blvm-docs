# Pull Request Process

This document explains the PR review process, governance tiers, signature requirements, and how to get your PR reviewed and merged.

## Overview

BLVM uses a **5-tier constitutional governance model** with cryptographic signatures to ensure secure, transparent, and accountable code changes. Every PR is automatically classified into a governance tier based on the scope and impact of the changes.

## PR Lifecycle

### 1. Developer Opens PR

When you open a Pull Request:

1. **Automated CI runs** - Tests, linting, and build verification
2. **Governance tier classification** - PR is automatically classified (with temporary manual override available)
3. **Status checks appear** - Shows what needs to happen for merge

### 2. Maintainers Review and Sign

Maintainers review your code and cryptographically sign approval:

1. **Review PR** - Understand the change and its impact
2. **Generate signature** - Use `blvm-sign` from blvm-sdk
3. **Post signature** - Comment `/governance-sign <signature>` on PR
4. **Governance App verifies** - Cryptographically verifies signature
5. **Status check updates** - Shows signature count progress

### 3. Review Period Elapses

Each tier has a specific review period that must elapse:

- **Tier 1**: 7 days
- **Tier 2**: 30 days
- **Tier 3**: 90 days
- **Tier 4**: 0 days (immediate)
- **Tier 5**: 180 days

The review period starts when the PR is opened and all required signatures are collected.

### 4. Economic Node Veto Period (Tier 3+ Only)

For Tier 3+ changes, economic nodes can veto during the review period:

- **Hashpower threshold**: 30%+ of network hashpower
- **Economic activity threshold**: 40%+ of economic activity
- **Veto process**: Economic nodes register and signal veto
- **Enforcement**: Veto blocks merge until resolved

### 5. Requirements Met → Merge Enabled

Once all requirements are met:
- ✅ Required signatures collected
- ✅ Review period elapsed
- ✅ No economic node veto (if applicable)
- ✅ All CI checks pass

The PR can be merged.

## Governance Tiers

### Tier 1: Routine Maintenance

**Scope**: Bug fixes, documentation, performance optimizations

**Requirements**:
- **Signatures**: 3-of-5 maintainers
- **Review Period**: 7 days
- **Restriction**: Non-consensus changes only

**Examples**:
- Fixing a typo in documentation
- Performance optimization in non-consensus code
- Bug fix in node networking code
- Code refactoring

### Tier 2: Feature Changes

**Scope**: New RPC methods, P2P changes, wallet features

**Requirements**:
- **Signatures**: 4-of-5 maintainers
- **Review Period**: 30 days
- **Requirement**: Must include technical specification

**Examples**:
- Adding a new RPC method
- Implementing a new P2P protocol feature
- Adding wallet functionality
- New SDK features

### Tier 3: Consensus-Adjacent

**Scope**: Changes affecting consensus validation code

**Requirements**:
- **Signatures**: 5-of-5 maintainers
- **Review Period**: 90 days
- **Economic Node Veto**: 30%+ hashpower or 40%+ economic activity
- **Requirement**: Formal verification (Kani) required

**Examples**:
- Changes to consensus validation logic
- Modifications to block/transaction validation
- Updates to consensus-critical algorithms

**Note**: This tier requires the most scrutiny because changes can affect network consensus.

### Tier 4: Emergency Actions

**Scope**: Critical security patches, network-threatening bugs

**Requirements**:
- **Signatures**: 4-of-5 maintainers
- **Review Period**: 0 days (immediate)
- **Requirement**: Real-time economic node oversight, post-mortem required

**Sub-tiers**:
- **Critical Emergency**: Network-threatening (7 day maximum duration)
- **Urgent Security**: Security issues (30 day maximum duration)
- **Elevated Priority**: Important fixes (90 day maximum duration)

**Examples**:
- Critical security vulnerability
- Network-threatening bug
- Consensus-breaking issue requiring immediate fix

### Tier 5: Governance Changes

**Scope**: Changes to governance rules themselves

**Requirements**:
- **Signatures**: Special process (5-of-7 maintainers + 2-of-3 emergency keyholders)
- **Review Period**: 180 days
- **Economic Node Signaling**: 50%+ hashpower, 60%+ economic activity

**Examples**:
- Changing signature requirements
- Modifying review periods
- Updating governance tier definitions

## Layer + Tier Combination

The governance system combines two dimensions:

1. **Layers** (Repository Architecture) - Which repository the change affects
2. **Tiers** (Action Classification) - What type of change is being made

When both apply, the system uses **"most restrictive wins"** rule:

| Example | Layer | Tier | Final Signatures | Final Review | Source |
|---------|-------|------|------------------|--------------|---------|
| Bug fix in Protocol Engine | 3 | 1 | 4-of-5 | 90 days | Layer 3 |
| New feature in Developer SDK | 5 | 2 | 4-of-5 | 30 days | Tier 2 |
| Consensus change in Orange Paper | 1 | 3 | 6-of-7 | 180 days | Layer 1 |
| Emergency fix in Reference Node | 4 | 4 | 4-of-5 | 0 days | Tier 4 |

See [Layer-Tier Model](../governance/layer-tier-model.md) for the complete decision matrix.

## Signature Requirements by Layer

In addition to tier requirements, layers have their own signature requirements:

- **Layer 1-2 (Constitutional)**: 6-of-7 maintainers, 180 days (365 for consensus changes)
- **Layer 3 (Implementation)**: 4-of-5 maintainers, 90 days
- **Layer 4 (Application)**: 3-of-5 maintainers, 60 days
- **Layer 5 (Extension)**: 2-of-3 maintainers, 14 days

The most restrictive requirement (layer or tier) applies.

## Maintainer Signing Process

### How Maintainers Sign

1. **Review PR**: Understand the change and its impact
2. **Generate signature**: Use `blvm-sign` from blvm-sdk:
   ```bash
   blvm-sign --message "Approve PR #123" --key ~/.blvm/maintainer.key
   ```
3. **Post signature**: Comment on PR:
   ```
   /governance-sign <signature>
   ```
4. **Governance App verifies**: Cryptographically verifies signature
5. **Status check updates**: Shows signature count progress

### Signature Verification

The Governance App cryptographically verifies each signature:
- Uses secp256k1 ECDSA (Bitcoin-compatible)
- Verifies signature matches maintainer's public key
- Ensures signature is for the correct PR
- Prevents signature reuse

## Economic Node Veto System

For Tier 3+ changes, economic nodes can veto during the review period.

### Veto Thresholds

- **Hashpower threshold**: 30%+ of network hashpower
- **Economic activity threshold**: 40%+ of economic activity

### Veto Process

1. **Economic nodes register** - Nodes that meet threshold requirements
2. **Signal veto** - During review period, nodes can signal veto
3. **Veto blocks merge** - PR cannot be merged while veto is active
4. **Resolution** - Veto must be resolved before merge

### Why Economic Node Veto?

Economic nodes (miners, exchanges, large holders) have significant stake in the network. For consensus-adjacent changes, they need a way to signal concerns before changes are merged.

## Emergency Procedures

The system includes a three-tiered emergency response system:

### Tier 1: Critical Emergency (Network-threatening)

- **Review period**: 0 days
- **Signatures**: 4-of-7 maintainers
- **Activation**: 5-of-7 emergency keyholders required
- **Maximum duration**: 7 days

### Tier 2: Urgent Security Issue

- **Review period**: 7 days
- **Signatures**: 5-of-7 maintainers
- **Maximum duration**: 30 days

### Tier 3: Elevated Priority

- **Review period**: 30 days
- **Signatures**: 6-of-7 maintainers
- **Maximum duration**: 90 days

## How to Get Your PR Reviewed

### 1. Ensure PR is Ready

- ✅ All CI checks pass
- ✅ Code is well-documented
- ✅ Tests are included
- ✅ PR description is clear

### 2. Be Patient

Review periods vary by tier:
- **Tier 1**: 7 days minimum
- **Tier 2**: 30 days minimum
- **Tier 3**: 90 days minimum
- **Tier 4**: 0 days (immediate)
- **Tier 5**: 180 days minimum

### 3. Respond to Feedback

- Address review comments promptly
- Update PR as needed
- Keep PR description current

### 4. Keep PRs Small

- Smaller PRs are reviewed faster
- Easier to understand
- Less risk of issues

### 5. Communicate

- Update PR description if scope changes
- Respond to questions
- Ask for help if stuck

## PR Status Indicators

Your PR will show status indicators:

- **Signature progress**: `3/5 signatures collected`
- **Review period**: `5 days remaining`
- **CI status**: All checks passing/failing
- **Veto status**: No veto / Veto active

## Common Questions

### How do I know what tier my PR is?

The Governance App automatically classifies your PR. You'll see the tier in the PR status checks.

### Can I speed up the review process?

No. Review periods are fixed by tier to ensure adequate scrutiny. However, you can:
- Ensure your PR is ready (all checks pass)
- Respond to feedback quickly
- Keep PRs small and focused

### What if I disagree with the tier classification?

Contact maintainers. There's a temporary manual override available for tier classification.

### What happens if economic nodes veto my PR?

The veto blocks merge. You'll need to:
- Address concerns raised by economic nodes
- Update PR to address issues
- Wait for veto to be lifted

### Can I merge my own PR?

No. All PRs require maintainer signatures and review period to elapse, regardless of who opened it.

## Additional Resources

- [Contributing Guide](contributing.md) - Complete developer workflow
- [Governance Model](../governance/governance-model.md) - Detailed governance documentation
- [Layer-Tier Model](../governance/layer-tier-model.md) - Complete decision matrix
- [Economic Nodes](../governance/economic-nodes.md) - Economic node system details

