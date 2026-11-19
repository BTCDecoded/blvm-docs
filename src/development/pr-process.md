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

## Schedules

Review windows by layer and by tier are on [Governance model](../governance/governance-model.md#review-window-by-repository-layer).

| Tier | What it covers | Signatures | Review |
|---|---|---|---|
| 1 | Bug fixes, documentation, performance. Non-consensus only | [[gov:tier_1_signatures]] | [[gov:tier_1_review_days]] days |
| 2 | New RPC methods, P2P changes, wallet features. A technical specification is required | [[gov:tier_2_signatures]] | [[gov:tier_2_review_days]] days |
| 3 | Consensus validation. Specification Lock is required | [[gov:tier_3_signatures]] | [[gov:tier_3_review_days]] days |
| 4 | Critical patches. A post-mortem is required. This row is not an emergency class | [[gov:tier_4_signatures]] | [[gov:tier_4_review_days]] days |
| 5 | Changes to the governance rules | Special process in [GOVERNANCE.md](https://github.com/BTCDecoded/governance/blob/main/GOVERNANCE.md) | [[gov:tier_5_review_days]] days |

Tier 5 is a special process (5-of-7 maintainers + 2-of-3 emergency keyholders). That pair is not the `tier_5_governance` row alone. The YAML review is [[gov:tier_5_review_days]] days. `GOVERNANCE.md` also states a 90-day special-process review. Both remain.

## Layer and tier together

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

See [Layers and tiers](../governance/layer-tier-model.md) for the full matrix. The higher signature count and the longer review window win. Constitutional consensus changes use [[gov:layer_1_consensus_review_days]] days.

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

| Class | Review | Signatures | Activation | Maximum |
|---|---|---|---|---|
| Critical | [[gov:emergency_critical_review_days]] days | [[gov:emergency_critical_signature]] | [[gov:emergency_critical_activation]] | [[gov:emergency_critical_max_days]] days |
| Urgent | [[gov:emergency_urgent_review_days]] days | [[gov:emergency_urgent_signature]] | [[gov:emergency_urgent_activation]] | [[gov:emergency_urgent_max_days]] days |
| Elevated | [[gov:emergency_elevated_review_days]] days | [[gov:emergency_elevated_signature]] | [[gov:emergency_elevated_activation]] | [[gov:emergency_elevated_max_days]] days |

While enforcement is off, CI is the check that runs. The periods above do not start and do not block a merge. A Tier 1 change in a Layer 3 repository can still require [[gov:matrix_3_1_review_days]] days once enforcement is on.

## Additional Resources

- [Contributing Guide](contributing.md) - Complete developer workflow
- [Governance Model](../governance/governance-model.md) - Detailed governance documentation
- [Layer-Tier Model](../governance/layer-tier-model.md) - Complete decision matrix

