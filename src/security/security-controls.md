# Security Controls System

## Overview

Bitcoin Commons implements a security controls system that automatically classifies pull requests based on affected security controls and determines required governance tiers. This embeds security controls directly into the governance system, making it self-enforcing.

## Architecture

### Security Control Mapping

Security controls are defined in a YAML configuration file that maps file patterns to security controls:

- **File Patterns**: Glob patterns matching code files
- **Control Definitions**: Security control metadata
- **Priority Levels**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- **Categories**: Control categories (consensus_integrity, cryptographic, etc.)

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L12-L35)

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
    required_signatures: "7-of-7"
    review_period_days: 180
    requires_security_audit: true
    requires_formal_verification: true
    requires_cryptography_expert: false
```

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L20-L35)

## Priority Levels

### P0 (Critical)

Highest priority security controls:

- **Impact**: Blocks production deployment and security audit
- **Requirements**: Security audit, formal verification, cryptographer approval
- **Governance Tier**: `security_critical`
- **Examples**: Genesis block implementation, cryptographic primitives

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L62-L69)

### P1 (High)

High priority security controls:

- **Impact**: Medium impact, may require cryptography expert
- **Requirements**: Security review, formal verification
- **Governance Tier**: `cryptographic` or `security_enhancement`
- **Examples**: Signature verification, key management

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L62-L69)

### P2 (Medium)

Medium priority security controls:

- **Impact**: Low impact
- **Requirements**: Security review by maintainer
- **Governance Tier**: `security_enhancement`
- **Examples**: Access control, rate limiting

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L62-L69)

### P3 (Low)

Low priority security controls:

- **Impact**: Minimal impact
- **Requirements**: Standard review
- **Governance Tier**: None (standard process)
- **Examples**: Logging, monitoring

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L62-L69)

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

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L107-L185)

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

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L62-L69)

### Governance Tier Mapping

Impact levels map to governance tiers:

- **Critical/High**: `security_critical` tier
- **Medium (crypto)**: `cryptographic` tier
- **Medium (other)**: `security_enhancement` tier
- **Low**: `security_enhancement` tier
- **None**: Standard tier

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L342-L374)

## Placeholder Detection

### Placeholder Patterns

The validator detects placeholder implementations in security-critical files:

- `PLACEHOLDER`
- See [Threat Models](threat-models.md) for comprehensive security documentation
- `0x00[PLACEHOLDER`
- `0x02[PLACEHOLDER`
- `0x03[PLACEHOLDER`
- `0x04[PLACEHOLDER`
- `return None as a placeholder`
- `return vec![] as a placeholder`
- `This is a placeholder`

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L412-L473)

### Placeholder Violations

Placeholder violations block PRs affecting P0 controls:

- **Detection**: Automatic scanning of changed files
- **Blocking**: Blocks production deployment
- **Reporting**: Detailed violation reports

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L412-L429)

## Security Gate CLI

### Status Check

Check security control status:

```bash
security-gate status
security-gate status --detailed
```

**Code**: [security-gate.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/bin/security-gate.rs#L25-L210)

### PR Impact Analysis

Analyze security impact of a PR:

```bash
security-gate check-pr 123
security-gate check-pr 123 --format json
```

**Code**: [security-gate.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/bin/security-gate.rs#L212-L298)

### Placeholder Check

Check for placeholder implementations:

```bash
security-gate check-placeholders
security-gate check-placeholders --fail-on-placeholder
```

**Code**: [security-gate.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/bin/security-gate.rs#L300-L338)

### Production Readiness

Verify production readiness:

```bash
security-gate verify-production-readiness
security-gate verify-production-readiness --format json
```

**Code**: [security-gate.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/bin/security-gate.rs#L340-L397)

## Integration with Governance

### Automatic Classification

Security controls automatically classify PRs:

- **File Analysis**: Analyzes changed files
- **Control Matching**: Matches files to controls
- **Tier Assignment**: Assigns governance tier
- **Requirement Collection**: Collects requirements

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L1-L5)

### PR Comments

The validator generates PR comments with security impact:

- **Impact Level**: Visual indicator of impact
- **Affected Controls**: List of affected controls
- **Required Tier**: Governance tier required
- **Additional Requirements**: List of requirements
- **Blocking Status**: Production/audit blocking status

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L475-L545)

## Control Requirements

### Security Critical Tier

Requirements for `security_critical` tier:

- All affected P0 controls must be certified
- No placeholder implementations in diff
- Formal verification proofs passing
- Security audit report attached to PR
- Cryptographer approval required

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L379-L385)

### Cryptographic Tier

Requirements for `cryptographic` tier:

- Cryptographer approval required
- Test vectors from standard specifications
- Side-channel analysis performed
- Formal verification proofs passing

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L386-L391)

### Security Enhancement Tier

Requirements for `security_enhancement` tier:

- Security review by maintainer
- Comprehensive test coverage
- No placeholder implementations

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L392-L396)

## Production Blocking

### P0 Control Blocking

P0 controls block production deployment:

- **Blocks Production**: Cannot deploy to production
- **Blocks Audit**: Cannot proceed with security audit
- **Requires Certification**: Must be certified before merge

**Code**: [security_controls.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/validation/security_controls.rs#L148-L152)

## Components

The security controls system includes:
- Security control mapping (YAML configuration)
- Security control validator (impact analysis)
- Placeholder detection
- Security gate CLI tool
- Governance tier integration
- PR comment generation

**Location**: `blvm-commons/src/validation/security_controls.rs`, `blvm-commons/src/bin/security-gate.rs`

## See Also

- [Threat Models](threat-models.md) - Security threat analysis
- [Developer Security Checklist](DEVELOPER_SECURITY_CHECKLIST.md) - Security checklist for developers
- [Security Architecture Review Template](ARCHITECTURE_REVIEW_TEMPLATE.md) - Architecture review process
- [Security Testing Template](SECURITY_TESTING_TEMPLATE.md) - Security testing guidelines
- [Contributing](../development/contributing.md) - Development workflow
- [PR Process](../development/pr-process.md) - Security review in PR process
