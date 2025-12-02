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

**Code**: ```12:35:bllvm-commons/src/validation/security_controls.rs```

### Security Control Structure

```yaml
security_controls:
  - id: "A-001"
    name: "Genesis Block Implementation"
    category: "consensus_integrity"
    priority: "P0"
    description: "Proper genesis blocks"
    files:
      - "bllvm-protocol/**/*.rs"
    required_signatures: "7-of-7"
    review_period_days: 180
    requires_security_audit: true
    requires_formal_verification: true
    requires_cryptography_expert: false
    economic_node_veto_enabled: true
```

**Code**: ```20:35:bllvm-commons/src/validation/security_controls.rs```

## Priority Levels

### P0 (Critical)

Highest priority security controls:

- **Impact**: Blocks production deployment and security audit
- **Requirements**: Security audit, formal verification, cryptographer approval
- **Governance Tier**: `security_critical`
- **Examples**: Genesis block implementation, cryptographic primitives

**Code**: ```62:69:bllvm-commons/src/validation/security_controls.rs```

### P1 (High)

High priority security controls:

- **Impact**: Medium impact, may require cryptography expert
- **Requirements**: Security review, formal verification
- **Governance Tier**: `cryptographic` or `security_enhancement`
- **Examples**: Signature verification, key management

**Code**: ```62:69:bllvm-commons/src/validation/security_controls.rs```

### P2 (Medium)

Medium priority security controls:

- **Impact**: Low impact
- **Requirements**: Security review by maintainer
- **Governance Tier**: `security_enhancement`
- **Examples**: Access control, rate limiting

**Code**: ```62:69:bllvm-commons/src/validation/security_controls.rs```

### P3 (Low)

Low priority security controls:

- **Impact**: Minimal impact
- **Requirements**: Standard review
- **Governance Tier**: None (standard process)
- **Examples**: Logging, monitoring

**Code**: ```62:69:bllvm-commons/src/validation/security_controls.rs```

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

**Code**: ```107:185:bllvm-commons/src/validation/security_controls.rs```

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

**Code**: ```62:69:bllvm-commons/src/validation/security_controls.rs```

### Governance Tier Mapping

Impact levels map to governance tiers:

- **Critical/High**: `security_critical` tier
- **Medium (crypto)**: `cryptographic` tier
- **Medium (other)**: `security_enhancement` tier
- **Low**: `security_enhancement` tier
- **None**: Standard tier

**Code**: ```342:374:bllvm-commons/src/validation/security_controls.rs```

## Placeholder Detection

### Placeholder Patterns

The validator detects placeholder implementations in security-critical files:

- `PLACEHOLDER`
- `TODO: Implement`
- `0x00[PLACEHOLDER`
- `0x02[PLACEHOLDER`
- `0x03[PLACEHOLDER`
- `0x04[PLACEHOLDER`
- `return None as a placeholder`
- `return vec![] as a placeholder`
- `This is a placeholder`

**Code**: ```412:473:bllvm-commons/src/validation/security_controls.rs```

### Placeholder Violations

Placeholder violations block PRs affecting P0 controls:

- **Detection**: Automatic scanning of changed files
- **Blocking**: Blocks production deployment
- **Reporting**: Detailed violation reports

**Code**: ```412:429:bllvm-commons/src/validation/security_controls.rs```

## Security Gate CLI

### Status Check

Check security control status:

```bash
security-gate status
security-gate status --detailed
```

**Code**: ```25:210:bllvm-commons/src/bin/security-gate.rs```

### PR Impact Analysis

Analyze security impact of a PR:

```bash
security-gate check-pr 123
security-gate check-pr 123 --format json
```

**Code**: ```212:298:bllvm-commons/src/bin/security-gate.rs```

### Placeholder Check

Check for placeholder implementations:

```bash
security-gate check-placeholders
security-gate check-placeholders --fail-on-placeholder
```

**Code**: ```300:338:bllvm-commons/src/bin/security-gate.rs```

### Production Readiness

Verify production readiness:

```bash
security-gate verify-production-readiness
security-gate verify-production-readiness --format json
```

**Code**: ```340:397:bllvm-commons/src/bin/security-gate.rs```

## Integration with Governance

### Automatic Classification

Security controls automatically classify PRs:

- **File Analysis**: Analyzes changed files
- **Control Matching**: Matches files to controls
- **Tier Assignment**: Assigns governance tier
- **Requirement Collection**: Collects requirements

**Code**: ```1:5:bllvm-commons/src/validation/security_controls.rs```

### PR Comments

The validator generates PR comments with security impact:

- **Impact Level**: Visual indicator of impact
- **Affected Controls**: List of affected controls
- **Required Tier**: Governance tier required
- **Additional Requirements**: List of requirements
- **Blocking Status**: Production/audit blocking status

**Code**: ```475:545:bllvm-commons/src/validation/security_controls.rs```

## Control Requirements

### Security Critical Tier

Requirements for `security_critical` tier:

- All affected P0 controls must be certified
- No placeholder implementations in diff
- Formal verification proofs passing
- Security audit report attached to PR
- Cryptographer approval required

**Code**: ```379:385:bllvm-commons/src/validation/security_controls.rs```

### Cryptographic Tier

Requirements for `cryptographic` tier:

- Cryptographer approval required
- Test vectors from standard specifications
- Side-channel analysis performed
- Formal verification proofs passing

**Code**: ```386:391:bllvm-commons/src/validation/security_controls.rs```

### Security Enhancement Tier

Requirements for `security_enhancement` tier:

- Security review by maintainer
- Comprehensive test coverage
- No placeholder implementations

**Code**: ```392:396:bllvm-commons/src/validation/security_controls.rs```

## Production Blocking

### P0 Control Blocking

P0 controls block production deployment:

- **Blocks Production**: Cannot deploy to production
- **Blocks Audit**: Cannot proceed with security audit
- **Requires Certification**: Must be certified before merge

**Code**: ```148:152:bllvm-commons/src/validation/security_controls.rs```

## Components

The security controls system includes:
- Security control mapping (YAML configuration)
- Security control validator (impact analysis)
- Placeholder detection
- Security gate CLI tool
- Governance tier integration
- PR comment generation

**Location**: `bllvm-commons/src/validation/security_controls.rs`, `bllvm-commons/src/bin/security-gate.rs`

