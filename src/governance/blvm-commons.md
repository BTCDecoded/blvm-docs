# blvm-commons

## Overview

blvm-commons is the governance tooling crate for Bitcoin Commons. It contains GitHub, OpenTimestamps, and Nostr clients. Merge enforcement is off.

## Key Features

- **GitHub Integration**: App client for signature checks. `set_required_status_checks` sends `enforce_admins: false`. A failed branch-protection response is logged and returned as success.
- **OpenTimestamps**: Calendar client for governance artifacts. Designed to anchor those artifacts to Bitcoin. Not a step in consensus CI today.
- **Nostr Integration**: Relay client for governance messages
- **Cross-Layer Validation**: Security-control checks in the crate
- **CI/CD Workflows**: Reusable workflows for Bitcoin Commons repositories

## Components

### GitHub Integration

The GitHub App code can post checks and call the branch-protection API. It does not block a merge by itself. Admin enforcement is off, and a rejected protection update does not fail the caller. `set_required_status_checks` sends `enforce_admins: false`. See `blvm-commons/src/github/client.rs`. That is what is Built. Enforcement is off today.

The design, once Phase 2 begins, is a quorum of governance nodes. Governance bots hold administrator access. Human repository administrators are shut out of governance-relevant actions. An action that does not conform, including an action by a human administrator, is reversed by the bots. Two of three nodes in a written set must each conclude that an action, or a reversal, conforms before it stands. Anyone may run a node and publish a conclusion. Only the written set binds. A node applies a host action only after two of the three have published the same conclusion. Credentials that can install or remove the app are held by that quorum. A standing personal owner account is not part of the design. The company that operates the host can still override the organization. Operators accept a release only when the required maintainer signatures attest to it and the build is reproducible. A merge that lacks those signatures does not become a signed release. The nodes check signatures, thresholds, periods, tier classification, and the presence of a required record. An AI flag is evidence. It is not that check. This paragraph is Designed. It is not Running.


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
