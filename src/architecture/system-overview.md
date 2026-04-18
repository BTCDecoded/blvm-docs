# System Overview

Bitcoin Commons is a Bitcoin implementation ecosystem with six tiers building on the [Orange Paper](../reference/orange-paper.md) mathematical specifications. blvm-consensus and blvm-protocol share the **blvm-primitives** crate for types, serialization, and crypto. The system implements consensus rules directly from the spec, provides protocol abstraction, delivers a full node implementation, and includes a developer SDK.

## 6-Tier Component Architecture

```mermaid
graph TB
    T1[Orange Paper<br/>Mathematical Foundation]
    T2[blvm-consensus<br/>Pure Math Implementation]
    T3[blvm-protocol<br/>Protocol Abstraction]
    T4[blvm-node<br/>Full Node Implementation]
    T5[blvm-sdk<br/>Developer Toolkit]
    T6[blvm-commons<br/>Governance Enforcement]
    
    T1 -->|direct implementation| T2
    T2 -->|protocol abstraction| T3
    T3 -->|full node| T4
    T4 -->|ergonomic API| T5
    T5 -->|cryptographic governance| T6
    
    style T1 fill:#f9f,stroke:#333,stroke-width:2px
    style T2 fill:#bbf,stroke:#333,stroke-width:2px
    style T3 fill:#bfb,stroke:#333,stroke-width:2px
    style T4 fill:#fbf,stroke:#333,stroke-width:2px
    style T5 fill:#ffb,stroke:#333,stroke-width:2px
    style T6 fill:#fbb,stroke:#333,stroke-width:2px
```

## BLVM Stack Architecture

![BLVM Stack Architecture](https://thebitcoincommons.org/assets/images/stack.png)
*Figure: BLVM stack (marketing image): Orange Paper / blvm-spec as the foundation, blvm-consensus with verification tooling, then blvm-protocol, blvm-node, blvm-sdk, and governance enforcement (blvm-commons). The numbered 6-tier diagram above is the canonical layer list.*

## Tiered Architecture

![Tiered Architecture](../images/tier-architecture.png)
*Figure: High-level tiered view (simplified graphic). **Canonical numbering** is the six layers in the mermaid diagram and section headings above (Orange Paper → consensus → protocol → node → SDK → blvm-commons); this image simplifies the stack for layout.*

## Component Overview

### Tier 1: [Orange Paper](../reference/orange-paper.md) (Mathematical Foundation)
- Mathematical specifications for Bitcoin consensus rules
- Source of truth for all implementations
- Timeless, immutable consensus rules

### Tier 2: [blvm-consensus](../consensus/overview.md) (Pure Math Implementation)
- Direct implementation of [Orange Paper](../reference/orange-paper.md) functions
- [Formal proofs](../consensus/formal-verification.md) verify mathematical correctness
- Side-effect-free, deterministic functions
- Consensus-critical dependencies pinned to exact versions

**Code**: [README.md](https://github.com/BTCDecoded/blvm-consensus/blob/main/README.md)

### Tier 3: [blvm-protocol](../protocol/overview.md) (Protocol Abstraction)
- Bitcoin protocol abstraction for multiple variants
- Supports mainnet, testnet, regtest
- Commons-specific protocol extensions ([UTXO commitments](../consensus/utxo-commitments.md), ban list sharing)
- BIP implementations (BIP152, BIP157, BIP158, BIP173/350/351)

**Code**: [README.md](https://github.com/BTCDecoded/blvm-protocol/blob/main/README.md)

### Tier 4: [blvm-node](../node/overview.md) (Node Implementation)
- Reference full node (non-consensus infrastructure: storage, P2P, RPC, modules); operational hardening required for real deployments
- [Storage layer](../node/storage-backends.md) (database abstraction with multiple backends)
- Network manager ([multi-transport](../node/transport-abstraction.md): TCP, QUIC, Iroh)
- [RPC server](../node/rpc-api.md) (JSON-RPC 2.0, conventional Bitcoin RPC surface)
- [Module system](../architecture/module-system.md) (process-isolated runtime modules)
- Payment processing with CTV (CheckTemplateVerify) support
- RBF and mempool policies (4 configurable modes)
- Advanced indexing (address and value range indexing)
- [Mining coordination](../node/mining-stratum-v2.md) (Stratum V2, merge mining)
- P2P governance message relay
- Governance integration (webhooks, user signaling)
- ZeroMQ notifications (optional)

**Code**: [README.md](https://github.com/BTCDecoded/blvm-node/blob/main/README.md)

### Tier 5: [blvm-sdk](../sdk/overview.md) (Developer Toolkit)
- Governance primitives (key management, signatures, [multisig](../governance/multisig-configuration.md))
- CLI tools (blvm-keygen, blvm-sign, blvm-verify)
- [Composition framework](../architecture/module-system.md) (declarative node composition)
- Bitcoin-compatible signing standards

**Code**: [README.md](https://github.com/BTCDecoded/blvm-sdk/blob/main/README.md)

### Tier 6: blvm-commons (Governance Enforcement)
- GitHub App for governance enforcement
- Cryptographic signature verification
- Multisig threshold enforcement
- Audit trail management
- OpenTimestamps integration

## Data Flow

1. **Orange Paper** provides mathematical consensus specifications
2. **blvm-consensus** directly implements mathematical functions
3. **blvm-protocol** layers protocol parameters and network behavior on **blvm-consensus** types and validation
4. **blvm-node** uses blvm-protocol and blvm-consensus for validation
5. **blvm-sdk** provides governance primitives
6. **blvm-commons** uses **blvm-sdk** and **blvm-protocol** for governance enforcement and shared types

## Cross-Layer Validation

- Dependencies between layers are strictly enforced in the **crate graph** (application layers do not reimplement consensus).
- Consensus rule modifications are prevented in application layers by design (validation calls into **blvm-consensus**).
- The [Orange Paper](../reference/orange-paper.md) is the specification; **blvm-consensus** is checked with [formal verification](../consensus/formal-verification.md), tests, and review—not a single proof of the entire spec in one step.
- Version coordination (Cargo / release sets) keeps compatible crate versions together.

## Key Features

### Mathematical Rigor
- Direct implementation of [Orange Paper](../reference/orange-paper.md) specifications
- [Formal verification](../consensus/formal-verification.md) with [BLVM Specification Lock](../consensus/formal-verification.md)
- [Property-based testing](../development/property-based-testing.md) for mathematical invariants
- [Formal proofs](../consensus/formal-verification.md) verify critical consensus functions

### Protocol Abstraction
- Multiple Bitcoin variants (mainnet, testnet, regtest)
- Commons-specific protocol extensions
- BIP implementations (BIP152, BIP157, BIP158)
- Protocol evolution support

### Node and operational features
- Full Bitcoin node–style functionality (when configured and secured appropriately)
- [Performance optimizations](../node/performance.md) (PGO, parallel validation)
- [Multiple storage backends](../node/storage-backends.md) with automatic fallback
- [Multi-transport networking](../node/transport-abstraction.md) (TCP, QUIC, Iroh)
- Payment processing infrastructure
- REST API alongside [JSON-RPC](../node/rpc-api.md)

### Governance Infrastructure
- [Cryptographic governance primitives](../governance/overview.md)
- [Multisig threshold enforcement](../governance/multisig-configuration.md)
- [Transparent audit trails](../governance/audit-trails.md)
- [Forkable governance rules](../governance/governance-fork.md)

## See Also

- [Component Relationships](component-relationships.md) - Detailed component interactions
- [Design Philosophy](design-philosophy.md) - Core design principles
- [Module System](module-system.md) - Module system architecture
- [Node Overview](../node/overview.md) - Node implementation details
- [Consensus Overview](../consensus/overview.md) - Consensus layer details
- [Protocol Overview](../protocol/overview.md) - Protocol layer details

