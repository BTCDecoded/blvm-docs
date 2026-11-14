# Operator guide

<!-- diataxis: how-to -->

How-to hub for running a BLVM node. You do not need the Consensus, Protocol, or Governance sections for day-to-day operations.

**New to BLVM?** [Installation](installation.md) → [Quick Start](quick-start.md) (regtest, ~5 minutes) → this page for ongoing tasks.

The `blvm` binary speaks Bitcoin Core JSON-RPC. Script history is `blvm-index`. The node binds Electrum and Esplora. An unset `[services]` `listen` does not open a port. See [First Node Setup](first-node.md). Payment, vault, pool, and congestion methods are the separate `blvm-payment` process: `createpaymentrequest`, `createcovenantproof`, `getpaymentstate`, `listpayments`, `verifyonchainpayment`, `verifyonchainpaymentbytx`, `verifycovenantproof`, `createvault`, `unvault`, `withdrawfromvault`, `getvaultstate`, `createpool`, `joinpool`, `distributepool`, `getpoolstate`, `createbatch`, `addtobatch`, `getcongestion`, `getcongestionmetrics`, and `broadcastbatch`. The default node answers those names with method-not-found until that module is loaded. It is not in the default module set. Chain and mempool reads go through the node API. A `merchant_key` in the module `config.toml` signs a peer payment acknowledgement.

## First sync and daily run

| Task | Guide |
|------|--------|
| Config, RPC verify, and mainnet IBD | [First Node Setup](first-node.md) ([mainnet IBD](first-node.md#mainnet-initial-sync)) |
| Regtest local dev (5 min) | [Quick Start](quick-start.md) |
| Start / stop / backup | [Node Operations](../node/operations.md) |
| Import Bitcoin Core datadir | [Operations: Core datadir](../node/operations.md#starting-from-a-bitcoin-core-datadir) |
| Configuration file and env | [Node configuration](../node/configuration.md) |
| All config keys (reference) | [Configuration Reference](../reference/configuration-reference.md) |

## Initial block download (IBD) {#initial-block-download-ibd}

Mainnet first sync touches several docs, use this map instead of reading them in arbitrary order.

| Topic | Guide |
|------|--------|
| First mainnet sync (config, RPC verify, checklist) | [First Node Setup: Mainnet IBD](first-node.md#mainnet-initial-sync) |
| Parallel download, chunk tuning, assume-valid | [Performance: Parallel IBD](../node/performance.md#parallel-initial-block-download-ibd) |
| Age-tiered UTXO store (on unless `BLVM_IBD_ENGINE=0`) | [IBD UTXO engine](../node/ibd-engine.md) |
| Bandwidth limits when **serving** peers during their IBD | [IBD bandwidth protection](../node/ibd-protection.md) |
| Stuck, slow, or quiet sync | [Troubleshooting: Mainnet IBD](../appendices/troubleshooting.md#mainnet-ibd) |
| `[ibd]` keys and `BLVM_IBD_*` env vars | [Configuration Reference: IBD](../reference/configuration-reference.md#ibd-configuration) |

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
| Health / metrics / logs | [Operations: Monitoring](../node/operations.md#monitoring) |

## Storage and network

| Task | Guide |
|------|--------|
| Database backends | [Storage Backends](../node/storage-backends.md) |
| LAN peering (faster sync when LAN peers exist) | [LAN Peering](../node/lan-peering.md) |
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

- [RBF configuration examples](../node/rbf-mempool-policies.md#configuration-examples)
- [FAQ](../appendices/faq.md)
- [Troubleshooting](../appendices/troubleshooting.md)

## When you need deeper context

- [Stack overview](../architecture/system-overview.md): what the crates are
- [Node overview](../node/overview.md): node architecture
- [API Index](../reference/api-index.md): cross-repo API map
