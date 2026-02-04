# Privacy Relay Protocols

## Overview

Bitcoin Commons implements multiple privacy-preserving and performance-optimized transaction relay protocols: Dandelion++, Fibre, and Package Relay. These protocols improve privacy, reduce bandwidth, and enable efficient transaction propagation.

## Dandelion++

### Overview

Dandelion++ provides privacy-preserving transaction relay with formal anonymity guarantees against transaction origin analysis. It operates in two phases: stem phase (obscures origin) and fluff phase (standard diffusion).

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs#L1-L621)

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

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs#L37-L46)

### Stem Phase Behavior

- Transactions relayed to next peer in stem path
- Random path selection obscures transaction origin
- Stem timeout: 10 seconds (default)
- Fluff probability: 10% per hop (default)
- Maximum stem hops: 2 (default)

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs#L152-L200)

### Fluff Phase Behavior

- Transaction broadcast to all peers
- Standard Bitcoin transaction diffusion
- Triggered by:
  - Random probability at each hop
  - Stem timeout expiration
  - Maximum hop count reached

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs#L200-L300)

### Configuration

```toml
[network.dandelion]
enabled = true
stem_timeout_secs = 10
fluff_probability = 0.1  # 10%
max_stem_hops = 2
```

**Code**: [dandelion.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/dandelion.rs#L19-L35)

### Benefits

1. **Privacy**: Obscures transaction origin
2. **Formal Guarantees**: Anonymity guarantees against origin analysis
3. **Backward Compatible**: Falls back to standard relay if disabled
4. **Configurable**: Adjustable timeouts and probabilities

## Fibre

### Overview

Fibre (Fast Internet Bitcoin Relay Engine) provides high-performance block relay using UDP transport with Forward Error Correction (FEC) encoding for packet loss tolerance.

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs#L1-L1293)

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

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs#L65-L173)

### Block Encoding Process

1. Serialize block to bytes
2. Split into data shards
3. Generate parity shards via FEC
4. Create FEC chunks for transmission
5. Send chunks via UDP

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs#L617-L708)

### Block Assembly Process

1. Receive FEC chunks via UDP
2. Track received chunks per block
3. When enough chunks received (data shards), reconstruct block
4. Verify block hash matches

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs#L814-L946)

### UDP Transport

Fibre uses UDP for low-latency transmission:

- **Connection Tracking**: Per-peer connection state
- **Retry Logic**: Automatic retry for lost chunks
- **Sequence Numbers**: Duplicate detection
- **Timeout Handling**: Connection timeout management

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs#L216-L498)

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

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs#L506-L559)

### Statistics

Fibre tracks comprehensive statistics:

- Blocks sent/received
- Chunks sent/received
- FEC recoveries
- UDP errors
- Average latency
- Success rate

**Code**: [fibre.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/fibre.rs#L1011-L1040)

### Benefits

1. **Low Latency**: UDP transport reduces latency
2. **Packet Loss Tolerance**: FEC recovers from lost chunks
3. **High Throughput**: Efficient chunk-based transmission
4. **Automatic Recovery**: No manual retry needed

## Package Relay (BIP331)

### Overview

Package Relay (BIP331) allows nodes to relay and validate groups of transactions together, enabling efficient fee-bumping (RBF) and CPFP (Child Pays For Parent) scenarios.

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L1-L400)

### Package Structure

A transaction package contains:

- **Transactions**: Ordered list (parents before children)
- **Package ID**: Combined hash of all transactions
- **Combined Fee**: Sum of all transaction fees
- **Combined Weight**: Total weight for fee rate calculation

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L34-L45)

### Package Validation

Packages are validated for:

- **Size Limits**: Maximum 25 transactions (BIP331)
- **Weight Limits**: Maximum 404,000 WU (BIP331)
- **Fee Rate**: Minimum fee rate requirement
- **Ordering**: Parents must precede children
- **No Duplicates**: No duplicate transactions

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L86-L250)

### Use Cases

1. **Fee-Bumping (RBF)**: Parent + child transaction for fee increase
2. **CPFP**: Child transaction pays for parent's fees
3. **Atomic Sets**: Multiple transactions that must be accepted together

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L1-L15)

### Package ID Calculation

Package ID is calculated as double SHA256 of all transaction IDs:

```rust
pub fn from_transactions(transactions: &[Transaction]) -> PackageId {
    // Hash all txids, then double hash
}
```

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L107-L134)

### Configuration

```toml
[network.package_relay]
enabled = true
max_package_size = 25
max_package_weight = 404000  # 404k WU
min_fee_rate = 1000  # 1 sat/vB
```

**Code**: [package_relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/package_relay.rs#L86-L105)

### Benefits

1. **Efficient Fee-Bumping**: Better fee rate calculation for packages
2. **Reduced Orphans**: Reduces orphan transactions in mempool
3. **Atomic Validation**: Package validated as unit
4. **DoS Resistance**: Size and weight limits prevent abuse

## Integration

### Relay Manager

The `RelayManager` coordinates all relay protocols:

- Standard block/transaction relay
- Dandelion++ integration (optional)
- Fibre integration (optional)
- Package relay support

**Code**: [relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/relay.rs#L1-L390)

### Protocol Selection

Relay protocols are selected based on:

- Feature flags (`dandelion`, `fibre`)
- Peer capabilities
- Configuration settings
- Runtime preferences

**Code**: [relay.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/relay.rs#L67-L129)

## Components

The privacy relay system includes:
- Dandelion++ stem/fluff phase management
- Fibre UDP transport with FEC encoding
- Package Relay (BIP331) validation
- Relay manager coordination
- Statistics tracking

**Location**: `blvm-node/src/network/dandelion.rs`, `blvm-node/src/network/fibre.rs`, `blvm-node/src/network/package_relay.rs`, `blvm-node/src/network/relay.rs`

