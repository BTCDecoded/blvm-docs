# blvm-commons

## Overview

blvm-commons is the governance tooling crate for Bitcoin Commons. It contains GitHub, OpenTimestamps, and Nostr clients. Merge enforcement is off.

## Key Features

- **GitHub Integration**: App client for signature checks. `set_required_status_checks` sends `enforce_admins: false`. A failed branch-protection response is logged and returned as success.
- **OpenTimestamps**: Calendar client for governance artifacts. It is not a step in consensus CI.
- **Nostr Integration**: Relay client for governance messages
- **Cross-Layer Validation**: Security-control checks in the crate
- **CI/CD Workflows**: Reusable workflows for Bitcoin Commons repositories

## Components

### GitHub Integration

The GitHub App code can post checks and call the branch-protection API. It does not block a merge by itself. Admin enforcement is off, and a rejected protection update does not fail the caller. See `blvm-commons/src/github/client.rs`.


### OpenTimestamps Integration

`OtsClient` in `src/ots/anchor.rs` can submit a hash to the calendars this build allows (alice and bob). That call is separate from consensus CI and from merge enforcement.


### Nostr Integration

Enables decentralized governance communication, voting, and proposal distribution through Nostr relays.


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
