# blvm-commons

## Overview

blvm-commons is the governance app for Bitcoin Commons. It contains the GitHub App, an OpenTimestamps client, a Nostr client, and cross-layer checks.

## Key Features

- **GitHub Integration**: GitHub App for signature checks and review periods
- **OpenTimestamps**: Timestamp client for governance artifacts
- **Nostr Integration**: Relay client for governance messages
- **Cross-Layer Validation**: Security controls and validation across all layers
- **CI/CD Workflows**: Reusable workflows for Bitcoin Commons repositories

## Components

### GitHub Integration

The GitHub App checks signatures and review periods against the published schedule.


### OpenTimestamps Integration

Submits governance artifacts to OpenTimestamps calendars.


### Nostr Integration

Publishes governance messages to Nostr relays.


### Security Controls

Validates code changes, detects placeholder implementations, and enforces security policies across all Bitcoin Commons repositories.

**Documentation:** [PR security control classification](../development/security-controls.md)

## Repository

**GitHub**: [blvm-commons](https://github.com/BTCDecoded/blvm-commons)

## Source

- [GitHub App](https://github.com/BTCDecoded/blvm-commons)
- [OpenTimestamps Integration](opentimestamps-integration.md)
- [Nostr Integration](nostr-integration.md)
## See Also

- [Governance Overview](overview.md) - Governance system introduction
- [OpenTimestamps Integration](opentimestamps-integration.md) - Audit trail system
- [Nostr Integration](nostr-integration.md) - Decentralized communication
- [PR security control classification](../development/security-controls.md) - Security validation
- [CI/CD Workflows](../development/ci-cd-workflows.md) - Reusable workflows
