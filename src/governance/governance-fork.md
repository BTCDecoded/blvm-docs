# Governance Fork System

## Overview

The governance fork mechanism enables users to choose between different governance rulesets without affecting Bitcoin consensus. This provides an escape hatch for users who disagree with governance decisions while maintaining Bitcoin protocol integrity.

## Fork Types

| Type | Definition | Compatibility | Examples |
|------|------------|---------------|----------|
| **Soft Fork** | Changes without breaking compatibility | Existing users continue, new users choose updated | Adding signature requirements, modifying time locks, updating thresholds |
| **Hard Fork** | Breaking changes | All users must choose, no backward compatibility | Changing signature schemes, modifying fundamental principles, removing tiers |

## Ruleset Export

### Export Format

Governance rulesets exported as versioned, signed packages in YAML format:

```yaml
ruleset_version: "1.2.0"
export_timestamp: "YYYY-MM-DDTHH:MM:SSZ"
previous_ruleset_hash: "sha256:abc123..."
governance_rules:
  action_tiers: { /* tier definitions */ }
  repository_layers: { /* layer definitions */ }
  maintainers: { /* maintainer registry */ }
  economic_nodes: { /* economic node registry */ }
  emergency_procedures: { /* emergency protocols */ }
cryptographic_proofs:
  maintainer_signatures: [ /* signed by maintainers */ ]
  ruleset_hash: "sha256:def456..."
  merkle_root: "sha256:ghi789..."
compatibility:
  min_version: "1.0.0"
  max_version: "2.0.0"
  breaking_changes: false
```

### Export Process

1. Ruleset preparation (compile current governance rules from YAML files)
2. Cryptographic signing (maintainers sign the ruleset)
3. Hash calculation (generate tamper-evident hash)
4. Merkle tree (create verification structure)
5. Export generation (package for distribution)
6. Publication (make available for download)

**Code**: ```1:200:bllvm-commons/src/fork/export.rs```

## Versioning System

| Version Component | Meaning | Example |
|-------------------|---------|---------|
| **Major** | Breaking changes (hard fork) | 2.0.0 (incompatible with 1.x) |
| **Minor** | New features (soft fork) | 1.2.0 (compatible with 1.x) |
| **Patch** | Bug fixes and improvements | 1.1.1 (compatible with 1.1.x) |

**Compatibility**: Compatible (upgrade without issues), Incompatible (must choose), Deprecated (removed), Supported (receives updates).

## Adoption Tracking

Track ruleset adoption through: node count, hash rate, user count, exchange support.

**Public Dashboard**: Current distribution, adoption trends, geographic distribution, economic node support, exchange listings.

## Fork Decision Process

### User Choice

1. Download ruleset package
2. Verify maintainer signatures
3. Validate ruleset integrity (hash)
4. Configure client (set ruleset)
5. Announce choice (publicly declare)

### Client Implementation

- Ruleset loading (load chosen ruleset)
- Signature verification (verify maintainer signatures)
- Rule enforcement (apply governance rules)
- Status reporting (report chosen ruleset)
- Update mechanism (handle ruleset updates)

**Code**: ```1:150:bllvm-commons/src/fork/executor.rs```

## Fork Resolution

### Conflict Resolution

When forks occur:
1. User notification (alert users to fork)
2. Choice period (30 days to choose ruleset)
3. Migration support (tools for ruleset migration)
4. Documentation (clear migration guides)
5. Support (community support during transition)

### Fork Merging

Forks can be merged by: consensus building, gradual migration, feature adoption, clean slate.

## Security Considerations

| Aspect | Requirements |
|--------|--------------|
| **Ruleset Integrity** | Cryptographic signatures, hash verification, Merkle trees, timestamp anchoring |
| **Fork Security** | Replay protection, version validation, signature verification, threshold enforcement |

## Examples

| Scenario | Type | Change | Result |
|----------|------|--------|--------|
| Adding signature requirement | Soft Fork | Require 4-of-5 instead of 3-of-5 | Existing users continue with 3-of-5, new users use 4-of-5 |
| Changing signature scheme | Hard Fork | Switch from Ed25519 to Dilithium | Clean split into two governance models |

## Configuration

- `governance/config/governance-fork.yml` - Fork configuration
- `governance/fork-registry.yml` - Registered forks

