# Transaction relay

## Overview

The node supports **Dandelion++** and **Fibre** for transaction propagation. **Package relay (BIP331)** is documented separately in [Package Relay (BIP331)](package-relay.md).

## Dandelion++

### Overview

Dandelion++ provides privacy-preserving transaction relay with formal anonymity guarantees against transaction origin analysis. It operates in two phases: stem phase (obscures origin) and fluff phase (standard diffusion).

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs)

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

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs)

### Stem Phase Behavior

- Transactions relayed to next peer in stem path
- Random path selection obscures transaction origin
- Stem timeout: 10 seconds (default)
- Fluff probability: 10% per hop (default)
- Maximum stem hops: 2 (default)

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs)

### Fluff Phase Behavior

- Transaction broadcast to all peers
- Standard Bitcoin transaction diffusion
- Triggered by:
  - Random probability at each hop
  - Stem timeout expiration
  - Maximum hop count reached

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs)

### Configuration

```toml
[network.dandelion]
enabled = true
stem_timeout_secs = 10
fluff_probability = 0.1  # 10%
max_stem_hops = 2
```

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs)

### Benefits

1. **Privacy**: Obscures transaction origin
2. **Formal Guarantees**: Anonymity guarantees against origin analysis
3. **Backward Compatible**: Falls back to standard relay if disabled
4. **Configurable**: Adjustable timeouts and probabilities

## Fibre

### Overview

Fibre (Fast Internet Bitcoin Relay Engine) provides high-performance block relay using UDP transport with Forward Error Correction (FEC) encoding for packet loss tolerance.

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs)

### Architecture

Fibre uses:
- **UDP Transport**: Low-latency UDP for block relay
- **FEC Encoding**: Reed-Solomon erasure coding for packet loss tolerance
- **Chunk-based Transmission**: Blocks split into chunks with parity shards
- **Automatic Recovery**: Missing chunks recovered via FEC

### FEC Encoding

Blocks are encoded using Reed-Solomon erasure coding:

- **Data Shards**: Original block data split into shards
- **Parity Shards**: Redundant shards for error recovery
- **Shard Size**: Configurable (default: 1024 bytes)
- **Parity Ratio**: Configurable (default: 0.2 = 20% parity)

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs)

### Block Encoding Process

1. Serialize block to bytes
2. Split into data shards
3. Generate parity shards via FEC
4. Create FEC chunks for transmission
5. Send chunks via UDP

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs)

### Block Assembly Process

1. Receive FEC chunks via UDP
2. Track received chunks per block
3. When enough chunks received (data shards), reconstruct block
4. Verify block hash matches

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs)

### UDP Transport

Fibre uses UDP for low-latency transmission:

- **Connection Tracking**: Per-peer connection state
- **Retry Logic**: Automatic retry for lost chunks
- **Sequence Numbers**: Duplicate detection
- **Timeout Handling**: Connection timeout management

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs)

### Configuration

```toml
[network.fibre]
enabled = true
bind_addr = "0.0.0.0:8334"
chunk_timeout_secs = 5
max_retries = 3
fec_parity_ratio = 0.2  # 20% parity
max_assemblies = 100
```

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs)

### Statistics

Fibre tracks per-peer and per-chunk statistics:

- Blocks sent/received
- Chunks sent/received
- FEC recoveries
- UDP errors
- Average latency
- Success rate

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs)

### Benefits

1. **Low Latency**: UDP transport reduces latency
2. **Packet Loss Tolerance**: FEC recovers from lost chunks
3. **High Throughput**: Efficient chunk-based transmission
4. **Automatic Recovery**: No manual retry needed

## Integration

### Relay Manager

The `RelayManager` coordinates relay protocols:

- Standard block/transaction relay
- Dandelion++ integration (optional)
- Fibre integration (optional)
- Package relay (optional; see [Package Relay (BIP331)](package-relay.md))

**Code**: [relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/relay.rs)

### Protocol Selection

Relay protocols are selected based on:

- Feature flags (`dandelion`, `fibre`)
- Peer capabilities
- Configuration settings
- Runtime preferences

**Code**: [relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/relay.rs)

## Components

- Dandelion++ stem/fluff phase management
- Fibre UDP transport with FEC encoding
- Relay manager coordination
- Statistics tracking

**Location**: `blvm-node/src/network/dandelion.rs`, `blvm-node/src/network/fibre.rs`, `blvm-node/src/network/relay.rs`

