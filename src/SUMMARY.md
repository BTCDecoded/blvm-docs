# Summary

[Introduction](introduction.md)

# Getting Started

- [Installation](getting-started/installation.md)
- [Quick Start](getting-started/quick-start.md)
- [Operator guide](getting-started/operator-guide.md)
- [Developer guide](getting-started/developer-guide.md)
- [First Node Setup (regtest)](getting-started/first-node.md)
- [Mainnet initial sync](getting-started/mainnet-sync.md)
- [Building your first module](getting-started/first-module.md)

# Running a node

- [Node Operations](node/operations.md)
- [Node configuration guide](node/configuration.md)
- [RPC API Reference](node/rpc-api.md)
- [Storage Backends](node/storage-backends.md)
- [Transaction Indexing](node/transaction-indexing.md)
- [IBD Bandwidth Protection](node/ibd-protection.md)
- [IBD UTXO engine](node/ibd-engine.md)
- [UTXO Commitments](node/utxo-commitments.md)
- [Peer Consensus Protocol](node/peer-consensus.md)
- [Spam Filtering](node/spam-filtering.md)
- [LAN Peering System](node/lan-peering.md)
- [RBF and Mempool Policies](node/rbf-mempool-policies.md)
- [Transaction relay](node/privacy-relay.md)
- [Package Relay (BIP331)](node/package-relay.md)
- [Performance Optimizations](node/performance.md)
- [QUIC RPC](node/quic-rpc.md)
- [Mining Integration](node/mining.md)
- [Stratum V2 + Merge Mining](node/mining-stratum-v2.md)
- [Transport abstraction](node/transport-abstraction.md)
- [Node overview](node/overview.md)

# Security

- [Deployment posture](security/deployment-posture.md)
- [RPC transport × authentication](security/rpc-transport-auth-matrix.md)
- [Threat Models](security/threat-models.md)

# Building on BLVM

## Developer SDK

- [Overview](sdk/overview.md)
- [Building modules](sdk/module-development.md)
- [API Reference](sdk/api-reference.md)
- [Examples](sdk/examples.md)

## Modules

- [Module catalog](modules/overview.md)
- [Lightning Network Module](modules/lightning.md)
- [Commons Mesh Module](modules/mesh.md)
- [Stratum V2 Module](modules/stratum-v2.md)
- [Datum Module](modules/datum.md)
- [Mining OS Module](modules/miningos.md)
- [Selective Sync Module](modules/selective-sync.md)
- [FIBRE Module](modules/fibre.md)
- [ZMQ Module](modules/zmq.md)
- [Miniscript Module](modules/miniscript.md)
- [Governance Module](modules/governance-module.md)
- [Marketplace Module](modules/marketplace-module.md)

# Architecture

- [Stack overview](architecture/system-overview.md)
- [Crate dependencies](architecture/component-relationships.md)
- [Design Philosophy](architecture/design-philosophy.md)
- [Module system (design)](architecture/module-system.md)
- [Module IPC Protocol](architecture/module-ipc-protocol.md)
- [Module events](architecture/module-events.md)
- [Janitorial events](architecture/janitorial-events.md)

# Consensus Layer

- [Overview](consensus/overview.md)
- [Architecture](consensus/architecture.md)
- [Formal Verification](consensus/formal-verification.md)
- [Mathematical Specifications](consensus/mathematical-specifications.md)

# Protocol Layer

- [Overview](protocol/overview.md)
- [Architecture](protocol/architecture.md)
- [Message Formats](protocol/message-formats.md)
- [Network Protocol](protocol/network-protocol.md)

# Governance

- [Overview](governance/overview.md)
- [Review standards](governance/review-standards.md)
- [blvm-commons](governance/blvm-commons.md)
- [Governance Model](governance/governance-model.md)
- [Governance layers and tiers](governance/layer-tier-model.md)
- [Governance configuration](governance/configuration-system.md)
- [Governance Fork System](governance/governance-fork.md)
- [P2P Governance Messages](governance/p2p-governance-messages.md)
- [OpenTimestamps Integration](governance/opentimestamps-integration.md)
- [Nostr Integration](governance/nostr-integration.md)
- [Multisig Configuration](governance/multisig-configuration.md)
- [Keyholder Procedures](governance/keyholder-procedures.md)
- [Audit Trails](governance/audit-trails.md)

# Reference

- [Orange Paper](reference/orange-paper.md)
- [Protocol Specifications](reference/protocol-specifications.md)
- [Configuration Reference](reference/configuration-reference.md)
- [JSON-RPC error reference](reference/rpc-errors.md)
- [API Index](reference/api-index.md)
- [Glossary](reference/glossary.md)

# Development

## Contributing

- [Contributing](development/contributing.md)
- [PR security control classification](development/security-controls.md)
- [Repository layout](development/repository-architecture.md)
- [Rust MSRV vs CI toolchains](development/msrv-note.md)
- [CI/CD Workflows](development/ci-cd-workflows.md)
- [PR Process](development/pr-process.md)
- [Release Process](development/release-process.md)

## Testing

- [Testing Infrastructure](development/testing.md)
- [Fuzzing Infrastructure](development/fuzzing.md)
- [Property-Based Testing](development/property-based-testing.md)
- [Benchmarking](development/benchmarking.md)
- [Differential Testing](development/differential-testing.md)
- [Snapshot Testing](development/snapshot-testing.md)

# Appendices

- [RBF Configuration Example](examples/rbf-configuration-example.md)
- [Migration Guides](appendices/migration-guides.md)
- [FAQ](appendices/faq.md)
- [Troubleshooting](appendices/troubleshooting.md)
- [Contributing to Documentation](appendices/contributing-docs.md)

## Templates

- [Developer Security Checklist](appendices/templates/DEVELOPER_SECURITY_CHECKLIST.md)
- [Security Architecture Review Template](appendices/templates/ARCHITECTURE_REVIEW_TEMPLATE.md)
- [Security Testing Template](appendices/templates/SECURITY_TESTING_TEMPLATE.md)
