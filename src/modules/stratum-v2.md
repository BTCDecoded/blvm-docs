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
- Optional: node `stratum-v2` feature for P2P Stratum TLV demux — see [Stratum V2 mining](../node/mining-stratum-v2.md).

## Loading

Pin in `blvm.toml`:

```toml
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"

[enabled_modules]
blvm-stratum-v2 = "0.1.*"
```

Per-module overrides:

```toml
[modules.blvm-stratum-v2]
enabled = true
listen_addr = "0.0.0.0:3333"
```

See [Installing modules](overview.md#installing-modules).

## Configuration

Create a `config.toml` file **in the module’s directory** (this `[stratum_v2]` table is read by **`blvm-stratum-v2`**, not a substitute for the node’s top-level `blvm.toml` schema — avoid copying into the node file without reading [Stratum V2 mining](../node/mining-stratum-v2.md)).

```toml
[stratum_v2]
# Enable/disable module
enabled = true

# Network listening address for Stratum V2 server
listen_addr = "0.0.0.0:3333"

# Mining pool URL (for pool mode)
pool_url = "stratum+tcp://pool.example.com:3333"
```

### Configuration Options

- `enabled` (default: `true`): Enable or disable the module
- `listen_addr` (default: `"0.0.0.0:3333"`): Network address to listen on for Stratum V2 server
- `pool_url` (optional): Mining pool URL when operating in pool mode

## Module Manifest

The module includes a `module.toml` manifest (see [Building modules](../sdk/module-development.md#module-manifest)):

```toml
name = "blvm-stratum-v2"
version = "0.1.0"
description = "Stratum V2 mining protocol module"
author = "Bitcoin Commons Team"
entry_point = "blvm-stratum-v2"

capabilities = [
    "read_blockchain",
    "subscribe_events",
]
```

## Events

### Subscribed Events

The module subscribes to the following node events:

- `BlockMined` - Block successfully mined
- `BlockTemplateUpdated` - New block template available
- `MiningDifficultyChanged` - Mining difficulty changed
- `NewBlock` - New block connected
- `ChainReorg` - Chain reorganization

### Published Events

The module publishes the following events:

- `MiningJobCreated` - New mining job created
- `ShareSubmitted` - Mining share submitted
- `MiningPoolConnected` - Connected to mining pool
- `MiningPoolDisconnected` - Disconnected from mining pool

**Note**: Merge mining events (such as `MergeMiningReward`) are published by the separate `blvm-merge-mining` module, not by this module.

## Stratum V2 Protocol

The Stratum V2 **specification** defines binary TLV framing, optional encryption, and (in some deployments) multiplexed transports. In this stack, **`blvm-stratum-v2`** binds **`listen_addr`** for **miner TCP**; **`blvm-node`** may **demux Stratum-shaped TLV on P2P** into **`StratumV2MessageReceived`** when the `stratum-v2` feature is enabled ([Stratum V2 mining](../node/mining-stratum-v2.md)). **TLS**, **QUIC**, or stream multiplexing apply only if **your deployment** actually uses those stacks.

Stratum V2 features commonly discussed in spec materials:

- **Binary / TLV framing** — compact binary messages vs Stratum V1 text
- **Template and share flow** — template distribution, share submission, channels (see upstream [Stratum V2](https://stratumprotocol.org/) docs)

### Protocol Components

- **Server**: `StratumV2Server` manages connections and job distribution
- **Pool**: `StratumV2Pool` manages miners, channels, and share validation
- **Template Generator**: `BlockTemplateGenerator` creates block templates from mempool
- **Protocol Parser**: Handles TLV-encoded Stratum V2 messages

For detailed information about the Stratum V2 protocol, see [Stratum V2 Mining Protocol](../node/mining-stratum-v2.md).

## Merge Mining (Separate Plugin)

**Merge mining is NOT part of the Stratum V2 module.** It is available as a separate paid plugin module (`blvm-merge-mining`) that integrates with the Stratum V2 module.

For merge mining functionality, see:
- [blvm-merge-mining README](https://github.com/BTCDecoded/blvm-merge-mining/blob/main/README.md) — merge mining module documentation (repository; optional checkout beside `blvm-docs`)
- [Stratum V2 + Merge Mining](../node/mining-stratum-v2.md) - How merge mining integrates with Stratum V2

## Usage

Once installed and configured, the module typically:

1. Subscribes to mining-related events from the node
2. Accepts **miner connections** on **`listen_addr`** (module-owned TCP) and parses Stratum V2 TLV frames locally
3. Optionally handles **P2P-delivered** Stratum-shaped traffic when the node publishes **`StratumV2MessageReceived`** (`stratum-v2` feature on the node)
4. Creates and distributes mining jobs to connected miners
5. Manages mining pool connections (if configured)
6. Tracks mining rewards and publishes mining events

**Note**: Merge mining is handled by a separate module (`blvm-merge-mining`) that integrates with this module.

**P2P path**: With the node’s `stratum-v2` feature, the network layer may classify inbound bytes as Stratum V2 TLV and dispatch **`StratumV2MessageReceived`**; that path does **not** replace the module’s miner listener. Firewalls and `listen_addr` still matter for miners connecting to the module.

### Integration with Other Modules

- **blvm-datum**: Works together with `blvm-datum` for DATUM Gateway mining. `blvm-stratum-v2` handles miner connections while `blvm-datum` handles pool communication.
- **blvm-miningos**: MiningOS can update pool configuration via this module's inter-module API.
- **blvm-merge-mining**: Separate module that integrates with Stratum V2 for merge mining functionality.

## API Integration

The module integrates with the node via `ModuleClient` and `NodeApiIpc`:

- **Read-only blockchain access**: Queries blockchain data for block templates
- **Event subscription**: Receives real-time mining events from the node
- **Event publication**: Publishes mining-specific events

**Note**: The module subscribes to `MiningJobCreated` and `ShareSubmitted` events for coordination with other modules (e.g., merge mining), but these events are also published by this module when jobs are created and shares are submitted.

## Troubleshooting

| Symptom | Check |
|---------|--------|
| Module not loading | Binary path; `module.toml`; capabilities in node logs |
| No mining jobs | Node synced; `BlockTemplateUpdated` events; miners connected |
| Pool connection fails | `pool_url` reachable; pool supports Stratum V2 |
| Miners cannot connect | Firewall on `listen_addr`; not the node P2P port |

## Repository

- **GitHub**: [blvm-stratum-v2](https://github.com/BTCDecoded/blvm-stratum-v2)
- **Version**: 0.1.0

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


