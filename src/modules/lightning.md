# Lightning Network Module

## Overview

The Lightning Network module (`blvm-lightning`) handles invoice verification, payment routing, channel management, and payment state tracking for blvm-node.

## Features

- **Invoice Verification**: Validates Lightning Network invoices (BOLT11) using multiple provider backends
- **Payment Processing**: Processes Lightning payments via LNBits API or LDK
- **Provider Abstraction**: Supports multiple Lightning providers (LNBits, LDK, Stub) through one interface
- **Payment State Tracking**: Monitors payment lifecycle from request to settlement

## Installation

### Via Cargo

```bash
cargo install blvm-lightning
```

When the crate is not on crates.io, use [registry bootstrap](overview.md#installing-modules) or build from the GitHub repository.

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
   cp module.toml /path/to/node/modules/blvm-lightning/
   ```

## Requirements

- `blvm-node` with the module system enabled.
- External Lightning backend for real payments: **LNBits** (HTTP API) or **LDK** (embedded). **Stub** is for tests only.
- Secrets (`api_key`, `node_private_key`) in module config — never commit to git.

## Loading

Pin in `blvm.toml`:

```toml
[modules]
registry_url = "https://raw.githubusercontent.com/BTCDecoded/blvm/main/registry/modules.json"
blvm-lightning = "0.1.*"
```

Module config: `<modules.data_dir>/blvm-lightning/config.toml` (same schema as examples below). See [Installing modules](overview.md#installing-modules).

## Configuration

The module supports multiple Lightning providers. Create a `config.toml` file in the module directory with **flat top-level keys** (no `[lightning]` wrapper — invalid tables are **silently ignored** and the module falls back to **`stub`**):

### LNBits Provider (Recommended)

```toml
provider = "lnbits"

[lnbits]
api_url = "https://lnbits.example.com"
api_key = "your_lnbits_api_key"
wallet_id = "optional_wallet_id"  # Optional
```

### LDK Provider (Rust-native)

```toml
provider = "ldk"

[ldk]
network = "testnet"  # or "mainnet" or "regtest"
node_private_key = "hex_encoded_private_key"  # optional; generated when unset
```

### Stub Provider (Testing, default)

```toml
provider = "stub"
```

When `provider` is omitted, the default is **`stub`** (safe for local dev; no real Lightning).

### Global limits (all providers)

```toml
provider = "lnbits"
min_payment_sats = 1000      # optional; enforced in create_invoice
max_payment_sats = 1000000   # optional
channel_reserve = 10000      # optional; LDK channel reserve in sats
```

### Configuration options

- `provider`: `"lnbits"`, `"ldk"`, or `"stub"` (default **`stub`**)
- **LNBits** (`[lnbits]`): `api_url`, `api_key`, `wallet_id` (optional)
- **LDK** (`[ldk]`): `network` (default `testnet`), `node_private_key` (optional)
- **Stub**: no extra keys

### Provider Comparison

| Feature | LNBits | LDK | Stub |
|---------|--------|-----|------|
| **Status** | Operational (REST) | Operational (Rust/LDK) | Stub / dev |
| **API Type** | REST (HTTP) | Rust-native (lightning-invoice) | None |
| **Real Lightning** | ✅ Yes | ✅ Yes | ❌ No |
| **External Service** | ✅ Yes | ❌ No | ❌ No |
| **Invoice Creation** | ✅ Via API | ✅ Native | ✅ Mock |
| **Payment Verification** | ✅ Via API | ✅ Native | ✅ Mock |
| **Best For** | Payment processing | Full control, Rust-native | Testing |

**Switching Providers**: All providers implement the same interface, so switching providers is just a configuration change. No code changes required.

## Module Manifest

The module includes a `module.toml` manifest (see [Building modules](../sdk/module-development.md#module-manifest)):

```toml
name = "blvm-lightning"
description = "Lightning Network payment processor module for blvm-node"
author = "Bitcoin Commons Team"
entry_point = "blvm-lightning"

capabilities = [
    "read_blockchain",
    "subscribe_events",
]
```

Shipped **`version`** is in each release’s `module.toml` and **`registry/modules.json`** — do not hardcode it in the book.

## Events

### Subscribed events

Via `#[on_event(...)]` in the module:

- `PaymentRequestCreated`
- `PaymentSettled`
- `PaymentFailed`

### Published events

`LightningProcessor` may publish (depending on provider path):

- `PaymentRequestCreated` — new invoice / payment request
- `PaymentVerified` — Lightning payment verified
- `PaymentSettled` — on-chain settlement observed (when applicable)
- `PaymentFailed` — verification or payment failed
- `PaymentRouteFound` / `PaymentRouteFailed` — outgoing payment routing
- `ChannelClosed` — channel close notification

`ChannelOpened` exists on the shared `EventType` enum but is **not emitted** by this module today.

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

### Batch Payment Verification

The module supports batch payment verification for improved performance when processing multiple payments:

```rust
use blvm_lightning::processor::LightningProcessor;

// Verify multiple payments in parallel
let payments = vec![
    ("invoice1", "payment_id_1"),
    ("invoice2", "payment_id_2"),
    ("invoice3", "payment_id_3"),
];

let results = processor.verify_payments_batch(&payments).await?;
// Returns Vec<bool> with verification results in same order as inputs
```

Batch verification processes all payments concurrently, significantly improving throughput for high-volume payment processing scenarios.

## API Integration

The module integrates with the node via `ModuleClient` and `NodeApiIpc`:

- **Read-only blockchain access**: Queries blockchain data for payment verification
- **Event subscription**: Receives real-time events from the node
- **Event publication**: Publishes Lightning-specific events
- **Module storage**: Stores provider configuration and channel statistics in module storage tree `lightning_config`

### Storage Usage

The module uses module storage to persist configuration and statistics:
- `provider_type`: Current provider type (lnbits, ldk, stub)
- `channel_count`: Number of active Lightning channels
- `total_capacity_sats`: Total channel capacity in satoshis

## Troubleshooting

| Symptom | Check |
|---------|--------|
| Module not loading | Binary at `target/release/blvm-lightning`; valid `module.toml`; node logs |
| LNBits errors | `api_url`, `api_key`; HTTPS reachability |
| LDK errors | `network` matches node; optional `node_private_key` valid hex |
| No payment events | Node publishes `PaymentRequestCreated`; provider not `stub` for real traffic |

## Repository

- **GitHub**: [blvm-lightning](https://github.com/BTCDecoded/blvm-lightning) — releases and current `module.toml` **`version`**

## See Also

- [Module catalog](overview.md) - Overview of all available modules
- [Module System Architecture](../architecture/module-system.md) - Detailed module system documentation
- [Building modules](../sdk/module-development.md) - Guide for developing custom modules
- [SDK Overview](../sdk/overview.md) - SDK introduction and capabilities
- [SDK API Reference](../sdk/api-reference.md) - Complete SDK API documentation
- [SDK Examples](../sdk/examples.md) - Module development examples


