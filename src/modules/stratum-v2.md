# Stratum V2 Module

## Overview

The Stratum V2 module (`blvm-stratum-v2`) implements [Stratum V2 mining protocol](../node/mining-stratum-v2.md) support: server, pool management, and job distribution.

**Note**: Merge mining is available as a separate paid plugin module (`blvm-merge-mining`) that integrates with the Stratum V2 module. It is not built into the Stratum V2 module itself.

## Features

- **Stratum V2 Server**: Full Stratum V2 protocol server implementation
- **Mining Pool Management**: Manages connections to mining pools
- **Mining Job Distribution**: Distributes mining jobs to connected miners
- **Network integration**: Uses **`NodeAPI`** and node events; optional P2P Stratum TLV demux surfaces **`StratumV2MessageReceived`** (see [Stratum V2 mining](../node/mining-stratum-v2.md)); dedicated miner TCP is served by this module

## Installation

### Via Cargo

```bash
cargo install blvm-stratum-v2
```

### Manual Installation

1. Clone the repository:
 ```bash
 git clone https://github.com/BTCDecoded/blvm-stratum-v2.git
 cd blvm-stratum-v2
 ```

2. Build the module:
 ```bash
 cargo build --release
 ```

3. Install to node modules directory:
 ```bash
 mkdir -p /path/to/node/modules/blvm-stratum-v2/target/release
 cp target/release/blvm-stratum-v2 /path/to/node/modules/blvm-stratum-v2/target/release/
 cp module.toml /path/to/node/modules/blvm-stratum-v2/
 ```

## Requirements

- `blvm-node` with the module system enabled.
- Miners connect to this module’s **`listen_addr`** (module-owned TCP), not the node P2P port.
- Admin RPC auth for `getblocktemplate` / `submitblock` when miners submit blocks via the node.
- Optional: node `stratum-v2` feature for P2P Stratum TLV demux: see [Stratum V2 mining](../node/mining-stratum-v2.md).

## Loading

Pin in `blvm.toml`:

```toml
[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
blvm-stratum-v2 = "0.1.*"
```

Per-module overrides in node `blvm.toml` (passed as `MODULE_CONFIG_*` on spawn):

```toml
[modules.blvm-stratum-v2]
listen_addr = "0.0.0.0:3333"
difficulty_target = 1
```

See [Installing modules](overview.md#installing-modules).

## Configuration

Module `config.toml` at `<modules.data_dir>/blvm-stratum-v2/config.toml` (flat keys: same fields as `[modules.blvm-stratum-v2]` overrides):

```toml
listen_addr = "0.0.0.0:3333"
difficulty_target = 1
max_connections = 100
# pool_name = "My pool"
# extra_extranonce = "01020304"
```

| Key | Default | Purpose |
|-----|---------|---------|
| `listen_addr` | `0.0.0.0:3333` | Miner TCP bind (module-owned; not the node P2P port) |
| `difficulty_target` | `1` | Default channel difficulty when the miner sends 0 |
| `max_connections` | `100` | Max concurrent miner connections |
| `pool_name` |: | Optional display name |
| `extra_extranonce` |: | Optional extra extranonce bytes (hex) |

> **Scope:** This TOML lives under **`[modules].data_dir`** for **`blvm-stratum-v2`**, **not** in the node’s top-level **`blvm.toml`**. Node-side Stratum P2P demux and merge-mining keys are under **`[stratum_v2]`** in `blvm.toml`: see [Mining with Stratum V2](../node/mining-stratum-v2.md). There is **no** module `enabled` or `pool_url` key; enable loading via a **`[modules]`** version pin (e.g. `blvm-stratum-v2 = "0.1.*"`).

## Module Manifest

The module includes a `module.toml` manifest (see [Building modules](../sdk/module-development.md#module-manifest)):

```toml
name = "blvm-stratum-v2"
description = "Stratum V2 mining protocol module for blvm-node"
author = "Bitcoin Commons Team"
entry_point = "blvm-stratum-v2"

capabilities = [
 "read_blockchain",
 "subscribe_events",
]
```

Shipped **`version`** is in each release’s `module.toml` and **`registry/modules.json`**: do not hardcode it in the book.

## Events

### Subscribed events

| Event | Module action |
|-------|----------------|
| `BlockMined` | Refresh template / job distribution for locally mined blocks |
| `BlockTemplateUpdated` | Pull new template and distribute jobs to miners |
| `MiningDifficultyChanged` | Log; pool recalculates targets on next job |
| `MiningJobCreated` | Coordination with other modules (e.g. merge mining); jobs are driven by `BlockTemplateUpdated` |
| `ShareSubmitted` | Coordination with other modules |
| `StratumV2MessageReceived` | Handle P2P-delivered Stratum TLV when node `stratum-v2` feature + `p2p_stratum_demux` are enabled |

### Published events

| Event | When |
|-------|------|
| `StratumClientConnected` | Miner completes setup on module TCP |
| `StratumClientDisconnected` | Miner disconnects or times out |
| `ShareSubmitted` | Valid share accepted by the pool |

**Note**: Merge mining events (such as `MergeMiningReward`) are published by the separate `blvm-merge-mining` module, not by this module.

## Stratum V2 Protocol

The Stratum V2 **specification** defines binary TLV framing, optional encryption, and (in some deployments) multiplexed transports. In this stack, **`blvm-stratum-v2`** binds **`listen_addr`** for **miner TCP**; **`blvm-node`** may **demux Stratum-shaped TLV on P2P** into **`StratumV2MessageReceived`** when the `stratum-v2` feature is enabled ([Stratum V2 mining](../node/mining-stratum-v2.md)). **TLS**, **QUIC**, or stream multiplexing apply only if **your deployment** actually uses those stacks.

Stratum V2 features commonly discussed in spec materials:

- **Binary / TLV framing**: compact binary messages vs Stratum V1 text
- **Template and share flow**: template distribution, share submission, channels (see upstream [Stratum V2](https://stratumprotocol.org/) docs)

### Protocol Components

- **Server**: `StratumV2Server` manages connections and job distribution
- **Pool**: `StratumV2Pool` manages miners, channels, and share validation
- **Template Generator**: `BlockTemplateGenerator` creates block templates from mempool
- **Protocol Parser**: Handles TLV-encoded Stratum V2 messages

For detailed information about the Stratum V2 protocol, see [Stratum V2 Mining Protocol](../node/mining-stratum-v2.md).

## Merge Mining (Separate Plugin)

**Merge mining is NOT part of the Stratum V2 module.** It is available as a separate paid plugin module (`blvm-merge-mining`) that integrates with the Stratum V2 module.

For merge mining functionality, see:
- [blvm-merge-mining README](https://github.com/BTCDecoded/blvm-merge-mining/blob/main/README.md): merge mining module documentation (repository; optional checkout beside `blvm-docs`)
- [Stratum V2 + Merge Mining](../node/mining-stratum-v2.md) - How merge mining integrates with Stratum V2

## Usage

Once installed and configured, the module typically:

1. Subscribes to mining-related events from the node
2. Accepts **miner connections** on **`listen_addr`** (module-owned TCP) and parses Stratum V2 TLV frames locally
3. Optionally handles **P2P-delivered** Stratum-shaped traffic when the node publishes **`StratumV2MessageReceived`** (`stratum-v2` feature on the node)
4. Creates and distributes mining jobs to connected miners
5. Publishes `StratumClientConnected` / `ShareSubmitted` / `StratumClientDisconnected` for observability
6. Tracks mining rewards via share and block submission paths

**Note**: Merge mining is handled by a separate module (`blvm-merge-mining`) that integrates with this module.

**P2P path**: With the node’s `stratum-v2` feature, the network layer may classify inbound bytes as Stratum V2 TLV and dispatch **`StratumV2MessageReceived`**; that path does **not** replace the module’s miner listener. Firewalls and `listen_addr` still matter for miners connecting to the module.

### Integration with Other Modules

- **blvm-datum**: Works together with `blvm-datum` for DATUM Gateway mining. `blvm-stratum-v2` handles miner connections while `blvm-datum` handles pool communication.
- **blvm-miningos**: MiningOS can update pool configuration via this module's inter-module API.
- **blvm-merge-mining**: Separate module that integrates with Stratum V2 for merge mining functionality.

## API Integration

The module integrates with the node via `ModuleClient` and `NodeApiIpc`:

- **Read-only blockchain access**: Queries blockchain data for block templates
- **Event subscription**: Receives mining and template events from the node
- **Event publication**: Publishes `StratumClientConnected`, `ShareSubmitted`, and `StratumClientDisconnected`

The module also **subscribes** to `MiningJobCreated` and `ShareSubmitted` from other modules for coordination (e.g. merge mining); job creation is driven internally from `BlockTemplateUpdated`.

## Troubleshooting

| Symptom | Check |
|---------|--------|
| Module not loading | Binary path; `module.toml`; capabilities in node logs |
| No mining jobs | Node synced; `BlockTemplateUpdated` events; miners connected on `listen_addr` |
| Miners cannot connect | Firewall on `listen_addr`; not the node P2P port |

## Repository

- **GitHub**: [blvm-stratum-v2](https://github.com/BTCDecoded/blvm-stratum-v2): releases and current `module.toml` **`version`**

## External Resources

- **Stratum V2 Specification**: [Stratum V2 Protocol Specification](https://stratumprotocol.org/) - Official Stratum V2 mining protocol specification
- **Stratum V2 Documentation**: [Stratum V2 Docs](https://docs.stratumprotocol.org/) - Complete Stratum V2 protocol documentation

## See Also

- [Module catalog](overview.md) - Overview of all available modules
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Building modules](../sdk/module-development.md) - Guide for developing custom modules
- [SDK Overview](../sdk/overview.md) - SDK introduction and capabilities
- [Stratum V2 + Merge Mining](../node/mining-stratum-v2.md) - Stratum V2 protocol documentation
- [Mining Integration](../node/mining.md) - Mining functionality
- [Datum Module](datum.md) - DATUM Gateway mining protocol (works with Stratum V2)


