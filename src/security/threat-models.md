# Threat Models

## Overview

Bitcoin Commons implements security boundaries and threat models to protect against various attack vectors. The system uses defense-in-depth principles with multiple layers of security.

## Security Boundaries

### Node Security Boundaries

**What bllvm-node Handles**:
- Consensus validation (delegated to bllvm-consensus)
- Network protocol (P2P message parsing, peer management)
- Storage layer (block storage, UTXO set, chain state)
- RPC interface (JSON-RPC 2.0 API)
- Module orchestration (loading, IPC, lifecycle management)
- Mempool management
- Mining coordination

**What bllvm-node NEVER Handles**:
- Consensus rule validation (delegated to bllvm-consensus)
- Protocol variant selection (delegated to bllvm-protocol)
- Private key management (no wallet functionality)
- Cryptographic key generation (delegated to bllvm-sdk or modules)
- Governance enforcement (delegated to bllvm-commons)

**Code**: ```11:28:bllvm-node/SECURITY.md```

### Module System Security Boundaries

**Process Isolation**:
- Modules run in separate processes with isolated memory
- Node consensus state is protected and read-only to modules
- Module crashes are isolated and do not affect the base node

**Code**: ```115:142:bllvm-node/docs/MODULE_SYSTEM.md```

**What Modules Cannot Do**:
- Modify consensus rules
- Modify UTXO set
- Access node private keys
- Bypass security boundaries
- Affect other modules

**Code**: ```334:341:bllvm-node/docs/MODULE_SYSTEM.md```

## Threat Model: Pre-Production Testing

### Environment

- **Network**: Trusted network only
- **Timeline**: 6-12 months testing phase
- **Threats**: Limited to development and testing scenarios

### Threats NOT Applicable (Trusted Network)

- Eclipse attacks
- Sybil attacks
- Network partitioning attacks
- Malicious peer injection

**Code**: ```79:91:bllvm-node/SECURITY.md```

### Threats That Apply

- **Code vulnerabilities** in consensus validation
- **Memory corruption** in parsing
- **Integer overflow** in calculations
- **Resource exhaustion** (DoS)
- **Supply chain attacks** on dependencies

**Code**: ```92:98:bllvm-node/SECURITY.md```

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

**Code**: ```99:112:bllvm-node/SECURITY.md```

## Attack Vectors

### Eclipse Attacks

**Threat**: Malicious peers isolate node from honest network

**Mitigations**:
- IP diversity tracking
- Limits connections from same IP range
- Geographic diversity requirements
- ASN diversity tracking

**Code**: ```156:156:bllvm-node/SECURITY.md```

### Sybil Attacks

**Threat**: Attacker creates many fake peer identities

**Mitigations**:
- Connection rate limiting
- Per-IP connection limits
- Peer reputation tracking
- Ban list sharing

**Code**: ```125:127:bllvm-node/SECURITY.md```

### Resource Exhaustion (DoS)

**Threat**: Attacker exhausts node resources (memory, CPU, network)

**Mitigations**:
- Connection rate limiting (token bucket)
- Message queue limits
- Auto-ban for abusive peers
- Resource monitoring
- Per-user RPC rate limiting

**Code**: ```125:127:bllvm-node/SECURITY.md```

### Protocol Manipulation

**Threat**: Attacker sends malformed messages to exploit parsing bugs

**Mitigations**:
- Input validation and sanitization
- Fuzzing (19 fuzz targets)
- Formal verification (201 Kani proofs)
- Property-based testing (141 property tests)
- Network protocol validation

**Code**: ```134:138:bllvm-node/SECURITY.md```

### Memory Corruption

**Threat**: Buffer overflows, use-after-free, double-free

**Mitigations**:
- Rust memory safety
- MIRI integration (undefined behavior detection)
- Fuzzing with sanitizers (ASAN, UBSAN, MSAN)
- Runtime assertions (913 assertions)

**Code**: ```167:170:bllvm-consensus/docs/CONSENSUS_COVERAGE_ASSESSMENT.md```

### Integer Overflow

**Threat**: Integer overflow in calculations causing consensus divergence

**Mitigations**:
- Checked arithmetic
- Formal verification (Kani proofs)
- Property-based testing
- Runtime assertions

**Code**: ```156:160:bllvm-consensus/docs/CONSENSUS_COVERAGE_ASSESSMENT.md```

### Supply Chain Attacks

**Threat**: Malicious dependencies compromise node

**Mitigations**:
- Dependency pinning (exact versions)
- Regular security audits (cargo audit)
- Minimal dependency set
- Trusted dependency sources

**Code**: ```136:137:bllvm-node/SECURITY.md```

## Security Hardening

### Phase 1: Pre-Production (Current)

- ✅ Fix signature verification with real transaction hashes
- ✅ Implement proper Bitcoin double SHA256 hashing
- ✅ Pin all dependencies to exact versions
- ✅ Add network protocol input validation
- ✅ Replace sled with redb (production-ready database)
- ✅ Add DoS protection mechanisms
- ✅ Add RPC authentication
- ✅ Implement rate limiting
- ✅ Add comprehensive fuzzing
- ✅ Add eclipse attack prevention
- ✅ Add storage bounds checking

**Code**: ```142:158:bllvm-node/SECURITY.md```

### Phase 2: Production Readiness

- ✅ All Phase 1 items completed
- ⏳ Professional security audit (external, requires security firm)
- ✅ Formal verification of critical paths
- ✅ Advanced peer management

**Code**: ```159:162:bllvm-node/SECURITY.md```

## Module System Security

### Process Isolation

Modules run in separate processes:

- **Isolated Memory**: Each module has separate memory space
- **IPC Communication**: Modules communicate only via IPC
- **Crash Isolation**: Module crashes don't affect node
- **Resource Limits**: CPU, memory, and network limits enforced

**Code**: ```1:13:bllvm-node/src/module/mod.rs```

### Sandboxing

Modules are sandboxed:

- **File System**: Restricted file system access
- **Network**: Network access controlled
- **Process**: Resource limits enforced
- **Capabilities**: Permission-based access control

**Code**: ```1:12:bllvm-node/src/module/sandbox/mod.rs```

### Permission System

Modules require explicit permissions:

- **Capability Checks**: Permission validator checks capabilities
- **Tier Validation**: Tier-based permission system
- **Resource Limits**: Enforced resource limits
- **Request Validation**: All requests validated

**Code**: ```317:325:bllvm-node/docs/MODULE_SYSTEM.md```

## RPC Security

### Authentication

RPC authentication implemented:

- **Token-Based**: Token-based authentication
- **Certificate-Based**: Certificate-based authentication
- **Configurable**: Authentication method configurable

**Code**: ```129:132:bllvm-node/SECURITY.md```

### Rate Limiting

RPC rate limiting implemented:

- **Per-User**: Per-user rate limiting
- **Token Bucket**: Token bucket algorithm
- **Configurable**: Rate limits configurable

**Code**: ```130:130:bllvm-node/SECURITY.md```

### Input Validation

RPC input validation:

- **Sanitization**: Input sanitization
- **Validation**: Input validation
- **Access Control**: Access control via authentication

**Code**: ```131:132:bllvm-node/SECURITY.md```

## Network Security

### DoS Protection

DoS protection mechanisms:

- **Connection Rate Limiting**: Token bucket, per-IP connection limits
- **Message Queue Limits**: Limits on message queue size
- **Auto-Ban**: Automatic banning of abusive peers
- **Resource Monitoring**: Resource usage monitoring

**Code**: ```125:127:bllvm-node/SECURITY.md```

### Eclipse Attack Prevention

Eclipse attack prevention:

- **IP Diversity Tracking**: Tracks IP diversity
- **Subnet Limits**: Limits connections from same IP range
- **Geographic Diversity**: Geographic diversity requirements
- **ASN Diversity**: ASN diversity tracking

**Code**: ```156:156:bllvm-node/SECURITY.md```

## Storage Security

### Database Security

Storage layer security:

- **redb Default**: Production-ready database (pure Rust, ACID)
- **sled Fallback**: Available as fallback (beta quality)
- **Database Abstraction**: Allows switching backends
- **Storage Bounds**: Storage bounds checking

**Code**: ```117:121:bllvm-node/SECURITY.md```

## See Also

- [Security Controls](security-controls.md) - Security control implementation
- [Developer Security Checklist](DEVELOPER_SECURITY_CHECKLIST.md) - Security checklist for developers
- [Security Architecture Review Template](ARCHITECTURE_REVIEW_TEMPLATE.md) - Architecture review process
- [Security Testing Template](SECURITY_TESTING_TEMPLATE.md) - Security testing guidelines
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

**Location**: `bllvm-node/SECURITY.md`, `bllvm-node/src/module/`, `bllvm-node/docs/MODULE_SYSTEM.md`

