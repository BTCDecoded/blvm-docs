# Stratum V2 Module

## Overview

The Stratum V2 module (`bllvm-stratum-v2`) provides Stratum V2 mining protocol support for bllvm-node, including Stratum V2 server implementation, mining pool management, merge mining coordination, and mining job distribution.

## Features

- **Stratum V2 Server**: Full Stratum V2 protocol server implementation
- **Mining Pool Management**: Manages connections to mining pools
- **Merge Mining Coordination**: Coordinates merge mining across multiple chains
- **Mining Job Distribution**: Distributes mining jobs to connected miners

## Installation

### Via Cargo

```bash
cargo install bllvm-stratum-v2
```

### Via Module Installer

```bash
cargo install cargo-bllvm-module
cargo bllvm-module install bllvm-stratum-v2
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BTCDecoded/bllvm-stratum-v2.git
   cd bllvm-stratum-v2
   ```

2. Build the module:
   ```bash
   cargo build --release
   ```

3. Install to node modules directory:
   ```bash
   mkdir -p /path/to/node/modules/bllvm-stratum-v2/target/release
   cp target/release/bllvm-stratum-v2 /path/to/node/modules/bllvm-stratum-v2/target/release/
   ```

## Configuration

Create a `config.toml` file in the module directory:

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

The module includes a `module.toml` manifest:

```toml
name = "bllvm-stratum-v2"
version = "0.1.0"
description = "Stratum V2 mining protocol module"
author = "Bitcoin Commons Team"
entry_point = "bllvm-stratum-v2"

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
- `ChainTipUpdated` - Chain tip updated (new block)

### Published Events

The module publishes the following events:

- `MiningJobCreated` - New mining job created
- `ShareSubmitted` - Mining share submitted
- `MergeMiningReward` - Merge mining reward received
- `MiningPoolConnected` - Connected to mining pool
- `MiningPoolDisconnected` - Disconnected from mining pool

## Stratum V2 Protocol

The module implements the Stratum V2 protocol specification, providing:

- **Binary Protocol**: 50-66% bandwidth savings compared to Stratum V1
- **Encrypted Communication**: TLS/QUIC encryption for secure connections
- **Multiplexed Channels**: QUIC stream multiplexing for multiple mining streams
- **Template Distribution**: Efficient block template distribution
- **Share Submission**: Optimized share submission protocol

For detailed information about the Stratum V2 protocol, see [Stratum V2 + Merge Mining](../node/mining-stratum-v2.md).

## Merge Mining

The module supports merge mining coordination, enabling simultaneous mining of Bitcoin and secondary chains (e.g., RSK, Namecoin) using the same proof-of-work.

Merge mining features:
- Multiple chain support via multiplexed channels
- Revenue tracking and distribution
- Automatic chain coordination

## Usage

Once installed and configured, the module automatically:

1. Subscribes to mining-related events from the node
2. Creates and distributes mining jobs to connected miners
3. Manages mining pool connections (if configured)
4. Coordinates merge mining across multiple chains
5. Tracks mining rewards and publishes mining events

## API Integration

The module integrates with the node via the Node API IPC protocol:

- **Read-only blockchain access**: Queries blockchain data for block templates
- **Event subscription**: Receives real-time mining events from the node
- **Event publication**: Publishes mining-specific events

## Troubleshooting

### Module Not Loading

- Verify the module binary exists at the correct path
- Check `module.toml` manifest is present and valid
- Verify module has required capabilities
- Check node logs for module loading errors

### Mining Jobs Not Creating

- Verify node has `read_blockchain` capability
- Check that block template events are being published
- Verify listening address is accessible
- Check node logs for mining job creation errors

### Pool Connection Failing

- Verify pool URL is correct and accessible
- Check network connectivity to mining pool
- Verify pool supports Stratum V2 protocol
- Check node logs for connection errors

## See Also

- [Module System Overview](overview.md) - Overview of all available modules
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Stratum V2 + Merge Mining](../node/mining-stratum-v2.md) - Stratum V2 protocol documentation


