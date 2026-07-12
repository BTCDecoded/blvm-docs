# PR security control classification

Contributor and CI documentation: how pull requests are classified against security controls and governance tiers. **Operators** preparing a mainnet deployment should start with [Deployment posture](../security/deployment-posture.md) instead.

## Overview

Bitcoin Commons implements a security controls system that automatically classifies pull requests based on affected security controls and determines required governance tiers. This embeds security controls directly into the governance system, making it self-enforcing.

## Architecture

### Security Control Mapping

Security controls are defined in a YAML configuration file that maps file patterns to security controls:

- **File Patterns**: Glob patterns matching code files
- **Control Definitions**: Security control metadata
- **Priority Levels**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- **Categories**: Control categories (consensus_integrity, cryptographic, etc.)


### Security Control Structure

```yaml
security_controls:
  - id: "A-001"
    name: "Genesis Block Implementation"
    category: "consensus_integrity"
    priority: "P0"
    description: "Proper genesis blocks"
    files:
      - "blvm-protocol/**/*.rs"
    required_signatures: "[[gov:security_critical_signatures]]"
    review_period_days: [[gov:security_critical_review_days]]
    requires_security_audit: true
    requires_formal_verification: true
    requires_cryptography_expert: false
```


## Priority Levels

### P0 (Critical)

Highest priority security controls:

- **Impact**: Blocks production deployment and security audit
- **Requirements**: Security audit, formal verification, cryptographer approval
- **Governance Tier**: `security_critical`
- **Examples**: Genesis block implementation, cryptographic primitives


### P1 (High)

High priority security controls:

- **Impact**: Medium impact, may require cryptography expert
- **Requirements**: Security review, formal verification
- **Governance Tier**: `cryptographic` or `security_enhancement`
- **Examples**: Signature verification, key management


### P2 (Medium)

Medium priority security controls:

- **Impact**: Low impact
- **Requirements**: Security review by maintainer
- **Governance Tier**: `security_enhancement`
- **Examples**: Access control, rate limiting


### P3 (Low)

Low priority security controls:

- **Impact**: Minimal impact
- **Requirements**: Standard review
- **Governance Tier**: None (standard process)
- **Examples**: Logging, monitoring


## Control Categories

### Consensus Integrity

Controls related to consensus-critical code:

- **Max Priority**: P0
- **Examples**: Block validation, transaction validation, UTXO management
- **Requirements**: Formal verification, security audit

### Cryptographic

Controls related to cryptographic operations:

- **Max Priority**: P0
- **Examples**: Signature verification, key generation, hash functions
- **Requirements**: Cryptographer approval, side-channel analysis

### Access Control

Controls related to authorization and access:

- **Max Priority**: P1
- **Examples**: Maintainer authorization, server authorization
- **Requirements**: Security review

### Network Security

Controls related to network protocols:

- **Max Priority**: P1
- **Examples**: P2P message validation, relay security
- **Requirements**: Security review

## Security Control Validator

### Impact Analysis

The `SecurityControlValidator` analyzes security impact of changed files:

1. **File Matching**: Matches changed files against control patterns
2. **Control Identification**: Identifies affected security controls
3. **Priority Calculation**: Determines highest priority affected
4. **Tier Determination**: Determines required governance tier
5. **Requirement Collection**: Collects additional requirements


### Impact Levels

```rust
pub enum ImpactLevel {
    None,      // No controls affected
    Low,       // P2 controls
    Medium,    // P1 controls
    High,      // P0 controls
    Critical,  // Multiple P0 controls
}
```


### Governance Tier Mapping

Impact levels map to governance tiers:

- **Critical/High**: `security_critical` tier
- **Medium (crypto)**: `cryptographic` tier
- **Medium (other)**: `security_enhancement` tier
- **Low**: `security_enhancement` tier
- **None**: Standard tier


## Placeholder Detection

### Placeholder Patterns

The validator detects placeholder implementations in security-critical files:

- `PLACEHOLDER`
- See [Threat Models](../security/threat-models.md) for security documentation
- `0x00[PLACEHOLDER`
- `0x02[PLACEHOLDER`
- `0x03[PLACEHOLDER`
- `0x04[PLACEHOLDER`
- `return None as a placeholder`
- return vec![] as a placeholder
- `This is a placeholder`


### Placeholder Violations

Placeholder violations block PRs affecting P0 controls:

- **Detection**: Automatic scanning of changed files
- **Blocking**: Blocks production deployment
- **Reporting**: Detailed violation reports


## Security Gate CLI

### Status Check

Check security control status:

```bash
security-gate status
security-gate status --detailed
```


### PR Impact Analysis

Analyze security impact of a PR:

```bash
security-gate check-pr 123
security-gate check-pr 123 --format json
```


### Placeholder Check

Check for placeholder implementations:

```bash
security-gate check-placeholders
security-gate check-placeholders --fail-on-placeholder
```


### Production Readiness

Verify production readiness:

```bash
security-gate verify-production-readiness
security-gate verify-production-readiness --format json
```


## Integration with Governance

### Automatic Classification

Security controls automatically classify PRs:

- **File Analysis**: Analyzes changed files
- **Control Matching**: Matches files to controls
- **Tier Assignment**: Assigns governance tier
- **Requirement Collection**: Collects requirements


### PR Comments

The validator generates PR comments with security impact:

- **Impact Level**: Visual indicator of impact
- **Affected Controls**: List of affected controls
- **Required Tier**: Governance tier required
- **Additional Requirements**: List of requirements
- **Blocking Status**: Production/audit blocking status


## Control Requirements

### Security Critical Tier

Requirements for `security_critical` tier:

- All affected P0 controls must be certified
- No placeholder implementations in diff
- Formal verification proofs passing
- Security audit report attached to PR
- Cryptographer approval required


### Cryptographic Tier

Requirements for `cryptographic` tier:

- Cryptographer approval required
- Test vectors from standard specifications
- Side-channel analysis performed
- Formal verification proofs passing


### Security Enhancement Tier

Requirements for `security_enhancement` tier:

- Security review by maintainer
- Unit, integration, property, and differential tests across consensus, node, and SDK crates (see each repository's `cargo test` targets)
- No placeholder implementations


## Production Blocking

### P0 Control Blocking

P0 controls block production deployment:

- **Blocks Production**: Cannot deploy to production
- **Blocks Audit**: Cannot proceed with security audit
- **Requires Certification**: Must be certified before merge


## Components

The security controls system includes:
- Security control mapping (YAML configuration)
- Security control validator (impact analysis)
- Placeholder detection
- Security gate CLI tool
- Governance tier integration
- PR comment generation


## Source

- [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs)
- [security-gate.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/bin/security-gate.rs)
## See Also

- [Threat Models](../security/threat-models.md) - Security threat analysis
- [Developer Security Checklist](../appendices/templates/DEVELOPER_SECURITY_CHECKLIST.md) - Security checklist for developers
- [Security Architecture Review Template](../appendices/templates/ARCHITECTURE_REVIEW_TEMPLATE.md) - Architecture review process
- [Security Testing Template](../appendices/templates/SECURITY_TESTING_TEMPLATE.md) - Security testing guidelines
- [Contributing](../development/contributing.md) - Development workflow
- [PR Process](../development/pr-process.md) - Security review in PR process
