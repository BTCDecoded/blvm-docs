# Lightning Network Module

## Overview

The Lightning Network module (`blvm-lightning`) handles Lightning Network payment processing for blvm-node: invoice verification, payment routing, channel management, and payment state tracking. For information on developing custom modules, see [Module Development](../sdk/module-development.md).

## Features

- **Invoice Verification**: Validates Lightning Network invoices (BOLT11) using multiple provider backends
- **Payment Processing**: Processes Lightning payments via LNBits API or LDK
- **Provider Abstraction**: Supports multiple Lightning providers (LNBits, LDK, Stub) with unified interface
- **Payment State Tracking**: Monitors payment lifecycle from request to settlement

## Installation

### Via Cargo

```bash
cargo install blvm-lightning
```

### Via Module Installer

```bash
cargo install cargo-blvm-module
cargo blvm-module install blvm-lightning
```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BTCDecoded/blvm-lightning.git
   cd blvm-lightning
   ```

2. Build the module:
   ```bash
   cargo build --release
   ```

3. Install to node modules directory:
   ```bash
   mkdir -p /path/to/node/modules/blvm-lightning/target/release
   cp target/release/blvm-lightning /path/to/node/modules/blvm-lightning/target/release/
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

### Provider Comparison

| Feature | LNBits | LDK | Stub |
|---------|--------|-----|------|
| **Status** | ✅ Production-ready | ✅ Fully implemented | ✅ Testing |
| **API Type** | REST (HTTP) | Rust-native (lightning-invoice) | None |
| **Real Lightning** | ✅ Yes | ✅ Yes | ❌ No |
| **External Service** | ✅ Yes | ❌ No | ❌ No |
| **Invoice Creation** | ✅ Via API | ✅ Native | ✅ Mock |
| **Payment Verification** | ✅ Via API | ✅ Native | ✅ Mock |
| **Best For** | Payment processing | Full control, Rust-native | Testing |

**Switching Providers**: All providers implement the same interface, so switching providers is just a configuration change. No code changes required.

## Module Manifest

The module includes a `module.toml` manifest (see [Module Development](../sdk/module-development.md#module-manifest)):

```toml
name = "blvm-lightning"
version = "0.1.0"
description = "Lightning Network payment processor"
author = "Bitcoin Commons Team"
entry_point = "blvm-lightning"

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

1. Subscribes to payment-related events from the node (`PaymentRequestCreated`, `PaymentSettled`, `PaymentFailed`)
2. Verifies Lightning invoices (BOLT11) when payment requests are created
3. Processes payments using the configured provider (LNBits, LDK, or Stub)
4. Publishes payment verification and status events (`PaymentVerified`, `PaymentRouteFound`, `PaymentRouteFailed`)
5. Monitors payment lifecycle and publishes status events

The module automatically selects the provider based on configuration. All providers implement the same interface, so switching providers requires only a configuration change.

### Provider Selection

The module uses the `LightningProcessor` to handle payment processing. The processor:
- Reads provider configuration from `lightning.provider`
- Creates the appropriate provider instance (LNBits, LDK, or Stub)
- Routes all payment operations through the provider interface
- Stores provider configuration in module storage for persistence

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

- **LNBits Provider**: Verify API URL and API key are correct, check LNBits service is accessible
- **LDK Provider**: Verify data directory permissions, check network configuration (mainnet/testnet/regtest)
- **General**: Verify module has `read_blockchain` capability, check node logs for detailed error messages

### Provider-Specific Issues

- **LNBits**: Check API endpoint is accessible, verify wallet_id if specified, check API rate limits
- **LDK**: Verify data directory exists and is writable, check network matches node configuration
- **Stub**: No real verification - only for testing

## Repository

- **GitHub**: [blvm-lightning](https://github.com/BTCDecoded/blvm-lightning)
- **Version**: 0.1.0

## See Also

- [Module System Overview](overview.md) - Overview of all available modules
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Module Development](../sdk/module-development.md) - Guide for developing custom modules
- [SDK Overview](../sdk/overview.md) - SDK introduction and capabilities
- [SDK API Reference](../sdk/api-reference.md) - Complete SDK API documentation
- [SDK Examples](../sdk/examples.md) - Module development examples


