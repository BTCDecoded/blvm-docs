# Transaction relay

> **Experimental build** — Dandelion++ (`dandelion` feature) is not in stable release binaries. FIBRE is a loadable module (`blvm-fibre`). See [Installation — experimental variant](../getting-started/installation.md#experimental-variant).

## Overview

The node supports **Dandelion++** for privacy-preserving **transaction** relay (optional `dandelion` compile-time feature). **FIBRE** is **block** relay over UDP/FEC — provided by the loadable **`blvm-fibre`** module, not an in-node `[network.fibre]` table. See [FIBRE module](../modules/fibre.md). **Package relay (BIP331)** is documented in [Package Relay (BIP331)](package-relay.md).

Stable GitHub Release binaries use the **base** feature set (`production`); Dandelion++, CTV, Stratum V2, and related flags require an [experimental source build](../getting-started/installation.md#experimental-variant) or local `cargo build` with the matching features.

## Dandelion++ *(experimental build)*

Dandelion++ provides privacy-preserving transaction relay with formal anonymity guarantees against transaction origin analysis. It operates in two phases: stem phase (obscures origin) and fluff phase (standard diffusion).

**Requires:** `dandelion` Cargo feature in the binary ([experimental build](../getting-started/installation.md#experimental-variant)).

### Architecture

Dandelion++ operates in two phases:

1. **Stem Phase**: Transaction relayed along a random path (obscures origin)
2. **Fluff Phase**: Transaction broadcast to all peers (standard diffusion)

### Stem Path Management

Each peer maintains a stem path to a randomly selected peer:

```rust
pub struct StemPath {
    pub next_peer: String,
    pub expiry: Instant,
    pub hop_count: u8,
}
```


### Stem Phase Behavior

- Transactions relayed to next peer in stem path
- Random path selection obscures transaction origin
- Stem timeout: 10 seconds (default)
- Fluff probability: 10% per hop (default)
- Maximum stem hops: 2 (default)


### Fluff Phase Behavior

- Transaction broadcast to all peers
- Standard Bitcoin transaction diffusion
- Triggered by:
  - Random probability at each hop
  - Stem timeout expiration
  - Maximum hop count reached


### Configuration

Enable at runtime via **`[relay].enable_dandelion`** (or `--enable-dandelion` when the binary includes the feature). Tune stem/fluff under **`[dandelion]`**:

```toml
[relay]
enable_dandelion = true

[dandelion]
stem_timeout_seconds = 10
fluff_probability = 0.1   # 10%
max_stem_hops = 2
```


### Benefits

1. **Privacy**: Obscures transaction origin
2. **Formal Guarantees**: Anonymity guarantees against origin analysis
3. **Backward Compatible**: Falls back to standard relay if disabled
4. **Configurable**: Adjustable timeouts and probabilities

## FIBRE block relay (module)

FIBRE (Fast Internet Bitcoin Relay Engine) is **block** transport over UDP with FEC — not transaction propagation.

- **Operator path:** load **`blvm-fibre`** ([FIBRE module](../modules/fibre.md)) — outbound on `NewBlock` / `BlockMined`, inbound via `queue_received_block_bytes`.
- **Node support:** advertises **`NODE_FIBRE`** on P2P and publishes **`CompanionUdpPeerRegistered`** / **`CompanionUdpPeerUnregistered`** when peers advertise FIBRE (companion UDP = peer TCP port + 1) so the module can register dynamic peers.


There is **no** in-node `network/fibre.rs` or `[network.fibre]` configuration table.

## Integration

### Relay Manager

The `RelayManager` coordinates relay protocols:

- Standard block/transaction relay
- Dandelion++ integration (optional `dandelion` feature + `[relay].enable_dandelion`)
- Package relay (optional; see [Package Relay (BIP331)](package-relay.md))

FIBRE block relay runs in the **`blvm-fibre`** module process, not inside `RelayManager`.


### Protocol Selection

Relay protocols are selected based on:

- Compile-time features (`dandelion`, etc.)
- Peer capabilities
- Configuration settings
- Runtime preferences


## Components

- Dandelion++ stem/fluff phase management
- Relay manager coordination
- P2P `NODE_FIBRE` service bit and companion-UDP events for modules

## Source

- [network_manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/network_manager.rs) (companion UDP events), [blvm-fibre](https://github.com/BTCDecoded/blvm-fibre) (UDP/FEC relay)
- [relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/relay.rs)
- [blvm-node/src/network/dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs), [blvm-node/src/network/relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/relay.rs), [blvm-node/src/network/network_manager.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/network_manager.rs) (blvm-node/src/network/relay.rsblvm-node/src/network/network_manager.rs`)

