# Threat Models

## Overview

Bitcoin Commons implements security boundaries and threat models to protect against various attack vectors. The system uses defense-in-depth principles with multiple layers of security.

**Operator-facing maturity language** (required / recommended / unsupported for deployments) lives in **[Deployment posture](deployment-posture.md)** — use that page for bind addresses, RPC exposure, and QUIC × auth limitations.

## Security Boundaries

### Node Security Boundaries

**What blvm-node Handles**:
- Consensus validation (delegated to blvm-consensus)
- Network protocol (P2P message parsing, peer management)
- Storage layer (block storage, UTXO set, chain state)
- RPC interface (JSON-RPC 2.0 API)
- Module orchestration (loading, IPC, lifecycle management)
- Mempool management
- Mining coordination

**What blvm-node NEVER Handles**:
- Consensus rule validation (delegated to blvm-consensus)
- Protocol variant selection (delegated to blvm-protocol)
- Private key management (no wallet functionality)
- Cryptographic key generation (delegated to blvm-sdk or modules)
- Governance enforcement (delegated to blvm-commons)

**Consensus validation and timing:** `blvm-consensus` **verifies** signatures and scripts on **public** block data only—variable-time verify paths are appropriate. It does **not** sign or hold private keys. Secret-path **constant-time** signing lives in **`blvm-secp256k1`** ([TIMING.md](https://github.com/BTCDecoded/blvm-secp256k1/blob/main/TIMING.md)); governance signing in **blvm-sdk** delegates there. Spec-lock ([Formal Verification](../consensus/formal-verification.md)) checks consensus **conformance**, not side-channels.


### Module System Security Boundaries

**Process Isolation**:
- Modules run in separate processes with isolated memory
- Node consensus state is protected and read-only to modules
- Module crashes are isolated and do not affect the base node


**What Modules Cannot Do**:
- Modify consensus rules
- Modify UTXO set
- Access node private keys
- Bypass security boundaries
- Affect other modules


## Threat Model: Pre-Production Testing

Operator-facing maturity: **[Deployment posture](deployment-posture.md)** (published: [docs.thebitcoincommons.org](https://docs.thebitcoincommons.org/security/deployment-posture.html)).

### Environment

- **Network**: Trusted network only
- **Timeline**: Extended testing before production use
- **Threats**: Limited to development and testing scenarios

### Threats NOT Applicable (Trusted Network)

- Eclipse attacks
- Sybil attacks
- Network partitioning attacks
- Malicious peer injection


### Threats That Apply

- **Code vulnerabilities** in consensus validation
- **Memory corruption** in parsing
- **Integer overflow** in calculations
- **Resource exhaustion** (DoS)
- **Supply chain attacks** on dependencies


## Threat Model: Mainnet Deployment

### Environment

- **Network**: Public Bitcoin network
- **Timeline**: After security audit and hardening
- **Threats**: Full Bitcoin network threat model

### Additional Threats for Mainnet

- **Eclipse attacks** - malicious peers isolate node
- **Sybil attacks** - fake peer identities
- **Network partitioning** - routing attacks
- **Resource exhaustion** - memory/CPU DoS
- **Protocol manipulation** - malformed messages


## Attack Vectors

### Eclipse Attacks

**Threat**: Malicious peers isolate node from honest network

**Mitigations**:
- IP diversity tracking
- Limits connections from same IP range
- LAN peering security: 25% LAN peer cap, 75% internet peer minimum, checkpoint validation
- Geographic diversity requirements
- ASN diversity tracking


### Sybil Attacks

**Threat**: Attacker creates many fake peer identities

**Mitigations**:
- Connection rate limiting
- Per-IP connection limits
- Peer reputation tracking
- Ban list sharing


### Resource Exhaustion (DoS)

**Threat**: Attacker exhausts node resources (memory, CPU, network)

**Mitigations**:
- Connection rate limiting (token bucket)
- Message queue limits
- Auto-ban for abusive peers
- Resource monitoring
- Per-user RPC rate limiting


### Protocol Manipulation

**Threat**: Attacker sends malformed messages to exploit parsing bugs

**Mitigations**:
- Input validation and sanitization
- Fuzzing ([overview](../development/testing.md#fuzzing))
- Formal verification
- Property-based testing
- Network protocol validation


### Memory Corruption

**Threat**: Buffer overflows, use-after-free, double-free

**Mitigations**:
- Rust memory safety
- MIRI integration (undefined behavior detection)
- Fuzzing with sanitizers (ASAN, UBSAN, MSAN)
- Runtime assertions


### Integer Overflow

**Threat**: Integer overflow in calculations causing consensus divergence

**Mitigations**:
- Checked arithmetic
- Formal verification (Z3 proofs via BLVM Specification Lock)
- Property-based testing
- Runtime assertions


### Supply Chain Attacks

**Threat**: Malicious dependencies compromise node

**Mitigations**:
- **Version constraints** and lockfiles as defined per repository (`Cargo.toml`; use **`--locked`** when a lockfile is part of that project’s workflow)
- Regular security audits (cargo audit)
- Minimal dependency set
- Trusted dependency sources


## Security Hardening

### Pre-Production (Current)

- Fix signature verification with real transaction hashes
- Implement proper Bitcoin double SHA256 hashing
- Review **Cargo.toml** dependency constraints and run **`cargo audit`**
- Add network protocol input validation
- Prefer **`database_backend = "auto"`** with supported backends over ad-hoc defaults; use **redb** when omitting RocksDB/heed3 for pure-Rust minimal builds
- Add DoS protection mechanisms
- Add RPC authentication
- Implement rate limiting
- Add fuzzing
- Add eclipse attack prevention
- Add storage bounds checking


### Production Readiness

- All pre-production items completed
- Professional security audit (external, requires security firm)
- Formal verification of critical paths
- Advanced peer management


## Module System Security

### Process Isolation

Modules run in separate processes:

- **Isolated Memory**: Each module has separate memory space
- **IPC Communication**: Modules communicate only via IPC
- **Crash Isolation**: Module crashes don't affect node
- **Resource Limits**: CPU, memory, and network limits enforced


### Sandboxing

Modules are sandboxed:

- **File System**: Restricted file system access
- **Network**: Network access controlled
- **Process**: Resource limits enforced
- **Capabilities**: Permission-based access control


### Permission System

Modules require explicit permissions:

- **Capability Checks**: Permission validator checks capabilities
- **Tier Validation**: Tier-based permission system
- **Resource Limits**: Enforced resource limits
- **Request Validation**: All requests validated


## RPC Security

### Authentication

RPC authentication implemented:

- **Token-Based**: Token-based authentication
- **Certificate-Based**: Certificate-based authentication
- **Configurable**: Authentication method configurable


### Rate Limiting

RPC rate limiting implemented:

- **Per-User**: Per-user rate limiting
- **Token Bucket**: Token bucket algorithm
- **Configurable**: Rate limits configurable


### Input Validation

RPC input validation:

- **Sanitization**: Input sanitization
- **Validation**: Input validation
- **Access Control**: Access control via authentication


## Network Security

### DoS Protection

DoS protection mechanisms:

- **Connection Rate Limiting**: Token bucket, per-IP connection limits
- **Message Queue Limits**: Limits on message queue size
- **Auto-Ban**: Automatic banning of abusive peers
- **Resource Monitoring**: Resource usage monitoring


### Eclipse Attack Prevention

Eclipse attack prevention:

- **IP Diversity Tracking**: Tracks IP diversity
- **Subnet Limits**: Limits connections from same IP range
- **Geographic Diversity**: Geographic diversity requirements
- **ASN Diversity**: ASN diversity tracking


## Storage Security

### Database Security

Storage layer security:

- **`auto` / heed3**: Default path in typical builds (mmap UTXO reads + rkyv); **`rocksdb`**: explicit choice or fallback (performance + Core layout interop; see storage docs)
- **redb / sled / tidesdb**: Alternative backends with different trust and build surfaces; **redb** is pure Rust when RocksDB is not used
- **Database Abstraction**: Allows switching backends explicitly
- **Storage Bounds**: Storage bounds checking


## LAN Peering Security

The LAN peering system includes multiple security mechanisms to prevent eclipse attacks while allowing fast local network sync:

### Security Limits

- **25% LAN Peer Cap**: Maximum percentage of peers that can be LAN peers (hard limit)
- **75% Internet Peer Minimum**: Minimum percentage of peers that must be internet peers
- **Minimum 3 Internet Peers**: Required for checkpoint validation consensus
- **Maximum 1 Discovered LAN Peer**: Limits automatically discovered peers (whitelisted are separate)


### Checkpoint Validation

Internet checkpoints are the **primary security mechanism** for LAN peering:

- **Block Checkpoints**: Every 1000 blocks, validate block hash against internet peers
- **Header Checkpoints**: Every 10000 blocks, validate header hash against internet peers
- **Consensus Requirement**: Requires agreement from at least 3 internet peers
- **Failure Response**: Checkpoint failure results in permanent ban (1 year duration)


### Progressive Trust System

LAN peers start with limited trust and earn higher priority over time:

- **Initial Trust**: 1.5x multiplier for newly discovered peers
- **Level 2 Trust**: 2.0x multiplier after 1000 valid blocks
- **Maximum Trust**: 3.0x multiplier after 10000 blocks AND 1 hour connection
- **Demotion**: After 3 failures, peer loses LAN status
- **Banning**: Checkpoint failure results in permanent ban


### Eclipse Attack Prevention

The security model ensures eclipse attack prevention:

1. **Internet Peer Majority**: 75% minimum ensures connection to honest network
2. **Checkpoint Validation**: Regular validation prevents chain divergence
3. **LAN Address Privacy**: LAN addresses never advertised to external peers
4. **Failure Handling**: Multiple failures result in demotion or ban


For complete documentation, see [LAN Peering System](../node/lan-peering.md).

## Source

- [SECURITY.md](https://github.com/BTCDecoded/blvm-node/blob/main/SECURITY.md)
- [MODULE_SYSTEM.md](https://github.com/BTCDecoded/blvm-node/blob/main/docs/MODULE_SYSTEM.md)
- [PROOF_LIMITATIONS.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/docs/PROOF_LIMITATIONS.md)
- [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/mod.rs)
- [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/module/sandbox/mod.rs)
- [lan_security.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/lan_security.rs)
- [SECURITY.md](https://github.com/BTCDecoded/blvm-node/blob/main/SECURITY.md)
- [module/](https://github.com/BTCDecoded/blvm-node/tree/main/src/module/)
## See Also

- [LAN Peering System](../node/lan-peering.md) - Complete LAN peering documentation
- [PR security control classification](../development/security-controls.md) - Automated PR classification (contributors)
- [Developer Security Checklist](../appendices/templates/DEVELOPER_SECURITY_CHECKLIST.md) - Security checklist for developers
- [Security Architecture Review Template](../appendices/templates/ARCHITECTURE_REVIEW_TEMPLATE.md) - Architecture review process
- [Security Testing Template](../appendices/templates/SECURITY_TESTING_TEMPLATE.md) - Security testing guidelines
- [Node Overview](../node/overview.md) - Node security features
- [Contributing](../development/contributing.md) - Security in development workflow
## Components

The threat model and security boundaries include:
- Node security boundaries (what node handles vs. never handles)
- Module system security (process isolation, sandboxing)
- Threat models (pre-production, mainnet)
- Attack vectors and mitigations
- Security hardening roadmap
- RPC security (authentication, rate limiting)
- Network security (DoS protection, eclipse prevention)
- Storage security
