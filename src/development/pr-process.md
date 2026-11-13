# Pull Request Process

For **human maintainer expectations** and the **AI review intelligence** operating document (alternative implementation vs Core fork, flags, Compact alignment), see [Review standards](../governance/overview.md#review-standards).

## Overview

BLVM writes a **5-tier** action-tier model. Cryptographic enforcement is Designed and is off. The keys are test keys. The tier of a change is the written rule in the governance repository. A signature does not block a merge while enforcement is off.

## PR Lifecycle

The steps below are the written schedule. They do not run while enforcement is off.

### 1. Developer Opens PR

When you open a Pull Request:

1. **Automated CI runs** - Tests, linting, and build verification
2. **Governance tier** - The tier is the written rule for the files the change touches. The app does not classify the pull request while enforcement is off.
3. **Status checks** - CI results appear. A governance status check is not posted while the app is not installed.

### 2. Maintainer review

Maintainers review the change. A cryptographic signature is the written schedule. It is not collected, and it does not block the merge, while enforcement is off.

The designed steps, once enforcement is on, are: review the change, produce a signature with `blvm-sign` from blvm-sdk, comment `/governance-sign <signature>`, and have the Governance App verify it. The app is not installed.

### 3. Review period

Each tier has a written review period:

- **Tier 1**: [[gov:lifecycle_tier1_days]] days
- **Tier 2**: [[gov:lifecycle_tier2_days]] days
- **Tier 3**: [[gov:lifecycle_tier3_days]] days
- **Tier 4**: [[gov:lifecycle_tier4_days]] days (immediate)
- **Tier 5**: [[gov:lifecycle_tier5_days]] days

That period does not start, and it does not block a merge, while enforcement is off.

### 4. Merge

CI is the check that runs. A signature count and a review period do not enable or block the merge while enforcement is off.

## Governance Tiers

### Tier 1: Routine Maintenance

**Scope**: Bug fixes, documentation, performance optimizations

**Requirements**:
- **Signatures**: [[gov:tier_1_signatures]] maintainers
- **Review Period**: [[gov:tier_1_review_days]] days
- **Restriction**: Non-consensus changes only

**Examples**:
- Fixing a typo in documentation
- Performance optimization in non-consensus code
- Bug fix in node networking code
- Code refactoring

### Tier 2: Feature Changes

**Scope**: New RPC methods, P2P changes, wallet features

**Requirements**:
- **Signatures**: [[gov:tier_2_signatures]] maintainers
- **Review Period**: [[gov:tier_2_review_days]] days
- **Requirement**: Must include technical specification

**Examples**:
- Adding a new RPC method
- Implementing a new P2P protocol feature
- Adding wallet functionality
- New SDK features

### Tier 3: Consensus-Adjacent

**Scope**: Changes affecting consensus validation code

**Requirements**:
- **Signatures**: [[gov:tier_3_signatures]] maintainers
- **Review Period**: [[gov:tier_3_review_days]] days
- **Requirement**: Formal verification (BLVM Specification Lock) required

**Examples**:
- Changes to consensus validation logic
- Modifications to block/transaction validation
- Updates to consensus-critical algorithms

**Note**: This tier requires the most scrutiny because changes can affect network consensus.

### Tier 4: Emergency Actions

**Scope**: Critical security patches, network-threatening bugs

**Requirements**:
- **Signatures**: [[gov:tier_4_signatures]] maintainers
- **Review Period**: [[gov:tier_4_review_days]] days (immediate)
- **Requirement**: Post-mortem required

**Severity classes** (incident path; see [Emergency Procedures](#emergency-procedures)):
- **Critical**: network-threatening (short maximum duration once activated)
- **Urgent security**: serious issues (intermediate duration cap)
- **Elevated priority**: important but not critical (longer cap)

**Examples**:
- Critical security vulnerability
- Network-threatening bug
- Consensus-breaking issue requiring immediate fix

### Tier 5: Governance Changes

**Scope**: Changes to governance rules themselves

**Requirements**:
- **Signatures**: Special process (5-of-7 maintainers + 2-of-3 emergency keyholders): see [governance policy](https://github.com/BTCDecoded/governance/blob/main/GOVERNANCE.md) and [action tiers](https://github.com/BTCDecoded/governance/blob/main/docs/ACTION_TIERS.md) (not the `action-tiers.yml` row alone)
- **Review Period**: [[gov:tier_5_review_days]] days. This placeholder renders `tier_5_governance.review_period_days`, which is 180 days. `GOVERNANCE.md` states a 90-day special-process review. Both remain.

**Examples**:
- Changing signature requirements
- Modifying review periods
- Updating governance tier definitions

## Layer + Tier Combination

The governance system combines two dimensions:

1. **Layers** (repository layout) - Which repository the change affects
2. **Tiers** (Action Classification) - What type of change is being made

When both apply, the system uses **"most restrictive wins"** rule:

| Example | Layer | Tier | Final Signatures | Final Review | Source |
|---------|-------|------|------------------|--------------|---------|
| Bug fix in Protocol Engine | 3 | 1 | [[gov:matrix_3_1_signatures]] | [[gov:matrix_3_1_review_days]] days | [[gov:matrix_3_1_source]] |
| New feature in Developer SDK | 5 | 2 | [[gov:matrix_5_2_signatures]] | [[gov:matrix_5_2_review_days]] days | [[gov:matrix_5_2_source]] |
| Consensus change in Orange Paper | 1 | 3 | [[gov:matrix_1_3_signatures]] | [[gov:matrix_1_3_review_days]] days | [[gov:matrix_1_3_source]] |
| Emergency fix in Reference Node | 4 | 4 | [[gov:matrix_4_4_signatures]] | [[gov:matrix_4_4_review_days]] days | [[gov:matrix_4_4_source]] |

See [Layer-Tier Model](../governance/layer-tier-model.md) for the complete decision matrix.

## Signature Requirements by Layer

In addition to tier requirements, layers have their own signature requirements:

- **Layer 1-2 (Constitutional)**: [[gov:layer_1_signatures]] maintainers, [[gov:layer_1_review_days]] days ([[gov:layer_1_consensus_review_days]] days for consensus changes)
- **Layer 3 (Implementation)**: [[gov:layer_3_signatures]] maintainers, [[gov:layer_3_review_days]] days
- **Layer 4 (Application)**: [[gov:layer_4_signatures]] maintainers, [[gov:layer_4_review_days]] days
- **Layer 5 (Extension)**: [[gov:layer_5_signatures]] maintainers, [[gov:layer_5_review_days]] days

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

## Emergency Procedures

The numbered **governance tiers** (Tier 1-5) above describe normal pull-request classification. **Emergency response classes** are a separate axis: when incident handling is escalated, parameters follow the [governance](https://github.com/BTCDecoded/governance) repo's `config/emergency-tiers.yml` (activation by **[[gov:emergency_critical_activation]] emergency keyholders**, then the thresholds below). **Do not confuse "Critical emergency" here with governance Tier 1**, which means routine maintenance PRs.

**Governance Tier 4** (PR classification for emergency merges) remains **[[gov:tier_4_signatures]]** maintainers and **[[gov:tier_4_review_days]]-day** review as in the Tier 4 section above. The classes below describe **post-activation** incident governance on the wider maintainer pool where the YAML specifies **7** eligible signers.

### Critical emergency (network-threatening)

- **Review period**: [[gov:emergency_critical_review_days]] days
- **Maintainer signatures**: [[gov:emergency_critical_signature]] (per `emergency-tiers.yml`)
- **Activation**: [[gov:emergency_critical_activation]] emergency keyholders
- **Maximum duration**: [[gov:emergency_critical_max_days]] days

### Urgent security issue

- **Review period**: [[gov:emergency_urgent_review_days]] days
- **Maintainer signatures**: [[gov:emergency_urgent_signature]]
- **Activation**: [[gov:emergency_urgent_activation]] emergency keyholders
- **Maximum duration**: [[gov:emergency_urgent_max_days]] days

### Elevated priority

- **Review period**: [[gov:emergency_elevated_review_days]] days
- **Maintainer signatures**: [[gov:emergency_elevated_signature]]
- **Activation**: [[gov:emergency_elevated_activation]] emergency keyholders
- **Maximum duration**: [[gov:emergency_elevated_max_days]] days

## How to Get Your PR Reviewed

### 1. Ensure PR is Ready

- All CI checks pass
- Code is well-documented
- Tests are included
- PR description is clear

### 2. Be Patient

Effective review time is set by **combining [repository layer](../governance/layer-tier-model.md) and governance tier** (most restrictive wins). The bullets below are **tier-only** floors where the layer does not impose something stricter, for example, a **Tier 1** change in a **Layer 3** repository can still require **[[gov:matrix_3_1_review_days]] days** (see the matrix in the Layer-Tier Model).

- **Tier 1**: [[gov:tier_1_review_days]] days minimum when layer allows
- **Tier 2**: [[gov:tier_2_review_days]] days minimum when layer allows
- **Tier 3**: [[gov:tier_3_review_days]] days minimum when layer allows
- **Tier 4**: [[gov:tier_4_review_days]] days (immediate once signatures and checks are met)
- **Tier 5**: [[gov:tier_5_review_days]] days minimum when layer allows

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

## Common Questions

### How do I know what tier my PR is?

The Governance App automatically classifies your PR. You'll see the tier in the PR status checks.

### Can I speed up the review process?

No. Effective review periods are fixed by **layer + tier** rules to ensure adequate scrutiny. However, you can:
- Ensure your PR is ready (all checks pass)
- Respond to feedback quickly
- Keep PRs small and focused

### What if I disagree with the tier classification?

Contact maintainers. There's a temporary manual override available for tier classification.

### Can I merge my own PR?

No. All PRs require maintainer signatures and review period to elapse, regardless of who opened it.

## Additional Resources

- [Contributing Guide](contributing.md) - Complete developer workflow
- [Governance Model](../governance/governance-model.md) - Detailed governance documentation
- [Layer-Tier Model](../governance/layer-tier-model.md) - Complete decision matrix

