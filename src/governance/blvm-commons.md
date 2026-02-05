# blvm-commons

## Overview

blvm-commons is the governance enforcement system for Bitcoin Commons. It provides GitHub integration, OpenTimestamps verification, Nostr integration, and cross-layer validation for the Bitcoin Commons governance framework.

## Key Features

- **GitHub Integration**: GitHub App for cryptographic signature verification and merge enforcement
- **OpenTimestamps**: Immutable audit trail for governance artifacts
- **Nostr Integration**: Decentralized governance communication and voting
- **Cross-Layer Validation**: Security controls and validation across all layers
- **CI/CD Workflows**: Reusable workflows for Bitcoin Commons repositories

## Components

### GitHub Integration

The GitHub App enforces cryptographic signatures on pull requests, verifies signature thresholds, and blocks merges until governance requirements are met.

**Code**: [GitHub App](https://github.com/BTCDecoded/blvm-commons)

### OpenTimestamps Integration

Provides immutable timestamping for governance artifacts, verification proofs, and audit trails.

**Code**: [OpenTimestamps Integration](opentimestamps-integration.md)

### Nostr Integration

Enables decentralized governance communication, voting, and proposal distribution through Nostr relays.

**Code**: [Nostr Integration](nostr-integration.md)

### Security Controls

Validates code changes, detects placeholder implementations, and enforces security policies across all Bitcoin Commons repositories.

**Code**: [Security Controls](../security/security-controls.md)

## Repository

**GitHub**: [blvm-commons](https://github.com/BTCDecoded/blvm-commons)

## See Also

- [Governance Overview](overview.md) - Governance system introduction
- [OpenTimestamps Integration](opentimestamps-integration.md) - Audit trail system
- [Nostr Integration](nostr-integration.md) - Decentralized communication
- [Security Controls](../security/security-controls.md) - Security validation
- [CI/CD Workflows](../development/ci-cd-workflows.md) - Reusable workflows
