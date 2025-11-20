# Component Relationships

BLLVM implements a 6-tier layered architecture where each tier builds upon the previous one.

## Dependency Graph

```
bllvm-consensus (no dependencies)
    ↓
bllvm-protocol (depends on bllvm-consensus)
    ↓
bllvm-node (depends on bllvm-protocol + bllvm-consensus)

bllvm-sdk (no dependencies)
    ↓
bllvm-commons (depends on bllvm-sdk)
```

## Layer Descriptions

### Tier 1: Orange Paper (bllvm-spec)
- **Purpose**: Mathematical foundation - timeless consensus rules
- **Type**: Documentation and specification
- **Governance**: Layer 1 (Constitutional - 6-of-7 maintainers, 180 days)

### Tier 2: Consensus Proof (bllvm-consensus)
- **Purpose**: Pure mathematical implementation of Orange Paper functions
- **Type**: Rust library (pure functions, no side effects)
- **Dependencies**: None (foundation layer)
- **Governance**: Layer 2 (Constitutional - 6-of-7 maintainers, 180 days)
- **Key Functions**: CheckTransaction, ConnectBlock, EvalScript, VerifyScript

### Tier 3: Protocol Engine (bllvm-protocol)
- **Purpose**: Protocol abstraction layer enabling multiple Bitcoin variants
- **Type**: Rust library
- **Dependencies**: bllvm-consensus (exact version)
- **Governance**: Layer 3 (Implementation - 4-of-5 maintainers, 90 days)
- **Supports**: mainnet, testnet, regtest, and future protocol variants

### Tier 4: Reference Node (bllvm-node)
- **Purpose**: Minimal, production-ready Bitcoin implementation
- **Type**: Rust binaries (full node)
- **Dependencies**: bllvm-protocol, bllvm-consensus (exact versions)
- **Governance**: Layer 4 (Application - 3-of-5 maintainers, 60 days)
- **Components**: Block validation, storage (sled), P2P networking, RPC, mining

### Tier 5: Developer SDK (bllvm-sdk)
- **Purpose**: Developer toolkit and governance cryptographic primitives
- **Type**: Rust library and CLI tools
- **Dependencies**: Standalone (no consensus dependencies)
- **Governance**: Layer 5 (Extension - 2-of-3 maintainers, 14 days)
- **Components**: Key generation, signing, verification, multisig operations

### Tier 6: Governance Infrastructure (bllvm-commons)
- **Purpose**: Cryptographic governance enforcement
- **Type**: Rust service (GitHub App)
- **Dependencies**: bllvm-sdk
- **Governance**: Layer 5 (Extension - 2-of-3 maintainers, 14 days)
- **Components**: GitHub integration, signature verification, status checks

## Data Flow

![How the Stack Works](../images/how-the-stack-works-in-practice.png)
*Figure: End-to-end data flow through Reference Node, Consensus Proof, Protocol Engine, modules, and governance.*

1. **Orange Paper** provides mathematical consensus specifications
2. **bllvm-consensus** directly implements mathematical functions
3. **bllvm-protocol** wraps bllvm-consensus with protocol-specific parameters
4. **bllvm-node** uses bllvm-protocol and bllvm-consensus for validation
5. **bllvm-sdk** provides governance primitives
6. **bllvm-commons** uses bllvm-sdk for cryptographic operations

## Cross-Layer Validation

- Dependencies between layers are strictly enforced
- Consensus rule modifications are prevented in application layers
- Equivalence proofs required between Orange Paper and bllvm-consensus
- Version coordination ensures compatibility across layers

## See Also

- [System Overview](system-overview.md) - High-level architecture overview
- [Design Philosophy](design-philosophy.md) - Core design principles
- [Consensus Architecture](../consensus/architecture.md) - Consensus layer details
- [Protocol Architecture](../protocol/architecture.md) - Protocol layer details
- [Node Overview](../node/overview.md) - Node implementation details

