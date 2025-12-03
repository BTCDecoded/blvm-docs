# Lightning Network Module

## Overview

The Lightning Network module (`bllvm-lightning`) handles Lightning Network payment processing for bllvm-node: invoice verification, payment routing, channel management, and payment state tracking. For information on developing custom modules, see [Module Development](../sdk/module-development.md). For information on developing custom modules, see [Module Development](../sdk/module-development.md).

## Features

- **Invoice Verification**: Validates Lightning Network invoices (BOLT11)
- **Payment Routing**: Discovers and manages payment routes
- **Channel Management**: Tracks Lightning channel state
- **Payment State Tracking**: Monitors payment lifecycle from request to settlement

## Installation

### Via Cargo

```bash
cargo install bllvm-lightning
```

### Via Module Installer

```bash
cargo install cargo-bllvm-module
cargo bllvm-module install bllvm-lightning
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-lightning.git
   cd bllvm-lightning
   ```

2. Build the module:
   ```bash
   cargo build --release
   ```

3. Install to node modules directory:
   ```bash
   mkdir -p /path/to/node/modules/bllvm-lightning/target/release
   cp target/release/bllvm-lightning /path/to/node/modules/bllvm-lightning/target/release/
   ```

## Configuration

The module supports multiple Lightning providers. Create a `config.toml` file in the module directory:

### LNBits Provider (Recommended)

```toml
[lightning]
provider = "lnbits"

[lightning.lnbits]
api_url = "https://lnbits.example.com"
api_key = "your_lnbits_api_key"
wallet_id = "optional_wallet_id"  # Optional
```

### LDK Provider (Rust-native)

```toml
[lightning]
provider = "ldk"

[lightning.ldk]
data_dir = "data/ldk"
network = "testnet"  # or "mainnet" or "regtest"
node_private_key = "hex_encoded_private_key"  # Optional, will generate if not provided
```

### Stub Provider (Testing)

```toml
[lightning]
provider = "stub"
```

### Configuration Options

- `provider` (required): Lightning provider to use (`"lnbits"`, `"ldk"`, or `"stub"`)
- **LNBits**: `api_url`, `api_key`, `wallet_id` (optional)
- **LDK**: `data_dir`, `network`, `node_private_key` (optional)
- **Stub**: No additional configuration needed

## Module Manifest

The module includes a `module.toml` manifest (see [Module Development](../sdk/module-development.md#module-manifest)):

```toml
name = "bllvm-lightning"
version = "0.1.0"
description = "Lightning Network payment processor"
author = "Bitcoin Commons Team"
entry_point = "bllvm-lightning"

capabilities = [
    "read_blockchain",
    "subscribe_events",
]
```

## Events

### Subscribed Events

The module subscribes to the following node events:

- `PaymentRequestCreated` - New payment request created
- `PaymentSettled` - Payment confirmed on-chain
- `PaymentFailed` - Payment failed

### Published Events

The module publishes the following events:

- `PaymentVerified` - Lightning payment verified
- `PaymentRouteFound` - Payment route discovered
- `PaymentRouteFailed` - Payment routing failed
- `ChannelOpened` - Lightning channel opened
- `ChannelClosed` - Lightning channel closed

## Usage

Once installed and configured, the module automatically:

1. Subscribes to payment-related events from the node
2. Verifies Lightning invoices when payment requests are created
3. Discovers payment routes for Lightning payments
4. Tracks channel state and publishes channel events
5. Monitors payment lifecycle and publishes status events

## API Integration

The module integrates with the node via the Node API IPC protocol:

- **Read-only blockchain access**: Queries blockchain data for payment verification
- **Event subscription**: Receives real-time events from the node
- **Event publication**: Publishes Lightning-specific events

## Troubleshooting

### Module Not Loading

- Verify the module binary exists at the correct path
- Check `module.toml` manifest is present and valid
- Verify module has required capabilities
- Check node logs for module loading errors

### Payment Verification Failing

- Verify Lightning node URL is correct (if using external node)
- Check node public key is valid
- Verify module has `read_blockchain` capability
- Check node logs for detailed error messages

## See Also

- [Module System Overview](overview.md) - Overview of all available modules
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules
- [SDK Overview](../sdk/overview.md) - SDK introduction and capabilities
- [SDK API Reference](../sdk/api-reference.md) - Complete SDK API documentation
- [SDK Examples](../sdk/examples.md) - Module development examples


