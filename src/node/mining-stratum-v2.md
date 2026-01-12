# Stratum V2 + Merge Mining

## Overview

Bitcoin Commons implements the Stratum V2 mining protocol with merge mining support, enabling efficient mining coordination and revenue generation through auxiliary chain mining. The system uses QUIC-based multiplexed channels for simultaneous mining of Bitcoin and secondary chains.

## Stratum V2 Protocol

### Protocol Features

- **Binary Protocol**: 50-66% bandwidth savings compared to Stratum V1
- **Encrypted Communication**: TLS/QUIC encryption for secure connections
- **Multiplexed Channels**: QUIC stream multiplexing for multiple mining streams
- **Template Distribution**: Efficient block template distribution
- **Share Submission**: Optimized share submission protocol

**Code**: ```1:45:blvm-node/src/network/stratum_v2/mod.rs```

### Message Encoding

Stratum V2 uses Tag-Length-Value (TLV) encoding:

```
[4-byte length][2-byte tag][4-byte length][payload]
```

**Code**: ```1:189:blvm-node/src/network/stratum_v2/protocol.rs```

### Transport Support

Stratum V2 works with both TCP and QUIC transports via the transport abstraction layer:

- **TCP**: Bitcoin P2P compatible
- **Quinn QUIC**: Direct QUIC transport
- **Iroh/QUIC**: QUIC with NAT traversal and DERP

**Code**: ```712:768:blvm-node/src/config/mod.rs```

## Merge Mining

### Overview

Merge mining enables simultaneous mining of Bitcoin and secondary chains (e.g., RSK, Namecoin) using the same proof-of-work. The system uses Stratum V2 multiplexed channels to coordinate mining across multiple chains.

### Architecture

```
┌─────────────────────────────────────┐
│      Stratum V2 Server              │
│  ┌───────────────────────────────┐ │
│  │  Merge Mining Coordinator     │ │
│  │  ┌──────────┐  ┌──────────┐  │ │
│  │  │ Bitcoin  │  │   RSK    │  │ │
│  │  │ Channel  │  │ Channel  │  │ │
│  │  └──────────┘  └──────────┘  │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
              │ QUIC Multiplexed
              │
┌─────────────┴─────────────────────┐
│         Miner Client              │
│  Simultaneous Mining              │
└───────────────────────────────────┘
```

### Merge Mining Coordinator

The `MergeMiningCoordinator` manages merge mining operations:

- Tracks secondary chains (RSK, Namecoin, etc.)
- Manages merge mining channels per chain
- Records rewards and shares per chain
- Calculates revenue distribution

**Code**: ```1:308:blvm-node/src/network/stratum_v2/merge_mining.rs```

### Secondary Chain Configuration

```rust
pub struct SecondaryChain {
    pub chain_id: String,      // e.g., "rsk", "namecoin"
    pub chain_name: String,
    pub enabled: bool,
}
```

**Code**: ```13:23:blvm-node/src/network/stratum_v2/merge_mining.rs```

### Merge Mining Channels

Each secondary chain uses a separate Stratum V2 channel:

```rust
pub struct MergeMiningChannel {
    pub chain_id: String,
    pub channel_id: u32,
    pub current_job_id: Option<u32>,
    pub total_rewards: u64,
    pub shares_submitted: u64,
}
```

**Code**: ```24:37:blvm-node/src/network/stratum_v2/merge_mining.rs```

## Revenue Distribution

### Distribution Model

Revenue from merge mining is distributed according to the whitepaper allocation:

- **60% Core Development**: Core Bitcoin Commons development
- **25% Grants**: Community grants and funding
- **10% Audits**: Security audits and formal verification
- **5% Operations**: Infrastructure and operations

**Code**: ```244:252:blvm-node/src/network/stratum_v2/merge_mining.rs```

### Revenue Tracking

The system tracks:
- Total revenue across all chains
- Revenue per individual chain
- Shares submitted per chain
- Fee collection (if enabled)

**Code**: ```192:227:blvm-node/src/network/stratum_v2/merge_mining.rs```

### Fee Configuration

Optional fee collection for merge mining revenue:

```rust
pub struct MergeMiningFeeConfig {
    pub enabled: bool,
    pub fee_percentage: u8,        // Default: 1%
    pub commons_address: Option<String>,
    pub contributor_id: Option<String>,
    pub auto_distribute: bool,
}
```

**Code**: ```738:759:blvm-node/src/config/mod.rs```

## Server Implementation

### StratumV2Server

The server accepts miner connections and coordinates mining operations:

- Accepts miner connections
- Distributes mining jobs
- Validates share submissions
- Coordinates merge mining channels

**Code**: ```1:311:blvm-node/src/network/stratum_v2/server.rs```

### Pool Implementation

The `StratumV2Pool` manages mining pool operations:

- Job distribution
- Share validation
- Channel management
- Connection pooling

**Code**: ```1:200:blvm-node/src/network/stratum_v2/pool.rs```

## Client Implementation

### StratumV2Miner

The miner client connects to pools and submits shares:

- Connection management
- Job reception
- Share submission
- Merge mining coordination

**Code**: ```1:200:blvm-node/src/network/stratum_v2/miner.rs```

### StratumV2Client

The client handles protocol communication:

- Message encoding/decoding
- Connection establishment
- Channel management
- Error handling

**Code**: ```1:200:blvm-node/src/network/stratum_v2/client.rs```

## Configuration

### StratumV2Config

```toml
[stratum_v2]
enabled = true
pool_url = "tcp://pool.example.com:3333"  # or "iroh://<nodeid>"
listen_addr = "0.0.0.0:3333"  # Server mode
merge_mining_enabled = true
secondary_chains = ["rsk", "namecoin"]

[stratum_v2.merge_mining_fee]
enabled = true
fee_percentage = 1
commons_address = "bc1q..."
contributor_id = "contributor-123"
auto_distribute = false
```

**Code**: ```712:768:blvm-node/src/config/mod.rs```

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
4. **Revenue Generation**: Merge mining enables sustainable funding
5. **Flexibility**: Support for multiple secondary chains
6. **Transport Choice**: Works with TCP or QUIC

## Components

The Stratum V2 system includes:
- Protocol encoding/decoding
- Server and client implementations
- Merge mining coordination
- Revenue distribution tracking
- QUIC multiplexed channels
- Transport abstraction support

**Location**: `blvm-node/src/network/stratum_v2/`

