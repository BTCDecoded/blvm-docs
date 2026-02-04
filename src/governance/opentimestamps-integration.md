# OpenTimestamps Integration

## Overview

Bitcoin Commons uses OpenTimestamps (OTS) to anchor governance registries to the Bitcoin blockchain, providing cryptographic proof that governance state existed at specific points in time. This creates immutable historical records that cannot be retroactively modified.

## Purpose

OpenTimestamps integration serves as a temporal proof mechanism by:
- Anchoring governance registries to Bitcoin blockchain
- Providing cryptographic proof of governance state
- Creating immutable historical records
- Enabling verification of governance timeline

## Architecture

### Monthly Registry Anchoring

**Anchoring Schedule**:
- **Frequency**: Monthly on the 1st day of each month
- **Content**: Complete governance registry snapshot
- **Proof**: OpenTimestamps proof anchored to Bitcoin
- **Storage**: Local proof files and public registry

**Code**: [anchor.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/ots/anchor.rs#L1-L77)

### Registry Structure

```json
{
  "version": "YYYY-MM",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "previous_registry_hash": "sha256:abc123...",
  "maintainers": [...],
  "authorized_servers": [...],
  "audit_logs": {...},
  "multisig_config": {...}
}
```

**Code**: [anchor.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/ots/anchor.rs#L27-L37)

## OTS Client

### Client Implementation

The `OtsClient` handles communication with OpenTimestamps calendar servers:

- **Calendar Servers**: Multiple calendar servers for redundancy
- **Hash Submission**: Submits SHA256 hashes for timestamping
- **Proof Generation**: Receives OpenTimestamps proofs
- **Verification**: Verifies proofs against Bitcoin blockchain

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/ots/client.rs#L1-L200)

### Calendar Servers

Default calendar servers:
- `alice.btc.calendar.opentimestamps.org`
- `bob.btc.calendar.opentimestamps.org`

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/ots/client.rs#L25-L33)

## Proof Generation

### OTS Proof Format

- **Format**: Binary OpenTimestamps proof
- **Extension**: `.json.ots` (e.g., `YYYY-MM.json.ots`)
- **Content**: Cryptographic proof of registry existence
- **Verification**: Can be verified against Bitcoin blockchain

### Proof Process

1. **Calculate Hash**: SHA256 hash of registry JSON
2. **Submit to Calendar**: POST hash to OpenTimestamps calendar
3. **Receive Proof**: Calendar returns OTS proof
4. **Store Proof**: Save proof file locally
5. **Publish**: Make proof publicly available

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/ots/client.rs#L42-L59)

## Registry Anchorer

### Monthly Anchoring

The `RegistryAnchorer` creates monthly governance registries:

- **Registry Generation**: Creates complete registry snapshot
- **Hash Chain**: Links to previous registry via hash
- **OTS Stamping**: Submits registry for timestamping
- **Proof Storage**: Stores proofs for verification

**Code**: [anchor.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/ots/anchor.rs#L19-L25)

### Registry Content

Monthly registries include:
- Maintainer information
- Authorized servers
- Audit log summaries
- Multisig configuration
- Previous registry hash (hash chain)

**Code**: [anchor.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/ots/anchor.rs#L27-L77)

## Verification

### Proof Verification

OTS proofs can be verified:

```bash
ots verify YYYY-MM.json.ots
```

**Code**: [verify.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/ots/verify.rs#L1-L51)

### Verification Process

1. **Load Proof**: Read OTS proof file
2. **Verify Structure**: Validate proof format
3. **Check Calendar**: Verify calendar server signatures
4. **Verify Bitcoin**: Check Bitcoin blockchain anchor
5. **Verify Hash**: Confirm hash matches registry

## Integration with Governance

### Audit Trail Anchoring

Audit log entries are anchored via monthly registries:

- **Monthly Snapshots**: Complete audit log state
- **Hash Chain**: Links between monthly registries
- **Immutable History**: Cannot be retroactively modified
- **Public Verification**: Anyone can verify proofs

**Code**: [entry.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/audit/entry.rs#L1-L73)

### Governance State Proof

Monthly registries prove governance state:

- **Maintainer List**: Who had authority at that time
- **Server Authorization**: Which servers were authorized
- **Configuration**: Governance configuration snapshot
- **Timeline**: Historical record of changes

## Configuration

```toml
[ots]
enabled = true
aggregator_url = "https://alice.btc.calendar.opentimestamps.org"
monthly_anchor_day = 1  # Anchor on 1st of each month
registry_path = "./registries"
proofs_path = "./proofs"
```

**Code**: [config.rs](https://github.com/BTCDecoded/blvm-commons/blob/main/src/config.rs#L53-L60)

## Benefits

1. **Immutability**: Proofs anchored to Bitcoin blockchain
2. **Verifiability**: Anyone can verify proofs independently
3. **Historical Record**: Complete timeline of governance state
4. **Tamper-Evident**: Any modification breaks hash chain
5. **Decentralized**: No single point of failure

## Components

The OpenTimestamps integration includes:
- OTS client for calendar communication
- Registry anchorer for monthly anchoring
- Proof verification
- Hash chain maintenance
- Proof storage and publishing

**Location**: `blvm-commons/src/ots/`, `blvm-commons/src/audit/`

