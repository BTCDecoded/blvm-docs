# Lightning Network Module

> **Registry status:** Not listed in [`registry/modules.json`](https://github.com/BTCDecoded/blvm/blob/main/registry/modules.json). `[modules]` registry bootstrap cannot download `blvm-lightning`; [build it from source](overview.md#build-from-source) and place it under `modules_dir`.

## Overview

The Lightning Network module (`blvm-lightning`) handles invoice verification and payment state for blvm-node. LNBits talks to an external wallet. The LDK provider keeps a channel manager inside the module process.

## Features

- **Invoice Verification**: Validates Lightning Network invoices (BOLT11) using multiple provider backends
- **Payment Processing**: LNBits sends and receives on the network. LDK registers invoices with its own channel manager and reports a payment only after LDK says it is claimable.
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
- External Lightning backend for payments that move on the network: **LNBits** (HTTP API). **LDK** runs inside the module, listens and dials when configured, and opens a channel from coins that pay its deposit address. **Stub** is for tests only.
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

### LDK Provider

```toml
provider = "ldk"

[ldk]
network = "testnet"  # mainnet, testnet, signet, or regtest
node_private_key = "hex_encoded_32_byte_seed"  # optional; generated and stored when unset
listen_port = 9735   # optional; unset means do not listen
peers = ["02pubkeyhex@127.0.0.1:9735"]  # optional, pubkey@host:port
```

`node_private_key` is the LDK seed. LDK derives the node id from that seed. The module stores it at `<data_dir>/ldk/seed`. A configured seed that does not match the stored seed refuses to start.

What this provider does:

- Builds an LDK 0.0.125 `ChannelManager` and `ChainMonitor` in the module process.
- `create_invoice` registers the payment with that manager, adds a route hint for each usable private channel, and returns a BOLT11 invoice signed by the node key. Received HTLCs are forwarded when LDK reports them ready, and a claimable invoice payment is claimed.
- `verify_payment` is true only after LDK emits `PaymentClaimable` or `PaymentClaimed`.
- Anchors a genesis manager that has no channels at the node tip. Any other manager connects each missing block in order. `BlockDisconnected` applies when it is the LDK tip.
- Submits broadcasts to the node mempool and appends them to `<data_dir>/ldk/broadcasts.log`.
- Listens on `listen_port` and dials `peers`. `max_inbound_sats` caps an inbound channel. When it is unset, inbound opens are rejected. `pay_invoice` returns when LDK queues the send. `PaymentRouteFound` follows the path LDK used. `PaymentVerified` carries the payment amount. No route is an error.
- Persists `ldk/network_graph`, `ldk/scorer`, `ldk/payments.json`, and `ldk/funding.json`.
- `deposit-address` is the P2WPKH address for the LDK seed's on-chain key. `open-channel` spends `txid:vout` coins that pay that address once the peer accepts, and submits the funding transaction to the node. The reserved coins are stored in `<data_dir>/ldk/funding.json` so a restart can still sign that transaction. Change and swept channel outputs return to the same address.

What it does not do:

- Invent a second wallet. On-chain coins must already pay the deposit address. A peer can also open a channel to a listening node.
- Hold mainnet channel funds. That stays out of scope until a restart and a reorg deeper than the LDK tip are in the test record. A queued `pay_invoice` is not a settled payment.

LNBits is the provider that pays through an external wallet.

### Stub Provider (Testing, default)

```toml
provider = "stub"
```

When `provider` is omitted, the default is **`stub`** (safe for local dev; no real Lightning).

### Global limits (all providers)

```toml
provider = "lnbits"
min_payment_sats = 1000      # optional; create_invoice rejects a smaller amount
max_payment_sats = 1000000   # optional; create_invoice rejects a larger amount
```

### Configuration options

- `provider`: `"lnbits"`, `"ldk"`, or `"stub"` (default **`stub`**)
- `min_payment_sats` / `max_payment_sats`: optional satoshi bounds. Absent means `create_invoice` has no bound. The amount argument is millisatoshis.
- **LNBits** (`[lnbits]`): `api_url`, `api_key`, `wallet_id` (optional). File only.
- **LDK** (`[ldk]`): `network` (`mainnet`, `testnet`, `signet`, or `regtest`; default `testnet`), `node_private_key` (optional 32-byte hex seed), `listen_port` (optional), `peers` (optional `pubkey@host:port` list), `max_inbound_sats` (optional; absent rejects inbound channels). File only.
- **Stub**: no extra keys

### Provider Comparison

| Feature | LNBits | LDK | Stub |
|---------|--------|-----|------|
| **Status** | Operational (REST) | Channel manager, node chain, optional peers | Stub / dev |
| **API Type** | REST (HTTP) | LDK 0.0.125 `ChannelManager` | None |
| **Pays and receives on the network** | Yes | When a peer and a route exist | No |
| **External Service** | Yes | No | No |
| **Invoice Creation** | Via API | Registered with the channel manager | Mock |
| **Payment Verification** | Via API | True only after an LDK claim event | Mock, always true |
| **Best For** | Payment processing | A channel manager inside the module | Testing |

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
    "read_chain_state",
    "read_utxo",
    "read_mempool",
    "send_transactions",
    "subscribe_events",
    "publish_events",
]
```

Shipped **`version`** is in each release’s `module.toml` and **`registry/modules.json`** — do not hardcode it in the book.

## Events

### Subscribed events

Via `#[on_event(...)]` in the module:

- `PaymentRequestCreated`
- `PaymentSettled`
- `PaymentFailed`
- `NewBlock`
- `BlockDisconnected`

### Published events

`LightningProcessor` may publish (depending on provider path):

- `PaymentRequestCreated` — new invoice / payment request
- `PaymentVerified` — Lightning payment verified
- `PaymentSettled` — on-chain settlement observed (when applicable)
- `PaymentFailed` — verification or payment failed
- `PaymentRouteFound` / `PaymentRouteFailed` — outgoing payment routing
- `ChannelClosed` — channel close notification

`ChannelOpened` is published when LDK reports the channel ready.

## Usage

Once installed and configured, the module automatically:

1. Subscribes to payment and chain events from the node (`PaymentRequestCreated`, `PaymentSettled`, `PaymentFailed`, `NewBlock`, `BlockDisconnected`)
2. Verifies Lightning invoices (BOLT11) when payment requests are created
3. Asks the configured provider to verify the payment. LNBits checks its wallet. LDK reports a payment only after a claim event. Stub always reports success. The LDK provider also advances its chain tip from `NewBlock`.
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
| LDK errors | `network` is mainnet, testnet, signet, or regtest. `node_private_key`, when set, is 32 bytes of hex and matches `<data_dir>/ldk/seed`. `peers` entries are `pubkey@host:port`. `pay_invoice` fails when LDK has no route. A missing block between the LDK tip and the node tip stops sync. |
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


