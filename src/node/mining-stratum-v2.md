# Stratum V2 Mining Protocol

## Overview

Bitcoin Commons implements the Stratum V2 mining protocol, enabling efficient mining coordination. **Merge mining is available as a separate paid plugin module** (`blvm-merge-mining`) that integrates with Stratum V2.

## Stratum V2 Protocol

### Protocol Features

- **Binary Protocol**: 50-66% bandwidth savings compared to Stratum V1
- **Encrypted Communication**: TLS/QUIC encryption for secure connections
- **Multiplexed Channels**: QUIC stream multiplexing for multiple mining streams
- **Template Distribution**: Efficient block template distribution
- **Share Submission**: Optimized share submission protocol

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/stratum_v2/mod.rs#L1-L45)

### Message Encoding

Stratum V2 uses Tag-Length-Value (TLV) encoding:

```
[4-byte length][2-byte tag][4-byte length][payload]
```

**Code**: [protocol.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/stratum_v2/protocol.rs#L1-L189)

### Transport Support

Stratum V2 works with both TCP and QUIC transports via the transport abstraction layer:

- **TCP**: Bitcoin P2P compatible
- **Quinn QUIC**: Direct QUIC transport
- **Iroh/QUIC**: QUIC with NAT traversal and DERP

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs#L712-L768)

## Merge Mining (Optional Plugin)

### Overview

**Merge mining is NOT built into the core node.** It is available as a **separate, optional paid plugin module** (`blvm-merge-mining`) that integrates with the Stratum V2 module.

### Key Points

- **Separate Module**: `blvm-merge-mining` is not part of the core node
- **Requires Stratum V2**: The merge mining module depends on `blvm-stratum-v2` module
- **One-Time Activation Fee**: 100,000 sats (0.001 BTC) required to activate
- **Revenue Model**: Module developer receives a fixed percentage (default 5%) of merge mining rewards
- **Not a Commons Funding Model**: Merge mining revenue goes to the module developer, not to Commons infrastructure

### Installation

To use merge mining:

1. **Install Stratum V2 module** (required dependency)
2. **Install merge mining module**: `blvm-merge-mining`
3. **Pay activation fee**: 100,000 sats one-time payment
4. **Configure**: Set up secondary chains and revenue share

### Documentation

For complete merge mining documentation, see:
- [blvm-merge-mining README](../../blvm-merge-mining/README.md) - Module documentation
- [Module System](../modules/overview.md) - How modules work

## Server Implementation

### StratumV2Server

The server accepts miner connections and coordinates mining operations:

- Accepts miner connections
- Distributes mining jobs
- Validates share submissions
- Coordinates merge mining channels

**Code**: [server.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/stratum_v2/server.rs#L1-L311)

### Pool Implementation

The `StratumV2Pool` manages mining pool operations:

- Job distribution
- Share validation
- Channel management
- Connection pooling

**Code**: [pool.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/stratum_v2/pool.rs#L1-L200)

## Client Implementation

### StratumV2Miner

The miner client connects to pools and submits shares:

- Connection management
- Job reception
- Share submission

**Code**: [miner.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/stratum_v2/miner.rs#L1-L200)

### StratumV2Client

The client handles protocol communication:

- Message encoding/decoding
- Connection establishment
- Channel management
- Error handling

**Code**: [client.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/network/stratum_v2/client.rs#L1-L200)

## Configuration

### StratumV2Config

```toml
[stratum_v2]
enabled = true
pool_url = "tcp://pool.example.com:3333"  # or "iroh://<nodeid>"
listen_addr = "0.0.0.0:3333"  # Server mode
```

**Note**: Merge mining configuration is handled by the `blvm-merge-mining` module, not in Stratum V2 config.

**Code**: [mod.rs](https://github.com/BTCDecoded/blvm-node/blob/main/src/config/mod.rs#L712-L768)

## Usage

### Server Mode

```rust
use blvm_node::network::stratum_v2::StratumV2Server;

let server = StratumV2Server::new(
    network_manager,
    mining_coordinator,
    listen_addr,
);

server.start().await?;
```

### Miner Mode

```rust
use blvm_node::network::stratum_v2::StratumV2Miner;

let miner = StratumV2Miner::new(pool_url);
miner.connect().await?;
miner.start_mining().await?;
```

## Benefits

1. **Bandwidth Efficiency**: 50-66% bandwidth savings vs Stratum V1
2. **Security**: Encrypted communication via TLS/QUIC
3. **Efficiency**: Multiplexed channels for simultaneous mining
4. **Flexibility**: Support for multiple mining streams
5. **Transport Choice**: Works with TCP or QUIC

## Components

The Stratum V2 system includes:
- Protocol encoding/decoding
- Server and client implementations
- QUIC multiplexed channels
- Transport abstraction support

**Location**: `blvm-node/src/network/stratum_v2/`

**Note**: Merge mining functionality is provided by the separate `blvm-merge-mining` module, not by the core Stratum V2 implementation.

