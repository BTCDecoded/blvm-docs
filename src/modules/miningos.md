# Mining OS Module

## Overview

The Mining OS module (`blvm-miningos`) provides bidirectional integration between BLVM and MiningOS (Mos), enabling BLVM to be managed as a MiningOS "rack" (worker) and exposing miners as "things". For information on developing custom modules, see [Module Development](../sdk/module-development.md).

## Features

- **BLVM → MiningOS**: Register BLVM as a MiningOS rack, expose miners as things, provide block templates
- **MiningOS → BLVM**: Execute actions (reboot, power management, pool config updates), query statistics, receive commands
- **HTTP REST API Client**: Full REST API integration with MiningOS app-node
- **OAuth2 Authentication**: Token-based authentication with automatic token refresh
- **P2P Worker Bridge**: Node.js bridge for Hyperswarm P2P integration
- **Block Template Provider**: Provides block templates to MiningOS
- **Enhanced Statistics**: Chain info, network stats, mempool statistics
- **Action Execution System**: Executes MiningOS actions (integrates with Stratum V2 for pool config updates)
- **Data Conversion**: Converts BLVM data to MiningOS "Thing" format
- **Event Subscription**: Subscribes to block mined, template updates, and other events

## Architecture

The module uses a hybrid approach combining:

1. **Rust Module**: Core integration logic, HTTP client, data conversion, action handling
2. **Node.js Bridge**: P2P worker that extends `TetherWrkBase` for Hyperswarm integration
3. **IPC Communication**: Unix socket-based JSON-RPC between Rust and Node.js

```
┌─────────────────────┐
│  MiningOS           │
│  Orchestrator       │
│  (Hyperswarm P2P)   │
└──────────┬──────────┘
           │
           │ Hyperswarm
           │
┌──────────▼──────────┐      Unix Socket      ┌──────────────┐
│  Node.js Bridge     │ ◄───────────────────► │ Rust Module  │
│  (worker.js)        │      JSON-RPC          │              │
└─────────────────────┘                        └──────┬───────┘
                                                       │ IPC
                                                       │
                                                ┌──────▼───────┐
                                                │  BLVM Node   │
                                                └──────────────┘
```

## Installation

### Via Cargo

```bash
cargo install blvm-miningos
```

### Via Module Installer

```bash
cargo install cargo-blvm-module
cargo blvm-module install blvm-miningos
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-miningos.git
   cd blvm-miningos
   ```

2. Build the Rust module:
   ```bash
   cargo build --release
   ```

3. Install Node.js bridge dependencies:
   ```bash
   cd bridge
   npm install
   ```

4. Install to node modules directory:
   ```bash
   mkdir -p /path/to/node/modules/blvm-miningos/target/release
   cp target/release/blvm-miningos /path/to/node/modules/blvm-miningos/target/release/
   cp -r bridge /path/to/node/modules/blvm-miningos/
   ```

## Configuration

The module searches for configuration files in the following order (first found is used):

1. `{data_dir}/config/miningos.toml`
2. `{data_dir}/miningos.toml`
3. `./config/miningos.toml`
4. `./miningos.toml`

If no configuration file is found, the module uses default values.

Create `data/config/miningos.toml`:

```toml
[miningos]
enabled = true

[p2p]
enabled = true
rack_id = "blvm-node-001"
rack_type = "miner"
auto_register = true

[http]
enabled = true
app_node_url = "https://api.mos.tether.io"
oauth_provider = "google"
oauth_client_id = "your-client-id"
oauth_client_secret = "your-client-secret"
token_cache_file = "miningos-token.json"

[stats]
enabled = true
collection_interval_seconds = 60

[template]
enabled = true
update_interval_seconds = 30
```

### Configuration Options

- `enabled` (default: `true`): Enable or disable the module
- **P2P Configuration**:
  - `enabled` (default: `true`): Enable P2P worker bridge
  - `rack_id` (required): Unique identifier for this BLVM node in MiningOS
  - `rack_type` (default: `"miner"`): Type of rack (e.g., `"miner"`)
  - `auto_register` (default: `true`): Automatically register with MiningOS
- **HTTP Configuration**:
  - `enabled` (default: `true`): Enable HTTP REST API client
  - `app_node_url` (required): MiningOS app-node API URL
  - `oauth_provider` (required): OAuth2 provider (e.g., `"google"`)
  - `oauth_client_id` (required): OAuth2 client ID
  - `oauth_client_secret` (required): OAuth2 client secret
  - `token_cache_file` (default: `"miningos-token.json"`): Token cache file path
- **Statistics Configuration**:
  - `enabled` (default: `true`): Enable statistics collection
  - `collection_interval_seconds` (default: `60`): Statistics collection interval
- **Template Configuration**:
  - `enabled` (default: `true`): Enable block template provider
  - `update_interval_seconds` (default: `30`): Template update interval

## Module Manifest

The module includes a `module.toml` manifest (see [Module Development](../sdk/module-development.md#module-manifest)):

```toml
name = "blvm-miningos"
version = "0.1.0"
description = "MiningOS integration module for BLVM"
author = "Bitcoin Commons Team"
entry_point = "blvm-miningos"

capabilities = [
    "read_blockchain",
    "subscribe_events",
    "publish_events",
    "call_module",
    "get_block_template",
    "submit_block",
]
```

## Events

### Subscribed Events

The module subscribes to node events including:

- **Chain Events**: `NewBlock`, `ChainTipUpdated`, `BlockDisconnected`
- **Mining Events**: `BlockTemplateGenerated`, `BlockFound`, `ShareSubmitted`
- **Network Events**: `PeerConnected`, `PeerDisconnected`
- **Mempool Events**: `MempoolTransactionAdded`, `MempoolTransactionRemoved`

### Published Events

The module publishes the following events:

- `MiningOSRegistered` - Successfully registered with MiningOS
- `MiningOSActionExecuted` - Action executed from MiningOS
- `MiningOSStatsUpdated` - Statistics updated and sent to MiningOS
- `MiningOSTemplateUpdated` - Block template updated and sent to MiningOS

## API Integration

The module integrates with the node via `ModuleClient` and `NodeApiIpc`:

- **Read-only blockchain access**: Queries blockchain data for statistics
- **Event subscription**: Receives real-time events from the node
- **Event publication**: Publishes MiningOS-specific events
- **Module calls**: Can call other modules (e.g., Stratum V2 for pool config updates) via `call_module`
- **Block templates**: Gets block templates via `get_block_template`
- **Block submission**: Submits mined blocks via `submit_block`

## Action Execution System

The module can execute actions from MiningOS:

- **Reboot**: System reboot commands
- **Power Management**: Power on/off commands
- **Pool Config Update**: Updates pool configuration via inter-module IPC to Stratum V2 module
- **Statistics Query**: Queries node statistics (chain info, network stats, mempool)
- **Template Refresh**: Refreshes block templates

### Inter-Module Integration

The module integrates with other modules via inter-module IPC:

- **Stratum V2**: Can update pool configuration when MiningOS sends pool config update actions
- **Node API**: Queries blockchain data, network statistics, and mempool information

## Usage

The module is automatically discovered and loaded by the BLVM node system when placed in the modules directory.

For manual testing:

```bash
./target/release/blvm-miningos \
    --module-id blvm-miningos \
    --socket-path ./data/modules/modules.sock \
    --data-dir ./data
```

## Troubleshooting

### Module Not Loading

- Verify the module binary exists at the correct path
- Check `module.toml` manifest is present and valid
- Verify module has required capabilities
- Check node logs for module loading errors
- Ensure Node.js bridge is properly installed

### OAuth2 Authentication Issues

- Verify OAuth2 credentials are correct
- Check token cache file permissions
- Verify OAuth2 provider URL is accessible
- Check node logs for authentication errors
- Ensure token refresh is working correctly

### P2P Bridge Issues

- Verify Node.js bridge is installed (`npm install` in `bridge/` directory)
- Check bridge process is running
- Verify Hyperswarm connectivity
- Check bridge logs for connection errors
- Ensure rack_id is unique

### Statistics Collection Issues

- Verify node is synced and can provide statistics
- Check collection interval configuration
- Verify NodeAPI is accessible
- Check node logs for statistics collection errors

## Repository

- **GitHub**: [blvm-miningos](https://github.com/BTCDecoded/blvm-miningos)
- **Version**: 0.1.0
- **Documentation**: [QUICKSTART.md](https://github.com/BTCDecoded/blvm-miningos/blob/main/QUICKSTART.md), [Integration Guide](https://github.com/BTCDecoded/blvm-miningos/blob/main/docs/INTEGRATION.md)

## External Resources

- **MiningOS**: [https://mos.tether.io/](https://mos.tether.io/) - The open-source, self-hosted OS for Bitcoin mining and energy orchestration that this module integrates with

## See Also

- [Module System Overview](overview.md) - Overview of all available modules
- [Stratum V2 Module](stratum-v2.md) - Stratum V2 mining protocol (integrates with MiningOS for pool config updates)
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules
