# Summary

[Introduction](introduction.md)

# Getting Started

- [Operator guide](getting-started/operator-guide.md)
- [Developer guide](getting-started/developer-guide.md)

## Operators

- [Installation](getting-started/installation.md)
- [Quick Start](getting-started/quick-start.md)
- [First Node Setup](getting-started/first-node.md)

## Developers

- [Building your first module](getting-started/first-module.md)

# Architecture

- [Stack overview](architecture/system-overview.md)
- [Design philosophy](architecture/design-philosophy.md)
- [Crate dependencies](architecture/component-relationships.md)

## Module runtime

- [Module system](architecture/module-system.md)
- [Module IPC protocol](architecture/module-ipc-protocol.md)
- [Module events](architecture/module-events.md)
- [Janitorial events](architecture/janitorial-events.md)

# Consensus

- [Overview](consensus/overview.md)
- [Mathematical specifications](consensus/mathematical-specifications.md)
- [Formal verification](consensus/formal-verification.md)

# Protocol

- [Overview](protocol/overview.md)
- [Wire format](protocol/network-protocol.md)

# Node

- [Overview](node/overview.md)
- [Operations](node/operations.md)
- [Configuration](node/configuration.md)
- [RPC API](node/rpc-api.md)

## Sync and chainstate

- [Storage backends](node/storage-backends.md)
- [IBD bandwidth protection](node/ibd-protection.md)
- [IBD UTXO engine](node/ibd-engine.md)
- [UTXO commitments](node/utxo-commitments.md)
- [Peer consensus protocol](node/peer-consensus.md)

## Network and relay

- [Transport abstraction](node/transport-abstraction.md)
- [LAN peering](node/lan-peering.md)
- [Transaction relay](node/privacy-relay.md)
- [Package relay (BIP331)](node/package-relay.md)
- [Spam filtering](node/spam-filtering.md)

## Mempool and indexing

- [RBF and mempool policies](node/rbf-mempool-policies.md)
- [Transaction indexing](node/transaction-indexing.md)

## Mining

- [Mining integration](node/mining.md)
- [Stratum V2 and merge mining](node/mining-stratum-v2.md)

## Performance

- [Performance optimizations](node/performance.md)

# Security

- [Deployment posture](security/deployment-posture.md)
- [RPC transport and authentication](security/rpc-transport-auth-matrix.md)
- [Threat models](security/threat-models.md)

# SDK and modules

- [SDK overview](sdk/overview.md)
- [Building modules](sdk/module-development.md)
- [API reference](sdk/api-reference.md)
- [Examples](sdk/examples.md)

## Module catalog

- [Overview](modules/overview.md)
- [Lightning Network](modules/lightning.md)
- [Commons Mesh](modules/mesh.md)
- [Stratum V2](modules/stratum-v2.md)
- [Datum](modules/datum.md)
- [Selective Sync](modules/selective-sync.md)
- [FIBRE](modules/fibre.md)
- [ZMQ](modules/zmq.md)
- [Miniscript](modules/miniscript.md)
- [Governance module](modules/governance-module.md)
- [Marketplace](modules/marketplace-module.md)

# Governance

- [Overview](governance/overview.md)
- [blvm-commons](governance/blvm-commons.md)
- [Governance model](governance/governance-model.md)
- [Layers and tiers](governance/layer-tier-model.md)
- [Configuration system](governance/configuration-system.md)
- [Governance fork](governance/governance-fork.md)
- [P2P governance messages](governance/p2p-governance-messages.md)
- [OpenTimestamps](governance/opentimestamps-integration.md)
- [Nostr integration](governance/nostr-integration.md)
- [Multisig configuration](governance/multisig-configuration.md)
- [Keyholder procedures](governance/keyholder-procedures.md)
- [Audit trails](governance/audit-trails.md)

# Reference

- [Orange Paper](reference/orange-paper.md)
- [Protocol specifications (BIPs)](reference/protocol-specifications.md)
- [Configuration reference](reference/configuration-reference.md)
- [JSON-RPC errors](reference/rpc-errors.md)
- [API index](reference/api-index.md)
- [Glossary](reference/glossary.md)

# Development

## Contributing

- [Contributing](development/contributing.md)
- [PR security controls](development/security-controls.md)
- [Repository layout](development/repository-architecture.md)
- [Rust MSRV and CI toolchains](development/msrv-note.md)
- [CI/CD workflows](development/ci-cd-workflows.md)
- [PR process](development/pr-process.md)
- [Release process](development/release-process.md)

## Testing and benchmarks

- [Testing infrastructure](development/testing.md)
- [Property-based testing](development/property-based-testing.md)
- [Differential testing](development/differential-testing.md)
- [Benchmarking](development/benchmarking.md)
- [Snapshot testing](development/snapshot-testing.md)

# Appendices

- [FAQ](appendices/faq.md)
- [Troubleshooting](appendices/troubleshooting.md)
- [Contributing to documentation](appendices/contributing-docs.md)

## Templates

- [Developer security checklist](appendices/templates/DEVELOPER_SECURITY_CHECKLIST.md)
- [Security architecture review](appendices/templates/ARCHITECTURE_REVIEW_TEMPLATE.md)
- [Security testing template](appendices/templates/SECURITY_TESTING_TEMPLATE.md)
