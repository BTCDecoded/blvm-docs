# Stratum V2 Module

## Overview

The Stratum V2 module (`blvm-stratum-v2`) implements [Stratum V2 mining protocol](../node/mining-stratum-v2.md) support for blvm-node: Stratum V2 server implementation, mining pool management, and mining job distribution. For information on developing custom modules, see [Module Development](../sdk/module-development.md).

**Note**: Merge mining is available as a separate paid plugin module (`blvm-merge-mining`) that integrates with the Stratum V2 module. It is not built into the Stratum V2 module itself.

## Features

- **Stratum V2 Server**: Full Stratum V2 protocol server implementation
- **Mining Pool Management**: Manages connections to mining pools
- **Mining Job Distribution**: Distributes mining jobs to connected miners
- **Network Integration**: Fully integrated with node network layer (messages routed automatically)

## Installation

### Via Cargo

```bash
cargo install blvm-stratum-v2
```

### Via Module Installer

```bash
cargo install cargo-blvm-module
cargo blvm-module install blvm-stratum-v2
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

The module includes a `module.toml` manifest (see [Module Development](../sdk/module-development.md#module-manifest)):

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
- `ChainTipUpdated` - Chain tip updated (new block)

### Published Events

The module publishes the following events:

- `MiningJobCreated` - New mining job created
- `ShareSubmitted` - Mining share submitted
- `MiningPoolConnected` - Connected to mining pool
- `MiningPoolDisconnected` - Disconnected from mining pool

**Note**: Merge mining events (such as `MergeMiningReward`) are published by the separate `blvm-merge-mining` module, not by this module.

## Stratum V2 Protocol

The module implements the Stratum V2 protocol specification, providing:

- **Binary Protocol**: 50-66% bandwidth savings compared to Stratum V1
- **TLV Encoding**: Tag-Length-Value encoding for efficient message serialization
- **Encrypted Communication**: TLS/QUIC encryption for secure connections
- **Multiplexed Channels**: QUIC stream multiplexing for multiple mining streams
- **Template Distribution**: Efficient block template distribution
- **Share Submission**: Optimized share submission protocol
- **Channel Management**: Multiple mining channels per connection

### Protocol Components

- **Server**: `StratumV2Server` manages connections and job distribution
- **Pool**: `StratumV2Pool` manages miners, channels, and share validation
- **Template Generator**: `BlockTemplateGenerator` creates block templates from mempool
- **Protocol Parser**: Handles TLV-encoded Stratum V2 messages

For detailed information about the Stratum V2 protocol, see [Stratum V2 Mining Protocol](../node/mining-stratum-v2.md).

## Merge Mining (Separate Plugin)

**Merge mining is NOT part of the Stratum V2 module.** It is available as a separate paid plugin module (`blvm-merge-mining`) that integrates with the Stratum V2 module.

For merge mining functionality, see:
- [blvm-merge-mining README](../../blvm-merge-mining/README.md) - Merge mining module documentation
- [Stratum V2 + Merge Mining](../node/mining-stratum-v2.md) - How merge mining integrates with Stratum V2

## Usage

Once installed and configured, the module automatically:

1. Subscribes to mining-related events from the node
2. Receives Stratum V2 messages via the node's network layer (automatic routing)
3. Creates and distributes mining jobs to connected miners
4. Manages mining pool connections (if configured)
5. Tracks mining rewards and publishes mining events

**Note**: Merge mining is handled by a separate module (`blvm-merge-mining`) that integrates with this module.

The node's network layer automatically detects Stratum V2 messages (via TLV format) and routes them to this module via the event system. No additional network configuration is required.

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

### Module Not Loading

- Verify the module binary exists at the correct path
- Check `module.toml` manifest is present and valid
- Verify module has required capabilities
- Check node logs for module loading errors

### Mining Jobs Not Creating

- Verify node has `read_blockchain` capability
- Check that block template events (`BlockTemplateUpdated`) are being published by the node
- Verify listening address is accessible and not blocked by firewall
- Check node logs for mining job creation errors
- Verify node is synced and can generate block templates
- Check that miners are connected (if no miners, jobs may not be created)

### Pool Connection Failing

- Verify pool URL is correct and accessible
- Check network connectivity to mining pool
- Verify pool supports Stratum V2 protocol
- Check node logs for connection errors

## Repository

- **GitHub**: [blvm-stratum-v2](https://github.com/BTCDecoded/blvm-stratum-v2)
- **Version**: 0.1.0

## See Also

- [Module System Overview](overview.md) - Overview of all available modules
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules
- [SDK Overview](../sdk/overview.md) - SDK introduction and capabilities
- [Stratum V2 + Merge Mining](../node/mining-stratum-v2.md) - Stratum V2 protocol documentation
- [Mining Integration](../node/mining.md) - Mining functionality
- [Datum Module](datum.md) - DATUM Gateway mining protocol (works with Stratum V2)


