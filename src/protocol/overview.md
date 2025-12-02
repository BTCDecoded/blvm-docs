# Protocol Layer Overview

The protocol layer (`bllvm-protocol`) abstracts Bitcoin protocol for multiple variants and protocol evolution. It sits between the pure mathematical consensus rules ([bllvm-consensus](../consensus/overview.md)) and the Bitcoin node implementation ([bllvm-node](../node/overview.md)), supporting mainnet, testnet, regtest, and future protocol variants.

## Architecture Position

Tier 3 of the 6-tier Bitcoin Commons architecture:

```
1. Orange Paper (mathematical foundation)
2. bllvm-consensus (pure math implementation)
3. bllvm-protocol (Bitcoin abstraction) ← THIS LAYER
4. bllvm-node (full node implementation)
5. bllvm-sdk (developer toolkit)
6. bllvm-commons (governance enforcement)
```

## Protocol Variants

The protocol layer supports multiple Bitcoin network variants:

| Variant | Network Name | Default Port | Purpose |
|---------|--------------|--------------|---------|
| **BitcoinV1** | mainnet | 8333 | Production Bitcoin network |
| **Testnet3** | testnet | 18333 | Bitcoin test network |
| **Regtest** | regtest | 18444 | Regression testing network |

### Network Parameters

Each variant has specific network parameters:

- **Magic Bytes**: P2P protocol identification (mainnet: `0xf9beb4d9`, testnet: `0x0b110907`, regtest: `0xfabfb5da`)
- **Genesis Blocks**: Network-specific genesis block hashes
- **Difficulty Targets**: Proof-of-work difficulty adjustment
- **Halving Intervals**: Block subsidy halving schedule (210,000 blocks)
- **Feature Activation**: [SegWit](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki), [Taproot](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) activation heights

**Code**: ```1:100:bllvm-protocol/src/network_params.rs```

## Core Components

### Protocol Engine

The `BitcoinProtocolEngine` is the main interface:

```rust
pub struct BitcoinProtocolEngine {
    version: ProtocolVersion,
    network_params: NetworkParams,
    config: ProtocolConfig,
}
```

**Features**:
- Protocol variant selection
- Network parameter access
- Feature flag management
- Validation rule enforcement

**Code**: ```1:200:bllvm-protocol/src/lib.rs```

### Network Messages

Supports Bitcoin P2P protocol messages:

**Core Messages**:
- `Version`, `VerAck` - Connection handshake
- `Addr`, `GetAddr` - Peer address management
- `Inv`, `GetData`, `NotFound` - Inventory management
- `Block`, `Tx` - Block and transaction relay
- `GetHeaders`, `Headers`, `GetBlocks` - Header synchronization
- `Ping`, `Pong` - Connection keepalive
- `MemPool`, `FeeFilter` - Mempool synchronization

**BIP152 (Compact Block Relay)**:
- `SendCmpct` - Compact block negotiation
- `CmpctBlock` - Compact block transmission
- `GetBlockTxn`, `BlockTxn` - Transaction reconstruction

**Commons Extensions**:
- `GetUTXOSet`, `UTXOSet` - [UTXO commitment protocol](../consensus/utxo-commitments.md)
- `GetFilteredBlock`, `FilteredBlock` - Spam-filtered blocks
- `GetBanList`, `BanList` - Distributed ban list sharing

**Code**: ```1:500:bllvm-protocol/src/network/messages.rs```

### Service Flags

Service flags indicate node capabilities:

**Standard Flags**:
- `NODE_NETWORK` - Full node with all blocks
- `NODE_WITNESS` - SegWit support
- `NODE_COMPACT_FILTERS` - BIP157/158 support
- `NODE_NETWORK_LIMITED` - Pruned node

**Commons Flags**:
- `NODE_UTXO_COMMITMENTS` - UTXO commitment support
- `NODE_BAN_LIST_SHARING` - Ban list sharing
- `NODE_FIBRE` - FIBRE protocol support
- `NODE_DANDELION` - Dandelion++ privacy relay
- `NODE_PACKAGE_RELAY` - BIP331 package relay

**Code**: ```1:200:bllvm-protocol/src/service_flags/mod.rs```

### Validation Rules

Protocol-specific validation rules:

- **Size Limits**: Block (4MB), transaction (1MB), script (10KB)
- **Feature Flags**: [SegWit](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki), [Taproot](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki), RBF support
- **Fee Rules**: Minimum and maximum fee rates
- **DoS Protection**: Message size limits, address count limits

**Code**: ```1:300:bllvm-protocol/src/validation/mod.rs```

## Commons-Specific Extensions

### UTXO Commitments

Protocol messages for [UTXO set synchronization](../consensus/utxo-commitments.md):

- `GetUTXOSet` - Request UTXO set at specific height
- `UTXOSet` - UTXO set response with merkle proof

**Code**: ```1:200:bllvm-protocol/src/commons/utxo_commitments.rs```

### Filtered Blocks

Spam-filtered block relay for efficient syncing:

- `GetFilteredBlock` - Request filtered block
- `FilteredBlock` - Filtered block with spam transactions removed

**Code**: ```1:200:bllvm-protocol/src/commons/filtered_blocks.rs```

### Ban List Sharing

Distributed ban list management:

- `GetBanList` - Request ban list
- `BanList` - Ban list response with signatures

**Code**: ```1:200:bllvm-protocol/src/commons/ban_list.rs```

## BIP Support

Implemented Bitcoin Improvement Proposals:

- **BIP152**: Compact Block Relay
- **BIP157**: Client-side Block Filtering
- **BIP158**: Compact Block Filters
- **BIP173/350/351**: Bech32/Bech32m Address Encoding
- **BIP70**: Payment Protocol

**Code**: ```1:200:bllvm-protocol/src/bip157/mod.rs```

## Protocol Evolution

The protocol layer supports protocol evolution:

- **Version Support**: Multiple protocol versions
- **Feature Management**: Enable/disable features based on version
- **Breaking Changes**: Track and manage protocol evolution
- **Backward Compatibility**: Maintain compatibility with existing nodes

## Usage Example

```rust
use bllvm_protocol::{BitcoinProtocolEngine, ProtocolVersion};

// Create a mainnet protocol engine
let engine = BitcoinProtocolEngine::new(ProtocolVersion::BitcoinV1)?;

// Get network parameters
let params = engine.get_network_params();
println!("Network: {}", params.network_name);
println!("Port: {}", params.default_port);

// Check feature support
if engine.supports_feature("segwit") {
    println!("SegWit is supported");
}
```

## See Also

- [Protocol Architecture](architecture.md) - Protocol layer design and components
- [Network Protocol](network-protocol.md) - Transport abstraction and protocol details
- [Message Formats](message-formats.md) - P2P message specifications
- [Protocol Specifications](../reference/protocol-specifications.md) - BIP implementations
- [Node Configuration](../node/configuration.md) - Configuring protocol variants

