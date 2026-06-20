# Operator guide

<!-- diataxis: how-to -->

How-to hub for running a BLVM node. You do not need the Consensus, Protocol, or Governance sections for day-to-day operations.

**New to BLVM?** [Installation](installation.md) → [Quick Start](quick-start.md) (regtest, ~5 minutes) → this page for ongoing tasks.

## First sync and daily run

| Task | Guide |
|------|--------|
| Config, RPC verify, and mainnet IBD | [First Node Setup](first-node.md) ([mainnet IBD](first-node.md#mainnet-initial-sync)) |
| Regtest local dev (5 min) | [Quick Start](quick-start.md) |
| Start / stop / backup | [Node Operations](../node/operations.md) |
| Import Bitcoin Core datadir | [Operations — Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir) |
| Configuration file and env | [Node configuration](../node/configuration.md) |
| All config keys (reference) | [Configuration Reference](../reference/configuration-reference.md) |

## Security before mainnet

| Task | Guide |
|------|--------|
| Pre-mainnet checklist | [Deployment posture](../security/deployment-posture.md) |
| RPC auth and transport | [RPC transport × authentication](../security/rpc-transport-auth-matrix.md) |
| Threat surfaces | [Threat models](../security/threat-models.md) |

## RPC and monitoring

| Task | Guide |
|------|--------|
| JSON-RPC methods and parity | [RPC API Reference](../node/rpc-api.md) |
| Error codes | [JSON-RPC error reference](../reference/rpc-errors.md) |
| Health / metrics / logs | [Operations — Monitoring](../node/operations.md#monitoring) |

## Storage, sync, and network

| Task | Guide |
|------|--------|
| Database backends | [Storage Backends](../node/storage-backends.md) |
| IBD tuning and protection | [IBD UTXO engine](../node/ibd-engine.md), [IBD bandwidth protection](../node/ibd-protection.md) |
| LAN peering | [LAN Peering](../node/lan-peering.md) |
| Transports (TCP default) | [Transport abstraction](../node/transport-abstraction.md) |
| Mempool / RBF policies | [RBF and Mempool Policies](../node/rbf-mempool-policies.md) |

## Mining (optional)

| Task | Guide |
|------|--------|
| Mining overview | [Mining Integration](../node/mining.md) |
| Stratum V2 | [Stratum V2 + Merge Mining](../node/mining-stratum-v2.md), [Stratum V2 module](../modules/stratum-v2.md) |
| DATUM / Ocean | [Datum module](../modules/datum.md) |

## Optional modules

| Module | Page |
|--------|------|
| Full catalog | [Module catalog](../modules/overview.md) |
| ZMQ notifications | [ZMQ module](../modules/zmq.md) |
| FIBRE block relay | [FIBRE module](../modules/fibre.md) |
| Mesh payments | [Mesh module](../modules/mesh.md) |

## Examples and troubleshooting

- [RBF configuration example](../examples/rbf-configuration-example.md)
- [FAQ](../appendices/faq.md)
- [Troubleshooting](../appendices/troubleshooting.md)

## When you need deeper context

- [Stack overview](../architecture/system-overview.md) — what the crates are
- [Node overview](../node/overview.md) — node architecture
- [API Index](../reference/api-index.md) — cross-repo API map
