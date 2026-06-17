# Datum Module

## Overview

The Datum module (`blvm-datum`) implements the DATUM Gateway mining protocol for Ocean pool support. Pool communication runs here; miners connect through `blvm-stratum-v2`.

## Features

- **DATUM Protocol Client**: Encrypted communication with DATUM pools (Ocean)
- **Decentralized Templates**: Block templates generated locally via NodeAPI
- **Coinbase Coordination**: Coordinates coinbase payouts with DATUM pool
- **Module Cooperation**: Works with `blvm-stratum-v2` for complete mining solution

## Architecture

The module integrates with both the node and the Stratum V2 module:

```
┌─────────────────┐
│   blvm-node     │
│  (Core Node)    │
└────────┬────────┘
         │ NodeAPI
         │ (get_block_template, submit_block)
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ blvm-   │ │ blvm-datum   │
│ stratum │ │ (Module)     │
│ v2      │ │              │
│         │ │ ┌──────────┐ │
│ ┌─────┐ │ │ │ DATUM   │ │◄─── DATUM Pool (Ocean)
│ │ SV2 │ │ │ │ Client  │ │     (Encrypted Protocol)
│ │Server│ │ │ └──────────┘ │
│ └─────┘ │ └──────────────┘
│         │
│    │    │
│    ▼    │
│ Mining  │
│Hardware │
└─────────┘
```

**Key Points**:
- `blvm-datum`: Handles DATUM pool communication only
- `blvm-stratum-v2`: Handles miner connections
- Both modules share block templates via NodeAPI
- Both modules can submit blocks independently

## Installation

### Via Cargo

```bash
cargo install blvm-datum
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-datum.git
   cd blvm-datum
   ```

2. Build the module:
   ```bash
   cargo build --release
   ```

3. Install to node modules directory:
   ```bash
   mkdir -p /path/to/node/modules/blvm-datum/target/release
   cp target/release/blvm-datum /path/to/node/modules/blvm-datum/target/release/
   cp module.toml /path/to/node/modules/blvm-datum/
   ```

## Requirements

- `blvm-node` with the module system enabled.
- **`blvm-stratum-v2`** enabled — miners connect to Stratum V2; this module handles DATUM pool (Ocean) only.
- Valid DATUM pool credentials (`pool_url`, `pool_username`, `pool_password`).
- Optional `pool_public_key` for encrypted pool channel.

## Loading

Pin both modules in `blvm.toml`:

```toml
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"

[enabled_modules]
blvm-stratum-v2 = "0.1.*"
blvm-datum = "0.1.*"
```

Example node overrides:

```toml
[modules.blvm-stratum-v2]
listen_addr = "0.0.0.0:3333"

[modules.blvm-datum]
pool_url = "https://ocean.xyz/datum"
pool_username = "user"
pool_password = "pass"
```

See [Installing modules](overview.md#installing-modules).

## Configuration

Both `blvm-stratum-v2` and `blvm-datum` modules should be enabled for full DATUM Gateway functionality. Create configuration in your node's `config.toml`:

```toml
[modules.blvm-stratum-v2]
enabled = true
listen_addr = "0.0.0.0:3333"
mode = "solo"  # or "pool"

[modules.blvm-datum]
enabled = true
pool_url = "https://ocean.xyz/datum"
pool_username = "user"
pool_password = "pass"
pool_public_key = "hex_encoded_32_byte_public_key"  # Optional, for encryption

[modules.blvm-datum.mining]
coinbase_tag_primary = "DATUM Gateway"
coinbase_tag_secondary = "BLVM User"
pool_address = "bc1q..."  # Bitcoin address for pool payouts
```

### Configuration Options

- `enabled` (default: `true`): Enable or disable the module
- `pool_url` (required): DATUM pool URL (e.g., `https://ocean.xyz/datum`)
- `pool_username` (required): Pool username
- `pool_password` (required): Pool password
- `pool_public_key` (optional): Pool public key (32-byte hex-encoded) for encryption
- `coinbase_tag_primary` (optional): Primary coinbase tag
- `coinbase_tag_secondary` (optional): Secondary coinbase tag
- `pool_address` (optional): Bitcoin address for pool payouts

**Note**: The `blvm-stratum-v2` module must also be enabled and configured for miners to connect.

## Module Manifest

The module includes a `module.toml` manifest (see [Building modules](../sdk/module-development.md#module-manifest)):

```toml
name = "blvm-datum"
version = "0.1.0"
description = "DATUM Gateway mining protocol module for blvm-node"
author = "Bitcoin Commons Team"
entry_point = "blvm-datum"

capabilities = [
    "read_blockchain",
    "subscribe_events",
]
```

## Events

### Subscribed Events

The module subscribes to node events including:

- **Chain Events**: `NewBlock`, `ChainReorg`, `BlockDisconnected`
- **Mining Events**: `BlockTemplateGenerated`, `BlockFound`

### Published Events

The module publishes the following events:

- `DatumPoolConnected` - Successfully connected to DATUM pool
- `DatumPoolDisconnected` - Disconnected from DATUM pool
- `DatumTemplateReceived` - Received block template from pool
- `DatumBlockSubmitted` - Block submitted to pool

## Dependencies

- `blvm-node`: Module system integration
- `sodiumoxide`: Encryption for DATUM protocol (Ed25519, X25519, ChaCha20Poly1305, NaCl sealed boxes)
- `ed25519-dalek`: Ed25519 signature verification
- `x25519-dalek`: X25519 key exchange
- `chacha20poly1305`: ChaCha20-Poly1305 authenticated encryption
- `tokio`: Async runtime

## API Integration

The module integrates with the node via `ModuleClient` and `NodeApiIpc`:

- **Read-only blockchain access**: Queries blockchain data for template generation
- **Event subscription**: Receives real-time events from the node
- **Event publication**: Publishes DATUM-specific events
- **NodeAPI calls**: Uses `get_block_template` and `submit_block` via NodeAPI
- **ModuleAPI registration**: Registers `DatumModuleApi` for inter-module communication

### Inter-Module Communication

The module exposes a `ModuleAPI` for other modules (e.g., `blvm-stratum-v2`) to query coinbase payout requirements:

- **`get_coinbase_payout`**: Returns the current coinbase payout structure (outputs, tags, unique ID) required by the DATUM pool

This allows other modules to construct block templates with the correct coinbase structure for DATUM pool coordination.

## Integration with Stratum V2

The `blvm-datum` module works in conjunction with `blvm-stratum-v2`:

1. **blvm-stratum-v2**: Handles miner connections via Stratum V2 protocol
   - Miners connect to the Stratum V2 server
   - Receives mining jobs and submits shares
2. **blvm-datum**: Handles DATUM pool communication
   - Communicates with Ocean pool via encrypted DATUM protocol
   - Coordinates coinbase payouts
3. **Shared templates**: Both modules use NodeAPI to get block templates independently
4. **Independent submission**: Either module can submit blocks to the network

**Architecture Flow**:
```
Miners → blvm-stratum-v2 (Stratum V2 server) → NodeAPI (block templates)
                                                      ↓
Ocean Pool ← blvm-datum (DATUM client) ← NodeAPI (block templates)
```

## Status

🚧 **In Development** - Initial implementation

## Troubleshooting

| Symptom | Check |
|---------|--------|
| Module not loading | Binary path; `module.toml`; `blvm-stratum-v2` also enabled |
| Pool connection fails | `pool_url`, credentials; TLS reachability to Ocean |
| Template / coinbase errors | `pool_address`, coinbase tags; `get_coinbase_payout` API |
| Miners idle | Stratum module `listen_addr`; miners point to Stratum not DATUM |

## Repository

- **GitHub**: [blvm-datum](https://github.com/BTCDecoded/blvm-datum)
- **Version**: 0.1.0
- **Status**: 🚧 In Development

## External Resources

- **DATUM Gateway**: [Ocean DATUM Documentation](https://ocean.xyz/docs/datum) - Official DATUM Gateway protocol documentation
- **Ocean Pool**: [Ocean.xyz](https://ocean.xyz/) - Mining pool that supports DATUM Gateway protocol

## See Also

- [Module catalog](overview.md) - Overview of all available modules
- [Stratum V2 Module](stratum-v2.md) - Stratum V2 mining protocol (required for miners to connect)
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Building modules](../sdk/module-development.md) - Guide for developing custom modules
- [DATUM Gateway Documentation](https://ocean.xyz/docs/datum) - Official DATUM documentation
