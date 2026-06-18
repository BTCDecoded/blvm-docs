# Mining OS Module

## Overview

The Mining OS module (`blvm-miningos`) integrates BLVM with MiningOS (Mos): BLVM runs as a MiningOS "rack" (worker) and exposes miners as "things".

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

## Requirements

- `blvm-node` with the module system enabled.
- **Node.js** (for the Hyperswarm P2P bridge) — install bridge deps under `bridge/`.
- MiningOS app-node URL and **OAuth2** credentials (`oauth_client_id`, `oauth_client_secret`).
- Optional: `blvm-stratum-v2` for pool config actions from MiningOS.

## Loading

Pin in `blvm.toml`:

```toml
[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
blvm-miningos = "0.1.*"
```

Config file search order (first found wins): `{data_dir}/config.toml`, `{data_dir}/config/miningos.toml`, `{data_dir}/miningos.toml`, then `./config/miningos.toml` / `./miningos.toml`. See [Configuration](#configuration). See [Installing modules](overview.md#installing-modules).

## Configuration

The module searches for configuration in this order (first found is used):

1. `{data_dir}/config.toml`
2. `{data_dir}/config/miningos.toml`
3. `{data_dir}/miningos.toml`
4. `./config/miningos.toml`
5. `./miningos.toml`

If no file is found, defaults from `MiningOsConfig::default()` apply.

Example `{data_dir}/config/miningos.toml`:

```toml
[miningos]
enabled = true

[p2p]
enabled = true
orchestrator_rpc_public_key = "hex-or-base58-orchestrator-key"
rack_id = "blvm-node-001"
rack_type = "miner"
auto_register = true
reconnect_interval_seconds = 30

[http]
enabled = true
app_node_url = "https://api.mos.tether.io"
oauth_provider = "google"
oauth_client_id = "your-client-id"
oauth_client_secret = "your-client-secret"
oauth_callback_url = "http://localhost:3000/oauth/google/callback"
token_cache_file = "miningos-token.json"
# oauth_token_url = "https://..."  # optional; derived from provider when unset

[stats]
enabled = true
collection_interval_seconds = 60
hashrate_unit = "TH/s"
temperature_unit = "celsius"
power_unit = "watts"

[template]
enabled = true
update_interval_seconds = 30
expose_via_http = true
expose_via_p2p = true
cache_duration_seconds = 10

[actions]
enabled = true
supported_actions = ["reboot", "setPowerMode", "updatePoolConfig", "setHashrate"]
require_approval = true
timeout_seconds = 120

[things]
auto_register_miners = true
miner_tag = "t-miner"
update_interval_seconds = 60
```

Node overrides: `[modules.blvm-miningos]` in `blvm.toml` or `MODULE_CONFIG_*` env vars (see [Configuration Reference](../reference/configuration-reference.md#module-system-configuration)).

### Configuration options

| Section | Key | Notes |
|---------|-----|--------|
| `[miningos]` | `enabled` | Master switch (default `true`) |
| `[p2p]` | `enabled`, `orchestrator_rpc_public_key`, `rack_id`, `rack_type`, `auto_register`, `reconnect_interval_seconds` | Hyperswarm bridge via Node.js `bridge/` |
| `[http]` | `enabled`, `app_node_url`, `oauth_*`, `token_cache_file`, `oauth_token_url` | MiningOS app-node REST + OAuth2 |
| `[stats]` | `enabled`, `collection_interval_seconds`, `hashrate_unit`, `temperature_unit`, `power_unit` | Periodic stats push |
| `[template]` | `enabled`, `update_interval_seconds`, `expose_via_http`, `expose_via_p2p`, `cache_duration_seconds` | Block template provider |
| `[actions]` | `enabled`, `supported_actions`, `require_approval`, `timeout_seconds` | MiningOS action handlers |
| `[things]` | `auto_register_miners`, `miner_tag`, `update_interval_seconds` | Miner → MiningOS “thing” registration |

## Module Manifest

The module includes a `module.toml` manifest (see [Building modules](../sdk/module-development.md#module-manifest)):

```toml
name = "blvm-miningos"
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

Shipped **`version`** is in each release’s `module.toml` and **`registry/modules.json`** — do not hardcode it in the book.

The node maps manifest **`capabilities`** to module permissions at load time — include **`get_block_template`** and **`submit_block`** when this module fetches templates or submits blocks.

## Events

### Subscribed events

At startup the module subscribes to:

- `BlockMined`
- `BlockTemplateUpdated`
- `MiningDifficultyChanged`

### Published events

When actions complete via the module API, the module may publish:

- `ActionExecuted` — MiningOS action handled (payload includes action name and result)

Statistics and template updates are pushed to MiningOS over HTTP/P2P; they are **not** separate custom `EventType` values.

## API integration

The module connects via **`ModuleIntegration`**, registers **`MiningOsModuleApi`**, and uses **`NodeAPI`** for chain/template queries:

- **Statistics / templates**: background tasks when `[stats]` / `[template]` are enabled
- **Module API**: other modules can invoke MiningOS actions through the registered API
- **Block templates / submit**: requires manifest capabilities **`get_block_template`** and **`submit_block`** (enforced as permissions)
- **Inter-module**: pool config updates can call **`blvm-stratum-v2`** when loaded

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

| Symptom | Check |
|---------|--------|
| Module not loading | Binary + `module.toml`; Node.js bridge installed |
| OAuth2 failures | Client ID/secret; `token_cache_file` permissions; app-node URL |
| P2P bridge down | `npm install` in `bridge/`; unique `rack_id`; Hyperswarm reachability |
| Stats not updating | Node synced; `collection_interval_seconds`; NodeAPI access |

## Repository

- **GitHub**: [blvm-miningos](https://github.com/BTCDecoded/blvm-miningos) — releases and current `module.toml` **`version`**
- **Documentation**: [QUICKSTART.md](https://github.com/BTCDecoded/blvm-miningos/blob/main/QUICKSTART.md), [Integration Guide](https://github.com/BTCDecoded/blvm-miningos/blob/main/docs/INTEGRATION.md)

## External Resources

- **MiningOS**: [https://mos.tether.io/](https://mos.tether.io/) - The open-source, self-hosted OS for Bitcoin mining and energy orchestration that this module integrates with

## See Also

- [Module catalog](overview.md) - Overview of all available modules
- [Stratum V2 Module](stratum-v2.md) - Stratum V2 mining protocol (integrates with MiningOS for pool config updates)
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Building modules](../sdk/module-development.md) - Guide for developing custom modules
